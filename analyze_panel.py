"""Panel analysis: TB incidence vs lagged GP prescribing across upper-tier local authorities
in England, 2014-2024.

Outcome:  3-year TB notification counts (Fingertips 91361) for rolling windows ending in year t.
Exposure: mean annual items per 1,000 residents over a window defined relative to t (primary:
          the 3 years immediately before the outcome window, t-5..t-3).
Model:    Poisson pseudo-maximum likelihood with UTLA and window fixed effects, log population
          offset, cluster-robust SEs by UTLA (overlapping windows => serial correlation).
          Coefficient on log(prescribing rate) => IRR for a 10% within-area increase.

Fixed effects remove time-invariant area confounding (country-of-birth mix, deprivation,
geography) but not time-varying confounding; time-varying covariates, a lead (future exposure)
falsification test and positive/negative control exposures are included for that reason.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

from build_dataset import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
PANEL = ROOT / "data" / "processed" / "utla_panel_annual.csv"
OUT = ROOT / "outputs" / "panel"
OUT.mkdir(parents=True, exist_ok=True)

TIME_VARYING = ["pct_age_65plus", "pct_age_15_44", "intl_in_per_1000", "hiv_prev", "diabetes_prev"]

# exposure window (first, last year) relative to the outcome window's end year t
EXPOSURE_WINDOWS = {
    "primary: t-5..t-3": (-5, -3),
    "lag: t-3 only": (-3, -3),
    "concurrent: t-2..t": (-2, 0),
    "lead (falsification): t+1..t+3": (1, 3),
}


def window_mean(annual, cols, first, last):
    """Mean of annual values over [t+first, t+last] for each area and outcome year t."""
    frames = []
    for t in sorted(annual.year.unique()):
        sub = annual[annual.year.between(t + first, t + last)].dropna(subset=cols)
        n_years = sub.groupby("utla").year.nunique()
        m = sub.groupby("utla")[cols].mean()[n_years == last - first + 1]
        frames.append(m.assign(window_end=t))
    return pd.concat(frames).reset_index()


def log_rate(s):
    floor = s[s > 0].min() / 2
    return np.log(s.clip(lower=floor))


def fit_ppml(df, exposure, covars):
    X = pd.DataFrame({"log_exposure": log_rate(df[exposure])}, index=df.index)
    for c in covars:
        X[c] = df[c]
    X = X.join(pd.get_dummies(df.utla, prefix="a", drop_first=True, dtype=float))
    X = X.join(pd.get_dummies(df.window_end, prefix="t", drop_first=True, dtype=float))
    X = sm.add_constant(X)
    model = sm.GLM(df.tb_count, X, family=sm.families.Poisson(), offset=np.log(df.tb_denominator))
    return model.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.utla)[0]}, maxiter=200)


def summarise(res, **meta):
    b, se = res.params["log_exposure"], res.bse["log_exposure"]
    k = np.log(1.1)
    return dict(**meta, irr_10pct=np.exp(b * k), ci_low=np.exp((b - 1.96 * se) * k),
                ci_high=np.exp((b + 1.96 * se) * k), p=res.pvalues["log_exposure"], n_obs=int(res.nobs))


def main():
    panel = pd.read_csv(PANEL)
    annual_cols = [f"rate_{d}" for d in DRUG_GROUPS] + ["rate_total_items"]
    annual = panel[["utla", "year"] + annual_cols + TIME_VARYING]
    tb = panel.dropna(subset=["tb_count", "tb_denominator"])[["utla", "year", "tb_count", "tb_denominator"]]
    tb = tb.rename(columns={"year": "window_end"})

    rows = []
    for window_label, (first, last) in EXPOSURE_WINDOWS.items():
        expo = window_mean(annual, annual_cols, first, last)
        # confounders of TB measured over the outcome window; migration also over the exposure window
        cov = window_mean(annual, TIME_VARYING, -2, 0)
        mig = window_mean(annual, ["intl_in_per_1000"], first, last).rename(
            columns={"intl_in_per_1000": "intl_in_exposure_window"})
        df = (tb.merge(expo, on=["utla", "window_end"]).merge(cov, on=["utla", "window_end"])
              .merge(mig, on=["utla", "window_end"]))
        df = df.dropna()
        # (identical to intl_in_per_1000 when the exposure window is the outcome window)
        covars = TIME_VARYING + (["intl_in_exposure_window"] if (first, last) != (-2, 0) else [])
        specs = {"FE only": [], "FE + time-varying": covars}
        if window_label.startswith("primary"):
            specs["FE + time-varying + total prescribing"] = covars + ["log_total"]
            df["log_total"] = log_rate(df.rate_total_items)
        print(f"{window_label}: {len(df)} area-windows, {df.utla.nunique()} UTLAs, "
              f"windows ending {df.window_end.min()}-{df.window_end.max()}")
        for drug in DRUG_GROUPS:
            for spec_label, covars in specs.items():
                res = fit_ppml(df, f"rate_{drug}", covars)
                rows.append(summarise(res, drug=drug, exposure_window=window_label, model=spec_label,
                                      converged=res.converged))

    out = pd.DataFrame(rows)
    primary = (out.exposure_window == "primary: t-5..t-3") & (out.model == "FE + time-varying")
    out.loc[primary, "q_fdr"] = multipletests(out.loc[primary, "p"], method="fdr_bh")[1]
    out.to_csv(OUT / "panel_results.csv", index=False)

    fmt = out.assign(est=out.apply(lambda r: f"{r.irr_10pct:.3f} ({r.ci_low:.3f}-{r.ci_high:.3f})", axis=1))
    for window_label in EXPOSURE_WINDOWS:
        w = fmt[fmt.exposure_window == window_label].pivot(index="drug", columns="model", values="est")
        print(f"\nIRR per 10% within-area increase in prescribing — exposure {window_label}")
        print(w.loc[list(DRUG_GROUPS)].to_string())
    print("\nPrimary model p / FDR q:")
    print(out[primary][["drug", "p", "q_fdr", "converged"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
