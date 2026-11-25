"""第五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("qec")

CH = "05"


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def fig_matching():
    nodes = [(1, 1), (6, 2), (2, 5), (4, 6)]
    good = [(0, 1), (2, 3)]
    bad = [(0, 2), (1, 3)]
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    for x in range(0, 8):
        ax.plot([x, x], [0.2, 6.8], color="#eef1f5", lw=0.8, zorder=0)
    for y in range(1, 7):
        ax.plot([0.4, 7.0], [y, y], color="#eef1f5", lw=0.8, zorder=0)

    wg = sum(manhattan(nodes[i], nodes[j]) for i, j in good)
    wb = sum(manhattan(nodes[i], nodes[j]) for i, j in bad)
    for i, j in bad:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]],
                color="#9aa5b1", lw=1.2, ls=(0, (4, 3)), zorder=2)
    for i, j in good:
        ax.plot([nodes[i][0], nodes[j][0]], [nodes[i][1], nodes[j][1]],
                color=bs.BLUE, lw=2.0, zorder=3)
    for (x, y) in nodes:
        ax.plot([x], [y], "o", ms=7, mfc=bs.RED, mec="white", mew=1.2, zorder=4)

    ax.text(0.5, 7.05, f"总权重 {wg} 的配对（更可能）", fontsize=8.0, color=bs.BLUE,
            ha="left", va="bottom")
    ax.text(0.5, 6.55, f"总权重 {wb} 的配对", fontsize=8.0, color="#6b7785",
            ha="left", va="bottom")
    ax.set_xlabel("数据比特的位置")
    ax.set_ylabel("测量周期")
    ax.set_xlim(0.2, 7.4)
    ax.set_ylim(0, 7.6)
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticks([1, 2, 3, 4, 5, 6])
    bs.clean(ax)
    bs.save(fig, CH, "fig01")


def fig_latency():
    rows = [
        ("双比特门序列", 0.0, 0.40, "#c9d6e4"),
        ("读出与数字化", 0.40, 0.30, "#c9d6e4"),
        ("数据搬运", 0.70, 0.15, "#c9d6e4"),
        ("解码，码距 3", 0.85, 0.25, bs.BLUE),
        ("解码，码距 5", 0.85, 1.20, "#4a7fb0"),
        ("解码，码距 7", 0.85, 6.00, "#7a5f9e"),
        ("反馈门", 1.10, 0.08, bs.GREEN),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for k, (name, start, dur, col) in enumerate(rows):
        y = len(rows) - 1 - k
        ax.add_patch(Rectangle((start, y - 0.30), dur, 0.60, facecolor=col, alpha=0.85,
                               edgecolor="none", zorder=3))
        ax.text(-0.10, y, name, fontsize=8.2, ha="right", va="center", color="#33414f")
        ax.text(7.05, y, f"{dur:.2f} μs", fontsize=7.4, ha="left", va="center",
                color="#6b7785")
    ax.axvline(1.0, color=bs.RED, lw=1.0, ls=(0, (3, 2)), zorder=2)
    ax.text(1.10, len(rows) - 0.35, "一个测量周期", fontsize=7.6, color=bs.RED,
            ha="left", va="center")
    ax.set_xlim(-1.55, 8.4)
    ax.set_ylim(-0.75, len(rows) - 0.15)
    ax.set_yticks([])
    ax.set_xlabel("自本轮测量开始算起的时间（微秒）")
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    bs.clean(ax, grid_axis="x")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_matching()
    fig_latency()
