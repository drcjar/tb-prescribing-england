# Additional data sources (checked 2026-09-14)

## A. Practice-level prescribing before 2014 (HSCIC PDPI) — verified, feasible

- **Where:** data.gov.uk package `176ae264-2484-4afe-a297-d51798eb8228` ("GP practice prescribing data – Presentation level"). Files are hosted on `files.digital.nhs.uk`. All 41 months from Aug 2010 to Dec 2013 are listed and returned HTTP 200. Inventory with URLs and byte sizes: `data/raw/pre2014/pre2014_file_inventory.csv`.
- **Files per month:** `T{yyyymm}PDPI BNFT.CSV` (~1.4 GB), `ADDR BNFT` (~1.7 MB), `CHEM SUBS` (~0.3 MB), plus a monthly zip (~250 MB) holding all three. Oct 2011, Jun 2012 and Mar 2013 have no zip.
- **No chemical-level summary exists.** The CHEM file is only a code-to-name lookup, so the PDPI files have to be downloaded.
- **Total size:** PDPI CSVs 57.0 GB. The zip route is 9.5 GB, plus ~4.2 GB of CSVs for the 3 months with no zip, so **~13.7 GB**. Measured speed was 8.7 MB/s, so about 30 min in total.
- **Jan 2012 downloaded** to `data/raw/pre2014/` (PDPI, ADDR, CHEM):
  - PDPI columns: `SHA, PCT, PRACTICE, BNF CODE, BNF NAME, ITEMS, NIC, ACT COST, QUANTITY, PERIOD`. Fields are space-padded with a trailing empty column. 9,930,772 rows, 10,134 practices, 78.9M items.
  - ADDR has no header: `PERIOD, PRACTICE, name, addr1–4, postcode`. It covers all 10,134 practices, with postcodes.
- **Pilot item counts, Jan 2012:**

  | Group | BNF prefix | Items |
  |---|---|---|
  | Oral corticosteroids | 0603020 | 615k |
  | Inhaled corticosteroids | 0302000 | 1.47M |
  | Anti-TB | 0501090 | 4.6k |
  | PPI | 0103050 | 3.73M |
  | Statins ("statin" in name) | 0212000 | 4.71M |
  | Levothyroxine | 0602010V0 | 2.10M |
  | Metformin | 0601022B0 | 1.31M |

- **Code corrections:**
  - **Levothyroxine is `0602010V0`, not `0601010H0`.**
  - Metformin `0601022B0` is confirmed.
  - `0603020` includes injectable glucocorticoids.
  - `0103050A0` is the *H. pylori* eradication pack.
  - `0212000` also contains non-statin drugs, hence the name filter.
- **Script (not run in full):** `fetch_pre2014_practice.py`. It works one month at a time: download, aggregate per practice-month (total items plus the 7 groups, with postcode), then delete the raw file. Peak disk use is ~1.7 GB.
- **Still needed:** postcode→LAD mapping (NSPL), practice list sizes before 2013, and a check on 2010–13 PCT→LA changes.

## B. NHS LTBI testing and treatment programme — partial, verified

- **Source:** UKHSA, "Latent tuberculosis testing and treatment programme for migrants", 2020 report and data tables (FY2015/16–2019/20). https://www.gov.uk/government/publications/latent-tuberculosis-testing-and-treatment-programme-for-migrants. Saved to `data/raw/ltbi/` (xlsx + pdf).
- **What it covers:**
  - IGRA tests submitted, tests with a confirmed result, and positives, by CCG, 2015/16–2019/20 (50 CCG rows plus an England total).
  - Treatment referral and completion cohorts, 2017/18–2019/20.
  - Tests by country of birth.
- **Tidy output:** `data/raw/ltbi/ltbi_programme_area_year.csv` (255 rows). Columns:
  - `area_code` (blank: the source has names only)
  - `area_name`, `geography_type`, `year`, `fy_start_year`
  - `tests_submitted`, `tests_confirmed`, `ltbi_positive`
  - `cohort_should_refer`, `referred_treatment`, `cohort_should_complete`, `completed_treatment`
  - `programme_active` (my derived flag: ≥20 tests in the year)
  - `programme_first_active_fy_start`, `notes`
- **England totals (tests):** 2,858 (15/16), 10,871, 14,770, 17,104, 22,221 (19/20).
- **First active year:** 8 CCGs in 2015/16 (Newham, Bradford, Leeds, Manchester, Blackburn/E Lancs, Greenwich, Greater Huddersfield, N Kirklees), 19 in 2016/17, 9 in 2017/18, 10 in 2018/19, 2 in 2019/20.
- **Caveats:**
  - Several rows are joint submissions: Blackburn + East Lancashire; Bradford City + Districts; Barnet/Camden/Islington/Haringey under "Haringey".
  - Some names are truncated in the source.
  - Low positivity in a few small cells (e.g. Stoke 2016/17 at 97%) suggests data-quality problems.
- **Needed:** CCG name→ODS code→LA mapping (ONS CCG-to-LAD lookups, April 2019/2020). CCGs are mostly coterminous with one or more LAs.
- **Not found (unverified):** any area-level LTBI data after 2019/20. Later figures appear only as national totals in the "TB in England" annual reports. No official list of CCG start dates was found. Programme years before 2015 don't apply.

## C. LA covariates

| Covariate | Source / URL | Years | Geography | Local file(s) |
|---|---|---|---|---|
| **Asylum seekers on Home Office support** | Immigration system statistics, Asy_D11 (https://www.gov.uk/government/statistical-data-sets/immigration-system-statistics-data-tables) | 2014 Q1–2026 Q2, quarter-end stock | LAD (UK) | `covariates/support-local-authority-datasets-jun-2026.xlsx`; `asylum_support_by_la_2014q1_2026q2_long.csv` (date, support_type [s95/s4/s98], region, local_authority, lad_code, accommodation_type, people); `asylum_support_england_lad_year.csv` (lad_code, local_authority, year, people_mean_quarter_end, n_quarters, people_31dec) |
| **Homelessness (statutory)** | MHCLG live tables (https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness) | P1E quarterly 2009–2017 (acceptances, temporary accommodation); H-CLIC annual FY2018/19–2024/25 (tables A1 duties owed, TA1) | LA (lower tier) | `covariates/homelessness/` holds the P1E 2009–16 zip (extracted), FY 16/17, 17/18 xlsx, FY 18/19–24/25 ods, and the England time series. **Not harmonised:** the HRA 2018 break changes definitions. |
| Homelessness (tidy, 2019/20+) | Fingertips 93735 (temporary accommodation per 1,000), 93736 (owed HRA duty) | 2019/20– | LTLA 501, UTLA 502 | `covariates/fingertips_drugs_homeless_{ltla501,utla502}.csv` |
| **Opiate/crack use (OCU) prevalence** | OHID estimates (https://www.gov.uk/government/publications/opiate-and-crack-cocaine-use-prevalence-estimates, and the 2022–23 release); Fingertips 91117 | 2011/12, 2014/15, 2016/17, 2018/19*, 2019/20, 2022/23 (*gov.uk only) | UTLA; ages 15–64, rate per 1,000 with CI | `covariates/drugs/*.ods` (Table_1 = OCU/opiate/crack counts and rates); Fingertips UTLA file |
| Drug treatment | Fingertips 90244/90245 (successful completion, opiate/non-opiate); OHID adult substance misuse treatment statistics (national); NDTMS (https://www.ndtms.net) for LA numbers in treatment | 2010/11– | UTLA | Fingertips UTLA file. LA counts in treatment are on NDTMS; not downloaded or verified. |
| Prisons (optional, unverified) | MoJ Offender Management Statistics, prison population by establishment (monthly/quarterly), https://www.gov.uk/government/collections/prison-population-statistics | 2011– | Establishment; needs geocoding to LAD | not downloaded |

**Notes:**
- Asylum support is in LAD codes as issued, so pre-2019/2021 LAD mergers need recoding.
- Before 2018, Section 4 support is not split by LA ("N/A – Section 4").
- In late 2022–23, Section 98 contingency hotels cause a big jump in the data (England 31 Dec: 51k in 2021, 98k in 2022).
