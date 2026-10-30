import time
import multiprocessing as mp

TOTAL_ITEMS = 400_000
WORKERS = [1, 2, 4, 8]


def queue_worker(out_queue, start_index, items_per_worker):
    for i in range(start_index, start_index + items_per_worker):
        out_queue.put(i % 7)


def run_queue_benchmark(p, total_items=TOTAL_ITEMS):
    if total_items % p != 0:
        raise ValueError("total_items must be divisible by p")

    q = mp.Queue()
    items_per_worker = total_items // p

    workers = [
        mp.Process(
            target=queue_worker,
            args=(q, worker_id * items_per_worker, items_per_worker)
        )
        for worker_id in range(p)
    ]

    start = time.perf_counter()

    for w in workers:
        w.start()

    collected = 0
    checksum = 0

    while collected < total_items:
        checksum += q.get()
        collected += 1

    for w in workers:
        w.join()

    elapsed = time.perf_counter() - start

    q.close()
    q.join_thread()

    return elapsed, checksum


def karp_flatt(t1, tp, p):
    return ((p * tp / t1) - 1.0) / (p - 1)


def main():
    print("=== EXPERIMENT B: QUEUE CONTENTION ===")
    print("Total items:", TOTAL_ITEMS)

    runtimes = {}

    for p in WORKERS:
        elapsed, checksum = run_queue_benchmark(p)
        runtimes[p] = elapsed

        print(
            f"P={p} | Time={elapsed:.3f}s "
            f"| Checksum={checksum}"
        )

    t1 = runtimes[1]


if __name__ == "__main__":
    mp.freeze_support()
    main()

    print("\n--- KARП-FLATT ANALYSIS ---")

    for p in [2, 4, 8]:

        tp = runtimes[p]

        speedup = t1 / tp
        efficiency = speedup / p * 100

        e = karp_flatt(t1, tp, p)

        print(
            f"P={p} | Speedup={speedup:.3f}x "
            f"| Efficiency={efficiency:.2f}% "
            f"| Karp-Flatt={e:.4f}"
        )


if __name__ == "__main__":
    mp.freeze_support()
    main()
