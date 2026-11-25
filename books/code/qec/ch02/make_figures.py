"""第二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs
from circuit import Circuit

bs.use("qec")

CH = "02"


def fig_syndrome_circuit():
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 3.5))
    fig.subplots_adjust(hspace=0.42)
    labels = [r"$d_1$", r"$d_2$", r"$d_3$", r"$d_4$", r"$a$"]

    ax = axes[0]
    c = Circuit(ax, 5, 6, labels=labels)
    for k in range(4):
        c.cnot(k, k, 4)
    c.measure(4.7, 4)
    ax.text(-1.0, 0.55, r"(a) 测量 $Z_1Z_2Z_3Z_4$", fontsize=8.4, color="#33414f")

    ax = axes[1]
    c = Circuit(ax, 5, 8, labels=labels)
    c.gate(0, 4, "H")
    for k in range(4):
        c.cnot(1 + k, 4, k)
    c.gate(5.2, 4, "H")
    c.measure(6.5, 4)
    ax.text(-1.0, 0.55, r"(b) 测量 $X_1X_2X_3X_4$", fontsize=8.4, color="#33414f")
    bs.save(fig, CH, "fig01")


STABS = [
    ("X", [4, 5, 6, 7], r"$g_1$"),
    ("X", [2, 3, 6, 7], r"$g_2$"),
    ("X", [1, 3, 5, 7], r"$g_3$"),
    ("Z", [4, 5, 6, 7], r"$g_4$"),
    ("Z", [2, 3, 6, 7], r"$g_5$"),
    ("Z", [1, 3, 5, 7], r"$g_6$"),
]
LOGS = [
    ("X", [1, 2, 3, 4, 5, 6, 7], r"$\bar X$"),
    ("Z", [1, 2, 3, 4, 5, 6, 7], r"$\bar Z$"),
]


def fig_steane():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ncol, nrow = 7, 9
    fill = {"X": "#cfe0f0", "Z": "#f0d8d2"}
    edge = {"X": "#2b5c94", "Z": "#b4462f"}
    for r, (kind, cols, name) in enumerate(STABS):
        y = nrow - 1 - r
        for q in range(1, ncol + 1):
            ax.add_patch(Rectangle((q - 0.3, y - 0.3), 0.6, 0.6,
                                   facecolor=fill[kind] if q in cols else "#f2f4f7",
                                   edgecolor=edge[kind] if q in cols else "#dde2e8",
                                   lw=1.0 if q in cols else 0.7, zorder=2))
        ax.text(-0.55, y, name, fontsize=8.4, ha="right", va="center", color="#33414f")
    ax.text(7.75, nrow - 3, "稳定子\n六个", fontsize=7.8, va="center", ha="left", color="#6b7785")
    ax.plot([-0.45, 7.7], [1.55, 1.55], color="#b9c3cf", lw=0.8, ls=(0, (3, 3)))
    for r, (kind, cols, name) in enumerate(LOGS):
        y = 1 - r
        for q in range(1, ncol + 1):
            ax.add_patch(Rectangle((q - 0.3, y - 0.3), 0.6, 0.6,
                                   facecolor="#c9c2d6", edgecolor="#5d5480", lw=1.0, zorder=2))
        ax.text(-0.55, y, name, fontsize=8.4, ha="right", va="center", color="#33414f")
    ax.text(7.75, 0.0, "逻辑算符\n两个", fontsize=7.8, va="center", ha="left", color="#6b7785")
    for q in range(1, ncol + 1):
        ax.text(q, nrow - 0.05, f"$q_{q}$", fontsize=8.2, ha="center", va="bottom", color="#33414f")
    ax.set_xlim(-1.3, 9.2)
    ax.set_ylim(-1.15, nrow + 0.5)
    ax.axis("off")
    ax.text(4.0, -0.95, "同一行中的方块表示该算符作用的比特", fontsize=7.4,
            ha="center", va="center", color="#6b7785")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_syndrome_circuit()
    fig_steane()
