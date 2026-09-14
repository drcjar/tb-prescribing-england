"""Build the Sub-ICB location (April 2026 boundaries) analysis dataset.

Outcome:    TB incidence, three-year average 2022-24 (UKHSA Fingertips indicator 91361),
            published on April 2024 Sub-ICB boundaries and re-apportioned to 2026 boundaries
            using mid-2022 LSOA population weights.
Exposures:  GP/primary care prescribing, June 2026 (NHSBSA English Prescribing Dataset),
            items per 1,000 registered patients for pre-specified drug groups.
Covariates: Census 2021 % born outside the UK, IMD 2025 (population-weighted score),
            registered-list age structure (June 2026), QOF diabetes prevalence 2024/25.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# Pre-specified exposure groups. `code` = regex on BNF chemical substance code,
# `name` = case-insensitive regex on substance name; both given => both must match.
DRUG_GROUPS = {
    # positive control / reverse-causation check (LTBI and active TB treatment)
    "antituberculosis": dict(code=r"^0501090"),
    "oral_corticosteroids": dict(code=r"^0603020"),
    "inhaled_corticosteroids": dict(code=r"^0302000"),
    "immunosuppressants": dict(name=r"^(?:methotrexate|leflunomide|azathioprine|mycophenol|ciclosporin|tacrolimus|sirolimus|everolimus|tofacitinib|baricitinib|upadacitinib|filgotinib)"),
    "proton_pump_inhibitors": dict(code=r"^0103050"),
    "statins": dict(code=r"^0212000", name=r"statin"),
    "metformin": dict(name=r"metformin"),
    "insulins": dict(code=r"^060101"),
    "fluoroquinolones": dict(name=r"^(?:ciprofloxacin|levofloxacin|moxifloxacin|ofloxacin)"),
    "all_antibacterials": dict(code=r"^0501"),
    "vitamin_d": dict(name=r"^(?:colecalciferol|ergocalciferol)"),
    # negative control exposure: no plausible causal pathway to TB
    "levothyroxine": dict(name=r"^levothyroxine"),
}
# eye, ear/nose and skin preparations (e.g. topical tacrolimus, ciclosporin eye drops)
EXCLUDE_CHAPTERS = r"^(11|12|13)"


def load_lookups():
    imd = pd.read_csv(RAW / "imd2025_file7.csv")
    imd = imd.rename(columns={
        "LSOA code (2021)": "LSOA21CD",
        "Index of Multiple Deprivation (IMD) Score": "imd_score",
        "Total population: mid 2022": "population",
    })[["LSOA21CD", "imd_score", "population"]]
    l24 = pd.read_csv(RAW / "LSOA21_SICBL24_lookup.csv")[["LSOA21CD", "SICBL24CD"]]
    l26 = pd.read_csv(RAW / "LSOA21_SICBL26_lookup.csv")[
        ["LSOA21CD", "SICBL26CD", "SICBL26CDH", "SICBL26NM", "ICB26NM", "NHSER26NM"]]
    lsoa = l26.merge(l24, on="LSOA21CD", how="left").merge(imd, on="LSOA21CD", how="left")
    assert lsoa.population.notna().all() and lsoa.SICBL24CD.notna().all()
    return lsoa


def build_crosswalk(lsoa):
    xw = lsoa.groupby(["SICBL24CD", "SICBL26CD"], as_index=False)["population"].sum()
    xw["share_of_24"] = xw["population"] / xw.groupby("SICBL24CD")["population"].transform("sum")
    n_src = xw.groupby("SICBL26CD")["SICBL24CD"].transform("nunique")
    xw["boundary_changed"] = (n_src > 1) | (xw["share_of_24"] < 0.999)
    return xw


def fingertips(path, indicator, period):
    f = pd.read_csv(RAW / path)
    f = f[(f["Indicator ID"] == indicator) & (f["Time period"] == period) & (f["Area Type"] != "England")]
    # Fingertips publishes Surrey Heartlands (92A) and Sussex (70F) under their pre-2024 ONS codes
    f = f.replace({"Area Code": {"E38000246": "E38000264", "E38000248": "E38000265"}})
    return f.rename(columns={"Area Code": "SICBL24CD"})


def tb_outcome(xw):
    tb = fingertips("tb_incidence_3yr_at66.csv", 91361, "2022 - 24")
    tb = tb[["SICBL24CD", "Area Name", "Count", "Denominator", "Value note"]]
    missing24 = sorted(set(xw.SICBL24CD) - set(tb.SICBL24CD))
    print("2024 Sub-ICBs absent from Fingertips TB data:", missing24)
    print("Suppressed/annotated TB rows:\n", tb[tb["Value note"].notna()].to_string())
    d = xw.merge(tb, on="SICBL24CD", how="left")
    d["cnt_w"] = d["share_of_24"] * d["Count"]
    d["den_w"] = d["share_of_24"] * d["Denominator"]
    out = d.groupby("SICBL26CD").agg(
        tb_count=("cnt_w", "sum"),
        tb_denominator=("den_w", "sum"),
        tb_any_missing=("Count", lambda s: s.isna().any()),
        boundary_changed=("boundary_changed", "any"),
    )
    out.loc[out.tb_any_missing, ["tb_count", "tb_denominator"]] = np.nan
    out["tb_rate_per_100k"] = out.tb_count / out.tb_denominator * 1e5
    return out.drop(columns="tb_any_missing")


def diabetes_covariate(xw):
    dm = fingertips("covars_fingertips_at66.csv", 241, "2024/25")[["SICBL24CD", "Value"]]
    d = xw.merge(dm, on="SICBL24CD", how="left")
    d["wv"] = d["population"] * d["Value"]
    g = d.groupby("SICBL26CD")
    prev = g["wv"].sum() / g["population"].sum()
    prev[g["Value"].apply(lambda s: s.isna().any())] = np.nan
    return prev.rename("diabetes_prev")


def lsoa_covariates(lsoa):
    cob = pd.read_csv(RAW / "census21_ts004_lsoa.csv")
    cob = cob.pivot_table(index="GEOGRAPHY_CODE", columns="C2021_COB_12_NAME", values="OBS_VALUE", aggfunc="sum")
    cob = cob.rename(columns={"Total: All usual residents": "residents", "Europe: United Kingdom": "uk_born"})
    d = lsoa.merge(cob, left_on="LSOA21CD", right_index=True, how="left")
    assert d.residents.notna().all()
    d["imd_x_pop"] = d.imd_score * d.population
    g = d.groupby("SICBL26CD")
    return pd.DataFrame({
        "pct_non_uk_born": 100 * (1 - g.uk_born.sum() / g.residents.sum()),
        "imd_score": g.imd_x_pop.sum() / g.population.sum(),
        "resident_pop_mid2022": g.population.sum(),
    })


def registered_population(ods_to_ons):
    # June 2026 file mixes 2024 and 2026 ONS codes for re-organised areas, so link on ODS code
    reg = pd.read_csv(RAW / "gp-reg-pat-prac-quin-age.csv", dtype=str)
    reg = reg[(reg.ORG_TYPE == "SUB_ICB_LOCATION_CODE") & reg.ORG_CODE.isin(ods_to_ons)].copy()
    reg["ONS_CODE"] = reg.ORG_CODE.map(ods_to_ons)
    print(f"Sub-ICBs with registration data: {reg.ONS_CODE.nunique()} of {len(ods_to_ons)}")
    reg["n"] = reg.NUMBER_OF_PATIENTS.astype(float)
    total = reg[(reg.SEX == "ALL") & (reg.AGE_GROUP_5 == "ALL")].groupby("ONS_CODE").n.sum()
    by_age = reg[reg.SEX.isin(["MALE", "FEMALE"]) & (reg.AGE_GROUP_5 != "ALL")].copy()
    by_age["lower"] = by_age.AGE_GROUP_5.map(lambda g: int(re.match(r"\d+", g).group()))
    g = by_age.groupby("ONS_CODE")
    persons = g.n.sum()
    return pd.DataFrame({
        "registered_patients": total,
        "pct_age_65plus": 100 * by_age[by_age.lower >= 65].groupby("ONS_CODE").n.sum() / persons,
        "pct_age_15_44": 100 * by_age[(by_age.lower >= 15) & (by_age.lower < 45)].groupby("ONS_CODE").n.sum() / persons,
    })


def prescribing(sicbl_cdh):
    e = pd.read_csv(RAW / "epd_202606_pco_substance.csv.gz", dtype={"PCO_CODE": str, "BNF_CHEMICAL_SUBSTANCE_CODE": str})
    e["SICBL26CDH"] = e.PCO_CODE.where(e.PCO_CODE.isin(sicbl_cdh), e.PCO_CODE.str.replace(r"00$", "", regex=True))
    matched = e.SICBL26CDH.isin(sicbl_cdh)
    print(f"Prescribing items linked to a Sub-ICB: {e.ITEMS[matched].sum() / e.ITEMS.sum():.2%}")
    e = e[matched]

    code = e.BNF_CHEMICAL_SUBSTANCE_CODE.fillna("")
    name = e.BNF_CHEMICAL_SUBSTANCE.fillna("")
    listing, rates = [], {"total_items": e.groupby("SICBL26CDH").ITEMS.sum()}
    for group, rule in DRUG_GROUPS.items():
        mask = ~code.str.match(EXCLUDE_CHAPTERS)
        if "code" in rule:
            mask &= code.str.match(rule["code"])
        if "name" in rule:
            mask &= name.str.contains(rule["name"], case=False, regex=True)
        sub = e[mask]
        rates[f"items_{group}"] = sub.groupby("SICBL26CDH").ITEMS.sum()
        listing.append(sub.groupby(["BNF_CHEMICAL_SUBSTANCE_CODE", "BNF_CHEMICAL_SUBSTANCE"], as_index=False)
                       .ITEMS.sum().assign(group=group))
    pd.concat(listing).sort_values(["group", "ITEMS"], ascending=[True, False]).to_csv(
        OUT / "drug_group_substances.csv", index=False)
    return pd.DataFrame(rates).fillna(0)


def main():
    lsoa = load_lookups()
    xw = build_crosswalk(lsoa)
    xw.to_csv(OUT / "crosswalk_sicbl24_to_sicbl26.csv", index=False)

    areas = lsoa.drop_duplicates("SICBL26CD").set_index("SICBL26CD")[["SICBL26CDH", "SICBL26NM", "ICB26NM", "NHSER26NM"]]
    areas = areas.rename(columns={"NHSER26NM": "region"})
    df = (areas.join(tb_outcome(xw)).join(diabetes_covariate(xw)).join(lsoa_covariates(lsoa))
          .join(registered_population(dict(zip(areas.SICBL26CDH, areas.index)))))

    rx = prescribing(set(areas.SICBL26CDH))
    df = df.merge(rx, left_on="SICBL26CDH", right_index=True, how="left")
    for col in [c for c in rx.columns if c.startswith("items_")] + ["total_items"]:
        df["rate_" + col.removeprefix("items_")] = df[col] / df.registered_patients * 1000

    print(df.describe().T.round(2).to_string())
    print("Areas with missing values:\n", df[df.isna().any(axis=1)].iloc[:, :4])
    df.to_csv(OUT / "sicbl26_analysis.csv")
    print(f"Wrote {len(df)} Sub-ICB locations to {OUT / 'sicbl26_analysis.csv'}")


if __name__ == "__main__":
    main()
