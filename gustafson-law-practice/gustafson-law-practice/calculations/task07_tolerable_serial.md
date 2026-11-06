# Task 07 — Maximum Tolerable Serial Fraction

**Given:** `P = 8192`, requirement `S(P) ≥ 7500`.

## Derivation

```
S(P) = P − α(P − 1) ≥ S_req
P − S_req ≥ α(P − 1)
α ≤ (P − S_req) / (P − 1)
```

So

```
α_max = (P − S_req) / (P − 1)
```

## Numbers

```
α_max = (8192 − 7500) / (8192 − 1)
      = 692 / 8191
      = 0.0844829...
```

**α_max ≈ 0.08448, which is 8.45%.**

## Check

```
S = 8192 − 0.0844830 · 8191 = 8192 − 692.00 = 7500.0  ✔
```

## Extra notes

- Required efficiency: `E = 7500/8192 = 91.55%`. This fits, because `E ≈ 1 − α = 91.55%`.
- If α goes above 8.45%, even by a little (for example α = 0.09 gives S = 7454.8), the requirement fails.
- **Compare with Amdahl:** to reach 7500× with fixed-size scaling, the serial fraction measured on one core must satisfy `1/(s + (1 − s)/8192) ≥ 7500`. This gives `s ≤ 1.13 × 10⁻⁵`, which is about 7500 times stricter.
