# Title page

**Title.** Can open prescribing data detect effects of medicines on tuberculosis? An ecological
study of primary care and hospital prescribing and TB notifications in England, 2011–2024

**Short title.** Prescribing and tuberculosis notifications in England

**Authors.** [To be confirmed]

**Affiliations.** [To be confirmed]

**Corresponding author.** [Name, address, email]

**Word counts.** Main text: 3456 words. Abstract: 300 words.

**Keywords.** tuberculosis; pharmacoepidemiology; ecological study; routinely collected health
data; glucocorticoids; biological therapy

**Reporting guideline.** RECORD, an extension of STROBE for studies using routinely collected
health data. The completed checklist is in the supplementary file.

## Statements

**Ethics approval.** Not required. All data are aggregate, openly published and anonymous, and no
individual-level records were used.

**Patient and public involvement.** Patients and the public were not involved in the design,
conduct, reporting or dissemination of this research, which used aggregate published statistics.

**Data availability.** All data are publicly available: NHSBSA Open Data Portal (English
Prescribing Dataset; Secondary Care Medicines Data), NHS Digital practice-level prescribing and
patients registered at a GP practice by LSOA, UK Health Security Agency tuberculosis reports and
OHID Fingertips, OHID acute trust catchment populations, ONS/Nomis population and migration
estimates, Home Office asylum support statistics, NHS England Organisation Data Service, and MHCLG
English Indices of Deprivation. Analysis code, processed datasets, result files and the figures in
this paper are at https://github.com/drcjar/tb-prescribing-england.

**Funding.** This research received no specific grant from any funding agency in the public,
commercial or not-for-profit sectors.

**Competing interests.** None declared.

**Author contributions.** [To be confirmed.] Suggested wording: [X] conceived the study, obtained
and processed the data, did the analysis and wrote the first draft. [Y] contributed to the design
and interpretation and revised the manuscript. All authors approved the final version and accept
accountability for the work.

**Acknowledgements.** We thank the NHS Business Services Authority, NHS England, UKHSA, OHID and
ONS for publishing the data used here.

**Transparency statement.** The lead author affirms that this manuscript is an honest, accurate and
transparent account of the study being reported; that no important aspects of the study have been
omitted; and that any discrepancies from the study as originally planned have been explained. The
chronology of the analysis, including analyses added after initial null results, is described in
the Methods.


## Abstract

**Objectives.** To assess whether openly published English prescribing and tuberculosis (TB)
surveillance data can detect population-level associations between medicines and TB, and how large
an effect such designs could detect.

**Design.** Ecological study: Poisson panel models with area and year fixed effects, negative-control
exposures, falsification tests, a disease-specific positive control, minimum detectable effects and
a power simulation.

**Setting.** England: primary care prescribing 2011–2024, hospital medicines 2019–2024, TB
notifications 2014–2024.

**Data sources.** Prescribing apportioned to local authorities by patients' area of residence;
hospital medicines in defined daily doses apportioned by trust catchment; UK Health Security Agency
TB notifications for 294 lower-tier and 151 upper-tier authorities.

**Main outcome measures.** Annual TB notifications, as incidence rate ratios (IRR) per 10%
within-area increase in prescribing, and the minimum detectable effect versus effects expected from
published relative risks and recorded drug-associated TB.

**Results.** The positive control, hospital treatment for active TB, tracked notifications between
areas (Spearman rho 0.81) and within areas in the same year (IRR 1.035, 95% CI 1.009 to 1.061),
elasticity only 0.36 to 0.40. After correction for multiple testing, no medicine was associated with
notifications in the following year: systemic oral glucocorticoids 0.969 (0.929 to 1.012). A
negative-control exposure and prescribing in the following year showed inverse associations of
similar size, indicating residual confounding by area trends. For oral glucocorticoids the minimum
detectable effect (6.3% per 10% increase) was 18 times the expected effect (0.34%) and 70 to 140
times that implied by recorded steroid-associated TB. In simulations, the published glucocorticoid
effect was detected no more often than no effect (8.3% versus 7.8%).

**Conclusions.** These data link only with heavy attenuation, and such designs cannot detect
plausible effects of medicines on TB; apparent associations are compatible with confounding or
chance. Causal questions need individual-level linked data; surveillance needs fuller recording of
immunosuppression.

## Strengths and limitations of this study

- The study links every openly published source for this question: 14 years of practice-level
  prescribing apportioned to where registered patients live, hospital medicines converted to
  defined daily doses and apportioned by trust catchment, and annual local authority TB
  notifications.
- A disease-specific positive control (hospital treatment for active TB), negative-control
  exposures and falsification tests allow the validity of the linkage and residual confounding to
  be examined rather than assumed.
- Detectability is quantified both analytically (minimum detectable effects and attributable
  fractions) and by a permutation simulation that preserves the real notification counts, and is
  compared with effects expected from published relative risks and from UKHSA records of
  drug-associated TB.
- The design is ecological: associations are between areas and years rather than between people,
  so cross-level bias cannot be excluded, and prescribing volume is only a proxy for the number of
  people treated.
- Most analyses beyond the first pass were added after initial null results and are exploratory,
  and no working positive control exists for primary care prescribing, so the validity of that
  linkage is untested.


## Introduction

Tuberculosis (TB) notifications in England fell by 44% between 2011 and 2018, rose again from 2021,
and reached 5,490 in 2024, of which 81.9% were in people born outside the UK [1]. For
2011–2015, most of the decline reflected falling TB rates across populations, with smaller
contributions from fewer recent non-EU migrants and from pre-entry screening [2,3].

Several commonly prescribed medicines change individual TB risk. Current oral glucocorticoid use
carries an odds ratio of about 5 [4]; inhaled corticosteroids and conventional
disease-modifying antirheumatic drugs carry smaller increases [5,6,7]; TB associated with tumour necrosis factor (TNF) inhibitors typically presents
within months of starting treatment [8], and screening for latent infection before
treatment greatly reduces that risk [9,10]. Proton pump inhibitors have been
associated with higher risk [11], and statins and metformin with lower risk [12,13]. Many of these estimates come from high-incidence settings or from designs vulnerable
to confounding by indication and to protopathic bias.

England publishes monthly prescribing for every general practice, hospital medicines issued by
every NHS trust, and TB notifications by local authority. Linking these openly published sources
would be a low-cost way to generate or test hypotheses about medicines and TB. Ecological analyses
of such data face well-recognised problems: confounding by area characteristics, cross-level bias
that covariate adjustment cannot remove when effects differ between groups [14,15], and limited power, which depends mainly on the number of areas [16].
The data carry further problems: practice list sizes are inflated in ways that track population
mobility [17,18]; practices are not where their patients live; prescribing
is patterned by deprivation and was disrupted by COVID-19 [19]; and hospital-prescribed
medicines are recorded separately from primary care [20].

We found no previous study linking area-level prescribing to TB. In analogous settings, drugs with
large individual-level effects have produced weak population signals [21], and
between-area and within-area associations have had opposite signs [22].

We therefore asked whether open English prescribing data can detect associations between medicines
and TB notifications at population level, and, if not, why. We combined cross-sectional and
fixed-effects panel designs at two geographic scales, with primary care prescribing apportioned to
where registered patients live, hospital medicines apportioned by trust catchment, a
disease-specific positive control, negative-control exposures and falsification tests
[23,24], and regional analyses by place of birth and age. We compared the
smallest effects these designs could detect, both analytically and by simulation, with the
population effects implied by published individual-level relative risks and by national
surveillance records of drug-associated TB.


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
to reflect service disruption rather than less disease [25,26].

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

We fitted Poisson pseudo-maximum-likelihood models [27] of annual notifications with
area and year fixed effects, a log population offset and standard errors clustered by area. The
primary exposure was log prescribing in year *t*−1, because drug-associated TB typically presents
within months [8] and same-year prescribing may be prescribing for undiagnosed TB.
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


## Results

### Prescribing and notifications

England recorded 6,474 TB notifications in 2014, 4,123 in 2020 and 5,490 in 2024. The primary
analysis covered 294 lower-tier authorities and 3,233 area-years for outcome years 2014–2024.

Once prescribing was apportioned to where patients live, it varied little within areas over time.
For systemic oral glucocorticoids, the standard deviation of the log rate after removing area and
year means was 0.042, against 0.29 between areas, and 95% of area-years lay within 9% of their area
and year means (figure 2). Proton pump inhibitors (0.036), metformin (0.041) and levothyroxine
(0.042) were similar, and prednisolone-equivalent milligrams and average daily quantities varied as
little as items. A 10% within-area change in prescribing is therefore at the edge of the observed
data.

### Primary care prescribing and notifications

No drug group was associated with notifications in the following year after correction for multiple
testing (table 1; all q ≥ 0.51). For systemic oral glucocorticoids the IRR was 0.969 (95% CI 0.929
to 1.012) per 10% within-area increase. Metformin (0.966, 0.934 to 0.998) and the negative-control
exposure levothyroxine (0.962, 0.933 to 0.992) were both nominally inverse and of similar size,
which is the pattern expected from shared area trends rather than drug effects.

Upper-tier geography (0.974, 0.928 to 1.023 for oral glucocorticoids), assigning prescribing by
practice postcode (0.974, 0.939 to 1.010), and sensitivity analyses covering exposure windows,
area-specific trends, alternative covariates, COVID-affected years, NTBS-era outcome years and
alternative exposure measures all gave similar results (supplementary tables). Inhaled
corticosteroids were nominally inverse in several sensitivity analyses, the direction opposite to
any plausible harmful effect.

The data were compatible with an attributable fraction of at most 5% for oral glucocorticoids, 18%
for conventional DMARDs and 4% for transplant immunosuppressants. These bounds depend on point
estimates that happened to fall below 1: dividing each upper limit by the negative-control estimate,
as if its bias applied to every drug, raised them to 44%, 58% and 44%, close to the minimum
detectable attributable fractions.

In falsification tests, prescribing in the following year was inversely associated with
notifications for inhaled corticosteroids (0.879, 0.840 to 0.921), insulins (0.921, 0.866 to 0.980)
and oral glucocorticoids (0.952, 0.912 to 0.994) (figure 3). When same-year prescribing was added,
the previous-year and following-year estimates became almost uncorrelated (−0.23 to +0.17) but the
inverse following-year associations persisted, so they are not an artefact of collinearity between
adjacent years. Of 277 estimates across all lower-tier specifications, 30 were nominally
significant; these are overlapping specifications of the same data, and the test rejected in 7.8% of
simulated replicates when there was no effect, so this count cannot be compared with a nominal 5%.
Nominal results were concentrated in the negative control, metformin and inhaled corticosteroids.

Raw notification rates were strongly spatially clustered in every year (Moran's I 0.25 to 0.39),
but residual dependence after the primary model was weak (median I 0.026) and concentrated in 2014,
the only outcome year whose previous-year exposure comes from the earlier prescribing series.

### Hospital medicines

Hospital treatment for active TB, the positive control, tracked notifications between areas
(Spearman rho 0.81) and within areas in the same year (1.035, 1.009 to 1.061 per 10% increase;
figure 4). Its within-area elasticity was 0.36 (95% CI 0.10 to 0.62) at upper-tier and 0.40 (0.14 to
0.66) at lower-tier level, so even a drug used almost exclusively for the outcome was recovered with
heavy attenuation. Rifamycin and isoniazid products, which are also used for latent infection, had a
similar elasticity (0.37, 0.22 to 0.51), suggesting that drug specificity is not the main source of
that attenuation. Estimates for the previous year (1.001, 0.993 to 1.010) and the following year
(0.997, 0.986 to 1.007) were null, as expected when treatment follows diagnosis.

No candidate drug group was robustly associated with notifications in the following year
(supplementary tables): TNF inhibitors 0.989 (0.972 to 1.007), interleukin-6 inhibitors and
abatacept 1.001 (0.992 to 1.009), JAK inhibitors 0.994 (0.987 to 1.002), rituximab 0.998 (0.984 to
1.012), calcineurin and mTOR inhibitors 1.008 (0.996 to 1.020) and antiproliferatives 0.996 (0.978
to 1.014). Hospital systemic glucocorticoids showed a small nominal association (1.024, 1.001 to
1.046) that was not robust to clustering by principal trust (0.999 to 1.049), was similar but
imprecise when COVID-affected outcome years were excluded, and was absent when the exposure was
restricted to oral forms (1.011, 0.991 to 1.032). It would imply that hospital glucocorticoids
account for about a quarter of all notifications, whereas steroid-associated immunosuppression was
recorded for 0.5% of notifications in 2024 [1]. Negative-control exposures were null.
Across 260 within-area hospital estimates at both geographic levels, 22 were nominally significant,
12 of them the expected same-year associations for the two TB treatment groups.

### National trends, regional analyses and detectability

Nationally, systemic oral glucocorticoid items rose from 119 to 132 per 1,000 residents between
2011 and 2016 and fell to 111 by 2024, while the prednisolone-equivalent dose per item fell from
225 mg to 192 mg. National notification rates and prescribing were not correlated in levels
(r = 0.33), and year-on-year changes were not correlated at lags of 0 to 2 years.

Regional models, with nine regions, were very imprecise: minimum detectable effects for
glucocorticoid exposures were 46% to 98% per 10% increase for UK-born notifications and 54% to 119%
at age 65 and over, far above the 10% maximum attainable under the model used for expected effects,
so any nominally significant regional estimate must reflect chance or bias. Of 81 adjusted regional
estimates, 4 had randomisation p ≤ 0.05, all of them falsification terms. Prednisolone-equivalent
milligrams were imprecisely associated with UK-born notifications (joint lag estimate 1.45), but
this was not significant by randomisation inference (p = 0.23) and fell to 1.12 when London was
excluded.

Table 2 compares detectable with expected effects. For oral glucocorticoids the minimum detectable
effect was 6.3% per 10% increase, against an expected 0.34% from published relative risks, 0.29%
after age stratification, and 0.043% to 0.087% from recorded steroid-associated notifications: a gap
of 18 to 140 times. The design could only detect a drug responsible for 63% of all notifications.
For other primary care groups, minimum detectable effects exceeded expected effects by 11 to 272
times, and for hospital drugs, where detectable effects were smaller (1.0% to 2.9%), by 26 to 520
times before any allowance for attenuation.

In simulations that preserved the real notification counts, the test rejected in 7.8% of replicates
when there was no effect. The published glucocorticoid relative risk was detected in 8.3% of
replicates, no more often than no effect at all. Power reached 83% only for a direct effect of 5%
more notifications per 10% more prescribing, and analytic power at the real-data standard error for
the same effect was 65%.


## Discussion

We linked openly published English prescribing and TB surveillance data in several ecological
designs at two geographic scales. The linkage worked only partly, and no medicine plausibly
affecting TB risk was robustly associated with subsequent notifications. The designs could detect
only effects roughly 10 to several hundred times larger than those implied by published relative
risks or by national records of drug-associated TB.

Three features explain this. First, expected population effects are small: oral glucocorticoids
carry an odds ratio of about 5 [4] but are used by about 1% of people at any time
[28,29], so a 10% change in use should change notifications by about 0.3%, and
recorded steroid-associated immunosuppression implies less [1]. Screening for latent
infection before anti-TNF therapy has been standard since 2005 [9] and largely removes the
excess risk [10], so the risk relevant to a marginal increase in biologic use is small.
Second, the data carry little information: within-area variation in prescribing was very small
against between-area variation, and fixed effects remove the between-area variation where most
information lies [30], while power in aggregate studies depends mainly on the number of
areas [16], which cannot be increased. Third, the linkage attenuates: the positive
control, a drug used almost exclusively for the outcome, was recovered with an elasticity of only
0.36 to 0.40, and a similar elasticity for less specific TB drugs suggests apportionment rather than
drug specificity as the main cause. No equivalent positive control exists for primary care
prescribing, so the validity of that linkage remains untested.

Two patterns indicate residual confounding rather than drug effects. The negative-control exposure,
which has no plausible effect on TB, was inversely associated with notifications to the same degree
as metformin; and prescribing in the following year was inversely associated with notifications for
several groups, which persisted when same-year prescribing was added and the estimates were almost
uncorrelated. Both are expected when prescribing and notifications share area-specific trends, for
example migration-driven changes in population age and origin, accompanying changes in practice
registration, and changes in diagnostic activity. Year fixed effects cannot remove such trends.
Area-level adjustment also cannot remove cross-level bias [14,15]: people
prescribed glucocorticoids are mostly older and UK-born, whereas most notifications are in younger
people born abroad. Protopathic prescribing for undiagnosed TB, and glucocorticoids used in treating
TB meningitis and pericarditis [31], further complicate same-year associations, which is
why the primary exposure was the previous year.

The one nominal candidate association, for hospital systemic glucocorticoids, illustrates the
argument rather than contradicting it. It did not survive clustering by trust, disappeared when
intravenous methylprednisolone pulses were excluded, and would imply an attributable fraction some
50 times larger than surveillance records support. The same applies to the regional association
between prednisolone dose and UK-born TB: it exceeded the maximum attainable under any relative
risk, was not significant by randomisation inference, and depended on one region.

This study has limitations beyond those in the summary box. Exposure was prescribing volume per
resident, not people treated, and additional volume may lengthen existing courses rather than reach
new users. Apportionment used annual registration snapshots, and hospital quantities were
apportioned with 2024 catchments applied to earlier years. Prescriptions written in hospital and
dispensed in the community were excluded by the restriction to general practices. The outcome is
notified TB, subject to diagnostic delay and to the 2021 change of surveillance system. Social risk
factors and the area-level share of recent arrivals were not available as consistent annual series.

Open prescribing data are valuable for describing prescribing and its variation [20,32], but they cannot estimate the effects of medicines on a rare outcome such as
TB. Ecological studies of rare outcomes should report the minimum detectable effect, a positive
control with its elasticity, negative controls and falsification tests alongside any association;
had we reported only the primary estimates, several nominal associations here could have been
over-interpreted. Causal questions need individual-level linked data analysed as a target trial
emulation, and even national cohorts give wide intervals for modest relative risks [33];
the only drug–TB target trial emulation we identified concerned DPP-4 inhibitors [34].

These null results do not mean the drugs are safe. Glucocorticoids, biologics and JAK inhibitors
remain important treatments, and drug-associated TB is serious, often extrapulmonary [8]
and largely preventable. Monitoring is better served by more complete recording of immunosuppression
in the National TB Surveillance System, including drug class, time since starting and whether latent
infection screening was done, than by ecological analysis of prescribing. The practical lever is
auditing screening before biologics, JAK inhibitors and prolonged high-dose glucocorticoids.

In conclusion, open English prescribing and TB notification data can be linked, but hospital
medicines only with heavy attenuation and primary care prescribing without any means of validation.
Ecological analyses of these data cannot detect the population-level effects of medicines on TB:
plausible effects lie one to several hundred times below what the designs can resolve, and the
associations that do arise are compatible with residual confounding, chance or measurement error.


## Tables

**Table 1. Primary care prescribing and TB notifications: incidence rate ratio per 10% within-area increase (95% CI)**

| Drug group | Previous year: LTLA, residence (294 areas, 2014-2024) | Previous year: UTLA, residence | Previous year: LTLA, practice postcode | Joint model: previous year (t−1) | Joint model: following year (t+1) | p, t−1 vs t+1 | Largest compatible PAF / prevented fraction (PAF after negative-control shift) |
|:---|---:|---:|---:|---:|---:|---:|---:|
| Antituberculosis (descriptive) | 1.000 (0.997–1.003) | 1.000 (0.996–1.004) | 1.001 (0.998–1.003) | 1.000 (0.996–1.003) | 1.002 (0.998–1.005) | 0.423 | 3% / 2% (42%) |
| Systemic oral glucocorticoids | 0.969 (0.929–1.012) | 0.974 (0.928–1.023) | 0.974 (0.939–1.010) | 0.990 (0.941–1.041) | 0.952 (0.912–0.994) | 0.334 | 5% / 39% (44%) |
| Oral hydrocortisone | 0.998 (0.985–1.011) | 0.999 (0.985–1.014) | 0.999 (0.987–1.011) | 0.995 (0.978–1.012) | 1.007 (0.991–1.023) | 0.416 | 9% / 11% (49%) |
| Oral dexamethasone | 1.003 (0.992–1.014) | 1.004 (0.992–1.016) | 1.001 (0.991–1.011) | 1.002 (0.991–1.013) | 1.003 (0.993–1.013) | 0.907 | 12% / 6% (52%) |
| Inhaled corticosteroids | 0.966 (0.920–1.014) | 0.965 (0.916–1.017) | 0.973 (0.934–1.014) | 1.058 (0.995–1.126) | 0.879 (0.840–0.921) | 0.000 | 7% / 42% (46%) |
| Conventional DMARDs | 1.002 (0.983–1.021) | 1.001 (0.978–1.023) | 1.004 (0.987–1.021) | 1.011 (0.982–1.042) | 0.988 (0.954–1.024) | 0.446 | 18% / 13% (58%) |
| Transplant immunosuppressants | 0.999 (0.993–1.005) | 0.998 (0.992–1.005) | 1.000 (0.995–1.006) | 0.999 (0.990–1.009) | 0.999 (0.992–1.006) | 0.954 | 4% / 6% (44%) |
| Proton pump inhibitors | 0.996 (0.955–1.039) | 0.997 (0.953–1.043) | 0.992 (0.955–1.029) | 1.033 (0.979–1.090) | 0.966 (0.900–1.037) | 0.253 | 32% / 28% (72%) |
| Statins | 0.992 (0.952–1.034) | 0.985 (0.943–1.030) | 0.989 (0.954–1.025) | 0.996 (0.940–1.055) | 0.992 (0.922–1.068) | 0.954 | 27% / 29% (68%) |
| Metformin | 0.966 (0.934–0.998) | 0.958 (0.924–0.992) | 0.964 (0.935–0.994) | 0.967 (0.913–1.024) | 0.999 (0.939–1.062) | 0.576 | 0% / 38% (32%) |
| Insulins | 0.966 (0.929–1.005) | 0.971 (0.929–1.014) | 0.972 (0.940–1.005) | 1.028 (0.974–1.085) | 0.921 (0.866–0.980) | 0.038 | 0% / 39% (38%) |
| Fluoroquinolones | 1.005 (0.992–1.017) | 1.004 (0.991–1.018) | 1.003 (0.991–1.016) | 1.010 (0.995–1.026) | 0.993 (0.979–1.009) | 0.185 | 15% / 6% (55%) |
| All antibacterials | 0.996 (0.955–1.039) | 1.003 (0.957–1.052) | 0.995 (0.958–1.033) | 1.000 (0.957–1.045) | 0.998 (0.967–1.031) | 0.945 | 32% / 28% (73%) |
| Vitamin D | 1.007 (0.987–1.027) | 1.009 (0.987–1.031) | 1.007 (0.988–1.025) | 1.001 (0.975–1.028) | 1.007 (0.980–1.033) | 0.827 | 24% / 9% (64%) |
| Levothyroxine (negative control) | 0.962 (0.933–0.992) | 0.956 (0.926–0.988) | 0.965 (0.939–0.993) | 0.983 (0.928–1.042) | 0.972 (0.908–1.040) | 0.846 | 0% / 38% (26%) |

Poisson PML with area and year fixed effects, adjusted for age structure, international in-migration, HIV and diabetes prevalence (diabetes not adjusted for metformin and insulins); SEs clustered by area. Joint model: prescribing in t−1 and t+1 in one model on a common sample; their estimates can be negatively correlated (Table S2b gives the correlation and the model with year t added). PAF, largest population attributable fraction compatible with the upper 90% confidence limit; prevented fraction, the same from the lower 90% limit; in brackets, the PAF after dividing the upper limit by the negative control (levothyroxine) estimate, as if its bias applied to every drug.


**Table 2. Minimum detectable effects (LTLA panel, residence apportionment, exposure t−1) versus expected population effects of a 10% increase in use**

| Drug group | Individual RR/OR | Prevalence of use | PAF (negative: prevented fraction) | SE of log IRR per 10% | Expected change | MDE | MDE ÷ expected | Power | Minimum detectable PAF | RR for 80% power |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Systemic oral glucocorticoids | 4.9 | 0.9% | 3.4% | 0.0218 | 0.34% | 6.3% | 18 | 3.6% | 63% | 190 |
| Inhaled corticosteroids | 1.27 | 5.2% | 1.4% | 0.0249 | 0.14% | 7.2% | 50 | 2.8% | 72% | 51 |
| Conventional DMARDs | 1.2 | 0.5% | 0.1% | 0.0097 | 0.01% | 2.8% | 272 | 2.6% | 28% | 77 |
| Transplant immunosuppressants | 2 | 0.1% | 0.0% | 0.0031 | 0.00% | 0.9% | 172 | 2.6% | 9% | 190 |
| Proton pump inhibitors | 1.28 | 14.2% | 3.8% | 0.0213 | 0.38% | 6.2% | 16 | 3.7% | 62% | 12 |
| Statins | 0.6 | 12.8% | -5.4% | 0.0210 | -0.54% | 6.1% | 11 | 4.4% | 61% | not attainable |
| Metformin | 0.51 | 4.4% | -2.2% | 0.0169 | -0.22% | 4.8% | 21 | 3.4% | 48% | not attainable |

Expected changes use published individual-level relative risks (ORs for oral glucocorticoids and PPIs) and UK prevalence of use, assuming that prevalence of use scales with prescribing, that extra prescribing reaches new users, a homogeneous baseline risk and aligned timing. Negative PAF values are prevented fractions. MDE = exp(2.80 × SE) − 1. The ratio of MDE to expected change is essentially independent of the 10% contrast, because for small changes both scale in proportion to it. Power is one-sided power to detect the expected effect in the correct direction. Benchmarks: recorded cases (steroids), UKHSA 2024, 100% recorded, RR 4.9: 0.043%; recorded cases (steroids), UKHSA 2024, 50% recorded, RR 4.9: 0.087%; recorded cases (biological_therapy), UKHSA 2024, 100% recorded, RR 4.9: 0.078%; recorded cases (biological_therapy), UKHSA 2024, 50% recorded, RR 4.9: 0.157%; age-stratified (oral corticosteroids, RR 4.9): 0.293%; homogeneous (oral corticosteroids, RR 4.9, prevalence 0.9%): 0.339%.


## Figure legends

**Figure 1.** Assumed causal structure for area-level prescribing and TB notifications. Area fixed effects absorb stable area characteristics; year fixed effects absorb national shocks; time-varying measured factors are adjusted for; dashed nodes are unmeasured.

**Figure 2.** Within-area versus between-area variation in log prescribing rates, 294 lower-tier local authorities, 2014-2024. Orange line: a 10% increase.

**Figure 3.** Primary care prescribing and TB notifications, lower-tier local authorities, prescribing apportioned by patient residence. Blue: prescribing in the previous year (primary analysis). Orange: prescribing in the following year, estimated jointly (falsification test).

**Figure 4.** Positive control: hospital treatment for active TB (pyrazinamide DDD-years per 1,000 residents) and TB notifications, between areas (left) and within areas over time (right).

## References

1. UK Health Security Agency. Tuberculosis in England: 2025 report (data up to end of 2024), chapter 1 and supplementary tables 5, 12 and 22; and TB regional reports 2024, supplementary data. London: UKHSA; first published 8 October 2025 (GOV.UK change history; the content API timestamp reads 9 October 2025 BST), last updated 15 July 2026. https://www.gov.uk/government/publications/tuberculosis-in-england-2025-report
2. Thomas HL, Harris RJ, Muzyamba MC, et al. Reduction in tuberculosis incidence in the UK from 2011 to 2015: a population-based study. *Thorax* 2018;73(8):769–75. doi:10.1136/thoraxjnl-2017-211074. PMID 29674389
3. Aldridge RW, Zenner D, White PJ, et al. Tuberculosis in migrants moving from high-incidence to low-incidence countries: a population-based cohort study of 519 955 migrants screened before entry to England, Wales, and Northern Ireland. *Lancet* 2016;388(10059):2510–8. doi:10.1016/S0140-6736(16)31008-X. PMID 27742165
4. Jick SS, Lieberman ES, Rahman MU, Choi HK. Glucocorticoid use, other associated factors, and the risk of tuberculosis. *Arthritis Rheum* 2006;55(1):19–26. doi:10.1002/art.21705. PMID 16463407
5. Brassard P, Suissa S, Kezouh A, Ernst P. Inhaled corticosteroids and risk of tuberculosis in patients with respiratory diseases. *Am J Respir Crit Care Med* 2011;183(5):675–8. doi:10.1164/rccm.201007-1099OC. PMID 20889902
6. Castellana G, Castellana M, Castellana C, et al. Inhaled corticosteroids and risk of tuberculosis in patients with obstructive lung diseases: a systematic review and meta-analysis of non-randomized studies. *Int J Chron Obstruct Pulmon Dis* 2019;14:2219–27. doi:10.2147/COPD.S209273. PMID 31576118
7. Brassard P, Kezouh A, Suissa S. Antirheumatic drugs and the risk of tuberculosis. *Clin Infect Dis* 2006;43(6):717–22. doi:10.1086/506935. PMID 16912945
8. Keane J, Gershon S, Wise RP, et al. Tuberculosis associated with infliximab, a tumor necrosis factor α-neutralizing agent. *N Engl J Med* 2001;345(15):1098–104. doi:10.1056/NEJMoa011110. PMID 11596589
9. British Thoracic Society Standards of Care Committee. BTS recommendations for assessing risk and for managing *Mycobacterium tuberculosis* infection and disease in patients due to start anti-TNF-α treatment. *Thorax* 2005;60(10):800–5. doi:10.1136/thx.2005.046797. PMID 16055611
10. Carmona L, Gómez-Reino JJ, Rodríguez-Valverde V, et al. Effectiveness of recommendations to prevent reactivation of latent tuberculosis infection in patients treated with tumor necrosis factor antagonists. *Arthritis Rheum* 2005;52(6):1766–72. doi:10.1002/art.21043. PMID 15934089
11. Song HJ, Park H, Park S, Kwon JW. The association between proton pump inhibitor use and the risk of tuberculosis: a case-control study. *Pharmacoepidemiol Drug Saf* 2019;28(6):830–9. doi:10.1002/pds.4773. PMID 30920070
12. Li X, Sheng L, Lou L. Statin use may be associated with reduced active tuberculosis infection: a meta-analysis of observational studies. *Front Med (Lausanne)* 2020;7:121. doi:10.3389/fmed.2020.00121. PMID 32391364
13. Zhang M, He JQ. Impacts of metformin on tuberculosis incidence and clinical outcomes in patients with diabetes: a systematic review and meta-analysis. *Eur J Clin Pharmacol* 2020;76(2):149–59. doi:10.1007/s00228-019-02786-y. PMID 31786617
14. Greenland S, Morgenstern H. Ecological bias, confounding, and effect modification. *Int J Epidemiol* 1989;18(1):269–74. doi:10.1093/ije/18.1.269. PMID 2656561
15. Morgenstern H. Ecologic studies in epidemiology: concepts, principles, and methods. *Annu Rev Public Health* 1995;16:61–81. doi:10.1146/annurev.pu.16.050195.000425. PMID 7639884
16. Sheppard L, Prentice RL, Rossing MA. Design considerations for estimation of exposure effects on disease risk, using aggregate data studies. *Stat Med* 1996;15(17-18):1849–58. doi:10.1002/(SICI)1097-0258(19960915)15:17<1849::AID-SIM396>3.0.CO;2-4. PMID 8888477
17. Hudson SM, Hudson C. Is GP practice bowel, breast and cervical cancer screening coverage correlated with GP practice list inflation? *J Med Screen* 2026;33(1):1–8 (epub 17 June 2025). doi:10.1177/09691413251347408. PMID 40525516
18. Venkatesan S, et al. Correcting for the inflated adult population denominator in an English nationwide health care cohort: database analysis study. *JMIR Public Health Surveill* 2025;11:e64788. doi:10.2196/64788. PMID 41144579
19. Richards TC, et al. Using OpenPrescribing.net to evaluate neighbourhood-level prescribing of inhalers for asthma and COPD. *Sci Rep* 2025;15:18089. doi:10.1038/s41598-025-02969-x. PMID 40413267
20. Bacon S, Goldacre B. Barriers to working with National Health Service England's open data. *J Med Internet Res* 2020;22(1):e15603. doi:10.2196/15603. PMID 31929101
21. Hermans S, Boulle A, Caldwell J, et al. Temporal trends in TB notification rates during ART scale-up in Cape Town: an ecological analysis. *J Int AIDS Soc* 2015;18(1):20240. doi:10.7448/IAS.18.1.20240. PMID 26411694
22. Költringer FA, et al. The social determinants of national tuberculosis incidence rates in 116 countries: a longitudinal ecological study between 2005–2015. *BMC Public Health* 2023;23:337. doi:10.1186/s12889-023-15213-w. PMID 36793018
23. Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative controls: a tool for detecting confounding and bias in observational studies. *Epidemiology* 2010;21(3):383–8. doi:10.1097/EDE.0b013e3181d61eeb. PMID 20335814
24. Prasad V, Jena AB. Prespecified falsification end points: can they validate true observational associations? *JAMA* 2013;309(3):241–2. doi:10.1001/jama.2012.96867. PMID 23321761
25. UK Health Security Agency. Tuberculosis in England: 2021 report (presenting data to end of 2020). London: UKHSA; 2021 (added to GOV.UK 28 October 2021; corrected PDF 30 March 2022). https://assets.publishing.service.gov.uk/media/62441310e90e075f124018e8/TB_annual-report-2021.pdf
26. Morrison H, et al. Impact of COVID-19 on NHS tuberculosis services: results of a UK-wide survey. *J Infect* 2023;87(1):59–61. doi:10.1016/j.jinf.2023.04.004. PMID 37044162
27. Santos Silva JMC, Tenreyro S. The log of gravity. *Rev Econ Stat* 2006;88(4):641–58. doi:10.1162/rest.88.4.641 (not indexed in PubMed)
28. van Staa TP, Leufkens HG, Abenhaim L, et al. Use of oral corticosteroids in the United Kingdom. *QJM* 2000;93(2):105–11. doi:10.1093/qjmed/93.2.105. PMID 10700481
29. Fardet L, Petersen I, Nazareth I. Prevalence of long-term oral glucocorticoid prescriptions in the UK over the past 20 years. *Rheumatology (Oxford)* 2011;50(11):1982–90. doi:10.1093/rheumatology/ker017. PMID 21393338
30. Gunasekara FI, Richardson K, Carter K, Blakely T. Fixed effects analysis of repeated measures data. *Int J Epidemiol* 2014;43(1):264–9. doi:10.1093/ije/dyt221. PMID 24366487
31. Thwaites GE, Nguyen DB, Nguyen HD, et al. Dexamethasone for the treatment of tuberculous meningitis in adolescents and adults. *N Engl J Med* 2004;351(17):1741–51. doi:10.1056/NEJMoa040573. PMID 15496623
32. OpenPrescribing.net, Bennett Institute for Applied Data Science, University of Oxford. Frequently asked questions. 2026. https://openprescribing.net/faq/ Accessed 14 September 2026.
33. Pealing L, Wing K, Mathur R, et al. Risk of tuberculosis in patients with diabetes: population based cohort study using the UK Clinical Practice Research Datalink. *BMC Med* 2015;13:135. doi:10.1186/s12916-015-0381-9. PMID 26048371
34. Chen YG, et al. Target trial emulation of DPP-4 inhibitors in patients with T2DM for pulmonary tuberculosis: a nationwide observational data. *BMC Med* 2025;23:587. doi:10.1186/s12916-025-04423-1. PMID 41137015
