"""Forest plot of NB incidence rate ratios (per SD of prescribing rate), unadjusted vs adjusted."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_dataset import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

LABELS = {
    "antituberculosis": "Antituberculosis (positive control)",
    "oral_corticosteroids": "Oral corticosteroids",
    "inhaled_corticosteroids": "Inhaled corticosteroids",
    "immunosuppressants": "Immunosuppressants",
    "proton_pump_inhibitors": "Proton pump inhibitors",
    "statins": "Statins",
    "metformin": "Metformin",
    "insulins": "Insulins",
    "fluoroquinolones": "Fluoroquinolones",
    "all_antibacterials": "All antibacterials",
    "vitamin_d": "Vitamin D",
    "levothyroxine": "Levothyroxine (negative control)",
}
SERIES = [("unadjusted", "Unadjusted", "#2a78d6"), ("adjusted", "Adjusted", "#eb6834")]
INK, SECONDARY, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def main():
    res = pd.read_csv(OUT / "nb_results.csv")
    drugs = list(DRUG_GROUPS)[::-1]
    y = {d: i for i, d in enumerate(drugs)}

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})
    fig, ax = plt.subplots(figsize=(8, 6.4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axvline(1, color="#c3c2b7", lw=1, zorder=1)

    for k, (model, label, colour) in enumerate(SERIES):
        r = res[res.model == model].set_index("drug").loc[drugs]
        pos = [y[d] + (0.17 if k == 0 else -0.17) for d in drugs]
        ax.hlines(pos, r.ci_low, r.ci_high, color=colour, lw=2, zorder=2)
        ax.scatter(r.irr_per_sd, pos, s=64, color=colour, edgecolor=SURFACE, linewidth=2, zorder=3, label=label)

    ax.set_yticks(range(len(drugs)), [LABELS[d] for d in drugs], color=INK)
    ax.set_xscale("log")
    ticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.minorticks_off()
    ax.set_xlim(0.5, 1.6)
    ax.tick_params(axis="x", colors=MUTED)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.set_xlabel("TB incidence rate ratio per SD of prescribing rate (95% CI, log scale)", color=SECONDARY)
    ax.legend(loc="lower right", frameon=False, labelcolor=SECONDARY)
    fig.suptitle("TB incidence 2022–24 vs GP prescribing June 2026, 105 Sub-ICB locations in England",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.text(0.02, 0.925, "Negative binomial models; adjusted for % born outside UK, IMD 2025, age structure "
             "and diabetes prevalence.\nEcological, cross-sectional associations — not causal estimates.",
             fontsize=9, color=SECONDARY, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "forest_plot.png", dpi=200, facecolor=SURFACE)
    print("Wrote", OUT / "forest_plot.png")


if __name__ == "__main__":
    main()
