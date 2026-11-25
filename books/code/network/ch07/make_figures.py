"""第 7 章插图：原子频率梳的原理与各体系存储指标的对照。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("network")

CH = "07"


def fig_afc():
    DELTA = 2.0    # 梳齿间距 MHz
    sigma = 13.0

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.8),
                             gridspec_kw={"width_ratios": [1.0, 1.12], "wspace": 0.30})

    ax = axes[0]
    det = np.linspace(-26, 26, 800)
    env = np.exp(-det ** 2 / (2 * sigma ** 2))
    ax.fill_between(det, 0, env, color="#eef2f7", zorder=0)
    ax.plot(det, env, color=bs.GRAY, lw=0.9, ls=(0, (4, 3)), zorder=2)
    for kk in np.arange(-13, 14):
        h = np.exp(-(kk * DELTA) ** 2 / (2 * sigma ** 2))
        if h < 0.02:
            continue
        ax.add_patch(Rectangle((kk * DELTA - 0.07, 0), 0.14, h, fc=bs.BLUE,
                               ec="none", zorder=3))
    ax.plot([18, 18], [0, 0.62], color=bs.RED, lw=0.7, ls=(0, (2, 2)), zorder=5)
    ax.plot([20, 20], [0, 0.62], color=bs.RED, lw=0.7, ls=(0, (2, 2)), zorder=5)
    ax.text(19.2, 0.74, r"$\Delta$", fontsize=8.6, ha="left", color=bs.RED)
    ax.annotate("", xy=(-20, 1.12), xytext=(20, 1.12),
                arrowprops=dict(arrowstyle="<->", color="#5b6a7a", lw=0.8, mutation_scale=7))
    ax.text(0, 1.16, "带宽 $B$", fontsize=8.2, ha="center", color="#5b6a7a")
    ax.set_xlim(-26, 26)
    ax.set_ylim(0, 1.26)
    ax.set_xlabel("相对中心频率的失谐（MHz）")
    ax.set_ylabel("吸收（归一化）")
    ax.set_xticks([-20, -10, 0, 10, 20])
    bs.clean(ax)

    ax = axes[1]
    t = np.linspace(-120, 780, 1600)
    sig_in = np.exp(-(t ** 2) / (2 * 22.0 ** 2))
    echo = 0.30 * np.exp(-((t - 500) ** 2) / (2 * 26.0 ** 2))
    ax.axvspan(0, 500, color="#eef2f7", zorder=0)
    ax.fill_between(t, 0, sig_in, color=bs.BLUE, alpha=0.16, zorder=2)
    ax.plot(t, sig_in, color=bs.BLUE, lw=1.4, label="输入的信号脉冲", zorder=3)
    ax.fill_between(t, 0, echo, color=bs.ORANGE, alpha=0.20, zorder=2)
    ax.plot(t, echo, color=bs.ORANGE, lw=1.4, label="回声，效率 30%", zorder=3)
    ax.text(250, 0.55, "激发留在晶体里\n各组分相位逐渐分开", fontsize=7.6,
            ha="center", va="center", color="#4a5563")
    ax.annotate("", xy=(0, 0.09), xytext=(500, 0.09),
                arrowprops=dict(arrowstyle="<->", color=bs.RED, lw=1.0, mutation_scale=7))
    ax.text(250, 0.145, r"$t=1/\Delta=500$ ns", fontsize=8.2, ha="center", color=bs.RED)
    ax.set_xlim(-120, 780)
    ax.set_ylim(0, 1.30)
    ax.set_xlabel("时间（ns）")
    ax.set_ylabel("光强（归一化）")
    ax.set_yticks([0, 0.3, 0.6, 0.9])
    ax.legend(loc="upper right", fontsize=7.6, handlelength=1.8)
    bs.clean(ax)

    bs.save(fig, CH, "fig01")


def fig_platforms():
    # 名称, 可读出光子的存储时间（s）, 寿命范围, 总效率, 标签位置, 对齐
    data = [
        ("稀土 自旋波",   1.0,   (1e-2, 1e1),  0.15, (2.6, 25.0), "left"),
        ("冷原子系综",     1e-3,  (1e-4, 1e-1), 0.85, (1.2e-3, 93.0), "center"),
        ("热原子蒸气",     1e-3,  (3e-4, 4e-3), 0.60, (1.2e-3, 51.5), "center"),
        ("掺铒晶体",       2e-3,  (5e-4, 5e-2), 0.22, (2.0e-2, 33.0), "left"),
        ("稀土 光子回声",  2e-6,  (2e-7, 1e-4), 0.32, (1.4e-6, 41.0), "center"),
        ("金刚石色心",     1e-2,  (1e-3, 1e-1), 0.06, (3.4e-2, 7.0), "left"),
    ]

    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.add_patch(Rectangle((1e-1, 50), 2.9e1, 50, fc="#f2f7f2", ec=bs.GREEN,
                           lw=1.0, ls=(0, (4, 3)), zorder=0))
    ax.text(1.3e-1, 96, "中继链路要求的区间", fontsize=8.0, color=bs.GREEN, va="top")

    for name, T, rng, eta, txt, ha in data:
        ax.errorbar([T], [eta * 100],
                    xerr=[[T - rng[0]], [rng[1] - T]],
                    fmt="o", ms=5.0, color=bs.BLUE, ecolor="#9fb0c2",
                    elinewidth=1.0, capsize=2.2, zorder=4)
        ax.annotate(name, xy=(T, eta * 100), xytext=txt,
                    fontsize=7.8, ha=ha, va="center", color="#33414f",
                    arrowprops=dict(arrowstyle="-", color="#a9b6c4", lw=0.6,
                                    shrinkA=0, shrinkB=3))

    ax.set_xscale("log")
    ax.minorticks_off()
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlim(5e-8, 5e1)
    ax.set_ylim(0, 100)
    ax.set_xlabel("可读出光子的存储时间（s）")
    ax.set_ylabel("存储加读出的效率（%）")
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_afc()
    fig_platforms()
