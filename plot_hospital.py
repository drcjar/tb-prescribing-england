"""Hospital medicines positive-control figure: active-TB treatment (pyrazinamide/ethambutol-containing
products, patient-year equivalents per 1,000 residents, SCMD apportioned by trust catchment) vs TB
notification rate, 2019-2024, by UTLA:
  left  - between areas (period means, log scales);
  right - within areas (log values after removing area and year means).
MDE and expected-effect tables are produced by hospital_medicines.py.

Usage: python plot_hospital.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "hospital"
EXPOSURE = "rate_antituberculosis_active"


def style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(color=GRID, lw=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, length=0)


def log_ticks(ax, axis, values, candidates):
    ticks = [t for t in candidates if values.min() / 1.2 <= t <= values.max() * 1.2]
    getattr(ax, f"set_{axis}ticks")(ticks, [f"{t:g}" for t in ticks])


def main():
    df = pd.read_csv(ROOT / "data" / "processed" / "utla_hospital_medicines_panel.csv")
    df = df[df.year.between(2019, 2024) & (df[EXPOSURE] > 0) & df.tb_count.notna()]

    period = df.groupby("utla").agg(tb=("tb_count", "sum"), py=("population", "sum"),
                                    drug=(EXPOSURE, "mean"), pop=("population", "mean"))
    period["tb_rate"] = period.tb / period.py * 1e5
    rho = spearmanr(period.drug, period.tb_rate).statistic

    d = df.assign(log_tb=np.log((df.tb_count + 0.5) / df.population), log_drug=np.log(df[EXPOSURE]))
    for col in ("log_tb", "log_drug"):
        d[col + "_w"] = d[col] - d.groupby("utla")[col].transform("mean") - d.groupby("year")[col].transform("mean") + d[col].mean()
    within_r = np.corrcoef(d.log_drug_w, d.log_tb_w)[0, 1]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), facecolor=SURFACE)
    for ax in axes:
        style(ax)
    axes[0].scatter(period.drug, period.tb_rate, s=8 + 60 * period["pop"] / period["pop"].max(), color="#2a78d6",
                    alpha=0.75, edgecolor=SURFACE, linewidth=0.8)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    log_ticks(axes[0], "x", period.drug, (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5))
    log_ticks(axes[0], "y", period.tb_rate, (1, 2, 5, 10, 20, 50))
    axes[0].minorticks_off()
    axes[0].set_xlabel("Active-TB treatment, patient-years per 1,000 residents", color=SECONDARY)
    axes[0].set_ylabel("TB notifications per 100,000 per year", color=SECONDARY)
    axes[0].set_title(f"Between areas, 2019–24 (Spearman ρ = {rho:.2f})", loc="left", color=INK, fontsize=11)

    axes[1].scatter(d.log_drug_w, d.log_tb_w, s=6, color="#2a78d6", alpha=0.35, edgecolor="none")
    axes[1].axhline(np.mean(d.log_tb_w), color="#c3c2b7", lw=1)
    axes[1].axvline(np.mean(d.log_drug_w), color="#c3c2b7", lw=1)
    axes[1].set_xlabel("Log drug use, area and year means removed", color=SECONDARY)
    axes[1].set_ylabel("Log TB rate, area and year means removed", color=SECONDARY)
    axes[1].set_title(f"Within areas over time (r = {within_r:.2f})", loc="left", color=INK, fontsize=11)
    fig.suptitle("Positive control: hospital active-TB treatment (pyrazinamide/ethambutol) and TB notifications, "
                 f"{period.shape[0]} upper-tier authorities", x=0.02, ha="left", fontsize=11.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "hospital_positive_control.png", dpi=200, facecolor=SURFACE)
    print(f"Positive control: between-area Spearman rho {rho:.3f}; within-area r {within_r:.3f}")


if __name__ == "__main__":
    main()
