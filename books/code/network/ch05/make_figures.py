"""第 5 章插图：纠缠交换的时空图、中继链的端到端速率。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import bookstyle as bs

bs.use("network")

CH = "05"


def wavy(x0, y0, x1, y1, color, lw=1.2, amp=0.035, n=11):
    t = np.linspace(0, 1, 300)
    x = x0 + (x1 - x0) * t
    y = y0 + (y1 - y0) * t
    dy = np.sin(2 * np.pi * n * t) * amp * (y1 - y0) / max(abs(y1 - y0), 1e-9)
    ax.plot(x, y + dy * 0.4, color=color, lw=lw, solid_capstyle="round")


def fig_swap():
    global ax
    fig, ax = plt.subplots(figsize=(6.3, 3.5))
    xs = [0.0, 1.6, 3.4, 5.0]
    names = ["Alice", "中继 1", "中继 2", "Bob"]

    for x, nm in zip(xs, names):
        ax.plot([x, x], [0.0, 3.9], color="#ccd5df", lw=1.0, zorder=0)
        ax.plot([x], [0.0], "o", ms=4, color="#7b8a9b", zorder=6)
        ax.text(x, -0.22, nm, fontsize=8.6, ha="center", color="#33414f")

    # 两组独立的纠缠对
    wavy(xs[0], 0.35, (xs[0] + xs[1]) / 2, 1.15, bs.BLUE)
    wavy(xs[1], 0.35, (xs[0] + xs[1]) / 2, 1.15, bs.BLUE)
    wavy(xs[2], 0.35, (xs[2] + xs[3]) / 2, 1.15, bs.BLUE)
    wavy(xs[3], 0.35, (xs[2] + xs[3]) / 2, 1.15, bs.BLUE)
    ax.text((xs[0] + xs[1]) / 2, 1.30, "纠缠对 A", fontsize=8.2, ha="center", color=bs.BLUE)
    ax.text((xs[2] + xs[3]) / 2, 1.30, "纠缠对 B", fontsize=8.2, ha="center", color=bs.BLUE)

    # 两个中继把各自的光子留在存储器里，再送到中点做贝尔态测量
    ax.plot([xs[1], xs[1]], [1.15, 2.45], color=bs.GREEN, lw=3.0, alpha=0.55,
            solid_capstyle="butt")
    ax.plot([xs[2], xs[2]], [1.15, 2.45], color=bs.GREEN, lw=3.0, alpha=0.55,
            solid_capstyle="butt")
    ax.text(xs[1] - 0.10, 1.85, "存储", fontsize=7.8, ha="right", color=bs.GREEN)
    ax.text(xs[2] + 0.10, 1.85, "存储", fontsize=7.8, ha="left", color=bs.GREEN)

    xm = (xs[1] + xs[2]) / 2
    wavy(xs[1], 2.45, xm - 0.22, 2.85, bs.ORANGE)
    wavy(xs[2], 2.45, xm + 0.22, 2.85, bs.ORANGE)
    box = FancyBboxPatch((xm - 0.22, 2.82), 0.44, 0.40, boxstyle="round,pad=0.04",
                         fc="#fbf3e4", ec=bs.ORANGE, lw=1.1, zorder=7)
    ax.add_patch(box)
    ax.text(xm, 3.02, "BSM", fontsize=8.2, ha="center", va="center", color=bs.ORANGE, zorder=8)

    # 经典结果送到两端
    ax.annotate("", xy=(xs[0] + 0.10, 3.42), xytext=(xm - 0.22, 3.16),
                arrowprops=dict(arrowstyle="-|>", color="#7b8a9b", lw=0.9,
                                ls=(0, (3, 2)), mutation_scale=9))
    ax.annotate("", xy=(xs[3] - 0.10, 3.42), xytext=(xm + 0.22, 3.16),
                arrowprops=dict(arrowstyle="-|>", color="#7b8a9b", lw=0.9,
                                ls=(0, (3, 2)), mutation_scale=9))
    ax.text(xm + 0.35, 3.47, "经典信道", fontsize=7.8, ha="left", color="#5b6a7a")

    wavy(xs[0] + 0.1, 3.72, xs[3] - 0.1, 3.72, bs.RED, lw=1.7, amp=0.55, n=26)
    ax.text((xs[0] + xs[3]) / 2, 3.95, "Alice 与 Bob 之间出现纠缠", fontsize=8.2,
            ha="center", color=bs.RED)

    ax.set_xlim(-0.55, 5.55)
    ax.set_ylim(-0.40, 4.30)
    ax.set_xlabel("距离")
    ax.set_ylabel("时间")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    bs.save(fig, CH, "fig01")


def fig_rate():
    L = np.linspace(100, 1600, 600)
    f_rep = 1e9
    alpha = 0.2
    direct = f_rep * 10 ** (-alpha * L / 10)

    N = np.arange(1, 17)
    rate = f_rep * 10 ** (-alpha * 100 / 10) / (N * 2.0 ** (N - 1))

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.semilogy(L, direct, color=bs.RED, lw=1.6, label="无中继，单段光纤直连")
    ax.semilogy(N * 100.0, rate, color=bs.BLUE, lw=1.6, marker="o", ms=3.6,
                label="中继链，每段 100 km")

    ax.set_xlim(100, 1600)
    ax.set_ylim(1e-26, 1e11)
    ax.set_xlabel("两端之间的距离（km）")
    ax.set_ylabel("每秒建立的纠缠对（对/s）")
    ax.set_xticks([100, 400, 800, 1200, 1600])
    ax.legend(loc="upper right")

    ax.annotate("1600 km 处相差\n二十多个数量级", xy=(1600, 19), xytext=(1010, 2e-9),
                fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_swap()
    fig_rate()
