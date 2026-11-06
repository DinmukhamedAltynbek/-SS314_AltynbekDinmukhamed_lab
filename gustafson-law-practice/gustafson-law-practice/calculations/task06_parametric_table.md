# Task 06 — Scaled Speedup and Efficiency for α = 0.04

## Formulas

```
S(P) = P − α(P − 1)
E(P) = S(P)/P = 1 − α(P − 1)/P
```

## Worked numbers (α = 0.04)

```
P = 16    : S = 16    − 0.04·15    = 16    − 0.60   = 15.40     E = 15.40/16       = 0.962500
P = 64    : S = 64    − 0.04·63    = 64    − 2.52   = 61.48     E = 61.48/64       = 0.960625
P = 256   : S = 256   − 0.04·255   = 256   − 10.20  = 245.80    E = 245.80/256     = 0.960156
P = 1024  : S = 1024  − 0.04·1023  = 1024  − 40.92  = 983.08    E = 983.08/1024    = 0.960039
P = 4096  : S = 4096  − 0.04·4095  = 4096  − 163.80 = 3932.20   E = 3932.20/4096   = 0.960010
P = 16384 : S = 16384 − 0.04·16383 = 16384 − 655.32 = 15728.68  E = 15728.68/16384 = 0.960002
```

## Table

| P | S(P) Gustafson | E(P) | Lost cores `P − S` | Amdahl S (s = 0.04), for comparison |
|---|---|---|---|---|
| 16 | 15.40 | 96.25% | 0.60 | 10.00 |
| 64 | 61.48 | 96.06% | 2.52 | 18.18 |
| 256 | 245.80 | 96.02% | 10.20 | 22.86 |
| 1024 | 983.08 | 96.00% | 40.92 | 24.43 |
| 4096 | 3932.20 | 96.00% | 163.80 | 24.85 |
| 16384 | 15728.68 | 96.00% | 655.32 | 24.96 |

## Evaluation

- P grows by 4× each step (exponentially), and S also grows about 4× each step. The speedup stays linear.
- Efficiency falls only from 96.25% to 96.00%. Its limit is `1 − α = 0.96` (Task 04), and the difference from the limit, `α/P`, gets 4 times smaller at each step.
- The number of "lost" cores, `α(P − 1)`, grows linearly. This is always about 4% of the machine, never more.
- With the same 4%, Amdahl gives at most 25×. This shows clearly how big the difference is between strong and weak scaling.
