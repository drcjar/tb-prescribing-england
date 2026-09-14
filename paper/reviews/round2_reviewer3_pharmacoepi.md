# Peer review, round 2: Reviewer 3 (pharmacoepidemiology and prescribing data)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England" (Draft 3, revised after peer review, 14 September 2026)

**Materials examined:**
- My round 1 report and the authors' response (`paper/reviews/response_round1.md`).
- The revised manuscript (`paper/manuscript.md`) and `paper/tables/`.
- Code: `drug_groups.py`, `fetch_prescribing_panel.py`, `fetch_pre2014_practice.py`, `build_practice_lad_shares.py`, `build_panel.py`, `hospital_medicines.py`, `build_scmd_classification.py`, `steroid_trends.py`, `run_revision.sh`.
- Audit and output files:
  - `data/raw/scmd/vmp_classification.csv`, `trust_successor_map.csv`, `README_classification.md`, `trust_catchment_la.csv`
  - `data/raw/openprescribing/epraccur.csv`
  - `data/processed/practice_lad23_shares_diagnostics.md`
  - `outputs/hospital/*`, `outputs/descriptives/*`, `outputs/logs/build_panel_*`
  - one monthly practice extract per year (small reads only)

Numbers not in the manuscript were computed from these files, as described below. I modified no project file other than this report.

---

## 1. Overall assessment and recommendation

**Recommendation: major revision (much narrower in scope than round 1).**

The revision is substantial and, for the most part, well executed.

**What has been done well:**
- **Primary care groups.** These are now defined at presentation level.
- **Residence apportionment.** Prescribing is apportioned by patients' residence from the practice × LSOA registration files. This is the most important improvement, and it is implemented carefully, with good diagnostics.
- **SCMD products.** Each product is classified with WHO DDDs and hard-coded fixed-dose-combination strengths.
- **Trust mergers.** These are resolved through the ODS successor chain.
- **Positive control.** It is disease-specific, and its elasticity is carried into the MDE comparison.
- **Standard errors.** They are also clustered by principal trust, and elective catchments are used as a sensitivity analysis.
- **Target trial box.** This is useful.

I checked most of these changes in the code, not only in the response letter. They do what the response says.

**Why I still recommend major revision:**
1. **A new data-handling error.** It affects the within-area primary care exposure in 2011–2016 (N1). The RO76 restriction uses a current `epraccur` file that no longer lists practices closed before about 2017. It therefore silently removes genuine GP practices, and the share removed changes over time: 3.4% of items in December 2011, 1.5% in December 2014, 0% from 2016. This is exactly the within-area artefact that the residence apportionment was meant to remove. Its size is comparable to the within-area SD of the exposure (0.043).
2. **Response claims not reflected in the manuscript or code** (N4):
   - the presentation-level listing;
   - SCMD final/provisional status and extraction dates;
   - FP10(HP) as a limitation;
   - a respecified hospital glucocorticoid scenario;
   - separate transplant inputs in Table 2;
   - an elasticity grid for primary care MDEs.
3. **The hospital positive control and the hospital glucocorticoid exposure are not constructed as described** (N2, N3), and a small double-counting bug remains (N6).

**Effect on the conclusions.** I do not expect any of this to overturn the qualitative conclusion. Correcting N1 would, if anything, reduce spurious within-area variation. However:
- the manuscript's claims about exposure quality ("98–99% of items", "prednisolone-equivalent mg", "60% attenuation", "98–100% coverage") need to match the code;
- the response letter needs to be accurate.

All requested fixes use data the authors already hold, except a historical ODS prescribing-setting file for N1, which is small.

---

## 2. Point-by-point status of round 1 items

### Major comments

| Item | Status | Verification / remaining gap |
|---|---|---|
| **M1** Primary care group definitions | **Partly** | **Done:**<br>• `drug_groups.py:28-51` implements the requested groups: systemic oral glucocorticoids without hydrocortisone, injectables or betamethasone; DMARDs split from transplant agents; oncology methotrexate (0801030P0) excluded by code; mercaptopurine added (0801030L0).<br>• The PDPI and EPD pipelines use the same rules (`fetch_pre2014_practice.py:25,58-61`; `fetch_prescribing_panel.py:35`).<br>**Not done:**<br>• Request 3, the presentation-level listing at three time points, is claimed ("provided in the supplement", response l. 279-280). It is not in the manuscript, in `paper/tables/`, or among the outputs.<br>• New regex issues: see N5 and minor 7-8. |
| **M2** Hospital groups, units, DDD | **Largely addressed** | **Done:**<br>• `build_scmd_classification.py` classifies all 534 (VMP, unit) rows.<br>• DDD values, and the documented non-WHO doses, are sensible.<br>• Intra-articular and depot forms are excluded (`DEPOT`, l. 106; hydrocortisone acetate, l. 172).<br>• Oncology methotrexate vials and >30 mg syringes are excluded (l. 175-186).<br>• Ruxolitinib is kept separate; IL-17, IL-12/23, α4β7 and anakinra form a comparison group.<br>**Not done:**<br>• Request 6, within-group DDD composition by year, is only in `README_classification.md`, not in the paper.<br>• The hospital glucocorticoid analysis is not in prednisolone-equivalent mg as the Methods state (N3).<br>• Tacrolimus granules are double-counted (N6). |
| **M3** Positive control | **Addressed, with new concerns** | **Done:**<br>• A pyrazinamide/ethambutol-based control is used, with Rifater and Voractiv included.<br>• Elasticity is reported (Table 3).<br>• Attenuation is carried into Table S3.<br>• "Valid linkage" wording is removed.<br>**Remaining:** the DDD construction mixes one-component and two-component counting, and the attenuation factor is applied to the wrong model (N2). |
| **M4** Items as exposure | **Partly** | **Done:**<br>• ADQ is extracted (`fetch_prescribing_panel.py:29-41`).<br>• Prednisolone-equivalent mg is derived for all oral presentations and both data formats (`drug_groups.py:53-117`).<br>• An ADQ sensitivity analysis is added (Table S1).<br>**Not done:**<br>• Request 3: the within-area SD is not reported for the ADQ or mg measures. `within_between_variation.csv` has items only, for four groups. The response (l. 291) says it is reported "for each measure".<br>• Request 2: the within-area correlation of log items with log ADQ is not reported.<br>• Request 4: no long-course prednisolone proxy. |
| **M5** SCMD coverage and mergers | **Partly** | **Done:**<br>• The successor map (`hospital_medicines.py:99-105`) reassigns predecessor codes, including RAP → RAL. RW6 is split 50/50, which is acceptable and stated in the README.<br>• Coverage by year is in Table S7.<br>**Not done:**<br>• Request 5: final versus provisional months and extraction dates are not stated anywhere in the manuscript. The response (l. 299) says they are.<br>• Homecare capture is not tested (acknowledged, manuscript l. 674). |
| **M6** Practice-to-area mapping | **Addressed** | • `build_practice_lad_shares.py` and `build_panel.py:122-136` are correct in structure. Shares sum to 1 per practice (asserted, l. 233).<br>• Unmapped patients are ≤0.1% per release.<br>• Diagnostics are good (GP at Hand, out-of-area share by LAD).<br>• Two small issues: N7 (City of London at UTLA level) and minor 4. |
| **M7** Denominators and cross-section | **Addressed** | Resident denominators and same-period prescribing are used. `build_dataset.py` (registered denominators) is no longer used for the reported analyses. |
| **M8** PDPI/EPD splice | **Partly** | **Done:**<br>• Identical rules in both series; atomic writes and try/finally clean-up (`fetch_pre2014_practice.py:77-107`).<br>• National year-on-year changes at the splice are reported (`splice_agreement_2013_2014.csv`; manuscript l. 672).<br>• EPD-only sensitivity analysis.<br>**Not done:**<br>• No overlap concordance. To my knowledge, NHS Digital continued to publish "Practice Level Prescribing Data" after January 2014, until publication moved to the NHSBSA. The authors should check that series again before stating that no overlap exists.<br>• Rebuttal: my round 1 request was for an area-specific splice indicator (pre-2014 × area). Year fixed effects do not absorb it. The EPD-only restriction is an acceptable substitute.<br>**Important:** the "same practice restriction" is not in fact the same over time (N1). |
| **M9** MDE inputs | **Partly** | **Done:**<br>• SCMD-derived prevalences are used for hospital groups (`hospital_medicines.py:228`).<br>• A screening-attenuated TNF scenario is added.<br>• Table 2 labels OR versus RR.<br>**Not done:**<br>• Request 1: no prevalence × RR × elasticity grid for the primary care MDEs; `paper/mde_inputs.csv` has single values.<br>• Request 3: the hospital glucocorticoid scenario is unchanged (RR 4.9, `hospital_medicines.py:54`), although the response (l. 320) says it was "respecified".<br>• Request 4: no dose-stratified OCS scenario.<br>• Transplant immunosuppressants have no RR or prevalence row in Table 2 or `mde_inputs.csv`, although separating them was the reason for the split.<br>• Conventional DMARD prevalence (0.5%) remains an assumption. |
| **M10** Catchments and SEs | **Addressed** | Elective catchments and principal-trust clustering are implemented (`hospital_medicines.py:204-212`). Request 3, the number of trusts contributing >10% to each area, is not reported. This is minor. |
| **M11** Individual-level design | **Addressed** | The Box is adequate. |

### Bugs B1–B20

| Bug | Status | Comment |
|---|---|---|
| B1 Rifater/Voractiv strengths | **Addressed** | Hard-coded (`build_scmd_classification.py:96-101`). The rows are present and included in `vmp_classification.csv`. See N2 on how they enter the DDD. |
| B2 Predecessor ODS codes | **Addressed** | Successor map; RAP mapped to RAL. |
| B3 SE clustering | **Addressed** | Principal-trust clustering added. |
| B4 Classification | **Partly** | The depot, ruxolitinib, oncology methotrexate and biologic regrouping are fixed. The hospital glucocorticoid group still mixes oral hydrocortisone replacement, IV hydrocortisone and dexamethasone (about 43% of group DDD; N3). |
| B5 Stale audit files | **Partly** | The new files are consistent with the code. The legacy `scmd_products_by_group.csv`, `scmd_trust_month_groups.csv` and `scmd_trust_month_group_summary.csv` still sit in the same directory, unlabelled. Delete them or move them to `legacy/`. |
| B6 `summarise_scmd.py` failure | **Partly** | Described as "superseded", but the file is still in the repository and is not in `run_revision.sh`. Remove it or mark it deprecated. |
| B7 Cross-sectional denominators | **Addressed** | |
| B8–B9 OCS and immunosuppressant groups | **Addressed** | See N5 and minor 7-8 for residual definition issues. |
| B10 RO76 not applied | **Partly / new error** | The restriction is now applied (`build_panel.py:112-116`, `steroid_trends.py:45-49`), but with a truncated `epraccur` file (N1). |
| B11 Postcode attribution | **Addressed** | |
| B12 Pre-2014 pipeline | **Addressed** | |
| B13 Prednisolone mg regex | **Addressed** | The strength, microgram and per-volume parsing in `drug_groups.py:59-117` handles EPD and PDPI descriptions, oral solutions and brands. The SQL and pandas versions are equivalent. |
| B14 Table 2 not reproducible | **Addressed** | `mde.py` writes `mde_table_{ltla,utla}_residence.csv`, and `make_tables.py` reads them. |
| B15 Hospital MDE scenarios | **Partly** | TNF prevalence is now SCMD-derived. The glucocorticoid RR 4.9 scenario is unchanged (N3). |
| B16 Cost measure | **Addressed** | Dropped. |
| B17 Negative quantities | **Addressed** | Clipped at trust × group × month (`hospital_medicines.py:77,85`). |
| B18 Time-invariant catchments | **Partly** | Admission-based catchment misallocation is stated (l. 673). Applying 2024 shares to 2019 is not stated explicitly. |
| B19 Coverage statement | **Partly** | Now given by year (Table S7). The text claim "98–100% of DDD in every group and year" (l. 258, l. 483) is wrong for levetiracetam: 95.0–95.7% matched in every year (Table S7). |
| B20 References | **Addressed** | |

### Minor comments 1–22 (summary)

**Addressed:** 3, 4, 7, 8, 11, 12, 14, 15, 16, 17, 19, 20.

**Partly addressed:**
- **5.** The ONSPD version is not stated in the Methods. The City of London is described as combined with Hackney at both levels, but the UTLA code merges it with Westminster (N7).
- **6.** Area counts are still inconsistent: "294, of which 292 were analysed" (l. 171); "294 lower-tier authorities" (l. 383); "294 areas" (Table 1 header, l. 406); "292" (Figure 2).
- **9.** Table S3 has no source column for the illustrative RRs.
- **22.** Only a general statement about RECORD and STROBE.

**Not addressed:**
- **10.** No uncertainty is given for the MDEs.
- **18.** No extraction dates or archived extract DOI.
- **21.** FP10(HP) prescriptions appear nowhere in the manuscript. The response (l. 219) says they are discussed as a limitation.
- **13.** Moot: the analysis was removed.

---

## 3. New major issues

### N1. The RO76 restriction silently removes practices that closed before about 2017, creating a time-varying, area-clustered exposure artefact

**Where.** `build_panel.py:88-91` builds the GP set from the current `data/raw/openprescribing/epraccur.csv` (`ep[25] == "RO76"`), and l. 113-116 filters the practice-month extracts with it. `steroid_trends.py:45-49` does the same for the national series and figures.

**What I found.**
- **The file is truncated.** It contains 8,126 RO76 codes (6,558 active, 1,568 inactive). The earliest close date among the inactive RO76 practices is 2017. Practices closed before then are simply absent.
- **Share of items from codes absent from the file.** I classified every prescribing code in single-month extracts. All of the absent codes have standard GP practice code format (letter + five digits):

| Month | Codes not in `epraccur` | Items not in `epraccur` | Codes with a non-RO76 setting | Items with a non-RO76 setting |
|---|---|---|---|---|
| December 2011 | 1,360 | 3.4% | 1,140 | 0.8% |
| December 2013 | 562 | 2.3% | 1,704 | 1.1% |
| December 2014 | 370 | 1.5% | 1,906 | 1.1% |
| December 2015 | 144 | 0.2% | 2,090 | 1.2% |
| December 2016 | 0 | 0% | 2,232 | 1.2% |
| December 2019 | 0 | 0% | 2,449 | 1.2% |

- **Logged "RO76 share".** It rises from 95.5% (2011) to 98.8% (2016) and is flat afterwards (`outputs/logs/build_panel_ltla_residence.txt`). The genuine non-GP share is stable at 0.8–1.2%, so almost all of the rise is dropped closed practices.
- **The manuscript misstates the share.** It says RO76 practices "accounted for 98–99% of items after 2014" (l. 196-197). The 2014 value is 97.1%, and the pre-2014 values (95.5–96.5%) are not reported.

**Why it matters.**
- **Artefactual within-area increases.** When a practice closes or merges, its patients and their prescribing move to surviving practices. Before the closure, the items were dropped; afterwards they are counted. This produces artefactual within-area increases in 2011–2016 in areas with many closures and mergers (inner London APMS re-procurements, practice mergers).
- **The residence shares hide it.** The logged residence-apportioned share of 99.99% for 2011–2013 is computed after the RO76 filter, so it cannot reveal the problem.
- **Size.** Area-level shifts of several per cent are the same order as the within-area SD of the exposure (0.043 for oral glucocorticoids; `within_between_variation.csv`).
- **Analyses affected:**
  - the primary panel (exposure 2013–2016 for outcome years 2014–2017);
  - the "EPD-only" splice sensitivity analysis, since the 2014–2015 EPD years are also affected;
  - the distributed-lag and three-year-window models;
  - the national trend figure (Figure 3) and the splice-agreement table.
- **The splice finding.** Part of the reported 2013/14 discontinuity in oral glucocorticoids (+3.3%) and all antibacterials may come from this artefact rather than from the change of source.

**Requests.**
1. Build the GP practice set from a setting source that covers the whole period. Options:
   - the archived ODS `epraccur` releases, e.g. a 2014 release unioned with the current one, taking the last known setting per code;
   - or, as a simpler rule, keep codes that appear in any practice × LSOA registration release, or codes that are absent from `epraccur` but have GP code format and registered patients.
2. Report the RO76 share by year before and after the fix, for 2011–2024.
3. Re-run the panels, Table S1 (including the EPD-only and outcomes 2018–2024 rows), `steroid_trends.py` and the splice table.
4. Report how many LTLAs lose more than 2% of items in any year under the current rule. This shows readers where the artefact was concentrated.

### N2. Positive control: DDD construction and use of the attenuation factor

**Where.** `build_scmd_classification.py:147-161, 197`; `hospital_medicines.py:216-238`.

**The DDD construction.**
- **Two regimens, different units.** For fixed-dose combinations, only the principal component enters the DDD: pyrazinamide for Rifater and Voractiv (l. 152-153). The 275 mg ethambutol in Voractiv is ignored. Separate pyrazinamide and ethambutol products each contribute their own DDD. So:
  - a patient on RHZE as separate tablets contributes about 2 "patient-year equivalents" per day of intensive phase (Z + E);
  - a patient on Voractiv contributes about 1;
  - a patient on Rifater plus separate ethambutol contributes about 2.
- **Effect.** The unit is not patient-years (the manuscript's Table 3 title and Figure 5 legend say it is). Trust-level or temporal shifts between combination and separate-component prescribing move the measure without any change in patients.
- **Composition.** In the README, ethambutol is about 53% of group DDD and fixed-dose combinations about 31%, so the mix is not negligible.
- **Consistency check.** 2,957 "patient-years" in 2024, against about 5,500 notifications × about 2 months of intensive phase ≈ 900 patient-years, is consistent with double counting plus some continuation-phase ethambutol and NTM use.

**Requests on construction.**
- Define the positive control as **intensive-phase treatment-days**: the maximum over component DDDs within a regimen, or pyrazinamide DDD alone including the fixed-dose-combination pyrazinamide content.
- Alternatively, report ethambutol-only and pyrazinamide-only series, counting fixed-dose-combination content for each, and show that the elasticity is robust.

**Interpretation of the elasticity.**
- **No specificity gain.** The "active" control has the same concurrent elasticity as the rifamycin/isoniazid products: UTLA 0.361 vs 0.365; LTLA 0.40 vs 0.39 (`hospital_results_*.csv`). The latter include LTBI and non-TB rifampicin. If the more specific measure gains nothing, the attenuation is dominated by apportionment and catchment error, not by drug specificity.
- **It is not a pure linkage error.** The elasticity also absorbs non-proportionality between cases and drug volume: treatment duration, children, MDR, extrapulmonary regimens and treatment spanning two calendar years.
- **Requested wording.** Say this explicitly, and soften "roughly 60% attenuation" at l. 489 and l. 613 to "an elasticity of 0.36–0.40, reflecting apportionment error and imperfect proportionality between cases and drug volume".

**Model mismatch in the attenuation.**
- **What the code does.** `expected_effects` takes the elasticity from the concurrent model (l. 220-221) but applies it to MDEs from the previous-year model (l. 224, 232).
- **The same control lagged.** The positive control's own previous-year elasticity is 0.048 at UTLA (`hospital_results_utla.csv`), and the joint lag/lead estimates are about 0.
- **Why the concurrent value is still defensible.** Treatment follows diagnosis, so the concurrent value is the relevant linkage attenuation.
- **Requested wording.** State that the attenuated ratios in Table S3 assume the linkage attenuation is the same for previous-year exposure. This is optimistic, so it favours detection.

### N3. The hospital systemic glucocorticoid exposure is not what the Methods describe, and its expected-effect scenario is unchanged

**The measure used is DDD, not prednisolone-equivalent mg.**
- **The claim.** Methods l. 246-247 say systemic glucocorticoids were "measured in prednisolone-equivalent mg".
- **The code.** `hospital_medicines.within_area` and `cross_sectional` loop over `GROUPS`, using `rate_systemic_glucocorticoid = ddd / 365 / population` (l. 147-149). `rate_glucocorticoid_pred_mg` is computed (l. 149) but never analysed.
- **The two measures differ.** WHO DDDs are not potency-equivalent across routes. Parenteral methylprednisolone (DDD 20 mg) is weighted 2.5 times lower than its prednisolone-equivalent (1.25 × 20 = 25 mg vs 10 mg per DDD), and 1 g pulse vials are among the largest mg items.
- **Request.** Either analyse the prednisolone-equivalent mg series or correct the Methods and the Table 3 title.

**The group composition is not TB-relevant immunosuppression.**
- **Composition.** In the README and `vmp_national_annual_by_substance.csv`:
  - oral dexamethasone is about 29% of group DDD;
  - parenteral dexamethasone is 13–15%;
  - oral hydrocortisone, documented in the notes column as "largely physiological adrenal replacement", is included;
  - IV hydrocortisone sodium succinate 100 mg vials (10.9 million units) are included.
- **What that means.** About 43% of the group is dexamethasone, which is mostly oncology (including myeloma 20–40 mg regimens), antiemetic, perioperative, cerebral oedema and COVID-19 (RECOVERY) use. This is a heterogeneous exposure whose within-area changes track cancer services and COVID waves.
- **Requests.**
  - Restrict the candidate exposure to oral prednisolone, prednisone, methylprednisolone and deflazacort, with IV methylprednisolone pulses reported separately.
  - Report dexamethasone and hydrocortisone as descriptive series, mirroring the primary care approach.

**The expected-effect scenario is unchanged.**
- **The code.** `hospital_medicines.py:54` still applies the primary care glucocorticoid OR (4.9, current oral use, Jick 2006) to a hospital "prevalence" of 0.46% derived from DDD/365.
- **Why that is wrong.** DDD/365 is not prevalence of current use when most supply is short inpatient courses and antiemetic doses. The resulting row in Table S3 (expected change 0.177% per 10%, the largest of any hospital group) is not meaningful.
- **Contradiction with the response.** The response (l. 320) says this scenario was respecified.
- **Request.** Remove the row, or specify a pulse or long-term scenario with justified inputs.

### N4. Response claims not reflected in the manuscript or code

Several statements in the response letter are not borne out.

| Response claim | Location in response | What I found |
|---|---|---|
| Presentation-level listing "provided in the supplement" | l. 279-280 | Absent from the manuscript, `paper/tables/` and outputs |
| "Provisional versus final data and the extraction date are stated" | l. 299 | Not in the manuscript |
| FP10(HP) "discussed as a limitation" | l. 219 | "FP10" does not appear in the manuscript |
| Hospital glucocorticoid scenario "respecified" | l. 320 | Unchanged in code and in Table S3 (N3) |
| "Within-area SD is reported for each measure" | l. 291 | Items only, four groups |
| "Sensitivity to the elasticity is shown" | l. 319 | Hospital Table S3 only; no primary care grid |
| Separate RR and prevalence inputs for transplant immunosuppressants (implied by the split, R3 M1.2) | — | No row in Table 2 or `paper/mde_inputs.csv` |

**Request.** Implement these, or correct the response letter. Editors and readers rely on the letter as a record of what was done.

---

## 4. Minor issues

1. **N5. Dexamethasone inside "systemic oral glucocorticoids"** (`drug_groups.py:31-33`).
   - Dexamethasone is only about 3% of items (3.6 of about 116 per 1,000 in 2024). However, with a potency factor of 6.67 and oncology and palliative regimens of 8–16 mg a day, it can be a much larger share of prednisolone-equivalent mg. That share would drive the mg series used in the regional UK-born analysis (Table S5-S6).
   - Report the share of prednisolone-equivalent mg from dexamethasone by year.
   - Re-run the regional mg analysis excluding dexamethasone, since it is already a separate group.
2. **N6. Tacrolimus granules are double-counted.**
   - `hospital_medicines.py:71` merges SCMD rows to the classification on (VMP code, unit) only. `vmp_classification.csv` has two included rows each (old and new dm+d names) for 16658211000001106 (tacrolimus 200 microgram granules) and 16658611000001108 (tacrolimus 1 mg granules).
   - Every SCMD row for these products is therefore counted twice: roughly 140,000 DDD a year, about 1% of the calcineurin/mTOR group. It is concentrated in paediatric transplant centres, so the error is trust-specific.
   - Deduplicate on (code, unit) before merging, and add an assertion that the merge does not increase the row count.
3. **N7. City of London at UTLA level.**
   - `build_panel.py:135` applies `MERGES["ltla"]` (City → Hackney) before mapping to areas at both levels. At UTLA level, City residents' prescribing therefore goes to Hackney, while population (l. 149) and TB counts (`build_tb_annual.py:65`) are merged into Westminster (`MERGES["utla"]`).
   - The magnitude is negligible, but the code and the text disagree: l. 172-173 says Hackney at both levels.
   - Use `MERGES[level]`, and state the UTLA and LTLA treatment separately.
4. **Residence shares for practices not present in an April snapshot.**
   - Practices that open after April, or change code mid-year, lose that year's items (`build_panel.py:124-133`); the apportioned share was 99.86% in 2015.
   - Practices that closed before April 2014 lose all their 2011–2013 items. At present the N1 truncation hides this.
   - After fixing N1, report the apportioned share for 2011–2013 again. Fall back to the nearest later or earlier release per practice rather than the calendar-year snapshot.
5. **`UNIDENTIFIED` filter.**
   - `fetch_prescribing_panel.py:38`: `CAST(UNIDENTIFIED AS STRING) NOT IN ('true','Y')` evaluates to NULL, and drops the row, when `UNIDENTIFIED` is NULL.
   - Confirm that the field is never NULL, or use `COALESCE(...,'false')`. A check of annual `items_total` against the published EPD national totals would settle it.
6. **`INJECTABLE` regex** (`drug_groups.py:26`). Unanchored `amp` and `inj` match any substring. I found no false exclusions among glucocorticoid presentations, but use word boundaries (`\bamp`, `\binj`) for robustness across PDPI abbreviations.
7. **Conventional DMARDs** (`drug_groups.py:38-39`).
   - Mercaptopurine (0801030L0, a chapter 8 cytotoxic) includes maintenance therapy for paediatric acute lymphoblastic leukaemia. That is inconsistent with excluding oncology methotrexate.
   - Hydroxychloroquine and sulfasalazine are omitted. That is defensible for TB risk, but state it, since "conventional DMARDs" usually includes them.
8. **"Transplant immunosuppressants"** (`drug_groups.py:40-41`). In primary care, mycophenolate and ciclosporin are widely used under shared care for lupus, vasculitis, interstitial lung disease, psoriasis and atopic dermatitis. Rename the group, e.g. "calcineurin inhibitors, mTOR inhibitors and mycophenolate", or note the mixed indications. This matters for the RR in N4.
9. **Hospital coverage text.** Lines 258 and 483 should read "95–100%" or name levetiracetam. The unmatched share also rises in 2023–24 for antiproliferatives (1.9%), IL-6/abatacept (1.8%) and JAK inhibitors (1.3%). Identify the trusts responsible (e.g. codes created by 2024–25 mergers whose successor is not in the 2024 table), because this is again time-varying.
10. **High-volume unmatched non-acute trusts.** `trust_successor_map.csv` flags RRE (Midlands Partnership; up to 1.1% of a key group's national DDD) and RDR (Sussex Community; 0.9%). Say what these trusts supply, e.g. community TB or homecare services, and whether their exclusion is stable over time.
11. **RO76 share text** (l. 196-197): see N1.
12. **Hospital glucocorticoid label in Table 3.** Currently "patient-year equivalents per 1,000 residents". It is a DDD-based measure for glucocorticoids, not a count of patients (N3).
13. **Levetiracetam negative control.**
    - It is built from the older `approx_mg` extract (`scmd_negative_control_trust_month.csv`) with a fixed 1,500 mg DDD (`hospital_medicines.py:79-85`), not through the new classification.
    - Its unmatched share (4.3–4.9%) is the highest of any group.
    - Pass it through `build_scmd_classification.py`: exclude IV loading doses if desired, and confirm units.
14. **Stale code.**
    - `build_panel.py:26` imports `build_dataset.DRUG_GROUPS`, which is unused and refers to the superseded definitions.
    - The module docstring (l. 6-7) still describes postcode assignment as the method.
    - Remove the import and update the docstring, so readers do not assume the old groups are used.
15. **Area counts** (l. 171, 383, 406; Figure 2): harmonise 292 versus 294.
16. **Extraction dates and archiving.** State the NHSBSA EPD and SCMD extraction dates, the final/provisional status of the SCMD months in 2024, the OHID catchment release (April 2026), the `epraccur` release, and the registration releases. Deposit the aggregated practice-month and trust-month extracts with a DOI; the portals revise data.
17. **FP10(HP).** Add the one-sentence limitation promised in the response.
18. **Within-area SD by measure.** Extend `within_between_variation.csv` to ADQ and prednisolone-equivalent mg, for all candidate groups. The MDE depends directly on it.

---

*Reviewer 3*
