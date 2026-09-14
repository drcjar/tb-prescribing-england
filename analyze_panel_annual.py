"""Annual panel: TB notifications by local authority and calendar year (UKHSA regional reports,
2001-2024) vs GP prescribing 2014-2024, at UTLA or LTLA level. Same estimator as analyze_panel.py
(Poisson PML, area + year fixed effects, ONS population offset, SEs clustered by area), with
exposure windows defined relative to the outcome year t.

Usage: python analyze_panel_annual.py [utla|ltla]
"""
import sys
from pathlib import Path

import pandas as pd
from statsmodels.stats.multitest import multipletests

from analyze_panel import TIME_VARYING, fit_ppml, log_rate, summarise, window_mean
from build_dataset import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
OUT_DIRS = {"utla": ROOT / "outputs" / "panel_annual", "ltla": ROOT / "outputs" / "panel_annual_ltla"}
ANNUAL_COLS = [f"rate_{d}" for d in DRUG_GROUPS] + ["rate_total_items"]

EXPOSURE_WINDOWS = {
    "primary: t-3..t-1": (-3, -1),
    "lag: t-1 only": (-1, -1),
    "concurrent: t": (0, 0),
    "lead (falsification): t+1..t+3": (1, 3),
}


def build_frame(level, first, last):
    """Analysis frame for one exposure window: TB outcome, exposures and covariates by area-year."""
    panel = pd.read_csv(PROCESSED / f"{level}_panel_annual.csv")
    tb = pd.read_csv(PROCESSED / f"{level}_tb_annual.csv")
    tb = tb.merge(panel[["utla", "year", "population"]], on=["utla", "year"]).dropna()
    tb = tb.rename(columns={"year": "window_end", "population": "tb_denominator"})
    annual = panel[["utla", "year"] + ANNUAL_COLS + TIME_VARYING + ["asylum_per_1000"]]

    expo = window_mean(annual, ANNUAL_COLS, first, last)
    cov = window_mean(annual, TIME_VARYING, 0, 0)
    asylum = window_mean(annual, ["asylum_per_1000"], 0, 0)
    tb = tb.merge(asylum, on=["utla", "window_end"], how="left")
    df = tb.merge(expo, on=["utla", "window_end"]).merge(cov, on=["utla", "window_end"])
    covars = list(TIME_VARYING)
    if (first, last) != (0, 0):
        mig = window_mean(annual, ["intl_in_per_1000"], first, last).rename(
            columns={"intl_in_per_1000": "intl_in_exposure_window"})
        df = df.merge(mig, on=["utla", "window_end"])
        covars.append("intl_in_exposure_window")
    # asylum support is only published from 2014, so it is kept out of the primary covariate set
    # (and out of the missing-data filter) and used in a sensitivity model instead
    return df.dropna(subset=[c for c in df.columns if c != "asylum_per_1000"]).reset_index(drop=True), covars


def main(level="utla"):
    out_dir = OUT_DIRS[level]
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for window_label, (first, last) in EXPOSURE_WINDOWS.items():
        df, covars = build_frame(level, first, last)
        specs = {"FE only": (df, []), "FE + time-varying": (df, covars)}
        if window_label.startswith("primary"):
            df["log_total"] = log_rate(df.rate_total_items)
            specs["FE + time-varying + total prescribing"] = (df, covars + ["log_total"])
            specs["FE + time-varying, excluding 2020-21"] = (df[~df.window_end.isin([2020, 2021])], covars)
            specs["FE + time-varying + asylum support"] = (df.dropna(subset=["asylum_per_1000"]),
                                                           covars + ["asylum_per_1000"])
        print(f"{level} {window_label}: {len(df)} area-years, {df.utla.nunique()} areas, "
              f"outcome years {df.window_end.min()}-{df.window_end.max()}")
        for drug in DRUG_GROUPS:
            for spec_label, (data, spec_covars) in specs.items():
                res = fit_ppml(data, f"rate_{drug}", spec_covars)
                rows.append(summarise(res, drug=drug, exposure_window=window_label, model=spec_label,
                                      converged=res.converged))

    out = pd.DataFrame(rows)
    primary = (out.exposure_window == "primary: t-3..t-1") & (out.model == "FE + time-varying")
    out.loc[primary, "q_fdr"] = multipletests(out.loc[primary, "p"], method="fdr_bh")[1]
    name = "panel_annual_results.csv" if level == "utla" else "panel_annual_ltla_results.csv"
    out.to_csv(out_dir / name, index=False)

    fmt = out.assign(est=out.apply(lambda r: f"{r.irr_10pct:.3f} ({r.ci_low:.3f}-{r.ci_high:.3f})", axis=1))
    for window_label in EXPOSURE_WINDOWS:
        w = fmt[fmt.exposure_window == window_label].pivot(index="drug", columns="model", values="est")
        print(f"\nIRR per 10% within-area increase in prescribing — {level}, annual outcome, exposure {window_label}")
        print(w.loc[list(DRUG_GROUPS)].to_string())
    print("\nPrimary model p / FDR q:")
    print(out[primary][["drug", "p", "q_fdr", "converged"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main(*sys.argv[1:2])
