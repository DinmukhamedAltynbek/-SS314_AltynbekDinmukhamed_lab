# Weak-Scaling Benchmark Suite (Task 22)

A Python `multiprocessing` benchmark. Each worker does a **constant** amount of work: midpoint integration of `f(x) = sqrt(1 + x²)·cos(x)` with `k` points on its own interval. So the total work grows like `P·k` (weak scaling).

## Requirements

- Python 3.9+
- `pip install numpy matplotlib`

No compilation is needed.

## Run

```bash
cd benchmarks/weak_scale_bench
python bench.py                 # P = 1..max cores, 5 runs each, k = 30,000,000
python bench.py --quick         # quick smoke test (k = 2,000,000)
python bench.py --procs 1 2 3 4 8 --runs 5 --k 30000000
```

The output is `benchmarks/results.csv`, with one row per run.

Then fit and plot (Tasks 23–24):

```bash
cd ..
python fit_gustafson.py         # -> fit_result.json, plots/scaling_comparison.png/.pdf
```

## Design notes

- **P levels:** by default `1 … os.cpu_count()`. If this gives fewer than 5 levels (small laptops), oversubscribed levels (2×, 3× cores) are added. These are marked in the CSV and are **not** used in the fit.
- **Timing:** for each P the pool is created once and warmed up. After that only `pool.map` is timed (dispatch + compute + gather). The pool start-up time is saved separately in `pool_startup_s`. On Windows this matters, because `spawn` re-imports Python and numpy in every worker.
- **Single-threaded numpy:** `OMP_NUM_THREADS=1` etc. are set, so the only parallelism comes from processes.
- **Memory:** work is done in chunks of 1M elements (about 8 MB per array), so the data does not grow with k.
- **Run the script from a terminal**, not from Jupyter (multiprocessing on Windows/macOS needs a real `__main__`).
- Close other programs and keep the laptop on the charger during the run to reduce noise.
