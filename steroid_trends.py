"""Oral corticosteroid (OCS) prescribing trends in English primary care, 2014-2024, and whether
changes over time correlate with changes in TB incidence.

Three complementary analyses of change:
1. National: annual OCS rate vs annual England TB incidence (Fingertips 91359), levels and
   year-on-year changes (n = 11 years; descriptive only).
2. Regional annual panel: 9 regions x 2014-2024, annual TB counts (91359) vs OCS rate lagged
   1-3 years; Poisson with region + year fixed effects (few clusters -> HC1 SEs, cautious).
3. UTLA long differences: change in OCS rate (2014-16 -> 2019-21) vs change in log TB incidence
   (3-yr window 2014-16 -> 2022-24), adjusted for change in international in-migration.
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

from build_panel import lad_to_utla, norm_postcode, postcode_to_lad
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "steroids"
OUT.mkdir(parents=True, exist_ok=True)
SUBSTANCES = ["prednisolone", "dexamethasone", "hydrocortisone"]
COLOURS = {"prednisolone": "#2a78d6", "dexamethasone": "#eb6834", "hydrocortisone": "#1baf7a", "other": "#898781"}


def load_steroids():
    files = sorted((RAW / "epd_steroids_monthly").glob("epd_steroids_*.csv"))
    rx = pd.concat(pd.read_csv(f, dtype={"PRACTICE_CODE": str, "POSTCODE": str}) for f in files)
    rx["year"] = rx.YEAR_MONTH // 100
    rx["date"] = pd.to_datetime(rx.YEAR_MONTH.astype(str), format="%Y%m")
    rx["items_other"] = rx.items_ocs - rx[[f"items_{s}" for s in SUBSTANCES]].sum(axis=1)
    rx["pcds"] = rx.POSTCODE.map(norm_postcode)
    lad = postcode_to_lad(rx.pcds.dropna().unique())
    rx["utla"] = rx.pcds.map(lad).map(lad_to_utla())
    regions = json.load(open(RAW / "fingertips_utla502_to_region6.json"))
    rx["region"] = rx.utla.map({u: r for r, us in regions.items() for u in us})
    print(f"OCS items linked to a region: {rx.items_ocs[rx.region.notna()].sum() / rx.items_ocs.sum():.2%}")
    return rx


def tb_annual():
    tb = pd.read_csv(RAW / "tb_at6.csv")
    tb = tb[tb["Indicator ID"] == 91359]
    tb["year"] = tb["Time period"].astype(int)
    tb["geo"] = np.where(tb["Area Type"] == "England", "England", tb["Area Code"])
    tb = tb.drop_duplicates(["geo", "year"])
    return tb.set_index(["geo", "year"])[["Area Name", "Count", "Denominator", "Value"]]


def national_trends(rx, pop):
    item_cols = ["items_ocs", "items_other"] + [f"items_{s}" for s in SUBSTANCES]
    dose_cols = ["mg_prednisolone_tablets", "items_prednisolone_tablets"]
    monthly = rx.groupby("date")[item_cols + dose_cols].sum()
    monthly["population"] = monthly.index.year.map(pop)
    rates = monthly[item_cols + dose_cols].div(monthly.population, axis=0) * 100_000
    rates.to_csv(OUT / "national_monthly_ocs_per_100k.csv")

    totals = rx.groupby("year")[item_cols + dose_cols].sum()
    mg_per_item = (totals.mg_prednisolone_tablets / totals.items_prednisolone_tablets).rename("mg_per_prednisolone_tablet_item")
    annual = totals.div(totals.index.map(pop), axis=0) * 1000
    annual.columns = [c.replace("items_", "items_per_1000_").replace("mg_", "mg_per_1000_") for c in annual.columns]
    annual = annual.join(mg_per_item)
    annual.to_csv(OUT / "national_annual_ocs_per_1000.csv")
    change = 100 * (annual.loc[2024] / annual.loc[2014] - 1)
    print("\nNational OCS per 1,000 residents per year:\n", annual.round(1).to_string())
    print("\n% change 2014 -> 2024:\n", change.round(1).to_string())
    return rates, annual


def plot_national(rates):
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True, facecolor=SURFACE,
                             gridspec_kw={"height_ratios": [1.2, 1, 1]})
    for ax in axes:
        ax.set_facecolor(SURFACE)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, length=0)
    axes[0].plot(rates.index, rates.items_prednisolone, color=COLOURS["prednisolone"], lw=2)
    axes[0].set_title("Prednisolone items per 100,000 residents per month", loc="left", color=INK, fontsize=11)
    for s in ["hydrocortisone", "dexamethasone", "other"]:
        label = "Other (betamethasone, methylprednisolone, deflazacort…)" if s == "other" else s.capitalize()
        axes[1].plot(rates.index, rates[f"items_{s}"], color=COLOURS[s], lw=2, label=label)
    axes[1].set_title("Other oral corticosteroid items per 100,000 residents per month", loc="left",
                      color=INK, fontsize=11)
    axes[1].legend(loc="upper left", frameon=False, fontsize=9, labelcolor=SECONDARY, ncol=3)
    axes[1].set_ylim(0, rates[["items_hydrocortisone", "items_dexamethasone", "items_other"]].max().max() * 1.35)
    axes[2].plot(rates.index, rates.mg_prednisolone_tablets / 100_000, color=COLOURS["prednisolone"], lw=2)
    axes[2].set_title("Prednisolone tablets: milligrams dispensed per resident per month",
                      loc="left", color=INK, fontsize=11)
    for ax in axes:
        ax.set_ylim(bottom=0)
    fig.suptitle("Oral corticosteroid prescribing in English primary care, 2014–2024", x=0.02, ha="left",
                 fontsize=13, color=INK)
    fig.text(0.02, 0.945, "NHSBSA English Prescribing Dataset (practice level), per resident using ONS mid-year "
             "population estimates.", fontsize=9, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "ocs_national_trends.png", dpi=200, facecolor=SURFACE)


def national_correlation(annual, tb):
    eng = tb.loc["England"]
    d = annual[["items_per_1000_ocs", "mg_per_1000_prednisolone_tablets"]].join(eng.Value.rename("tb_rate"), how="inner")
    rows = []
    for lag in range(0, 4):
        x = d.items_per_1000_ocs.shift(lag)
        ok = x.notna()
        r_lvl = pearsonr(x[ok], d.tb_rate[ok])
        dx, dy = x.diff(), d.tb_rate.diff()
        ok2 = dx.notna() & dy.notna()
        r_diff = pearsonr(dx[ok2], dy[ok2])
        rows.append(dict(level="England", lag_years=lag, n_years=int(ok.sum()), r_levels=r_lvl.statistic,
                         p_levels=r_lvl.pvalue, r_year_on_year_change=r_diff.statistic, p_change=r_diff.pvalue))
    res = pd.DataFrame(rows)
    print("\nEngland: OCS items/1,000 vs TB incidence (annual)\n", res.round(3).to_string(index=False))
    return d, res


def region_year(rx, panel):
    """Region x year OCS prescribing, resident population, in-migration and age structure."""
    regions = json.load(open(RAW / "fingertips_utla502_to_region6.json"))
    reg_items = rx.dropna(subset=["region"]).groupby(["region", "year"])[["items_ocs", "mg_prednisolone_tablets"]].sum()
    p = panel.assign(region=panel.utla.map({u: r for r, us in regions.items() for u in us}))
    for c in ["pct_age_65plus", "pct_age_15_44"]:
        p[c + "_n"] = p[c] * p.population / 100
    group_items = [c for c in p.columns if c.startswith("items_")]
    agg = p.groupby(["region", "year"])[["population", "international_in", "pct_age_65plus_n", "pct_age_15_44_n"]
                                        + group_items].sum(min_count=1)
    reg = reg_items.join(agg, how="right")
    for c in group_items:
        reg["rate_" + c.removeprefix("items_")] = reg[c] / reg.population * 1000
    reg["ocs_per_1000"] = reg.items_ocs / reg.population * 1000
    reg["pred_mg_per_resident"] = reg.mg_prednisolone_tablets / reg.population
    reg["intl_in_per_1000"] = reg.international_in / reg.population * 1000
    reg["pct_age_65plus"] = 100 * reg.pct_age_65plus_n / reg.population
    reg["pct_age_15_44"] = 100 * reg.pct_age_15_44_n / reg.population
    return reg.reset_index()


def regional_panel(reg, outcome, outcome_label, exposure="ocs_per_1000", lags=(1, 2, 3), exclude_years=()):
    """Poisson region + year FE model of annual TB counts (outcome: region, year, Count,
    Denominator) on log exposure lagged by each of `lags` years (negative = lead, for
    falsification). With 9 clusters, SEs are cluster-robust by region with t(8) critical values,
    and a leave-one-region-out range is reported."""
    t_crit = student_t.ppf(0.975, df=8)
    k = np.log(1.1)
    rows = []
    for lag in lags:
        x = reg[["region", "year", exposure]].assign(year=lambda f: f.year + lag)
        cov = reg[["region", "year", "intl_in_per_1000", "pct_age_65plus", "pct_age_15_44"]]
        df = outcome.merge(x, on=["region", "year"]).merge(cov, on=["region", "year"]).dropna()
        df = df[~df.year.isin(exclude_years)]
        df["log_exposure"] = np.log(df[exposure])
        for label, rhs in [("FE only", ""), ("FE + migration + age", " + intl_in_per_1000 + pct_age_65plus + pct_age_15_44")]:
            formula = f"Count ~ log_exposure{rhs} + C(region) + C(year)"
            fit = lambda data: smf.glm(formula, data=data, family=sm.families.Poisson(),
                                       offset=np.log(data.Denominator)).fit(
                cov_type="cluster", cov_kwds={"groups": pd.factorize(data.region)[0]})
            m = fit(df)
            b, se = m.params.log_exposure, m.bse.log_exposure
            loo = [np.exp(fit(df[df.region != r]).params.log_exposure * k) for r in df.region.unique()]
            rows.append(dict(outcome=outcome_label, exposure=exposure, model=label, lag_years=lag, n_obs=len(df),
                             years=f"{df.year.min()}-{df.year.max()}", irr_per_10pct=np.exp(b * k),
                             ci_low=np.exp((b - t_crit * se) * k), ci_high=np.exp((b + t_crit * se) * k),
                             p=2 * student_t.sf(abs(b / se), df=8),
                             leave_one_region_out_range=f"{min(loo):.3f}-{max(loo):.3f}"))
    return pd.DataFrame(rows)


def utla_long_difference(rx, panel):
    utla_items = rx.dropna(subset=["utla"]).groupby(["utla", "year"]).items_ocs.sum()
    p = panel.set_index(["utla", "year"]).join(utla_items)
    p["ocs_per_1000"] = p.items_ocs / p.population * 1000

    def period_mean(col, years):
        return p[p.index.get_level_values("year").isin(years)].groupby(level="utla")[col].mean()

    d = pd.DataFrame({
        "ocs_2014_16": period_mean("ocs_per_1000", [2014, 2015, 2016]),
        "ocs_2019_21": period_mean("ocs_per_1000", [2019, 2020, 2021]),
        "mig_2014_16": period_mean("intl_in_per_1000", [2014, 2015, 2016]),
        "mig_2022_24": period_mean("intl_in_per_1000", [2022, 2023, 2024]),
    })
    tb = p.xs(2016, level="year")[["tb_count", "tb_denominator"]].join(
        p.xs(2024, level="year")[["tb_count", "tb_denominator"]], lsuffix="_1416", rsuffix="_2224")
    d = d.join(tb).dropna()
    d = d[(d.tb_count_1416 >= 10) & (d.tb_count_2224 >= 10)]  # stable log rates
    d["dlog_ocs"] = np.log(d.ocs_2019_21 / d.ocs_2014_16)
    d["dlog_tb"] = np.log((d.tb_count_2224 / d.tb_denominator_2224) / (d.tb_count_1416 / d.tb_denominator_1416))
    d["d_mig"] = d.mig_2022_24 - d.mig_2014_16
    rho = spearmanr(d.dlog_ocs, d.dlog_tb)
    ols = smf.wls("dlog_tb ~ dlog_ocs + d_mig", data=d, weights=d.tb_count_1416).fit(cov_type="HC1")
    b, se = ols.params.dlog_ocs, ols.bse.dlog_ocs
    k = np.log(1.1)
    res = dict(n_utla=len(d), median_pct_change_ocs=100 * (np.exp(d.dlog_ocs.median()) - 1),
               median_pct_change_tb=100 * (np.exp(d.dlog_tb.median()) - 1),
               spearman_rho=rho.statistic, spearman_p=rho.pvalue,
               adj_tb_ratio_per_10pct_ocs_increase=np.exp(b * k),
               ci_low=np.exp((b - 1.96 * se) * k), ci_high=np.exp((b + 1.96 * se) * k), p=ols.pvalues.dlog_ocs)
    print("\nUTLA long differences (OCS 2014-16 -> 2019-21; TB 2014-16 -> 2022-24):\n",
          pd.Series(res).round(3).to_string())
    d.to_csv(OUT / "utla_long_differences.csv")
    return d, res


def plot_long_difference(d, res):
    fig, ax = plt.subplots(figsize=(7, 5.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    size = 8 + 60 * d.tb_count_1416 / d.tb_count_1416.max()
    ax.scatter(100 * (np.exp(d.dlog_ocs) - 1), 100 * (np.exp(d.dlog_tb) - 1), s=size, color="#2a78d6",
               alpha=0.7, edgecolor=SURFACE, linewidth=1)
    ax.axhline(0, color="#c3c2b7", lw=1)
    ax.axvline(0, color="#c3c2b7", lw=1)
    ax.grid(color=GRID, lw=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, length=0)
    ax.set_xlabel("Change in OCS items per 1,000 residents, 2014–16 to 2019–21 (%)", color=SECONDARY)
    ax.set_ylabel("Change in TB incidence, 2014–16 to 2022–24 (%)", color=SECONDARY)
    fig.suptitle("Area-level changes in oral corticosteroid prescribing and TB incidence", x=0.02, ha="left",
                 fontsize=12, color=INK)
    fig.text(0.02, 0.925, f"{res['n_utla']} upper-tier local authorities (≥10 TB cases in each period); "
             f"point size ∝ baseline TB cases. Spearman ρ = {res['spearman_rho']:.2f} (p = {res['spearman_p']:.2f}).",
             fontsize=9, color=SECONDARY)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    fig.savefig(OUT / "ocs_tb_long_difference.png", dpi=200, facecolor=SURFACE)


def main():
    panel = pd.read_csv(ROOT / "data" / "processed" / "utla_panel_annual.csv")
    pop_national = panel.groupby("year").population.sum()
    rx = load_steroids()
    tb = tb_annual()

    rates, annual = national_trends(rx, pop_national)
    plot_national(rates)
    _, nat = national_correlation(annual, tb)
    region_frame = region_year(rx, panel)
    tb_regions = tb.reset_index().rename(columns={"geo": "region"})
    tb_regions = tb_regions[tb_regions.region != "England"]
    reg = pd.concat([regional_panel(region_frame, tb_regions, "All TB", e)
                     for e in ("ocs_per_1000", "pred_mg_per_resident")])
    print("\nRegional annual panel (Poisson, region + year FE; cluster SE, t(8)):\n",
          reg.round(3).to_string(index=False))
    d, ld = utla_long_difference(rx, panel)
    plot_long_difference(d, ld)

    pd.concat([nat, reg]).to_csv(OUT / "ocs_tb_change_correlations.csv", index=False)
    pd.Series(ld).to_csv(OUT / "utla_long_difference_summary.csv")


if __name__ == "__main__":
    main()
