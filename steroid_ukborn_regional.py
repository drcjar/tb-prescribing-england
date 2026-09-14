"""Oral corticosteroid prescribing vs TB in UK-born and non-UK-born people, by UKHSA region and
year (2014-2024). TB in UK-born people is less driven by migration and more likely to reflect
host factors such as immunosuppression, so it is the more relevant outcome for steroid effects.

Outcome: TB in England 2025 report, Supplementary Table 12 (region x place of birth x year, with
Labour Force Survey population denominators). Model: Poisson with region + year fixed effects,
lagged log OCS rate, cluster-robust SEs by region with t(8) critical values (steroid_trends.py).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_tb_annual import norm
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE
from steroid_trends import OUT, RAW, load_steroids, region_year, regional_panel

ROOT = Path(__file__).resolve().parent


def region_codes():
    ft = pd.read_csv(RAW / "tb_at6.csv")
    ft = ft[(ft["Indicator ID"] == 91359) & (ft["Area Type"] != "England")].drop_duplicates("Area Code")
    return {norm(n): c for n, c in zip(ft["Area Name"], ft["Area Code"])}


def birthplace_outcomes():
    bp = pd.read_csv(ROOT / "data" / "processed" / "region_tb_birthplace_annual.csv")
    codes = region_codes()
    bp["region"] = bp.region_name.map(norm).map(codes)
    unmatched = sorted(bp.loc[bp.region.isna(), "region_name"].unique())
    if unmatched:
        print("Region names not matched (excluded):", unmatched)
    return bp.dropna(subset=["region"]).rename(columns={"tb_count": "Count", "population_lfs": "Denominator"})


def plot_indexed(reg, bp):
    uk = bp[bp.birthplace == "UK born"].assign(rate=lambda d: d.Count / d.Denominator * 1e5)
    names = bp.drop_duplicates("region").set_index("region").region_name
    fig, axes = plt.subplots(3, 3, figsize=(10, 8.5), sharex=True, sharey=True, facecolor=SURFACE)
    for ax, region in zip(axes.flat, sorted(names.index, key=lambda r: names[r])):
        r_tb = uk[(uk.region == region) & uk.year.between(2014, 2024)].set_index("year").rate
        r_ocs = reg[(reg.region == region) & reg.year.between(2014, 2024)].set_index("year").ocs_per_1000
        ax.set_facecolor(SURFACE)
        ax.axhline(100, color="#c3c2b7", lw=1)
        ax.plot(r_ocs.index, 100 * r_ocs / r_ocs.loc[2014], color="#2a78d6", lw=2, label="OCS items per 1,000")
        ax.plot(r_tb.index, 100 * r_tb / r_tb.loc[2014], color="#eb6834", lw=2, label="UK-born TB rate")
        ax.set_title(names[region], loc="left", fontsize=10, color=INK)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, length=0, labelsize=8)
    axes[0, 0].legend(loc="lower left", frameon=False, fontsize=8, labelcolor=SECONDARY)
    fig.suptitle("Oral corticosteroid prescribing and UK-born TB incidence by region, indexed to 2014 = 100",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.text(0.02, 0.93, "OCS: NHSBSA English Prescribing Dataset, items per 1,000 residents.\n"
             "UK-born TB: UKHSA TB in England 2025, Supplementary Table 12 (LFS denominators; small annual "
             "counts in some regions).", fontsize=8.5, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / "ocs_ukborn_tb_by_region.png", dpi=200, facecolor=SURFACE)


def main():
    panel = pd.read_csv(ROOT / "data" / "processed" / "utla_panel_annual.csv")
    reg = region_year(load_steroids(), panel)
    bp = birthplace_outcomes()
    # steroid exposures, plus comparison drug groups: levothyroxine (negative control exposure),
    # and PPIs / statins (no plausible large population effect)
    exposures = ("ocs_per_1000", "pred_mg_per_resident", "rate_levothyroxine", "rate_proton_pump_inhibitors",
                 "rate_statins")
    analyses = {"lagged exposure": {}, "lagged, excluding 2020-21": {"exclude_years": (2020, 2021)},
                "lead (falsification)": {"lags": (-1, -2, -3)}}
    results = []
    for birthplace in ("UK born", "Non-UK born"):
        outcome = bp[bp.birthplace == birthplace]
        print(f"{birthplace}: {int(outcome[outcome.year.between(2015, 2024)].Count.sum())} notifications 2015-2024")
        for exposure in exposures:
            for analysis, kwargs in analyses.items():
                results.append(regional_panel(reg, outcome, f"TB, {birthplace}", exposure, **kwargs)
                               .assign(analysis=analysis))
    # UK-born TB aged 65+: heaviest steroid users and mostly reactivation disease. Denominator is all
    # residents aged 65+ (ONS), as UK-born population by age is not published by region.
    age = pd.read_csv(ROOT / "data" / "processed" / "region_tb_birthplace_age_annual.csv")
    codes = region_codes()
    age["region"] = age.region_name.map(norm).map(codes)
    older = age[(age.birthplace == "UK born") & (age.age_group.astype(str).str.startswith("65"))]
    older = older.merge(reg[["region", "year", "population", "pct_age_65plus"]], on=["region", "year"])
    older = older.assign(Count=older.tb_count, Denominator=older.population * older.pct_age_65plus / 100)
    print(f"UK born aged 65+: {int(older[older.year.between(2015, 2024)].Count.sum())} notifications 2015-2024")
    for exposure in ("ocs_per_1000", "pred_mg_per_resident", "rate_levothyroxine"):
        for analysis, kwargs in analyses.items():
            results.append(regional_panel(reg, older[["region", "year", "Count", "Denominator"]],
                                          "TB, UK born aged 65+", exposure, **kwargs).assign(analysis=analysis))

    res = pd.concat(results)
    res.to_csv(OUT / "ocs_tb_by_birthplace_regional.csv", index=False)
    adjusted = res[res.model == "FE + migration + age"]
    adjusted = adjusted.assign(est=adjusted.apply(
        lambda r: f"{r.irr_per_10pct:.2f} ({r.ci_low:.2f}-{r.ci_high:.2f}){'*' if r.p < 0.05 else ''}", axis=1))
    print(adjusted.pivot_table(index=["outcome", "exposure", "analysis"], columns="lag_years", values="est",
                               aggfunc="first").to_string())
    plot_indexed(reg, bp)


if __name__ == "__main__":
    main()
