"""第十章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

import bookstyle as bs

bs.use("foundations")

CH = "10"


def fig_sg():
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    # 炉子
    ax.add_patch(FancyBboxPatch((0.3, 1.72), 1.35, 0.98,
                                boxstyle="round,pad=0.05,rounding_size=0.12",
                                facecolor="#f4e9df", edgecolor="#9a7455", lw=1.0))
    ax.text(0.97, 2.21, "银原子炉", fontsize=8.0, ha="center", va="center", color="#5c452f")
    ax.plot([1.68, 2.02], [2.21, 2.21], color="#9a7455", lw=2.6)

    # 准直狭缝
    for xv in (2.42, 2.60):
        ax.plot([xv, xv], [1.62, 2.02], color="#4a5563", lw=2.2)
        ax.plot([xv, xv], [2.40, 2.80], color="#4a5563", lw=2.2)
    ax.text(2.51, 1.30, "准直狭缝", fontsize=7.8, ha="center", va="top", color="#4a5563")

    # 入射束
    ax.plot([2.02, 3.72], [2.21, 2.21], color="#7d8b9c", lw=1.1, ls=(0, (4, 2.5)))

    # 磁极
    ax.add_patch(Rectangle((3.72, 3.02), 2.92, 0.62, facecolor="#e7ecf4",
                           edgecolor="#5a6d85", lw=1.0))
    ax.text(5.18, 3.33, "N", fontsize=9.0, ha="center", va="center", color="#3a4a5c")
    pole = [(3.72, 0.78), (6.64, 0.78), (6.64, 1.40), (5.34, 1.40),
            (5.18, 1.72), (5.02, 1.40), (3.72, 1.40)]
    ax.add_patch(plt.Polygon(pole, closed=True, facecolor="#e7ecf4",
                             edgecolor="#5a6d85", lw=1.0))
    ax.text(5.18, 1.08, "S", fontsize=9.0, ha="center", va="center", color="#3a4a5c")

    # 磁极之间的磁场箭头，向尖头磁极收拢
    ax.add_patch(Rectangle((3.72, 1.40), 2.92, 1.62, facecolor="#f2f6fb",
                           edgecolor="none", zorder=0))
    for xv in np.linspace(3.92, 6.44, 9):
        xl = 5.18 + 0.62 * (xv - 5.18) / 1.26
        ax.annotate("", xy=(xl, 1.85), xytext=(xv, 2.88),
                    arrowprops=dict(arrowstyle="-|>", color="#9db3c9", lw=0.8,
                                    mutation_scale=6))

    ax.text(5.18, 4.02, "非均匀磁场", fontsize=8.2, ha="center", va="center", color="#4a5563")

    ax.plot([3.72, 6.64], [2.21, 2.21], color="#98a6b6", lw=1.0, ls=(0, (4, 2.5)), zorder=5)

    # 分裂后的两条原子束
    t = np.linspace(0, 1, 60)
    xb = 6.64 + 2.02 * t
    ax.plot(xb, 2.21 + 0.80 * t ** 2, color=bs.BLUE, lw=1.3)
    ax.plot(xb, 2.21 - 0.80 * t ** 2, color=bs.RED, lw=1.3)

    # 荧光屏
    ax.add_patch(Rectangle((8.70, 0.52), 0.16, 3.38, facecolor="#dfe6ee",
                           edgecolor="#8b98a8", lw=0.9))
    ax.scatter([8.70], [3.01], s=26, color=bs.BLUE, zorder=5)
    ax.scatter([8.70], [1.41], s=26, color=bs.RED, zorder=5)

    ax.annotate("两条斑", xy=(8.78, 3.01), xytext=(9.05, 3.42),
                fontsize=8.0, color="#3a4a5c",
                arrowprops=dict(arrowstyle="-", color="#8b98a8", lw=0.8,
                                connectionstyle="arc3,rad=-0.2"))
    ax.text(9.02, 2.21, "荧光屏", fontsize=8.0, ha="left", va="center", color="#4a5563")
    ax.text(9.02, 1.10, "无中间成分", fontsize=8.0, ha="left", va="center", color=bs.RED)

    bs.save(fig, CH, "fig01")


def sg_box(ax, x, y, w, h, label):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="#eaf1f8",
                           edgecolor="#4a6f9c", lw=1.0, zorder=3))
    ax.text(x + w / 2, y + h / 2, label, fontsize=8.4, ha="center", va="center",
            color="#25384d", zorder=4)


def fig_sequence():
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.45))

    # （a）一台磁铁，未极化束
    ax = axes[0]
    ax.set_xlim(0, 3.4)
    ax.set_ylim(0, 2.7)
    ax.axis("off")
    ax.annotate("", xy=(0.62, 0.95), xytext=(0.08, 0.95),
                arrowprops=dict(arrowstyle="-|>", color="#7d8b9c", lw=1.1, mutation_scale=8))
    sg_box(ax, 0.62, 0.60, 0.92, 0.70, "$\\mathrm{SG}_z$")
    ax.plot([1.54, 2.34], [0.95, 1.55], color=bs.BLUE, lw=1.2)
    ax.plot([1.54, 2.34], [0.95, 0.35], color=bs.RED, lw=1.2)
    ax.text(2.38, 1.55, "50%", fontsize=8.0, ha="left", va="center", color=bs.BLUE)
    ax.text(2.38, 0.35, "50%", fontsize=8.0, ha="left", va="center", color=bs.RED)
    ax.text(0.04, 2.40, "（a）", fontsize=8.2, color="#4a5563")

    # （b）两台同向磁铁
    ax = axes[1]
    ax.set_xlim(0, 3.4)
    ax.set_ylim(0, 2.7)
    ax.axis("off")
    sg_box(ax, 0.08, 0.30, 0.82, 0.64, "$\\mathrm{SG}_z$")
    ax.plot([0.90, 1.62], [0.62, 1.50], color=bs.BLUE, lw=1.2)
    ax.plot([0.90, 1.44], [0.62, 0.14], color="#c2ccd8", lw=1.2)
    ax.plot([1.40, 1.52], [0.26, -0.02], color="#4a5563", lw=2.6)
    sg_box(ax, 1.66, 1.18, 0.82, 0.64, "$\\mathrm{SG}_z$")
    ax.plot([2.48, 3.10], [1.50, 1.50], color=bs.BLUE, lw=1.2)
    ax.text(3.12, 1.50, "100%", fontsize=8.0, ha="left", va="center", color=bs.BLUE)
    ax.text(0.04, 2.40, "（b）", fontsize=8.2, color="#4a5563")

    # （c）换一个方向
    ax = axes[2]
    ax.set_xlim(0, 3.4)
    ax.set_ylim(0, 2.7)
    ax.axis("off")
    sg_box(ax, 0.08, 0.30, 0.82, 0.64, "$\\mathrm{SG}_z$")
    ax.plot([0.90, 1.62], [0.62, 1.50], color=bs.BLUE, lw=1.2)
    ax.plot([0.90, 1.44], [0.62, 0.14], color="#c2ccd8", lw=1.2)
    ax.plot([1.40, 1.52], [0.26, -0.02], color="#4a5563", lw=2.6)
    sg_box(ax, 1.66, 1.18, 0.82, 0.64, "$\\mathrm{SG}_x$")
    ax.plot([2.48, 3.06], [1.50, 1.92], color=bs.BLUE, lw=1.2)
    ax.plot([2.48, 3.06], [1.50, 1.08], color=bs.ORANGE, lw=1.2)
    ax.text(3.08, 1.94, "50%", fontsize=8.0, ha="left", va="center", color=bs.BLUE)
    ax.text(3.08, 1.04, "50%", fontsize=8.0, ha="left", va="center", color=bs.ORANGE)
    ax.text(0.04, 2.40, "（c）", fontsize=8.2, color="#4a5563")

    fig.subplots_adjust(wspace=0.12)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_sg()
    fig_sequence()
