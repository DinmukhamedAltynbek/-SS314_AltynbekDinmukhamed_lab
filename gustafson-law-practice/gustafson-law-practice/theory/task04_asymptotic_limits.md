# Task 04 — Asymptotic Limits of Parallel Efficiency

## 1. Gustafson efficiency

```
E_G(P) = S_G(P)/P = (P − α(P − 1))/P = 1 − α + α/P
```

**Limit:**

```
lim (P → ∞) E_G(P) = 1 − α
```

**Proof (ε–N):** `|E_G(P) − (1 − α)| = α/P`. For any `ε > 0`, choose `N > α/ε`. Then for all `P > N` we get `α/P < ε`. ∎

**Properties:**
- `E_G` goes down monotonically: `dE/dP = −α/P² < 0`.
- It never falls below `1 − α`. For example, with α = 0.04, efficiency stays above 96% forever.
- `E_G(1) = 1`, so the total loss is never more than α.

## 2. Amdahl efficiency

```
S_A(P) = 1/(s + (1 − s)/P)
E_A(P) = S_A(P)/P = 1/(sP + 1 − s)
```

**Limit:**

```
lim (P → ∞) E_A(P) = 0        (for any s > 0)
```

**Proof:** the denominator `sP + 1 − s → ∞` when `s > 0`, so `E_A → 0`. More exactly, `E_A(P) ≈ 1/(sP)` for big P, so efficiency falls like `1/P`. ∎

## 3. Comparison

| | Gustafson (weak) | Amdahl (strong) |
|---|---|---|
| E(P) | `1 − α + α/P` | `1/(1 + s(P − 1))` |
| Limit P → ∞ | `1 − α` (positive constant) | `0` |
| Speed of decay | `α/P` → flattens fast | `~1/(sP)` → keeps falling |
| Speedup limit | ∞ (linear, slope 1 − α) | `1/s` |

Example with α = s = 0.04:

| P | E_G | E_A |
|---|---|---|
| 16 | 0.9625 | 0.625 |
| 1024 | 0.9600 | 0.024 |

## 4. Conclusion

Under Gustafson, extra processors are never wasted: each one keeps giving about `(1 − α)` of a processor. Under Amdahl, after about `P ≈ 1/s` cores, new cores mostly sit idle. This is why weak scaling is the normal way to use supercomputers.
