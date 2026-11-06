# Task 10 — Memory Growth vs. Scaled Speedup

## 1. Model

- Weak scaling: `W(P) = P · W(1)`, and memory `M(P) = c · P`.
- Per-node cap: `m = 32 GiB = 32 · 2³⁰ B = 34,359,738,368 B`.
- Total memory on P nodes: `M_max(P) = P · m`.
- 3D grid with `N × N × N` points. Each point needs `b` bytes, so memory is `b · N³`.

## 2. Memory ceiling

```
b · N³ ≤ P · m      ⇒      N_max(P) = ⌊ (P · m / b)^(1/3) ⌋
```

Two notes:
- `N_max ∝ P^(1/3)`. With 8× more nodes, the grid side only doubles.
- Grid points per node `N³/P = m/b` is constant. This is exactly Gustafson's weak scaling.

## 3. Calculation (one double per point, b = 8 B)

**64 nodes:**
```
M = 64 · 32 GiB = 2048 GiB = 2⁴¹ B
N³ ≤ 2⁴¹ / 8 = 2³⁸ = 274,877,906,944
N_max = ⌊2^(38/3)⌋ = 6501         (6501³ = 2.7475·10¹¹ ≤ 2³⁸ < 6502³)
```

**512 nodes:**
```
M = 512 · 32 GiB = 16384 GiB = 2⁴⁴ B
N³ ≤ 2⁴⁴ / 8 = 2⁴¹ = 2,199,023,255,552
N_max = ⌊2^(41/3)⌋ = 13003        (13004³ > 2⁴¹)
```

Check: 512/64 = 8, and `8^(1/3) = 2`, so `13003 ≈ 2 · 6501` ✔

## 4. More realistic solvers (several values per point)

| Bytes per point b | Example | N_max (64 nodes) | N_max (512 nodes) |
|---|---|---|---|
| 8 | 1 double | 6501 | 13003 |
| 40 | 5 doubles (ρ, u, v, w, E) | 3802 | 7604 |
| 80 | 5 fields × 2 time levels | 3017 | 6035 |

## 5. Link to scaled speedup

- If the solver work is O(N³) per time step, work ∝ memory ∝ P. Gustafson's law holds and the time per step stays constant.
- If the solver needs more steps for a finer grid (CFL rule: steps ∝ N ∝ P^(1/3)), then the total time grows like `P^(1/3)` even with perfect weak scaling (see Task 13).
- The 32 GB cap is the real reason the problem cannot grow faster than P. It is the "memory-bounded" limit in Sun–Ni (Task 11).
