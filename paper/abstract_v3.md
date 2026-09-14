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
- **Linkage.** Hospital active-TB treatment tracked TB notifications between areas (Spearman ρ = 0.81) and within areas in the same year (incidence rate ratio [IRR] 1.035, 95% CI 1.009–1.061, per 10% increase). The within-area elasticity was only 0.36–0.40, indicating substantial attenuation even for a disease-specific drug.
- **Primary care.** No drug group was associated with notifications in the following year. For systemic oral glucocorticoids the IRR was 0.969 (0.929–1.012) per 10% within-area increase.
- **Hospital medicines.** TNF inhibitors (0.989, 0.972–1.007), JAK inhibitors and other immunosuppressants were null. Hospital systemic glucocorticoids had a small nominal association (1.024, 1.001–1.046) that was not robust to clustering by trust or to excluding COVID-19 years.
- **Falsification and negative control.** The negative-control exposure showed inverse estimates similar in size to metformin, and following-year prescribing was inversely associated with notifications for several groups. With collinear adjacent-year exposures these tests are weak, but the pattern is compatible with residual confounding by area-specific trends.
- **Power.**
  - For oral glucocorticoids, the MDE (6.3% per 10% increase) was about 18 times the effect expected from published relative risks (0.34%), and about 70–140 times that implied by UKHSA-recorded steroid-associated TB (0.04–0.09%).
  - In simulations on the real counts, the null hypothesis was rejected for the published effect in {{sim_power_rr49_ltla}} of replicates, no more often than with no effect ({{sim_null_rejection_ltla}}); simulated power exceeded analytic power at the real standard error.
- **UK-born TB.** A regional association between prednisolone dose and UK-born TB was implausibly large, not significant by randomisation inference, dependent on London, and accompanied by failed negative-control and falsification tests.

**Conclusions.**
- Hospital medicines data could be linked to TB notifications only with heavy attenuation, and no working positive control was available for primary care. Ecological analyses of these data cannot detect plausible population-level effects of medicines on TB.
- Apparent associations are compatible with residual confounding, chance or measurement error, not with drug effects of plausible size.
- Causal questions require individual-level linked data analysed with target trial emulation. Surveillance of drug-associated TB is better served by more complete recording of immunosuppression in national TB surveillance.
