# Peer review, round 3: Reviewer 1 (epidemiology and biostatistics)

**Manuscript:** "Can open prescribing data detect medicine effects on tuberculosis? An ecological study of primary care and hospital prescribing and TB notifications in England" (Draft 4, revised after peer review round 2, 14 September 2026)

**Materials examined:** `paper/manuscript.md` (including Tables 1–3, S1–S9, S2b, S3b); `paper/reviews/response_round2.md`; my round 2 report. Outputs: `outputs/panel_annual_{ltla,utla}_residence/panel_results.csv`, `outputs/power_simulation/power_summary_*.csv` and `simulations_*.csv`, `outputs/mde/*.csv`, `outputs/hospital/hospital_results_*.csv` and `hospital_mde_*.csv`, `outputs/steroids/*.csv`, `outputs/spatial/*.csv`, `outputs/descriptives/within_between_variation.csv` and `splice_agreement_2013_2014.csv`. Code: `analyze_panel_annual.py`, `steroid_trends.py`, `make_tables.py`, `mde.py`.

No models were refitted. All checks below come from reading output files and code, plus arithmetic on reported values.

---

## 1. Recommendation

**Minor revision.** None of the remaining issues changes the conclusions, and none needs new analysis. Four text corrections must be made before acceptance (Section 3, items R1–R4).

This revision properly addresses the main statistical problems from round 2:
- **Simulation.** It is now read correctly, and analytic power at the real-data SE is shown beside simulated power.
- **Falsification.** A joint t−1/t/t+1 model is added, with Wald tests and the correlation between the estimates.
- **Regional inference.** Randomisation inference now uses the studentised statistic, and the regional MDEs are set against the expected effect.
- **Bounds.** The bound shifted by the negative control and the prevented fraction are reported.
- **Counts.** Counts of estimates and areas are generated from the output files.

Almost every number I checked matches the outputs. The exceptions are listed in Section 3.

---

## 2. Status of round 2 items

### Major items

| Item | Status | Verification / comment |
|---|---|---|
| N1 Simulation misinterpreted | **Addressed** | Median replicate SE, which I recomputed from `simulations_*.csv` as \|log IRR\|/z(p): LTLA 0.0161 against null SD 0.0166; UTLA 0.0167 against 0.0171. Both match Table S4. Null rejection is 7.8%/7.6%, correctly called mildly anti-conservative. I recomputed analytic power at the real SE: LTLA IRR 1.05 gives 64.6%; RR 100 gives 52.1%. Both match. "Conservative" and "agreed" are gone. Remaining point: R5. |
| N2 Joint lag/lead logic | **Partly** | (a) The t−1, t, t+1 model is added (Table S2b). (b) The Wald test and correlation are in the output (`p_first_minus_last`, `corr_first_last`), but the reported correlation range is wrong, and the interpretation no longer fits the new model (R2, R3). (c) The joint t−1 column is in Table 1. (d) The wording is more cautious. |
| N3 Framing | **Addressed** | (a) "Roughly 10 to several hundred times" replaces "one to two orders of magnitude". Table 2 gives 11–272 and Table S3 (unattenuated) 23–522. The attenuated ratios, up to 1,443, are labelled illustrative, which is acceptable. (b) "Compatible with residual confounding, chance or measurement error" is used in the Abstract, Discussion and Conclusion. The Results (lines 483, 500) are still firmer; see R4. (c) Heavy attenuation is now restricted to hospital medicines, and primary care linkage is described as untested. (d) The regional negative-control wording rests on levothyroxine lead 1 (randomisation p = 0.038), which is acceptable. |
| N4 Regional analyses | **Addressed** | (a) The regional MDEs and the 0.9% expected effect at age ≥65 are reported. Recomputing from the t(8) intervals in Table S5 (2.80 × SE) reproduces about 46–82% (UK-born) and up to about 100% (≥65). I checked 0.9%: [1 + 1.1 × 0.025 × 3.9] / [1 + 0.025 × 3.9] = 1.0089. See R6 on reproducibility. (b) `steroid_trends.py` lines 143–159 now permute the cluster-robust t statistic. (c) Exchangeability and the p-value formula are stated. "4 of 81, all lead terms" is verified from Table S5 (p = 0.012, 0.040, 0.044, 0.038). |
| N5 Largest compatible PAF | **Addressed** | The shifted bound for oral glucocorticoids is 1.005/0.962 → 44%, which matches `max_compatible_paf_nc_shifted_pct`. Prevented fractions are reported for metformin (38%) and statins (29%), and the text explains the difference from the minimum detectable PAF. Presentation point: R8. |
| N6 Text vs outputs | **Addressed** | 277 estimates with 30 nominally significant, and q ≥ 0.51 (LTLA) and ≥ 0.22 (UTLA): all verified. 294 LTLAs, 151 UTLAs and 3,233 area-years are harmonised. The inhaled corticosteroid sensitivity estimates are now qualified (line 490). |

### Earlier major items still open in round 2

| Item | Status | Comment |
|---|---|---|
| M1(a) Direction of assumption 1 | Addressed | Stated as unknown; assumption 2 added. |
| M1(b) Birthplace benchmark | Addressed | Relabelled "age-stratified". |
| M1(c) Recorded-case benchmark | Addressed | 0.043% and 0.087% verified (0.55% × 3.9/4.9 = 0.435% attributable share). |
| M1(d) Invariance to the 10% contrast | Addressed | Added to the Table 2 note. |
| M3(a) Elasticity CI | Addressed | UTLA 0.36 (0.10–0.62) and LTLA 0.40 (0.14–0.66) verified from `hospital_results_*.csv`. |
| M3(b) Timing | Addressed | See R7 for a residual inconsistency. |
| M3(c) Failed primary care positive control | Addressed | Methods chronology, lines 133–135. |
| M3(d) Harder positive control | Addressed | Given as a limitation. |
| M4 Dominant-trust shares | Not done | Acceptable. |
| M5 Spatial | Addressed | 2 of 11 LTLA years (2014: I = 0.163; 2023: I = 0.079) and UTLA 2014 only are verified. LTLA 2019 has p = 0.050 exactly, which is fine. |
| M6(a) Original design | Addressed | Table S8. |
| M6(b) Zero-exposure drops | Addressed | `n_dropped_zero_exposure` = 0 for every primary care row at both levels. |
| M7 Compositional exposure change | Addressed | Briefly, at line 703. |
| M8(a) Chronology | Addressed | |
| M8(b) Test counts | Partly | Panel (277) and regional (81) counts are given. There is still no count for the hospital family. |

### Round 2 minor items

| # | Status | Comment |
|---|---|---|
| 1 | Addressed | SE column and label added. |
| 2 | Addressed | Legend added. |
| 3 | Addressed | Long-difference methods added. |
| 4 | Addressed | Missing data and asylum years. |
| 5 | Addressed | RECOVERY cited. |
| 6 | Addressed | Table S9 and file. |
| **7** | **Not addressed** | Figure 4 is still placed before Figure 3, Table 3 before Table 2, and S2b/S3b after S7/S8. The response says "[pending check at assembly]". |
| 8 | Addressed | FDR family stated. |
| 9 | Partly | Results use 4,123 for 2020 (Fingertips), but the Introduction (line 54) still gives 4,125. |
| 10 | Addressed | In the legend; see R7. |
| 11 | Addressed | |
| 12 | Addressed | |

---

## 3. Issues in draft 4

### Must fix

**R1. The splice figures in the Limitations are out of date (line 734).** The text says oral glucocorticoids changed by "+3.3% at the splice against +0.6% and +1.0% either side", and all antibacterials by "−0.1% against −4.5% and −5.6%". The rerun output, `outputs/descriptives/splice_agreement_2013_2014.csv`, gives:
- oral glucocorticoids: 2012/13 +0.1%, 2013/14 +2.8%, 2014/15 +0.1%;
- all antibacterials: −5.0%, −0.6%, −6.4%.

The response letter quotes the corrected oral glucocorticoid figures, but the manuscript kept the old paragraph (it is carried over verbatim from `paper/discussion_v3.md`). The pattern is unchanged, but the numbers must match the output. Other sentences taken from the v3 drafts should be checked the same way.

**R2. The lag/lead correlation range is wrong, and "strongly negatively correlated" is too broad** (Results line 497; Methods line 322; Table 1 legend; Discussion line 702; response letter).
- The text says the two-year-model correlations were "−0.16 to −0.83 across groups". In `panel_results.csv` (LTLA, model "lag and lead (t-1, t+1)") they run from **−0.83 to +0.08**:
  - levothyroxine −0.83, metformin −0.77;
  - oral glucocorticoids −0.38, inhaled corticosteroids −0.46, all antibacterials −0.16;
  - antituberculosis −0.02, oral dexamethasone +0.08.
- For the two groups the text relies on most (oral glucocorticoids and inhaled corticosteroids), the correlation is moderate, not strong.
- In the three-year model (Table S2b), the t−1/t+1 correlations are −0.23 to +0.17.

Please report the correct range and drop "strongly" as a general statement.

**R3. The collinearity caveat does not explain the persistent inverse lead terms; reinterpret them.** My round 2 point N2 was that seesaw estimates can arise from collinearity. The new model largely answers that concern, but the manuscript has not updated its reading of the evidence:
- With year t included, the t−1 and t+1 estimates are nearly uncorrelated. Yet the t+1 terms remain clearly inverse:
  - oral glucocorticoids 0.943 (0.898–0.990);
  - inhaled corticosteroids 0.861 (0.809–0.917);
  - proton pump inhibitors 0.910 (0.835–0.991);
  - insulins 0.888 (0.829–0.950).
- Chance sign reversal from collinearity cannot account for these. They are stronger evidence of residual confounding by area-specific trends, or some reverse pathway, than lines 497 and 702 imply.
- The *same-year* sign also depends on the specification:
  - inhaled corticosteroids: 0.922 (0.874–0.973) without t+1 (Table S2), 1.043 with t+1 (Table S2b);
  - proton pump inhibitors: 1.002 against 1.128.

  So the statement that positive same-year terms are "the direction expected from prescribing for undiagnosed TB" (line 498; Discussion line 702) is not robust.

Suggested wording: "In the three-year model the lag and lead estimates were almost uncorrelated, yet following-year terms stayed inverse for several groups. This is not explained by collinearity and is compatible with shared area-specific trends. Same-year estimates changed sign between specifications and are not interpreted."

**R4. The multiplicity statement (line 500) uses an invalid reference rate and overstates.**
- **Verified:** "30 of 277 … more than the 5% expected by chance", with 8 hits for inhaled corticosteroids, 6 for levothyroxine and 5 for metformin.
- **Invalid comparison:** the 277 estimates are not independent tests. They are 13 overlapping specifications of the same drug on largely the same data. A binomial 5% benchmark therefore does not apply.
- **Anti-conservative p-values:** the authors' own simulation shows the clustered Wald test rejects in 7.8% of null replicates.
- **Stronger than the Abstract:** "a pattern that points to shared trends rather than drug effects" goes further than the wording in the Abstract and Discussion.

Recommended changes:
- Drop the comparison with 5%.
- Say the hits are clustered within a few drugs and repeated across correlated specifications.
- Use the "compatible with" wording.
- Soften line 483 ("This suggests residual confounding by trends") in the same way.

### Should fix (minor)

**R5. The simulation mechanism is stated as established** (lines 618 and 681; Table S4 note: "because permuting exposure trajectories … breaks their alignment"). No analysis tests this. It is plausible: the cluster-robust meat term Σᵢ(Σₜ x̃ᵢₜ eᵢₜ)² is inflated when within-area exposure and residual trajectories co-vary differently across areas, and permutation removes that. Write "probably because". Also note that this heterogeneity is part of the real uncertainty, which is why analytic power at the real SE is the relevant figure. The response letter still quotes the superseded SEs (0.0154 vs 0.0158).

**R6. The regional MDEs are not reproducible from the repository.** "45–82%" and "46–99%" (line 642) and the 0.9% expected effect do not appear in any output file or script I could find. Please:
- write them to `outputs/steroids/` or add a column to Table S5;
- state the multiplier. With a t(8) reference, 2.80 understates the MDE; t₀.₉₇₅,₈ + t₀.₈₀,₈ ≈ 3.2. This strengthens the argument rather than weakening it.

**R7. The positive-control timing and apportionment inference.**
- **Timing.** Line 538 says timing contributes to the elasticity, because treatment of people notified late in a year continues into the next. If so, following-year pyrazinamide should be associated with notifications. Instead the lead estimates are null: alone 1.002 (0.992–1.013) and jointly 0.997 (0.986–1.007) at UTLA. The data therefore suggest timing is a small component. Say so.
- **Apportionment.** Line 539 infers from the equal rifamycin/isoniazid elasticity that "attenuation is dominated by apportionment". The comparison shows only that drug specificity adds little. It cannot separate apportionment from dose per person. Write "suggests drug specificity is not the limiting factor".

**R8. The Table 1 bounds column.** Methods (line 344) restrict the prevented fraction to drugs expected to protect, but Table 1 shows it for every drug. For example, "5% / 39% (44%)" for oral glucocorticoids is easy to misread. Either blank the prevented fraction for drugs hypothesised to be harmful, or say in the legend that it is shown for completeness.

**R9. The Abstract's primary care statement.** "No drug group was associated with notifications in the following year" should add "after correction for multiple testing", as line 432 does. Metformin (p = 0.04) and the negative control (p = 0.01) were nominally associated.

**R10. Small inconsistencies.**
- **Hospital ranges.** "MDEs exceeded expected effects by 26 to 520 times" (line 613) is the UTLA area-clustered range; across both levels Table S3 gives 23–522. "1.0–2.9%" mixes the LTLA minimum (0.97) with the trust-clustered UTLA maximum (2.85). Give the range across Table S3, or name the level and SE type.
- **2020 count.** Introduction 4,125 against Results 4,123 (minor item 9).
- **Hospital test count.** Give the number of tests in the hospital family (M8b).
- **Ordering.** Renumber figures and tables in order of first citation (minor item 7).

**R11. The response letter** contains unrendered placeholders ("{{n_sig_ltla}} of {{n_est_ltla}}", "[pending check at assembly]"). Fix these before the letter goes to the editor.

---

## 4. Do the remaining issues block publication?

No. R1–R4 are text corrections: one set of stale numbers, one misreported range, and two interpretive statements that need to match the evidence. Each takes a sentence or two and needs no refitting. R3 and R4, if anything, strengthen the paper's central argument that residual trend confounding is present and that the designs cannot detect plausible effects. The core quantitative results (Tables 1, 2, 3, S1–S6, S2b, S3b) match the outputs.

---

## 5. Verification summary

| Manuscript | Output | Result |
|---|---|---|
| Table 1 / line 433: oral glucocorticoids 0.969 (0.929–1.012); 3,233 area-years; 294 areas | LTLA `panel_results.csv` | Match |
| q ≥ 0.51 (LTLA), ≥ 0.22 (UTLA); metformin p = 0.04, levothyroxine p = 0.01 | same | 0.509, 0.224; 0.039, 0.014 |
| 277 estimates, 30 p < 0.05; inhaled corticosteroids 8, levothyroxine 6, metformin 5 | same | Match |
| Two-year lag/lead correlation "−0.16 to −0.83" | `corr_first_last` | **−0.83 to +0.08** (R2) |
| Table S2b correlations −0.23 to 0.17; t+1 estimates | same | Match |
| Table S4: all rates; median replicate SE 0.0161/0.0167; null SD 0.0166/0.0171; analytic power | `power_summary_*.csv`; recomputed from `simulations_*.csv` | Match |
| Table 2: MDE 6.3%, ratio 18, minimum detectable PAF 63%, RR 190; ratios 11–272 | `mde_table_ltla_residence.csv` | Match |
| Benchmarks 0.043/0.087/0.078/0.157/0.293/0.339% | `expected_effect_benchmarks.csv` | Match |
| Largest compatible PAF 5%, shifted 44%; metformin prevented fraction 38% | `max_compatible_*` columns | Match |
| Positive control ρ 0.81; 1.035 (1.009–1.061); elasticity 0.36 (0.10–0.62), LTLA 0.40 (0.14–0.66); rifamycin/isoniazid 0.37 (0.22–0.51) | `hospital_results_*.csv` | Match |
| Hospital glucocorticoids 1.024 (1.001–1.046); trust-clustered 0.999–1.049; excluding 2020–21 1.018 (0.969–1.069) | Table 3, S3b, `hospital_results_utla.csv` | Match |
| Table S3 ratios; "26–520" | `hospital_mde_*.csv` | Table matches; text range is UTLA only (R10) |
| Within-area SD 0.042/0.29; PPIs 0.036; DMARDs 0.088; mg 0.041; ±9% | `within_between_variation.csv` | Match |
| Splice: oral glucocorticoids +3.3% (+0.6%, +1.0%); antibacterials −0.1% (−4.5%, −5.6%) | `splice_agreement_2013_2014.csv` | **+2.8% (+0.1%, +0.1%); −0.6% (−5.0%, −6.4%)** (R1) |
| Moran's I: LTLA median 0.026 (−0.004 to 0.163), 2 of 11; UTLA 0.009, 2014 I = 0.209 | `morans_i_*.csv` | Match |
| Regional: items lag 1 1.034, p = 0.80; mg 1.094, p = 0.57; national r = 0.33; lag-3 change r = −0.75 | `ocs_tb_change_correlations.csv` | Match |
| Table S6; UK-born mg joint 1.45/0.88, p = 0.035, randomisation 0.232; excluding London 1.12, p = 0.73 | `ocs_tb_by_birthplace_lag_lead.csv` | Match |
| Long difference: 140 UTLAs, ρ −0.19, 0.983 (0.917–1.054) | `utla_long_difference_summary.csv` | Match |
| Regional MDEs 45–82% / 46–99%; expected 0.9% | No output file | Reproduced approximately by hand (R6) |

*Reviewer 1*
