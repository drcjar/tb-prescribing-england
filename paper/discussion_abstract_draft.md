## Abstract

**Background.** Several commonly prescribed medicines, notably corticosteroids and other
immunosuppressants, modify individual TB risk. Openly published English prescribing and TB
surveillance data could, in principle, be linked to study these relationships at population level.
We assessed whether such ecological analyses can detect drug–TB associations.

**Methods.** We linked NHSBSA English Prescribing Dataset records (practice-level, 2014–2024) for
12 pre-specified drug groups, including positive and negative control exposures, to UKHSA TB
notifications. Three designs were used:
- a cross-sectional analysis of 105 Sub-ICB locations
- panel analyses of 149–151 upper-tier local authorities with rolling three-year and annual
  outcomes, using Poisson pseudo-maximum-likelihood with area and time fixed effects, lagged
  exposures and a lead-exposure falsification test
- analyses of change in oral corticosteroid prescribing against TB overall and in UK-born and
  non-UK-born people by region.

We calculated minimum detectable effects (MDEs) and compared them with the population effects
implied by published individual-level relative risks.

**Results.**
- **Cross-sectional analysis:** most drug groups were inversely associated with TB, but the
  associations disappeared after adjusting for country of birth and age structure.
- **Panel analyses:** no drug group was associated with subsequent TB incidence. For oral
  corticosteroids, a 10% within-area increase in prescribing gave an IRR of 0.985 (95% CI
  0.940–1.033).
- **Controls and falsification:** the positive control (antituberculosis drugs) was not detected,
  and future prescribing of some drugs "predicted" past TB, indicating residual confounding by
  trends.
- **Steroid trends:** oral corticosteroid items fell 9.7% and prednisolone milligrams per resident
  fell 21.2% between 2014 and 2024, but these changes did not track changes in TB incidence.
- **UK-born TB:** a regional association with prednisolone dose was implausibly large and did not
  survive multiple-testing correction.
- **Power:** the MDE for oral corticosteroids was 7.0% per 10% increase in prescribing, about 20
  times the expected effect (0.34%). Power to detect the expected effect was below 4% for every
  drug group.

**Conclusions.** Routinely published prescribing and TB notification data cannot detect plausible
population-level effects of primary care medicines on TB in England. Apparent associations mainly
reflect confounding by migration, age and area-specific trends. Causal questions about medicines
and TB require individual-level linked data, such as primary care records linked to hospital and
TB surveillance data, analysed with target trial emulation.

---

## Discussion

### Principal findings
Using three ecological designs and more than a decade of practice-level prescribing, we found no
credible association between primary care prescribing and TB incidence in England.
- **Cross-sectional results were reversed by adjustment:** crude inverse associations for nearly
  every drug class were explained by areas with young, migrant populations having both more TB and
  less chronic-disease prescribing.
- **Within-area models were null** for all drug groups, with confidence intervals excluding changes
  larger than about 5–10% per 10% change in prescribing.
- **The design could not have detected plausible effects:** the positive control was not detected,
  falsification tests failed for several exposures, and MDE calculations showed that even strong
  individual-level effects would move area-level TB incidence by well under 1%.

### Interpretation
**Why so little power.** The MDE analysis explains why the design was uninformative. Oral
corticosteroids carry about a five-fold individual risk,[Jick 2006] but only about 1% of people
use them at any time.[van Staa 2000; Fardet 2011]
- **Expected population signal:** a 10% relative change in use should move TB incidence by about
  0.3%. That is consistent with the small population attributable fractions reported for inhaled
  corticosteroids (0.5%)[Castellana 2019] and estimated here for oral corticosteroids (3.4%).
- **Detectable effects:** within-area models could detect only changes of 3.5–10%.
- **Why more data per area would not help:** power in aggregate studies depends mainly on the
  number of areas,[Sheppard 1996] and prescribing varies little within areas over time (within-area
  SD of log oral corticosteroid rate 0.07 vs 0.31 between areas). Fixed effects remove the
  between-area variation, which is where most of the information lies.[Gunasekara 2014]

**Why the crude and fixed-effects estimates differ.** The contrast mirrors the between- versus
within-country sign reversal reported for diabetes and TB.[Költringer 2023] Ecological bias from
effect modification cannot be removed by covariate adjustment.[Greenland & Morgenstern 1989] This
is relevant here because drug-associated TB risk may differ by ethnicity and country of
birth.[Dixon 2010; Ruzangi 2020]

**Steroid prescribing trends.** Corticosteroid prescribing fell during 2014–2024, with courses
becoming smaller and a step reduction in 2020–21. Over the same period TB incidence fell and then
rose, driven largely by migration.[UKHSA 2025; Thomas 2018] The two trends are unrelated once
shared national shocks are removed.

**The UK-born association.** The association between prednisolone dose and UK-born TB across
regions illustrates how apparent signals arise in these data.
- **It passed some checks:** lead exposure and the negative control exposure.
- **But its size is impossible under the model:** under the model used for the MDE, no relative
  risk, however large, could produce a 37% change in incidence from a 10% change in use.
- **And it is fragile:** it rests on nine regions and did not survive correction for multiple
  testing.

Region-specific declines in UK-born TB, which fell by roughly half in most regions and reflect
social risk factors, transmission and demographic change,[Davidson 2018; Nguipdop-Djomo 2020] are
the most plausible explanation.

### Strengths and limitations
**Strengths:**
- All data sources are public, and every analysis is reproducible from published code.
- Exposure groups and falsification tests were specified before the results were seen.
- Data quality was checked in three ways:
  - the older and newer prescribing releases were identical for June 2024
  - annual TB counts matched the published three-year counts (r = 0.996)
  - 98% of prescribing items were linked to an area.
- Positive and negative control exposures and lead tests were used,[Lipsitch 2010; Prasad & Jena
  2013] and power was quantified explicitly.

**Limitations of the exposure data:**
- **Primary care only:** the prescribing data miss hospital-prescribed medicines, including
  biologics, most specialist immunosuppression and in-hospital dexamethasone during the COVID-19
  pandemic.[RECOVERY 2021] These are among the highest-risk exposures.
- **Items and residents, not patients and dose:** exposure was measured as items per resident, not
  people treated or dose. The exception is prednisolone, where we derived milligrams from tablet
  strength because the ADQ field is not populated for steroids in the older release.
- **Area mapping:** practices were mapped to areas by postcode, so prescribing for patients
  registered across boundaries is misattributed.
- **Denominators:** we used ONS resident populations to avoid list inflation,[Hudson 2025;
  Venkatesan 2025] at the cost of a mismatch between practice catchments and local authority
  populations.

**Limitations of the outcome and confounder data:**
- **Birthplace:** TB by place of birth was available only at region level.
- **Unmeasured time-varying confounders:** the latent TB screening programme for new
  migrants,[Berrocal-Almanza 2022] social risk factors and diagnostic intensity[Kumwichar 2023]
  were not measured.
- **Minor boundary mismatches:** City of London and Isles of Scilly were combined with neighbouring
  authorities differently in the TB and population sources.

### Implications and future research
Open prescribing data are valuable for describing prescribing and for health services research,
but they are not suitable for estimating the effects of medicines on rare infectious outcomes such
as TB. Future work should use individual-level linked records. For example, CPRD Aurum linked to
Hospital Episode Statistics and UKHSA TB surveillance could support target trial emulations of
corticosteroid or immunosuppressant initiation and TB. We identified no such study for these drugs;
the only drug–TB target trial emulation we found concerned DPP-4 inhibitors.[Chen 2025]

At population level, the most useful additions would be annual local TB notifications stratified by
place of birth and age, obtainable through a UKHSA data request. Explicit adjustment for the latent
TB screening programme would also help.

### Conclusion
Ecological analyses of English prescribing data do not, and on power grounds cannot, detect the
population-level effects of primary care medicines on TB. Studies using these data should report
minimum detectable effects and falsification tests alongside associations.
