"""Build tidy NHS acute trust catchment populations by local authority (LTLA and UTLA).

Source: OHID "NHS acute (hospital) trust catchment populations: April 2026"
https://www.gov.uk/government/statistics/nhs-acute-hospital-trust-catchment-populations-april-2026
ODS: https://assets.publishing.service.gov.uk/media/6a199144050971fbebf3bc3f/
     nhs-acute-hospital-trust-catchment-populations-data_tables-april-2026.ods

The ODS gives MSOA21-level catchment populations per trust (Tables 2-4: all / elective /
emergency). MSOA21 are aggregated to LTLA (LAD23, ONS MSOA21->LAD23 best-fit lookup; MSOA21
nest exactly in LAD23) and to UTLA using data/raw/fingertips_ltla501_to_utla502.json.

catchment_patients      = sum of OHID "MSOA total catchment" (modelled resident population
                          assigned to the trust) over MSOAs in the LA.
prop_of_trust_catchment = LA catchment / sum over all LAs of that trust's catchment
                          (sum of published MSOA rows, not the published trust total, which is
                          larger because of suppression/rounding of small MSOA rows).
prop_of_la_population   = LA catchment for trust / sum over all trusts of catchment in that LA.
"""
import json
import subprocess
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
SCMD = RAW / "scmd"
ODS_URL = ("https://assets.publishing.service.gov.uk/media/6a199144050971fbebf3bc3f/"
           "nhs-acute-hospital-trust-catchment-populations-data_tables-april-2026.ods")
ODS = SCMD / "nhs-acute-hospital-trust-catchment-populations-data_tables-april-2026.ods"
LOOKUP = SCMD / "ons_msoa21_lad23_ew_lu.csv"
LOOKUP_URL = ("https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
              "MSOA21_LAD23_EW_LU/FeatureServer/0/query")
SHEETS = {"All_admissions": "All", "Elective": "Elective", "Emergency": "Emergency"}
OUT = SCMD / "trust_catchment_la.csv"


def ensure_sheets():
    SCMD.mkdir(parents=True, exist_ok=True)
    if not ODS.exists():
        ODS.write_bytes(requests.get(ODS_URL, timeout=300).content)
    missing = [s for s in SHEETS if not (SCMD / f"catchment2026_{s}.csv").exists()]
    if missing:
        tmp = SCMD / "_ods_csv"
        tmp.mkdir(exist_ok=True)
        # export every sheet to CSV (UTF-8) with LibreOffice
        subprocess.run(["soffice", "--headless", "--convert-to",
                        "csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1",
                        str(ODS), "--outdir", str(tmp)], check=True)
        for f in tmp.glob("*.csv"):
            f.rename(SCMD / ("catchment2026_" + f.name.split("april-2026-")[-1]))
        tmp.rmdir()


def ensure_lookup():
    if LOOKUP.exists():
        return pd.read_csv(LOOKUP)
    rows, off = [], 0
    while True:
        r = requests.get(LOOKUP_URL, params=dict(where="1=1", outFields="*", f="json",
                         resultOffset=off, resultRecordCount=2000, returnGeometry="false"),
                         timeout=60).json()
        feats = r.get("features", [])
        rows += [x["attributes"] for x in feats]
        if not feats or not r.get("exceededTransferLimit"):
            break
        off += len(feats)
    df = pd.DataFrame(rows)
    df.to_csv(LOOKUP, index=False)
    return df


def load_msoa():
    frames = []
    for sheet, adm in SHEETS.items():
        df = pd.read_csv(SCMD / f"catchment2026_{sheet}.csv", skiprows=2)
        df.columns = [" ".join(c.split()) for c in df.columns]
        df = df.rename(columns={"MSOA21 total catchment": "msoa_catchment",
                                "MSOA total catchment": "msoa_catchment"})
        frames.append(pd.DataFrame({
            "year": df["Catchment year"], "admission_type": adm,
            "trust_code": df["Trust code"], "trust_name": df["Trust name"],
            "msoa21cd": df["MSOA21CD"], "msoa_catchment": df["msoa_catchment"],
            "trust_total_published": df["Trust total catchment population"]}))
    return pd.concat(frames, ignore_index=True)


def main():
    ensure_sheets()
    lu = ensure_lookup()
    msoa = load_msoa()

    # MSOA -> LTLA (LAD23)
    msoa = msoa.merge(lu[["MSOA21CD", "LAD23CD", "LAD23NM"]], left_on="msoa21cd",
                      right_on="MSOA21CD", how="left")
    assert msoa["LAD23CD"].notna().all(), "unmatched MSOAs"

    # LTLA -> UTLA (Fingertips 502 is keyed UTLA -> [LTLA])
    u2l = json.loads((RAW / "fingertips_ltla501_to_utla502.json").read_text())
    l2u = {l: u for u, ls in u2l.items() for l in ls}
    msoa["UTLA"] = msoa["LAD23CD"].map(l2u)
    assert msoa["UTLA"].notna().all(), f"LTLA without UTLA: {msoa.loc[msoa.UTLA.isna(), 'LAD23CD'].unique()}"

    # names: LTLA from ONS lookup; UTLA from ONS MYE file (2023 codes) where available
    names = dict(zip(lu["LAD23CD"], lu["LAD23NM"]))
    mye = pd.read_csv(RAW / "ons_mye_utla23_2011_2025.csv", usecols=["GEOGRAPHY_CODE", "GEOGRAPHY_NAME"])
    names.update(dict(zip(mye["GEOGRAPHY_CODE"], mye["GEOGRAPHY_NAME"])))

    keys = ["year", "admission_type", "trust_code"]
    tnames = msoa.groupby(keys)["trust_name"].first()
    out = []
    for level, col in [("LTLA", "LAD23CD"), ("UTLA", "UTLA")]:
        g = (msoa.groupby(keys + [col], as_index=False)["msoa_catchment"].sum()
             .rename(columns={col: "la_code", "msoa_catchment": "catchment_patients"}))
        g["la_level"] = level
        g["la_name"] = g["la_code"].map(names)
        g["prop_of_trust_catchment"] = g["catchment_patients"] / g.groupby(keys)["catchment_patients"].transform("sum")
        g["prop_of_la_population"] = g["catchment_patients"] / g.groupby(
            ["year", "admission_type", "la_code"])["catchment_patients"].transform("sum")
        out.append(g)
    res = pd.concat(out, ignore_index=True)
    res["trust_name"] = res.set_index(keys).index.map(tnames)
    res = res[["year", "admission_type", "trust_code", "trust_name", "la_level", "la_code", "la_name",
               "catchment_patients", "prop_of_trust_catchment", "prop_of_la_population"]]
    res = res.sort_values(["year", "admission_type", "la_level", "trust_code", "la_code"])
    res.to_csv(OUT, index=False)

    # ---- checks ----
    print(f"wrote {OUT} rows={len(res)}")
    print(res.groupby(["year", "admission_type", "la_level"]).agg(
        rows=("la_code", "size"), trusts=("trust_code", "nunique"), las=("la_code", "nunique")))
    s1 = res.groupby(["year", "admission_type", "la_level", "trust_code"])["prop_of_trust_catchment"].sum()
    s2 = res.groupby(["year", "admission_type", "la_level", "la_code"])["prop_of_la_population"].sum()
    print("prop_of_trust_catchment sums: min %.6f max %.6f" % (s1.min(), s1.max()))
    print("prop_of_la_population sums:   min %.6f max %.6f" % (s2.min(), s2.max()))
    tt = msoa.groupby(keys).agg(msoa_sum=("msoa_catchment", "sum"), published=("trust_total_published", "first"))
    r = tt.msoa_sum / tt.published
    print("MSOA-row sum / published trust total: median %.3f min %.3f (trust %s)" % (r.median(), r.min(), r.idxmin()))
    la = res[res.la_level == "UTLA"].groupby(["year", "admission_type", "la_code"])["catchment_patients"].sum()
    print("England total catchment by year/admission type (sum over UTLAs):")
    print(la.groupby(level=[0, 1]).sum())


if __name__ == "__main__":
    main()
