
import multiprocessing as mp
import ctypes
import time
import csv
import os

# Experiment configuration
ITERATIONS = 5_000_000
WORKERS = [1, 2, 4, 8]

OUTPUT_FILE = os.path.join(
    "results",
    "false_sharing_karp_flatt.tsv"
)


# --------------------------------------------------
# 1. UNPADDED: adjacent counters share cache lines
# --------------------------------------------------

def worker_unpadded(counter_array, worker_id, iterations):
    for _ in range(iterations):
        counter_array[worker_id] += 1


# --------------------------------------------------
# 2. PADDED: each counter is 64 bytes apart
# 8 integers * 8 bytes = 64 bytes
# --------------------------------------------------

def worker_padded(counter_array, worker_id, iterations):
    index = worker_id * 8

    for _ in range(iterations):
        counter_array[index] += 1


# --------------------------------------------------
# 3. PRIVATIZED: local counter, one shared write
# --------------------------------------------------

def worker_privatized(counter_array, worker_id, iterations):
    local_counter = 0

    for _ in range(iterations):
        local_counter += 1

    # One synchronized write after local computation
    counter_array[worker_id] = local_counter


# --------------------------------------------------
# Benchmark one implementation with P processes
# --------------------------------------------------

def run_benchmark(variant, processes):
    ctx = mp.get_context()

    if variant == "unpadded":
        shared_arr = ctx.RawArray(ctypes.c_int64, 8)
        target = worker_unpadded

    elif variant == "padded":
        shared_arr = ctx.RawArray(
            ctypes.c_int64,
            processes * 8
        )
        target = worker_padded

    elif variant == "privatized":
        # Synchronized shared array:
        # each worker writes its final result once.
        shared_arr = ctx.Array(
            ctypes.c_int64,
            processes,
            lock=True
        )
        target = worker_privatized

    else:
        raise ValueError("Unknown benchmark variant")

    workers = []

    start = time.perf_counter()

    for worker_id in range(processes):
        process = ctx.Process(
            target=target,
            args=(shared_arr, worker_id, ITERATIONS)
        )
        workers.append(process)
        process.start()

    for process in workers:
        process.join()

        if process.exitcode != 0:
            raise RuntimeError(
                f"Worker failed with exit code {process.exitcode}"
            )

    elapsed = time.perf_counter() - start

    # Read the counters and verify correctness
    if variant == "unpadded":
        counters = [
            shared_arr[i] for i in range(processes)
        ]

    elif variant == "padded":
        counters = [
            shared_arr[i * 8] for i in range(processes)
        ]

    else:
        counters = [
            shared_arr[i] for i in range(processes)
        ]

    expected = [ITERATIONS] * processes

    if counters != expected:
        raise RuntimeError(
            f"Incorrect counters: {counters}, expected: {expected}"
        )

    return elapsed, sum(counters)


# --------------------------------------------------
# Karp-Flatt metric
# --------------------------------------------------

def karp_flatt(t1, tp, p):
    if p == 1:
        return 0.0

    return ((p * tp / t1) - 1) / (p - 1)


# --------------------------------------------------
# Main experiment
# --------------------------------------------------

def main():
    os.makedirs("results", exist_ok=True)

    variants = [
        "unpadded",
        "padded",
        "privatized"
    ]

    all_results = []

    print("=== TASK 2: FALSE SHARING DIAGNOSTICS ===")
    print("Iterations per worker:", ITERATIONS)
    print("Worker counts:", WORKERS)
    print("Logical CPUs:", os.cpu_count())

    for variant in variants:
        print(f"\n=== {variant.upper()} ===")

        runtimes = {}

        for p in WORKERS:
            elapsed, checksum = run_benchmark(variant, p)
            runtimes[p] = elapsed

            print(
                f"P={p} | Time={elapsed:.4f}s "
                f"| Checksum={checksum}"
            )

        t1 = runtimes[1]

        print("\nScaling analysis:")

        for p in WORKERS:
            tp = runtimes[p]
            speedup = t1 / tp
            efficiency = speedup / p
            e = karp_flatt(t1, tp, p)

            print(
                f"P={p} | Speedup={speedup:.3f}x "
                f"| Efficiency={efficiency * 100:.2f}% "
                f"| Karp-Flatt={e:.4f}"
            )

            all_results.append({
                "variant": variant,
                "processes": p,
                "iterations_per_worker": ITERATIONS,
                "runtime_seconds": f"{tp:.6f}",
                "speedup": f"{speedup:.4f}",
                "efficiency": f"{efficiency:.4f}",
                "karp_flatt": "" if p == 1 else f"{e:.6f}",
                "checksum": p * ITERATIONS
            })

    # Save all measurements as TSV
    fieldnames = [
        "variant",
        "processes",
        "iterations_per_worker",
        "runtime_seconds",
        "speedup",
        "efficiency",
        "karp_flatt",
        "checksum"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter="\t"
        )
        writer.writeheader()
        writer.writerows(all_results)

    print("\n=== EXPERIMENT COMPLETED ===")
    print("Results saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    mp.freeze_support()
    main()
