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
  - In simulations on the real counts, the published effect was detected in {{sim_power_rr49_ltla}} of replicates, no better than the {{sim_null_rejection_ltla}} false-positive rate with no effect.
- **UK-born TB.** A regional association between prednisolone dose and UK-born TB was implausibly large and was accompanied by failed negative-control and falsification tests.

**Conclusions.**
- Open English prescribing and TB notification data can be linked, but only with heavy attenuation, and ecological analyses of them cannot detect plausible population-level effects of medicines on TB.
- Apparent associations reflect confounding by migration, age and area trends.
- Causal questions require individual-level linked data analysed with target trial emulation. Surveillance of drug-associated TB is better served by more complete recording of immunosuppression in national TB surveillance.
