# Peer review, round 3: Reviewer 3 (pharmacoepidemiology and prescribing data)

**Manuscript:** Draft 4 (`paper/manuscript.md`), with the response to round 2 (`paper/reviews/response_round2.md`).

**What I checked.** I read the code, not only the letter:
- `build_panel.py`, `hospital_medicines.py`, `steroid_trends.py`, `plot_variation.py`, `make_tables.py` and `check_epd_dexamethasone.py`;
- `outputs/logs/build_panel_*.txt`, `outputs/hospital/*` and `outputs/descriptives/*`;
- `data/raw/openprescribing/epraccur.csv`, `data/raw/scmd/vmp_classification.csv` and a few single-month practice extracts (small reads only).

I modified no project file other than this report.

---

## 1. Recommendation

**Minor revision. Nothing blocks publication.**

The two data-handling problems from round 2 are fixed correctly, and I confirmed both in the data:
- **N1, closed practices silently dropped.** The share of items from standard GP practices is now flat at 98.7–98.9% from 2010 to 2024 (`build_panel_ltla_residence.txt`, line 2).
- **N2, positive control.** It is now measured in pyrazinamide DDD.

The hospital glucocorticoid exposure now matches the Methods. The tacrolimus double-count is removed, with an assertion.

What remains is:
- two text figures that were not updated after the rerun;
- inaccuracies and leftover placeholders in the response letter;
- one advisable sensitivity analysis (IV methylprednisolone pulses).

None of these could change the conclusions.

---

## 2. Status of round 2 items

### New major issues from round 2

| Item | Status | Verification |
|---|---|---|
| **N1** Truncated `epraccur` removes closed practices | **Addressed** | **Code:**<br>• `build_panel.py:90-101` adds codes absent from `epraccur` that have GP code format.<br>• `steroid_trends.py:45` uses the same mask.<br>**Is the format rule sound?** I checked it against the registration releases:<br>• Unlisted GP-format items were 3.31% in July 2011, 2.11% in December 2013 and 1.58% in July 2014.<br>• Of those items, 62.6%, 96.6% and 99.2% came from practices present in a practice × LSOA registration release, so they are confirmed GP practices. The remainder in 2011 is practices closed before April 2014.<br>• Among listed codes, non-RO76 codes with GP format carry only about 0.2% of items, and most of that is RO76 dual-setting practices (see new issue 5). Genuine non-GP settings with GP-format codes carry about 0.05%.<br>• So the rule can admit at most a negligible amount of non-GP prescribing.<br>**Rerun:** the splice table was rerun.<br>**Not done:**<br>• Request 4 (LTLAs losing >2% of items under the old rule) was not reported. This is acceptable now that the artefact is removed.<br>• The text figures are wrong (new issue 1). |
| **N2** Positive-control DDD construction and attenuation | **Addressed** | **DDD construction:**<br>• `hospital_medicines.py:83-86` counts pyrazinamide content only; ethambutol-only products contribute 0.<br>• All 13 pyrazinamide-containing VMPs have the correct `pyrazinamide_mg_per_unit` for their SCMD unit (TABLET or ML), e.g. Rifater 300 mg, Voractiv 400 mg, 500 mg/5 ml = 100 mg/ml.<br>• 2024 national pyrazinamide DDD-years (after apportionment) = 1,339. That is plausible for about 5,500 notifications with 2+ months of pyrazinamide; the old measure gave about 2,957.<br>**Elasticity:**<br>• Values and CIs match the outputs: UTLA 0.361 (SE 0.134 → 0.10–0.62); rifamycin/isoniazid 0.367 (0.22–0.51).<br>• The requested wording is in place: manuscript l. 538-539, the Table S3 note (l. 953), and the timing assumption.<br>**Not done:** separate pyrazinamide-only and ethambutol-only series (declined). Acceptable. |
| **N3** Hospital glucocorticoid measure and scenario | **Largely addressed** | **Fixed:**<br>• `hospital_medicines.py:89-92, 167`: the candidate exposure is prednisolone-equivalent mg from prednisolone and methylprednisolone only.<br>• Dexamethasone and hydrocortisone form a separate DDD-based descriptive group.<br>• The RR 4.9 scenario is removed from `RR_SCENARIOS` (l. 50-58), and the Methods (l. 262-266) and Table 3 labels agree.<br>• Substance matching is clean. `substances` has only five values in this group, so "hydrocortisone" cannot catch fludrocortisone, and every row has `mg_per_unit` and `pred_equiv_factor`.<br>**Not done:** the request to report IV methylprednisolone pulses separately. It was neither implemented nor declined in the letter (new issue 3). |
| **N4** Response claims not reflected | **Mostly addressed** | **Now present:**<br>• FP10(HP) (l. 738);<br>• extraction dates and final/provisional status (l. 840);<br>• within-area SD for items, ADQ and mg (`within_between_variation.csv`, 23 rows);<br>• transplant inputs in Table 2;<br>• drug-group rules (Table S9).<br>**Declined, with reasons given:** the primary care elasticity grid and the dose-stratified OCS scenario. Acceptable.<br>**Not done:** a presentation-level listing at three time points. Table S9 gives rules, not listings. Acceptable given the rules are published and code is public. |

### Other round 2 items

| Item | Status | Comment |
|---|---|---|
| N5 Dexamethasone share of primary care mg | **Addressed** | `check_epd_dexamethasone.txt`: 5.6%, 6.7% and 6.5% of mg (Jan 2015, Jul 2019, Jul 2024), matching l. 739. There were no NULL `UNIDENTIFIED` rows, which also closes round 2 minor 5. |
| N6 Tacrolimus double count | **Addressed** | `hospital_medicines.py:75-77`: dedupe plus an assertion. The duplicate rows were identical in DDD and mg, so keeping the first row is safe. |
| N7 City of London at UTLA | **Addressed** | `MERGES` now sends City to Hackney at both levels (`build_panel.py:38-41`). This is used consistently for population (l. 177), covariates (l. 208-211), TB counts (`build_tb_annual.py:50,64`), hospital catchments (`hospital_medicines.py:113`) and census birthplace (l. 151). Residual: the Fingertips 3-year windows put City with Westminster, but they are used only for Table S8 and the docstring says so. |
| Minor 4 Nearest registration release and fallback | **Addressed** | `build_panel.py:141-163`. Share apportioned by residence plus share assigned by postcode: 2011 99.79%, 2012 99.85%, 2013 99.91%, from 2014 ≥99.99%. The loss of at most 0.2% in 2011 is negligible. |
| Minor 6 `INJECTABLE` regex | Declined | Acceptable; I found no false exclusions. |
| Minor 7-8 DMARD and transplant definitions | **Addressed** | Limitations, l. 739. |
| Minor 9-10 Unmatched trusts in 2023-24 | Declined | Acceptable. Unmatched shares are ≤1.5% for candidate and control groups (Table S7). |
| Minor 13 Levetiracetam classification | Declined | Acceptable; coverage of 95% is now stated (l. 532). |
| Minor 14 Stale import and docstring | **Partly** | The import is removed. Docstrings are still stale (new issue 6). |
| Minor 15 Area counts | **Addressed** | 151 and 294 are used throughout; "292" no longer appears. |
| Minor 16 Extraction dates, DOI | **Partly** | Dates are stated. There is no DOI deposit, and the ONSPD version (August 2025, `build_panel.py:33`) is not stated in the manuscript. |
| Minor 5 (round 1) ONSPD version | **Not** | As above. It is a one-line fix. |
| M8 Overlap concordance at the splice | Declined | It is stated as unassessed (l. 734). Acceptable. |
| B5/B6 Legacy files | **Addressed** | Moved to `legacy/`, per the letter. I did not re-inspect them. |
| B18, B19 | **Addressed** | l. 735 (catchments applied across years); l. 532 (coverage). |
| Minor 10, 22 (round 1) MDE uncertainty, reporting checklist | **Not** | Minor. I do not insist. |

---

## 3. New issues

### Must fix (text and letter; no reanalysis)

1. **Wrong percentages for the closed-practice correction** (manuscript l. 209-211; response l. 10-11). Both documents say the old rule dropped "3.8% of items in 2011, 1.9% in 2014". The logs give different values. From `build_panel_ltla_residence.txt:1-2`, the difference between standard GP practices and practices listed as RO76, as a share of all items, is:
   - 2010: 3.8%
   - 2011: 3.4%
   - 2013: 2.3%
   - 2014: 1.7%
   - 2015: 0.7%
   - 2016: 0.0%

   My single-month checks agree: 3.31% in July 2011 and 1.58% in July 2014. The quoted "3.8%" is the 2010 value, a year with 5 months that is not analysed. Correct both documents to 3.4% (2011) and 1.7% (2014), or state how the figures were derived.

2. **Stale splice figures** (manuscript l. 734). The text still gives the round 2 numbers:
   - oral glucocorticoids: "+3.3% at the splice against +0.6% and +1.0% either side";
   - all antibacterials: "−0.1% against −4.5% and −5.6%".

   The rerun `outputs/descriptives/splice_agreement_2013_2014.csv` gives:
   - oral glucocorticoids: +2.8% against +0.1% and +0.1%;
   - all antibacterials: −0.6% against −5.0% and −6.4%.

   The response letter (l. 17-18) quotes the new values, so the manuscript was not updated. Note also that the oral glucocorticoid discontinuity is now relatively larger against its neighbours than before. The text's conclusion (EPD-only restriction, l. 489: 0.979, 0.939–1.021) still holds.

3. **The response letter is not in a submittable state.**
   - l. 80 contains unrendered template fields: `{{n_sig_ltla}} of {{n_est_ltla}}`.
   - l. 138 reads "[pending check at assembly]".
   - **Inaccurate dedupe claim.** l. 45-47 says the (code, unit) dedupe also affected pyrazinamide 500 mg, ethambutol 100 mg and 400 mg, and Rifater. It did not. In `vmp_classification.csv` those products appear under two *different* SNOMED codes (the old and new dm+d VMP identifiers, e.g. 324477005 and 41954211000001104). The only included (code, unit) duplicates are the four tacrolimus granule rows. The earlier positive-control inflation came from counting ethambutol and fixed-dose-combination content, and that is what N2 fixed. Correct the letter.

4. **SCMD provisional status** (l. 840). The text says "final data where available, otherwise provisional". In `scmd_trust_month_vmp.csv.gz`, every month from January 2019 to December 2024 is `final`; provisional data start in April 2026. State plainly that all analysed SCMD months were final.

### Advisable (small reanalysis)

5. **IV methylprednisolone pulses dominate part of the hospital glucocorticoid exposure.** Using the classification and SCMD quantities, parenteral methylprednisolone vials of 500 mg or more make up 18–22% of the candidate exposure's prednisolone-equivalent mg each year, peaking in 2020–21. All parenteral forms make up 20–24%.
   - **Why it matters.** A single 1 g × 3 pulse equals about 375 days of prednisolone 10 mg. Pulses serve neurology (MS relapse), renal and transplant rejection, vasculitis and, in 2020–21, COVID-19 pneumonitis.
   - **Why a sensitivity analysis is worthwhile.** This is the one candidate exposure with a nominal hit (UTLA t−1: 1.024, 1.001–1.046), and the text attributes that hit to chance or bias.
   - **Request.** Refit that model with oral forms only; this is my round 2 N3 request. One row in Table S3b would do.
   - **Why not must-fix.** The estimate is already reported as not robust.

### Minor (optional)

6. **Stale docstrings and constants.**
   - `build_panel.py:111-116`: the `annual_prescribing` docstring still says "RO76" and "earliest year's shares used for earlier years", not the nearest-release rule.
   - `build_panel.py:42`: `MERGE = MERGES["utla"]` is unused.
   - `steroid_trends.py:5`: says "(RO76)".
   - `hospital_medicines.py:235-236`: `expected_effects` still says "patient-year equivalents".
   - `hospital_medicines.py:267`: the log label still says "patient-year equivalents".

7. **Dual-setting practices.** `build_panel.py:99` tests `ep[25] == "RO76"` exactly. The 6 practices whose setting is `"RO76|RO268"` are therefore excluded: they are listed, so the unlisted-code rule does not rescue them. They carry 0.14–0.15% of items in every sampled year from 2011 to 2024. The share is stable, so fixed effects absorb it and it is harmless. Use `.str.contains("RO76")` for correctness.

8. **Welsh `W` prefix in `GP_CODE`** (`build_panel.py:90`). Welsh practice codes are in the pattern. They are harmless, since they are not in the English registration releases and their postcodes map to no English LAD. Say so in a comment, or drop `W`.

9. **Hospital coverage metric for glucocorticoids.** `hospital_medicines.py:130` computes coverage on DDD even for the prednisolone-equivalent mg exposure. The Table S7 title correctly says "share of DDD", so the label is right. Coverage in mg would differ slightly, because pulse vials are concentrated in tertiary trusts. Optional.

---

## 4. Summary for the editor

The substantive exposure-construction errors I raised in round 2 are corrected, and the corrections are verified in data. The GP-format rule for closed practices is well supported: 97–99% of the items it admits in 2013–14 belong to practices that appear in registration releases. Before acceptance:
- fix the two stale or incorrect figures in the manuscript (l. 209-211, l. 734) and the SCMD status sentence (l. 840);
- clean up the response letter (placeholders; the incorrect dedupe claim).

A sensitivity analysis of hospital glucocorticoids restricted to oral forms is advisable, but not required.

*Reviewer 3*
