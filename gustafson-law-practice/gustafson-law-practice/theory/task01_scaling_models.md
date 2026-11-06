# Task 01 — Strong Scaling vs. Weak Scaling

## 1. Amdahl (1967): fixed-size model

**Main assumption:** the problem size `W` is fixed. We take the same job and give it to more processors.

- Time on 1 processor is normalized: `T(1) = s + (1 − s) = 1`.
- Time on P processors: `T(P) = s + (1 − s)/P`.
- Speedup: `S_A(P) = 1 / (s + (1 − s)/P)`.

**What happens when P → ∞:** the problem size stays the same (`W(P) = W`). Each processor gets less and less work (`W/P → 0`). Only the serial part `s` is left, so

```
lim S_A(P) = 1/s        (P → ∞)
```

Example: with `s = 0.05` the speedup can never be bigger than 20, even with a million cores.

## 2. Gustafson (1988): fixed-time model

**Main assumption:** the run time is fixed. When we get more processors, we solve a bigger problem in the same time.

- Time on P processors is normalized: `T(P) = s + p = 1`.
- The same job on 1 processor would take `s + p·P`.
- Scaled speedup: `S_G(P) = s + p·P = P − α(P − 1)`.

**What happens when P → ∞:** the problem size grows with P (`W(P) ≈ s + p·P`, linear in P). The work per processor stays constant. The speedup grows without limit:

```
S_G(P) ≈ (1 − α)·P → ∞
```

## 3. Why "fixed-size" and "fixed-time"

| | Amdahl | Gustafson |
|---|---|---|
| What is constant | problem size W | wall-clock time T |
| What changes with P | time goes down | problem size goes up |
| Scaling type | strong scaling | weak scaling |
| Serial fraction measured on | 1 processor | the parallel machine |
| Limit as P → ∞ | 1/s | grows like (1 − α)P |
| Mood | pessimistic | optimistic |

- Amdahl is **fixed-size** because the question is: *"How fast can I finish this one job?"*
- Gustafson is **fixed-time** because the question is: *"How big a job can I finish in one hour?"*

## 4. Philosophical and physical difference

- **Amdahl** thinks like a user with one fixed task (for example, one image to render). More hardware only cuts time, and the serial part becomes the bottleneck.
- **Gustafson** thinks like a scientist. People buy a bigger machine to get finer grids, more particles or more time steps, not to wait less. In most scientific codes the serial part (input, setup) grows slowly or not at all, while the parallel part grows with problem size. So the serial fraction gets *smaller* when the problem grows.
- Physically, both laws are true. They just answer different questions. Amdahl describes strong scaling, and Gustafson describes weak scaling.
