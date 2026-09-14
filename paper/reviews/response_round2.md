# Response to reviewers, round 2

We thank the reviewers for careful second reports. Each claim was checked against the code and
outputs before acting on it, and all analyses were rerun. Numbers below come from the rerun and
match the revised manuscript (draft 4). Where we did not do what was asked, we say so.

## Main changes

1. **GP practice restriction corrected** (R3 N1). We confirmed the error: the current ODS file
   omits practices closed before 2017, so their prescribing was dropped (3.4% of items in 2011,
   1.7% in 2014, none from 2016). Practices absent from the file with the standard GP code format
   are now included (the format matches 94% of RO76 codes and few codes in other settings). The
   GP share of items is now flat at 98.7–98.9% in every year from 2010 (previously rising from
   95.5% to 98.8%). Each practice-year now uses that practice's nearest registration release, and
   practices in no release fall back to their postcode (1.1% of items in 2011, 0.02% from 2014).
   All panels, models, the national series and the splice table were rerun. The oral
   glucocorticoid discontinuity at the 2013/14 splice persists (+2.8%, against +0.1% in the years
   either side), so it is not this artefact; restricting to EPD-era exposure gave 0.979
   (0.939–1.021).
2. **Simulation interpretation corrected** (R1 N1). We confirmed that replicate SEs matched the
   null SD (LTLA 0.0161 vs 0.0166; UTLA 0.0167 vs 0.0171 in the rerun), so the test was
   approximately calibrated (mildly anti-conservative), not conservative. "Conservative" and "agreed" were removed. Analytic power at the real-data SE is
   now reported beside simulated power (Table S4, Results, Abstract). On the mechanism, permuted
   exposures retained 93% of the real exposure's residual variance after fixed effects and
   covariates, so lower exposure variance does not explain the gap. The likelier explanation is
   that permutation breaks the alignment between an area's exposure trajectory and its own
   notification trend, which the clustered SE picks up on real data. We did not implement a
   calibrated (residualised) permutation. Simulations were rerun on the corrected panels. With no
   effect, rejection was 7.8% (LTLA) and 7.6% (UTLA), so the clustered test is mildly
   anti-conservative. For the published glucocorticoid effect, rejection was 8.3% and 8.0%. For IRR
   1.05 per 10%, simulated rejection was 83% (LTLA) and 78% (UTLA), against analytic power at the
   real SE of 65% and 51%.
3. **Falsification models** (R1 N2). Previous, same and following years are now fitted jointly
   (Table S2b), with a Wald test of t−1 against t+1 and the correlation of the two estimates at
   both levels. Table 1 now shows the joint t−1 and t+1 estimates and the difference p. With
   year t added, previous-year terms were null for every group, same-year terms were positive for
   several groups and following-year terms stayed inverse. In the two-year model the lag and lead
   estimates were correlated from −0.83 to +0.08; with year t added, from −0.23 to +0.17. The
   inverse following-year terms persisted in that model, so they are not a collinearity artefact.
4. **Framing** (R1 N3; R2 N3). "One to two orders of magnitude" is replaced by the reported
   ranges (10 to several hundred times). "Reflect confounding" is replaced by "compatible with
   residual confounding, chance or measurement error, not with drug effects of plausible size".
   Heavy attenuation is now stated for hospital medicines only, and the Methods chronology states
   that the pre-specified primary care positive control failed.
5. **Hospital medicines** (R3 N2, N3, N6; R2 M6, N2, N3).
   - Duplicate (code, unit) rows are removed before merging, with an assertion. Only the tacrolimus
     granule rows were duplicated.
   - The positive control is now pyrazinamide DDD from all pyrazinamide-containing products,
     including fixed-dose combinations.
   - Systemic glucocorticoids are now prednisolone-equivalent mg without dexamethasone and
     hydrocortisone, which form a separate descriptive group. The RR 4.9 hospital scenario is
     removed.
   - The TNF scenarios are RR 4 (before screening) and RR 1.5 (with screening), described as
     illustrative and favouring detection, with Carmona 2005 cited for the 6.2-fold pre-screening
     contrast and the fall to the untreated rate afterwards.
   - The elasticity is reported with its CI. The attenuated ratios are described as illustrative,
     with the timing assumption and the differences in supply routes stated.
   - A sensitivity table (Table S3b) reports hospital models excluding outcome years 2020–21 and
     using elective catchments.
   - Results. The positive control's same-year IRR was 1.035 (1.009–1.061), elasticity 0.36
     (0.10–0.62). Candidate drugs were null except hospital systemic glucocorticoids, 1.024
     (1.001–1.046) at upper-tier level. That estimate was not robust to trust clustering
     (0.999–1.049) or to excluding outcome years 2020–21 (1.018, 0.969–1.069), and would imply an
     attributable fraction of 24%. Oral forms alone gave 1.011 (0.991–1.032), so the association
     depended on intravenous methylprednisolone pulses. We report it as chance or bias. Hospital MDEs were 1.0–2.9% per
     10%, 26–520 times the illustrative expected effects before attenuation.
6. **Regional analyses** (R1 N4; R2 minor 3). The randomisation test now uses the cluster-robust t
   statistic, with permutations drawn directly. Exchangeability and p = (1 + count)/(1 + 499) are
   stated. A leave-London-out joint model is reported for UK-born notifications. Regional MDEs
   are compared with the expected effect in UK-born people aged ≥65. Regional MDEs, from the t(8) intervals, were 46–119%
   per 10% for glucocorticoid exposures, against an expected 0.9%. With the studentised test, the
   UK-born joint lag estimate for prednisolone mg (1.45) had randomisation p = 0.23 (previously
   0.04), and excluding London gave 1.12 (p = 0.73). All 4 of the 81 adjusted regional estimates
   with randomisation p ≤ 0.05 were lead terms.
7. **Bounds** (R1 N5). Tables and text now give the largest prevented fraction for drugs expected
   to protect and a PAF bound after dividing by the negative-control estimate. For oral
   glucocorticoids the bound is 5%, rising to 44% after the negative-control shift, close to the
   minimum detectable PAF (63%). The text explains the difference between the two.
8. **Text matching the outputs** (R1 N6; R2 M1; R3 minor 15). Counts of estimates and nominal
   hits, areas and area-years are now generated from result files. The original design is
   tabulated (Table S8). Lower-tier models: 30 of 277 estimates nominally significant, concentrated in
   the negative control, metformin and inhaled corticosteroids.
9. **Promised items now in the manuscript** (R2 N4; R3 N4).
   - FP10(HP) limitation.
   - RECOVERY cited for hospital dexamethasone.
   - NICE NG33 cited in general terms, because the guideline text could not be fetched to confirm
     specific wording.
   - Description of the LTBI programme, including that the indicator was carried forward after
     2019/20 and that 2020 disruption was not modelled.
   - Pre-entry screening in the limitations.
   - Drug group definitions (Table S9) and the SCMD classification with DDDs
     (`outputs/hospital/vmp_classification.csv`).
   - Within-area SD for every group and measure (items, ADQ, prednisolone-equivalent mg).
   - Transplant immunosuppressant inputs in Table 2, labelled illustrative.
   - Data extraction dates in Data availability.
10. **UK TB epidemiology** (R2 N1). Checked against PubMed and our data:
    - Thomas 2018 is described correctly (2011–2015; most of the fall from declining rates).
    - The 2011–2018 fall is 44%.
    - The UK-born fall is 48% to 2022 and 43% to 2024.
    - 81.9% of 2024 notifications were in people born outside the UK.
    - 2014 and 2020 counts are from the Fingertips national series.
    - Davidson 2018 is cited only for transmission and social risk.
    - The 78% and seven-fold figures are attributed to Carmona 2005 and Gómez-Reino 2007
      respectively.
    - The Box uses the 2024 UK-born rate (2.1 per 100,000).
11. **Checks requested** (R3 minor 1, 5). Dexamethasone contributes 5.6–6.7% of primary care
    prednisolone-equivalent mg (January 2015, July 2019, July 2024), so the regional mg analysis
    was not rerun without it. There were no rows with a NULL UNIDENTIFIED flag in those months.

## Reviewer 1

- **M1(a) Direction of assumption 1.** Now stated as unknown, with a fourth assumption (new users
  rather than longer courses) added.
- **M1(b) Birthplace stratification.** The benchmark is relabelled "age-stratified";
  birthplace-specific prevalence was not added.
- **M1(c) Recorded-case benchmark.** Converted to an attributable fraction (× (RR − 1)/RR). The
  upper bound assumes 50% recording: steroids 0.043–0.087%, biological therapy 0.078–0.157%.
- **M1(d) Invariance to the 10% contrast.** A sentence is added to the Table 2 note.
- **M3(a) Elasticity CI.** Given in the Table S3 note.
- **M3(b) Timing.** The timing component of the elasticity is stated.
- **M3(c) Failed positive control.** Now in the Methods chronology.
- **M3(d) Harder positive control.** Not done; added as a limitation.
- **M4.** Principal-trust clustering is retained. Multiway clustering and dominant-trust shares
  were not added.
- **M5.** Residual dependence is described as weak and concentrated in 2014 (the only outcome year
  with pre-2014 exposure).
- **M6(a) Original design.** Table S8.
- **M6(b) Dropped zero-exposure area-years.** Counted in the result files: none in the primary
  care models.
- **M7 Compositional exposure change.** Mentioned under likely causes.
- **M8(a) Chronology.** Reworded.
- **M8(b) Test counts.** Generated from files for the panel and regional families.
- **Minor 1.** Table 2 relabelled, with the SE added.
- **Minor 2.** Table 3 legend added.
- **Minor 3.** Long-difference methods added.
- **Minor 4.** Missing-data handling added; the asylum model years corrected.
- **Minor 5.** RECOVERY cited.
- **Minor 6.** Definitions and classification added (Table S9 and file).
- **Minor 7.** Figures are renumbered in order of first citation, and supplementary tables are
  first cited in numerical order in the Methods.
- **Minor 8.** FDR family stated.
- **Minor 9.** Count conventions: Fingertips national series used.
- **Minor 10.** Hospital lead comment added to the Table 3 legend.
- **Minor 11.** Randomisation p resolution stated.
- **Minor 12.** The "±9%" wording is clarified.

## Reviewer 2

- **M1.** The following are now stated:
  - notification year;
  - that the handling of people without a postcode is not described in the tables;
  - that zero counts are retained;
  - the discrepancy reworded as "possibly";
  - area counts harmonised.
- **M2.** FP10(HP) added.
- **M3.** Inverse same-year estimates under the earlier models are now superseded: with previous,
  same and following years fitted together, same-year terms are positive for several groups,
  which we describe. Hospital dexamethasone is separated. A maintenance-dose proxy was not added.
- **M4.** The ≥65 denominator mismatch is stated explicitly, and the Davidson citation corrected.
- **M5.** The LTBI programme is described, the carry-forward disclosed, and pre-entry screening
  added to the limitations.
- **M6.** RECOVERY cited. Hospital glucocorticoids exclude dexamethasone, and a model excluding
  outcome years 2020–21 is reported (Table S3b). Geographically differential rebound was not
  examined.
- **M7.** NG33 cited in the text, the attributions corrected, and the TNF scenarios corrected.
- **M8 minor.** The single-year counts and the breadth of "biological therapy" are noted.
- **M10.** Culture-confirmed and drug-resistant outcomes are stated as not available by local
  authority and year.
- **N3.** Elasticity caveats added. Rifamycin/isoniazid products had the same elasticity (0.37,
  0.22–0.51), which we now report and interpret.
- **Minor 1.** Screening before oral glucocorticoids now qualified.
- **Minor 2.** Keane 2001 cited; UKHSA rate in the Box.
- **Minor 3.** Leave-London-out added; shared downward trends stated.
- **Minor 4.** Metformin sentence added.
- **Minor 5.** Fourth assumption added.
- **Minor 6.** Input sources are in Table 2 inputs (`paper/mde_inputs.csv`).
- **Minor 7.** Completeness assumption stated.
- **Minor 8.** Pre-entry screening added.
- **Minor 9.** Data dates added.
- **Minor 10.** Figure titles use counts from the data.
- **Minor 11.** Denominator stated in Methods.
- **Minor 12.** Legend note added.
- **Minor 13.** Dexamethasone separated.
- **Minor 14.** Language checked.

## Reviewer 3

- **N1.** See main change 1.
- **N2.** See main change 5. Separate pyrazinamide-only and ethambutol-only series were not
  reported.
- **N3.** See main change 5.
- **N4.** See main change 9. The within-area correlation of log items with log ADQ was not
  reported. A dose-stratified oral glucocorticoid scenario and a primary care elasticity grid were
  not added: primary care has no validated elasticity.
- **M5.** Final/provisional status and the extraction period are now stated.
- **M8.** We did not re-examine NHS Digital practice-level files after January 2014, so overlap
  concordance remains unassessed. The EPD-only sensitivity analysis is reported.
- **B5 and B6.** `summarise_scmd.py` moved to `legacy/` with a README saying it is superseded and not
  run; the legacy SCMD audit files moved to a `legacy/` subfolder of the raw data.
- **B18.** Applying 2024 catchments to 2019 is stated as a limitation.
- **B19.** Coverage text corrected (95% for levetiracetam).
- **Minor 4.** Nearest-release apportionment implemented.
- **Minor 6.** The INJECTABLE regex was not changed: no false exclusions were found.
- **Minor 7 and 8.** Definitions noted in the limitations.
- **Minor 9 and 10.** Rising unmatched shares in 2023–24 and unmatched non-acute trusts were not
  investigated.
- **Minor 13.** Levetiracetam was not passed through the new classification.
- **Minor 14.** Stale import removed and docstring updated.
- **Minor 16.** Extraction dates stated. Deposit with a DOI not done.
- **Minor 17 and 18.** Done.
