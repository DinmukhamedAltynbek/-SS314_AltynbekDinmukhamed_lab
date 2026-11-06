# Task 11 — Sun–Ni Memory-Bounded Speedup vs. Gustafson

## 1. The Sun–Ni model (1990/1993)

Sun and Ni asked a different question: *"How big can the problem get if we use **all the memory** of P nodes?"*

Let `s` be the serial fraction of the base problem on one node, and let `G(P)` show how much the parallel work grows when memory grows P times:

```
S_SN(P) = (s + (1 − s)·G(P)) / (s + (1 − s)·G(P)/P)
```

## 2. It includes both classic laws

| G(P) | Model | Result |
|---|---|---|
| `G = 1` | work does not grow | `1/(s + (1 − s)/P)` = **Amdahl** |
| `G = P` | work grows like memory | `s + (1 − s)P` = **Gustafson** |
| `G > P` | work grows faster than memory | above Gustafson |
| `1 < G < P` | work grows slower than memory | between Amdahl and Gustafson |

So Gustafson is just the special case where work ∝ memory ∝ P.

## 3. How G(P) comes from the algorithm

If the memory is `M ∝ N^m` and the work is `W ∝ N^w`, then using P times more memory gives

```
N ∝ P^(1/m),    W ∝ P^(w/m),    so G(P) = P^(w/m)
```

| Algorithm | Memory | Work | G(P) |
|---|---|---|---|
| Vector add, Monte Carlo, stencil (1 sweep) | N | N | P |
| Dense matrix multiply (GEMM) | N² | N³ | P^1.5 |
| Dense LU | N² | N³ | P^1.5 |
| Work grows slower than memory (e.g. a big lookup table used rarely) | N | √N | P^0.5 |

## 4. Numbers (s = 0.04, P = 1024)

| G(P) | Sun–Ni speedup |
|---|---|
| 1 (Amdahl) | 24.4 |
| P^0.5 | 439.4 |
| P (Gustafson) | 983.1 |
| P^1.5 (GEMM) | 1022.7 |

## 5. When Gustafson is wrong

**Gustafson overestimates throughput when:**
- the work cannot grow as fast as P because memory per node is too small, or the data does not fit (`G(P) < P`);
- the problem has a natural maximum size (for example, the weather model is already at the resolution of the input data);
- communication, synchronization or memory bandwidth grows with P. These effects are in neither model, but Gustafson hides them because it assumes constant time.

**Gustafson underestimates throughput when:**
- work grows faster than memory (`G(P) > P`, for example GEMM, LU and N-body). Filling the memory gives more than P times more work, so the speedup is even closer to P.
- *Note:* in this case the run time is **not** constant. It grows like `G(P)/P = P^0.5` for GEMM. The higher speedup costs a longer wall time, and that breaks Gustafson's fixed-time premise.

## 6. Conclusion

Sun–Ni is the more general model. Gustafson is correct only when work grows exactly like memory. For O(N) algorithms the two give the same answer. For O(N³)-type kernels, Sun–Ni is the better guide, but the user must accept a longer run time.
