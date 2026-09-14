## Methods

### Study design and setting
We conducted two ecological studies of primary care prescribing and tuberculosis (TB) incidence in
England: (i) a cross-sectional analysis of Sub-Integrated Care Board locations (Sub-ICBs), and
(ii) a longitudinal panel analysis of upper-tier local authorities (UTLAs) with area and time
fixed effects. We also described trends in oral corticosteroid prescribing between 2014 and 2024
and related them to changes in TB incidence at national, regional and local authority level.
We computed the minimum detectable effects of each design and compared them with the population
effects implied by published individual-level relative risks. All data were publicly available,
aggregate and anonymised, so ethical approval was not required.

### Data sources
**TB incidence.** TB notification rates came from the UK Health Security Agency (UKHSA) TB Strategy
Monitoring Indicators on the Fingertips platform. At Sub-ICB and UTLA level these are published
only as three-year counts and rates (indicator 91361; windows 2001–03 to 2022–24). Annual rates
(indicator 91359) are published for the nine English regions and England. Counts suppressed for
disclosure control were treated as missing.

**Prescribing.** Items dispensed in the community from primary care prescribing came from the
NHS Business Services Authority English Prescribing Dataset (EPD). We totalled items by prescribing
organisation and month on the NHSBSA server. The cross-sectional analysis used June 2026
(SNOMED-coded EPD). The panel used all 132 months from January 2014 to December 2024 (BNF-coded EPD),
aggregated to practice level. Totals for June 2024 were identical in the BNF- and SNOMED-coded
releases. Oral corticosteroid (BNF 6.3.2) items and average daily quantities (ADQ) were also
extracted by substance: prednisolone, dexamethasone, hydrocortisone and other.

**Exposure groups.** Twelve groups were specified before analysis using BNF chemical substance codes
and names (eye, ear/nose and skin preparations excluded):
- **Positive control:** antituberculosis drugs (BNF 5.1.9), expected to track TB incidence through
  treatment.
- **Candidate drug groups:** oral corticosteroids, inhaled corticosteroids, non-biologic
  immunosuppressants (methotrexate, leflunomide, azathioprine, mycophenolate, calcineurin and mTOR
  inhibitors, JAK inhibitors), proton pump inhibitors, statins, metformin, insulins,
  fluoroquinolones, all antibacterials and vitamin D.
- **Negative control:** levothyroxine, with no plausible causal pathway to TB.

**Denominators and covariates.**
- **Cross-sectional analysis:** GP-registered patients by five-year age band (NHS England, June
  2026); Census 2021 percentage of residents born outside the UK; Index of Multiple Deprivation
  2025 (population-weighted LSOA scores); QOF diabetes prevalence 2024/25.
- **Panel analysis:** ONS mid-year population estimates by age; ONS international in-migration
  (components of change); diagnosed HIV prevalence and QOF diabetes prevalence (Fingertips).

**Geographic linkage.**
- **Sub-ICBs:** TB data (2024 boundaries) were re-apportioned to 2026 boundaries using mid-2022
  LSOA population weights.
- **Practices:** each practice was assigned to a local authority using its postcode (ONS Postcode
  Directory, August 2025). Local authorities were mapped to April 2023 UTLAs, with City of London
  merged with Westminster and the Isles of Scilly with Cornwall, as in the TB data.

### Statistical analysis
**Cross-sectional analysis.** Negative binomial regression of 2022–24 TB counts on each prescribing
rate (standardised), with log population offset and robust standard errors. Models were
unadjusted and adjusted for percentage non-UK-born, deprivation, percentage aged ≥65 and 15–44,
and diabetes prevalence. Further models added NHS region fixed effects, restricted to areas with
stable boundaries, or excluded London.

**Panel analysis.** Poisson pseudo-maximum-likelihood regression of three-year TB counts for rolling
windows ending in year *t*:
- **Exposure:** the log mean annual prescribing rate over years *t*−5 to *t*−3, which precedes the
  outcome window.
- **Fixed effects:** UTLA and window.
- **Offset:** log population.
- **Standard errors:** clustered by UTLA, to account for overlapping windows.
- **Time-varying covariates:** age structure, international in-migration, HIV and diabetes
  prevalence over the outcome window, plus in-migration over the exposure window.
- **Effect measure:** incidence rate ratio (IRR) per 10% within-area increase in prescribing.

Sensitivity analyses used a one-year exposure (*t*−3), concurrent exposure (*t*−2 to *t*), and
adjustment for total prescribing volume. As a falsification test we modelled prescribing in the
three years *after* the outcome window (*t*+1 to *t*+3), which cannot cause earlier TB. Multiple
testing was addressed with the Benjamini–Hochberg false discovery rate across drug groups.

**Steroid trends and change analyses.** National monthly and annual oral corticosteroid rates were
described by substance and ADQ. Changes in steroid prescribing were related to changes in TB
incidence in three ways:
- **England:** correlation of annual levels and year-on-year changes (lags 0–3 years).
- **Regions:** an annual panel of nine regions (Poisson; region and year fixed effects; lags 1–3
  years).
- **UTLAs:** long differences, i.e. change in steroid rate 2014–16 to 2019–21 against change in log
  TB incidence 2014–16 to 2022–24, weighted by baseline cases and adjusted for change in
  in-migration.

**Minimum detectable effects.** For each drug group, the design MDE is the IRR per 10% increase in
prescribing detectable with 80% power (two-sided α = 0.05), calculated from the standard error of
the primary panel model: MDE = exp(2.80 × SE). Assuming incidence ∝ 1 + *p*(RR − 1), where *p* is
the population prevalence of use and RR the published individual-level relative risk, the expected
population IRR for a 10% rise in use is [1 + 1.1*p*(RR − 1)] / [1 + *p*(RR − 1)]. This assumes no
confounding or ecological bias and is therefore favourable to detection. We report the power
available to detect the expected effect and the individual RR that would be needed to reach 80%
power.

Analyses used Python 3.14 (pandas, statsmodels). Code is available at [repository].
