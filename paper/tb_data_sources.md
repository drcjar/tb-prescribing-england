# UK tuberculosis incidence / notification data sources

Checked 2026-09-14. "Verified" means the URL returned HTTP 200 or the file was downloaded and opened. Anything not verified is marked **[unverified]**. Files downloaded to `data/raw/tb_sources/`.

## Ranked summary (usefulness for an annual, sub-national panel stratified by country of birth)

| Rank | Source (publisher) | Geography | Time | Years | Stratification | Format / access | Key caveats |
|---|---|---|---|---|---|---|---|
| 1 | **UKHSA TB regional reports 2024: supplementary data** (9 regional workbooks) | UKHSA region; **annual counts by LTLA (294 areas) and UTLA**, plus ICB | Annual | 2001-2024 | Region-level: UK-born vs non-UK-born (T8); **UK/non-UK x 4 age bands, by year** (T9); ethnicity x birthplace by year (T13, some regions); children under 18 by birthplace. LA-level: **totals only** | XLSX, open. [page](https://www.gov.uk/government/publications/tuberculosis-tb-regional-reports-2024-supplementary-data) | LA tables give counts only (no birthplace split); rates tables are separate. Sheet numbers differ by region. LTLA sums run slightly above national ST5 (2024: 5,539 vs 5,490; 2001: 6,291 vs 6,171), presumably from a different extract date or residence assignment. No suppression markers seen. |
| 2 | **Tuberculosis in England 2025 report** (data to 2024), supplementary tables ch.1 (UKHSA) | England; UKHSA region; NHS region; ICB / sub-ICB / UTLA / LTLA as **3-yr average only** | Annual (region); 3-yr (local) | 2000-2024 | **ST12/12.5: UKHSA region x UK/non-UK born, annual counts + LFS/APS denominators + rates**; ST9: England by birthplace; ST10/11: age x birthplace x sex (England, 2024 only); ST18: ethnicity x birthplace (England); ST22: social risk factors by region 2018-24; ST26: IMD | XLSX, open. [page](https://www.gov.uk/government/publications/tuberculosis-in-england-2025-report) | No age x birthplace x region (see #1 T9). Local tables are 3-yr averages, as in Fingertips. The 2024 report (2023 data) has the same structure (ST12 = region x birthplace, 2000-2023). |
| 3 | **Cases of TB reported to enhanced TB surveillance systems: UK, 2000 to 2025** (UKHSA official statistics) | UK countries; England UKHSA region / UTLA / LTLA (3-yr avg, T3) | Annual (country); 3-yr (local) | 2000-2025 | Culture confirmation, drug resistance, treatment outcome by country | ODS, open. [page](https://www.gov.uk/government/statistics/reports-of-cases-of-tb-to-uk-enhanced-tuberculosis-surveillance-systems-2000-to-2025) | Most recent year (2025, provisional-ish). No birthplace split sub-nationally. |
| 4 | **NOIDs annual report 2021** (UKHSA) | UKHSA region + **local/unitary authority (348 area rows, England and Wales)** | Annual | **2021 only** on gov.uk | Separate tables by region x sex and disease x age (not LA) | XLS, open. [page](https://www.gov.uk/government/publications/notifiable-diseases-annual-report) | Clinical notifications, not ETS cases. Only 2021 is still hosted; I could not retrieve older annual files (2013-2020) from the web archive **[unverified]**. Historic national totals 1912-2021 are in a separate file. |
| 5 | **NOIDs weekly reports** (UKHSA) | England & Wales -> region -> county -> **local/unitary authority** | Weekly | Yearly pages for 2015/16-2025 | None (TB excludes chemoprophylaxis) | PDF (Table 2), open. [2025](https://www.gov.uk/government/publications/notifiable-diseases-weekly-reports-for-2025) | Would need PDF scraping of about 52 files a year to build annual LA counts. Reports paused and reinstated wk44 2024 with LA remapping; UKHSA says post-wk27 2024 data are not comparable with earlier reports. 2025 page last updated wk13. |
| 6 | **Fingertips TB Strategy Monitoring Indicators** (OHID/UKHSA API) | 91361: Sub-ICB (66), UTLA/LTLA (202-502), GOR (6), England; 91359: GOR/England only | 3-yr / annual (region) | 2001-03 to 2022-24 | None (other indicators: culture confirmation, DST, outcomes, HIV test, treatment delay, drug resistance; mostly ICB (221)/UTLA) | API, open | **No TB indicator by country of birth at any level.** 12 TB indicators in total: 91359, 91361, 91365-69, 91373-75, 91450-51. |
| 7 | **Enhanced TB Surveillance (ETS) / NTBS individual-level extract** via UKHSA data access (formerly PHE Office for Data Release, ODR) | Postcode-derived: LSOA/LTLA/UTLA etc. | Case date | 2000- (NTBS from 2021) | Full: country of birth, year of entry, age, sex, ethnicity, site, social risk factors, drug resistance, HIV, outcomes | Application form + approval standards (GDPR basis, data security, lay summary). [page](https://www.gov.uk/government/publications/accessing-ukhsa-protected-data). Approvals register: [xlsx](https://assets.publishing.service.gov.uk/media/67e2eb1ddcd2d93561195baa/UKHSA-data-access-approvals-register-1-january-2022-to-31-december-2024.xlsx) | Months to approve. Old ODR form withdrawn. Aggregate LA x birthplace x year tables with small-number suppression might be a lighter-weight request **[unverified that UKHSA would supply]**. |
| 8 | **Scotland: PHS national quarterly TB reports + annual report** | Scotland; NHS board (14) in quarterly report narrative | Quarterly / annual | Quarterly 2019-2025; annual reports (e.g. 2022) | Sex, site (quarterly); annual adds age, UK vs non-UK birth, SIMD, drug resistance (national) | PDF, open. [quarterly Q4 2024](https://publichealthscotland.scot/publications/national-quarterly-report-of-tuberculosis-in-scotland/national-quarterly-report-of-tuberculosis-in-scotland-quarter-4-2024/), [annual](https://www.publichealthscotland.scot/publications/tuberculosis-annual-report-for-scotland/) | Small numbers (270 cases in 2024). No board x birthplace table found. |
| 9 | **Wales: PHW "Tuberculosis in Wales" annual report (data to 2024)** | Wales; health board; local authority (5-yr average) | Annual | reports for 2022-2024 data | Age, ethnicity, drug resistance, outcomes by HB | PDF. [page](https://phw.nhs.wales/publications/publications1/tb-in-wales-annual-report-data-to-end-2024/) **[unverified: bot-blocked (404 to curl); contents from search snippets]** | About 95 cases a year. |
| 10 | **Northern Ireland: PHA TB surveillance report 2025 (data to 2024)** | NI; **Local Government District, annual rates 2018-2024 (Table 1)**; HSC Trust | Annual | 2018-2024 (LGD) | Age, sex, born outside UK & Ireland, social risk factors, site, drug resistance (NI level) | PDF, open. [pdf](https://www.publichealth.hscni.net/sites/default/files/2025-08/Tuberculosis%20(TB)%20Surveillance%20Report%202025.pdf) | About 86 cases a year. |
| 11 | **Hospital admissions with TB (HES APC, ICD-10 A15-A19)** (NHS England) | Published: England, by provider; LA of residence only via DARS extract | Financial year | 1998/99- | Age, sex | XLSX (national diagnosis tables, open) [page](https://digital.nhs.uk/data-and-information/publications/statistical/hospital-admitted-patient-care-activity); LA-level needs a DARS application **[unverified for a TB-specific LA table]** | Measures admissions, not incidence. Small numbers need suppression. |
| 12 | **TB deaths (ONS mortality, A15-A19)** | National: NHS Digital compendium (by age, [page](https://digital.nhs.uk/data-and-information/publications/statistical/compendium-mortality/current/mortality-from-infectious-diseases/mortality-from-tuberculosis-number-by-age-group-annual-mfp)). LA-level only via ONS ad hoc request (Health.Data@ons.gov.uk) | Annual | long series | Age, sex | Open (national) / paid bespoke (LA) | About 200-300 deaths a year; underlying cause under-records TB (Lipman/UKHSA IJTLD 2018). |
| 13 | **UKHSA national quarterly TB reports (provisional)** | England + 9 UKHSA regions | Quarterly (rolling) | 2019- | UK/non-UK born, site, drug resistance, social risk factors | HTML, open. [collection](https://www.gov.uk/government/statistics/tuberculosis-in-england-national-quarterly-reports) | Provisional; no LA geography. |
| 14 | **WHO Global TB Programme / ECDC Surveillance Atlas** | UK national only | Annual | 1980s/2000- | Age, sex, origin, site, resistance | Open. [WHO](https://www.who.int/teams/global-programme-on-tuberculosis-and-lung-health/data), [ECDC atlas](https://atlas.ecdc.europa.eu/public/index.aspx) | National only; UK left ECDC reporting after 2020 **[unverified]**. |

Other checks:
- **TB Trends UK** (tbtrends.uk) is a third-party browser for the TB in England 2025 report. It was blocked by the local network proxy, so its content and provenance are **[unverified]**.
- **CPRD-ETS or HES-ETS linkage:** I found no published CPRD-ETS linkage, and CPRD does not appear to offer ETS as a standard linked dataset **[unverified: CPRD site blocked by Cloudflare]**. CPRD TB studies use GP-coded TB (e.g. PMID 26048371, 32998703). "Million Migrants" (PMID 30801036) links migrant records with HES, not ETS. Hospital data (HES) is routinely matched into ETS/NTBS internally at UKHSA, but that match is not a released product.

## Files downloaded (`data/raw/tb_sources/`)

**`regional_2024/<Region>-TB-report-2024-supplementary-data-tables.xlsx`** (9 files)
- **Table 8 (region by place of birth):** long format, columns `Year | Place of birth | Number of TB notifications`. Values are `UK-born` / `Non UK-born`; 2001-2024; 48 rows.
- **Table 9 (region by place of birth and age):** long format, columns `Year | Age group (years) | Place of birth | Number of TB notifications`. Age groups are 0-14, 15-44, 45-64 and 65+; place of birth is UK born / Non-UK born / All; 2001-2024; 288 rows.
- **LTLA and UTLA count tables:** wide format, one column per year 2001-2024; header row at index 2.
  - LTLA sheets: EM T32, EoE T34, London T35, NE T31, NW T35, SE T35, SW T34, WM T32, Y&H T32.
  - UTLA sheets: EM T36, EoE T38, London T39, NE T35, NW T39, SE T39, SW T38, WM T36, Y&H T36.
  - LTLA area rows per region: EM 35, EoE 46, London 32, NE 12, NW 35, SE 63, SW 26, WM 30, YH 15, giving 294 in total.
- **Other tables:** ICB tables are next to the LA tables. There are matching rates tables (London T36 = LTLA rates).

**`TB-in-England-2025-report-supplementary-data-tables-1-incidence-and-epidemiology.xlsx`**
- **Supplementary_Table_12 (region x UK/non-UK born):** header row 3. Columns are `Year`, then for each UKHSA region and birthplace group (UK born / Non-UK born): LFS population, number of notifications, rate per 100,000, lower CI, upper CI.
  - 9 regions x 2 groups x 5 columns = 90 columns plus Year.
  - Years 2000-2024.
- **Supplementary_Table_12.5:** the same layout with APS denominators, 2004-2024.
- **Other tables:** ST4 (NHS region annual), ST5 (UKHSA region annual, 2001-24), ST8 (3-yr LA).

**`Tuberculosis-in-England-2023-incidence-and-epidemiology.xlsx`** (2024 report; ST12 = region x birthplace 2000-2023)

**`cases-of-tuberculosis-reported-to-enhanced-TB-surveillance-systems-England-2025-supplementary-data-tables.ods`**

**`London-TB-report-2023-supplementary-data-tables.xlsx`** (2001-2023 borough tables)

**`NOIDS_Annual_Report_2021_Final.xls`**
- Sheet "Table 1 PHE Region & LA": header row 5; columns are `Region/Area` plus 29 disease columns (including `Tuberculosis`) and `Grand Total`.
- Rows: 11 region header rows in upper case (including WALES and PORT HEALTH AUTHORITY) and 348 area rows (English local/unitary authorities plus Welsh LAs).
- TB is non-missing in 323 area rows. Area rows sum to 4,787, which matches the E&W grand total (London 1,654; Wales 92).
- Other sheets: diseases A-K and L-Z by LA, region x sex, disease x age.
- Year: 2021 only.

**`NOIDS_Annual_Totals_2021_Final.xls`** (England & Wales national TB notification totals, 1982-2021)

## Recommendations

- **Use the 2024 regional supplementary workbooks as the main panel.** They give annual LTLA and UTLA TB counts for 2001-2024 across all of England (294 LTLAs, 24 years), which removes the 3-yr-average limitation. Harmonise names to current LAD codes and use ONS mid-year estimates as denominators.
- **For UK-born incidence, work at region x year level.**
  - Report ST12/12.5 gives counts plus LFS/APS UK-born denominators for 9 regions, 2000-2024.
  - Regional Table 9 adds UK-born counts x 4 age bands x year. Pair it with ONS/APS population by country of birth x age x region for age-specific rates.
  - That is 9 regions x 24 years (216 region-years), stratifiable by age, which suits an ecological comparison with oral corticosteroid trends.
- **For LA x country of birth x year, request aggregate tables or an ETS/NTBS extract through UKHSA data access.** No public source gives birthplace below region. Consider asking first for suppressed aggregate tables, e.g. UTLA x year x UK/non-UK x broad age, which may be quicker than record-level data.
- **Use NOIDs only for sensitivity or validation.** The 2021 annual LA file and the weekly LA PDFs measure clinical notifications, which differ from ETS cases, and there is a 2024 geography/processing break. NOIDs does not fill the birthplace gap.
- **Be careful pooling across the devolved nations or using HES/ONS.** Devolved data are PDF-only with very small counts (Wales about 95/yr, NI about 86/yr, Scotland about 270/yr). HES admissions and ONS deaths at LA level need DARS/ONS bespoke requests and measure different outcomes.
