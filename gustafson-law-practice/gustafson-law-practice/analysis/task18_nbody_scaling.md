# Task 18 — N-Body: Direct O(N²) vs. Barnes–Hut O(N log N)

## 1. Goal

Keep the time per iteration constant while P grows (Gustafson). How fast can N grow, and what happens to the serial/parallel balance?

## 2. Direct all-pairs method

- Work per step: `W = c·N²`. With ideal division, `T = c·N²/P`.
- Constant time: `N²/P = const` ⇒ **`N ∝ P^(1/2)`**.
- Memory per processor: `N/P ∝ P^(−1/2)`, so it goes **down**.
- Communication: every processor needs all N positions each step (all-gather), so the data received per processor is `∝ N ∝ P^(1/2)`. Computation per processor is constant, so **the comm/comp ratio grows like `P^(1/2)`**.
- Serial part: integration and I/O are `O(N)` and are small next to `N²`. So the *algorithmic* serial share drops like `1/N`, but the communication share grows.

| P | N (start N = 10,000) | Work per proc | Data received per proc |
|---|---|---|---|
| 1 | 10,000 | 1× | 1× |
| 64 | 80,000 | 1× | 8× |
| 1024 | 320,000 | 1× | 32× |

## 3. Barnes–Hut tree code

- Work per step: `W = c·N log N`. Constant time: `N log N / P = const` ⇒ **`N ≈ P`** (slightly less than P because of the log).
- Memory per processor: `N/P ≈ const`. This is close to ideal weak scaling.
- Serial or hard-to-parallelize parts:
  - **building the tree** (top levels are shared by everyone, about `O(log N)` depth),
  - **load balancing** (space-filling curve / ORB repartitioning),
  - **exchanging the "locally essential tree"** (`∝ log P` messages per process).
- These parts grow like `log N` or `log P`, so the effective α **grows slowly**.

## 4. Comparison of the serial/parallel shift

| Aspect | Direct O(N²) | Barnes–Hut O(N log N) |
|---|---|---|
| N growth for constant time | `P^(1/2)` | `≈ P / log P` |
| Memory per processor | falls | ≈ constant |
| Communication per processor | grows like `P^(1/2)` (all-gather) | grows like `log P` |
| Effective serial fraction α | algorithmic part ↓, communication ↑ fast | grows slowly (tree top + rebalance) |
| Fit to Gustafson | weak: N grows slowly, communication kills it | good: nearly linear |

## 5. Conclusion

- The direct method has a lot of computation per particle, so it is easy to keep cores busy at small P. But for constant time, the problem can only grow like `√P`, and the all-to-all data flow becomes the bottleneck.
- Barnes–Hut has less work per particle, so N can grow almost like P. The serial share comes from the tree build and rebalancing, and it grows slowly, like `log P`. For big machines Barnes–Hut is much closer to Gustafson's ideal, even though its fixed-size speedup at small P is lower.
