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
