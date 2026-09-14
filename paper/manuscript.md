---
title: "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care prescribing and TB incidence in England, 2014–2024"
short_title: "Prescribing and TB in England"
article_type: "Original research · Ecological study"
date: "Draft, 14 September 2026"
authors: "[Authors to be confirmed]"
thesis: "For oral corticosteroids, the smallest effect these data could detect (7.0% per 10% more prescribing) is about 20 times the effect expected from published relative risks (0.34%)."
---

## Abstract

**Background.** Several commonly prescribed medicines, notably corticosteroids and other immunosuppressants, modify individual risk of tuberculosis (TB). Openly published English prescribing and TB surveillance data could, in principle, be linked to study these relationships at population level. We assessed whether such ecological analyses can detect drug–TB associations.

**Methods.** We linked practice-level NHSBSA English Prescribing Dataset records (2014–2024) for 12 pre-specified drug groups, including a positive and a negative control exposure, to UKHSA TB notifications. We used:

- a cross-sectional analysis of 105 Sub-ICB locations;
- panel analyses of upper-tier local authorities with annual and rolling three-year outcomes, using Poisson pseudo-maximum-likelihood with area and time fixed effects, lagged exposures and a lead-exposure falsification test;
- analyses of change in oral corticosteroid prescribing against TB overall and in UK-born and non-UK-born people by region.

We calculated minimum detectable effects (MDEs) and compared them with the population effects implied by published individual-level relative risks.

**Results.**

- **Cross-sectional:** most drug groups were inversely associated with TB, but these associations disappeared after adjustment for country of birth and age structure.
- **Annual panel** (1,191 area-years, 149 authorities): no drug group was associated with subsequent TB. For oral corticosteroids, the incidence rate ratio (IRR) per 10% within-area increase in prescribing was 0.985 (95% CI 0.940–1.033).
- **Controls:** the positive control was not detected, and future vitamin D prescribing "predicted" past TB.
- **Steroid trends:** oral corticosteroid items fell 9.7% and prednisolone milligrams per resident fell 21.2% between 2014 and 2024. These changes did not track changes in TB incidence.
- **UK-born TB:** a regional association with prednisolone dose was implausibly large and did not survive correction for multiple testing.
- **Power:** the MDE for oral corticosteroids was 7.0% per 10% increase in prescribing, about 20 times the expected effect (0.34%). Power to detect the expected effect was below 4% for every drug group.

**Conclusions.** Routinely published prescribing and TB notification data cannot detect plausible population-level effects of primary care medicines on TB in England. Apparent associations mainly reflect confounding by migration, age and area-specific trends. Causal questions need individual-level linked data analysed with target trial emulation.

## Introduction

TB remains a public health problem in England. After falling from 2011 to a low of 4,125 notifications in 2020, TB notifications rose by 13% in 2024 to 5,480 [1]. Most cases occur in people born outside the UK, many through reactivation of infection acquired abroad [1,2]. Recent national trends have been driven largely by migration and screening policy [3,4].

Host factors also modify TB risk, and several are shaped by commonly prescribed medicines. In individual-level studies:

- current oral glucocorticoid use is associated with about a five-fold increase in TB risk, rising with dose [5];
- inhaled corticosteroids and conventional disease-modifying antirheumatic drugs (DMARDs) are associated with smaller increases [6–8];
- proton pump inhibitors (PPIs) are associated with increased risk [9];
- statins and metformin are associated with lower risk [10,11].

Many of these estimates come from high-incidence settings and observational designs prone to confounding.

England publishes monthly prescribing for every general practice, and UKHSA publishes TB notifications by area. Linking the two is an attractive, low-cost way to generate or test hypotheses about medicines and TB. Such ecological analyses face four problems:

- confounding by area characteristics;
- cross-level bias, which adjustment cannot remove when effects differ between population groups [12,13];
- power, which depends on the number of areas rather than the volume of data within them [14];
- dataset-specific limitations: prescribing data exclude hospital medicines, practice list sizes are inflated in ways that track population mobility [15,16], and prescribing is patterned by deprivation and was disrupted by COVID-19 [17].

We found no previous study linking area-level prescribing to TB. The closest analogues show two things: drugs with large individual-level effects can produce much weaker population signals, and cross-sectional and within-area associations can have opposite signs [18,19].

We asked whether published English prescribing data can detect drug–TB associations at population level. We combined cross-sectional and fixed-effects panel designs with positive and negative control exposures and a falsification test [20,21]. We also examined TB in UK-born people, which is less influenced by migration [22]. Finally, we calculated the minimum effects these designs could detect.

## Methods

### Design and data sources

All data were public, aggregate and anonymised; ethical approval was not required.

**Prescribing.**

- **Source:** the NHS Business Services Authority English Prescribing Dataset (EPD) records items dispensed in the community from primary care prescriptions [30,40].
- **Extraction:** we aggregated items by practice and month on the NHSBSA server, for January 2014–December 2024 (BNF-coded release) and June 2026 (SNOMED-coded release, cross-sectional analysis).
- **Consistency:** national totals for June 2024 were identical in the two releases.
- **Setting:** standard GP practices (ODS prescribing setting RO76) accounted for 98.6% of items.
- **Dose:** the average daily quantity field is not populated for corticosteroids in the BNF-coded release. We therefore derived prednisolone dose as tablets dispensed × tablet strength.

**TB outcomes.**

- **Annual counts by upper-tier local authority (UTLA), 2001–2024:** UKHSA TB regional reports 2024 supplementary tables. Summed to three years, these matched the Fingertips three-year counts (149 UTLAs; r = 0.996; total ratio 1.008).
- **Three-year counts:** Fingertips indicator 91361, for Sub-ICB locations and UTLAs.
- **Annual counts by UKHSA region and place of birth, with Labour Force Survey denominators:** *TB in England 2025*, Supplementary Table 12 [1].

**Covariates.**

- Office for National Statistics (ONS) mid-year population estimates by age.
- ONS international in-migration (components of change).
- Census 2021 percentage born outside the UK and Index of Multiple Deprivation 2025 (cross-sectional analysis only).
- Diagnosed HIV prevalence and Quality and Outcomes Framework (QOF) diabetes prevalence (Fingertips).

**Geography.**

- Practices were assigned to local authorities by postcode (ONS Postcode Directory) and aggregated to April 2023 UTLAs.
- Sub-ICB TB data were re-apportioned from 2024 to 2026 boundaries using LSOA population weights.
- Denominators were resident populations, which avoids list inflation.

**Exposures.** Twelve groups were specified before analysis:

- **Positive control:** antituberculosis drugs.
- **Candidate groups:** oral corticosteroids; inhaled corticosteroids; non-biologic immunosuppressants (methotrexate, leflunomide, azathioprine, mycophenolate, calcineurin and mTOR inhibitors, JAK inhibitors); PPIs; statins; metformin; insulins; fluoroquinolones; all antibacterials; vitamin D.
- **Negative control:** levothyroxine.

Eye, ear, nose and skin preparations were excluded.

### Statistical analysis

**Cross-sectional analysis.** Negative binomial regression of 2022–24 TB counts (population offset; robust SEs) on each standardised prescribing rate, unadjusted and adjusted for percentage non-UK-born, deprivation, age structure and diabetes prevalence.

**Panel analyses.**

- **Model:** Poisson pseudo-maximum-likelihood regression [23] of TB counts on the log mean prescribing rate, with UTLA and year fixed effects, a log population offset and SEs clustered by UTLA.
- **Primary exposure window:** years *t*−3 to *t*−1 before the outcome year *t* (annual outcomes, 2017–2024).
- **Time-varying covariates:** age structure, international in-migration (outcome and exposure windows), HIV prevalence and diabetes prevalence.
- **Sensitivity analyses:** one-year and concurrent exposure; exclusion of 2020–21; rolling three-year outcomes with exposure *t*−5 to *t*−3.
- **Falsification test:** prescribing in the three years *after* the outcome year.
- **Effect measure:** IRR per 10% within-area increase in prescribing, with Benjamini–Hochberg false discovery rate (FDR) correction across drug groups.

**Oral corticosteroid change analyses.**

- **National:** correlations of annual levels and year-on-year changes (lags 0–3).
- **Regional:** Poisson region and year fixed-effects models of annual TB (lags 1–3), adjusted for in-migration and age. With nine clusters, inference used cluster-robust SEs with *t*(8) critical values, and we report leave-one-region-out ranges.
  - Outcomes: all TB, UK-born TB and non-UK-born TB.
  - Exposures: oral corticosteroid items and prednisolone milligrams per resident.
  - Checks: levothyroxine, PPIs and statins as comparison exposures; lead exposures; exclusion of 2020–21.
- **Local authority long differences:** changes between 2014–16 and 2019–21 (prescribing) and between 2014–16 and 2022–24 (TB).

**Minimum detectable effects.** From the primary panel model, the MDE for a 10% increase in prescribing, with 80% power and two-sided α = 0.05, is exp(2.80 × SE).

We assumed incidence ∝ 1 + *p*(RR − 1), where *p* is the prevalence of use and RR the published individual-level relative risk (Table 2 sources [5,6,8,9,10,11,24–29]). Under that assumption, a 10% relative increase in use gives an expected population IRR of [1 + 1.1*p*(RR − 1)] / [1 + *p*(RR − 1)].

This assumption ignores confounding and ecological bias, so it favours detection. We also report:

- the population attributable fraction;
- power to detect the expected effect;
- the RR needed for 80% power.

Analyses used Python 3.14 (pandas, statsmodels).

## Results

### Prescribing and TB trends

TB incidence in England fell from 11.9 per 100,000 in 2014 to 7.3 in 2020, then rose to 9.4 in 2024. Between 2014 and 2024, prescribing per 1,000 residents changed as follows:

- **Rose:** PPIs (+35%), statins (+31%), metformin (+30%) and vitamin D (+42%).
- **Fell:** oral corticosteroids (−10%), immunosuppressants (−10%), fluoroquinolones (−51%) and antituberculosis drugs (−67%).

Within-area variation was small relative to between-area variation. For oral corticosteroids, the SD of the area-demeaned log rate was 0.07, against 0.31 between areas.

### Cross-sectional analysis

In 105 Sub-ICB locations, TB incidence was strongly associated with the percentage of residents born outside the UK (IRR per SD 1.40) and inversely with the percentage aged 65 and over (0.67).

- **Unadjusted:** almost every drug group was inversely associated with TB (Table 1), e.g. oral corticosteroids 0.59 (0.53–0.66) per SD.
- **Adjusted:** all estimates moved close to the null, and none survived FDR correction (all *q* ≥ 0.20). The negative control levothyroxine (0.94, 0.88–1.00) was as "significant" as PPIs (0.89, 0.80–1.00).

### Panel analyses

**Primary model.** The annual panel included 1,191 area-years from 149 UTLAs. No drug group was associated with TB incidence (Table 1, Figure 1; all *q* ≥ 0.67). For example:

- oral corticosteroids 0.985 (0.940–1.033);
- immunosuppressants 1.010 (0.986–1.035);
- inhaled corticosteroids 0.968 (0.910–1.030).

The positive control was not detected: antituberculosis drugs gave 1.004 (0.999–1.010).

**Sensitivity analyses.** One-year and concurrent exposures, exclusion of 2020–21 and rolling three-year outcomes gave similar results; for example, rolling-window oral corticosteroids were 1.001 (0.951–1.055).

**Falsification test.** Future vitamin D prescribing was associated with past TB (1.026, 1.001–1.052). Without covariates, future inhaled corticosteroid, insulin and levothyroxine prescribing were too. Adjusting for total prescribing volume produced a spurious inverse association for the negative control (0.940, 0.895–0.988), so this adjustment was not used.

![**Figure 1.** Fixed-effects panel estimates for annual TB notifications by upper-tier local authority. Blue: prescribing in the three years before the outcome year (primary analysis). Orange: prescribing in the three years after (falsification test). IRR per 10% within-area increase in prescribing; area and year fixed effects; adjusted for age structure, in-migration, HIV and diabetes prevalence.](figures/panel_annual_forest_plot.png)

**Table 1.** Associations between prescribing and TB incidence across designs. Cross-sectional: IRR per SD of prescribing rate (105 Sub-ICBs, TB 2022–24, prescribing June 2026). Panel: IRR per 10% within-area increase (149 UTLAs, annual TB 2017–2024).

| Drug group | Cross-sectional, crude | Cross-sectional, adjusted | Panel, prior 3 years | Panel, next 3 years (falsification) |
|:---|:---|:---|:---|:---|
| Antituberculosis (positive control) | 0.96 (0.60–1.51) | 0.89 (0.79–1.00) | 1.004 (0.999–1.010) | 1.001 (0.996–1.007) |
| Oral corticosteroids | 0.59 (0.53–0.66) | 0.97 (0.82–1.14) | 0.985 (0.940–1.033) | 1.003 (0.955–1.054) |
| Inhaled corticosteroids | 0.73 (0.64–0.83) | 1.02 (0.90–1.15) | 0.968 (0.910–1.030) | 0.967 (0.914–1.023) |
| Immunosuppressants | 0.68 (0.61–0.77) | 1.01 (0.93–1.09) | 1.010 (0.986–1.035) | 1.006 (0.977–1.035) |
| Proton pump inhibitors | 0.66 (0.59–0.75) | 0.89 (0.80–1.00) | 0.966 (0.913–1.022) | 1.046 (0.993–1.102) |
| Statins | 0.67 (0.60–0.75) | 0.93 (0.85–1.02) | 1.009 (0.949–1.073) | 1.033 (0.983–1.086) |
| Metformin | 1.24 (1.05–1.46) | 0.98 (0.89–1.08) | 0.977 (0.927–1.031) | 1.015 (0.972–1.060) |
| Insulins | 0.94 (0.75–1.18) | 0.97 (0.87–1.08) | 0.992 (0.928–1.060) | 0.951 (0.901–1.005) |
| Fluoroquinolones | 0.77 (0.66–0.89) | 0.97 (0.90–1.03) | 1.000 (0.979–1.021) | 0.997 (0.977–1.017) |
| All antibacterials | 0.65 (0.56–0.74) | 0.89 (0.78–1.01) | 0.995 (0.952–1.040) | 1.010 (0.973–1.048) |
| Vitamin D | 0.73 (0.65–0.83) | 0.95 (0.88–1.02) | 1.011 (0.983–1.040) | 1.026 (1.001–1.052) |
| Levothyroxine (negative control) | 0.64 (0.57–0.72) | 0.94 (0.88–1.00) | 0.967 (0.928–1.008) | 0.973 (0.929–1.019) |

### Minimum detectable effects

For oral corticosteroids, a 10% increase in use would be expected to raise TB incidence by 0.34%, while the primary panel could detect only a 7.0% change (Table 2). Power was 3.4%, and an individual RR of about 257 would have been needed for 80% power.

For the other groups, the MDE exceeded the expected effect by 16-fold (statins) to 345-fold (immunosuppressants). For the protective associations (statins, metformin), no individual effect, even complete protection, could have produced a detectable change.

**Table 2.** Minimum detectable effects of the annual panel versus expected population effects. Percentages refer to the change in TB incidence for a 10% within-area increase in prescribing.

| Drug group | Individual RR | Prevalence of use | PAF | Expected change | MDE | MDE ÷ expected | Power | RR for 80% power |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| Oral corticosteroids | 4.9 | 0.9% | 3.4% | 0.34% | 7.0% | 20 | 3.4% | 257 |
| Inhaled corticosteroids | 1.27 | 5.2% | 1.4% | 0.14% | 9.2% | 64 | 2.8% | 236 |
| Immunosuppressants | 1.2 | 0.5%^a^ | 0.1% | 0.01% | 3.5% | 345 | 2.5% | 109 |
| Proton pump inhibitors | 1.28 | 14.2% | 3.8% | 0.38% | 8.4% | 21 | 3.4% | 38 |
| Statins | 0.60 | 12.8% | −5.4% | −0.54% | 9.1% | 16 | 3.7% | not attainable^b^ |
| Metformin | 0.51 | 4.4% | −2.2% | −0.22% | 7.9% | 34 | 3.0% | not attainable^b^ |

^a^ Assumed from EPD item volumes; no verified UK prevalence found. ^b^ Even RR = 0 changes incidence by less than the MDE. PAF, population attributable fraction; MDE, minimum detectable effect (80% power, α = 0.05).

### Oral corticosteroids and changes in TB incidence

**Trends.** Oral corticosteroid items fell from 141.5 to 127.7 per 1,000 residents between 2014 and 2024 (Figure 2).

- Prednisolone, 92% of items, fell 12.9%.
- Prednisolone milligrams per resident fell 21.2%, because courses also became smaller: milligrams per item fell from 205 to 186.
- Hydrocortisone, used mainly as replacement therapy, rose 41.9%.
- Most of the decline occurred in 2020–21.

**National level.** Annual oral corticosteroid prescribing and TB incidence were correlated in levels (r = 0.63), driven by the shared 2020 dip. Year-on-year changes were not correlated at any lag (all *p* ≥ 0.2).

**Regional level (all TB).** Adjusted estimates were null, e.g. lag 1: 0.997 (0.788–1.260) per 10%.

**Local authority long differences.** Across 138 UTLAs, changes in prescribing were unrelated to changes in TB (Spearman ρ = −0.13; adjusted ratio 1.000, 0.934–1.072).

![**Figure 2.** Oral corticosteroid prescribing in English primary care, 2014–2024: items per 100,000 residents per month by substance (top) and prednisolone tablet milligrams dispensed per resident (bottom).](figures/ocs_national_trends.png)

**Non-UK-born TB.** 36,633 notifications in 2015–2024. Oral corticosteroid prescribing was not associated with TB at any lag. The falsification test failed: future prescribing was associated with past TB (items, lead 3: 1.36, 1.03–1.80; PPIs 1.25, 1.02–1.53).

**UK-born TB.** 11,876 notifications in 2015–2024.

- **Prednisolone milligrams per resident** were associated with TB at lags of 2 years (1.37, 1.08–1.73) and 3 years (1.38, 1.04–1.83). These estimates:
  - were unchanged after excluding 2020–21;
  - were not reproduced with lead exposures (0.95–1.18) or with levothyroxine, PPIs or statins;
  - did not survive correction for the six steroid tests (Holm-adjusted *p* = 0.09 and 0.16).
- **Oral corticosteroid items** gave imprecise positive estimates (1.26–1.32, all *p* > 0.09).
- **Across all 90 adjusted regional models,** 7 were nominally significant, against 4.5 expected by chance.

UK-born TB fell by roughly half in most regions over the decade (Figure 3).

![**Figure 3.** Oral corticosteroid items per 1,000 residents (blue) and UK-born TB notification rate (orange) by UKHSA region, indexed to 2014 = 100.](figures/ocs_ukborn_tb_by_region.png)

## Discussion

### Principal findings

We used three ecological designs and more than a decade of practice-level prescribing, and found no credible association between primary care prescribing and TB incidence in England.

- **Cross-sectional associations were confounded.** Crude inverse associations were explained by areas with young, migrant populations having both more TB and less chronic-disease prescribing.
- **Within-area estimates were null** for every drug group.
- **The design could not have detected plausible effects.** The positive control was not detected, falsification tests failed for several exposures, and expected population effects were 16 to 345 times smaller than the minimum detectable effects.

### Interpretation

The minimum detectable effect analysis explains why the design was uninformative.

- **Expected effect.** Oral corticosteroids carry about a five-fold individual risk [5], but only about 1% of people use them at any time [24,25]. A 10% change in use should therefore move TB incidence by about 0.3%. This is consistent with the small attributable fractions reported for inhaled corticosteroids (0.5%) [7] and estimated here.
- **Why more data would not help.** Power in aggregate studies depends on the number of areas [14], and prescribing varies little within areas over time. Fixed effects remove the between-area variation where most information lies [31].

**Crude versus adjusted estimates.** The contrast mirrors the between- versus within-country sign reversal reported for diabetes and TB [19]. Adjustment cannot remove ecological bias from effect modification [12]. This is relevant because drug-associated TB risk may differ by ethnicity [32,33].

**The UK-born association** shows how apparent signals arise in these data. It passed a lead test and a negative-control comparison, but it is implausibly large. Under the model used for the MDE, a 10% increase in the prevalence of any exposure can raise incidence by at most 10%, and by less than 1% under published relative risks. An IRR of 1.37 per 10% therefore cannot reflect a causal effect of steroid prescribing.

With only nine regions and multiple tests, the association more likely reflects region-specific declines in UK-born TB, which are shaped by social risk factors, transmission and demographic change [22,34].

### Strengths and limitations

**Strengths.**

- All data are public, and the analysis is reproducible.
- Exposures, controls and the falsification test were specified in advance.
- Data consistency was checked:
  - the two prescribing releases gave identical totals;
  - annual TB counts matched the published three-year counts;
  - 98% of prescribing items were linked to an area.
- Power was quantified explicitly.

**Limitations.**

- **Missing exposures.** The EPD excludes hospital-prescribed medicines, including biologics, most specialist immunosuppression and in-hospital dexamethasone during COVID-19 [35]. These are the highest-risk exposures.
- **Exposure measurement.** Exposure was measured as items, or prednisolone milligrams, per resident, not as people treated.
- **Geographic mapping.** Mapping practices to local authorities by postcode misattributes cross-boundary registrations.
- **Outcome stratification.** TB by place of birth was available only by region.
- **Unmeasured confounding.** Time-varying confounders were not measured: the latent TB screening programme for new migrants [36], social risk factors and diagnostic intensity [37].
- **Area boundaries.** City of London and the Isles of Scilly are grouped differently in the TB and population sources.

### Implications

**Open prescribing data** remain valuable for describing prescribing [30,40], but they are not suited to estimating medicine effects on rare infectious outcomes such as TB.

**Causal questions need individual-level linked data.** CPRD primary care records linked to Hospital Episode Statistics and UKHSA TB surveillance could support target trial emulations of corticosteroid or immunosuppressant initiation. Even national primary care cohorts produce wide confidence intervals for modest relative risks [39]. We found no target trial emulation of these drugs and TB; the only drug–TB emulation identified concerned DPP-4 inhibitors [38].

**Better population data would help.** Annual local TB notifications stratified by place of birth and age, available through a UKHSA data request, would improve future population analyses.

**Reporting.** Studies using open prescribing data for rare outcomes should report minimum detectable effects and falsification tests alongside associations.

### Conclusion

Ecological analyses of English prescribing data do not, and on power grounds cannot, detect population-level effects of primary care medicines on TB.

## Data and code availability

**Data.** All data are publicly available:

- NHSBSA Open Data Portal (English Prescribing Dataset);
- UKHSA Fingertips and TB report supplementary tables;
- ONS/Nomis population and migration estimates;
- NHS England Organisation Data Service;
- MHCLG English Indices of Deprivation 2025.

**Code.** Analysis code is available from the authors [repository to be added].

## References

1. UK Health Security Agency. Tuberculosis in England: 2025 report (data up to end of 2024). London: UKHSA; 2025.
2. Aldridge RW, et al. Tuberculosis in migrants moving from high-incidence to low-incidence countries: a population-based cohort study of 519 955 migrants screened before entry to England, Wales, and Northern Ireland. *Lancet* 2016. doi:10.1016/S0140-6736(16)31008-X
3. Thomas HL, et al. Explaining the recent decline in tuberculosis incidence in the UK. *Thorax* 2018. doi:10.1136/thoraxjnl-2017-211074
4. Crofts JP, et al. Tuberculosis trends in England. *Public Health* 2008. doi:10.1016/j.puhe.2008.04.011
5. Jick SS, Lieberman ES, Rahman MU, Choi HK. Glucocorticoid use, other associated factors, and the risk of tuberculosis. *Arthritis Rheum* 2006;55:19–26. doi:10.1002/art.21705
6. Brassard P, Suissa S, Kezouh A, Ernst P. Inhaled corticosteroids and risk of tuberculosis in patients with respiratory diseases. *Am J Respir Crit Care Med* 2011;183:675–8. doi:10.1164/rccm.201007-1099OC
7. Castellana G, et al. Inhaled corticosteroids and risk of tuberculosis in patients with obstructive lung diseases: a systematic review and meta-analysis. *Int J Chron Obstruct Pulmon Dis* 2019;14:2219–27. doi:10.2147/COPD.S209273
8. Brassard P, Kezouh A, Suissa S. Antirheumatic drugs and the risk of tuberculosis. *Clin Infect Dis* 2006;43:717–22. doi:10.1086/506935
9. Song HJ, Park H, Park S, Kwon JW. Association of proton pump inhibitor use with risk of tuberculosis. *Pharmacoepidemiol Drug Saf* 2019;28:830–9. doi:10.1002/pds.4773
10. Li X, Sheng L, Lou L. Statin use may be associated with reduced active tuberculosis infection: a meta-analysis. *Front Med* 2020;7:121. doi:10.3389/fmed.2020.00121
11. Zhang M, He JQ. Impacts of metformin on tuberculosis incidence and clinical outcomes in patients with diabetes: a systematic review and meta-analysis. *Eur J Clin Pharmacol* 2020;76:149–59. doi:10.1007/s00228-019-02786-y
12. Greenland S, Morgenstern H. Ecological bias, confounding, and effect modification. *Int J Epidemiol* 1989;18:269–74. doi:10.1093/ije/18.1.269
13. Morgenstern H. Ecologic studies in epidemiology: concepts, principles, and methods. *Annu Rev Public Health* 1995;16:61–81. doi:10.1146/annurev.pu.16.050195.000425
14. Sheppard L, et al. Ecologic inference in aggregate data studies. *Stat Med* 1996. PMID 8888477
15. Hudson SM, et al. GP practice list inflation and cancer screening coverage. *J Med Screen* 2025. doi:10.1177/09691413251347408
16. Venkatesan S, et al. Registered patient denominators compared with Census 2021. *JMIR Public Health Surveill* 2025. doi:10.2196/64788
17. Richards TC, et al. Neighbourhood variation in prescribing using OpenPrescribing data. *Sci Rep* 2025. doi:10.1038/s41598-025-02969-x
18. Hermans S, et al. Ecological analysis of TB notifications during antiretroviral therapy scale-up in Cape Town. *J Int AIDS Soc* 2015. doi:10.7448/IAS.18.1.20240
19. Költringer FA, et al. Diabetes and tuberculosis: within- and between-country associations in a global panel. *BMC Public Health* 2023. doi:10.1186/s12889-023-15213-w
20. Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative controls: a tool for detecting confounding and bias in observational studies. *Epidemiology* 2010;21:383–8. doi:10.1097/EDE.0b013e3181d61eeb
21. Prasad V, Jena AB. Prespecified falsification end points: can they validate true observational associations? *JAMA* 2013;309:241–2. doi:10.1001/jama.2012.96867
22. Nguipdop-Djomo P, et al. Small-area level socio-economic deprivation and tuberculosis rates in England. *PLoS One* 2020. doi:10.1371/journal.pone.0240879
23. Santos Silva JMC, Tenreyro S. The log of gravity. *Rev Econ Stat* 2006;88:641–58.
24. van Staa TP, et al. Use of oral corticosteroids in the United Kingdom. *QJM* 2000;93:105–11. doi:10.1093/qjmed/93.2.105
25. Fardet L, Petersen I, Nazareth I. Prevalence of long-term oral glucocorticoid prescriptions in the UK over the past 20 years. *Rheumatology* 2011;50:1982–90. doi:10.1093/rheumatology/ker017
26. Bloom CI, Saglani S, Feary J, Jarvis D, Quint JK. Changing prevalence of current asthma and inhaled corticosteroid treatment in the UK. *Eur Respir J* 2019;53:1802130. doi:10.1183/13993003.02130-2018
27. Abrahami D, McDonald EG, Schnitzer M, Azoulay L. Trends in acid suppressant drug prescriptions in primary care in the UK. *BMJ Open* 2020;10:e041529. doi:10.1136/bmjopen-2020-041529
28. O'Keeffe AG, Nazareth I, Petersen I. Time trends in the prescription of statins for the primary prevention of cardiovascular disease in the United Kingdom. *Clin Epidemiol* 2016;8:123–32. doi:10.2147/CLEP.S104258
29. Sharma M, Nazareth I, Petersen I. Trends in incidence, prevalence and prescribing in type 2 diabetes mellitus in the UK. *BMJ Open* 2016;6:e010210. doi:10.1136/bmjopen-2015-010210
30. Bacon S, Goldacre B. Barriers to working with national health service England's open data. *J Med Internet Res* 2020. doi:10.2196/15603
31. Gunasekara FI, Richardson K, Carter K, Blakely T. Fixed effects analysis of repeated measures data. *Int J Epidemiol* 2014;43:264–9. doi:10.1093/ije/dyt221
32. Dixon WG, et al. Drug-specific risk of tuberculosis in patients with rheumatoid arthritis treated with anti-TNF therapy. *Ann Rheum Dis* 2010;69:522–8. doi:10.1136/ard.2009.118935
33. Ruzangi J, et al. Chronic kidney disease and tuberculosis: a CPRD cohort study. *BMC Nephrol* 2020. doi:10.1186/s12882-020-02065-4
34. Davidson JA, et al. Risk factors for recent transmission of tuberculosis in England. *Am J Epidemiol* 2018. doi:10.1093/aje/kwy119
35. RECOVERY Collaborative Group. Dexamethasone in hospitalized patients with Covid-19. *N Engl J Med* 2021;384:693–704. doi:10.1056/NEJMoa2021436
36. Berrocal-Almanza LC, et al. Effectiveness of nationwide programmatic testing and treatment for latent tuberculosis infection in migrants in England. *Lancet Public Health* 2022. doi:10.1016/S2468-2667(22)00031-7
37. Kumwichar P, et al. Tuberculosis following COVID-19 pneumonia: national claims data from Thailand. *EClinicalMedicine* 2023. doi:10.1016/j.eclinm.2023.101825
38. Chen YG, et al. DPP-4 inhibitors and pulmonary tuberculosis: a target trial emulation. *BMC Med* 2025. doi:10.1186/s12916-025-04423-1
39. Pealing L, et al. Risk of tuberculosis in patients with diabetes: population based cohort study using the UK Clinical Practice Research Datalink. *BMC Med* 2015. doi:10.1186/s12916-015-0381-9
40. OpenPrescribing.net, Bennett Institute for Applied Data Science, University of Oxford. Frequently asked questions. 2026.

*Reference titles for [2–4, 14–19, 22, 30, 33, 34, 37, 38] are abbreviated and must be checked against the source records before submission.*
