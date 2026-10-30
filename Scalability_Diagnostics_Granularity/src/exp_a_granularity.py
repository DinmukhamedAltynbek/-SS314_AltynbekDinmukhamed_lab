
import time
import multiprocessing as mp

TOTAL_ITEMS = 1_000_000
WORKERS = [1, 2, 4, 8]
CHUNK_SIZES = [1, 10_000]


def collatz_steps(n):
    steps = 0

    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

        steps += 1

    return steps


def run_granularity(workers, total_items, chunk_size):
    numbers = range(1, total_items + 1)

    start = time.perf_counter()

    with mp.Pool(processes=workers) as pool:
        results = pool.map(
            collatz_steps,
            numbers,
            chunksize=chunk_size
        )

    elapsed = time.perf_counter() - start

    return elapsed, sum(results)


def karp_flatt(t1, tp, p):
    return ((p * tp / t1) - 1) / (p - 1)


def main():

    print("=== EXPERIMENT A: GRANULARITY TRAP ===")
    print("Total items:", TOTAL_ITEMS)

    all_results = {}

    for chunk_size in CHUNK_SIZES:

        print(f"\n--- CHUNKSIZE = {chunk_size} ---")

        for p in WORKERS:

            elapsed, checksum = run_granularity(
                p,
                TOTAL_ITEMS,
                chunk_size
            )

            all_results[(chunk_size, p)] = elapsed

            print(
                f"P={p} | Time={elapsed:.3f}s "
                f"| Checksum={checksum}"
            )

        t1 = all_results[(chunk_size, 1)]

        print("\nScaling Analysis:")

        for p in [2, 4, 8]:

            tp = all_results[(chunk_size, p)]

            speedup = t1 / tp
            efficiency = speedup / p * 100
            e = karp_flatt(t1, tp, p)

            print(
                f"P={p} | Speedup={speedup:.2f}x "
                f"| Efficiency={efficiency:.2f}% "
                f"| Karp-Flatt={e:.4f}"
            )


if __name__ == "__main__":
    mp.freeze_support()
    main()
