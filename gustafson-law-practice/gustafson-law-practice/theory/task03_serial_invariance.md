# Task 03 — The Serial Fraction Invariance Paradox

## The paradox

- Amdahl says that a small serial part (say 1%) limits speedup to 100×.
- Gustafson measured speedup above 1000× on 1024 processors, with a "serial fraction" of 0.4–0.8%.

Both look correct, so how is this possible? The answer is that **the two serial fractions are measured in different frames of reference.**

## Two frames of reference

| Symbol | Where it is measured | Meaning |
|---|---|---|
| `f` (Amdahl's s) | on **1 processor** | serial time / total serial run time |
| `α` (Gustafson's s) | on **P processors** | serial time / total parallel run time |

Let `t_s` be the serial time and `t_p` the parallel part time on P cores.

- On the parallel machine: `α = t_s / (t_s + t_p)`.
- On one processor, the same job takes `t_s + P·t_p`, so `f = t_s / (t_s + P·t_p)`.

## The link between them

Divide the top and bottom by `t_s + t_p`:

```
f = α / (α + (1 − α)·P)
```

So `f` depends on P, while `α` is fixed. When P grows, `f → 0`.

**Example (nCUBE, α = 0.004, P = 1024):**

```
f = 0.004 / (0.004 + 0.996·1024) ≈ 3.9 × 10⁻⁶
```

Put this f into Amdahl's law:

```
S_A = 1 / (f + (1 − f)/1024) ≈ 1020
```

This is the **same** number as Gustafson's `S = 1024 − 0.004·1023 ≈ 1020`.

## Proof that the two laws agree

Start from Amdahl with `f`:

```
S_A = 1 / (f + (1 − f)/P)
```

Substitute `f = α / (α + (1 − α)P)`. Then `1 − f = (1 − α)P / (α + (1 − α)P)`, and

```
f + (1 − f)/P = [α + (1 − α)] / (α + (1 − α)P) = 1 / (α + (1 − α)P)
S_A = α + (1 − α)P = S_G         ∎
```

## Why this resolves the contradiction

- The serial part (reading input, setup) takes about the **same absolute time** when the problem grows.
- The parallel part grows with the problem.
- So, *measured on one processor*, the serial share of a big problem is tiny. Amdahl's ceiling `1/f` becomes huge (about 255,000 for f = 3.9 × 10⁻⁶).
- The serial overhead "does not throttle" scaling because it does not grow with the problem.

## Conclusion

There is no real contradiction. It is one law written in two frames. Errors appear when people take `α` measured on a parallel machine and put it into Amdahl's formula as if it was `f`. This mistake gives about 201× instead of 1020× for the nCUBE case.
