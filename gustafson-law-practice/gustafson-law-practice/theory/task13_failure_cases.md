# Task 13 — When Gustafson Fails

Gustafson's law needs one key premise: **if each core keeps the same amount of data, the run time stays the same.** Below are two well-known algorithms where this premise breaks.

---

## Case 1. Conjugate Gradient (CG) for the Poisson equation

**Setup.** We solve `Ax = b` on a 3D grid with `N³` points. Each core holds a fixed block of `n³` points, so `N = n · P^(1/3)`.

**Why the time is not constant:**

1. **The number of iterations grows.** For the Poisson matrix the condition number is `κ ∝ N²`, and CG needs about `√κ ∝ N` iterations. So the iterations grow like `P^(1/3)`. With 8× more cores, the same per-core work is repeated about 2× more times.
2. **Every iteration has global dot products.** Each one is an `Allreduce`, which costs about `log P`, and it is a synchronization point. The slowest core blocks all the others.

**Result:**

```
T(P) ∝ P^(1/3) · (n³ + c·log P)      → grows with P, not constant
```

The "parallel fraction" is not P-independent. The algorithm itself gets more expensive when the problem grows. (Multigrid fixes the iteration count, but it adds coarse levels that are almost serial.)

---

## Case 2. Distributed 3D FFT

**Setup.** We do a 3D FFT on `N³` points, with a fixed `n³` points per core.

**Why the time is not constant:**

1. **The work per point grows.** FFT costs `N³ log N³`. Per core this is `n³ · log(n³P)`, so it grows like `log P`.
2. **All-to-all transpose.** Each core must send data to many other cores. The total traffic is `∝ N³ = n³P`, but the network bisection bandwidth grows slower than P (on a 3D torus it is `∝ P^(2/3)`). So the transpose time grows like `P^(1/3)`.
3. **Message count.** Each core sends up to `P − 1` small messages, and latency `∝ P` starts to dominate.

**Result:**

```
T(P) ∝ n³ log(n³P) + c₁·P^(1/3) + c₂·P   → grows with P
```

---

## Other short examples

- **Shared lock / atomic counter**: with more threads, contention for one lock grows. The serial critical section is serialized P times, so `α` grows with P.
- **Dense direct solver (LU)**: work is `N³` but memory is `N²`. With fixed memory per node, `N ∝ √P` and the time grows like `√P` (see Task 11).

## Why the constant-runtime premise breaks

| Reason | CG | FFT |
|---|---|---|
| Complexity is above O(N) | iterations ∝ N | N log N |
| Global synchronization | Allreduce every step | all-to-all |
| Network cost grows with P | log P | P^(1/3) … P |

Gustafson's law silently assumes **O(N) work and O(1) communication per core**. When the algorithm is superlinear, or needs global communication, the parallel part per core grows, and the law overestimates the speedup.
