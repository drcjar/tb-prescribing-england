"""Systemic oral glucocorticoid prescribing in English primary care, 2011-2024, and whether changes
correlate with changes in TB notifications (revised after peer review, round 1).

Exposure data: practice-level extracts (epd_practice_monthly_v2; HSCIC PDPI 2011-2013, NHSBSA EPD
2014-2024), standard GP practices (RO76): systemic oral glucocorticoid items, oral hydrocortisone
and oral dexamethasone items, and prednisolone-equivalent mg.

Analyses:
1. National: annual rates vs England TB notification rate (Fingertips 91359), levels and changes.
2. Regional annual panel (9 regions): Poisson with region + year fixed effects, lagged exposure;
   inference by randomisation (whole regional exposure histories permuted across regions) as well as
   cluster-robust t(8); lag and lead estimated jointly on a common sample.
3. UTLA long differences, 2014-16 -> 2019-21 (prescribing) and 2014-16 -> 2022-24 (TB).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import pearsonr, spearmanr
from scipy.stats import t as student_t

from build_panel import PRACTICE_FILES, gp_practice_masks
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "steroids"
OUT.mkdir(parents=True, exist_ok=True)
MONTHLY_COLS = ["items_oral_glucocorticoids", "items_oral_hydrocortisone", "items_oral_dexamethasone",
                "mg_pred_equivalent", "items_total"]
K = np.log(1.1)


def national_monthly():
    frames = []
    for f in sorted(PRACTICE_FILES.glob("epd_practice_*.csv")):
        d = pd.read_csv(f, usecols=["YEAR_MONTH", "PRACTICE_CODE"] + MONTHLY_COLS, dtype={"PRACTICE_CODE": str})
        _, gp = gp_practice_masks(d.PRACTICE_CODE)
        frames.append(d[gp].groupby("YEAR_MONTH")[MONTHLY_COLS].sum())
    m = pd.concat(frames)
    m.index = pd.to_datetime(m.index.astype(str), format="%Y%m")
    return m[m.index.year >= 2011]


def national_trends(monthly, pop):
    rates = monthly.div(monthly.index.year.map(pop), axis=0) * 100_000
    rates.to_csv(OUT / "national_monthly_ocs_per_100k.csv")
    annual = monthly.groupby(monthly.index.year).sum()
    annual = annual.div(annual.index.map(pop), axis=0) * 1000
    annual["mg_per_item"] = (monthly.groupby(monthly.index.year).mg_pred_equivalent.sum()
                             / monthly.groupby(monthly.index.year).items_oral_glucocorticoids.sum())
    annual.to_csv(OUT / "national_annual_ocs_per_1000.csv")
    print("\nNational per 1,000 residents per year:\n", annual.round(1).to_string())
    print("\n% change 2014 -> 2024:\n", (100 * (annual.loc[2024] / annual.loc[2014] - 1)).round(1).to_string())
    return rates, annual


def plot_national(rates):
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True, facecolor=SURFACE)
    panels = [
        ("items_oral_glucocorticoids", "Systemic oral glucocorticoid items per 100,000 residents per month", "#2a78d6"),
        ("items_oral_hydrocortisone", "Oral hydrocortisone items per 100,000 residents per month (mainly replacement)", "#1baf7a"),
        ("mg_pred_equivalent", "Prednisolone-equivalent mg per resident per month", "#2a78d6"),
    ]
    for ax, (col, title, colour) in zip(axes, panels):
        y = rates[col] / (100_000 if col.startswith("mg") else 1)
        ax.set_facecolor(SURFACE)
        ax.plot(rates.index, y, color=colour, lw=2)
        ax.set_title(title, loc="left", color=INK, fontsize=11)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, length=0)
    fig.suptitle("Oral glucocorticoid prescribing in English primary care, 2011–2024", x=0.02, ha="left",
                 fontsize=13, color=INK)
    fig.text(0.02, 0.945, "Standard GP practices; HSCIC practice-level prescribing (2011–13) and NHSBSA English "
             "Prescribing Dataset (2014–24);\nper resident using ONS mid-year estimates. Systemic = prednisolone, "
             "prednisone, methylprednisolone, deflazacort, dexamethasone.", fontsize=9, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / "ocs_national_trends.png", dpi=200, facecolor=SURFACE)


def tb_annual():
    tb = pd.read_csv(RAW / "tb_at6.csv")
    tb = tb[tb["Indicator ID"] == 91359]
    tb["year"] = tb["Time period"].astype(int)
    tb["geo"] = np.where(tb["Area Type"] == "England", "England", tb["Area Code"])
    return tb.drop_duplicates(["geo", "year"]).set_index(["geo", "year"])[["Area Name", "Count", "Denominator", "Value"]]


def national_correlation(annual, tb):
    d = annual[["items_oral_glucocorticoids"]].join(tb.loc["England"].Value.rename("tb_rate"), how="inner")
    rows = []
    for lag in range(0, 4):
        x = d.items_oral_glucocorticoids.shift(lag)
        ok = x.notna()
        dx, dy = x.diff(), d.tb_rate.diff()
        ok2 = dx.notna() & dy.notna()
        r_lvl, r_diff = pearsonr(x[ok], d.tb_rate[ok]), pearsonr(dx[ok2], dy[ok2])
        rows.append(dict(level="England", lag_years=lag, n_years=int(ok.sum()), r_levels=r_lvl.statistic,
                         p_levels=r_lvl.pvalue, r_year_on_year_change=r_diff.statistic, p_change=r_diff.pvalue))
    res = pd.DataFrame(rows)
    print("\nEngland: systemic OCS items/1,000 vs TB notification rate (annual)\n", res.round(3).to_string(index=False))
    return res


def region_year(panel):
    """Region x year prescribing (from the UTLA panel), resident population, in-migration and age."""
    regions = json.load(open(RAW / "fingertips_utla502_to_region6.json"))
    p = panel.assign(region=panel.utla.map({u: r for r, us in regions.items() for u in us}))
    for c in ["pct_age_65plus", "pct_age_15_44"]:
        p[c + "_n"] = p[c] * p.population / 100
    item_cols = [c for c in p.columns if c.startswith(("items_", "mg_"))]
    reg = p.groupby(["region", "year"])[["population", "international_in", "pct_age_65plus_n", "pct_age_15_44_n"]
                                        + item_cols].sum(min_count=1)
    for c in item_cols:
        name = "rate_mg_pred_equivalent" if c.startswith("mg_") else "rate_" + c.removeprefix("items_")
        reg[name] = reg[c] / reg.population * 1000
    reg["intl_in_per_1000"] = reg.international_in / reg.population * 1000
    reg["pct_age_65plus"] = 100 * reg.pct_age_65plus_n / reg.population
    reg["pct_age_15_44"] = 100 * reg.pct_age_15_44_n / reg.population
    return reg.reset_index()


COVARIATE_RHS = " + intl_in_per_1000 + pct_age_65plus + pct_age_15_44"


def _fit(df, terms, adjusted):
    formula = f"Count ~ {' + '.join(terms)}{COVARIATE_RHS if adjusted else ''} + C(region) + C(year)"
    return smf.glm(formula, data=df, family=sm.families.Poisson(), offset=np.log(df.Denominator)).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(df.region)[0]})


def randomisation_p(df, exposure_cols, term, adjusted, n_perm=999, seed=1):
    """Permute whole regional exposure histories across regions (9! possible) and refit. The statistic is
    the cluster-robust t statistic, which is less size-distorted than the raw coefficient when exposure
    variability differs between regions. Valid for the sharp null under exchangeability of regional
    exposure histories; p = (1 + count) / (1 + draws)."""
    observed = _fit(df, exposure_cols, adjusted).tvalues[term]
    regions = sorted(df.region.unique())
    rng = np.random.default_rng(seed)
    # draw random permutations directly: materialising all 9! orderings on every call wastes memory
    stats = []
    for _ in range(n_perm):
        mapping = dict(zip(regions, rng.permutation(regions)))
        donor = df.set_index(["region", "year"])[exposure_cols]
        permuted = donor.reindex(list(zip(df.region.map(mapping), df.year))).to_numpy()
        stats.append(_fit(df.assign(**dict(zip(exposure_cols, permuted.T))), exposure_cols, adjusted).tvalues[term])
    stats = np.array(stats)
    return (1 + (np.abs(stats) >= abs(observed)).sum()) / (len(stats) + 1)


def regional_panel(reg, outcome, outcome_label, exposure="rate_oral_glucocorticoids", lags=(1, 2, 3),
                   exclude_years=(), n_perm=499):
    """Poisson region + year FE model of annual TB counts (outcome: region, year, Count, Denominator)
    on log exposure lagged by each of `lags` years, fitted separately; negative lags are leads.
    Inference: cluster-robust SEs by region with t(8) critical values, and randomisation p-values."""
    t_crit = student_t.ppf(0.975, df=8)
    rows = []
    for lag in lags:
        x = reg[["region", "year", exposure]].assign(year=lambda f: f.year + lag)
        cov = reg[["region", "year", "intl_in_per_1000", "pct_age_65plus", "pct_age_15_44"]]
        df = outcome.merge(x, on=["region", "year"]).merge(cov, on=["region", "year"]).dropna()
        df = df[~df.year.isin(exclude_years) & (df[exposure] > 0)].reset_index(drop=True)
        df["log_exposure"] = np.log(df[exposure])
        for label, adjusted in [("FE only", False), ("FE + migration + age", True)]:
            m = _fit(df, ["log_exposure"], adjusted)
            b, se = m.params.log_exposure, m.bse.log_exposure
            rows.append(dict(outcome=outcome_label, exposure=exposure, model=label, lag_years=lag, n_obs=len(df),
                             years=f"{df.year.min()}-{df.year.max()}", irr_per_10pct=np.exp(b * K),
                             ci_low=np.exp((b - t_crit * se) * K), ci_high=np.exp((b + t_crit * se) * K),
                             p_cluster_t8=2 * student_t.sf(abs(b / se), df=8),
                             p_randomisation=randomisation_p(df, ["log_exposure"], "log_exposure", adjusted, n_perm)))
    return pd.DataFrame(rows)


def regional_lag_lead(reg, outcome, outcome_label, exposure="rate_oral_glucocorticoids", lag=2, n_perm=499,
                      exclude_regions=()):
    """Lag and lead in one model on a common sample: a true effect should load on the lag only.
    exclude_regions: leave-region-out check (e.g. London, with the steepest regional trends)."""
    lagged = reg[["region", "year", exposure]].assign(year=lambda f: f.year + lag).rename(columns={exposure: "x_lag"})
    lead = reg[["region", "year", exposure]].assign(year=lambda f: f.year - lag).rename(columns={exposure: "x_lead"})
    cov = reg[["region", "year", "intl_in_per_1000", "pct_age_65plus", "pct_age_15_44"]]
    df = outcome.merge(lagged, on=["region", "year"]).merge(lead, on=["region", "year"]).merge(cov, on=["region", "year"])
    df = df[~df.region.isin(exclude_regions)].dropna().reset_index(drop=True)
    df["log_lag"], df["log_lead"] = np.log(df.x_lag), np.log(df.x_lead)
    m = _fit(df, ["log_lag", "log_lead"], True)
    diff = m.params.log_lag - m.params.log_lead
    cov_m = m.cov_params()
    se_diff = np.sqrt(cov_m.loc["log_lag", "log_lag"] + cov_m.loc["log_lead", "log_lead"] - 2 * cov_m.loc["log_lag", "log_lead"])
    return dict(outcome=outcome_label, exposure=exposure, lag=lag, excluded_regions="none", n_obs=len(df),
                years=f"{df.year.min()}-{df.year.max()}",
                irr_lag_10pct=np.exp(m.params.log_lag * K), irr_lead_10pct=np.exp(m.params.log_lead * K),
                ratio_lag_to_lead=np.exp(diff * K),
                p_difference_t8=2 * student_t.sf(abs(diff / se_diff), df=df.region.nunique() - 1),
                p_randomisation_lag=randomisation_p(df, ["log_lag", "log_lead"], "log_lag", True, n_perm))


def utla_long_difference(panel):
    # annual UKHSA counts replace the Fingertips 3-year windows carried in the UTLA panel
    p = panel.drop(columns=["tb_count", "tb_denominator"], errors="ignore").set_index(["utla", "year"])
    tb = pd.read_csv(PROCESSED / "utla_tb_annual.csv").set_index(["utla", "year"]).tb_count
    p = p.join(tb)

    def period(col, years):
        return p[p.index.get_level_values("year").isin(years)].groupby(level="utla")[col].mean()

    def period_sum(col, years):
        return p[p.index.get_level_values("year").isin(years)].groupby(level="utla")[col].sum()

    d = pd.DataFrame({
        "ocs_2014_16": period("rate_oral_glucocorticoids", [2014, 2015, 2016]),
        "ocs_2019_21": period("rate_oral_glucocorticoids", [2019, 2020, 2021]),
        "mig_2014_16": period("intl_in_per_1000", [2014, 2015, 2016]),
        "mig_2022_24": period("intl_in_per_1000", [2022, 2023, 2024]),
        "tb_1416": period_sum("tb_count", [2014, 2015, 2016]), "pop_1416": period_sum("population", [2014, 2015, 2016]),
        "tb_2224": period_sum("tb_count", [2022, 2023, 2024]), "pop_2224": period_sum("population", [2022, 2023, 2024]),
    }).dropna()
    d = d[(d.tb_1416 >= 10) & (d.tb_2224 >= 10)]
    d["dlog_ocs"] = np.log(d.ocs_2019_21 / d.ocs_2014_16)
    d["dlog_tb"] = np.log((d.tb_2224 / d.pop_2224) / (d.tb_1416 / d.pop_1416))
    d["d_mig"] = d.mig_2022_24 - d.mig_2014_16
    rho = spearmanr(d.dlog_ocs, d.dlog_tb)
    ols = smf.wls("dlog_tb ~ dlog_ocs + d_mig", data=d, weights=d.tb_1416).fit(cov_type="HC1")
    b, se = ols.params.dlog_ocs, ols.bse.dlog_ocs
    res = dict(n_utla=len(d), median_pct_change_ocs=100 * (np.exp(d.dlog_ocs.median()) - 1),
               median_pct_change_tb=100 * (np.exp(d.dlog_tb.median()) - 1), spearman_rho=rho.statistic,
               spearman_p=rho.pvalue, adj_tb_ratio_per_10pct_ocs_increase=np.exp(b * K),
               ci_low=np.exp((b - 1.96 * se) * K), ci_high=np.exp((b + 1.96 * se) * K), p=ols.pvalues.dlog_ocs)
    print("\nUTLA long differences:\n", pd.Series(res).round(3).to_string())
    d.to_csv(OUT / "utla_long_differences.csv")
    pd.Series(res).to_csv(OUT / "utla_long_difference_summary.csv")
    return res


def main():
    # prescribing apportioned by where registered patients live (primary)
    panel = pd.read_csv(PROCESSED / "utla_panel_annual_residence.csv")
    pop = panel.groupby("year").population.sum()
    monthly = national_monthly()
    rates, annual = national_trends(monthly, pop)
    plot_national(rates)
    nat = national_correlation(annual, tb_annual())

    reg = region_year(panel)
    tb = tb_annual().reset_index().rename(columns={"geo": "region"})
    tb = tb[tb.region != "England"]
    regional = pd.concat([regional_panel(reg, tb, "All TB", e) for e in ("rate_oral_glucocorticoids", "rate_mg_pred_equivalent")])
    print("\nRegional annual panel:\n", regional.round(3).to_string(index=False))
    pd.concat([nat, regional]).to_csv(OUT / "ocs_tb_change_correlations.csv", index=False)
    utla_long_difference(panel)


if __name__ == "__main__":
    main()
