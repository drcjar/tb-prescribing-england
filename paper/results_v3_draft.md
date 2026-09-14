## Results

### Prescribing, TB notifications and within-area variation

**TB notifications in England**
- Fell from 6,474 in 2014 to a low of 4,123 in 2020 (Fingertips national series).
- Rose to 5,490 in 2024, when 81.9% of people notified were born outside the UK.

**Within-area variation in prescribing**
- Once prescribing was apportioned by where patients live, it varied little within areas over time.
- For systemic oral glucocorticoids, the SD of the log rate after removing area and year means was 0.042, against 0.29 between areas; after removing area and year means, 95% of area-years were within ±9%.
- PPIs (0.036), metformin (0.041) and levothyroxine (0.042) were similar; conventional DMARDs varied more (0.088). Prednisolone-equivalent mg (0.041) and ADQ measures (0.026–0.097) varied as little as items.
- A 10% within-area change in prescribing is therefore at the edge of the observed data (Figure 2).

{{figure:variation}}

### Primary care prescribing and TB notifications (panel analyses)

**Primary analysis** ({{n_areas_ltla}} lower-tier authorities, {{n_obs_ltla}} area-years, outcome years 2014–2024)
- No drug group was associated with notifications in the following year after correction for multiple testing (Table 1; all FDR q ≥ 0.51).
- Systemic oral glucocorticoids: IRR 0.969 (95% CI 0.929–1.012) per 10% within-area increase.

Other groups (same scale, 95% CI):

| Drug group | IRR |
|---|---|
| Oral hydrocortisone | 0.998 (0.985–1.011) |
| Inhaled corticosteroids | 0.966 (0.920–1.014) |
| Conventional DMARDs | 1.002 (0.983–1.021) |
| Transplant immunosuppressants | 0.999 (0.993–1.005) |
| Proton pump inhibitors | 0.996 (0.955–1.039) |
| Statins | 0.992 (0.952–1.034) |
| Metformin | 0.966 (0.934–0.998) |
| Levothyroxine (negative control) | 0.962 (0.933–0.992) |

- Metformin (nominal p = 0.04) was inversely associated to the same extent as the negative control, levothyroxine (p = 0.01), which has no plausible effect on TB.

{{figure:forest}}

{{table:table1_primary_care_panel}}

**Largest attributable fraction compatible with the data** (upper 90% confidence limit)
- Systemic oral glucocorticoids 5%; conventional DMARDs 18%; transplant immunosuppressants 4%.
- These bounds depend on point estimates that happened to fall below 1, and they are not robust to the bias revealed by the negative control. Dividing each upper limit by the levothyroxine estimate raised them to 44%, 58% and 44%, close to the minimum detectable attributable fractions (Table 2).
- For drugs expected to protect, the data were compatible with prevented fractions of up to 38% (metformin) and 29% (statins).

**Robustness**
- Upper-tier geography ({{n_areas_utla}} areas) gave similar results:
  - systemic oral glucocorticoids 0.974 (0.928–1.023); all FDR q ≥ 0.22
  - the negative control, levothyroxine, was nominally inverse at 0.956 (0.926–0.988), the same size as metformin (0.958, 0.924–0.992). This suggests residual confounding by trends.
- Apportioning prescribing by practice postcode gave similar results: lower-tier oral glucocorticoids 0.974 (0.939–1.010).
- For oral glucocorticoids, estimates were also materially unchanged by (Table S1):
  - a three-year prior exposure window, area-specific linear trends, or log population as a covariate
  - adjustment for the LTBI programme or asylum support
  - excluding COVID-affected years
  - restricting to outcome years 2018–2024 (0.983, 0.941–1.028) or to EPD-era exposure (0.979, 0.939–1.021).
- Inhaled corticosteroids were nominally inverse in several sensitivity analyses (for example 0.938 for outcome years 2018–2024), the direction opposite to any plausible harmful effect.

**Falsification tests** (prescribing in years t−1 and t+1 estimated jointly; Table 1 and Table S2b)
- Following-year prescribing was inversely associated with notifications for some groups:
  - inhaled corticosteroids: t−1 1.058 (0.995–1.126), t+1 0.879 (0.840–0.921); difference p < 0.001
  - insulins: t−1 1.028 (0.974–1.085), t+1 0.921 (0.866–0.980); difference p = 0.04
  - systemic oral glucocorticoids: t−1 0.990 (0.941–1.041), t+1 0.952 (0.912–0.994); difference p = 0.33.
- Within areas, prescribing in nearby years is highly correlated, so in the two-year model the t−1 and t+1 estimates were negatively correlated (−0.16 to −0.83 across groups) and opposite signs can arise by chance.
- With same-year prescribing added, previous-year terms were null for every group. Same-year terms were positive for several groups (for example proton pump inhibitors 1.128, 1.035–1.229), the direction expected from prescribing for undiagnosed TB, and following-year terms remained inverse.
- Area-specific linear trends gave inhaled corticosteroids 1.033 (0.981–1.087).
- **Multiplicity.** Of all {{n_est_ltla}} estimates in the lower-tier residence models, {{n_sig_ltla}} were nominally significant, more than the 5% expected by chance. They were concentrated in the negative control (levothyroxine, 6, all inverse), metformin (5, inverse) and inhaled corticosteroids (8, mostly inverse or following-year terms), a pattern that points to shared trends rather than drug effects.

**Spatial dependence**
- Raw TB notification rates were strongly spatially clustered in every year (Moran's I 0.25–0.39 lower-tier; 0.40–0.49 upper-tier).
- Residual dependence after the primary model was weak and concentrated in 2014:
  - lower-tier: median I 0.026 (range −0.004 to 0.163), nominally significant in 2 of 11 years (2014, I = 0.163; 2023, I = 0.079)
  - upper-tier: median I 0.009, nominally significant only in 2014 (I = 0.209).
- 2014 is the only outcome year whose previous-year exposure comes from the pre-2014 HSCIC series.

### Oral glucocorticoid prescribing trends and changes in TB notifications

**National trends, 2011–2024** (standard GP practices)
- Systemic oral glucocorticoid items rose from 119 to 132 per 1,000 residents in 2011–2016, then fell to 111 in 2024. Most of the fall came in 2020–21 (Figure 3).
- Prednisolone-equivalent mg per item fell from 225 to 192, so courses became smaller.
- Oral hydrocortisone items, mainly replacement therapy, rose from 5.5 to 9.1 per 1,000.

{{figure:ocs_trends}}

**Correlation with national TB trends**
- National notification rates and prescribing were not correlated in levels (14 years; r = 0.33, p = 0.25).
- Year-on-year changes were not correlated at lags of 0–2 years.
- At a 3-year lag, one of eight correlations was nominally significant and inverse (r = −0.75).

**Regional and local changes**
- In the regional panel (9 regions, 2012–2024), adjusted estimates were null:
  - items, lag 1: 1.034 (0.774–1.382); randomisation p = 0.80
  - prednisolone mg, lag 1: 1.094 (0.845–1.416); randomisation p = 0.57.
- Across 140 upper-tier authorities, changes in prescribing (2014–16 to 2019–21) and in notifications (2014–16 to 2022–24) were weakly inversely related before adjustment (Spearman ρ = −0.19). After adjustment for change in in-migration they were unrelated (ratio per 10% 0.983, 0.917–1.054).

### Hospital medicines

**Coverage**
- After reassigning merged trusts to their successors, 98–100% of DDD in every drug group and year came from trusts with catchment data, and 95% for levetiracetam (Table S7).

**Positive control: active-TB treatment** (pyrazinamide DDD, upper-tier authorities)
- Between areas: tracked notifications (Spearman ρ = 0.81; adjusted IRR per SD 1.23, 1.10–1.36).
- Within areas, same year: 1.035 (1.009–1.061) per 10% increase.
- Previous year: 1.001 (0.993–1.010). Following year, estimated jointly: 0.997 (0.986–1.007).
- The within-area elasticity was 0.36 (95% CI 0.10–0.62; lower-tier 0.40, 0.14–0.66). It reflects apportionment error, timing (treatment of people notified late in a year continues into the next) and variation in drug volume per person treated, not linkage error alone.
- Rifamycin/isoniazid products, which also cover latent TB and other infections, had the same elasticity (0.37, 0.22–0.51). The more specific measure gained nothing, so the attenuation is dominated by apportionment rather than drug specificity.

{{figure:hospital}}

**Candidate drugs** (prescribing in the previous year, IRR per 10% increase; Table 3 and Table S3b)

| Drug group | Upper-tier | Lower-tier |
|---|---|---|
| TNF inhibitors | 0.989 (0.972–1.007) | 0.992 (0.976–1.008) |
| IL-6 inhibitors/abatacept | 1.001 (0.992–1.009) | 1.001 (0.993–1.010) |
| JAK inhibitors | 0.994 (0.987–1.002) | 0.995 (0.989–1.002) |
| Rituximab | 0.998 (0.984–1.012) | 1.001 (0.986–1.016) |
| Calcineurin/mTOR inhibitors | 1.008 (0.996–1.020) | 1.008 (0.997–1.020) |
| Antiproliferatives | 0.996 (0.978–1.014) | 0.997 (0.982–1.013) |
| Systemic glucocorticoids (prednisolone-equivalent mg) | 1.024 (1.001–1.046) | 1.021 (1.000–1.043) |
| Dexamethasone and hydrocortisone (descriptive) | 1.008 (0.980–1.036) | 1.010 (0.984–1.036) |

- **Systemic glucocorticoids** were nominally associated with notifications in the following year at upper-tier level. The association:
  - was not robust to clustering by principal trust (1.024, 0.999–1.049) or to excluding outcome years 2020–21 (1.018, 0.969–1.069);
  - would imply, under the model used for expected effects, that hospital glucocorticoids account for about a quarter of all notifications (an IRR of 1.024 per 10% corresponds to an attributable fraction of 24%), whereas steroid-associated immunosuppression was recorded for 0.5% of notifications [UKHSA 2025].
  We interpret it as chance or confounding by hospital activity, not a drug effect.
- The negative controls were null: low-TB-risk biologics 1.002 (0.986–1.018); levetiracetam 1.014 (0.986–1.042).
- Clustering by principal trust or using elective catchments barely changed the other estimates (Table S3b).
- JAK inhibitors showed small inverse estimates (same year 0.993, 0.987–0.999; previous year excluding outcome years 2020–21 0.978, 0.961–0.996), consistent with trends in uptake rather than protection.

{{table:table3_hospital}}

### Minimum detectable effects and expected population effects

**Primary care, oral glucocorticoids** (lower-tier panel)
- Minimum detectable effect (MDE): 6.3% per 10% increase in prescribing.
- Expected effect under published relative risks and prevalence: 0.34% (Table 2).
  - Stratified by age: 0.29%.
  - Based on UKHSA-recorded steroid-associated notifications, converted to an attributable fraction: 0.043% with complete recording, 0.087% if only half are recorded.
- The design could therefore detect only effects about 18 to 140 times larger than expected.
- The MDE corresponds to a drug responsible for 63% of all notifications.
- For the other candidate groups, MDEs exceeded expected effects by factors of 11 (statins) to 272 (conventional DMARDs).

**Hospital medicines**
- MDEs were smaller (1.0–2.9% per 10% increase), but so were expected effects.
- TNF inhibitors (SCMD DDD-years per resident 0.34%):
  - An illustrative RR of 4 before latent TB screening implies an expected change of 0.10% (MDE 26 times larger at upper-tier level).
  - An RR of 1.5 with screening, which probably overstates post-screening risk, implies 0.017% (MDE 154 times larger).
  - Dividing by the positive-control elasticity widens these gaps to 72 and 426 times (Table S3).
- Across hospital scenarios, MDEs exceeded expected effects by 26 to 520 times before attenuation.
- UKHSA-recorded biological-therapy notifications imply 0.08–0.16%.

**Simulation** (permutation-based, real notification counts; Table S4)
- **Calibration.** With no effect, the two-sided test rejected in {{sim_null_rejection_ltla}} of replicates at lower-tier level ({{sim_null_rejection_utla}} upper-tier), against a nominal 5%. Within the simulation, replicate SEs (median {{sim_replicate_se_ltla}}) were close to the spread of null estimates ({{sim_null_sd_ltla}}), so the clustered test was mildly anti-conservative, not conservative.
- **Real-data precision.** The real-data SE ({{sim_real_se_ltla}}) was larger than in the simulation, because permuting exposure trajectories across areas breaks their alignment with each area's own notification trends. Simulated power is therefore optimistic, so we also give analytic power at the real-data SE.
- **Published glucocorticoid effect (RR 4.9).** Rejection {{sim_power_rr49_ltla}} (upper-tier {{sim_power_rr49_utla}}), no more often than with no effect; power in the correct direction {{sim_direction_rr49_ltla}}, against {{sim_null_direction_ltla}} with no effect.
- **Larger individual relative risks.** Rejection {{sim_power_rr25_ltla}} for RR 25 and {{sim_power_rr100_ltla}} for RR 100 (analytic power at the real SE for RR 100: {{sim_analytic_rr100_ltla}}).
- **Direct population effects.** Rejection {{sim_power_irr102_ltla}}, {{sim_power_irr105_ltla}} and {{sim_power_irr110_ltla}} for IRR 1.02, 1.05 and 1.10 per 10%; analytic power at the real SE {{sim_analytic_irr102_ltla}}, {{sim_analytic_irr105_ltla}} and {{sim_analytic_irr110_ltla}} (upper-tier, IRR 1.05: {{sim_analytic_irr105_utla}}).
- **Effect acting through same-year prescribing** (analysed with previous-year exposure). Rejection {{sim_power_irr105_concurrent_ltla}} for 1.05 and {{sim_power_irr110_concurrent_ltla}} for 1.10.

{{table:table2_mde}}

### Regional analyses by place of birth and age

**Precision**
- Regional models were very imprecise. MDEs for glucocorticoid prescribing were 45–82% per 10% increase for UK-born notifications and 46–99% for UK-born notifications at age ≥65.
- Under the model used for expected effects, a 10% increase in use can raise notifications by at most 10%. The expected effect for UK-born people aged ≥65 (prevalence of use 2.5%, RR 4.9) is 0.9%.
- Any nominally significant regional estimate must therefore reflect chance or bias.

**Non-UK-born notifications**
- Oral glucocorticoid prescribing in earlier years was not associated with notifications (lag 1–3: 0.95–1.03).
- The falsification test failed: prescribing three years later predicted earlier notifications (items 1.49, 1.17–1.89, randomisation p = 0.01; prednisolone mg 1.29, 1.03–1.60, p = 0.04).

**UK-born notifications**
- Prednisolone-equivalent mg: lagged estimates were imprecise positive values (lag 1: 1.25, 0.95–1.65, randomisation p = 0.12; lag 2: 1.33, 0.96–1.84, p = 0.16).
- With lag 2 and lead 2 estimated jointly: lag 1.45 and lead 0.88 (difference p = 0.04; randomisation p for lag = 0.23). Excluding London: 1.12 and 0.90 (difference p = 0.43; randomisation p = 0.73) (Table S6).
- Oral glucocorticoid items: null (joint lag 2: 1.27; randomisation p = 0.46).

**UK-born notifications at age ≥65**
- Glucocorticoid prescribing in earlier years was not associated with notifications.
- The falsification test failed for glucocorticoid items (lead 2: 1.68, 1.04–2.70; randomisation p = 0.04).
- The negative control, levothyroxine, was associated with notifications in the following year (lead 1: 1.38, 1.05–1.80; randomisation p = 0.04), and imprecisely with the previous year (lag 1: 1.23, 1.00–1.51; p = 0.07).

**Summary**
- Of {{n_regional_tests}} adjusted regional estimates, {{n_regional_sig}} had randomisation p ≤ 0.05, all of them falsification (lead) terms.
- The UK-born association with prednisolone mg was implausibly large, not significant by randomisation inference, and dependent on London.

{{figure:ukborn}}
