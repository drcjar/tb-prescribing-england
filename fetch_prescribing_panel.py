"""Extract monthly practice-level prescribing items for the pre-specified drug groups,
January 2014 - December 2024, from the NHSBSA English Prescribing Dataset (EPD, BNF-coded
series) using server-side SQL. One cached CSV per month in data/raw/epd_practice_monthly/.

Usage: python fetch_prescribing_panel.py [START_YYYYMM] [END_YYYYMM]
"""
import io
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

from build_dataset import DRUG_GROUPS, EXCLUDE_CHAPTERS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "epd_practice_monthly"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql"

CODE, NAME = "BNF_CHEMICAL_SUBSTANCE", "CHEMICAL_SUBSTANCE_BNF_DESCR"


def group_condition(rule):
    conds = [f"NOT REGEXP_CONTAINS({CODE}, r'{EXCLUDE_CHAPTERS}')"]
    if "code" in rule:
        conds.append(f"REGEXP_CONTAINS({CODE}, r'{rule['code']}')")
    if "name" in rule:
        conds.append(f"REGEXP_CONTAINS(LOWER({NAME}), r'{rule['name']}')")
    return " AND ".join(conds)


def month_sql(resource):
    sums = ",\n".join(f"SUM(CASE WHEN {group_condition(rule)} THEN ITEMS ELSE 0 END) AS items_{group}"
                      for group, rule in DRUG_GROUPS.items())
    return (f"SELECT PRACTICE_CODE, MAX(POSTCODE) AS POSTCODE, SUM(ITEMS) AS items_total,\n{sums}\n"
            f"FROM `{resource}` WHERE PRACTICE_CODE != '-' "
            f"AND CAST(UNIDENTIFIED AS STRING) NOT IN ('true', 'Y') GROUP BY PRACTICE_CODE")


def fetch_month(ym, sql_fn=month_sql, out_dir=OUT, prefix="epd_practice", retries=5):
    path = out_dir / f"{prefix}_{ym}.csv"
    if path.exists():
        return ym, "cached"
    resource = f"EPD_{ym}"
    for attempt in range(retries):
        try:
            r = requests.get(API, params={"resource_id": resource, "sql": sql_fn(resource)}, timeout=600)
            r.raise_for_status()
            res = r.json()["result"]
            if "gc_urls" in res:
                parts = [pd.read_csv(io.BytesIO(requests.get(u["url"], timeout=600).content), compression="gzip")
                         for u in res["gc_urls"]]
                df = pd.concat(parts)
            else:
                df = pd.DataFrame(res["result"]["records"])
            if df.empty:
                raise ValueError("no records returned")
            df.insert(0, "YEAR_MONTH", ym)
            df.to_csv(path, index=False)
            return ym, f"{len(df)} practices"
        except Exception as exc:  # network / API hiccups: back off and retry
            if attempt == retries - 1:
                return ym, f"FAILED: {exc}"
            time.sleep(10 * (attempt + 1))


def months(start, end):
    y, m = divmod(int(start), 100)
    while y * 100 + m <= int(end):
        yield f"{y}{m:02d}"
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def main():
    start, end = (sys.argv[1:3] + ["201401", "202412"][len(sys.argv[1:3]):])
    todo = list(months(start, end))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for fut in as_completed([pool.submit(fetch_month, ym) for ym in todo]):
            ym, status = fut.result()
            print(ym, status, flush=True)


if __name__ == "__main__":
    main()
