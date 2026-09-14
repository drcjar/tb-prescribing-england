"""Product classification (DDD / prednisolone-equivalent) and trust successor mapping for SCMD extracts.

Reads (does not modify):
  data/raw/scmd/scmd_trust_month_vmp.csv.gz   trust x month x VMP extract (fetch_scmd.py)
  data/raw/scmd/trust_catchment_la.csv        trust catchments (year 2024, admission_type All used)
  NHS ODS ORD API (cached JSON in data/raw/scmd/ods_ord_cache/)

Writes (data/raw/scmd/):
  vmp_classification.csv                one row per (VMP code, product name, upper-case unit)
  vmp_national_annual_by_group.csv      2019-2024 national totals by new_group (DDD, patient-years, pred-equiv mg)
  vmp_national_annual_by_substance.csv  2019-2024 composition by substance within group
  trust_successor_map.csv               SCMD ODS codes absent from 2024 catchment -> successor chain
  trust_match_share_by_group.csv        share of DDD matched directly / via successor / unmatched, by year x group

WHO ATC/DDD values were checked against https://atcddd.fhi.no/atc_ddd_index/ on 2026-09-14.
"""
import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

D = Path(__file__).parent / "data/raw/scmd"
CACHE = D / "ods_ord_cache"
CACHE.mkdir(exist_ok=True)
ORD = "https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/"
YEARS = range(2019, 2025)

# --------------------------------------------------------------------------------------------------
# Reference tables
# --------------------------------------------------------------------------------------------------
GROUP_OF = {
    "adalimumab": "tnf_inhibitor", "infliximab": "tnf_inhibitor", "etanercept": "tnf_inhibitor",
    "certolizumab pegol": "tnf_inhibitor", "golimumab": "tnf_inhibitor",
    "tocilizumab": "il6_abatacept", "sarilumab": "il6_abatacept", "abatacept": "il6_abatacept",
    "tofacitinib": "jak_inhibitor_rheum", "baricitinib": "jak_inhibitor_rheum",
    "upadacitinib": "jak_inhibitor_rheum", "filgotinib": "jak_inhibitor_rheum",
    "ruxolitinib": "ruxolitinib", "rituximab": "rituximab",
    "secukinumab": "low_tb_risk_biologic", "ixekizumab": "low_tb_risk_biologic",
    "ustekinumab": "low_tb_risk_biologic", "vedolizumab": "low_tb_risk_biologic", "anakinra": "low_tb_risk_biologic",
    "prednisolone": "systemic_glucocorticoid", "prednisone": "systemic_glucocorticoid",
    "methylprednisolone": "systemic_glucocorticoid", "dexamethasone": "systemic_glucocorticoid",
    "hydrocortisone": "systemic_glucocorticoid", "deflazacort": "systemic_glucocorticoid",
    "tacrolimus": "transplant_cni_mtor", "ciclosporin": "transplant_cni_mtor",
    "sirolimus": "transplant_cni_mtor", "everolimus": "transplant_cni_mtor",
    "mycophenolate mofetil": "antiproliferative", "mycophenolic acid": "antiproliferative",
    "azathioprine": "antiproliferative", "methotrexate": "antiproliferative",
    "pyrazinamide": "antituberculosis_active", "ethambutol": "antituberculosis_active",
    "rifampicin": "antituberculosis_rifamycin_isoniazid", "isoniazid": "antituberculosis_rifamycin_isoniazid",
    "rifapentine": "antituberculosis_rifamycin_isoniazid",
    "bedaquiline": "antituberculosis_mdr", "delamanid": "antituberculosis_mdr",
}
# substance search order (longest / most specific first)
SUBST_ORDER = ["methylprednisolone", "prednisolone", "prednisone", "deflazacort", "dexamethasone", "hydrocortisone",
               "mycophenolic acid", "mycophenolate mofetil", "certolizumab pegol"] + \
              [s for s in GROUP_OF if s not in ("methylprednisolone", "prednisolone", "prednisone", "deflazacort",
                                                "dexamethasone", "hydrocortisone", "mycophenolic acid",
                                                "mycophenolate mofetil", "certolizumab pegol")]

# (ddd_mg, source) keyed by (substance, route) with route in {"O","P"}; "*" = any route.
W = "WHO ATC/DDD index (atcddd.fhi.no, checked 2026-09-14)"
DDD = {
    ("adalimumab", "*"): (2.9, W), ("etanercept", "*"): (7.0, W), ("certolizumab pegol", "*"): (14.0, W),
    ("golimumab", "*"): (1.66, W),
    ("infliximab", "P_iv"): (6.25, "defined maintenance dose: 5 mg/kg x 70 kg every 8 weeks (WHO DDD 3.75 mg judged unrepresentative)"),
    ("infliximab", "P_sc"): (8.57, "defined maintenance dose: SC 120 mg every 2 weeks (no separate WHO DDD for SC)"),
    ("tocilizumab", "*"): (20.0, W + "; equals 8 mg/kg x 70 kg every 4 weeks"), ("sarilumab", "*"): (14.3, W),
    ("abatacept", "*"): (27.0, W),
    ("tofacitinib", "*"): (10.0, W), ("baricitinib", "*"): (3.0, W), ("upadacitinib", "*"): (15.0, W),
    ("filgotinib", "*"): (200.0, W), ("ruxolitinib", "*"): (30.0, W + " (L01EJ01)"),
    ("rituximab", "*"): (5.48, "defined maintenance dose: 1 g x 2 every 6 months (2000 mg/365 d); WHO has no DDD (L01FA01)"),
    ("secukinumab", "*"): (10.0, W), ("ixekizumab", "*"): (2.9, W), ("anakinra", "*"): (100.0, W),
    ("ustekinumab", "P_sc"): (0.54, W),
    ("ustekinumab", "P_iv"): (6.96, "defined induction dose: 130 mg x3 (~6 mg/kg) covering 8 weeks before first SC dose; WHO 0.54 mg unrepresentative for IV induction"),
    ("vedolizumab", "*"): (5.4, W),
    ("prednisolone", "*"): (10.0, W), ("prednisone", "*"): (10.0, W), ("dexamethasone", "*"): (1.5, W),
    ("methylprednisolone", "O"): (7.5, W), ("methylprednisolone", "P"): (20.0, W + " (parenteral 20 mg)"),
    ("hydrocortisone", "*"): (30.0, W), ("deflazacort", "*"): (15.0, W),
    ("tacrolimus", "*"): (5.0, W), ("ciclosporin", "*"): (250.0, W),
    ("sirolimus", "*"): (3.0, "WHO ATC/DDD index (not re-checked; substance absent from extract)"),
    ("everolimus", "*"): (1.5, "WHO ATC/DDD index L04AH02 (not re-checked; substance absent from extract)"),
    ("mycophenolate mofetil", "*"): (2000.0, W + " (as mycophenolate mofetil)"),
    ("mycophenolic acid", "*"): (1440.0, "derived: WHO 2 g as mycophenolate mofetil ~ 1440 mg mycophenolic acid (as sodium; 720 mg = 1 g MMF)"),
    ("azathioprine", "*"): (150.0, W), ("methotrexate", "*"): (2.5, W + " (L04AX03)"),
    ("pyrazinamide", "*"): (1500.0, W), ("ethambutol", "*"): (1200.0, W),
    ("rifampicin", "*"): (600.0, W), ("isoniazid", "O"): (300.0, W),
    ("isoniazid", "P"): (300.0, "WHO oral DDD applied (WHO lists no parenteral DDD for isoniazid)"),
    ("rifapentine", "*"): (110.0, W), ("bedaquiline", "*"): (86.0, W), ("delamanid", "*"): (200.0, W),
}
PRED_EQ = {"prednisolone": 1.0, "prednisone": 1.0, "methylprednisolone": 1.25, "dexamethasone": 6.67,
           "hydrocortisone": 0.25, "deflazacort": 0.83}
# Fixed-dose combinations (mg per tablet/capsule): rifampicin, isoniazid, pyrazinamide, ethambutol
FDC = [
    (r"voractiv", dict(rifampicin=150, isoniazid=75, pyrazinamide=400, ethambutol=275)),
    (r"rifater", dict(rifampicin=120, isoniazid=50, pyrazinamide=300)),
    (r"rifampicin 150mg / isoniazid 100mg", dict(rifampicin=150, isoniazid=100)),
    (r"rifampicin 300mg / isoniazid 150mg", dict(rifampicin=300, isoniazid=150)),
]

TOPICAL = (r"cream|ointment|\beye\b|\bear\b|drops|inhal|nasal|\bgel\b|foam|enema|suppositor|spray|rectal|buccal|"
           r"oromucosal|mouthwash|lozenge|intravitreal|implant|cutaneous|lotion|scalp|dental|paste|emulsion|"
           r"soft paraffin|\bpowder$")
DEPOT = r"suspension for injection|lidocaine|acetate .*injection"
PARENT = r"injection|infusion|\bvials?\b|ampoules?|pre-filled|cartridge"
ORAL = r"tablet|capsule|\boral\b|granules|sachet"
UNIT_MG = {"mg": 1.0, "microgram": 1e-3, "micrograms": 1e-3, "g": 1000.0}
STRENGTH = re.compile(r"(\d+(?:\.\d+)?)\s*(mg|micrograms?|g)\b(?:\s*/\s*(\d+(?:\.\d+)?)?\s*ml)?", re.I)


def strength(name, unit):
    """(mg per UNIT, numerator mg, volume ml) for the first-named strength."""
    m = STRENGTH.search(name)
    if not m:
        return None, None, None
    mg = float(m.group(1)) * UNIT_MG[m.group(2).lower()]
    per_ml = "/" in m.group(0)
    vol = float(m.group(3)) if m.group(3) else (1.0 if per_ml else None)
    if unit == "ML":
        return (mg / vol if per_ml else None), mg, vol
    if unit in ("GRAM", "DOSE", "APPLICATION", "ACTUATION"):
        return None, mg, vol
    return mg, mg, vol  # TABLET, CAPSULE, VIAL, SACHET, DEVICE, SUPPOSITORY, pre-filled syringe/pen counts


def classify(code, name, unit):
    low = name.lower()
    r = dict(vmp_snomed_code=code, vmp_product_name=name, unit=unit, substances="", new_group="exclude",
             route_class="", mg_per_unit=np.nan, rifampicin_mg_per_unit=np.nan, isoniazid_mg_per_unit=np.nan,
             pyrazinamide_mg_per_unit=np.nan, ethambutol_mg_per_unit=np.nan, ddd_mg=np.nan, ddd_source="",
             pred_equiv_factor=np.nan, include=False, notes=[])
    # route
    if re.search(TOPICAL, low) or unit in ("GRAM", "SUPPOSITORY", "APPLICATION", "ACTUATION", "DEVICE"):
        r["route_class"] = "topical_other"
    elif re.search(DEPOT, low):
        r["route_class"] = "intra_articular_depot"
    elif re.search(PARENT, low):
        r["route_class"] = "parenteral_systemic"
    elif re.search(ORAL, low):
        r["route_class"] = "oral"
    else:
        r["route_class"] = "topical_other"
        r["notes"].append("route not recognised")
    # substance(s)
    fdc = next((v for pat, v in FDC if re.search(pat, low)), None)
    if fdc:
        subs = list(fdc)
        for s, mg in fdc.items():
            r[f"{s}_mg_per_unit"] = mg
        principal = "pyrazinamide" if "pyrazinamide" in fdc else "rifampicin"
        r["mg_per_unit"] = fdc[principal]
        r["notes"].append(f"fixed-dose combination; hard-coded strengths; mg_per_unit/DDD refer to {principal}")
    else:
        subs = [s for s in SUBST_ORDER if s in low and not (s == "prednisolone" and "methylprednisolone" in low)]
        subs = subs[:1]
        principal = subs[0] if subs else None
        r["mg_per_unit"], num_mg, vol = strength(name, unit)
        if principal in ("rifampicin", "isoniazid", "pyrazinamide", "ethambutol"):
            r[f"{principal}_mg_per_unit"] = r["mg_per_unit"]
    r["substances"] = "+".join(subs)
    if principal is None:
        r["notes"].append("no candidate substance")
        return finish(r)
    grp = GROUP_OF[principal]
    route_is_P = r["route_class"] != "oral"
    # exclusions / special cases
    if r["route_class"] in ("topical_other", "intra_articular_depot"):
        r["notes"].append(f"non-systemic ({r['route_class']})")
        return finish(r, grp_hint=grp, principal=principal)
    if principal == "hydrocortisone" and "acetate" in low:
        r["notes"].append("hydrocortisone acetate: local/depot")
        return finish(r, grp_hint=grp, principal=principal)
    if principal == "methotrexate" and not fdc:
        _, num_mg, vol = strength(name, unit)
        pfs = re.search(r"pre-filled|cartridge", low)
        if r["route_class"] == "oral":
            r["notes"].append("low-dose methotrexate (oral)")
        elif pfs and num_mg is not None and num_mg <= 30:
            r["notes"].append("low-dose methotrexate (SC pre-filled syringe/pen <= 30 mg)")
        else:
            conc = (num_mg / vol) if (num_mg and vol) else None
            why = "vial/infusion" if not pfs else "pre-filled syringe > 30 mg (not a rheumatology strength)"
            r["notes"].append(f"methotrexate {why}; conc {conc} mg/ml - oncology/other, excluded")
            return finish(r, grp_hint=grp, principal=principal)
    if principal == "everolimus" and (r["mg_per_unit"] or 0) not in (0.25, 0.5, 0.75, 1.0):
        r["notes"].append("oncology everolimus strength")
        return finish(r, grp_hint=grp, principal=principal)
    r["new_group"] = grp
    r["include"] = True
    # route-specific DDD key
    if principal in ("infliximab", "ustekinumab"):
        rk = "P_iv" if re.search(r"infusion", low) else "P_sc"
    else:
        rk = "P" if route_is_P else "O"
    ddd = DDD.get((principal, rk)) or DDD.get((principal, "*"))
    r["ddd_mg"], r["ddd_source"] = ddd
    if principal in PRED_EQ:
        r["pred_equiv_factor"] = PRED_EQ[principal]
    if principal == "hydrocortisone" and r["route_class"] == "oral":
        r["notes"].append("oral hydrocortisone largely physiological adrenal replacement")
    if principal == "dexamethasone" and r["route_class"] == "parenteral_systemic":
        r["notes"].append("parenteral dexamethasone includes antiemetic/perioperative and some local use")
    if principal == "rituximab":
        r["notes"].append("rituximab mostly haematological malignancy; indication not identifiable")
    if principal == "isoniazid" and "rifampicin" not in subs:
        r["notes"].append("isoniazid monotherapy (largely LTBI)")
    if r["mg_per_unit"] is None or pd.isna(r["mg_per_unit"]):
        r["notes"].append("mg_per_unit not derivable")
    return finish(r)


def finish(r, grp_hint=None, principal=None):
    if grp_hint and r["new_group"] == "exclude":
        r["notes"].insert(0, f"would be {grp_hint}")
    r["notes"] = "; ".join(r["notes"])
    return r


# --------------------------------------------------------------------------------------------------
# Task A
# --------------------------------------------------------------------------------------------------
def load_vmp():
    v = pd.read_csv(D / "scmd_trust_month_vmp.csv.gz",
                    usecols=["YEAR_MONTH", "ODS_CODE", "VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT", "QTY"],
                    dtype={"YEAR_MONTH": str, "ODS_CODE": str, "VMP_SNOMED_CODE": str, "VMP_PRODUCT_NAME": str,
                           "UNIT": str, "QTY": float})
    v["year"] = v.YEAR_MONTH.str.replace("-", "").str[:4].astype(int)
    v["UNIT"] = v.UNIT.str.upper()
    return v.drop(columns="YEAR_MONTH")


def build_classification(v):
    keys = v[["VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT"]].drop_duplicates()
    cls = pd.DataFrame([classify(*k) for k in keys.itertuples(index=False)])
    tot = v.groupby(["VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT"]).QTY.sum().rename("total_qty_all_months")
    cls = cls.merge(tot, left_on=["vmp_snomed_code", "vmp_product_name", "unit"], right_index=True)
    cls["ddd_per_unit"] = cls.mg_per_unit / cls.ddd_mg
    cls = cls.sort_values(["new_group", "substances", "vmp_product_name"])
    cls.to_csv(D / "vmp_classification.csv", index=False)
    return cls


def national_summary(v, cls):
    k = ["VMP_SNOMED_CODE", "VMP_PRODUCT_NAME", "UNIT"]
    c = cls.rename(columns={"vmp_snomed_code": k[0], "vmp_product_name": k[1], "unit": k[2]})
    x = v[v.year.isin(YEARS)].merge(c, on=k)
    x["ddd"] = x.QTY * x.ddd_per_unit
    x["pred_eq_mg"] = x.QTY * x.mg_per_unit * x.pred_equiv_factor
    x["rif_ddd"] = x.QTY * x.rifampicin_mg_per_unit / 600
    inc = x[x.include]
    g = inc.groupby(["new_group", "year"]).agg(ddd=("ddd", "sum"), pred_eq_mg=("pred_eq_mg", "sum"),
                                               rif_ddd=("rif_ddd", "sum")).reset_index()
    g["patient_years"] = g.ddd / 365
    g.to_csv(D / "vmp_national_annual_by_group.csv", index=False)
    s = inc.groupby(["new_group", "substances", "route_class", "year"]).agg(ddd=("ddd", "sum"),
                                                                           pred_eq_mg=("pred_eq_mg", "sum")).reset_index()
    s["patient_years"] = s.ddd / 365
    s["share_of_group_ddd"] = s.ddd / s.groupby(["new_group", "year"]).ddd.transform("sum")
    s.to_csv(D / "vmp_national_annual_by_substance.csv", index=False)
    return x, g, s


# --------------------------------------------------------------------------------------------------
# Task B
# --------------------------------------------------------------------------------------------------
ORG_CLASS = {  # manual classification of SCMD codes absent from the 2024 catchment table
    **{c: "mental_health" for c in "R1L RAT RGD RHA RJ8 RKL RLY RMY RNU RP1 RP7 RPG RQY RRP RT1 RT2 RT5 RTV RV3 RV5 "
                                  "RV9 RVN RW1 RW4 RW5 RWK RWR RWV RWX RX2 RX3 RX4 RXA RXE RXG RXM RXT RXV RXX RXY "
                                  "RYG TAD TAF TAH TAJ G6V2S RDY RTQ RRE R1A".split()},
    **{c: "community" for c in "R1C R1D R1E R1J RDR RY2 RY3 RY4 RY5 RY6 RY7 RY8 RY9 RYK RYV RYW RYX RYY".split()},
    "RT3": "specialist_acute",
}


def ord_get(code):
    f = CACHE / f"{code}.json"
    if not f.exists() or f.stat().st_size == 0:
        for attempt in range(3):
            try:
                resp = requests.get(ORD + code, timeout=30)
                f.write_text(resp.text)
                break
            except Exception:  # noqa
                time.sleep(3)
    try:
        return json.loads(f.read_text())["Organisation"]
    except Exception:  # noqa
        return None


def successors(org):
    return [(s["Target"]["OrgId"]["extension"], s["Date"][0].get("Start", ""))
            for s in org.get("Succs", {}).get("Succ", []) if s.get("Type") == "Successor"]


def build_successor_map(v, x):
    cat = pd.read_csv(D / "trust_catchment_la.csv", usecols=["year", "admission_type", "trust_code", "trust_name"])
    cat = cat[(cat.year == 2024) & (cat.admission_type == "All")].drop_duplicates("trust_code")
    incat = set(cat.trust_code)
    rows = []
    for code in sorted(set(v.ODS_CODE) - incat):
        org = ord_get(code) or {}
        role = next((ro["id"] for ro in org.get("Roles", {}).get("Role", []) if ro.get("primaryRole")), "")
        chain, frontier, dates, notes = [], [code], [], []
        final = []
        for _ in range(6):
            nxt = []
            for c in frontier:
                o = org if c == code else (ord_get(c) or {})
                ss = successors(o)
                if c != code and c in incat:
                    final.append(c)
                    continue
                if not ss:
                    if c != code:
                        final.append(c)
                    continue
                if len(ss) > 1:
                    notes.append(f"{c} split between {', '.join(s for s, _ in ss)}")
                for s, d in ss:
                    chain.append(f"{c}->{s}")
                    dates.append(d)
                    nxt.append(s)
            if not nxt:
                break
            frontier = nxt
        final = list(dict.fromkeys(final))
        names = [(ord_get(s) or {}).get("Name", "") for s in final]
        in_cat = bool(final) and all(s in incat for s in final)
        oc = ORG_CLASS.get(code, "acute")
        if final and not in_cat:
            notes.append("successor not in 2024 catchment")
        if not final:
            notes.append("no successor in ODS")
        if oc == "specialist_acute" and in_cat:
            notes.append("specialist acute trust merged into acute successor")
        elif oc != "acute" and in_cat:
            notes.append("non-acute trust mapped to acute successor: use with caution")
        rows.append(dict(ods_code=code, name=org.get("Name", ""), org_role=role, org_class=oc,
                         status=org.get("Status", ""), successor_code=";".join(final),
                         successor_name=";".join(names), successor_in_catchment=in_cat,
                         merger_date=";".join(dates), chain=" | ".join(chain), notes="; ".join(notes)))
    m = pd.DataFrame(rows)

    # DDD volume for flags
    inc = x[x.include]
    tot = inc.groupby(["new_group", "year"]).ddd.sum()
    tr = inc.groupby(["ODS_CODE", "new_group", "year"]).ddd.sum()
    share = (tr / tot.reindex(tr.index.droplevel(0)).values).rename("share")
    key_groups = ["antituberculosis_active", "antituberculosis_rifamycin_isoniazid", "antituberculosis_mdr",
                  "tnf_inhibitor", "il6_abatacept", "jak_inhibitor_rheum", "rituximab"]
    mx = share.reset_index().query("new_group in @key_groups").groupby("ODS_CODE").share.max()
    m["max_annual_share_antitb_or_biologic"] = m.ods_code.map(mx).fillna(0).round(4)
    m["flag_high_volume_unmatched"] = (~m.successor_in_catchment) & (m.max_annual_share_antitb_or_biologic >= 0.005)
    m.to_csv(D / "trust_successor_map.csv", index=False)

    # match shares
    status = {c: "direct" for c in incat}
    for r in m.itertuples():
        if r.successor_in_catchment:
            status[r.ods_code] = "successor_acute" if r.org_class in ("acute", "specialist_acute") else "successor_nonacute"
        else:
            status[r.ods_code] = "unmatched_nonacute" if r.org_class != "acute" else "unmatched_acute"
    inc = inc.assign(match=inc.ODS_CODE.map(status).fillna("unmatched_acute"))
    sh = inc.groupby(["year", "new_group", "match"]).ddd.sum().unstack(fill_value=0)
    sh = sh.div(sh.sum(axis=1), axis=0).round(4).reset_index()
    sh.to_csv(D / "trust_match_share_by_group.csv", index=False)
    return m, sh


def main():
    v = load_vmp()
    cls = build_classification(v)
    print(cls.new_group.value_counts())
    x, g, s = national_summary(v, cls)
    pd.set_option("display.width", 250, "display.max_rows", 500)
    print(g.pivot(index="new_group", columns="year", values="patient_years").round(0))
    print(g.query("new_group=='systemic_glucocorticoid'")[["year", "pred_eq_mg"]])
    print("rifampicin DDD incl FDC:", x.groupby("year").rif_ddd.sum().round(0).to_dict())
    m, sh = build_successor_map(v, x)
    print(m.drop(columns=["chain"]).to_string())
    print(sh.to_string())


if __name__ == "__main__":
    main()
