# Task 08 — Amdahl vs. Gustafson at s = α = 0.08, P = 128

## Step 1. Amdahl

```
S_A = 1 / (s + (1 − s)/P)
    = 1 / (0.08 + 0.92/128)
    = 1 / (0.08 + 0.0071875)
    = 1 / 0.0871875
    = 11.4695
```

Efficiency: `11.4695/128 = 8.96%`.

## Step 2. Gustafson

```
S_G = P − α(P − 1)
    = 128 − 0.08 · 127
    = 128 − 10.16
    = 117.84
```

Efficiency: `117.84/128 = 92.06%`.

## Step 3. Discrepancy

| Measure | Value |
|---|---|
| Absolute difference | `117.84 − 11.47 = 106.37` |
| Ratio `S_G / S_A` | **10.27** |
| Discrepancy relative to Amdahl | `(117.84 − 11.4695)/11.4695 = 927.4%` |
| Discrepancy relative to Gustafson | `(117.84 − 11.4695)/117.84 = 90.27%` |

## Step 4. Why they diverge as P grows

- Amdahl has a ceiling: `S_A → 1/s = 12.5`. At P = 128 we already have 11.47, which is 92% of the ceiling. More cores add almost nothing.
- Gustafson grows linearly: `S_G ≈ 0.92·P`. Each new core adds 0.92.
- So the ratio grows almost linearly with P:

```
S_G/S_A = (P − α(P − 1)) · (s + (1 − s)/P)  →  ≈ s(1 − s)·P  for large P
```

| P | S_A | S_G | Ratio |
|---|---|---|---|
| 8 | 5.13 | 7.44 | 1.45 |
| 128 | 11.47 | 117.84 | 10.3 |
| 1024 | 12.36 | 942.16 | 76.22 |

- The root cause: the 0.08 means something different in each law (Task 03). In Amdahl the problem stays fixed, so the serial time becomes the main part. In Gustafson the problem grows, so the serial time becomes a smaller and smaller share of the equivalent serial job.
