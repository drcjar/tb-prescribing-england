# RECORD checklist

RECORD (REporting of studies Conducted using Observational Routinely-collected health Data) extends
STROBE. Items below give where each point is addressed in the manuscript (M), supplementary file (S)
or repository (R). STROBE items not listed are addressed in the corresponding manuscript sections.

| Item | Requirement | Where addressed |
|:---|:---|:---|
| 1.1 (Title/abstract) | Type of data used stated in title or abstract | Title and abstract: prescribing data and TB notifications, England |
| 1.2 | Databases and geographic region named | Abstract, Data sources: NHSBSA prescribing data, Secondary Care Medicines Data, UKHSA TB notifications; England |
| 1.3 | Period and population covered | Abstract, Setting: 2011–2024 primary care; 2019–2024 hospital; 2014–2024 notifications; all English local authorities |
| 6.1 (Participants) | Methods of selecting the population, including codes and algorithms | M Methods (primary care prescribing; hospital medicines); S drug group definitions (table S9) and SCMD classification (R: outputs/hospital/vmp_classification.csv) |
| 6.2 | Validation of selection has been reported | Positive and negative controls (M Methods, Results); consistency of notification counts with Fingertips (r = 0.996) |
| 6.3 | Diagram of population selection | Not applicable: analysis is of all local authorities, with area counts given in Methods |
| 7.1 (Variables) | Classification codes and algorithms for exposures, outcomes and confounders | M Methods; S table S9; R drug_groups.py, hospital_medicines.py |
| 12.1 (Statistical methods) | Data cleaning methods | M Methods (practice restriction, apportionment, complete-case handling); R build_panel.py |
| 12.2 | Linkage methods and quality | M Methods: practice-to-area apportionment by registered patients; trust catchments; S hospital coverage by year (table S7) |
| 12.3 | Sensitivity analyses | M Methods, Results; S tables S1, S2, S2b, S3b |
| 13.1 (Participants) | Detail on the selected population | M Methods and Results: 294 lower-tier and 151 upper-tier authorities; 3,233 area-years |
| 19.1 (Limitations) | Limitations of the data sources and misclassification | M Discussion; strengths and limitations box |
| 22.1 (Accessibility) | How to access data, protocol and code | M Data availability statement; R https://github.com/drcjar/tb-prescribing-england |

**Pre-specification.** The chronology of the analysis, including which elements were specified
before results were seen and which were added afterwards, is described in Methods. A formal
protocol was not registered.
