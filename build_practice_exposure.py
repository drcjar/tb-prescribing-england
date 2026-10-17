"""Practice x year x BNF-section prescribing, from the cached monthly section extracts.

No apportionment is needed here: the prescribing unit and the outcome unit are both the
practice, which is why this design has far more within-unit variation than the area panels.

Usage: python build_practice_exposure.py
Writes data/processed/practice_section_exposure.csv.gz (practice-years x sections, items)
"""
from pathlib import Path

import pandas as pd

from build_panel import gp_practice_masks

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / "data" / "raw" / "epd_practice_section"
OUT = ROOT / "data" / "processed"
YEARS = range(2014, 2025)


def main():
    frames = []
    for year in YEARS:
        files = sorted(SECTIONS.glob(f"epd_section_{year}??.csv.gz"))
        if len(files) < 12:
            print(f"{year}: only {len(files)} months, skipped", flush=True)
            continue
        parts = []
        for f in files:
            d = pd.read_csv(f, dtype={"PRACTICE_CODE": str, "bnf_section": str})
            d["bnf_section"] = d.bnf_section.astype(str).str.zfill(4)
            parts.append(d.groupby(["PRACTICE_CODE", "bnf_section"], as_index=False)["items"].sum())
        d = pd.concat(parts, ignore_index=True)
        d = d.groupby(["PRACTICE_CODE", "bnf_section"], as_index=False)["items"].sum()
        _, gp = gp_practice_masks(d.PRACTICE_CODE)
        d = d[gp]
        wide = d.pivot(index="PRACTICE_CODE", columns="bnf_section", values="items")
        wide.insert(0, "year", year)
        frames.append(wide.reset_index())
        print(f"{year}: {wide.shape[0]:,} practices x {wide.shape[1] - 1} sections", flush=True)
    out = pd.concat(frames, ignore_index=True).rename(columns={"PRACTICE_CODE": "practice"})
    path = OUT / "practice_section_exposure.csv.gz"
    out.to_csv(path, index=False, compression="gzip")
    print(f"wrote {path}: {len(out):,} practice-years x {out.shape[1] - 2} sections", flush=True)


if __name__ == "__main__":
    main()
