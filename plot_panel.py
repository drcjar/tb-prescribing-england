"""Forest plots for the panel analyses: prior exposure (primary) vs future exposure (lead
falsification test), both from the fixed-effects + time-varying covariate model.

Usage: python plot_panel.py [rolling|annual]
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_dataset import DRUG_GROUPS
from plot_results import GRID, INK, LABELS, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
LEAD = "lead (falsification): t+1..t+3"

CONFIGS = {
    "rolling": dict(
        results=ROOT / "outputs" / "panel" / "panel_results.csv",
        out=ROOT / "outputs" / "panel" / "panel_forest_plot.png",
        primary="primary: t-5..t-3", primary_label="Prescribing in the 3 years before the TB window",
        outcome="Rolling 3-year TB windows (Fingertips)", unit="area-windows"),
    "annual": dict(
        results=ROOT / "outputs" / "panel_annual" / "panel_annual_results.csv",
        out=ROOT / "outputs" / "panel_annual" / "panel_annual_forest_plot.png",
        primary="primary: t-3..t-1", primary_label="Prescribing in the 3 years before the TB year",
        outcome="Annual TB notifications (UKHSA regional reports)", unit="area-years"),
}


def main(kind="rolling"):
    cfg = CONFIGS[kind]
    res = pd.read_csv(cfg["results"])
    res = res[res.model == "FE + time-varying"]
    drugs = list(DRUG_GROUPS)[::-1]
    series = [(cfg["primary"], cfg["primary_label"], "#2a78d6"),
              (LEAD, "Prescribing in the 3 years after (falsification test)", "#eb6834")]

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})
    fig, ax = plt.subplots(figsize=(8, 6.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axvline(1, color="#c3c2b7", lw=1, zorder=1)

    for k, (window, label, colour) in enumerate(series):
        r = res[res.exposure_window == window].set_index("drug").loc[drugs]
        pos = [i + (0.17 if k == 0 else -0.17) for i in range(len(drugs))]
        ax.hlines(pos, r.ci_low, r.ci_high, color=colour, lw=2, zorder=2)
        ax.scatter(r.irr_10pct, pos, s=64, color=colour, edgecolor=SURFACE, linewidth=2, zorder=3, label=label)

    ax.set_yticks(range(len(drugs)), [LABELS[d] for d in drugs], color=INK)
    ax.set_xscale("log")
    ticks = [0.9, 0.95, 1.0, 1.05, 1.1]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.minorticks_off()
    ax.set_xlim(0.88, 1.12)
    ax.tick_params(axis="x", colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.set_xlabel("TB incidence rate ratio per 10% within-area increase in prescribing (95% CI)", color=SECONDARY)
    ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.1), frameon=False, labelcolor=SECONDARY, ncol=1)
    n_obs = res[res.exposure_window == cfg["primary"]].n_obs.max()
    fig.suptitle("TB incidence vs GP prescribing: fixed-effects panel, upper-tier local authorities, England",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.text(0.02, 0.94, f"{cfg['outcome']} vs prescribing 2014–24 ({n_obs} {cfg['unit']} in primary model).\n"
             "Poisson PML with area and time fixed effects; adjusted for age structure, international\n"
             "in-migration, HIV and diabetes prevalence; SEs clustered by area. Not causal estimates.",
             fontsize=9, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.89))
    fig.savefig(cfg["out"], dpi=200, facecolor=SURFACE)
    print("Wrote", cfg["out"])


if __name__ == "__main__":
    main(*sys.argv[1:2])
