# Gustafson's Law — Practice Repository

Parallel Computing practice task sheet (Instructor: Sufyan bin Uzayr). The repository covers Tasks 01–25: theory, calculations, benchmarks and analysis of **weak scaling (Gustafson)** compared with **strong scaling (Amdahl)**.

## Table of Contents

1. [Core rules](#1-core-rules)
2. [Repository index](#2-repository-index)
3. [How to run](#3-how-to-run)
4. [Key findings](#4-key-findings)
5. [When to design for weak scaling](#5-when-to-design-for-weak-scaling)

---

## 1. Core rules

| Law | Formula | Constant | Limit P → ∞ |
|---|---|---|---|
| Amdahl (strong) | `S = 1 / (s + (1 − s)/P)` | problem size | `S → 1/s`, `E → 0` |
| Gustafson (weak) | `S = P − α(P − 1) = s + p·P` | run time | `S → ∞`, `E → 1 − α` |
| Efficiency | `E = S/P = 1 − α(P − 1)/P` | | |
| Sun–Ni | `S = (s + (1 − s)G) / (s + (1 − s)G/P)` | memory | `G = 1` → Amdahl, `G = P` → Gustafson |
| With communication | `S = S_G / (1 + C(P))` | | depends on C(P) |
| Serial fractions | `f = α / (α + (1 − α)P)` | | links the two laws |

## 2. Repository index

### theory/
| Task | File | Topic |
|---|---|---|
| 01 | [task01_scaling_models.md](theory/task01_scaling_models.md) | Strong vs weak scaling |
| 02 | [task02_derivation.md](theory/task02_derivation.md) | Derivation of `S = P − α(P − 1)` |
| 03 | [task03_serial_invariance.md](theory/task03_serial_invariance.md) | Serial fraction frames, proof that both laws agree |
| 04 | [task04_asymptotic_limits.md](theory/task04_asymptotic_limits.md) | Limits of efficiency |
| 05 | [task05_historical_ncube.md](theory/task05_historical_ncube.md) | nCUBE 10, 1024 processors, 1988 |
| 11 | [task11_sun_ni_comparison.md](theory/task11_sun_ni_comparison.md) | Memory-bounded speedup |
| 12 | [task12_communication_penalty.md](theory/task12_communication_penalty.md) | Model with C(P) |
| 13 | [task13_failure_cases.md](theory/task13_failure_cases.md) | CG and 3D FFT |
| 14 | [task14_isoefficiency.md](theory/task14_isoefficiency.md) | Isoefficiency Θ(P) |
| 15 | [task15_energy_scaling.md](theory/task15_energy_scaling.md) | Energy model |

### calculations/
| Task | File | Key result |
|---|---|---|
| 06 | [task06_parametric_table.md](calculations/task06_parametric_table.md) | α = 0.04: E falls from 96.25% to 96.00% |
| 07 | [task07_tolerable_serial.md](calculations/task07_tolerable_serial.md) | α_max = 692/8191 ≈ 0.0845 |
| 08 | [task08_cross_divergence.md](calculations/task08_cross_divergence.md) | Amdahl 11.47 vs Gustafson 117.84 (×10.27) |
| 09 | [task09_multicomponent.md](calculations/task09_multicomponent.md) | α = 0.08; S(512) = 471.12, S(2048) = 1884.24 |
| 10 | [task10_memory_growth.md](calculations/task10_memory_growth.md) | N_max = 6501 (64 nodes), 13003 (512 nodes) |
| 16 | [task16_gemm_scaling.md](calculations/task16_gemm_scaling.md) | N ∝ P^(1/3) |
| 17 | [task17_stencil_scaling.md](calculations/task17_stencil_scaling.md) | comm/comp stays constant per process |

### analysis/
| Task | File | Topic |
|---|---|---|
| 18 | [task18_nbody_scaling.md](analysis/task18_nbody_scaling.md) | Direct O(N²) vs Barnes–Hut |
| 19 | [task19_monte_carlo.md](analysis/task19_monte_carlo.md) | PRNG, reduction trees |
| 20 | [task20_graph_processing.md](analysis/task20_graph_processing.md) | BFS / PageRank |
| 24 | [task24_hardware_audit.md](analysis/task24_hardware_audit.md) | Hardware audit and deviations |

### benchmarks/ and plots/
| Task | File | What it does |
|---|---|---|
| 21 | [benchmarks/simulator.py](benchmarks/simulator.py) | Amdahl + Gustafson simulator, CSV export, overlay plot |
| 22 | [benchmarks/weak_scale_bench/](benchmarks/weak_scale_bench/) | Weak-scaling benchmark (multiprocessing) |
| 23 | [benchmarks/results.csv](benchmarks/results.csv), [benchmarks/fit_gustafson.py](benchmarks/fit_gustafson.py) | Raw data, least-squares α fit |
| 24 | [plots/scaling_comparison.png](plots/scaling_comparison.png) / `.pdf` | Empirical vs theoretical plot |
| 21 | [plots/simulator_overlay.png](plots/simulator_overlay.png) / `.pdf` | Strong vs weak overlay |

## 3. How to run

```bash
pip install numpy matplotlib

# Task 21: simulator
python benchmarks/simulator.py

# Task 22–23: benchmark (5 runs per P level), takes a few minutes
cd benchmarks/weak_scale_bench
python bench.py
cd ..

# Task 23–24: fit α and draw plots
python fit_gustafson.py
```

## 4. Key findings

1. **Both laws are one law in two frames** (Task 03). The α measured on the parallel machine and the f measured on one core are linked by `f = α/(α + (1 − α)P)`. For nCUBE (α = 0.4%) this gives f ≈ 3.9·10⁻⁶ and the same ~1020× speedup.
2. **Weak-scaling efficiency has a floor**, `1 − α` (Task 04, 06). Strong-scaling efficiency goes to 0.
3. **Requirements set a hard α budget** (Task 07). 7500× on 8192 cores needs α ≤ 8.45%.
4. **Communication breaks the constant-time premise.** `C(P) ∝ log P` costs a little, `√P` costs a lot, and `∝ P` brings back an Amdahl-like ceiling (Tasks 12, 19).
5. **Algorithm complexity matters.** O(N) kernels (stencils, Monte Carlo) scale like Gustafson. O(N²)/O(N³) kernels or kernels with global sync (direct N-body, CG, FFT, graphs) do not (Tasks 13, 16–20).
6. **Isoefficiency of a Gustafson program is Θ(P)**, which is the best possible (Task 14).
7. **Energy per unit of work stays almost constant** under weak scaling. The extra cost is about `α·P_idle/((1 − α)P_active)` (Task 15).
8. **On a laptop, measured α is mostly hardware**: Hyper-Threading, lower turbo clocks and heat, not the code's serial part (Task 24).

## 5. When to design for weak scaling

Design software around Gustafson's principles when:
- users want **a bigger or more accurate problem** in the same time (finer grids, more samples, more particles);
- the work is **O(N) per time step** and communication is **local** (nearest neighbours);
- the data fits in **memory per node** and grows with the machine.

Practical rules:
- Keep **α small and constant**: parallel I/O, tree reductions, no global locks.
- Make sub-domains **large and compact** (surface-to-volume ratio ∝ 1/n).
- Replace O(P) steps with O(log P) steps: broadcasts, reductions, seeding.
- Check isoefficiency: if `T_o` grows faster than P, plain weak scaling will lose efficiency.
- Measure α at several P values. If α grows with P, the overhead comes from communication or hardware, not from serial code.

Use **Amdahl / strong scaling** instead when the problem size is fixed by the user (one image, one query, a real-time deadline).
