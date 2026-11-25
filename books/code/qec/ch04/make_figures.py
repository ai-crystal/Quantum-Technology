"""第四章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs
from circuit import Circuit

bs.use("qec")

CH = "04"


def fig_transversal():
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    labels = [r"$a_1$", r"$a_2$", r"$a_3$", r"$b_1$", r"$b_2$", r"$b_3$"]
    c = Circuit(ax, 6, 5, labels=labels)
    for k in range(3):
        c.cnot(1, k, 3 + k)

    for y0, y1, name in [(0.36, -2.34, "逻辑比特 A"), (-2.66, -5.34, "逻辑比特 B")]:
        ax.add_patch(Rectangle((c.x0 - 0.95, y1), (5.0 * c.dx + 0.2) - (c.x0 - 0.95) + c.x0 - c.x0,
                               y0 - y1, facecolor="#eef2f7", edgecolor="none", zorder=0))
    ax.text(c.x0 - 0.30, 0.62, "逻辑比特 A", fontsize=8.0, color="#6b7785", ha="left", va="bottom")
    ax.text(c.x0 - 0.30, -5.62, "逻辑比特 B", fontsize=8.0, color="#6b7785", ha="left", va="top")
    ax.text(c.x(1), 0.62, "三个独立的 CNOT", fontsize=8.0, color="#6b7785", ha="left", va="bottom")
    ax.set_ylim(-6.1, 0.95)
    bs.save(fig, CH, "fig01")


def fig_distill():
    p = np.logspace(-4, -0.5, 500)
    p1 = 35 * p ** 3
    p2 = 35 * p1 ** 3
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.loglog(p, p, color=bs.GRAY, lw=1.0, ls=(0, (4, 3)), label="不蒸馏")
    ax.loglog(p, np.where(p1 > 2e-17, p1, np.nan), color=bs.BLUE, lw=1.6, label="蒸馏一轮")
    ax.loglog(p, np.where(p2 > 2e-17, p2, np.nan), color=bs.GREEN, lw=1.6, label="蒸馏两轮")
    ax.set_xlim(1e-4, 0.3)
    ax.set_ylim(1e-16, 0.4)
    ax.set_xlabel("输入魔法态的出错概率 $p$")
    ax.set_ylabel("输出魔法态的出错概率")
    ax.axvline(1e-3, color=bs.ORANGE, lw=0.9, ls=(0, (3, 2)))
    ax.plot([1e-3], [35e-9], "o", ms=4.5, color=bs.BLUE, zorder=5)
    ax.annotate("$p=10^{-3}$ 时\n约 $3.5\\times10^{-8}$", xy=(1e-3, 35e-9), xytext=(2.2e-3, 3e-12),
                fontsize=7.6, color="#33414f",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8))
    ax.legend(loc="lower right", handlelength=1.8)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_transversal()
    fig_distill()
