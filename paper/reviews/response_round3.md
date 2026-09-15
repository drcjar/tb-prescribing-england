# Response to reviewers, round 3

All three reviewers recommended minor revision, with nothing blocking publication. Every
must-fix item was checked against the outputs and corrected. No primary analysis changed. One
advised sensitivity analysis was added (oral-only hospital glucocorticoids).

## Reviewer 1 (epidemiology and biostatistics)

1. **Splice figures in Limitations.** Updated to the rerun values: oral glucocorticoids +2.8%
   against +0.1% in each adjacent year; all antibacterials −0.6% against −5.0% and −6.4%.
2. **Lag/lead correlation range.** Corrected to −0.83 to +0.08 in the two-year model (oral
   glucocorticoids −0.38, inhaled corticosteroids −0.46). "Strongly negatively correlated" is
   removed from Methods, the Table 1 legend and the Discussion.
3. **Falsification reading.** We agree. With year t added, the lag and lead estimates are almost
   uncorrelated (−0.23 to +0.17), yet the following-year terms stay inverse. Results, Discussion
   and Abstract now say that collinearity does not explain the inverse following-year associations,
   which are more consistent with shared trends. The protopathic reading of the same-year terms is
   removed, and we note that their sign differs between Tables S2 and S2b.
4. **Multiplicity.** The comparison with 5% is removed. The text now notes that estimates are
   overlapping specifications and that the null simulation rejected 7.8%, and uses "compatible
   with shared trends".

**Minor.**
- **Simulation mechanism.** Now "probably".
- **Regional MDEs.** Now calculated from the t(8) intervals and quantiles, written to
  `outputs/steroids/regional_mde.csv` and shown in Table S5 (46–98% per 10% for UK-born
  notifications, 54–119% at age ≥65).
- **Positive control.** Timing is removed as an explanation of the elasticity (the following-year
  estimate was null). "Dominated by apportionment" is replaced by "drug specificity is not its main
  source".
- **Prevented fraction.** Methods now say it is reported for all drugs and is relevant for drugs
  expected to protect.
- **Abstract.** Now says "after correction for multiple testing".
- **Hospital ratios.** Qualified by level (26–520 upper-tier, 23–522 lower-tier).
- **2020 count.** 4,123 throughout.
- **Hospital test count.** Now given: 22 of 260 within-area estimates nominally significant, 12 of
  them the expected same-year TB-treatment associations.
- **Figure and table order.** Figures renumbered in order of first citation; supplementary tables
  first cited in numerical order in Methods.
- **Round 2 letter.** Template placeholders and old simulation SEs corrected.

## Reviewer 2 (TB clinical and public health)

1. **NICE NG33.** Now cited in the Discussion (screening before biologics). The
   screening-registry detail (6.2-fold before recommendations, fall to the untreated rate after
   [Carmona 2005]) was moved into the main Discussion. That text had been drafted in a file the
   assembly script does not include, which is why it was missing. The remaining reference note
   ("accessed date to be added") is replaced with the access date.
2. **FP10(HP).** Corrected. These prescriptions are in the EPD under hospital prescribers, were
   excluded by our restriction to GP practices, and are not in SCMD.
3. **Pre-entry screening.** Corrected: piloted in selected high-incidence countries from 2005 and
   extended to all high-incidence countries in 2012–2014.
4. **2020 count.** 4,123 throughout.

**Optional.**
- **LTBI programme.** Wording changed from "reduce notifications" to "target recent entrants",
  noting incomplete testing coverage [Berrocal-Almanza 2022].
- **Hospital glucocorticoids.** Now described as "similar but imprecise" when 2020–21 is excluded.
  The oral-only sensitivity analysis shows the association depended on IV methylprednisolone.
  Hospital hydrocortisone is described as used mainly for acute illness.
- **Rifamycin/isoniazid.** Wording softened.
- **"41% within five years".** Now cited to UKHSA 2025.
- **Box.** The unsourced clause about rates in older UK-born adults is removed.
- **"Biological therapy".** Now stated in the Discussion as a single-year count that includes
  non-TNF biologics.

## Reviewer 3 (pharmacoepidemiology and prescribing data)

1. **Dropped-item shares.** Corrected to 3.4% (2011) and 1.7% (2014), matching the logs, in the
   manuscript and the round 2 letter.
2. **Splice figures.** Corrected (see Reviewer 1, item 1).
3. **Round 2 letter.**
   - Placeholders filled.
   - The duplicate-row statement corrected: only the tacrolimus granule rows were duplicated.
   - The figure-order item completed.
4. **SCMD status.** Months from April 2019 are final data. January–March 2019 exist only in an
   earlier, since-retired release whose final status could not be confirmed. This is now stated
   in Data availability.

**Advisable.** Done. Restricting hospital glucocorticoids to oral forms gave 1.011 (0.991–1.032)
at upper-tier and 1.015 (0.994–1.036) at lower-tier level. The nominal association therefore
depended on IV methylprednisolone pulses, and this is reported in Results, Discussion and Abstract.

**Minor.**
- **ONSPD version.** Now stated (August 2025).
- **Not changed:** stale docstrings, the unused `MERGE` constant, the exact-match test for
  dual-setting practices (0.15% of items, stable) and the Welsh `W` code prefix. None affects the
  results.
