# Task 19 — Monte Carlo: The Ideal Weak-Scaling Workload

## 1. Why Monte Carlo fits Gustafson

Each worker simulates its own random paths. The workers do not need to talk to each other during the run. With more workers we simply take more samples in the same time, and the error falls like `1/√(P·k)`. So the fixed-time model is natural here.

## 2. Where the non-zero α comes from

| Source | What happens | Cost |
|---|---|---|
| **PRNG seed management** | The master makes P independent streams (skip-ahead, or counter-based like Philox) and sends them out | `O(P)` if done in a loop on the master, `O(log P)` with a tree broadcast, `O(1)` if each worker derives its seed from its rank |
| **Start-up / broadcast** | sending parameters and starting processes | `O(log P)` with a tree |
| **Reduction** | adding the partial sums (mean, variance) | `O(P)` linear, `O(log P)` with a tree |
| **Output serialization** | one process writes the final results / histograms | constant, or `O(P)` if all workers write through one process |
| **Load imbalance** | paths have different lengths (e.g. barrier options) | the slowest worker sets the time |

**PRNG quality note:** bad seeding (for example `seed = rank`) with a simple LCG can give correlated streams. This is not a time cost, but it makes the results wrong. Use `numpy.random.SeedSequence.spawn()` or counter-based generators.

## 3. Model with reduction

Let `t_s` = constant serial time (seed setup + output), `t_w` = work time per worker, `t_r` = cost of one combine step.

```
Tree reduction:    T(P) = t_s + t_w + t_r · log₂ P
Linear reduction:  T(P) = t_s + t_w + t_r · (P − 1)
Scaled speedup:    S(P) = (t_s + P · t_w) / T(P)
```

## 4. Numbers (`t_s = 0.005`, `t_w = 1.0`, `t_r = 0.001`)

| P | Tree: S | Tree: E | Tree: α_eff | Linear: S | Linear: E | Linear: α_eff |
|---|---|---|---|---|---|---|
| 64 | 63.3 | 98.9% | 0.011 | 59.9 | 93.6% | 0.065 |
| 1024 | 1008.9 | 98.5% | 0.015 | 504.9 | 49.3% | 0.507 |
| 16384 | 16078.5 | 98.1% | 0.019 | 942.3 | 5.8% | 0.943 |

(`α_eff = (P − S)/(P − 1)`, which is the α we would fit from measurements.)

## 5. How the reduction tree affects S(P)

- With a **tree**, the overhead grows only like `log₂ P`. At 16384 cores it is just 14 combine steps, and efficiency stays above 98%. α_eff grows very slowly.
- With a **linear** gather to one root, the root does `P − 1` additions, and the reduction becomes the new serial bottleneck. After about `P ≈ t_w/t_r = 1000` the speedup stops growing, just like Amdahl's ceiling.
- Rule: always use a tree / butterfly reduction (`MPI_Reduce`, or a reduction in `multiprocessing` done in steps). Keep the reduced data small (sums and counts, not all samples).

## 6. Conclusion

Monte Carlo is the closest real workload to Gustafson's ideal. But it is not perfect: α is never exactly 0. Seeding, start-up, reduction and I/O add a small serial part, and the reduction tree decides whether this part grows like `log P` (good) or like `P` (bad).
