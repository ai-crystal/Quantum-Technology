"""第三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import bookstyle as bs

bs.use("qec")

CH = "03"
D = 5
XCOL = "#2b5c94"
ZCOL = "#b4462f"


def face_xy(i, j):
    return i + 0.5, j + 0.5


def is_x(i, j):
    return (i + j) % 2 == 1


def draw_patch(ax, d=D, face_size=0.30):
    for i in range(d - 1):
        for j in range(d - 1):
            cx, cy = face_xy(i, j)
            col = XCOL if is_x(i, j) else ZCOL
            ax.add_patch(Rectangle((cx - face_size / 2, cy - face_size / 2), face_size, face_size,
                                   facecolor=col, edgecolor="none", alpha=0.18, zorder=1))
    for i in range(d):
        ax.plot([i, i], [0, d - 1], color="#dfe4ea", lw=0.7, zorder=0)
    for j in range(d):
        ax.plot([0, d - 1], [j, j], color="#dfe4ea", lw=0.7, zorder=0)
    for i in range(d):
        for j in range(d):
            ax.add_patch(Circle((i, j), 0.115, facecolor="white", edgecolor="#3b4a5a", lw=1.0, zorder=3))
    ax.add_patch(Rectangle((0, 0), d - 1, d - 1, facecolor="none", edgecolor="#8f9aa8",
                           lw=0.9, ls=(0, (4, 3)), zorder=2))


def fig_lattice():
    fig, ax = plt.subplots(figsize=(5.6, 4.9))
    draw_patch(ax)
    d = D

    ax.plot([2, 2], [-0.42, d - 0.58], color=ZCOL, lw=3.0, alpha=0.55, zorder=4,
            solid_capstyle="round")
    ax.plot([-0.42, d - 0.58], [2, 2], color=XCOL, lw=3.0, alpha=0.55, zorder=4,
            solid_capstyle="round")
    for k in range(d):
        ax.add_patch(Circle((2, k), 0.115, facecolor="white", edgecolor=ZCOL, lw=1.6, zorder=5))
        ax.add_patch(Circle((k, 2), 0.115, facecolor="white", edgecolor=XCOL, lw=1.6, zorder=5))

    ax.text(-0.80, 2.0, r"$\bar X$", fontsize=11, color=XCOL, ha="center", va="center")
    ax.text(2.0, -0.95, r"$\bar Z$", fontsize=11, color=ZCOL, ha="center", va="center")

    ax.annotate("X 型稳定子", xy=(2.5, 3.5), xytext=(3.05, 4.55),
                fontsize=7.8, color="#33414f", ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8))
    ax.annotate("Z 型稳定子", xy=(0.5, 2.5), xytext=(-1.75, 4.55),
                fontsize=7.8, color="#33414f", ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8,
                                connectionstyle="angle,angleA=0,angleB=90,rad=0"))

    ax.set_xlim(-2.0, 6.2)
    ax.set_ylim(-1.35, 5.05)
    ax.set_aspect("equal")
    ax.axis("off")
    bs.save(fig, CH, "fig01")


def fig_chain():
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    draw_patch(ax)
    d = D

    err = [(1, 1), (2, 1)]
    alt = [(1, 2), (2, 2)]
    ax.plot([1, 2], [1, 1], color=bs.ORANGE, lw=3.4, alpha=0.9, zorder=4, solid_capstyle="round")
    ax.plot([1, 2], [2, 2], color=bs.ORANGE, lw=1.7, alpha=0.9, zorder=4, ls=(0, (3, 2)))
    for (i, j) in err + alt:
        ax.add_patch(Circle((i, j), 0.115, facecolor=bs.ORANGE, edgecolor="white", lw=0.8, zorder=6))

    for (i, j) in [(0, 0), (2, 0)]:
        cx, cy = face_xy(i, j)
        ax.add_patch(Rectangle((cx - 0.21, cy - 0.21), 0.42, 0.42, facecolor=ZCOL,
                               edgecolor="black", lw=0.9, alpha=0.85, zorder=5))

    cx, cy = face_xy(1, 1)
    ax.add_patch(Rectangle((cx - 0.30, cy - 0.30), 0.60, 0.60, facecolor="none",
                           edgecolor=bs.GREEN, lw=1.4, ls=(0, (3, 2)), zorder=5))

    ax.annotate("综合征 −1", xy=(0.34, 0.34), xytext=(-2.0, -1.25),
                fontsize=7.8, color="#33414f", ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8))
    ax.annotate("综合征 −1", xy=(2.34, 0.34), xytext=(3.85, -1.35),
                fontsize=7.8, color="#33414f", ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8))

    ax.set_xlim(-2.2, 6.3)
    ax.set_ylim(-1.75, 4.35)
    ax.set_aspect("equal")
    ax.axis("off")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_lattice()
    fig_chain()
