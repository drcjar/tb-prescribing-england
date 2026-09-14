"""Hospital negative-control exposure for the SCMD analysis: levetiracetam (anti-epileptic; high
hospital volume, similar urban/teaching-hospital geography to other hospital-issued medicines, no
plausible causal link with TB). Reuses the extraction helpers in fetch_scmd.py with a separate
search term, month cache and outputs, so the main SCMD extraction files are not touched.

Output: data/raw/scmd/scmd_negative_control_trust_month.csv
        (year_month, ods_code, group, approx_mg, indicative_cost, source)
"""
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

import fetch_scmd as fs

TERM = "levetiracetam"


def main():
    fs.ALL_TERMS = [TERM]
    fs.CACHE = fs.OUT / "months_negative_control"
    fs.CACHE.mkdir(parents=True, exist_ok=True)
    use = fs.resources()
    with ThreadPoolExecutor(4) as ex:
        raw = pd.concat(list(ex.map(fs.get_month, use.to_dict("records"))), ignore_index=True)
    raw["YEAR_MONTH"] = raw.YEAR_MONTH.astype(str).str.replace("-", "").astype(int)
    raw["UNIT"] = raw.UNIT.astype(str).str.upper()
    mgu = {k: fs.approx_mg_per_unit(*k) for k in raw[["VMP_PRODUCT_NAME", "UNIT"]].drop_duplicates().itertuples(index=False)}
    raw["approx_mg"] = raw.QTY * [mgu[k] for k in zip(raw.VMP_PRODUCT_NAME, raw.UNIT)]
    out = (raw.groupby(["YEAR_MONTH", "ODS_CODE"], as_index=False)
              .agg(approx_mg=("approx_mg", "sum"), indicative_cost=("COST", "sum"), source=("source", "first"))
              .rename(columns={"YEAR_MONTH": "year_month", "ODS_CODE": "ods_code"})
              .assign(group="negative_control_levetiracetam"))
    out.to_csv(fs.OUT / "scmd_negative_control_trust_month.csv", index=False)
    print(len(raw), "product rows;", out.ods_code.nunique(), "trusts;", out.year_month.nunique(), "months")


if __name__ == "__main__":
    main()
