"""Minimum detectable effects (MDE) of the ecological designs versus the population-level effects
expected from published individual-level relative risks.

Design MDE: smallest IRR per 10% within-area increase in prescribing detectable with 80% power
(two-sided alpha = 0.05), from the precision actually achieved: ln(MDE) = (z_0.975 + z_0.80) * SE.

Expected ecological effect: if TB incidence in an area is I0 * (1 + p * (RR - 1)), where p is the
prevalence of drug use and RR the individual-level relative risk, and prevalence scales with the
prescribing rate, a 10% increase in prescribing gives
    IRR_expected = (1 + 1.1 p (RR - 1)) / (1 + p (RR - 1)).
This assumes no confounding or ecological bias, so it is the most favourable case for detection.

Inputs: outputs/panel/panel_results.csv and paper/mde_inputs.csv (drug, rr, prevalence, sources).
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs" / "mde"
OUT.mkdir(parents=True, exist_ok=True)
Z = norm.ppf(0.975) + norm.ppf(0.80)
K = 1.1


def expected_irr(rr, p):
    q = p * (rr - 1)
    return (1 + K * q) / (1 + q)


def rr_needed(mde, p):
    """Individual RR needed for the expected ecological IRR to reach the design MDE."""
    if mde >= K:  # even an infinite RR cannot move incidence by more than the exposure change
        return np.inf
    q = (mde - 1) / (K - mde)
    return 1 + q / p


def main(results="outputs/panel/panel_results.csv", window="primary: t-5..t-3", out_name="mde_table.csv"):
    res = pd.read_csv(ROOT / results)
    primary = res[(res.exposure_window == window) & (res.model == "FE + time-varying")].set_index("drug")
    se = (np.log(primary.ci_high) - np.log(primary.ci_low)) / (2 * norm.ppf(0.975))
    design = pd.DataFrame({"se_log_irr_10pct": se, "mde_irr_10pct_increase": np.exp(Z * se),
                           "mde_irr_10pct_decrease_equiv": np.exp(-Z * se)})

    inputs = pd.read_csv(ROOT / "paper" / "mde_inputs.csv").set_index("drug")
    d = design.join(inputs, how="left")
    d["expected_irr_10pct"] = [expected_irr(r, p) if pd.notna(r) and pd.notna(p) else np.nan
                               for r, p in zip(d.rr, d.prevalence)]
    d["expected_pct_change_tb"] = 100 * (d.expected_irr_10pct - 1)
    # population attributable fraction implied by the same RR and prevalence (Levin's formula)
    q = d.prevalence * (d.rr - 1)
    d["paf_pct"] = 100 * q / (1 + q)
    d["mde_pct_change_tb"] = 100 * (d.mde_irr_10pct_increase - 1)
    # how many times larger the (log) effect would need to be to reach 80% power
    d["mde_to_expected_ratio"] = np.log(d.mde_irr_10pct_increase) / np.abs(np.log(d.expected_irr_10pct))
    d["rr_needed_for_80pct_power"] = [rr_needed(m, p) if pd.notna(p) else np.nan
                                      for m, p in zip(d.mde_irr_10pct_increase, d.prevalence)]
    # power actually available for the literature effect
    d["power_for_expected"] = norm.cdf(np.abs(np.log(d.expected_irr_10pct)) / d.se_log_irr_10pct - norm.ppf(0.975))

    d.to_csv(OUT / out_name)
    cols = ["rr", "prevalence", "expected_pct_change_tb", "mde_pct_change_tb", "mde_to_expected_ratio",
            "power_for_expected", "rr_needed_for_80pct_power"]
    print(f"\n{results} — {window}")
    print(d[cols].round(4).to_string())


if __name__ == "__main__":
    main()
    if (ROOT / "outputs" / "panel_annual" / "panel_annual_results.csv").exists():
        main("outputs/panel_annual/panel_annual_results.csv", "primary: t-3..t-1", "mde_table_annual.csv")
