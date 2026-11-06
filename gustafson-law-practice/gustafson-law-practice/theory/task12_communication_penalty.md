# Task 12 — Adding Communication Overhead to Gustafson's Law

## 1. Problem with the classic law

Classic Gustafson assumes that the parallel run time `s + p = 1` stays the same for every P. In real clusters each step needs messages (halo exchange, reductions, barriers), and their cost grows with P.

## 2. Modified model

Keep the work per core fixed and add a communication term `C(P)` to the parallel time:

```
T(P) = s + p + C(P),          with s + p = 1 and C(1) = 0
T(1) = s + p·P                (one core needs no messages)
```

Modified scaled speedup:

```
S_C(P) = (α + (1 − α)P) / (1 + C(P))  =  S_G(P) / (1 + C(P))
```

Modified efficiency:

```
E_C(P) = (1 − α + α/P) / (1 + C(P))
```

## 3. Common forms of C(P)

| Pattern | C(P) | Example |
|---|---|---|
| Nearest-neighbour halo | `c₀` (constant) | stencil codes |
| Tree reduction / broadcast | `c₀ · log₂ P` | global sum, MPI_Allreduce |
| 2D-grid / torus collectives | `c₀ · √P` | some matrix codes |
| All-to-all | `c₀ · P` | FFT transpose |

## 4. Limits as P → ∞

- `C = c₀` → `E → (1 − α)/(1 + c₀)`, a constant. The law still holds with a smaller slope.
- `C = c₀ log P` → `E ≈ (1 − α)/(c₀ log P) → 0`, but very slowly.
- `C = c₀ √P` → `E → 0` faster, and `S ≈ (1 − α)√P / c₀` grows only like `√P`.
- `C = c₀ P` → `S → (1 − α)/c₀`, so the speedup has a ceiling like Amdahl.

## 5. Example (α = 0.04, c₀ = 0.01)

| P | Classic S | log P model: S (E) | √P model: S (E) |
|---|---|---|---|
| 64 | 61.5 | 58.0 (0.906) | 56.9 (0.890) |
| 1024 | 983.1 | 893.7 (0.873) | 744.8 (0.727) |
| 16384 | 15728.7 | 13797.1 (0.842) | 6898.5 (0.421) |

## 6. An effective serial fraction

We can also write the model in the classic form with an **effective α** that grows with P:

```
α_eff(P) = (α + C(P)) / (1 + C(P))
S_C(P) ≈ P − α_eff(P)·(P − 1)     (for large P)
```

So in experiments a fitted α that grows with P is a sign of communication overhead. This is the same idea as a rising Karp–Flatt metric.
