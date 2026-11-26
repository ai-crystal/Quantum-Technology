"""第 17 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "17"

E = 1.602176634e-19
EPS0 = 8.8541878128e-12
KB = 1.380649e-23


def charging_meV(d_nm, eps_r=11.7):
    a = d_nm * 1e-9 / 2
    C = 8 * eps_r * EPS0 * a
    return E ** 2 / (2 * C) / E * 1e3


def fig_dot():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    d = np.linspace(12, 120, 400)
    ax.plot(d, charging_meV(d), color=bs.BLUE, lw=1.4)
    for dd in [20, 40, 80]:
        ax.plot(dd, charging_meV(dd), "o", color=bs.BLUE, ms=4.5)
        ax.annotate("%.1f meV" % charging_meV(dd), (dd, charging_meV(dd)),
                    textcoords="offset points", xytext=(8, 6), fontsize=7.2,
                    color="#33414f")
    ax.set_xlim(12, 120)
    ax.set_ylim(0, 10)
    ax.set_xlabel("量子点直径（nm）")
    ax.set_ylabel("充电能（meV）")
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    w = np.linspace(0.4, 5.0, 400)
    ax2.semilogy(w, 0.8 * np.exp(-w / 1.2), color=bs.RED, lw=1.4)
    ax2.set_xlim(0.4, 5.0)
    ax2.set_ylim(1e-3, 2)
    ax2.set_xlabel("界面过渡层厚度（nm）")
    ax2.set_ylabel("谷分裂（meV）")
    ax2.text(2.2, 0.35, "陡界面", fontsize=7.4, color="#4a5563")
    ax2.text(3.3, 0.012, "渐变界面", fontsize=7.4, color="#4a5563")
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_yield():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    n = np.logspace(0, 4, 400)
    for p, col in [(0.001, bs.GREEN), (0.01, bs.BLUE), (0.05, bs.RED)]:
        ax.semilogx(n, (1 - p) ** n, color=col, lw=1.3,
                    label="单点失效率 %.1f%%" % (p * 100))
    ax.axhline(0.5, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax.text(1.2, 0.54, "50%", fontsize=7.2, color="#4a5563")
    ax.set_xlim(1, 1e4)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("阵列中的量子点数")
    ax.set_ylabel("全部可用的概率")
    ax.legend(loc="lower left", fontsize=7.2)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    d = np.linspace(12, 120, 400)
    tmax = charging_meV(d) * 1e-3 * E / (20 * KB)
    ax2.plot(d, tmax, color=bs.BLUE, lw=1.4)
    ax2.axhline(4.2, color=bs.RED, lw=0.8, ls=(0, (4, 3)))
    ax2.text(70, 4.6, "液氦 4.2 K", fontsize=7.2, color=bs.RED)
    ax2.axhline(1.0, color=bs.GREEN, lw=0.8, ls=(0, (4, 3)))
    ax2.text(95, 1.2, "1 K", fontsize=7.2, color=bs.GREEN)
    ax2.set_xlim(12, 120)
    ax2.set_ylim(0, 12)
    ax2.set_xlabel("量子点直径（nm）")
    ax2.set_ylabel("单电子限制允许的最高温度（K）")
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_dot()
    fig_yield()
