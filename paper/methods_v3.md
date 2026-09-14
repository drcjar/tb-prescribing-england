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

{{figure:dag}}

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
