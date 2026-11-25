"""第十三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import bookstyle as bs

bs.use("foundations")

CH = "13"


def fig_chain():
    fig, ax = plt.subplots(figsize=(6.4, 2.55))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.7)
    ax.axis("off")

    names = ["量子系统", "测量装置", "视网膜", "神经与大脑"]
    xs = [0.35, 2.58, 4.81, 7.04]
    w, h = 1.72, 0.82

    for x, name in zip(xs, names):
        ax.add_patch(FancyBboxPatch((x, 1.72), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.10",
                                    facecolor="#eaf1f8", edgecolor="#4a6f9c", lw=1.0))
        ax.text(x + w / 2, 2.13, name, fontsize=8.2, ha="center", va="center", color="#25384d")

    for i in range(3):
        ax.annotate("", xy=(xs[i + 1] - 0.05, 2.13), xytext=(xs[i] + w + 0.05, 2.13),
                    arrowprops=dict(arrowstyle="-|>", color="#5a6d85", lw=1.0, mutation_scale=8))
        ax.text((xs[i] + w + xs[i + 1]) / 2, 2.62, "纠缠", fontsize=7.2,
                ha="center", va="bottom", color="#6b7785")

    ax.annotate("", xy=(9.06, 2.13), xytext=(xs[3] + w + 0.05, 2.13),
                arrowprops=dict(arrowstyle="-|>", color="#5a6d85", lw=1.0, mutation_scale=8))
    ax.add_patch(FancyBboxPatch((9.10, 1.72), 0.72, h,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                facecolor="white", edgecolor="#8b98a8", lw=1.0, ls=(0, (3, 2))))
    ax.text(9.46, 2.13, "？", fontsize=10.0, ha="center", va="center", color="#6b7785")

    ax.plot([0.35, 9.82], [1.30, 1.30], color="#c9d2dc", lw=1.0)
    ax.plot([0.35, 0.35], [1.24, 1.36], color="#c9d2dc", lw=1.0)
    ax.plot([9.82, 9.82], [1.24, 1.36], color="#c9d2dc", lw=1.0)
    ax.text(5.08, 1.02, "每一环都能写成薛定谔方程，链上没有天然的断点",
            fontsize=8.0, ha="center", va="top", color="#4a5563")
    ax.text(5.08, 0.60, "各家说法的分歧，在于把坍缩放在哪一环，或者干脆不放",
            fontsize=8.0, ha="center", va="top", color="#6b7785")

    bs.save(fig, CH, "fig01")


def fig_correlation():
    th = np.linspace(0, 180, 800)
    rad = np.deg2rad(th)
    q = -np.cos(rad)
    cl = -1 + 2 * th / 180

    fig, ax = plt.subplots(figsize=(5.9, 2.95))
    ax.fill_between(th, q, cl, where=(np.abs(q) >= np.abs(cl)), color="#e5edf7", zorder=0)
    ax.plot(th, q, color=bs.BLUE, lw=1.6, label="量子力学（单重态）")
    ax.plot(th, cl, color=bs.RED, lw=1.1, ls=(0, (5, 2.5)), label="定域隐变量上限")

    ax.set_xlim(0, 180)
    ax.set_ylim(-1.12, 1.12)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel("两个测量方向的夹角 $\\theta$（度）")
    ax.set_ylabel("关联 $E(\\theta)$")
    ax.legend(loc="upper left")
    bs.clean(ax, grid_axis="y")

    ax.plot([45], [-np.cos(np.deg2rad(45))], "o", ms=4, color=bs.BLUE, zorder=5)
    ax.annotate("$\\theta=45^\\circ$，量子 $-0.71$，经典极限 $-0.50$",
                xy=(45, -0.71), xytext=(50, -0.98), fontsize=7.6, color="#33414f",
                arrowprops=dict(arrowstyle="-", color="#8b98a8", lw=0.8))

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_chain()
    fig_correlation()
