"""第十一章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import bookstyle as bs

bs.use("computing")

CH = "02"


def fig_sg():
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    ax.add_patch(Rectangle((0.5, 2.0), 1.3, 1.3, facecolor="#f2f5f9", edgecolor="#5c6b7a", lw=1.0))
    ax.text(1.15, 1.72, "原子炉", fontsize=8.2, color="#33414f", ha="center", va="top")
    ax.text(1.15, 2.65, "Ag", fontsize=8.4, color="#5c6b7a", ha="center", va="center")

    ax.annotate("", xy=(3.1, 2.65), xytext=(1.95, 2.65),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.4, shrinkA=0, shrinkB=0))

    ax.add_patch(Rectangle((3.1, 3.55), 1.9, 0.55, facecolor="#e8eef6", edgecolor="#5c6b7a", lw=1.0))
    ax.text(4.05, 3.83, "N", fontsize=9, color="#33414f", ha="center", va="center")
    ax.add_patch(Rectangle((3.1, 1.20), 1.9, 0.55, facecolor="#e8eef6", edgecolor="#5c6b7a", lw=1.0))
    ax.text(4.05, 1.48, "S", fontsize=9, color="#33414f", ha="center", va="center")
    ax.text(4.05, 0.92, "非均匀磁场", fontsize=7.8, color="#4a5563", ha="center", va="top")

    for y0, y1 in [(3.50, 3.05), (1.80, 2.25)]:
        ax.annotate("", xy=(3.75, y1), xytext=(3.75, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#8a95a3", lw=0.9, shrinkA=0, shrinkB=0))

    ax.plot([5.3, 7.3], [2.65, 3.45], color=bs.BLUE, lw=1.5)
    ax.plot([5.3, 7.3], [2.65, 1.85], color=bs.RED, lw=1.5)
    ax.plot([3.1, 5.3], [2.65, 2.65], color="#33414f", lw=1.2)

    ax.plot([7.35, 7.35], [1.3, 4.0], color="#33414f", lw=2.0)
    ax.add_patch(Circle((7.4, 3.45), 0.09, facecolor=bs.BLUE, edgecolor="none"))
    ax.add_patch(Circle((7.4, 1.85), 0.09, facecolor=bs.RED, edgecolor="none"))
    ax.text(7.55, 3.45, r"$S_z = +\hbar/2$", fontsize=8.2, color=bs.BLUE, ha="left", va="center")
    ax.text(7.55, 1.85, r"$S_z = -\hbar/2$", fontsize=8.2, color=bs.RED, ha="left", va="center")
    ax.text(7.35, 1.10, "接收屏", fontsize=7.8, color="#4a5563", ha="center", va="top")
    bs.save(fig, CH, "fig01")


def fig_bases():
    theta = np.deg2rad(54.7)
    phi = np.deg2rad(0)
    a = np.cos(theta / 2)
    b = np.exp(1j * phi) * np.sin(theta / 2)
    state = np.array([a, b], dtype=complex)
    bases = {
        r"$Z$ 基 $(|0\rangle,|1\rangle)$": [np.array([1, 0]), np.array([0, 1])],
        r"$X$ 基 $(|+\rangle,|-\rangle)$": [np.array([1, 1]) / np.sqrt(2), np.array([1, -1]) / np.sqrt(2)],
        r"$Y$ 基 $(|{+}i\rangle,|{-}i\rangle)$": [np.array([1, 1j]) / np.sqrt(2), np.array([1, -1j]) / np.sqrt(2)],
    }
    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    width = 0.34
    xs = np.arange(len(bases))
    p0s, p1s = [], []
    for name, (e0, e1) in bases.items():
        p0s.append(abs(np.vdot(e0, state)) ** 2)
        p1s.append(abs(np.vdot(e1, state)) ** 2)
    ax.bar(xs - width / 2, p0s, width, color=bs.BLUE, label="第一个基矢")
    ax.bar(xs + width / 2, p1s, width, color=bs.RED, label="第二个基矢")
    for i, (p0, p1) in enumerate(zip(p0s, p1s)):
        ax.text(i - width / 2, p0 + 0.02, f"{p0:.2f}", ha="center", fontsize=7.8, color=bs.BLUE)
        ax.text(i + width / 2, p1 + 0.02, f"{p1:.2f}", ha="center", fontsize=7.8, color=bs.RED)
    ax.set_xticks(xs)
    ax.set_xticklabels(list(bases.keys()), fontsize=8)
    ax.set_ylabel("测量概率")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", ncol=2, handlelength=1.2)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_sg()
    fig_bases()
