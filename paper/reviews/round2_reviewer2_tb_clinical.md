# Peer review, round 2: Reviewer 2 (TB clinical medicine and public health)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England" (Draft 3, revised after peer review, 14 September 2026)

**Reviewer expertise:** TB physician and public health epidemiologist; UK TB surveillance (ETS/NTBS), migrant and LTBI screening, TB in UK-born and inclusion health populations.

**What I checked.** I read the round 1 report, the response letter and the revised manuscript, including the supplementary tables and Figures 5 and 6.

I checked the letter's claims against the manuscript text, not just against the letter. This was done by searching the main text (lines 1–773) for each reference and topic the letter says was added.

I recomputed the national, UK-born and regional TB counts from `data/processed/*tb_annual*.csv`. I also inspected:
- `build_ltbi_covariate.py` and `data/processed/ltbi_programme_utla.csv`;
- `outputs/hospital/hospital_results_*.csv` and `hospital_mde_utla.csv`;
- `outputs/steroids/ocs_tb_by_birthplace_regional.csv`.

I spot-checked 12 key citations against PubMed abstracts: Carmona 2005, Gómez-Reino 2007, Jick 2006, Thomas 2018, Davidson 2018, Castellana 2019, Brassard 2006, Brassard 2011, Song 2019, Li 2020, Zhang 2020 and Aldridge 2016.

---

## 1. Recommendation

**Minor revision.** The corrections below are required before acceptance.

The authors have done a great deal of work, and the paper is much stronger. The key improvements are:
- **Positive control:** it is now disease-specific (pyrazinamide/ethambutol), with a within-area negative control (levetiracetam).
- **Exposure timing:** year *t*−1 is primary, with a distributed lag.
- **Expected effects:** now benchmarked against UKHSA-recorded drug-associated TB.
- **Screening before biologics:** the Discussion now covers it.
- **Implications:** there is a specific section for TB programmes.

I am confident the main conclusion is robust: ecological designs cannot detect plausible drug effects on TB.

What remains falls into four groups:
- **Epidemiology statements:** several are still inaccurate or wrongly attributed.
- **Letter vs manuscript:** a number of changes promised in the response letter are not in the manuscript.
- **Screening-attenuated RR:** the calculation for TNF inhibitors has a sourcing problem and a derivation problem.
- **Two data-construction issues:** the LTBI programme covariate, and COVID-era hospital glucocorticoids. Both need to be stated or handled.

None of these requires new data collection, and only one (M-new-5) involves reporting analyses the authors have already run.

---

## 2. Point-by-point status of round 1 major comments

| Item | Status | Comment |
|---|---|---|
| **M1. Notifications, surveillance description** | **Partly** | See below |
| **M2. Positive control** | **Addressed** (one residual item) | See below |
| **M3. Lag windows** | **Mostly addressed** | See below |
| **M4. Birthplace, age, social risk** | **Partly** | See below |
| **M5. Pre-entry screening, LTBI programme, migration** | **Partly** | See below |
| **M6. COVID-19** | **Partly** | See below |
| **M7. Screening before biologics** | **Partly** | See below |
| **M8. Surveillance benchmark** | **Addressed** | See below |
| **M9. Implications for TB programmes** | **Addressed** | See below |
| **M10. Alternative data** | **Partly (acceptable)** | See below |

### M1. Notifications, surveillance description: Partly

**Done:**
- "Notifications" replaces "incidence" throughout, including the title.
- ETS→NTBS is described, with data from 2018 migrated.
- The case definition and residential-postcode assignment are given.
- The 2023 boundary handling and the LTLA-sum vs national discrepancy (5,539 vs 5,490) are reported.
- An NTBS-era sensitivity analysis (outcomes 2018–2024) is in Table S1.

**Still missing:**
- **Notification year.** Is it notification date or treatment-start date? Not stated.
- **Extract and publication dates** of the regional workbooks are not stated.
- **Zero-count area-years.** Their number is not given.
- **People without a residential postcode.** Handling of no fixed abode, prison and asylum accommodation is not described.
- **The discrepancy explanation is asserted, not shown.** The Methods attribute the discrepancy to "different extract dates", but nothing in `build_tb_annual.py` or the manuscript demonstrates this. Either cite the UKHSA methodology note that says so, or write "possibly reflecting different extract dates or residence-assignment rules".
- **Area counts are inconsistent.** The Abstract and the primary-analysis heading say 294 LTLAs and 151 UTLAs. The Methods say 292 and 149 were analysed. The Figure 5 title says "151 upper-tier authorities". Please reconcile.

### M2. Positive control: Addressed (one residual item)

**Done:**
- The positive control is redefined as pyrazinamide/ethambutol-containing products.
- Rifamycin/isoniazid products are reported separately.
- The within-area elasticity is reported (0.36 UTLA, 0.40 LTLA) and interpreted as attenuation.
- A hospital negative control (levetiracetam) behaves as it should: the between-area correlation is weak (ρ ≈ 0.21) and within-area estimates are null.
- Primary care antituberculosis prescribing is reframed as descriptive only.

**Residual item:** the response says FP10(HP) prescriptions "are discussed as a limitation". There is no mention of FP10(HP), or of the routes by which TB drugs reach patients, anywhere in the manuscript. Please add one sentence. (See also new issue N3 on how the elasticity is used.)

### M3. Lag windows: Mostly addressed

**Done:**
- Exposure in *t*−1 is primary, with a distributed lag (*t*, *t*−1, *t*−2) and the old three-year window as sensitivity analyses.
- Keane 2001 and Thwaites 2004 are cited.
- Protopathic bias is discussed, including its effect on the Jick estimate.

**Not done, and not mentioned:**
- a maintenance-dose proxy for oral glucocorticoids (for example 1 mg and 2.5 mg prednisolone tablets);
- separate reporting of hospital dexamethasone.

**One interpretive point to add.** With annual data and a median time to TB of about 12 weeks, much of the plausible causal window falls in year *t*, not *t*−1.

In Table S2 the same-year terms are *inverse*:
- inhaled corticosteroids 0.896 (0.849–0.946);
- insulins 0.931;
- oral glucocorticoids 0.966.

Protopathic prescribing would bias same-year estimates *upwards*. Inverse same-year estimates therefore indicate trend confounding rather than protopathic bias. Please say so, because it supports the authors' interpretation.

### M4. Birthplace, age, social risk: Partly

**Done:**
- An age- and birthplace-stratified expected effect is added (0.29% vs 0.34%).
- The Nguipdop-Djomo misuse is removed.
- "UK-born TB is heterogeneous" is stated.
- The regional birthplace limitation is stated.

**Declined, with reasonable justification:** social-risk covariates and ethnicity-by-birthplace analysis.

**Still problematic:**
- **The UK-born trend statements are wrong** (see new issue N1).
- **The ≥65 denominator mismatch** (all residents aged ≥65 as the denominator for UK-born TB at ≥65) is only implied by "UK-born population denominators by age are not published regionally". State the mismatch explicitly in the regional Methods or the limitations, and say that it can create trend confounding as the older non-UK-born population grows.
- **The Davidson 2018 citation does not fit the claim.** Davidson is cited for UK-born TB including "disease in UK-born children of migrant families". According to PubMed, Davidson et al. found that clustering was associated with being UK-born, male, pulmonary disease, previous TB, drug misuse and imprisonment ([doi:10.1093/aje/kwy119](https://doi.org/10.1093/aje/kwy119)). It supports the social-risk and transmission component, not the children-of-migrants component. Cite UKHSA ethnicity-by-birthplace data for the latter, or remove it.

### M5. Pre-entry screening, LTBI programme, migration: Partly

**Done:**
- The LTBI programme is mapped from CCGs to local authorities (63 UTLAs and 83 LTLAs ever active; I confirmed 63 in `ltbi_programme_utla.csv`) and used as a sensitivity covariate.
- The asylum-support sensitivity analysis is in Table S1.
- Pre-entry screening is mentioned in the Introduction.

**Remaining:**
- **The covariate is not constructed as described in the response.**
  - `ltbi_active` stays at 1 through the April–October 2020 pause.
  - `ltbi_tests_per_1000` for 2019/20 is carried forward unchanged to 2025.
  - The manuscript describes only the active-area indicator.
  - Please state the carry-forward, and either model the 2020 pause or state that it was not modelled.
- **The programme itself is never described.**
  - What the text should say: introduced 2015/16; primary care based; migrants aged 16–35 from high-incidence countries who entered within the previous 5 years; about 55 areas; paused 2020.
  - The references to use: Berrocal-Almanza 2022 and Loutet 2018 are in the reference list but cited nowhere in the text.
  - Why it matters: the programme targets young recent entrants, so any effect on notifications would appear in non-UK-born adults aged 15–44. Adjusting all-TB models for an area indicator is a weak control for it. Say this.
- **Pre-entry screening appears only in the Introduction.** It is not in the Discussion or the limitations. Given that outcomes start in 2014 and *t*−1 exposure goes back to 2013, a single sentence in the limitations is enough.

### M6. COVID-19: Partly

**Done:**
- Outcome and exposure years 2020–21 are excluded in a primary care sensitivity analysis.
- The caveat that the 2020 fall reflects disruption is added, with Morrison 2023 cited.

**Not in the manuscript, although the response says it is:**
- **RECOVERY is not cited in the text.** It is in the reference list only.
- **COVID-era hospital glucocorticoids are not discussed.** The words "COVID" and "dexamethasone" appear nowhere in the hospital sections.

**Hospital glucocorticoids need a COVID sensitivity analysis.** Hospital systemic glucocorticoids include dexamethasone (`build_scmd_classification.py`), and the *t*−1 exposure for outcome years 2021–22 is 2020–21 prescribing, which was dominated by COVID-19. The results files already contain a "*t*−1, excluding outcome years 2020–21" model for systemic glucocorticoids, with point estimates about 1.03–1.04. That model is not reported. Please:
- report it;
- ideally report a version excluding dexamethasone;
- add two sentences on hospital dexamethasone for hypoxic COVID-19 as a severity marker patterned by deprivation and ethnicity.

**Not done:** discussion of whether the post-2021 rebound was geographically differential.

### M7. Screening before biologics: Partly

**Done:**
- A Discussion paragraph cites BTS 2005, Carmona 2005 and Gómez-Reino 2007.
- A screening-attenuated scenario is added.
- The Dixon 2010 misuse is removed from the text.

**Problems:**
- **NICE NG33 is not cited in the text**, although the response says it is. It is in the reference list only.
- **The "about 78%" reduction is attributed to both Carmona 2005 and Gómez-Reino 2007.** According to PubMed, the 78% reduction (IRR 0.22, 95% CI 0.03–0.88) comes from Carmona et al. ([doi:10.1002/art.21043](https://doi.org/10.1002/art.21043)). Gómez-Reino et al. report a 7-fold higher risk when recommendations were not followed (IRR 7.09) ([doi:10.1002/art.22768](https://doi.org/10.1002/art.22768)). Attribute each figure to its own source.
- **The derivation and sourcing of the relative risks** are covered in new issue N2.

### M8. Surveillance benchmark: Addressed

The benchmark appears in the Abstract, Table 2 footnote and Discussion:
- 30 steroid-associated cases of 5,490, giving 0.055% per 10%;
- 54 biologic-associated cases, giving 0.098% per 10%.

The arithmetic is correct. The aggregate UKHSA data request is recommended in the Implications.

**Minor:**
- Note that UKHSA's "biological therapy" category includes non-TNF biologics.
- Note that the counts are for a single year (2024).

### M9. Implications for TB programmes: Addressed

The following are now present and well put:
- the null results do not mean these drugs are safe;
- NTBS immunosuppression fields (drug class, time since start, whether LTBI screening was done and treated);
- audit of screening as the practical lever;
- realistic data routes in the Box, with CPRD–NTBS linkage correctly described as bespoke.

"Linked validly" is gone.

### M10. Alternative data: Partly (acceptable)

**Done:** the UKHSA aggregate extract is recommended, and the reason 2025 local authority data were not used is stated.

**Neither done nor discussed:**
- a sensitivity outcome restricted to culture-confirmed pulmonary TB;
- a note on why drug-resistance outcomes were not pursued.

One sentence covering both would suffice.

---

## 3. Status of round 1 minor comments and factual corrections

**Minor comments**

| # | Status | Comment |
|---|---|---|
| 1 | Addressed | |
| 2 | Addressed | The cross-section now uses the same period |
| 3 | Addressed | Residence apportionment is now primary |
| 4 | Addressed | |
| 5 | Addressed | |
| 6 | Addressed as a limitation | |
| 7 | Partly | Elective catchments are used; specialist centres are listed as a limitation |
| 8 | No longer applicable | |
| 9 | Addressed | |
| 10 | Partly | Mechanisms for the failed falsification tests are discussed only generically; migration-driven registration and vitamin D in South Asian-born populations are not named |
| 11 | Not addressed | Metformin: no statement on diabetes prevalence among South Asian-born people with high LTBI prevalence |
| 12 | Addressed | Wording removed |
| 13 | Addressed | |
| 14 | Addressed | Randomisation inference |
| 15 | Not addressed | Extra items may go to existing users rather than new users; this is absent from the listed assumptions |
| 16 | Partly | Pre-entry screening is absent from the limitations |
| 17 | Partly | Table numbers are given in the Methods, but the Data availability section lacks publication and extract dates |
| 18 | Addressed | |
| 19 | Addressed | |
| 20 | Addressed | |

**Factual and referencing corrections**

| # | Status | Comment |
|---|---|---|
| 1 | Addressed | 5,490 in 2024; 5,424 in 2025 with 2024 revised to 5,487. But see N1 on 81.5% |
| 2 | Partly | Citations updated, but Thomas 2018 is now misrepresented (N1) |
| 3 | **Not addressed** | Now misdated (N1) |
| 4 | Addressed in the text | Nguipdop-Djomo still sits uncited in the reference list |
| 5 | Addressed | |
| 6 | Partly | Dixon removed from the text, but RR 4 for TNF inhibitors is now unsourced (N2) |
| 7 | Addressed | |
| 8 | Addressed | |
| 9 | **Not addressed** | RECOVERY is still uncited |
| 10 | **Not addressed** | The LTBI programme is not described |
| 11 | Addressed | Introduction only |
| 12 | Addressed | |

---

## 4. New major issues

### N1. UK TB epidemiology statements are still inaccurate or misattributed

**(a) Thomas 2018 is misrepresented.**
- **What the manuscript says (Introduction):** the 2011–2018 decline "was largely explained by fewer recent migrants from high-incidence countries and by pre-entry screening [Thomas 2018; Aldridge 2016]".
- **What the paper found:** according to PubMed, Thomas et al. covered 2011–2015, not 2011–2018. They attributed 61.9% of the fall in notifications to *decreases in TB rates* in almost all populations, 33.4% to fewer recent or mid-term non-EU migrants, and 11.4% to pre-entry screening ([doi:10.1136/thoraxjnl-2017-211074](https://doi.org/10.1136/thoraxjnl-2017-211074)).
- **Aldridge 2016** is a cohort of migrants screened before entry. It does not quantify the contribution of screening to the national decline ([doi:10.1016/S0140-6736(16)31008-X](https://doi.org/10.1016/S0140-6736(16)31008-X)).
- **Suggested wording:** "Notifications fell by 44% between 2011 and 2018; for 2011–2015, most of the fall reflected declining TB rates across populations, with smaller contributions from fewer recent non-EU migrants and from pre-entry screening [Thomas 2018]."
- **Check the size of the fall.** "Almost half" should be checked against the published national series. My LTLA sums give 8,373 → 4,665, a fall of 44%.

**(b) The UK-born decline is misdated.**
- **What the manuscript says (Introduction and Discussion):** "UK-born notifications fell by 43% between 2014 and 2022".
- **What the data show** (the authors' `region_tb_birthplace_annual.csv`, from Supplementary Table 12): 1,756 (2014), 916 (2022), 995 (2024). That is a **48%** fall from 2014 to the 2022 low, and 43% from 2014 to 2024.
- **Regional variation:** the 2024/2014 ratio ranges from 0.38 (North East) to 0.75 (East of England).
- **Suggested wording:** "fell by 48% between 2014 and 2022 (43% by 2024), with regional falls of 25–62%".

**(c) The drivers of the UK-born decline are still asserted without support.**
- **What the Discussion says:** the UK-born fall "reflect[s] social risk factors, transmission and demographic change [Davidson 2018; UKHSA 2025]".
- **Why this is a problem:** Davidson 2018 shows declining clustering in 2010–2015. It does not establish the causes of the 2014–2022 fall. I raised this in round 1 (item 5.3).
- **Suggested wording:** "coincided with declining strain-typing clustering [Davidson 2018]", and drop "reflecting".

**(d) The share of people born outside the UK needs checking.**
- **What the manuscript says:** "81.5%" of 2024 notifications were in people born outside the UK (Introduction and Results).
- **What the data show:** 4,489 / (4,489 + 995) = **81.9%**, which matches the 2025 report figure I cited in round 1. The 2025 news release gave 81.6% for *2025*.
- **Action:** use the figure for the year and release stated.

**(e) The 2014 figure needs a source.** The Results give "6,474 in 2014", but UTLA and LTLA sums give 6,565 and 6,548. Cite the release that gives 6,474.

### N2. The screening-attenuated relative risk for TNF inhibitors: sourcing and derivation

**Sourcing.** Table S3 uses "RR 4 (unscreened)", but no source is given now that Dixon 2010 has been removed. Please cite a comparison with *unexposed* patients, for example the pre-recommendation BIOBADASER vs EMECAR contrast of 6.2-fold in Carmona 2005, or another registry, and state the comparator.

**Derivation.** "RR 1.7 (~78% reduction)" is obtained by reducing the *excess* risk by 78%: (4 − 1) × 0.22 + 1 ≈ 1.66. Carmona's IRR 0.22 applies to the *rate* in treated patients. Applied that way, it would give 4 × 0.22 ≈ 0.9. Carmona also reports that after screening, the rate in RA patients on TNF antagonists fell to the rate in untreated RA patients (IRR 1.0).

**Why it matters for the paper.** The screening-era RR relative to comparable non-users is plausibly close to 1. RR 1.7 is therefore a *conservative* (detection-favouring) choice. The authors should say this, because it strengthens their conclusion.

### N3. Using the positive-control elasticity as a general attenuation factor

Reporting the elasticity is an improvement. Applying 0.36 to every hospital drug class (the last column of Table S3) assumes those classes share the positive control's sources of error. They do not.

**Error specific to the positive control.** Pyrazinamide and ethambutol volume per person is not proportional to cases. Sources of variation include:
- extended regimens for CNS, bone and spinal TB;
- ethambutol stopped once drug sensitivity is known;
- drug-resistant regimens;
- body-weight dosing;
- cases notified late in the year whose intensive phase falls in the next year (limited, because the *t*+1 estimate is null).

Some of the 0.36 is therefore variation in drug per case, not linkage error.

**Error specific to other drugs, not captured by the positive control:**
- homecare delivery of biologics, which the authors could not verify;
- concentration of transplant and specialist biologic services in particular centres;
- biosimilar switching.

These may make attenuation *larger* for candidate drugs.

**Action:** present the elasticity-attenuated ratios as illustrative, and add two sentences on these differences.

Separately, note in the Results that rifamycin/isoniazid products had the same elasticity (0.37). Latent TB and non-TB rifampicin use therefore did not measurably dilute the within-area signal. This is informative and currently only described as "behaved similarly".

### N4. Changes promised in the response letter are not in the manuscript; uncited references

Searching the main text (lines 1–773) finds no mention of:
- RECOVERY;
- NICE NG33;
- Berrocal-Almanza 2022;
- Loutet 2018;
- Dixon 2010;
- Nguipdop-Djomo 2020;
- FP10(HP).

The response states that RECOVERY, NG33 and FP10(HP) were added, and that COVID-era hospital glucocorticoids and the LTBI programme are discussed. Please:
- add the promised text, or remove the claims from the response;
- delete uncited references;
- remove the reference-verification notes ("Corrections made relative to references_v3.md", "Could not be fully verified", bracketed notes within entries) from the submitted manuscript;
- check the NICE NG33 wording by hand before citing it (the authors flag it as unverified).

---

## 5. Minor issues

**TB epidemiology and interpretation**

1. **Oral glucocorticoids rarely trigger screening (Discussion).** Add a source, or qualify it: "LTBI screening is not routinely undertaken before oral glucocorticoids in UK practice, although guidance recommends considering it for prolonged high-dose therapy". Check against NG33.
2. **Uncited clinical claims.**
   - *"Drug-associated TB is serious, often extrapulmonary"* (Implications): cite Keane 2001, where 40 of 70 cases were extrapulmonary.
   - *"Baseline TB incidence in older UK-born adults is about 2–5 per 100,000 person-years"* (Box): cite the UKHSA table. The all-age UK-born rate in 2024 was 2.1 per 100,000.
3. **UK-born regional finding.** The interpretation (implausible magnitude above the 1.10 ceiling; failed falsification and negative-control tests) is sound and clearly argued. Two additions would help:
   - **Small counts.** Some regional UK-born counts are small (North East: 16 in 2022, 30 in 2024), and LFS denominators carry sampling error. Both inflate year-to-year noise, which Figure 6 makes visible.
   - **Shared downward trends.** Say explicitly that Figure 6 shows a small decline in prescribing alongside a much steeper decline in UK-born TB. Any two declining series will correlate regionally, and London (the steepest fall in UK-born TB and in prednisolone mg) may be influential. A leave-one-region-out check (at least for London) would be cheap.
4. **Metformin (round 1 minor 11).** Add one sentence: the inverse or null estimates should be read against the high diabetes and LTBI prevalence in South Asian-born populations. Diabetes is itself a TB risk factor [Pealing 2015].
5. **Expected-effect assumptions.** Add a fourth assumption: extra prescribing reaches new users rather than lengthening existing courses. The Results already show mg per item falling from 225 to 192, so this matters.
6. **Inputs to the expected-effect calculation.** For Table 2, state:
   - that Brassard 2011's ICS RR of 1.27 is for "any use", and that the Castellana 2019 pooled OR is 1.46;
   - that the PPI OR of 1.28 is for *recent* use in a Korean case-control study;
   - that the metformin RR of 0.51 is within people with diabetes, and is applied here to whole-population prevalence.

   These are acceptable as detection-favouring inputs, but the table should say where they come from.
7. **Recorded-benchmark range.** "Even allowing for under-recording, that implies 0.05–0.1%." State the completeness assumption behind the upper bound (for example, 50% recording).

**Surveillance, data and presentation**

8. **Limitations: pre-entry screening.** Add it and the 2020 LTBI programme pause.
9. **Data availability.** Name the specific UKHSA tables with publication and last-updated dates (the 2025 report was updated 15 July 2026). UKHSA revises figures between releases, as the 5,490 → 5,487 revision shows.
10. **Figure 5 title.** Change "151 upper-tier authorities" to the analysed number.
11. **Figure 6 caption.** It uses LFS denominators; say that the ≥65 regional model uses a different, all-resident denominator.
12. **Table 3 wording.** "Following year (joint with previous)" for the positive control should carry the note that for anti-TB drugs a lead association is expected (treatment continues). For candidate drugs it acts as the falsification test.
13. **Glucocorticoid tables.** Hospital dexamethasone should be reported separately or excluded (see M6).
14. **Language.** "Cases" is still used for people in places. Keep "cases" for surveillance counts and "people with TB" for individuals.

---

## 6. Summary for the editor

The revision responds seriously to my main clinical concerns. The disease-specific positive control, *t*−1 timing, the recorded-case benchmark and the discussion of screening before biologics all make the paper considerably more credible to TB readers.

Remaining problems are mostly text and accuracy corrections:
- misstatements of the 2011–2018 decline (Thomas 2018) and of the UK-born trend (48% to 2022, not 43%);
- an unsourced RR, and an excess-risk derivation, in the TNF screening scenario;
- over-generalisation of the positive-control elasticity;
- several changes promised in the response but absent from the manuscript (RECOVERY, NG33, FP10(HP), LTBI programme description, COVID-era hospital glucocorticoids);
- undisclosed construction details of the LTBI covariate (2020 pause not modelled, test rates carried forward).

I would not need to see the manuscript again if these are corrected and checked by the editor.
