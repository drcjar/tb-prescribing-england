## Discussion

### Principal findings

We linked open English data on primary care and hospital prescribing with TB notifications, using several ecological designs at two geographic scales. The linkage worked only partly.

- **The positive control.** Hospital active-TB treatment tracked notifications between and within areas, but even this disease-specific signal was recovered with roughly 60% attenuation.
- **Candidate drugs.** No medicine plausibly affecting TB risk was associated with subsequent notifications. This held for systemic oral glucocorticoids, inhaled corticosteroids, DMARDs, transplant immunosuppressants, TNF, IL-6 and JAK inhibitors, and rituximab.
- **Signs of confounding.**
  - The negative-control exposure showed inverse estimates of similar size to some candidate drugs.
  - Several falsification tests failed.
  - The one nominal regional association was implausibly large.

  These patterns point to residual confounding by area-specific trends, not drug effects.
- **Power.** The analytic calculations and the simulation agreed: the designs could detect only effects one to two orders of magnitude larger than those implied by published relative risks or by UKHSA records of drug-associated TB.

### Why population effects of these medicines are undetectable

**Expected effects are small.** The population effect of a medicine is roughly its attributable fraction scaled by the relative change in use.

- **Oral glucocorticoids.** Current use carries an odds ratio of about 5 [Jick 2006], but only about 1% of people use them at any time [van Staa 2000; Fardet 2011]. A 10% change in use should therefore change TB notifications by about 0.3%.
  - Stratifying by age and place of birth lowers this to 0.29%, because use is concentrated in older UK-born people with low baseline risk.
  - UKHSA recorded steroid-associated immunosuppression in 30 of 5,490 people notified in 2024 [UKHSA 2025]. Even allowing for under-recording, that implies 0.05–0.1%.
- **Biologics.** Latent TB screening before anti-TNF therapy has been standard in the UK since 2005 [BTS 2005] and reduced TB risk by about 78% in registry data [Carmona 2005; Gómez-Reino 2007]. Growth in biologic use during 2019–2024 therefore took place under screening, so the relative risk relevant to a marginal increase in use is small. Oral glucocorticoids rarely trigger screening.

**The data carry little information.**
- **Little within-area variation.** Within-area variation in prescribing was very small (SD of log rate 0.04 for glucocorticoids, against 0.29 between areas), so a 10% change sits at the edge of the observed data. Fixed effects remove the between-area variation where most information lies [Gunasekara 2014].
- **Few areas.** Power in aggregate studies depends mainly on the number of areas [Sheppard 1996], which cannot be increased.
- **Linkage attenuation.** The positive control shows that attenuation from apportionment and dilution would shrink any true effect further.
- **Simulation.** Simulations that preserved the real error structure found power close to the false-positive rate for the published glucocorticoid effect.

### Confounding, falsification and negative controls

**Crude versus within-area associations.** Crude cross-sectional associations were strongly inverse and were explained by country of birth and age. Within areas, residual confounding remained visible:
- **Negative control.** Levothyroxine, which has no plausible effect on TB, showed inverse estimates (0.96–0.97) similar to metformin.
- **Opposite-signed lag and lead.** Inhaled corticosteroids and insulins had opposite-signed estimates when prescribing before and after the outcome year was estimated jointly.
- **Likely cause.** Both patterns are expected when prescribing and notifications share area-specific trends, for example migration-driven changes in the age and origin of the population, changes in registration or diagnostic activity, and prescribing policy. Year fixed effects cannot remove these trends.

**Ecological bias.** Area-level adjustment cannot remove bias arising from effect modification or from differences in baseline risk between people within areas [Greenland 1989; Morgenstern 1995]. For example, steroid users are mostly older and UK-born, whereas most notifications are in younger people born abroad.

**The UK-born association.** Regionally, prednisolone dose was associated with UK-born TB when prescribing before and after was estimated jointly (randomisation p = 0.04). We do not interpret this as a drug effect:
- An IRR of 1.41 per 10% increase exceeds the maximum possible under any relative risk (1.10) in the model used for expected effects.
- The same nine-region design produced failed falsification tests for non-UK-born TB.
- It also produced a failed negative control (levothyroxine) for older UK-born people.
- UK-born TB fell by 43% between 2014 and 2022, reflecting social risk factors, transmission and demographic change [Davidson 2018; UKHSA 2025]. Coincident regional trends in steroid dosing are the most plausible explanation.

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
- **Pre-2014 data.** The 2011–2013 series come from a different release, and overlap-period concordance could not be assessed. National year-on-year changes were continuous across the 2013/2014 splice for most groups, but not for oral glucocorticoids (+3.3% at the splice against +0.6% and +1.0% either side) or all antibacterials (−0.1% against −4.5% and −5.6%). Restricting to EPD-era exposure did not change the conclusions (Table S1).
- **Hospital catchments.** Hospital quantities were apportioned using admission-based catchments, which may misallocate specialist services.
- **Hospital data capture.** Capture of homecare-delivered biologics in SCMD could not be verified.
- **Hospital data period.** The hospital series spans only 2019–2024, including the pandemic.

**Limitations: outcome and confounder data.**
- **Notifications, not incidence.** The outcome is notified TB, subject to diagnostic delay, residence assignment, the 2021 transition from ETS to NTBS, and 2020 disruption.
- **Birthplace data.** TB by place of birth is published only by region, and UK-born population denominators by age are not published regionally.
- **Unmeasured confounders.**
  - Social risk factors and diagnostic intensity.
  - The area-level share of recent arrivals.
  - Latent TB programme activity after 2019/20.

**Limitations: design and analysis.**
- **Pre-specification.** Many analyses were added after initial null results and are exploratory.
- **Expected-effect inputs.** Relative risks for PPIs, statins and metformin come mainly from high-incidence settings, and prevalence inputs for hospital drugs are derived or illustrative. Neither would change the conclusions unless the true effects were an order of magnitude larger.

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
- **The null results do not mean these drugs are safe.** Glucocorticoids, biologics and JAK inhibitors remain important for individual patients. Drug-associated TB is serious, often extrapulmonary, and largely preventable.
- **Surveillance.** Monitoring is better served by more complete and detailed immunosuppression fields in NTBS than by ecological analysis of prescribing. Useful fields would record drug class, time since starting, and whether latent TB screening was done and treated.
- **Audit.** The practical lever is auditing latent TB screening before biologics, JAK inhibitors and high-dose, long-term glucocorticoids.
- **Aggregate data from UKHSA.** Aggregate UKHSA tables would allow population monitoring in the groups where drug-associated reactivation matters, namely:
  - notifications with recorded biologic or steroid immunosuppression;
  - notifications by area, year, place of birth, age and time since entry.

### Conclusion

Open English prescribing and TB notification data can be linked, but with heavy attenuation. Ecological analyses of these data cannot detect the population-level effects of medicines on TB: plausible effects lie one to two orders of magnitude below what the designs can resolve, and the apparent associations that do arise reflect confounding by migration and area-specific trends.

{{box_target_trial}}
