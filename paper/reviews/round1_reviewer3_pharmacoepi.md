# Peer review, round 1: Reviewer 3 (pharmacoepidemiology and prescribing data)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB incidence in England" (Draft 2, 14 September 2026)

**Journal:** Pharmacoepidemiology and Drug Safety

**Reviewer expertise:** English prescribing data (NHSBSA EPD, NHS Digital PDPI, OpenPrescribing, SCMD), drug exposure measurement, hospital trust catchments, target trial emulation in CPRD/HES.

**Materials examined:** the manuscript; the code (`build_dataset.py`, `fetch_prescribing_panel.py`, `fetch_steroids.py`, `fetch_pre2014_practice.py`, `fetch_scmd.py`, `summarise_scmd.py`, `hospital_medicines.py`, `build_panel.py`, `build_trust_catchment.py`, `analyze_panel*.py`, `mde.py`, `plot_hospital.py`, `simulate_power.py`, `steroid_*.py`); `data/processed/drug_group_substances.csv`; `data/raw/scmd/scmd_products_by_group.csv`; `data/raw/scmd/scmd_trust_month_vmp.csv.gz`; `data/raw/scmd/scmd_trust_month_group_summary.csv`; `data/raw/scmd/trust_catchment_la.csv`; `data/raw/epd_202606_pco_substance.csv.gz`; the monthly practice extracts; outputs; and `paper/revision_notes.md`. Where I quote numbers not in the manuscript, I computed them from the project's own files. The calculations are described so the authors can reproduce them. I have not modified any project file. I understand the primary-care panel estimates will be updated when the pre-2014 data are added. My comments on the primary-care panel therefore concern design and measurement, not the specific point estimates.

---

## 1. Summary

The authors link openly published English prescribing data to UKHSA TB notifications to ask whether ecological designs can detect effects of medicines on TB.

**Exposures:**
- **Primary care:** 12 BNF-defined drug groups from the NHSBSA English Prescribing Dataset (EPD), 2014–2024. Items are assigned to local authorities by practice postcode and expressed per 1,000 residents.
- **Hospital:** six drug groups from Secondary Care Medicines Data (SCMD), 2019–2024, apportioned to local authorities with 2024 OHID all-admissions trust catchment shares.

**Designs:**
- cross-sectional negative binomial models at Sub-ICB level;
- Poisson fixed-effects panels at UTLA and LTLA level, with lagged, concurrent and lead exposures;
- regional analyses by place of birth;
- analytic and simulation-based minimum detectable effects (MDEs).

**Findings:**
- Hospital antituberculosis drug use (the positive control) tracks TB between and within areas.
- No drug group of interest is associated with TB.
- MDEs exceed the population effects implied by published relative risks by one to two orders of magnitude.

The authors conclude that open data can be linked validly but cannot detect plausible medicine effects on TB, and that individual-level linked data are needed.

## 2. Overall assessment and recommendation

**Recommendation: major revision.**

The central message is sensible and, I suspect, robust: ecological analyses of rare outcomes with small population attributable fractions are grossly underpowered. It is useful to demonstrate this with open English data, a positive control and explicit MDEs. The code is unusually transparent. The product-level SCMD audit file is exactly the kind of artefact reviewers should be given, and it made this review possible. The MDE framework and the plasmode simulation are appropriate and clearly explained.

However, exposure measurement is the core of a paper whose thesis is "the data cannot detect the effect". It currently has several problems, some of which bias the headline positive-control and MDE results.

1. **Drug group definitions.** Several hospital groups are not pharmacologically coherent or TB-relevant, and their "approximate mg" quantities are dominated by one or two products with high milligram doses. Examples:
   - Filgotinib is 60% of JAK-inhibitor mg but about 10% of patient-years.
   - Mycophenolate is 93% of the calcineurin/antiproliferative group mg.
   - Hydrocortisone, methylprednisolone and dexamethasone mg are summed without potency conversion.
   - Intra-articular depot methylprednisolone is counted as systemic.

   The primary-care "oral corticosteroids" group (BNF 6.3.2) includes hydrocortisone replacement therapy, injectables and betamethasone soluble tablets, about 11% of items.
2. **The positive control is weaker and more ambiguous than presented.** The within-area elasticity is about 0.20 (IRR 1.019 per 10%), when a pure TB-treatment measure should have an elasticity near 1. The rifampicin DDD measure omits fixed-dose combinations (about 10% of rifampicin). It also includes substantial non-TB and latent TB infection (LTBI) rifampicin use. Rather than simply validating the linkage, the positive control quantifies roughly five-fold dilution. That dilution should be carried into the MDE argument.
3. **Hospital catchment apportionment has a time-varying coverage artefact.** Share of hospital quantity from trusts with 2024 catchment data rises from about 90% in 2019 to 99% in 2024. The cause is that predecessor trust ODS codes do not match the 2024 catchments. This creates spurious within-area increases in exposure in areas served by merged trusts, and the manuscript's pooled "96–99%" figure hides it. Standard errors are clustered by local authority, but hospital exposure varies at trust level, so precision (and therefore the hospital MDEs) is probably overstated.
4. **Items per resident, assigned by practice postcode, is a noisy and time-inconsistent measure of prevalence of use.** Changes in prescription duration, COVID-19, practice list movements (e.g. GP at Hand, a sevenfold rise in items at a single SW6 practice) and the planned PDPI–EPD splice all affect it. Better alternatives exist in the same open data: quantity or ADQ/DDD measures, and list-based apportionment by patient LSOA.
5. **Some inputs to the MDE calculation are not well matched to the exposure measured.** Examples are prevalence of use for hospital systemic corticosteroids and for anti-TNF therapy, the RR for transplant immunosuppressants, and the assumed elasticity of 1 between items and users.
6. **Several reproducibility problems.** Stale SCMD audit files do not match the current code, and `summarise_scmd.py` fails on them. There is no code path for the LTLA MDE table (Table 2). The manuscript's description of denominators contradicts `build_dataset.py`.

None of these is likely to overturn the qualitative conclusion. Most of them, if corrected, would widen the gap between expected and detectable effects. But several quantitative statements in the abstract depend on them, as does the claim that the linkage is "valid": the 13-fold JAK rise, "MDE 0.9–2.1%" for hospital drugs, "trusts with catchment data accounted for 96–99%", and the positive control. The Implications section should also give more concrete guidance on individual-level designs, which is where a PDS readership would benefit most. I give specific, feasible requests below. Most require re-running existing code with modified group definitions rather than new data acquisition.

---

## 3. Major comments

### M1. Primary-care drug group definitions: oral corticosteroids, immunosuppressants and the topical exclusion

**Problem.** `build_dataset.DRUG_GROUPS` defines groups at BNF chemical-substance level (9 characters), used by `fetch_prescribing_panel.py` and `fetch_pre2014_practice.py`. From `drug_group_substances.csv` (June 2026):

- **"Oral corticosteroids" (`^0603020`) is not oral glucocorticoid therapy at immunosuppressive doses.** Of 526,586 items:
  - hydrocortisone accounts for 48,448 (9.2%), overwhelmingly adrenal/pituitary replacement at physiological doses;
  - injectables account for 3,876: hydrocortisone sodium succinate (mostly emergency adrenal-crisis kits), dexamethasone phosphate / sodium phosphate, hydrocortisone sodium phosphate and methylprednisolone sodium succinate;
  - betamethasone sodium phosphate accounts for 5,352, largely soluble tablets used as a mouthwash for oral ulceration;
  - dexamethasone accounts for 16,090 (3.1%), predominantly palliative, oncology and antiemetic use, plus COVID-19 treatment in 2020–21.

  In total, about 11% of "OCS" items are not systemic immunosuppressive glucocorticoids. This is not trivial when the within-area SD of the log rate is 0.07.
- **"Immunosuppressants" is a name-regex group.** It includes methotrexate from both BNF 10.1.3 and 8.1.3 (oncology, 3,268 items), azathioprine, mycophenolate, leflunomide, tacrolimus, ciclosporin and sirolimus. It omits mercaptopurine (0801030L0; 3,921 items in June 2026, a thiopurine used in IBD) and cyclophosphamide. In primary care, prescribing of tacrolimus, mycophenolate and ciclosporin under shared care varies geographically, so between- and within-area variation partly reflects local shared-care agreements rather than patient numbers. Transplant immunosuppression has a very different TB relative risk (roughly 20-fold or more in low-incidence settings) from conventional DMARDs in RA (the RR 1.2 used in Table 2).
- **The topical exclusion (BNF chapters 11–13) works at substance level** (e.g. tacrolimus 1305030C0, ciclosporin eye drops 1104020AE). But it cannot separate forms within 0603020 or 0802. Rectal and oral-topical corticosteroids sit in chapter 1 (0105020, 0107020) and are correctly not captured.
- **Inhaled corticosteroids (`^0302000`)** correctly include ICS/LABA and triple combinations. A 20-fold dose range across molecules and devices is ignored.
- **Vitamin D:** I checked that calcium/colecalciferol combinations are captured under 0906040G0 in the June 2026 file. The authors should confirm this holds in the 2014–2019 and PDPI BNF versions.

**Why it matters.** Any OCS signal would be diluted. More importantly, hydrocortisone replacement and palliative dexamethasone have different area-level and temporal determinants (endocrine services, hospice provision, COVID) from immunosuppressive prednisolone. The group-level MDEs are then attached to an RR (Jick 2006, current oral glucocorticoid use) that applies to only part of the group.

**Requests.**
1. Redefine the primary exposure at BNF presentation level (15-character code or `BNF_DESCRIPTION`) as oral prednisolone, prednisone, methylprednisolone, deflazacort and dexamethasone solid/liquid forms. Exclude hydrocortisone, injectables and betamethasone soluble tablets. Show hydrocortisone and dexamethasone separately as sensitivity exposures. Present prednisolone-equivalent mg per 1,000 residents as a co-primary measure, since the authors already derive prednisolone mg in `fetch_steroids.py` (see M4).
2. Split "immunosuppressants" into (a) conventional DMARDs (methotrexate 10.1.3, leflunomide, azathioprine, mercaptopurine) and (b) transplant agents (tacrolimus, ciclosporin, mycophenolate, sirolimus, everolimus). Assign separate RR and prevalence inputs. Exclude oncology methotrexate (8.1.3).
3. Publish a complete presentation-level listing for every group, analogous to `scmd_products_by_group.csv`, for at least three time points (e.g. January 2011 PDPI, January 2014 EPD, December 2024). This lets readers verify continuity across BNF code changes.

### M2. Hospital drug group definitions, product classification and the "approximate mg" measure

**Problem.** The SCMD audit file is excellent, but it reveals that the "approx_mg" quantity is not a meaningful common unit within most groups. National kg by substance (2019–2024, from `scmd_trust_month_vmp.csv.gz`, excluded products removed, final data preferred over provisional):

| Group | Composition of mg | Issue |
|---|---|---|
| JAK inhibitors | Filgotinib 60% of mg over the whole period (206 of 321 kg in 2024); upadacitinib 21%; baricitinib 4%; tofacitinib 6%; ruxolitinib 9% | A filgotinib patient-year is about 73 g (200 mg/day) and a baricitinib patient-year about 1.5 g (4 mg/day), a 50-fold difference. The "about 13-fold" rise (25 kg in 2019 to 321 kg in 2024) is mainly the uptake of filgotinib and upadacitinib. On WHO DDD patient-year equivalents I estimate about 6,800 in 2019 and about 27,000 in 2024, a roughly 4-fold rise. Ruxolitinib is haematology (myelofibrosis, polycythaemia vera, GVHD), a different population. |
| Anti-TNF | Infliximab 32%, adalimumab 32%, etanercept 24%, certolizumab 10%, golimumab 1% | Annual mg per patient ranges from about 600 mg (golimumab 50 mg monthly) to about 5,200 mg (certolizumab 200 mg every 2 weeks). Subcutaneous infliximab (120 mg every 2 weeks, about 3.1 g/year, first seen 2020-03) replaces IV 5 mg/kg every 8 weeks (about 2.3 g/year). IBD dose escalation (adalimumab weekly, infliximab 10 mg/kg) is increasing. Within-trust changes in mg therefore reflect product mix, route switching and dose intensification, not patient numbers. |
| "Other biologics with TB risk" | Rituximab 34% (mostly haematology/oncology bags and vials), tocilizumab 21%, secukinumab 12%, vedolizumab 11%, abatacept 10%, anakinra 7%, ustekinumab 4%, ixekizumab 1% | Secukinumab, ixekizumab (IL-17), ustekinumab (IL-12/23) and vedolizumab (gut-selective α4β7) have no established TB risk comparable to TNF or IL-6 blockade; together they are about 28% of group mg. Tocilizumab rose in 2021 (71 kg vs 52 kg in 2020) because of COVID-19 treatment. IL-23 inhibitors (guselkumab, risankizumab, tildrakizumab) are absent, which is defensible, but the group label should change. |
| Systemic corticosteroids | Prednisolone 53%, hydrocortisone 22% (IV hydrocortisone sodium succinate 100 mg vials alone 18%), methylprednisolone 17%, dexamethasone 8% | Mg is not potency-adjusted. Dexamethasone is about 6.7 times prednisolone and would become the largest component in prednisolone-equivalents; hydrocortisone is 0.25 times. Methylprednisolone acetate 40 mg/ml suspension (5.1 million ml; about 3.5% of group mg) and methylprednisolone/lidocaine are intra-articular depot preparations, classified as systemic. Monthly dexamethasone shows the COVID-19 surge (e.g. 7.7 kg in January 2021 vs about 4.5 kg pre-pandemic), a within-area shock correlated with COVID admission patterns. |
| Calcineurin inhibitors/antiproliferatives | Mycophenolate mofetil 86% + mycophenolic acid 7%, azathioprine 3%, ciclosporin 3%, methotrexate 0.5%, tacrolimus 0.4% | Effectively a mycophenolate measure. Tacrolimus, the dominant transplant calcineurin inhibitor and the group's largest cost item (£650m), contributes almost nothing to mg. About half of methotrexate mg is high-dose oncology infusion (5 g/50 ml vials). |
| Antituberculosis | Rifampicin DDD derived from products whose name starts "Rifampicin" | "Generic Rifater tablets" (6.6 million) and "Generic Voractiv tablets" (2.8 million) have no parsable strength (`mg_per_unit` = NaN), so their rifampicin (120 mg and 150 mg per tablet) is omitted. This is 9–10% of rifampicin DDD in every year (e.g. 336,000 of 3.23 million in 2024), spread across 172 trusts. See M3. |

The `approx_mg_per_unit` parser itself works correctly for dm+d "X mg/Y ml" names with ML units; I found no unit-conversion errors in the rows checked. Its limitations are:
- it returns the strength of the first-named ingredient only;
- it cannot parse brand-style VMP names;
- it returns NaN for GRAM units (harmless here).

Negative quantities (e.g. −623,990 g of hydrocortisone butyrate ointment, excluded; −30 ml prednisolone injection, included) are SCMD backtracking artefacts. They are harmless at this scale but should be truncated or reported.

**Why it matters.**
- **Hospital MDEs and expected effects:** Table 3 and the "0.9–2.1%" statement assume that a 10% change in the measured quantity corresponds to a 10% change in exposed people. For JAK inhibitors, anti-TNF, "other biologics" and calcineurin/antiproliferatives, most within-area variation in mg comes from product mix, not patients.
- **The JAK result:** the inverse concurrent JAK estimate (0.990, 0.984–0.996), attributed to a "trend artefact", is more specifically a product-mix artefact.
- **Positive control:** the result is attenuated by the omitted fixed-dose combinations.

**Requests.**
1. Replace approx_mg with a **patient-year-equivalent measure** for every hospital group. Use WHO ATC/DDD values where available (e.g. adalimumab 2.9 mg, etanercept 7 mg, infliximab 3.75 mg, certolizumab pegol 14 mg, golimumab 1.66 mg, tofacitinib 10 mg, baricitinib 4 mg, upadacitinib 15 mg, filgotinib 200 mg; verify against the current ATC/DDD index). Where no DDD exists or the DDD is unrepresentative (e.g. rituximab, IV infliximab in IBD), use a documented defined maintenance dose. Provide the substance-to-DDD table as supplementary material.
2. For systemic corticosteroids, use **prednisolone-equivalent mg** (standard conversions, e.g. prednisolone 1, methylprednisolone 1.25, dexamethasone 6.67, hydrocortisone 0.25) and exclude intra-articular and depot suspensions (methylprednisolone acetate, hydrocortisone acetate, and triamcinolone if added). Consider separating IV hydrocortisone and methylprednisolone pulses, which are acute exposures, from oral maintenance.
3. Reconstitute the biologic groups by mechanism with established TB risk:
   - TNF inhibitors;
   - IL-6 pathway inhibitors (tocilizumab, sarilumab) and abatacept;
   - JAK inhibitors, with ruxolitinib shown separately.

   Report B-cell depletion (rituximab) separately, split into haematology and rheumatology if dose and presentation permit. Treat IL-17, IL-12/23 and α4β7 agents as a "low-TB-risk biologic" comparison exposure. That comparison is a useful negative-control exposure measured with the same data-generating process.
4. Split "calcineurin/antiproliferatives" into transplant calcineurin/mTOR inhibitors (tacrolimus, ciclosporin, sirolimus, everolimus) and antiproliferatives (mycophenolate, azathioprine). Exclude oncology high-dose methotrexate (vials ≥ 500 mg or strength ≥ 25 mg/ml in large volumes).
5. Hard-code strengths for fixed-dose combination anti-TB VMPs (Rifater: rifampicin 120 mg / isoniazid 50 mg / pyrazinamide 300 mg; Voractiv: rifampicin 150 mg / isoniazid 75 mg / pyrazinamide 400 mg / ethambutol 275 mg). Re-run the positive control.
6. Report the within-group DDD composition by year, e.g. a supplementary stacked area chart, so readers can see that trends are not product-mix driven.

### M3. The positive control: what it shows and what it does not

**Problem.** The manuscript states that hospital antituberculosis drug use "tracked TB incidence ... as it should" and that "the linkage can therefore detect a real signal".

- **Elasticity.** A within-area IRR of 1.019 per 10% increase corresponds to an elasticity of log(1.019)/log(1.1) = 0.20 (95% CI 0.05–0.35). If rifampicin DDDs measured TB treatment without error, the elasticity would be close to 1. The observed 0.2 implies roughly 80% attenuation.
- **Non-TB rifampicin.** Rifampicin DDD is not a TB-specific measure. About 2.5–2.9 million DDD a year are counted nationally. 4,700–5,500 notified cases a year × about 180 rifampicin DDD per 6-month regimen gives roughly 0.85–1.0 million DDD, perhaps a third of the total. The rest reflects:
  - LTBI treatment (3 months of isoniazid plus rifampicin, including the new-entrant screening programme, which tracks migration rather than disease);
  - non-TB indications (prosthetic joint and bone infection, staphylococcal endocarditis, pruritus in cholestatic liver disease, hidradenitis suppurativa);
  - treatment of cases notified in the previous year.
- **What else is missing.**
  - Isoniazid-only LTBI regimens are excluded.
  - Fixed-dose combinations are omitted (M2).
  - Catchment coverage is time-varying (M5).
  - Hospital-supplied drugs dispensed in community pharmacy (FP10(HP)) are excluded from SCMD by design (SCMD guidance, "Coverage").
- **Timing.** The lead association (t+1: 1.017), with a null lag (t−1: 0.999), is consistent with continuing treatment. It is also consistent with LTBI treatment of contacts identified in year t.
- **Between-area estimate.** The cross-sectional Spearman ρ of 0.74 largely reflects where TB services are located, which correlates strongly with migrant populations. That is the same confounder that defeats the drug analyses.

**Why it matters.** The positive control is used to argue two things: that the nulls are credible, and that the linkage is valid. It does show that the exposure measure is sensitive to large between-area differences and, weakly, to within-area changes. But it quantifies dilution rather than establishing validity. With an elasticity of about 0.2 even for a drug used almost exclusively in the disease, MDEs for drugs of interest should be judged against expected effects that are also attenuated by linkage error. That strengthens the paper's conclusion, but it should be stated.

**Requests.**
1. Report the positive-control elasticity and its CI explicitly. Discuss the sources of attenuation above.
2. Construct a more TB-specific positive control, and report both:
   - treatment-course equivalents (rifampicin DDD from ≥ 2-drug regimens: ethambutol or pyrazinamide DDD, which are almost TB-specific), or
   - ethambutol DDD alone.

   Ethambutol is used mainly in active TB intensive phase (and some non-tuberculous mycobacterial disease). Its within-area elasticity should be closer to 1 if the catchment linkage works.
3. Use the positive-control attenuation factor in the MDE comparison. For example, show expected hospital-drug effects multiplied by the observed positive-control elasticity as a "linkage-attenuated" scenario, or propagate the positive-control misclassification in the plasmode simulation.
4. Tone down "valid linkage" in the abstract and conclusion to "a linkage that can detect large between-area differences and, weakly, within-area changes in a disease-specific drug".

### M4. Items as the exposure measure, and consistency over time

**Problem.** Primary-care exposure is items per 1,000 residents per year. Items are a poor proxy for prevalence of use, and the relationship changes over time and between areas:

- **Prescription duration.** For chronic medicines (levothyroxine, statins, PPIs, metformin, insulins, ICS, conventional DMARDs), items per patient-year depend on local 28- versus 56-day policies and electronic repeat dispensing. These changed differentially across CCGs/ICBs during 2014–2024, and at the start of the COVID-19 pandemic many practices lengthened prescriptions. Area-specific policy changes are not absorbed by year fixed effects. This is a plausible explanation for the negative-control (levothyroxine) and "total prescribing volume" artefacts the authors observe.
- **Acute medicines.** OCS items are dominated by short courses (asthma/COPD exacerbations, seasonal respiratory infections). TB risk is concentrated in the roughly 0.5–1% on long-term or high-dose therapy. The authors' own data show items falling 10% while prednisolone mg fell 21%: courses are shorter or lower-dose and the items-to-dose relationship drifts. Within-area variation in items is therefore driven mainly by acute use, which carries lower TB risk. The effective elasticity of TB-relevant exposure to items is plausibly well below 1.
- **COVID-19.** In 2020–21 OCS and antibacterial items fell sharply, while ICS items rose in 2020 (406 vs 378 per 1,000), consistent with stockpiling. Regional heterogeneity in COVID waves makes these within-area shocks.
- **Prednisolone dose derivation** (`fetch_steroids.PRED_TABLET_MG`) matches only generically described presentations (`^prednisolone Xmg (gastro-resistant |soluble )?tablets`). Dispensing under brand descriptions and oral solutions is excluded. If the branded share changed over time or between areas, the mg series is biased.
- The manuscript states that the ADQ field is "not populated for corticosteroids". ADQ values are populated for most other groups in the EPD (the June 2026 PCO file used by `build_dataset.py` has an `ADQ` column).

**Why it matters.** The fixed-effects panel identifies effects entirely from within-area changes (SD 0.07 on the log scale). If a large part of that variation reflects prescription-length policy, practice list movements (M6) or acute-course patterns unrelated to TB-relevant exposure, the MDEs are attached to the wrong denominator. Non-differential error of this kind biases towards the null and inflates the MDE-to-expected ratio. The design conclusion survives, but the "17-fold" and similar statements are not interpretable without this caveat.

**Requests.**
1. Re-extract **total quantity** and **ADQ usage** (EPD `TOTAL_QUANTITY`, `ADQUSAGE`) at practice-month level. Compute ADQ- or DDD-based exposure per 1,000 residents per day for every group. For groups without ADQ (corticosteroids), use prednisolone-equivalent mg over all oral presentations, with strengths taken from dm+d via the BNF-to-dm+d mapping rather than a name regex.
2. Show national and within-area trends for items, quantity and ADQ/DDD per group on the same figure, marking 2020–21. Report the within-area correlation between the log changes in items and in ADQ.
3. Re-run the primary panel with ADQ/DDD exposure. Report the within-area SD of the exposure under each measure, since it directly determines the MDE.
4. For OCS, add an exposure closer to TB risk: prednisolone-equivalent mg from ≥ 5 mg tablets in quantities ≥ 56 (a proxy for longer courses), or the share of mg from presentations and quantities consistent with long-term use. Be clear that this remains an aggregate proxy.

### M5. SCMD coverage: trust mergers, specialist and unmatched trusts, homecare and provisional data

**Problem.** `hospital_medicines.apportion` keeps only trusts whose ODS code appears in the 2024 catchment table and prints a pooled coverage share. From the project files, coverage by year is:

| Group | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Antituberculosis (rifampicin DDD) | 0.904 | 0.949 | 0.975 | 0.990 | 0.990 | 0.991 |
| Anti-TNF (mg) | 0.909 | 0.951 | 0.976 | 0.985 | 0.986 | 0.989 |
| Systemic corticosteroids (mg) | 0.899 | 0.942 | 0.971 | 0.982 | 0.986 | 0.988 |

(Other groups are similar.) The excluded quantity is mainly from **predecessor trusts** that later merged into trusts present in the 2024 catchment. Their data stop at the merger date, for example:
- RW6 to 2021-09;
- RXH to 2021-03;
- RDZ and RD3 to 2020-09;
- RQ8, RDD, RC1 and RA3 to 2020-03;
- RQ6 and RNL to 2019-09;
- RBZ to 2022-03;
- RA4 and RVY to 2023;
- RT3 to 2021-01.

Successor codes (R0A, R0B, R0D) also have partial series. Separately, some trusts are **never matched**. North Middlesex University Hospital (RAP) is excluded in every year with about 106,000 rifampicin DDD, in one of England's highest-TB areas. Community and mental health trusts (e.g. RRE, RW5, RV3, RYW, R1C) are also unmatched and supply some anti-TB drugs.

Separately:
- The OHID catchment table used has only 2023 and 2024 catchment years; 2024 shares are applied to all years.
- The SCMD guidance notes that trusts may keep reporting under historic ODS codes after merging.
- Provisional SCMD data are subject to backtracking for up to about a year. The pipeline correctly prefers finalised data, but the analysis period's final months should be confirmed as final.
- Homecare: the manuscript says capture "could not be verified". I estimate adalimumab supply at roughly 90,000 patient-year equivalents a year on average, and anti-TNF supply at about 0.35–0.4% of the English population in 2024 (see M9). That is consistent with substantial homecare capture nationally, but completeness may vary by trust and over time.

**Why it matters.** Coverage rising from 90% to 99% is not uniform across areas. It is concentrated in the catchments of merged trusts (Greater Manchester, Sussex, Dorset, mid and south Essex, Somerset, Liverpool, north Cumbria, Bedfordshire, Devon). This produces **artefactual within-area increases** in exposure for these areas in the merger years. Year fixed effects do not remove them. Such increases attenuate the positive control and add noise that looks like precision in MDE terms. Unmatched high-TB trusts such as RAP bias the cross-sectional estimates.

**Requests.**
1. Build an ODS predecessor-successor map (NHS ODS "successor" records, or the NHS England Digital mergers and acquisitions list referenced in the SCMD guidance). Re-assign predecessor quantities to successor catchments before apportionment. Report coverage by group and year in a supplementary table.
2. Map unmatched acute and specialist trusts explicitly. For RAP, use its pre-merger catchment from an earlier OHID release, or its successor's catchment. For specialist trusts (e.g. Royal Brompton / Guy's and St Thomas', The Christie, Royal Marsden, Royal Free transplant and rheumatology services), consider apportioning with elective or outpatient-based shares.
3. Restrict the within-area hospital analysis to area-years with ≥ 98% coverage, or to areas whose principal trusts had no ODS change in 2019–2024, as a sensitivity analysis.
4. Test homecare capture directly. By trust and year, compute the ratio of subcutaneous biologic patient-year equivalents (adalimumab, etanercept, certolizumab, golimumab, SC tocilizumab/abatacept, all typically homecare) to IV infliximab/tocilizumab (day-case). Flag outlier trusts and trust-years with abrupt changes, and exclude them in sensitivity analysis.
5. State which SCMD months are final and which provisional, and the data extraction date.

### M6. Practice-to-area mapping: practice postcode versus patient residence

**Problem.** `build_panel.annual_prescribing` assigns every item to the local authority containing the practice postcode (ONSPD August 2025), and divides by ONS residents. This mismatches numerator and denominator wherever practice lists cross local authority boundaries. That is common at LTLA level in London and other conurbations, and it changes over time with practice mergers, relocations, closures and list growth. The most extreme example is in the authors' own extracts. Practice E85124 (Babylon GP at Hand, postcode SW6 7SX) went from about 1,000–4,500 items a month in 2014–2017 to about 28,000 a month in 2021–2024. Its registrants live across London and beyond, but every item is attributed to Hammersmith & Fulham. Smaller versions of this (practice mergers across a boundary, "super-practices", care-home and homeless practices) are widespread.

**Why it matters.** Postcode-based attribution introduces within-area exposure variation unrelated to residents' drug use, precisely the variation the fixed-effects model exploits. At LTLA level, where the authors report CIs about 20% narrower, the problem is larger. The narrower CIs may partly reflect more measurement noise in exposure rather than more information.

**Requests.**
1. Apportion each practice's monthly items (or ADQs) to LSOAs, and hence to LTLAs and UTLAs, using NHS England's "Patients Registered at a GP Practice" LSOA-level files. These give counts of registered patients by practice and LSOA and are published regularly for much of the study period; the authors should state the earliest release available and interpolate between releases. The project already holds the practice mapping file from this series (`gp-reg-pat-prac-map.csv`) but not the LSOA file.
2. Report the share of each local authority's apportioned items that comes from practices located outside it, and re-run the LTLA panel restricted to areas where this share is below, say, 10%.
3. Consider age-sex standardisation of the numerator using practice list age-sex structure (e.g. STAR-PU or ASTRO-PU weights for the relevant BNF sections). Time-varying adjustment for resident age structure does not correct for age-selective list movements.
4. For the cross-sectional analysis, the PCO/Sub-ICB assignment in `build_dataset.py` is list-based and does not have this problem. It does have the denominator issue in M7.

### M7. Residents versus registered denominators, and the cross-sectional analysis

**Problem.**
- The Methods state that "Denominators were resident populations, which avoids list inflation". But `build_dataset.py` (the Sub-ICB cross-sectional dataset) computes `rate_* = items / registered_patients * 1000`, with registered patients from June 2026, so this analysis *does* use inflated lists.
- The panels use residents in the denominator with practice-postcode numerators (M6), which is a different mismatch.
- In the cross-sectional analysis, exposure (June 2026, a single month) is measured 18–30 months *after* the outcome period (2022–24), acknowledged in `PROGRESS.md` but not in the manuscript. A single June month under-represents seasonal medicines (antibacterials, OCS for exacerbations).
- The TB outcome is apportioned from 2024 to 2026 Sub-ICB boundaries on population weights.

**Why it matters.** List inflation is strongly patterned by mobility, age and migration, the dominant confounders here. It biases the crude cross-sectional associations (the "inverse associations" in the abstract) in exactly the direction observed: high-migration areas have more inflated lists and therefore lower items per registered patient. A single month after the outcome period is also hard to justify.

**Requests.**
1. Correct the Methods text, or re-compute Sub-ICB rates per resident (LSOA-to-Sub-ICB population, as already done for covariates) and report both.
2. Use 12 months of prescribing preceding or covering the outcome window (e.g. January 2021 – December 2023) for the cross-sectional analysis. The extracts already exist in `epd_practice_monthly`.
3. Report list inflation (registered ÷ resident) by area and show that the crude inverse associations attenuate when it is adjusted for or when resident denominators are used.

### M8. Comparability of NHS Digital PDPI (2010–2013) with NHSBSA EPD (2014 onwards)

**Problem.** `fetch_pre2014_practice.py` splices PDPI monthly files into the same directory and format as the EPD extracts. `build_panel.py` then treats them as one series.
- The pipeline appears to have been interrupted: raw `201106.zip` and `T201201*` files remain in `data/raw/pre2014`.
- Comparing the extracted months: PDPI files contain about 10,260 prescribing organisation codes with 72–83 million items a month (2010–2011). EPD January–March 2014 contains about 9,900–9,970 codes with 79–88 million items.
- EPD extraction excludes `PRACTICE_CODE == '-'` and `UNIDENTIFIED` rows; PDPI has no equivalent filter.
- PDPI settings include out-of-hours, walk-in and other non-standard organisations; the RO76 restriction the manuscript mentions is not applied in either series (`gp_only=False` is the default in `annual_prescribing`, and `main()` does not set it).
- BNF chemical-substance names in the PDPI CHEM files may differ from EPD descriptions, which affects the name-regex groups (immunosuppressants, metformin, fluoroquinolones, vitamin D, levothyroxine).
- Practice postcodes from PDPI ADDR files are mapped with ONSPD 2025. Terminated or re-used postcodes should be checked.

Between January 2011 and January 2014, the group ratios differ markedly (PPIs about 1.33, vitamin D about 1.45, levothyroxine about 1.15, all items about 1.08 on the months extracted). Some of this is genuine secular growth. But group-specific discontinuities at the splice cannot be separated from trends without an overlap period.

**Why it matters.** Any level shift at the splice that differs between areas is an artefactual within-area change. For 3-year lagged exposure windows it will contaminate outcome years 2014–2016. Year fixed effects remove only national shifts.

**Requests.**
1. Validate the splice using an overlap period. To my knowledge, NHS Digital continued publishing practice-level prescribing for several years after January 2014, so at least 12 overlapping months can be extracted from both sources through the same `aggregate()` function. Report practice-level and area-level concordance (ratio, correlation, Bland–Altman) by drug group.
2. Apply equivalent practice-setting restrictions in both series (e.g. RO76 standard GP practices, using the historical epraccur file for the pre-2014 period). Report the share of items excluded by year.
3. Add a splice indicator (pre-2014 × area) or restrict windows to one source as a sensitivity analysis. Report whether the primary estimates change.
4. Make `process_month` robust to interruption: use try/finally for clean-up, write output atomically, and log failures.

### M9. Inputs to the MDE and expected-effect calculations

**Problem.** The expected-effect formula is appropriate. Several of its inputs are poorly matched to the measured exposure:

- **Elasticity of users to measured quantity.** The formula assumes prevalence of use scales one-to-one with items or mg. For OCS (M4), anti-TNF and JAK inhibitors (M2), and in view of the positive-control elasticity of 0.2 (M3), this assumption favours detection by an unknown but probably large factor. The authors say the formula "favours detection", which is correct, but the elasticity assumption is not listed among the reasons.
- **OCS prevalence of 0.9%** (van Staa 2000) comes from 1989–1998 GPRD data on adult current use, applied to the whole population. Jick 2006 reports an **odds ratio** (4.9) from a nested case-control study with dose-response (higher at ≥ 15 mg/day). Presenting it as an RR is acceptable given rarity, but it should be labelled as such. A more defensible input is a dose-stratified calculation using recent long-term use prevalence (Fardet 2011: about 0.8% on ≥ 3 months).
- **Hospital systemic corticosteroids** reuse the primary-care OCS inputs (RR 4.9, prevalence 0.9%; `plot_hospital.SCENARIOS`). Hospital supply is mostly inpatient short courses and outpatient initiations, a different population and a different risk. This row of Table 3 is not meaningful as specified.
- **Anti-TNF prevalence of 0.2%** is "illustrative". It can be estimated from the SCMD data. With WHO DDDs, 2024 supply is roughly 108,000 (adalimumab) + 85,000 (infliximab; about 51,000 on label dosing) + 30,000 (etanercept) + 7,000 (certolizumab) + 5,000 (golimumab) patient-year equivalents, about 0.35–0.40% of the English population. JAK inhibitors in 2024 are about 27,000 patient-year equivalents, about 0.05%, consistent with the assumption.
- **Anti-TNF RR in England.** The RR under routine LTBI screening before biologic initiation (NICE and BSR guidance) is lower than historical estimates. Dixon 2010 compares drugs within BSRBR-RA rather than against the general population.
- **Immunosuppressants.** RR 1.2 applies to conventional DMARDs in RA; transplant immunosuppression carries far higher risk (M1).
- **PPI (Korea), statin and metformin RRs** come from high-incidence settings with strong healthy-user or indication confounding. They are acknowledged but should not be presented as "published effects" in the thesis statement without qualification.
- The analytic power calculation uses a one-sided normal approximation; fine.
- The simulation injects the effect into exactly the modelled exposure window with no exposure measurement error, so it is the best case. That is fine but should be stated.

**Why it matters.** The qualitative conclusion is robust to all of these; most corrections make detection harder. But Table 2, Table 3 and the abstract state precise ratios (17-fold, 5–87-fold, "RR above 100"). Those should rest on inputs matched to the exposure measured, with ranges.

**Requests.**
1. Present MDE-to-expected ratios over a grid of prevalence (e.g. 0.5×–2× the base case), RR (published CI limits) and elasticity (0.2, 0.5, 1). Put this in a figure rather than single numbers.
2. Replace the illustrative hospital prevalences with SCMD-derived patient-year equivalents (M2, request 1), with uncertainty from alternative maintenance doses.
3. Remove the hospital systemic corticosteroid expected-effect row, or specify an appropriate scenario (e.g. high-dose pulses: RR ≥ 5, prevalence ≤ 0.05%).
4. Use a dose-stratified OCS scenario (e.g. prevalence 0.3% at ≥ 7.5 mg/day long-term with RR 7–8; 0.5% at lower doses with RR 2–3).
5. In the simulation, add a scenario where true exposure is the "long-term" component of items with elasticity < 1, and a scenario with the positive-control-derived measurement error.

### M10. Catchment apportionment for outpatient-dispensed and specialist-centre medicines, and standard errors

**Problem.**
- **Admission-based shares.** Trust quantities are apportioned with 2024 all-admissions catchment shares. Biologics, JAK inhibitors and transplant immunosuppressants are supplied mainly through outpatient clinics and homecare. Their patient catchments differ from emergency-dominated admission catchments, especially for tertiary centres: transplant (e.g. Royal Free, Guy's, Birmingham, Leeds, Manchester, Newcastle), IBD and paediatric rheumatology services, and regional TB services.
- **Standard errors.** Each local authority's apportioned exposure is a weighted average of a few trust series with weights fixed over time. All within-area variation in hospital exposure therefore comes from trust-level changes shared across all local authorities in the catchment. There are about 134 catchment trusts for 149 UTLAs and 292 LTLAs, so the effective number of independent exposure trajectories is at most the number of trusts, and fewer at LTLA level. Clustering by local authority (`fit_ppml`) ignores this cross-area correlation, so SEs, and hence MDEs of "0.9–2.1%", are probably too small.

**Requests.**
1. Repeat with elective-admission catchments (available in the same OHID table) and report both.
2. Cluster SEs by principal trust (the trust with the largest `prop_of_la_population`), or use two-way clustering (area and principal trust). Alternatively, reverse the apportionment: allocate TB notifications to trusts using `prop_of_la_population` and analyse at trust level (n ≈ 134). That makes the unit of exposure variation the unit of analysis.
3. Report the median and range of the number of trusts contributing more than 10% of each area's exposure.

### M11. Individual-level design: be concrete about what should be done

**Problem.** The Implications say causal questions "need individual-level linked data, for example CPRD ... analysed with target trial emulation", but give no specification. For a PDS readership, and given that the manuscript's contribution is essentially a feasibility and power argument, a concrete design recommendation with feasibility numbers would add substantial value.

**Request.** Add a short, structured specification, for example in a box or table. For oral glucocorticoids, it could look like this:

- **Data:**
  - CPRD Aurum (primary care prescribing with dose and quantity; ethnicity; comorbidity);
  - HES Admitted Patient Care and Outpatients (TB diagnoses, ICD-10 A15–A19; hospital comorbidity);
  - ONS death registration;
  - small-area IMD;
  - a **bespoke linkage to the UKHSA National TB Surveillance System** (NTBS, successor to Enhanced TB Surveillance). This is not a standard CPRD linkage and would need a linkage application. It supplies notification-validated outcomes, site of disease, culture confirmation and, critically, **country of birth and year of UK entry**, which are poorly recorded in CPRD.

  Hospital-only drugs (biologics, JAK inhibitors) are not in CPRD. Options include the NHS England high-cost drugs data available in OpenSAFELY-TPP, or disease registries (BSRBR-RA, BADBIR, the UK IBD Registry) with the same TB linkage.
- **Target trial protocol (OCS):**
  - *Eligibility:* adults ≥ 18 years with ≥ 12 months' registration; no prior TB, TB treatment, LTBI treatment or OCS in the previous 12 months (new users); no HIV, solid organ transplant or current biologic; restricted to a defined indication cohort (e.g. polymyalgia rheumatica/giant cell arteritis, RA, COPD, asthma, IBD) to reduce confounding by indication.
  - *Treatment strategies:* initiate OCS with sustained use ≥ 3 months (by prednisolone-equivalent dose category: < 7.5, 7.5–< 15, ≥ 15 mg/day) versus no OCS initiation, or an active comparator where one exists (e.g. RA: methotrexate without versus with bridging glucocorticoid).
  - *Assignment and time zero:* sequential monthly nested trials, with time zero at the eligible visit or prescription. Clone-censor-weight for sustained-use and dose strategies, to avoid immortal time.
  - *Outcome:* incident active TB, the earliest of NTBS notification, HES A15–A19, or CPRD TB code with treatment; secondary outcomes pulmonary versus extrapulmonary TB, culture-confirmed TB, and TB death.
  - *Follow-up:* from time zero to the earliest of outcome, death, deregistration, end of linkage, or 5 years.
  - *Causal contrasts:* intention-to-treat and per-protocol, with inverse probability of censoring weights for deviation. Estimate 1-, 2- and 5-year cumulative incidence differences and ratios with pooled logistic regression.
  - *Confounders:* age, sex, ethnicity (CPRD + HES), country of birth and time since entry (NTBS/UKHSA or migration codes), IMD, diabetes, CKD, smoking, alcohol, BMI, prior TB contact or LTBI screening codes, indication severity (exacerbation counts, disease activity proxies), healthcare use, and co-prescribed immunosuppressants.
  - *Effect modification:* country of birth (TB incidence in the country of origin) as the pre-specified modifier, since absolute risk differences depend on LTBI prevalence.
  - *Bias checks:* negative-control exposure (e.g. levothyroxine initiation in the same framework); negative-control outcome unaffected by glucocorticoids; E-values.
- **Feasibility arithmetic.** Show a back-of-envelope expected number of TB events. For example: tens of thousands of long-term OCS initiators in CPRD Aurum, × a baseline incidence of about 5–10 per 100,000 person-years in UK-born older adults (much higher in migrants from high-incidence countries), × follow-up. That arithmetic makes the sample-size problem of the individual-level study explicit too. Reference 39 (Pealing 2015) already illustrates it.

---

## 4. Minor comments

1. **Abstract, "Methods: Exposures".** State the exposure measure (items; approximate mg; rifampicin DDD) and the apportionment method in one line each. The Results "positive control" bullet should report the elasticity (M3).
2. **Abstract, "Power".** "RR 4.9" is an odds ratio from a nested case-control study (Jick 2006). Label it "OR (approximating RR)" throughout, including Table 2 and the thesis line.
3. **Pre-specification.** "The exposures, controls and falsification tests were specified in advance" (Strengths). The progress log shows pre-specification within an iterative analysis, and several analyses (LTLA, hospital, UK-born 65+, asylum adjustment) were added after results were seen. Describe these as post hoc, or cite a time-stamped protocol.
4. **Methods, "Primary care prescribing".** "Standard GP practices (RO76) accounted for 98.6% of items" is reported as a data check, but the analysis does not apply the restriction. Say so, or apply it (M8).
5. **Methods, Geography.** Give the ONSPD version, the LAD vintage used for the Fingertips LTLA-to-UTLA mapping, and the treatment of City of London and Isles of Scilly (merged into different neighbours at UTLA and LTLA level; `build_panel.MERGES`).
6. **Numbers of areas.** The hospital log reports 151 UTLA areas and the LTLA panel file 294 areas; the manuscript reports 149 and 292. Explain the exclusions.
7. **Hospital within-area models.** The lag (t−1) analysis uses outcome years 2020–2024 only, dominated by the pandemic and the 2023–24 TB resurgence. Add an exclusion-of-2020–21 sensitivity analysis as for primary care. State that five outcome years with area fixed effects leave little within-area information.
8. **Cost as a sensitivity measure.** Indicative cost is missing for January–March 2019 (retired SCMD files have no cost; the `hospital_medicines.py` docstring mentions cost as a sensitivity measure). Biosimilar entry (adalimumab from late 2018) cut prices by large and trust-varying amounts, so cost is not a valid volume measure over 2019–2024. Drop it or explain.
9. **Table 3.** The "Expected change (assumption)" column mixes scenarios with different justifications. Add a source column, as in Table 2.
10. **Table 2.** Add CIs for MDE (from SE uncertainty), or at least note that the MDE is itself estimated.
11. **UK-born 65+ analysis.** The denominator is all residents aged 65+, not UK-born residents aged 65+ (acknowledged in code). This matters for the falsification failure and should be in the manuscript.
12. **Regional analyses with 9 clusters.** Cluster-robust SEs with t(8) critical values can still be anti-conservative. Consider wild cluster bootstrap p-values, and report them for the prednisolone mg result.
13. **"Spurious inverse associations" with total prescribing adjustment.** This is expected when group items are a component of total items (a compositional ratio). Explain it briefly rather than presenting it as an empirical finding.
14. **Discussion, "Why better data did not solve the problem".** Hospital data did not make exposure "more complete and more precise" in any demonstrated sense (M2, M5, M10). Rephrase.
15. **References.** Reference 35 (RECOVERY) is listed but not cited. It is relevant to the dexamethasone and tocilizumab COVID-19 surges, so cite it in the hospital methods or limitations. Reference 33 (CKD and TB, CPRD) is cited for "Drug-associated TB risk may differ by ethnicity", which it does not appear to support. Several references are flagged by the authors as unchecked.
16. **Figure 1.** Label the y-axis as rifampicin DDD "including non-TB and LTBI use", and show ethambutol DDD as a second panel (M3).
17. **Figure 3.** State that prednisolone mg is from generically described tablet presentations only.
18. **Data availability.** State the extraction dates for EPD, SCMD (final versus provisional) and OHID catchments, and archive the exact extracts (e.g. Zenodo DOI). The NHSBSA portal revises data.
19. **Terminology.** "Defined daily doses" for anti-TB drugs refers to rifampicin DDD only. Say "rifampicin DDD" consistently.
20. **Seasonality.** For the single-month cross-sectional exposure (June), note the seasonal pattern of antibacterials and OCS, or use 12 months (M7).
21. **Limitations.** Add FP10(HP) hospital prescriptions dispensed in community pharmacy. They are in neither SCMD (by definition) nor practice-level EPD rows (they appear under hospital or trust prescriber codes), and they are relevant to OCS and some DMARDs.
22. **Reporting.** Consider RECORD-PE for the individual-level recommendation and a brief GATHER- or STROBE-ecological style checklist for the ecological analysis.

---

## 5. Bugs and inconsistencies in code and data

| # | File / function / line | Issue | Likely impact |
|---|---|---|---|
| B1 | `fetch_scmd.py`, `approx_mg_per_unit` (l. 122–135); `rif_mg` (l. 162) | VMPs named "Generic Rifater tablets" and "Generic Voractiv tablets" have no parsable strength, so `mg_per_unit` = NaN and `rif_mg` = 0. About 9–10% of rifampicin DDD is omitted every year (e.g. about 336,000 DDD in 2024), across 172 trusts; the top five trusts hold 22% of fixed-dose combination supply. | Measurement error in the positive control; biases towards the null and varies between trusts. |
| B2 | `hospital_medicines.py`, `apportion` (l. 57–69) | Inner merge on 2024 catchment trust codes drops predecessor ODS codes. Coverage rises from about 0.90 (2019) to 0.99 (2024); the printed pooled share (0.96–0.99) hides this. North Middlesex (RAP) is never matched. | Artefactual within-area exposure increases in merged-trust catchments; attenuated positive control; biased cross-section in high-TB north London. |
| B3 | `hospital_medicines.py`, `within_area` (l. 118–133), via `analyze_panel.fit_ppml` | SEs clustered by area, but exposure variation is at trust level and shared across areas. | Understated SEs and MDEs for hospital drugs. |
| B4 | `fetch_scmd.py`, `GROUPS` and `EXCL_*` (l. 34–50) | Methylprednisolone acetate (± lidocaine) and hydrocortisone acetate suspensions, which are intra-articular or depot, are classed as systemic corticosteroids. No potency conversion. Ruxolitinib is classed with JAK inhibitors; IL-17, IL-12/23 and α4β7 agents with "biologics with TB risk"; oncology high-dose methotrexate with antiproliferatives. | Group heterogeneity; product-mix-driven trends (e.g. JAK "13-fold" rise, largely filgotinib mg). |
| B5 | `data/raw/scmd/scmd_products_by_group.csv`, `scmd_trust_month_groups.csv`, `scmd_trust_month_group_summary.csv` | The files contain lower-case unit names ("ml", "vial") and `YYYY-MM` month strings for January–March 2019 (retired source). The current `fetch_scmd.main()` upper-cases units and converts months to integers before writing, so the files were produced by an earlier code version. The groups-by-unit file therefore splits ML and ml rows. | Audit files do not correspond to the code; reproducibility. Totals unaffected. |
| B6 | `summarise_scmd.py`, l. 28 (`s["year"] = s.year_month // 100`) and l. 63 (`s.year_month >= 202204`) | Fails with `TypeError` on the current summary file (mixed string and integer `year_month`; confirmed when reading the file with default dtypes). | Descriptive checks cannot be reproduced. |
| B7 | `build_dataset.py`, l. 177 | Cross-sectional rates use `registered_patients` as denominator; the manuscript says residents. Exposure is June 2026, after the 2022–24 outcome. | Methods misreported; list-inflation bias in crude cross-sectional associations. |
| B8 | `build_dataset.py`, `DRUG_GROUPS["oral_corticosteroids"]` (`^0603020`) | Includes hydrocortisone (9.2% of items), injectables, betamethasone sodium phosphate soluble tablets and dexamethasone. | Dilution and confounding by non-immunosuppressive use (M1). |
| B9 | `build_dataset.py`, `DRUG_GROUPS["immunosuppressants"]` | Omits mercaptopurine; includes oncology methotrexate (0801030P0); mixes conventional DMARDs with transplant agents (one RR used). | Misspecified expected effect. |
| B10 | `build_panel.py`, `annual_prescribing(lad_area, gp_only=False)` (l. 94); `main()` (l. 176) | RO76 restriction not applied, although reported in the Methods as a data check. Non-GP settings are included and assigned by postcode. | Minor noise; description inconsistent. |
| B11 | `build_panel.py`, `annual_prescribing` (l. 107–109) | Practice-postcode-to-LAD attribution. E85124 (GP at Hand, SW6) rises from about 1–4.5k to about 28k items a month, all attributed to Hammersmith & Fulham. | Within-area exposure artefacts, especially at LTLA level. |
| B12 | `fetch_pre2014_practice.py`, `aggregate` and `process_month` | No filter equivalent to the EPD `UNIDENTIFIED` / `'-'` exclusion; no practice-setting restriction; about 10,260 PDPI organisation codes vs about 9,930 EPD codes. Raw files `201106.zip` and `T201201*` remain, indicating an interrupted run with no try/finally clean-up. The name-regex groups depend on the PDPI CHEM file names. | Splice discontinuity at 2014 (M8); fragile pipeline. |
| B13 | `fetch_steroids.py`, `PRED_TABLET_MG` (l. 23–24) | Regex matches only generically described prednisolone tablets; branded descriptions and oral liquids are excluded from mg and `items_prednisolone_tablets`. | Possible time-varying bias in the mg series (Figure 3; UK-born regional analyses). |
| B14 | `mde.py`, `__main__` | Writes `mde_table.csv` (3-year rolling panel, t−5..t−3) and `mde_table_annual.csv` only. No code produces `outputs/mde/mde_table_ltla.csv`, the source of Table 2. The docstring says `outputs/panel/panel_results.csv` is the input. | Table 2 not reproducible from the repository. |
| B15 | `plot_hospital.py`, `SCENARIOS` (l. 31–36) | Hospital systemic corticosteroids use the primary-care OCS inputs (RR 4.9, prevalence 0.9%). Anti-TNF prevalence of 0.2% is below the SCMD-implied 0.35–0.4% in 2024. | Table 3 expected-change column misspecified. |
| B16 | `hospital_medicines.py`, `trust_year_quantities` (l. 53) | `quantity` is approx_mg for all non-anti-TB groups (see M2); `indicative_cost` is NaN for January–March 2019 but summed (NaN treated as 0). | Cost-based sensitivity understates 2019. |
| B17 | `fetch_scmd.py`, `main` (l. 186–191) | Negative quantities from SCMD backtracking are retained (e.g. −623,990 g hydrocortisone butyrate ointment, excluded; −30 ml prednisolone 25 mg/ml injection, included). | Negligible, but should be truncated or logged. |
| B18 | `build_trust_catchment.py` | Only catchment years 2023 and 2024 are available in the extracted table; `hospital_medicines.py` applies 2024 shares to 2019–2024. | Time-invariant catchments ignore service reconfiguration (M5, M10). |
| B19 | `paper/manuscript.md`, Methods, "Hospital medicines" | "Trusts with catchment data accounted for 96–99% of quantity in every group" is pooled over years; by year it is 90–99%. | Misleading completeness statement. |
| B20 | `paper/manuscript.md`, References | Reference 35 not cited in text; reference 33 does not support the sentence citing it. | Editorial. |

---

*Reviewer 3*
