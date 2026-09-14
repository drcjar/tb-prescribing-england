"""Build annual local authority panels (April 2023 boundaries), 2011-2025, at upper-tier (UTLA)
or lower-tier (LTLA) level.

Usage: python build_panel.py [utla|ltla]

- Prescribing: monthly practice-level items (fetch_prescribing_panel.py) -> practice postcode ->
  LAD (ONS Postcode Directory, Aug 2025) -> area; summed by calendar year, per 1,000 residents.
- Population by age: ONS mid-year estimates (Nomis NM_31_1).
- International in-migration: ONS mid-year estimates components of change (MYEB3), by LAD.
- HIV diagnosed prevalence (90790) and QOF diabetes prevalence (241): Fingertips.
- TB (UTLA only): Fingertips 91361, 3-year counts/denominators keyed on the window's final year.
  Annual TB counts for both levels come from build_tb_annual.py.

The area identifier column is called `utla` at both levels for compatibility with the analysis
scripts; at LTLA level it holds LTLA codes.
"""
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from build_dataset import DRUG_GROUPS

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

ONSPD = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/ONSPD_AUG_2025_UK/FeatureServer/0/query"
# Small areas reported with a neighbour. Fingertips (UTLA) puts City of London with Westminster;
# the UKHSA regional tables used at LTLA level put it with Hackney. Isles of Scilly -> Cornwall.
MERGES = {
    "utla": {"E09000001": "E09000033", "E06000053": "E06000052"},
    "ltla": {"E09000001": "E09000012", "E06000053": "E06000052"},
}
MERGE = MERGES["utla"]
POPULATION_FILES = {"utla": "ons_mye_utla23_2011_2025.csv", "ltla": "ons_mye_ltla23_2011_2025.csv"}
COVARIATE_FILES = {"utla": "covars_fingertips_at502.csv", "ltla": "covars_fingertips_at501.csv"}
YEARS = range(2011, 2026)


def norm_postcode(pc):
    pc = re.sub(r"\s+", "", str(pc).upper())
    return f"{pc[:-3]} {pc[-3:]}" if len(pc) >= 5 else None


def lad_to_area(level="utla"):
    m = json.load(open(RAW / "fingertips_ltla501_to_utla502.json"))
    merge = MERGES[level]
    if level == "utla":
        return {lad: merge.get(utla, utla) for utla, lads in m.items() for lad in lads}
    return {lad: merge.get(lad, lad) for lads in m.values() for lad in lads}


def lad_to_utla():
    return lad_to_area("utla")


def postcode_to_lad(postcodes, batch=200):
    cache_path = RAW / "practice_postcode_lad25.csv"
    cache = pd.read_csv(cache_path) if cache_path.exists() else pd.DataFrame({"pcds": [], "lad25cd": []})
    todo = sorted(set(postcodes) - set(cache.pcds))
    found = []
    for i in range(0, len(todo), batch):
        where = "pcds IN (" + ",".join(f"'{p}'" for p in todo[i:i + batch]) + ")"
        for attempt in range(5):
            try:
                r = requests.post(ONSPD, data={"where": where, "outFields": "pcds,lad25cd",
                                               "returnGeometry": "false", "f": "json"}, timeout=120)
                found += [f["attributes"] for f in r.json()["features"]]
                break
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(5 * (attempt + 1))
    new = pd.DataFrame(found, columns=["pcds", "lad25cd"])
    unmatched = pd.DataFrame({"pcds": sorted(set(todo) - set(new.pcds)), "lad25cd": None})
    cache = pd.concat([cache, new, unmatched]).drop_duplicates("pcds")
    cache.to_csv(cache_path, index=False)
    print(f"Postcodes looked up: {len(todo)} new, {len(unmatched)} not in ONSPD")
    return dict(zip(cache.pcds, cache.lad25cd))


def gp_practice_codes():
    """Standard GP practices (ODS prescribing setting RO76) from the ODS epraccur file."""
    ep = pd.read_csv(RAW / "openprescribing" / "epraccur.csv", header=None, dtype=str, encoding="latin-1")
    return set(ep.loc[ep[25] == "RO76", 0])


PRACTICE_FILES = RAW / "epd_practice_monthly_v2"
RESIDENCE_SHARES = OUT / "practice_lad23_shares.csv"


def annual_prescribing(lad_area, gp_only=True, apportion="postcode"):
    """Area x year prescribing totals from practice x month extracts (2010-2024).

    gp_only   - keep standard GP practices (ODS prescribing setting RO76), applied identically to the
                HSCIC (pre-2014) and NHSBSA (2014+) series.
    apportion - "postcode": each practice's prescribing goes to the LAD containing its postcode;
                "residence": shared across LADs in proportion to where its registered patients live
                (NHS Digital practice x LSOA registrations; earliest year's shares used for earlier
                years, latest year's for later years).
    """
    files = sorted(PRACTICE_FILES.glob("epd_practice_*.csv"))
    rx = pd.concat(pd.read_csv(f, dtype={"PRACTICE_CODE": str, "POSTCODE": str}) for f in files)
    value_cols = [c for c in rx.columns if c.startswith(("items_", "adq_", "mg_"))]
    rx["year"] = rx.YEAR_MONTH // 100
    if gp_only:
        gp = gp_practice_codes()
        share = (rx[rx.PRACTICE_CODE.isin(gp)].groupby("year").items_total.sum() / rx.groupby("year").items_total.sum())
        print("Share of items from standard GP practices (RO76) by year:", share.round(4).to_dict())
        rx = rx[rx.PRACTICE_CODE.isin(gp)]
    n_months = rx.groupby("year").YEAR_MONTH.nunique()
    complete = n_months[n_months == 12].index
    print("Months extracted per year:", n_months.to_dict())
    rx = rx[rx.year.isin(complete)]

    if apportion == "residence":
        practice_year = rx.groupby(["PRACTICE_CODE", "year"])[value_cols].sum(min_count=1).reset_index()
        shares = pd.read_csv(RESIDENCE_SHARES, dtype={"practice_code": str})
        first, last = shares.year.min(), shares.year.max()
        practice_year["share_year"] = practice_year.year.clip(first, last)
        m = practice_year.merge(shares.rename(columns={"practice_code": "PRACTICE_CODE", "year": "share_year"}),
                                on=["PRACTICE_CODE", "share_year"], how="left")
        linked = m.lad23cd.notna()
        print("Share of items apportioned by residence by year:",
              (m[linked].groupby("year").apply(lambda g: (g.items_total * g.share).sum())
               / practice_year.groupby("year").items_total.sum()).round(4).to_dict())
        m = m[linked]
        m[value_cols] = m[value_cols].mul(m.share, axis=0)
        m["utla"] = m.lad23cd.replace(MERGES["ltla"]).map(lad_area)
        return m.dropna(subset=["utla"]).groupby(["utla", "year"])[value_cols].sum(min_count=1)

    rx["pcds"] = rx.POSTCODE.map(norm_postcode)
    lad = postcode_to_lad(rx.pcds.dropna().unique())
    rx["utla"] = rx.pcds.map(lad).map(lad_area)
    linked = rx.utla.notna()
    print("Share of items linked to an area by year:",
          (rx[linked].groupby("year").items_total.sum() / rx.groupby("year").items_total.sum()).round(4).to_dict())
    return rx[linked].groupby(["utla", "year"])[value_cols].sum(min_count=1)


def population(lad_area, level="utla"):
    nomis = pd.read_csv(RAW / POPULATION_FILES[level])
    nomis["utla"] = nomis.GEOGRAPHY_CODE.replace(MERGES[level])
    nomis = nomis.rename(columns={"DATE_NAME": "year"})
    by_age = nomis.pivot_table(index=["utla", "year"], columns="AGE_NAME", values="OBS_VALUE", aggfunc="sum")
    ages_15_44 = [f"Aged {a} - {a + 4} years" for a in range(15, 45, 5)]
    pop = pd.DataFrame({
        "population": by_age["All ages"],
        "pct_age_65plus": 100 * by_age["Aged 65 and over"] / by_age["All ages"],
        "pct_age_15_44": 100 * by_age[ages_15_44].sum(axis=1) / by_age["All ages"],
    })

    myeb = pd.read_csv(RAW / "ons_myeb3_components_lad23.csv")
    myeb["utla"] = myeb.ladcode23.map(lad_area)
    assert myeb.utla.notna().all(), myeb[myeb.utla.isna()]
    intl = myeb.melt(id_vars=["utla"], value_vars=[c for c in myeb.columns if c.startswith("international_in_")])
    intl["year"] = intl.variable.str[-4:].astype(int)
    intl = intl.groupby(["utla", "year"]).value.sum().rename("international_in")
    pop = pop.join(intl)
    pop["intl_in_per_1000"] = pop.international_in / pop.population * 1000

    # people in receipt of asylum support (Home Office), mean of quarter-end counts, 2014 onwards
    asylum = pd.read_csv(RAW / "covariates" / "asylum_support_england_lad_year.csv")
    asylum["utla"] = asylum.lad_code.map(lad_area)
    asylum = asylum.dropna(subset=["utla"]).groupby(["utla", "year"]).people_mean_quarter_end.sum()
    pop = pop.join(asylum.rename("asylum_supported"))
    pop["asylum_per_1000"] = pop.asylum_supported / pop.population * 1000
    return pop


def fingertips_covariates(level="utla"):
    f = pd.read_csv(RAW / COVARIATE_FILES[level])
    f = f[f["Area Type"] != "England"].copy()
    f["year"] = f["Time period"].str[:4].astype(int)  # QOF 2012/13 -> 2012
    f["name"] = f["Indicator ID"].map({90790: "hiv_prev", 241: "diabetes_prev"})
    f["utla"] = f["Area Code"].replace(MERGES[level])
    return f.pivot_table(index=["utla", "year"], columns="name", values="Value", aggfunc="mean")


def tb_windows():
    tb = pd.read_csv(RAW / "tb_at502.csv")
    tb = tb[(tb["Indicator ID"] == 91361) & (tb["Area Type"] != "England")]
    tb["year"] = 2000 + tb["Time period"].str[-2:].astype(int)
    tb = tb.rename(columns={"Area Code": "utla", "Area Name": "area_name", "Count": "tb_count",
                            "Denominator": "tb_denominator"})
    print("TB windows with missing/suppressed counts:", int(tb.tb_count.isna().sum()))
    return tb.set_index(["utla", "year"])[["area_name", "tb_count", "tb_denominator"]]


def main(level="utla", apportion="postcode"):
    lad_area = lad_to_area(level)
    pop = population(lad_area, level)
    grid = pd.MultiIndex.from_product([sorted(pop.index.get_level_values(0).unique()), YEARS],
                                      names=["utla", "year"])
    panel = pd.DataFrame(index=grid).join(pop).join(fingertips_covariates(level))
    if level == "utla":
        panel = panel.join(tb_windows())
        panel["area_name"] = panel.groupby(level="utla").area_name.transform("first")
    panel = panel.join(annual_prescribing(lad_area, apportion=apportion))

    for col in [c for c in panel.columns if c.startswith("items_")]:
        name = "rate_total_items" if col == "items_total" else col.replace("items_", "rate_")
        panel[name] = panel[col] / panel.population * 1000

    national = panel.groupby(level="year")[[c for c in panel.columns if c.startswith("rate_")]]
    print("\nMean annual items per 1,000 residents across areas, by year:")
    print(national.mean().round(1).T.to_string())
    print("\nNon-missing values per column:\n", panel.notna().sum().to_string())
    path = OUT / f"{level}_panel_annual{'' if apportion == 'postcode' else '_' + apportion}.csv"
    panel.reset_index().to_csv(path, index=False)
    print(f"\nWrote {len(panel)} rows ({panel.index.get_level_values(0).nunique()} areas) to {path}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
