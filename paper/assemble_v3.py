"""Assemble manuscript draft 3 (paper/manuscript.md) from section files, generated tables and result
files, so that every table and simulation number in the text comes directly from the outputs.

Sections: abstract_v3.md, introduction_v3.md, methods_v3.md, results_v3_draft.md, discussion_v3.md,
references_v3_verified.md. Placeholders:
  {{table:<name>}}   contents of paper/tables/<name>.md
  {{figure:<key>}}   figure markdown from FIGURES
  {{sim_...}}        values from outputs/power_simulation/power_summary_<level>.csv
  {{box_target_trial}} the target trial box from discussion_additions_v3.md

Usage: python paper/assemble_v3.py
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parent

FRONT_MATTER = """---
title: "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England"
short_title: "Prescribing and TB in England"
article_type: "Original research · Ecological study"
date: "Draft 4 (revised after peer review, round 2), 14 September 2026"
authors: "[Authors to be confirmed]"
thesis: "A disease-specific positive control shows hospital medicines data link to TB notifications only with heavy attenuation, and plausible effects of medicines on TB lie roughly 10 to several hundred times below what these ecological designs can detect."
---
"""

FIGURES = {
    "dag": ("figures/dag.png", "**Figure 1.** Assumed causal structure for area-level prescribing and TB notifications. "
            "Area fixed effects absorb stable area characteristics; year fixed effects absorb national shocks; "
            "time-varying measured factors are adjusted for; dashed nodes are unmeasured. Same-year prescribing for "
            "undiagnosed TB (protopathic bias) motivates the use of prescribing in the previous year."),
    "variation": ("figures/within_between_variation.png", "**Figure 2.** Within-area versus between-area variation in "
                  "log prescribing rates, 294 lower-tier authorities, 2014–2024. Orange line: a 10% increase."),
    "ocs_trends": ("figures/ocs_national_trends.png", "**Figure 4.** Oral glucocorticoid prescribing in English primary "
                   "care, 2011–2024: systemic oral glucocorticoid items, oral hydrocortisone items and "
                   "prednisolone-equivalent mg per resident."),
    "forest": ("figures/panel_forest_ltla_residence.png", "**Figure 3.** Primary care prescribing and TB notifications, "
               "lower-tier authorities, prescribing apportioned by patient residence. Blue: prescribing in the previous "
               "year (primary). Orange: prescribing in the following year, estimated jointly (falsification)."),
    "hospital": ("figures/hospital_positive_control.png", "**Figure 5.** Positive control: hospital active-TB treatment "
                 "(pyrazinamide DDD-years per 1,000 residents, including fixed-dose combinations) and TB "
                 "notifications between areas (left) and within areas over time (right)."),
    "ukborn": ("figures/ocs_ukborn_tb_by_region.png", "**Figure 6.** Oral glucocorticoid prescribing and UK-born TB "
               "notification rates by region, indexed to 2014 = 100."),
}


def sim_values():
    values = {}
    for level in ("ltla", "utla"):
        path = ROOT / "outputs" / "power_simulation" / f"power_summary_{level}.csv"
        if not path.exists():
            continue
        s = pd.read_csv(path).set_index("scenario")
        if "power_correct_direction" not in s.columns:
            continue
        pct = lambda x: f"{100 * x:.1f}%"
        keys = {"rr49": "Published RR 4.9", "rr25": "RR 25", "rr100": "RR 100", "irr102": "IRR 1.02 per 10%",
                "irr105": "IRR 1.05 per 10%", "irr110": "IRR 1.10 per 10%",
                "irr105_concurrent": "IRR 1.05 per 10%, acting via concurrent year",
                "irr110_concurrent": "IRR 1.10 per 10%, acting via concurrent year"}
        for k, scenario in keys.items():
            if scenario in s.index:
                values[f"sim_power_{k}_{level}"] = pct(s.loc[scenario, "rejection_two_sided"])
                values[f"sim_direction_{k}_{level}"] = pct(s.loc[scenario, "power_correct_direction"])
                z = abs(np.log(s.loc[scenario, "median_irr_10pct"])) / s.loc[scenario, "real_data_se"]
                values[f"sim_analytic_{k}_{level}"] = pct(norm.cdf(z - 1.96) + norm.cdf(-z - 1.96))
        sims = pd.read_csv(ROOT / "outputs" / "power_simulation" / f"simulations_{level}.csv")
        null = sims[(sims.scenario == "No effect") & (sims.p < 0.999)]
        values[f"sim_replicate_se_{level}"] = f"{(null.log_irr_10pct.abs() / norm.isf(null.p / 2)).median():.4f}"
        values[f"sim_null_direction_{level}"] = pct(s.loc["No effect", "power_correct_direction"])
        values[f"sim_null_rejection_{level}"] = pct(s.loc["No effect", "rejection_two_sided"])
        values[f"sim_null_sd_{level}"] = f"{s.loc['No effect', 'null_empirical_sd']:.4f}"
        values[f"sim_real_se_{level}"] = f"{s.loc['No effect', 'real_data_se']:.4f}"
    return values


def count_values():
    """Counts quoted in the text ({{n_...}}), taken from the result files."""
    values = {}
    for level in ("ltla", "utla"):
        path = ROOT / "outputs" / f"panel_annual_{level}_residence" / "panel_results.csv"
        if path.exists():
            r = pd.read_csv(path)
            primary = r[(r.model == "primary (t-1)") & (r.term == "exposure_lag1")]
            values[f"n_est_{level}"] = str(len(r))
            values[f"n_sig_{level}"] = str(int((r.p < 0.05).sum()))
            values[f"n_areas_{level}"] = str(int(primary.n_areas.max()))
            values[f"n_obs_{level}"] = f"{int(primary[primary.drug == 'oral_glucocorticoids'].n_obs.iloc[0]):,}"
    hospital = [pd.read_csv(p) for p in sorted((ROOT / "outputs" / "hospital").glob("hospital_results_*.csv"))]
    if hospital:
        h = pd.concat(hospital)
        h = h[h.design == "within-area FE"]
        values["n_hosp_est"] = str(len(h))
        values["n_hosp_sig"] = str(int((h.p < 0.05).sum()))
    path = ROOT / "outputs" / "steroids" / "ocs_tb_by_birthplace_regional.csv"
    if path.exists():
        r = pd.read_csv(path)
        r = r[r.model == "FE + migration + age"]
        values["n_regional_tests"] = str(len(r))
        values["n_regional_sig"] = str(int((r.p_randomisation <= 0.05).sum()))
    return values


def target_trial_box():
    text = (PAPER / "discussion_additions_v3.md").read_text()
    start = text.index("### Box.")
    return text[start:]


def fill(text, sims):
    def table(m):
        path = PAPER / "tables" / f"{m.group(1)}.md"
        return path.read_text() if path.exists() else f"*[table {m.group(1)} not yet generated]*"

    def figure(m):
        src, caption = FIGURES[m.group(1)]
        return f"![{caption}]({src})"

    text = re.sub(r"\{\{table:([\w]+)\}\}", table, text)
    text = re.sub(r"\{\{figure:([\w]+)\}\}", figure, text)
    text = text.replace("{{box_target_trial}}", target_trial_box())
    text = re.sub(r"\{\{((?:sim|n)_[\w]+)\}\}", lambda m: sims.get(m.group(1), f"[{m.group(1)} pending]"), text)
    return text


def main():
    sims = {**sim_values(), **count_values()}
    sections = ["abstract_v3.md", "introduction_v3.md", "methods_v3.md", "results_v3_draft.md", "discussion_v3.md"]
    body = "\n\n".join(fill((PAPER / s).read_text(), sims) for s in sections)
    references = (PAPER / "references_v3_verified.md").read_text()
    data = ("## Data and code availability\n\nAll inputs are publicly available (NHSBSA Open Data Portal: English "
            "Prescribing Dataset and Secondary Care Medicines Data; NHS Digital practice-level prescribing and "
            "registered patients by LSOA; UKHSA TB reports and Fingertips; OHID acute trust catchment populations; "
            "ONS/Nomis; Home Office asylum statistics; NHS England ODS; MHCLG English Indices of Deprivation). Code, "
            "processed datasets and outputs: https://github.com/drcjar/tb-prescribing-england. Data were obtained in "
            "September 2026: the EPD and SCMD through the NHSBSA API (all SCMD months analysed were final data, three of them "
            "from an earlier, since-retired release), and the NHS England ODS epraccur file, practice registration releases (April 2014–2024), OHID "
            "acute trust catchments (2024 catchment year), and the UKHSA TB in England 2025 and regional 2024 supplementary "
            "tables as published at that time. These portals revise data between releases.\n")
    supplement = ["## Supplementary tables"] + [f"{{{{table:{n}}}}}" for n in
                  ("tableS1_sensitivity", "tableS2_distributed_lag", "tableS3_hospital_mde", "tableS4_power_simulation",
                   "tableS5_regional", "tableS6_regional_lag_lead", "tableS7_hospital_coverage")]
    supplement += [f"{{{{table:{n}}}}}" for n in
                   ("tableS2b_lag_same_lead", "tableS3b_hospital_sensitivity", "tableS8_original_design", "tableS9_drug_groups")]
    manuscript = "\n\n".join([FRONT_MATTER, body, data, references, fill("\n\n".join(supplement), sims)])
    (PAPER / "manuscript.md").write_text(manuscript)
    pending = sorted(set(re.findall(r"\[((?:sim|n)_[\w]+) pending\]|\[table (\w+) not yet generated\]", manuscript)))
    print("Wrote", PAPER / "manuscript.md", "| pending:", pending or "none")


if __name__ == "__main__":
    main()
