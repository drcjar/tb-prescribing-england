"""Extend the practice-level prescribing panel back to August 2010 using HSCIC (NHS Digital)
Practice Level Prescribing Data (PDPI), available monthly Aug 2010 - Dec 2013.

Each month is downloaded, aggregated to practice x month with the same revised drug groups as the
EPD extraction (drug_groups.py: BNF chemical code, chemical name and presentation rules) and written
to data/raw/epd_practice_monthly_v2/epd_practice_{ym}.csv in the EPD extraction format. ADQ is not
available in PDPI (adq_* columns left empty). Raw files are deleted after processing, including on
failure, and outputs are written atomically.

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

from drug_groups import DRUG_GROUPS, pandas_mask, pandas_pred_equivalent_mg

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "pre2014"
OUT = ROOT / "data" / "raw" / "epd_practice_monthly_v2"


def load_inventory():
    inv = pd.read_csv(RAW / "pre2014_file_inventory.csv", dtype=str)
    return {ym: g.set_index("kind").url.to_dict() for ym, g in inv.groupby("yyyymm")}


def fetch(url, dest):
    subprocess.run(["curl", "-sSfL", "--retry", "5", "-o", str(dest), url], check=True)


def aggregate(pdpi_fh, chem_fh, ym, chunksize=2_000_000):
    """Practice totals by drug group. The PDPI file (~10M rows) is read in chunks to bound memory."""
    chem = pd.read_csv(chem_fh, dtype=str, skipinitialspace=True)
    chem_names = dict(zip(chem.iloc[:, 0].str.strip(), chem.iloc[:, 1].str.strip()))
    item_cols = ["items_total"] + [f"items_{g}" for g in DRUG_GROUPS] + ["mg_pred_equivalent"]
    parts = []
    reader = pd.read_csv(pdpi_fh, dtype=str, skipinitialspace=True, chunksize=chunksize,
                         usecols=lambda c: c.strip() in {"PRACTICE", "BNF CODE", "BNF NAME", "ITEMS", "QUANTITY"})
    for chunk in reader:
        chunk.columns = [c.strip() for c in chunk.columns]
        practice = chunk.PRACTICE.str.strip()
        code = chunk["BNF CODE"].str.strip().str[:9]
        presentation = chunk["BNF NAME"].str.strip()
        items = chunk.ITEMS.str.strip().astype(int)
        quantity = pd.to_numeric(chunk.QUANTITY.str.strip(), errors="coerce").fillna(0)
        name = code.map(chem_names).fillna("")
        part = pd.DataFrame({"PRACTICE": practice, "items_total": items})
        for group, rule in DRUG_GROUPS.items():
            part[f"items_{group}"] = items.where(pandas_mask(rule, code, name, presentation), 0)
        ocs = pandas_mask(DRUG_GROUPS["oral_glucocorticoids"], code, name, presentation)
        part["mg_pred_equivalent"] = pandas_pred_equivalent_mg(name, presentation, quantity).where(ocs, 0)
        parts.append(part.groupby("PRACTICE")[item_cols].sum())
    out = pd.concat(parts).groupby(level=0).sum()
    out = out.reset_index().rename(columns={"PRACTICE": "PRACTICE_CODE"})
    for group in DRUG_GROUPS:
        out[f"adq_{group}"] = float("nan")
    out.insert(0, "YEAR_MONTH", int(ym))
    return out


def practice_postcodes(fh):
    a = pd.read_csv(fh, header=None, dtype=str).iloc[:, :8]
    a.columns = ["PERIOD", "PRACTICE_CODE", "name", "addr1", "addr2", "town", "county", "POSTCODE"]
    return a.apply(lambda s: s.str.strip())[["PRACTICE_CODE", "POSTCODE"]].drop_duplicates("PRACTICE_CODE")


def process_month(ym, urls):
    downloads = []
    try:
        if "ZIP" in urls:
            z = RAW / f"{ym}.zip"
            downloads.append(z)
            fetch(urls["ZIP"], z)
            with zipfile.ZipFile(z) as zf:
                names = {re.search(r"(PDPI|ADDR|CHEM)", n).group(1): n for n in zf.namelist()
                         if re.search(r"(PDPI|ADDR|CHEM)", n)}
                with zf.open(names["PDPI"]) as p, zf.open(names["CHEM"]) as c:
                    agg = aggregate(io.TextIOWrapper(p, encoding="latin-1"), io.TextIOWrapper(c, encoding="latin-1"), ym)
                with zf.open(names["ADDR"]) as a:
                    postcodes = practice_postcodes(io.TextIOWrapper(a, encoding="latin-1"))
        else:
            paths = {kind: RAW / f"{ym}_{kind}.csv" for kind in ("PDPI", "ADDR", "CHEM")}
            downloads += list(paths.values())
            for kind, path in paths.items():
                fetch(urls[kind], path)
            agg = aggregate(paths["PDPI"], paths["CHEM"], ym)
            postcodes = practice_postcodes(paths["ADDR"])
    finally:
        for path in downloads:
            path.unlink(missing_ok=True)
    agg = agg.merge(postcodes, on="PRACTICE_CODE", how="left")
    lead = ["YEAR_MONTH", "PRACTICE_CODE", "POSTCODE", "items_total"]
    agg = agg[lead + [c for c in agg.columns if c not in lead]]
    path = OUT / f"epd_practice_{ym}.csv"
    agg.to_csv(path.with_suffix(".tmp"), index=False)
    path.with_suffix(".tmp").rename(path)
    return len(agg), int(agg.items_total.sum())


def main(start="201008", end="201312"):
    OUT.mkdir(parents=True, exist_ok=True)
    for ym, urls in sorted(load_inventory().items()):
        if not (start <= ym <= end) or (OUT / f"epd_practice_{ym}.csv").exists():
            continue
        try:
            n, items = process_month(ym, urls)
            print(ym, n, "practices", f"{items:,} items", flush=True)
        except Exception as exc:
            print(ym, "FAILED:", exc, flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
