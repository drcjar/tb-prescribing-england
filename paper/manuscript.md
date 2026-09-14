---
title: "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB incidence in England"
short_title: "Prescribing and TB in England"
article_type: "Original research · Ecological study"
date: "Draft 2, 14 September 2026"
authors: "[Authors to be confirmed]"
thesis: "Hospital TB-drug use tracks TB incidence, so the linkage works; yet for oral corticosteroids the smallest detectable effect (5.8% per 10% more prescribing) is 17 times the effect expected from published relative risks (0.34%)."
---

## Abstract

**Background.** Corticosteroids, biologics and other immunosuppressants increase individual risk of tuberculosis (TB). Openly published English prescribing and TB surveillance data could, in principle, be linked to study these relationships at population level. We assessed whether such ecological analyses can detect drug–TB associations, and why they may not.

**Methods.**

- **Exposures.** Practice-level primary care prescribing (NHSBSA English Prescribing Dataset, 2014–2024) for 12 pre-specified drug groups, including a positive and a negative control exposure. Hospital medicines use (Secondary Care Medicines Data, 2019–2024), apportioned to local authorities with acute trust catchment populations.
- **Outcomes.** Annual UKHSA TB notifications for 149 upper-tier and 292 lower-tier local authorities, and by region and place of birth.
- **Designs.** Cross-sectional models, and Poisson fixed-effects panels with lagged exposures, lead-exposure falsification tests, spatial diagnostics, and analytic and simulation-based power.

**Results.**

- **Positive control.** Hospital antituberculosis drug use tracked TB incidence both between areas (Spearman ρ = 0.74) and within areas over time (incidence rate ratio [IRR] 1.019, 95% CI 1.005–1.034, per 10% increase). The linkage can therefore detect a real signal.
- **Cross-sectional analyses.** Inverse associations between primary care prescribing and TB disappeared after adjustment for country of birth and age.
- **Within-area analyses.** No drug group was associated with subsequent TB incidence. Lower-tier oral corticosteroids gave an IRR of 0.982 (0.944–1.021) per 10% increase. Hospital anti-TNF biologics (0.993, 0.983–1.003), JAK inhibitors and systemic corticosteroids were also null.
- **Power.** In simulations, power to detect the published oral corticosteroid effect (RR 4.9, prevalence 0.9%) was 3.0%, equal to the false-positive rate. An individual RR above 100 was needed for even 57% power.
- **UK-born TB.** A regional association with prednisolone dose was implausibly large and did not survive multiple-testing correction. In people aged 65 and over, the design failed its falsification test.

**Conclusions.** Open prescribing and TB data can be linked validly, but they cannot detect plausible population-level effects of medicines on TB in England: expected effects are one to two orders of magnitude below what these designs can resolve. Causal questions need individual-level linked data.

## Introduction

TB remains a public health problem in England. After falling to a low of 4,125 notifications in 2020, notifications rose by 13% in 2024 to 5,480 [1]. Most cases occur in people born outside the UK, many through reactivation of infection acquired abroad [1,2], and recent national trends have been driven largely by migration and screening policy [3,4].

Host factors, several of them shaped by medicines, also modify TB risk:

- Current oral glucocorticoid use is associated with a five-fold increase in risk, rising with dose [5].
- Inhaled corticosteroids and conventional disease-modifying drugs carry smaller increases [6–8].
- Anti-TNF biologics carry large increases [32].
- Proton pump inhibitors are associated with increased risk, and statins and metformin with lower risk [9–11].

England publishes monthly prescribing for every general practice, hospital medicines use by trust, and TB notifications by local authority. Linking these is a low-cost way to generate or test hypotheses about medicines and TB. Such ecological analyses face four problems:

- confounding by area characteristics;
- cross-level bias, which covariate adjustment cannot remove when effects differ between groups [12,13];
- power that depends on the number of areas rather than data volume [14];
- limitations of the datasets themselves, including inflated practice lists that track population mobility [15,16] and prescribing patterned by deprivation and disrupted by COVID-19 [17].

We found no previous study linking area-level prescribing to TB. The closest analogues show that drugs with large individual effects can produce weak population signals, and that between- and within-area associations can have opposite signs [18,19].

We asked whether open English prescribing data can detect drug–TB associations at population level. We combined four elements:

- cross-sectional and fixed-effects designs at two geographic scales;
- primary care and hospital medicines, including a positive control that validates the linkage;
- negative control exposures and falsification tests [20,21];
- TB in UK-born and older people, which is less influenced by migration [22].

We quantified the smallest effects these designs could detect, both analytically and by simulation.

## Methods

### Data sources

All data were public, aggregate and anonymised; ethical approval was not required. Code and processed data are available at https://github.com/drcjar/tb-prescribing-england.

**Primary care prescribing.**

- **Source:** the NHS Business Services Authority English Prescribing Dataset (EPD) [30,40]. It records items dispensed in the community from primary care prescriptions.
- **Extraction:** we aggregated items by practice and month on the NHSBSA server for January 2014–December 2024. The cross-sectional analysis used June 2026.
- **Data checks:** the BNF- and SNOMED-coded releases gave identical national totals for June 2024. Standard GP practices (ODS prescribing setting RO76) accounted for 98.6% of items.
- **Prednisolone dose:** because the average daily quantity field is not populated for corticosteroids, we derived dose as tablets dispensed multiplied by tablet strength.

**Hospital medicines.**

- **Source:** NHS Secondary Care Medicines Data (SCMD), which reports monthly quantities of each product by NHS trust.
- **Groups:** we aggregated products into six groups: antituberculosis drugs (positive control); anti-TNF biologics; other biologics with TB risk (e.g. tocilizumab, rituximab, abatacept); JAK inhibitors; systemic corticosteroids; and calcineurin inhibitors/antiproliferatives.
- **Quantities:** rifampicin defined daily doses for antituberculosis drugs, and approximate milligrams for the other groups.
- **Mapping to areas:** we apportioned trust quantities to local authorities using the share of each trust's catchment population living in each area (OHID acute trust catchment populations, 2024, all admissions). Trusts with catchment data accounted for 96–99% of quantity in every group.

**TB notifications.**

- **Annual counts by local authority, 2001–2024:** from the UKHSA TB regional reports 2024 supplementary tables, covering upper-tier (UTLA, n = 149 analysed) and lower-tier (LTLA, n = 292) authorities. Summed to three years, these matched Fingertips three-year counts (r = 0.996).
- **Three-year counts:** Fingertips indicator 91361, for Sub-ICB locations (cross-sectional analysis).
- **By region and place of birth, with Labour Force Survey denominators:** from *TB in England 2025*, Supplementary Table 12 [1], and by region, place of birth and age from the regional reports.

**Covariates.**

- ONS mid-year population estimates by age.
- ONS international in-migration.
- Home Office asylum support by local authority (2014 onwards).
- Census 2021 country of birth.
- Index of Multiple Deprivation 2025.
- Diagnosed HIV and QOF diabetes prevalence.

**Geography.** Practices were assigned to local authorities by postcode (ONS Postcode Directory). Denominators were resident populations, which avoids list inflation.

**Primary care exposure groups.** Twelve groups were specified before analysis:

- **Positive control:** antituberculosis drugs.
- **Candidate drugs:** oral corticosteroids; inhaled corticosteroids; non-biologic immunosuppressants; proton pump inhibitors; statins; metformin; insulins; fluoroquinolones; all antibacterials; vitamin D.
- **Negative control:** levothyroxine.

### Statistical analysis

**Cross-sectional analysis.** Negative binomial regression of TB counts on each standardised prescribing rate, with a population offset and robust standard errors. Models were fitted unadjusted and adjusted for percentage non-UK-born, deprivation, age structure and diabetes prevalence. The primary care analysis used Sub-ICBs (2022–24); the hospital analysis used local authorities (2019–24).

**Panel analyses.**

- **Model:** Poisson pseudo-maximum-likelihood regression [23] of annual TB counts, with area and year fixed effects, a log population offset and SEs clustered by area, fitted separately for UTLAs and LTLAs.
- **Primary care exposure:** the log mean prescribing rate in years *t*−3 to *t*−1 before outcome year *t* (outcomes 2017–2024).
- **Hospital exposures:** analysed in the concurrent year, at lag *t*−1 (the causally ordered exposure) and at lead *t*+1.
- **Time-varying covariates:** age structure, international in-migration, HIV prevalence and diabetes prevalence.
- **Sensitivity analyses:** one-year and concurrent windows; exclusion of 2020–21; additional adjustment for asylum support; rolling three-year outcomes.
- **Falsification test:** exposure in the three years after the outcome year.
- **Effect measure:** IRR per 10% within-area increase in prescribing, with Benjamini–Hochberg false discovery rate (FDR) correction across drug groups.
- **Spatial diagnostics:** Moran's I of area-mean residuals, using 5-nearest-neighbour weights and 999 permutations.

**Oral corticosteroid change analyses.**

- **National level:** annual correlations between prescribing and TB incidence.
- **Regional level:** Poisson region and year fixed-effects models (9 regions; lags 1–3) for all TB, UK-born TB, non-UK-born TB and UK-born TB at age 65 and over. With 9 clusters, we used cluster-robust SEs with *t*(8) critical values and leave-one-region-out estimates. Checks included lead exposures, levothyroxine, PPIs and statins as comparison exposures, and exclusion of 2020–21.
- **Local authority level:** long differences, comparing change in prescribing with change in TB incidence.

**Minimum detectable effects and power.**

- **Analytic MDE:** the MDE for a 10% increase in prescribing (80% power, two-sided α = 0.05) is exp(2.80 × SE), taken from the primary models.
- **Expected effect:** assuming incidence ∝ 1 + *p*(RR − 1), a 10% relative increase in use gives an expected population IRR of [1 + 1.1*p*(RR − 1)] / [1 + *p*(RR − 1)], where *p* is prevalence of use and RR the individual-level relative risk (sources [5,6,8,9,10,11,24–29]). This ignores confounding and ecological bias, so it favours detection.
- **Simulation-based power:** we kept the real UTLA panel (areas, years, populations, covariates and oral corticosteroid prescribing) and replaced TB counts with counts drawn from the fitted null model, overdispersion matched to the data, and a known prescribing effect. We fitted the primary model to 200 simulated datasets per scenario.

Analyses used Python 3.14 (pandas, statsmodels).

## Results

### Trends

TB incidence in England fell from 11.9 per 100,000 in 2014 to 7.3 in 2020, then rose to 9.4 in 2024.

**Primary care prescribing, per 1,000 residents, 2014–2024:**

- **Rose:** proton pump inhibitors (+35%), statins (+31%) and vitamin D (+42%).
- **Fell:** oral corticosteroids (−10%) and fluoroquinolones (−51%).

Within-area variation was small relative to between-area variation: the SD of the area-demeaned log oral corticosteroid rate was 0.07, against 0.31 between areas.

**Hospital use, 2019–2024:**

- **Rose:** anti-TNF biologics (+64%) and JAK inhibitors (about 13-fold).
- **Stable:** systemic corticosteroids (+15%, with a 2020 dip).

### Positive control: hospital antituberculosis drugs

Hospital antituberculosis drug use tracked TB incidence (Figure 1).

- **Between areas:** UTLA Spearman ρ = 0.74. The IRR per SD was 1.71 (1.44–2.02) unadjusted and 1.14 (1.04–1.25) adjusted.
- **Within areas over time:**
  - Same-year use: 1.019 (1.005–1.034) per 10% increase.
  - Following-year use: 1.017 (1.003–1.032), consistent with treatment continuing into the next year.
  - Previous-year use: 0.999 (0.989–1.009), not associated.
- **Lower-tier areas:** results were similar (same-year 1.019, 1.005–1.033).

In contrast, primary care antituberculosis prescribing, which is rare, did not track TB incidence.

![**Figure 1.** Positive control. Hospital antituberculosis drug use (rifampicin defined daily doses per 1,000 residents, apportioned by trust catchment) and TB incidence across 149 upper-tier local authorities, 2019–2024. Left: between areas (period means). Right: within areas, after removing area and year means.](figures/hospital_positive_control.png)

### Cross-sectional analyses

- **Primary care prescribing:** in 105 Sub-ICB locations, TB incidence was associated with the percentage of residents born outside the UK (IRR per SD 1.40) and inversely with the percentage aged 65 and over (0.67). Almost every drug group was inversely associated with TB before adjustment (e.g. oral corticosteroids 0.59, 0.53–0.66 per SD). After adjustment, estimates were close to the null (Table 1).
- **Hospital medicines:** across UTLAs, adjusted estimates were null for anti-TNF biologics (0.96, 0.91–1.02), other biologics, JAK inhibitors and systemic corticosteroids. Calcineurin inhibitors/antiproliferatives showed a positive association (1.06, 1.00–1.11), consistent with confounding by the catchments of transplant centres; the within-area estimate was null.

### Panel analyses

**Primary care prescribing.** No drug group was associated with TB incidence at either geographic scale (Table 1, Figure 2; all *q* ≥ 0.65).

- **Oral corticosteroids:** 0.982 (0.944–1.021) across 292 LTLAs (2,335 area-years) and 0.986 (0.940–1.034) across 149 UTLAs.
- **Sensitivity analyses:** additional adjustment for asylum support, exclusion of 2020–21, alternative exposure windows and rolling three-year outcomes did not change the results.
- **Falsification test:** future vitamin D prescribing was associated with past TB (UTLA 1.026, 1.001–1.052).
- **Total prescribing volume:** adjusting for it produced spurious inverse associations, including for the negative control, so this adjustment was not used.
- **Spatial diagnostics:** raw TB rates were strongly spatially autocorrelated (Moran's I 0.49 UTLA, 0.42 LTLA; *p* = 0.001), but model residuals were not (0.04, *p* = 0.38; −0.01, *p* = 0.70).

**Hospital medicines.** Within-area estimates with exposure in the previous year were null and precise (Table 3):

- anti-TNF biologics 0.993 (0.983–1.003);
- other biologics 0.994 (0.982–1.006);
- JAK inhibitors 0.995 (0.989–1.001);
- systemic corticosteroids 1.003 (0.989–1.018).

![**Figure 2.** Fixed-effects panel estimates for primary care prescribing and annual TB notifications in 292 lower-tier local authorities. Blue: prescribing in the three years before the outcome year (primary analysis). Orange: prescribing in the three years after (falsification test). IRR per 10% within-area increase; area and year fixed effects; adjusted for age structure, in-migration, HIV and diabetes prevalence.](figures/panel_annual_ltla_forest_plot.png)

**Table 1.** Associations between primary care prescribing and TB incidence. Cross-sectional: IRR per SD of prescribing rate (105 Sub-ICBs). Panels: IRR per 10% within-area increase, exposure in the three prior years (annual TB, 2017–2024).

| Drug group | Cross-sectional, crude | Cross-sectional, adjusted | UTLA panel (149) | LTLA panel (292) | UTLA falsification (next 3 years) |
|:---|:---|:---|:---|:---|:---|
| Antituberculosis (positive control) | 0.96 (0.60–1.51) | 0.89 (0.79–1.00) | 1.004 (0.999–1.009) | 1.002 (0.998–1.006) | 1.001 (0.996–1.007) |
| Oral corticosteroids | 0.59 (0.53–0.66) | 0.97 (0.82–1.14) | 0.986 (0.940–1.034) | 0.982 (0.944–1.021) | 1.003 (0.955–1.054) |
| Inhaled corticosteroids | 0.73 (0.64–0.83) | 1.02 (0.90–1.15) | 0.968 (0.909–1.030) | 0.975 (0.925–1.027) | 0.967 (0.914–1.023) |
| Immunosuppressants | 0.68 (0.61–0.77) | 1.01 (0.93–1.09) | 1.010 (0.985–1.035) | 1.002 (0.982–1.022) | 1.006 (0.977–1.035) |
| Proton pump inhibitors | 0.66 (0.59–0.75) | 0.89 (0.80–1.00) | 0.967 (0.914–1.023) | 0.969 (0.918–1.022) | 1.046 (0.993–1.102) |
| Statins | 0.67 (0.60–0.75) | 0.93 (0.85–1.02) | 1.012 (0.951–1.076) | 1.001 (0.948–1.058) | 1.033 (0.983–1.086) |
| Metformin | 1.24 (1.05–1.46) | 0.98 (0.89–1.08) | 0.979 (0.928–1.032) | 0.979 (0.934–1.026) | 1.015 (0.972–1.060) |
| Insulins | 0.94 (0.75–1.18) | 0.97 (0.87–1.08) | 0.989 (0.924–1.058) | 0.979 (0.927–1.034) | 0.951 (0.901–1.005) |
| Fluoroquinolones | 0.77 (0.66–0.89) | 0.97 (0.90–1.03) | 1.000 (0.979–1.021) | 0.999 (0.981–1.018) | 0.997 (0.977–1.017) |
| All antibacterials | 0.65 (0.56–0.74) | 0.89 (0.78–1.01) | 0.995 (0.952–1.041) | 0.983 (0.947–1.021) | 1.010 (0.973–1.048) |
| Vitamin D | 0.73 (0.65–0.83) | 0.95 (0.88–1.02) | 1.010 (0.982–1.039) | 1.003 (0.979–1.028) | 1.026 (1.001–1.052) |
| Levothyroxine (negative control) | 0.64 (0.57–0.72) | 0.94 (0.88–1.00) | 0.967 (0.928–1.008) | 0.975 (0.937–1.013) | 0.973 (0.929–1.019) |

### Minimum detectable effects and power

**Analytic MDEs.** Designs could detect only effects far larger than those implied by published relative risks (Table 2).

- **Oral corticosteroids:** a 10% increase in use would be expected to raise TB incidence by 0.34%. The LTLA panel could detect only 5.8% (power 3.7%). An individual RR of about 153 would be needed for 80% power.
- **Other primary care groups:** the MDE exceeded the expected effect 15- to 283-fold. For protective associations (statins, metformin), no individual effect could have produced a detectable change.
- **Hospital medicines:** within-area models were more precise (MDE 0.9–2.1% per 10%). Expected effects were still 5–87 times smaller under illustrative assumptions; for example, anti-TNF biologics with RR 4–15 and prevalence 0.2% imply changes of 0.06–0.27%.

**Simulation.** Results matched the analytic calculations.

- **Calibration:** with no true effect the false-positive rate was 4.5%, and estimates were unbiased.
- **Published RR (4.9):** power was 3.0%.
- **Larger individual effects:** RR 25 gave 11% power and RR 100 gave 57%.
- **Direct population effects:** an IRR of 1.05 per 10% increase gave 75% power, and 1.10 gave 100%.

**Table 2.** Minimum detectable effects (LTLA panel) versus expected population effects. Changes in TB incidence refer to a 10% within-area increase in prescribing.

| Drug group | Individual RR | Prevalence of use | PAF | Expected change | MDE | MDE ÷ expected | Power | RR for 80% power |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| Oral corticosteroids | 4.9 | 0.9% | 3.4% | 0.34% | 5.8% | 17 | 3.7% | 153 |
| Inhaled corticosteroids | 1.27 | 5.2% | 1.4% | 0.14% | 7.8% | 54 | 2.8% | 69 |
| Immunosuppressants | 1.2 | 0.5%^a^ | 0.1% | 0.01% | 2.9% | 283 | 2.6% | 81 |
| Proton pump inhibitors | 1.28 | 14.2% | 3.8% | 0.38% | 8.0% | 20 | 3.4% | 28 |
| Statins | 0.60 | 12.8% | −5.4% | −0.54% | 8.2% | 15 | 3.9% | not attainable^b^ |
| Metformin | 0.51 | 4.4% | −2.2% | −0.22% | 7.0% | 31 | 3.1% | not attainable^b^ |

^a^ Assumed from EPD item volumes. ^b^ Even RR = 0 changes incidence by less than the MDE. PAF, population attributable fraction; MDE, minimum detectable effect (80% power, α = 0.05).

**Table 3.** Hospital medicines and TB incidence, UTLAs, 2019–2024. Within-area IRR per 10% increase; MDE per 10% increase with exposure in the previous year. Expected changes use illustrative assumptions of individual RR and prevalence.

| Drug group | Within-area, same year | Within-area, previous year | Within-area, next year | MDE | Expected change (assumption) |
|:---|:---|:---|:---|---:|:---|
| Antituberculosis (positive control) | 1.019 (1.005–1.034) | 0.999 (0.989–1.009) | 1.017 (1.003–1.032) | 1.5% | — |
| Anti-TNF biologics | 0.993 (0.983–1.002) | 0.993 (0.983–1.003) | 1.006 (0.991–1.022) | 1.5% | 0.06–0.27% (RR 4–15, 0.2%) |
| Other biologics | 0.992 (0.980–1.004) | 0.994 (0.982–1.006) | 1.007 (0.990–1.024) | 1.7% | 0.02% (RR 2, 0.2%) |
| JAK inhibitors | 0.990 (0.984–0.996) | 0.995 (0.989–1.001) | 0.995 (0.988–1.002) | 0.9% | 0.02% (RR 4, 0.05%) |
| Systemic corticosteroids | 0.993 (0.980–1.006) | 1.003 (0.989–1.018) | 1.005 (0.985–1.025) | 2.1% | 0.34% (RR 4.9, 0.9%) |
| Calcineurin inhibitors/antiproliferatives | 0.995 (0.987–1.004) | 1.003 (0.993–1.012) | 0.997 (0.986–1.009) | 1.4% | 0.06% (RR 3, 0.3%) |

### Oral corticosteroids and TB by place of birth and age

**Trends.** Oral corticosteroid items fell from 141.5 to 127.7 per 1,000 residents between 2014 and 2024. Prednisolone milligrams per resident fell 21.2%, because courses also became smaller (Figure 3). Changes in prescribing were not associated with changes in TB incidence in any of the following:

- nationally (year-on-year changes, all *p* ≥ 0.2);
- across regions (adjusted lag 1: 0.997, 0.788–1.260);
- across 138 UTLAs (long differences 1.000, 0.934–1.072).

![**Figure 3.** Oral corticosteroid prescribing in English primary care, 2014–2024: prednisolone items, other oral corticosteroid items, and prednisolone tablet milligrams per resident.](figures/ocs_national_trends.png)

**Non-UK-born TB** (36,633 notifications, 2015–2024). Oral corticosteroid prescribing was not associated with TB. The falsification test failed: future prescribing was associated with past TB (lead 3: 1.36, 1.03–1.80).

**UK-born TB** (11,876 notifications).

- **Prednisolone milligrams per resident** were associated with TB at lags of 2 years (1.37, 1.08–1.73) and 3 years (1.38, 1.04–1.83). This association:
  - passed the lead-exposure and comparison-exposure checks;
  - did not survive correction for the six steroid tests (Holm *p* = 0.09 and 0.16).
- **All adjusted regional models:** 7 of 90 were nominally significant, against 4.5 expected by chance.

**UK-born TB at age 65 and over** (2,401 notifications), the group with the highest steroid use and mostly reactivation disease.

- **Lagged prescribing:** not associated with TB (lag 1: 1.34, 0.74–2.42).
- **Falsification test:** failed. Future prescribing was associated with past TB (lead 2: 1.59, 1.04–2.43), and so was future levothyroxine prescribing (lead 1: 1.33, 1.05–1.69).

![**Figure 4.** Oral corticosteroid items per 1,000 residents (blue) and UK-born TB notification rate (orange) by UKHSA region, indexed to 2014 = 100.](figures/ocs_ukborn_tb_by_region.png)

## Discussion

### Principal findings

Linking open English prescribing and TB data is feasible and valid. Hospital antituberculosis drug use tracked TB incidence between areas and within areas over time, as it should. Yet across primary care and hospital medicines, two geographic scales and several designs, we found no credible association between medicines that modify TB risk and TB incidence.

The analytic and simulation analyses explain why. Expected population effects of these medicines are 5 to more than 100 times smaller than the smallest effects the designs can detect. Apparent associations arose, but each was explained by confounding or chance:

- crude cross-sectional associations were explained by country of birth and age;
- falsification tests failed for several exposures;
- the one nominal signal, prednisolone dose and UK-born TB, was implausibly large and fragile.

### Interpretation

**Why the positive control succeeded and the other drugs did not.** Antituberculosis drugs are used almost exclusively by people with TB, so their volume scales almost one-to-one with incidence. By contrast, a medicine that increases risk affects incidence only through the small fraction of the population exposed.

- **Oral corticosteroids:** the RR of about 5 [5] applies to roughly 1% of people [24,25], so a 10% change in use should move TB incidence by about 0.3%. This is consistent with the small population attributable fractions reported for inhaled corticosteroids (0.5%) [7].
- **Anti-TNF biologics:** the individual RR is large [32], but prevalence is lower, so expected changes are even smaller.

**Why better data did not solve the problem.** Hospital data made exposure measurement more complete and more precise (MDE about 1.5% per 10%), and lower-tier geography narrowed confidence intervals by about 20%. Neither closed a gap of one to two orders of magnitude. Power in aggregate studies depends on the number of areas [14], and prescribing varies little within areas over time [31]. The simulations show that only direct population effects of about 5% per 10% change in prescribing, implying individual RRs above 100, would be reliably detectable.

**Crude versus adjusted estimates.** The sign reversal between crude cross-sectional and adjusted or within-area estimates mirrors that reported for diabetes and TB between and within countries [19]. Ecological bias from effect modification cannot be removed by adjustment [12]. Drug-associated TB risk may differ by ethnicity [32,33].

**UK-born TB and trend confounding.** The UK-born analyses illustrate how false signals arise. UK-born TB roughly halved in most regions over the decade, driven by social risk factors, transmission and demographic change [22,34]. With only nine regions, coincident trends in prescribing produce apparent associations. The failed falsification tests in non-UK-born TB and in older UK-born people show this directly.

### Strengths and limitations

**Strengths:**

- All data were public, and code and processed data are openly available.
- The exposures, controls and falsification tests were specified in advance.
- A positive control validated the linkage.
- Internal consistency was checked:
  - the prescribing releases gave identical totals;
  - annual TB counts matched published three-year counts;
  - 98% of items linked to an area.
- Two geographic scales were used, together with spatial diagnostics.
- Power was assessed both analytically and by simulation.

**Limitations:**

- **Exposure measurement:**
  - Exposure was measured as dispensed quantities per resident, not people treated.
  - Hospital quantities mix products with different dose conventions.
  - Homecare-delivered biologics may be incompletely captured in SCMD; we could not verify this.
- **Hospital catchments:** shares derived from admissions were applied to all years and all drug groups, and may misallocate specialist services such as transplant and rheumatology centres.
- **Stratified outcomes:** TB by place of birth and age was available only by region.
- **Unmeasured confounding:** the latent TB screening programme for new migrants (area-level data end in 2019/20 and are unmatched to local authority codes) [36], social risk factors and diagnostic intensity [37] could not be adjusted for.
- **Individual relative risks:** those for proton pump inhibitors, statins and metformin come mainly from high-incidence settings, and prevalence assumptions for hospital drugs are illustrative. Neither would change the conclusion unless the true values were larger by an order of magnitude.

### Implications

Open prescribing data remain valuable for describing prescribing [30,40], and our positive control shows they can be linked validly to surveillance data. They cannot, however, estimate medicine effects on a rare outcome such as TB.

- **Causal questions:** these need individual-level linked data, for example CPRD primary care records linked to Hospital Episode Statistics and UKHSA TB surveillance, analysed with target trial emulation. Even national cohorts give wide intervals for modest RRs [39]. We found no target trial emulation of these drugs and TB; the only drug–TB emulation identified concerned DPP-4 inhibitors [38].
- **Reporting:** ecological studies of rare outcomes should report minimum detectable effects, positive controls and falsification tests alongside associations.

### Conclusion

Open prescribing and TB notification data in England can be linked validly, but ecological analyses of them cannot detect the population-level effects of medicines on TB: plausible effects lie one to two orders of magnitude below what these designs can resolve.

## Data and code availability

All inputs are publicly available:

- NHSBSA Open Data Portal: English Prescribing Dataset and Secondary Care Medicines Data;
- NHS Digital practice-level prescribing;
- UKHSA Fingertips and TB report supplementary tables;
- OHID acute trust catchment populations;
- ONS/Nomis population and migration estimates;
- Home Office asylum support statistics;
- NHS England Organisation Data Service;
- MHCLG English Indices of Deprivation 2025.

Code, processed datasets and outputs are available at https://github.com/drcjar/tb-prescribing-england.

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

*Reference titles for [2–4, 14–19, 22, 30, 33, 34, 37, 38] are abbreviated and must be checked against source records before submission.*
