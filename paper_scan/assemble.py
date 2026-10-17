"""Assemble the scan paper from its section files, generated tables and figures.

Placeholders: {{table:<name>}} pulls paper_scan/tables/<name>.csv, {{figure:<key>}} pulls the
matching PNG, so every number in the text traces to a generated file.

Usage: python paper_scan/assemble.py
"""
import re
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SECTIONS = ["abstract.md", "introduction.md", "methods.md", "results.md", "discussion.md"]

CAPTIONS = {
    "fig1": ("fig1_between_within.png",
             "**Figure 1.** Correlation between prescribing of a drug and the prevalence of the "
             "disease it treats, upper-tier local authorities. Between areas the two are nearly "
             "interchangeable; within areas over time the relationship is absent."),
    "fig2": ("fig2_qq.png",
             "**Figure 2.** Observed against expected |z| for every drug-outcome pair. Blue: "
             "prescribing in the year before the outcome. Orange: prescribing in the year after, "
             "which cannot be a cause and so serves as an empirical null. Left, upper-tier areas: "
             "the two are indistinguishable. Right, GP practices: both are inflated and the "
             "year-after curve is higher."),
}
TITLES = {
    "table1_scan_summary": "**Table 1.** Results of the scan at each unit of analysis, with "
                           "prescribing measured before and after the outcome.",
    "table2_between_within": "**Table 2.** Drug against its own indication: correlation between "
                             "areas and within areas over time.",
    "table3_indication_controls": "**Table 3.** Positive controls at area and practice level "
                                  "(z statistics).",
    "table4_top_hits": "**Table 4.** Strongest candidates in the whole scan after requiring the "
                       "year-before association to beat the year-after one.",
    "table5_top_disease_hits": "**Table 5.** The same filter restricted to disease outcomes.",
}


def md_table(name):
    path = HERE / "tables" / f"{name}.csv"
    if not path.exists():
        return f"*[table {name} not generated]*"
    d = pd.read_csv(path)
    head = "| " + " | ".join(str(c) for c in d.columns) + " |"
    rule = "|" + "|".join([":---"] + ["---:"] * (len(d.columns) - 1)) + "|"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join([TITLES.get(name, ""), "", head, rule] + body)


def fill(text):
    text = re.sub(r"\{\{table:([\w]+)\}\}", lambda m: md_table(m.group(1)), text)

    def figure(m):
        src, caption = CAPTIONS[m.group(1)]
        return f"![{caption}](figures/{src})\n\n{caption}"
    return re.sub(r"\{\{figure:([\w]+)\}\}", figure, text)


def main():
    body = "\n\n".join(fill((HERE / s).read_text()) for s in SECTIONS)
    avail = ("\n\n## Data and code availability\n\nAll inputs are public: NHSBSA English "
             "Prescribing Dataset, OHID Fingertips, NHS Digital practice registration counts and "
             "NHS England Organisation Data Service. Code, processed datasets, the full scan "
             "results and the tuberculosis supplement are at "
             "https://github.com/drcjar/tb-prescribing-england\n")
    out = HERE / "manuscript.md"
    out.write_text(body + avail)
    words = len(re.sub(r"\|[^\n]*\|", "", body.split("## Introduction", 1)[1]).split())
    for fmt in ("docx", "pdf"):
        try:
            subprocess.run(["pandoc", "manuscript.md", "-o", f"manuscript.{fmt}"],
                           cwd=HERE, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"  {fmt} build failed: {e.stderr.decode()[:200]}")
    print(f"wrote {out} | main text ~{words} words")


if __name__ == "__main__":
    main()
