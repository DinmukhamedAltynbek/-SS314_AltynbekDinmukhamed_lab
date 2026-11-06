# Task 16 — Dense Matrix Multiplication (GEMM) Scaling

## 1. Cost model

- Computation: `2N³` flops, so `T_comp ∝ N³`.
- Memory: 3 matrices × `N²` × 8 B = `24N²` bytes.

## 2. Constant parallel run time

With an ideal distribution, the time on P processors is

```
T(P) = c · N³ / P
```

Gustafson needs `T(P) = T(1)`:

```
N(P)³ / P = N(1)³    ⇒    N(P) = N(1) · P^(1/3)
```

**Proof:** put `N = N(1)·P^(1/3)` back in: `c·N(1)³·P/P = c·N(1)³ = T(1)` ✔ ∎

So the **matrix dimension must grow like the cube root of P**.

## 3. Results of this scaling

| Quantity | Growth |
|---|---|
| Work `N³` | ∝ P (good, this is Gustafson) |
| Total memory `N²` | ∝ P^(2/3) |
| Memory per processor `N²/P` | ∝ P^(−1/3), so it **goes down** |

Weak scaling for GEMM does **not** use all the memory. Each node gets fewer data, so caches work better, but the communication share grows. In SUMMA / Cannon the communication per processor is `∝ N²/√P`, and computation is `∝ N³/P`. Their ratio is `√P/N ∝ P^(1/6)`, which slowly gets worse.

## 4. Scaling targets (start: N = 1000 on 1 processor)

| P | N = 1000·P^(1/3) | Work (×) | Total memory (24N² B) | Memory per proc |
|---|---|---|---|---|
| 1 | 1,000 | 1 | 24 MB | 24 MB |
| 8 | 2,000 | 8 | 96 MB | 12 MB |
| 64 | 4,000 | 64 | 384 MB | 6 MB |
| 512 | 8,000 | 512 | 1,536 MB | 3 MB |
| 4096 | 16,000 | 4096 | 6,144 MB | 1.5 MB |

## 5. Comparison: memory-bounded scaling

If we fill the memory instead (`N²/P` constant, so `N ∝ P^(1/2)`):
- the work grows like `P^(3/2)`,
- the time grows like `P^(1/2)`, which breaks Gustafson's fixed-time rule (see Task 11).
