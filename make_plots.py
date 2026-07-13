"""
make_plots.py
MSCS 532 Assignment 4
Frenie Labrador

Reads benchmark_results.csv and produces one line chart per input
distribution, saved into plots/.
"""

import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    data = defaultdict(lambda: defaultdict(list))  # dist -> algo -> [(n, t)]
    with open("benchmark_results.csv") as f:
        for row in csv.DictReader(f):
            data[row["distribution"]][row["algorithm"]].append(
                (int(row["n"]), float(row["avg_seconds"])))

    for dist, algos in data.items():
        plt.figure(figsize=(8, 5))
        for algo, points in algos.items():
            points.sort()
            ns = [p[0] for p in points]
            ts = [p[1] for p in points]
            plt.plot(ns, ts, marker="o", label=algo)
        plt.title(f"Sorting time vs input size ({dist} input)")
        plt.xlabel("n (elements)")
        plt.ylabel("average time (seconds)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        out = f"plots/{dist}_comparison.png"
        plt.savefig(out, dpi=150)
        plt.close()
        print(f"saved {out}")


if __name__ == "__main__":
    main()
