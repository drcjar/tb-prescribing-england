"""Extract monthly practice-level prescribing for the revised drug groups (drug_groups.py),
January 2014 - December 2024, from the NHSBSA English Prescribing Dataset (EPD, BNF-coded series)
using server-side SQL. For each group: items and ADQ usage (populated for some BNF sections only);
for systemic oral glucocorticoids also prednisolone-equivalent mg. One cached CSV per month in
data/raw/epd_practice_monthly_v2/.

Usage: python fetch_prescribing_panel.py [START_YYYYMM] [END_YYYYMM]
"""
import io
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

from drug_groups import DRUG_GROUPS, sql_condition, sql_pred_equivalent_mg

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "epd_practice_monthly_v2"
OUT.mkdir(parents=True, exist_ok=True)
API = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql"

CODE, NAME, PRES = "BNF_CHEMICAL_SUBSTANCE", "CHEMICAL_SUBSTANCE_BNF_DESCR", "BNF_DESCRIPTION"


# ADQ usage is populated in the EPD only for some BNF sections (checked for January 2019)
ADQ_GROUPS = ["inhaled_corticosteroids", "proton_pump_inhibitors", "statins", "metformin", "fluoroquinolones",
              "all_antibacterials", "levothyroxine"]


def month_sql(resource):
    """Group flags are computed once per row in a subquery to keep the SQL short."""
    flags = [f"({sql_condition(rule, CODE, NAME, PRES)}) AS g_{group}" for group, rule in DRUG_GROUPS.items()]
    inner = (f"SELECT PRACTICE_CODE, POSTCODE, ITEMS, ADQUSAGE, "
             f"{sql_pred_equivalent_mg(NAME, PRES, 'TOTAL_QUANTITY')} AS mg, {', '.join(flags)} "
             f"FROM `{resource}` WHERE PRACTICE_CODE != '-' AND CAST(UNIDENTIFIED AS STRING) NOT IN ('true', 'Y')")
    cols = ["SUM(ITEMS) AS items_total"]
    cols += [f"SUM(IF(g_{group}, ITEMS, 0)) AS items_{group}" for group in DRUG_GROUPS]
    cols += [f"SUM(IF(g_{group}, ADQUSAGE, 0)) AS adq_{group}" for group in ADQ_GROUPS]
    cols.append("SUM(IF(g_oral_glucocorticoids, mg, 0)) AS mg_pred_equivalent")
    return f"SELECT PRACTICE_CODE, MAX(POSTCODE) AS POSTCODE, {', '.join(cols)} FROM ({inner}) GROUP BY PRACTICE_CODE"


def fetch_month(ym, sql_fn=month_sql, out_dir=OUT, prefix="epd_practice", retries=5):
    path = out_dir / f"{prefix}_{ym}.csv"
    if path.exists():
        return ym, "cached"
    resource = f"EPD_{ym}"
    for attempt in range(retries):
        try:
            # POST: the SQL for all drug groups is too long for a GET URL (HTTP 414)
            r = requests.post(API, json={"resource_id": resource, "sql": sql_fn(resource)}, timeout=600)
            r.raise_for_status()
            res = r.json()["result"]
            if "gc_urls" in res:
                parts = [pd.read_csv(io.BytesIO(requests.get(u["url"].replace("`", "%60"), timeout=600).content),
                                     compression="gzip") for u in res["gc_urls"]]
                df = pd.concat(parts)
            else:
                df = pd.DataFrame(res["result"]["records"])
            if df.empty:
                raise ValueError("no records returned")
            df.insert(0, "YEAR_MONTH", ym)
            tmp = path.with_suffix(".tmp")
            df.to_csv(tmp, index=False)
            tmp.rename(path)
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
