# Peer review, round 1: Reviewer 1 (epidemiology and biostatistics)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB incidence in England" (Draft 2, 14 September 2026)

**Reviewer expertise:** ecological study design, fixed-effects panel models, count regression, causal inference.

**Materials examined:** manuscript; `analyze_panel.py`, `analyze_panel_annual.py`, `simulate_power.py`, `mde.py`, `hospital_medicines.py`, `steroid_ukborn_regional.py`, `steroid_trends.py`, `spatial_autocorrelation.py`, `build_panel.py`; outputs in `outputs/` (CSV and logs); `data/processed/`; `paper/revision_notes.md`; `PROGRESS.md`. I know the primary care series is being extended back to 2011, so I focus on design and reasoning. I flag numbers where the manuscript and current outputs disagree.

---

## 1. Summary

The authors link openly published English data to see whether ecological designs can detect effects of medicines on TB incidence. The data are:

- practice-level primary care prescribing (EPD, 2014–2024; 12 drug groups);
- hospital medicines use (SCMD, 2019–2024), apportioned to local authorities using acute trust catchments;
- UKHSA TB notifications by UTLA (149), LTLA (292) and region by place of birth and age.

The designs are:

- cross-sectional negative binomial models (105 Sub-ICBs);
- Poisson pseudo-maximum-likelihood (PPML) models with area and year fixed effects and a lagged three-year mean exposure;
- lead-exposure "falsification" tests;
- regional models with 9 clusters for UK-born and non-UK-born TB;
- analytic minimum detectable effects (MDEs) compared with population effects derived from published individual relative risks;
- a plasmode power simulation.

Main claims:

1. The linkage is "valid": hospital antituberculosis drug use tracks TB between and within areas.
2. No drug group is associated with later TB.
3. Expected population effects (for example +0.34% TB per 10% more oral corticosteroid prescribing) are one to two orders of magnitude below the MDEs (for example 5.8%).
4. Ecological designs using these data therefore cannot detect plausible medicine effects on TB, and individual-level linked data are needed.

## 2. Overall assessment and recommendation

**Recommendation: major revision.**

This is a thoughtful, transparent and unusually self-critical ecological study. Its most valuable contribution is methodological: it shows, with numbers, why area-level prescribing cannot resolve drug effects on a rare outcome whose population attributable fraction (PAF) for any one drug is a few percent. Positive and negative controls, lead tests, explicit MDEs and open code are all welcome. The core conclusion, that these data are badly underpowered for plausible effects, is very likely correct and is fairly robust to the problems below.

Several parts of the argument need repair before the conclusions can be stated as strongly as they are:

- **Positive control.** It is weaker evidence of "validity" than claimed. Structurally it is a reverse-causation signal with a PAF of about 100%. Its within-area elasticity (about 0.2) actually shows heavy attenuation, which the manuscript does not discuss.
- **Simulation.** It does not reproduce the variance of the real data. It gives materially higher power than the analytic calculation, so "results matched the analytic calculations" is inaccurate.
- **Hospital inference.** Standard errors are likely too small, because apportioned exposures share trust-level variation across neighbouring areas. The spatial diagnostic cannot detect this by construction.
- **Pre-specification.** The claim is overstated. Several key components were added after initial (null) results, and the originally pre-specified positive control failed.
- **Stale results.** At least one reported result (the UTLA vitamin D falsification estimate and several others in the same column) does not match the current output files.
- **Interpreting nulls.** Nulls are interpreted informally. An equivalence or "effects excluded" framing would make the conclusions more precise and more honest.

None of these requires new data. Most require re-analysis, re-framing or clearer reporting.

---

## 3. Major comments

### M1. The MDE and expected-effect framework: sound in outline, but the assumptions need stating and stress-testing, and the most intuitive quantity is missing

**Problem.** The expected population IRR for a 10% increase in use, [1 + 1.1p(RR − 1)] / [1 + p(RR − 1)] (`mde.py`, `expected_irr`), rests on three assumptions the manuscript does not examine.

1. **Prevalence of use is proportional to items.** The authors' own data show items and dose diverging: prednisolone mg per item fell 9.2% between 2014 and 2024 (`outputs/steroids/steroid_trends_log.txt`). A 10% rise in items may reflect more or longer courses among existing users, not 10% more users. Because TB risk with glucocorticoids is dose-dependent, the direction of the error is unclear. It should be stated, not assumed to "favour detection".
2. **The same baseline risk in users and non-users.** The formula applies the RR multiplicatively to a homogeneous baseline. In England, baseline TB incidence differs about 10–15-fold by country of birth, and oral corticosteroid users are disproportionately older and UK-born, where baseline incidence is low. The share of total TB attributable to oral corticosteroids is then smaller than Levin's p(RR − 1)/(1 + p(RR − 1)). The expected effect on all-TB is overstated, and the expected effect on UK-born TB at 65+ is understated. This matters for the regional analyses (M7), where the expected effect is largest and was never calculated.
3. **Timing.** The RR of 4.9 [5] is for *current* use, and most steroid-associated TB occurs during or soon after exposure. The primary exposure window (t−3 to t−1) excludes the outcome year, so it is mis-timed relative to the risk window. That misalignment attenuates any true effect further. The expected-effect calculation assumes it away.

The "RR needed for 80% power" (for example 153) is also hard to interpret, because it holds prevalence fixed at an assumed value. A more natural quantity follows directly from the same model: because the elasticity of incidence with respect to use is roughly the PAF, the MDE maps onto a minimum detectable PAF. Solving the authors' formula:

- LTLA oral corticosteroid MDE of 5.78% per 10% (`outputs/mde/mde_table_ltla.csv`, `mde_irr_10pct_increase` = 1.0578) needs q = p(RR − 1) ≈ 1.37, that is, **PAF ≈ 58%**;
- the UTLA MDE (1.0697, `mde_table_annual.csv`) needs **PAF ≈ 70%**.

"The design can only detect a medicine to which more than half of all TB is attributable" is more transparent and more general than "RR 153". It also makes clear why the positive control (PAF about 100% by construction) is detectable.

**Why it matters.** The headline ratio "17 times" depends on these assumptions. Readers will generalise from it to other outcomes.

**Requests.**

- (a) State the three assumptions explicitly in Methods.
- (b) Report the minimum detectable PAF (or elasticity) for each drug and design, alongside or instead of "RR for 80% power".
- (c) Add a sensitivity analysis of the expected effect that allows baseline risk to differ between users and non-users. For example, stratify by UK-born/non-UK-born and age, using published age-specific prevalence of oral corticosteroid use and the region-by-birthplace incidence already in hand.
- (d) Note that the ratio MDE/expected is approximately invariant to the "10%" contrast, since both scale roughly linearly in log exposure. The 10% framing is harmless, but readers should be told this.
- (e) Relate the per-10% contrast to observed variation. The within-area SD of the annual log oral corticosteroid rate is 0.071 (`outputs/descriptives/national_prescribing_2014_2024.csv`) and is smaller for three-year means. A 10% within-area change is therefore towards the edge of the observed data.
- (f) The "Power" column in Table 2 (`power_for_expected` in `mde.py`) uses a one-sided normal approximation, Φ(|log E|/SE − 1.96). That is why the values (2.6–3.9%) are below α. State this and define power as "detection in the correct direction", or give two-sided power.

### M2. The power simulation is a reasonable plasmode, but it under-represents the noise in the real data, so it overstates power and does not "match" the analytic results

**Problem.**

**(i) The simulated datasets are less noisy than the real data.** Overdispersion is added as independent observation-level gamma noise, with NB2 method-of-moments α estimated from the null model: α = 0.0014 at UTLA (`outputs/power_simulation/power_utla_log.txt`). This does not reproduce the variance the clustered SE detects in the real data.

From `outputs/power_simulation/simulations_utla.csv`:

- the empirical SD of the estimated log IRR per 10% under the null is **0.0173**;
- the median implied SE is **0.0180**;
- the cluster-robust SE for the same model fitted to the real data is **0.0241** (`outputs/mde/mde_table_annual.csv`).

So the simulated data carry about half the sampling variance of the real data. The analytic power for a direct IRR of 1.05 per 10% using the real SE is Φ(ln 1.05/0.0241 − 1.96) ≈ **53%**, against a simulated **74.5%**. For IRR 1.02 it is about 13% analytic against 17% simulated.

The missing variance is almost certainly within-area serial correlation and area-specific trends (unmodelled time-varying confounding), which the simulation does not generate. The good type I error (4.5%) shows only that the clustered SE is calibrated *under independent noise*, not under the real error structure.

**(ii) The simulation is partly circular.** The effect is generated through exactly the exposure metric analysed: the same three-year lagged mean, no misclassification, no timing misspecification. It therefore mainly checks the Wald SE. It adds little about the realistic failure modes that make detection harder, such as mis-timed windows, items not proportional to users, and confounding by trends.

**(iii) Monte Carlo precision.** With 200 replicates, the Monte Carlo SE is about 1.5 percentage points at 4.5% and about 3.5 points at 50%. Power of "3.0%" and "4.5%" cannot be distinguished, and "equal to the false-positive rate" is not a valid comparison anyway. The 3.0% counts only significant estimates in the correct direction; significance in either direction for RR 4.9 was 5.5% in the same file.

**(iv) Level mismatch.** The simulation is at UTLA, while Table 2 and the abstract's main MDE are LTLA. `outputs/power_simulation/power_ltla_log.txt` contains only a header line and a multiprocessing warning, so the LTLA run appears not to have completed.

**Requests.**

- (a) Generate residual noise that reproduces the real data. Options: area-specific random slopes or AR(1) area-by-year random effects, calibrated so that the null-scenario empirical SD matches the real cluster-robust SE; or block-bootstrap real Pearson residuals by area.
- (b) Add scenarios where the true effect acts through concurrent-year exposure while the analysis uses the lagged window, and where the effect acts through dose (mg) while the analysis uses items.
- (c) Use at least 1,000 replicates for the null and key scenarios, and report Monte Carlo SEs.
- (d) Report two-sided rejection rates and correct-direction power separately.
- (e) Complete the LTLA simulation or remove the implied comparison.
- (f) Change "Results matched the analytic calculations" to an accurate statement.

### M3. The hospital positive control is "too easy", and it actually reveals heavy attenuation

**Problem.**

1. **It is reverse causation by design.** Antituberculosis drugs are a consequence of TB, and the PAF of TB for antituberculosis drug use is close to 100%. A same-year association and a lead (t+1) association are exactly what one expects: treatment lasts about 6 months or more, so cases notified late in year t are treated in t+1. A null lag (t−1) is also expected. The control shows that trust-level treatment volume can be placed in roughly the right areas. It does not show that the design can detect a *prior* exposure diluted through a small exposed fraction, which is the inference the paper needs. Calling the t−1 window "the causally ordered exposure" is right for the candidate drugs but inverted for the positive control. Tables and text should make that explicit.
2. **The within-area elasticity is about 0.2, not about 1.** If treatment volume scaled one-to-one with cases, the within-area IRR per 10% would be about 1.10. The observed same-year IRR is 1.019 (`outputs/hospital/hospital_results_utla.csv`), an elasticity of ln 1.019/ln 1.1 ≈ 0.20. That implies roughly 80% attenuation from:
   - catchment apportionment error (a 2024 catchment applied to all years; admissions-based shares applied to TB services, which are often centralised);
   - treatment of latent infection (rifampicin-containing regimens; the migrant LTBI programme);
   - differences between the timing of notification and treatment;
   - DDD conventions;
   - homecare and outsourcing.

   This is arguably the most informative number in the positive-control analysis. If a signal with PAF about 100% is attenuated about five-fold, the expected within-area effects of hospital drugs should be attenuated similarly. That makes the gap to the MDE even larger, and it undermines "linked validly".
3. **The pre-specified positive control failed.** Primary care antituberculosis prescribing failed in every design: LTLA 1.002 (0.998–1.006); cross-sectional adjusted 0.89 (0.79–1.00), in the *inverse* direction (`outputs/nb_results_wide.csv`). The hospital control was introduced afterwards (`PROGRESS.md`, "Improving the data and design"). This should be stated plainly.

**Requests.**

- (a) Reframe the hospital control as validating the *spatial placement* of hospital drug volume, not the linkage's ability to detect exposure effects.
- (b) Report and discuss the elasticity (about 0.2), and propagate an attenuation factor into the expected-effect calculations for hospital drugs, at least as a sensitivity analysis.
- (c) Consider a harder positive control with prior exposure and partial PAF. Options:
  - a plasmode that injects a synthetic lagged effect of a known small PAF into real TB counts, using the *apportioned* hospital exposure;
  - an external exposure–outcome pair with a known moderate population effect, such as antiretroviral volume against diagnosed HIV prevalence (both available) for the SCMD linkage, or metformin items against QOF diabetes prevalence for primary care.
- (d) Tone down "linked validly" in the abstract, discussion and conclusion.

### M4. Hospital within-area SEs are likely too small because apportioned exposures are correlated across areas

**Problem.** Every local authority's hospital exposure is a weighted sum of the same trust-level quantities, with time-invariant weights (2024 catchments). Within-area changes in exposure are therefore shared by all areas served by a trust. Clustering by local authority treats those areas as independent, but the effective number of independent exposure trajectories is the number of trusts, and fewer where trusts co-vary.

The near-identical UTLA and LTLA point estimates support this: anti-TNF lag 0.993 against 0.991; JAK inhibitors 0.995 against 0.995 (`hospital_mde.csv`). They are consistent with trust-level variation merely being copied into more units. The "precise" hospital MDEs (0.9–2.1%) may therefore be optimistic.

**Requests.**

- (a) Re-estimate with multiway clustering (local authority and dominant trust), or cluster at ICB or region level with appropriate small-sample corrections.
- (b) Alternatively, run the analysis at trust level, apportioning TB counts to trust catchments (the reverse mapping). This is the natural unit of exposure measurement.
- (c) Report how many distinct trusts contribute to each area and the share of the dominant trust.

### M5. Spatial diagnostics are nearly uninformative by construction

**Problem.** `spatial_autocorrelation.py` computes Moran's I of *area-mean* Pearson residuals from a model with area fixed effects. In Poisson maximum likelihood with area dummies, the raw residuals sum to exactly zero within each area (first-order conditions), so area-mean residuals are close to zero by construction. The reported residual Moran's I (0.04 and −0.01) therefore says little about spatial dependence in the within-area variation, which is what drives the standard errors. The statement "area fixed effects remove the spatial structure, so no spatial correction is needed" (`revision_notes.md`) does not follow.

**Requests.**

- (a) Test spatial and cross-sectional dependence of the year-specific residuals, for example Moran's I per year or a Pesaran CD test.
- (b) If dependence is present, report Conley (spatial HAC) SEs or cluster at a coarser geography.
- (c) Revise the Results and Strengths text accordingly.

### M6. The fixed-effects Poisson specification: windows, identification and robustness

**Problem and requests.**

1. **Estimator.** PPML with area and year fixed effects, a log-population offset and area-clustered SEs is appropriate for these counts, and the incidental-parameter problem does not bias Poisson fixed-effects slopes. Clustering handles serial correlation induced by overlapping three-year exposure windows, and with 149 and 292 clusters the cluster-robust SEs are reasonable. However, overlapping moving-average exposures leave very little independent within-area variation over 8 outcome years. Please report the within-area SD of the *three-year-mean* exposure in the estimation sample for each drug, not only the annual-rate SD.
2. **Area-specific trends.** Identification comes from area-specific deviations from national year effects. Smooth area-specific trends in prescribing and TB (demographic change, migration composition) will drive estimates. Please add area-specific linear trends as a sensitivity analysis. It will probably widen intervals further, which supports the paper's thesis.
3. **Shared-denominator bias.** The exposure rate (items/population) and the outcome offset share the ONS population estimate. Within-area errors in the population estimate (for example around Census 2021 rebasing) bias the exposure coefficient *upwards* by about var(e)/var(x). With a within-area SD of log exposure of 0.07 or less, a denominator error SD of 0.01–0.02 gives an elasticity bias of about 0.02–0.08, that is, IRR per 10% of about 1.002–1.008. That is the same order as the expected effects. Please add a sensitivity analysis with log population as a free covariate instead of an offset, and with exposure expressed per registered patient.
4. **Exposure window.** Given M1(3), a concurrent or t−1 exposure is more causally apt for oral corticosteroids than t−3 to t−1. The concurrent and t−1 windows are in the output files. Report them in a supplementary table, with MDEs, and justify the primary choice.
5. **Zero handling.** Primary care uses a log floor of half the minimum positive value (`log_rate`). The hospital models drop area-years with zero exposure (`d = d[d[f"rate_{g}"] > 0]`, `hospital_medicines.py`). Harmonise the approaches or justify the difference, and report how many observations are dropped. This matters for JAK inhibitors early in the series.
6. **Deviation from the original design.** The pre-specified panel design (`PROGRESS.md`, "Panel design (pre-specified before results)") used Fingertips three-year rolling outcomes with an exposure window of t−5 to t−3. The manuscript's primary model (annual UKHSA outcome, t−3 to t−1) replaced it after those results were seen. That is a reasonable improvement, but it is a deviation and should be reported, with the original design's results given as a sensitivity analysis.

### M7. Choice of covariates: bad-control and mediator risks

**Problem.**

- **Diabetes prevalence (QOF)** is adjusted in every model, including metformin and insulin. Within areas, QOF prevalence changes largely through case-finding and coding, which directly drive metformin and insulin prescribing. Conditioning on it changes the estimand to "prescribing intensity given recorded diabetes", absorbs much of the exposure variation (inflating the SE) and can induce collider-type bias. Diabetes is also itself a TB risk factor. For metformin that makes it a confounder, but only if the question is the drug's protective effect among people with diabetes, and an ecological design cannot isolate that.
- **In-migration.** Adjusting for in-migration in both the exposure window and the outcome year is defensible, since migration affects both prescribing (new registrants, age mix) and TB. But migration-driven change in *who is exposed* is part of the exposure. Please discuss.
- **Total prescribing volume.** The authors rightly identify it as a bad control.
- **The key time-varying confounder is missing:** the non-UK-born population share. It is modelled only through the 2021 Census cross-sectionally, which the fixed effects absorb. Annual local authority estimates by country of birth from the Annual Population Survey (ONS, "Population of the UK by country of birth and nationality") exist for much of the period and should be tried, with appropriate caveats about sampling error.

**Requests.**

- (a) Present metformin and insulin models with and without diabetes prevalence.
- (b) Present a directed acyclic graph (DAG) showing the assumed roles of age, migration, HIV, diabetes and deprivation.
- (c) Try APS-based time-varying non-UK-born share as a covariate.
- (d) Report the FE-only and adjusted estimates side by side in the main table, since both are in the outputs.

### M8. Pre-specification and multiple testing

**Problem.** The Strengths section says "the exposures, controls and falsification tests were specified in advance".

- There is no registered or time-stamped protocol.
- The project log shows the design being built iteratively within a day. The first-pass cross-sectional results preceded the panel design.
- The hospital analyses, LTLA panel, UK-born-by-age analyses, simulation, spatial diagnostics and asylum covariate were all added "in response to 'find more/better data and do better'" (`revision_notes.md`) after the primary results were null.
- The drug groups may have been fixed early, but analytic choices (windows, outcome source, geography, covariates) were not.

On multiple testing, Benjamini–Hochberg FDR is applied only to 12 drugs in one model per level. It is not applied to:

- the hospital analyses (JAK inhibitor same-year 0.990 (0.984–0.996) is nominally significant);
- the lead tests;
- the sensitivity models;
- the 117 regional models.

The positive and negative controls should not be in the FDR family, because they test different hypotheses.

**Requests.**

- (a) Replace "specified in advance" with an accurate account: drug groups and the core panel design specified before panel results; hospital, LTLA, UK-born-by-age and simulation analyses added afterwards.
- (b) Label post hoc analyses as exploratory.
- (c) Remove the controls from the FDR family.
- (d) Apply a declared correction (or at least report the number of tests) to the hospital and falsification families.
- (e) Given that almost everything is null, multiplicity mainly matters for the few "signals". The paper's best argument against those is plausibility (see M9), which should carry more of the weight than Holm-adjusted p-values over a post hoc family of six.

### M9. The falsification (lead) test logic and the regional analyses with 9 clusters

**Problem.**

1. **Lead tests are compared by significance, not by estimate.** A lead estimate that is "not significant" does not show absence of trend confounding when its CI is wide. For UK-born TB and prednisolone mg, the lead estimates were 1.18 (0.85–1.63), 0.96 (0.73–1.25) and 0.95 (0.86–1.04), with CIs compatible with sizeable confounding. Conversely, one or two significant leads among many tests do not prove confounding. Lag and lead coefficients should be estimated *jointly* in one model, and their *difference* tested.
2. **Different samples.** In the UTLA panel, the lead windows use outcome years 2013–2021 and the primary windows 2017–2024 (`outputs/panel_annual/panel_annual_log.txt`). Differences may reflect period, not confounding. Restrict to a common sample (the 2011 extension will help).
3. **Nine clusters.** CR1 SEs with t(8) critical values can still be anti-conservative with 9 heterogeneous clusters, and the leave-one-region-out ranges are descriptive only. Use a wild cluster bootstrap-t (Webb weights) or randomisation inference (permuting regions' exposure trajectories), and consider region-specific linear trends.
4. **Denominators.** UK-born denominators come from the Labour Force Survey and carry sampling error. The 65+ model uses *all* residents aged 65+ (`steroid_ukborn_regional.py`), so changes in the non-UK-born share among older people enter the offset.
5. **Plausibility is the strongest argument and should lead.** An IRR of 1.37 per 10% exceeds the logical maximum of 1.10 under the authors' model, which is attainable only if all TB were attributable to the drug. That settles the prednisolone signal more convincingly than Holm p-values over a post hoc family. For the UK-born 65+ group, calculate the expected effect with age-specific steroid prevalence (see M1c) and compare it with the regional MDE, which from a 95% CI of 0.74–2.42 is enormous.
6. **The "7 of 90 against 4.5 expected" statement.** It pools lagged, lead and 2020–21-exclusion models that are not independent. It also counts lead-test failures as "chance" hits even though the paper elsewhere interprets them as confounding, and it omits the 27 models for UK-born 65+ (3 more significant: 10 of 117). Delete it or replace it with a coherent summary.

**Requests.** Items 1–6 as above. Also report all 65+ lead results in the text: OCS lead 3, 1.45 (1.01–2.09), is significant but appears only in the revision notes.

### M10. Interpreting nulls: move from "no association" to "effects excluded" and equivalence

**Problem.** The manuscript mixes "null", "null and precise" and "cannot detect". A 95% CI of 0.944–1.021 (LTLA oral corticosteroids) is compatible with a 2% *increase* per 10%, which is about six times the expected effect. The data cannot show equivalence at the scale of plausible effects, and that is the paper's point, but it should be quantified.

**Requests.**

- (a) For each drug, report the largest effect excluded by the upper 95% (or 90%) confidence limit, and translate it into the maximum compatible PAF. For example, the LTLA oral corticosteroid 90% upper limit is about 1.015 per 10%, which excludes a PAF above about 15%.
- (b) Where a bound can be justified, report two one-sided tests (TOST). A bound of ±5% per 10% (PAF about 50%) would be declared "equivalent"; a bound near the expected effect (±0.5%) cannot be. Being explicit about this is informative in itself.
- (c) Avoid "precise" for hospital estimates until M4 is addressed.

### M11. Ecological bias and scope of the conclusions

**Problem.** Fixed effects remove time-invariant area confounding, but cross-level bias remains when drug effects or baseline risk vary within areas in ways correlated with exposure change (M1(2)). The conclusions also generalise beyond what was tested.

- "Cannot detect plausible population-level effects of medicines on TB in England" is supported for these 12 primary care groups and 6 hospital groups with these designs.
- The abstract's "one to two orders of magnitude" sits uneasily with the ratios reported (5 to 283; systemic corticosteroids 6, anti-TNF RR 15 about 5).
- "Linked validly" is overstated (M3).
- The Discussion attributes every apparent signal to "confounding or chance". The data are compatible with that, but also with measurement error.

**Requests.**

- (a) Reword the conclusion: "ecological analyses of these data could not detect, and are not powered to detect, the population effects implied by published individual-level relative risks."
- (b) Reconcile "one to two orders of magnitude" with the reported ranges (say "about 5 to more than 100 times").
- (c) Discuss how cross-level bias and exposure misalignment (timing, items against users, apportionment) all push in the direction of further attenuation.

### M12. Result integrity: several reported estimates do not match current outputs (see Section 5)

The UTLA falsification column of Table 1 and the vitamin D statement in Results do not match `outputs/panel_annual/panel_annual_results.csv`. The difference changes a statistical conclusion (vitamin D). Several LTLA hospital findings are also unreported. Please regenerate all tables from code (ideally programmatically, from the results CSVs) after the 2011 extension, and state which level each number refers to.

---

## 4. Minor comments

1. **Cross-sectional exposure timing and denominators.** Methods say "the cross-sectional analysis used June 2026"; `analyze.py` confirms June 2026 prescribing against TB in 2022–24. The exposure postdates the outcome. The denominators were registered-list populations (`PROGRESS.md`), which contradicts "Denominators were resident populations, which avoids list inflation". Clarify both, and state the temporal inversion as a limitation.
2. **Table 1 scales.** Table 1 mixes per-SD (cross-sectional) and per-10% (panel) effects in adjacent columns. Separate them or add a clear column-group header. Say whether the falsification column is UTLA or LTLA: Figure 2 shows LTLA leads, Table 1 claims UTLA.
3. **Table 2 labels.**
   - "PAF" is negative for statins and metformin; call it "prevented fraction" or "PAF/PF".
   - "Power" is one-sided correct-direction power (see M1f).
   - Give the SE, or the 95% CI the MDE was derived from.
4. **Harmonise geographic levels.** Table 2 (LTLA), Table 3 (UTLA), the simulation (UTLA) and the abstract (both) use different levels. Present both levels in supplementary tables.
5. **Unreported LTLA hospital results** (`outputs/hospital/hospital_results_ltla.csv`) should be reported:
   - concurrent anti-TNF, 0.989 (0.980–0.997), nominally significant and inverse;
   - adjusted cross-sectional JAK inhibitors, 0.946 (0.908–0.984);
   - calcineurin inhibitors/antiproliferatives cross-sectional at LTLA, 1.006 (0.963–1.051), null. This bears on the transplant-centre explanation offered for the UTLA association.
6. **Hospital quantity units.** "Approximate milligrams" summed across products of very different potency (hydrocortisone and dexamethasone differ about 25-fold; the anti-TNF agents differ in dose) makes group totals sensitive to product mix, for example COVID-era dexamethasone in 2020–21. Use prednisolone-equivalent mg and DDDs, or show that the product mix is stable. Reference 35 (RECOVERY) is listed but not cited in the text; cite it here if this is its purpose.
7. **Rifampicin DDD includes LTBI treatment.** Quantify or discuss (see M3).
8. **Abstract wording.**
   - "An individual RR above 100 was needed for even 57% power" is garbled; RR 100 gave 56.5%.
   - "3.0%, equal to the false-positive rate" is wrong (type I error 4.5%; see M2(iii)).
9. **Reference order.** References are not numbered in order of first citation ([32] is cited before [9]; [30,40] are cited early). Reference titles marked "abbreviated" must be completed.
10. **Record-level reporting (RECORD/STROBE).** Provide:
    - code lists (BNF chemical substances per group; `data/processed/drug_group_substances.csv` should be a supplementary file);
    - SCMD product lists and conversion factors;
    - linkage rates by year;
    - a flow of areas: 149 of 151 UTLAs, 292 of about 296 LTLAs, 105 of 106 Sub-ICBs, 138 UTLAs in the long-difference analysis (with the ≥10-case restriction), with reasons for exclusion;
    - handling of suppressed counts and boundary merges (City of London, Isles of Scilly);
    - software versions.
11. **Two different linkage figures.** Methods say 98.6% of items came from RO76 practices, and Strengths says "98% of items linked to an area" (logs: 98.1% UTLA; 98.38% of OCS items to region). These are different quantities; label each clearly.
12. **Notification counts.** The Introduction's 4,125 (2020) and 5,480 (2024) differ from `outputs/descriptives/england_tb_annual.csv` (4,123 and 5,490). Use one source, or note that the report and Fingertips differ.
13. **Missing figures.**
    - A figure of within-area exposure variation (distribution of demeaned three-year exposures) would help readers see why power is low.
    - Figure 4 shows OCS items, but the regional "signal" was prednisolone mg; show mg too.
14. **Hospital cross-sectional model.** State the covariates, the period and the exposure scale (per SD of the *log* rate) in the Table 3 legend or the text.
15. **Long-difference analysis.** Describe the windows (OCS 2014–16 → 2019–21; TB 2014–16 → 2022–24), the case-count restriction (≥10) and the weighting in Methods.
16. **Missing data.** State how missing covariate years (HIV, QOF) were handled, and how many area-years each model loses.
17. **COVID years.** Consider an indicator for area-level COVID disruption, or at least discuss the heterogeneity in 2020–21 that year fixed effects do not absorb.
18. **Terminology.** Use "negative control exposure" and "falsification test" consistently. "Lead exposure" can be misread as the metal; "future-exposure test" is clearer.
19. **"Data checks" wording.** "The BNF- and SNOMED-coded releases gave identical national totals for June 2024" is a consistency check of one month. Say so, or extend it to a sample of months.

---

## 5. Verification of reported numbers against output files

### 5a. Numbers that match

| Manuscript value | Output file | Output value |
|---|---|---|
| LTLA OCS IRR 0.982 (0.944–1.021), 2,335 area-years | `outputs/panel_annual_ltla/panel_annual_ltla_log.txt` | 0.982 (0.944–1.021); 2,335 area-years, 292 areas |
| UTLA OCS 0.986 (0.940–1.034) | `outputs/panel_annual/panel_annual_log.txt` | 0.986 (0.940–1.034) |
| All q ≥ 0.65 | `panel_annual_ltla_results.csv` | minimum q_fdr = 0.650 (LTLA); UTLA minimum 0.709 |
| Table 2 OCS: expected 0.34%, MDE 5.8%, ratio 17, power 3.7%, RR 153 | `outputs/mde/mde_table_ltla.csv` | 0.339; 5.779; 16.6; 0.0366; 153.1 |
| Table 2, other rows (ICS 54×/69; immunosuppressants 283×/81; PPI 20×/28; statins 15×; metformin 31×) | `mde_table_ltla.csv` | 54.2/68.8; 283.1/81.4; 20.1/28.5; 14.5; 30.6 |
| Hospital positive control: same year 1.019 (1.005–1.034); next year 1.017 (1.003–1.032); previous year 0.999 (0.989–1.009); ρ = 0.74; per SD 1.71 and 1.14 | `outputs/hospital/hospital_utla_log.txt` | identical; ρ = 0.743; 1.708 (1.442–2.023); 1.136 (1.035–1.247) |
| Table 3 lag estimates and MDEs (1.5, 1.5, 1.7, 0.9, 2.1, 1.4%) | `outputs/hospital/hospital_mde.csv` | 1.451, 1.465, 1.746, 0.909, 2.070, 1.392 |
| Ratios "5–87" | `hospital_mde.csv` | 5.35–86.7 |
| Moran's I 0.49/0.42 (p = 0.001); residuals 0.04 (p = 0.38) and −0.01 (p = 0.70) | `outputs/spatial/morans_i.csv` | 0.490, 0.415; 0.044 (0.383), −0.014 (0.695) |
| Simulation: 4.5%, 3.0%, 11%, 57%, 75%, 100% | `outputs/power_simulation/power_summary_utla.csv` | 0.045, 0.030, 0.110, 0.565, 0.745, 1.000 |
| UK-born prednisolone mg lag 2 1.37 (1.08–1.73), lag 3 1.38 (1.04–1.83); Holm p 0.09 and 0.16 | `outputs/steroids/ocs_tb_by_birthplace_regional.csv` | 1.368 (1.082–1.731), p = 0.0151; 1.378 (1.035–1.833), p = 0.0322. Holm over 6 tests: 0.090 and 0.161 (recomputed) |
| Non-UK-born lead 3 1.36 (1.03–1.80); 65+ lag 1 1.34 (0.74–2.42); 65+ lead 2 1.59 (1.04–2.43); levothyroxine lead 1 1.33 (1.05–1.69) | same file | 1.363 (1.030–1.803); 1.338 (0.739–2.423); 1.593 (1.044–2.428); 1.333 (1.049–1.694) |
| "7 of 90 nominally significant" | same file (UK-born + non-UK-born adjusted models) | 7 of 90 (but 10 of 117 including the 65+ models; see M9(6)) |
| Notifications: 11,876 UK-born; 36,633 non-UK-born; 2,401 UK-born 65+ | `data/processed/region_tb_birthplace_annual.csv`, `region_tb_birthplace_age_annual.csv` (2015–2024) | 11,876; 36,633; 2,401 |
| Regional adjusted lag 1 0.997 (0.788–1.260); long differences 1.000 (0.934–1.072), 138 UTLAs | `outputs/steroids/steroid_trends_log.txt`, `utla_long_difference_summary.csv` | 0.997 (0.788–1.260); 1.0004 (0.9337–1.0718), n = 138 |
| Trends: PPI +35%, statins +31%, vitamin D +42%, OCS −10%, fluoroquinolones −51%; within/between SD 0.07/0.31 | `outputs/descriptives/national_prescribing_2014_2024.csv` | +34.98, +31.23, +41.53, −9.83, −51.37; 0.071/0.306 |
| OCS items 141.5 → 127.7; prednisolone mg −21.2% | `outputs/steroids/national_annual_ocs_per_1000.csv`, `steroid_trends_log.txt` | 141.51 → 127.74; −21.2% |
| Hospital trends: anti-TNF +64%, JAK about 13-fold, systemic corticosteroids +15% | `hospital_utla_log.txt` (mean rates) | 3,589 → 5,902 (+64%); 408 → 5,364 (13.1×); 12,290 → 14,124 (+15%) |
| TB incidence 11.9 (2014), 7.3 (2020), 9.4 (2024) | `outputs/descriptives/england_tb_annual.csv` | 11.91, 7.32, 9.37 |
| Cross-sectional: non-UK-born IRR per SD 1.40; aged 65+ 0.67; Table 1 cross-sectional columns | `outputs/analysis_log.txt`, `outputs/nb_results_wide.csv` | 1.398, 0.673; all Table 1 cross-sectional entries match |

### 5b. Discrepancies

**D1. Table 1 "UTLA falsification (next 3 years)" column and the Results text on vitamin D do not match the current output.**

In `outputs/panel_annual/panel_annual_results.csv` (exposure window "lead (falsification): t+1..t+3", model "FE + time-varying"), 7 of 12 rows differ:

| Drug group | Manuscript | Output file |
|---|---|---|
| Vitamin D | 1.026 (1.001–1.052), described as an association | **1.025 (0.999–1.051), p = 0.056** |
| Oral corticosteroids | 1.003 (0.955–1.054) | 1.003 (0.954–1.053) |
| Immunosuppressants | 1.006 (0.977–1.035) | 1.005 (0.976–1.035) |
| PPIs | 1.046 (0.993–1.102) | 1.044 (0.991–1.100) |
| Statins | 1.033 (0.983–1.086) | 1.034 (0.984–1.087) |
| Insulins | 0.951 (0.901–1.005) | 0.949 (0.899–1.002) |
| Fluoroquinolones | 0.997 (0.977–1.017) | 0.996 (0.976–1.016) |
| All antibacterials | 1.010 (0.973–1.048) | 1.009 (0.972–1.048) |

For vitamin D, the manuscript's "UTLA 1.026, 1.001–1.052" is statistically significant; the output is not. The corresponding *LTLA* lead estimate *is* significant: 1.028 (1.004–1.051), p = 0.019 (`panel_annual_ltla_results.csv`). The substantive point survives at LTLA, but the reported UTLA numbers appear to come from a stale run.

**D2. "Simulation: results matched the analytic calculations."**

- Real-data SE for OCS at UTLA: 0.0241 (`outputs/mde/mde_table_annual.csv`, `se_log_irr_10pct`).
- Simulated null empirical SD: 0.0173 (derived from `outputs/power_simulation/simulations_utla.csv`).
- Analytic power for a direct IRR of 1.05 per 10%: about 53%, against 74.5% simulated.
- The analytic UTLA "RR for 80% power" is 257 (`mde_table_annual.csv`), which is hard to reconcile with 56.5% simulated power at RR 100 unless the simulated noise is too small.

See M2.

**D3. "Power 3.0%, equal to the false-positive rate."**

- `power_summary_utla.csv` gives a type I error of 0.045 and correct-direction power of 0.030.
- The two-sided rejection rate for RR 4.9 in `simulations_utla.csv` is 0.055.

The two are not the same quantity and not equal.

**D4. Abstract: "An individual RR above 100 was needed for even 57% power."**

`power_summary_utla.csv` shows RR 100 gives 0.565. It is RR = 100, not "above 100", and the sentence should be rephrased.

**D5. Incomplete LTLA simulation.**

`outputs/power_simulation/power_ltla_log.txt` contains only "ltla: 2335 area-years, 292 areas; overdispersion alpha = 0.0009" and a semaphore-leak warning. No LTLA power summary exists, although Table 2 and the abstract lead with LTLA.

**D6. Selectively reported LTLA hospital results.**

`outputs/hospital/hospital_results_ltla.csv` / `hospital_ltla_log.txt` contain results the manuscript does not report:

- anti-TNF concurrent 0.989 (0.980–0.997), significant;
- JAK inhibitors cross-sectional adjusted 0.946 (0.908–0.984), significant;
- calcineurin inhibitors/antiproliferatives cross-sectional adjusted 1.006 (0.963–1.051), null at LTLA against 1.055 (1.001–1.112) at UTLA;
- positive control lead at LTLA 1.014 (1.000–1.028).

The manuscript reports only the LTLA same-year positive control.

**D7. Omitted significant 65+ lead estimate.**

`ocs_tb_by_birthplace_regional.csv` shows UK-born 65+ OCS lead 3 at 1.452 (1.007–2.093), p = 0.047. The manuscript reports only lead 2.

**D8. Notification counts (minor).**

The Introduction's 4,125 (2020) and 5,480 (2024) differ from `outputs/descriptives/england_tb_annual.csv` (4,123 and 5,490). This is probably a different source (report against Fingertips) and should be harmonised or footnoted.

---

*Reviewer 1*
