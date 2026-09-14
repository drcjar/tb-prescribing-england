---
title: "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England"
short_title: "Prescribing and TB in England"
article_type: "Original research · Ecological study"
date: "Draft 3 (revised after peer review), 14 September 2026"
authors: "[Authors to be confirmed]"
thesis: "A disease-specific positive control shows the linkage works only with heavy attenuation, and plausible effects of medicines on TB lie one to two orders of magnitude below what these ecological designs can detect."
---


## Abstract

**Background.**
- Corticosteroids, biologics and other immunosuppressants increase individual risk of tuberculosis (TB).
- Openly published English prescribing and TB surveillance data could, in principle, be linked to study these relationships at population level.
- We assessed whether such ecological analyses can detect associations between medicines and TB, and why they might not.

**Methods.**
- **Exposures.**
  - Primary care prescribing, 2011–2024: practice-level data apportioned to local authorities by where registered patients live. Drug groups were defined at presentation level (systemic oral glucocorticoids, conventional DMARDs, transplant immunosuppressants and others), including a negative-control exposure.
  - Hospital medicines, 2019–2024: NHS Secondary Care Medicines Data in WHO defined daily doses, apportioned by trust catchment. Controls were a disease-specific positive control (active-TB treatment) and negative-control exposures.
- **Outcomes.** Annual UKHSA TB notifications for 294 lower-tier and 151 upper-tier authorities, and by region, place of birth and age.
- **Analysis.**
  - Poisson panel models with area and year fixed effects, exposure in the previous year, and falsification (lead) tests.
  - Regional models with randomisation inference.
  - Minimum detectable effects (MDE), compared with expected population effects derived from published relative risks and UKHSA-recorded drug-associated TB.
  - A permutation-based power simulation on the real notification counts.

**Results.**
- **Linkage.** Hospital active-TB treatment tracked TB notifications between areas (Spearman ρ = 0.79) and within areas in the same year (incidence rate ratio [IRR] 1.035, 95% CI 1.013–1.058, per 10% increase). The within-area elasticity was only 0.36–0.40, indicating substantial attenuation even for a disease-specific drug.
- **Primary care.** No drug group was associated with notifications in the following year. For systemic oral glucocorticoids the IRR was 0.982 (0.941–1.025) per 10% within-area increase.
- **Hospital medicines.** TNF inhibitors (0.989, 0.972–1.006), JAK inhibitors and systemic glucocorticoids were also null.
- **Falsification and negative control.** Several falsification tests failed, and the negative-control exposure showed inverse estimates similar in size to candidate drugs. This indicates residual confounding by area-specific trends.
- **Power.**
  - For oral glucocorticoids, the MDE (6.3% per 10% increase) was about 18 times the effect expected from published relative risks (0.34%), and about 110 times that implied by UKHSA-recorded steroid-associated TB (0.055%).
  - In simulations on the real counts, the published effect was detected in 7.7% of replicates, no better than the 7.0% false-positive rate with no effect.
- **UK-born TB.** A regional association between prednisolone dose and UK-born TB was implausibly large and was accompanied by failed negative-control and falsification tests.

**Conclusions.**
- Open English prescribing and TB notification data can be linked, but only with heavy attenuation, and ecological analyses of them cannot detect plausible population-level effects of medicines on TB.
- Apparent associations reflect confounding by migration, age and area trends.
- Causal questions require individual-level linked data analysed with target trial emulation. Surveillance of drug-associated TB is better served by more complete recording of immunosuppression in national TB surveillance.


## Introduction

Tuberculosis (TB) remains a public health problem in England.

**Recent trends.**
- **Decline:** notifications fell by almost half between 2011 and 2018. The fall was largely
  explained by fewer recent migrants from high-incidence countries and by pre-entry screening,
  extended in 2012 to long-term visa applicants from high-incidence countries [Thomas 2018;
  Aldridge 2016].
- **2020:** notifications dropped to 4,125 during the COVID-19 pandemic, a fall thought to reflect
  service disruption rather than less disease [UKHSA 2021; Morrison 2023].
- **2021–2024 rise:** notifications then increased, reaching 5,490 in 2024 (9.4 per 100,000).
  - 81.5% were in people born outside the UK.
  - 41% of those were notified within five years of arrival.
  - The rise has been attributed mainly to migration from higher-incidence countries [UKHSA 2025].
- **2025:** national data show 5,424 notifications, with 2024 revised to 5,487 [UKHSA 2026].

**TB in UK-born people.** UK-born notifications fell by 43% between 2014 and 2022, then rose
[UKHSA 2025]. UK-born TB is heterogeneous: it includes reactivation in older adults, transmission
linked to social risk factors, and disease in UK-born children of migrant families [Davidson 2018].

**Medicines that change TB risk.** Host factors also modify TB risk, and several are shaped by
commonly prescribed medicines.
- **Oral glucocorticoids:** current use is associated with an odds ratio of about 5 for active TB,
  higher at doses ≥15 mg/day [Jick 2006].
- **Inhaled corticosteroids and conventional DMARDs:** smaller increases [Brassard 2011;
  Castellana 2019; Brassard 2006].
- **Anti-TNF biologics:** TB typically presents within months of starting treatment [Keane 2001].
  Latent infection screening before treatment greatly reduces this risk [BTS 2005; Carmona 2005].
- **Proton pump inhibitors:** associations with increased risk [Song 2019].
- **Statins and metformin:** associations with lower risk [Li 2020; Zhang 2020].

Many of these estimates come from high-incidence settings or designs vulnerable to confounding
by indication and protopathic bias.

**Open data and their problems.** England publishes monthly prescribing for every general
practice, hospital medicines use by NHS trust, and TB notifications by local authority. Linking
these offers a low-cost way to generate or test hypotheses about medicines and TB. Such ecological
analyses face well-known problems:
- confounding by area characteristics;
- cross-level bias, which covariate adjustment cannot remove when effects differ between groups
  [Greenland 1989; Morgenstern 1995];
- limited power, which depends on the number of areas [Sheppard 1996].

The data carry specific problems too:
- practice lists are inflated in ways that track population mobility [Hudson 2025;
  Venkatesan 2025];
- practice locations do not match where patients live;
- prescribing is patterned by deprivation and was disrupted by COVID-19 [Richards 2025];
- hospital-prescribed medicines are recorded separately from primary care [Bacon 2020].

**The gap.** We found no previous study linking area-level prescribing to TB. In analogous
settings, drugs with large individual effects produced weak population signals [Hermans 2015], and
between-area and within-area associations had opposite signs [Költringer 2023].

**This study.** We asked whether open English prescribing data can detect associations between
medicines and TB notifications at population level, and why they might not. We combined:
- cross-sectional and fixed-effects panel designs at two geographic scales;
- primary care prescribing apportioned to where registered patients live;
- hospital medicines apportioned by trust catchment, with a disease-specific positive control;
- negative-control exposures and falsification tests [Lipsitch 2010; Prasad 2013];
- regional analyses of TB in UK-born and older people.

We compared the smallest effects these designs could detect, both analytically and by simulation,
with the population effects implied by published individual-level relative risks and by UKHSA
surveillance records of drug-associated TB.


## Methods

### Design and reporting

This study uses aggregate, openly published data in three linked ecological designs:

- a cross-sectional analysis;
- a longitudinal panel analysis of local authorities with area and year fixed effects;
- regional analyses by place of birth and age.

It was reported with reference to the RECORD and STROBE guidance. All data were public, aggregate
and anonymised, so ethical approval was not required. Code, processed data and outputs are
available at https://github.com/drcjar/tb-prescribing-england.

**Pre-specification.** The analysis developed in stages, and we report the chronology.

1. **First pass.** Before any results were seen, we specified the drug groups (including a
   negative-control exposure), the cross-sectional design and the first panel design. The first
   panel design used three-year rolling notifications and exposure in years *t*−5 to *t*−3.
2. **Later additions, made after those analyses gave null results:**
   - annual outcomes;
   - lower-tier authorities;
   - hospital medicines and their controls;
   - regional analyses by birthplace and age;
   - power simulation;
   - spatial diagnostics.
3. **Revisions after peer review:**
   - drug groups redefined;
   - prescribing apportioned by patient residence;
   - exposure in year *t*−1 as primary;
   - lag and lead estimated jointly;
   - randomisation inference;
   - additional covariates.

All analyses after the first pass are exploratory. Estimates from the original designs are given
in the supplement.

### Assumed causal structure

Figure 1 sets out the assumed causal structure. It shows which factors are absorbed by area and year
fixed effects, which are measured and adjusted for, and which remain unmeasured. The primary
exposure is prescribing in the year before the outcome year, because same-year prescribing may be
prescribing for undiagnosed TB (protopathic bias).

![**Figure 1.** Assumed causal structure for area-level prescribing and TB notifications. Area fixed effects absorb stable area characteristics; year fixed effects absorb national shocks; time-varying measured factors are adjusted for; dashed nodes are unmeasured. Same-year prescribing for undiagnosed TB (protopathic bias) motivates the use of prescribing in the previous year.](figures/dag.png)

### TB notifications

TB notifications are cases reported to UKHSA surveillance: the Enhanced TB Surveillance system
(ETS) until 2021, and the National TB Surveillance System (NTBS) since, into which data from 2018
onwards were migrated. Cases are culture-confirmed or clinically diagnosed, and are assigned to
areas by residential postcode at notification.

We used four sources:

1. **Annual counts by local authority, 2001–2024.**
   - *Source:* UKHSA TB regional reports 2024, supplementary tables.
   - *Coverage:* upper-tier authorities (UTLAs; 151, of which 149 were analysed) and lower-tier
     authorities (LTLAs; 294, of which 292 were analysed).
   - *Boundary handling:* counts are published on April 2023 boundaries. The City of London is
     combined with Hackney, and the Isles of Scilly with Cornwall.
   - *Consistency:* summed over three years, these counts matched the Fingertips three-year counts
     (r = 0.996). Local authority sums slightly exceed national totals (5,539 vs 5,490 in 2024),
     reflecting different extract dates.
2. **Region × place of birth × year, 2000–2024**, with Labour Force Survey denominators: *TB in
   England 2025*, Supplementary Table 12.
3. **Region × place of birth × age group × year**: regional reports, Table 9.
4. **National notifications with recorded immunosuppression by cause, 2024**: *TB in England 2025*,
   chapter 1.

The 2020 fall in notifications is thought to reflect service disruption rather than a true
reduction in incidence.

### Primary care prescribing

**Sources.**
- **2010–2013:** HSCIC practice-level prescribing (PDPI), August 2010–December 2013.
- **2014–2024:** NHSBSA English Prescribing Dataset (EPD).

Both record items dispensed in the community from primary care prescriptions. We aggregated each
month to practice level using identical drug-group rules. For the EPD this was done with
server-side SQL.

**Practices included.** We restricted to standard GP practices (NHS ODS prescribing setting RO76),
which accounted for 98–99% of items after 2014.

**Drug groups.** Groups were defined at BNF presentation level:

| Group | Definition |
|---|---|
| Systemic oral glucocorticoids | Prednisolone, prednisone, methylprednisolone, deflazacort and dexamethasone. Injectables, hydrocortisone (mainly replacement therapy) and betamethasone soluble tablets excluded. Oral hydrocortisone and oral dexamethasone are also reported separately. |
| Inhaled corticosteroids | — |
| Conventional DMARDs | Rheumatology methotrexate (including subcutaneous), leflunomide, azathioprine, mercaptopurine. |
| Transplant immunosuppressants | Tacrolimus, ciclosporin, mycophenolate, sirolimus, everolimus. |
| Other groups | Proton pump inhibitors; statins; metformin; insulins; fluoroquinolones; all antibacterials; vitamin D. |
| Descriptive only | Antituberculosis drugs: TB treatment in England is delivered by specialist services, so primary care prescribing of these drugs is not a valid positive control. |
| Negative control exposure | Levothyroxine. |

Eye, ear, nose and skin preparations were excluded.

**Exposure measures.**
- Items per 1,000 residents per year (primary).
- Prednisolone-equivalent milligrams for systemic oral glucocorticoids: strength × quantity ×
  potency, with dexamethasone 6.67, methylprednisolone 1.25 and deflazacort 0.83.
- Average daily quantities (ADQ) for the groups where the EPD populates them.

**Apportionment to areas.** Each practice's annual prescribing was shared across local authority
districts in proportion to where its registered patients lived, using NHS Digital counts of
patients registered at each practice by LSOA:
- April releases from 2014 to 2024 were used;
- 2014 shares were applied to 2011–2013;
- LSOAs were mapped to April 2023 districts.

Assigning each practice to the district containing its postcode was a sensitivity analysis. In
2024, 7.3% of registered patients lived outside the district of their practice.

**Denominators.** ONS mid-year resident population estimates.

### Hospital medicines

**Source and period.** NHS Secondary Care Medicines Data (SCMD; NHSBSA), which gives trust × month ×
product quantities. We used January 2019 to December 2024.

**Classification.** Products were grouped by mechanism, with patient-year equivalents calculated
from WHO defined daily doses (DDD), or documented maintenance doses where WHO gives none. The groups
were:

- TNF inhibitors;
- IL-6 inhibitors and abatacept;
- JAK inhibitors used in rheumatology (ruxolitinib reported separately);
- rituximab;
- calcineurin and mTOR inhibitors;
- antiproliferatives;
- systemic glucocorticoids, measured in prednisolone-equivalent mg and excluding intra-articular,
  depot and topical forms.

**Controls.**
- **Positive control:** active-TB treatment, defined as pyrazinamide- or ethambutol-containing
  products, including the fixed-dose combinations Rifater and Voractiv.
- **Reported separately:** rifamycin and isoniazid products, which are also used for latent TB and,
  in the case of rifampicin, other infections.
- **Negative-control exposures:** IL-17, IL-12/23 and α4β7 inhibitors and anakinra (low TB risk),
  and levetiracetam.

**Trust mergers.** Trusts that merged during 2019–2024 were reassigned to their successors using
NHS ODS records. With this, 98–100% of DDD in every group and year came from trusts with catchment
data.

**Apportionment to areas.** Trust quantities were shared across local authorities using OHID acute
trust catchment populations (2024, all admissions). Elective-admission catchments were a
sensitivity analysis.

### Covariates

**Time-varying (panel analyses):**
- ONS mid-year population estimates by age (% aged ≥65; % aged 15–44);
- international in-migration per 1,000 (ONS components of population change);
- diagnosed HIV prevalence;
- QOF diabetes prevalence;
- the latent TB infection (LTBI) testing and treatment programme for new migrants, as an active-area
  indicator mapped from CCGs to local authorities (active in 83 LTLAs);
- people receiving asylum support per 1,000 (Home Office; from 2014).

**Cross-sectional analyses:**
- Census 2021 percentage born outside the UK.

### Statistical analysis

**Panel analyses.**
- **Model:** Poisson pseudo-maximum-likelihood regression of annual notifications, with area and
  year fixed effects, a log population offset and SEs clustered by area.
- **Primary exposure:** log prescribing rate in year *t*−1. Drug-associated TB typically presents
  within months of exposure [Keane 2001], and same-year prescribing is affected by prescribing for
  undiagnosed TB (protopathic bias).
- **Outcome years:** 2014–2024.
- **Covariates:** the time-varying set above. Diabetes prevalence was not adjusted for in the
  metformin and insulin models.
- **Effect measure:** incidence rate ratio (IRR) per 10% within-area increase in prescribing, with
  Benjamini–Hochberg false discovery rate (FDR) correction across candidate drug groups. Controls
  were excluded from the FDR correction.
- **Falsification:** prescribing in year *t*−1 and year *t*+1 estimated jointly on a common sample;
  a true effect should load on *t*−1 only.
- **Sensitivity analyses:**
  - no covariates;
  - a distributed lag (*t*, *t*−1, *t*−2);
  - the original three-year window (*t*−3 to *t*−1);
  - area-specific linear trends;
  - log population as a covariate instead of an offset (shared-denominator bias);
  - adjustment for the LTBI programme;
  - adjustment for asylum support;
  - excluding outcome years 2020–21 and exposure years 2020–21;
  - outcome years 2018–2024 only (NTBS-era data);
  - outcome years 2015–2024 only, so that all exposure comes from the EPD (splice sensitivity);
  - ADQ instead of items, for groups where the EPD populates ADQ;
  - practice-postcode apportionment;
  - UTLA geography.
- **Spatial dependence:** Moran's I of year-specific Pearson residuals (5-nearest-neighbour weights,
  999 permutations).

**Hospital analyses.** The same model was fitted for 2019–2024, with exposure in:
- the same year (for the positive control, where treatment follows diagnosis);
- the previous year (for candidate drugs);
- the following year.

SEs were also clustered by each area's principal trust, because apportioned exposures share trust-level
variation. The within-area elasticity of the positive control (log IRR per log unit of exposure)
was used as an attenuation factor.

**Regional analyses.**
- **Units:** 9 regions × year.
- **Outcomes:** all TB notifications; UK-born and non-UK-born notifications; UK-born notifications at
  age ≥65 (denominator: all residents aged ≥65).
- **Model:** Poisson regression with region and year fixed effects, exposure lagged or led 1–3
  years, adjusted for in-migration and age structure.
- **Inference:** with only nine clusters, cluster-robust *t*(8) intervals and randomisation
  p-values, permuting whole regional exposure histories across regions (499 permutations).
- **Falsification:** lag 2 and lead 2 estimated jointly.

**Cross-sectional analyses.** Negative binomial regression of TB notifications on standardised log
prescribing rates for the same period, adjusted for percentage born outside the UK, age structure,
in-migration, HIV and diabetes prevalence.

**Expected effects and minimum detectable effects (MDEs).**

*Expected effects.* The population effect of a 10% increase in use was calculated as
[1 + 1.1*p*(RR − 1)] / [1 + *p*(RR − 1)], where *p* is prevalence of use and RR the individual-level
relative risk (odds ratios where only these were available). The calculation assumes that:

1. prevalence of use scales with the prescribing measure;
2. baseline risk is homogeneous;
3. timing is aligned.

All three favour detection. Alternative expected effects came from three sources:

- recorded drug-associated notifications;
- stratification by age and place of birth;
- SCMD-derived prevalence of hospital drug use, including screening-attenuated relative risks for
  TNF inhibitors and attenuation by the positive-control elasticity.

*MDEs.* The MDE was calculated as exp(2.80 × SE). For each MDE we report:

- the minimum detectable population attributable fraction (PAF);
- the largest PAF compatible with the upper 90% confidence limit.

*Power simulation.* A permutation-based simulation kept the real TB counts, so real overdispersion,
serial correlation and trends were preserved. Whole exposure trajectories were permuted across
areas, and known effects were injected by adding cases. This gave 500 null and 300 effect replicates
per scenario, including scenarios where the effect acts through same-year exposure.

Analyses used Python 3.14 (pandas 3.0, statsmodels).


## Results

### Prescribing, TB notifications and within-area variation

**TB notifications in England**
- Fell from 6,474 in 2014 to a low of 4,125 in 2020.
- Rose to 5,490 in 2024, when 81.5% of people notified were born outside the UK.

**Within-area variation in prescribing**
- Once prescribing was apportioned by where patients live, it varied little within areas over time.
- For systemic oral glucocorticoids, the SD of the log rate after removing area and year means was 0.043, against 0.29 between areas. 95% of area-years were within ±9% of their expected value.
- PPIs (0.038) and levothyroxine (0.043) were similar; conventional DMARDs varied more (0.089).
- A 10% within-area change in prescribing is therefore at the edge of the observed data (Figure 2).

![**Figure 2.** Within-area versus between-area variation in log prescribing rates, 292 lower-tier authorities, 2014–2024. Orange line: a 10% increase.](figures/within_between_variation.png)

### Primary care prescribing and TB notifications (panel analyses)

**Primary analysis** (294 lower-tier authorities, 3,233 area-years, outcome years 2014–2024)
- No drug group was associated with notifications in the following year (Table 1; all FDR q ≥ 0.77).
- Systemic oral glucocorticoids: IRR 0.982 (95% CI 0.941–1.025) per 10% within-area increase.

Other groups (same scale, 95% CI):

| Drug group | IRR |
|---|---|
| Oral hydrocortisone | 1.002 (0.990–1.014) |
| Inhaled corticosteroids | 0.981 (0.935–1.029) |
| Conventional DMARDs | 1.003 (0.984–1.023) |
| Transplant immunosuppressants | 0.999 (0.993–1.005) |
| Proton pump inhibitors | 1.009 (0.967–1.054) |
| Statins | 1.000 (0.960–1.041) |
| Metformin | 0.969 (0.938–1.001) |
| Levothyroxine (negative control) | 0.970 (0.938–1.003) |

- Metformin's inverse point estimate was matched in size by the negative control, levothyroxine.

![**Figure 4.** Primary care prescribing and TB notifications, lower-tier authorities, prescribing apportioned by patient residence. Blue: prescribing in the previous year (primary). Orange: prescribing in the following year, estimated jointly (falsification).](figures/panel_forest_ltla_residence.png)

**Table 1. Primary care prescribing in the previous year and TB notifications: incidence rate ratio per 10% within-area increase (95% CI)**

| Drug group | LTLA, residence (294 areas, 2014-2024) | UTLA, residence | LTLA, practice postcode | Falsification: following year (t+1, joint with t−1) | Largest compatible PAF (90% upper limit) |
|:---|---:|---:|---:|---:|---:|
| Antituberculosis (descriptive) | 1.000 (0.997–1.003) | 1.000 (0.997–1.004) | 1.001 (0.998–1.004) | 1.001 (0.998–1.005) | 3% |
| Systemic oral glucocorticoids | 0.982 (0.941–1.025) | 0.987 (0.940–1.037) | 0.983 (0.948–1.019) | 0.946 (0.906–0.987) | 18% |
| Oral hydrocortisone | 1.002 (0.990–1.014) | 0.998 (0.983–1.014) | 1.002 (0.991–1.014) | 1.006 (0.990–1.022) | 12% |
| Oral dexamethasone | 1.004 (0.994–1.015) | 1.005 (0.993–1.018) | 1.002 (0.993–1.012) | 1.003 (0.993–1.014) | 13% |
| Inhaled corticosteroids | 0.981 (0.935–1.029) | 0.976 (0.927–1.028) | 0.983 (0.944–1.024) | 0.875 (0.837–0.914) | 21% |
| Conventional DMARDs | 1.003 (0.984–1.023) | 1.003 (0.980–1.026) | 1.005 (0.988–1.023) | 0.984 (0.950–1.019) | 19% |
| Transplant immunosuppressants | 0.999 (0.993–1.005) | 0.999 (0.992–1.005) | 1.000 (0.995–1.006) | 0.999 (0.991–1.006) | 4% |
| Proton pump inhibitors | 1.009 (0.967–1.054) | 1.004 (0.960–1.050) | 1.001 (0.963–1.040) | 0.969 (0.908–1.034) | 46% |
| Statins | 1.000 (0.960–1.041) | 0.997 (0.955–1.042) | 0.994 (0.959–1.031) | 0.992 (0.929–1.060) | 34% |
| Metformin | 0.969 (0.938–1.001) | 0.964 (0.929–1.000) | 0.967 (0.938–0.996) | 0.998 (0.945–1.054) | 0% |
| Insulins | 0.981 (0.945–1.019) | 0.987 (0.945–1.030) | 0.983 (0.952–1.015) | 0.903 (0.852–0.957) | 13% |
| Fluoroquinolones | 1.010 (0.997–1.023) | 1.007 (0.993–1.021) | 1.008 (0.995–1.020) | 0.994 (0.980–1.009) | 20% |
| All antibacterials | 1.012 (0.971–1.054) | 1.016 (0.970–1.064) | 1.004 (0.967–1.042) | 0.993 (0.962–1.025) | 47% |
| Vitamin D | 1.008 (0.989–1.029) | 1.011 (0.989–1.033) | 1.007 (0.989–1.026) | 1.004 (0.978–1.031) | 25% |
| Levothyroxine (negative control) | 0.970 (0.938–1.003) | 0.961 (0.930–0.994) | 0.971 (0.942–1.000) | 0.967 (0.909–1.030) | 0% |

Poisson PML with area and year fixed effects, adjusted for age structure, international in-migration, HIV and diabetes prevalence (diabetes not adjusted for metformin and insulins); SEs clustered by area. PAF, population attributable fraction implied by the upper 90% confidence limit.


**Largest attributable fraction compatible with the data** (upper 90% confidence limit)
- Systemic oral glucocorticoids: 18%
- Conventional DMARDs: 19%
- Transplant immunosuppressants: 4%

**Robustness**
- Upper-tier geography (151 areas, 1,661 area-years) gave similar results:
  - systemic oral glucocorticoids 0.987 (0.940–1.037); all FDR q ≥ 0.62
  - the negative control, levothyroxine, was nominally inverse at 0.961 (0.930–0.994), the same size as metformin (0.964, 0.929–1.000). This suggests residual confounding by trends.
- Apportioning prescribing by practice postcode gave similar results: lower-tier oral glucocorticoids 0.983 (0.948–1.019).
- Estimates were also materially unchanged by:
  - a three-year prior exposure window
  - adjustment for the LTBI programme or asylum support
  - excluding COVID-affected years
  - log population as a covariate
  - restricting to outcome years 2018–2024 (oral glucocorticoids 0.986, 0.944–1.030)
  - restricting to EPD-era exposure (0.991, 0.950–1.033)
  - ADQ instead of items (Table S1)
- Area-specific linear trends moved inhaled corticosteroids to 1.053 (1.003–1.105).

**Falsification tests** (prescribing in years t−1 and t+1 estimated jointly)
- Several drug groups showed opposite-signed lag and lead estimates, a pattern expected from shared trends rather than drug effects:
  - inhaled corticosteroids: t−1 1.076 (1.017–1.138), t+1 0.875 (0.837–0.914)
  - insulins: t−1 1.055 (1.006–1.106), t+1 0.903 (0.852–0.957)
  - systemic oral glucocorticoids: t+1 0.946 (0.906–0.987)
- Across all 195 estimates in the LTLA residence models, 11 were nominally significant, most of them lead or distributed-lag terms.

**Spatial dependence**
- Raw TB notification rates were strongly spatially clustered in every year (Moran's I 0.25–0.39 lower-tier; 0.40–0.49 upper-tier).
- Residuals from the primary model were not:
  - lower-tier: median I 0.028 (range −0.016 to 0.167), nominally significant in 3 of 11 years
  - upper-tier: median I 0.017, nominally significant in 1 of 11 years.

### Oral glucocorticoid prescribing trends and changes in TB notifications

**National trends, 2011–2024** (standard GP practices)
- Systemic oral glucocorticoid items rose from 115 to 132 per 1,000 residents in 2011–2016, then fell to 111 in 2024. Most of the fall came in 2020–21 (Figure 3).
- Prednisolone-equivalent mg per item fell from 225 to 192, so courses became smaller.
- Oral hydrocortisone items, mainly replacement therapy, rose from 5.3 to 9.1 per 1,000.

![**Figure 3.** Oral glucocorticoid prescribing in English primary care, 2011–2024: systemic oral glucocorticoid items, oral hydrocortisone items and prednisolone-equivalent mg per resident.](figures/ocs_national_trends.png)

**Correlation with national TB trends**
- National notification rates and prescribing were not correlated in levels (14 years; r = 0.17).
- Year-on-year changes were not correlated at lags of 0–2 years.
- At a 3-year lag, one of eight correlations was nominally significant and inverse (r = −0.75).

**Regional and local changes**
- In the regional panel (9 regions, 2012–2024), adjusted estimates were null:
  - items, lag 1: 1.008 (0.764–1.331); randomisation p = 0.95
  - prednisolone mg, lag 1: 1.064 (0.843–1.344).
- Across 140 upper-tier authorities, changes in prescribing (2014–16 to 2019–21) and in notifications (2014–16 to 2022–24) were weakly inversely related before adjustment (Spearman ρ = −0.17). After adjustment for change in in-migration they were unrelated (ratio per 10% 0.989, 0.925–1.057).

### Hospital medicines

**Coverage**
- After reassigning merged trusts to their successors, 98–100% of defined daily doses (DDD) in every drug group and year came from trusts with catchment data (Table S7).

**Positive control: active-TB treatment** (upper-tier authorities)
- Between areas: tracked notifications (Spearman ρ = 0.79; adjusted IRR per SD 1.17, 1.03–1.32).
- Within areas, same year: 1.035 (1.013–1.058) per 10% increase.
- Previous year: 1.005 (0.995–1.014). Following year, estimated jointly: 1.000 (0.988–1.012).
- The within-area elasticity was 0.36 (0.40 at lower-tier level): even a disease-specific drug was recovered with roughly 60% attenuation.
- Rifamycin/isoniazid products behaved similarly (same year 1.035).

![**Figure 5.** Positive control: hospital active-TB treatment (pyrazinamide/ethambutol-containing products, patient-year equivalents per 1,000 residents) and TB notifications between areas (left) and within areas over time (right).](figures/hospital_positive_control.png)

**Candidate drugs**
- No drug group with plausible TB risk was associated with notifications in the following year (Table 3). At upper-tier level, per 10% increase:

| Drug group | IRR, previous year |
|---|---|
| TNF inhibitors | 0.989 (0.972–1.006) |
| IL-6 inhibitors/abatacept | 1.000 (0.992–1.008) |
| JAK inhibitors | 0.994 (0.987–1.001) |
| Rituximab | 0.998 (0.985–1.011) |
| Calcineurin/mTOR inhibitors | 1.008 (0.996–1.020) |
| Antiproliferatives | 0.996 (0.978–1.014) |
| Systemic glucocorticoids | 1.019 (0.991–1.048) |

- The negative controls were null: low-TB-risk biologics 1.001 (0.985–1.018); levetiracetam 1.014 (0.985–1.043).
- Clustering by principal trust or using elective catchments barely changed the estimates.
- Lower-tier results were concordant.
- JAK inhibitors showed small inverse same-year estimates (0.993). These were not reproduced with previous-year or following-year exposure and are consistent with trends in uptake.

**Table 3. Hospital medicines (SCMD, patient-year equivalents per 1,000 residents) and TB notifications, 2019–2024**

| Level | Drug group | Cross-sectional, adjusted (per SD) | Within-area, same year (per 10%) | Elasticity (same year) | Within-area, previous year (per 10%) | Previous year, SE clustered by principal trust | Following year (joint with previous) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| UTLA | Active-TB treatment (pyrazinamide/ethambutol; positive control) | 1.165 (1.026–1.324) | 1.035 (1.013–1.058) | 0.36 | 1.005 (0.995–1.014) | 1.005 (0.995–1.014) | 1.000 (0.988–1.012) |
| UTLA | Rifamycin/isoniazid (active and latent TB, other infections) | 1.151 (1.032–1.284) | 1.035 (1.021–1.050) | 0.37 | 1.005 (0.993–1.018) | 1.005 (0.993–1.018) | 1.017 (0.994–1.040) |
| UTLA | TNF inhibitors | 0.956 (0.905–1.010) | 0.996 (0.979–1.013) | -0.04 | 0.989 (0.972–1.006) | 0.989 (0.970–1.008) | 0.978 (0.948–1.008) |
| UTLA | IL-6 inhibitors and abatacept | 0.972 (0.923–1.024) | 1.000 (0.990–1.010) | -0.00 | 1.000 (0.992–1.008) | 1.000 (0.993–1.008) | 1.001 (0.983–1.018) |
| UTLA | JAK inhibitors (rheumatology) | 0.974 (0.916–1.035) | 0.993 (0.987–0.999) | -0.07 | 0.994 (0.987–1.001) | 0.994 (0.986–1.002) | 0.998 (0.984–1.012) |
| UTLA | Rituximab | 0.942 (0.885–1.003) | 0.992 (0.979–1.006) | -0.08 | 0.998 (0.985–1.011) | 0.998 (0.987–1.009) | 1.007 (0.990–1.024) |
| UTLA | Calcineurin/mTOR inhibitors | 1.047 (0.992–1.105) | 0.994 (0.985–1.004) | -0.06 | 1.008 (0.996–1.020) | 1.008 (0.996–1.020) | 0.985 (0.966–1.005) |
| UTLA | Antiproliferatives | 1.023 (0.968–1.081) | 0.993 (0.978–1.008) | -0.07 | 0.996 (0.978–1.014) | 0.996 (0.979–1.014) | 0.993 (0.974–1.013) |
| UTLA | Systemic glucocorticoids | 0.950 (0.912–0.990) | 1.005 (0.977–1.033) | 0.05 | 1.019 (0.991–1.048) | 1.019 (0.987–1.053) | 0.985 (0.935–1.037) |
| UTLA | Low-TB-risk biologics (negative control) | 1.015 (0.962–1.072) | 1.004 (0.990–1.019) | 0.05 | 1.001 (0.985–1.018) | 1.001 (0.983–1.020) | 1.010 (0.981–1.039) |
| UTLA | Levetiracetam (negative control) | 1.016 (0.968–1.066) | 0.997 (0.975–1.020) | -0.03 | 1.014 (0.985–1.043) | 1.014 (0.986–1.043) | 0.985 (0.946–1.026) |
| LTLA | Active-TB treatment (pyrazinamide/ethambutol; positive control) | 1.090 (1.011–1.175) | 1.039 (1.017–1.062) | 0.40 | 1.002 (0.993–1.012) | 1.002 (0.993–1.012) | 0.999 (0.987–1.011) |
| LTLA | Rifamycin/isoniazid (active and latent TB, other infections) | 1.065 (1.000–1.135) | 1.038 (1.025–1.051) | 0.39 | 1.004 (0.992–1.016) | 1.004 (0.992–1.016) | 1.015 (0.995–1.036) |
| LTLA | TNF inhibitors | 0.967 (0.925–1.010) | 0.995 (0.979–1.010) | -0.06 | 0.992 (0.977–1.007) | 0.992 (0.977–1.007) | 0.975 (0.945–1.007) |
| LTLA | IL-6 inhibitors and abatacept | 0.944 (0.905–0.983) | 1.001 (0.991–1.011) | 0.01 | 1.001 (0.993–1.009) | 1.001 (0.993–1.009) | 0.996 (0.979–1.012) |
| LTLA | JAK inhibitors (rheumatology) | 0.948 (0.905–0.992) | 0.994 (0.989–1.000) | -0.06 | 0.996 (0.989–1.002) | 0.996 (0.989–1.002) | 0.999 (0.985–1.013) |
| LTLA | Rituximab | 0.971 (0.925–1.019) | 0.991 (0.977–1.005) | -0.10 | 1.001 (0.986–1.016) | 1.001 (0.988–1.014) | 1.006 (0.988–1.023) |
| LTLA | Calcineurin/mTOR inhibitors | 0.998 (0.955–1.043) | 0.994 (0.985–1.003) | -0.07 | 1.009 (0.997–1.021) | 1.009 (0.999–1.019) | 0.983 (0.960–1.005) |
| LTLA | Antiproliferatives | 0.982 (0.935–1.030) | 0.997 (0.983–1.012) | -0.03 | 0.997 (0.982–1.013) | 0.997 (0.980–1.015) | 0.993 (0.974–1.013) |
| LTLA | Systemic glucocorticoids | 0.967 (0.934–1.002) | 1.006 (0.980–1.034) | 0.07 | 1.020 (0.993–1.047) | 1.020 (0.990–1.051) | 0.973 (0.927–1.022) |
| LTLA | Low-TB-risk biologics (negative control) | 0.991 (0.948–1.036) | 1.005 (0.991–1.019) | 0.05 | 1.003 (0.988–1.018) | 1.003 (0.987–1.019) | 1.010 (0.983–1.038) |
| LTLA | Levetiracetam (negative control) | 1.013 (0.975–1.052) | 1.003 (0.981–1.025) | 0.03 | 1.012 (0.988–1.037) | 1.012 (0.989–1.035) | 0.989 (0.951–1.027) |


### Minimum detectable effects and expected population effects

**Primary care, oral glucocorticoids** (lower-tier panel)
- Minimum detectable effect (MDE): 6.3% per 10% increase in prescribing.
- Expected effect under published relative risks and prevalence: 0.34% (Table 2).
  - Stratified by age and place of birth: 0.29%.
  - Based on UKHSA-recorded steroid-associated notifications: 0.055%.
- The design could therefore detect only effects about 18–110 times larger than expected.
- The MDE corresponds to a drug responsible for more than half of all notifications.
- For the other candidate groups, MDEs exceeded expected effects by one to two orders of magnitude.

**Hospital medicines**
- MDEs were smaller (0.9–4.7% per 10% increase), but so were expected effects.
- TNF inhibitors (SCMD-derived prevalence 0.34%):
  - RR 4 without latent TB screening implies an expected change of 0.10% (MDE 25× larger).
  - A screening-attenuated RR implies 0.02% (MDE 113× larger).
  - Further attenuation by the positive-control elasticity widens these gaps (Table S3).
- UKHSA-recorded biologic-associated notifications imply 0.098%.

**Simulation** (permutation-based, real notification counts; Table S4)
- **Calibration.**
  - False-positive rate: 7.0% at lower-tier level (6.8% upper-tier).
  - Empirical null SD: 0.0158, against a real-data SE of 0.0218. The clustered SEs are therefore conservative for the estimate, but the slightly raised false-positive rate shows that permuted exposure histories still produce spurious associations with the real notification trends.
- **Published glucocorticoid effect (RR 4.9).** Power 7.7% (upper-tier 9.0%).
- **Larger individual relative risks.** Power 20.7% for RR 25 and 78.3% for RR 100.
- **Direct population effects.** Power 21.0% for IRR 1.02 per 10%, 85.0% for 1.05 and 100.0% for 1.10.
- **Effect acting through same-year prescribing** (analysed with previous-year exposure). Power 60.7% for 1.05 and 99.7% for 1.10.

**Table 2. Minimum detectable effects (LTLA panel, residence apportionment, exposure t−1) versus expected population effects of a 10% increase in use**

| Drug group | Individual RR/OR | Prevalence of use | PAF | Expected change | MDE | MDE ÷ expected | Power | Minimum detectable PAF | RR for 80% power |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Systemic oral glucocorticoids | 4.9 | 0.9% | 3.4% | 0.34% | 6.3% | 18 | 3.6% | 63% | 191 |
| Inhaled corticosteroids | 1.27 | 5.2% | 1.4% | 0.14% | 7.0% | 49 | 2.9% | 70% | 47 |
| Conventional DMARDs | 1.2 | 0.5% | 0.1% | 0.01% | 2.8% | 274 | 2.6% | 28% | 78 |
| Proton pump inhibitors | 1.28 | 14.2% | 3.8% | 0.38% | 6.3% | 16 | 3.7% | 63% | 13 |
| Statins | 0.6 | 12.8% | -5.4% | -0.54% | 6.0% | 11 | 4.5% | 60% | not attainable |
| Metformin | 0.51 | 4.4% | -2.2% | -0.22% | 4.7% | 21 | 3.4% | 47% | not attainable |

Expected changes use published individual-level relative risks (ORs for oral glucocorticoids and PPIs) and UK prevalence of use, assuming prevalence scales with prescribing and a homogeneous baseline risk (which favours detection). Power is one-sided power to detect the expected effect in the correct direction. Benchmarks: recorded cases (steroids), UKHSA 2024: 0.055%; recorded cases (biological_therapy), UKHSA 2024: 0.098%; stratified by age and birthplace (oral corticosteroids, RR 4.9): 0.293%; homogeneous (oral corticosteroids, RR 4.9, prevalence 0.9%): 0.339%.


### Regional analyses by place of birth and age

**Non-UK-born notifications**
- Oral glucocorticoid prescribing in earlier years was not associated with notifications (lag 1–3: 0.92–1.02).
- The falsification test failed: prescribing three years later predicted earlier notifications (1.49, 1.17–1.90; randomisation p = 0.01).

**UK-born notifications**
- Prednisolone-equivalent mg:
  - Lagged estimates were imprecise positive values (lag 2: 1.30, 0.97–1.75; randomisation p = 0.08).
  - With lag and lead estimated jointly, lag 1.41 and lead 0.85 (difference p = 0.04; randomisation p for lag = 0.04) (Table S6).
- Oral glucocorticoid items: null (lag 2 joint 1.22).

**UK-born notifications at age ≥65**
- Glucocorticoid prescribing was not associated with notifications.
- The falsification test failed for glucocorticoid items (lead 2: 1.74, 0.99–3.07; randomisation p = 0.03).
- The negative control failed in both directions: levothyroxine lag 1 1.23 (1.00–1.50; p = 0.05) and lead 1 1.37 (1.04–1.79; p = 0.01).

**Interpretation of the one nominal association**
- The UK-born association with prednisolone mg is implausibly large. Under the model used for expected effects, a 10% increase in use can raise incidence by at most 10%.
- Falsification tests and the negative control failed at similar magnitudes in the same regional design.
- We therefore interpret it as residual confounding by regional trends in a nine-cluster design, not a drug effect.

![**Figure 6.** Oral glucocorticoid prescribing and UK-born TB notification rates by region, indexed to 2014 = 100.](figures/ocs_ukborn_tb_by_region.png)


## Discussion

### Principal findings

We linked open English data on primary care and hospital prescribing with TB notifications, using several ecological designs at two geographic scales. The linkage worked only partly.

- **The positive control.** Hospital active-TB treatment tracked notifications between and within areas, but even this disease-specific signal was recovered with roughly 60% attenuation.
- **Candidate drugs.** No medicine plausibly affecting TB risk was associated with subsequent notifications. This held for systemic oral glucocorticoids, inhaled corticosteroids, DMARDs, transplant immunosuppressants, TNF, IL-6 and JAK inhibitors, and rituximab.
- **Signs of confounding.**
  - The negative-control exposure showed inverse estimates of similar size to some candidate drugs.
  - Several falsification tests failed.
  - The one nominal regional association was implausibly large.

  These patterns point to residual confounding by area-specific trends, not drug effects.
- **Power.** The analytic calculations and the simulation agreed: the designs could detect only effects one to two orders of magnitude larger than those implied by published relative risks or by UKHSA records of drug-associated TB.

### Why population effects of these medicines are undetectable

**Expected effects are small.** The population effect of a medicine is roughly its attributable fraction scaled by the relative change in use.

- **Oral glucocorticoids.** Current use carries an odds ratio of about 5 [Jick 2006], but only about 1% of people use them at any time [van Staa 2000; Fardet 2011]. A 10% change in use should therefore change TB notifications by about 0.3%.
  - Stratifying by age and place of birth lowers this to 0.29%, because use is concentrated in older UK-born people with low baseline risk.
  - UKHSA recorded steroid-associated immunosuppression in 30 of 5,490 people notified in 2024 [UKHSA 2025]. Even allowing for under-recording, that implies 0.05–0.1%.
- **Biologics.** Latent TB screening before anti-TNF therapy has been standard in the UK since 2005 [BTS 2005] and reduced TB risk by about 78% in registry data [Carmona 2005; Gómez-Reino 2007]. Growth in biologic use during 2019–2024 therefore took place under screening, so the relative risk relevant to a marginal increase in use is small. Oral glucocorticoids rarely trigger screening.

**The data carry little information.**
- **Little within-area variation.** Within-area variation in prescribing was very small (SD of log rate 0.04 for glucocorticoids, against 0.29 between areas), so a 10% change sits at the edge of the observed data. Fixed effects remove the between-area variation where most information lies [Gunasekara 2014].
- **Few areas.** Power in aggregate studies depends mainly on the number of areas [Sheppard 1996], which cannot be increased.
- **Linkage attenuation.** The positive control shows that attenuation from apportionment and dilution would shrink any true effect further.
- **Simulation.** Simulations that preserved the real error structure found power close to the false-positive rate for the published glucocorticoid effect.

### Confounding, falsification and negative controls

**Crude versus within-area associations.** Crude cross-sectional associations were strongly inverse and were explained by country of birth and age. Within areas, residual confounding remained visible:
- **Negative control.** Levothyroxine, which has no plausible effect on TB, showed inverse estimates (0.96–0.97) similar to metformin.
- **Opposite-signed lag and lead.** Inhaled corticosteroids and insulins had opposite-signed estimates when prescribing before and after the outcome year was estimated jointly.
- **Likely cause.** Both patterns are expected when prescribing and notifications share area-specific trends, for example migration-driven changes in the age and origin of the population, changes in registration or diagnostic activity, and prescribing policy. Year fixed effects cannot remove these trends.

**Ecological bias.** Area-level adjustment cannot remove bias arising from effect modification or from differences in baseline risk between people within areas [Greenland 1989; Morgenstern 1995]. For example, steroid users are mostly older and UK-born, whereas most notifications are in younger people born abroad.

**The UK-born association.** Regionally, prednisolone dose was associated with UK-born TB when prescribing before and after was estimated jointly (randomisation p = 0.04). We do not interpret this as a drug effect:
- An IRR of 1.41 per 10% increase exceeds the maximum possible under any relative risk (1.10) in the model used for expected effects.
- The same nine-region design produced failed falsification tests for non-UK-born TB.
- It also produced a failed negative control (levothyroxine) for older UK-born people.
- UK-born TB fell by 43% between 2014 and 2022, reflecting social risk factors, transmission and demographic change [Davidson 2018; UKHSA 2025]. Coincident regional trends in steroid dosing are the most plausible explanation.

**Protopathic bias.** Glucocorticoids and antibacterials prescribed for undiagnosed TB, and glucocorticoids used in treating TB meningitis and pericarditis [Thwaites 2004], create reverse associations in the same year. This is why the primary exposure was prescribing in the previous year. The same bias probably inflates the individual-level estimates used to derive expected effects [Jick 2006]; if so, the true gap between expected and detectable effects is even wider.

### Strengths and limitations

**Strengths.**
- **Open and reproducible.** All data are public, and code and processed data are openly available.
- **Exposure measurement.**
  - Primary care exposure was defined at presentation level, with dose measures, and apportioned by where registered patients live.
  - Hospital medicines were classified by mechanism using defined daily doses, with trust mergers resolved.
- **Checks on validity.**
  - A disease-specific positive control, negative-control exposures and falsification tests estimated jointly.
  - Randomisation inference for the nine-region analyses.
  - Year-specific spatial diagnostics.
  - Power assessed both analytically and by simulation on the real data.
- **Independent peer review.** Three independent reviews prompted substantial revision.

**Limitations: exposure data.**
- **Prescribing measures.** Exposure was measured as prescribing volume per resident, not as people treated.
- **Apportionment.** Apportioning by patient residence used annual April snapshots, with 2014 shares applied to 2011–2013.
- **Pre-2014 data.** The 2011–2013 series come from a different release, and overlap-period concordance could not be assessed. National year-on-year changes were continuous across the 2013/2014 splice for most groups, but not for oral glucocorticoids (+3.3% at the splice against +0.6% and +1.0% either side) or all antibacterials (−0.1% against −4.5% and −5.6%). Restricting to EPD-era exposure did not change the conclusions (Table S1).
- **Hospital catchments.** Hospital quantities were apportioned using admission-based catchments, which may misallocate specialist services.
- **Hospital data capture.** Capture of homecare-delivered biologics in SCMD could not be verified.
- **Hospital data period.** The hospital series spans only 2019–2024, including the pandemic.

**Limitations: outcome and confounder data.**
- **Notifications, not incidence.** The outcome is notified TB, subject to diagnostic delay, residence assignment, the 2021 transition from ETS to NTBS, and 2020 disruption.
- **Birthplace data.** TB by place of birth is published only by region, and UK-born population denominators by age are not published regionally.
- **Unmeasured confounders.**
  - Social risk factors and diagnostic intensity.
  - The area-level share of recent arrivals.
  - Latent TB programme activity after 2019/20.

**Limitations: design and analysis.**
- **Pre-specification.** Many analyses were added after initial null results and are exploratory.
- **Expected-effect inputs.** Relative risks for PPIs, statins and metformin come mainly from high-incidence settings, and prevalence inputs for hospital drugs are derived or illustrative. Neither would change the conclusions unless the true effects were an order of magnitude larger.

### Implications

**For research.**
- Open prescribing data are valuable for describing prescribing [Bacon 2020; OpenPrescribing 2026] but cannot estimate the effects of medicines on rare outcomes such as TB.
- Ecological studies of rare outcomes should report the following alongside any associations:
  - minimum detectable effects;
  - a positive control with its elasticity;
  - negative controls;
  - falsification tests.
- Causal questions need individual-level linked data analysed with target trial emulation (Box). Even national cohorts give wide intervals for modest relative risks [Pealing 2015]. The only drug–TB target trial emulation we identified concerned DPP-4 inhibitors [Chen 2025].

**For TB programmes.**
- **The null results do not mean these drugs are safe.** Glucocorticoids, biologics and JAK inhibitors remain important for individual patients. Drug-associated TB is serious, often extrapulmonary, and largely preventable.
- **Surveillance.** Monitoring is better served by more complete and detailed immunosuppression fields in NTBS than by ecological analysis of prescribing. Useful fields would record drug class, time since starting, and whether latent TB screening was done and treated.
- **Audit.** The practical lever is auditing latent TB screening before biologics, JAK inhibitors and high-dose, long-term glucocorticoids.
- **Aggregate data from UKHSA.** Aggregate UKHSA tables would allow population monitoring in the groups where drug-associated reactivation matters, namely:
  - notifications with recorded biologic or steroid immunosuppression;
  - notifications by area, year, place of birth, age and time since entry.

### Conclusion

Open English prescribing and TB notification data can be linked, but with heavy attenuation. Ecological analyses of these data cannot detect the population-level effects of medicines on TB: plausible effects lie one to two orders of magnitude below what the designs can resolve, and the apparent associations that do arise reflect confounding by migration and area-specific trends.

### Box. Individual-level target trial emulation (example: oral glucocorticoids and TB)

**Data**
- CPRD Aurum (primary care prescribing with dose and quantity).
- Hospital Episode Statistics (admitted patient care and outpatients) and ONS deaths.
- Small-area deprivation.
- A bespoke linkage to the UKHSA National TB Surveillance System, which provides notification-validated
  TB, site of disease, culture confirmation, and country of birth and year of entry.
- Hospital-only drugs (biologics, JAK inhibitors) are not captured in CPRD. For these, use NHS England
  high-cost drugs data (e.g. via OpenSAFELY) or disease registries (BSRBR-RA, BADBIR, UK IBD Registry)
  with the same TB linkage.

**Eligibility**
- Adults aged ≥18 years with ≥12 months' registration.
- No previous TB, TB or latent TB treatment, or oral glucocorticoid use in the previous 12 months.
- No HIV or solid organ transplant.
- Defined indication cohorts (e.g. polymyalgia rheumatica/giant cell arteritis, rheumatoid arthritis,
  COPD, asthma, inflammatory bowel disease).

**Treatment strategies**
- Initiate and sustain oral glucocorticoids for ≥3 months, by prednisolone-equivalent dose (<7.5,
  7.5–<15, ≥15 mg/day), versus no initiation.
- An active comparator where available.

**Assignment and time zero**
- Sequential monthly nested trials.
- Clone–censor–weight methods for sustained-use and dose strategies.

**Outcome**
- Incident active TB: the first of an NTBS notification, a HES diagnosis (ICD-10 A15–A19), or a CPRD
  diagnosis with treatment.
- Secondary: pulmonary vs extrapulmonary, culture-confirmed TB, TB death.

**Follow-up**
- Up to 5 years, or until death, deregistration or end of linkage.

**Estimands and analysis**
- Intention-to-treat and per-protocol cumulative incidence differences and ratios at 1, 2 and 5 years.
- Pooled logistic regression with inverse probability of treatment and censoring weights.

**Confounders**
- Age, sex, ethnicity, country of birth and time since entry, deprivation.
- Diabetes, chronic kidney disease, smoking, alcohol, BMI.
- TB contact or latent TB screening codes.
- Indication severity, healthcare use, co-prescribed immunosuppressants.

**Effect modification and bias checks**
- Effect modification by country of birth, specified in advance.
- Negative-control exposure (levothyroxine initiation) and negative-control outcome.
- E-values.

**Feasibility**
- Baseline TB incidence in older UK-born adults is about 2–5 per 100,000 person-years. Tens of
  thousands of long-term initiators followed for several years would yield only tens of TB events,
  so the individual-level study is itself constrained by sample size.



## Data and code availability

All inputs are publicly available (NHSBSA Open Data Portal: English Prescribing Dataset and Secondary Care Medicines Data; NHS Digital practice-level prescribing and registered patients by LSOA; UKHSA TB reports and Fingertips; OHID acute trust catchment populations; ONS/Nomis; Home Office asylum statistics; NHS England ODS; MHCLG English Indices of Deprivation). Code, processed datasets and outputs: https://github.com/drcjar/tb-prescribing-england.


## References (draft 3, verified 14 September 2026; ordered alphabetically, to be renumbered on assembly)

Each journal entry was checked against PubMed metadata (via DOI→PMID conversion or citation lookup) and Crossref DOI metadata. Each DOI below resolves to the stated article. The grey literature was checked on GOV.UK, in the report PDF, or through search results where a site blocks automated access. Corrections relative to references_v3.md are listed at the end.

- Aldridge RW, Zenner D, White PJ, et al. Tuberculosis in migrants moving from high-incidence to low-incidence countries: a population-based cohort study of 519 955 migrants screened before entry to England, Wales, and Northern Ireland. *Lancet* 2016;388(10059):2510–8. doi:10.1016/S0140-6736(16)31008-X. PMID 27742165
- Bacon S, Goldacre B. Barriers to working with National Health Service England's open data. *J Med Internet Res* 2020;22(1):e15603. doi:10.2196/15603. PMID 31929101
- Berrocal-Almanza LC, Harris RJ, Collin SM, et al. Effectiveness of nationwide programmatic testing and treatment for latent tuberculosis infection in migrants in England: a retrospective, population-based cohort study. *Lancet Public Health* 2022;7(4):e305–15. doi:10.1016/S2468-2667(22)00031-7. PMID 35338849
- Brassard P, Kezouh A, Suissa S. Antirheumatic drugs and the risk of tuberculosis. *Clin Infect Dis* 2006;43(6):717–22. doi:10.1086/506935. PMID 16912945
- Brassard P, Suissa S, Kezouh A, Ernst P. Inhaled corticosteroids and risk of tuberculosis in patients with respiratory diseases. *Am J Respir Crit Care Med* 2011;183(5):675–8. doi:10.1164/rccm.201007-1099OC. PMID 20889902
- British Thoracic Society Standards of Care Committee. BTS recommendations for assessing risk and for managing *Mycobacterium tuberculosis* infection and disease in patients due to start anti-TNF-α treatment. *Thorax* 2005;60(10):800–5. doi:10.1136/thx.2005.046797. PMID 16055611
- Carmona L, Gómez-Reino JJ, Rodríguez-Valverde V, et al. Effectiveness of recommendations to prevent reactivation of latent tuberculosis infection in patients treated with tumor necrosis factor antagonists. *Arthritis Rheum* 2005;52(6):1766–72. doi:10.1002/art.21043. PMID 15934089
- Castellana G, Castellana M, Castellana C, et al. Inhaled corticosteroids and risk of tuberculosis in patients with obstructive lung diseases: a systematic review and meta-analysis of non-randomized studies. *Int J Chron Obstruct Pulmon Dis* 2019;14:2219–27. doi:10.2147/COPD.S209273. PMID 31576118
- Chen YG, et al. Target trial emulation of DPP-4 inhibitors in patients with T2DM for pulmonary tuberculosis: a nationwide observational data. *BMC Med* 2025;23:587. doi:10.1186/s12916-025-04423-1. PMID 41137015
- Davidson JA, Thomas HL, Maguire H, et al. Understanding tuberculosis transmission in the United Kingdom: findings from 6 years of mycobacterial interspersed repetitive unit-variable number tandem repeats strain typing, 2010–2015. *Am J Epidemiol* 2018;187(10):2233–42. doi:10.1093/aje/kwy119. PMID 29878041
- Dixon WG, Hyrich KL, Watson KD, et al. Drug-specific risk of tuberculosis in patients with rheumatoid arthritis treated with anti-TNF therapy: results from the British Society for Rheumatology Biologics Register (BSRBR). *Ann Rheum Dis* 2010;69(3):522–8. doi:10.1136/ard.2009.118935. PMID 19854715
- Fardet L, Petersen I, Nazareth I. Prevalence of long-term oral glucocorticoid prescriptions in the UK over the past 20 years. *Rheumatology (Oxford)* 2011;50(11):1982–90. doi:10.1093/rheumatology/ker017. PMID 21393338
- Gómez-Reino JJ, Carmona L, Angel Descalzo M, et al. [PubMed lists a fourth, collective author whose name was not returned; probably the BIOBADASER group, unconfirmed] Risk of tuberculosis in patients treated with tumor necrosis factor antagonists due to incomplete prevention of reactivation of latent infection. *Arthritis Rheum* 2007;57(5):756–61. doi:10.1002/art.22768. PMID 17530674
- Greenland S, Morgenstern H. Ecological bias, confounding, and effect modification. *Int J Epidemiol* 1989;18(1):269–74. doi:10.1093/ije/18.1.269. PMID 2656561
- Gunasekara FI, Richardson K, Carter K, Blakely T. Fixed effects analysis of repeated measures data. *Int J Epidemiol* 2014;43(1):264–9. doi:10.1093/ije/dyt221. PMID 24366487
- Hermans S, Boulle A, Caldwell J, et al. Temporal trends in TB notification rates during ART scale-up in Cape Town: an ecological analysis. *J Int AIDS Soc* 2015;18(1):20240. doi:10.7448/IAS.18.1.20240. PMID 26411694
- Hudson SM, Hudson C. Is GP practice bowel, breast and cervical cancer screening coverage correlated with GP practice list inflation? *J Med Screen* 2026;33(1):1–8 (epub 17 June 2025). doi:10.1177/09691413251347408. PMID 40525516
- Jick SS, Lieberman ES, Rahman MU, Choi HK. Glucocorticoid use, other associated factors, and the risk of tuberculosis. *Arthritis Rheum* 2006;55(1):19–26. doi:10.1002/art.21705. PMID 16463407
- Keane J, Gershon S, Wise RP, et al. Tuberculosis associated with infliximab, a tumor necrosis factor α-neutralizing agent. *N Engl J Med* 2001;345(15):1098–104. doi:10.1056/NEJMoa011110. PMID 11596589
- Költringer FA, et al. The social determinants of national tuberculosis incidence rates in 116 countries: a longitudinal ecological study between 2005–2015. *BMC Public Health* 2023;23:337. doi:10.1186/s12889-023-15213-w. PMID 36793018
- Li X, Sheng L, Lou L. Statin use may be associated with reduced active tuberculosis infection: a meta-analysis of observational studies. *Front Med (Lausanne)* 2020;7:121. doi:10.3389/fmed.2020.00121. PMID 32391364
- Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative controls: a tool for detecting confounding and bias in observational studies. *Epidemiology* 2010;21(3):383–8. doi:10.1097/EDE.0b013e3181d61eeb. PMID 20335814
- Loutet MG, Burman M, Jayasekera N, et al. National roll-out of latent tuberculosis testing and treatment for new migrants in England: a retrospective evaluation in a high-incidence area. *Eur Respir J* 2018;51(1):1701226. doi:10.1183/13993003.01226-2017. PMID 29326327
- Morgenstern H. Ecologic studies in epidemiology: concepts, principles, and methods. *Annu Rev Public Health* 1995;16:61–81. doi:10.1146/annurev.pu.16.050195.000425. PMID 7639884
- Morrison H, et al. Impact of COVID-19 on NHS tuberculosis services: results of a UK-wide survey. *J Infect* 2023;87(1):59–61. doi:10.1016/j.jinf.2023.04.004. PMID 37044162
- National Institute for Health and Care Excellence. Tuberculosis. NICE guideline [NG33]. London: NICE; published 13 January 2016, last updated 16 February 2024. https://www.nice.org.uk/guidance/ng33 [dates confirmed from search results only; nice.org.uk returned HTTP 403 to automated access. The wording of the LTBI testing recommendation still needs checking by hand against the current text.]
- Nguipdop-Djomo P, Rodrigues LC, Abubakar I, Mangtani P. Small-area level socio-economic deprivation and tuberculosis rates in England: an ecological analysis of tuberculosis notifications between 2008 and 2012. *PLoS One* 2020;15(10):e0240879. doi:10.1371/journal.pone.0240879. PMID 33075092
- OpenPrescribing.net, Bennett Institute for Applied Data Science, University of Oxford. Frequently asked questions. 2026. https://openprescribing.net/faq/ [accessed date to be added; the FAQ asks academic users to cite "OpenPrescribing.net, Bennett Institute for Applied Data Science, University of Oxford, 2026", confirmed via search results because a direct fetch failed]
- Pealing L, Wing K, Mathur R, et al. Risk of tuberculosis in patients with diabetes: population based cohort study using the UK Clinical Practice Research Datalink. *BMC Med* 2015;13:135. doi:10.1186/s12916-015-0381-9. PMID 26048371
- Prasad V, Jena AB. Prespecified falsification end points: can they validate true observational associations? *JAMA* 2013;309(3):241–2. doi:10.1001/jama.2012.96867. PMID 23321761
- RECOVERY Collaborative Group; Horby P, Lim WS, Emberson JR, et al. Dexamethasone in hospitalized patients with Covid-19. *N Engl J Med* 2021;384(8):693–704. doi:10.1056/NEJMoa2021436. PMID 32678530
- Richards TC, et al. Using OpenPrescribing.net to evaluate neighbourhood-level prescribing of inhalers for asthma and COPD. *Sci Rep* 2025;15:18089. doi:10.1038/s41598-025-02969-x. PMID 40413267
- Santos Silva JMC, Tenreyro S. The log of gravity. *Rev Econ Stat* 2006;88(4):641–58. doi:10.1162/rest.88.4.641 (not indexed in PubMed)
- Sheppard L, Prentice RL, Rossing MA. Design considerations for estimation of exposure effects on disease risk, using aggregate data studies. *Stat Med* 1996;15(17-18):1849–58. doi:10.1002/(SICI)1097-0258(19960915)15:17<1849::AID-SIM396>3.0.CO;2-4. PMID 8888477
- Song HJ, Park H, Park S, Kwon JW. The association between proton pump inhibitor use and the risk of tuberculosis: a case-control study. *Pharmacoepidemiol Drug Saf* 2019;28(6):830–9. doi:10.1002/pds.4773. PMID 30920070
- Thomas HL, Harris RJ, Muzyamba MC, et al. Reduction in tuberculosis incidence in the UK from 2011 to 2015: a population-based study. *Thorax* 2018;73(8):769–75. doi:10.1136/thoraxjnl-2017-211074. PMID 29674389
- Thwaites GE, Nguyen DB, Nguyen HD, et al. Dexamethasone for the treatment of tuberculous meningitis in adolescents and adults. *N Engl J Med* 2004;351(17):1741–51. doi:10.1056/NEJMoa040573. PMID 15496623
- UK Health Security Agency. Tuberculosis in England: 2021 report (presenting data to end of 2020). London: UKHSA; 2021 (added to GOV.UK 28 October 2021; corrected PDF 30 March 2022). https://assets.publishing.service.gov.uk/media/62441310e90e075f124018e8/TB_annual-report-2021.pdf [The PDF reports "In 2020, 4,125 people were notified with TB in England, with a rate of 7.3 per 100,000 population". Its suggested citation is "UK Health Security Agency. (2021) Tuberculosis in England: 2020. UK Health Security Agency, London."]
- UK Health Security Agency. Tuberculosis in England: 2025 report (data up to end of 2024), chapter 1 and supplementary tables 5, 12 and 22; and TB regional reports 2024, supplementary data. London: UKHSA; first published 8 October 2025 (GOV.UK change history; the content API timestamp reads 9 October 2025 BST), last updated 15 July 2026. https://www.gov.uk/government/publications/tuberculosis-in-england-2025-report [the GOV.UK page title reads "Tuberculosis in England, 2025 report". The specific supplementary table numbers and the regional reports publication were not individually checked.]
- UK Health Security Agency. Tuberculosis notifications in England stabilise in 2025. News story, 29 January 2026. https://www.gov.uk/government/news/tuberculosis-notifications-in-england-stabilise-in-2025 [confirmed: "5,424 people notified compared to 5,487 in 2024 – a decrease of 1.1%"; rate 9.4 per 100,000]
- van Staa TP, Leufkens HG, Abenhaim L, et al. Use of oral corticosteroids in the United Kingdom. *QJM* 2000;93(2):105–11. doi:10.1093/qjmed/93.2.105. PMID 10700481
- Venkatesan S, et al. Correcting for the inflated adult population denominator in an English nationwide health care cohort: database analysis study. *JMIR Public Health Surveill* 2025;11:e64788. doi:10.2196/64788. PMID 41144579
- Zhang M, He JQ. Impacts of metformin on tuberculosis incidence and clinical outcomes in patients with diabetes: a systematic review and meta-analysis. *Eur J Clin Pharmacol* 2020;76(2):149–59. doi:10.1007/s00228-019-02786-y. PMID 31786617

### Corrections made relative to references_v3.md
- Thomas HL 2018: the title was wrong. The actual title is "Reduction in tuberculosis incidence in the UK from 2011 to 2015: a population-based study". Volume and pages (73:769–75) were correct.
- Költringer 2023: the placeholder title was replaced, and the article number is 337, not 311.
- Castellana 2019: the full title ends "...meta-analysis of non-randomized studies".
- Song 2019: the title was wrong. The actual title is "The association between proton pump inhibitor use and the risk of tuberculosis: a case-control study".
- Hudson 2025: there are only two authors (Hudson SM, Hudson C), so "et al." was removed. The print issue is 2026;33(1):1–8, epub 2025.
- Placeholder titles were replaced for Chen (BMC Med 2025;23:587), Hermans, Richards (Sci Rep 2025;15:18089), Sheppard (Stat Med 1996;15:1849–58, authors Sheppard, Prentice, Rossing) and Venkatesan (2025;11:e64788).
- Tuberculosis in England 2021 report: it was published by the UK Health Security Agency, not Public Health England. The document and its suggested citation both name UKHSA, and UKHSA replaced PHE on 1 October 2021, before the report was added on 28 October 2021.
- Added the Santos Silva DOI, all PMIDs and issue numbers, and the NICE NG33 publication and update dates.

### Could not be fully verified
- NICE NG33: nice.org.uk blocks automated access (HTTP 403). The 16 February 2024 last-updated date comes from search results only, and the LTBI recommendation wording must be checked by hand.
- The OpenPrescribing FAQ page could not be fetched directly. Its content was confirmed through search results only.
- UKHSA 2025 report: which supplementary tables are numbered 5, 12 and 22, and the "TB regional reports 2024" supplementary data, were not individually checked.
- The full author lists of the "et al." entries (Chen, Költringer, Morrison, Richards, Venkatesan) were not expanded. The PubMed records list 9, 5, 10, 5 and 14 authors respectively.


## Supplementary tables

**Table S1. Sensitivity analyses, LTLA panel (residence apportionment): IRR per 10% increase (95% CI)**

| Drug group | primary (t-1) | FE only (t-1) | prior 3 years (t-3..t-1) | + area trends (t-1) | population covariate (t-1) | + LTBI programme (t-1) | + asylum support (t-1) | exclude COVID years (t-1) | outcome years 2018-2024 (t-1) | EPD exposure only (t-1) | ADQ measure (t-1) |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Antituberculosis (descriptive) | 1.000 (0.997–1.003) | 1.002 (0.998–1.005) | 1.001 (0.997–1.005) | 0.999 (0.996–1.003) | 1.000 (0.997–1.004) | 1.000 (0.997–1.004) | 1.001 (0.998–1.004) | 1.000 (0.997–1.004) | 1.001 (0.998–1.004) | 1.001 (0.998–1.004) | — |
| Systemic oral glucocorticoids | 0.982 (0.941–1.025) | 0.972 (0.925–1.021) | 0.988 (0.941–1.037) | 0.999 (0.945–1.057) | 0.984 (0.943–1.028) | 0.983 (0.941–1.028) | 0.993 (0.949–1.039) | 0.990 (0.947–1.035) | 0.986 (0.944–1.030) | 0.991 (0.950–1.033) | — |
| Oral hydrocortisone | 1.002 (0.990–1.014) | 0.996 (0.982–1.012) | 1.000 (0.984–1.016) | 1.002 (0.984–1.019) | 1.003 (0.991–1.016) | 1.002 (0.990–1.014) | 0.996 (0.984–1.009) | 1.002 (0.987–1.017) | 0.994 (0.978–1.011) | 0.998 (0.987–1.010) | — |
| Oral dexamethasone | 1.004 (0.994–1.015) | 1.006 (0.994–1.018) | 1.009 (0.994–1.025) | 0.996 (0.986–1.007) | 1.004 (0.994–1.015) | 1.005 (0.994–1.015) | 1.003 (0.993–1.014) | 1.009 (0.998–1.020) | 0.998 (0.986–1.010) | 1.004 (0.994–1.014) | — |
| Inhaled corticosteroids | 0.981 (0.935–1.029) | 0.952 (0.905–1.001) | 0.999 (0.947–1.053) | 1.053 (1.003–1.105) | 0.984 (0.935–1.034) | 0.982 (0.936–1.030) | 0.964 (0.921–1.008) | 0.977 (0.930–1.026) | 0.948 (0.902–0.996) | 0.970 (0.929–1.013) | 0.975 (0.952–0.999) |
| Conventional DMARDs | 1.003 (0.984–1.023) | 1.005 (0.985–1.026) | 1.004 (0.984–1.026) | 1.022 (0.985–1.060) | 1.003 (0.984–1.022) | 1.003 (0.984–1.022) | 0.998 (0.980–1.016) | 1.006 (0.987–1.026) | 1.003 (0.979–1.026) | 1.001 (0.985–1.018) | — |
| Transplant immunosuppressants | 0.999 (0.993–1.005) | 0.997 (0.991–1.003) | 1.000 (0.993–1.007) | 1.001 (0.993–1.008) | 0.999 (0.993–1.005) | 0.999 (0.993–1.005) | 0.999 (0.993–1.005) | 1.001 (0.995–1.008) | 1.001 (0.994–1.008) | 1.000 (0.995–1.006) | — |
| Proton pump inhibitors | 1.009 (0.967–1.054) | 0.975 (0.930–1.022) | 1.006 (0.960–1.055) | 0.988 (0.932–1.048) | 1.011 (0.965–1.059) | 1.014 (0.970–1.060) | 0.997 (0.952–1.044) | 1.006 (0.961–1.054) | 0.947 (0.888–1.010) | 1.001 (0.958–1.046) | 1.000 (0.938–1.065) |
| Statins | 1.000 (0.960–1.041) | 0.974 (0.933–1.017) | 0.995 (0.952–1.041) | 0.996 (0.944–1.051) | 0.999 (0.959–1.041) | 1.005 (0.964–1.047) | 1.009 (0.965–1.054) | 0.991 (0.951–1.034) | 0.997 (0.936–1.063) | 1.009 (0.969–1.051) | 1.002 (0.963–1.043) |
| Metformin | 0.969 (0.938–1.001) | 0.953 (0.921–0.986) | 0.968 (0.933–1.004) | 0.966 (0.925–1.009) | 0.970 (0.938–1.003) | 0.974 (0.942–1.008) | 0.977 (0.942–1.014) | 0.965 (0.935–0.997) | 0.985 (0.931–1.042) | 0.977 (0.944–1.011) | 0.991 (0.941–1.044) |
| Insulins | 0.981 (0.945–1.019) | 0.980 (0.941–1.020) | 0.989 (0.948–1.030) | 1.042 (0.980–1.109) | 0.986 (0.944–1.029) | 0.983 (0.947–1.022) | 0.980 (0.936–1.027) | 0.979 (0.940–1.020) | 0.982 (0.915–1.054) | 0.985 (0.944–1.028) | — |
| Fluoroquinolones | 1.010 (0.997–1.023) | 1.010 (0.995–1.024) | 1.011 (0.998–1.025) | 1.008 (0.994–1.023) | 1.011 (0.998–1.024) | 1.009 (0.997–1.022) | 1.008 (0.995–1.021) | 1.006 (0.992–1.020) | 0.995 (0.976–1.015) | 1.006 (0.994–1.019) | 1.004 (0.992–1.016) |
| All antibacterials | 1.012 (0.971–1.054) | 1.009 (0.961–1.058) | 1.023 (0.980–1.069) | 0.995 (0.955–1.037) | 1.015 (0.976–1.056) | 1.007 (0.965–1.051) | 1.005 (0.964–1.046) | 1.030 (0.984–1.078) | 0.957 (0.914–1.002) | 1.007 (0.968–1.048) | 1.007 (0.970–1.045) |
| Vitamin D | 1.008 (0.989–1.029) | 1.011 (0.988–1.034) | 1.009 (0.988–1.030) | 0.986 (0.962–1.010) | 1.010 (0.991–1.030) | 1.006 (0.985–1.027) | 1.007 (0.984–1.030) | 1.019 (0.998–1.040) | 0.989 (0.958–1.020) | 1.006 (0.986–1.027) | — |
| Levothyroxine (negative control) | 0.970 (0.938–1.003) | 0.948 (0.919–0.978) | 0.968 (0.936–1.001) | 0.980 (0.930–1.033) | 0.968 (0.936–1.002) | 0.975 (0.940–1.011) | 0.977 (0.941–1.014) | 0.967 (0.930–1.006) | 0.980 (0.929–1.032) | 0.978 (0.943–1.014) | 0.964 (0.916–1.014) |


**Table S2. Distributed lag model (t, t−1, t−2 in one model), LTLA residence**

| Drug group | t (same year) | t−1 | t−2 |
|:---|---:|---:|---:|
| Antituberculosis (descriptive) | 0.999 (0.996–1.002) | 1.001 (0.998–1.004) | 1.000 (0.997–1.003) |
| Systemic oral glucocorticoids | 0.966 (0.924–1.009) | 1.003 (0.952–1.057) | 1.007 (0.963–1.053) |
| Oral hydrocortisone | 1.009 (0.991–1.027) | 0.993 (0.973–1.014) | 1.002 (0.983–1.022) |
| Oral dexamethasone | 1.001 (0.991–1.011) | 1.004 (0.994–1.013) | 1.001 (0.991–1.011) |
| Inhaled corticosteroids | 0.896 (0.849–0.946) | 1.042 (0.966–1.123) | 1.034 (0.969–1.104) |
| Conventional DMARDs | 1.005 (0.968–1.043) | 0.994 (0.936–1.056) | 1.006 (0.964–1.049) |
| Transplant immunosuppressants | 1.000 (0.990–1.010) | 0.996 (0.983–1.009) | 1.004 (0.995–1.013) |
| Proton pump inhibitors | 0.994 (0.924–1.069) | 1.048 (0.969–1.134) | 0.965 (0.893–1.044) |
| Statins | 1.013 (0.942–1.089) | 1.022 (0.942–1.110) | 0.965 (0.898–1.038) |
| Metformin | 1.005 (0.943–1.071) | 0.995 (0.925–1.071) | 0.968 (0.915–1.024) |
| Insulins | 0.931 (0.872–0.995) | 1.033 (0.954–1.118) | 1.006 (0.951–1.064) |
| Fluoroquinolones | 1.002 (0.986–1.019) | 1.002 (0.985–1.020) | 1.007 (0.992–1.022) |
| All antibacterials | 1.020 (0.985–1.056) | 0.972 (0.928–1.017) | 1.030 (0.987–1.075) |
| Vitamin D | 1.011 (0.976–1.048) | 0.991 (0.947–1.038) | 1.008 (0.975–1.041) |
| Levothyroxine (negative control) | 0.987 (0.923–1.056) | 1.025 (0.946–1.110) | 0.955 (0.889–1.026) |


**Table S3. Hospital medicines: minimum detectable effects (previous-year exposure) versus illustrative expected effects**

| Level | Drug group | Scenario (illustrative RR) | Prevalence (SCMD patient-years) | Expected change per 10% | MDE | MDE ÷ expected | MDE ÷ expected, attenuated by positive-control elasticity |
|:---|---:|---:|---:|---:|---:|---:|---:|
| UTLA | TNF inhibitors | RR 4 (unscreened) | 0.34% | 0.100% | 2.5% | 25 | 70 |
| UTLA | TNF inhibitors | RR 1.7 (with LTBI screening, ~78% reduction) | 0.34% | 0.022% | 2.5% | 113 | 313 |
| UTLA | IL-6 inhibitors and abatacept | RR 2 | 0.02% | 0.002% | 1.2% | 507 | 1403 |
| UTLA | JAK inhibitors (rheumatology) | RR 2 | 0.04% | 0.004% | 1.0% | 229 | 633 |
| UTLA | Rituximab | RR 1.5 | 0.09% | 0.005% | 1.9% | 416 | 1152 |
| UTLA | Calcineurin/mTOR inhibitors | RR 10 (solid organ transplant) | 0.07% | 0.067% | 1.7% | 26 | 71 |
| UTLA | Antiproliferatives | RR 2 | 0.16% | 0.016% | 2.6% | 161 | 447 |
| UTLA | Systemic glucocorticoids | RR 4.9 | 0.46% | 0.177% | 4.1% | 23 | 62 |
| LTLA | TNF inhibitors | RR 4 (unscreened) | 0.34% | 0.100% | 2.2% | 22 | 54 |
| LTLA | TNF inhibitors | RR 1.7 (with LTBI screening, ~78% reduction) | 0.34% | 0.022% | 2.2% | 98 | 244 |
| LTLA | IL-6 inhibitors and abatacept | RR 2 | 0.02% | 0.002% | 1.2% | 517 | 1279 |
| LTLA | JAK inhibitors (rheumatology) | RR 2 | 0.04% | 0.004% | 0.9% | 211 | 521 |
| LTLA | Rituximab | RR 1.5 | 0.09% | 0.005% | 2.2% | 471 | 1166 |
| LTLA | Calcineurin/mTOR inhibitors | RR 10 (solid organ transplant) | 0.07% | 0.067% | 1.7% | 25 | 61 |
| LTLA | Antiproliferatives | RR 2 | 0.16% | 0.016% | 2.2% | 138 | 343 |
| LTLA | Systemic glucocorticoids | RR 4.9 | 0.46% | 0.177% | 3.8% | 21 | 53 |


**Table S4. Permutation-based power simulation (systemic oral glucocorticoids, exposure t−1)**

| Level | Scenario | Replicates | Two-sided rejection | Power, correct direction (95% MC interval) | Median estimated IRR per 10% | Null empirical SD | Real-data SE |
|:---|---:|---:|---:|---:|---:|---:|---:|
| LTLA | No effect | 500 | 7.0% | 3.2% (±1.5) | 1.001 | 0.0158 | 0.0218 |
| LTLA | Published RR 4.9 | 300 | 7.7% | 4.3% (±2.3) | 1.005 | 0.0158 | 0.0218 |
| LTLA | RR 25 | 300 | 20.7% | 20.3% (±4.6) | 1.017 | 0.0158 | 0.0218 |
| LTLA | RR 100 | 300 | 78.3% | 78.3% (±4.7) | 1.046 | 0.0158 | 0.0218 |
| LTLA | IRR 1.02 per 10% | 300 | 21.0% | 21.0% (±4.6) | 1.019 | 0.0158 | 0.0218 |
| LTLA | IRR 1.05 per 10% | 300 | 85.0% | 85.0% (±4.0) | 1.052 | 0.0158 | 0.0218 |
| LTLA | IRR 1.10 per 10% | 300 | 100.0% | 100.0% (±0.0) | 1.101 | 0.0158 | 0.0218 |
| LTLA | IRR 1.05 per 10%, acting via concurrent year | 300 | 60.7% | 60.7% (±5.5) | 1.037 | 0.0158 | 0.0218 |
| LTLA | IRR 1.10 per 10%, acting via concurrent year | 300 | 99.7% | 99.7% (±0.7) | 1.080 | 0.0158 | 0.0218 |
| UTLA | No effect | 500 | 6.8% | 3.8% (±1.7) | 1.000 | 0.0166 | 0.0250 |
| UTLA | Published RR 4.9 | 300 | 9.0% | 8.0% (±3.1) | 1.003 | 0.0166 | 0.0250 |
| UTLA | RR 25 | 300 | 20.3% | 19.7% (±4.5) | 1.017 | 0.0166 | 0.0250 |
| UTLA | RR 100 | 300 | 71.7% | 71.7% (±5.1) | 1.046 | 0.0166 | 0.0250 |
| UTLA | IRR 1.02 per 10% | 300 | 24.7% | 24.7% (±4.9) | 1.023 | 0.0166 | 0.0250 |
| UTLA | IRR 1.05 per 10% | 300 | 81.3% | 81.3% (±4.4) | 1.050 | 0.0166 | 0.0250 |
| UTLA | IRR 1.10 per 10% | 300 | 100.0% | 100.0% (±0.0) | 1.100 | 0.0166 | 0.0250 |
| UTLA | IRR 1.05 per 10%, acting via concurrent year | 300 | 64.0% | 64.0% (±5.4) | 1.042 | 0.0166 | 0.0250 |
| UTLA | IRR 1.10 per 10%, acting via concurrent year | 300 | 99.3% | 99.3% (±0.9) | 1.085 | 0.0166 | 0.0250 |


**Table S5. Regional models (9 regions): TB notifications by place of birth and age vs primary care prescribing**

| Outcome | Exposure | Analysis | Lag (years; negative = lead) | IRR per 10% (t(8) 95% CI) | p (cluster t8) | p (randomisation) |
|:---|---:|---:|---:|---:|---:|---:|
| TB, UK born | oral_glucocorticoids | lagged exposure | 1 | 1.18 (0.87–1.60) | 0.238 | 0.284 |
| TB, UK born | oral_glucocorticoids | lagged exposure | 2 | 1.18 (0.79–1.77) | 0.376 | 0.354 |
| TB, UK born | oral_glucocorticoids | lagged exposure | 3 | 1.07 (0.64–1.76) | 0.778 | 0.768 |
| TB, UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 1 | 1.20 (0.86–1.66) | 0.243 | 0.226 |
| TB, UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 2 | 1.19 (0.79–1.80) | 0.362 | 0.342 |
| TB, UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 3 | 1.08 (0.65–1.80) | 0.743 | 0.762 |
| TB, UK born | oral_glucocorticoids | lead (falsification) | -1 | 1.20 (0.76–1.90) | 0.393 | 0.262 |
| TB, UK born | oral_glucocorticoids | lead (falsification) | -2 | 1.07 (0.65–1.76) | 0.769 | 0.706 |
| TB, UK born | oral_glucocorticoids | lead (falsification) | -3 | 1.11 (0.82–1.49) | 0.454 | 0.576 |
| TB, UK born | mg_pred_equivalent | lagged exposure | 1 | 1.23 (0.95–1.58) | 0.102 | 0.132 |
| TB, UK born | mg_pred_equivalent | lagged exposure | 2 | 1.30 (0.97–1.75) | 0.076 | 0.078 |
| TB, UK born | mg_pred_equivalent | lagged exposure | 3 | 1.33 (0.93–1.89) | 0.103 | 0.134 |
| TB, UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 1 | 1.27 (0.93–1.72) | 0.113 | 0.086 |
| TB, UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 2 | 1.30 (0.97–1.75) | 0.073 | 0.072 |
| TB, UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 3 | 1.30 (0.89–1.89) | 0.149 | 0.212 |
| TB, UK born | mg_pred_equivalent | lead (falsification) | -1 | 1.15 (0.84–1.56) | 0.337 | 0.326 |
| TB, UK born | mg_pred_equivalent | lead (falsification) | -2 | 0.89 (0.71–1.13) | 0.303 | 0.546 |
| TB, UK born | mg_pred_equivalent | lead (falsification) | -3 | 0.93 (0.84–1.03) | 0.121 | 0.662 |
| TB, UK born | levothyroxine | lagged exposure | 1 | 0.94 (0.84–1.05) | 0.246 | 0.588 |
| TB, UK born | levothyroxine | lagged exposure | 2 | 0.89 (0.79–1.00) | 0.050 | 0.390 |
| TB, UK born | levothyroxine | lagged exposure | 3 | 0.89 (0.76–1.03) | 0.097 | 0.390 |
| TB, UK born | levothyroxine | lagged, excluding 2020-21 | 1 | 0.94 (0.83–1.06) | 0.270 | 0.572 |
| TB, UK born | levothyroxine | lagged, excluding 2020-21 | 2 | 0.89 (0.78–1.02) | 0.079 | 0.404 |
| TB, UK born | levothyroxine | lagged, excluding 2020-21 | 3 | 0.89 (0.75–1.05) | 0.136 | 0.404 |
| TB, UK born | levothyroxine | lead (falsification) | -1 | 0.92 (0.80–1.07) | 0.257 | 0.488 |
| TB, UK born | levothyroxine | lead (falsification) | -2 | 0.95 (0.80–1.14) | 0.560 | 0.654 |
| TB, UK born | levothyroxine | lead (falsification) | -3 | 0.97 (0.80–1.16) | 0.675 | 0.694 |
| TB, Non-UK born | oral_glucocorticoids | lagged exposure | 1 | 0.92 (0.70–1.20) | 0.478 | 0.588 |
| TB, Non-UK born | oral_glucocorticoids | lagged exposure | 2 | 0.97 (0.80–1.18) | 0.737 | 0.834 |
| TB, Non-UK born | oral_glucocorticoids | lagged exposure | 3 | 1.02 (0.81–1.30) | 0.820 | 0.854 |
| TB, Non-UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 1 | 0.95 (0.70–1.28) | 0.678 | 0.732 |
| TB, Non-UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 2 | 1.00 (0.82–1.22) | 0.968 | 0.978 |
| TB, Non-UK born | oral_glucocorticoids | lagged, excluding 2020-21 | 3 | 1.06 (0.83–1.35) | 0.606 | 0.700 |
| TB, Non-UK born | oral_glucocorticoids | lead (falsification) | -1 | 1.15 (0.91–1.46) | 0.216 | 0.424 |
| TB, Non-UK born | oral_glucocorticoids | lead (falsification) | -2 | 1.37 (1.01–1.86) | 0.046 | 0.112 |
| TB, Non-UK born | oral_glucocorticoids | lead (falsification) | -3 | 1.49 (1.17–1.90) | 0.005 | 0.010 |
| TB, Non-UK born | mg_pred_equivalent | lagged exposure | 1 | 0.97 (0.76–1.23) | 0.745 | 0.814 |
| TB, Non-UK born | mg_pred_equivalent | lagged exposure | 2 | 1.06 (0.92–1.22) | 0.393 | 0.650 |
| TB, Non-UK born | mg_pred_equivalent | lagged exposure | 3 | 1.11 (0.94–1.31) | 0.185 | 0.444 |
| TB, Non-UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 1 | 1.00 (0.78–1.29) | 0.988 | 0.992 |
| TB, Non-UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 2 | 1.06 (0.92–1.22) | 0.395 | 0.662 |
| TB, Non-UK born | mg_pred_equivalent | lagged, excluding 2020-21 | 3 | 1.13 (0.94–1.36) | 0.176 | 0.384 |
| TB, Non-UK born | mg_pred_equivalent | lead (falsification) | -1 | 1.16 (0.90–1.51) | 0.208 | 0.356 |
| TB, Non-UK born | mg_pred_equivalent | lead (falsification) | -2 | 1.32 (0.94–1.86) | 0.096 | 0.122 |
| TB, Non-UK born | mg_pred_equivalent | lead (falsification) | -3 | 1.28 (1.03–1.60) | 0.033 | 0.124 |
| TB, Non-UK born | levothyroxine | lagged exposure | 1 | 1.02 (0.89–1.15) | 0.786 | 0.868 |
| TB, Non-UK born | levothyroxine | lagged exposure | 2 | 1.01 (0.88–1.17) | 0.843 | 0.908 |
| TB, Non-UK born | levothyroxine | lagged exposure | 3 | 1.01 (0.88–1.16) | 0.859 | 0.914 |
| TB, Non-UK born | levothyroxine | lagged, excluding 2020-21 | 1 | 1.02 (0.89–1.16) | 0.762 | 0.864 |
| TB, Non-UK born | levothyroxine | lagged, excluding 2020-21 | 2 | 1.01 (0.88–1.17) | 0.840 | 0.902 |
| TB, Non-UK born | levothyroxine | lagged, excluding 2020-21 | 3 | 1.01 (0.88–1.16) | 0.856 | 0.920 |
| TB, Non-UK born | levothyroxine | lead (falsification) | -1 | 1.00 (0.85–1.16) | 0.961 | 0.988 |
| TB, Non-UK born | levothyroxine | lead (falsification) | -2 | 1.02 (0.88–1.18) | 0.806 | 0.920 |
| TB, Non-UK born | levothyroxine | lead (falsification) | -3 | 1.09 (0.91–1.29) | 0.300 | 0.550 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged exposure | 1 | 1.04 (0.71–1.51) | 0.823 | 0.868 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged exposure | 2 | 1.02 (0.68–1.54) | 0.894 | 0.894 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged exposure | 3 | 0.86 (0.44–1.68) | 0.618 | 0.434 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged, excluding 2020-21 | 1 | 1.11 (0.77–1.59) | 0.530 | 0.624 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged, excluding 2020-21 | 2 | 1.10 (0.73–1.66) | 0.615 | 0.592 |
| TB, UK born aged 65+ | oral_glucocorticoids | lagged, excluding 2020-21 | 3 | 0.92 (0.50–1.68) | 0.757 | 0.682 |
| TB, UK born aged 65+ | oral_glucocorticoids | lead (falsification) | -1 | 1.29 (0.82–2.02) | 0.228 | 0.204 |
| TB, UK born aged 65+ | oral_glucocorticoids | lead (falsification) | -2 | 1.74 (0.99–3.07) | 0.055 | 0.028 |
| TB, UK born aged 65+ | oral_glucocorticoids | lead (falsification) | -3 | 1.55 (0.96–2.49) | 0.066 | 0.070 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged exposure | 1 | 1.06 (0.75–1.49) | 0.707 | 0.684 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged exposure | 2 | 1.10 (0.79–1.53) | 0.524 | 0.548 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged exposure | 3 | 0.97 (0.54–1.73) | 0.909 | 0.882 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged, excluding 2020-21 | 1 | 1.14 (0.77–1.69) | 0.463 | 0.424 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged, excluding 2020-21 | 2 | 1.12 (0.76–1.64) | 0.527 | 0.418 |
| TB, UK born aged 65+ | mg_pred_equivalent | lagged, excluding 2020-21 | 3 | 0.93 (0.49–1.79) | 0.809 | 0.722 |
| TB, UK born aged 65+ | mg_pred_equivalent | lead (falsification) | -1 | 1.29 (0.86–1.91) | 0.185 | 0.150 |
| TB, UK born aged 65+ | mg_pred_equivalent | lead (falsification) | -2 | 1.59 (0.88–2.87) | 0.107 | 0.086 |
| TB, UK born aged 65+ | mg_pred_equivalent | lead (falsification) | -3 | 1.31 (0.81–2.14) | 0.233 | 0.252 |
| TB, UK born aged 65+ | levothyroxine | lagged exposure | 1 | 1.23 (1.00–1.50) | 0.051 | 0.050 |
| TB, UK born aged 65+ | levothyroxine | lagged exposure | 2 | 1.16 (0.95–1.42) | 0.126 | 0.226 |
| TB, UK born aged 65+ | levothyroxine | lagged exposure | 3 | 1.07 (0.90–1.26) | 0.415 | 0.584 |
| TB, UK born aged 65+ | levothyroxine | lagged, excluding 2020-21 | 1 | 1.22 (1.00–1.50) | 0.053 | 0.054 |
| TB, UK born aged 65+ | levothyroxine | lagged, excluding 2020-21 | 2 | 1.18 (0.97–1.44) | 0.090 | 0.142 |
| TB, UK born aged 65+ | levothyroxine | lagged, excluding 2020-21 | 3 | 1.10 (0.92–1.32) | 0.239 | 0.398 |
| TB, UK born aged 65+ | levothyroxine | lead (falsification) | -1 | 1.37 (1.04–1.79) | 0.028 | 0.008 |
| TB, UK born aged 65+ | levothyroxine | lead (falsification) | -2 | 1.20 (0.84–1.72) | 0.276 | 0.302 |
| TB, UK born aged 65+ | levothyroxine | lead (falsification) | -3 | 1.29 (0.83–2.00) | 0.223 | 0.106 |


**Table S6. Regional models: lag 2 and lead 2 estimated jointly**

| Outcome | Exposure | Years | IRR lag (per 10%) | IRR lead (per 10%) | Lag ÷ lead | p difference | p randomisation (lag) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| TB, UK born | oral_glucocorticoids | 2013-2022 | 1.22 | 0.94 | 1.29 | 0.239 | 0.324 |
| TB, UK born | mg_pred_equivalent | 2013-2022 | 1.41 | 0.85 | 1.66 | 0.037 | 0.040 |
| TB, UK born | levothyroxine | 2013-2022 | 0.82 | 1.00 | 0.82 | 0.564 | 0.408 |
| TB, Non-UK born | oral_glucocorticoids | 2013-2022 | 0.94 | 1.40 | 0.67 | 0.111 | 0.742 |
| TB, Non-UK born | mg_pred_equivalent | 2013-2022 | 1.09 | 1.27 | 0.86 | 0.498 | 0.628 |
| TB, Non-UK born | levothyroxine | 2013-2022 | 0.87 | 1.07 | 0.81 | 0.557 | 0.466 |
| TB, UK born aged 65+ | oral_glucocorticoids | 2013-2022 | 0.81 | 1.78 | 0.46 | 0.079 | 0.372 |
| TB, UK born aged 65+ | mg_pred_equivalent | 2013-2022 | 1.01 | 1.53 | 0.66 | 0.302 | 0.968 |
| TB, UK born aged 65+ | levothyroxine | 2013-2022 | 0.92 | 1.14 | 0.81 | 0.546 | 0.790 |


**Table S7. Hospital medicines: share of DDD from trusts matched to catchments directly, via successor trusts, or unmatched**

| Drug group | Year | Direct | Successor | Unmatched |
|:---|---:|---:|---:|---:|
| Antiproliferatives | 2019 | 90.9% | 8.4% | 0.7% |
| Antiproliferatives | 2020 | 93.8% | 4.8% | 1.4% |
| Antiproliferatives | 2021 | 96.4% | 2.4% | 1.2% |
| Antiproliferatives | 2022 | 97.7% | 0.7% | 1.6% |
| Antiproliferatives | 2023 | 97.6% | 0.5% | 1.9% |
| Antiproliferatives | 2024 | 97.7% | 0.4% | 1.9% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2019 | 91.3% | 8.3% | 0.4% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2020 | 94.6% | 5.1% | 0.3% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2021 | 97.4% | 2.5% | 0.1% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2022 | 98.5% | 1.4% | 0.1% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2023 | 98.9% | 1.0% | 0.1% |
| Active-TB treatment (pyrazinamide/ethambutol; positive control) | 2024 | 98.3% | 0.9% | 0.7% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2019 | 90.6% | 9.0% | 0.3% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2020 | 95.1% | 4.6% | 0.3% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2021 | 97.7% | 2.1% | 0.2% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2022 | 99.0% | 0.8% | 0.2% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2023 | 99.0% | 0.8% | 0.2% |
| Rifamycin/isoniazid (active and latent TB, other infections) | 2024 | 99.2% | 0.6% | 0.1% |
| IL-6 inhibitors and abatacept | 2019 | 90.1% | 8.7% | 1.2% |
| IL-6 inhibitors and abatacept | 2020 | 93.9% | 4.9% | 1.2% |
| IL-6 inhibitors and abatacept | 2021 | 96.3% | 2.8% | 0.9% |
| IL-6 inhibitors and abatacept | 2022 | 97.8% | 1.0% | 1.2% |
| IL-6 inhibitors and abatacept | 2023 | 97.9% | 0.5% | 1.5% |
| IL-6 inhibitors and abatacept | 2024 | 97.8% | 0.4% | 1.8% |
| JAK inhibitors (rheumatology) | 2019 | 90.1% | 8.9% | 0.9% |
| JAK inhibitors (rheumatology) | 2020 | 94.8% | 4.4% | 0.9% |
| JAK inhibitors (rheumatology) | 2021 | 97.1% | 2.5% | 0.4% |
| JAK inhibitors (rheumatology) | 2022 | 98.5% | 1.1% | 0.4% |
| JAK inhibitors (rheumatology) | 2023 | 98.9% | 0.4% | 0.7% |
| JAK inhibitors (rheumatology) | 2024 | 98.4% | 0.3% | 1.3% |
| Low-TB-risk biologics (negative control) | 2019 | 91.9% | 7.9% | 0.2% |
| Low-TB-risk biologics (negative control) | 2020 | 96.0% | 3.9% | 0.1% |
| Low-TB-risk biologics (negative control) | 2021 | 97.9% | 2.0% | 0.1% |
| Low-TB-risk biologics (negative control) | 2022 | 99.1% | 0.8% | 0.1% |
| Low-TB-risk biologics (negative control) | 2023 | 99.5% | 0.4% | 0.1% |
| Low-TB-risk biologics (negative control) | 2024 | 99.6% | 0.2% | 0.2% |
| Levetiracetam (negative control) | 2019 | 87.6% | 7.5% | 4.9% |
| Levetiracetam (negative control) | 2020 | 91.3% | 4.2% | 4.5% |
| Levetiracetam (negative control) | 2021 | 93.5% | 2.3% | 4.2% |
| Levetiracetam (negative control) | 2022 | 94.7% | 1.2% | 4.0% |
| Levetiracetam (negative control) | 2023 | 94.8% | 0.9% | 4.3% |
| Levetiracetam (negative control) | 2024 | 95.0% | 0.7% | 4.3% |
| Rituximab | 2019 | 91.2% | 8.4% | 0.4% |
| Rituximab | 2020 | 95.1% | 4.4% | 0.5% |
| Rituximab | 2021 | 97.5% | 2.1% | 0.5% |
| Rituximab | 2022 | 98.7% | 0.8% | 0.5% |
| Rituximab | 2023 | 99.0% | 0.4% | 0.5% |
| Rituximab | 2024 | 99.2% | 0.2% | 0.6% |
| Systemic glucocorticoids | 2019 | 90.6% | 8.8% | 0.5% |
| Systemic glucocorticoids | 2020 | 94.6% | 4.8% | 0.6% |
| Systemic glucocorticoids | 2021 | 97.3% | 2.2% | 0.5% |
| Systemic glucocorticoids | 2022 | 98.4% | 1.1% | 0.5% |
| Systemic glucocorticoids | 2023 | 98.8% | 0.7% | 0.5% |
| Systemic glucocorticoids | 2024 | 99.0% | 0.5% | 0.5% |
| TNF inhibitors | 2019 | 91.2% | 8.2% | 0.6% |
| TNF inhibitors | 2020 | 95.3% | 4.1% | 0.6% |
| TNF inhibitors | 2021 | 97.6% | 2.0% | 0.4% |
| TNF inhibitors | 2022 | 98.5% | 0.9% | 0.6% |
| TNF inhibitors | 2023 | 98.6% | 0.4% | 0.9% |
| TNF inhibitors | 2024 | 98.9% | 0.3% | 0.9% |
| Calcineurin/mTOR inhibitors | 2019 | 92.3% | 7.6% | 0.1% |
| Calcineurin/mTOR inhibitors | 2020 | 96.3% | 3.6% | 0.1% |
| Calcineurin/mTOR inhibitors | 2021 | 99.3% | 0.6% | 0.1% |
| Calcineurin/mTOR inhibitors | 2022 | 99.8% | 0.1% | 0.1% |
| Calcineurin/mTOR inhibitors | 2023 | 99.9% | 0.0% | 0.1% |
| Calcineurin/mTOR inhibitors | 2024 | 99.9% | 0.0% | 0.1% |
