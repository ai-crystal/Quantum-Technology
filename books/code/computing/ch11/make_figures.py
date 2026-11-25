"""第十一章插图：复杂度类的相互位置、经典模拟的存储代价。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import bookstyle as bs

bs.use("computing")
CH = "11"


def box(ax, x0, y0, w, h, fc, ec):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.22",
                                facecolor=fc, edgecolor=ec, lw=1.0))


def fig_classes():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    box(ax, 0.35, 0.8, 9.3, 5.2, "#f8fafc", "#6b7785")
    ax.text(0.68, 5.72, "PSPACE", fontsize=9.4, color="#33414f")

    box(ax, 0.85, 1.15, 5.35, 4.45, "#edf4ee", "#5f8a5f")
    ax.text(1.15, 5.15, "BQP", fontsize=9.4, color="#3f6440")
    ax.text(1.95, 5.22, "Shor 算法在这一类里", fontsize=7.2, color="#3f6440")

    box(ax, 1.35, 1.55, 3.2, 2.75, "#eaf1f9", "#4a6f9c")
    ax.text(1.62, 3.98, "BPP", fontsize=9.0, color="#2b5c94")

    box(ax, 1.75, 1.95, 1.6, 1.3, "#ffffff", "#4a6f9c")
    ax.text(2.55, 2.62, "P", fontsize=9.4, color="#1f2a37", ha="center", va="center")
    ax.text(2.55, 2.15, "判定问题", fontsize=7.2, color="#6b7785", ha="center", va="center")

    box(ax, 6.95, 1.75, 2.45, 3.3, "#faf3ec", "#b07a3a")
    ax.text(8.18, 4.6, "NP", fontsize=9.4, color="#8a5a22", ha="center")
    ax.text(8.18, 2.95, "NP 完全问题\n一般认为\n不在 BQP 内", fontsize=7.6,
            color="#6b4a20", ha="center", va="center", linespacing=1.7)

    ax.add_patch(FancyArrowPatch((6.32, 3.1), (6.88, 3.1), arrowstyle="<|-|>",
                                 mutation_scale=9, color="#8a97a6", lw=0.9,
                                 linestyle=(0, (3, 3))))
    ax.text(6.6, 3.35, "?", fontsize=8.4, color="#8a97a6", ha="center")
    ax.set_ylim(0.55, 6.2)
    bs.save(fig, CH, "fig01")


def fig_memory():
    n = np.arange(10, 61)
    sv = 2.0 ** n * 16
    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    ax.semilogy(n, sv, "-", lw=1.4, color=bs.RED, label="完整态矢量")
    for chi, color in [(64, bs.BLUE), (512, bs.GREEN), (4096, bs.PURPLE)]:
        mps = n * chi ** 2 * 16
        ax.semilogy(n, mps, "-", lw=1.1, color=color, label=rf"张量网络 $\chi={chi}$")
    ax.axhline(1e12, color="#8a97a6", lw=0.8, ls=(0, (4, 3)))
    ax.text(11, 3.2e12, "一台服务器的内存", fontsize=7.4, color="#6b7785")
    ax.set_xlabel("比特数 $n$")
    ax.set_ylabel("所需存储（字节）")
    ax.set_xlim(10, 60)
    ax.set_ylim(1e2, 1e20)
    ax.text(0.03, 0.06, r"完整态矢量按 $16\cdot2^n$ 字节，张量网络按 $16\,n\chi^2$ 字节",
            transform=ax.transAxes, fontsize=7.2, color="#6b7785")
    ax.legend(loc="upper left", fontsize=7.6, handlelength=2.2)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_classes()
    fig_memory()
