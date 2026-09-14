# Peer review, round 2: Reviewer 1 (epidemiology and biostatistics)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England" (Draft 3, revised after peer review, 14 September 2026)

**Materials examined:**
- `paper/manuscript.md`, including Tables 1–3 and S1–S7
- `paper/reviews/response_round1.md`
- Code: `analyze_panel_annual.py`, `simulate_power.py`, `mde.py`, `steroid_trends.py`, `steroid_ukborn_regional.py`
- Outputs: `outputs/panel_annual_ltla_residence/panel_results.csv`, `outputs/panel_annual_utla_residence/panel_results.csv`, `outputs/power_simulation/power_summary_*.csv` and `simulations_*.csv`, `outputs/mde/*.csv`, `outputs/hospital/hospital_mde_*.csv`, `outputs/steroids/ocs_tb_by_birthplace_lag_lead.csv`, `outputs/steroids/ocs_tb_change_correlations.csv`, `outputs/spatial/morans_i_*.csv`, `outputs/descriptives/*.csv`, `PROGRESS.md`

No models were refitted. All checks below come from reading output files and code, plus simple arithmetic on reported estimates.

---

## 1. Recommendation

**Minor revision, with one issue that must be fixed before acceptance (N1).**

The revision is substantial and mostly in good faith:
- the exposures have been redefined;
- prescribing is apportioned by where patients live;
- a disease-specific positive control with its elasticity has been added;
- lag and lead are estimated jointly on a common sample;
- randomisation inference is used for the nine-region models;
- a minimum detectable PAF and a largest compatible PAF are reported;
- tables are generated from the result files.

The tables I spot-checked (Table 1, Table 2, Table 3, S1, S4, S5, S6, S3/hospital MDE) match the output files to the reported precision. The core conclusion, that these ecological designs are badly underpowered for plausible effects, is better supported than in round 1.

Four problems remain:
1. The simulation is still misinterpreted, now in a new way. It still overstates power, and the Discussion again says it "agreed" with the analytic calculation.
2. The joint lag/lead falsification logic has a collinearity problem that the text does not recognise.
3. Several statements in the text do not match the outputs.
4. The framing ("one to two orders of magnitude"; "apparent associations reflect confounding") is still stronger than the evidence.

All four can be fixed by rewriting and small extra calculations. None needs new data.

---

## 2. Status of round 1 major comments

| Item | Status | Comment |
|---|---|---|
| M1 MDE and expected-effect assumptions | **Partly** | See below |
| M2 Simulation noise and "matched analytic" | **Partly (new error)** | See N1 |
| M3 Positive control too easy | **Partly** | See below |
| M4 Hospital SEs, shared trust variation | **Partly (acceptable)** | See below |
| M5 Spatial diagnostics | **Largely addressed** | See below |
| M6 Specification | **Partly** | See below |
| M7 Covariates | **Addressed** (APS not added, with a reasonable justification) | See below |
| M8 Pre-specification and multiplicity | **Partly** | See below |
| M9 Lead tests and 9 clusters | **Partly** | See N2 and N4 |
| M10 Nulls versus equivalence | **Partly** | See N5 |
| M11 Scope of conclusions | **Not adequately addressed** | See N3 |
| M12 Result integrity | **Largely addressed for tables; new text errors** | See N6 |

### M1. MDE and expected-effect assumptions: Partly

**Done:**
- The assumptions are listed (Methods, lines 339–343).
- The minimum detectable PAF is reported (Table 2). I verified it: oral glucocorticoids 63.1% (`mde_table_ltla_residence.csv`).
- Power is labelled as one-sided, correct-direction power.
- Stratified and surveillance-based benchmarks are given (`expected_effect_benchmarks.csv`: 0.293% and 0.055%).

**Remaining:**
- **(a) "All three favour detection" (line 345) is still asserted for assumption 1**, that prevalence scales with items. Round 1 asked for the direction to be argued, not assumed. Your own Results show items and dose diverging (mg per item fell from 225 to 192, line 464). Either justify the direction or say it is unknown.
- **(b) The "stratified by age and birthplace" benchmark does not stratify by birthplace in any meaningful way.** `mde.py` lines 53–55 apply the same age-specific prevalence to UK-born and non-UK-born people. Only the age distribution of cases changes the result. The Discussion (line 628) says the reduction arises "because use is concentrated in older UK-born people with low baseline risk". The calculation does not model that. Either give birthplace-specific prevalence (even as an illustrative ratio) or describe the benchmark as "age-stratified".
- **(c) The recorded-case benchmark treats recorded steroid-associated cases as the attributable fraction** (`expected_irr_from_share`, `mde.py` line 90). Cases among users are not all attributable. The attributable share is about the exposed-case share × (RR − 1)/RR, roughly 0.43% rather than 0.55% at RR 4.9. Under-recording works in the opposite direction. The "0.05–0.1%" range (line 629) has no stated derivation. State how the upper bound was chosen.
- **(d) The invariance of the MDE/expected ratio to the 10% contrast** is described as "shown" in the response, but I cannot find it in the manuscript. Add one sentence.

### M2. Simulation: Partly, with a new interpretive error

The redesign is a real improvement. It keeps the real counts, permutes exposure trajectories, uses 500 null and 300 effect replicates with Monte Carlo SEs, adds a timing-misspecification scenario, and runs at both levels.

However, the key calibration statement is wrong, and the comparison with the analytic results is again misreported. See **N1**.

### M3. Positive control: Partly

**Done:**
- The control is reframed as validating placement.
- The elasticity is reported (0.36 UTLA and 0.40 LTLA; verified: ln 1.035 / ln 1.1 = 0.361).
- The elasticity is carried into hospital expected effects (Table S3, matches `hospital_mde_*.csv`).
- "Linked validly" is removed.

**Remaining:**
- **(a) The elasticity has no uncertainty.** From the same-year CI (1.013–1.058) it is 0.14–0.59 at UTLA, and 0.18–0.63 at LTLA. The "attenuated" ratios in Table S3 should carry this range, or at least the text should state it.
- **(b) The same-year elasticity would be below 1 even with perfect linkage.** Treatment lasts at least 6 months, so a case notified late in year t is mostly treated in year t+1. "Roughly 60% attenuation" (lines 489 and 613) therefore attributes to linkage some dilution that comes from timing. The positive control is also same-year, while the candidate drugs are analysed at t−1, so the attenuation factor is borrowed across timings. Say so.
- **(c) The primary care control failure is not stated plainly.** In `PROGRESS.md` ("Pre-specified exposure groups"; "Panel design (pre-specified before results)"), primary care antituberculosis prescribing was the pre-specified positive control. The chronology in Methods (lines 129–131) says the drug groups included "a negative-control exposure" and does not mention that the pre-specified positive control failed and was later reclassified as "descriptive". Add one sentence.
- **(d) A harder positive control was not attempted** (a plasmode with a small lagged PAF through the *apportioned hospital* exposure, or an external exposure–outcome pair). This is acceptable if acknowledged as a limitation.
- **(e) The attenuation finding is generalised beyond the hospital linkage.** See N3.

### M4. Hospital SEs: Partly (acceptable)

- Clustering by principal trust is added. It changes the SEs modestly: for example, the UTLA systemic glucocorticoid MDE rises from 4.1% to 4.7% (`hospital_mde_utla.csv`).
- Multiway clustering was not done. The number of contributing trusts and the dominant-trust share per area (M4c) are not reported.
- Report the number of principal-trust clusters, and the distribution of the dominant-trust share, in a footnote to Table 3.

### M5. Spatial diagnostics: Largely addressed

Year-specific Moran's I is reported. However:
- **"Residuals from the primary model were not [spatially clustered]" (line 456) is slightly too strong.** At LTLA, 3 of 11 years have p < 0.05 (`morans_i_summary.csv`), against about 0.55 expected by chance. 2014 has I = 0.167, p = 0.001 (`morans_i_by_year.csv`).
- Rephrase as "weak residual dependence, concentrated in 2014". Note that 2014 is the only outcome year whose t−1 exposure comes from the pre-2014 HSCIC series, which may be relevant.

### M6. Specification: Partly

**Done:**
- area-specific trends;
- log population as a covariate;
- concurrent and distributed-lag windows;
- COVID and NTBS-era restrictions (Table S1 matches `panel_results.csv`).

**Remaining:**
- **(a) The original design is not reported.** The response says its results are given in the supplement, and Methods line 147 says "Estimates from the original designs are given in the supplement". No supplementary table reports the original design: Fingertips three-year rolling outcomes with exposure t−5 to t−3. Table S1's "prior 3 years (t−3..t−1)" column is a different design. The results exist (`outputs/panel/panel_results.csv`, "primary: t-5..t-3") and should be tabulated, as promised.
- **(b) Dropped zero-exposure area-years are not counted.** `analyze_panel_annual.py` line 82 drops area-years with zero exposure. Report how many were dropped for each group, particularly for transplant immunosuppressants, oral dexamethasone and DMARDs.

### M7. Covariates: Addressed

- Diabetes adjustment is removed for metformin and insulins.
- A DAG is added (Figure 1).
- FE-only and adjusted estimates are side by side (Table S1).
- The reason for not using APS data is reasonable.
- One small gap: the specific point that migration changes *who is exposed* (so that part of within-area exposure change is compositional) is not discussed. Line 643 discusses migration only as a confounder.

### M8. Pre-specification and multiplicity: Partly

**Done:** the chronology is described, post hoc analyses are labelled exploratory, and controls are excluded from the FDR family (code line 149; verified that `q_fdr` is NaN for antituberculosis and levothyroxine).

**Remaining:**
- **(a) The chronology does not match the project log.** Methods line 129 says the first panel design was specified "before any results were seen". In `PROGRESS.md` the panel design was specified before *panel* results, but after the first-pass cross-sectional design. Please reword to match the log (see also M3c).
- **(b) The test count is wrong.** The response says "the number of tests is reported for the hospital and falsification families". The only count in the manuscript is line 452, and it does not match the outputs (N6a). No count is given for the hospital family (Table 3 contains 22 drug × level rows across 6 estimate columns) or for the regional family (Tables S5 and S6: 90 tests with randomisation p-values).

### M9. Lead tests and nine clusters: Partly

**Done:**
- Lag and lead are estimated jointly on a common sample, at LTLA (2014–2023, 2,939 area-years) and regionally (lag 2/lead 2, 2013–2022).
- A difference test is given for the regional models.
- Randomisation inference is used.
- The "7 of 90" statement is removed.
- The implausibility argument now leads.
- The 65+ results are reported in full (Table S5).
- Verified: Table S6 matches `ocs_tb_by_birthplace_lag_lead.csv`, and all regional numbers in Results lines 585–597 match Table S5.

**Remaining:** see **N2** (joint-model logic) and **N4** (randomisation inference and regional MDEs). Specifically:
- The LTLA joint models have no lag − lead difference test.
- The expected effect for UK-born people aged 65+ has not been compared with the regional MDE (round 1 M9.5).

### M10. Nulls versus equivalence: Partly

The largest compatible PAF from the 90% upper limit is reported (verified: oral glucocorticoids 17.8%, from `max_compatible_paf_pct`). See **N5**: as reported, it is not robust to the confounding the paper itself documents, and it is uninformative for protective drugs.

### M11. Scope of conclusions: Not adequately addressed

The response says "one to two orders of magnitude" was reconciled with the reported ratios. It was not. See **N3**.

### M12. Result integrity: Largely addressed for tables

Tables are generated from the result files, and every cell I spot-checked matches. Several statements in the text do not match the outputs; see **N6**.

---

## 3. New major issues

### N1. The simulation is misinterpreted: the SEs are not "conservative", and the simulation does not "agree" with the analytic power

**What the manuscript says:**
- Results, line 562: "Empirical null SD: 0.0158, against a real-data SE of 0.0218. The clustered SEs are therefore conservative".
- Discussion, line 621: "The analytic calculations and the simulation agreed".
- Discussion, line 636: the simulation found "power close to the false-positive rate for the published glucocorticoid effect".

**What the outputs show.** I derived the SE implied by each replicate as |log IRR| / z(p) from `simulations_ltla.csv`:

| Quantity (LTLA null replicates) | Value |
|---|---|
| Median replicate SE | 0.0154 |
| Empirical SD of estimates | 0.0158 |
| Real-data clustered SE | 0.0218 |

UTLA gives the same picture: median SE 0.0163, empirical SD 0.0166, real-data SE 0.0250.

Inside the simulation, the clustered SEs are therefore approximately calibrated, or slightly small. That explains the 7.0% and 6.8% two-sided rejection rates. It does not show that they are conservative. The 0.0158 vs 0.0218 gap is not a property of the SE estimator. It shows that the **permuted exposure trajectories give an estimate with about half the sampling variance of the real exposure**: (0.0158/0.0218)² = 0.53 at LTLA and 0.44 at UTLA.

A likely mechanism is that permutation breaks the correlation between an area's exposure trajectory and its own covariate trends (ageing, migration, diabetes) and neighbours' trajectories. More of the permuted exposure's within-area variation then survives partialling out.

**Consequence: simulated power is for a less collinear exposure than the one analysed.** Normal-approximation power at LTLA:

| Scenario | Using real SE (0.0218) | Using simulation SD (0.0158) | Simulated (Table S4) |
|---|---|---|---|
| IRR 1.05 per 10% | 61% | 87% | 85.0% |
| RR 100 (expected IRR 1.047) | 56% | 83% | 78.3% |
| IRR 1.02 per 10% | 15% | 24% | 21.0% |

UTLA: IRR 1.05 gives 50% analytic against 81.3% simulated.

The simulation reproduces the analytic calculation *at its own SD*, not at the real SE. This is essentially the round 1 M2(i) problem in a different form. Table 2's "RR for 80% power = 191" also cannot be reconciled with 78% simulated power at RR 100. The Discussion claim that they "agreed" was removed according to the response letter but reappears at line 621.

**Requests:**
1. Delete "The clustered SEs are therefore conservative". Report the median replicate SE next to the null empirical SD.
2. State that permuted exposures give about half the sampling variance of the real exposure, so simulated power is optimistic relative to the analytic power based on the real SE.
3. Either calibrate the simulation, or report analytic power at the real SE next to each simulated scenario in Table S4. Two calibration options:
   - permute *residualised* exposure (after area FE, year FE and covariates) and add it back to each area's own fitted exposure trajectory;
   - rescale the permuted within-area deviations so the null SD matches 0.0218.
4. Replace line 621 with an accurate statement, for example: "Both approaches showed that plausible effects are undetectable. The simulation gave higher power than the analytic calculation for large effects because permuted exposures were less collinear with covariates."
5. Abstract (line 36): "detected in 7.7% of replicates" is the two-sided rejection rate. Correct-direction power was 4.3%, against 3.2% under the null (Table S4). Use one metric consistently and call the two-sided figure "rejection".
6. Note that a 7.0% null rejection rate with 500 replicates (Monte Carlo SE about 1.1 points) points to mild anti-conservatism of the clustered Wald test. That is the opposite of "conservative".

### N2. The joint lag/lead falsification test is confounded by collinearity, and the omitted year-t term, and is then over-interpreted

**What the manuscript says.** Results lines 447–451 present opposite-signed t−1 and t+1 estimates as "a pattern expected from shared trends rather than drug effects". The Discussion (lines 642–643) and the Abstract (line 33) treat failed falsification tests as indicating residual confounding by area-specific trends.

**Problems:**

1. **Opposite signs are expected mechanically.** Within areas, log prescribing at t−1 and at t+1 are highly positively correlated (within-area SD only 0.04 for most groups; Figure 2). When two highly collinear regressors enter one model, their coefficient estimates are strongly negatively correlated. Opposite signs are therefore expected under the null from sampling error alone. The joint estimates for inhaled corticosteroids (t−1 1.076, 1.017–1.138; t+1 0.875, 0.837–0.914) and insulins (1.055 and 0.903) are exactly this seesaw (`panel_results.csv`, model "lag and lead (t-1, t+1)").
2. **The joint model omits year t.** The distributed-lag model shows strong *same-year* inverse associations for inhaled corticosteroids (0.896, 0.849–0.946) and insulins (0.931, 0.872–0.995) (Table S2). Year-t prescribing is correlated with both t−1 and t+1, so the omitted same-year association loads onto both terms. The "failed" lead may simply reflect the protopathic or concurrent same-year association the authors already describe, not trend confounding.
3. **No LTLA difference test.** The response says a test of the lag − lead difference was added. It is reported only for the regional models (Table S6), not for the LTLA joint models.
4. **The joint t−1 estimates are not in Table 1.** The primary column comes from a *separate* model, while the falsification column comes from the joint model. The nominally significant joint t−1 estimates for inhaled corticosteroids and insulins, both in the direction of harm, appear only in the text. With the area-trend result for inhaled corticosteroids (1.053, 1.003–1.105; Table S1), inhaled corticosteroids have two positive nominal estimates. That sits awkwardly with the unqualified abstract statement "No drug group was associated with notifications".

**Requests:**
- (a) Fit t−1, t and t+1 jointly (or add year t to the joint model).
- (b) Report the correlation between the lag and lead coefficient estimates (from the covariance matrix) and the lag − lead difference test at LTLA and UTLA.
- (c) Add the joint t−1 column to Table 1 or S1.
- (d) Interpret opposite signs cautiously ("consistent with collinearity or shared trends"), and mention the inhaled corticosteroid t−1 and area-trend estimates in the Results alongside the null primary estimate.

### N3. Framing still overstates what was shown

**(a) "One to two orders of magnitude"** appears in the front matter thesis (line 7), Results (line 549), Discussion (line 621) and Conclusion (line 710). The reported ratios are:

| Source | Range of MDE ÷ expected |
|---|---|
| Table 2 | 11–274 |
| Table S3, unattenuated | 21–517 |
| Table S3, attenuated | 53–1,403 |
| UKHSA-recorded benchmark | about 110 |

Several exceed two orders of magnitude, and statins (11) sits at the bottom edge. Say "from about 10 to several hundred times" or give the range. This was requested in round 1 (M11b) and the response says it was done.

**(b) "Apparent associations reflect confounding by migration, age and area trends"** (Abstract line 41; Conclusion line 710) is stated as fact. The evidence is compatible with confounding, but also with chance and collinearity (N2):
- At LTLA, 13 of 232 estimates were nominally significant (5.6%; `panel_results.csv`).
- Across the 90 regional tests, about 5 randomisation p-values are ≤ 0.05.

Both rates are close to what chance alone would give. The paper cannot treat one lag hit as spurious and a similar number of lead or negative-control hits as proof of confounding. Reword to "are compatible with residual confounding, chance or measurement error, and not with drug effects of plausible size".

**(c) The hospital attenuation is generalised to primary care.** "Open English prescribing and TB notification data can be linked, but only with heavy attenuation" (Abstract line 40, Conclusion line 710, front matter) generalises an elasticity estimated for the *hospital catchment* linkage to all the data. Primary care has no working positive control: the pre-specified one failed (M3c). Discussion line 635 applies the positive-control attenuation to "any true effect". Restrict these statements to hospital medicines, or say explicitly that primary care linkage validity is untested.

**(d) Regional negative control.** "The negative control failed in both directions" (line 597) is too strong. Levothyroxine lag 1 at age 65+ has a CI of 1.00–1.50 with randomisation p = 0.050 (Table S5).

### N4. The regional analyses are uninformative by construction, and the randomisation inference needs a caveat

**(a) Regional MDEs exceed the logical maximum.** Using the t(8) intervals in Table S5:

| Model | SE of log IRR per 10% | MDE per 10% |
|---|---|---|
| UK-born, prednisolone mg, lag 2 (0.97–1.75) | 0.128 | about 50% |
| UK-born 65+, prednisolone mg, lag 1 (0.75–1.49) | 0.149 | about 60% |

The expected effect for UK-born people aged 65+, using the authors' own 2.5% age-specific prevalence and RR 4.9, is 0.9% per 10%. Every regional MDE is therefore far above the 10% maximum attainable under the expected-effect model. Any nominally significant regional estimate *must* be a false positive or bias under that model.

This is the strongest form of the implausibility argument, and round 1 (M9.5) requested it. Report the regional MDEs and the 65+ expected effect. That would let the "UK-born association" paragraphs (lines 599–602 and 647–651) be much shorter.

**(b) The randomisation test statistic is the raw coefficient.** `randomisation_p` (`steroid_trends.py` lines 144–158) permutes the coefficient, not a studentised statistic. With nine heterogeneous regions (London dominates non-UK-born counts), a non-studentised permutation test can be size-distorted when exposure-trajectory variance differs across regions. Several randomisation p-values are notably *smaller* than the cluster-t(8) p-values:
- levothyroxine 65+ lead 1: 0.008 vs 0.028;
- oral glucocorticoids 65+ lead 2: 0.028 vs 0.055.

Use the cluster-robust t statistic as the permutation statistic, or show that the results agree.

**(c) The exchangeability assumption should be stated.** Regional exposure histories are not randomly assigned, so the test is valid for the sharp null only under exchangeability of trajectories across regions. With 499 draws, the Monte Carlo SE of p = 0.04 is about 0.009.

### N5. "Largest compatible PAF" is not robust to the documented bias and is uninformative for protective drugs

1. **It depends on the realised estimate and ignores the bias the paper documents.** The negative control, levothyroxine, is 0.970 per 10% at LTLA and 0.961 at UTLA. The paper interprets this as downward bias from area trends. If that bias applies to oral glucocorticoids, shifting the oral glucocorticoid 90% upper limit (1.0178) by the levothyroxine estimate gives about 1.050, which corresponds to a compatible PAF of about **50%**, not 18%. "Excludes PAF above 18%" should either be qualified or reported with a negative-control-calibrated sensitivity bound.
2. **It is meaningless for protective drugs.** For metformin and levothyroxine, Table 1 reports 0% because `max_compatible_paf` returns 0 when the upper limit is ≤ 1 (`analyze_panel_annual.py` lines 98–99). For drugs hypothesised to be protective (statins, metformin), report the largest compatible *prevented* fraction from the lower 90% limit.
3. **Relate the two PAF figures.** Explain briefly why the largest compatible PAF (18%) is far below the minimum detectable PAF (63%): one is conditional on an estimate that happened to fall below 1. An equivalence framing (TOST at a stated margin) would make this clearer.

### N6. Text statements that do not match the outputs

**(a) Line 452.** "Across all 195 estimates in the LTLA residence models, 11 were nominally significant, most of them lead or distributed-lag terms."

| File | Estimates | p < 0.05 |
|---|---|---|
| `outputs/panel_annual_ltla_residence/panel_results.csv` | 232 | 13 |
| `outputs/panel_annual_utla_residence/panel_results.csv` | 195 | 21 |

The 195 matches the UTLA file, not LTLA, and 11 matches neither. Of the 13 LTLA hits, only 5 are lead or distributed-lag terms, so "most" is also wrong. The others are:
- 2 joint t−1 terms;
- FE-only estimates for metformin and levothyroxine;
- the inhaled corticosteroid estimates with area trends, restricted to 2018–2024, and using ADQ;
- metformin excluding COVID years.

**(b) Number of areas analysed.** Methods lines 170–172 say 149 UTLAs and 292 LTLAs were analysed. Results, Table 1 and the outputs use 294 LTLAs (`n_areas` = 294) and 151 UTLAs. The Figure 2 caption, hard-coded in `plot_variation.py` line 50, says 292. Harmonise, and give the flow of areas (round 1 minor 10).

**(c) Line 437.** "Estimates were also materially unchanged by … restricting to outcome years 2018–2024 … ADQ instead of items". Inhaled corticosteroids became nominally inverse in both cases: 0.948 (0.902–0.996) and 0.975 (0.952–0.999). PPIs (0.947) and all antibacterials (0.957) also moved. This is not material to the conclusions, but "materially unchanged" should be qualified for inhaled corticosteroids.

**(d) Lines 562 and 621.** See N1.

---

## 4. Minor issues

1. **Table 2 "PAF" column.** Negative values for statins (−5.4%) and metformin (−2.2%) are still labelled "PAF". Relabel as "PAF / prevented fraction (−)" (round 1 minor 3, not done). Also add the SE or 95% CI from which each MDE was derived.
2. **Table 3 has no legend.** State the covariates, the period, and the exposure scale for the cross-sectional column (per SD of *log* rate). State how the elasticity is defined, and that it is shown for all drugs but is interpretable only for the positive control (round 1 minor 14).
3. **Long-difference analysis.** The windows, the ≥10-case restriction and the case weighting (`steroid_trends.py` lines 216–228) are described only in the Results (line 478), not in Methods (round 1 minor 15).
4. **Missing data.** Handling of missing covariate years, and the number of area-years lost for each model, are still not described (round 1 minor 16). `n_obs` varies (3,233 vs 3,234), and the asylum model starts in 2015 in code (`analyze_panel_annual.py` line 136) while Methods line 274 says "from 2014".
5. **RECOVERY citation.** RECOVERY is in the reference list but not cited in the text, although the response says it was cited for COVID-era hospital glucocorticoids.
6. **RECORD items.** The code lists (presentation-level definitions), SCMD product lists and DDD table, flow of areas, and handling of suppressed counts are said to be "in the supplement", but Tables S1–S7 do not contain them. Add them, or point to repository files.
7. **Order of figures and tables.** Figure 4 is cited and placed before Figure 3, and Table 3 before Table 2. Renumber in order of first appearance.
8. **FDR family.** Methods say the FDR family is the "candidate drug groups". In code it includes oral hydrocortisone and oral dexamethasone (subsets or alternative definitions of glucocorticoids) and descriptive groups such as vitamin D and all antibacterials: 13 groups. State the family explicitly.
9. **2020 count.** The Results give 4,125 for 2020 (from the 2021 report), while `england_tb_annual.csv` gives 4,123. That is fine if footnoted as "report figure". Similarly, 2024 is 5,490 in the text but the report now revises it to 5,487 (Introduction line 60). Use one convention.
10. **Hospital joint lead.** For the positive control, the following-year estimate from the joint model is 1.000 (0.988–1.012). Given that treatment runs into the next year, a positive lead would be expected. Briefly comment, since it bears on the timing interpretation of the elasticity (M3b).
11. **Randomisation p resolution.** State that p-values are computed as (1 + count)/(1 + 499), so the minimum attainable p is 0.002.
12. **Line 375.** "95% of area-years were within ±9% of their expected value" refers to deviations after removing area and year means (`within_p95_abs` = 0.089). Say "after removing area and year means" to avoid confusion with model-expected values.

---

## 5. Verification summary

### 5a. Numbers that match

| Manuscript | Output | Value |
|---|---|---|
| Table 1, LTLA primary column (all 15 rows); oral glucocorticoids 0.982 (0.941–1.025); 3,233 area-years; 294 areas | `panel_annual_ltla_residence/panel_results.csv` | 0.9819 (0.9407–1.0248); 3,233; 294 |
| "All FDR q ≥ 0.77" (LTLA); "≥ 0.62" (UTLA) | same; UTLA file | minimum 0.7679; 0.621 |
| Table 1 falsification column (joint t+1) | model "lag and lead (t-1, t+1)" | all match, e.g. oral glucocorticoids 0.946 (0.906–0.987) |
| Joint t−1: inhaled corticosteroids 1.076 (1.017–1.138); insulins 1.055 (1.006–1.106) | same | match |
| Table 1 largest compatible PAF, oral glucocorticoids 18% | `max_compatible_paf_pct` | 17.75 |
| Table 2, oral glucocorticoids: MDE 6.3%, ratio 18, power 3.6%, minimum detectable PAF 63%, RR 191 | `mde/mde_table_ltla_residence.csv` | 6.306; 18.06; 0.0355; 63.06; 190.6 |
| Benchmarks 0.055%, 0.098%, 0.293%, 0.339% | `mde/expected_effect_benchmarks.csv` | match |
| Table S4 (all rows) | `power_summary_ltla.csv`, `power_summary_utla.csv` | match |
| Table S3 | `hospital/hospital_mde_*.csv` (clustered by area) | match; "0.9–4.7%" includes trust-clustered 4.69 |
| Positive control Spearman ρ 0.79; cross-sectional 1.165 (1.026–1.324) | `hospital_results_utla.csv`; `logs/plot_hospital.txt` | 0.796; match |
| Table S6; Results lines 585–597 | `steroids/ocs_tb_by_birthplace_lag_lead.csv`; Table S5 | match |
| Regional all-TB items lag 1 1.008 (0.764–1.331), p = 0.95; mg 1.064 (0.843–1.344) | `steroids/ocs_tb_change_correlations.csv` | match |
| National r = 0.17 (levels); lag-3 change r = −0.75 | same | 0.165; −0.750 |
| Long difference: 140 UTLAs, ρ = −0.17, 0.989 (0.925–1.057) | `steroids/utla_long_difference_summary.csv` | match |
| Within-area SD 0.043 / 0.29; PPI 0.038; DMARD 0.089; ±9% | `descriptives/within_between_variation.csv` | match |
| Moran's I: residual LTLA median 0.028 (−0.016 to 0.167), 3 of 11 years; UTLA 0.017, 1 of 11 | `spatial/morans_i_summary.csv` | match |

### 5b. Discrepancies and misinterpretations

| # | Location | Issue |
|---|---|---|
| D1 | Line 452 | "195 estimates, 11 significant" (LTLA). Output: 232 estimates, 13 significant (LTLA); 195 and 21 (UTLA) |
| D2 | Line 562 | "SEs are therefore conservative". Median replicate SE 0.0154 ≈ null SD 0.0158; rejection 7.0% |
| D3 | Line 621 | "analytic calculations and the simulation agreed". Analytic power at real SE for IRR 1.05 is 61% vs 85% simulated (LTLA); 50% vs 81% (UTLA) |
| D4 | Lines 170–172 vs 383, Table 1, Figure 2 caption | 292/149 vs 294/151 areas |
| D5 | Line 147; response M6 | Original-design estimates "given in the supplement". No such table exists (results are in `outputs/panel/panel_results.csv`) |
| D6 | Line 36 (Abstract) | "Detected in 7.7%" is two-sided rejection; correct-direction power was 4.3% |
| D7 | Line 7, 549, 621, 710 | "One to two orders of magnitude" vs reported ratios of 11–517 (up to 1,403 attenuated) |

---

*Reviewer 1*
