"""Hypothesis-free outcome extract: every Fingertips indicator available at upper- and
lower-tier local authority level, with counts and denominators, 2010 onwards.

Pairs with fetch_prescribing_wide.py: prescribing by BNF section against many disease
outcomes, instead of picking drug-disease pairs in advance.

Usage: python fetch_fingertips_wide.py
Writes data/raw/fingertips_wide/{metadata.json,available.json,at<area>_batch<n>.csv.gz}
"""
import json
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "raw" / "fingertips_wide"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://fingertips.phe.org.uk/api"
AREA_TYPES = {502: "UTLA", 501: "LTLA"}
BATCH = 20


def catalogue():
    meta_path, avail_path = OUT / "metadata.json", OUT / "available.json"
    if not meta_path.exists():
        meta_path.write_text(requests.get(f"{BASE}/indicator_metadata/all?include_definition=no", timeout=300).text)
    if not avail_path.exists():
        avail_path.write_text(requests.get(f"{BASE}/available_data", timeout=300).text)
    return json.loads(meta_path.read_text()), json.loads(avail_path.read_text())


def fetch_batch(ids, area_type, n, retries=4):
    path = OUT / f"at{area_type}_batch{n:03d}.csv.gz"
    if path.exists():
        return f"batch {n}: cached"
    url = (f"{BASE}/all_data/csv/by_indicator_id?indicator_ids={','.join(map(str, ids))}"
           f"&child_area_type_id={area_type}&parent_area_type_id=15")
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=600)
            r.raise_for_status()
            if len(r.content) < 200:
                raise ValueError("empty response")
            tmp = path.with_suffix(".tmp")
            tmp.write_bytes(r.content)
            pd.read_csv(tmp, nrows=5, compression=None)  # sanity check before keeping
            df = pd.read_csv(tmp, low_memory=False)
            df.to_csv(path, index=False, compression="gzip")
            tmp.unlink()
            return f"batch {n}: {len(df):,} rows, {df['Indicator ID'].nunique()} indicators"
        except Exception as exc:
            if attempt == retries - 1:
                return f"batch {n}: FAILED {exc}"
            time.sleep(5 * (attempt + 1))


def main():
    meta, avail = catalogue()
    by_area = {}
    for x in avail:
        by_area.setdefault(x["AreaTypeId"], []).append(x["IndicatorId"])
    for area_type, label in AREA_TYPES.items():
        ids = sorted(set(by_area.get(area_type, [])))
        print(f"{label} ({area_type}): {len(ids)} indicators", flush=True)
        for n in range(0, len(ids), BATCH):
            print("  " + fetch_batch(ids[n:n + BATCH], area_type, n // BATCH), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
