#!/usr/bin/env bash
# Permutation-based power simulations on the rebuilt panels (hours; two worker processes), then tables.
# Run after run_revision.sh. Each step logs to outputs/logs/<step>.txt.
set -uo pipefail
cd "$(dirname "$0")"
P="$(pwd)/.venv/bin/python"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p outputs/logs

run() {
    local name=$1; shift
    echo "== $(date +%H:%M) $name"
    if "$P" "$@" > "outputs/logs/$name.txt" 2>&1; then echo "   ok"; else echo "   FAILED (see outputs/logs/$name.txt)"; fi
}

run simulate_ltla simulate_power.py ltla 500 300 residence
run simulate_utla simulate_power.py utla 500 300 residence
run make_tables make_tables.py
echo "== $(date +%H:%M) done"
