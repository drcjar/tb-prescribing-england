"""Hypothesis-free scan: every BNF section against every usable disease outcome.

For each outcome, all ~194 section exposures are regressed one at a time on the log outcome
rate with area and year fixed effects (two-way within transformation, solved by alternating
projections), with cluster-robust standard errors by area. Doing all sections for an outcome
as one matrix operation makes the full scan minutes rather than hours.

Each pair is estimated twice: exposure in the year before the outcome (lag) and the year
after (lead). Shared area trends produce both; a drug effect should favour the lag, so the
lead scan is the empirical null against which the lag scan is judged.

Usage: python scan_prescribing_outcomes.py [utla|ltla] [min_years]
Writes outputs/scan/{level}_scan.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "scan"
OUT.mkdir(parents=True, exist_ok=True)


def demean(M, area_idx, year_idx, n_area, n_year, iters=12):
    """Two-way within transformation by alternating projections (exact for balanced panels,
    convergent otherwise). M is n x k; returns M with area and year means swept out."""
    M = M.copy()
    for _ in range(iters):
        am = np.zeros((n_area, M.shape[1]))
        np.add.at(am, area_idx, M)
        am /= np.bincount(area_idx, minlength=n_area)[:, None]
        M -= am[area_idx]
        ym = np.zeros((n_year, M.shape[1]))
        np.add.at(ym, year_idx, M)
        ym /= np.bincount(year_idx, minlength=n_year)[:, None]
        M -= ym[year_idx]
    return M


def scan_outcome(y, X, area_idx, n_area, year_idx, n_year):
    """Regress y on each column of X separately with area+year FE; cluster-robust SEs by area."""
    Xd = demean(X, area_idx, year_idx, n_area, n_year)
    yd = demean(y[:, None], area_idx, year_idx, n_area, n_year)[:, 0]
    sxx = (Xd ** 2).sum(axis=0)
    ok = sxx > 1e-12
    beta = np.full(X.shape[1], np.nan)
    se = np.full(X.shape[1], np.nan)
    if not ok.any():
        return beta, se
    Xo = Xd[:, ok]
    b = (Xo * yd[:, None]).sum(axis=0) / sxx[ok]
    resid = yd[:, None] - Xo * b                      # n x k residuals, one column per section
    g = Xo * resid                                     # score contributions
    gs = np.zeros((n_area, g.shape[1]))
    np.add.at(gs, area_idx, g)                         # cluster sums by area
    meat = (gs ** 2).sum(axis=0)
    beta[ok] = b
    se[ok] = np.sqrt(meat) / sxx[ok]
    return beta, se


def main(level="utla", min_years=6):
    min_years = int(min_years)
    exp = pd.read_csv(PROCESSED / f"{level}_section_exposure.csv", dtype={"utla": str})
    out = pd.read_csv(PROCESSED / f"{level}_outcomes_long.csv", dtype={"utla": str})
    cat = pd.read_csv(PROCESSED / f"{level}_outcomes_catalogue.csv")

    sections = [c for c in exp.columns if c not in ("utla", "year", "population")]
    exp = exp.dropna(subset=["population"])
    logX = exp[["utla", "year"]].copy()
    vals = exp[sections].to_numpy(dtype=float)
    vals[vals <= 0] = np.nan
    logX[sections] = np.log(vals)

    usable = cat[(cat.n_years >= min_years) & (cat.count_complete > 0.9)
                 & (cat.denom_complete > 0.9) & (~cat.pooled.astype(bool))]
    out = out[out.indicator_id.isin(usable.indicator_id)]
    out = out[(out["count"] > 0) & (out.denominator > 0)].copy()
    out["log_rate"] = np.log(out["count"] / out.denominator)
    names = dict(zip(cat.indicator_id, cat.indicator))
    print(f"{level}: {len(sections)} sections x {out.indicator_id.nunique()} outcomes", flush=True)

    rows = []
    for lag_name, shift in (("lag (t-1)", 1), ("lead (t+1)", -1)):
        X = logX.copy()
        X["year"] = X.year + shift      # exposure year shifted onto the outcome year
        for k, (iid, o) in enumerate(out.groupby("indicator_id"), 1):
            d = o.merge(X, on=["utla", "year"], how="inner").dropna(subset=["log_rate"])
            if d.utla.nunique() < 30 or d.year.nunique() < min_years:
                continue
            area_idx, areas = pd.factorize(d.utla)
            year_idx, years = pd.factorize(d.year)
            Xm = d[sections].to_numpy(dtype=float)
            keep = ~np.isnan(Xm).any(axis=0)         # sections observed throughout this sample
            if keep.sum() == 0:
                continue
            beta, se = scan_outcome(d.log_rate.to_numpy(dtype=float), Xm[:, keep],
                                    area_idx, len(areas), year_idx, len(years))
            rows.append(pd.DataFrame({
                "indicator_id": iid, "indicator": names.get(iid), "section": np.array(sections)[keep],
                "model": lag_name, "beta": beta, "se": se, "n_obs": len(d),
                "n_areas": len(areas), "n_years": len(years)}))
            if k % 50 == 0:
                print(f"  {lag_name}: {k} outcomes", flush=True)
    res = pd.concat(rows, ignore_index=True)
    res["z"] = res.beta / res.se
    res["irr_10pct"] = np.exp(res.beta * np.log(1.1))
    res.to_csv(OUT / f"{level}_scan.csv", index=False)
    print(f"wrote {OUT / f'{level}_scan.csv'}: {len(res):,} pair-models", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:3])
