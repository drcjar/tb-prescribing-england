"""Hospital medicines: positive-control figure and minimum detectable effects.

Figure: hospital antituberculosis drug use (rifampicin DDD per 1,000 residents per year, SCMD
apportioned by trust catchment) vs TB incidence, 2019-2024, by UTLA:
  left  - between areas (period means, log scales);
  right - within areas (log values after removing area and year means).

MDE table: within-area model with exposure in year t-1, 80% power, alpha 0.05, compared with
illustrative population effects. The prevalence and RR values for hospital drugs are assumptions
for illustration (no verified UK prevalence estimates were found) and are labelled as such.

Usage: python plot_hospital.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr

from mde import expected_irr, rr_needed
from plot_results import GRID, INK, MUTED, SECONDARY, SURFACE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "hospital"
Z = norm.ppf(0.975) + norm.ppf(0.80)

# illustrative scenarios (assumptions, not verified estimates)
SCENARIOS = {
    "anti_tnf": [("RR 4, prevalence 0.2%", 4, 0.002), ("RR 15, prevalence 0.2%", 15, 0.002)],
    "jak_inhibitor": [("RR 4, prevalence 0.05%", 4, 0.0005)],
    "other_biologic": [("RR 2, prevalence 0.2%", 2, 0.002)],
    "systemic_corticosteroid": [("RR 4.9, prevalence 0.9%", 4.9, 0.009)],
    "calcineurin_antiproliferative": [("RR 3, prevalence 0.3%", 3, 0.003)],
}


def style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(color=GRID, lw=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=MUTED, length=0)


def figure():
    df = pd.read_csv(ROOT / "data" / "processed" / "utla_hospital_medicines_panel.csv")
    df = df[df.year.between(2019, 2024) & (df.rate_antituberculosis > 0) & df.tb_count.notna()]
    df["tb_rate"] = df.tb_count / df.population * 1e5

    period = df.groupby("utla").agg(tb=("tb_count", "sum"), py=("population", "sum"),
                                    drug=("rate_antituberculosis", "mean"), pop=("population", "mean"))
    period["tb_rate"] = period.tb / period.py * 1e5
    rho = spearmanr(period.drug, period.tb_rate).statistic

    d = df.assign(log_tb=np.log((df.tb_count + 0.5) / df.population), log_drug=np.log(df.rate_antituberculosis))
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
    axes[0].set_xlabel("Hospital rifampicin DDD per 1,000 residents per year", color=SECONDARY)
    axes[0].set_ylabel("TB notifications per 100,000 per year", color=SECONDARY)
    axes[0].set_title(f"Between areas, 2019–24 (Spearman ρ = {rho:.2f})", loc="left", color=INK, fontsize=11)

    axes[1].scatter(d.log_drug_w, d.log_tb_w, s=6, color="#2a78d6", alpha=0.35, edgecolor="none")
    axes[1].axhline(np.mean(d.log_tb_w), color="#c3c2b7", lw=1)
    axes[1].axvline(np.mean(d.log_drug_w), color="#c3c2b7", lw=1)
    axes[1].set_xlabel("Log drug use, area and year means removed", color=SECONDARY)
    axes[1].set_ylabel("Log TB rate, area and year means removed", color=SECONDARY)
    axes[1].set_title(f"Within areas over time (r = {within_r:.2f})", loc="left", color=INK, fontsize=11)
    fig.suptitle("Positive control: hospital antituberculosis drug use tracks TB incidence (149 upper-tier authorities)",
                 x=0.02, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(OUT / "hospital_positive_control.png", dpi=200, facecolor=SURFACE)
    return rho, within_r


def mde_table(level):
    res = pd.read_csv(OUT / f"hospital_results_{level}.csv")
    lag = res[(res.design == "within-area FE") & (res.model == "lag (t-1)")].set_index("drug")
    rows = []
    for drug, r in lag.iterrows():
        se = (np.log(r.ci_high) - np.log(r.ci_low)) / (2 * norm.ppf(0.975))
        mde = np.exp(Z * se)
        for label, rr, p in SCENARIOS.get(drug, [(None, np.nan, np.nan)]):
            exp_irr = expected_irr(rr, p) if label else np.nan
            rows.append(dict(level=level, drug=drug, estimate_lag1=r.estimate, ci_low=r.ci_low, ci_high=r.ci_high,
                             mde_pct=100 * (mde - 1), scenario=label, expected_pct=100 * (exp_irr - 1),
                             mde_to_expected=np.log(mde) / abs(np.log(exp_irr)) if label else np.nan,
                             rr_needed=rr_needed(mde, p) if label else np.nan))
    return pd.DataFrame(rows)


def main():
    rho, within_r = figure()
    print(f"Positive control: between-area Spearman rho {rho:.3f}; within-area r {within_r:.3f}")
    table = pd.concat([mde_table("utla"), mde_table("ltla")])
    table.to_csv(OUT / "hospital_mde.csv", index=False)
    print(table.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
