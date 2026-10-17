"""Hypothesis-free prescribing extract: practice x month x BNF section items, 2014-2024.

Unlike fetch_prescribing_panel.py (15 curated drug groups), this pulls every BNF section
(~194) so that prescribing can be scanned against many disease outcomes without picking
drugs in advance. Server-side SQL aggregates to practice x section; one gzipped file per
month keeps memory and disk small.

Usage: python fetch_prescribing_wide.py [workers]
"""
import io
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "epd_practice_section"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql"
MONTHS = [f"{y}{m:02d}" for y in range(2014, 2025) for m in range(1, 13)]


def month_sql(resource):
    # BNF code: chapter(2) + section(2); SUBSTR(...,1,4) is the section, e.g. 0603 corticosteroids
    return (f"SELECT PRACTICE_CODE, SUBSTR(BNF_CHEMICAL_SUBSTANCE,1,4) AS bnf_section, "
            f"SUM(ITEMS) AS items FROM `{resource}` "
            f"WHERE PRACTICE_CODE != '-' AND CAST(UNIDENTIFIED AS STRING) NOT IN ('true', 'Y') "
            f"GROUP BY PRACTICE_CODE, bnf_section")


def fetch_month(ym, retries=5):
    path = OUT / f"epd_section_{ym}.csv.gz"
    if path.exists():
        return ym, "cached"
    resource = f"EPD_{ym}"
    for attempt in range(retries):
        try:
            r = requests.post(API, json={"resource_id": resource, "sql": month_sql(resource)}, timeout=900)
            r.raise_for_status()
            res = r.json()["result"]
            if "gc_urls" in res:  # >32k rows come back as gzipped parts; backticks must be %60-encoded
                parts = [pd.read_csv(io.BytesIO(requests.get(u["url"].replace("`", "%60"), timeout=900).content),
                                     compression="gzip", dtype={"PRACTICE_CODE": str, "bnf_section": str}) for u in res["gc_urls"]]
                df = pd.concat(parts, ignore_index=True)
            else:
                df = pd.DataFrame(res["result"]["records"])
            if df.empty:
                raise ValueError("no records returned")
            df["items"] = pd.to_numeric(df["items"], errors="coerce")
            df["bnf_section"] = df["bnf_section"].astype(str).str.zfill(4)
            df = df.dropna(subset=["bnf_section"])
            df.insert(0, "YEAR_MONTH", int(ym))
            tmp = path.with_suffix(".tmp")
            df.to_csv(tmp, index=False, compression="gzip")
            tmp.rename(path)
            return ym, f"{len(df):,} rows, {df.PRACTICE_CODE.nunique():,} practices"
        except Exception as exc:
            if attempt == retries - 1:
                return ym, f"FAILED: {exc}"
            time.sleep(10 * (attempt + 1))


def main(workers=3):
    todo = [m for m in MONTHS if not (OUT / f"epd_section_{m}.csv.gz").exists()]
    print(f"{len(todo)} of {len(MONTHS)} months to fetch, {workers} workers", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for ym, msg in ex.map(fetch_month, todo):
            print(f"{ym}: {msg}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
