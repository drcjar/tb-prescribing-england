"""Extend the practice-level prescribing panel back to August 2010 using NHS Digital (HSCIC)
Practice Level Prescribing Data (PDPI), which is available monthly Aug 2010 - Dec 2013.

Each month is downloaded, aggregated to practice x month using the same pre-specified drug groups
as the EPD extraction (build_dataset.DRUG_GROUPS: BNF chemical code and/or chemical name rules,
excluding BNF chapters 11-13), and written to data/raw/epd_practice_monthly/epd_practice_{ym}.csv
in the same format as fetch_prescribing_panel.py. Raw files are deleted after processing.

Source inventory: data/raw/pre2014/pre2014_file_inventory.csv (data.gov.uk package
176ae264-2484-4afe-a297-d51798eb8228). Monthly zips (~250 MB) contain PDPI, ADDR and CHEM files;
three months (201110, 201206, 201303) are fetched as separate CSVs.

Usage: python fetch_pre2014_practice.py [START_YYYYMM] [END_YYYYMM]
"""
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import pandas as pd

from build_dataset import DRUG_GROUPS, EXCLUDE_CHAPTERS

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "pre2014"
OUT = ROOT / "data" / "raw" / "epd_practice_monthly"


def load_inventory():
    inv = pd.read_csv(RAW / "pre2014_file_inventory.csv", dtype=str)
    return {ym: g.set_index("kind").url.to_dict() for ym, g in inv.groupby("yyyymm")}


def fetch(url, dest):
    subprocess.run(["curl", "-sSfL", "--retry", "5", "-o", str(dest), url], check=True)


def read_csv_stripped(fh, **kwargs):
    df = pd.read_csv(fh, dtype=str, skipinitialspace=True, **kwargs)
    df.columns = [str(c).strip() for c in df.columns]
    return df.apply(lambda s: s.str.strip())


def aggregate(pdpi_fh, chem_fh, ym, chunksize=2_000_000):
    """Practice totals by drug group. The PDPI file (~10M rows) is read in chunks to bound memory."""
    chem = read_csv_stripped(chem_fh)
    chem_names = dict(zip(chem.iloc[:, 0], chem.iloc[:, 1]))
    item_cols = ["items_total"] + [f"items_{g}" for g in DRUG_GROUPS]
    parts = []
    reader = pd.read_csv(pdpi_fh, dtype=str, skipinitialspace=True, chunksize=chunksize,
                         usecols=lambda c: c.strip() in {"PRACTICE", "BNF CODE", "ITEMS"})
    for chunk in reader:
        chunk.columns = [c.strip() for c in chunk.columns]
        practice = chunk.PRACTICE.str.strip()
        code = chunk["BNF CODE"].str.strip().str[:9]
        items = chunk.ITEMS.str.strip().astype(int)
        name = code.map(chem_names).fillna("").str.lower()
        part = pd.DataFrame({"PRACTICE": practice, "items_total": items})
        for group, rule in DRUG_GROUPS.items():
            mask = ~code.str.match(EXCLUDE_CHAPTERS)
            if "code" in rule:
                mask &= code.str.match(rule["code"])
            if "name" in rule:
                mask &= name.str.contains(rule["name"], regex=True)
            part[f"items_{group}"] = items.where(mask, 0)
        parts.append(part.groupby("PRACTICE")[item_cols].sum())
    out = pd.concat(parts).groupby(level=0).sum().astype(int)
    out = out.reset_index().rename(columns={"PRACTICE": "PRACTICE_CODE"})
    out.insert(0, "YEAR_MONTH", int(ym))
    return out


def practice_postcodes(fh):
    a = pd.read_csv(fh, header=None, dtype=str).iloc[:, :8]
    a.columns = ["PERIOD", "PRACTICE_CODE", "name", "addr1", "addr2", "town", "county", "POSTCODE"]
    return a.apply(lambda s: s.str.strip())[["PRACTICE_CODE", "POSTCODE"]].drop_duplicates("PRACTICE_CODE")


def process_month(ym, urls):
    if "ZIP" in urls:
        z = RAW / f"{ym}.zip"
        fetch(urls["ZIP"], z)
        with zipfile.ZipFile(z) as zf:
            names = {re.search(r"(PDPI|ADDR|CHEM)", n).group(1): n for n in zf.namelist()
                     if re.search(r"(PDPI|ADDR|CHEM)", n)}
            with zf.open(names["PDPI"]) as p, zf.open(names["CHEM"]) as c:
                agg = aggregate(io.TextIOWrapper(p, encoding="latin-1"), io.TextIOWrapper(c, encoding="latin-1"), ym)
            with zf.open(names["ADDR"]) as a:
                postcodes = practice_postcodes(io.TextIOWrapper(a, encoding="latin-1"))
        z.unlink()
    else:
        paths = {kind: RAW / f"{ym}_{kind}.csv" for kind in ("PDPI", "ADDR", "CHEM")}
        for kind, path in paths.items():
            fetch(urls[kind], path)
        agg = aggregate(paths["PDPI"], paths["CHEM"], ym)
        postcodes = practice_postcodes(paths["ADDR"])
        for path in paths.values():
            path.unlink()
    agg = agg.merge(postcodes, on="PRACTICE_CODE", how="left")
    cols = ["YEAR_MONTH", "PRACTICE_CODE", "POSTCODE", "items_total"] + [f"items_{g}" for g in DRUG_GROUPS]
    agg[cols].to_csv(OUT / f"epd_practice_{ym}.csv", index=False)
    return len(agg), int(agg.items_total.sum())


def main(start="201008", end="201312"):
    OUT.mkdir(parents=True, exist_ok=True)
    for ym, urls in sorted(load_inventory().items()):
        if not (start <= ym <= end) or (OUT / f"epd_practice_{ym}.csv").exists():
            continue
        n, items = process_month(ym, urls)
        print(ym, n, "practices", f"{items:,} items", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
