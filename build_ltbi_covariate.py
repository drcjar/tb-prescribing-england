"""Latent TB infection (LTBI) testing and treatment programme for new migrants, as a time-varying
area covariate (reviewer request).

Source: UKHSA LTBI programme annual report data tables, 2015/16-2019/20, by CCG (2019/20
configuration; names only, some truncated, some joint submissions). Mapped to 2019 CCGs by name,
then to local authority districts using the share of each CCG's LSOAs in each LAD (ONS LSOA11 ->
CCG19 -> LAD19 lookup). Tests are apportioned to LADs by that share; LAD19 codes for the programme
areas are unchanged in the April 2023 boundaries used elsewhere.

Outputs data/processed/ltbi_programme_{utla,ltla}.csv with, by area and calendar year 2011-2025:
  ltbi_active       - 1 from the first year the area's CCG was active (>= 20 tests) onwards
                      (the programme continued after 2019/20, when area-level reporting stopped);
  ltbi_tests_per_1000 - tests submitted per 1,000 residents (0 before the programme; the last
                      reported year carried forward after 2019).
"""
import re
from pathlib import Path

import pandas as pd

from build_panel import lad_to_area

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "ltbi"
OUT = ROOT / "data" / "processed"

JOINT = {
    "blackburn with darwen and east lancashir": ["blackburn with darwen", "east lancashire"],
    "bradford": ["bradford city", "bradford districts"],
    "haringey": ["barnet", "camden", "islington", "haringey"],
}


def norm(name):
    s = str(name).lower().replace("&", "and")
    s = re.sub(r"\bnhs\b|\bccg\b", " ", s)
    return re.sub(r"\s+", " ", s).strip(" ,")


def ccg_to_lad():
    lk = pd.read_csv(RAW / "lsoa11_ccg19_lad19.csv")
    share = lk.groupby(["CCG19NM", "LAD19CD"]).size().rename("n").reset_index()
    share["share_of_ccg"] = share.n / share.groupby("CCG19NM").n.transform("sum")
    share["ccg_norm"] = share.CCG19NM.map(norm)
    return share


def programme_by_lad():
    prog = pd.read_csv(RAW / "ltbi_programme_area_year.csv")
    prog = prog[prog.area_name != "Total"].copy()
    share = ccg_to_lad()
    ccg_names = share.ccg_norm.unique()
    rows = []
    for name in prog.area_name.unique():
        key = norm(name)
        components = JOINT.get(key, [key])
        matched = [c for comp in components for c in ccg_names if c == comp or c.startswith(comp)]
        if not matched:
            print("unmatched programme area:", name)
            continue
        rows += [(name, c) for c in sorted(set(matched))]
    mapping = pd.DataFrame(rows, columns=["area_name", "ccg_norm"])
    # joint submissions: split tests across component CCGs by LSOA count
    ccg_size = share.groupby("ccg_norm").n.sum()
    mapping["ccg_weight"] = mapping.ccg_norm.map(ccg_size)
    mapping["ccg_weight"] /= mapping.groupby("area_name").ccg_weight.transform("sum")
    m = prog.merge(mapping, on="area_name").merge(share, on="ccg_norm")
    m["tests"] = m.tests_submitted * m.ccg_weight * m.share_of_ccg
    first = m.groupby("LAD19CD").programme_first_active_fy_start.min()
    tests = m.groupby(["LAD19CD", "fy_start_year"]).tests.sum().rename_axis(["lad", "year"]).reset_index()
    return tests, first.rename_axis("lad").rename("first_active_year").reset_index()


def main():
    tests, first = programme_by_lad()
    print(f"Programme LADs: {tests.lad.nunique()}; tests apportioned: {tests.tests.sum():,.0f}")
    for level in ("ltla", "utla"):
        panel = pd.read_csv(OUT / f"{level}_panel_annual.csv", usecols=["utla", "year", "population"])
        lad_area = lad_to_area(level)
        t = tests.assign(utla=tests.lad.map(lad_area)).dropna(subset=["utla"]).groupby(["utla", "year"]).tests.sum()
        f = first.assign(utla=first.lad.map(lad_area)).dropna(subset=["utla"]).groupby("utla").first_active_year.min()
        d = panel.merge(t.reset_index(), on=["utla", "year"], how="left")
        d["tests"] = d.tests.fillna(0)
        last_reported = d[d.year == 2019].set_index("utla").tests
        after = d.year > 2019
        d.loc[after, "tests"] = d.loc[after, "utla"].map(last_reported).fillna(0)
        d["ltbi_tests_per_1000"] = d.tests / d.population * 1000
        d["ltbi_active"] = (d.year >= d.utla.map(f)).astype(int)
        d[["utla", "year", "ltbi_active", "ltbi_tests_per_1000"]].to_csv(OUT / f"ltbi_programme_{level}.csv", index=False)
        print(level, "areas ever active:", int(d.groupby("utla").ltbi_active.max().sum()))


if __name__ == "__main__":
    main()
