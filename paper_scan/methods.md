## Methods

### Data

**Prescribing.** NHS Business Services Authority English Prescribing Dataset, January 2014 to
December 2024, aggregated with server-side SQL to practice by month by BNF section, giving 194
sections covering all prescribing. We restricted to standard general practices: those with NHS
Organisation Data Service prescribing setting RO76, plus codes absent from the current ODS file,
which omits practices closed before 2017, that have the standard practice code format. Without
that addition, prescribing by practices that later closed is dropped unevenly over time.

**Outcomes.** Every indicator published in OHID Fingertips for the relevant unit with counts and
denominators: 661 at upper-tier and 436 at lower-tier local authority level, and 197 at practice
level. For each indicator we kept one headline series (Persons, no inequality breakdown, the age
group with the most unit-years), mapped financial years to calendar years and excluded pooled
multi-year periods. Indicators with fewer than six single years of counts and denominators were
dropped, leaving 211 outcomes at upper-tier level and 106 at practice level.

**Units of analysis.** Three: 151 upper-tier local authorities, 294 lower-tier authorities, and
about 6,200 general practices. At area level prescribing was apportioned to areas in proportion to
where each practice's registered patients lived, using NHS Digital practice by LSOA registration
counts, since practices do not sit where their patients live. At practice level no apportionment
is needed, because exposure and outcome are measured on the same unit.

### What these data are, and are not

Every figure used here is an aggregate count published openly. For prescribing, the unit is a
practice-month: the number of items dispensed in a BNF section, with no patient identifiers and
no link between a prescription and the person who received it. For outcomes, the unit is a
practice-year or area-year: the size of a disease register, or a count of deaths, admissions or
screening tests. Nothing in this study links an individual's prescription to their own diagnosis,
and nothing identifies an individual prescriber.

"Prescribing in the year before the outcome" therefore means that the practice's total prescribing
in one calendar year is compared with its recorded disease count in the next, across practices.
It does not mean that a drug was given to a patient before that patient was diagnosed. This
distinction matters for interpretation: an aggregate temporal ordering of this kind is a weak
instrument for causal direction, which is precisely why we treat the reverse ordering as a null
rather than reading the forward one as an effect.

A related limitation applies to the outcomes. Disease registers depend on practices recording and
coding diagnoses, which is incentivised by the Quality and Outcomes Framework but varies between
practices and over time. Register counts are therefore a measure of recorded disease, not of
disease, and the difference is itself correlated with how actively a practice does everything
else, including prescribing.

### The scan

For every drug-outcome pair we fitted

    log(outcome rate) = beta * log(prescribing rate) + unit effect + year effect

with unit and year fixed effects swept out by alternating projections and standard errors
clustered by unit. Exposure was items per 1,000 residents at area level and items per 1,000
registered patients at practice level. At practice level many section-years are genuinely zero,
so a continuity correction was applied and sections prescribed by fewer than 80% of practice-years
were dropped. Estimating all sections for one outcome as a single matrix operation makes the full
scan minutes rather than hours.

### Calibration

A scan of this size will produce many associations whatever is true, so the design carries three
internal standards.

**An empirical null.** Every pair was estimated twice: with prescribing in the year *before* the
outcome, and with prescribing in the year *after*. A drug effect can only act forwards. Shared
local trends, changes in coding, and the drift of a practice or area over time act on both.
The distribution of results from the second scan is therefore what the first must beat, and we
summarise the excess with an inflation factor, the median squared z statistic divided by its
expectation under the null, which is 1 when nothing is going on.

**Positive controls.** Each drug group was paired with the disease it is prescribed for: diabetes
drugs with the diabetes register, inhaled therapy with COPD, antiepileptics with epilepsy, and so
on. Whatever the direction of causation, these must show associations. If they do not, the design
cannot detect anything and nothing else in the scan is interpretable.

**Where the variation lives.** For the same pairs we compared the correlation between units, using
unit means, with the correlation within units over time, after removing unit and year means. This
shows directly how much information the fixed effects remove.

### Worked example: immunosuppressants and tuberculosis

As a contrast to the unguided scan we report a conventional analysis of one clinically plausible
question. Systemic glucocorticoids, inhaled corticosteroids, DMARDs and transplant
immunosuppressants in primary care, and TNF inhibitors, interleukin-6 inhibitors, JAK inhibitors,
rituximab and other agents issued by NHS trusts, were related to UK Health Security Agency
tuberculosis notifications for 2014 to 2024. That analysis used Poisson models with the same fixed
effects, prescribing in the preceding year, a disease-specific positive control (hospital
treatment for active tuberculosis, measured as pyrazinamide defined daily doses), negative-control
exposures, falsification tests, minimum detectable effects compared against effects expected from
published individual-level relative risks and from national records of drug-associated
tuberculosis, and a permutation power simulation on the real notification counts. Full detail is
given in the supplement.

Analyses used Python 3.14 with pandas, NumPy, SciPy and statsmodels. All data are public and the
code and processed datasets are openly available.
