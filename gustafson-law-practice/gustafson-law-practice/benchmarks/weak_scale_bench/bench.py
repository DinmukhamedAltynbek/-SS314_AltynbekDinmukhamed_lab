#!/usr/bin/env python3
"""
Task 22/23 - Empirical weak-scaling benchmark (Python multiprocessing).

Workload: midpoint numerical integration of f(x) = sqrt(1 + x^2) * cos(x)
Weak scaling: every worker integrates its OWN k sample points (k is constant),
so total work = P * k grows with the number of workers P.

For each P the pool is started once and warmed up; only the parallel map
(dispatch + compute + gather) is timed. Pool start-up time is logged separately.

Usage:
    python bench.py                       # P = 1..max cores (+ oversubscribed to reach 5 levels), 5 runs each
    python bench.py --k 30000000 --runs 5
    python bench.py --procs 1 2 3 4 6 8   # custom P list
    python bench.py --quick               # small k for a quick test
"""
import argparse
import csv
import os
import platform
import statistics
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")       # keep numpy single-threaded per worker
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import multiprocessing as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(os.path.dirname(HERE), "results.csv")
CHUNK = 1_000_000          # elements per numpy chunk (~8 MB per array) to keep memory small


def worker_integrate(args):
    """Integrate f on this worker's own interval [rank, rank+1) with k midpoints."""
    rank, k = args
    h = 1.0 / k
    acc = 0.0
    for start in range(0, k, CHUNK):
        n = min(CHUNK, k - start)
        x = rank + (np.arange(start, start + n, dtype=np.float64) + 0.5) * h
        acc += float(np.sum(np.sqrt(1.0 + x * x) * np.cos(x)))
    return acc * h


def default_levels(max_hw, min_levels=5):
    """1..max_hw; on small machines add oversubscribed levels (2x, 3x ... cores) to reach 5."""
    levels = list(range(1, max_hw + 1))
    m = 2
    while len(levels) < min_levels:
        levels.append(max_hw * m)
        m += 1
    return levels


def run_level(p, k, runs):
    t0 = time.perf_counter()
    with mp.Pool(processes=p) as pool:
        startup = time.perf_counter() - t0
        pool.map(worker_integrate, [(r, 1000) for r in range(p)])     # warm-up (imports, page faults)
        times, checks = [], []
        for _ in range(runs):
            ts = time.perf_counter()
            parts = pool.map(worker_integrate, [(r, k) for r in range(p)], chunksize=1)
            times.append(time.perf_counter() - ts)
            checks.append(sum(parts))
    return startup, times, checks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--k", type=int, default=30_000_000, help="points per worker (constant)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--procs", type=int, nargs="+", default=None)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--quick", action="store_true", help="k = 2,000,000 for a fast smoke test")
    args = ap.parse_args()
    if args.quick:
        args.k = 2_000_000

    max_hw = os.cpu_count() or 1
    levels = args.procs or default_levels(max_hw)

    print("=" * 70)
    print(f"Weak-scaling benchmark | k = {args.k:,} points/worker | runs = {args.runs}")
    print(f"Host: {platform.processor() or platform.machine()} | logical cores = {max_hw}")
    print(f"Python {sys.version.split()[0]} | numpy {np.__version__} | start method = {mp.get_start_method()}")
    print(f"P levels: {levels}")
    print("=" * 70)

    rows = []
    t1_mean = None
    for p in levels:
        startup, times, checks = run_level(p, args.k, args.runs)
        mean = statistics.mean(times)
        sd = statistics.stdev(times) if len(times) > 1 else 0.0
        if p == 1:
            t1_mean = mean
        scaled = p * t1_mean / mean if t1_mean else float("nan")
        print(f"P={p:3d} | mean T={mean:8.4f}s  sd={sd:.4f}  | scaled S={scaled:7.3f} "
              f"| E={scaled / p:6.3f} | pool start={startup:.3f}s"
              + ("  [oversubscribed]" if p > max_hw else ""))
        for i, (t, c) in enumerate(zip(times, checks), start=1):
            rows.append({
                "p": p, "run": i, "wall_time_s": f"{t:.6f}",
                "k_per_worker": args.k, "total_points": p * args.k,
                "pool_startup_s": f"{startup:.6f}", "checksum": f"{c:.10f}",
                "oversubscribed": int(p > max_hw), "logical_cores": max_hw,
                "cpu": platform.processor() or platform.machine(),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    os.makedirs(os.path.dirname(os.path.abspath(args.csv)), exist_ok=True)
    with open(args.csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\n[+] {len(rows)} rows -> {args.csv}")
    print("[+] Next: python ../fit_gustafson.py")


if __name__ == "__main__":
    mp.freeze_support()
    main()
