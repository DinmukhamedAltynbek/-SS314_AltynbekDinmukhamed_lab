# Task 17 — 3D 7-Point Stencil: Surface-to-Volume Scaling

## 1. Setup

- Global cube `N × N × N`, split into P sub-cubes of size `n × n × n`, so `N³ = P·n³`.
- Computation per process per step: `T_comp = a · 7 · n³` (7 points per update).
- Halo exchange per process: 6 faces × `n²` values, so `T_comm = 6·(L + b·n²)`, where L is latency and b is time per value.

Communication-to-computation ratio per process:

```
R(n) = T_comm / T_comp = 6(L + b·n²) / (7a·n³)  ≈  (6b / 7a) · (1/n)    for big n
```

## 2. Weak scaling (Gustafson): n is fixed

The domain volume grows like P: `N³ = P·n³`, so `N = n·P^(1/3)`.

```
R = (6b/7a)·(1/n) = constant     (does not depend on P)
```

**Proof:** n does not change, and each inner process always has exactly 6 neighbours. Its faces and volume stay the same, so `T_comm` and `T_comp` stay the same. ∎

Global view: the surface-to-volume ratio of the *whole domain* is `6N²/N³ = 6/N ∝ P^(−1/3)`, so it **improves**. Physical boundaries become a smaller share of the problem.

## 3. Strong scaling (Amdahl): N is fixed

```
n = N / P^(1/3)       ⇒       R ∝ 1/n = P^(1/3)/N     → gets worse
```

## 4. Numeric example (n = 100 per process in weak scaling, N = 400 in strong scaling)

| P | Weak: n | Weak: halo/volume `6/n` | Strong: n = 400/P^(1/3) | Strong: `6/n` |
|---|---|---|---|---|
| 1 | 100 | 0.060 | 400 | 0.015 |
| 8 | 100 | 0.060 | 200 | 0.030 |
| 64 | 100 | 0.060 | 100 | 0.060 |
| 512 | 100 | 0.060 | 50 | 0.120 |
| 4096 | 100 | 0.060 | 25 | 0.240 |

(For P = 1 there is no real exchange. The value shows only the geometric ratio.)

## 5. Conclusion

- Under Gustafson scaling the comm/comp ratio **stays constant** per process, and the global ratio **improves** like `P^(−1/3)`. This is why stencil codes are a textbook example of good weak scaling.
- It degrades only if (1) the subdomain becomes smaller (strong scaling), (2) global reductions are added (for example a residual check, `∝ log P`), or (3) the network cannot carry all neighbour messages at the same time.
- Tip: make sub-domains as cubic and as large as the memory allows, because R falls like `1/n`.
