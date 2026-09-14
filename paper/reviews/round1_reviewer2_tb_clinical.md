# Peer review, round 1: Reviewer 2 (TB clinical and public health epidemiology)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB incidence in England" (Draft 2, 14 September 2026)

**Reviewer expertise:** TB physician and public health epidemiologist; UK TB surveillance (ETS/NTBS), migrant and latent TB infection (LTBI) screening, TB in UK-born and inclusion health populations, and NHS TB service delivery.

---

## 1. Summary

The authors link three sets of open data: practice-level primary care prescribing (EPD, 2014–2024), trust-level hospital medicines use (SCMD, 2019–2024, apportioned to local authorities by acute trust catchment) and UKHSA annual TB notifications by upper- and lower-tier local authority. They also use regional TB notifications by place of birth and age. They fit cross-sectional negative binomial models, Poisson fixed-effects panels with lagged and lead exposures, and regional models of UK-born TB, and they calculate minimum detectable effects (MDEs) analytically and by simulation. Hospital antituberculosis drug volume tracks TB notifications between and within areas; the authors treat this as a positive control. No candidate drug group shows a credible association. The authors conclude that the linkage is valid but that ecological designs are 1–2 orders of magnitude too insensitive to detect plausible population effects of medicines on TB.

## 2. Overall assessment and recommendation

**Recommendation: major revision.**

This is a transparent, carefully conducted and honestly reported study. It pre-specifies negative controls and falsification tests, publishes its code, and quantifies power rather than over-reading null results. The central message is useful to TB programmes and to the growing number of groups mining OpenPrescribing-type data: ecological prescribing–TB analyses in a low-incidence country cannot answer causal questions about medicines. I expect the main conclusion to survive revision, and several points below would strengthen it.

My concerns come mostly from TB clinical practice and surveillance rather than statistics:

1. **The positive control validates less than claimed.** The hospital antituberculosis drug group mixes active TB treatment with LTBI treatment and non-TB rifampicin use. Its within-area slope (about 0.2 on the log–log scale) shows substantial attenuation, not a clean validation.
2. **The lag windows do not match what is known about when drug-associated TB appears.** Most such TB is diagnosed within months of exposure.
3. **Several important time-varying drivers of TB notifications in England are not handled or not discussed.** These are pre-entry screening, the LTBI programme, recent-entrant migration and asylum, social risk factors, COVID-19 disruption, and the ETS-to-NTBS transition.
4. **Mandatory LTBI screening before biologics is absent from the Discussion.** It is a major reason why population effects of these drugs should be even smaller than the authors' calculations imply.
5. **UKHSA already publishes the number of TB notifications with recorded biologic or steroid immunosuppression.** This gives a direct empirical benchmark for the expected population effect that the authors have not used.
6. **Some statements about UK TB epidemiology are inaccurate or poorly referenced** (Section 5).

The outcome is notifications, not incidence, and the title and abstract should say so. The manuscript would fit IJTLD or ERJ Open Research well once framed as a methods and feasibility paper with explicit implications for TB surveillance.

---

## 3. Major comments

### M1. The outcome is TB notifications, not incidence, and case definition, residence assignment and timing need describing

**Problem.**
- The title, abstract and results refer to "TB incidence", but the data are UKHSA surveillance notifications.
- The Methods do not describe the surveillance system: ETS until 2021, NTBS thereafter. The UKHSA methodology notes state that NTBS replaced ETS and the London TB Register in 2021, with data from 2018 onwards migrated in July–December 2021.
- Nor do they describe:
  - the case definition (culture-confirmed and clinically diagnosed cases);
  - how cases are assigned to a local authority (residential postcode at notification, and the handling of people with no fixed abode, in prison or in asylum accommodation);
  - which date defines the notification year;
  - the extract date and denominators.
- The authors' own notes (tb_data_sources.md) show that LTLA sums in the regional workbooks exceed national totals (2024: 5,539 vs 5,490). This points to a different extract or residence-assignment rule, and is not mentioned in the manuscript.
- Local authority boundaries were reorganised during 2019–2023 (for example Dorset, Buckinghamshire, Northamptonshire, Cumbria, North Yorkshire and Somerset). The manuscript does not say how counts for 2001–2024 were harmonised (294 LTLAs in the source vs 292 analysed).

**Why it matters.**
- Delay from symptom onset to treatment is often several months. Diagnostic intensity, TB service capacity and the pandemic all shift the calendar year in which a case is notified.
- A migration of the surveillance system during the panel period could produce area-specific step changes in counts or residence coding that year fixed effects will not absorb.
- These issues bear directly on the lag structure (M3) and on the COVID-19 period (M6).

**Requests.**
- Use "TB notification rate" throughout, including the title. Add a short "TB surveillance data" paragraph covering the case definition, residence assignment, year definition, extract date, ETS→NTBS transition and the LTLA-vs-national discrepancy.
- Describe the LA harmonisation and state how many area-years had zero counts.
- Add a sensitivity analysis restricted to outcome years 2018–2024 (NTBS-migrated data only), or include an indicator for the transition interacted with region.

### M2. What the hospital antituberculosis positive control does and does not validate

**Problem 1: the drug group is not specific to active TB.** It is built from rifampicin, isoniazid, pyrazinamide, ethambutol, Rifinah, Rifater, Voractiv, rifapentine, bedaquiline and delamanid, quantified as rifampicin DDD (fetch_scmd.py). The product breakdown (data/raw/scmd/scmd_products_by_group.csv) shows three things:
- **Rifampicin monotherapy capsules are a large share of volume** (about 14.3 million 300 mg and 5.7 million 150 mg). In hospitals, rifampicin monotherapy is also used for staphylococcal bone, joint, prosthetic and endovascular infection, and occasionally for other indications such as cholestatic pruritus and hidradenitis.
- **Rifampicin–isoniazid combinations (Rifinah) and isoniazid alone are also used for LTBI.** This includes 3 months of rifampicin–isoniazid or 6 months of isoniazid for contacts, for migrants in the LTBI programme, and for patients screened before biologics.
- **Only rifampicin milligrams enter the DDD metric.** LTBI-programme activity, which varied by area and year (introduced 2015/16, paused April–October 2020), and pre-biologic LTBI treatment therefore both feed into the "positive control".

The last point creates a direct mechanical link between the positive control and anti-TNF/JAK volume: areas starting more biologics also treat more LTBI.

**Problem 2: the within-area slope shows marked attenuation.**
- If active-TB drug volume were proportional to cases, the within-area elasticity should be about 1, i.e. an IRR of about 1.10 per 10% increase.
- The observed IRR is 1.019 per 10%, an elasticity of about 0.2.
- So even for a near-deterministic relationship, the within-area exposure measure recovers only about a fifth of the true association. Plausible reasons are catchment apportionment error, stock issues rather than patient-level supply, bulk ordering, cross-trust referral of TB and MDR-TB care, and dilution by LTBI and non-TB use.

**Why it matters.**
- The Abstract and Discussion present the positive control as showing the linkage "can detect a real signal" and is "valid".
- What it actually shows is that a very large signal survives, heavily attenuated.
- If similar exposure measurement error affects the biologic and corticosteroid groups, the "null and precise" hospital estimates (Table 3) are precise only on the scale of a mismeasured exposure. On the true-exposure scale the MDE would be several-fold larger. This strengthens the paper's overall conclusion but contradicts the statement that "Hospital data made exposure measurement more complete and more precise (MDE about 1.5% per 10%)".
- The between-area Spearman ρ of 0.74 is largely driven by where TB services and TB burden are concentrated (London and other urban catchments). Many hospital-issued products would correlate with TB between areas for the same reason.

**Requests (all feasible with data already in hand).**
1. **Redefine the positive control around active-TB-specific products:** pyrazinamide and its fixed-dose combinations (Rifater, Voractiv), which are used only in the intensive phase of active TB treatment, plus ethambutol. Report pyrazinamide-containing products separately from rifampicin/isoniazid products, and from rifampicin monotherapy as a "mixed-indication" group. Pyrazinamide also has the tightest timing: about 2 months from treatment start, so it should load on the same year.
2. **Report the within-area elasticity explicitly** and interpret it as an attenuation factor. Show how the hospital MDEs change once rescaled by it.
3. **Add a hospital negative-control exposure** with similar between-area geography but no TB link (for example a high-volume oncology supportive or anti-epileptic product) to show the positive control is specific within areas.
4. **Reframe primary care "antituberculosis" prescribing** (BNF 5.1.9) as an invalid positive control rather than a pre-specified one that "did not track". TB treatment in England is delivered almost entirely through specialist TB services. Community-dispensed items in this BNF section are mostly non-TB uses and occasional prophylaxis. The cross-sectional adjusted estimate for this group was in fact inverse (0.89, 0.79–1.00).
5. **Describe how TB drugs actually reach patients in England**: hospital TB clinic dispensing, outsourced outpatient pharmacies, FP10(HP) prescriptions dispensed in the community, and specialist MDR-TB centres. The SCMD release guidance lists "GP Prescriptions – accounted for in other data sources" among its exclusions. Please check whether any hospital-issued FP10(HP) prescriptions fall outside both SCMD and the practice-restricted EPD extract (setting RO76).

### M3. Lag windows do not match the timing of drug-associated TB

**Problem.**
- Drug-associated TB is predominantly early progression or reactivation of existing infection, and manifests within months.
  - In the FDA MedWatch series of TB after infliximab, the median time to TB was 12 weeks, and 48 of 70 cases developed after three or fewer infusions (Keane et al., *N Engl J Med* 2001;345:1098–104, doi:10.1056/NEJMoa011110).
  - The glucocorticoid risk the authors use (Jick 2006, OR 4.9) applies to *current* use.
- The primary care panel instead uses mean prescribing in years *t*−3 to *t*−1 and excludes year *t*. The hospital panel treats *t*−1 as "the causally ordered exposure".
- Year *t* has a counter-problem. Protopathic prescribing means oral corticosteroids for undiagnosed respiratory symptoms (labelled COPD or asthma exacerbation) and antibacterials or fluoroquinolones given during diagnostic delay are *consequences* of prodromal TB, and fall in the same or preceding months.
- Corticosteroids are also part of TB treatment: adjunctive dexamethasone or prednisolone for TB meningitis and pericarditis (Thwaites et al., *N Engl J Med* 2004;351:1741–51, doi:10.1056/NEJMoa040573). These are counted in hospital "systemic corticosteroids" in the same year.

**Why it matters.**
- The 3-year averaged lag dilutes most of the plausible causal window.
- A concurrent-year association would not be interpretable as causal in either direction.
- The same protopathic bias probably inflates the individual-level OR used for the expected-effect calculation, because Jick's current-use estimate cannot fully exclude prescribing for early TB symptoms.

**Requests.**
- State the biological timing explicitly in the Methods, with references.
- Replace the single 3-year window with separate year *t* and *t*−1 terms, or an unconstrained distributed lag (*t*, *t*−1, *t*−2), and interpret year *t* as mixing a causal effect with reverse causation.
- For primary care corticosteroids, consider a maintenance-use proxy less affected by short protopathic courses, such as 1 mg and 2.5 mg prednisolone tablets or long-duration quantities.
- For hospital corticosteroids, note the TB-treatment use, and ideally exclude dexamethasone or report it separately.
- Discuss protopathic bias in the individual-level RRs used for Table 2.

### M4. Place of birth, recent entry, age and social risk factors

**Problem 1: the stratification is only partly aligned with how UK TB behaves.**
- **Non-UK-born TB (81.9% of 2024 notifications) is increasingly recent-entrant disease.** In 2024, 41.1% of non-UK-born people with TB were notified within 5 years of entry, up from 31.3% in 2021 (UKHSA, *TB in England 2025*, chapter 1).
  - Recent-entrant TB is driven by arrivals, pre-entry screening coverage and asylum routes, not by local prescribing. Drug-associated TB in migrants is reactivation of long-established infection in people already settled and in care.
- **UK-born TB is not migration-free.** It includes UK-born children and grandchildren of migrants from high-incidence countries, with household exposure and travel. It is also concentrated in people with social risk factors. In 2024, 15.3% of people aged 15 and over with TB had at least one social risk factor (homelessness 6.3%, asylum seeker 5.7%, drug use 4.5%), with higher proportions in UK-born people.
  - Reference [22] (small-area deprivation, 2008–2012) does not support the claim that UK-born TB is "less influenced by migration".
- **In the regional UK-born ≥65 analysis, the denominator is the whole population aged 65+**, which includes a growing non-UK-born older population. The numerator is UK-born TB, and the exposure is all-resident prescribing. This mismatch in the rate can itself create trend confounding.
- **The expected-effect formula assumes risk is uniform across the population.** In England, baseline risk differs about 20-fold by place of birth (2024 notification rates 46.9 vs 2.1 per 100,000; UKHSA 2025). Corticosteroid and other immunosuppressant use is concentrated in older UK-born people with low LTBI prevalence. The population effect of a 10% rise in use is therefore smaller than the homogeneous calculation implies, because exposure is concentrated where baseline risk is lowest.

**Problem 2: social risk factors are listed as unmeasured, yet some data are in hand.** The authors have downloaded homelessness, opiate/crack use, drug treatment and prison data (additional_data_sources.md, section C), and *TB in England 2025* Supplementary Table 22 gives social risk factors by region, 2018–2024.

**Requests.**
- Recompute the expected population effects allowing for different baseline TB rates by place of birth and age. For example, apply RR × exposure prevalence within UK-born and non-UK-born strata weighted by their notification rates, using any published age-specific steroid prevalence. Report this as the primary expected effect.
- Use UK-born population denominators (LFS/APS, as in Supplementary Table 12) for UK-born ≥65 rates, or ONS population by country of birth and age where available.
- Add time-varying social-risk covariates at UTLA level (opiate/crack use prevalence, statutory homelessness) as sensitivity analyses. Use Supplementary Table 22 in the regional models.
- Correct the justification for the UK-born analysis and cite appropriately (see Section 5). Acknowledge that "UK-born" is a heterogeneous stratum; if possible, use ethnicity-by-birthplace data (Supplementary Table 18) at least descriptively.

### M5. Pre-entry screening, the LTBI programme and migration flows as time-varying confounders

**Problem.** Area-level TB trends in England over 2011–2024 were shaped by three programme and migration factors.
- **Pre-entry screening.** From 2012, chest radiograph screening was extended to visa applicants staying more than 6 months from high-incidence countries (see Aldridge et al. [2], cohort screened 2006–2013). This policy is not mentioned in the manuscript, yet it matters now that the primary care panel is being extended back to 2011.
- **The primary care-based LTBI testing and treatment programme for new migrants.** It started in 2015/16 in high-incidence CCGs and covered about 55 areas (Berrocal-Almanza et al., *Lancet Public Health* 2022;7:e305–15, doi:10.1016/S2468-2667(22)00031-7). Its timing was staggered (8 CCGs first active in 2015/16, 19 in 2016/17, and so on; additional_data_sources.md), and it was paused April–October 2020. Berrocal-Almanza found testing brought diagnosis forward in the first 6 months (HR 9.93) and reduced TB thereafter (HR 0.57). That is exactly the kind of staggered, area-specific shift in notification timing that two-way fixed effects cannot absorb.
- **Changing arrival routes.** Asylum and irregular arrivals are not covered by pre-entry screening. Asylum support placements, including contingency hotels, changed sharply by LA in 2022–23.

The Limitations state that LTBI programme data "end in 2019/20 and are unmatched to local authority codes". Yet the authors hold CCG-level test counts for 2015/16–2019/20, which can be mapped to LAs with ONS CCG-to-LAD lookups.

**Why it matters.** These programmes also change prescribing:
- LTBI treatment adds to rifampicin and isoniazid volume (M2).
- New GP registrations change practice-based prescribing per resident.
- Migrant-population growth changes the denominator for all drugs.

The failed falsification tests (future vitamin D prescribing and past TB; future oral corticosteroids and past non-UK-born TB) are what one would expect if migration-driven population change affects both series.

**Requests.**
- Map LTBI programme activity to LAs. Include (a) a programme-active indicator by first active year and (b) tests per 100,000 as time-varying covariates in 2015–2019. Model 2020 as a pause.
- Describe pre-entry screening in the Introduction and Discussion. For the extended 2011–2024 panel, include a post-2012 × baseline-share-of-recent-entrants interaction, or at least discuss it.
- Report the asylum support sensitivity analysis in a supplementary table rather than a single sentence.

### M6. COVID-19 effects on notifications, prescribing and the hospital panel

**Problem.**
- **2020 notifications fell sharply and are unlikely to reflect true incidence.** England notifications fell from 4,725 in 2019 to 4,125 in 2020, the largest annual decline in 11 years, which UKHSA judged unlikely to reflect a true reduction in TB (*TB in England 2021 report*). Contributing factors were:
  - service disruption (Morrison et al., *J Infect* 2023;87:59–61, doi:10.1016/j.jinf.2023.04.004);
  - delayed presentation;
  - reduced migration;
  - the LTBI programme pause.
- **Delayed diagnoses carry cases into 2021–22, unevenly by area.**
- **Prescribing was also disrupted:**
  - fewer primary care antibacterial prescriptions;
  - changes in asthma/COPD management;
  - from June 2020, hospital dexamethasone for hypoxic COVID-19 (RECOVERY [35], listed in the references but never cited).

Hospital "systemic corticosteroids" in 2020–22 is therefore largely a COVID-19 severity marker, patterned by deprivation and ethnicity, which are themselves TB risk markers.

**Why it matters.**
- The whole hospital panel (2019–2024) has only one pre-pandemic year.
- In the primary care panel, "exclusion of 2020–21" drops those *outcome* years. But exposures for outcomes in 2022–2024 (windows *t*−3 to *t*−1) still include 2020–21 prescribing.
- Year fixed effects absorb the national shock, not area-differential shocks (London and other high-incidence urban areas were affected earliest and most).

**Requests.**
- Additionally exclude exposure years 2020–21, or add area-specific COVID-19 intensity (for example 2020–21 COVID-19 mortality rate) × year interactions.
- For hospital corticosteroids, exclude dexamethasone or restrict to 2019 and 2022–2024 as a sensitivity analysis.
- Cite RECOVERY where relevant, or remove it from the references.
- Discuss the rebound after 2021 and whether it was geographically differential.

### M7. LTBI screening before biologics and JAK inhibitors: an important omission from the Discussion

**Problem.**
- The expected effects for anti-TNF biologics use RR 4–15 from reference [32] (Dixon et al.). That paper compares anti-TNF agents with each other (infliximab and adalimumab vs etanercept), not with unexposed patients, so it cannot supply that range as stated.
- More importantly, the Discussion does not mention that in the UK, candidates for anti-TNF therapy have been assessed for LTBI and treated since the BTS recommendations of 2005 (BTS Joint Tuberculosis Committee, *Thorax* 2005;60:800–5, doi:10.1136/thx.2005.046797). NICE NG33 also recommends LTBI testing (IGRA, with or without Mantoux) for immunocompromised adults, with treatment if positive. Pre-treatment screening is standard for JAK inhibitors and other biologics.
- Screening works:
  - In the Spanish BIOBADASER registry, active TB rates in patients on TNF antagonists fell by 78% after official LTBI recommendations (IRR 0.22, 95% CI 0.03–0.88; Carmona et al., *Arthritis Rheum* 2005;52:1766–72, doi:10.1002/art.21043).
  - TB risk was about 7 times higher when recommendations were not followed (IRR 7.09; Gómez-Reino et al., *Arthritis Rheum* 2007;57:756–61, doi:10.1002/art.22768).
- Recent growth in biologic volume (+64% for anti-TNF over 2019–2024) has occurred under routine screening. Much of it probably followed biosimilar-driven expansion to broader, lower-risk populations.

**Why it matters.**
- In 2019–2024, the RR that applies to a *marginal* increase in screened biologic use is probably well below historical, pre-screening estimates. Expected population effects are smaller still.
- This is a key substantive reason, beyond statistical power, why the null hospital findings are expected. TB programme readers will look for it.
- The contrast is informative: oral corticosteroids generally do not trigger LTBI screening in practice. Residual drug-associated TB is therefore more plausible for steroids than for biologics.

**Requests.**
- Add a Discussion paragraph on pre-treatment LTBI screening and its effectiveness, citing BTS 2005, NICE NG33, Carmona 2005 and Gómez-Reino 2007.
- Revise the anti-TNF expected-effect assumptions:
  - use an RR against unexposed or screened patients, with a verified source;
  - show a scenario with a screening-attenuated RR (for example, a 70–80% reduction);
  - state explicitly that screening makes the ecological signal even less detectable.
- Correct the use of reference [32].

### M8. Use the surveillance-recorded immunosuppression data as a direct benchmark

**Problem.**
- NTBS records clinical risk factors, including immunosuppression and its cause. *TB in England 2025* (chapter 1) reports that in 2024, 344 of 5,490 people with TB reported immunosuppression: 90 cancer, **54 biological therapy**, **30 steroids**, and 156 other or not specified.
- The expected-effect calculations rely entirely on literature RR × prevalence. For oral corticosteroids that gives a population attributable fraction of 3.4%, which implies about 180 steroid-attributable cases a year.
- Recorded steroid-associated TB is about 30 cases a year (about 0.5%), and biologic-associated TB about 54 (about 1%).

**Why it matters.**
- Even allowing for incomplete recording, these counts give an empirical upper bound on the numerator the ecological design is trying to detect.
- About 54 biologic-associated cases a year across 149 UTLAs is about 0.36 per area-year. A 10% change in biologic use would plausibly change the national total by about 5 cases.
- This makes the authors' argument more concrete and more persuasive to TB readers. It also suggests the Table 2 expected effect for oral corticosteroids may be *overstated*, which strengthens rather than weakens the conclusions.

**Requests.**
- Add these national counts (and trends from earlier reports, if available) to the Discussion as a triangulating benchmark, with caveats about completeness of the risk-factor field.
- Consider a supplementary "surveillance-based expected effect": recorded drug-associated cases × (10% change) ÷ total notifications.
- As a feasible data request, ask UKHSA for aggregate counts of TB with recorded biological therapy or steroid immunosuppression by region (or UTLA) and year, with small-number suppression. That outcome is causally specific. Even an ecological association with hospital biologic volume could be informative, and it would be a much better "drug-relevant" outcome than all-cause notifications.

### M9. Conclusions and implications for TB programmes

**Problem.** The Implications section is written for data scientists ("causal questions need individual-level linked data"). It says little about what TB programmes should take from the study, and it risks implying that medicine-associated TB is unimportant.

**Requests.**
- State clearly that the null population-level findings do *not* mean that steroids, biologics or JAK inhibitors are unimportant for individual patients or TB services. Drug-associated TB is clinically serious, often extrapulmonary or disseminated (40 of 70 in Keane 2001), and largely preventable through screening.
- Give implications specific to TB programmes:
  - Surveillance of drug-associated TB is better served by improving completeness and granularity of NTBS immunosuppression fields (named drug class, time since start, whether LTBI screening was done and treated) than by ecological prescribing analyses.
  - Auditing LTBI screening before biologics, JAK inhibitors and high-dose, long-term corticosteroids is the actionable lever.
- Soften "linked validly" to reflect M2, for example "linked with detectable but heavily attenuated signal".
- On individual-level data, name realistic UK routes:
  - CPRD Aurum/GOLD with HES linkage (TB identified from GP and hospital coding, as in Pealing et al. [39]);
  - UKHSA NTBS extracts through the UKHSA data access process;
  - biologics registers (BSRBR-RA, BADBIR) linked to TB surveillance.
- Avoid implying that CPRD–ETS linkage is a standard product. The authors' notes say they could not find one.

### M10. Alternative and additional data

Beyond M4, M5 and M8, the following are feasible:
1. **UKHSA aggregate extract** of TB notifications by UTLA × year × place of birth (UK/non-UK) × broad age × time since entry (<5 years, ≥5 years), with suppression. It would allow LA-level analysis of UK-born and settled-migrant TB, which are the strata where drug-associated reactivation is relevant. Recent-entrant TB, which is dominated by migration, could be excluded.
2. **Culture-confirmed pulmonary TB only** (published by UKHSA at LA level as 3-year aggregates and in the official statistics), as a sensitivity outcome less affected by diagnostic intensity.
3. **Drug-resistance data.** Fluoroquinolone prescribing and fluoroquinolone-resistant or isoniazid-resistant TB is mechanistically more direct. However, numbers are very small and most resistance in England is acquired abroad, so I would only suggest a brief descriptive note on why this was not pursued.
4. **The 2025 notification data now available** (see Section 5) could extend the outcome series by one year.

---

## 4. Minor comments

1. **Title, thesis line and abstract.** Replace "TB incidence" with "TB notifications" or "TB notification rates" (M1). "Lower-tier oral corticosteroids" in the abstract is ambiguous; write "oral corticosteroids (lower-tier authorities)".
2. **Methods, EPD.** "The cross-sectional analysis used June 2026" conflicts with "January 2014–December 2024" and with Sub-ICB TB counts for 2022–24. Please clarify which prescribing period the cross-sectional analysis used and why it does not align with the outcome period.
3. **Practice-to-area assignment.** Assigning practice prescribing to the LA containing the practice postcode misallocates cross-boundary registrants, more so at LTLA level. NHS Digital publishes quarterly "Patients registered at a GP practice" by LSOA, which would allow apportionment by where registered patients live. This would at least serve as a sensitivity analysis.
4. **Prednisolone dose.** Tablets × strength ignores soluble and enteric-coated formulations and other glucocorticoids. State what proportion of oral corticosteroid items the prednisolone-mg metric covers and how dexamethasone, hydrocortisone and methylprednisolone were handled.
5. **Hospital quantities.** "Approximate milligrams" sums drugs of very different potency (for example infliximab mg vs adalimumab mg; hydrocortisone vs dexamethasone). Log within-area changes partly offset this, but switches between agents, biosimilar transitions and changing dose conventions will create spurious within-area change. Consider DDD-based or cost-based sensitivity analyses. The authors mention indicative cost in code but not in the paper.
6. **Homecare.** The SCMD release guidance lists its excluded categories (breakages, disposals, expired stock, general sales, stock adjustments, GP prescriptions, private patients, internal transfers). It does not explicitly mention homecare, and I could not find a definitive statement either. Please ask NHSBSA directly, or triangulate SCMD adalimumab volume against national biosimilar uptake figures, rather than leaving this unverified.
7. **Specialist centres.** Transplant, rheumatology and MDR-TB centres serve patients far beyond their admission catchments. Consider excluding specialist trusts, or apportioning by outpatient rather than all-admissions catchments where available.
8. **Table 1.** The positive control's adjusted cross-sectional estimate is 0.89 (0.79–1.00), i.e. inverse. Comment on this.
9. **Table 3 labels.** Label columns as "t (same year)", "t−1 (exposure precedes outcome)" and "t+1 (exposure follows outcome)". "Following-year use … consistent with treatment continuing" is correct for antituberculosis drugs but acts as the falsification test for the other groups. Make this explicit.
10. **Falsification failures.** Discuss plausible mechanisms for future vitamin D and future oral corticosteroid prescribing being associated with past TB: growth in migrant populations and new GP registrations, and vitamin D testing and supplementation in South Asian-born populations. Currently they are simply reported as failures.
11. **Metformin.** The crude positive association (1.24) almost certainly reflects diabetes prevalence in South Asian-born populations, which carry both high LTBI prevalence and high diabetes prevalence. Say so; diabetes is itself a TB risk factor.
12. **"Mostly reactivation disease" in UK-born people aged 65 and over.** This is clinically plausible but needs a citation, for example strain-typing clustering data by age.
13. **Regional analyses.** "7 of 90 were nominally significant, against 4.5 expected" should state that the 90 tests are highly correlated, so the binomial expectation is only indicative.
14. **Nine-cluster inference.** Consider a wild cluster bootstrap (Webb weights) as well as *t*(8) critical values.
15. **Expected-effect formula.** It assumes that additional prescribing reaches new users with the same RR. In practice, a 10% rise in items often reflects longer courses or more items per existing user. State this, and note that it would further reduce the expected effect.
16. **Limitations.** Add:
    - the ETS→NTBS transition;
    - residence-based numerators with practice-location exposure;
    - pre-entry screening;
    - dilution of the positive control by LTBI treatment;
    - LTBI screening before biologics (M7).
17. **Data availability.** List the specific UKHSA tables used (regional workbook table numbers; *TB in England 2025* Supplementary Tables 5, 12 and 22) and their extract or publication dates, because UKHSA revises figures between releases.
18. **Draft note on the reference list.** Reference titles for [2–4, 14–19, 22, 30, 33, 34, 37, 38] are flagged as abbreviated; see Section 5 for specific problems.
19. **Primary care panel extension to 2011.** When extending, note that it will span the 2012 pre-entry screening expansion, the 2013 PCT→CCG reorganisation, and the 2013–2015 PHE/NHS England changes to TB control boards. Pre-2013 PDPI data use PCT codes, so practice mapping needs care.
20. **Language.** Use "people with TB" rather than "TB patients" or "cases" where referring to individuals, in line with UKHSA and Stop TB Partnership language guidance.

---

## 5. Factual errors and referencing problems concerning UK TB epidemiology and data sources

1. **National figures need updating and sourcing to a stated release** (Introduction, para 1).
   - The manuscript says notifications "rose by 13% in 2024 to 5,480". The current *TB in England 2025* report (chapter 1, as updated on gov.uk) gives **5,490 notifications in 2024 (9.4 per 100,000), a 13.5–13.6% increase on 4,831 in 2023**, described as the largest annual increase since national surveillance began. Earlier releases gave 5,480 and 13.0%.
   - UKHSA has also published 2025 data: **5,424 notifications in 2025 (9.4 per 100,000), a 1.1% decrease from 5,487 in 2024**, with 81.6% in people born outside the UK (UKHSA news release, "Tuberculosis notifications in England stabilise in 2025", 29 January 2026).
   - For a manuscript dated September 2026, cite the most recent release, state the extract, and ideally add 2025 as an outcome year.
   - The "low of 4,125 in 2020" matches the *TB in England 2021 report*. It should carry UKHSA's caveat that the 2020 fall was unlikely to reflect a true reduction in TB.
2. **"Recent national trends have been driven largely by migration and screening policy [3,4]."**
   - Reference [4] (Crofts et al., 2008) predates the period discussed.
   - Thomas et al. [3] addresses the 2011–2016 decline.
   - UKHSA attributes the 2023–2024 rise to increased migration from higher-incidence countries and COVID-19-related disruption of TB care globally, with a growing share of recent entrants (41.1% within 5 years of entry in 2024) [1].
   - Please update the citations and distinguish the decline (2011–2018) from the rise (2021–2024).
3. **"UK-born TB roughly halved in most regions over the decade, driven by social risk factors, transmission and demographic change [22,34]."**
   - From *TB in England 2025* Supplementary Table 12, UK-born notifications in England fell from 1,756 (2014) to a nadir of 916 (2022) and rose to 995 (2024): a 43% decline over the decade, with a recent upturn. UKHSA notes that the 2024 increase in the UK-born rate was only the second year-on-year rise since 2012.
   - Regional 2024/2014 ratios range from 0.38 (North East) to 0.75 (East of England). "Fell by 25–62%, with a nadir in 2022" is more accurate than "roughly halved in most regions".
   - Neither cited reference shows what *drove* the decade's decline. [22] is a 2008–2012 cross-sectional deprivation analysis; [34] is a 2010–2015 strain-typing study of transmission.
4. **Reference [22] is cited for UK-born and older people's TB being "less influenced by migration"** (Introduction). Nguipdop-Djomo et al. (*PLoS One* 2020;15:e0240879, doi:10.1371/journal.pone.0240879) is an ecological analysis of small-area deprivation and TB, 2008–2012. It does not address this claim.
5. **Reference [34] title is wrong.** Davidson et al., *Am J Epidemiol* 2018;187:2233–42 (doi:10.1093/aje/kwy119) is titled "Understanding Tuberculosis Transmission in the United Kingdom: Findings From 6 Years of Mycobacterial Interspersed Repetitive Unit-Variable Number Tandem Repeats Strain Typing, 2010–2015", not "Risk factors for recent transmission of tuberculosis in England".
6. **Reference [32] (Dixon et al. 2010) does not provide an RR against non-users.** Its IRRs compare infliximab and adalimumab with etanercept, and all 40 TB cases were in the anti-TNF cohort. The "RR 4–15" in Table 3 and the claim that "anti-TNF biologics carry large increases [32]" need a correct source for the comparison with unexposed patients, and a note on screening-era estimates (M7).
7. **Reference [37] (Kumwichar et al., TB after COVID-19 pneumonia in Thailand) is cited for "diagnostic intensity"** as an unmeasured confounder in England. It does not support this; please replace or remove.
8. **Reference [33] (Ruzangi et al., chronic kidney disease and TB) is cited for drug-associated TB risk differing by ethnicity.** Please check. If the intended point is that TB risk factors differ by ethnicity in UK primary care data, say so; otherwise use a more appropriate source.
9. **Reference [35] (RECOVERY) is listed but not cited in the text.**
10. **The LTBI programme is incompletely described.** It began in 2015/16 as a primary care-based programme for migrants aged 16–35 from high-incidence countries who had entered within 5 years, in high-incidence areas (about 55 areas; Berrocal-Almanza et al. [36]). It was paused April–October 2020. The statement that area-level data are "unmatched to local authority codes" reflects a mapping task, not a data gap (M5).
11. **Pre-entry screening is not mentioned.** UK pre-entry TB screening for visa applicants from high-incidence countries staying more than 6 months was extended nationally in 2012 (UK Border Agency announcement, May 2012; phased country roll-out from mid-2012). This should appear in the Introduction and Discussion, especially for the extended 2011–2024 panel.
12. **Surveillance system naming.** The manuscript never names ETS or NTBS. NTBS replaced ETS and the London TB Register in 2021, with 2018-onwards data migrated (UKHSA *TB in England* methodology). This should be stated (M1).

---

### References verified by the reviewer for the above suggestions

- Keane J, et al. Tuberculosis associated with infliximab, a tumor necrosis factor alpha-neutralizing agent. *N Engl J Med* 2001;345:1098–104. PMID 11596589; doi:10.1056/NEJMoa011110.
- BTS Joint Tuberculosis Committee. BTS recommendations for assessing risk and for managing *Mycobacterium tuberculosis* infection and disease in patients due to start anti-TNF-alpha treatment. *Thorax* 2005;60:800–5. PMID 16055611; doi:10.1136/thx.2005.046797.
- Carmona L, et al. Effectiveness of recommendations to prevent reactivation of latent tuberculosis infection in patients treated with tumor necrosis factor antagonists. *Arthritis Rheum* 2005;52:1766–72. PMID 15934089; doi:10.1002/art.21043.
- Gómez-Reino JJ, Carmona L, Angel Descalzo M. Risk of tuberculosis in patients treated with tumor necrosis factor antagonists due to incomplete prevention of reactivation of latent infection. *Arthritis Rheum* 2007;57:756–61. PMID 17530674; doi:10.1002/art.22768.
- Thwaites GE, et al. Dexamethasone for the treatment of tuberculous meningitis in adolescents and adults. *N Engl J Med* 2004;351:1741–51. PMID 15496623; doi:10.1056/NEJMoa040573.
- Berrocal-Almanza LC, et al. Effectiveness of nationwide programmatic testing and treatment for latent tuberculosis infection in migrants in England: a retrospective, population-based cohort study. *Lancet Public Health* 2022;7:e305–15. PMID 35338849; doi:10.1016/S2468-2667(22)00031-7.
- Loutet MG, et al. National roll-out of latent tuberculosis testing and treatment for new migrants in England: a retrospective evaluation in a high-incidence area. *Eur Respir J* 2018;51:1701226. PMID 29326327; doi:10.1183/13993003.01226-2017.
- Morrison H, et al. Impact of COVID-19 on NHS tuberculosis services: results of a UK-wide survey. *J Infect* 2023;87:59–61. PMID 37044162; doi:10.1016/j.jinf.2023.04.004.
- Nguipdop-Djomo P, et al. Small-area level socio-economic deprivation and tuberculosis rates in England: an ecological analysis of tuberculosis notifications between 2008 and 2012. *PLoS One* 2020;15:e0240879. PMID 33075092.
- Davidson JA, et al. Understanding tuberculosis transmission in the United Kingdom: findings from 6 years of MIRU-VNTR strain typing, 2010–2015. *Am J Epidemiol* 2018;187:2233–42. PMID 29878041.
- UK Health Security Agency. Tuberculosis in England: 2025 report, chapter 1 (incidence and epidemiology, 2024) and Supplementary Tables 12 and 22. gov.uk.
- UK Health Security Agency. Tuberculosis notifications in England stabilise in 2025. News release, 29 January 2026. gov.uk.
- Public Health England. Tuberculosis in England 2021 report (presenting data to end of 2020). gov.uk.
- NHSBSA. Secondary Care Medicines Data release guidance (data exclusions section).
- NICE. Tuberculosis (NG33), recommendations on testing for latent TB in immunocompromised people. *The NICE page returned HTTP 403 to automated retrieval, so the wording was confirmed from secondary summaries only. Please check against the current NG33 text.*
