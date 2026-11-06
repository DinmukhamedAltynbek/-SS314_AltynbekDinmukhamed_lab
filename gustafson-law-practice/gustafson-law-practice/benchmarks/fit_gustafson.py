#!/usr/bin/env python3
"""
Task 23/24 - Fit Gustafson's law to measured weak-scaling data and plot it.

Reads benchmarks/results.csv (from weak_scale_bench/bench.py) and:
  1. computes mean / std / standard error of wall time per P,
  2. computes scaled speedup S(P) = P * T(1) / T(P) for every run,
  3. fits alpha by least squares on  S(P) = P - alpha (P - 1)
     ->  (P - S) = alpha (P - 1)  ->  alpha = sum((P-1)(P-S)) / sum((P-1)^2)
  4. plots ideal, Gustafson fit, measured points (+ error bars), Amdahl with the same alpha.

Oversubscribed levels (P > logical cores) are plotted but NOT used in the fit
(their slowdown comes from time-sharing cores, not from a serial fraction).

Usage:
    python fit_gustafson.py
    python fit_gustafson.py --csv results.csv --include-oversub
"""
import argparse
import csv
import json
import math
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(path):
    data = defaultdict(list)
    meta = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            p = int(row["p"])
            data[p].append(float(row["wall_time_s"]))
            meta[p] = int(row.get("oversubscribed", 0))
            meta["cpu"] = row.get("cpu", "")
            meta["logical_cores"] = int(row.get("logical_cores", 0) or 0)
    return dict(sorted((k, v) for k, v in data.items())), meta


def summarize(data):
    t1 = np.mean(data[1])
    out = []
    for p, ts in data.items():
        ts = np.array(ts)
        s_runs = p * t1 / ts                         # scaled speedup per run
        n = len(ts)
        out.append({
            "p": p, "n": n,
            "t_mean": ts.mean(), "t_std": ts.std(ddof=1) if n > 1 else 0.0,
            "s_mean": s_runs.mean(),
            "s_std": s_runs.std(ddof=1) if n > 1 else 0.0,
            "s_sem": (s_runs.std(ddof=1) / math.sqrt(n)) if n > 1 else 0.0,
            "s_runs": s_runs,
        })
    return out


def fit_alpha(stats, use):
    """Least-squares alpha using every individual run (not only means)."""
    x, y = [], []
    for st in stats:
        if st["p"] in use:
            for s in st["s_runs"]:
                x.append(st["p"] - 1.0)
                y.append(st["p"] - s)
    x, y = np.array(x), np.array(y)
    if not np.any(x > 0):
        raise SystemExit("Need at least one P > 1 to fit alpha.")
    alpha = float(np.sum(x * y) / np.sum(x * x))
    resid = y - alpha * x
    dof = max(len(x) - 1, 1)
    se = float(math.sqrt(np.sum(resid ** 2) / dof / np.sum(x * x)))
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = float(1 - np.sum(resid ** 2) / ss_tot) if ss_tot > 0 else float("nan")
    return alpha, se, r2


def plot(stats, alpha, meta, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ps = np.array([st["p"] for st in stats])
    pgrid = np.linspace(1, ps.max(), 200)
    fig, ax = plt.subplots(figsize=(8, 5.5))

    ax.plot(pgrid, pgrid, "k:", lw=1.3, label="(1) Ideal linear S = P")
    ax.plot(pgrid, pgrid - alpha * (pgrid - 1), "-", color="tab:blue", lw=2,
            label=f"(2) Gustafson fit, α = {alpha:.4f}")
    a_clip = min(max(alpha, 1e-9), 1.0)
    ax.plot(pgrid, 1 / (a_clip + (1 - a_clip) / pgrid), "--", color="tab:red", lw=1.8,
            label=f"(4) Amdahl, s = {alpha:.4f}")

    norm = [st for st in stats if not meta.get(st["p"], 0)]
    over = [st for st in stats if meta.get(st["p"], 0)]
    ax.errorbar([st["p"] for st in norm], [st["s_mean"] for st in norm],
                yerr=[st["s_sem"] for st in norm], fmt="o", color="tab:green",
                capsize=5, ms=7, label="(3) Measured (mean ± SEM)")
    if over:
        ax.errorbar([st["p"] for st in over], [st["s_mean"] for st in over],
                    yerr=[st["s_sem"] for st in over], fmt="s", color="tab:orange",
                    mfc="none", capsize=5, ms=7, label="Measured, oversubscribed (not in fit)")
    if meta.get("logical_cores"):
        ax.axvline(meta["logical_cores"], color="gray", lw=0.8, alpha=0.6)
        ax.text(meta["logical_cores"], 0.02, " logical cores", transform=ax.get_xaxis_transform(),
                fontsize=8, color="gray", va="bottom")

    ax.set_xlabel("Number of worker processes P")
    ax.set_ylabel("Scaled speedup S(P) = P·T(1)/T(P)")
    ax.set_title(f"Weak scaling: empirical vs theoretical\n{meta.get('cpu', '')}", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    fig.savefig(out_png, dpi=300)
    fig.savefig(os.path.splitext(out_png)[0] + ".pdf")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=os.path.join(HERE, "results.csv"))
    ap.add_argument("--plot", default=os.path.join(ROOT, "plots", "scaling_comparison.png"))
    ap.add_argument("--json", default=os.path.join(HERE, "fit_result.json"))
    ap.add_argument("--include-oversub", action="store_true")
    args = ap.parse_args()

    data, meta = load(args.csv)
    if 1 not in data:
        raise SystemExit("results.csv must contain P = 1 (baseline).")
    stats = summarize(data)
    use = {st["p"] for st in stats if args.include_oversub or not meta.get(st["p"], 0)}
    alpha, se, r2 = fit_alpha(stats, use)

    print(f"{'P':>4} {'n':>3} {'T mean (s)':>11} {'T std':>8} {'S mean':>8} {'S SEM':>7} {'E':>6} {'Gust fit':>9}")
    for st in stats:
        flag = "" if st["p"] in use else "  (oversub, excluded)"
        print(f"{st['p']:4d} {st['n']:3d} {st['t_mean']:11.4f} {st['t_std']:8.4f} "
              f"{st['s_mean']:8.3f} {st['s_sem']:7.3f} {st['s_mean'] / st['p']:6.3f} "
              f"{st['p'] - alpha * (st['p'] - 1):9.3f}{flag}")
    print(f"\nalpha_observed = {alpha:.5f} ± {se:.5f} (std. error), R² = {r2:.4f}")

    plot(stats, alpha, meta, args.plot)
    print(f"[+] plot -> {args.plot} (+ .pdf)")

    with open(args.json, "w") as f:
        json.dump({
            "alpha_observed": alpha, "alpha_std_error": se, "r_squared": r2,
            "levels_used_in_fit": sorted(use), "cpu": meta.get("cpu"),
            "logical_cores": meta.get("logical_cores"),
            "table": [{k: (float(v) if k != "s_runs" else None) for k, v in st.items() if k != "s_runs"}
                      for st in stats],
        }, f, indent=2)
    print(f"[+] fit summary -> {args.json}")


if __name__ == "__main__":
    main()
