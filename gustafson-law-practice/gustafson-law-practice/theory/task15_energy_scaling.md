# Task 15 — Energy and Power under Scaled Speedup

## 1. Power model

Each node uses:
- `P_idle` when it waits (static power, always present),
- `P_active` when it computes (`P_active > P_idle`).

Run time on P nodes is `T` (fixed time). The serial phase lasts `αT` and the parallel phase lasts `(1 − α)T`.

## 2. Energy on P nodes (weak scaling)

Serial phase: 1 node is active and `P − 1` nodes wait. Parallel phase: all P nodes are active.

```
E_P = T · [ α·(P_active + (P − 1)·P_idle) + (1 − α)·P·P_active ]
```

Useful work done: `S(P) = α + (1 − α)P` (in units of the 1-node job).

## 3. Energy on 1 node, same wall-clock time T

```
E_1 = T · P_active,     work done = 1 unit
```

**Comparison for identical runtime:**

```
E_P / E_1 = α·(1 + (P − 1)·r) + (1 − α)·P,       r = P_idle / P_active
```

So P nodes use about P times more energy, but they also do about P times more work.

## 4. Energy per unit of work (the fair comparison)

If one node had to do the *same scaled job*, it would need time `S(P)·T` and energy `S(P)·T·P_active`. The ratio is

```
E_P / E_1,scaled = 1 + α·(P − 1)·r / (α + (1 − α)P)
```

- The extra term is always ≥ 0. It is the energy of the waiting nodes during the serial phase.
- When P → ∞:

```
E_P / E_1,scaled → 1 + α·r/(1 − α)
```

So weak scaling costs **only a constant extra share of energy**, even on a huge machine.

## 5. Example: α = 0.04, P_active = 150 W, P_idle = 50 W (r = 1/3)

| P | Scaled speedup S | E_P / E_1 (same T) | Extra energy per unit of work |
|---|---|---|---|
| 1 | 1.00 | 1.00 | 0% |
| 16 | 15.40 | 15.60 | 1.3% |
| 64 | 61.48 | 62.32 | 1.37% |
| 1024 | 983.08 | 996.72 | 1.39% |
| ∞ | — | — | 1.39% (= 0.04·(1/3)/0.96) |

## 6. Comparison with strong scaling

In strong scaling (Amdahl) the job is fixed. Waiting nodes burn `P_idle` for a long time while the serial part runs. When `P ≫ 1/s`, most nodes are idle, so the energy per job grows almost linearly with P, while the time stops going down.

## 7. Conclusion

- Under Gustafson, energy per unit of useful work stays almost constant. It is only about `α·r/(1 − α)` worse than one node.
- To save energy: lower `α`, lower `P_idle` (power gating), or let idle nodes sleep during the serial phase.
