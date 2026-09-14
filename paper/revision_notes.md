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
