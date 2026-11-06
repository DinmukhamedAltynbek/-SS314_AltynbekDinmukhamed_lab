# Run from the ROOT of your personal Git repository (the folder that contains gustafson-law-practice/).
# Creates one atomic commit per task. Usage (PowerShell):
#   git checkout -b gustafson-law-practice
#   powershell -ExecutionPolicy Bypass -File .\commit_tasks.ps1
$ErrorActionPreference = "Stop"
$d = "gustafson-law-practice"

function C($msg, [string[]]$files) {
    $existing = $files | ForEach-Object { "$d/$_" } | Where-Object { Test-Path $_ }
    if ($existing.Count -eq 0) { Write-Host "skip: $msg (files not found)"; return }
    git add -- $existing
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) { git commit -m $msg | Out-Null; Write-Host "ok:   $msg" }
    else { Write-Host "skip: $msg (nothing changed)" }
}

C "feat: complete task 01 scaling models summary"          @("theory/task01_scaling_models.md")
C "feat: complete task 02 derivation"                      @("theory/task02_derivation.md")
C "feat: complete task 03 serial invariance memo"          @("theory/task03_serial_invariance.md")
C "feat: complete task 04 asymptotic limits"               @("theory/task04_asymptotic_limits.md")
C "feat: complete task 05 nCUBE historical case"           @("theory/task05_historical_ncube.md")
C "feat: complete task 06 parametric table"                @("calculations/task06_parametric_table.md")
C "feat: complete task 07 tolerable serial fraction"       @("calculations/task07_tolerable_serial.md")
C "feat: complete task 08 Amdahl vs Gustafson divergence"  @("calculations/task08_cross_divergence.md")
C "feat: complete task 09 multi-component workload"        @("calculations/task09_multicomponent.md")
C "feat: complete task 10 memory growth limits"            @("calculations/task10_memory_growth.md")
C "feat: complete task 11 Sun-Ni comparison"               @("theory/task11_sun_ni_comparison.md")
C "feat: complete task 12 communication penalty model"     @("theory/task12_communication_penalty.md")
C "feat: complete task 13 failure cases"                   @("theory/task13_failure_cases.md")
C "feat: complete task 14 isoefficiency proof"             @("theory/task14_isoefficiency.md")
C "feat: complete task 15 energy scaling"                  @("theory/task15_energy_scaling.md")
C "feat: complete task 16 GEMM scaling"                    @("calculations/task16_gemm_scaling.md")
C "feat: complete task 17 stencil surface-to-volume"       @("calculations/task17_stencil_scaling.md")
C "feat: complete task 18 N-body scaling"                  @("analysis/task18_nbody_scaling.md")
C "feat: complete task 19 Monte Carlo analysis"            @("analysis/task19_monte_carlo.md")
C "feat: complete task 20 graph processing essay"          @("analysis/task20_graph_processing.md")
C "feat: complete task 21 speedup simulator"               @("benchmarks/simulator.py","benchmarks/simulator_output.csv","plots/simulator_overlay.png","plots/simulator_overlay.pdf")
C "feat: complete task 22 weak-scaling benchmark suite"    @("benchmarks/weak_scale_bench/bench.py","benchmarks/weak_scale_bench/README.md")
C "feat: complete task 23 data collection and fit"         @("benchmarks/results.csv","benchmarks/fit_gustafson.py","benchmarks/fit_result.json")
C "feat: complete task 24 plots and hardware audit"        @("plots/scaling_comparison.png","plots/scaling_comparison.pdf","analysis/task24_hardware_audit.md")
C "docs: complete task 25 master README"                   @("README.md",".gitignore")
Write-Host "`nDone. Now run: git push -u origin gustafson-law-practice"
