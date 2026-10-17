"""Practice x year outcome panel from the practice-level Fingertips extract.

Keeps one headline series per indicator (Persons, no inequality breakdown, the age group
with the most practice-years) and maps QOF financial years to the calendar year in which
most of the register was accrued: 2014/15 -> 2014.

Usage: python build_practice_outcomes.py
Writes data/processed/practice_outcomes_long.csv.gz and practice_outcomes_catalogue.csv
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "fingertips_practice"
WIDE = ROOT / "data" / "raw" / "fingertips_wide"
OUT = ROOT / "data" / "processed"


def period_to_year(p):
    p = str(p).strip()
    if re.fullmatch(r"\d{4}", p):
        return int(p), False
    m = re.fullmatch(r"(\d{4})/\d{2}", p)
    if m:
        return int(m.group(1)), False
    m = re.fullmatch(r"(\d{4})\s*-\s*(\d{2,4})", p)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
        end = end if end > 100 else start - start % 100 + end
        return (start + end) // 2, True
    return None, None


def main():
    files = sorted(RAW.glob("ind*.csv.gz"))
    if not files:
        raise SystemExit("no practice indicator files; run fetch_fingertips_practice.py first")
    meta = json.loads((WIDE / "metadata.json").read_text())
    keep = []
    for f in files:
        d = pd.read_csv(f, low_memory=False)
        if "Sex" in d:
            d = d[d["Sex"] == "Persons"]
        if "Category Type" in d:
            d = d[d["Category Type"].isna()]
        if d.empty:
            continue
        keep.append(d)
    d = pd.concat(keep, ignore_index=True)
    years = d["Time period"].map(period_to_year)
    d["year"] = [y for y, _ in years]
    d["pooled"] = [p for _, p in years]
    d = d.dropna(subset=["year"])
    d["year"] = d["year"].astype(int)

    best = (d.groupby(["Indicator ID", "Age"]).size().rename("n").reset_index()
            .sort_values("n", ascending=False).drop_duplicates("Indicator ID"))
    d = d.merge(best[["Indicator ID", "Age"]], on=["Indicator ID", "Age"])
    d = d.rename(columns={"Indicator ID": "indicator_id", "Indicator Name": "indicator",
                          "Area Code": "practice", "Value": "value", "Count": "count",
                          "Denominator": "denominator"})
    d = d[["indicator_id", "indicator", "practice", "year", "value", "count", "denominator", "pooled"]]
    d = d.drop_duplicates(["indicator_id", "practice", "year"])

    cat = (d.groupby(["indicator_id", "indicator"]).agg(
        n_rows=("value", "size"), n_years=("year", "nunique"), n_practices=("practice", "nunique"),
        first_year=("year", "min"), last_year=("year", "max"),
        count_complete=("count", lambda s: round(s.notna().mean(), 3)),
        denom_complete=("denominator", lambda s: round(s.notna().mean(), 3)),
        pooled=("pooled", "max")).reset_index())
    cat["pooled"] = cat.pooled.astype(bool)
    cat["value_type"] = cat.indicator_id.map(lambda i: meta.get(str(i), {}).get("ValueType", {}).get("Name"))

    d.to_csv(OUT / "practice_outcomes_long.csv.gz", index=False, compression="gzip")
    cat.to_csv(OUT / "practice_outcomes_catalogue.csv", index=False)
    usable = cat[(cat.n_years >= 6) & (cat.count_complete > 0.9) & (cat.denom_complete > 0.9) & (~cat.pooled)]
    print(f"{len(cat)} indicators, {len(d):,} practice-years")
    print(f"usable for annual count models: {len(usable)}")
    print(usable.head(20)[["indicator_id", "indicator", "n_years", "n_practices", "first_year", "last_year"]].to_string(index=False))


if __name__ == "__main__":
    main()
