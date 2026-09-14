"""Hospital-prescribed medicines and TB notifications by local authority, 2019-2024 (revised after
peer review, round 1).

Exposure: NHS Secondary Care Medicines Data (SCMD; NHSBSA), trust x month x product
(fetch_scmd.py), classified with data/raw/scmd/vmp_classification.csv (build_scmd_classification.py):
  - quantity in WHO defined daily doses (DDD; documented maintenance doses where WHO has none),
    expressed as DDD-years per 1,000 residents; systemic glucocorticoids (without dexamethasone and
    hydrocortisone, reported separately) in prednisolone-equivalent mg; the positive control in
    pyrazinamide DDD including fixed-dose combinations; intra-articular/depot, topical and oncology
    forms excluded;
  - trusts that merged during 2019-2024 are reassigned to their successors (trust_successor_map.csv);
  - apportioned to local authorities with OHID acute trust catchment shares (2024, all admissions;
    elective admissions as a sensitivity analysis).
Controls: active-TB treatment (pyrazinamide, including fixed-dose combinations; positive control);
low-TB-risk biologics (IL-17, IL-12/23, alpha4beta7 inhibitors, anakinra) and levetiracetam
(negative control exposures).
Outcome: annual TB notifications (UKHSA regional reports).

Usage: python hospital_medicines.py [utla|ltla]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analyze_panel import TIME_VARYING, fit_ppml_multi
from build_panel import MERGES
from mde import expected_irr

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
SCMD = RAW / "scmd"
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "hospital"
OUT.mkdir(parents=True, exist_ok=True)

GROUPS = ["antituberculosis_active", "antituberculosis_rifamycin_isoniazid", "tnf_inhibitor", "il6_abatacept",
          "jak_inhibitor_rheum", "rituximab", "transplant_cni_mtor", "antiproliferative", "systemic_glucocorticoid",
          "systemic_glucocorticoid_oral", "glucocorticoid_dexamethasone_hydrocortisone", "low_tb_risk_biologic",
          "negative_control_levetiracetam"]
SOURCE_PRIORITY = {"final": 0, "provisional": 1, "retired": 2}
YEARS = range(2019, 2025)
K = np.log(1.1)
LEVETIRACETAM_DDD_MG = 1500
PYRAZINAMIDE_DDD_MG = 1500
CROSS_SECTIONAL_COVARS = ["pct_non_uk_born", "pct_age_65plus", "pct_age_15_44", "intl_in_per_1000", "hiv_prev",
                          "diabetes_prev"]
# Illustrative individual-level relative risks for the expected-effect scenarios (not estimates)
RR_SCENARIOS = {
    "tnf_inhibitor": [("RR 4 (illustrative, before LTBI screening)", 4.0),
                      ("RR 1.5 (illustrative, with LTBI screening; probably nearer 1, so favours detection)", 1.5)],
    "il6_abatacept": [("RR 2", 2.0)],
    "jak_inhibitor_rheum": [("RR 2", 2.0)],
    "rituximab": [("RR 1.5", 1.5)],
    "transplant_cni_mtor": [("RR 10 (solid organ transplant)", 10.0)],
    "antiproliferative": [("RR 2", 2.0)],
}


def monthly_products():
    v = pd.read_csv(SCMD / "scmd_trust_month_vmp.csv.gz", dtype={"YEAR_MONTH": str, "VMP_SNOMED_CODE": str},
                    usecols=["YEAR_MONTH", "ODS_CODE", "VMP_SNOMED_CODE", "UNIT", "QTY", "source"])
    v["YEAR_MONTH"] = v.YEAR_MONTH.str.replace("-", "").astype(int)
    v["UNIT"] = v.UNIT.astype(str).str.upper()
    v["priority"] = v.source.map(SOURCE_PRIORITY)
    return v[v.priority == v.groupby("YEAR_MONTH").priority.transform("min")]


def trust_year_quantities():
    v = monthly_products()
    cls = pd.read_csv(SCMD / "vmp_classification.csv", dtype={"vmp_snomed_code": str})
    cls = cls[cls.include.astype(str).str.lower() == "true"]
    # dm+d renames leave some (code, unit) pairs listed twice; merging on both would double-count them
    cls = cls.drop_duplicates(["vmp_snomed_code", "unit"])
    m = v.merge(cls, left_on=["VMP_SNOMED_CODE", "UNIT"], right_on=["vmp_snomed_code", "unit"], how="left")
    assert len(m) == len(v), "classification merge duplicated SCMD rows"
    print(f"SCMD product rows classified as included: {m.new_group.notna().mean():.1%}")
    m = m.dropna(subset=["new_group"])
    m["ddd"] = m.QTY * m.ddd_per_unit
    # positive control in pyrazinamide DDD, counting fixed-dose combination content, so a day of
    # intensive-phase treatment counts once whatever the formulation; ethambutol-only products add nothing
    pza_mg = m.pyrazinamide_mg_per_unit.fillna(
        m.mg_per_unit.where(m.substances.astype(str).str.strip().str.lower() == "pyrazinamide"))
    active = m.new_group == "antituberculosis_active"
    m.loc[active, "ddd"] = m.loc[active, "QTY"] * pza_mg[active].fillna(0) / PYRAZINAMIDE_DDD_MG
    # candidate glucocorticoid exposure excludes dexamethasone and hydrocortisone (oncology, antiemetic,
    # COVID-19 and replacement use), which are reported as a separate descriptive group
    dex_hc = (m.new_group == "systemic_glucocorticoid") & m.substances.astype(str).str.contains(
        "dexamethasone|hydrocortisone", case=False)
    m.loc[dex_hc, "new_group"] = "glucocorticoid_dexamethasone_hydrocortisone"
    # sensitivity: oral forms only, since IV methylprednisolone pulses mark acute severe disease
    oral = m[(m.new_group == "systemic_glucocorticoid") & (m.route_class == "oral")]
    m = pd.concat([m, oral.assign(new_group="systemic_glucocorticoid_oral")], ignore_index=True)
    m["pred_mg"] = np.where(m.new_group.isin(["systemic_glucocorticoid", "systemic_glucocorticoid_oral"]),
                            m.QTY * m.mg_per_unit * m.pred_equiv_factor, 0.0)
    m["year"] = m.YEAR_MONTH // 100
    monthly = m.groupby(["ODS_CODE", "new_group", "YEAR_MONTH", "year"])[["ddd", "pred_mg"]].sum().clip(lower=0)

    n = pd.read_csv(SCMD / "scmd_negative_control_trust_month.csv", dtype={"year_month": str})
    n["YEAR_MONTH"] = n.year_month.str.replace("-", "").astype(int)
    n["priority"] = n.source.map(SOURCE_PRIORITY)
    n = n[n.priority == n.groupby("YEAR_MONTH").priority.transform("min")]
    neg = pd.DataFrame({"ODS_CODE": n.ods_code, "new_group": "negative_control_levetiracetam",
                        "YEAR_MONTH": n.YEAR_MONTH, "year": n.YEAR_MONTH // 100,
                        "ddd": (n.approx_mg / LEVETIRACETAM_DDD_MG).clip(lower=0), "pred_mg": 0.0})

    q = pd.concat([monthly.reset_index(), neg], ignore_index=True)
    months = q.groupby("year").YEAR_MONTH.nunique()
    q = q[q.year.isin([y for y in YEARS if months.get(y, 0) == 12])]
    return q.groupby(["ODS_CODE", "new_group", "year"], as_index=False)[["ddd", "pred_mg"]].sum()


def catchment(level, admission_type="All"):
    c = pd.read_csv(SCMD / "trust_catchment_la.csv")
    c = c[(c.year == 2024) & (c.admission_type == admission_type) & (c.la_level == level.upper())]
    return c.assign(utla=c.la_code.replace(MERGES[level]))


def trust_targets(catchment_trusts):
    """Map every SCMD trust to catchment trust(s): itself if present, else its successor(s)."""
    s = pd.read_csv(SCMD / "trust_successor_map.csv")
    s = s[s.successor_in_catchment.astype(str).str.lower() == "true"][["ods_code", "successor_code"]]
    s["weight"] = 1 / s.groupby("ods_code").successor_code.transform("count")
    direct = pd.DataFrame({"ods_code": sorted(catchment_trusts), "successor_code": sorted(catchment_trusts), "weight": 1.0})
    return pd.concat([direct, s.rename(columns={})], ignore_index=True)


def apportion(q, level, admission_type="All"):
    c = catchment(level, admission_type)
    targets = trust_targets(set(c.trust_code))
    m = q.merge(targets, left_on="ODS_CODE", right_on="ods_code", how="left")
    m["match"] = np.select([m.successor_code.isna(), m.ODS_CODE == m.successor_code], ["unmatched", "direct"], "successor")
    coverage = (m.groupby(["new_group", "year", "match"]).ddd.sum() / m.groupby(["new_group", "year"]).ddd.sum()).unstack("match")
    m = m.dropna(subset=["successor_code"])
    m = m.merge(c[["trust_code", "utla", "prop_of_trust_catchment"]], left_on="successor_code", right_on="trust_code")
    for col in ("ddd", "pred_mg"):
        m[col] = m[col] * m.weight * m.prop_of_trust_catchment
    wide = m.groupby(["utla", "year", "new_group"])[["ddd", "pred_mg"]].sum().unstack("new_group")
    wide.columns = [f"{a}_{g}" for a, g in wide.columns]
    return wide.reset_index(), coverage


def principal_trust(level):
    c = catchment(level)
    return c.sort_values("prop_of_la_population").drop_duplicates("utla", keep="last").set_index("utla").trust_code


def census_non_uk_born(level):
    from build_panel import lad_to_area
    cob = pd.read_csv(RAW / "census21_ts004_lsoa.csv").pivot_table(
        index="GEOGRAPHY_CODE", columns="C2021_COB_12_NAME", values="OBS_VALUE", aggfunc="sum")
    lk = pd.read_csv(RAW / "LSOA21_SICBL26_lookup.csv")[["LSOA21CD", "LAD26CD"]]
    d = lk.merge(cob, left_on="LSOA21CD", right_index=True)
    d["utla"] = d.LAD26CD.map(lad_to_area(level))
    g = d.dropna(subset=["utla"]).groupby("utla")
    return (100 * (1 - g["Europe: United Kingdom"].sum() / g["Total: All usual residents"].sum())).rename("pct_non_uk_born")


def build(level, admission_type="All"):
    panel = pd.read_csv(PROCESSED / f"{level}_panel_annual.csv")
    tb = pd.read_csv(PROCESSED / f"{level}_tb_annual.csv")
    exposure, coverage = apportion(trust_year_quantities(), level, admission_type)
    df = (panel[["utla", "year", "population"] + TIME_VARYING].merge(tb, on=["utla", "year"])
          .merge(exposure, on=["utla", "year"], how="left"))
    df = df.merge(census_non_uk_born(level), left_on="utla", right_index=True, how="left")
    df["principal_trust"] = df.utla.map(principal_trust(level))
    for g in GROUPS:
        df[f"rate_{g}"] = df.get(f"ddd_{g}", np.nan) / 365 / df.population * 1000
    # the candidate glucocorticoid exposure is prednisolone-equivalent mg per 1,000 residents per year
    df["rate_systemic_glucocorticoid"] = df["pred_mg_systemic_glucocorticoid"] / df.population * 1000
    df["rate_systemic_glucocorticoid_oral"] = df["pred_mg_systemic_glucocorticoid_oral"] / df.population * 1000
    return df, coverage


def z(s):
    return (s - s.mean()) / s.std()


def cross_sectional(df, level):
    period = df[df.year.isin(YEARS)]
    rates = [f"rate_{g}" for g in GROUPS]
    agg = period.groupby("utla").agg(tb_count=("tb_count", "sum"), person_years=("population", "sum"),
                                     **{r: (r, "mean") for r in rates}, **{c: (c, "mean") for c in CROSS_SECTIONAL_COVARS})
    rows = []
    for g in GROUPS:
        d = agg.dropna(subset=[f"rate_{g}"] + CROSS_SECTIONAL_COVARS)
        d = d[d[f"rate_{g}"] > 0]
        x = np.log(d[f"rate_{g}"])
        rho = x.corr(np.log((d.tb_count + 0.5) / d.person_years), method="spearman")
        X = sm.add_constant(pd.concat([z(x).rename("exposure")] + [z(d[c]) for c in CROSS_SECTIONAL_COVARS], axis=1))
        m = sm.NegativeBinomial(d.tb_count, X, exposure=d.person_years).fit(disp=0, maxiter=500, cov_type="HC1")
        b, (lo, hi) = m.params["exposure"], m.conf_int().loc["exposure"]
        rows.append(dict(level=level, design="cross-sectional 2019-24, adjusted", drug=g, model="per SD of log rate",
                         term="exposure", n=len(d), spearman_rho_log=rho, estimate=np.exp(b), ci_low=np.exp(lo),
                         ci_high=np.exp(hi), p=m.pvalues["exposure"]))
    return rows


def within_area(df, level, elective=None):
    base = df.copy()
    rates = [f"rate_{g}" for g in GROUPS]
    for lag in (1, -1):
        shifted = base[["utla", "year"] + rates].assign(year=base.year + lag)
        base = base.merge(shifted.rename(columns={r: f"{r}_lag{lag}" for r in rates}), on=["utla", "year"], how="left")
    base = base[base.year.isin(YEARS)].rename(columns={"year": "window_end", "population": "tb_denominator"})
    rows = []

    def run(label, d, exposures, **kwargs):
        d = d.dropna(subset=exposures + TIME_VARYING + ["tb_count"])
        d = d[(d[exposures] > 0).all(axis=1)]
        res = fit_ppml_multi(d, exposures, TIME_VARYING, **kwargs)
        for e in exposures:
            b, se = res.params[f"log_{e}"], res.bse[f"log_{e}"]
            rows.append(dict(level=level, design="within-area FE", drug=g, model=label,
                             term="t" if e.endswith(g) else ("t-1" if e.endswith("lag1") else "t+1"),
                             n=int(res.nobs), estimate=np.exp(b * K), ci_low=np.exp((b - 1.96 * se) * K),
                             ci_high=np.exp((b + 1.96 * se) * K), se_log_irr_10pct=se * K,
                             elasticity=b, p=res.pvalues[f"log_{e}"], years=f"{d.window_end.min()}-{d.window_end.max()}"))

    for g in GROUPS:
        x = f"rate_{g}"
        run("concurrent (t)", base, [x])
        run("lag (t-1)", base, [f"{x}_lag1"])
        run("lead (t+1)", base, [f"{x}_lag-1"])
        run("lag and lead jointly", base, [f"{x}_lag1", f"{x}_lag-1"])
        run("lag (t-1), clustered by principal trust", base, [f"{x}_lag1"], cluster="principal_trust")
        run("concurrent (t), clustered by principal trust", base, [x], cluster="principal_trust")
        run("lag (t-1), excluding outcome years 2020-21", base[~base.window_end.isin([2020, 2021])], [f"{x}_lag1"])
        if elective is not None:
            e = elective.rename(columns={"year": "window_end", "population": "tb_denominator"})
            e = e.merge(e[["utla", "window_end", x]].assign(window_end=e.window_end + 1)
                        .rename(columns={x: f"{x}_lag1"}), on=["utla", "window_end"], how="left")
            run("lag (t-1), elective catchments", e[e.window_end.isin(YEARS)], [f"{x}_lag1"])
            run("concurrent (t), elective catchments", e[e.window_end.isin(YEARS)], [x])
    return rows


def expected_effects(df, results, level):
    """MDE (lag model) versus expected population effects, with prevalence of use from SCMD
    patient-year equivalents, plus attenuation by the positive control's within-area elasticity."""
    national = df[df.year == 2024]
    positive = results[(results.drug == "antituberculosis_active") & (results.model == "concurrent (t)")]
    attenuation = float(positive.elasticity.iloc[0]) if len(positive) else np.nan
    rows = []
    for g, scenarios in RR_SCENARIOS.items():
        lag = results[(results.drug == g) & (results.model == "lag (t-1)")]
        trust_lag = results[(results.drug == g) & (results.model == "lag (t-1), clustered by principal trust")]
        if lag.empty:
            continue
        prevalence = national[f"ddd_{g}"].sum() / 365 / national.population.sum()
        for label, rr in scenarios:
            exp_irr = expected_irr(rr, prevalence)
            for se_label, r in [("clustered by area", lag.iloc[0]), ("clustered by principal trust", trust_lag.iloc[0])]:
                mde = np.exp(2.80 * r.se_log_irr_10pct)
                rows.append(dict(level=level, drug=g, scenario=label, prevalence_pct=100 * prevalence,
                                 expected_pct_change=100 * (exp_irr - 1),
                                 expected_pct_change_attenuated=100 * (exp_irr - 1) * attenuation,
                                 se_type=se_label, mde_pct=100 * (mde - 1),
                                 mde_to_expected=np.log(mde) / np.log(exp_irr),
                                 mde_to_expected_attenuated=np.log(mde) / (np.log(exp_irr) * attenuation)))
    out = pd.DataFrame(rows)
    out["positive_control_elasticity"] = attenuation
    return out


def main(level="utla"):
    df, coverage = build(level)
    coverage.to_csv(OUT / f"hospital_coverage_by_year_{level}.csv")
    elective, _ = build(level, "Elective")
    df.to_csv(PROCESSED / f"{level}_hospital_medicines_panel.csv", index=False)
    print(f"{level}: {df.utla.nunique()} areas; national patient-year equivalents per 1,000 residents:")
    print(df[df.year.isin(YEARS)].groupby("year")[[f"rate_{g}" for g in GROUPS]].mean().round(2).T.to_string())
    print("Coverage (share of DDD) by year:\n", coverage.round(3).to_string())

    results = pd.DataFrame(cross_sectional(df, level) + within_area(df, level, elective))
    results.to_csv(OUT / f"hospital_results_{level}.csv", index=False)
    expected = expected_effects(df, results, level)
    expected.to_csv(OUT / f"hospital_mde_{level}.csv", index=False)

    show = results.assign(est=results.apply(
        lambda r: f"{r.estimate:.3f} ({r.ci_low:.3f}-{r.ci_high:.3f}){'*' if r.p < 0.05 else ''}", axis=1))
    print(show.pivot_table(index="drug", columns=["model", "term"], values="est", aggfunc="first").loc[GROUPS].T.to_string())
    print(expected.round(3).to_string(index=False))


if __name__ == "__main__":
    main(*sys.argv[1:2])
