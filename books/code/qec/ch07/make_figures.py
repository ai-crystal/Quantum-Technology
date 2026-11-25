"""第七章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

import bookstyle as bs

bs.use("qec")

CH = "07"


def draw_lattice(ax, n, lw=0.7):
    for k in range(n):
        ax.plot([0, n - 1], [k, k], color="#dfe6ee", lw=lw, zorder=0)
        ax.plot([k, k], [0, n - 1], color="#dfe6ee", lw=lw, zorder=0)


def draw_qubits(ax, n, ms=6.0, z=3):
    for i in range(n):
        for j in range(n):
            ax.plot([i], [j], "o", ms=ms, mfc="white", mec="#4a5563", mew=0.9, zorder=z)


def fig_torus():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4),
                             gridspec_kw={"width_ratios": [1.0, 0.92], "wspace": 0.12})

    # ---- (a) 环面码：周期边界与两条逻辑环 ----
    ax = axes[0]
    n = 5
    draw_lattice(ax, n)
    for i in range(n - 1):
        for j in range(n - 1):
            xface = "#c9d6e4" if (i + j) % 2 == 0 else "#e8c4bb"
            edge = bs.BLUE if (i + j) % 2 == 0 else bs.RED
            ax.add_patch(Rectangle((i + 0.17, j + 0.17), 0.66, 0.66, facecolor=xface,
                                   edgecolor=edge, lw=0.8, alpha=0.9, zorder=1))
    draw_qubits(ax, n)

    ax.plot([0, n - 1], [2, 2], color=bs.BLUE, lw=1.7, ls=(0, (5, 2.5)), zorder=4)
    ax.plot([3, 3], [0, n - 1], color=bs.RED, lw=1.7, ls=(0, (5, 2.5)), zorder=4)
    ax.text(4.06, 2.02, r"$\bar Z_1$", fontsize=9.5, color=bs.BLUE, va="center")
    ax.text(3.18, 4.26, r"$\bar Z_2$", fontsize=9.5, color=bs.RED, va="center")

    ax.add_patch(FancyArrowPatch((-0.62, 3.55), (-0.62, 1.45), arrowstyle="<->",
                                 mutation_scale=9, color="#7a848f", lw=1.0,
                                 connectionstyle="arc3,rad=0.35", zorder=5))
    ax.text(-1.42, 2.5, "首尾相接", fontsize=7.8, color="#6b7785",
            rotation=90, ha="center", va="center")
    ax.add_patch(FancyArrowPatch((1.45, -0.62), (3.55, -0.62), arrowstyle="<->",
                                 mutation_scale=9, color="#7a848f", lw=1.0,
                                 connectionstyle="arc3,rad=0.35", zorder=5))
    ax.text(2.5, -1.42, "首尾相接", fontsize=7.8, color="#6b7785", ha="center", va="center")

    ax.text(0.0, 4.85, "蓝色面测 $X$，红色面测 $Z$", fontsize=7.8, color="#4a5563")
    ax.set_xlim(-1.85, 5.3)
    ax.set_ylim(-1.85, 5.35)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-1.85, 4.85, "(a)", fontsize=10, color=bs.INK)

    # ---- (b) 编织：e 绕 m 一周 ----
    ax = axes[1]
    n = 4
    draw_lattice(ax, n, lw=0.8)
    draw_qubits(ax, n, ms=5.6)
    ax.add_patch(Rectangle((1.18, 1.18), 0.64, 0.64, facecolor="#e8c4bb",
                           edgecolor=bs.RED, lw=0.9, alpha=0.9, zorder=2))
    ax.plot([1.5], [1.5], "s", ms=6, mfc=bs.RED, mec="white", mew=0.8, zorder=4)
    ax.text(1.9, 1.62, "$m$", fontsize=9.5, color=bs.RED, va="center")

    t = np.linspace(0.42 * np.pi, 2.42 * np.pi, 260)
    r = 0.95
    ax.plot(1.5 + r * np.cos(t), 1.5 + r * np.sin(t), color=bs.BLUE, lw=1.4,
            ls=(0, (4, 2.5)), zorder=5)
    ax.annotate("", xy=(1.5 + r * np.cos(0.33 * np.pi), 1.5 + r * np.sin(0.33 * np.pi)),
                xytext=(1.5 + r * np.cos(0.51 * np.pi), 1.5 + r * np.sin(0.51 * np.pi)),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.4), zorder=6)
    ex, ey = 1.5 + r * np.cos(0.42 * np.pi), 1.5 + r * np.sin(0.42 * np.pi)
    ax.plot([ex], [ey], "o", ms=7, mfc=bs.BLUE, mec="white", mew=0.9, zorder=7)
    ax.text(ex - 0.02, ey + 0.24, "$e$", fontsize=9.5, color=bs.BLUE, ha="center")

    ax.text(-0.32, 3.95, "$e$ 绕 $m$ 一圈", fontsize=7.8, color="#4a5563")
    ax.text(-0.32, 3.55, "整体相位变成 $-1$", fontsize=7.8, color="#4a5563")
    ax.set_xlim(-0.45, 4.35)
    ax.set_ylim(-0.45, 4.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-0.45, 4.32, "(b)", fontsize=10, color=bs.INK)

    bs.save(fig, CH, "fig01")


def hexagon(cx, cy, r):
    ang = np.deg2rad(90 + 60 * np.arange(6))
    return np.column_stack([cx + r * np.cos(ang), cy + r * np.sin(ang)])


def fig_color_subsystem():
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.6),
                             gridspec_kw={"width_ratios": [1.08, 0.92], "wspace": 0.06})

    # ---- (a) 6.6.6 色彩码 ----
    ax = axes[0]
    r = 1.0
    fills = {0: "#c9d6e4", 1: "#e6cdc4", 2: "#cfe0cd"}
    edges = {0: bs.BLUE, 1: bs.RED, 2: bs.GREEN}
    centres = [(i, j) for j in range(3) for i in range(j + 1)]
    verts = set()
    for (i, j) in centres:
        cx = np.sqrt(3) * r * (i + j / 2.0)
        cy = -1.5 * r * j
        c = (i - j) % 3
        ax.add_patch(Polygon(hexagon(cx, cy, r), closed=True, facecolor=fills[c],
                             edgecolor=edges[c], lw=1.0, alpha=0.95, zorder=2))
        for vx, vy in hexagon(cx, cy, r):
            verts.add((round(vx, 3), round(vy, 3)))
    for (vx, vy) in verts:
        ax.plot([vx], [vy], "o", ms=3.4, mfc="#33414f", mec="none", zorder=3)

    ax.text(0.02, 1.55, "三色面片，相邻面共用一条边", fontsize=7.6, color="#4a5563")
    ax.text(0.02, -4.62, "黑色小点是数据比特，每个面同时对易地测 $X$ 和 $Z$",
            fontsize=7.6, color="#4a5563")
    ax.set_xlim(-1.15, 6.55)
    ax.set_ylim(-5.05, 1.85)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-1.15, 1.55, "(a)", fontsize=10, color=bs.INK)

    # ---- (b) Bacon-Shor 的规范算符 ----
    ax = axes[1]
    n = 3
    draw_lattice(ax, n, lw=0.8)
    for i in range(n - 1):
        for j in range(n):
            ax.plot([i + 0.13, i + 0.87], [j, j], color=bs.BLUE, lw=2.6,
                    solid_capstyle="round", alpha=0.5, zorder=2)
    for j in range(n - 1):
        for i in range(n):
            ax.plot([i, i], [j + 0.13, j + 0.87], color=bs.RED, lw=2.6,
                    solid_capstyle="round", alpha=0.5, zorder=2)
    draw_qubits(ax, n, ms=7.2)

    ax.annotate("", xy=(4.15, 0.5), xytext=(2.3, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.5))
    ax.text(4.24, 0.5, r"$\bar X$", fontsize=9.5, color=bs.BLUE, va="center")
    ax.annotate("", xy=(0.35, 3.05), xytext=(0.35, 2.1),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.5))
    ax.text(0.35, 3.16, r"$\bar Z$", fontsize=9.5, color=bs.RED, ha="center", va="bottom")

    ax.text(0.05, 4.02, "蓝线 $X$ 型，红线 $Z$ 型", fontsize=7.6, color="#4a5563")
    ax.text(-0.45, -0.62, "一条横线才构成逻辑 $\\bar X$，一条竖线构成逻辑 $\\bar Z$",
            fontsize=7.6, color="#4a5563")
    ax.set_xlim(-0.55, 4.85)
    ax.set_ylim(-1.05, 4.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-0.55, 4.02, "(b)", fontsize=10, color=bs.INK)

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_torus()
    fig_color_subsystem()
