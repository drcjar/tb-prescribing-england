# Revision round 1: new analyses (2026-09-14)

Changes made in response to "find more/better data and do better".

## Spatial autocorrelation (`spatial_autocorrelation.py`)

Moran's I, k=5 nearest-neighbour weights, 999 permutations:

| Level | Areas | Mean log TB rate (raw) | Primary-model residuals |
|---|---|---|---|
| UTLA | 149 | I = 0.490 (p = 0.001) | I = 0.044 (p = 0.38) |
| LTLA | 292 | I = 0.415 (p = 0.001) | I = −0.014 (p = 0.70) |

Area fixed effects remove the spatial structure, so no spatial correction is needed.

## UK-born TB aged ≥65 by region (`steroid_ukborn_regional.py`)

2,401 notifications in 2015–2024. The denominator is ONS population aged 65+.

- **Oral corticosteroid items, lagged:** 1.34 (0.74–2.42), 1.06 (0.54–2.09), 1.09 (0.44–2.67).
- **Falsification test failed:** lead 3 gives 1.45 (1.01–2.09) and lead 2 gives 1.59 (1.04–2.43).
- **Prednisolone mg:**
  - lagged: 1.21–1.28 (not significant)
  - leads: 1.28–1.40 (not significant)
- **Levothyroxine (negative control):**
  - lag 1: 1.23 (0.97–1.55)
  - lead 1: 1.33 (1.05–1.69)

**Conclusion.** In the age group with the highest steroid exposure and mostly reactivation disease, the
regional design still mainly picks up confounding by trends.

## LTLA annual panel (292 lower-tier authorities; `analyze_panel_annual.py ltla`)

The primary model has 2,335 area-years, with outcome years 2017–2024. All drug groups are null
(all q ≥ 0.65). IRR per 10% within-area increase in prescribing:

| Drug group | LTLA (292 areas) | UTLA (149 areas) |
|---|---|---|
| Oral corticosteroids | 0.982 (0.944–1.021) | 0.986 (0.940–1.034) |
| Inhaled corticosteroids | 0.975 (0.925–1.027) | — |
| Immunosuppressants | 1.002 (0.982–1.022) | — |
| PPIs | 0.969 (0.918–1.022) | — |
| Levothyroxine | 0.975 (0.937–1.013) | — |
| Antituberculosis | 1.002 (0.998–1.006) | — |

Confidence intervals are about 20% narrower at LTLA than at UTLA.

**Sensitivity analyses:**
- **Asylum support (2014+):** adding it as a covariate leaves the estimates unchanged at both
  levels.
- **Total prescribing volume:** adjusting for it again produces spurious inverse associations
  (PPIs 0.92; levothyroxine 0.96 at LTLA).

## Simulation-based power, UTLA (`simulate_power.py utla 200`)

Oral corticosteroid exposure, 200 simulated datasets per scenario:

| Scenario | Detected (p < 0.05, correct direction) | Median estimated IRR per 10% |
|---|---|---|
| No effect | 4.5% (type I error) | 0.999 |
| Published RR 4.9, prevalence 0.9% | 3.0% | 1.002 |
| RR 25 | 11% | 1.017 |
| RR 100 | 57% | 1.042 |
| Direct IRR 1.02 per 10% | 17% | 1.020 |
| Direct IRR 1.05 per 10% | 75% | 1.052 |
| Direct IRR 1.10 per 10% | 100% | 1.100 |

The estimator is unbiased and well calibrated. Power to detect the published individual-level
effect equals the false-positive rate.

## Hospital medicines (SCMD), 2019–2024 (`hospital_medicines.py`)

**Method.** Trust × drug-group quantities were apportioned to local authorities using OHID 2024 acute
trust catchment shares (all admissions). Quantities are rifampicin defined daily doses (DDD) for
anti-TB drugs and approximate mg for the other groups. Trusts with catchment data account for
96–99% of quantity in every group.

**Positive control works.**
- **Between areas:** hospital anti-TB drug use vs TB incidence, 2019–24.
  - UTLA: Spearman ρ = 0.74; per SD, IRR 1.71 (1.44–2.02) unadjusted and 1.14 (1.04–1.25) adjusted.
  - LTLA: ρ = 0.52; adjusted 1.08 (1.01–1.14).
- **Within areas** (IRR per 10% increase):
  - concurrent year: 1.019 (1.005–1.034) at UTLA, 1.019 (1.005–1.033) at LTLA
  - next year (t+1): 1.017, consistent with treatment continuing
  - previous year (t−1): null (0.999), as expected

**Drug groups with plausible TB risk (UTLA):**

| Drug group | Within-area, lag t−1 | Within-area, lead t+1 | Cross-sectional adjusted (per SD) |
|---|---|---|---|
| Anti-TNF | 0.993 (0.983–1.003) | 1.006 | 0.964 (0.909–1.022) |
| Other biologics | 0.994 (0.982–1.006) | — | 0.973 |
| JAK inhibitors | 0.995 (0.989–1.001) | — | 0.978 |
| Systemic corticosteroids | 1.003 (0.989–1.018) | — | 0.967 |
| Calcineurin/antiproliferatives | 1.003 (0.993–1.012) | — | 1.055 (1.001–1.112) |

- **JAK inhibitors:** a small inverse concurrent estimate (0.990). Use rose about 13-fold over
  2019–24, so this is likely a trend artefact.
- **Calcineurin/antiproliferatives:** the positive cross-sectional association is plausibly
  confounded by transplant-centre catchments. The within-area estimate is null.

**Interpretation.**
- The positive control shows the catchment linkage can detect a real prescribing–TB signal, both
  between and within areas. This strengthens the credibility of the null results.
- High-risk hospital drugs show no within-area association, with CIs of about ±1% per 10% change.
  Expected population effects are still far smaller (see `outputs/hospital/hospital_mde.csv`).

## Public code repository

https://github.com/drcjar/tb-prescribing-england
