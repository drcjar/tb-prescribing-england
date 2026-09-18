## Methods

### Design and pre-specification

This study used aggregate, openly published data in three linked ecological designs: a
cross-sectional analysis, a longitudinal panel analysis of local authorities with area and year
fixed effects, and regional analyses by place of birth and age. It is reported following RECORD,
an extension of STROBE for routinely collected health data (supplementary file).

The analysis developed in stages. Before any results were seen we specified the drug groups,
including a negative-control exposure (levothyroxine) and a positive control (primary care
antituberculosis prescribing), and the cross-sectional design. The pre-specified positive control
failed, because TB treatment in England is delivered by specialist services rather than general
practice, and was reclassified as descriptive. The first panel design, specified after the
cross-sectional results but before any panel results, used three-year rolling notifications.
Annual outcomes, lower-tier authorities, hospital medicines, regional analyses, the power
simulation and the spatial diagnostics were added after those analyses gave null results, and are
exploratory. Supplementary tables report the original design and all sensitivity analyses.

Figure 1 shows the assumed causal structure: what area and year fixed effects absorb, what is
measured and adjusted for, and what remains unmeasured.

### TB notifications

TB notifications are cases reported to UK Health Security Agency surveillance (the Enhanced TB
Surveillance system until 2021, the National TB Surveillance System since), assigned to areas by
residential postcode and counted by year of notification. We used annual counts by local authority
for 2001–2024 from UKHSA regional reports, published on April 2023 boundaries, which combine the
City of London with Hackney and the Isles of Scilly with Cornwall; we merged population, covariate
and prescribing data in the same way, giving 294 lower-tier (LTLA) and 151 upper-tier (UTLA)
authorities. We also used national counts by region, place of birth and age, and national
notifications with recorded immunosuppression by cause for 2024. Summed over three years, local
authority counts matched the Fingertips three-year counts (r = 0.996). The fall in 2020 is thought
to reflect service disruption rather than less disease [UKHSA 2021; Morrison 2023].

### Primary care prescribing

We used HSCIC practice-level prescribing for 2011–2013 and the NHS Business Services Authority
English Prescribing Dataset for 2014–2024, aggregating each month to practice level with identical
presentation-level drug-group rules (supplementary file). Groups were systemic oral glucocorticoids
(prednisolone, prednisone, methylprednisolone, deflazacort and dexamethasone, excluding injectables
and hydrocortisone), inhaled corticosteroids, conventional DMARDs, transplant immunosuppressants,
proton pump inhibitors, statins, metformin, insulins, fluoroquinolones, all antibacterials, vitamin
D, and levothyroxine as the negative-control exposure.

We restricted to standard general practices: those with NHS Organisation Data Service prescribing
setting RO76, plus practice codes absent from the current ODS file, which omits practices that
closed before 2017, that have the standard practice code format. Without this addition, prescribing
by practices that later closed would have been dropped unevenly over time (3.4% of items in 2011,
1.7% in 2014, none from 2016).

Each practice's annual prescribing was apportioned across local authority districts in proportion
to where its registered patients lived, using NHS Digital counts of patients registered at each
practice by lower-layer super output area (April releases 2014–2024, each practice-year taking that
practice's nearest release in time). Practices in no release were assigned to the district of their
postcode. Exposure was expressed as items per 1,000 residents per year, with
prednisolone-equivalent milligrams and average daily quantities as alternative measures.
Denominators were ONS mid-year population estimates.

### Hospital medicines

We used NHS Secondary Care Medicines Data for January 2019 to December 2024, classified by
mechanism and converted to defined daily dose (DDD)-years: TNF inhibitors, interleukin-6 inhibitors
and abatacept, rheumatology JAK inhibitors, rituximab, calcineurin and mTOR inhibitors,
antiproliferatives, and systemic glucocorticoids in prednisolone-equivalent milligrams
(dexamethasone and hydrocortisone reported separately, and a sensitivity analysis restricted to
oral forms). The positive control was treatment for active TB, measured as pyrazinamide DDD from
all pyrazinamide-containing products including fixed-dose combinations; rifamycin and isoniazid
products, which are also used for latent infection, were reported separately. Negative-control
exposures were low-TB-risk biologics and levetiracetam. Trusts that merged were reassigned to their
successors, after which 98–100% of DDD in every drug group and year (95% for levetiracetam) came
from trusts with catchment data. Trust quantities were apportioned to local authorities using OHID
acute trust catchment populations, with elective-admission catchments as a sensitivity analysis.

### Covariates

Time-varying covariates were the percentages of residents aged 65 and over and aged 15–44,
international in-migration per 1,000, diagnosed HIV prevalence, QOF diabetes prevalence, an
indicator of latent TB infection programme activity for new migrants mapped from clinical
commissioning groups to local authorities, and people receiving asylum support per 1,000. Diabetes
prevalence was not adjusted for in the metformin and insulin models. Cross-sectional analyses used
the 2021 Census percentage born outside the UK.

### Statistical analysis

We fitted Poisson pseudo-maximum-likelihood models [Santos Silva 2006] of annual notifications with
area and year fixed effects, a log population offset and standard errors clustered by area. The
primary exposure was log prescribing in year *t*−1, because drug-associated TB typically presents
within months [Keane 2001] and same-year prescribing may be prescribing for undiagnosed TB.
Outcome years were 2014–2024. Effects are reported as incidence rate ratios (IRR) per 10%
within-area increase in prescribing, with Benjamini–Hochberg false discovery rate correction across
the 13 non-control drug groups. Falsification tests estimated prescribing in years *t*−1 and *t*+1
jointly, and again with year *t* added, with a Wald test of the difference. Sensitivity analyses
covered alternative covariate sets, exposure windows, area-specific trends, COVID-affected years,
NTBS-era outcome years, alternative exposure measures and geography (supplementary file). Spatial
dependence was assessed with year-specific Moran's I of Pearson residuals. Regional analyses used
nine regions with cluster-robust *t*(8) intervals and randomisation inference, permuting whole
regional exposure histories across regions.

For each drug we calculated the minimum detectable effect (MDE) as exp(2.80 × standard error), the
corresponding minimum detectable population attributable fraction, and the largest attributable or
prevented fraction compatible with the 90% confidence limits. Expected population effects were
calculated as [1 + 1.1*p*(RR − 1)] / [1 + *p*(RR − 1)], where *p* is prevalence of use and RR the
individual-level relative risk, assuming that prevalence scales with prescribing, that additional
prescribing reaches new users, homogeneous baseline risk and aligned timing. Alternative benchmarks
used UKHSA records of drug-associated TB converted to attributable fractions, age-stratified
prevalence of use, and SCMD-derived prevalence for hospital drugs. A permutation-based simulation
kept the real notification counts, permuted whole exposure trajectories across areas and injected
known effects, with 500 null and 300 effect replicates per scenario; analytic power at the
real-data standard error is reported alongside.

Analyses used Python 3.14 with pandas and statsmodels. Code and outputs are openly available.
