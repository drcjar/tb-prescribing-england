# Prescribing and tuberculosis in England

Code and manuscript for an ecological study that asks whether openly published English prescribing
data can detect the effects of medicines on tuberculosis (TB) incidence. The draft manuscript is in
[`paper/manuscript.md`](paper/manuscript.md), with rendered versions in `paper/manuscript.pdf` and
`paper/manuscript.docx`.

All inputs are public, aggregate data. Raw downloads (~300 MB) are not committed; the scripts fetch
them into `data/raw/`. Processed analysis datasets are in `data/processed/` and results in `outputs/`.

## Data sources

**Prescribing**
- NHSBSA English Prescribing Dataset (EPD), practice-level monthly items, 2014–2024 plus June 2026.
  Aggregated server-side through the NHSBSA Open Data Portal SQL API.

**TB**
- UKHSA TB regional reports 2024, supplementary tables: annual TB notifications by upper- and
  lower-tier local authority, 2001–2024.
- UKHSA *TB in England 2025*, Supplementary Table 12: region × UK-born/non-UK-born, by year.
- UKHSA Fingertips TB Strategy Monitoring Indicators: three-year incidence by Sub-ICB and local
  authority.

**Population and covariates**
- ONS mid-year population estimates (Nomis) and ONS components of population change (international
  in-migration).
- Census 2021 country of birth.
- English Indices of Deprivation 2025.
- Fingertips HIV and QOF diabetes prevalence.

**Geography lookups**
- ONS Postcode Directory, ONS geography lookups, and NHS ODS practice file (epraccur).

## Pipeline

Run the scripts in this order. Python ≥3.12; install dependencies with `pip install -r requirements.txt`.

Revised pipeline after peer review, round 1 (primary analyses):

| Step | Script | Output |
|---|---|---|
| Drug group definitions (presentation level) | `drug_groups.py` | — |
| Practice-month prescribing, 2014–2024 (NHSBSA EPD, SQL via POST) | `fetch_prescribing_panel.py` | `data/raw/epd_practice_monthly_v2/` |
| Practice-month prescribing, 2010–2013 (HSCIC PDPI) | `fetch_pre2014_practice.py` | `data/raw/epd_practice_monthly_v2/` |
| Practice → LAD shares by patient residence (NHS Digital LSOA registrations) | `build_practice_lad_shares.py` | `data/processed/practice_lad23_shares.csv` |
| Annual TB counts | `build_tb_annual.py` | `data/processed/*_tb_annual.csv` |
| Annual panels (postcode or residence apportionment) | `build_panel.py utla|ltla [postcode|residence]` | `data/processed/*_panel_annual*.csv` |
| Latent TB programme covariate | `build_ltbi_covariate.py` | `data/processed/ltbi_programme_*.csv` |
| Annual panel models | `analyze_panel_annual.py utla|ltla [postcode|residence]`, `plot_panel.py` | `outputs/panel_annual_*/` |
| MDE and expected-effect benchmarks | `mde.py` | `outputs/mde/` |
| Permutation-based power | `simulate_power.py utla|ltla` | `outputs/power_simulation/` |
| Spatial dependence by year | `spatial_autocorrelation.py` | `outputs/spatial/` |
| Hospital medicines: extraction, classification, analysis | `fetch_scmd.py`, `fetch_scmd_negative_control.py`, `build_scmd_classification.py`, `hospital_medicines.py`, `plot_hospital.py` | `outputs/hospital/` |
| Oral glucocorticoid trends and regional analyses | `steroid_trends.py`, `steroid_ukborn_regional.py` | `outputs/steroids/` |

First-pass pipeline (draft 1–2; retained for transparency):

| Step | Script | Output |
|---|---|---|
| Cross-sectional dataset (Sub-ICB, June 2026) | `build_dataset.py` | `data/processed/sicbl26_analysis.csv` |
| Cross-sectional models | `analyze.py`, `plot_results.py` | `outputs/` |
| Practice-month prescribing extraction, 2014–2024 | `fetch_prescribing_panel.py` | `data/raw/epd_practice_monthly/` |
| Oral corticosteroid extraction (substance, prednisolone mg) | `fetch_steroids.py` | `data/raw/epd_steroids_monthly/` |
| Annual local authority panels | `build_panel.py utla` / `build_panel.py ltla` | `data/processed/*_panel_annual.csv` |
| Annual TB counts (UTLA, LTLA, region × birthplace) | `build_tb_annual.py` | `data/processed/*_tb_annual.csv` |
| Rolling three-year panel models | `analyze_panel.py`, `plot_panel.py rolling` | `outputs/panel/` |
| Annual panel models | `analyze_panel_annual.py utla|ltla`, `plot_panel.py annual` | `outputs/panel_annual*/` |
| Minimum detectable effects | `mde.py` (inputs `paper/mde_inputs.csv`) | `outputs/mde/` |
| Simulation-based power | `simulate_power.py utla|ltla [n_sims]` | `outputs/power_simulation/` |
| Steroid trends and change analyses | `steroid_trends.py`, `steroid_ukborn_regional.py` | `outputs/steroids/` |
| Manuscript | `paper/build_paper.sh` (pandoc, xelatex) | `paper/manuscript.*` |

Some raw files were downloaded manually or by one-off commands; the documented source links are in
`paper/tb_data_sources.md` and the script docstrings.

## Main result

Prescribing–TB associations were null within areas over time. The designs are underpowered by an
order of magnitude or more for effects implied by published individual-level relative risks. The
paper therefore argues that causal questions about medicines and TB need individual-level linked
data.

## Journal submission package (BMJ Open)

`paper/submission/` holds a version targeted at BMJ Open, condensed from the full manuscript:

| File | Contents |
|---|---|
| `title_page.md` | Title, authors, word counts, and the required statements (ethics, PPI, data availability, funding, competing interests, contributions) |
| `abstract.md` | Structured abstract (<= 300 words) and the "Strengths and limitations of this study" box |
| `introduction.md`, `methods.md`, `results.md`, `discussion.md` | Main text as prose, about 3,450 words |
| `cover_letter.md` | Draft cover letter |
| `record_checklist.md` | RECORD checklist with pointers to where each item is addressed |
| `assemble_submission.py` | Builds `build/manuscript_bmjopen.docx` and `build/supplementary_bmjopen.docx`, renumbering `[Author Year]` citations into Vancouver style |

Main paper: figures 1-4 and tables 1-2. Everything else (hospital results, sensitivity analyses,
power simulation, regional models, coverage, original design, drug definitions) is supplementary.
The full-length manuscript remains at `paper/manuscript.md`.

## Hypothesis-free prescribing and disease scan (October 2026)

The tuberculosis analysis asked whether one disease could be linked to a handful of drug groups.
It could not, and the more useful question turned out to be the general one: can these data
support any claim that a medicine affects a disease? That scan is the current work, and the
tuberculosis analysis is now a worked example inside it (`paper_scan/`).

| Script | Does |
|---|---|
| `fetch_prescribing_wide.py` | practice x month x BNF section (194 sections), 2014-2024 |
| `fetch_fingertips_wide.py` | all indicators published for upper- and lower-tier local authorities |
| `fetch_fingertips_practice.py` | all 197 indicators published for GP practices |
| `build_wide_exposure.py` / `build_practice_exposure.py` | area and practice exposure panels |
| `build_wide_outcomes.py` / `build_practice_outcomes.py` | outcome panels and catalogues |
| `scan_prescribing_outcomes.py` / `scan_practice.py` | the scans, with lead as empirical null |
| `scan_practice_lags.py` | robustness to lag length and to practice case-mix |
| `analyse_scan.py`, `scan_figures.py` | calibration, figures and tables |

Large intermediate panels (`data/processed/*_outcomes_long.csv*`,
`practice_section_exposure.csv.gz`) exceed GitHub's file size limit and are gitignored; rebuild
them with the build scripts above.

**Status of the tuberculosis manuscript.** `paper/` holds the completed standalone TB paper
(draft 5, three rounds of review, BMJ Open submission package in `paper/submission/`). It is
superseded by `paper_scan/`, which makes the same argument more generally with TB as its worked
example. It is kept for the record and because its supplement is the detailed case study.
