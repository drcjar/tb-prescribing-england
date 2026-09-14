#!/usr/bin/env python
"""Apportion GP practices to LADs (April 2023 codes) by where registered patients live.

Source: NHS Digital "Patients Registered at a GP Practice" practice x LSOA files.
Outputs:
  data/processed/practice_lad23_shares.csv  (year, practice_code, lad23cd, patients, share)
  data/processed/practice_lad23_shares_diagnostics.md

Memory-conscious: one release at a time, usecols + dtypes, raw downloads deleted after aggregation
(aggregated practice x LSOA totals are cached as data/raw/practice_lsoa/agg_YYYYMM.csv.gz).
"""
import io
import json
import zipfile
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Releases: one per calendar year (April snapshot). Earliest LSOA-level release is
# January 2014 (wide format, pub13365); Oct 2013 and earlier have no LSOA files.
# fmt: "tall" = CSV with PRACTICE_CODE, LSOA_CODE, "All Patients";
#      "zip"  = zip containing gp-reg-pat-prac-lsoa-all.csv (PRACTICE_CODE, LSOA_CODE, SEX, NUMBER_OF_PATIENTS)
RELEASES = [
    (2014, "201404", "tall", "https://files.digital.nhs.uk/publicationimport/pub13xxx/pub13932/gp-reg-patients-04-2014-totals-lsoa-alt.csv"),
    (2015, "201504", "tall", "https://files.digital.nhs.uk/publicationimport/pub17xxx/pub17356/gp-reg-patients-lsoa-alt-tall.csv"),
    (2016, "201604", "tall", "https://files.digital.nhs.uk/publicationimport/pub20xxx/pub20480/lsoa-alt-format-tall.csv"),
    (2017, "201704", "zip", "https://files.digital.nhs.uk/publicationimport/pub23xxx/pub23475/gp-reg-pat-prac-lsoa-all-females-males.zip"),
    (2018, "201804", "zip", "https://files.digital.nhs.uk/62/638799/gp-reg-pat-prac-lsoa-all-females-males.zip"),
    (2019, "201904", "zip", "https://files.digital.nhs.uk/16/740C9E/gp-reg-pat-prac-lsoa-male-female-apr-19.zip"),
    (2020, "202004", "zip", "https://files.digital.nhs.uk/93/714E7D/gp-reg-pat-prac-lsoa-male-female-Apr-20.zip"),
    (2021, "202104", "zip", "https://files.digital.nhs.uk/52/2D964D/gp-reg-pat-prac-lsoa-male-female-Apr-21.zip"),
    (2022, "202204", "zip", "https://files.digital.nhs.uk/20/64261B/gp-reg-pat-prac-lsoa-male-female-April-22.zip"),
    (2023, "202304", "zip", "https://files.digital.nhs.uk/AA/B3CF39/gp-reg-pat-prac-lsoa-male-female-April-23.zip"),
    (2024, "202404", "zip", "https://files.digital.nhs.uk/5C/704155/gp-reg-pat-prac-lsoa-male-female-Apr-24.zip"),
]
LSOA11_LU_URL = ("https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
                 "LSOA11_LSOA21_LAD22_EW_LU_v5/FeatureServer/0/query")

ROOT = Path("/home/drcjar/jack-tb-prescribing-balls")
RAW = ROOT / "data/raw"
PL = RAW / "practice_lsoa"
OUT = ROOT / "data/processed"
UA = {"User-Agent": "Mozilla/5.0"}

# LAD22 -> LAD23 (April 2023 unitaries)
LAD22_TO_23 = {**{c: "E06000063" for c in ["E07000026", "E07000028", "E07000029"]},  # Cumberland
               **{c: "E06000064" for c in ["E07000027", "E07000030", "E07000031"]},  # Westmorland & Furness
               **{c: "E06000065" for c in [f"E0700016{i}" for i in range(3, 10)]},  # North Yorkshire
               **{c: "E06000066" for c in ["E07000187", "E07000188", "E07000189", "E07000246"]}}  # Somerset
# LAD24+ recodes back to LAD23 (Barnsley/Sheffield boundary change 2024)
LAD26_TO_23 = {"E08000038": "E08000016", "E08000039": "E08000019"}


def md(df, index=False, floatfmt=".4f"):
    """Minimal markdown table (avoids tabulate dependency)."""
    d = df.reset_index() if index else df
    fmt = lambda v: format(v, floatfmt) if isinstance(v, float) else str(v)
    out = ["| " + " | ".join(map(str, d.columns)) + " |", "|" + "---|" * len(d.columns)]
    out += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in d.itertuples(index=False)]
    return "\n".join(out)


def ltla23_set():
    d = json.loads((RAW / "fingertips_ltla501_to_utla502.json").read_text())
    return {c for v in d.values() for c in v}


def lsoa_lookups():
    """Return (map21, map11): DataFrames code -> lad23cd with weight (splits for LSOA11)."""
    f = PL / "lsoa11_lsoa21_lad22_ew_lu_v5.csv"
    if not f.exists():
        rows, off = [], 0
        while True:
            r = requests.get(LSOA11_LU_URL, params=dict(
                where="1=1", outFields="LSOA11CD,LSOA21CD,CHGIND,LAD22CD,LAD22NM", resultRecordCount=2000,
                resultOffset=off, orderByFields="ObjectId", f="json"), timeout=120).json()
            feats = [x["attributes"] for x in r["features"]]
            rows += feats
            off += len(feats)
            if not feats or not r.get("exceededTransferLimit"):
                break
        pd.DataFrame(rows).to_csv(f, index=False)
    v5 = pd.read_csv(f, dtype=str)
    v5["lad23cd"] = v5.LAD22CD.replace(LAD22_TO_23)
    # LSOA11 -> LAD23; split LSOA11s shared equally across their LSOA21 pieces
    m11 = v5[["LSOA11CD", "lad23cd"]].copy()
    m11["w"] = 1.0 / m11.groupby("LSOA11CD").LSOA11CD.transform("size")
    m11 = m11.groupby(["LSOA11CD", "lad23cd"], as_index=False).w.sum().rename(columns={"LSOA11CD": "lsoa"})
    # LSOA21 -> LAD23: England from local SICBL26 lookup (LAD26 recoded), Wales from v5
    l21 = pd.read_csv(RAW / "LSOA21_SICBL26_lookup.csv", usecols=["LSOA21CD", "LAD26CD"], dtype=str)
    l21["lad23cd"] = l21.LAD26CD.replace(LAD26_TO_23)
    wal = v5.loc[v5.LSOA21CD.str.startswith("W"), ["LSOA21CD", "lad23cd"]].drop_duplicates()
    m21 = pd.concat([l21[["LSOA21CD", "lad23cd"]], wal]).drop_duplicates("LSOA21CD").rename(columns={"LSOA21CD": "lsoa"})
    m21["w"] = 1.0
    # consistency check: v5 LAD22 (recoded) vs local LAD26 (recoded) for English LSOA21s
    chk = v5[["LSOA21CD", "lad23cd"]].drop_duplicates().merge(l21, on="LSOA21CD", suffixes=("_v5", "_26"))
    nd = (chk.lad23cd_v5 != chk.lad23cd_26).sum()
    print(f"LSOA21 LAD disagreement v5(LAD22->23) vs SICBL26(LAD26->23): {nd} LSOAs")
    return m21, m11, nd


def download(url, dest):
    with requests.get(url, headers=UA, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)


def load_release(ym, fmt, url):
    """Practice x LSOA totals (all sexes) for one release; cached as csv.gz. Returns (df, meta)."""
    agg = PL / f"agg_{ym}.csv.gz"
    metaf = PL / f"agg_{ym}.meta.json"
    if agg.exists() and metaf.exists():
        return pd.read_csv(agg, dtype={"practice_code": str, "lsoa": str, "patients": "int64"}), json.loads(metaf.read_text())
    dest = PL / (f"{ym}_" + url.rsplit("/", 1)[1])
    if not dest.exists():
        download(url, dest)
    if fmt == "zip":
        with zipfile.ZipFile(dest) as z:
            member = [n for n in z.namelist() if n.lower().endswith("lsoa-all.csv")][0]
            with z.open(member) as fh:
                cols = pd.read_csv(fh, nrows=0).columns.tolist()
            # column names vary between releases (e.g. "Number of Patients" in Apr 2018): normalise
            norm = {c: c.strip().upper().replace(" ", "_") for c in cols}
            want = ["EXTRACT_DATE", "PRACTICE_CODE", "LSOA_CODE", "SEX", "NUMBER_OF_PATIENTS"]
            orig = {v: k for k, v in norm.items()}
            with z.open(member) as fh:
                df = pd.read_csv(fh, usecols=[orig[w] for w in want],
                                 dtype={orig[w]: ("int32" if w == "NUMBER_OF_PATIENTS" else "category") for w in want})
            df = df.rename(columns=norm)
        meta = dict(file=member, columns=cols, raw_rows=len(df), sex_values=sorted(df.SEX.astype(str).unique()),
                    extract_date=sorted(df.EXTRACT_DATE.astype(str).unique()))
        df = df[df.SEX.astype(str).str.upper() == "ALL"]
        df = df.rename(columns={"PRACTICE_CODE": "practice_code", "LSOA_CODE": "lsoa", "NUMBER_OF_PATIENTS": "patients"})
    else:
        cols = pd.read_csv(dest, nrows=0).columns.tolist()
        df = pd.read_csv(dest, usecols=["PRACTICE_CODE", "LSOA_CODE", "All Patients"],
                         dtype={"PRACTICE_CODE": "category", "LSOA_CODE": "category", "All Patients": "int32"})
        meta = dict(file=dest.name, columns=cols, raw_rows=len(df))
        df = df.rename(columns={"PRACTICE_CODE": "practice_code", "LSOA_CODE": "lsoa", "All Patients": "patients"})
    df["practice_code"] = df.practice_code.astype(str).str.strip()
    df["lsoa"] = df.lsoa.astype(str).str.strip()
    df = df.groupby(["practice_code", "lsoa"], as_index=False, observed=True).patients.sum()
    df["patients"] = df.patients.astype("int64")
    meta.update(url=url, agg_rows=len(df), total_patients=int(df.patients.sum()))
    df.to_csv(agg, index=False, compression="gzip")
    metaf.write_text(json.dumps(meta, indent=1))
    dest.unlink()
    return df, meta


def practice_home_lad(ym):
    """Practice -> LAD23 of practice postcode, from EPD practice file for that month."""
    epd = pd.read_csv(RAW / f"epd_practice_monthly/epd_practice_{ym}.csv", usecols=["PRACTICE_CODE", "POSTCODE"], dtype=str)
    epd = epd.drop_duplicates("PRACTICE_CODE")
    pc = pd.read_csv(RAW / "practice_postcode_lad25.csv", dtype=str)
    pc["home"] = pc.lad25cd.replace(LAD26_TO_23)
    m = epd.merge(pc, left_on="POSTCODE", right_on="pcds", how="left")
    return dict(zip(m.PRACTICE_CODE, m.home))


def main():
    PL.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    lt23 = ltla23_set()
    m21, m11, n_disagree = lsoa_lookups()
    set21, set11 = set(m21.lsoa), set(m11.lsoa)
    only21, only11 = set21 - set11, set11 - set21

    shares_all, rel_rows, diag_year, top_rows, lad_rows = [], [], [], [], []
    for year, ym, fmt, url in RELEASES:
        df, meta = load_release(ym, fmt, url)
        codes = pd.Series(df.lsoa.unique())
        n21, n11 = codes.isin(only21).sum(), codes.isin(only11).sum()
        vintage = "2021" if n21 > n11 else "2011"
        prim, sec = (m21, m11) if vintage == "2021" else (m11, m21)
        a = df.merge(prim, on="lsoa", how="left")
        miss = a.lad23cd.isna()
        b = a[miss].drop(columns=["lad23cd", "w"]).merge(sec, on="lsoa", how="left")  # fallback to other vintage
        a = pd.concat([a[~miss], b], ignore_index=True)
        a["pw"] = a.patients * a.w.fillna(1.0)
        tot = df.patients.sum()
        fallback = (b.patients * b.w).where(b.lad23cd.notna()).sum() / tot
        unm = a[a.lad23cd.isna()]
        unmapped_share = unm.patients.sum() / tot
        unm_top = unm.groupby("lsoa").patients.sum().sort_values(ascending=False).head(5).to_dict()
        g = a.dropna(subset=["lad23cd"]).groupby(["practice_code", "lad23cd"], as_index=False).pw.sum()
        g = g.rename(columns={"pw": "patients"})
        g["share"] = g.patients / g.groupby("practice_code").patients.transform("sum")
        g.insert(0, "year", year)
        bad_codes = sorted(set(g.lad23cd[g.lad23cd.str.startswith("E")]) - lt23)
        shares_all.append(g)
        rel_rows.append(dict(year=year, release=ym, url=url, file=meta["file"], columns=", ".join(meta["columns"]),
                             raw_rows=meta["raw_rows"], agg_rows=meta["agg_rows"], patients=meta["total_patients"],
                             vintage=vintage, n_only21=int(n21), n_only11=int(n11), fallback_share=fallback,
                             unmapped_share=unmapped_share, unmapped_top=unm_top, non_lt23_codes=bad_codes,
                             welsh_share=g.loc[g.lad23cd.str.startswith("W"), "patients"].sum() / tot,
                             extract_date=meta.get("extract_date", "")))

        # --- diagnostics
        home = practice_home_lad(ym)
        pr = g.groupby("practice_code").patients.sum().rename("list").to_frame()
        pr["home"] = pr.index.map(home)
        g2 = g.merge(pr, left_on="practice_code", right_index=True)
        inhome = g2[g2.lad23cd == g2.home].groupby("practice_code").share.sum()
        pr["in_share"] = inhome.reindex(pr.index).fillna(0.0)
        pr["out_share"] = 1 - pr.in_share
        hp = pr[pr.home.notna()]
        w = hp.out_share * hp.list
        diag_year.append(dict(year=year, practices=len(pr), practices_with_home_lad=len(hp),
                              median_out=hp.out_share.median(), p90_out=hp.out_share.quantile(0.9),
                              patient_weighted_out=w.sum() / hp.list.sum()))
        if year in (2014, 2019, 2024):
            t = hp[hp.list >= 1000].sort_values("out_share", ascending=False).head(10).assign(year=year, kind="largest out-of-area share (list>=1000)")
            t2 = hp.sort_values("list", ascending=False).head(10).assign(year=year, kind="largest lists")
            t3 = hp.loc[hp.index.isin(["E85124"])].assign(year=year, kind="E85124 (GP at Hand)")
            top_rows.append(pd.concat([t, t2, t3]).reset_index())
        # per-LAD: residents registered at practices located outside LAD
        g3 = g2[g2.home.notna() & g2.lad23cd.str.startswith("E")]
        lad = g3.assign(outside=g3.patients.where(g3.home != g3.lad23cd, 0.0)).groupby("lad23cd")[["patients", "outside"]].sum()
        lad["share_outside"] = lad.outside / lad.patients
        lad["year"] = year
        lad_rows.append(lad.reset_index())
        print(f"{year}: practices={len(pr)} vintage={vintage} unmapped={unmapped_share:.4%} fallback={fallback:.4%} bad={bad_codes}")
        del df, a, b, g2, g3

    shares = pd.concat(shares_all, ignore_index=True)
    shares[["year", "practice_code", "lad23cd", "patients", "share"]].to_csv(OUT / "practice_lad23_shares.csv", index=False, float_format="%.6g")
    chk = shares.groupby(["year", "practice_code"]).share.sum()
    assert (chk - 1).abs().max() < 1e-9

    rel = pd.DataFrame(rel_rows)
    dy = pd.DataFrame(diag_year)
    tops = pd.concat(top_rows, ignore_index=True)
    lads = pd.concat(lad_rows, ignore_index=True)

    L = ["# Practice -> LAD23 apportionment by registered-patient residence: diagnostics", ""]
    L += ["Source: NHS Digital 'Patients Registered at a GP Practice', practice x LSOA files (April snapshots). "
          "Earliest LSOA-level release is January 2014 (wide format, pub13365); no LSOA files exist for 2013 or earlier "
          "publications, so 2011-2013 must borrow the 2014 shares downstream.", ""]
    L += ["LSOA11 -> LAD23: ONS LSOA11_LSOA21_LAD22_EW_LU_v5 (LAD22 recoded to April 2023 unitaries for Cumbria, "
          "North Yorkshire, Somerset; LSOA11s split across LSOA21s are apportioned equally among pieces). "
          "LSOA21 -> LAD23: LSOA21_SICBL26_lookup.csv (LAD26; E08000038/39 recoded to E08000016/19), Welsh LSOA21 from v5. "
          f"English LSOA21s where the two sources disagree on LAD23: {n_disagree}. "
          "Codes not found in the release's own vintage fall back to the other vintage. Welsh residents are kept as W06 "
          "LAD codes (so English shares are net of patients living in Wales). Isles of Scilly and City of London keep their codes.", ""]
    L += ["## Releases", "", "| year | release | vintage | raw rows | practice x LSOA rows | patients | unmapped share | fallback-vintage share | Welsh-resident share | E-codes not in LTLA23 list |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rel_rows:
        L.append(f"| {r['year']} | {r['release']} | LSOA{r['vintage'][2:]} (only-21 codes {r['n_only21']}, only-11 codes {r['n_only11']}) | {r['raw_rows']:,} | {r['agg_rows']:,} | {r['patients']:,} | {r['unmapped_share']:.4%} | {r['fallback_share']:.4%} | {r['welsh_share']:.3%} | {r['non_lt23_codes'] or '-'} |")
    L += ["", "URLs, columns and top unmapped codes:", ""]
    for r in rel_rows:
        L.append(f"- {r['year']}: {r['url']} (file {r['file']}; columns: {r['columns']}; extract date {r['extract_date']}; top unmapped LSOA codes: {r['unmapped_top']})")
    L += ["", "## Practices and out-of-area share", "",
          "out_share = share of a practice's registered patients living outside the LAD23 containing the practice postcode "
          "(practice postcode from EPD for the release month; postcode LAD from ONSPD cache).", "",
          md(dy), ""]
    L += ["## Selected practices", "", md(tops[["year", "kind", "practice_code", "home", "list", "out_share"]], floatfmt=".3f"), ""]
    L += ["## Per LAD: share of resident registered patients registered at practices located outside the LAD", ""]
    piv = lads.pivot(index="lad23cd", columns="year", values="share_outside")
    summ = piv.describe(percentiles=[0.1, 0.5, 0.9]).T
    L += ["Distribution across LADs:", "", md(summ, index=True, floatfmt=".3f"), ""]
    last = lads[lads.year == RELEASES[-1][0]].sort_values("share_outside", ascending=False)
    L += [f"Top 20 LADs in {RELEASES[-1][0]}:", "", md(last.head(20), floatfmt=".3f"), ""]
    L += [f"Bottom 10 LADs in {RELEASES[-1][0]}:", "", md(last.tail(10), floatfmt=".3f"), ""]
    (OUT / "practice_lad23_shares_diagnostics.md").write_text("\n".join(L))
    lads.to_csv(PL / "lad_share_registered_outside.csv", index=False)
    print("done", len(shares))


if __name__ == "__main__":
    main()
