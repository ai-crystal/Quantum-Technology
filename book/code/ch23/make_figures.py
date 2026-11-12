"""第二十三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

import bookstyle as bs

CH = "23"


def block(ax, x, y, w, h, text, fc="#eaf1f9", ec="#4a6f9c"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, fontsize=8.2, color="#1f2a37", ha="center", va="center")


def fig_chip():
    fig, ax = plt.subplots(figsize=(7.0, 2.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    ax.add_patch(Rectangle((0.4, 0.55), 11.2, 3.0, facecolor="#f7f9fc", edgecolor="#b9c6d4",
                           lw=1.0, ls=(0, (4, 2))))
    ax.text(0.6, 3.75, "集成光量子芯片", fontsize=8.2, color="#6b7785", ha="left")

    block(ax, 0.9, 1.55, 1.7, 1.0, "单光子源")
    block(ax, 3.4, 1.55, 1.5, 1.0, "分束器")
    block(ax, 5.6, 1.55, 1.6, 1.0, "相位调制")
    block(ax, 7.9, 1.55, 1.5, 1.0, "分束器")
    block(ax, 10.1, 2.45, 1.3, 0.75, "探测器")
    block(ax, 10.1, 0.95, 1.3, 0.75, "探测器")

    for x0, x1, y in [(2.6, 3.4, 2.05), (4.9, 5.6, 2.05), (7.2, 7.9, 2.05)]:
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.2, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(10.1, 2.82), xytext=(9.4, 2.35),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.2, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(10.1, 1.32), xytext=(9.4, 1.75),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(6.4, 0.78, "波导中的光子", fontsize=7.6, color="#6b7785", ha="center")
    bs.save(fig, CH, "fig01")


def fig_loss():
    L = np.linspace(0, 1000, 800)
    fiber = 0.2 * L
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    ax.plot(L, fiber, color=bs.BLUE, lw=1.5)
    ax.axhline(3, color=bs.GRAY, lw=0.8, ls=(0, (3, 3)))
    ax.text(300, 8, "探测效率极限约 3 dB", fontsize=7.6, color="#5a6674")
    for x, lab, ox, oy in [(100, "100 km，20 dB", 60, 22), (500, "500 km，100 dB", 40, -16)]:
        y = 0.2 * x
        ax.plot([x], [y], "o", ms=3.6, color=bs.RED)
        ax.annotate(lab, xy=(x, y), xytext=(x + ox, y + oy), fontsize=7.6, color=bs.RED)
        ax.plot([x, x + ox * 0.8], [y, y + oy * 0.7], color=bs.RED, lw=0.5, ls=(0, (2, 2)))
    ax.set_xlabel("光纤长度 (km)")
    ax.set_ylabel("总损耗 (dB)")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 210)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_chip()
    fig_loss()
