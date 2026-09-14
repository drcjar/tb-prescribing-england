"""Within-area versus between-area variation in prescribing (peer review, round 1): distribution of
log prescribing rates after removing area and year means, against the distribution of area means,
for selected drug groups (LTLA panel, residence apportionment, 2014-2024).

Usage: python plot_variation.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from drug_groups import DRUG_GROUPS
from plot_panel import LABELS
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "descriptives"
OUT.mkdir(parents=True, exist_ok=True)
GROUPS = ["oral_glucocorticoids", "conventional_dmards", "proton_pump_inhibitors", "levothyroxine"]


def deviations(x, d):
    """Within-area deviations (area and year means removed) and between-area deviations of area means."""
    within = x - x.groupby(d.utla).transform("mean") - x.groupby(d.year).transform("mean") + x.mean()
    return within, x.groupby(d.utla).mean() - x.mean()


def main():
    panel = pd.read_csv(ROOT / "data" / "processed" / "ltla_panel_annual_residence.csv")
    panel = panel[panel.year.between(2014, 2024)]
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5), facecolor=SURFACE)
    for ax, g in zip(axes.flat, GROUPS):
        d = panel[["utla", "year", f"rate_{g}"]].dropna()
        d = d[d[f"rate_{g}"] > 0]
        within, between = deviations(np.log(d[f"rate_{g}"]), d)
        bins = np.linspace(-1, 1, 81)
        ax.set_facecolor(SURFACE)
        ax.hist(between.clip(-1, 1), bins=bins, color="#898781", alpha=0.6, label="Between areas (area means)")
        ax.hist(within.clip(-1, 1), bins=bins, color="#2a78d6", alpha=0.8, label="Within areas (area and year means removed)")
        ax.axvline(np.log(1.1), color="#eb6834", lw=1.5)
        ax.set_title(f"{LABELS[g]}: SD within {within.std():.2f}, between {between.std():.2f}", loc="left", color=INK, fontsize=10)
        ax.grid(axis="y", color=GRID, lw=0.8)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c3c2b7")
        ax.tick_params(colors=MUTED, length=0, labelsize=8)
    axes[0, 0].legend(frameon=False, fontsize=8, labelcolor=SECONDARY, loc="upper left")
    fig.suptitle(f"How much does prescribing vary within areas over time? Log rate deviations, {panel.utla.nunique()} "
                 "lower-tier authorities, 2014–2024", x=0.02, ha="left", fontsize=11.5, color=INK)
    fig.text(0.02, 0.935, "Orange line: a 10% increase (log 1.1), the contrast used for effect estimates.", fontsize=9,
             color=SECONDARY, va="top")
    fig.supxlabel("Log prescribing rate deviation", color=SECONDARY, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / "within_between_variation.png", dpi=200, facecolor=SURFACE)
    # every candidate group and exposure measure: items per 1,000, ADQ and prednisolone-equivalent mg per resident
    measures = [(f"rate_{g}", g, "items", False) for g in DRUG_GROUPS]
    measures += [(f"adq_{g}", g, "ADQ", True) for g in DRUG_GROUPS if f"adq_{g}" in panel]
    measures += [("mg_pred_equivalent", "oral_glucocorticoids", "prednisolone-equivalent mg", True)]
    rows = []
    for col, g, measure, per_resident in measures:
        d = panel[["utla", "year", "population", col]].dropna()
        d = d[d[col] > 0]
        if d.year.nunique() < 2:
            continue
        within, between = deviations(np.log(d[col] / d.population) if per_resident else np.log(d[col]), d)
        rows.append(dict(drug=g, measure=measure, n_areas=d.utla.nunique(), years=f"{d.year.min()}-{d.year.max()}",
                         sd_within=within.std(), sd_between=between.std(), within_p95_abs=np.percentile(np.abs(within), 95)))
    pd.DataFrame(rows).to_csv(OUT / "within_between_variation.csv", index=False)
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
