## Discussion

### Principal findings

We linked open English data on primary care and hospital prescribing with TB notifications, using several ecological designs at two geographic scales. The linkage worked only partly.

- **The positive control.** Hospital active-TB treatment tracked notifications between areas and, weakly, within areas. Its elasticity of 0.36–0.40, with wide confidence intervals, reflects apportionment error and variation in drug volume per person treated.
- **Candidate drugs.** No medicine plausibly affecting TB risk was robustly associated with subsequent notifications. This held for systemic oral glucocorticoids, inhaled corticosteroids, DMARDs, transplant immunosuppressants, TNF, IL-6 and JAK inhibitors, and rituximab. Hospital systemic glucocorticoids had a small nominal association that was not robust, was absent for oral forms, and implied an implausibly large attributable fraction.
- **Signs of confounding.**
  - The negative-control exposure showed inverse estimates of similar size to some candidate drugs.
  - Following-year prescribing was inversely associated with notifications for several groups, and collinearity between adjacent years did not explain this.
  - The regional association with UK-born TB was implausibly large, not significant by randomisation inference, and dependent on London.

  These patterns are compatible with residual confounding by area-specific trends, chance or measurement error, and not with drug effects of plausible size.
- **Power.** The analytic calculations and the simulation both showed that plausible effects are undetectable: the designs could detect only effects roughly 10 to several hundred times larger than those implied by published relative risks or by UKHSA records of drug-associated TB. Simulated power exceeded analytic power at the real standard error, probably because permuted exposures lost their alignment with local notification trends.

### Why population effects of these medicines are undetectable

**Expected effects are small.** The population effect of a medicine is roughly its attributable fraction scaled by the relative change in use.

- **Oral glucocorticoids.** Current use carries an odds ratio of about 5 [Jick 2006], but only about 1% of people use them at any time [van Staa 2000; Fardet 2011]. A 10% change in use should therefore change TB notifications by about 0.3%.
  - Stratifying by age lowers this to 0.29%, because use is concentrated in older people while most notifications are in younger adults.
  - UKHSA recorded steroid-associated immunosuppression in 30 of 5,490 people notified in 2024 [UKHSA 2025]. Converted to an attributable fraction, that implies 0.04% per 10% increase with complete recording, or 0.09% if only half of drug-associated immunosuppression is recorded.
- **Biologics.** Latent TB screening before anti-TNF therapy has been standard in the UK since 2005 [BTS 2005], and NICE guidance covers testing people who are or will be immunosuppressed [NG33]. In a Spanish registry, TB rates in people with rheumatoid arthritis treated with TNF antagonists were 6.2 times those in untreated people before screening recommendations, and fell by 83% to about the untreated rate afterwards [Carmona 2005]; risk was about seven times higher when the recommendations were not followed [Gómez-Reino 2007]. Growth in biologic use during 2019–2024 therefore took place under screening, so the relative risk relevant to a marginal increase in use is small. Screening is less consistently done before oral glucocorticoids. UKHSA recorded biological-therapy immunosuppression, a category that includes non-TNF biologics, in 54 notifications in 2024; converted to an attributable fraction, that implies 0.08–0.16% per 10% increase in use.

**The data carry little information.**
- **Little within-area variation.** Within-area variation in prescribing was very small (SD of log rate 0.04 for glucocorticoids, against 0.29 between areas), so a 10% change sits at the edge of the observed data. Fixed effects remove the between-area variation where most information lies [Gunasekara 2014].
- **Few areas.** Power in aggregate studies depends mainly on the number of areas [Sheppard 1996], which cannot be increased.
- **Linkage attenuation.** For hospital medicines, the positive control shows that apportionment would shrink any true effect further. No working positive control was available for primary care, so the validity of that linkage is untested. Other hospital drugs have their own sources of error (homecare delivery of biologics, specialist centres, biosimilar switching), and the positive control was analysed in the same year while candidate drugs were analysed in the previous year, so the attenuated ratios are illustrative.
- **Simulation.** Simulations on the real notification counts rejected the null for the published glucocorticoid effect no more often than when there was no effect.

### Confounding, falsification and negative controls

**Crude versus within-area associations.** Crude cross-sectional associations were strongly inverse and were explained by country of birth and age. Within areas, residual confounding remained visible:
- **Negative control.** Levothyroxine, which has no plausible effect on TB, showed inverse estimates (0.96) similar to metformin.
- **Lag and lead patterns.** Following-year prescribing was inversely associated with notifications for inhaled corticosteroids, insulins and oral glucocorticoids. These associations persisted when same-year prescribing was added and the lag and lead estimates were almost uncorrelated, so they are not an artefact of collinearity.
- **Likely cause.** Both patterns are compatible with prescribing and notifications sharing area-specific trends, for example migration-driven changes in the age and origin of the population (with accompanying changes in practice registration and in vitamin D prescribing in South Asian-born communities), changes in diagnostic activity, and prescribing policy. Year fixed effects cannot remove these trends.

**Metformin.** Its estimates should be read against the high prevalence of both diabetes and latent TB infection among South Asian-born people; diabetes itself increases TB risk [Pealing 2015].

**Ecological bias.** Area-level adjustment cannot remove bias arising from effect modification or from differences in baseline risk between people within areas [Greenland 1989; Morgenstern 1995]. For example, steroid users are mostly older and UK-born, whereas most notifications are in younger people born abroad.

**The UK-born association.** Regionally, prednisolone dose in an earlier year was imprecisely associated with UK-born TB (joint lag estimate 1.45 per 10% increase). We do not interpret this as a drug effect:
- The regional MDEs (roughly 50–120% per 10%) are far above the 10% maximum possible under the model used for expected effects, so any significant regional estimate must reflect chance or bias.
- It was not significant by randomisation inference (p = 0.23), and it largely disappeared when London was excluded (1.12).
- The same nine-region design produced failed falsification tests for non-UK-born TB and a failed negative control (levothyroxine) for older UK-born people.
- UK-born TB fell by 48% between 2014 and 2022 [UKHSA 2025], while oral glucocorticoid dosing also declined. Any two declining regional series will tend to correlate, so coincident trends are the most plausible explanation.

**Protopathic bias.** Glucocorticoids and antibacterials prescribed for undiagnosed TB, and glucocorticoids used in treating TB meningitis and pericarditis [Thwaites 2004], create reverse associations in the same year. This is why the primary exposure was prescribing in the previous year. The same bias probably inflates the individual-level estimates used to derive expected effects [Jick 2006]; if so, the true gap between expected and detectable effects is even wider.

### Strengths and limitations

**Strengths.**
- **Open and reproducible.** All data are public, and code and processed data are openly available.
- **Exposure measurement.**
  - Primary care exposure was defined at presentation level, with dose measures, and apportioned by where registered patients live.
  - Hospital medicines were classified by mechanism using defined daily doses, with trust mergers resolved.
- **Checks on validity.**
  - A disease-specific positive control, negative-control exposures and falsification tests estimated jointly.
  - Randomisation inference for the nine-region analyses.
  - Year-specific spatial diagnostics.
  - Power assessed both analytically and by simulation on the real data.
- **Independent peer review.** Three independent reviews prompted substantial revision.

**Limitations: exposure data.**
- **Prescribing measures.** Exposure was measured as prescribing volume per resident, not as people treated.
- **Apportionment.** Apportioning by patient residence used annual April snapshots, with 2014 shares applied to 2011–2013.
- **Pre-2014 data.** The 2011–2013 series come from a different release, and overlap-period concordance could not be assessed. National year-on-year changes were continuous across the 2013/2014 splice for most groups, but not for oral glucocorticoids (+2.8% at the splice against +0.1% in each adjacent year) or all antibacterials (−0.6% against −5.0% and −6.4%). Restricting to EPD-era exposure did not change the conclusions (Table S1).
- **Hospital catchments.** Hospital quantities were apportioned using admission-based catchments, which may misallocate specialist services, and the 2024 catchments were applied to every year from 2019.
- **Hospital data capture.** Capture of homecare-delivered biologics in SCMD could not be verified.
- **Hospital data period.** The hospital series spans only 2019–2024, including the pandemic. Hospital dexamethasone use rose with its adoption for severe COVID-19 [RECOVERY 2021], a marker of COVID-19 severity patterned by deprivation and ethnicity, so dexamethasone and hydrocortisone were separated from the candidate glucocorticoid exposure.
- **Hospital prescriptions dispensed in the community.** Prescriptions written in hospitals and dispensed by community pharmacies (FP10(HP)) are recorded in the English Prescribing Dataset under hospital prescribers, so our restriction to GP practices excluded them, and they are not in SCMD. Some TB treatment and specialist medicines reach patients this way, so they are missing from both exposures as analysed.
- **Drug group definitions.** Conventional DMARDs exclude hydroxychloroquine and sulfasalazine, which carry little TB risk. Mercaptopurine includes leukaemia maintenance therapy, and the primary care "transplant immunosuppressant" group includes shared-care use of mycophenolate and ciclosporin for autoimmune disease. Dexamethasone, despite its high potency, contributed only 5.6–6.7% of prednisolone-equivalent mg in primary care (2015, 2019 and 2024 samples), so it does not drive the dose measure.

**Limitations: outcome and confounder data.**
- **Notifications, not incidence.** The outcome is notified TB, subject to diagnostic delay, residence assignment, the 2021 transition from ETS to NTBS, and 2020 disruption.
- **Birthplace data.** TB by place of birth is published only by region, and UK-born population denominators by age are not published regionally. The model for UK-born notifications at age ≥65 therefore uses all residents aged ≥65 as the denominator, which can create spurious trends as the older non-UK-born population grows.
- **Screening of migrants.** Pre-entry screening of long-stay visa applicants (piloted in selected high-incidence countries from 2005 and extended to all high-incidence countries in 2012–2014) and the LTBI programme for new migrants, whose testing coverage was incomplete [Berrocal-Almanza 2022], both target recent entrants in the areas where they settle. Neither is fully captured by our covariates.
- **Outcome definitions.** We did not analyse culture-confirmed pulmonary TB or drug-resistant TB, which were not available by local authority and year in the published tables we used.
- **Unmeasured confounders.**
  - Social risk factors and diagnostic intensity.
  - The area-level share of recent arrivals.
  - Latent TB programme activity after 2019/20.

**Limitations: design and analysis.**
- **Pre-specification.** Many analyses were added after initial null results and are exploratory.
- **Expected-effect inputs.** Relative risks for PPIs, statins and metformin come mainly from high-incidence settings, and prevalence inputs for hospital drugs are derived or illustrative. Neither would change the conclusions unless the true effects were an order of magnitude larger.
- **Positive control.** The hospital positive control is a disease-specific drug with a large same-year signal. We did not test whether a small lagged effect injected through the apportioned hospital exposure would be recovered, and primary care had no working positive control.

### Implications

**For research.**
- Open prescribing data are valuable for describing prescribing [Bacon 2020; OpenPrescribing 2026] but cannot estimate the effects of medicines on rare outcomes such as TB.
- Ecological studies of rare outcomes should report the following alongside any associations:
  - minimum detectable effects;
  - a positive control with its elasticity;
  - negative controls;
  - falsification tests.
- Causal questions need individual-level linked data analysed with target trial emulation (Box). Even national cohorts give wide intervals for modest relative risks [Pealing 2015]. The only drug–TB target trial emulation we identified concerned DPP-4 inhibitors [Chen 2025].

**For TB programmes.**
- **The null results do not mean these drugs are safe.** Glucocorticoids, biologics and JAK inhibitors remain important for individual patients. Drug-associated TB is serious, often extrapulmonary [Keane 2001], and largely preventable.
- **Surveillance.** Monitoring is better served by more complete and detailed immunosuppression fields in NTBS than by ecological analysis of prescribing. Useful fields would record drug class, time since starting, and whether latent TB screening was done and treated.
- **Audit.** The practical lever is auditing latent TB screening before biologics, JAK inhibitors and high-dose, long-term glucocorticoids.
- **Aggregate data from UKHSA.** Aggregate UKHSA tables would allow population monitoring in the groups where drug-associated reactivation matters, namely:
  - notifications with recorded biologic or steroid immunosuppression;
  - notifications by area, year, place of birth, age and time since entry.

### Conclusion

Open English prescribing and TB notification data can be linked, although hospital medicines were linked only with heavy attenuation and the linkage of primary care prescribing could not be validated. Ecological analyses of these data cannot detect the population-level effects of medicines on TB: plausible effects lie roughly 10 to several hundred times below what the designs can resolve, and the associations that do arise are compatible with residual confounding, chance or measurement error rather than drug effects.

{{box_target_trial}}
