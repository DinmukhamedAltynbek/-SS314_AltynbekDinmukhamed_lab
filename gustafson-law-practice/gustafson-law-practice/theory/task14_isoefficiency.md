# Task 14 — Isoefficiency and Gustafson Scaling

## 1. Isoefficiency (Kumar & Grama)

- `W` = problem size, measured as serial work (time on one core).
- `T_o(W, P) = P·T_P − W` = total overhead (time that all cores together waste).
- Efficiency:

```
E = W / (W + T_o(W, P)) = 1 / (1 + T_o/W)
```

To keep `E` constant we need

```
W = K · T_o(W, P),     K = E/(1 − E)
```

The function `W = f(P)` that solves this is the **isoefficiency function**. Slow growth (like `P`) means a very scalable program. Fast growth (like `P²`) means a poorly scalable one.

## 2. Overhead of a Gustafson program

Gustafson program: serial time `t_s` and parallel time `t_p` per core, and both are constant with P.

- Parallel time: `T_P = t_s + t_p`
- Serial work: `W = t_s + P·t_p`
- Overhead:

```
T_o = P·T_P − W = P·t_s + P·t_p − t_s − P·t_p = t_s·(P − 1)
```

Only the serial part wastes time: while one core works, `P − 1` cores wait.

## 3. Isoefficiency function

```
W = K · t_s · (P − 1)    ⇒    W = Θ(P)
```

**Proof that E is constant along this curve.** Gustafson's weak scaling uses `W(P) = t_s + P·t_p`. Then

```
E = W/(W + T_o) = (t_s + P·t_p)/(P·t_s + P·t_p) = (1 − α) + α/P
```

with `α = t_s/(t_s + t_p)`. When P is big this goes to `1 − α`, a constant. So linear growth of W is **enough** to keep E (almost) constant. Because `T_o = Θ(P)`, it is also **necessary**: if W grows slower than P, then `T_o/W → ∞` and `E → 0`. ∎

**Conclusion:** a Gustafson-compliant program has **linear isoefficiency, W ∈ Θ(P).** This is the best possible class in Kumar–Grama theory, because `T_o ≥ Θ(P)` for any program that has some serial part.

## 4. Critique

1. **Gustafson assumes the answer.** It takes `W ∝ P` as given and then gets constant E. Isoefficiency *asks* how fast W must grow, so it is the more general tool.
2. **Real overheads are bigger than `t_s(P − 1)`.**
   - With a tree reduction: `T_o ≈ t_s P + c·P log P` → `W = Θ(P log P)`.
   - With all-to-all: `T_o ∝ P²` → `W = Θ(P²)`.
   In these cases plain linear weak scaling is not enough, and efficiency falls (see Task 12).
3. **The memory limit.** If isoefficiency needs W to grow faster than memory per node allows (for example `W ∝ P log P` with fixed memory per node), constant efficiency is impossible in practice.

| Overhead T_o | Isoefficiency W(P) | Gustafson OK? |
|---|---|---|
| `t_s(P − 1)` | Θ(P) | yes |
| `P log P` | Θ(P log P) | efficiency slowly falls |
| `P^1.5` | Θ(P^1.5) | no |
| `P²` | Θ(P²) | no |
