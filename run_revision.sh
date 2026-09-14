#!/usr/bin/env bash
# Re-run the full revised analysis (after peer review round 1) once all practice-month extracts exist.
# Steps run one at a time to keep memory use low; each step logs to outputs/logs/<step>.txt.
set -uo pipefail
cd "$(dirname "$0")"
P="$(pwd)/.venv/bin/python"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
mkdir -p outputs/logs

run() {
    local name=$1; shift
    echo "== $(date +%H:%M) $name"
    if "$P" "$@" > "outputs/logs/$name.txt" 2>&1; then echo "   ok"; else echo "   FAILED (see outputs/logs/$name.txt)"; fi
}

run build_tb_annual build_tb_annual.py
for spec in "ltla residence" "utla residence" "ltla postcode" "utla postcode"; do
    set -- $spec
    run "build_panel_$1_$2" build_panel.py "$1" "$2"
done
run build_ltbi_covariate build_ltbi_covariate.py

for spec in "ltla residence" "utla residence" "ltla postcode" "utla postcode"; do
    set -- $spec
    run "analyze_$1_$2" analyze_panel_annual.py "$1" "$2"
    run "plot_panel_$1_$2" plot_panel.py "$1" "$2"
done

run mde mde.py
run plot_variation plot_variation.py
run spatial spatial_autocorrelation.py
run steroid_trends steroid_trends.py
run steroid_regional steroid_ukborn_regional.py
run hospital_utla hospital_medicines.py utla
run hospital_ltla hospital_medicines.py ltla
run plot_hospital plot_hospital.py

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
run simulate_ltla simulate_power.py ltla 500 300 residence
run simulate_utla simulate_power.py utla 500 300 residence

run make_tables make_tables.py
echo "== $(date +%H:%M) done"
