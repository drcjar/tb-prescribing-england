## Results (cross-sectional and panel analyses: final numbers)

### Descriptive trends, England 2014–2024
- **TB:** England TB incidence fell from 11.9/100,000 in 2014 (6,474 cases) to 7.3 in 2020, then
  rose to 9.4 in 2024 (5,490 cases).
- **Rising prescribing (2014 to 2024, items per 1,000 residents):**
  - PPIs +35% (954 to 1,288)
  - statins +31%
  - metformin +30%
  - vitamin D +42%
  - insulins +22%
  - inhaled corticosteroids +8%
- **Falling prescribing:**
  - oral corticosteroids −10% (139 to 126)
  - immunosuppressants −10%
  - all antibacterials −17%
  - fluoroquinolones −51%
  - antituberculosis drugs −67% (0.98 to 0.32)
- **Within-area vs between-area variation:** within-area variation in log prescribing rates was
  small compared with between-area variation. For oral corticosteroids the SD of area-demeaned log
  rate was 0.07, against 0.31 between areas; for other groups within-area SDs were 0.04–0.13,
  except fluoroquinolones (0.23) and antituberculosis drugs (0.60).
  (Table: `outputs/descriptives/national_prescribing_2014_2024.csv`.)

### Cross-sectional analysis (Sub-ICBs, TB 2022–24, prescribing June 2026)
- **Sample and linkage:** 105 of 106 Sub-ICBs were analysed (one had a suppressed TB count), and
  99.5% of prescribing items were linked to a Sub-ICB. Mean TB incidence across areas was
  6.9/100,000/year (range 0.7–43.1).
- **Covariates:** in a model with covariates only, TB incidence was higher where more residents
  were born outside the UK (IRR per SD 1.40, p<0.001) and lower in older populations (% aged ≥65:
  0.67, p<0.001).
- **Unadjusted associations:** almost every drug group was inversely associated with TB incidence
  (IRR per SD 0.59–0.77; e.g. oral corticosteroids 0.59, 95% CI 0.53–0.66). Metformin was the
  exception (1.24, 1.05–1.46).
- **Adjusted associations:** all estimates moved close to the null (0.89–1.02) and none survived
  false-discovery-rate correction (all q ≥ 0.20). The negative control, levothyroxine (0.94,
  0.88–1.00), was as "significant" as proton pump inhibitors (0.89, 0.80–1.00).
- **Positive control:** antituberculosis drug prescribing was not associated with TB incidence
  (unadjusted 0.96, 0.60–1.51).

### Panel analysis (UTLAs, rolling TB windows ending 2019–2024, prescribing 2014–2024)
- **Sample and linkage:** 98.1% of prescribing items were linked to a UTLA. The primary model
  included 863 area-windows from 147 UTLAs.
- **Primary estimates:** with area and window fixed effects and time-varying covariates, no drug
  group was associated with later TB incidence. IRRs per 10% within-area increase ranged from 0.982
  (levothyroxine) to 1.041 (insulins), e.g. oral corticosteroids 1.001 (0.951–1.055),
  immunosuppressants 1.006 (0.978–1.034), inhaled corticosteroids 1.013 (0.944–1.086); all
  q ≥ 0.59.
- **Sensitivity analyses:** one-year and concurrent exposure windows gave similar results.
- **Adjusting for total prescribing volume:** this produced spurious inverse associations,
  including for the negative control (levothyroxine 0.940, 0.900–0.982).
- **Falsification test:** future prescribing was associated with past TB for vitamin D (1.028,
  1.002–1.055). Without covariate adjustment, it was also associated for inhaled corticosteroids
  (0.920), insulins (0.922) and levothyroxine (0.936). This indicates confounding by area-specific
  trends that fixed effects alone do not remove.
- **Positive control:** the positive control again showed no association (1.006, 0.999–1.012).
