"""Assemble the BMJ Open submission from the condensed section files.

Outputs (paper/submission/build/):
  manuscript_bmjopen.md/.docx  - title page, abstract, strengths box, main text, statements,
                                 numbered (Vancouver) references, figure legends
  supplementary_bmjopen.md/.docx - supplementary tables S1-S9 and supplementary figures

Citations are written in the section files as [Author Year] and renumbered here in order of first
appearance, so the prose stays readable while the submission uses Vancouver style.

Usage: python paper/submission/assemble_submission.py
"""
import re
import shutil
import subprocess
from pathlib import Path

SUB = Path(__file__).resolve().parent
PAPER = SUB.parent
ROOT = PAPER.parent
BUILD = SUB / "build"

SECTIONS = ["abstract.md", "introduction.md", "methods.md", "results.md", "discussion.md"]

# main paper display items (BMJ Open expects a small number; the rest go to the supplement)
FIGURES = {
    1: ("dag.png", "Assumed causal structure for area-level prescribing and TB notifications. Area fixed effects "
        "absorb stable area characteristics; year fixed effects absorb national shocks; time-varying measured "
        "factors are adjusted for; dashed nodes are unmeasured."),
    2: ("within_between_variation.png", "Within-area versus between-area variation in log prescribing rates, 294 "
        "lower-tier local authorities, 2014-2024. Orange line: a 10% increase."),
    3: ("panel_forest_ltla_residence.png", "Primary care prescribing and TB notifications, lower-tier local "
        "authorities, prescribing apportioned by patient residence. Blue: prescribing in the previous year "
        "(primary analysis). Orange: prescribing in the following year, estimated jointly (falsification test)."),
    4: ("hospital_positive_control.png", "Positive control: hospital treatment for active TB (pyrazinamide "
        "DDD-years per 1,000 residents) and TB notifications, between areas (left) and within areas over time "
        "(right)."),
}
SUPP_FIGURES = {
    "S1": ("ocs_national_trends.png", "Oral glucocorticoid prescribing in English primary care, 2011-2024."),
    "S2": ("ocs_ukborn_tb_by_region.png", "Oral glucocorticoid prescribing and UK-born TB notification rates by "
           "region, indexed to 2014 = 100."),
}
MAIN_TABLES = ["table1_primary_care_panel", "table2_mde"]
SUPP_TABLES = ["table3_hospital", "tableS1_sensitivity", "tableS2_distributed_lag", "tableS2b_lag_same_lead",
               "tableS3_hospital_mde", "tableS3b_hospital_sensitivity", "tableS4_power_simulation",
               "tableS5_regional", "tableS6_regional_lag_lead", "tableS7_hospital_coverage",
               "tableS8_original_design", "tableS9_drug_groups"]

# citation key -> a string that uniquely identifies the reference entry in references_v3_verified.md
PINNED = {
    "BTS 2005": "British Thoracic Society",
    "NG33": "National Institute for Health and Care Excellence",
    "RECOVERY 2021": "RECOVERY Collaborative Group",
    "UKHSA 2021": "2021 report",
    "UKHSA 2025": "2025 report",
    "UKHSA 2026": "Tuberculosis notifications in England stabilise",
    "OpenPrescribing 2026": "OpenPrescribing.net, Bennett Institute",
    "Santos Silva 2006": "Santos Silva",
}


def reference_entries():
    return [l[2:].strip() for l in (PAPER / "references_v3_verified.md").read_text().splitlines()
            if l.startswith("- ")]


def match_entry(key, entries):
    if key in PINNED:
        hits = [e for e in entries if PINNED[key] in e]
    else:
        author, year = key.rsplit(" ", 1)
        hits = [e for e in entries if e.startswith(author.split()[0]) and year in e]
    if len(hits) != 1:
        raise SystemExit(f"citation key {key!r} matched {len(hits)} reference entries")
    return hits[0]


def renumber(text, entries):
    """Replace [Author Year] citations with Vancouver numbers, in order of first appearance."""
    order, used = {}, []

    def repl(m):
        inner = m.group(1)
        if not re.search(r"(19|20)\d\d|NG33", inner) or "http" in inner:
            return m.group(0)
        numbers = []
        for part in re.split(r";\s*", inner):
            key = re.sub(r",\s*Supplementary Table \d+", "", part.strip())
            if key not in order:
                order[key] = len(order) + 1
                used.append(match_entry(key, entries))
            numbers.append(str(order[key]))
        return "[" + ",".join(numbers) + "]"

    return re.sub(r"\[([^\]\[]+)\]", repl, text), used


def table(name):
    path = PAPER / "tables" / f"{name}.md"
    return path.read_text() if path.exists() else f"*[table {name} not generated]*"


def main():
    BUILD.mkdir(exist_ok=True)
    entries = reference_entries()
    body = "\n\n".join((SUB / s).read_text() for s in SECTIONS)
    for n, (_, caption) in FIGURES.items():
        body = body.replace(f"(figure {n})", f"(figure {n})")  # captions listed at the end, per BMJ style
    body, used = renumber(body, entries)

    words = len(re.sub(r"\|[^\n]*\|", "", body.split("## Introduction", 1)[1]).split())
    abstract_words = len(body.split("## Abstract", 1)[1].split("## Strengths")[0].split())
    title = (SUB / "title_page.md").read_text().replace(
        "Main text: [filled at assembly]", f"Main text: {words} words").replace(
        "Abstract: [filled at assembly]", f"Abstract: {abstract_words} words")

    refs = "## References\n\n" + "\n".join(f"{i}. {e}" for i, e in enumerate(used, 1)) + "\n"
    tables = "## Tables\n\n" + "\n\n".join(table(t) for t in MAIN_TABLES)
    legends = "## Figure legends\n\n" + "\n\n".join(
        f"**Figure {n}.** {caption}" for n, (_, caption) in FIGURES.items())
    manuscript = "\n\n".join([title, body, tables, legends, refs])
    (BUILD / "manuscript_bmjopen.md").write_text(manuscript)

    supp = ["# Supplementary material", "", "Study: Can open prescribing data detect effects of medicines on "
            "tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in "
            "England, 2011-2024.", "", "## Supplementary tables", ""]
    supp += [table(t) for t in SUPP_TABLES]
    supp += ["## Supplementary figures", ""]
    supp += [f"**Figure {k}.** {caption}\n\n![Figure {k}](figures/{src})" for k, (src, caption) in SUPP_FIGURES.items()]
    supp += ["## Reporting checklist", "",
             "The completed RECORD checklist (paper/submission/record_checklist.md) is uploaded as a separate file."]
    (BUILD / "supplementary_bmjopen.md").write_text("\n\n".join(supp))

    figdir = BUILD / "figures"
    figdir.mkdir(exist_ok=True)
    for src, _ in list(FIGURES.values()) + list(SUPP_FIGURES.values()):
        shutil.copy(PAPER / "figures" / src, figdir / src)

    for name in ("manuscript_bmjopen", "supplementary_bmjopen"):
        subprocess.run(["pandoc", f"{name}.md", "-o", f"{name}.docx"], cwd=BUILD, check=True)

    print(f"main text {words} words; abstract {abstract_words} words; {len(used)} references")
    print("wrote", BUILD / "manuscript_bmjopen.docx", "and", BUILD / "supplementary_bmjopen.docx")


if __name__ == "__main__":
    main()
