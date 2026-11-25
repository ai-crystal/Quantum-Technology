"""第十二章插图：振幅估计的精度、线性方程组的代价等值线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import bookstyle as bs

bs.use("computing")
CH = "12"


def fig_qae():
    M = np.logspace(1, 6, 60)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.loglog(M, 0.8 / np.sqrt(M), "-", lw=1.2, color=bs.RED, label=r"经典抽样 $1/\sqrt{M}$")
    ax.loglog(M, 2.2 / M, "-", lw=1.2, color=bs.BLUE, label=r"振幅估计 $1/M$")
    ax.plot([1e4], [0.8 / 1e2], "o", ms=5.5, color=bs.RED, mfc="white", mew=1.3)
    ax.plot([1e4], [2.2 / 1e4], "o", ms=5.5, color=bs.BLUE, mfc="white", mew=1.3)
    ax.axvline(1e4, color="#c9d2dc", lw=0.8, ls=(0, (3, 3)))
    ax.text(1.15e4, 0.30, r"同样调用 $10^4$ 次", fontsize=7.6, color="#6b7785")
    ax.text(2.6e4, 9e-5, "误差小三十余倍", fontsize=7.6, color="#4a5563")
    ax.set_xlabel("对被测过程的调用次数 $M$")
    ax.set_ylabel("估计误差")
    ax.set_xlim(10, 1e6)
    ax.set_ylim(1e-6, 0.6)
    ax.legend(loc="lower left", fontsize=7.8, handlelength=2.2)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_contour():
    kap = np.logspace(0, 2, 240)
    eps = np.logspace(-1, -5, 240)
    K, E = np.meshgrid(kap, eps)
    gates = K ** 2 * 20.0 / E

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    cf = ax.pcolormesh(K, E, gates, cmap="Blues",
                       norm=LogNorm(vmin=1e2, vmax=1e11), shading="auto", rasterized=True)
    ax.contour(K, E, gates, levels=[1e4], colors="#1f2a37", linewidths=0.6, linestyles=":")
    ax.contour(K, E, gates, levels=[1e10], colors="#1f2a37", linewidths=0.7)
    cs = ax.contour(K, E, gates, levels=[1e6, 1e8], colors="#1f2a37", linewidths=0.7)
    ax.clabel(cs, fmt=lambda v: rf"$10^{{{int(np.log10(v))}}}$", fontsize=7.4, inline=True)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(0.13, 2.2e-5)
    ax.set_xlabel(r"条件数 $\kappa$")
    ax.set_ylabel(r"目标精度 $\varepsilon$")
    ax.set_yticks([1e-1, 1e-2, 1e-3, 1e-4, 1e-5])
    ax.set_yticklabels([r"$10^{-1}$", r"$10^{-2}$", r"$10^{-3}$", r"$10^{-4}$", r"$10^{-5}$"])
    cb = fig.colorbar(cf, ax=ax, pad=0.02, ticks=[1e2, 1e4, 1e6, 1e8, 1e10])
    cb.set_label("估计门数", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    bs.save(fig, CH, "fig02", kind="photo")


if __name__ == "__main__":
    fig_qae()
    fig_contour()
