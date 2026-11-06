#!/usr/bin/env python3
"""
Task 21 - Parametric speedup simulator (Amdahl vs. Gustafson).

Models strong scaling (Amdahl) and weak scaling (Gustafson) for
1 <= P <= 65536 and 0.001 <= alpha <= 0.20, exports a CSV and draws overlay plots.

Usage:
    python simulator.py                                  # defaults
    python simulator.py --alphas 0.001 0.01 0.05 0.1 0.2 --pmax 65536
    python simulator.py --points 200 --csv out.csv --plot out.png
"""
import argparse
import csv
import os

import numpy as np

P_MIN, P_MAX = 1, 65536
A_MIN, A_MAX = 0.001, 0.20

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def amdahl_speedup(p, s):
    """Fixed-size speedup: 1 / (s + (1 - s)/P)."""
    p = np.asarray(p, dtype=np.float64)
    return 1.0 / (s + (1.0 - s) / p)


def gustafson_speedup(p, alpha):
    """Fixed-time (scaled) speedup: P - alpha (P - 1)."""
    p = np.asarray(p, dtype=np.float64)
    return p - alpha * (p - 1.0)


def processor_grid(pmax, points):
    """Powers of two plus a log-spaced grid, all integers in [1, pmax]."""
    pows = [2 ** i for i in range(0, int(np.log2(pmax)) + 1)]
    logs = np.unique(np.round(np.logspace(0, np.log10(pmax), points)).astype(int))
    grid = sorted(set(pows) | set(logs.tolist()) | {pmax})
    return np.array([p for p in grid if P_MIN <= p <= pmax], dtype=np.int64)


def simulate(p_values, alphas):
    rows = []
    for a in alphas:
        s_a = amdahl_speedup(p_values, a)
        s_g = gustafson_speedup(p_values, a)
        for p, sa, sg in zip(p_values, s_a, s_g):
            rows.append({
                "alpha": a,
                "p": int(p),
                "amdahl_speedup": round(float(sa), 6),
                "amdahl_efficiency": round(float(sa / p), 6),
                "gustafson_speedup": round(float(sg), 6),
                "gustafson_efficiency": round(float(sg / p), 6),
                "ratio_gustafson_over_amdahl": round(float(sg / sa), 6),
            })
    return rows


def write_csv(rows, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def plot(p_values, alphas, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = plt.cm.viridis(np.linspace(0.0, 0.85, len(alphas)))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    ax1.plot(p_values, p_values, "k:", lw=1.2, label="Ideal S = P")
    for a, c in zip(alphas, colors):
        ax1.plot(p_values, gustafson_speedup(p_values, a), "-", color=c, lw=1.8,
                 label=f"Gustafson α={a:g}")
        ax1.plot(p_values, amdahl_speedup(p_values, a), "--", color=c, lw=1.4,
                 label=f"Amdahl s={a:g}")
    ax1.set_xscale("log", base=2)
    ax1.set_yscale("log", base=2)
    ax1.set_xlabel("Processors P")
    ax1.set_ylabel("Speedup S(P)")
    ax1.set_title("Speedup: weak (solid) vs strong (dashed) scaling")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=7, ncol=2)

    for a, c in zip(alphas, colors):
        ax2.plot(p_values, gustafson_speedup(p_values, a) / p_values, "-", color=c, lw=1.8)
        ax2.plot(p_values, amdahl_speedup(p_values, a) / p_values, "--", color=c, lw=1.4)
    ax2.set_xscale("log", base=2)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel("Processors P")
    ax2.set_ylabel("Efficiency E(P) = S/P")
    ax2.set_title("Efficiency: Gustafson → 1-α, Amdahl → 0")
    ax2.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path, dpi=200)
    if path.endswith(".png"):
        fig.savefig(path[:-4] + ".pdf")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.001, 0.01, 0.05, 0.10, 0.20])
    ap.add_argument("--pmax", type=int, default=P_MAX)
    ap.add_argument("--points", type=int, default=120, help="log-spaced grid points")
    ap.add_argument("--csv", default=os.path.join(HERE, "simulator_output.csv"))
    ap.add_argument("--plot", default=os.path.join(ROOT, "plots", "simulator_overlay.png"))
    ap.add_argument("--no-plot", action="store_true")
    args = ap.parse_args()

    if not (P_MIN <= args.pmax <= P_MAX):
        ap.error(f"--pmax must be in [{P_MIN}, {P_MAX}]")
    for a in args.alphas:
        if not (A_MIN <= a <= A_MAX):
            ap.error(f"alpha {a} outside [{A_MIN}, {A_MAX}]")

    p_values = processor_grid(args.pmax, args.points)
    rows = simulate(p_values, args.alphas)
    write_csv(rows, args.csv)
    print(f"[+] {len(rows)} rows -> {args.csv}")

    # short console summary
    print(f"{'alpha':>7} {'P':>7} {'Amdahl':>10} {'Gustafson':>11}")
    for a in args.alphas:
        for p in (16, 1024, args.pmax):
            if p <= args.pmax:
                print(f"{a:7.3f} {p:7d} {amdahl_speedup(p, a):10.2f} {gustafson_speedup(p, a):11.2f}")

    if not args.no_plot:
        plot(p_values, args.alphas, args.plot)
        print(f"[+] plot -> {args.plot} (+ .pdf)")


if __name__ == "__main__":
    main()
