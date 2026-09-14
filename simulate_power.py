"""Permutation-based ("plasmode") power for the primary annual fixed-effects panel.

The real TB counts are kept, so the simulated data carry the real overdispersion, serial
correlation and area-specific trends. Each replicate:
  1. permutes whole exposure trajectories across areas (area i receives area j's series of the
     analysed exposure, prescribing in year t-1, and of concurrent-year prescribing). This breaks
     any true association and any confounding between prescribing and TB;
  2. injects a known effect into the real counts through the permuted exposure:
       y = y_real + Poisson(y_real * (m - 1))   (m normalised so that min(m) = 1)
  3. fits the primary model (area + year fixed effects, covariates, SEs clustered by area).

Effect scenarios for systemic oral glucocorticoids:
  - individual-RR scenarios: m = 1 + p (RR - 1), prevalence p proportional to the prescribing rate
    and averaging 0.9%;
  - direct scenarios: fixed IRR per 10% increase in prescribing;
  - timing misspecification: effects acting through concurrent-year prescribing while the analysis
    uses year t-1.
"No effect" replicates give the null distribution (false-positive rate and empirical SD).

Usage: python simulate_power.py [utla|ltla] [n_null] [n_effect] [residence|postcode]
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_panel import TIME_VARYING, fit_ppml_multi
from analyze_panel_annual import OUTCOME_YEARS, load, with_lags

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "power_simulation"
OUT.mkdir(parents=True, exist_ok=True)

DRUG = "rate_oral_glucocorticoids"
EXPOSURE = f"{DRUG}_lag1"
PREVALENCE = 0.009  # current oral glucocorticoid use, UK adults (van Staa 2000)
SCENARIOS = [
    ("No effect", "null", 1.0, "window"),
    ("Published RR 4.9", "rr", 4.9, "window"),
    ("RR 25", "rr", 25.0, "window"),
    ("RR 100", "rr", 100.0, "window"),
    ("IRR 1.02 per 10%", "direct", 1.02, "window"),
    ("IRR 1.05 per 10%", "direct", 1.05, "window"),
    ("IRR 1.10 per 10%", "direct", 1.10, "window"),
    ("IRR 1.05 per 10%, acting via concurrent year", "direct", 1.05, "concurrent"),
    ("IRR 1.10 per 10%, acting via concurrent year", "direct", 1.10, "concurrent"),
]

_STATE = {}


def _init(df):
    _STATE["df"] = df


def multiplier(rate, kind, value):
    if kind == "null":
        return np.ones(len(rate))
    if kind == "rr":
        m = 1 + PREVALENCE * rate / rate.mean() * (value - 1)
    else:
        beta = np.log(value) / np.log(1.1)
        m = np.exp(beta * (np.log(rate) - np.log(rate).mean()))
    return np.asarray(m)


def one_sim(args):
    label, kind, value, source, seed = args
    df = _STATE["df"]
    rng = np.random.default_rng(seed)
    areas = df.utla.unique()
    mapping = dict(zip(areas, rng.permutation(areas)))
    donor = df.set_index(["utla", "window_end"])[[EXPOSURE, DRUG]]
    permuted = donor.reindex(list(zip(df.utla.map(mapping), df.window_end)))
    sim = df.assign(**{EXPOSURE: permuted[EXPOSURE].to_numpy(), DRUG: permuted[DRUG].to_numpy()})
    sim = sim.dropna(subset=[EXPOSURE, DRUG])
    sim = sim[(sim[EXPOSURE] > 0) & (sim[DRUG] > 0)]

    rate = sim[EXPOSURE] if source == "window" else sim[DRUG]
    m = multiplier(rate, kind, value)
    m = m / m.min()
    y = sim.tb_count.to_numpy().astype(int)
    y = y + rng.poisson(y * (m - 1))
    res = fit_ppml_multi(sim.assign(tb_count=y), [EXPOSURE], TIME_VARYING)
    b, p = res.params[f"log_{EXPOSURE}"], res.pvalues[f"log_{EXPOSURE}"]
    return dict(scenario=label, seed=seed, log_irr_10pct=b * np.log(1.1), p=p,
                rejected_two_sided=p < 0.05, detected_correct_direction=(p < 0.05) and (b > 0))


def main(level="ltla", n_null=500, n_effect=300, apportion="residence"):
    n_null, n_effect = int(n_null), int(n_effect)
    panel = load(level, apportion)
    df = with_lags(panel, [DRUG], lags=[1])
    df = df[df.year.isin(OUTCOME_YEARS)].rename(columns={"year": "window_end", "population": "tb_denominator"})
    df = df.dropna(subset=[EXPOSURE, DRUG, "tb_count"] + TIME_VARYING).reset_index(drop=True)
    real = fit_ppml_multi(df, [EXPOSURE], TIME_VARYING)
    real_se = real.bse[f"log_{EXPOSURE}"] * np.log(1.1)
    print(f"{level}: {len(df)} area-years, {df.utla.nunique()} areas; real-data SE of log IRR per 10% = {real_se:.4f}")

    tasks = [(label, kind, value, source, 1000 * i + s) for i, (label, kind, value, source) in enumerate(SCENARIOS)
             for s in range(n_null if kind == "null" else n_effect)]
    # memory grows over repeated GLM fits, so use two workers and recycle them often
    with ProcessPoolExecutor(max_workers=2, initializer=_init, initargs=(df,), max_tasks_per_child=10) as pool:
        results = pd.DataFrame(list(pool.map(one_sim, tasks, chunksize=2)))
    results.to_csv(OUT / f"simulations_{level}.csv", index=False)

    null_sd = results.loc[results.scenario == "No effect", "log_irr_10pct"].std()
    summary = results.groupby("scenario", sort=False).agg(
        n=("p", "size"), rejection_two_sided=("rejected_two_sided", "mean"),
        power_correct_direction=("detected_correct_direction", "mean"),
        median_irr_10pct=("log_irr_10pct", lambda s: np.exp(s.median())))
    summary["monte_carlo_se"] = np.sqrt(summary.power_correct_direction * (1 - summary.power_correct_direction) / summary.n)
    summary["null_empirical_sd"] = null_sd
    summary["real_data_se"] = real_se
    summary.to_csv(OUT / f"power_summary_{level}.csv")
    print(summary.round(4).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
