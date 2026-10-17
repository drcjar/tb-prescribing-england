"""Figures and tables for the hypothesis-free scan paper.

Inputs: outputs/scan/{utla,ltla,practice}_scan.csv, the exposure/outcome panels, and the
BNF section labels. Outputs go to paper_scan/figures and paper_scan/tables.

Usage: python scan_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr

ROOT = Path(__file__).resolve().parent
SCAN = ROOT / "outputs" / "scan"
PROCESSED = ROOT / "data" / "processed"
FIG = ROOT / "paper_scan" / "figures"
TAB = ROOT / "paper_scan" / "tables"
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)
SURFACE, INK, GRID = "#fbfaf7", "#1a1a1a", "#dcdad2"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#898781"

# drug section paired with the disease it is prescribed for
INDICATIONS = [("0601", "Diabetes: QOF prevalence", "Diabetes drugs"),
               ("0302", "COPD: QOF prevalence", "Inhaled therapy"),
               ("0205", "Hypertension: QOF prevalence", "Antihypertensives"),
               ("0403", "Depression: QOF prevalence", "Antidepressants"),
               ("0411", "Dementia: QOF prevalence", "Dementia drugs"),
               ("0209", "Stroke: QOF prevalence", "Antiplatelets"),
               ("0408", "Epilepsy: QOF prevalence", "Antiepileptics"),
               ("0206", "CHD: QOF prevalence", "Nitrates / CCBs")]


def style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(color=GRID, lw=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(colors=GREY, length=0)


def load(level):
    p = SCAN / f"{level}_scan.csv"
    if not p.exists():
        return None
    d = pd.read_csv(p, dtype={"section": str})
    lab = pd.read_csv(PROCESSED / "bnf_section_labels.csv", dtype={"bnf_section": str})
    return d.merge(lab.rename(columns={"bnf_section": "section"})[["section", "examples"]],
                   on="section", how="left")


def summary_table():
    rows = []
    for level, name in (("utla", "Upper-tier areas (151)"), ("ltla", "Lower-tier areas (294)"),
                        ("practice", "GP practices (~6,200)")):
        d = load(level)
        if d is None:
            continue
        for model in ("lag (t-1)", "lead (t+1)"):
            z = d[d.model == model].z.replace([np.inf, -np.inf], np.nan).dropna()
            if z.empty:
                continue
            rows.append(dict(unit=name, exposure="year before" if "lag" in model else "year after",
                             pairs=len(z), pct_significant=round(100 * (z.abs() > 1.96).mean(), 1),
                             median_abs_z=round(z.abs().median(), 2),
                             inflation_lambda=round(np.median(z ** 2) / 0.4549, 1)))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "table1_scan_summary.csv", index=False)
    print(t.to_string(index=False))
    return t


def between_within_figure():
    """The core area-level result: indication signal is strong between areas, absent within."""
    exp = pd.read_csv(PROCESSED / "utla_section_exposure.csv", dtype={"utla": str})
    out = pd.read_csv(PROCESSED / "utla_outcomes_long.csv", dtype={"utla": str})
    rows = []
    for sec, ind, label in INDICATIONS:
        if sec not in exp.columns:
            continue
        o = out[out.indicator == ind][["utla", "year", "count", "denominator"]].dropna()
        o = o[(o["count"] > 0) & (o.denominator > 0)]
        if o.empty:
            continue
        o["lr"] = np.log(o["count"] / o.denominator)
        d = o.merge(exp[["utla", "year", sec]].rename(columns={sec: "x"}), on=["utla", "year"]).dropna()
        d = d[d.x > 0]
        if len(d) < 100:
            continue
        d["lx"] = np.log(d.x)
        m = d.groupby("utla")[["lx", "lr"]].mean()
        between = spearmanr(m.lx, m.lr).statistic
        w = d.copy()
        for c in ("lx", "lr"):
            w[c] = (w[c] - w.groupby("utla")[c].transform("mean")
                    - w.groupby("year")[c].transform("mean") + w[c].mean())
        within = np.corrcoef(w.lx, w.lr)[0, 1]
        rows.append(dict(drug=label, outcome=ind.replace(": QOF prevalence", ""),
                         between_areas=round(between, 2), within_areas=round(within, 2)))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "table2_between_within.csv", index=False)
    print("\n" + t.to_string(index=False))

    fig, ax = plt.subplots(figsize=(8.6, 4.6), facecolor=SURFACE)
    style(ax)
    y = np.arange(len(t))
    ax.barh(y + 0.19, t.between_areas, height=0.36, color=BLUE, label="between areas", zorder=3)
    ax.barh(y - 0.19, t.within_areas, height=0.36, color=ORANGE, label="within areas, over time", zorder=3)
    ax.set_yticks(y, [f"{r.drug}\nvs {r.outcome}" for r in t.itertuples()], fontsize=8, color=INK)
    ax.axvline(0, color="#c3c2b7", lw=1)
    ax.set_xlabel("correlation of log prescribing with log disease prevalence", color=GREY, fontsize=9)
    ax.set_title("A drug and the disease it treats:\nthe signal is between areas, not within them",
                 loc="left", color=INK, fontsize=11)
    ax.set_xlim(-0.15, 1.0)
    ax.legend(frameon=False, fontsize=9, labelcolor=GREY, loc="upper center",
              bbox_to_anchor=(0.5, -0.17), ncol=2)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.24)
    fig.savefig(FIG / "fig1_between_within.png", dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def qq_figure():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), facecolor=SURFACE)
    for ax, (level, title) in zip(axes, (("utla", "Upper-tier areas"), ("practice", "GP practices"))):
        style(ax)
        d = load(level)
        if d is None:
            continue
        for model, colour, lbl in (("lag (t-1)", BLUE, "prescribing the year before"),
                                   ("lead (t+1)", ORANGE, "prescribing the year after")):
            z = d[d.model == model].z.replace([np.inf, -np.inf], np.nan).dropna().abs().sort_values()
            if z.empty:
                continue
            exp_q = norm.ppf(0.5 + 0.5 * (np.arange(1, len(z) + 1) - 0.5) / len(z))
            ax.plot(exp_q, z, ".", ms=2, color=colour, label=lbl, zorder=3)
        lim = 10
        ax.plot([0, lim], [0, lim], color=GREY, lw=1, zorder=2)
        ax.set_xlim(0, 4); ax.set_ylim(0, lim)
        ax.set_xlabel("expected |z| if nothing were going on", color=GREY, fontsize=9)
        ax.set_title(title, loc="left", color=INK, fontsize=11)
    axes[0].set_ylabel("observed |z|", color=GREY, fontsize=9)
    axes[0].legend(frameon=False, fontsize=9, labelcolor=GREY, loc="upper left")
    fig.suptitle("Associations with prescribing after the outcome are as strong as before it",
                 x=0.02, ha="left", color=INK, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(FIG / "fig2_qq.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)


def indication_table():
    rows = []
    for level in ("utla", "practice"):
        d = load(level)
        if d is None:
            continue
        w = d.pivot_table(index=["indicator", "section"], columns="model", values="z", aggfunc="first")
        w.columns = ["lag" if "lag" in c else "lead" for c in w.columns]
        w = w.reset_index()
        for sec, ind, label in INDICATIONS:
            m = w[(w.section == sec) & (w.indicator == ind)]
            for r in m.itertuples():
                rows.append(dict(level="areas" if level == "utla" else "practices", drug=label,
                                 outcome=ind.replace(": QOF prevalence", ""),
                                 z_year_before=round(r.lag, 1), z_year_after=round(r.lead, 1)))
    t = pd.DataFrame(rows)
    t.to_csv(TAB / "table3_indication_controls.csv", index=False)
    print("\n" + t.to_string(index=False))


def top_hits_table():
    d = load("practice")
    if d is None:
        return
    w = d.pivot_table(index=["indicator", "section", "examples"], columns="model",
                      values=["beta", "z"], aggfunc="first")
    w.columns = [f"{a}_{'lag' if 'lag' in b else 'lead'}" for a, b in w.columns]
    w = w.reset_index().dropna(subset=["z_lag", "z_lead"])
    w["asymmetry"] = w.z_lag.abs() - w.z_lead.abs()
    def fmt(sub, path, note):
        t = sub[["indicator", "section", "examples", "z_lag", "z_lead"]].copy()
        t["examples"] = t.examples.astype(str).str.slice(0, 46)
        t[["z_lag", "z_lead"]] = t[["z_lag", "z_lead"]].round(1)
        t.columns = ["outcome", "BNF section", "what is in it", "z (year before)", "z (year after)"]
        t.to_csv(path, index=False)
        print(f"\n{note}")
        print(t.to_string(index=False))
        return t

    fmt(w.sort_values("asymmetry", ascending=False).head(8), TAB / "table4_top_hits.csv",
        "strongest candidates in the whole scan after filtering on before-beats-after:")
    # the same filter restricted to disease outcomes, excluding service and satisfaction measures
    disease = w[w.indicator.str.contains(
        "prevalence|incidence|mortalit|admission|deaths|cancer", case=False, na=False)
        & ~w.indicator.str.contains("experience|satisf|retired|check|review|screening uptake",
                                    case=False, na=False)]
    fmt(disease.sort_values("asymmetry", ascending=False).head(8), TAB / "table5_top_disease_hits.csv",
        "same filter, restricted to disease outcomes:")


if __name__ == "__main__":
    summary_table()
    between_within_figure()
    qq_figure()
    indication_table()
    top_hits_table()
    print(f"\nwrote figures to {FIG} and tables to {TAB}")
