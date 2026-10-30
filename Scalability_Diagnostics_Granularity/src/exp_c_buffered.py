
import time
import multiprocessing as mp

TOTAL_ITEMS = 10_000_000
BATCH_SIZE = 10_000
WORKERS = [1, 2, 4, 8]


def buffered_worker(out_queue, start_index, items_per_worker):

    buffer = []

    for i in range(start_index, start_index + items_per_worker):

        buffer.append(i % 7)

        if len(buffer) >= BATCH_SIZE:
            out_queue.put(sum(buffer))
            buffer.clear()

    if buffer:
        out_queue.put(sum(buffer))

    out_queue.put(None)


def run_buffered(p, total_items=TOTAL_ITEMS):

    q = mp.Queue()

    items_per_worker = total_items // p

    workers = [
        mp.Process(
            target=buffered_worker,
            args=(q, worker_id * items_per_worker, items_per_worker)
        )
        for worker_id in range(p)
    ]

    start = time.perf_counter()

    for w in workers:
        w.start()

    total_sum = 0
    active = p

    while active > 0:

        value = q.get()

        if value is None:
            active -= 1
        else:
            total_sum += value

    for w in workers:
        w.join()

    elapsed = time.perf_counter() - start

    q.close()
    q.join_thread()

    return elapsed, total_sum


def karp_flatt(t1, tp, p):

    return ((p * tp / t1) - 1.0) / (p - 1)


def main():

    print("=== EXPERIMENT C: BUFFERED BATCH ===")
    print("Total items:", TOTAL_ITEMS)
    print("Batch size:", BATCH_SIZE)

    runtimes = {}

    for p in WORKERS:

        elapsed, checksum = run_buffered(p)

        runtimes[p] = elapsed

        print(
            f"P={p} | Time={elapsed:.3f}s "
            f"| Checksum={checksum}"
        )

    t1 = runtimes[1]

    print("\n--- BUFFERED KARР-FLATT ANALYSIS ---")

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
