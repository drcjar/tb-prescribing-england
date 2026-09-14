"""Spatial dependence of residuals from the primary annual panel model (systemic oral
glucocorticoids, exposure t-1), at UTLA and LTLA level.

With area fixed effects, area-mean residuals are close to zero by construction, so dependence is
assessed within each year: Moran's I of the Pearson residuals across areas for every outcome year,
with row-standardised k-nearest-neighbour weights (k = 5, great-circle distance between centroids)
and permutation p-values. Raw log TB rates are shown for comparison. UTLA centroids are
population-weighted means of their LTLA centroids.

Usage: python spatial_autocorrelation.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_panel import TIME_VARYING, fit_ppml_multi
from analyze_panel_annual import OUTCOME_YEARS, load, with_lags
from build_panel import MERGES, lad_to_area

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "spatial"
OUT.mkdir(parents=True, exist_ok=True)
K = 5
EXPOSURE = "rate_oral_glucocorticoids_lag1"


def centroids(level):
    lad = pd.read_csv(RAW / "lad_may2024_centroids.csv")
    lad = lad.rename(columns={"LAD24CD": "lad", "LAT": "lat", "LONG": "lon"})[["lad", "lat", "lon"]]
    pop = pd.read_csv(RAW / "ons_mye_ltla23_2011_2025.csv")
    pop = pop[(pop.DATE_NAME == 2022) & (pop.AGE_NAME == "All ages")].rename(
        columns={"GEOGRAPHY_CODE": "lad", "OBS_VALUE": "population"})[["lad", "population"]]
    lad = lad.merge(pop, on="lad")
    lad["area"] = lad.lad.map(lad_to_area(level)).fillna(lad.lad).replace(MERGES[level])
    return lad.groupby("area").apply(lambda g: pd.Series({
        "lat": np.average(g.lat, weights=g.population), "lon": np.average(g.lon, weights=g.population)}))


def knn_weights(coords):
    lat, lon = np.radians(coords.lat.to_numpy()), np.radians(coords.lon.to_numpy())
    dlat, dlon = lat[:, None] - lat[None, :], lon[:, None] - lon[None, :]
    a = np.sin(dlat / 2) ** 2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2
    dist = 2 * np.arcsin(np.sqrt(a))
    np.fill_diagonal(dist, np.inf)
    W = np.zeros_like(dist)
    np.put_along_axis(W, np.argsort(dist, axis=1)[:, :K], 1.0, axis=1)
    return W / W.sum(axis=1, keepdims=True)


def morans_i(x, W, n_perm=999, seed=1):
    z = x - x.mean()
    stat = lambda v: len(v) * (v @ W @ v) / (v @ v) / W.sum()
    observed = stat(z)
    rng = np.random.default_rng(seed)
    perms = np.array([stat(rng.permutation(z)) for _ in range(n_perm)])
    return observed, (1 + (np.abs(perms) >= abs(observed)).sum()) / (n_perm + 1)


def main():
    rows = []
    for level in ("utla", "ltla"):
        df = with_lags(load(level, "residence"), ["rate_oral_glucocorticoids"], lags=[1])
        df = df[df.year.isin(OUTCOME_YEARS)].rename(columns={"year": "window_end", "population": "tb_denominator"})
        df = df.dropna(subset=[EXPOSURE, "tb_count"] + TIME_VARYING).reset_index(drop=True)
        res = fit_ppml_multi(df, [EXPOSURE], TIME_VARYING)
        df["pearson_resid"] = res.resid_pearson.to_numpy()
        df["log_rate"] = np.log((df.tb_count + 0.5) / df.tb_denominator)
        coords = centroids(level)
        for year, g in df.groupby("window_end"):
            g = g.set_index("utla").loc[lambda f: f.index.isin(coords.index)]
            W = knn_weights(coords.loc[g.index])
            for label, col in [("Pearson residual (primary model)", "pearson_resid"), ("log TB rate (raw)", "log_rate")]:
                I, p = morans_i(g[col].to_numpy(), W)
                rows.append(dict(level=level, year=year, quantity=label, n_areas=len(g), morans_i=I, permutation_p=p))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "morans_i_by_year.csv", index=False)
    summary = out.groupby(["level", "quantity"]).agg(
        years=("year", "size"), median_i=("morans_i", "median"), min_i=("morans_i", "min"),
        max_i=("morans_i", "max"), years_p_below_005=("permutation_p", lambda p: int((p < 0.05).sum())))
    summary.to_csv(OUT / "morans_i_summary.csv")
    print(summary.round(3).to_string())


if __name__ == "__main__":
    main()
