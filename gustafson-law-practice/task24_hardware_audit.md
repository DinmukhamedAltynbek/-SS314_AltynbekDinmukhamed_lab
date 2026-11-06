# Task 24 — Empirical vs. Theoretical Scaling and Hardware Audit

## 1. Plot

![Scaling comparison](../plots/scaling_comparison.png)

Vector version: [`plots/scaling_comparison.pdf`](../plots/scaling_comparison.pdf)

The plot has four parts:
1. the ideal linear speedup `S = P` (dotted line),
2. the Gustafson curve with my fitted α (blue),
3. my measured mean scaled speedup with standard error bars (green; the orange point is oversubscribed),
4. Amdahl's curve with the same α (red dashed line).

## 2. Hardware

| Item | Value |
|---|---|
| CPU | Intel 7th gen Core, "Kaby Lake-U" (Family 6, Model 142, Stepping 9) (e.g. Core i5-7200U / i7-7500U class) |
| Cores / threads | 2 physical / 4 logical (Hyper-Threading) |
| Clock | low base clock, higher single-core turbo (the turbo clock drops when more cores are busy) |
| L1 cache | 32 KB data + 32 KB instruction per core |
| L2 cache | 256 KB per core |
| L3 cache | 3 MB (i5) or 4 MB (i7), shared |
| Memory | dual-channel DDR4-2133 / LPDDR3-1866 (Kaby Lake-U support) |
| Sockets / NUMA nodes | 1 socket, 1 NUMA node |
| TDP | 15 W (laptop) |
| OS / Python | Windows, Python 3.15.0, numpy 2.5.4, start method = spawn |

## 3. Results

Benchmark settings: k = 30,000,000 points per worker, 5 runs per level.

| P | Mean T (s) | Std T (s) | Scaled S (mean ± SEM) | E = S/P | Gustafson fit | Pool start (s) |
|---|---|---|---|---|---|---|
| 1 | 1.0132 | 0.0569 | 1.002 ± 0.024 | 1.002 | 1.000 | 0.046 |
| 2 | 1.4107 | 0.0113 | 1.436 ± 0.005 | 0.718 | 1.309 | 0.020 |
| 3 | 1.7860 | 0.0906 | 1.705 ± 0.036 | 0.568 | 1.619 | 0.045 |
| 4 | 2.2219 | 0.1257 | 1.828 ± 0.043 | 0.457 | 1.928 | 0.066 |
| 8 (oversub., not in fit) | 4.4593 | 0.3107 | 1.824 ± 0.052 | 0.228 | 3.166 | 0.147 |

From the fit (P = 1…4) I got **α_observed = 0.6906 ± 0.0135**, with R² = 0.9818.

If I put the same α into Amdahl's law, it gives only S(4) = 1/(0.6906 + 0.3094/4) ≈ 1.30. My measured value at P = 4 is 1.83, so Amdahl is clearly too low here.

To be honest, α = 0.69 looked strange to me at first. My code has almost no serial part: every worker just computes its own integral and sends back one number. So this α is not a "real" serial fraction of the program. It mostly shows the limits of my laptop, which I explain below.

## 4. Why the measured points deviate from the theory

**a) Turbo boost and the 15 W power limit (the main reason at P = 2).**
With two physical cores I expected S to be close to 2, but I only got 1.436 (E = 0.718). The run time went up from 1.01 s to 1.41 s, even though each worker had the same amount of work. I think the reason is turbo boost. When only one core is busy, the CPU can run it at a high clock. When both cores are busy, the laptop has to share its 15 W power budget, so the clock goes down and every worker becomes slower. In the formula this looks like a serial fraction, but it isn't one.

**b) Physical vs. logical cores (P = 3 and P = 4).**
At P = 3 and P = 4, two processes have to share one physical core through Hyper-Threading. They use the same FP/AVX units and the same L1/L2 cache, so they slow each other down. You can see this in the numbers: going from 2 to 3 processes adds only +0.27 to the speedup, and going from 3 to 4 adds only +0.12. The times also become less stable (std 0.09–0.13 s, compared to 0.01 s at P = 2).

**c) Oversubscription (P = 8).**
My laptop has only 4 hardware threads, so with 8 processes they just take turns. The time almost exactly doubled (2.22 s → 4.46 s), and the speedup stayed the same (1.828 → 1.824). This is time-sharing, not a serial part, so I did not use P = 8 in the fit. Still, it is a useful point, because it shows that the real maximum throughput of this machine is about 1.8×.

**Thermal throttling.** The standard deviation gets bigger as P grows (0.011 s at P = 2, 0.311 s at P = 8). In my opinion this is a typical sign of a laptop that heats up during long all-core runs and keeps changing its clock speed.

**d) Memory bandwidth.**
Each worker works on chunks of about 8 MB, which is more than the whole L3 cache (3–4 MB). So the data has to come from RAM, and all cores share the same two memory channels. When all of them read memory at the same time, they compete for bandwidth.

**e) NUMA boundaries.**
My laptop has just one socket and one NUMA node, so there is no NUMA effect in my results. On a dual-socket server it would be different: processes on the second socket would sometimes read memory from the other socket, which is slower, and the speedup would drop when P crosses the socket boundary.

**f) Python / OS overhead.**
`pool.map` has to pickle the arguments and results and send them through pipes between processes. Windows also runs background tasks. In my case these costs are small (only P short messages per run, and the pool start time is under 0.15 s), but they still add some noise.

## 5. Conclusion

In theory my benchmark is almost perfectly parallel, but on a 2-core / 4-thread laptop with a 15 W limit I still measured α = 0.69. The Gustafson line fits my data quite well (R² = 0.98), but the large α comes from the hardware and not from the code: the clock drops under load, Hyper-Threading shares the execution units, the laptop heats up, and the cores share memory bandwidth. Amdahl's curve with the same α (S(4) ≈ 1.30) stays below my measured points, so for weak scaling Gustafson's model is clearly the better reference. I expect that on a server with many physical cores and a stable clock, the measured α would be much smaller.
