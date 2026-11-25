"""第 3 章插图：弱相干光的光子数分布、三类脉冲的占比。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "03"


def poisson(mu, n):
    from math import exp, factorial

    return np.array([exp(-mu) * mu ** k / factorial(k) for k in n])


def fig_photon_number():
    n = np.arange(0, 9)
    means = [(0.1, bs.BLUE, "o"), (0.5, bs.ORANGE, "s"), (1.0, bs.RED, "^")]
    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    width = 0.26
    for i, (mu, color, mk) in enumerate(means):
        p = poisson(mu, n)
        ax.bar(n + (i - 1) * width, p, width=width * 0.94, color=color, alpha=0.85,
               label=f"$\\mu={mu}$", edgecolor="white", linewidth=0.4)
        p_multi = 1 - p[0] - p[1]
        ax.text(8.42, max(p) + 0.02, "", fontsize=8)
    ax.set_xlim(-0.65, 8.65)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(n)
    ax.set_xlabel("每个脉冲里的光子数 $n$")
    ax.set_ylabel("概率 $P(n)$")
    ax.legend(loc="upper right", ncol=3)
    ax.text(4.6, 0.68, "$\\mu=1$ 时多光子占 26%\n$\\mu=0.1$ 时只占 0.5%",
            fontsize=8, color="#4a5563")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_share():
    mu = np.linspace(0.01, 1.5, 400)
    p0 = np.exp(-mu)
    p1 = mu * np.exp(-mu)
    p2 = 1 - p0 - p1

    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    ax.plot(mu, p0 * 100, color=bs.GRAY, lw=1.5, label="零光子，被阻断")
    ax.plot(mu, p1 * 100, color=bs.BLUE, lw=1.6, label="单光子，可用")
    ax.plot(mu, p2 * 100, color=bs.RED, lw=1.6, label="多光子，可被分光")

    ax.axvline(0.5, color="#c3ccd6", lw=0.8, ls=(0, (4, 3)))
    for yv, cv, lb in [(np.exp(-0.5) * 100, bs.GRAY, "61%"),
                       (0.5 * np.exp(-0.5) * 100, bs.BLUE, "30%"),
                       ((1 - np.exp(-0.5) * 1.5) * 100, bs.RED, "9%")]:
        ax.plot([0.5], [yv], "o", ms=4.5, color=cv, zorder=5)
        ax.text(0.54, yv + 3.4, lb, fontsize=8.2, color=cv)
    ax.text(0.52, 98, "$\\mu=0.5$", fontsize=8.5, color="#4a5563")

    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 105)
    ax.set_xlabel("平均光子数 $\\mu$")
    ax.set_ylabel("脉冲占比（%）")
    ax.legend(loc="center right")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_photon_number()
    fig_share()
