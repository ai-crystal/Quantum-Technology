"""第 15 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

import bookstyle as bs

bs.use("devices")

CH = "15"


def fig_loading():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    t = np.linspace(0, 300, 400)
    for tau, col in [(20, bs.RED), (40, bs.BLUE), (80, bs.GREEN)]:
        mu = t / tau
        ax.plot(t, mu * np.exp(-mu), color=col, lw=1.3,
                label=r"$\tau=%d$ ms" % tau)
    ax.axhline(0.37, color="#8a97a6", lw=0.7, ls=(0, (4, 3)), label="单次上限 0.37")
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 0.55)
    ax.set_xlabel("装载时长（ms）")
    ax.set_ylabel(r"恰好一个原子的概率 $P_1$")
    ax.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    k = np.arange(1, 11)
    for p, col in [(0.4, bs.RED), (0.6, bs.BLUE), (0.8, bs.GREEN)]:
        ax2.plot(k, 1 - (1 - p) ** k, "o-", color=col, lw=1.2, ms=4.0,
                 label=r"单轮成功率 %d%%" % int(p * 100))
    ax2.axhline(0.99, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax2.text(0.75, 1.005, "99%", fontsize=7.4, color="#4a5563")
    ax2.set_xlim(0.5, 10.5)
    ax2.set_ylim(0.3, 1.04)
    ax2.set_xticks([1, 2, 3, 5, 7, 9])
    ax2.set_xlabel("重排轮数")
    ax2.set_ylabel("阵列填充率")
    ax2.legend(loc="lower right", fontsize=7.4)
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_rydberg_readout():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    r = np.linspace(1.5, 16, 400)
    C6 = {60: 862 * (60 / 70.0) ** 11, 70: 862.0, 80: 862 * (80 / 70.0) ** 11}
    for n, col in [(60, bs.RED), (70, bs.BLUE), (80, bs.GREEN)]:
        v = C6[n] * 1e3 / r ** 6
        ax.semilogy(r, v, color=col, lw=1.3, label=r"$n=%d$" % n)
    for om, ls in [(2.0, (0, (4, 3))), (10.0, (0, (1, 2)))]:
        ax.axhline(om, color="#8a97a6", lw=0.7, ls=ls)
        ax.text(15.6, om * 1.25, r"$\Omega/2\pi=%d$ MHz" % int(om), fontsize=7.2,
                color="#4a5563", ha="right")
    ax.set_xlim(1.5, 16)
    ax.set_ylim(1e0, 1e5)
    ax.set_xlabel(r"原子间距（$\mu$m）")
    ax.set_ylabel(r"$V/2\pi$（MHz）")
    ax.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    nbar = np.linspace(5, 400, 400)
    for dark, col in [(0.2, bs.GREEN), (1.0, bs.BLUE), (3.0, bs.RED)]:
        k = np.floor((nbar + dark) / 2)
        err = 0.5 * (poisson.cdf(k, nbar) + 1 - poisson.cdf(k, dark))
        ax2.semilogy(nbar, err, color=col, lw=1.3, label="暗计数均值 %.1f" % dark)
    ax2.axhline(1e-3, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax2.text(120, 1.4e-3, "千分之一", fontsize=7.4, color="#4a5563")
    ax2.set_xlim(5, 200)
    ax2.set_ylim(1e-6, 0.3)
    ax2.set_xlabel("亮态平均收集光子数")
    ax2.set_ylabel("判决错误率")
    ax2.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_loading()
    fig_rydberg_readout()
