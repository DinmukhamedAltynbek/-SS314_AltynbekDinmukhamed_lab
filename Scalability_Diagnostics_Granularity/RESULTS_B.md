RESULTS_B --- Scalability Diagnostics: Granularity & IPC Contention
1. Experimental Environment
- Operating System: Windows
- CPU: Intel64 Family 6 Model 142 Stepping 9, GenuineIntel
- Logical CPU count: 4
- Programming Language: Python
- Multiprocessing library: multiprocessing
- Tested worker counts: 1, 2, 4, 8
2. Experiment A --- Granularity Trap
Objective: Compare fine-grained and coarse-grained task distribution
using different chunk sizes.
- Total items: 1,000,000
- Worker counts: 1, 2, 4, 8
- Chunk sizes: 1 and 10,000
Results
Chunk size   Processes (P)   Time (s)   Speedup   Efficiency

         1               1     99.815     1.00x         100%
         1               2    140.480     0.71x       35.53%
         1               4    129.103     0.77x       19.33%
         1               8    136.952     0.73x        9.11%
    10,000               1     14.651     1.00x         100%
    10,000               2      8.693     1.69x       84.27%
    10,000               4      5.835     2.51x       62.78%
    10,000               8      6.158     2.38x       29.74%
Analysis
With a chunk size of 1, execution became slower when additional
processes were introduced. The overhead of distributing and scheduling
very small tasks outweighed the benefit of parallel execution.

With a chunk size of 10,000, performance improved considerably. The best
execution time was 5.835 seconds with four processes, achieving a
speedup of 2.51x.

Conclusion: Coarse-grained task distribution was significantly more
efficient than fine-grained distribution for this workload.
3. Experiment B --- Queue Contention
Objective: Demonstrate the performance impact of shared
multiprocessing.Queue contention.
- Total items: 400,000
- Worker counts: 1, 2, 4, 8
- Communication pattern: one queue message per item
Results
Processes (P)   Time (s)   Speedup   Efficiency   Karp-Flatt

            1      7.119    1.000x      100.00%          ---
            2     49.176    0.145x        7.24%      12.8157
            4     55.866    0.127x        3.19%      10.1301
            8     56.872    0.125x        1.56%       8.9874
Analysis
The experiment demonstrated severe contention caused by sending every
individual result through a shared multiprocessing queue.

Execution time increased from 7.119 seconds with one process to 56.872
seconds with eight processes. Speedup values below 1 indicate negative
scaling: adding workers made the program slower.

Conclusion: Frequent inter-process communication through a shared
queue can become a major performance bottleneck.
4. Experiment C --- Buffered Batch Processing
Objective: Reduce communication overhead by aggregating results
locally before sending them through the shared queue.
- Total items: 10,000,000
- Batch size: 10,000
- Worker counts: 1, 2, 4, 8
Results
Processes (P)   Time (s)   Speedup   Efficiency   Karp-Flatt

            1      1.125    1.000x      100.00%          ---
            2      0.850    1.324x       66.19%       0.5107
            4      0.849    1.324x       33.10%       0.6738
            8      1.129    0.996x       12.45%       1.0047
Analysis
Buffering reduced the number of messages sent through the shared queue.
Each worker accumulated values locally and sent a batch sum instead of
sending every individual value.

The best measured performance was achieved with four processes, taking
0.849 seconds. Increasing the number of processes to eight did not
improve performance.

The expected target of speedup greater than 5.0 at eight processes was
not achieved on this system.

Conclusion: Batching reduces communication overhead, but the
performance benefit depends on the workload and available hardware
resources.
5. Overall Comparison
  Experiment              Main observation        Best measured result
  A --- Fine-grained      Scheduling overhead     P=1 was fastest
(chunksize=1)         caused negative scaling 

  A --- Coarse-grained    Larger chunks improved  2.51x speedup at P=4
(chunksize=10000)     performance             

  B --- Queue Contention  Shared queue became a   P=1 was fastest
bottleneck              
C --- Buffered Batch    Batching reduced        0.849 s at P=4
communication overhead
6. Final Conclusion
The experiments demonstrate that multiprocessing performance depends not
only on the number of processes but also on task granularity and
communication overhead.

Experiment A showed that coarse-grained task distribution can
significantly improve performance compared with very small tasks.

Experiment B demonstrated that excessive communication through a shared
queue can cause severe contention and negative scaling.

Experiment C showed that local buffering reduces the number of queue
operations. However, adding more processes does not always improve
performance, especially when the workload is relatively simple.

Overall, efficient parallel programs require a balance between
computation, task distribution, synchronization, and inter-process
communication.

All experiments produced consistent checksums across their tested worker
counts: - Experiment A: 131434424 for all tested configurations. -
Experiment B: 1199997 for all tested process counts. - Experiment C:
29999994 for all tested process counts.

The results are empirical measurements from this machine. The expected
performance targets are not guaranteed and should not be represented as
achieved when the measurements do not meet them.