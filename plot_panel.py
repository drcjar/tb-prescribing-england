"""Forest plot for the annual panel: prescribing in the previous year (primary, t-1) and in the
following year (falsification, t+1, estimated jointly with t-1), fixed effects + covariates.

Usage: python plot_panel.py [utla|ltla] [postcode|residence]
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from drug_groups import DRUG_GROUPS
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
LABELS = {
    "antituberculosis": "Antituberculosis (descriptive)",
    "oral_glucocorticoids": "Systemic oral glucocorticoids",
    "oral_hydrocortisone": "Oral hydrocortisone",
    "oral_dexamethasone": "Oral dexamethasone",
    "inhaled_corticosteroids": "Inhaled corticosteroids",
    "conventional_dmards": "Conventional DMARDs",
    "transplant_immunosuppressants": "Transplant immunosuppressants",
    "proton_pump_inhibitors": "Proton pump inhibitors",
    "statins": "Statins",
    "metformin": "Metformin",
    "insulins": "Insulins",
    "fluoroquinolones": "Fluoroquinolones",
    "all_antibacterials": "All antibacterials",
    "vitamin_d": "Vitamin D",
    "levothyroxine": "Levothyroxine (negative control)",
}
LEVEL_NAMES = {"utla": "upper-tier", "ltla": "lower-tier"}


def main(level="ltla", apportion="postcode"):
    suffix = "" if apportion == "postcode" else f"_{apportion}"
    out_dir = ROOT / "outputs" / f"panel_annual_{level}{suffix}"
    res = pd.read_csv(out_dir / "panel_results.csv")
    series = [
        (res[(res.model == "primary (t-1)") & (res.term == "exposure_lag1")],
         "Prescribing in the previous year (t−1)", "#2a78d6"),
        (res[(res.model == "lag and lead (t-1, t+1)") & (res.term == "exposure_lag-1")],
         "Prescribing in the following year (t+1; falsification, estimated jointly with t−1)", "#eb6834"),
    ]
    drugs = list(DRUG_GROUPS)[::-1]

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})
    fig, ax = plt.subplots(figsize=(8, 7.4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axvline(1, color="#c3c2b7", lw=1, zorder=1)
    for k, (r, label, colour) in enumerate(series):
        r = r.set_index("drug").reindex(drugs)
        pos = [i + (0.17 if k == 0 else -0.17) for i in range(len(drugs))]
        ax.hlines(pos, r.ci_low, r.ci_high, color=colour, lw=2, zorder=2)
        ax.scatter(r.irr_10pct, pos, s=56, color=colour, edgecolor=SURFACE, linewidth=2, zorder=3, label=label)

    ax.set_yticks(range(len(drugs)), [LABELS[d] for d in drugs], color=INK)
    ax.set_xscale("log")
    ticks = [0.9, 0.95, 1.0, 1.05, 1.1]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.minorticks_off()
    shown = pd.concat([r for r, _, _ in series])
    ax.set_xlim(min(0.87, shown.ci_low.min() * 0.99), max(1.13, shown.ci_high.max() * 1.01))
    ax.tick_params(axis="x", colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.set_xlabel("TB notification rate ratio per 10% within-area increase in prescribing (95% CI)", color=SECONDARY)
    ax.legend(loc="upper center", bbox_to_anchor=(0.3, -0.09), frameon=False, labelcolor=SECONDARY, ncol=1)
    primary = series[0][0]
    fig.suptitle(f"TB notifications and primary care prescribing: {LEVEL_NAMES[level]} local authorities, England",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.text(0.02, 0.945, f"Annual notifications {primary.years.iloc[0]}, {primary.n_areas.max()} areas, "
             f"up to {primary.n_obs.max():,} area-years; prescribing apportioned by {apportion}.\n"
             "Poisson PML with area and year fixed effects; adjusted for age structure, international in-migration,\n"
             "HIV and diabetes prevalence (not diabetes for metformin and insulins); SEs clustered by area.",
             fontsize=9, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    path = out_dir / "panel_forest_plot.png"
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    print("Wrote", path)


if __name__ == "__main__":
    main(*sys.argv[1:3])
