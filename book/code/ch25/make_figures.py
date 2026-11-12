"""第二十五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import bookstyle as bs

CH = "25"


def fig_bb84():
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    ax.text(1.5, 5.45, "Alice", fontsize=9, color="#1f2a37", ha="center")
    ax.text(8.5, 5.45, "Bob", fontsize=9, color="#1f2a37", ha="center")
    for x in (1.5, 8.5):
        ax.plot([x, x], [0.7, 5.1], color="#b9c3cf", lw=1.0, ls=(0, (4, 3)))
        ax.add_patch(FancyBboxPatch((x - 0.35, 4.75), 0.7, 0.42, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    facecolor="#eaf1f9", edgecolor="#4a6f9c", lw=1.0))
        ax.text(x, 4.96, "○", fontsize=9, color="#4a6f9c", ha="center", va="center")

    steps = [
        (4.3, 1.5, 8.5, "发送量子态", bs.RED),
        (3.5, 8.5, 1.5, "公布测量基", "#4a5568"),
        (2.7, 8.5, 1.5, "通知保留哪些比特", "#4a5568"),
        (1.9, 1.5, 8.5, "抽样比对，估计误码率", "#4a5568"),
    ]
    for y, x0, x1, text, color in steps:
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, shrinkA=0, shrinkB=0))
        ax.text(5.0, y + 0.10, text, fontsize=7.8, color=color, ha="center", va="bottom")

    ax.annotate("", xy=(8.5, 1.1), xytext=(1.5, 1.1),
                arrowprops=dict(arrowstyle="-|>", color=bs.GREEN, lw=1.2, shrinkA=0, shrinkB=0))
    ax.text(5.0, 1.20, "双方各自得到相同的密钥", fontsize=7.8, color=bs.GREEN, ha="center", va="bottom")
    bs.save(fig, CH, "fig01")


def fig_keyrate():
    L = np.linspace(0, 400, 600)
    eta = 10 ** (-0.02 * L)
    rate = 0.5 * eta
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    ax.semilogy(L, rate, color=bs.BLUE, lw=1.5)
    for x, lab in [(100, "100 km"), (200, "200 km"), (300, "300 km")]:
        y = 0.5 * 10 ** (-0.02 * x)
        ax.plot([x], [y], "o", ms=3.4, color=bs.RED)
        ax.annotate(lab, xy=(x, y), xytext=(x + 14, y * 3.2), fontsize=7.6, color=bs.RED)
    ax.set_xlabel("光纤长度 (km)")
    ax.set_ylabel("每脉冲成码率上限")
    ax.set_xlim(0, 400)
    ax.set_ylim(1e-12, 1.5)
    ax.text(10, 2e-10, "按 0.2 dB/km 光纤与理想探测器估算，未计入误码与有限码长效应",
            fontsize=7.4, color="#4a5563")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bb84()
    fig_keyrate()
