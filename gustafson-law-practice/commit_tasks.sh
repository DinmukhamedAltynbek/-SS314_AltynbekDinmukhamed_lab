#!/usr/bin/env bash
# Run from the ROOT of your Git repo (Git Bash / Linux / macOS):
#   git checkout -b gustafson-law-practice && bash commit_tasks.sh
set -e
d=gustafson-law-practice
c(){ msg="$1"; shift; f=(); for x in "$@"; do [ -e "$d/$x" ] && f+=("$d/$x"); done
  if [ ${#f[@]} -eq 0 ]; then echo "skip: $msg (files not found)"; return; fi
  git add -- "${f[@]}"; if git diff --cached --quiet; then echo "skip: $msg (nothing changed)"; else git commit -q -m "$msg"; echo "ok:   $msg"; fi; }
c "feat: complete task 01 scaling models summary" "theory/task01_scaling_models.md"
c "feat: complete task 02 derivation" "theory/task02_derivation.md"
c "feat: complete task 03 serial invariance memo" "theory/task03_serial_invariance.md"
c "feat: complete task 04 asymptotic limits" "theory/task04_asymptotic_limits.md"
c "feat: complete task 05 nCUBE historical case" "theory/task05_historical_ncube.md"
c "feat: complete task 06 parametric table" "calculations/task06_parametric_table.md"
c "feat: complete task 07 tolerable serial fraction" "calculations/task07_tolerable_serial.md"
c "feat: complete task 08 Amdahl vs Gustafson divergence" "calculations/task08_cross_divergence.md"
c "feat: complete task 09 multi-component workload" "calculations/task09_multicomponent.md"
c "feat: complete task 10 memory growth limits" "calculations/task10_memory_growth.md"
c "feat: complete task 11 Sun-Ni comparison" "theory/task11_sun_ni_comparison.md"
c "feat: complete task 12 communication penalty model" "theory/task12_communication_penalty.md"
c "feat: complete task 13 failure cases" "theory/task13_failure_cases.md"
c "feat: complete task 14 isoefficiency proof" "theory/task14_isoefficiency.md"
c "feat: complete task 15 energy scaling" "theory/task15_energy_scaling.md"
c "feat: complete task 16 GEMM scaling" "calculations/task16_gemm_scaling.md"
c "feat: complete task 17 stencil surface-to-volume" "calculations/task17_stencil_scaling.md"
c "feat: complete task 18 N-body scaling" "analysis/task18_nbody_scaling.md"
c "feat: complete task 19 Monte Carlo analysis" "analysis/task19_monte_carlo.md"
c "feat: complete task 20 graph processing essay" "analysis/task20_graph_processing.md"
c "feat: complete task 21 speedup simulator" "benchmarks/simulator.py" "benchmarks/simulator_output.csv" "plots/simulator_overlay.png" "plots/simulator_overlay.pdf"
c "feat: complete task 22 weak-scaling benchmark suite" "benchmarks/weak_scale_bench/bench.py" "benchmarks/weak_scale_bench/README.md"
c "feat: complete task 23 data collection and fit" "benchmarks/results.csv" "benchmarks/fit_gustafson.py" "benchmarks/fit_result.json"
c "feat: complete task 24 plots and hardware audit" "plots/scaling_comparison.png" "plots/scaling_comparison.pdf" "analysis/task24_hardware_audit.md"
c "docs: complete task 25 master README" "README.md" ".gitignore"
echo; echo "Done. Now run: git push -u origin gustafson-law-practice"
