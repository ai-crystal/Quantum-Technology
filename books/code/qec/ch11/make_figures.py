"""第十一章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "11"


def fig_bounds():
    n = np.linspace(4, 100, 600)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))

    ax.plot(n, (n + 1) / 2.0, color=bs.GRAY, lw=1.1, ls=(0, (6, 3)))
    ax.text(13.5, 19.2, "Singleton 界", fontsize=8.2, color="#4a5563",
            ha="left", va="center")
    ax.annotate("", xy=(41.8, 21.4), xytext=(33.0, 19.4),
                arrowprops=dict(arrowstyle="->", color="#9aa6b4", lw=0.8))
    ax.plot(n, 0.7071 * np.sqrt(n), color=bs.RED, lw=1.4)
    ax.text(60, 4.2, "几何局域码的上限", fontsize=8.0, color=bs.RED,
            ha="left", va="top")

    ax.plot([5], [3], "o", ms=6.5, color=bs.BLUE, mec="white", mew=0.9, zorder=5)
    ax.annotate("$[\\![5,1,3]\\!]$", xy=(5, 3), xytext=(11.5, 1.35), fontsize=8.2,
                color=bs.BLUE, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color="#9db4cc", lw=0.7,
                                shrinkA=2, shrinkB=5))

    surf = [(17, 3), (49, 5), (97, 7)]
    ax.plot([p[0] for p in surf], [p[1] for p in surf], "s", ms=6.0,
            mfc=bs.ORANGE, mec="white", mew=0.9, zorder=6, ls="none")
    ax.annotate("表面码 $d=3$", xy=(17, 3), xytext=(15.5, 6.4), fontsize=7.8,
                color=bs.ORANGE, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color="#e0b27a", lw=0.7,
                                shrinkA=2, shrinkB=5))
    ax.annotate("$d=5$", xy=(49, 5), xytext=(36.5, 7.0), fontsize=7.8,
                color=bs.ORANGE, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color="#e0b27a", lw=0.7,
                                shrinkA=2, shrinkB=5))
    ax.annotate("$d=7$", xy=(97, 7), xytext=(85.5, 9.4), fontsize=7.8,
                color=bs.ORANGE, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", color="#e0b27a", lw=0.7,
                                shrinkA=2, shrinkB=5))

    ax.set_xlabel("物理比特数 $n$")
    ax.set_ylabel("码距 $d$")
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 27)
    ax.set_yticks([0, 3, 5, 7, 9, 12, 15, 20, 25])
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_cohinfo():
    p = np.linspace(5e-4, 0.30, 700)
    h2 = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    ic = 1.0 - h2 - p * np.log2(3.0)

    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.axhline(0, color="#8a97a6", lw=0.8)
    ax.plot(p, ic, color=bs.BLUE, lw=1.6)

    zero = p[np.argmin(np.abs(ic))]
    ax.plot([zero], [0], "o", ms=5.0, color=bs.BLUE, zorder=5)
    ax.axvline(zero, color=bs.BLUE, lw=0.8, ls=(0, (2, 2.5)), alpha=0.7)
    ax.text(zero + 0.007, 0.55, "相干信息归零\n$p\\approx 18.9\\%$", fontsize=7.8,
            color=bs.BLUE, ha="left", va="center")

    ax.axvspan(0.002, 0.010, color=bs.ORANGE, alpha=0.25, lw=0)
    ax.annotate("表面码能工作的范围", xy=(0.0105, 0.28), xytext=(0.045, 0.36),
                fontsize=7.6, color=bs.ORANGE, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color="#c9a06a", lw=0.8,
                                shrinkA=2, shrinkB=1))

    ax.text(0.072, 0.86, "容量为正", fontsize=8.0, color="#4a5563")
    ax.text(0.225, -0.16, "容量为零", fontsize=8.0, color="#4a5563")

    ax.set_xlabel("去极化错误率 $p$")
    ax.set_ylabel("相干信息 $I_c$（比特／比特）")
    ax.set_xlim(0, 0.30)
    ax.set_ylim(-0.45, 1.05)
    ax.set_xticks([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bounds()
    fig_cohinfo()
