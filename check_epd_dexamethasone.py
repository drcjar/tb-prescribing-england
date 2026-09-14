"""Two checks on the NHSBSA EPD extraction (peer review, round 2):
1. share of prednisolone-equivalent mg in the systemic oral glucocorticoid group contributed by each
   chemical substance (dexamethasone has potency 6.67), national, selected months;
2. number of rows with a NULL UNIDENTIFIED flag, which the extraction filter would silently drop.

Usage: python check_epd_dexamethasone.py
Writes outputs/descriptives/epd_glucocorticoid_mg_by_substance.csv
"""
from pathlib import Path

import pandas as pd
import requests

from drug_groups import DRUG_GROUPS, sql_condition, sql_pred_equivalent_mg
from fetch_prescribing_panel import API, CODE, NAME, PRES

ROOT = Path(__file__).resolve().parent
MONTHS = ["201501", "201907", "202407"]


def query(resource, sql):
    r = requests.post(API, json={"resource_id": resource, "sql": sql}, timeout=600)
    r.raise_for_status()
    result = r.json()["result"]
    records = result.get("result", {}).get("records") if isinstance(result.get("result"), dict) else result.get("records")
    if records is None:
        raise RuntimeError(f"unexpected response keys: {list(result)}")
    return pd.DataFrame(records)


def main():
    rows, nulls = [], []
    condition = sql_condition(DRUG_GROUPS["oral_glucocorticoids"], CODE, NAME, PRES)
    for ym in MONTHS:
        resource = f"EPD_{ym}"
        sql = (f"SELECT {NAME} AS substance, SUM(ITEMS) AS items, SUM(mg) AS mg FROM (SELECT {NAME}, ITEMS, "
               f"{sql_pred_equivalent_mg(NAME, PRES, 'TOTAL_QUANTITY')} AS mg, ({condition}) AS g FROM `{resource}` "
               f"WHERE PRACTICE_CODE != '-') WHERE g GROUP BY {NAME}")
        d = query(resource, sql).assign(month=ym)
        d[["items", "mg"]] = d[["items", "mg"]].apply(pd.to_numeric)
        d["mg_share_pct"] = 100 * d.mg / d.mg.sum()
        d["items_share_pct"] = 100 * d["items"] / d["items"].sum()
        rows.append(d)
        n = query(resource, f"SELECT COUNT(*) AS n_null FROM `{resource}` WHERE UNIDENTIFIED IS NULL")
        nulls.append((ym, int(n.iloc[0, 0])))
    out = pd.concat(rows)
    out.to_csv(ROOT / "outputs" / "descriptives" / "epd_glucocorticoid_mg_by_substance.csv", index=False)
    print(out.round(2).to_string(index=False))
    print("Rows with NULL UNIDENTIFIED:", nulls)


if __name__ == "__main__":
    main()
