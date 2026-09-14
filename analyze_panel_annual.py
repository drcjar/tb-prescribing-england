"""Annual panel: TB notifications by local authority and calendar year (UKHSA regional reports,
2001-2024) vs GP prescribing 2011-2024, at UTLA or LTLA level (revised after peer review, round 1).

Estimator: Poisson PML with area and year fixed effects, ONS population offset and SEs clustered by
area (analyze_panel.fit_ppml_multi). Exposure windows are defined relative to the outcome year t.

Primary exposure: prescribing in year t-1. Drug-associated TB typically presents within months of
exposure; year t is contaminated by prescribing for undiagnosed TB (protopathic bias), so it is
reported but not treated as causal.

Models per drug group:
  primary                 exposure t-1, time-varying covariates
  FE only                 exposure t-1, no covariates
  distributed lag         t, t-1 and t-2 in one model
  lag and lead            t-1 and t+1 in one model, on the common sample (falsification: t+1)
  prior 3 years           mean of t-3..t-1 (the original primary window)
  + area trends           area-specific linear trends
  population covariate    log population as a covariate instead of an offset
  + LTBI programme        latent TB testing programme indicator
  + asylum support        asylum support per 1,000 (2014 onwards)
  exclude COVID years     outcome years 2020-21 and exposure years 2020-21 removed
For metformin and insulins, diabetes prevalence is not adjusted for (it lies on the pathway between
diagnosis and prescribing).

Usage: python analyze_panel_annual.py [utla|ltla] [postcode|residence]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from analyze_panel import TIME_VARYING, fit_ppml_multi
from drug_groups import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
K = np.log(1.1)
CONTROLS = {"antituberculosis", "levothyroxine"}
NO_DIABETES_ADJUSTMENT = {"metformin", "insulins"}
OUTCOME_YEARS = range(2014, 2025)


def rate_name(group):
    return f"rate_{group}"


def load(level, apportion="postcode"):
    suffix = "" if apportion == "postcode" else f"_{apportion}"
    panel = pd.read_csv(PROCESSED / f"{level}_panel_annual{suffix}.csv")
    # the UTLA panel also carries Fingertips 3-year TB windows; annual counts come from the UKHSA tables
    panel = panel.drop(columns=["tb_count", "tb_denominator", "area_name"], errors="ignore")
    tb = pd.read_csv(PROCESSED / f"{level}_tb_annual.csv")
    ltbi = pd.read_csv(PROCESSED / f"ltbi_programme_{level}.csv")
    return panel.merge(tb, on=["utla", "year"], how="left").merge(ltbi, on=["utla", "year"], how="left")


def with_lags(panel, cols, lags):
    """Add exposure columns shifted by each lag (lag 1 = previous year; -1 = next year)."""
    out = panel.copy()
    base = panel[["utla", "year"] + cols]
    for lag in lags:
        shifted = base.assign(year=base.year + lag).rename(columns={c: f"{c}_lag{lag}" for c in cols})
        out = out.merge(shifted, on=["utla", "year"], how="left")
    return out


def prior_mean(panel, cols, first=3, last=1):
    frames = []
    for lag in range(last, first + 1):
        frames.append(panel[["utla", "year"] + cols].assign(year=panel.year + lag))
    grouped = pd.concat(frames).groupby(["utla", "year"])[cols]
    # keep a mean only where all years in the window are observed for that drug
    means = grouped.mean().where(grouped.count() == first - last + 1)
    return means.rename(columns={c: f"{c}_prior3" for c in cols}).reset_index()


def estimate(df, exposures, covars, label, drug, **kwargs):
    d = df.dropna(subset=exposures + covars + ["tb_count", "population"])
    d = d.rename(columns={"year": "window_end", "population": "tb_denominator"})
    n_before = len(d)
    d = d[(d[exposures] > 0).all(axis=1)]
    res = fit_ppml_multi(d, exposures, covars, **kwargs)
    rows = []
    for e in exposures:
        b, se = res.params[f"log_{e}"], res.bse[f"log_{e}"]
        rows.append(dict(drug=drug, model=label, term=e.replace(rate_name(drug), "exposure"),
                         irr_10pct=np.exp(b * K), ci_low=np.exp((b - 1.96 * se) * K),
                         ci_high=np.exp((b + 1.96 * se) * K), lower90=np.exp((b - 1.645 * se) * K),
                         upper90=np.exp((b + 1.645 * se) * K), se_log_irr_10pct=se * K, p=res.pvalues[f"log_{e}"],
                         n_obs=int(res.nobs), n_dropped_zero_exposure=n_before - len(d),
                         n_areas=d.utla.nunique(), years=f"{d.window_end.min()}-{d.window_end.max()}"))
    if len(exposures) > 1:
        # first versus last term (lag versus lead in the falsification models): Wald test of the difference,
        # and the correlation of the two estimates, strongly negative when the exposures are collinear
        names = list(res.params.index)
        first, last = names.index(f"log_{exposures[0]}"), names.index(f"log_{exposures[-1]}")
        contrast = np.zeros(len(names))
        contrast[first], contrast[last] = 1, -1
        V = np.asarray(res.cov_params())
        for r in rows:
            r.update(p_first_minus_last=float(np.squeeze(res.t_test(contrast).pvalue)),
                     corr_first_last=V[first, last] / np.sqrt(V[first, first] * V[last, last]))
    return rows


def max_compatible_paf(upper_irr):
    """Largest attributable fraction compatible with the upper confidence limit (same linear model
    as mde.expected_irr): IRR per 10% = (1 + 1.1q)/(1 + q), PAF = q/(1+q)."""
    if upper_irr <= 1:
        return 0.0
    if upper_irr >= 1.1:
        return np.nan
    q = (upper_irr - 1) / (1.1 - upper_irr)
    return q / (1 + q)


def max_compatible_prevented_fraction(lower_irr):
    """Largest prevented fraction compatible with the lower confidence limit, from the same linear model
    with RR < 1: IRR per 10% = (1 + 1.1q)/(1 + q), q = p(RR - 1) < 0, prevented fraction = -q."""
    if lower_irr >= 1:
        return 0.0
    return -(lower_irr - 1) / (1.1 - lower_irr)


def main(level="utla", apportion="postcode"):
    out_dir = ROOT / "outputs" / f"panel_annual_{level}{'' if apportion == 'postcode' else '_' + apportion}"
    out_dir.mkdir(parents=True, exist_ok=True)
    panel = load(level, apportion)
    rates = [rate_name(g) for g in DRUG_GROUPS]
    adq_rates = []
    for g in DRUG_GROUPS:
        if f"adq_{g}" in panel:
            panel[f"rate_adq_{g}"] = panel[f"adq_{g}"] / panel["population"] * 1000
            adq_rates.append(f"rate_adq_{g}")
    df = with_lags(panel, rates, lags=[1, 2, -1])
    df = with_lags(df, adq_rates, lags=[1])
    df = df.merge(prior_mean(panel, rates), on=["utla", "year"], how="left")
    covid_exposure = df.year.isin([2021, 2022])  # t-1 in 2020-21
    df = df[df.year.isin(OUTCOME_YEARS)]
    covid_exposure = covid_exposure.loc[df.index]

    rows = []
    for drug in DRUG_GROUPS:
        x = rate_name(drug)
        covars = [c for c in TIME_VARYING if not (drug in NO_DIABETES_ADJUSTMENT and c == "diabetes_prev")]
        lag1, lag2, lead1 = f"{x}_lag1", f"{x}_lag2", f"{x}_lag-1"
        rows += estimate(df, [lag1], covars, "primary (t-1)", drug)
        rows += estimate(df, [lag1], [], "FE only (t-1)", drug)
        rows += estimate(df, [x, lag1, lag2], covars, "distributed lag (t, t-1, t-2)", drug)
        rows += estimate(df, [lag1, lead1], covars, "lag and lead (t-1, t+1)", drug)
        rows += estimate(df, [lag1, x, lead1], covars, "lag, same year and lead (t-1, t, t+1)", drug)
        rows += estimate(df, [f"{x}_prior3"], covars, "prior 3 years (t-3..t-1)", drug)
        rows += estimate(df, [lag1], covars, "+ area trends (t-1)", drug, area_trends=True)
        rows += estimate(df, [lag1], covars, "population covariate (t-1)", drug, population_covariate=True)
        rows += estimate(df, [lag1], covars + ["ltbi_active"], "+ LTBI programme (t-1)", drug)
        rows += estimate(df[df.year >= 2015], [lag1], covars + ["asylum_per_1000"], "+ asylum support (t-1)", drug)
        rows += estimate(df[~df.year.isin([2020, 2021]) & ~covid_exposure], [lag1], covars,
                         "exclude COVID years (t-1)", drug)
        rows += estimate(df[df.year >= 2018], [lag1], covars, "outcome years 2018-2024 (t-1)", drug)
        # outcome 2014 is the only year whose t-1 exposure comes from the pre-2014 HSCIC series
        rows += estimate(df[df.year >= 2015], [lag1], covars, "EPD exposure only (t-1)", drug)
        adq = f"rate_adq_{drug}"
        if f"{adq}_lag1" in df and df[f"{adq}_lag1"].gt(0).sum() > 100:
            rows += [dict(r, term="exposure_lag1") for r in
                     estimate(df, [f"{adq}_lag1"], covars, "ADQ measure (t-1)", drug)]
        print(f"{level}/{apportion}: {drug} done", flush=True)

    out = pd.DataFrame(rows)
    primary = (out.model == "primary (t-1)") & ~out.drug.isin(CONTROLS)
    out.loc[primary, "q_fdr"] = multipletests(out.loc[primary, "p"], method="fdr_bh")[1]
    out["max_compatible_paf_pct"] = [100 * max_compatible_paf(u) for u in out.upper90]
    out["max_compatible_prevented_fraction_pct"] = [100 * max_compatible_prevented_fraction(l) for l in out.lower90]
    # sensitivity: shift each upper limit by the negative control's estimate from the same model and term,
    # as if its bias applied equally to every drug
    nc = out[out.drug == "levothyroxine"].set_index(["model", "term"]).irr_10pct
    shift = [nc.get((m, t), np.nan) for m, t in zip(out.model, out.term)]
    out["max_compatible_paf_nc_shifted_pct"] = [100 * max_compatible_paf(u / s) for u, s in zip(out.upper90, shift)]
    out.to_csv(out_dir / "panel_results.csv", index=False)

    fmt = out.assign(est=out.apply(lambda r: f"{r.irr_10pct:.3f} ({r.ci_low:.3f}-{r.ci_high:.3f})", axis=1))
    wide = fmt.pivot_table(index=["drug", "term"], columns="model", values="est", aggfunc="first")
    wide.to_csv(out_dir / "panel_results_wide.csv")
    show = fmt[fmt.term == "exposure_lag1"].pivot_table(index="drug", columns="model", values="est", aggfunc="first")
    print(show.loc[list(DRUG_GROUPS)].to_string())
    print(out[primary | (out.model == "primary (t-1)")][["drug", "irr_10pct", "ci_low", "ci_high", "p", "q_fdr",
                                                          "max_compatible_paf_pct", "n_obs", "years"]]
          .round(4).to_string(index=False))


if __name__ == "__main__":
    main(*sys.argv[1:3])
