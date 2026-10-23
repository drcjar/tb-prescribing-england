"""Robustness of the practice-level scan to lag length and to practice case-mix.

Two criticisms motivate this. First, an effect of prescribing on disease may take several
years, so a single one-year lag could miss it. Second, the associations that survive the
before-beats-after filter may simply mark practices with sicker, more intensively managed
patients. So this runs the scan at lags of 1, 2 and 3 years and the matching leads, each
optionally adjusting for the practice's total prescribing volume per patient as a
time-varying proxy for case-mix and activity.

Usage: python scan_practice_lags.py [adjusted|unadjusted|both]
Writes outputs/scan/practice_scan_lags.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from scan_practice import LIST_SIZE_INDICATOR, demean, group_means

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "scan"
SHIFTS = [("lag 1", 1), ("lag 2", 2), ("lag 3", 3), ("lead 1", -1), ("lead 2", -2), ("lead 3", -3)]


def scan_outcome(y, X, a_idx, n_a, y_idx, n_y, control=None):
    """Regress y on each column of X with practice+year FE, optionally partialling out a
    shared control (log total prescribing) from both sides first."""
    Xd = demean(X, a_idx, n_a, y_idx, n_y)
    yd = demean(y[:, None], a_idx, n_a, y_idx, n_y)[:, 0]
    if control is not None:
        cd = demean(control[:, None], a_idx, n_a, y_idx, n_y)
        denom = float((cd ** 2).sum())
        if denom > 1e-12:
            Xd = Xd - cd @ ((cd.T @ Xd) / denom)
            yd = yd - cd[:, 0] * float((cd[:, 0] * yd).sum() / denom)
    sxx = (Xd ** 2).sum(axis=0)
    ok = sxx > 1e-12
    beta = np.full(X.shape[1], np.nan)
    se = np.full(X.shape[1], np.nan)
    if not ok.any():
        return beta, se
    Xo = Xd[:, ok]
    b = (Xo * yd[:, None]).sum(axis=0) / sxx[ok]
    g = Xo * (yd[:, None] - Xo * b)
    gs = group_means(a_idx, n_a, g) * np.bincount(a_idx, minlength=n_a)[:, None]
    beta[ok] = b
    se[ok] = np.sqrt((gs ** 2).sum(axis=0)) / sxx[ok]
    return beta, se


def main(mode="both"):
    exp = pd.read_csv(PROCESSED / "practice_section_exposure.csv.gz", dtype={"practice": str})
    out = pd.read_csv(PROCESSED / "practice_outcomes_long.csv.gz", dtype={"practice": str})
    cat = pd.read_csv(PROCESSED / "practice_outcomes_catalogue.csv")
    size = out[out.indicator_id == LIST_SIZE_INDICATOR][["practice", "year", "count"]]
    size = size.rename(columns={"count": "list_size"}).dropna()
    exp = exp.merge(size[size.list_size > 0], on=["practice", "year"], how="inner")

    sections = [c for c in exp.columns if c not in ("practice", "year", "list_size")]
    vals = np.nan_to_num(exp[sections].to_numpy(dtype=float), nan=0.0)
    coverage = (vals > 0).mean(axis=0)
    sections = [s for s, c in zip(sections, coverage) if c >= 0.80]
    vals = vals[:, coverage >= 0.80]
    per1000 = (vals + 0.5) / exp.list_size.to_numpy()[:, None] * 1000
    logX = exp[["practice", "year"]].copy()
    logX[sections] = np.log(per1000)
    logX["total_items"] = np.log(vals.sum(axis=1) / exp.list_size.to_numpy() * 1000)

    usable = cat[(cat.n_years >= 6) & (cat.count_complete > 0.9) & (cat.denom_complete > 0.9)
                 & (~cat.pooled.astype(bool)) & (cat.indicator_id != LIST_SIZE_INDICATOR)]
    out = out[out.indicator_id.isin(usable.indicator_id)]
    out = out[(out["count"] > 0) & (out.denominator > 0)].copy()
    out["log_rate"] = np.log(out["count"] / out.denominator)
    names = dict(zip(cat.indicator_id, cat.indicator))
    modes = {"both": [False, True], "adjusted": [True], "unadjusted": [False]}[mode]
    print(f"{len(sections)} sections x {out.indicator_id.nunique()} outcomes x {len(SHIFTS)} shifts", flush=True)

    rows = []
    for adjusted in modes:
        for label, shift in SHIFTS:
            X = logX.copy()
            X["year"] = X.year + shift
            for iid, o in out.groupby("indicator_id"):
                d = o.merge(X, on=["practice", "year"], how="inner").dropna(subset=["log_rate"])
                if d.practice.nunique() < 500 or d.year.nunique() < 5:
                    continue
                a_idx, practices = pd.factorize(d.practice)
                y_idx, years = pd.factorize(d.year)
                beta, se = scan_outcome(
                    d.log_rate.to_numpy(dtype=float), d[sections].to_numpy(dtype=float),
                    a_idx, len(practices), y_idx, len(years),
                    control=d.total_items.to_numpy(dtype=float) if adjusted else None)
                rows.append(pd.DataFrame({"indicator_id": iid, "indicator": names.get(iid),
                                          "section": sections, "shift": label,
                                          "adjusted": adjusted, "beta": beta, "se": se,
                                          "n_obs": len(d)}))
            print(f"  {'adjusted' if adjusted else 'unadjusted'} {label}: done", flush=True)
    res = pd.concat(rows, ignore_index=True)
    res["z"] = res.beta / res.se
    res.to_csv(OUT / "practice_scan_lags.csv", index=False)
    print(f"wrote {OUT / 'practice_scan_lags.csv'}: {len(res):,} pair-models", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:2])
