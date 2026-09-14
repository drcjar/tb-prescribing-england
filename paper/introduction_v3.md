## Introduction

Tuberculosis (TB) remains a public health problem in England.

**Recent trends.**
- **Decline:** notifications fell by 44% between 2011 and 2018 (8,282 to 4,609). For 2011–2015,
  most of the fall reflected declining TB rates in almost all populations, with smaller
  contributions from fewer recent non-EU migrants and from pre-entry screening of long-stay visa
  applicants from high-incidence countries [Thomas 2018; Aldridge 2016].
- **2020:** notifications dropped to 4,123 during the COVID-19 pandemic, a fall thought to reflect
  service disruption rather than less disease [UKHSA 2021; Morrison 2023].
- **2021–2024 rise:** notifications then increased, reaching 5,490 in 2024 (9.4 per 100,000).
  - 81.9% were in people born outside the UK [UKHSA 2025, Supplementary Table 12].
  - 41% of those were notified within five years of arrival [UKHSA 2025].
  - The rise has been attributed mainly to migration from higher-incidence countries [UKHSA 2025].
- **2025:** national data show 5,424 notifications, with 2024 revised to 5,487 [UKHSA 2026].

**TB in UK-born people.** UK-born notifications fell by 48% between 2014 and 2022 (1,756 to 916),
then rose to 995 in 2024, still 43% below 2014 [UKHSA 2025]. UK-born TB is heterogeneous: it
includes reactivation in older adults and transmission linked to social risk factors [Davidson 2018].

**Medicines that change TB risk.** Host factors also modify TB risk, and several are shaped by
commonly prescribed medicines.
- **Oral glucocorticoids:** current use is associated with an odds ratio of about 5 for active TB,
  higher at doses ≥15 mg/day [Jick 2006].
- **Inhaled corticosteroids and conventional DMARDs:** smaller increases [Brassard 2011;
  Castellana 2019; Brassard 2006].
- **Anti-TNF biologics:** TB typically presents within months of starting treatment [Keane 2001].
  Latent infection screening before treatment greatly reduces this risk [BTS 2005; Carmona 2005].
- **Proton pump inhibitors:** associations with increased risk [Song 2019].
- **Statins and metformin:** associations with lower risk [Li 2020; Zhang 2020].

Many of these estimates come from high-incidence settings or designs vulnerable to confounding
by indication and protopathic bias.

**Open data and their problems.** England publishes monthly prescribing for every general
practice, hospital medicines use by NHS trust, and TB notifications by local authority. Linking
these offers a low-cost way to generate or test hypotheses about medicines and TB. Such ecological
analyses face well-known problems:
- confounding by area characteristics;
- cross-level bias, which covariate adjustment cannot remove when effects differ between groups
  [Greenland 1989; Morgenstern 1995];
- limited power, which depends on the number of areas [Sheppard 1996].

The data carry specific problems too:
- practice lists are inflated in ways that track population mobility [Hudson 2025;
  Venkatesan 2025];
- practice locations do not match where patients live;
- prescribing is patterned by deprivation and was disrupted by COVID-19 [Richards 2025];
- hospital-prescribed medicines are recorded separately from primary care [Bacon 2020].

**The gap.** We found no previous study linking area-level prescribing to TB. In analogous
settings, drugs with large individual effects produced weak population signals [Hermans 2015], and
between-area and within-area associations had opposite signs [Költringer 2023].

**This study.** We asked whether open English prescribing data can detect associations between
medicines and TB notifications at population level, and why they might not. We combined:
- cross-sectional and fixed-effects panel designs at two geographic scales;
- primary care prescribing apportioned to where registered patients live;
- hospital medicines apportioned by trust catchment, with a disease-specific positive control;
- negative-control exposures and falsification tests [Lipsitch 2010; Prasad 2013];
- regional analyses of TB in UK-born and older people.

We compared the smallest effects these designs could detect, both analytically and by simulation,
with the population effects implied by published individual-level relative risks and by UKHSA
surveillance records of drug-associated TB.
