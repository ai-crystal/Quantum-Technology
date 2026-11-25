"""第二十一章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

import bookstyle as bs

bs.use("devices")

CH = "04"


def fig_circuit():
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    # 上支路：电容
    ax.plot([1.2, 3.6], [3.4, 3.4], color="#33414f", lw=1.2)
    ax.plot([4.2, 7.8], [3.4, 3.4], color="#33414f", lw=1.2)
    ax.plot([3.6, 3.6], [3.0, 3.8], color="#33414f", lw=2.0)
    ax.plot([4.2, 4.2], [3.0, 3.8], color="#33414f", lw=2.0)
    ax.text(3.9, 4.02, "电容 $C$", fontsize=8.2, color="#33414f", ha="center", va="bottom")

    # 下支路：约瑟夫森结
    ax.plot([1.2, 1.2], [3.4, 1.4], color="#33414f", lw=1.2)
    ax.plot([7.8, 7.8], [3.4, 1.4], color="#33414f", lw=1.2)
    ax.plot([1.2, 3.9], [1.4, 1.4], color="#33414f", lw=1.2)
    ax.plot([5.1, 7.8], [1.4, 1.4], color="#33414f", lw=1.2)
    ax.add_patch(Rectangle((3.9, 1.0), 1.2, 0.8, facecolor="#eef3ee", edgecolor="#4a6f4a", lw=1.1))
    ax.plot([4.1, 5.0], [1.55, 1.55], color="#4a6f4a", lw=1.0)
    ax.plot([4.1, 5.0], [1.25, 1.25], color="#4a6f4a", lw=1.0)
    ax.text(4.5, 0.86, "约瑟夫森结", fontsize=8.2, color="#3f5a3f", ha="center", va="top")
    ax.text(1.05, 2.4, "$L_J$", fontsize=8.2, color="#33414f", ha="right", va="center")
    ax.text(0.9, 3.9, "超导岛", fontsize=8.0, color="#6b7785", ha="left")
    bs.save(fig, CH, "fig01")


def fig_levels():
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    ax.plot([0.6, 3.4], [0.7, 0.7], color=bs.GRAY, lw=1.4)
    ax.plot([0.6, 3.4], [1.65, 1.65], color=bs.GRAY, lw=1.4)
    ax.plot([0.6, 3.4], [2.60, 2.60], color=bs.GRAY, lw=1.4)
    ax.plot([0.6, 3.4], [3.55, 3.55], color=bs.GRAY, lw=1.4)
    ax.text(2.0, 0.45, "线性谐振子", fontsize=8.4, color="#4a5563", ha="center", va="top")
    ax.annotate("", xy=(3.6, 0.7), xytext=(3.6, 1.65),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GRAY, lw=0.9, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(3.6, 1.65), xytext=(3.6, 2.60),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GRAY, lw=0.9, shrinkA=0, shrinkB=0))

    ax.plot([6.4, 9.2], [0.7, 0.7], color=bs.BLUE, lw=1.4)
    ax.plot([6.4, 9.2], [1.58, 1.58], color=bs.BLUE, lw=1.4)
    ax.plot([6.4, 9.2], [2.36, 2.36], color=bs.BLUE, lw=1.4)
    ax.plot([6.4, 9.2], [3.04, 3.04], color=bs.BLUE, lw=1.4)
    ax.text(7.8, 0.45, "超导比特（非谐）", fontsize=8.4, color="#33414f", ha="center", va="top")
    ax.annotate("", xy=(9.4, 0.7), xytext=(9.4, 1.58),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(9.4, 1.58), xytext=(9.4, 2.36),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(5.6, 1.14, r"$\omega_{01}$", fontsize=8.2, color=bs.RED, ha="right")
    ax.text(5.6, 1.97, r"$\omega_{12}$", fontsize=8.2, color=bs.RED, ha="right")
    ax.text(7.8, 3.35, r"$\omega_{12} < \omega_{01}$", fontsize=8.2, color=bs.RED, ha="center")
    ax.text(2.0, 3.85, "相邻能级等间距", fontsize=7.8, color="#6b7785", ha="center")
    ax.text(7.8, 3.85, "相邻能级不等间距，可以单独寻址", fontsize=7.8, color="#6b7785", ha="center")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_circuit()
    fig_levels()
