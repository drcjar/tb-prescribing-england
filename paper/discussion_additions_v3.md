### Why population effects of these medicines are expected to be small

Three features of how these medicines are used in England shrink their expected population
signal below the figures implied by relative risk × prevalence.

**Screening before treatment.**
- Since the BTS recommendations of 2005, people starting anti-TNF therapy have been assessed and
  treated for latent infection [BTS 2005]. NICE recommends testing immunocompromised adults [NG33].
- Screening is also standard before JAK inhibitors and other biologics.
- In the Spanish BIOBADASER registry, TB rates on TNF antagonists fell by 78% after screening
  recommendations were introduced [Carmona 2005]. Risk was about seven times higher when the
  recommendations were not followed [Gómez-Reino 2007].
- Most growth in biologic use during 2019–2024 therefore occurred under screening, probably in
  lower-risk populations. The relative risk relevant to a marginal increase in use is well below
  historical estimates.
- Oral glucocorticoids rarely trigger screening, so residual drug-associated TB is more plausible
  for them than for biologics.

**Surveillance counts.**
- UKHSA recorded immunosuppression due to steroids in 30 and due to biological therapy in 54 of the
  5,490 people notified with TB in 2024 [UKHSA 2025].
- Even allowing for incomplete recording, a 10% change in use would then shift national
  notifications by about 0.05–0.1%. That is well below every minimum detectable effect in this
  study.

**Where use is concentrated.** Use is concentrated in older UK-born people, whose baseline TB risk
is about one-twentieth that of people born abroad. Stratifying by age and place of birth lowers the
expected effect of oral glucocorticoids from 0.34% to 0.29% per 10% increase.

### Protopathic bias and timing

- **Undiagnosed TB.** Oral glucocorticoids and antibacterials are prescribed for respiratory symptoms
  before TB is diagnosed, and glucocorticoids are part of treatment for TB meningitis and
  pericarditis [Thwaites 2004].
- **Timing.** Same-year associations are therefore not interpretable as causal. Our primary exposure
  (previous year) is closer to the months-long window in which drug-associated TB presents
  [Keane 2001], but it still averages over a calendar year.
- **The published estimates.** The same protopathic bias probably inflates the individual-level
  estimates we used [Jick 2006].

### The positive control

**What it shows.**
- Hospital active-TB treatment tracked notifications between areas and, weakly, within areas.
- Within areas, prescribing in the previous year and in the following year was not associated with
  notifications, as expected.

**What it does not show.**
- The within-area elasticity was about 0.4, not 1. Even a drug used almost exclusively for the
  outcome is recovered with roughly 60% attenuation. The likely causes are:
  - catchment apportionment error;
  - regional referral of complex TB;
  - the timing of supply;
  - dilution by other uses.
- It does not show that a medicine affecting a small fraction of the population can be detected.
  Any such effect would be attenuated similarly, widening the gap between expected and detectable
  effects.
- A positive control in primary care prescribing is not possible: TB treatment is not delivered
  there, and primary care antituberculosis prescribing did not track notifications.

### Implications for TB programmes

- **What the null result does not mean.** It does not mean glucocorticoids, biologics or JAK
  inhibitors are unimportant for patients. Drug-associated TB is clinically serious, often
  extrapulmonary or disseminated, and largely preventable.
- **Surveillance.** Monitoring is better served by more complete and detailed immunosuppression
  fields in NTBS (drug class, time since starting, whether latent TB screening was done and treated)
  than by ecological analyses of prescribing.
- **Audit.** The actionable lever is auditing latent TB screening before biologics, JAK inhibitors
  and high-dose, long-term glucocorticoids.
- **Data request.** Aggregate UKHSA tables would allow population monitoring of the strata where
  drug-associated reactivation matters: notifications with recorded biological-therapy or steroid
  immunosuppression, and notifications by area, year, place of birth, age and time since entry.

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
