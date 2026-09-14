"""Descriptive checks of SCMD extraction and linkage to OHID trust catchments (no modelling)."""
from pathlib import Path

import pandas as pd

D = Path(__file__).parent / "data/raw/scmd"
g = pd.read_csv(D / "scmd_trust_month_groups.csv")
s = pd.read_csv(D / "scmd_trust_month_group_summary.csv")
v = pd.read_csv(D / "scmd_trust_month_vmp.csv.gz", dtype={"VMP_SNOMED_CODE": str})
c = pd.read_csv(D / "trust_catchment_la.csv")
out = []
p = lambda *a: out.append(" ".join(str(x) for x in a))  # noqa

p("months:", s.year_month.min(), "-", s.year_month.max(), "n months", s.year_month.nunique())
allm = pd.period_range(pd.Period(str(s.year_month.min()), "M"), pd.Period(str(s.year_month.max()), "M"), freq="M")
have = set(pd.PeriodIndex([pd.Period(str(x), "M") for x in s.year_month.unique()]))
p("missing months:", [str(x) for x in allm if x not in have])
p("rows vmp-level:", len(v), "excluded rows:", int(v.excluded.sum()), "groups file:", len(g), "summary file:", len(s))
p("trusts per month (median):", s.groupby("year_month").ods_code.nunique().median(),
  "distinct trusts ever:", s.ods_code.nunique())
p(s.groupby("source").year_month.agg(["min", "max", "nunique"]).to_string())

# dominant unit per group
dom = g.groupby(["group", "unit"]).total_quantity.sum().reset_index().sort_values("total_quantity", ascending=False)
p("\nTop units per group:\n" + dom.groupby("group").head(3).to_string(index=False))

# national annual totals (calendar year) of approx mg and cost
s["year"] = s.year_month // 100
ann = s.groupby(["group", "year"]).agg(mg=("approx_mg", "sum"), cost=("indicative_cost", "sum"),
                                       trusts=("ods_code", "nunique")).reset_index()
p("\nAnnual approx mg (kg) by group:\n" + ann.assign(kg=lambda x: (x.mg / 1e6).round(1)).pivot(
    index="year", columns="group", values="kg").to_string())

# national monthly anti-TNF and anti-TB
nat = s[s.group.isin(["anti_tnf", "antituberculosis"])].pivot_table(
    index="year_month", columns="group", values=["approx_mg", "rif_ddd", "antitb_tabcap", "ods_code"],
    aggfunc={"approx_mg": "sum", "rif_ddd": "sum", "antitb_tabcap": "sum", "ods_code": "nunique"})
nat.columns = [f"{a}_{b}" for a, b in nat.columns]
nat = nat[["approx_mg_anti_tnf", "ods_code_anti_tnf", "rif_ddd_antituberculosis", "antitb_tabcap_antituberculosis",
           "ods_code_antituberculosis"]]
nat.to_csv(D / "scmd_national_monthly_antitnf_antitb.csv")
p("\nNational monthly (anti-TNF g; rifampicin DDD; anti-TB tabs/caps; trusts):\n" + nat.assign(
    approx_mg_anti_tnf=lambda x: (x.approx_mg_anti_tnf / 1000).round(0)).round(0).to_string())

# adalimumab by substance mg
sub = v[~v.excluded].assign(year=lambda x: x.YEAR_MONTH // 100).groupby(["substance", "year"]).approx_mg.sum().unstack()
p("\nApprox kg by substance and year:\n" + (sub / 1e6).round(2).to_string())

# dexamethasone monthly mg (COVID surge)
dex = v[(~v.excluded) & (v.substance == "dexamethasone")].groupby("YEAR_MONTH").agg(
    mg=("approx_mg", "sum"), trusts=("ODS_CODE", "nunique"))
p("\nDexamethasone monthly g (trusts):\n" + (dex.assign(g=lambda x: (x.mg / 1000).round(0))[["g", "trusts"]]).to_string())

# top trusts
for grp in ["anti_tnf", "antituberculosis", "other_biologic", "jak_inhibitor"]:
    t = s[s.group == grp].groupby("ods_code").approx_mg.sum().sort_values(ascending=False)
    p(f"\nTop trusts {grp} (share of approx mg):", (t / t.sum()).head(8).round(3).to_dict())

# catchment coverage
ct = set(c.trust_code.unique())
s["in_catchment"] = s.ods_code.isin(ct)
p("\nSCMD trusts in catchment:", s.loc[s.in_catchment, "ods_code"].nunique(), "not:", s.loc[~s.in_catchment, "ods_code"].nunique())
recent = s[s.year_month >= 202204]
cov = recent.groupby(["group", "in_catchment"]).agg(mg=("approx_mg", "sum"), cost=("indicative_cost", "sum")).reset_index()
tot = cov.groupby("group")[["mg", "cost"]].transform("sum")
cov["share_mg"] = (cov.mg / tot.mg).round(3)
cov["share_cost"] = (cov.cost / tot.cost).round(3)
p("\nShare of group quantity (approx mg) & indicative cost from trusts with/without catchment, 2022-04 onward:\n" +
  cov[["group", "in_catchment", "share_mg", "share_cost"]].to_string(index=False))
nc = recent[~recent.in_catchment].groupby("ods_code").indicative_cost.sum().sort_values(ascending=False)
p("\nTop non-catchment SCMD trusts by indicative cost (all groups, 2022-04+):", (nc / 1e6).round(2).head(15).to_dict())
pd.DataFrame({"ods_code": nc.index, "cost_gbp_2204_on": nc.values}).to_csv(D / "scmd_trusts_without_catchment.csv", index=False)
p("\nCatchment trusts absent from SCMD 2022-04+:", sorted(ct - set(recent.ods_code)))
print("\n".join(out))
(D / "scmd_summary.txt").write_text("\n".join(out))
