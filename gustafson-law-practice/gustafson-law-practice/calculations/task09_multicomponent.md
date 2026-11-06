# Task 09 — Multi-Component Workload

## Phase breakdown (share of the total parallel run time)

| Phase | Share | Type | Why |
|---|---|---|---|
| A. Disk I/O + parameter broadcast | 2% | serial | one file system or root process; it does not get faster with more cores |
| B. Boundary message-passing sync | 6% | serial (non-scaling) | cores wait for each other; this time does not do any useful parallel work |
| C. Core domain flux computation | 92% | parallel | every core works on its own subdomain |

## Aggregate serial fraction

```
α = α_A + α_B = 0.02 + 0.06 = 0.08
p = 1 − α     = 0.92
```

## Scaled speedup

```
S(P) = P − α(P − 1)

P = 512  : S = 512  − 0.08 · 511  = 512  − 40.88  = 471.12      E = 92.02%
P = 2048 : S = 2048 − 0.08 · 2047 = 2048 − 163.76 = 1884.24     E = 92.00%
```

## Composite analysis

| P | S(P) | E(P) | Loss from A (`0.02(P − 1)`) | Loss from B (`0.06(P − 1)`) |
|---|---|---|---|---|
| 512 | 471.12 | 92.02% | 10.22 | 30.66 |
| 2048 | 1884.24 | 92.00% | 40.94 | 122.82 |

- Phase B causes **75%** of the loss (6 out of 8 points). Reducing synchronization is the best place to optimize.
- **Sensitivity check:** if the sync phase could be overlapped with computation (only A is serial, α = 0.02), then S(512) = 501.78 and S(2048) = 2007.06. That is a 6.5% gain.
- **Warning:** in real codes phase B usually grows with P (for example `∝ log P`, see Task 12). Then α at 2048 cores would be bigger than at 512, and 1884 is an upper bound.
