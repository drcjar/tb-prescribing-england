"""Practice-level hypothesis-free scan: every BNF section against every practice outcome.

Same design as scan_prescribing_outcomes.py but with the practice as the unit: ~6,200
practices and up to 11 years instead of 151 areas and 11 years, and no apportionment, so
within-unit variation is much larger. Prescribing and outcome come from the same practice,
so shared ascertainment (practices that code more also prescribe more) is a confounder here
in a way it is not at area level; the lead scan and the indication controls are what show it.

Fixed effects are swept out by alternating projections implemented with sparse matrices,
which is what makes 200 sections x ~100 outcomes tractable.

Usage: python scan_practice.py [min_years]
Writes outputs/scan/practice_scan.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "scan"
OUT.mkdir(parents=True, exist_ok=True)
LIST_SIZE_INDICATOR = 114  # QOF Total List Size


def group_means(idx, n_groups, M):
    """mean of M within each group, returned as (n_groups x k); sparse product is far faster
    than np.add.at for matrices this size."""
    n = M.shape[0]
    S = sparse.csr_matrix((np.ones(n), (idx, np.arange(n))), shape=(n_groups, n))
    counts = np.asarray(S.sum(axis=1)).ravel()
    counts[counts == 0] = 1
    return (S @ M) / counts[:, None]


def demean(M, a_idx, n_a, y_idx, n_y, iters=10):
    M = M.copy()
    for _ in range(iters):
        M -= group_means(a_idx, n_a, M)[a_idx]
        M -= group_means(y_idx, n_y, M)[y_idx]
    return M


def scan_outcome(y, X, a_idx, n_a, y_idx, n_y):
    Xd = demean(X, a_idx, n_a, y_idx, n_y)
    yd = demean(y[:, None], a_idx, n_a, y_idx, n_y)[:, 0]
    sxx = (Xd ** 2).sum(axis=0)
    ok = sxx > 1e-12
    beta = np.full(X.shape[1], np.nan)
    se = np.full(X.shape[1], np.nan)
    if not ok.any():
        return beta, se
    Xo = Xd[:, ok]
    b = (Xo * yd[:, None]).sum(axis=0) / sxx[ok]
    g = Xo * (yd[:, None] - Xo * b)
    gs = group_means(a_idx, n_a, g) * np.bincount(a_idx, minlength=n_a)[:, None]  # cluster sums
    beta[ok] = b
    se[ok] = np.sqrt((gs ** 2).sum(axis=0)) / sxx[ok]
    return beta, se


def main(min_years=6):
    min_years = int(min_years)
    exp = pd.read_csv(PROCESSED / "practice_section_exposure.csv.gz", dtype={"practice": str})
    out = pd.read_csv(PROCESSED / "practice_outcomes_long.csv.gz", dtype={"practice": str})
    cat = pd.read_csv(PROCESSED / "practice_outcomes_catalogue.csv")

    size = out[out.indicator_id == LIST_SIZE_INDICATOR][["practice", "year", "count"]]
    size = size.rename(columns={"count": "list_size"}).dropna()
    size = size[size.list_size > 0]
    exp = exp.merge(size, on=["practice", "year"], how="inner")

    sections = [c for c in exp.columns if c not in ("practice", "year", "list_size")]
    vals = exp[sections].to_numpy(dtype=float)
    vals = np.nan_to_num(vals, nan=0.0)          # missing in the wide frame means no prescribing
    coverage = (vals > 0).mean(axis=0)
    sections = [s for s, c in zip(sections, coverage) if c >= 0.80]
    vals = vals[:, coverage >= 0.80]
    # at practice level many section-years are genuinely zero, so use a continuity correction
    # rather than dropping them; this touches only near-zero cells
    logX = exp[["practice", "year"]].copy()
    logX[sections] = np.log((vals + 0.5) / exp.list_size.to_numpy()[:, None] * 1000)
    print(f"exposure: {len(logX):,} practice-years x {len(sections)} sections "
          f"(dropped {len(coverage) - len(sections)} sections prescribed by <80% of practice-years)",
          flush=True)

    usable = cat[(cat.n_years >= min_years) & (cat.count_complete > 0.9)
                 & (cat.denom_complete > 0.9) & (~cat.pooled.astype(bool))
                 & (cat.indicator_id != LIST_SIZE_INDICATOR)]
    out = out[out.indicator_id.isin(usable.indicator_id)]
    out = out[(out["count"] > 0) & (out.denominator > 0)].copy()
    out["log_rate"] = np.log(out["count"] / out.denominator)
    names = dict(zip(cat.indicator_id, cat.indicator))
    print(f"outcomes: {out.indicator_id.nunique()} usable", flush=True)

    rows = []
    for label, shift in (("lag (t-1)", 1), ("lead (t+1)", -1)):
        X = logX.copy()
        X["year"] = X.year + shift
        for k, (iid, o) in enumerate(out.groupby("indicator_id"), 1):
            d = o.merge(X, on=["practice", "year"], how="inner").dropna(subset=["log_rate"])
            if d.practice.nunique() < 500 or d.year.nunique() < min_years:
                continue
            a_idx, practices = pd.factorize(d.practice)
            y_idx, years = pd.factorize(d.year)
            Xm = d[sections].to_numpy(dtype=float)
            keep = ~np.isnan(Xm).any(axis=0)  # all True after the continuity correction
            if keep.sum() == 0:
                continue
            beta, se = scan_outcome(d.log_rate.to_numpy(dtype=float), Xm[:, keep],
                                    a_idx, len(practices), y_idx, len(years))
            rows.append(pd.DataFrame({
                "indicator_id": iid, "indicator": names.get(iid), "section": np.array(sections)[keep],
                "model": label, "beta": beta, "se": se, "n_obs": len(d),
                "n_practices": len(practices), "n_years": len(years)}))
            print(f"  {label} {k}: {names.get(iid)[:50]} ({len(d):,} rows)", flush=True)
    res = pd.concat(rows, ignore_index=True)
    res["z"] = res.beta / res.se
    res.to_csv(OUT / "practice_scan.csv", index=False)
    print(f"wrote {OUT / 'practice_scan.csv'}: {len(res):,} pair-models", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:2])
