"""Simulation-based ("plasmode") power for the primary annual fixed-effects panel.

Keeps the real areas, years, populations, covariates and prescribing, and replaces the TB counts
with simulated counts:
    Y ~ Poisson(mu0 * m * G),  G ~ Gamma(k, 1/k)
where mu0 is the fitted mean of the null model (area + year fixed effects + covariates, no
exposure) on the real counts, G adds overdispersion matched to the real data, and m is a known
prescribing effect:
  - individual-RR scenarios: m = 1 + p (RR - 1), with prevalence of use p proportional to the area's
    prescribing rate and averaging the published prevalence;
  - direct scenarios: a fixed IRR per 10% increase in prescribing.
Each simulated dataset is analysed with the primary model; power = share of simulations with
p < 0.05 and an estimate in the true direction. RR = 1 gives the false-positive rate.

Usage: python simulate_power.py [utla|ltla] [n_sims]
"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analyze_panel import fit_ppml
from analyze_panel_annual import build_frame

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "power_simulation"
OUT.mkdir(parents=True, exist_ok=True)

DRUG = "rate_oral_corticosteroids"
PREVALENCE = 0.009  # current oral glucocorticoid use, UK adults (van Staa 2000)
SCENARIOS = [
    ("No effect (RR 1)", "rr", 1.0),
    ("Published RR 4.9", "rr", 4.9),
    ("RR 25", "rr", 25.0),
    ("RR 100", "rr", 100.0),
    ("IRR 1.02 per 10%", "direct", 1.02),
    ("IRR 1.05 per 10%", "direct", 1.05),
    ("IRR 1.10 per 10%", "direct", 1.10),
]

_STATE = {}


def _init(df, covars, mu0, k):
    _STATE.update(df=df, covars=covars, mu0=mu0, k=k)


def multiplier(df, kind, value):
    rate = df[DRUG]
    if kind == "rr":
        p = PREVALENCE * rate / rate.mean()
        m = 1 + p * (value - 1)
    else:
        beta = np.log(value) / np.log(1.1)
        m = np.exp(beta * (np.log(rate) - np.log(rate).mean()))
    return m / m.mean()


def one_sim(args):
    label, kind, value, seed = args
    df, covars, mu0, k = _STATE["df"], _STATE["covars"], _STATE["mu0"], _STATE["k"]
    rng = np.random.default_rng(seed)
    gamma = rng.gamma(k, 1 / k, size=len(df)) if np.isfinite(k) else 1.0
    sim = df.assign(tb_count=rng.poisson(mu0 * multiplier(df, kind, value) * gamma))
    res = fit_ppml(sim, DRUG, covars)
    b, p = res.params["log_exposure"], res.pvalues["log_exposure"]
    true_positive = value > 1
    detected = p < 0.05 and (b > 0 if true_positive else True)
    return dict(scenario=label, seed=seed, irr_10pct=np.exp(b * np.log(1.1)), p=p, detected=detected)


def main(level="utla", n_sims=200):
    n_sims = int(n_sims)
    df, covars = build_frame(level, -3, -1)
    X = sm.add_constant(pd.concat([df[covars],
                                   pd.get_dummies(df.utla, prefix="a", drop_first=True, dtype=float),
                                   pd.get_dummies(df.window_end, prefix="t", drop_first=True, dtype=float)], axis=1))
    null = sm.GLM(df.tb_count, X, family=sm.families.Poisson(), offset=np.log(df.tb_denominator)).fit()
    mu0 = null.fittedvalues.to_numpy()
    y = df.tb_count.to_numpy()
    alpha = max(((y - mu0) ** 2 - mu0).sum() / (mu0 ** 2).sum(), 1e-6)  # NB2 method of moments
    k = 1 / alpha
    print(f"{level}: {len(df)} area-years, {df.utla.nunique()} areas; overdispersion alpha = {alpha:.4f}")

    tasks = [(label, kind, value, 1000 * i + s) for i, (label, kind, value) in enumerate(SCENARIOS)
             for s in range(n_sims)]
    # capped: each worker holds a copy of the panel and a GLM design matrix, and more workers
    # previously exhausted memory when run alongside other jobs
    workers = min(4, max(1, (os.cpu_count() or 2) - 1))
    with ProcessPoolExecutor(max_workers=workers, initializer=_init, initargs=(df, covars, mu0, k)) as pool:
        results = pd.DataFrame(list(pool.map(one_sim, tasks, chunksize=4)))
    results.to_csv(OUT / f"simulations_{level}.csv", index=False)

    expected = {label: (value if kind == "direct" else np.nan) for label, kind, value in SCENARIOS}
    summary = results.groupby("scenario", sort=False).agg(
        n=("p", "size"), power_or_type1=("detected", "mean"),
        median_irr_10pct=("irr_10pct", "median"),
        irr_2_5=("irr_10pct", lambda s: s.quantile(0.025)), irr_97_5=("irr_10pct", lambda s: s.quantile(0.975)))
    summary["true_irr_10pct_direct"] = summary.index.map(expected)
    summary.to_csv(OUT / f"power_summary_{level}.csv")
    print(summary.round(4).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:3])
