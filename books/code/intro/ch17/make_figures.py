"""第 17 章插图：七道关口的漏斗与良率爬坡。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("intro")

CH = "17"


def fig_funnel():
    gates = [
        ("实验室演示", 1.00),
        ("一致性", 0.80),
        ("良率", 0.55),
        ("可靠性", 0.75),
        ("可维护性", 0.80),
        ("成本", 0.35),
        ("标准", 0.90),
        ("人才", 0.70),
    ]
    cum = [1.0]
    for _, p in gates[1:]:
        cum.append(cum[-1] * p)

    labels = [f"{n}  ×{p:.2f}" if i else n for i, (n, p) in enumerate(gates)]
    y = np.arange(len(gates))[::-1]

    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    for i, (c, lab) in enumerate(zip(cum, labels)):
        color = "#c3ccd8" if i == 0 else (bs.RED if i == len(cum) - 1 else bs.BLUE)
        ax.barh(y[i], c * 100, height=0.62, color=color, alpha=0.85,
                edgecolor="white", linewidth=0.8)
        ax.text(c * 100 + 1.6, y[i], f"{c * 100:.0f}%", va="center", ha="left",
                fontsize=8.0, color="#33414f")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.8)
    ax.set_xlim(0, 112)
    ax.set_xlabel("通过这道关口之后剩下的比例（%）")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.axvline(100, color="#b9c3cf", lw=0.8, ls=(0, (3, 3)))
    bs.clean(ax, grid_axis="x")

    bs.save(fig, CH, "fig01")


def fig_yield():
    V = np.logspace(0, 4, 400)
    D = V ** -0.3
    areas = [(0.25, "5 × 5 mm", bs.BLUE), (1.0, "10 × 10 mm", bs.GREEN),
             (4.0, "20 × 20 mm", bs.RED)]
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    for a, name, col in areas:
        ax.plot(V, np.exp(-a * D) * 100, color=col, lw=1.5, label="芯片边长 " + name)

    ax.annotate("首批流片只有百分之二", (1.0, 1.8), textcoords="offset points",
                xytext=(14, 22), fontsize=7.4, color=bs.RED,
                arrowprops=dict(arrowstyle="-", color=bs.RED, lw=0.7))

    ax.set_xscale("log")
    ax.set_xlim(1, 1e4)
    ax.set_ylim(0, 104)
    ax.set_xlabel("累计产量（以首次流片为 1）")
    ax.set_ylabel("良率（%）")
    ax.legend(loc="lower right", handlelength=1.8)
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_funnel()
    fig_yield()
