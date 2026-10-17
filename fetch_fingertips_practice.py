"""Practice-level outcomes: every Fingertips indicator published for GP practices.

Area-level panels turned out to have almost no within-area variation left after fixed
effects (see outputs/scan). Practices give ~6,200 units and 16 years instead of 151 areas
and 11 years, so this is the better-powered version of the same scan.

The API errors if several indicators are requested at practice level, so they are fetched
one at a time, filtered to practice rows and stored compressed.

Usage: python fetch_fingertips_practice.py
Writes data/raw/fingertips_practice/ind<id>.csv.gz
"""
import json
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
WIDE = ROOT / "data" / "raw" / "fingertips_wide"
OUT = ROOT / "data" / "raw" / "fingertips_practice"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://fingertips.phe.org.uk/api"
KEEP = ["Indicator ID", "Indicator Name", "Area Code", "Sex", "Age", "Category Type",
        "Time period", "Value", "Count", "Denominator"]


def fetch_indicator(iid, retries=4):
    path = OUT / f"ind{iid}.csv.gz"
    if path.exists():
        return f"{iid}: cached"
    url = (f"{BASE}/all_data/csv/by_indicator_id?indicator_ids={iid}"
           f"&child_area_type_id=7&parent_area_type_id=66")
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=600)
            r.raise_for_status()
            if r.content[:20].lstrip().startswith(b"<"):
                raise ValueError("HTML error page returned")
            tmp = path.with_suffix(".tmp")
            tmp.write_bytes(r.content)
            d = pd.read_csv(tmp, low_memory=False)
            d = d[d["Area Type"].astype(str).str.contains("GP|General", case=False, na=False)]
            d = d[[c for c in KEEP if c in d.columns]]
            d.to_csv(path, index=False, compression="gzip")
            tmp.unlink()
            return f"{iid}: {len(d):,} practice rows"
        except Exception as exc:
            if attempt == retries - 1:
                return f"{iid}: FAILED {exc}"
            time.sleep(10 * (attempt + 1))


def main():
    avail = json.loads((WIDE / "available.json").read_text())
    ids = sorted({x["IndicatorId"] for x in avail if x["AreaTypeId"] == 7})
    print(f"{len(ids)} practice-level indicators", flush=True)
    for n, iid in enumerate(ids, 1):
        print(f"[{n}/{len(ids)}] " + fetch_indicator(iid), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
