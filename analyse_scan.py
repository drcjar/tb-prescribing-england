"""Calibration and interpretation of the hypothesis-free prescribing x outcome scan.

The scan estimates every (BNF section, outcome) pair twice: prescribing in the year before
the outcome (lag) and in the year after (lead). Under confounding by shared area trends both
are inflated similarly, so the lead scan is the empirical null. What matters is not how many
lag associations are significant, but how many MORE there are than lead associations, and
whether specific pairs show lag >> lead.

Usage: python analyse_scan.py [utla|ltla]
Writes outputs/scan/{level}_scan_summary.csv, _asymmetry.csv and _qq.png
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "scan"

# drug sections paired with the disease they are prescribed for: these should show strong
# associations whatever the causal direction, so they calibrate the scan's sensitivity
INDICATION_CONTROLS = [
    ("0601", "diabetes"), ("0602", "thyroid"), ("0302", "copd"), ("0302", "asthma"),
    ("0212", "cholesterol"), ("0205", "hypertension"), ("0403", "depression"),
    ("0408", "epilep"), ("0411", "dementia"), ("0209", "stroke"), ("0206", "coronary"),
]


def summarise(d, label):
    z = d.z.replace([np.inf, -np.inf], np.nan).dropna()
    lam = np.median(z ** 2) / 0.4549  # genomic-control style inflation: 1.0 if null holds
    return dict(scan=label, pairs=len(z), nominal_p05=int((z.abs() > 1.96).sum()),
                frac_p05=round(float((z.abs() > 1.96).mean()), 4),
                strong_p001=int((z.abs() > 3.29).sum()), inflation_lambda=round(float(lam), 2))


def main(level="utla"):
    path = OUT / f"{level}_scan.csv"
    if not path.exists():
        raise SystemExit(f"{path} not found; run scan_prescribing_outcomes.py first")
    d = pd.read_csv(path, dtype={"section": str})
    labels = pd.read_csv(ROOT / "data" / "processed" / "bnf_section_labels.csv", dtype={"bnf_section": str})
    d = d.merge(labels.rename(columns={"bnf_section": "section"})[["section", "chapter", "examples"]],
                on="section", how="left")
    d["p"] = 2 * norm.sf(d.z.abs())

    rows = []
    for label, sub in d.groupby("model"):
        rows.append(summarise(sub, label))
    summary = pd.DataFrame(rows)
    # false discovery rate within each scan separately
    for label, sub in d.groupby("model"):
        ok = sub.p.notna()
        q = np.full(len(sub), np.nan)
        q[ok.to_numpy()] = multipletests(sub.p[ok], method="fdr_bh")[1]
        d.loc[sub.index, "q"] = q
    summary["fdr_q05"] = [int((d[(d.model == s) & (d.q < 0.05)]).shape[0]) for s in summary.scan]
    summary.to_csv(OUT / f"{level}_scan_summary.csv", index=False)
    print(summary.to_string(index=False))

    # lag vs lead for the same pair: a drug effect should load on the lag
    wide = d.pivot_table(index=["indicator_id", "indicator", "section", "chapter", "examples"],
                         columns="model", values=["beta", "se", "z", "q"], aggfunc="first")
    wide.columns = [f"{a}_{'lag' if 'lag' in b else 'lead'}" for a, b in wide.columns]
    wide = wide.reset_index().dropna(subset=["z_lag", "z_lead"])
    wide["z_diff"] = (wide.beta_lag - wide.beta_lead) / np.sqrt(wide.se_lag ** 2 + wide.se_lead ** 2)
    wide["asymmetry"] = wide.z_lag.abs() - wide.z_lead.abs()
    wide = wide.sort_values("asymmetry", ascending=False)
    wide.to_csv(OUT / f"{level}_asymmetry.csv", index=False)

    strong = wide[(wide.q_lag < 0.05) & (wide.z_lead.abs() < 1.96)]
    print(f"\npairs with FDR-significant lag but null lead: {len(strong)} of {len(wide)}")
    cols = ["indicator", "section", "examples", "beta_lag", "z_lag", "z_lead", "z_diff"]
    print(strong.head(15)[cols].to_string(index=False)[:3000])

    hits = []
    for sec, kw in INDICATION_CONTROLS:
        m = wide[(wide.section == sec) & wide.indicator.str.contains(kw, case=False, na=False)]
        for r in m.itertuples():
            hits.append(dict(section=sec, indicator=r.indicator[:60], z_lag=round(r.z_lag, 1),
                             z_lead=round(r.z_lead, 1), beta_lag=round(r.beta_lag, 3)))
    if hits:
        print("\nindication positive controls (expect large |z| whatever the direction):")
        print(pd.DataFrame(hits).to_string(index=False))

    fig, ax = plt.subplots(figsize=(6, 6))
    for label, colour in (("lag (t-1)", "#2a78d6"), ("lead (t+1)", "#eb6834")):
        z = d[d.model == label].z.replace([np.inf, -np.inf], np.nan).dropna().abs().sort_values()
        if z.empty:
            continue
        expected = norm.ppf(0.5 + 0.5 * (np.arange(1, len(z) + 1) - 0.5) / len(z))
        ax.plot(expected, z, ".", ms=2, color=colour, label=label)
    lim = 8
    ax.plot([0, lim], [0, lim], color="#898781", lw=1)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.set_xlabel("expected |z| under the null"); ax.set_ylabel("observed |z|")
    ax.set_title(f"Prescribing x outcome scan, {level.upper()}: lag vs lead")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / f"{level}_qq.png", dpi=180)
    print(f"\nwrote {OUT}/{level}_scan_summary.csv, _asymmetry.csv, _qq.png")


if __name__ == "__main__":
    main(*sys.argv[1:2])
