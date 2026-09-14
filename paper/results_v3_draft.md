## Results

### Prescribing, TB notifications and within-area variation

**TB notifications in England**
- Fell from 6,474 in 2014 to a low of 4,125 in 2020.
- Rose to 5,490 in 2024, when 81.5% of people notified were born outside the UK.

**Within-area variation in prescribing**
- Once prescribing was apportioned by where patients live, it varied little within areas over time.
- For systemic oral glucocorticoids, the SD of the log rate after removing area and year means was 0.043, against 0.29 between areas. 95% of area-years were within ±9% of their expected value.
- PPIs (0.038) and levothyroxine (0.043) were similar; conventional DMARDs varied more (0.089).
- A 10% within-area change in prescribing is therefore at the edge of the observed data (Figure 2).

{{figure:variation}}

### Primary care prescribing and TB notifications (panel analyses)

**Primary analysis** (294 lower-tier authorities, 3,233 area-years, outcome years 2014–2024)
- No drug group was associated with notifications in the following year (Table 1; all FDR q ≥ 0.77).
- Systemic oral glucocorticoids: IRR 0.982 (95% CI 0.941–1.025) per 10% within-area increase.

Other groups (same scale, 95% CI):

| Drug group | IRR |
|---|---|
| Oral hydrocortisone | 1.002 (0.990–1.014) |
| Inhaled corticosteroids | 0.981 (0.935–1.029) |
| Conventional DMARDs | 1.003 (0.984–1.023) |
| Transplant immunosuppressants | 0.999 (0.993–1.005) |
| Proton pump inhibitors | 1.009 (0.967–1.054) |
| Statins | 1.000 (0.960–1.041) |
| Metformin | 0.969 (0.938–1.001) |
| Levothyroxine (negative control) | 0.970 (0.938–1.003) |

- Metformin's inverse point estimate was matched in size by the negative control, levothyroxine.

{{figure:forest}}

{{table:table1_primary_care_panel}}

**Largest attributable fraction compatible with the data** (upper 90% confidence limit)
- Systemic oral glucocorticoids: 18%
- Conventional DMARDs: 19%
- Transplant immunosuppressants: 4%

**Robustness**
- Upper-tier geography (151 areas, 1,661 area-years) gave similar results:
  - systemic oral glucocorticoids 0.987 (0.940–1.037); all FDR q ≥ 0.62
  - the negative control, levothyroxine, was nominally inverse at 0.961 (0.930–0.994), the same size as metformin (0.964, 0.929–1.000). This suggests residual confounding by trends.
- Apportioning prescribing by practice postcode gave similar results: lower-tier oral glucocorticoids 0.983 (0.948–1.019).
- Estimates were also materially unchanged by:
  - a three-year prior exposure window
  - adjustment for the LTBI programme or asylum support
  - excluding COVID-affected years
  - log population as a covariate
  - restricting to outcome years 2018–2024 (oral glucocorticoids 0.986, 0.944–1.030)
  - restricting to EPD-era exposure (0.991, 0.950–1.033)
  - ADQ instead of items (Table S1)
- Area-specific linear trends moved inhaled corticosteroids to 1.053 (1.003–1.105).

**Falsification tests** (prescribing in years t−1 and t+1 estimated jointly)
- Several drug groups showed opposite-signed lag and lead estimates, a pattern expected from shared trends rather than drug effects:
  - inhaled corticosteroids: t−1 1.076 (1.017–1.138), t+1 0.875 (0.837–0.914)
  - insulins: t−1 1.055 (1.006–1.106), t+1 0.903 (0.852–0.957)
  - systemic oral glucocorticoids: t+1 0.946 (0.906–0.987)
- Across all 195 estimates in the LTLA residence models, 11 were nominally significant, most of them lead or distributed-lag terms.

**Spatial dependence**
- Raw TB notification rates were strongly spatially clustered in every year (Moran's I 0.25–0.39 lower-tier; 0.40–0.49 upper-tier).
- Residuals from the primary model were not:
  - lower-tier: median I 0.028 (range −0.016 to 0.167), nominally significant in 3 of 11 years
  - upper-tier: median I 0.017, nominally significant in 1 of 11 years.

### Oral glucocorticoid prescribing trends and changes in TB notifications

**National trends, 2011–2024** (standard GP practices)
- Systemic oral glucocorticoid items rose from 115 to 132 per 1,000 residents in 2011–2016, then fell to 111 in 2024. Most of the fall came in 2020–21 (Figure 3).
- Prednisolone-equivalent mg per item fell from 225 to 192, so courses became smaller.
- Oral hydrocortisone items, mainly replacement therapy, rose from 5.3 to 9.1 per 1,000.

{{figure:ocs_trends}}

**Correlation with national TB trends**
- National notification rates and prescribing were not correlated in levels (14 years; r = 0.17).
- Year-on-year changes were not correlated at lags of 0–2 years.
- At a 3-year lag, one of eight correlations was nominally significant and inverse (r = −0.75).

**Regional and local changes**
- In the regional panel (9 regions, 2012–2024), adjusted estimates were null:
  - items, lag 1: 1.008 (0.764–1.331); randomisation p = 0.95
  - prednisolone mg, lag 1: 1.064 (0.843–1.344).
- Across 140 upper-tier authorities, changes in prescribing (2014–16 to 2019–21) and in notifications (2014–16 to 2022–24) were weakly inversely related before adjustment (Spearman ρ = −0.17). After adjustment for change in in-migration they were unrelated (ratio per 10% 0.989, 0.925–1.057).

### Hospital medicines

**Coverage**
- After reassigning merged trusts to their successors, 98–100% of defined daily doses (DDD) in every drug group and year came from trusts with catchment data (Table S7).

**Positive control: active-TB treatment** (upper-tier authorities)
- Between areas: tracked notifications (Spearman ρ = 0.79; adjusted IRR per SD 1.17, 1.03–1.32).
- Within areas, same year: 1.035 (1.013–1.058) per 10% increase.
- Previous year: 1.005 (0.995–1.014). Following year, estimated jointly: 1.000 (0.988–1.012).
- The within-area elasticity was 0.36 (0.40 at lower-tier level): even a disease-specific drug was recovered with roughly 60% attenuation.
- Rifamycin/isoniazid products behaved similarly (same year 1.035).

{{figure:hospital}}

**Candidate drugs**
- No drug group with plausible TB risk was associated with notifications in the following year (Table 3). At upper-tier level, per 10% increase:

| Drug group | IRR, previous year |
|---|---|
| TNF inhibitors | 0.989 (0.972–1.006) |
| IL-6 inhibitors/abatacept | 1.000 (0.992–1.008) |
| JAK inhibitors | 0.994 (0.987–1.001) |
| Rituximab | 0.998 (0.985–1.011) |
| Calcineurin/mTOR inhibitors | 1.008 (0.996–1.020) |
| Antiproliferatives | 0.996 (0.978–1.014) |
| Systemic glucocorticoids | 1.019 (0.991–1.048) |

- The negative controls were null: low-TB-risk biologics 1.001 (0.985–1.018); levetiracetam 1.014 (0.985–1.043).
- Clustering by principal trust or using elective catchments barely changed the estimates.
- Lower-tier results were concordant.
- JAK inhibitors showed small inverse same-year estimates (0.993). These were not reproduced with previous-year or following-year exposure and are consistent with trends in uptake.

{{table:table3_hospital}}

### Minimum detectable effects and expected population effects

**Primary care, oral glucocorticoids** (lower-tier panel)
- Minimum detectable effect (MDE): 6.3% per 10% increase in prescribing.
- Expected effect under published relative risks and prevalence: 0.34% (Table 2).
  - Stratified by age and place of birth: 0.29%.
  - Based on UKHSA-recorded steroid-associated notifications: 0.055%.
- The design could therefore detect only effects about 18–110 times larger than expected.
- The MDE corresponds to a drug responsible for more than half of all notifications.
- For the other candidate groups, MDEs exceeded expected effects by one to two orders of magnitude.

**Hospital medicines**
- MDEs were smaller (0.9–4.7% per 10% increase), but so were expected effects.
- TNF inhibitors (SCMD-derived prevalence 0.34%):
  - RR 4 without latent TB screening implies an expected change of 0.10% (MDE 25× larger).
  - A screening-attenuated RR implies 0.02% (MDE 113× larger).
  - Further attenuation by the positive-control elasticity widens these gaps (Table S3).
- UKHSA-recorded biologic-associated notifications imply 0.098%.

**Simulation** (permutation-based, real notification counts; Table S4)
- **Calibration.**
  - False-positive rate: {{sim_null_rejection_ltla}} at lower-tier level ({{sim_null_rejection_utla}} upper-tier).
  - Empirical null SD: {{sim_null_sd_ltla}}, against a real-data SE of {{sim_real_se_ltla}}. The clustered SEs are therefore conservative for the estimate, but the slightly raised false-positive rate shows that permuted exposure histories still produce spurious associations with the real notification trends.
- **Published glucocorticoid effect (RR 4.9).** Power {{sim_power_rr49_ltla}} (upper-tier {{sim_power_rr49_utla}}).
- **Larger individual relative risks.** Power {{sim_power_rr25_ltla}} for RR 25 and {{sim_power_rr100_ltla}} for RR 100.
- **Direct population effects.** Power {{sim_power_irr102_ltla}} for IRR 1.02 per 10%, {{sim_power_irr105_ltla}} for 1.05 and {{sim_power_irr110_ltla}} for 1.10.
- **Effect acting through same-year prescribing** (analysed with previous-year exposure). Power {{sim_power_irr105_concurrent_ltla}} for 1.05 and {{sim_power_irr110_concurrent_ltla}} for 1.10.

{{table:table2_mde}}

### Regional analyses by place of birth and age

**Non-UK-born notifications**
- Oral glucocorticoid prescribing in earlier years was not associated with notifications (lag 1–3: 0.92–1.02).
- The falsification test failed: prescribing three years later predicted earlier notifications (1.49, 1.17–1.90; randomisation p = 0.01).

**UK-born notifications**
- Prednisolone-equivalent mg:
  - Lagged estimates were imprecise positive values (lag 2: 1.30, 0.97–1.75; randomisation p = 0.08).
  - With lag and lead estimated jointly, lag 1.41 and lead 0.85 (difference p = 0.04; randomisation p for lag = 0.04) (Table S6).
- Oral glucocorticoid items: null (lag 2 joint 1.22).

**UK-born notifications at age ≥65**
- Glucocorticoid prescribing was not associated with notifications.
- The falsification test failed for glucocorticoid items (lead 2: 1.74, 0.99–3.07; randomisation p = 0.03).
- The negative control failed in both directions: levothyroxine lag 1 1.23 (1.00–1.50; p = 0.05) and lead 1 1.37 (1.04–1.79; p = 0.01).

**Interpretation of the one nominal association**
- The UK-born association with prednisolone mg is implausibly large. Under the model used for expected effects, a 10% increase in use can raise incidence by at most 10%.
- Falsification tests and the negative control failed at similar magnitudes in the same regional design.
- We therefore interpret it as residual confounding by regional trends in a nine-cluster design, not a drug effect.

{{figure:ukborn}}
