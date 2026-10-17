"""Area x year x BNF-section prescribing rates, apportioned to where patients live.

Reuses the practice restriction, residence shares and area merges from build_panel.py, but
keeps all ~194 BNF sections instead of 15 curated groups. Apportionment is done as a sparse
matrix product (practices x areas)^T (practices x sections), one year at a time, so memory
stays small.

Usage: python build_wide_exposure.py [utla|ltla]
Writes data/processed/{level}_section_exposure.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

from build_panel import MERGES, RESIDENCE_SHARES, gp_practice_masks, lad_to_area, population

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / "data" / "raw" / "epd_practice_section"
OUT = ROOT / "data" / "processed"
YEARS = range(2014, 2025)


def year_practice_sections(year):
    """practice x section item totals for one calendar year (only complete years)."""
    files = sorted(SECTIONS.glob(f"epd_section_{year}??.csv.gz"))
    if len(files) < 12:
        return None
    frames = []
    for f in files:
        d = pd.read_csv(f, dtype={"PRACTICE_CODE": str, "bnf_section": str})
        d["bnf_section"] = d.bnf_section.astype(str).str.zfill(4)  # "601" -> "0601"
        frames.append(d.groupby(["PRACTICE_CODE", "bnf_section"], as_index=False)["items"].sum())
    d = pd.concat(frames, ignore_index=True)
    return d.groupby(["PRACTICE_CODE", "bnf_section"], as_index=False)["items"].sum()


def share_matrix(practices, year, shares, lad_area):
    """sparse practices x areas matrix of residence shares, using the nearest release year."""
    avail = np.array(sorted(shares.share_year.unique()))
    use = avail[np.argmin(np.abs(avail - year))]
    s = shares[shares.share_year == use].copy()
    s["area"] = s.lad23cd.replace(MERGES["ltla"]).map(lad_area)
    s = s.dropna(subset=["area"])
    areas = sorted(s.area.unique())
    pi = {p: i for i, p in enumerate(practices)}
    ai = {a: i for i, a in enumerate(areas)}
    s = s[s.PRACTICE_CODE.isin(pi)]
    m = sparse.csr_matrix((s.share.to_numpy(),
                           (s.PRACTICE_CODE.map(pi).to_numpy(), s.area.map(ai).to_numpy())),
                          shape=(len(practices), len(areas)))
    return m, areas


def main(level="utla"):
    lad_area = lad_to_area(level)
    shares = pd.read_csv(RESIDENCE_SHARES, dtype={"practice_code": str}).rename(
        columns={"practice_code": "PRACTICE_CODE", "year": "share_year"})
    out = []
    for year in YEARS:
        d = year_practice_sections(year)
        if d is None:
            print(f"{year}: incomplete, skipped", flush=True)
            continue
        _, gp = gp_practice_masks(d.PRACTICE_CODE)
        d = d[gp]
        practices = sorted(d.PRACTICE_CODE.unique())
        sections = sorted(d.bnf_section.unique())
        pi = {p: i for i, p in enumerate(practices)}
        si = {s: i for i, s in enumerate(sections)}
        P = np.zeros((len(practices), len(sections)))
        P[d.PRACTICE_CODE.map(pi).to_numpy(), d.bnf_section.map(si).to_numpy()] = d["items"].to_numpy()
        S, areas = share_matrix(practices, year, shares, lad_area)
        A = S.T @ P  # areas x sections, items apportioned by patient residence
        frame = pd.DataFrame(A, index=areas, columns=sections)
        frame.insert(0, "year", year)
        frame.index.name = "utla"
        out.append(frame.reset_index())
        print(f"{year}: {len(practices):,} practices, {len(sections)} sections, {len(areas)} areas", flush=True)
    wide = pd.concat(out, ignore_index=True)
    pop = population(lad_area, level).reset_index()[["utla", "year", "population"]]
    wide = wide.merge(pop, on=["utla", "year"], how="left")
    cols = [c for c in wide.columns if c not in ("utla", "year", "population")]
    wide[cols] = wide[cols].div(wide.population, axis=0) * 1000  # items per 1,000 residents
    path = OUT / f"{level}_section_exposure.csv"
    wide.to_csv(path, index=False)
    print(f"wrote {path}: {len(wide)} area-years x {len(cols)} sections", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:2])
