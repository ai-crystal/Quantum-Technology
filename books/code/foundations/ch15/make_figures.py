"""第十五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("foundations")

CH = "15"


def fig_packet():
    fig = plt.figure(figsize=(7.0, 2.75))
    gs = GridSpec(1, 2, width_ratios=[1.5, 1.0], wspace=0.30, figure=fig)

    # 左：两列波叠成包
    ax = fig.add_subplot(gs[0])
    x = np.linspace(0, 1.0, 3000)
    kbar = 2 * np.pi * 28
    dk = 2 * np.pi * 3.0
    f = np.cos((kbar + dk / 2) * x) + np.cos((kbar - dk / 2) * x)
    env = 2 * np.abs(np.cos(dk * x / 2))
    ax.plot(x, f, color=bs.BLUE, lw=0.9)
    ax.plot(x, env, color=bs.RED, lw=1.0, ls=(0, (5, 2.5)))
    ax.plot(x, -env, color=bs.RED, lw=1.0, ls=(0, (5, 2.5)))
    ax.axhline(0, color="#c9d2dc", lw=0.6)
    ax.annotate("包络", xy=(0.165, 1.92), xytext=(0.23, 2.55), fontsize=8, color=bs.RED,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7, mutation_scale=7))
    ax.annotate("载波", xy=(0.55, 1.35), xytext=(0.60, 2.55), fontsize=8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, mutation_scale=7))
    ax.annotate("", xy=(0.5, -2.35), xytext=(0.1667, -2.35),
                arrowprops=dict(arrowstyle="<|-|>", color="#6b7785", lw=0.8, mutation_scale=7))
    ax.text(0.333, -2.15, "包络宽 $\\pi/\\Delta k$", fontsize=7.6, ha="center", color="#4a5563")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-3.1, 3.1)
    ax.set_xlabel("位置")
    ax.set_yticks([])
    ax.set_ylabel("振幅")
    bs.clean(ax)

    # 右：色散曲线上的两种速度
    ax2 = fig.add_subplot(gs[1])
    k = np.linspace(0.05, 2.9, 400)
    w = 0.30 * k ** 2 + 0.25 * k
    k0 = 2.0
    w0 = 0.30 * k0 ** 2 + 0.25 * k0
    ax2.plot(k, w, color=bs.BLUE, lw=1.4)
    ax2.plot([0, k0], [0, w0], color=bs.GREEN, lw=1.0, ls=(0, (5, 2.5)))
    ax2.plot([k0 - 1.35, k0 + 0.95], [w0 - 1.35 * (0.6 * k0 + 0.25), w0 + 0.95 * (0.6 * k0 + 0.25)],
             color=bs.RED, lw=1.0)
    ax2.plot([k0], [w0], "o", ms=4.2, color=bs.INK, zorder=5)
    ax2.plot([k0, k0], [0, w0], color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax2.plot([0, k0], [w0, w0], color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax2.text(k0 + 0.10, w0 - 0.42, "$v_g=\\mathrm{d}\\omega/\\mathrm{d}k$", fontsize=8, color=bs.RED)
    ax2.text(1.02, 0.55 * w0 + 0.30, "$v_p=\\omega/k$", fontsize=8, color=bs.GREEN, rotation=0)
    ax2.set_xlim(0, 3.0)
    ax2.set_ylim(0, 3.6)
    ax2.set_xlabel("波数 $k$")
    ax2.set_ylabel("角频率 $\\omega$")
    bs.clean(ax2)

    bs.save(fig, CH, "fig01")


def fig_spread():
    fig = plt.figure(figsize=(7.0, 2.7))
    gs = GridSpec(1, 2, width_ratios=[1.0, 1.15], wspace=0.30, figure=fig)

    # 左：普适扩散曲线
    ax = fig.add_subplot(gs[0])
    t = np.logspace(-2, 2.2, 400)
    s = np.sqrt(1 + t ** 2)
    ax.plot(t, s, color=bs.BLUE, lw=1.4)
    ax.plot(t, t, color=bs.GRAY, lw=0.8, ls=(0, (3, 3)))
    ax.axvline(1.0, color="#c9d2dc", lw=0.8, ls=(0, (2, 3)))
    ax.axhline(np.sqrt(2), color="#c9d2dc", lw=0.8, ls=(0, (2, 3)))
    ax.text(2.3, 1.06, "$t=\\tau$", fontsize=7.8, color="#4a5563")
    ax.text(12, 7.0, "$\\sigma\\approx\\sigma_0\\,t/\\tau$", fontsize=7.8, color=bs.GRAY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-2, 1.6e2)
    ax.set_ylim(0.9, 200)
    ax.set_xlabel("时间 $t/\\tau$")
    ax.set_ylabel("宽度 $\\sigma/\\sigma_0$")
    bs.clean(ax)

    # 右：三个时刻的波包形状
    ax2 = fig.add_subplot(gs[1])
    x = np.linspace(-14, 14, 800)
    s0 = 1.0
    for tt, color, ls in [(0.0, bs.BLUE, "-"), (1.0, bs.GREEN, "-"), (3.0, bs.RED, "-")]:
        sg = s0 * np.sqrt(1 + tt ** 2)
        p = np.exp(-x ** 2 / (2 * sg ** 2)) / (np.sqrt(2 * np.pi) * sg)
        ax2.plot(x, p, color=color, lw=1.3, ls=ls, label="$t=%.0f\\tau$" % tt)
    ax2.legend(loc="upper left", handlelength=1.6, borderaxespad=0.4)
    ax2.set_xlim(-14, 14)
    ax2.set_ylim(0, 0.52)
    ax2.set_xlabel("位置 $x$（纳米）")
    ax2.set_ylabel("概率密度（每纳米）")
    bs.clean(ax2)

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_packet()
    fig_spread()
