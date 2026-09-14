"""First-pass ecological models: TB incidence (2022-24) vs GP prescribing (June 2026) across
Sub-ICB locations in England. Negative binomial regression of TB counts with log population
offset; exposures and covariates standardised, so IRRs are per 1 SD of the prescribing rate.

Cross-sectional ecological associations only -- not causal estimates.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests

from build_dataset import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

COVARS = ["pct_non_uk_born", "imd_score", "pct_age_65plus", "pct_age_15_44", "diabetes_prev"]


def z(s):
    return (s - s.mean()) / s.std()


def fit_nb(df, exposure, covars, region=False):
    X = pd.DataFrame(index=df.index)
    if exposure:
        X["exposure"] = z(df[exposure])
    for c in covars:
        X[c] = z(df[c])
    if region:
        X = X.join(pd.get_dummies(df["region"], prefix="region", drop_first=True, dtype=float))
    X = sm.add_constant(X)
    return sm.NegativeBinomial(df["tb_count"], X, exposure=df["tb_denominator"]).fit(
        disp=0, maxiter=1000, cov_type="HC1")


def summarise(model, label, drug, sd):
    b = model.params["exposure"]
    lo, hi = model.conf_int().loc["exposure"]
    return dict(drug=drug, model=label, irr_per_sd=np.exp(b), ci_low=np.exp(lo), ci_high=np.exp(hi),
                p=model.pvalues["exposure"], sd_items_per_1000=sd, n=int(model.nobs),
                converged=model.mle_retvals["converged"])


def main():
    df = pd.read_csv(ROOT / "data" / "processed" / "sicbl26_analysis.csv", index_col=0)
    df = df.dropna(subset=["tb_count", "tb_denominator"] + COVARS)
    print(f"Analytic sample: {len(df)} Sub-ICB locations "
          f"({df.boundary_changed.sum()} re-apportioned across 2024->2026 boundary changes)")

    base = fit_nb(df, None, COVARS)
    print("\nCovariate-only model (IRR per SD):")
    print(pd.DataFrame({"IRR": np.exp(base.params), "p": base.pvalues}).round(3).to_string())

    specs = [
        ("unadjusted", df, [], False),
        ("adjusted", df, COVARS, False),
        ("adjusted + region", df, COVARS, True),
        ("adjusted, boundary-stable areas", df[~df.boundary_changed], COVARS, False),
        ("adjusted, excluding London", df[df.region != "London"], COVARS, False),
    ]
    rows, corr = [], []
    for drug in DRUG_GROUPS:
        col = f"rate_{drug}"
        for label, data, covars, region in specs:
            rows.append(summarise(fit_nb(data, col, covars, region), label, drug, data[col].std()))
        corr.append(dict(drug=drug,
                         mean_items_per_1000=df[col].mean(),
                         rho_tb_rate=spearmanr(df[col], df.tb_rate_per_100k).statistic,
                         rho_pct_non_uk_born=spearmanr(df[col], df.pct_non_uk_born).statistic,
                         rho_imd=spearmanr(df[col], df.imd_score).statistic))

    res = pd.DataFrame(rows)
    adj = res.model == "adjusted"
    res.loc[adj, "q_fdr"] = multipletests(res.loc[adj, "p"], method="fdr_bh")[1]
    res.to_csv(OUT / "nb_results.csv", index=False)
    corr = pd.DataFrame(corr)
    corr.to_csv(OUT / "spearman_correlations.csv", index=False)

    wide = res.assign(est=lambda r: r.apply(
        lambda x: f"{x.irr_per_sd:.2f} ({x.ci_low:.2f}-{x.ci_high:.2f})", axis=1)
    ).pivot(index="drug", columns="model", values="est")[[s[0] for s in specs]].loc[list(DRUG_GROUPS)]
    print("\nIRR per SD of prescribing rate (95% CI, robust SE):")
    print(wide.to_string())
    print("\nAdjusted model p / FDR q:")
    print(res[adj][["drug", "p", "q_fdr", "converged"]].round(4).to_string(index=False))
    print("\nSpearman correlations:")
    print(corr.round(2).to_string(index=False))
    wide.to_csv(OUT / "nb_results_wide.csv")


if __name__ == "__main__":
    main()
