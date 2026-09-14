"""Primary care drug groups for the panel analyses (revised after peer review, round 1).

Rules are applied at BNF presentation level so that non-immunosuppressive forms can be excluded.
Each group is a dict of case-insensitive regular expressions (RE2- and Python-compatible):
  code          - BNF chemical substance code (9 characters)
  name          - chemical substance name
  presentation  - BNF presentation description must match
  exclude       - BNF presentation description must NOT match
A presentation must satisfy every rule given. BNF chapters 11-13 (eye, ear/nose/oropharynx, skin)
are always excluded.

Changes from build_dataset.DRUG_GROUPS (used by the first-pass cross-sectional analysis):
  - oral_corticosteroids -> systemic oral glucocorticoids (prednisolone, prednisone,
    methylprednisolone, deflazacort, dexamethasone); hydrocortisone (mainly replacement therapy),
    injectables and betamethasone soluble tablets (mainly mouthwash) removed; hydrocortisone and
    dexamethasone also reported separately
  - immunosuppressants -> conventional DMARDs (rheumatology methotrexate, leflunomide, azathioprine,
    mercaptopurine) and transplant immunosuppressants (tacrolimus, ciclosporin, mycophenolate,
    sirolimus, everolimus) as separate groups; oncology methotrexate excluded
  - prednisolone-equivalent mg of systemic oral glucocorticoids added as a dose measure
"""

import numpy as np

EXCLUDE_CHAPTERS = r"^(?:11|12|13)"
INJECTABLE = r"inj|infusion|amp|vial|syringe|pre-filled|prefilled|intra-articular|suspension for injection"

DRUG_GROUPS = {
    # descriptive only: TB treatment is delivered by specialist services, not primary care
    "antituberculosis": dict(code=r"^0501090"),
    "oral_glucocorticoids": dict(code=r"^0603020",
                                 name=r"^(?:prednisolone|prednisone|methylprednisolone|deflazacort|dexamethasone)",
                                 exclude=INJECTABLE),
    "oral_hydrocortisone": dict(code=r"^0603020", name=r"^hydrocortisone", exclude=INJECTABLE),
    "oral_dexamethasone": dict(code=r"^0603020", name=r"^dexamethasone", exclude=INJECTABLE),
    "inhaled_corticosteroids": dict(code=r"^0302000"),
    # subcutaneous methotrexate (rheumatology) is kept; oncology methotrexate (BNF 8.1.3) is excluded by code
    "conventional_dmards": dict(name=r"^(?:methotrexate|leflunomide|azathioprine|mercaptopurine)",
                                code=r"^(?:1001030|0802010|0801030L0)"),
    "transplant_immunosuppressants": dict(name=r"^(?:tacrolimus|ciclosporin|mycophenol|sirolimus|everolimus)",
                                          code=r"^0802"),
    "proton_pump_inhibitors": dict(code=r"^0103050"),
    "statins": dict(code=r"^0212000", name=r"statin"),
    "metformin": dict(name=r"metformin"),
    "insulins": dict(code=r"^060101"),
    "fluoroquinolones": dict(name=r"^(?:ciprofloxacin|levofloxacin|moxifloxacin|ofloxacin)"),
    "all_antibacterials": dict(code=r"^0501"),
    "vitamin_d": dict(name=r"^(?:colecalciferol|ergocalciferol)"),
    # negative control exposure
    "levothyroxine": dict(name=r"^levothyroxine"),
}

# prednisolone-equivalent potency for systemic oral glucocorticoids
PRED_EQUIVALENT = {"prednisolone": 1.0, "prednisone": 1.0, "methylprednisolone": 1.25,
                   "deflazacort": 0.83, "dexamethasone": 6.67}
# Strength in presentation descriptions, in both EPD ("Prednisolone 5mg tablets", "Dexamethasone
# 500microgram tablets", "Prednisolone 5mg/5ml oral solution") and HSCIC PDPI ("Prednisolone_Tab 5mg",
# "Dexameth_Tab 500mcg", "Dexameth_Oral Soln 2mg/5ml S/F") formats. Quantity is tablets or ml.
STRENGTH = r"(\d+(?:\.\d+)?)\s*(?:mg|microgram|mcg)"
MICROGRAM = r"\d\s*(?:microgram|mcg)"
PER_VOLUME = r"/\s*(\d+(?:\.\d+)?)?\s*ml"


def sql_condition(rule, code_col, name_col, pres_col):
    """BigQuery condition for a group rule (NHSBSA open data portal SQL)."""
    conds = []
    if "code" in rule:
        # every code rule already restricts to a BNF section outside chapters 11-13
        conds.append(f"REGEXP_CONTAINS({code_col}, r'{rule['code']}')")
    else:
        conds.append(f"NOT REGEXP_CONTAINS({code_col}, r'{EXCLUDE_CHAPTERS}')")
    if "name" in rule:
        conds.append(f"REGEXP_CONTAINS(LOWER({name_col}), r'{rule['name']}')")
    if "presentation" in rule:
        conds.append(f"REGEXP_CONTAINS(LOWER({pres_col}), r'{rule['presentation']}')")
    if "exclude" in rule:
        conds.append(f"NOT REGEXP_CONTAINS(LOWER({pres_col}), r'{rule['exclude']}')")
    return " AND ".join(conds)


def pandas_mask(rule, code, name, presentation):
    """Boolean mask for a group rule; code, name and presentation are aligned string Series."""
    name, presentation = name.str.lower(), presentation.str.lower()
    mask = ~code.str.match(EXCLUDE_CHAPTERS)
    if "code" in rule:
        mask &= code.str.match(rule["code"])
    if "name" in rule:
        mask &= name.str.contains(rule["name"], regex=True)
    if "presentation" in rule:
        mask &= presentation.str.contains(rule["presentation"], regex=True)
    if "exclude" in rule:
        mask &= ~presentation.str.contains(rule["exclude"], regex=True)
    return mask


def sql_pred_equivalent_mg(name_col, pres_col, quantity_col):
    """BigQuery expression: prednisolone-equivalent mg dispensed (strength x quantity x potency)."""
    pres = f"LOWER({pres_col})"
    strength = (f"SAFE_CAST(REGEXP_EXTRACT({pres}, r'{STRENGTH}') AS FLOAT64)"
                f" * IF(REGEXP_CONTAINS({pres}, r'{MICROGRAM}'), 0.001, 1)"
                f" / IF(REGEXP_CONTAINS({pres}, r'{PER_VOLUME}'),"
                f" COALESCE(SAFE_CAST(REGEXP_EXTRACT({pres}, r'{PER_VOLUME}') AS FLOAT64), 1), 1)")
    potency = "CASE " + " ".join(f"WHEN STARTS_WITH(LOWER({name_col}), '{k}') THEN {v}"
                                 for k, v in PRED_EQUIVALENT.items() if k != "prednisolone") + " ELSE 1 END"
    return f"IFNULL({quantity_col} * {strength} * {potency}, 0)"


def pandas_pred_equivalent_mg(name, presentation, quantity):
    pres = presentation.str.lower()
    strength = pres.str.extract(STRENGTH, expand=False).astype(float)
    strength = strength * np.where(pres.str.contains(MICROGRAM, regex=True), 0.001, 1)
    volume = pres.str.extract(PER_VOLUME, expand=False).astype(float).fillna(1)
    per_volume = pres.str.contains(PER_VOLUME.replace("(\\d", "(?:\\d"), regex=True)
    strength = strength / np.where(per_volume, volume, 1)
    lname = name.str.lower()
    potency = np.select([lname.str.startswith(k) for k in PRED_EQUIVALENT], list(PRED_EQUIVALENT.values()), 1.0)
    return (quantity * strength * potency).fillna(0)
