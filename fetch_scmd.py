"""Extract hospital (secondary care) medicines for TB-risk drug groups from NHSBSA SCMD.

Sources (NHSBSA Open Data Portal, CKAN):
  - finalised-secondary-care-medicines-data-scmd-with-indicative-price  (SCMD_FINAL_201904..202603)
  - secondary-care-medicines-data-indicative-price (provisional; used for months after last final)
  - secondary-care-medicines-data (RETIRED; used only for 201901-201903, no INDICATIVE_COST; CSV download)

Server-side SQL (datastore_search_sql) pulls trust x VMP x unit monthly totals for any VMP name
matching a candidate substance; classification, topical exclusion and dose derivation are done
locally so every match can be audited.

Outputs (data/raw/scmd/):
  scmd_trust_month_vmp.csv.gz        trust x month x VMP (all candidate matches, with excluded flag)
  scmd_trust_month_groups.csv        trust x month x group x unit (additive measures)
  scmd_trust_month_group_summary.csv trust x month x group (distinct VMPs, cost, approx mg, anti-TB doses)
  scmd_products_by_group.csv         group x substance x VMP x unit totals (audit listing)
"""
import io
import json
import re
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

BASE = "https://opendata.nhsbsa.net/api/3/action"
OUT = Path(__file__).parent / "data/raw/scmd"
CACHE = OUT / "months"
CACHE.mkdir(parents=True, exist_ok=True)

GROUPS = {
    "anti_tnf": ["adalimumab", "infliximab", "etanercept", "certolizumab", "golimumab"],
    "other_biologic": ["tocilizumab", "sarilumab", "rituximab", "abatacept", "ustekinumab",
                       "secukinumab", "ixekizumab", "vedolizumab", "anakinra"],
    "jak_inhibitor": ["tofacitinib", "baricitinib", "upadacitinib", "filgotinib", "ruxolitinib"],
    # methylprednisolone listed before prednisolone so it is matched first
    "systemic_corticosteroid": ["methylprednisolone", "dexamethasone", "prednisolone", "hydrocortisone"],
    "antituberculosis": ["rifampicin", "isoniazid", "pyrazinamide", "ethambutol", "rifinah", "rifater",
                         "voractiv", "rifapentine", "bedaquiline", "delamanid"],
    "calcineurin_antiproliferative": ["tacrolimus", "ciclosporin", "mycophenolate", "mycophenolic",
                                      "azathioprine", "methotrexate"],
}
ALL_TERMS = [t for ts in GROUPS.values() for t in ts]
# Specified exclusions (topical/eye/ear/inhaled etc.)
EXCL_SPEC = r"cream|ointment|\beye\b|\bear\b|drops|inhal|nasal|\bgel\b|foam|enema|suppositor|spray"
# Additional non-systemic forms excluded (documented)
EXCL_EXTRA = r"rectal|buccal|oromucosal|mouthwash|lozenge|intravitreal|implant|cutaneous|lotion|scalp|dental|paste|\botic\b|pellet"


def resources():
    rows = []
    for pkg, kind in [("finalised-secondary-care-medicines-data-scmd-with-indicative-price", "final"),
                      ("secondary-care-medicines-data-indicative-price", "provisional"),
                      ("secondary-care-medicines-data", "retired")]:
        res = requests.get(f"{BASE}/package_show", params={"id": pkg}, timeout=60).json()["result"]
        for r in res["resources"]:
            m = re.search(r"(\d{6})$", r["name"])
            if m:
                rows.append(dict(ym=int(m.group(1)), kind=kind, name=r["name"], id=r["id"], url=r["url"],
                                 datastore=bool(r.get("datastore_active"))))
    df = pd.DataFrame(rows)
    last_final = df.loc[df.kind == "final", "ym"].max()
    first_final = df.loc[df.kind == "final", "ym"].min()
    use = pd.concat([
        df[df.kind == "final"],
        df[(df.kind == "provisional") & (df.ym > last_final) & df.datastore],
        df[(df.kind == "retired") & (df.ym < first_final)],
    ]).sort_values("ym")
    df.to_csv(OUT / "scmd_resource_inventory.csv", index=False)
    return use


def sql_fetch(name):
    fields = [f["id"] for f in requests.get(f"{BASE}/datastore_search", params={"resource_id": name, "limit": 0},
                                            timeout=60).json()["result"]["fields"]]
    qty = "TOTAL_QUANITY_IN_VMP_UNIT" if "TOTAL_QUANITY_IN_VMP_UNIT" in fields else "TOTAL_QUANTITY_IN_VMP_UDFS_UNIT_OF_MEASURE"
    unit = "UNIT_OF_MEASURE_NAME" if "UNIT_OF_MEASURE_NAME" in fields else "VMP_UDFS_UNIT_OF_MEASURE_NAME"
    cost = "SUM(INDICATIVE_COST)" if "INDICATIVE_COST" in fields else "CAST(NULL AS FLOAT64)"
    pat = "|".join(ALL_TERMS)
    sql = (f"SELECT YEAR_MONTH, ODS_CODE, VMP_SNOMED_CODE, VMP_PRODUCT_NAME, {unit} AS UNIT, "
           f"SUM({qty}) AS QTY, {cost} AS COST FROM `{name}` "
           f"WHERE REGEXP_CONTAINS(LOWER(VMP_PRODUCT_NAME), r'{pat}') GROUP BY 1,2,3,4,5")
    for attempt in range(5):
        try:
            r = requests.get(f"{BASE}/datastore_search_sql", params={"resource_id": name, "sql": sql}, timeout=300)
            j = r.json()["result"]["result"]
            if j.get("gc_urls"):
                url = j["gc_urls"][0]
                url = url.replace("`", "%60")
                return pd.read_csv(io.StringIO(requests.get(url, timeout=300).text), dtype={"VMP_SNOMED_CODE": str})
            return pd.DataFrame(j["records"])
        except Exception as e:  # noqa
            print("retry", name, e)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(name)


def csv_fetch(url):
    df = pd.read_csv(url, dtype={"VMP_SNOMED_CODE": str})
    df = df[df.VMP_PRODUCT_NAME.str.lower().str.contains("|".join(ALL_TERMS))]
    return (df.rename(columns={"UNIT_OF_MEASURE_NAME": "UNIT", "TOTAL_QUANITY_IN_VMP_UNIT": "QTY"})
              .groupby(["YEAR_MONTH", "ODS_CODE", "VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT"], as_index=False)
              .QTY.sum().assign(COST=float("nan")))


def get_month(row):
    f = CACHE / f"{row['name']}.csv"
    if not f.exists():
        df = sql_fetch(row["name"]) if row["datastore"] else csv_fetch(row["url"])
        df.to_csv(f, index=False)
        print("fetched", row["name"], len(df))
    df = pd.read_csv(f, dtype={"VMP_SNOMED_CODE": str})
    return df.assign(source=row["kind"], resource=row["name"])


UNIT_MG = {"mg": 1.0, "microgram": 1e-3, "micrograms": 1e-3, "g": 1000.0}


def approx_mg_per_unit(name, unit):
    """Approximate mg of the first-named substance per VMP unit of measure (None if not derivable)."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*(mg|micrograms?|g)\b(?:\s*/\s*(\d+(?:\.\d+)?)?\s*ml)?", name, re.I)
    if not m:
        return None
    s = float(m.group(1)) * UNIT_MG[m.group(2).lower()]
    per_ml = "/" in m.group(0)
    vol = float(m.group(3)) if m.group(3) else 1.0
    u = str(unit).lower()
    if u == "ml":
        return s / vol if per_ml else None
    if u in ("gram", "g", "dose", "no value", "nan") or "unit/dose" in u:
        return None
    return s  # tablet, capsule, vial, ampoule, pre-filled syringe/device, sachet, etc.


def main():
    use = resources()
    print(use.groupby("kind").ym.agg(["min", "max", "count"]))
    with ThreadPoolExecutor(4) as ex:
        raw = pd.concat(list(ex.map(get_month, use.to_dict("records"))), ignore_index=True)

    # retired files use 'YYYY-MM' and lower-case unit names; harmonise
    raw["YEAR_MONTH"] = raw.YEAR_MONTH.astype(str).str.replace("-", "").astype(int)
    raw["UNIT"] = raw.UNIT.astype(str).str.upper()
    low = raw.VMP_PRODUCT_NAME.str.lower()
    pos = pd.DataFrame({t: low.str.find(t).where(lambda x: x >= 0) for t in ALL_TERMS})
    raw["substance"] = pos.idxmin(axis=1)
    term2grp = {t: g for g, ts in GROUPS.items() for t in ts}
    raw["group"] = raw.substance.map(term2grp)
    raw["excluded_reason"] = ""
    raw.loc[low.str.contains(EXCL_EXTRA), "excluded_reason"] = "extra_nonsystemic_form"
    raw.loc[low.str.contains(EXCL_SPEC), "excluded_reason"] = "specified_topical_form"
    raw["excluded"] = raw.excluded_reason != ""
    mgu = {k: approx_mg_per_unit(*k) for k in raw[["VMP_PRODUCT_NAME", "UNIT"]].drop_duplicates().itertuples(index=False)}
    raw["mg_per_unit"] = [mgu[k] for k in zip(raw.VMP_PRODUCT_NAME, raw.UNIT)]
    raw["approx_mg"] = raw.QTY * raw.mg_per_unit
    rif = low.str.contains("rifampicin")
    tabcap = raw.UNIT.str.lower().isin(["tablet", "capsule"])
    raw["rif_tabcap"] = (raw.QTY.where(rif & tabcap, 0.0))
    raw["rif_mg"] = raw.approx_mg.where(rif & low.str.startswith("rifampicin"), 0.0).fillna(0)
    raw["antitb_tabcap"] = raw.QTY.where(tabcap & (raw.group == "antituberculosis"), 0.0)
    raw.to_csv(OUT / "scmd_trust_month_vmp.csv.gz", index=False)

    inc = raw[~raw.excluded]
    keys = ["YEAR_MONTH", "ODS_CODE", "group"]
    by_unit = (inc.groupby(keys + ["UNIT"], as_index=False)
                  .agg(total_quantity=("QTY", "sum"), n_vmps=("VMP_SNOMED_CODE", "nunique"),
                       indicative_cost=("COST", "sum"), approx_mg=("approx_mg", "sum"),
                       rif_tabcap=("rif_tabcap", "sum"), rif_mg=("rif_mg", "sum"),
                       antitb_tabcap=("antitb_tabcap", "sum"), source=("source", "first")))
    by_unit.rename(columns={"YEAR_MONTH": "year_month", "ODS_CODE": "ods_code", "UNIT": "unit"}).to_csv(
        OUT / "scmd_trust_month_groups.csv", index=False)

    summ = (inc.groupby(keys, as_index=False)
               .agg(n_vmps=("VMP_SNOMED_CODE", "nunique"), n_substances=("substance", "nunique"),
                    indicative_cost=("COST", "sum"), approx_mg=("approx_mg", "sum"),
                    share_qty_mg_derivable=("mg_per_unit", lambda s: s.notna().mean()),
                    rif_tabcap=("rif_tabcap", "sum"), rif_mg=("rif_mg", "sum"),
                    antitb_tabcap=("antitb_tabcap", "sum"), source=("source", "first")))
    summ["rif_ddd"] = summ.rif_mg / 600.0  # WHO DDD rifampicin 0.6 g oral
    summ.rename(columns={"YEAR_MONTH": "year_month", "ODS_CODE": "ods_code"}).to_csv(
        OUT / "scmd_trust_month_group_summary.csv", index=False)

    prod = (raw.groupby(["group", "substance", "VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT", "excluded",
                         "excluded_reason"], as_index=False)
               .agg(total_quantity=("QTY", "sum"), indicative_cost=("COST", "sum"), mg_per_unit=("mg_per_unit", "first"),
                    n_trusts=("ODS_CODE", "nunique"), first_month=("YEAR_MONTH", "min"), last_month=("YEAR_MONTH", "max")))
    prod.sort_values(["group", "substance", "total_quantity"], ascending=[True, True, False]).to_csv(
        OUT / "scmd_products_by_group.csv", index=False)
    print(len(raw), len(by_unit), len(summ), len(prod))


if __name__ == "__main__":
    main()
