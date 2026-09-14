"""Spatial autocorrelation of residuals from the primary annual panel model (oral corticosteroids),
at UTLA and LTLA level. Moran's I of each area's mean Pearson residual, with row-standardised
k-nearest-neighbour weights (k = 5, great-circle distance between centroids) and a permutation
p-value. UTLA centroids are population-weighted means of their LTLA centroids.

Usage: python spatial_autocorrelation.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_panel import fit_ppml
from analyze_panel_annual import build_frame
from build_panel import MERGES, lad_to_area

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "spatial"
OUT.mkdir(parents=True, exist_ok=True)
K = 5


def centroids(level):
    lad = pd.read_csv(RAW / "lad_may2024_centroids.csv")
    code_col = next(c for c in lad.columns if c.upper().startswith("LAD") and c.upper().endswith("CD"))
    lad = lad.rename(columns={code_col: "lad", "LAT": "lat", "LONG": "lon"})[["lad", "lat", "lon"]]
    pop = pd.read_csv(RAW / "ons_mye_ltla23_2011_2025.csv")
    pop = pop[(pop.DATE_NAME == 2022) & (pop.AGE_NAME == "All ages")].rename(
        columns={"GEOGRAPHY_CODE": "lad", "OBS_VALUE": "population"})[["lad", "population"]]
    lad = lad.merge(pop, on="lad")
    lad["area"] = lad.lad.map(lad_to_area(level)).fillna(lad.lad).replace(MERGES[level])
    w = lad.groupby("area").apply(lambda g: pd.Series({
        "lat": np.average(g.lat, weights=g.population), "lon": np.average(g.lon, weights=g.population)}))
    return w


def knn_weights(coords):
    lat, lon = np.radians(coords.lat.to_numpy()), np.radians(coords.lon.to_numpy())
    dlat, dlon = lat[:, None] - lat[None, :], lon[:, None] - lon[None, :]
    a = np.sin(dlat / 2) ** 2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2) ** 2
    dist = 2 * np.arcsin(np.sqrt(a))
    np.fill_diagonal(dist, np.inf)
    W = np.zeros_like(dist)
    nearest = np.argsort(dist, axis=1)[:, :K]
    np.put_along_axis(W, nearest, 1.0, axis=1)
    return W / W.sum(axis=1, keepdims=True)


def morans_i(x, W, n_perm=999, seed=1):
    z = x - x.mean()
    stat = lambda v: len(v) * (v @ W @ v) / (v @ v) / W.sum()
    observed = stat(z)
    rng = np.random.default_rng(seed)
    perms = np.array([stat(rng.permutation(z)) for _ in range(n_perm)])
    p = (1 + (np.abs(perms) >= abs(observed)).sum()) / (n_perm + 1)
    return observed, p, -1 / (len(x) - 1)


def main():
    rows = []
    for level in ("utla", "ltla"):
        df, covars = build_frame(level, -3, -1)
        res = fit_ppml(df, "rate_oral_corticosteroids", covars)
        df["pearson_resid"] = res.resid_pearson.to_numpy()
        df["log_rate"] = np.log((df.tb_count + 0.5) / df.tb_denominator)
        area = df.groupby("utla")[["pearson_resid", "log_rate"]].mean()
        coords = centroids(level).reindex(area.index).dropna()
        area = area.loc[coords.index]
        W = knn_weights(coords)
        for label, col in [("mean Pearson residual (primary model)", "pearson_resid"),
                           ("mean log TB rate (raw, for comparison)", "log_rate")]:
            I, p, expected = morans_i(area[col].to_numpy(), W)
            rows.append(dict(level=level, quantity=label, n_areas=len(area), morans_i=I, expected_i=expected,
                             permutation_p=p))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "morans_i.csv", index=False)
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
