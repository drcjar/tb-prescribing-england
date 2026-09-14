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

import pandas as pd

PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parent

FRONT_MATTER = """---
title: "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England"
short_title: "Prescribing and TB in England"
article_type: "Original research · Ecological study"
date: "Draft 3 (revised after peer review), 14 September 2026"
authors: "[Authors to be confirmed]"
thesis: "A disease-specific positive control shows the linkage works only with heavy attenuation, and plausible effects of medicines on TB lie one to two orders of magnitude below what these ecological designs can detect."
---
"""

FIGURES = {
    "dag": ("figures/dag.png", "**Figure 1.** Assumed causal structure for area-level prescribing and TB notifications. "
            "Area fixed effects absorb stable area characteristics; year fixed effects absorb national shocks; "
            "time-varying measured factors are adjusted for; dashed nodes are unmeasured. Same-year prescribing for "
            "undiagnosed TB (protopathic bias) motivates the use of prescribing in the previous year."),
    "variation": ("figures/within_between_variation.png", "**Figure 2.** Within-area versus between-area variation in "
                  "log prescribing rates, 292 lower-tier authorities, 2014–2024. Orange line: a 10% increase."),
    "ocs_trends": ("figures/ocs_national_trends.png", "**Figure 3.** Oral glucocorticoid prescribing in English primary "
                   "care, 2011–2024: systemic oral glucocorticoid items, oral hydrocortisone items and "
                   "prednisolone-equivalent mg per resident."),
    "forest": ("figures/panel_forest_ltla_residence.png", "**Figure 4.** Primary care prescribing and TB notifications, "
               "lower-tier authorities, prescribing apportioned by patient residence. Blue: prescribing in the previous "
               "year (primary). Orange: prescribing in the following year, estimated jointly (falsification)."),
    "hospital": ("figures/hospital_positive_control.png", "**Figure 5.** Positive control: hospital active-TB treatment "
                 "(pyrazinamide/ethambutol-containing products, patient-year equivalents per 1,000 residents) and TB "
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
        values[f"sim_null_rejection_{level}"] = pct(s.loc["No effect", "rejection_two_sided"])
        values[f"sim_null_sd_{level}"] = f"{s.loc['No effect', 'null_empirical_sd']:.4f}"
        values[f"sim_real_se_{level}"] = f"{s.loc['No effect', 'real_data_se']:.4f}"
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
    text = re.sub(r"\{\{(sim_[\w]+)\}\}", lambda m: sims.get(m.group(1), f"[{m.group(1)} pending]"), text)
    return text


def main():
    sims = sim_values()
    sections = ["abstract_v3.md", "introduction_v3.md", "methods_v3.md", "results_v3_draft.md", "discussion_v3.md"]
    body = "\n\n".join(fill((PAPER / s).read_text(), sims) for s in sections)
    references = (PAPER / "references_v3_verified.md").read_text()
    data = ("## Data and code availability\n\nAll inputs are publicly available (NHSBSA Open Data Portal: English "
            "Prescribing Dataset and Secondary Care Medicines Data; NHS Digital practice-level prescribing and "
            "registered patients by LSOA; UKHSA TB reports and Fingertips; OHID acute trust catchment populations; "
            "ONS/Nomis; Home Office asylum statistics; NHS England ODS; MHCLG English Indices of Deprivation). Code, "
            "processed datasets and outputs: https://github.com/drcjar/tb-prescribing-england.\n")
    supplement = ["## Supplementary tables"] + [f"{{{{table:{n}}}}}" for n in
                  ("tableS1_sensitivity", "tableS2_distributed_lag", "tableS3_hospital_mde", "tableS4_power_simulation",
                   "tableS5_regional", "tableS6_regional_lag_lead", "tableS7_hospital_coverage")]
    manuscript = "\n\n".join([FRONT_MATTER, body, data, references, fill("\n\n".join(supplement), sims)])
    (PAPER / "manuscript.md").write_text(manuscript)
    pending = sorted(set(re.findall(r"\[(sim_[\w]+) pending\]|\[table (\w+) not yet generated\]", manuscript)))
    print("Wrote", PAPER / "manuscript.md", "| pending:", pending or "none")


if __name__ == "__main__":
    main()
