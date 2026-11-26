"""第十五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "15"

P2 = 1e-3
PM = 1e-2
PPREP = 1e-3
PIDLE = 5e-4
PTH = 6e-3


def p_cycle(pm):
    return (4 * P2 + 0.5 * (PPREP + pm) + 2 * PIDLE) / 7.0


def fig_budget():
    items = [
        ("读出", "$1.0\\times10^{-2}$", 0.5 * PM, "#c07a1e"),
        ("双比特门", "$1.0\\times10^{-3}$", 4 * P2, "#2b5c94"),
        ("空闲", "$5.0\\times10^{-4}$", 2 * PIDLE, "#6b7785"),
        ("初始化", "$1.0\\times10^{-3}$", 0.5 * PPREP, "#3d7a5a"),
    ]
    total = sum(v for _, _, v, _ in items)
    fig, ax = plt.subplots(figsize=(6.2, 2.95))
    for k, (name, raw, v, col) in enumerate(items):
        y = len(items) - 1 - k
        share = 100.0 * v / total
        ax.barh(y, share, height=0.5, color=col, alpha=0.9, zorder=3)
        ax.text(share + 1.5, y, f"{share:.0f}%", fontsize=8.2, color="#33414f",
                va="center", ha="left")
        ax.text(-1.8, y, name, fontsize=8.4, color="#33414f", ha="right", va="center")
        ax.text(-15.5, y, raw, fontsize=7.6, color="#6b7785", ha="right", va="center")

    ax.text(78, -0.36, "折算后 $p=0.15\\%$", fontsize=7.8, color="#6b7785",
            ha="right", va="center")

    ax.set_xlim(0, 80)
    ax.set_ylim(-0.6, 3.6)
    ax.set_yticks([3, 2, 1, 0])
    ax.set_yticklabels([""] * 4)
    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_xlabel("占每周期总错误的份额（%）")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    bs.clean(ax, grid_axis="x")
    bs.save(fig, CH, "fig01")


def fig_sensitivity():
    pm = np.logspace(-3, np.log10(3e-2), 400)
    p = p_cycle(pm)
    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    for d, c in zip([3, 5, 7], ["#9db4cc", "#5f86b0", bs.BLUE]):
        pl = 0.1 * (p / PTH) ** ((d + 1) / 2.0)
        ax.loglog(pm, pl, color=c, lw=1.4)
        ax.text(pm[0] * 1.08, pl[0] * 1.45, f"$d={d}$", fontsize=7.8, color=c,
                ha="left", va="bottom")

    pl7 = lambda x: 0.1 * (p_cycle(x) / PTH) ** 4
    ax.plot([PM, 3e-3], [pl7(PM), pl7(3e-3)], "o", ms=4.6, color=bs.BLUE, zorder=5)
    ax.annotate("", xy=(9.4e-3, 5.4e-4), xytext=(3.1e-3, 1.02e-4),
                arrowprops=dict(arrowstyle="<->", color="#7c9ab8", lw=1.0))
    ax.text(4.6e-3, 1.6e-4, "五倍", fontsize=8.0, color=bs.BLUE, ha="center",
            va="bottom")

    ax.axvline(PM, color=bs.ORANGE, lw=1.1, ls=(0, (3, 2.5)))
    ax.text(1.06e-2, 3.0e-2, "今天的读出水平", fontsize=7.4, color=bs.ORANGE,
            ha="left", va="top")

    ax.set_xlabel("读出错误率 $p_m$")
    ax.set_ylabel("逻辑错误率 $p_L$")
    ax.set_xlim(1e-3, 3e-2)
    ax.set_xticks([1e-3, 3e-3, 1e-2, 3e-2])
    ax.set_xticklabels(["$10^{-3}$", "$3\\times10^{-3}$", "$10^{-2}$", "$3\\times10^{-2}$"])
    ax.minorticks_off()
    ax.set_ylim(2e-5, 4e-2)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_budget()
    fig_sensitivity()
