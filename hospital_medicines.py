"""Hospital-prescribed medicines and TB incidence by local authority, 2019-2024.

Exposure: NHS Secondary Care Medicines Data (SCMD; NHSBSA), trust x month x drug group
(fetch_scmd.py / summarise_scmd.py), apportioned to local authorities using OHID acute trust
catchment populations (share of each trust's catchment living in each area; 2024 catchment, all
admissions), per 1,000 residents per year.
  - quantity measure: approximate milligrams for each group; rifampicin defined daily doses (DDD)
    for antituberculosis drugs; indicative cost as a sensitivity measure.
Outcome: annual TB notifications (UKHSA regional reports).

Analyses, at UTLA and LTLA level:
  1. Positive control: hospital antituberculosis drug use should track TB incidence, between
     areas (cross-sectional) and within areas over time (fixed effects, concurrent year).
  2. Drug groups with plausible TB risk (anti-TNF, other biologics, JAK inhibitors, systemic
     corticosteroids, calcineurin inhibitors/antiproliferatives):
       - cross-sectional negative binomial, 2019-2024 totals, adjusted for % non-UK-born, age,
         in-migration, HIV and diabetes prevalence;
       - within-area Poisson PML, exposure in year t-1, and a lead (t+1) falsification test.

Usage: python hospital_medicines.py [utla|ltla]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analyze_panel import fit_ppml
from build_panel import MERGES, lad_to_area

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUT = ROOT / "outputs" / "hospital"
OUT.mkdir(parents=True, exist_ok=True)

GROUPS = ["antituberculosis", "anti_tnf", "other_biologic", "jak_inhibitor", "systemic_corticosteroid",
          "calcineurin_antiproliferative"]
SOURCE_PRIORITY = {"final": 0, "provisional": 1, "retired": 2}
YEARS = range(2019, 2025)
COVARS = ["pct_non_uk_born", "pct_age_65plus", "pct_age_15_44", "intl_in_per_1000", "hiv_prev", "diabetes_prev"]


def trust_year_quantities():
    s = pd.read_csv(RAW / "scmd" / "scmd_trust_month_group_summary.csv", dtype={"year_month": str})
    s["year_month"] = s.year_month.str.replace("-", "")
    s["priority"] = s.source.map(SOURCE_PRIORITY)
    s = s.sort_values("priority").drop_duplicates(["year_month", "ods_code", "group"])
    s["year"] = s.year_month.str[:4].astype(int)
    months = s.groupby("year").year_month.nunique()
    s = s[s.year.isin([y for y in YEARS if months.get(y, 0) == 12])]
    s["quantity"] = np.where(s.group == "antituberculosis", s.rif_ddd, s.approx_mg)
    return s.groupby(["ods_code", "group", "year"])[["quantity", "indicative_cost"]].sum().reset_index()


def apportion(q, level):
    c = pd.read_csv(RAW / "scmd" / "trust_catchment_la.csv")
    c = c[(c.year == 2024) & (c.admission_type == "All") & (c.la_level == level.upper())]
    c = c.assign(utla=c.la_code.replace(MERGES[level]))
    covered = q.ods_code.isin(c.trust_code)
    share = (q[covered].groupby("group").quantity.sum() / q.groupby("group").quantity.sum()).round(3)
    print(f"{level}: share of quantity from trusts with catchment data:", share.to_dict())
    m = q.merge(c[["trust_code", "utla", "prop_of_trust_catchment"]], left_on="ods_code", right_on="trust_code")
    for col in ("quantity", "indicative_cost"):
        m[col] = m[col] * m.prop_of_trust_catchment
    wide = m.groupby(["utla", "year", "group"])[["quantity", "indicative_cost"]].sum().unstack("group")
    wide.columns = [f"{'qty' if a == 'quantity' else 'cost'}_{g}" for a, g in wide.columns]
    return wide.reset_index()


def census_non_uk_born(level):
    cob = pd.read_csv(RAW / "census21_ts004_lsoa.csv").pivot_table(
        index="GEOGRAPHY_CODE", columns="C2021_COB_12_NAME", values="OBS_VALUE", aggfunc="sum")
    lk = pd.read_csv(RAW / "LSOA21_SICBL26_lookup.csv")[["LSOA21CD", "LAD26CD"]]
    d = lk.merge(cob, left_on="LSOA21CD", right_index=True)
    d["utla"] = d.LAD26CD.map(lad_to_area(level))
    g = d.dropna(subset=["utla"]).groupby("utla")
    return (100 * (1 - g["Europe: United Kingdom"].sum() / g["Total: All usual residents"].sum())).rename("pct_non_uk_born")


def build(level):
    panel = pd.read_csv(PROCESSED / f"{level}_panel_annual.csv")
    tb = pd.read_csv(PROCESSED / f"{level}_tb_annual.csv")
    df = (panel[["utla", "year", "population", "pct_age_65plus", "pct_age_15_44", "intl_in_per_1000",
                 "hiv_prev", "diabetes_prev"]]
          .merge(tb, on=["utla", "year"]).merge(apportion(trust_year_quantities(), level), on=["utla", "year"], how="left"))
    df = df.merge(census_non_uk_born(level), left_on="utla", right_index=True, how="left")
    for g in GROUPS:
        df[f"rate_{g}"] = df[f"qty_{g}"] / df.population * 1000
        df[f"costrate_{g}"] = df[f"cost_{g}"] / df.population * 1000
    return df


def z(s):
    return (s - s.mean()) / s.std()


def cross_sectional(df, level):
    period = df[df.year.isin(YEARS)]
    agg = period.groupby("utla").agg(tb_count=("tb_count", "sum"), person_years=("population", "sum"),
                                     **{f"rate_{g}": (f"rate_{g}", "mean") for g in GROUPS},
                                     **{c: (c, "mean") for c in COVARS}).dropna()
    rows = []
    for g in GROUPS:
        x = np.log(agg[f"rate_{g}"].clip(lower=agg[f"rate_{g}"][agg[f"rate_{g}"] > 0].min() / 2))
        rho = x.corr(np.log((agg.tb_count + 0.5) / agg.person_years), method="spearman")
        for label, covs in [("unadjusted", []), ("adjusted", COVARS)]:
            X = sm.add_constant(pd.concat([z(x).rename("exposure")] + [z(agg[c]) for c in covs], axis=1))
            m = sm.NegativeBinomial(agg.tb_count, X, exposure=agg.person_years).fit(disp=0, maxiter=500, cov_type="HC1")
            b, (lo, hi) = m.params["exposure"], m.conf_int().loc["exposure"]
            rows.append(dict(level=level, design="cross-sectional 2019-24", drug=g, model=label, n=len(agg),
                             spearman_rho_log=rho, effect="IRR per SD of log rate", estimate=np.exp(b),
                             ci_low=np.exp(lo), ci_high=np.exp(hi), p=m.pvalues["exposure"]))
    return rows


def within_area(df, level):
    rows = []
    base = df.rename(columns={"year": "window_end", "population": "tb_denominator"})
    for g in GROUPS:
        for label, shift in [("concurrent (t)", 0), ("lag (t-1)", 1), ("lead (t+1, falsification)", -1)]:
            x = base[["utla", "window_end", f"rate_{g}"]].assign(window_end=lambda f: f.window_end + shift)
            d = base.drop(columns=[f"rate_{g}"]).merge(x, on=["utla", "window_end"]).dropna(
                subset=["tb_count", f"rate_{g}"] + COVARS[1:])
            d = d[d[f"rate_{g}"] > 0]
            res = fit_ppml(d, f"rate_{g}", COVARS[1:])
            b, se = res.params["log_exposure"], res.bse["log_exposure"]
            k = np.log(1.1)
            rows.append(dict(level=level, design="within-area FE", drug=g, model=label, n=int(res.nobs),
                             effect="IRR per 10% increase", estimate=np.exp(b * k), ci_low=np.exp((b - 1.96 * se) * k),
                             ci_high=np.exp((b + 1.96 * se) * k), p=res.pvalues["log_exposure"]))
    return rows


def main(level="utla"):
    df = build(level)
    df.to_csv(PROCESSED / f"{level}_hospital_medicines_panel.csv", index=False)
    print(f"{level}: {df.utla.nunique()} areas; mean rates per 1,000 residents per year:")
    print(df.groupby("year")[[f"rate_{g}" for g in GROUPS]].mean().round(1).to_string())
    res = pd.DataFrame(cross_sectional(df, level) + within_area(df, level))
    res.to_csv(OUT / f"hospital_results_{level}.csv", index=False)
    show = res.assign(est=res.apply(lambda r: f"{r.estimate:.3f} ({r.ci_low:.3f}-{r.ci_high:.3f}){'*' if r.p < 0.05 else ''}", axis=1))
    print(show.pivot_table(index="drug", columns=["design", "model"], values="est", aggfunc="first").loc[GROUPS].to_string())
    print(res[res.design.str.startswith("cross")].groupby("drug").spearman_rho_log.first().round(3).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:2])
