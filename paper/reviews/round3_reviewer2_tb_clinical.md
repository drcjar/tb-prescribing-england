# Peer review, round 3: Reviewer 2 (TB clinical medicine and UK TB public health)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England" (Draft 4, revised after round 2, 14 September 2026)

**What I checked.** I read my round 2 report, the round 2 response and the whole of Draft 4, including Tables S1–S9. I checked the response letter's claims against the manuscript text itself. I checked these data claims against the files:

- **National counts and rate.** 8,282 (2011), 6,474 (2014), 4,609 (2018), 4,123 (2020), 5,490 (2024) and 9.4 per 100,000, against `data/raw/tb_at6.csv` (Fingertips). All match.
- **UK-born counts and share.** 1,756 / 916 / 995 and 81.9%, against `data/processed/region_tb_birthplace_annual.csv`. All match.
- **LTBI programme areas.** "Active in 83 LTLAs", against `data/processed/ltbi_programme_ltla.csv`. Matches, and the indicator is flat at 83 from 2019 to 2025 (carried forward, as now disclosed).
- **Hospital glucocorticoids.** 1.024 (1.001–1.046), trust-clustered 0.999–1.049, and 1.018 (0.969–1.069) excluding outcome years 2020–21, against `outputs/hospital/hospital_results_utla.csv`. All match.
- **UK-born regional joint model.** 1.45, randomisation p = 0.232; without London 1.12, p = 0.73, against `outputs/steroids/ocs_tb_by_birthplace_lag_lead.csv`. All match.
- **Recorded-case benchmarks.** 0.043/0.087% and 0.078/0.157%, against `outputs/mde/expected_effect_benchmarks.csv` and `mde.py` (30 and 54 of 5,490). All match.
- **Arithmetic.** The TNF scenario figures (0.10% and 0.017%) and the 24% attributable fraction implied by IRR 1.024. Both correct.
- **PubMed spot-checks.** Berrocal-Almanza 2022 ([doi:10.1016/S2468-2667(22)00031-7](https://doi.org/10.1016/S2468-2667(22)00031-7)), Aldridge 2016 ([doi:10.1016/S0140-6736(16)31008-X](https://doi.org/10.1016/S0140-6736(16)31008-X)), Loutet 2018 ([doi:10.1183/13993003.01226-2017](https://doi.org/10.1183/13993003.01226-2017)) and RECOVERY 2021 ([doi:10.1056/NEJMoa2021436](https://doi.org/10.1056/NEJMoa2021436)).

---

## 1. Recommendation

**Accept after minor revision.** No scientific issue blocks publication. The editor can check the remaining corrections without further review.

The authors have dealt with nearly all of my round 2 concerns, and the changes are visible in the manuscript itself this time:

- **UK TB epidemiology.** It is now accurate and matches the data: the 44% fall, Thomas 2018 described correctly, 48%/43% for UK-born notifications, 81.9%, and Fingertips counts.
- **Hospital glucocorticoids.** Dexamethasone and hydrocortisone are separated out, RECOVERY is cited, and the nominal association is reported and interpreted appropriately.
- **TNF scenarios.** They are now sourced and labelled as detection-favouring.
- **LTBI programme.** It is described, and the carry-forward is disclosed.
- **UK-born regional finding.** It is now presented with a studentised randomisation test and a leave-London-out analysis. Both support the authors' reading.

The main conclusion is robust and clinically sensible: ecological analyses of these data cannot detect plausible drug effects on TB.

**Must fix before acceptance** (all are text changes):

1. **NICE NG33.** The response says it is "cited in the text", but it appears only in the reference list. Either cite it where screening is discussed or delete it. Also remove the verification notes still embedded in the reference list (N4 below).
2. **FP10(HP) sentence.** It is factually wrong about the EPD (N1).
3. **Pre-entry screening date.** "UK-wide from 2012" is incorrect (N2).
4. **2020 count.** The Introduction says 4,125 and the Results say 4,123; use one figure (N3).

---

## 2. Status of round 2 items

### Major items

| Item | Status | Comment |
|---|---|---|
| **M1. Surveillance description** | **Addressed** | Notification year, zero counts retained, no-postcode handling stated as undescribed, the discrepancy now "possibly", and area counts harmonised (151/294 throughout). |
| **M2. Positive control, FP10(HP)** | **Addressed, but the new sentence contains an error** | See N1. |
| **M3. Lag windows** | **Addressed (acceptable)** | Hospital dexamethasone is separated. The maintenance-dose proxy was declined, which is acceptable. With *t*−1, *t* and *t*+1 fitted jointly (Table S2b), same-year terms are positive, and the text now reads them correctly as consistent with protopathic prescribing. My round 2 point about inverse same-year terms is superseded. |
| **M4. Birthplace, age, social risk** | **Addressed** | The ≥65 denominator mismatch is stated explicitly (Methods and Limitations), and Davidson 2018 is now cited only for heterogeneity and transmission. |
| **M5. Pre-entry screening, LTBI programme** | **Addressed, with two wording issues** | The programme description, carry-forward, 2020 disruption and weak-control caveat are all present, and the 83 LTLAs are confirmed. See N2 (pre-entry date) and N4(b) (how much the programme affects notifications). |
| **M6. COVID-19** | **Addressed** | RECOVERY is cited. Dexamethasone and hydrocortisone form a separate descriptive group, and the model excluding outcome years 2020–21 is reported (Table S3b). Geographically differential rebound was not examined, which is acceptable. See N5 for a small interpretive point. |
| **M7. Screening before biologics** | **Mostly addressed** | The 78% figure is now attributed to Carmona 2005 and the seven-fold figure to Gómez-Reino 2007. The TNF scenarios are corrected (RR 4 and RR 1.5, with "probably nearer 1, so favours detection"). **NG33 is still not cited in the text** (must-fix 1). |
| **M8. Surveillance benchmark** | **Mostly addressed** | The single year (2024) is stated. That UKHSA's "biological therapy" category includes non-TNF biologics is still not said; half a sentence would do. |
| **M9. Implications** | **Addressed** | |
| **M10. Alternative outcomes** | **Addressed** | Culture-confirmed and drug-resistant outcomes are stated as unavailable by local authority and year. |

### New major issues from round 2

| Item | Status | Comment |
|---|---|---|
| **N1(a). Thomas 2018** | **Addressed** | Correctly described. Aldridge 2016 is still co-cited for the decline. It supports only the description of pre-entry screening, so move it to that clause. |
| **N1(b). UK-born decline** | **Addressed** | 48% to 2022, 43% to 2024, matching the data. The regional range (25–62%) was not added, which is optional. |
| **N1(c). Drivers of the UK-born decline** | **Addressed** | "Reflecting" is removed, and coincident trends are offered as the explanation. |
| **N1(d). Share born outside the UK** | **Addressed** | 81.9%. |
| **N1(e). 2014 count** | **Addressed** | Fingertips 6,474 is confirmed. See N3 for the 2020 inconsistency. |
| **N2. TNF relative risks** | **Addressed** | Sourced, labelled illustrative, and the post-screening RR is described as probably nearer 1. |
| **N3. Elasticity as general attenuation** | **Addressed** | Attenuated ratios are labelled illustrative. Timing, drug volume per person and supply-route caveats are in the Results and the Table S3 note. The rifamycin/isoniazid elasticity (0.37, 0.22–0.51) is now reported. See N6 for a small overreach. |
| **N4. Promised changes, uncited references, verification notes** | **Partly** | FP10(HP), RECOVERY, Berrocal-Almanza and Loutet are now in the text, and Dixon and Nguipdop-Djomo are removed. **NG33 is still uncited in the text.** The reference list still contains the reference-verification preamble ("Corrections relative to references_v3.md are listed at the end") and bracketed verification notes on NG33, OpenPrescribing ("accessed date to be added"), and the UKHSA 2021, 2025 and 2026 entries. |

### Round 2 minor items

| # | Status | Comment |
|---|---|---|
| 1. Screening before oral glucocorticoids | Addressed | "Less consistently done" is appropriately qualified. NG33 could be cited here. |
| 2. Uncited clinical claims | Addressed | Keane 2001 is cited, and the Box gives 2.1 per 100,000 with its source. The new clause "rates in older UK-born adults are of a similar order" is unsourced; give the UKHSA age-specific UK-born rate or delete it. |
| 3. UK-born regional finding | Mostly addressed | Leave-London-out and shared declining trends are now explicit, and well argued. Small regional counts and LFS sampling error are still not mentioned (one clause). |
| 4. Metformin | Addressed | |
| 5. Fourth assumption | Addressed | |
| 6. Expected-effect inputs | Partly | Sources are said to be in `paper/mde_inputs.csv`, but the Table 2 note still does not say that ICS RR 1.27 is "any use", that the PPI OR is for recent use in a Korean case-control study, or that the metformin RR is within people with diabetes. One sentence in the note would do. Not blocking. |
| 7. Completeness assumption | Addressed | 50% recording is stated. |
| 8. Pre-entry screening and LTBI pause in limitations | Addressed | But see N2. |
| 9. Data dates | Addressed | |
| 10. Figure 5 title | Addressed | |
| 11. Figure 6 denominator | Addressed (in Methods) | |
| 12. Table 3 lead note | Addressed | |
| 13. Dexamethasone separated | Addressed | |
| 14. Language | Addressed | |

---

## 3. New issues introduced by the revision

### N1. The FP10(HP) sentence is wrong about the EPD (must fix)

**What the Limitations say:** FP10(HP) prescriptions "are attributed to hospital prescribers, not GP practices, and are not in SCMD … so neither data source captures them."

**The problem.** The English Prescribing Dataset *does* include FP10(HP) items dispensed in the community. They appear under hospital trust prescribing cost centres rather than under GP practices. The reason they are absent from this study's primary care exposure is the authors' own restriction to standard GP practices (setting RO76 plus the practice-code-format rule).

**Suggested wording:** "Hospital prescriptions dispensed by community pharmacies (FP10(HP)) appear in the EPD under hospital prescribers, which our restriction to GP practices excluded, and are not in SCMD. Some TB treatment and specialist medicines reach patients this way, so neither of our exposure series captures them."

If FP10(HP) supply of antituberculosis drugs varies between trusts, it also adds to the attenuation of the hospital positive control. Half a sentence could say so.

### N2. The date of pre-entry screening is misstated (must fix)

**What the Limitations say:** "Pre-entry screening of long-stay visa applicants from high-incidence countries (UK-wide from 2012)".

**The problem.** Pre-entry screening was always a UK-wide visa requirement. What changed was the number of countries covered:

- **Pilot:** 15 high-incidence countries from 2005–06, the cohort described by Aldridge et al. (screened 2006–2012).
- **Full programme:** extended to all high-incidence countries between 2012 and 2014.

**Suggested wording:** "(piloted in 15 countries from 2005 and extended to all high-incidence countries during 2012–2014) [Aldridge 2016]". This also gives Aldridge 2016 a proper home (see N1(a) in the table).

### N3. The 2020 notification count differs between sections (must fix, trivial)

- **Introduction:** 4,125 [UKHSA 2021 report].
- **Results:** 4,123 (Fingertips; confirmed in `tb_at6.csv`).

Both are legitimate, from different releases. Use one figure, or say that figures are revised between releases.

### N4. LTBI programme text (minor)

**(a) Loutet 2018 is a local study.** It is a single-area evaluation (Newham, 2014–15), cited here to describe the national programme. Berrocal-Almanza 2022 is the right citation for the national eligibility criteria: aged 16–35, born in a high-incidence country, entered in the past 5 years, 55 high-burden areas. Loutet can stay as supporting context. Also add "who entered within the previous five years" to the Methods description.

**(b) "Reduce notifications … in the areas where they settle" overstates the programme's population impact.**

- *What Berrocal-Almanza found:* 10.1% of eligible registrants were tested. Testing and treatment was associated with a lower TB hazard among those tested (HR 0.76, 0.63–0.91).
- *Why the wording overstates it:* with that uptake, any effect on area-level notifications is likely to be small.
- *Suggested wording:* "may reduce notifications among recent entrants". This strengthens, rather than weakens, the point that the covariate is a weak and probably minor control.

### N5. Interpretation of the hospital glucocorticoid finding (minor; the conclusion is sound)

The interpretation is right. An IRR of 1.024 per 10% implies an attributable fraction of 24% (I confirm the arithmetic), against recorded steroid-associated immunosuppression in 0.5% of notifications. That implausibility is the decisive argument. Two refinements would make the robustness wording accurate:

- **"Not robust to excluding outcome years 2020–21" is really a loss of precision.** The point estimate barely moves (1.024 → 1.018), but dropping two of five outcome years (n 755 → 453) doubles the CI width.
  - The trust-clustered interval (0.999–1.049) is also borderline.
  - With elective catchments the estimate stays nominally significant (1.025, 1.003–1.048; Table S3b).
  - Say "imprecise when…" rather than "not robust", and let the attributable-fraction argument carry the interpretation.
- **Exposure year 2021 is still in the sensitivity model.** With *t*−1 exposure, excluding outcome years 2020–21 still leaves exposure year 2021 (the January 2021 wave) for outcome year 2022. Now that dexamethasone is separated this matters less, because prednisolone and methylprednisolone were far less affected by COVID-19 treatment. Still, the label should not be read as "COVID-free exposure".

Also, hospital hydrocortisone is used mainly intravenously for acute illness (asthma and COPD exacerbations, anaphylaxis, septic shock, adrenal crisis), not mainly as replacement therapy. Hospital dexamethasone is also used for TB meningitis [Thwaites 2004] and cerebral oedema. Adjust the parenthetical in the Methods. The first point is a further reason, consistent with the authors' choice, to keep hydrocortisone descriptive. The second is a protopathic route worth half a clause.

### N6. Rifamycin/isoniazid elasticity (minor)

"The more specific measure gained nothing, so the attenuation is dominated by apportionment rather than drug specificity."

- **What the equal elasticities show:** drug specificity is not the limiting factor.
- **What they cannot show:** how attenuation splits between apportionment, timing and drug volume per person treated. The previous sentence correctly lists all three.
- **Suggested wording:** "so drug specificity was not the limiting factor."

### N7. Unverified figure (minor)

"41% of those were notified within five years of arrival" [UKHSA 2025]: I could not check this against the processed files. Please give the specific supplementary table, and state whether the denominator is non-UK-born people with a known year of entry.

### N8. For the editor: the response letter

The round 2 response contains unrendered template placeholders ("{{n_sig_ltla}} of {{n_est_ltla}}", main change 8) and "[pending check at assembly]" (R1 minor 7). The manuscript itself gives the numbers (30 of 277), so this affects only the letter. The letter also says NG33 was cited in the text, which it was not.

---

## 4. Checks that found no problem

- **Epidemiology in the Introduction and Results.** The national counts, 44% fall, 2024 rate (9.37 per 100,000 in Fingertips), UK-born figures and 81.9% all reproduce from the data files.
- **New clinical statements.** These are accurate: RECOVERY (dexamethasone benefit in patients on oxygen or ventilation), Carmona and Gómez-Reino attributions, Keane 2001 timing, and Jick 2006 (OR about 5, higher at ≥15 mg/day).
- **Regional results.** The UK-born and regional numbers (Tables S5, S6), the "4 of 81, all lead terms" count and the leave-London-out results match the output files. The interpretation is appropriately cautious.
- **LTBI covariate.** It is now described accurately, including the carry-forward and the unmodelled 2020 disruption. The model uses only `ltbi_active`, so the carried-forward test rates I flagged in round 2 do not enter the analysis.
- **Recorded-case benchmarks.** The attributable-fraction conversion and the 50%-recording bound are correct.

## 5. Summary for the editor

Draft 4 addresses my substantive clinical and public health concerns, and the data claims I checked reproduce. The remaining items are:

- **Four short must-fix corrections:**
  - cite NG33 in the text or delete it, and strip the verification notes from the reference list;
  - correct the FP10(HP) sentence (FP10(HP) items are in the EPD but were excluded by the GP restriction);
  - correct "UK-wide from 2012" for pre-entry screening;
  - reconcile 4,125 and 4,123.
- **A handful of optional wording refinements** (N4–N7, and minor items 3 and 6).

I do not need to see the manuscript again.
