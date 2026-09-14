# Response to reviewers, round 1

We thank the three reviewers for detailed, constructive reports. All three recommended major
revision. Every point was considered, and most requests were implemented with new data and
re-analysis. Numbers marked [R] were updated after the full re-analysis and are reported in the
revised manuscript.

**Main changes**

1. **Primary care exposure definitions and measures** (R3 M1, M4; R2 M3).
   - Groups are now defined at BNF presentation level:
     - Systemic oral glucocorticoids (prednisolone, prednisone, methylprednisolone, deflazacort,
       dexamethasone) exclude hydrocortisone, injectables and betamethasone soluble tablets.
       Hydrocortisone and dexamethasone are also reported separately.
     - Conventional DMARDs (rheumatology methotrexate, leflunomide, azathioprine, mercaptopurine)
       and transplant immunosuppressants are separate groups. Oncology methotrexate is excluded.
   - Dose measures were added: prednisolone-equivalent mg for glucocorticoids, and ADQ for sections
     where the EPD populates it.
2. **Practice-to-area mapping** (R3 M6).
   - Prescribing is now apportioned by where registered patients live, using NHS Digital practice ×
     LSOA registrations for 2014–2024. Postcode assignment is kept as a sensitivity analysis.
   - In 2024, 7.3% of registered patients lived outside the local authority of their practice.
     GP at Hand (E85124) had 98,457 patients, 93% outside Hammersmith & Fulham.
3. **Longer series with a consistent practice restriction** (R3 M8; R2 minor 19).
   - Prescribing now runs from 2011: HSCIC practice-level data for 2011–2013, NHSBSA EPD from 2014.
   - The same drug-group rules and the RO76 standard-GP-practice restriction are applied to both
     series.
   - The level of agreement at the 2013/2014 splice is reported [R].
4. **Hospital medicines rebuilt** (R3 M2, M5, M10; R1 M4; R2 M2, M6).
   - Every product is classified by mechanism, with WHO defined daily doses (DDD) and patient-year
     equivalents. The groups are:
     - TNF inhibitors
     - IL-6 inhibitors and abatacept
     - rheumatology JAK inhibitors, with ruxolitinib separate
     - rituximab
     - transplant calcineurin/mTOR inhibitors
     - antiproliferatives
     - prednisolone-equivalent systemic glucocorticoids, excluding intra-articular and depot forms
   - Trust mergers are handled with an NHS ODS successor map.
   - Coverage is reported by year: 90–92% direct in 2019 plus 8–9% via successors; 98–99.9% direct
     in 2024.
   - Standard errors are also clustered by principal trust.
   - Elective-admission catchments are used as a sensitivity analysis.
   - Low-TB-risk biologics and levetiracetam are negative-control exposures.
5. **Positive control** (R1 M3; R2 M2; R3 M3).
   - The positive control is now active-TB treatment: pyrazinamide- and ethambutol-containing
     products, including Rifater and Voractiv.
   - Rifamycin/isoniazid products, which include latent TB and non-TB use, are reported separately.
   - The within-area elasticity is reported and interpreted as an attenuation factor. It is carried
     into the expected-effect calculations [R].
   - The primary care antituberculosis group is now described as descriptive only, not a positive
     control.
6. **Exposure timing** (R2 M3; R1 M1, M6).
   - The primary exposure is now prescribing in year t−1.
   - Year t is reported but interpreted as mixing causal and protopathic effects.
   - A distributed lag (t, t−1, t−2) and the original three-year window are sensitivity analyses.
7. **Falsification tests** (R1 M9).
   - Lag and lead are now estimated jointly on a common sample.
   - Regional models with 9 clusters use randomisation inference: whole regional exposure histories
     are permuted across regions.
8. **Power** (R1 M2).
   - The plasmode simulation was redesigned. The real TB counts are kept, so real overdispersion,
     serial correlation and area-specific trends are preserved.
   - Exposure trajectories are permuted across areas, and known effects are injected.
   - There are 500 null and 300 effect replicates per scenario, with Monte Carlo SEs.
   - A timing-misspecification scenario was added.
   - The UTLA and LTLA simulations are now complete [R].
9. **Expected effects** (R1 M1; R2 M4, M7, M8; R3 M9).
   - The assumptions are stated explicitly.
   - The expected effect now also comes from three alternatives:
     - UKHSA recorded drug-associated TB: 30 steroid and 54 biologic cases of 5,490 in 2024
     - an age- and birthplace-stratified calculation
     - SCMD-derived prevalence of hospital drug use
   - The minimum detectable PAF, and the largest PAF compatible with each 90% upper confidence
     limit, are reported.
   - Screening-attenuated relative risks are given for TNF inhibitors.
10. **Other additional analyses.**
    - Area-specific linear trends (R1 M6).
    - Log population as a covariate instead of an offset, for shared-denominator bias (R1 M6).
    - The latent TB programme mapped to local authorities as a time-varying covariate (R2 M5).
    - Asylum support.
    - Exclusion of COVID-affected outcome and exposure years (R2 M6).
    - Metformin and insulin models without diabetes adjustment (R1 M7).
    - Year-specific spatial dependence of residuals (R1 M5).
11. **Reporting and framing.**
    - "Notifications" replaces "incidence" throughout.
    - Surveillance data are described: ETS to NTBS, residence assignment, and the LTLA versus
      national count discrepancy.
    - Pre-entry screening and pre-biologic LTBI screening are discussed.
    - UK TB figures are updated.
    - Mis-cited references are corrected.
    - Pre-specification is described accurately, and post hoc analyses are labelled.
    - Controls are removed from the FDR family.
    - Tables are generated from result files.
    - An individual-level target trial specification is given.

---

## Reviewer 1 (epidemiology and biostatistics)

**M1. MDE framework assumptions.** Implemented.
- The assumptions are listed in Methods: prevalence proportional to prescribing, a homogeneous
  baseline, and timing.
- The minimum detectable PAF is reported for each drug and design.
- An expected effect stratified by age and birthplace is added (steroids: 0.29% per 10%, against 0.34%
  under homogeneity).
- One-sided correct-direction power is labelled.
- The 10% contrast is shown to cancel in the MDE-to-expected ratio.

**M2. Simulation noise.** Implemented.
- Real counts are kept, and exposure trajectories are permuted across areas, so null replicates
  reproduce the real error structure.
- The empirical null SD is compared with the real clustered SE [R].
- Timing-misspecification scenarios are added.
- There are 500 null replicates, with Monte Carlo SEs.
- LTLA is complete.
- The claim that the simulation "matched analytic" results was removed.

**M3. Positive control too easy.** Implemented.
- It is reframed as validating the placement of disease-specific drug volume.
- The elasticity is reported: 0.20 for all anti-TB drug quantity and 0.41 for pyrazinamide regimens
  before reclassification [R after reclassification].
- It is carried into the expected effects.
- "Linked validly" is removed.
- The failure of the primary care control is stated.

**M4. Hospital SEs.** Implemented.
- Clustering by principal trust is added.
- Coverage by year is reported.

**M5. Spatial diagnostics.** Implemented. Moran's I of residuals is now computed for each year.

**M6. Specification.** Implemented, as follows:
- Area-specific trends are added.
- Log population is used as a covariate.
- Zero handling is harmonised (positive exposures only).
- Concurrent and t−1 windows are reported.
- The deviation from the original rolling-window design is reported, with its results given in the
  supplement.

**M7. Covariates.** Partly implemented.
- Diabetes adjustment is removed for metformin and insulins.
- In-migration is discussed.
- Annual APS country-of-birth estimates by local authority were not added. They end in 2021 and have
  large sampling error at LTLA level. UK-born and non-UK-born outcomes are modelled regionally instead.

**M8. Pre-specification and multiplicity.** Implemented.
- The chronology is described accurately.
- Post hoc analyses are labelled exploratory.
- Controls are removed from the FDR family.
- The number of tests is reported for the hospital and falsification families.

**M9. Lead tests and 9 clusters.** Implemented.
- Lag and lead are estimated jointly on a common sample, with a test of their difference.
- Randomisation inference is used.
- The "7 of 90" statement is removed.
- The implausibility argument leads.
- All UK-born 65+ results are reported, including the lead-3 estimate.

**M10. Nulls versus equivalence.** Implemented. The largest compatible PAF from the 90% upper
limit is reported for each drug.

**M11. Scope of conclusions.** Implemented.
- The conclusion is reworded.
- The "one to two orders of magnitude" claim is reconciled with the reported ratios.
- Attenuation mechanisms are discussed.

**M12. Stale results.** Implemented. All tables are regenerated from output files after the final
re-run.

**Minor 1–19.** Implemented, as follows:
- The cross-sectional analysis is replaced by a same-period local authority cross-section with
  resident denominators.
- Table scales are separated.
- Levels are harmonised.
- LTLA hospital results are reported.
- DDD units are used.
- The RECOVERY trial is cited.
- Rifampicin use for latent TB is discussed.
- Wording is corrected.
- References are reordered.
- RECORD items are added to the supplement.
- The linkage figures are distinguished.
- Counts are harmonised to the TB in England 2025 report.
- The within-area variation figure is added.
- The long-difference methods are described.
- Missing data are described.
- Terminology is corrected.

---

## Reviewer 2 (TB clinical and public health)

**M1. Notifications and surveillance.** Implemented.
- "Notifications" is used throughout.
- A surveillance data paragraph covers:
  - ETS until 2021 and NTBS after, with data from 2018 migrated
  - the case definition
  - residence assignment
  - the notification year
  - the discrepancy between LTLA sums and the national total (5,539 vs 5,490 in 2024)
  - local authority harmonisation
- Sensitivity analysis restricted to outcome years 2018–2024 [R].

**M2. Positive control specificity.** Implemented.
- Pyrazinamide/ethambutol products form the positive control.
- Rifamycin/isoniazid products are reported separately.
- The hospital negative control is levetiracetam.
- Primary care anti-TB prescribing is reframed.
- FP10(HP) prescriptions are discussed as a limitation.

**M3. Lag windows.** Implemented.
- The primary exposure is t−1, with a distributed lag.
- Year t is interpreted as mixed.
- The timing literature is cited (Keane 2001).
- Adjunctive glucocorticoids used in TB treatment are discussed.
- Protopathic bias in individual-level relative risks is discussed.

**M4. Place of birth, age and social risk.** Partly implemented.
- A stratified expected effect is added.
- The "UK-born" rationale is corrected, and references are fixed.
- The mismatch in the 65+ denominator is stated as a limitation, because UK-born population by age
  is not published by region.
- Social risk covariates were not added to the local authority panels. Consistent annual series are
  not available before 2019/20. The limitation is discussed and cited.

**M5. Programmes and migration.** Implemented.
- The LTBI programme is mapped from CCGs to local authorities (83 LTLAs and 63 UTLAs ever active) and
  added as a covariate.
- Pre-entry screening is described.
- The asylum support sensitivity analysis is reported in the supplement.

**M6. COVID-19.** Implemented.
- Outcome and exposure years 2020–21 are excluded in a sensitivity analysis.
- COVID-era hospital glucocorticoids are discussed.
- The RECOVERY trial is cited.
- The notification caveat for 2020 is added.

**M7. LTBI screening before biologics.** Implemented.
- A Discussion paragraph is added (BTS 2005, NICE NG33, Carmona 2005, Gómez-Reino 2007).
- A screening-attenuated relative risk scenario is added.
- The use of Dixon 2010 is corrected.

**M8. Surveillance benchmark.** Implemented. The recorded share gives an expected change of 0.055%
per 10% for steroids and 0.098% for biologics. We recommend the aggregate data request.

**M9. Programme implications.** Implemented.
- The limits of the null findings are stated explicitly.
- TB programme implications are added: completeness of NTBS immunosuppression fields, and audit of
  pre-treatment LTBI screening.
- Realistic UK data routes are named.

**M10. Alternative data.** Discussed.
- The UKHSA aggregate extract is recommended.
- 2025 notifications are not yet available by local authority.

**Minor 1–20 and factual corrections 1–12.** Implemented, including:
- the 2024 count of 5,490, with the 2025 national figure of 5,424
- the UK-born decline (43%, reaching a low point in 2022)
- corrections to references 22, 32, 33, 34, 35 and 37
- naming of ETS and NTBS
- a description of the LTBI programme
- people-first language

---

## Reviewer 3 (pharmacoepidemiology and prescribing data)

**M1. Primary care groups.** Implemented, see main change 1. A presentation-level listing is
provided in the supplement.

**M2. Hospital groups and units.** Implemented, see main change 4.
- The DDD table is provided.
- The Rifater and Voractiv parser bug is fixed.
- Negative quantities are clipped.

**M3. Positive control.** Implemented, see main change 5.

**M4. Items as exposure.** Implemented.
- Prednisolone-equivalent mg and ADQ measures are added.
- Within-area SD is reported for each measure.
- Items versus ADQ is reported [R].

**M5. SCMD coverage.** Implemented.
- The successor map is applied.
- Coverage is reported by year.
- Provisional versus final data and the extraction date are stated.
- A homecare capture check was not performed. It is listed as a limitation.

**M6. Practice-to-area mapping.** Implemented, see main change 2.

**M7. Denominators and cross-section.** Implemented.
- The cross-section now uses resident denominators and prescribing from the same period.
- The earlier Methods error is corrected.

**M8. Splice.** Partly implemented.
- The same rules and practice restriction are applied to both series.
- A splice indicator is used as a sensitivity analysis [R].
- HSCIC practice-level files after 2013 were not located in the data.gov.uk inventory, so
  overlap-period concordance could not be assessed. This is stated.

**M9. MDE inputs.** Implemented.
- SCMD-derived prevalence is used.
- Sensitivity to the elasticity is shown.
- The hospital glucocorticoid scenario is respecified.
- The odds ratio is labelled as such.

**M10. Catchments and SEs.** Implemented. Elective catchments and principal-trust clustering are
added.

**M11. Individual-level design.** Implemented. A target trial specification box is added.

**Minor 1–22 and bugs B1–B20.** Addressed. Specifically:

| Bug | Action |
|---|---|
| B1 | Fixed-dose combination strengths |
| B2 | Successors |
| B3 | Principal-trust clustering |
| B4 | Classification |
| B5 | Audit files regenerated by `build_scmd_classification.py` |
| B6 | `summarise_scmd.py` superseded |
| B7 | Cross-section replaced |
| B8–B9 | Groups redefined |
| B10 | RO76 applied |
| B11 | Residence apportionment |
| B12 | Robust pre-2014 pipeline |
| B13 | Presentation-level mg for all formulations |
| B14 | `mde.py` produces LTLA and UTLA tables |
| B15 | Scenarios respecified |
| B16 | Cost measure dropped |
| B17 | Negative quantities clipped |
| B18 | Catchment year limitation stated |
| B19 | Coverage by year |
| B20 | References fixed |
