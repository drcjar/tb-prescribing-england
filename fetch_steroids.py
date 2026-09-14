"""Extract monthly practice-level oral corticosteroid (BNF 6.3.2) prescribing, Jan 2014 - Dec 2024:
items by substance (prednisolone, dexamethasone, hydrocortisone, other) and ADQ usage, from the
NHSBSA EPD (BNF-coded series). One cached CSV per month in data/raw/epd_steroids_monthly/.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import fetch_prescribing_panel as fp

OUT = fp.ROOT / "data" / "raw" / "epd_steroids_monthly"
OUT.mkdir(parents=True, exist_ok=True)

OCS = "REGEXP_CONTAINS(BNF_CHEMICAL_SUBSTANCE, r'^0603020')"
SUBSTANCES = {
    "prednisolone": r"^prednisolone",
    "dexamethasone": r"^dexamethasone",
    "hydrocortisone": r"^hydrocortisone",
}


# ADQUSAGE is not populated for corticosteroids in the BNF-coded EPD, so dose is derived for
# prednisolone solid oral forms: tablets dispensed x strength parsed from the presentation name.
PRED_TABLET_MG = (r"SAFE_CAST(REGEXP_EXTRACT(LOWER(BNF_DESCRIPTION), "
                  r"r'^prednisolone (\d+(?:\.\d+)?)mg (?:gastro-resistant |soluble )?tablets') AS FLOAT64)")


def steroid_sql(resource):
    cols = [f"SUM(CASE WHEN {OCS} THEN ITEMS ELSE 0 END) AS items_ocs",
            f"SUM(CASE WHEN {OCS} THEN TOTAL_QUANTITY * {PRED_TABLET_MG} ELSE 0 END) AS mg_prednisolone_tablets",
            f"SUM(CASE WHEN {OCS} AND {PRED_TABLET_MG} IS NOT NULL THEN ITEMS ELSE 0 END) AS items_prednisolone_tablets"]
    for name, pattern in SUBSTANCES.items():
        cond = f"{OCS} AND REGEXP_CONTAINS(LOWER(CHEMICAL_SUBSTANCE_BNF_DESCR), r'{pattern}')"
        cols.append(f"SUM(CASE WHEN {cond} THEN ITEMS ELSE 0 END) AS items_{name}")
    return (f"SELECT PRACTICE_CODE, MAX(POSTCODE) AS POSTCODE, {', '.join(cols)} "
            f"FROM `{resource}` WHERE PRACTICE_CODE != '-' "
            f"AND CAST(UNIDENTIFIED AS STRING) NOT IN ('true', 'Y') GROUP BY PRACTICE_CODE")


def main():
    todo = list(fp.months("201401", "202412"))
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(fp.fetch_month, ym, steroid_sql, OUT, "epd_steroids") for ym in todo]
        for fut in as_completed(futures):
            print(*fut.result(), flush=True)


if __name__ == "__main__":
    main()
