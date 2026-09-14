# Literature review: design, framing and discussion context
*(Individual-level relative risks and UK drug-use prevalence are covered separately in `literature_effect_sizes.md`; they are not repeated here.)*

Verification: every PubMed item below was checked against PubMed metadata/abstract (PMID, first author, year, journal, DOI), and the one-line claim was checked against the abstract. Grey literature (UKHSA/NHS) was checked against gov.uk / NHS England pages via web search. Items marked **[partly verified]** need a full-text check before citing.

---

## 1. Ecological / population-level studies of medication use (or drug-related conditions) and TB

Finding: **we found no ecological study linking area-level prescribing volumes to TB incidence** (searches covered corticosteroids, TNF inhibitors, PPIs, statins and fluoroquinolones). That makes the paper novel, but it also means the closest precedents come from other exposures.

- **Hermans S et al. 2015, J Int AIDS Soc** (PMID 26411694; doi:10.7448/IAS.18.1.20240). An ecological analysis of Cape Town sub-districts during ART scale-up. HIV-positive TB notifications fell, but less than individual-level efficacy would predict. *This is the best analogue: a drug with a large individual effect whose population-level signal is weakened by who gets treated and when.*
- **Goldhaber-Fiebert JD et al. 2011, Int J Epidemiol** (PMID 21252210; doi:10.1093/ije/dyq238). Individual survey data plus a 163-country longitudinal analysis: rising TB went with rising diabetes prevalence (OR 4.7–8.6, wide CIs). *Pairs a between-country ecological association with individual-level data. That combined design is what we argue for.*
- **Költringer FA et al. 2023, BMC Public Health** (PMID 36793018; doi:10.1186/s12889-023-15213-w). A 116-country panel with separate within-country and between-country Poisson effects. In high/upper-middle-income countries, *between*-country diabetes prevalence was associated with **lower** TB, but *within*-country increases were associated with higher TB. *A direct example of cross-sectional sign reversal from confounding, and of why a within-unit (fixed-effects) estimate is needed. Supports our panel design.*
- **Stevenson CR et al. 2007, BMC Public Health** (PMID 17822539; doi:10.1186/1471-2458-7-234). Estimates the population attributable fraction of TB due to diabetes in India (~15%). *Shows how a PAF is built from an RR and a prevalence. Useful for turning our MDE into a "plausible population effect".*
- **Shakoor S et al. 2016, Int J Mycobacteriol** (PMID 27931682; doi:10.1016/j.ijmyco.2016.07.008). Pakistan: population fluoroquinolone consumption correlated only weakly with *M. tuberculosis* FQ resistance, but strongly for *H. influenzae*/*Shigella*. *The only ecological drug–TB consumption study we found. It shows that aggregate consumption is a weak proxy for exposure in TB.*
- **Hogan CA et al. 2017, J Clin Tuberc Other Mycobact Dis** (PMID 31723692; doi:10.1016/j.jctube.2016.12.001). Meta-analysis: fluoroquinolone use delays TB diagnosis by ~11 days. *A mechanism by which antibiotic prescribing could shift notification **timing** rather than incidence. Relevant if we ever use antibiotics as an exposure or negative control.*
- **Dixon WG et al. 2010, Ann Rheum Dis** (PMID 19854715; doi:10.1136/ard.2009.118935). BSRBR: TB was 3–4× higher with infliximab/adalimumab than etanercept, and six-fold higher in non-white patients. *Effect modification by ethnicity is exactly the situation where Greenland & Morgenstern show ecological bias is unavoidable (see theme 5).*

## 2. Studies using English open prescribing data linked to area-level outcomes, and their pitfalls

- **Gulliford MC et al. 2016, BMJ** (PMID 27378578; doi:10.1136/bmj.i3410). CPRD practices grouped by antibiotic-prescribing rate. A 10% reduction predicted ~1.1 extra pneumonia cases per practice per year, with no change for rarer complications. *The main precedent for a practice-level prescribing exposure against an infection outcome. It also shows that rare outcomes can only be assessed with very large numbers.*
- **Balinskaite V et al. 2019, Clin Infect Dis** (PMID 30339254; doi:10.1093/cid/ciy904). A national interrupted time series of the Quality Premium: overall no unintended infection consequences, but condition-specific signals that were "explained by parallel policy changes or small numbers". *Shows how co-occurring policies (for us, the LTBI programme) confound national time trends.*
- **Richards TC et al. 2025, Sci Rep** (PMID 40413267; doi:10.1038/s41598-025-02969-x). OpenPrescribing data mapped to neighbourhoods show strong deprivation gradients and a COVID-lockdown discontinuity in inhaler prescribing. *Prescribing is itself patterned by deprivation and disrupted in 2020, so both are confounders of the prescribing–TB link.*
- **Bacon S, Goldacre B. 2020, J Med Internet Res** (PMID 31929101; doi:10.2196/15603). Documents structural changes, relocations and undocumented revisions in NHS open datasets. *Cite this for data-harmonisation limitations (BNF code changes, CCG→Sub-ICB boundaries).*
- **Hudson SM et al. 2025/26, J Med Screen** (PMID 40525516; doi:10.1177/09691413251347408). Median practice list inflation was 8.6% (IQR 4.7–16.9%) and independently predicted lower screening coverage. *List inflation varies between areas and deflates per-capita rates, and it is likely higher where mobile and migrant populations live.*
- **Venkatesan S et al. 2025, JMIR Public Health Surveill** (PMID 41144579; doi:10.2196/64788). The GP-registered adult denominator is inflated relative to Census 2021, *differentially by sociodemographics*. *So "items per registered patient" carries denominator error that correlates with migration, which is our main confounder.*
- Methodological gap: **no identified paper validates the mapping of EPD practice data to local-authority populations against TB or other notifiable outcomes.** We should say so explicitly.

## 3. Sub-national TB epidemiology in England: confounders

- **Nguipdop-Djomo P et al. 2020, PLoS One** (PMID 33075092; doi:10.1371/journal.pone.0240879). An LSOA negative binomial analysis for 2008–12: most- vs least-deprived quintile IRR 3.35. The gradient was steeper in UK-born people (IRR 2.39) than in non-UK-born (1.78). *The closest methodological template for our cross-sectional model. Supports using UK-born TB as a separate outcome.*
- **Thomas HL et al. 2018, Thorax** (PMID 29674389; doi:10.1136/thoraxjnl-2017-211074). Of the 2011–15 fall in UK TB: 62% came from lower rates, 33% from fewer recent non-EU migrants, and 11% from pre-entry screening. *Time trends in TB are driven by migrant flows and screening policy, and these vary across areas and time.*
- **Crofts JP et al. 2008, Public Health** (PMID 18672258; doi:10.1016/j.puhe.2008.04.011). Migration explained most recent TB trends in England; the deprivation distribution was stable. *Further evidence that migration is the dominant time-varying driver.*
- **Aldridge RW et al. 2016, Lancet** (PMID 27742165; doi:10.1016/S0140-6736(16)31008-X). Post-arrival TB rose with TB prevalence in the country of origin. Reactivation was estimated at 46–91/100,000, with negligible onward transmission. *Supports adjusting for origin-country mix, not just "% non-UK-born".*
- **Davidson JA et al. 2018, Am J Epidemiol** (PMID 29878041; doi:10.1093/aje/kwy119). MIRU-VNTR clustering, a marker of recent transmission, was associated with being UK-born, drug misuse and prison. *UK-born TB mixes reactivation with transmission linked to social risk, which prescribing will not capture.*
- **Nguipdop-Djomo P et al. 2020, Sci Rep** (PMID 32221405; doi:10.1038/s41598-020-62667-8). UK-born adults: smoking, drug use and homelessness were independent TB risks, with PAFs of 18% for tobacco and 15% for class-A drugs. *Social risk factors that also correlate with prescribing (opioids, gabapentinoids).*
- **Berrocal-Almanza LC et al. 2019, Lancet Infect Dis** (PMID 31471131; doi:10.1016/S1473-3099(19)30260-9) and **2022, Lancet Public Health** (PMID 35338849; doi:10.1016/S2468-2667(22)00031-7). Pre-entry screening, early GP registration and LTBI testing/treatment lowered migrant TB (LTBI treatment HR 0.14), but programme uptake was low (17.8% IGRA-positive; 26% started treatment). *The LTBI programme is a real, area-specific intervention in the panel period.*
- **Loutet MG et al. 2018, Eur Respir J** (PMID 29326327; doi:10.1183/13993003.01226-2017). Newham (2014–15) evaluation that informed the national rollout. *Documents the programme's start in high-incidence areas.*
- **Grey literature (UKHSA, verified on gov.uk):** *TB in England 2025 report* (data to end-2024). 2024 notifications were 5,480 (+13% on 2023), 81.5% non-UK-born; non-UK-born notifications rose 15.2% and UK-born 3.9%. Notifications within 5 years of entry nearly doubled compared with 2019. The largest rises were in London and the West Midlands. There were 4,125 cases in 2020 (−12.7%, a COVID-era dip). UKHSA's *TB in England 2024 report* recorded an 11% rise in 2023. The NHS England LTBI programme has run since 2015/16 for 16–35-year-olds who arrived within 5 years from countries with incidence ≥150/100,000. **[Rollout dates by CCG/local authority not yet extracted. Take them from UKHSA/NHSE annual LTBI programme reports.]**

## 4. Individual-level UK (CPRD/HES/ETS) studies and target-trial designs: "what design is needed"

- **Pealing L et al. 2015, BMC Med** (PMID 26048371; doi:10.1186/s12916-015-0381-9). CPRD matched cohort: diabetes aRR 1.30 (1.01–1.67), based on 969 TB cases in ~7 million person-years. *Even a national GP cohort gets wide CIs for a modest RR, which reinforces our MDE argument.*
- **Ruzangi J et al. 2020, BMC Nephrol** (PMID 32998703; doi:10.1186/s12882-020-02065-4). CPRD: CKD aRR 1.42, with possible effect modification by ethnicity (2.83 in non-white patients). *A template for the design, and more evidence of ethnicity-driven effect modification.*
- **Jick SS et al. 2006, Arthritis Rheum** (PMID 16463407; doi:10.1002/art.21705). A glucocorticoid nested case-control study with a dose–response (≥15 mg: OR 7.7). *A UK GPRD design; RR values are in the effect-sizes file.* **[GPRD data source is from full-text knowledge, not the abstract.]**
- **Critchley JA et al. 2025, Clin Infect Dis** (PMID 39495677; doi:10.1093/cid/ciae538). CPRD identified 15,820 incident TB cases from linked primary care, HES and mortality data for 2000–20. *Shows that CPRD–HES linkage can support TB outcome studies of adequate size.*
- **Chen YG et al. 2025, BMC Med** (PMID 41137015; doi:10.1186/s12916-025-04423-1). A Taiwan nationwide target trial emulation: DPP-4 inhibitors aHR 0.85 for pulmonary TB. *The only drug–TB target trial emulation we found. **No target trial emulation of immunosuppressants/corticosteroids and TB was identified.** That is a gap worth naming as future work (CPRD Aurum + HES + ETS/UKHSA linkage).*

## 5. Methods: ecological bias, negative controls, falsification, fixed effects, power

- **Greenland S, Morgenstern H. 1989, Int J Epidemiol** (PMID 2656561; doi:10.1093/ije/18.1.269). Effect modification alone can cause severe ecological bias, and ecological standardisation or adjustment generally does not remove it.
- **Morgenstern H. 1995, Annu Rev Public Health** (PMID 7639884; doi:10.1146/annurev.pu.16.050195.000425). The standard taxonomy of ecological designs (multiple-group, time-trend, mixed) and their biases, including temporal ambiguity and migration across groups. *Use it to name our designs.*
- **Wakefield J, Shaddick G. 2006, Biostatistics** (PMID 16428258; doi:10.1093/biostatistics/kxj017). Aggregation loses information, and using estimated exposures biases health effects.
- **Sheppard L et al. 1996, Stat Med** (PMID 8888477). In aggregate-data studies, power depends mainly on the *number of groups*, not survey size within groups. *Supports the MDE framing: ~150 UTLAs cannot be fixed by more data per area.*
- **Lipsitch M, Tchetgen Tchetgen E, Cohen T. 2010, Epidemiology** (PMID 20335814; doi:10.1097/EDE.0b013e3181d61eeb). The rationale for negative controls. *Frames levothyroxine as a negative-control exposure and anti-TB drugs as a positive control.*
- **Shi X, Miao W, Tchetgen Tchetgen E. 2020, Curr Epidemiol Rep** (PMID 33996381; doi:10.1007/s40471-020-00243-4). Review of negative-control assumptions and validation.
- **Prasad V, Jena AB. 2013, JAMA** (PMID 23321761; doi:10.1001/jama.2012.96867). Prespecified falsification end points. *Supports the lead-exposure test: future prescribing should not "predict" past TB.*
- **Gunasekara FI et al. 2014, Int J Epidemiol** (PMID 24366487; doi:10.1093/ije/dyt221). Fixed effects remove time-invariant confounding but not time-varying confounding or reverse causation, and they lose precision when exposure varies little within units. *This is exactly our limitation.*
- **Santos Silva JMC, Tenreyro S. 2006, Rev Econ Stat 88(4):641–58** (not in PubMed; verified via MIT Press). Poisson PML is consistent under heteroskedasticity. *The citation for our PPML estimator.*

## 6. COVID-era corticosteroids and subsequent TB

- **RECOVERY Collaborative Group. 2021, N Engl J Med 384:693–704** (PMID 32678530; doi:10.1056/NEJMoa2021436). Dexamethasone reduced mortality in patients on oxygen or ventilation. *This triggered the step change in steroid use from June 2020. Most of that use was in hospital, so it falls **outside EPD primary-care data**.*
- **Alemu A et al. 2022, PLoS One** (PMID 36441785; doi:10.1371/journal.pone.0277807). Systematic review of 33 case reports of TB after COVID-19: 62.5% had received corticosteroids, and 12 were migrants from endemic settings. *Anecdotal and confounded, but plausible.*
- **Kumwichar P et al. 2023, EClinicalMedicine** (PMID 36694864; doi:10.1016/j.eclinm.2023.101825). Thai national claims: COVID pneumonia was followed by pulmonary TB (HR ~7–10). The negative-control group also showed early excess (HR 1.58), suggesting detection bias. *Increased diagnostic contact can mimic incidence.*
- **Miyamori D et al. 2026, J Gen Fam Med** (PMID 42256042; doi:10.1002/jgf2.70139). Japanese insurance data: COVID was followed by TB treatment initiation (HR 4.14), and 14.7 with prior TB. *Separating the effects of COVID and of steroids is not possible in these data.*
- **Gopalaswamy R, Subbian S. 2021, Int J Mol Sci** (PMID 33917321; doi:10.3390/ijms22073773). Mechanistic review of the TB risk from corticosteroids given for COVID. **[Only the title/abstract screened.]**
- No population-level (ecological) study of COVID steroid use and TB incidence was identified.

---

## Implications for our paper

**Framing**
1. Present the work as a *falsification/feasibility* study: "Can routinely published prescribing data detect known drug–TB associations at population level?" Our answer is no, for reasons we can quantify: MDE, ecological bias and confounding. The null result is informative, not a failure. Hermans 2015 and Költringer 2023 are the best analogues.
2. Explain the sign reversal between the crude cross-sectional and fixed-effects estimates with Greenland & Morgenstern 1989 and Költringer 2023's between- vs within-country contrast.
3. State plainly that effect modification by country of birth/ethnicity (Dixon 2010; Ruzangi 2020) makes ecological bias unavoidable, *even with perfect covariate adjustment*.

**Additional analyses and covariates**
4. **Use UK-born TB notifications as an outcome.** This removes most reactivation of imported LTBI and migration-flow confounding (Nguipdop-Djomo 2020). Fingertips/UKHSA publish UK-born and non-UK-born rates by area, with small-number suppression, so check coverage.
5. **Model the LTBI programme as a time-varying covariate.** Code a UTLA-year indicator (or tests per 100,000) from UKHSA/NHSE LTBI annual reports, 2015/16 onwards. It is area-specific, it reduces TB in migrants (Berrocal-Almanza 2022), and it coincides with the prescribing trends.
6. Add time-varying migration measures: recent arrivals (e.g. NINo registrations or ONS long-term international migration by local authority), not just the static census % non-UK-born. Thomas 2018 and UKHSA 2025 show that recent entrants drove both the 2011–15 fall and the 2023–24 rise.
7. Treat 2020–21 as a structural break. Options: exclude it, add a COVID period × region interaction, or run a sensitivity analysis. Both notifications (−12.7% in 2020) and prescribing (Richards 2025) were disrupted.
8. Adjust for list inflation, or at least discuss it. Use ONS mid-year populations as denominators where possible, and do a sensitivity analysis on the ratio of registered to ONS population (Hudson 2025; Venkatesan 2025).
9. Consider a negative-control *outcome* as well as the exposure (e.g. an outcome unrelated to immunosuppression but sharing migration and deprivation structure) (Shi 2020).
10. Frame the MDE against a *population attributable fraction* benchmark (Stevenson 2007 approach): PAF = p(RR−1)/[1+p(RR−1)] with UK prevalence from the effect-sizes file. This shows that even a doubling of steroid use would move area TB rates by less than the MDE.

**Limitations to acknowledge**
- EPD covers primary-care dispensing only. It misses hospital dexamethasone (RECOVERY-era), biologics and most specialist immunosuppressants, which are exactly the high-RR exposures (TNF inhibitors).
- Practice-to-area mapping error and list inflation that correlates with migration.
- Unmeasured time-varying confounding (Gunasekara 2014). Examples: social risk factors, the LTBI programme, and diagnostic contact or detection bias (Kumwichar 2023; Hogan 2017).
- Few areas (Sheppard 1996), so our power is fundamentally limited.
- BNF/dataset structural changes (Bacon & Goldacre 2020).
- The appropriate design is individual-level CPRD Aurum–HES–UKHSA ETS linkage with target trial emulation. None exists yet for immunosuppressants and TB (theme 4 gap).

**Target journals** (all publish ecological or routine-data TB/prescribing work): *BMJ Open*; *PLoS One* (Nguipdop-Djomo 2020); *Journal of Public Health (Oxford)*; *ERJ Open Research* (Smith 2017, Pedrazzoli 2019); *Epidemiology and Infection*; *Pharmacoepidemiology and Drug Safety* (suits the negative-control/falsification angle); *BJGP Open*; *Int J Tuberc Lung Dis / IJTLD Open*.
