### Figure (causal diagram). Assumed causal structure for area-level prescribing and TB notifications

Nodes and arrows encode the assumptions behind the panel models. Solid boxes are measured and
adjusted for; dashed boxes are absorbed by fixed effects or unmeasured.

```mermaid
flowchart LR
    subgraph FE["Absorbed by area fixed effects (stable area characteristics)"]
        COB["Long-run country-of-birth / ethnicity mix"]
        DEP["Deprivation"]
        SERV["Service configuration<br/>(TB services, prescribing culture)"]
    end
    subgraph YR["Absorbed by year fixed effects (national shocks)"]
        COVID["COVID-19 disruption"]
        POLICY["National policy<br/>(pre-entry screening, guidance)"]
    end
    subgraph TV["Measured, time-varying: adjusted"]
        AGE["Age structure"]
        MIG["International in-migration"]
        HIV["Diagnosed HIV prevalence"]
        LTBI["LTBI programme for new migrants"]
        ASY["Asylum support (sensitivity)"]
    end
    DM["Diabetes prevalence<br/>(adjusted except for metformin/insulin)"]
    SRF["Social risk factors, diagnostic intensity,<br/>recent-arrival share (unmeasured)"]
    RX(["Prescribing in year t−1<br/>(exposure)"])
    TB(["TB notifications in year t<br/>(outcome)"])
    PRO["Prodromal/undiagnosed TB<br/>(protopathic prescribing in year t)"]

    COB --> RX & TB
    DEP --> RX & TB
    SERV --> RX & TB
    COVID --> RX & TB
    POLICY --> TB
    AGE --> RX & TB
    MIG --> RX & TB
    HIV --> TB
    LTBI --> TB
    ASY --> TB
    DM --> RX
    DM --> TB
    SRF -.-> RX
    SRF -.-> TB
    RX -->|"hypothesised effect"| TB
    TB --> PRO --> RX

    classDef unmeasured stroke-dasharray: 5 5;
    class SRF,PRO unmeasured;
```

**Legend.**
- **Fixed effects.** Area fixed effects remove confounding by stable area characteristics without
  measuring them. Year fixed effects remove national shocks.
- **Diabetes prevalence.** It confounds most drug groups, but for metformin and insulin it lies on
  the pathway from diagnosis to prescribing. It is therefore not adjusted for in those models.
- **Total prescribing volume.** It is not adjusted for. It shares a component with each drug group
  and produced spurious associations, including for the negative-control exposure.
- **Protopathic bias.** Prescribing for undiagnosed TB (e.g. glucocorticoids or antibacterials for
  respiratory symptoms) creates reverse arrows in the same year. For this reason the primary exposure
  is year t−1.
- **Unmeasured confounders.** Social risk factors, diagnostic intensity and the changing share of
  recent arrivals may confound within-area changes. We assess this with:
  - negative-control exposures (levothyroxine; hospital low-TB-risk biologics and levetiracetam);
  - falsification tests (prescribing in year t+1);
  - area-specific trends.
- **Cross-level bias.** Effects and baseline risks that differ between people within an area (e.g.
  older UK-born steroid users vs younger non-UK-born people with TB) cannot be represented in, or
  removed by, an area-level model.
