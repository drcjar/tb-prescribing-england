## Introduction

Tuberculosis (TB) remains a public health problem in England. After falling steadily from 2011 to
a low of 4,125 notifications in 2020, TB notifications rose by 13% in 2024, to 5,480.[UKHSA 2025]
Most cases occur in people born outside the UK, many from reactivation of latent infection acquired
abroad.[Aldridge 2016; UKHSA 2025] Recent changes in national incidence have been driven largely by
migration flows and screening policy.[Thomas 2018; Crofts 2008]

Host factors also modify TB risk, and several are shaped by commonly prescribed medicines. In
individual-level studies:
- **Oral glucocorticoids:** current use is associated with about a five-fold increase in TB risk,
  rising with dose.[Jick 2006]
- **Inhaled corticosteroids and conventional immunosuppressants:** associated with smaller
  increases.[Brassard 2011; Castellana 2019; Brassard 2006]
- **Proton pump inhibitors:** associated with increased TB risk.[Song 2019]
- **Statins and metformin:** associated with lower TB risk.[Li 2020; Zhang 2020]

Many of these estimates come from high-incidence settings and observational designs prone to
confounding. It is not known whether such associations are visible at population level in a
low-incidence country.

England publishes monthly prescribing for every general practice in the English Prescribing Dataset
(EPD), and UKHSA publishes TB notifications by area. Linking the two is an attractive, low-cost way
to generate or test hypotheses about medicines and TB. Ecological analyses of this kind are
vulnerable to well-known problems:
- **Confounding** by area characteristics such as country of birth, deprivation and age.
- **Cross-level bias,** which covariate adjustment cannot remove when effects differ between
  population groups.[Greenland & Morgenstern 1989; Morgenstern 1995]
- **Limited power,** which depends on the number of areas rather than the amount of data per
  area.[Sheppard 1996]

Prescribing data also carry specific limitations:
- they cover primary care dispensing only, not hospital-prescribed biologics or in-hospital
  corticosteroids
- practice list sizes are inflated, and the inflation varies with population
  mobility[Hudson 2025; Venkatesan 2025]
- prescribing is itself patterned by deprivation and was disrupted during the COVID-19
  pandemic.[Richards 2025]

We found no previous study linking area-level prescribing to TB incidence. The closest analogues
suggest that drugs with large individual-level effects can produce much weaker population-level
signals. Cross-sectional and within-area associations can even have opposite signs.[Hermans 2015;
Költringer 2023]

We therefore asked whether routinely published English prescribing data can detect known or
hypothesised drug–TB associations at population level. We used three complementary ecological
designs:
- a cross-sectional analysis
- a longitudinal panel with area and time fixed effects, lagged exposures, positive and negative
  control exposures, and a falsification (lead) test[Lipsitch 2010; Prasad & Jena 2013]
- analyses of change in oral corticosteroid prescribing, including TB in UK-born people, which is
  less influenced by migration.[Nguipdop-Djomo 2020]

We then calculated the minimum effects these designs could detect and compared them with the
population effects implied by published individual-level relative risks.
