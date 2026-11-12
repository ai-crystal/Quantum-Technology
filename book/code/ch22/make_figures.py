"""第二十二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import bookstyle as bs

CH = "22"


def fig_paul_trap():
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    for x in [2.4, 3.0, 7.0, 7.6]:
        ax.add_patch(Rectangle((x - 0.16, 1.1), 0.32, 2.2, facecolor="#dfe6ee",
                               edgecolor="#6b7785", lw=0.9))
    ax.plot([2.7, 7.3], [2.2, 2.2], color="#c9d2dc", lw=0.8, ls=(0, (4, 3)))
    ax.text(5.0, 0.85, "射频电极", fontsize=8.2, color="#4a5563", ha="center", va="top")

    for x in np.linspace(3.9, 6.1, 5):
        ax.add_patch(Circle((x, 2.2), 0.14, facecolor=bs.ORANGE, edgecolor="#8a5a12", lw=0.7))
    ax.annotate("离子链", xy=(5.0, 2.36), xytext=(5.0, 3.55), fontsize=8.4, color="#8a5a12",
                ha="center", arrowprops=dict(arrowstyle="-|>", color="#8a5a12", lw=0.8))
    ax.annotate("", xy=(7.9, 2.2), xytext=(8.9, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.4, shrinkA=0, shrinkB=0))
    ax.text(8.95, 3.05, "激光", fontsize=8.4, color=bs.RED, ha="left", va="center")
    ax.text(5.0, 1.45, "交变电场把离子束缚在轴线上", fontsize=7.8, color="#5a6674", ha="center", va="top")
    bs.save(fig, CH, "fig01")


def fig_rydberg():
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    x0, x1, x2 = 2.6, 4.4, 8.2
    y = 2.0
    Rb = 2.4
    ax.add_patch(Circle((x0, y), Rb, facecolor=bs.RED, alpha=0.07, edgecolor=bs.RED,
                        lw=0.9, ls=(0, (4, 3))))
    ax.plot([0.6, 9.4], [y - 0.5, y - 0.5], color="#b9c3cf", lw=1.0)

    ax.add_patch(Circle((x0, y - 0.5), 0.20, facecolor=bs.RED, edgecolor="#7a2a1a", lw=0.8))
    ax.add_patch(Circle((x1, y - 0.5), 0.20, facecolor="#9db8d2", edgecolor="#4a6f9c", lw=0.8))
    ax.add_patch(Circle((x2, y - 0.5), 0.20, facecolor="#9db8d2", edgecolor="#4a6f9c", lw=0.8))

    ax.annotate("", xy=(x0, y + 1.15), xytext=(x0 + Rb, y + 1.15),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(x0 + Rb / 2, y + 1.24, "阻塞半径 $R_b$", fontsize=8.2, color=bs.RED, ha="center", va="bottom")

    ax.text(x0, y - 0.85, "已激发的里德堡原子", fontsize=8.0, color="#7a2a1a", ha="center", va="top")
    ax.annotate("这一半径内无法再激发", xy=(x1, y - 0.5), xytext=(x1 + 0.15, y - 2.05),
                fontsize=8.0, color="#3a5570", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#3a5570", lw=0.7))
    ax.text(x2, y - 0.85, "可以自由激发", fontsize=8.0, color="#3a5570", ha="center", va="top")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_paul_trap()
    fig_rydberg()
