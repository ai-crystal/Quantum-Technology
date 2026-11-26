"""第二十章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("foundations")

CH = "20"


def resistance(T, Tc, width=0.12, Tmax=None):
    """归一化电阻：Tc 以下为零，以上按正常态线性回升。"""
    if Tmax is None:
        Tmax = 2.2 * Tc
    trans = 0.5 * (1 + np.tanh((T - Tc) / width))
    normal = 0.3 + 0.7 * np.clip((T - Tc) / (Tmax - Tc), 0, 1)
    return trans * normal


def fig_sc():
    fig = plt.figure(figsize=(7.0, 2.4))
    gs = GridSpec(1, 3, wspace=0.42, figure=fig)

    ax = fig.add_subplot(gs[0])
    T = np.linspace(0, 22, 700)
    ax.plot(T, resistance(T, 9.25), color=bs.BLUE, lw=1.5)
    ax.axvline(9.25, color="#c9d2dc", lw=0.8, ls=(0, (3, 3)))
    ax.annotate("9.25 K", xy=(9.25, 0.12), xytext=(11.0, 0.55), fontsize=7.4,
                color="#33414f", arrowprops=dict(arrowstyle="-|>", color="#8b98a8",
                                                lw=0.7, mutation_scale=7))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("温度（开尔文）")
    ax.set_ylabel("$R/R_n$")
    ax.text(0.6, 1.02, "铌", fontsize=8.2, color=bs.INK)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[1])
    T2 = np.linspace(0, 130, 900)
    ax2.plot(T2, resistance(T2, 92.0, width=1.2), color=bs.RED, lw=1.5)
    ax2.axvline(92.0, color="#c9d2dc", lw=0.8, ls=(0, (3, 3)))
    ax2.text(94.0, 0.62, "92 K", fontsize=7.4, color="#33414f", ha="left")
    ax2.axvline(77.0, color="#d8c9b4", lw=0.9)
    ax2.text(70.0, 1.06, "液氮 77 K", fontsize=7.0, color="#8a7355", ha="center")
    ax2.set_xlim(0, 130)
    ax2.set_ylim(0, 1.15)
    ax2.set_xlabel("温度（开尔文）")
    ax2.text(2.0, 1.02, "钇钡铜氧", fontsize=8.2, color=bs.INK)
    bs.clean(ax2, grid_axis="y")

    ax3 = fig.add_subplot(gs[2])
    delta = 0.18
    E = np.linspace(-0.8, 0.8, 1200)
    dos = np.zeros_like(E)
    mask = np.abs(E) > delta
    dos[mask] = np.abs(E[mask]) / np.sqrt(E[mask] ** 2 - delta ** 2)
    ax3.plot(E, dos, color=bs.GREEN, lw=1.4)
    ax3.fill_between(E, dos, 0, color=bs.GREEN, alpha=0.10)
    for s in (-1, 1):
        ax3.axvline(s * delta, color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax3.annotate("", xy=(delta, 0.12), xytext=(-delta, 0.12),
                 arrowprops=dict(arrowstyle="<|-|>", color=bs.ORANGE, lw=0.8,
                                 mutation_scale=6))
    ax3.text(0, 0.28, "$2\\Delta$", fontsize=7.6, color=bs.ORANGE, ha="center")
    ax3.set_xlim(-0.8, 0.8)
    ax3.set_ylim(0, 4.2)
    ax3.set_xlabel("能量（毫电子伏特）")
    ax3.set_ylabel("态密度 $N/N_0$")
    ax3.text(0.30, 3.1, "$\\Delta=0.18$ meV", fontsize=7.2, color=bs.GREEN, ha="left")
    bs.clean(ax3, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_squid():
    fig = plt.figure(figsize=(7.0, 2.7))
    gs = GridSpec(1, 2, width_ratios=[1.05, 1.0], wspace=0.30, figure=fig)

    ax = fig.add_subplot(gs[0])
    phi = np.linspace(-3, 3, 1200)
    ax.plot(phi, np.abs(np.cos(np.pi * phi)), color=bs.BLUE, lw=1.5)
    for s in (-2, -1, 1, 2):
        ax.axvline(s, color="#e2e8ef", lw=0.7, zorder=0)
    ax.annotate("", xy=(1.0, 1.12), xytext=(0.0, 1.12),
                arrowprops=dict(arrowstyle="<|-|>", color="#6b7785", lw=0.8, mutation_scale=7))
    ax.text(0.5, 1.16, "一个磁通量子 $\\Phi_0$", fontsize=7.6, color="#4a5563", ha="center")
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 1.32)
    ax.set_xlabel("环内磁通 $\\Phi/\\Phi_0$")
    ax.set_ylabel("临界电流 $I_c/I_{c0}$")
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[1])
    i = np.linspace(0, 1.05, 300)
    ax2.plot(5 * np.maximum(i - 1, 0), i, color=bs.GRAY, lw=1.1, ls=(0, (4, 2.5)),
             label="无微波")
    ax2.plot([0, 0], [0, 1.0], color=bs.GRAY, lw=1.1, ls=(0, (4, 2.5)))

    fs = 20.7
    hi = [1.0, 0.72, 0.48, 0.30, 0.18]
    lo = [0.78, 0.50, 0.30, 0.15, 0.05]
    for n in range(len(hi)):
        v = n * fs
        ax2.plot([v, v], [lo[n], hi[n]], color=bs.BLUE, lw=1.5)
        if n + 1 < len(hi):
            ax2.plot([v, v + fs], [lo[n], hi[n + 1]], color=bs.BLUE, lw=1.5)
        ax2.text(v, hi[n] + 0.035, "$V_%d$" % n, fontsize=6.8, color=bs.BLUE, ha="center")
    ax2.annotate("", xy=(fs, 0.34), xytext=(0, 0.34),
                 arrowprops=dict(arrowstyle="<|-|>", color=bs.ORANGE, lw=0.8, mutation_scale=6))
    ax2.text(fs / 2, 0.38, "20.7 微伏", fontsize=7.2, color=bs.ORANGE, ha="center")
    ax2.set_xlim(-4, 100)
    ax2.set_ylim(0, 1.25)
    ax2.set_xlabel("电压（微伏）")
    ax2.set_ylabel("电流 $I/I_c$")
    ax2.legend(loc="upper right", fontsize=7.2, handlelength=1.6, borderaxespad=0.3)
    bs.clean(ax2, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_sc()
    fig_squid()
