"""Area x year x indicator outcome panel from the wide Fingertips extract.

For each indicator keeps one headline series: Persons, no inequality breakdown, and the age
group with the most area-years. Single-year and financial-year periods are mapped to a
calendar year; pooled multi-year periods are kept but flagged, since they induce strong
serial correlation.

Usage: python build_wide_outcomes.py [utla|ltla]
Writes data/processed/{level}_outcomes_long.csv and {level}_outcomes_catalogue.csv
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "fingertips_wide"
OUT = ROOT / "data" / "processed"
AREA_TYPE_ID = {"utla": 502, "ltla": 501}
AREA_TYPE_LABEL = {"utla": "Counties & UAs", "ltla": "Districts & UAs"}


def period_to_year(p):
    """'2015' -> 2015; '2015/16' -> 2015; '2013 - 15' -> midpoint; else None."""
    p = str(p).strip()
    if re.fullmatch(r"\d{4}", p):
        return int(p), False
    m = re.fullmatch(r"(\d{4})/\d{2}", p)
    if m:
        return int(m.group(1)), False
    m = re.fullmatch(r"(\d{4})\s*-\s*(\d{2,4})", p)
    if m:
        start = int(m.group(1))
        end = int(m.group(2))
        end = end if end > 100 else start - start % 100 + end
        return (start + end) // 2, True
    return None, None


def main(level="utla"):
    at = AREA_TYPE_ID[level]
    files = sorted(RAW.glob(f"at{at}_batch*.csv.gz"))
    if not files:
        raise SystemExit(f"no batches for {level}; run fetch_fingertips_wide.py first")
    meta = json.loads((RAW / "metadata.json").read_text())
    keep = []
    for f in files:
        d = pd.read_csv(f, low_memory=False)
        d = d[d["Area Type"].astype(str).str.startswith(AREA_TYPE_LABEL[level])]
        d = d[(d["Sex"] == "Persons") & d["Category Type"].isna()]
        if d.empty:
            continue
        keep.append(d[["Indicator ID", "Indicator Name", "Area Code", "Age", "Time period",
                       "Value", "Count", "Denominator"]])
    d = pd.concat(keep, ignore_index=True)
    years = d["Time period"].map(period_to_year)
    d["year"] = [y for y, _ in years]
    d["pooled"] = [p for _, p in years]
    d = d.dropna(subset=["year"])
    d["year"] = d["year"].astype(int)

    # one headline age group per indicator: the one with the most area-years
    best = (d.groupby(["Indicator ID", "Age"]).size().rename("n").reset_index()
            .sort_values("n", ascending=False).drop_duplicates("Indicator ID"))
    d = d.merge(best[["Indicator ID", "Age"]], on=["Indicator ID", "Age"])
    d = d.rename(columns={"Indicator ID": "indicator_id", "Indicator Name": "indicator",
                          "Area Code": "utla", "Value": "value", "Count": "count",
                          "Denominator": "denominator"})
    d = d[["indicator_id", "indicator", "utla", "year", "value", "count", "denominator", "Age", "pooled"]]
    d = d.drop_duplicates(["indicator_id", "utla", "year"])

    cat = (d.groupby(["indicator_id", "indicator"]).agg(
        n_area_years=("value", "size"), n_years=("year", "nunique"), n_areas=("utla", "nunique"),
        first_year=("year", "min"), last_year=("year", "max"),
        count_complete=("count", lambda s: round(s.notna().mean(), 3)),
        denom_complete=("denominator", lambda s: round(s.notna().mean(), 3)),
        pooled=("pooled", "max")).reset_index())
    cat["value_type"] = cat.indicator_id.map(
        lambda i: meta.get(str(i), {}).get("ValueType", {}).get("Name"))
    cat["unit"] = cat.indicator_id.map(lambda i: meta.get(str(i), {}).get("Unit", {}).get("Label"))

    d.to_csv(OUT / f"{level}_outcomes_long.csv", index=False)
    cat.to_csv(OUT / f"{level}_outcomes_catalogue.csv", index=False)
    usable = cat[(cat.n_years >= 6) & (cat.count_complete > 0.9) & (cat.denom_complete > 0.9) & (~cat.pooled.astype(bool))]
    print(f"{level}: {len(cat)} indicators, {len(d):,} area-years")
    print(f"  usable for annual count models (>=6 single years, counts+denominators): {len(usable)}")
    print(usable.head(12)[["indicator_id", "indicator", "n_years", "first_year", "last_year"]].to_string(index=False))


if __name__ == "__main__":
    main(*sys.argv[1:2])
