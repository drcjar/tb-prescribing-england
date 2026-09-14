"""Minimum detectable effects (MDE) of the ecological designs versus the population-level effects
expected from published individual-level relative risks.

Design MDE: smallest IRR per 10% within-area increase in prescribing detectable with 80% power
(two-sided alpha = 0.05), from the precision actually achieved: ln(MDE) = (z_0.975 + z_0.80) * SE.

Expected ecological effect: if TB incidence in an area is I0 * (1 + p * (RR - 1)), where p is the
prevalence of drug use and RR the individual-level relative risk, and prevalence scales with the
prescribing rate, a 10% increase in prescribing gives
    IRR_expected = (1 + 1.1 p (RR - 1)) / (1 + p (RR - 1)).
This assumes no confounding or ecological bias, so it is the most favourable case for detection.

Inputs: outputs/panel_annual_<level>[_residence]/panel_results.csv and paper/mde_inputs.csv (drug, rr,
prevalence, sources).
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


def min_detectable_paf(mde):
    """Population attributable fraction a drug would need for its expected IRR per 10% increase
    in use to equal the MDE (same model as expected_irr). NaN if unattainable (MDE >= 1.1)."""
    if mde >= K:
        return np.nan
    q = (mde - 1) / (K - mde)
    return q / (1 + q)


# UKHSA TB in England 2025 (chapter 1): of 5,490 notifications in 2024, immunosuppression was
# recorded for 344, including 30 due to steroids and 54 due to biological therapy.
RECORDED_2024 = {"total": 5490, "steroids": 30, "biological_therapy": 54}
# Illustrative age-specific prevalence of current oral glucocorticoid use, anchored to van Staa
# 2000 (0.9% of adults overall, 2.5% at age 70-79); applied equally to UK-born and non-UK-born.
OCS_PREVALENCE_BY_AGE = {"0 to 14": 0.001, "15 to 44": 0.004, "45 to 64": 0.010, "65 and over": 0.025}


def benchmarks(rr=4.9):
    """Expected change in TB notifications for a 10% increase in use under two alternatives to the
    homogeneous calculation: (1) recorded drug-associated cases, converted to an attributable share;
    (2) age-specific prevalence of use applied to 2024 notifications by age (the same prevalence is
    used for UK-born and non-UK-born people, so only the age distribution of cases matters)."""
    rows = []
    for drug in ("steroids", "biological_therapy"):
        exposed_share = RECORDED_2024[drug] / RECORDED_2024["total"]
        # not every case in an exposed person is attributable: attributable share = exposed share x (RR-1)/RR.
        # The upper bound assumes only half of drug-associated immunosuppression is recorded.
        for completeness in (1.0, 0.5):
            share = exposed_share / completeness * (rr - 1) / rr
            rows.append(dict(method=f"recorded cases ({drug}), UKHSA 2024, {completeness:.0%} recorded, RR {rr}",
                             attributable_share_pct=100 * share,
                             expected_pct_change_10pct=100 * (expected_irr_from_share(share) - 1)))
    age = pd.read_csv(ROOT / "data" / "processed" / "region_tb_birthplace_age_annual.csv")
    age = age[(age.year == 2024) & age.birthplace.isin(["UK born", "Non-UK born"])]
    cases = age.groupby(["birthplace", "age_group"]).tb_count.sum().reset_index()
    cases["age_key"] = cases.age_group.astype(str).str.replace(r"\s*\(.*\)", "", regex=True)
    cases["prevalence"] = cases.age_key.map(
        lambda a: next((v for k, v in OCS_PREVALENCE_BY_AGE.items() if a.startswith(k.split()[0])), np.nan))
    cases = cases.dropna(subset=["prevalence"])
    q = cases.prevalence * (rr - 1)
    paf = (cases.tb_count * q / (1 + q)).sum() / cases.tb_count.sum()
    irr = (cases.tb_count * expected_irr(rr, cases.prevalence)).sum() / cases.tb_count.sum()
    rows.append(dict(method=f"age-stratified (oral corticosteroids, RR {rr})",
                     attributable_share_pct=100 * paf, expected_pct_change_10pct=100 * (irr - 1)))
    homogeneous_q = 0.009 * (rr - 1)
    rows.append(dict(method=f"homogeneous (oral corticosteroids, RR {rr}, prevalence 0.9%)",
                     attributable_share_pct=100 * homogeneous_q / (1 + homogeneous_q),
                     expected_pct_change_10pct=100 * (expected_irr(rr, 0.009) - 1)))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "expected_effect_benchmarks.csv", index=False)
    print(cases[["birthplace", "age_group", "tb_count", "prevalence"]].to_string(index=False))
    print(out.round(3).to_string(index=False))
    return out


def expected_irr_from_share(share):
    """Expected IRR per 10% increase in use when a fraction `share` of cases is attributable."""
    q = share / (1 - share)
    return (1 + K * q) / (1 + q)


def main(level="ltla", apportion="residence"):
    """MDE table for the primary annual panel (exposure t-1) at the given level and apportionment."""
    suffix = "" if apportion == "postcode" else f"_{apportion}"
    res = pd.read_csv(ROOT / "outputs" / f"panel_annual_{level}{suffix}" / "panel_results.csv")
    primary = res[(res.model == "primary (t-1)") & (res.term == "exposure_lag1")].set_index("drug")
    results, window, out_name = f"panel_annual_{level}{suffix}", "primary (t-1)", f"mde_table_{level}{suffix}.csv"
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
    d["min_detectable_paf_pct"] = [100 * min_detectable_paf(m) for m in d.mde_irr_10pct_increase]
    # power actually available for the literature effect
    d["power_for_expected"] = norm.cdf(np.abs(np.log(d.expected_irr_10pct)) / d.se_log_irr_10pct - norm.ppf(0.975))

    d.to_csv(OUT / out_name)
    cols = ["rr", "prevalence", "expected_pct_change_tb", "mde_pct_change_tb", "mde_to_expected_ratio",
            "power_for_expected", "rr_needed_for_80pct_power"]
    print(f"\n{results} — {window}")
    print(d[cols].round(4).to_string())


if __name__ == "__main__":
    for level in ("ltla", "utla"):
        for apportion in ("residence", "postcode"):
            suffix = "" if apportion == "postcode" else f"_{apportion}"
            if (ROOT / "outputs" / f"panel_annual_{level}{suffix}" / "panel_results.csv").exists():
                main(level, apportion)
    benchmarks()
