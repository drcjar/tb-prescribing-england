#!/usr/bin/env bash
# Re-run the full revised analysis (after peer review round 1) once all practice-month extracts exist.
# Steps run one at a time to keep memory use low; each step logs to outputs/logs/<step>.txt.
set -uo pipefail
cd "$(dirname "$0")"
P="$(pwd)/.venv/bin/python"
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
mkdir -p outputs/logs

# FROM=<step name> resumes at that step; each step is capped at MEM_KB of virtual memory (default 16 GB)
# so that a runaway step fails on its own rather than exhausting the machine; peak RSS is logged.
FROM="${FROM:-}"
MEM_KB="${MEM_KB:-16000000}"
run() {
    local name=$1; shift
    if [ -n "$FROM" ]; then
        if [ "$name" != "$FROM" ]; then echo "== skip $name"; return; fi
        FROM=""
    fi
    echo "== $(date +%H:%M) $name"
    if ( ulimit -v "$MEM_KB"; /usr/bin/time -f "peak RSS %M KB" -o "outputs/logs/$name.mem" "$P" "$@" > "outputs/logs/$name.txt" 2>&1 ); then
        echo "   ok ($(cat "outputs/logs/$name.mem"))"
    else
        echo "   FAILED (see outputs/logs/$name.txt)"
    fi
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

# power simulations take hours; they run separately afterwards (run_simulations.sh)
run make_tables make_tables.py
echo "== $(date +%H:%M) done"
