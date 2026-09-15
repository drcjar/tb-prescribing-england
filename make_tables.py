"""Generate manuscript and supplementary tables (markdown) directly from result files, so reported
numbers cannot drift from the outputs (peer review, round 1).

Writes paper/tables/*.md. Missing inputs are skipped with a note.

Usage: python make_tables.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import t as student_t

from drug_groups import DRUG_GROUPS
from plot_panel import LABELS

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"
TABLES = ROOT / "paper" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

HOSPITAL_LABELS = {
    "antituberculosis_active": "Active-TB treatment (pyrazinamide DDD, including fixed-dose combinations; positive control)",
    "antituberculosis_rifamycin_isoniazid": "Rifamycin/isoniazid (active and latent TB, other infections)",
    "tnf_inhibitor": "TNF inhibitors",
    "il6_abatacept": "IL-6 inhibitors and abatacept",
    "jak_inhibitor_rheum": "JAK inhibitors (rheumatology)",
    "rituximab": "Rituximab",
    "transplant_cni_mtor": "Calcineurin/mTOR inhibitors",
    "antiproliferative": "Antiproliferatives",
    "systemic_glucocorticoid": "Systemic glucocorticoids without dexamethasone/hydrocortisone (prednisolone-equivalent mg)",
    "systemic_glucocorticoid_oral": "Systemic glucocorticoids, oral forms only (sensitivity)",
    "glucocorticoid_dexamethasone_hydrocortisone": "Dexamethasone and hydrocortisone (descriptive)",
    "low_tb_risk_biologic": "Low-TB-risk biologics (negative control)",
    "negative_control_levetiracetam": "Levetiracetam (negative control)",
}


# shown in the hospital sensitivity table (S3b) only, not in main Table 3
HOSPITAL_SENSITIVITY_ONLY = {"systemic_glucocorticoid_oral"}


def ci(r, digits=3, est="irr_10pct"):
    if r is None or pd.isna(r.get(est, np.nan)):
        return "—"
    return f"{r[est]:.{digits}f} ({r.ci_low:.{digits}f}–{r.ci_high:.{digits}f})"


def pick(df, **conds):
    sel = df
    for k, v in conds.items():
        sel = sel[sel[k] == v]
    return sel.iloc[0] if len(sel) else None


def write(name, title, header, rows, note=""):
    lines = [f"**{title}**", "", "| " + " | ".join(header) + " |", "|" + "|".join([":---"] + ["---:"] * (len(header) - 1)) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    if note:
        lines += ["", note]
    (TABLES / f"{name}.md").write_text("\n".join(lines) + "\n")
    print("Wrote", TABLES / f"{name}.md")


def panel_results(level, apportion):
    suffix = "" if apportion == "postcode" else f"_{apportion}"
    path = OUT_DIR / f"panel_annual_{level}{suffix}" / "panel_results.csv"
    return pd.read_csv(path) if path.exists() else None


def table_primary_care():
    main = panel_results("ltla", "residence")
    if main is None:
        print("skip table 1: no LTLA residence results")
        return
    utla = panel_results("utla", "residence")
    postcode = panel_results("ltla", "postcode")
    rows = []
    for d in DRUG_GROUPS:
        p = pick(main, drug=d, model="primary (t-1)", term="exposure_lag1")
        lag = pick(main, drug=d, model="lag and lead (t-1, t+1)", term="exposure_lag1")
        lead = pick(main, drug=d, model="lag and lead (t-1, t+1)", term="exposure_lag-1")
        bounds = (f"{p.max_compatible_paf_pct:.0f}% / {p.max_compatible_prevented_fraction_pct:.0f}% "
                  f"({p.max_compatible_paf_nc_shifted_pct:.0f}%)" if p is not None and pd.notna(p.max_compatible_paf_pct) else "—")
        rows.append([LABELS[d], ci(p), ci(pick(utla, drug=d, model="primary (t-1)", term="exposure_lag1")) if utla is not None else "—",
                     ci(pick(postcode, drug=d, model="primary (t-1)", term="exposure_lag1")) if postcode is not None else "—",
                     ci(lag), ci(lead), f"{lead.p_first_minus_last:.3f}" if lead is not None else "—", bounds])
    p0 = pick(main, drug="oral_glucocorticoids", model="primary (t-1)", term="exposure_lag1")
    write("table1_primary_care_panel",
          "Table 1. Primary care prescribing and TB notifications: incidence rate ratio per 10% within-area increase (95% CI)",
          ["Drug group", f"Previous year: LTLA, residence ({p0.n_areas} areas, {p0.years})", "Previous year: UTLA, residence",
           "Previous year: LTLA, practice postcode", "Joint model: previous year (t−1)", "Joint model: following year (t+1)",
           "p, t−1 vs t+1", "Largest compatible PAF / prevented fraction (PAF after negative-control shift)"],
          rows, "Poisson PML with area and year fixed effects, adjusted for age structure, international in-migration, "
                "HIV and diabetes prevalence (diabetes not adjusted for metformin and insulins); SEs clustered by area. "
                "Joint model: prescribing in t−1 and t+1 in one model on a common sample; their estimates can be negatively "
                "correlated (Table S2b gives the correlation and the model with year t added). "
                "PAF, largest population attributable fraction compatible with the upper 90% confidence limit; prevented "
                "fraction, the same from the lower 90% limit; in brackets, the PAF after dividing the upper limit by the "
                "negative control (levothyroxine) estimate, as if its bias applied to every drug.")


def table_sensitivity():
    main = panel_results("ltla", "residence")
    if main is None:
        return
    models = ["primary (t-1)", "FE only (t-1)", "prior 3 years (t-3..t-1)", "+ area trends (t-1)",
              "population covariate (t-1)", "+ LTBI programme (t-1)", "+ asylum support (t-1)", "exclude COVID years (t-1)",
              "outcome years 2018-2024 (t-1)", "EPD exposure only (t-1)", "ADQ measure (t-1)"]
    rows = []
    for d in DRUG_GROUPS:
        row = [LABELS[d]]
        for m in models:
            term = "exposure_prior3" if m.startswith("prior") else "exposure_lag1"
            row.append(ci(pick(main, drug=d, model=m, term=term)))
        rows.append(row)
    write("tableS1_sensitivity", "Table S1. Sensitivity analyses, LTLA panel (residence apportionment): IRR per 10% increase (95% CI)",
          ["Drug group"] + models, rows)
    dl = []
    for d in DRUG_GROUPS:
        dl.append([LABELS[d]] + [ci(pick(main, drug=d, model="distributed lag (t, t-1, t-2)", term=t))
                                 for t in ("exposure", "exposure_lag1", "exposure_lag2")])
    write("tableS2_distributed_lag", "Table S2. Distributed lag model (t, t−1, t−2 in one model), LTLA residence",
          ["Drug group", "t (same year)", "t−1", "t−2"], dl)
    three = []
    for d in DRUG_GROUPS:
        m = "lag, same year and lead (t-1, t, t+1)"
        lead = pick(main, drug=d, model=m, term="exposure_lag-1")
        three.append([LABELS[d]] + [ci(pick(main, drug=d, model=m, term=t)) for t in ("exposure_lag1", "exposure", "exposure_lag-1")]
                     + ([f"{lead.p_first_minus_last:.3f}", f"{lead.corr_first_last:.2f}"] if lead is not None else ["—", "—"]))
    write("tableS2b_lag_same_lead", "Table S2b. Previous, same and following year in one model, LTLA residence: IRR per 10% (95% CI)",
          ["Drug group", "t−1", "t (same year)", "t+1", "p, t−1 vs t+1", "Correlation of t−1 and t+1 estimates"], three)


def table_mde():
    path = OUT_DIR / "mde" / "mde_table_ltla_residence.csv"
    if not path.exists():
        print("skip table 2")
        return
    d = pd.read_csv(path, index_col=0).dropna(subset=["rr"])
    rows = []
    for drug, r in d.iterrows():
        needed = "not attainable" if r.rr < 1 or not np.isfinite(r.rr_needed_for_80pct_power) else f"{r.rr_needed_for_80pct_power:.0f}"
        rows.append([LABELS.get(drug, drug), f"{r.rr:g}", f"{100 * r.prevalence:.1f}%", f"{r.paf_pct:.1f}%", f"{r.se_log_irr_10pct:.4f}",
                     f"{r.expected_pct_change_tb:.2f}%", f"{r.mde_pct_change_tb:.1f}%", f"{r.mde_to_expected_ratio:.0f}",
                     f"{100 * r.power_for_expected:.1f}%",
                     f"{r.min_detectable_paf_pct:.0f}%" if pd.notna(r.min_detectable_paf_pct) else "—", needed])
    bench = OUT_DIR / "mde" / "expected_effect_benchmarks.csv"
    note = ("Expected changes use published individual-level relative risks (ORs for oral glucocorticoids and PPIs) and UK "
            "prevalence of use, assuming that prevalence of use scales with prescribing, that extra prescribing reaches new users, "
            "a homogeneous baseline risk and aligned timing. Negative PAF values are prevented fractions. MDE = exp(2.80 × SE) − 1. "
            "The ratio of MDE to expected change is essentially independent of the 10% contrast, because for small changes both "
            "scale in proportion to it. Power is one-sided power to detect the expected effect in the correct direction.")
    if bench.exists():
        b = pd.read_csv(bench)
        note += " Benchmarks: " + "; ".join(f"{r.method}: {r.expected_pct_change_10pct:.3f}%" for r in b.itertuples()) + "."
    write("table2_mde", "Table 2. Minimum detectable effects (LTLA panel, residence apportionment, exposure t−1) versus expected population effects of a 10% increase in use",
          ["Drug group", "Individual RR/OR", "Prevalence of use", "PAF (negative: prevented fraction)", "SE of log IRR per 10%", "Expected change", "MDE", "MDE ÷ expected",
           "Power", "Minimum detectable PAF", "RR for 80% power"], rows, note)


def table_hospital():
    rows = []
    for level in ("utla", "ltla"):
        path = OUT_DIR / "hospital" / f"hospital_results_{level}.csv"
        if not path.exists():
            continue
        r = pd.read_csv(path)
        w = r[r.design == "within-area FE"]
        for g, label in HOSPITAL_LABELS.items():
            if g in HOSPITAL_SENSITIVITY_ONLY:
                continue
            t = pick(w, drug=g, model="concurrent (t)")
            lag = pick(w, drug=g, model="lag (t-1)")
            trust = pick(w, drug=g, model="lag (t-1), clustered by principal trust")
            lead = pick(w, drug=g, model="lag and lead jointly", term="t+1")
            cs = pick(r, drug=g, design="cross-sectional 2019-24, adjusted")
            fmt = lambda x: "—" if x is None else f"{x.estimate:.3f} ({x.ci_low:.3f}–{x.ci_high:.3f})"
            rows.append([level.upper(), label, fmt(cs), fmt(t),
                         f"{t.elasticity:.2f}" if t is not None else "—", fmt(lag), fmt(trust), fmt(lead)])
    if not rows:
        return
    write("table3_hospital", "Table 3. Hospital medicines (SCMD) and TB notifications, 2019–2024",
          ["Level", "Drug group", "Cross-sectional, adjusted (per SD)", "Within-area, same year (per 10%)",
           "Elasticity (same year)", "Within-area, previous year (per 10%)", "Previous year, SE clustered by principal trust",
           "Following year (joint with previous)"], rows,
          "Exposure: DDD-years per 1,000 residents (positive control: pyrazinamide DDD including fixed-dose combinations; systemic "
          "glucocorticoids: prednisolone-equivalent mg, without dexamethasone and hydrocortisone), apportioned by 2024 acute trust "
          "catchments. Cross-sectional: negative binomial regression of 2019–24 notifications on the standardised log mean rate "
          "(per SD), adjusted for % born outside the UK, age structure, in-migration, HIV and diabetes prevalence. Within-area: "
          "Poisson PML with area and year fixed effects and time-varying covariates, per 10% increase; SEs clustered by area unless "
          "stated. Elasticity: log IRR per log unit of exposure in the same-year model, shown for all groups but interpretable as "
          "linkage attenuation only for the positive control. Following year: for the positive control an association is possible "
          "because treatment continues into the next year; for candidate drugs it is a falsification test.")
    mde_rows = []
    for level in ("utla", "ltla"):
        path = OUT_DIR / "hospital" / f"hospital_mde_{level}.csv"
        if path.exists():
            for r in pd.read_csv(path).itertuples():
                if r.se_type == "clustered by area":
                    mde_rows.append([level.upper(), HOSPITAL_LABELS.get(r.drug, r.drug), r.scenario, f"{r.prevalence_pct:.2f}%",
                                     f"{r.expected_pct_change:.3f}%", f"{r.mde_pct:.1f}%", f"{r.mde_to_expected:.0f}",
                                     f"{r.mde_to_expected_attenuated:.0f}"])
    elasticity = []
    for level in ("utla", "ltla"):
        path = OUT_DIR / "hospital" / f"hospital_results_{level}.csv"
        if path.exists():
            pc = pick(pd.read_csv(path), drug="antituberculosis_active", model="concurrent (t)")
            if pc is not None:
                k = np.log(1.1)
                elasticity.append(f"{level.upper()} {pc.elasticity:.2f}, 95% CI {np.log(pc.ci_low) / k:.2f}–{np.log(pc.ci_high) / k:.2f}")
    write("tableS3_hospital_mde", "Table S3. Hospital medicines: minimum detectable effects (previous-year exposure) versus illustrative expected effects",
          ["Level", "Drug group", "Scenario (illustrative RR)", "Prevalence (SCMD DDD-years per resident)", "Expected change per 10%",
           "MDE", "MDE ÷ expected", "MDE ÷ expected, attenuated by positive-control elasticity"], mde_rows,
          "Relative risks are illustrative values, not estimates. DDD-years per resident approximate the proportion treated only "
          "for continuous maintenance therapy. The attenuated column divides the expected effect by the positive control's "
          "same-year elasticity (" + "; ".join(elasticity) + "). This assumes the same linkage attenuation for previous-year "
          "exposure and for drugs with other supply routes (homecare, specialist centres), and the elasticity also reflects "
          "variation in drug volume per person treated, so the attenuated ratios are illustrative.")


HOSPITAL_SENSITIVITY = ["lag (t-1)", "lag (t-1), excluding outcome years 2020-21", "lag (t-1), elective catchments",
                        "concurrent (t)", "concurrent (t), clustered by principal trust", "concurrent (t), elective catchments"]


def table_hospital_sensitivity():
    rows = []
    for level in ("utla", "ltla"):
        path = OUT_DIR / "hospital" / f"hospital_results_{level}.csv"
        if not path.exists():
            continue
        w = pd.read_csv(path)
        w = w[w.design == "within-area FE"]
        fmt = lambda x: "—" if x is None else f"{x.estimate:.3f} ({x.ci_low:.3f}–{x.ci_high:.3f})"
        for g, label in HOSPITAL_LABELS.items():
            rows.append([level.upper(), label] + [fmt(pick(w, drug=g, model=m)) for m in HOSPITAL_SENSITIVITY])
    if rows:
        write("tableS3b_hospital_sensitivity", "Table S3b. Hospital medicines: sensitivity analyses, IRR per 10% increase (95% CI)",
              ["Level", "Drug group"] + HOSPITAL_SENSITIVITY, rows)


def table_original_design():
    path = OUT_DIR / "panel" / "panel_results.csv"
    if not path.exists():
        return
    r = pd.read_csv(path)
    r = r[r.model == "FE + time-varying"]
    windows = list(dict.fromkeys(r.exposure_window))
    rows = [[LABELS.get(d, d)] + [ci(pick(r, drug=d, exposure_window=w)) for w in windows] for d in dict.fromkeys(r.drug)]
    write("tableS8_original_design", "Table S8. Original panel design (UTLA; Fingertips three-year notification windows; practice-postcode "
          "assignment; original drug groups): IRR per 10% increase (95% CI)", ["Drug group"] + windows, rows,
          "Poisson PML with area and year fixed effects and time-varying covariates. Drug groups follow the original definitions, "
          "before revision after peer review, so they are not directly comparable with Table 1.")


def table_drug_groups():
    rows = []
    for g, rule in DRUG_GROUPS.items():
        text = "; ".join(f"{k}: `{v}`" for k, v in rule.items()) if isinstance(rule, dict) else f"`{rule}`"
        rows.append([LABELS.get(g, g), text.replace("|", "\\|")])
    write("tableS9_drug_groups", "Table S9. Primary care drug group definitions (regular expressions applied to BNF chemical substance "
          "names and BNF codes; drug_groups.py)", ["Drug group", "Rule"], rows,
          "BNF chapters 11–13 (eye, ear and nose, skin) are excluded unless a code rule applies; injectable presentations are excluded "
          "from oral groups. Prednisolone-equivalent factors: prednisolone and prednisone 1, methylprednisolone 1.25, deflazacort 0.83, "
          "dexamethasone 6.67. The SCMD product classification with DDDs is in outputs/hospital/vmp_classification.csv.")


def table_power():
    rows = []
    for level in ("ltla", "utla"):
        path = OUT_DIR / "power_simulation" / f"power_summary_{level}.csv"
        if not path.exists():
            continue
        summary = pd.read_csv(path)
        if "rejection_two_sided" not in summary.columns:  # output of the superseded simulation design
            print(f"skip power table for {level}: old-format summary")
            continue
        sims = pd.read_csv(OUT_DIR / "power_simulation" / f"simulations_{level}.csv")
        null = sims[(sims.scenario == "No effect") & (sims.p < 0.999)]
        replicate_se = (null.log_irr_10pct.abs() / norm.isf(null.p / 2)).median()
        for r in summary.itertuples():
            z = abs(np.log(r.median_irr_10pct)) / r.real_data_se
            analytic = norm.cdf(z - 1.96) + norm.cdf(-z - 1.96)
            rows.append([level.upper(), r.scenario, r.n, f"{100 * r.rejection_two_sided:.1f}%",
                         f"{100 * r.power_correct_direction:.1f}% (±{196 * r.monte_carlo_se:.1f})", f"{100 * analytic:.1f}%",
                         f"{r.median_irr_10pct:.3f}", f"{replicate_se:.4f}", f"{r.null_empirical_sd:.4f}", f"{r.real_data_se:.4f}"])
    if rows:
        write("tableS4_power_simulation", "Table S4. Permutation-based power simulation (systemic oral glucocorticoids, exposure t−1)",
              ["Level", "Scenario", "Replicates", "Two-sided rejection", "Power, correct direction (95% MC interval)",
               "Analytic power at real-data SE", "Median estimated IRR per 10%", "Median replicate SE", "Null empirical SD",
               "Real-data SE"], rows,
              "Within the simulation, replicate SEs matched the spread of null estimates, so the test was approximately "
              "calibrated (slightly anti-conservative). Real-data SEs were larger than in the simulation, probably because permuting "
              "exposure trajectories across areas breaks their alignment with each area's own notification trends; simulated "
              "power is therefore optimistic. Analytic power uses the median simulated estimate as the effect and the "
              "real-data SE.")


def table_regional():
    path = OUT_DIR / "steroids" / "ocs_tb_by_birthplace_regional.csv"
    if not path.exists():
        return
    r = pd.read_csv(path)
    r = r[r.model == "FE + migration + age"]
    # MDE from the t(8) interval: SE of log IRR per 10%, times the t(8) quantiles for 5% two-sided alpha and 80% power
    se = (np.log(r.ci_high) - np.log(r.ci_low)) / (2 * student_t.ppf(0.975, 8))
    r = r.assign(mde_pct_10pct=100 * (np.exp((student_t.ppf(0.975, 8) + student_t.ppf(0.80, 8)) * se) - 1))
    r.to_csv(OUT_DIR / "steroids" / "regional_mde.csv", index=False)
    rows = [[x.outcome, x.exposure.replace("rate_", ""), x.analysis, x.lag_years,
             f"{x.irr_per_10pct:.2f} ({x.ci_low:.2f}–{x.ci_high:.2f})", f"{x.p_cluster_t8:.3f}", f"{x.p_randomisation:.3f}",
             f"{x.mde_pct_10pct:.0f}%"]
            for x in r.itertuples()]
    write("tableS5_regional", "Table S5. Regional models (9 regions): TB notifications by place of birth and age vs primary care prescribing",
          ["Outcome", "Exposure", "Analysis", "Lag (years; negative = lead)", "IRR per 10% (t(8) 95% CI)", "p (cluster t8)", "p (randomisation)", "MDE per 10%"], rows,
          "Randomisation p-values compare the cluster-robust t statistic with 499 permutations of whole regional exposure histories "
          "across regions, valid under exchangeability of those histories; p = (1 + count)/(1 + 499), so the minimum is 0.002.")
    jl = OUT_DIR / "steroids" / "ocs_tb_by_birthplace_lag_lead.csv"
    if jl.exists():
        j = pd.read_csv(jl)
        write("tableS6_regional_lag_lead", "Table S6. Regional models: lag 2 and lead 2 estimated jointly",
              ["Outcome", "Exposure", "Regions excluded", "Years", "IRR lag (per 10%)", "IRR lead (per 10%)", "Lag ÷ lead", "p difference", "p randomisation (lag)"],
              [[x.outcome, x.exposure.replace("rate_", ""), getattr(x, "excluded_regions", "none"), x.years, f"{x.irr_lag_10pct:.2f}", f"{x.irr_lead_10pct:.2f}",
                f"{x.ratio_lag_to_lead:.2f}", f"{x.p_difference_t8:.3f}", f"{x.p_randomisation_lag:.3f}"] for x in j.itertuples()])


def table_coverage():
    path = OUT_DIR / "hospital" / "hospital_coverage_by_year_utla.csv"
    if not path.exists():
        return
    c = pd.read_csv(path)
    rows = [[HOSPITAL_LABELS.get(x.new_group, x.new_group), x.year, f"{100 * (x.direct if pd.notna(x.direct) else 0):.1f}%",
             f"{100 * (x.successor if pd.notna(x.successor) else 0):.1f}%", f"{100 * (x.unmatched if pd.notna(x.unmatched) else 0):.1f}%"]
            for x in c.itertuples() if x.new_group in HOSPITAL_LABELS]
    write("tableS7_hospital_coverage", "Table S7. Hospital medicines: share of DDD from trusts matched to catchments directly, via successor trusts, or unmatched",
          ["Drug group", "Year", "Direct", "Successor", "Unmatched"], rows)


def main():
    table_primary_care()
    table_sensitivity()
    table_mde()
    table_hospital()
    table_hospital_sensitivity()
    table_power()
    table_regional()
    table_coverage()
    table_original_design()
    table_drug_groups()


if __name__ == "__main__":
    main()
