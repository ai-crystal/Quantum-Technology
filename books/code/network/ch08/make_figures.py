"""第 8 章插图：交换带来的保真度衰减，以及纯化迭代的代价。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "08"


def w_of(F):
    return (4 * F - 1) / 3


def F_of(w):
    return (1 + 3 * w) / 4


def pur(F):
    a = (1 - F) / 3
    return (F * F + a * a) / (F * F + 2 * F * a + 5 * a * a)


def fig_swap():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.12], "wspace": 0.30})

    ax = axes[0]
    F = np.linspace(0.25, 1.0, 400)
    ax.plot([0.25, 1.0], [0.25, 1.0], color="#b8c2ce", lw=0.9, ls=(0, (4, 3)))
    ax.plot(F, F_of(w_of(F) ** 2), color=bs.BLUE, lw=1.7)
    for f0 in [0.95, 0.85]:
        ax.plot([f0, f0], [0.25, f0], color=bs.RED, lw=0.8, ls=(0, (2, 2)))
        ax.plot([f0], [F_of(w_of(f0) ** 2)], "o", ms=4.2, color=bs.RED, zorder=4)
        ax.annotate(f"{F_of(w_of(f0) ** 2):.3f}", xy=(f0, F_of(w_of(f0) ** 2)),
                    xytext=(f0 - 0.075, F_of(w_of(f0) ** 2) - 0.035),
                    fontsize=7.8, color=bs.RED, ha="right",
                    bbox=dict(fc="white", ec="none", pad=1.2))
    ax.annotate("交换一次", xy=(0.72, F_of(w_of(0.72) ** 2)), xytext=(0.55, 0.86),
                fontsize=8.0, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-", color=bs.BLUE, lw=0.7))
    ax.annotate("对角线", xy=(0.44, 0.44), xytext=(0.30, 0.56), fontsize=7.6,
                color="#6b7785", arrowprops=dict(arrowstyle="-", color="#9aa6b4", lw=0.6))
    ax.set_xlim(0.25, 1.0)
    ax.set_ylim(0.25, 1.0)
    ax.set_xlabel("交换前每一段的保真度 $F_0$")
    ax.set_ylabel("交换后的保真度 $F_1$")
    ax.set_xticks([0.3, 0.5, 0.7, 0.9])
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    hops = np.arange(0, 21)
    for F0, c, nm in [(0.99, bs.GREEN, "0.99"), (0.95, bs.BLUE, "0.95"), (0.90, bs.ORANGE, "0.90")]:
        w = w_of(F0)
        ax.plot(hops, F_of(w ** (hops + 1)), color=c, lw=1.5, marker="o", ms=2.6,
                label=f"每段保真度 {nm}")
    ax.axhline(0.25, color="#9aa6b4", lw=0.9, ls=(0, (5, 3)))
    ax.text(19.6, 0.216, "完全混态", fontsize=7.8, ha="right", color="#6b7785")
    ax.set_xlim(0, 20)
    ax.set_ylim(0.2, 1.0)
    ax.set_xlabel("链路上的交换次数")
    ax.set_ylabel("端到端保真度")
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])
    ax.legend(loc="lower left", fontsize=7.8)
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_swap_cost():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.12], "wspace": 0.32})

    ax = axes[0]
    F = np.linspace(0.2, 1.0, 600)
    ax.plot(F, F, color="#b8c2ce", lw=0.9, ls=(0, (4, 3)))
    ax.plot(F, pur(F), color=bs.BLUE, lw=1.7)
    ax.axvline(0.5, color=bs.RED, lw=0.8, ls=(0, (2, 2)))
    ax.text(0.523, 0.305, "阈值 0.5", fontsize=7.8, color=bs.RED)

    f = 0.70
    for _ in range(5):
        f2 = pur(f)
        ax.plot([f, f], [f, f2], color=bs.ORANGE, lw=0.9)
        ax.plot([f, f2], [f2, f2], color=bs.ORANGE, lw=0.9)
        ax.plot([f2], [f2], "o", ms=3.0, color=bs.ORANGE)
        f = f2
    ax.text(0.275, 0.78, "从 0.70 出发\n五轮之后到 0.88", fontsize=7.6, color=bs.ORANGE)

    ax.set_xlim(0.2, 1.0)
    ax.set_ylim(0.2, 1.0)
    ax.set_xlabel("纯化前的保真度 $F$")
    ax.set_ylabel("一轮之后的保真度 $F'$")
    ax.set_xticks([0.3, 0.5, 0.7, 0.9])
    ax.set_yticks([0.3, 0.5, 0.7, 0.9])
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    F0s = np.arange(0.60, 0.951, 0.025)
    rounds = []
    for F0 in F0s:
        f, n = F0, 0
        while f < 0.95 and n < 20:
            f = pur(f)
            n += 1
        rounds.append(n)
    rounds = np.array(rounds)
    ax.semilogy(F0s * 100, 2.0 ** rounds, color=bs.BLUE, lw=1.4, marker="o", ms=4.2)
    ax.set_xlabel("单个纠缠对的初始保真度（%）")
    ax.set_ylabel("达到 0.95 所需的副本数")
    ax.set_xlim(55, 96)
    ax.set_xticks([60, 70, 80, 90, 95])
    ax.set_yticks([1, 10, 100, 1000, 10000])
    ax.set_ylim(0.7, 4e4)
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.annotate("约四千份", xy=(60.4, 4096), xytext=(64.5, 11000),
                fontsize=7.8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_swap()
    fig_swap_cost()
