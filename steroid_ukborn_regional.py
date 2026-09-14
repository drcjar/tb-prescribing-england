"""Systemic oral glucocorticoid prescribing vs TB notifications in UK-born and non-UK-born people, by
UKHSA region and year (revised after peer review, round 1).

Outcomes: TB in England 2025 report, Supplementary Table 12 (region x place of birth x year, Labour
Force Survey denominators); UK-born TB at age 65+ from the regional reports (Table 9), with all
residents aged 65+ as denominator (UK-born population by age is not published by region, so changes
in the non-UK-born share of older people enter the offset).

Models (steroid_trends.py): Poisson with region + year fixed effects, exposures lagged 1-3 years or
led 1-3 years (falsification), cluster-robust t(8) and randomisation p-values, and lag 2 and lead 2
estimated jointly on a common sample.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_tb_annual import norm
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE
from steroid_trends import OUT, RAW, region_year, regional_lag_lead, regional_panel

ROOT = Path(__file__).resolve().parent
EXPOSURES = ("rate_oral_glucocorticoids", "rate_mg_pred_equivalent", "rate_levothyroxine")


def region_codes():
    ft = pd.read_csv(RAW / "tb_at6.csv")
    ft = ft[(ft["Indicator ID"] == 91359) & (ft["Area Type"] != "England")].drop_duplicates("Area Code")
    return {norm(n): c for n, c in zip(ft["Area Name"], ft["Area Code"])}


def birthplace_outcomes():
    bp = pd.read_csv(ROOT / "data" / "processed" / "region_tb_birthplace_annual.csv")
    bp["region"] = bp.region_name.map(norm).map(region_codes())
    return bp.dropna(subset=["region"]).rename(columns={"tb_count": "Count", "population_lfs": "Denominator"})


def older_ukborn(reg):
    age = pd.read_csv(ROOT / "data" / "processed" / "region_tb_birthplace_age_annual.csv")
    age["region"] = age.region_name.map(norm).map(region_codes())
    older = age[(age.birthplace == "UK born") & (age.age_group.astype(str).str.startswith("65"))]
    older = older.merge(reg[["region", "year", "population", "pct_age_65plus"]], on=["region", "year"])
    return older.assign(Count=older.tb_count, Denominator=older.population * older.pct_age_65plus / 100)[
        ["region", "year", "Count", "Denominator"]]


def plot_indexed(reg, bp):
    uk = bp[bp.birthplace == "UK born"].assign(rate=lambda d: d.Count / d.Denominator * 1e5)
    names = bp.drop_duplicates("region").set_index("region").region_name
    fig, axes = plt.subplots(3, 3, figsize=(10, 8.5), sharex=True, sharey=True, facecolor=SURFACE)
    series = [("rate_oral_glucocorticoids", "Systemic OCS items per 1,000", "#2a78d6"),
              ("rate_mg_pred_equivalent", "Prednisolone-equivalent mg per 1,000", "#1baf7a")]
    for ax, region in zip(axes.flat, sorted(names.index, key=lambda r: names[r])):
        r_tb = uk[(uk.region == region) & uk.year.between(2014, 2024)].set_index("year").rate
        r = reg[(reg.region == region) & reg.year.between(2014, 2024)].set_index("year")
        ax.set_facecolor(SURFACE)
        ax.axhline(100, color="#c3c2b7", lw=1)
        for col, label, colour in series:
            ax.plot(r.index, 100 * r[col] / r.loc[2014, col], color=colour, lw=2, label=label)
        ax.plot(r_tb.index, 100 * r_tb / r_tb.loc[2014], color="#eb6834", lw=2, label="UK-born TB notification rate")
        ax.set_title(names[region], loc="left", fontsize=10, color=INK)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, length=0, labelsize=8)
    axes[0, 0].legend(loc="lower left", frameon=False, fontsize=7.5, labelcolor=SECONDARY)
    fig.suptitle("Oral glucocorticoid prescribing and UK-born TB notifications by region, indexed to 2014 = 100",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.text(0.02, 0.93, "Prescribing: standard GP practices, per 1,000 residents. UK-born TB: UKHSA TB in England 2025,\n"
             "Supplementary Table 12 (LFS denominators; small annual counts in some regions).",
             fontsize=8.5, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / "ocs_ukborn_tb_by_region.png", dpi=200, facecolor=SURFACE)


def main():
    panel = pd.read_csv(ROOT / "data" / "processed" / "utla_panel_annual_residence.csv")
    reg = region_year(panel)
    bp = birthplace_outcomes()
    outcomes = {f"TB, {b}": bp[bp.birthplace == b][["region", "year", "Count", "Denominator"]]
                for b in ("UK born", "Non-UK born")}
    outcomes["TB, UK born aged 65+"] = older_ukborn(reg)
    analyses = {"lagged exposure": {}, "lagged, excluding 2020-21": {"exclude_years": (2020, 2021)},
                "lead (falsification)": {"lags": (-1, -2, -3)}}

    results, joint = [], []
    for label, outcome in outcomes.items():
        print(f"{label}: {int(outcome[outcome.year.between(2014, 2024)].Count.sum())} notifications 2014-2024", flush=True)
        for exposure in EXPOSURES:
            for analysis, kwargs in analyses.items():
                results.append(regional_panel(reg, outcome, label, exposure, **kwargs).assign(analysis=analysis))
            joint.append(regional_lag_lead(reg, outcome, label, exposure, lag=2))
    res = pd.concat(results)
    res.to_csv(OUT / "ocs_tb_by_birthplace_regional.csv", index=False)
    pd.DataFrame(joint).to_csv(OUT / "ocs_tb_by_birthplace_lag_lead.csv", index=False)

    adjusted = res[res.model == "FE + migration + age"]
    adjusted = adjusted.assign(est=adjusted.apply(
        lambda r: f"{r.irr_per_10pct:.2f} ({r.ci_low:.2f}-{r.ci_high:.2f}) pR={r.p_randomisation:.2f}", axis=1))
    print(adjusted.pivot_table(index=["outcome", "exposure", "analysis"], columns="lag_years", values="est",
                               aggfunc="first").to_string())
    print(pd.DataFrame(joint).round(3).to_string(index=False))
    plot_indexed(reg, bp)


if __name__ == "__main__":
    main()
