"""第十九章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("foundations")

CH = "19"

RNG = np.random.default_rng(7)
T_DARK = 2.0     # 暗态平均停留时间，秒
T_BRIGHT = 0.8   # 亮态平均停留时间，秒
BIN = 0.02       # 计数时间bin，秒


def telegraph(total):
    """返回 (时间边界, 亮暗标记)。"""
    edges = [0.0]
    state = True
    while edges[-1] < total:
        mean = T_BRIGHT if state else T_DARK
        edges.append(edges[-1] + RNG.exponential(mean))
        state = not state
    return np.array(edges)


def fig_shelving():
    fig = plt.figure(figsize=(7.0, 3.3))
    gs = GridSpec(2, 2, width_ratios=[1.0, 1.5], wspace=0.28, hspace=0.62, figure=fig)

    # 左：三能级
    ax = fig.add_subplot(gs[:, 0])
    ax.set_xlim(0, 4.2)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    ax.plot([0.5, 2.3], [0.55, 0.55], color=bs.INK, lw=1.4)
    ax.plot([0.5, 2.3], [2.75, 2.75], color=bs.INK, lw=1.4)
    ax.plot([0.5, 2.3], [1.55, 1.55], color=bs.INK, lw=1.4)
    ax.text(2.42, 0.55, "$|g\\rangle$", fontsize=9, va="center")
    ax.text(2.42, 1.55, "$|D\\rangle$", fontsize=9, va="center")
    ax.text(2.42, 2.75, "$|e\\rangle$", fontsize=9, va="center")

    ax.annotate("", xy=(1.15, 2.62), xytext=(1.15, 0.68),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.3, mutation_scale=9))
    ax.text(0.22, 2.02, "493 nm\n强跃迁", fontsize=7.4, color=bs.BLUE, ha="left", va="bottom")

    ax.annotate("", xy=(1.85, 1.62), xytext=(1.85, 0.68),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.2, mutation_scale=9,
                                linestyle=(0, (4, 2))))
    ax.text(1.98, 0.92, "泵浦到暗态", fontsize=7.4, color=bs.ORANGE, ha="left", va="center")

    ax.annotate("", xy=(2.10, 2.62), xytext=(2.10, 1.68),
                arrowprops=dict(arrowstyle="-|>", color=bs.GRAY, lw=0.9, mutation_scale=8,
                                linestyle=(0, (2, 2))))
    ax.text(2.20, 2.18, "禁戒", fontsize=7.2, color=bs.GRAY, ha="left", va="center")

    # 右上：荧光记录
    ax2 = fig.add_subplot(gs[0, 1])
    edges = telegraph(600.0)
    t = np.arange(0, 26.0, BIN)
    rate = np.full_like(t, 0.4)
    for i in range(len(edges) - 1):
        mask = (t >= edges[i]) & (t < edges[i + 1])
        rate[mask] = 32.0 if i % 2 == 0 else 0.35
    counts = RNG.poisson(rate)
    ax2.plot(t, counts, color=bs.BLUE, lw=0.65)
    ax2.set_xlim(0, 26)
    ax2.set_ylim(-2, 62)
    ax2.set_xlabel("时间（秒）")
    ax2.set_ylabel("计数（每 20 毫秒）")
    ax2.text(0.6, 52, "亮", fontsize=8, color=bs.BLUE)
    bs.clean(ax2, grid_axis="y")

    # 右下：停留时间分布
    ax3 = fig.add_subplot(gs[1, 1])
    darks = (edges[2::2] - edges[1:-1:2])
    darks = darks[darks > 0]
    ax3.hist(darks, bins=np.arange(0, 9.0, 0.5), density=True,
             color="#dfe6ee", edgecolor="#9fb0c4", linewidth=0.7)
    tt = np.linspace(0, 9, 200)
    ax3.plot(tt, np.exp(-tt / T_DARK) / T_DARK, color=bs.RED, lw=1.2)
    ax3.text(4.3, 0.34, "$e^{-t/2\\,\\mathrm{s}}/2\\,\\mathrm{s}$", fontsize=7.6, color=bs.RED)
    ax3.set_xlim(0, 9)
    ax3.set_ylim(0, 0.55)
    ax3.set_xlabel("暗态停留时间（秒）")
    ax3.set_ylabel("概率密度（每秒）")
    bs.clean(ax3, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_zeno():
    fig, ax = plt.subplots(figsize=(5.6, 2.85))
    N = np.logspace(0, 3, 400)
    for frac, color, label in [(0.5, bs.BLUE, "总时间 $\\pi/2\\Omega$"),
                               (1.0, bs.RED, "总时间 $\\pi/\\Omega$")]:
        P = np.cos(np.pi * frac / (2 * N)) ** (2 * N)
        ax.plot(N, P, color=color, lw=1.5, label=label)
    ax.axhline(1.0, color="#c9d2dc", lw=0.8, ls=(0, (4, 3)))
    ax.set_xscale("log")
    ax.set_xlim(1, 1e3)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel("测量次数 $N$")
    ax.set_ylabel("留在初态的概率")
    ax.legend(loc="lower right", fontsize=7.6, handlelength=1.5, borderaxespad=0.3)
    ax.text(1.1, 0.06, "不测量", fontsize=7.4, color="#4a5563")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_shelving()
    fig_zeno()
