# Task 05 — The nCUBE 10 Experiment (Sandia, 1988)

## 1. Background

In 1988 Gustafson, Montry and Benner (Sandia National Laboratories) worked on an **nCUBE 10**. This was a hypercube machine with **1024 processors**, and each node had its own small local memory. At that time many people believed Amdahl's law made such machines pointless. With a serial part of only 1%, the speedup can never go above 100×.

## 2. The three applications

They wrote parallel versions of three real scientific codes:

| Application | Method | Scaled speedup on 1024 PEs |
|---|---|---|
| Beam stress analysis | conjugate gradients | **1021×** |
| Baffled surface wave simulation | explicit finite differences | **1020×** |
| Unstable fluid flow | flux-corrected transport | **1016×** |

The serial fraction measured on the parallel machine was **0.4% – 0.8%**.

They also did fixed-size runs, where the problem was the same on 1 and 1024 processors. There the speedup was **502× to 637×**. That was also very good, but it was clearly lower than the scaled speedup.

## 3. Why Amdahl looked broken

If we put s = 0.004 into Amdahl's formula:

```
S_A = 1 / (0.004 + 0.996/1024) ≈ 201×
```

With s = 0.008 we get only about 111×. But the machine reached about 1020×.

## 4. How problem expansion removed the ceiling

1. **They scaled the problem with the machine.** Each processor got about the same amount of work (the same number of grid points or elements). With 1024 processors the global problem was about 1024 times larger.
2. **The serial part did not grow.** Input, setup and global output took about the same absolute time.
3. **The parallel part grew linearly.** So the serial share *of the whole job* became tiny. Measured on one processor, it is about `f ≈ 3.9 × 10⁻⁶` (see Task 03).
4. **They could not even run the big problem on one node.** One processor did not have enough memory for the 1024× problem. So the serial time was *estimated* as `s + 1024·p`. This is exactly the scaled-speedup idea.

Gustafson's formula gives:

```
S = 1024 − 0.004 · 1023 ≈ 1019.9      (s = 0.4%)
S = 1024 − 0.008 · 1023 ≈ 1015.8      (s = 0.8%)
```

This is very close to the measured 1016–1021.

## 5. Other tricks that helped

- Overlapping communication with computation, and nearest-neighbour exchange on the hypercube.
- Trading communication for some redundant computation (computing values again locally instead of sending them).
- Careful load balance, so all nodes finish at the same time.

## 6. Lessons

- Amdahl's law is not wrong. It was applied to the wrong question.
- For big science, users grow the problem, so the fixed-time view is more realistic.
- Later work (Shi, 1996) showed that both laws are mathematically the same once the serial fraction is translated between frames (Task 03).

## References

- J. L. Gustafson, "Reevaluating Amdahl's Law", *Communications of the ACM* 31(5), 1988, pp. 532–533.
- J. L. Gustafson, G. R. Montry, R. E. Benner, "Development of Parallel Methods for a 1024-Processor Hypercube", *SIAM J. Sci. Stat. Comput.* 9(4), 1988.
- Y. Shi, "Reevaluating Amdahl's Law and Gustafson's Law", Temple University, 1996.
