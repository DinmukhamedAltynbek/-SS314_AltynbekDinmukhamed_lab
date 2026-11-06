# Task 20 — Graph Analytics (BFS, PageRank) and Weak Scaling

## 1. The ideal case: dense linear algebra

Dense GEMM or LU has:
- **regular memory access** (blocks, good cache reuse),
- **predictable work**, so every block takes the same time,
- **communication that is structured and known in advance**,
- **high arithmetic intensity** (many flops per byte).

Weak scaling works because each processor's work and messages are the same at every P.

## 2. Why graphs are different

### a) Irregular memory access
BFS and PageRank follow edges to random vertices. Almost every access is a cache miss, so performance is limited by **memory latency**, not flops. With more data per node, the cache hit rate does not improve. Arithmetic intensity is very low (about 1 operation per 8–16 bytes).

### b) Power-law degree distribution
In real graphs (social networks, the web) a few vertices have millions of edges, while most have very few. If we split vertices equally, some partitions get far more edges → **load imbalance**. The slowest node sets the time, so the effective α grows with P.

### c) Frontier imbalance in BFS
The frontier size changes a lot between levels: tiny at the start, huge in the middle, tiny again at the end. In small levels most processors have no work, but they still wait at the **barrier** after each level. The number of levels depends on the graph diameter, not on P.

### d) Data-dependent communication
Which processor needs which message is known only at run time. Edges cross partitions randomly, so with P partitions about `(P − 1)/P` of all edges are **remote**. More processors → more messages, and they look like **all-to-all** traffic. Total traffic grows faster than the network bisection bandwidth.

### e) Partitioning is hard
Good partitioning (fewer cut edges) is NP-hard. Good heuristics (METIS) take a lot of time and work badly for power-law graphs.

## 3. Scaling behaviour in numbers

| Property | Dense GEMM | BFS / PageRank on power-law graphs |
|---|---|---|
| Work per element | O(N) flops per element (high) | O(1) per edge (low) |
| Memory pattern | regular, cache friendly | random, cache misses |
| Load balance | perfect | poor (high-degree vertices) |
| Communication | structured, ∝ N²/√P | all-to-all, ∝ edges · (P − 1)/P |
| Synchronization | few, predictable | barrier every level / iteration |
| Typical weak-scaling efficiency | high, close to ideal | much lower, falls fast with P |

(This is the reason the Graph500 benchmark exists separately from LINPACK: it ranks machines by TEPS — traversed edges per second — and its numbers are far below peak.)

## 4. What helps

- **Direction-optimizing BFS** (switch between top-down and bottom-up search).
- **2D partitioning** of the adjacency matrix. This limits communication to √P processors.
- **Vertex delegation**: copy high-degree vertices to many nodes.
- **Asynchronous / message aggregation** to reduce latency and the number of barriers.

## 5. Conclusion

Gustafson's law assumes that more data per processor gives the same time, because the work is uniform and the communication is local. Graph analytics breaks these assumptions: work is skewed, access is random, and communication grows with P. So the effective serial (waiting) fraction grows with machine size, and weak scaling is much worse than for regular dense linear algebra.
