"""第 11 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("devices")

CH = "11"


def fig_shield():
    fig = plt.figure(figsize=(7.2, 3.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15], wspace=0.30)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 9.6)
    ax.set_ylim(0, 8.0)
    ax.axis("off")

    shells = [
        (0.25, 0.25, 5.0, 7.4, "#8a97a6", "坡莫合金\n室温"),
        (0.85, 0.85, 3.8, 6.2, "#7f9ab8", "铝壳\n50 K 与 4 K"),
        (1.45, 1.45, 2.6, 5.0, "#4a7f6a", "超导壳\n10 mK"),
    ]
    for x0, y0, w, h, c, _ in shells:
        ax.add_patch(Rectangle((x0, y0), w, h, facecolor="none", edgecolor=c, lw=1.4))

    ax.add_patch(Rectangle((2.35, 3.2), 0.8, 1.5, facecolor="#e3e9f0",
                           edgecolor="#4a5563", lw=0.9))
    ax.text(2.75, 3.05, "芯片", fontsize=7.0, color="#33414f", ha="center", va="top")

    ax.plot([2.75, 2.75], [7.65, 6.95], color="#b08d57", lw=0.8)
    ax.text(2.85, 7.30, "同轴", fontsize=6.8, color="#8a6a3a", ha="left", va="center")

    for (x0, y0, w, h, c, name), yy in zip(shells, (6.9, 4.4, 1.9)):
        ax.plot([x0 + w, 6.05], [y0 + h * 0.62, yy], color=c, lw=0.7, ls=(0, (3, 2)))
        ax.text(6.15, yy, name, fontsize=7.0, color=c, ha="left", va="center")

    ax.text(0.25, 7.75, "由外向内", fontsize=7.0, color="#6b7785", ha="left", va="bottom")

    ax = fig.add_subplot(gs[0, 1])
    f = np.logspace(0, 10, 500)
    mu0 = 4 * np.pi * 1e-7
    mats = [
        ("铜", 5.8e7, 1.0, bs.ORANGE),
        ("铝", 3.5e7, 1.0, bs.BLUE),
        ("坡莫合金", 1.6e6, 5e4, bs.GREEN),
    ]
    for name, sigma, mur, c in mats:
        delta = np.sqrt(2 / (mu0 * mur * sigma * 2 * np.pi * f))
        ax.loglog(f, delta * 1e3, color=c, lw=1.4, label=name)

    ax.axhline(3.0, color="#6b7785", lw=0.9, ls=(0, (4, 3)))
    ax.text(8e3, 4.2, "3 mm 罩壁", fontsize=7.0, color="#4a5563", va="bottom")
    ax.axhline(1e-4, color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(1.3, 6.5e-5, "超导穿透深度 100 nm", fontsize=7.0, color=bs.RED, va="top")

    ax.set_xlim(1, 1e10)
    ax.set_ylim(2e-5, 3e4)
    ax.set_xlabel("频率（Hz）")
    ax.set_ylabel("集肤深度（mm）")
    ax.legend(loc="upper right", fontsize=7.4, handlelength=1.6)
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig01")


def fig_event():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"wspace": 0.30})

    ax = axes[0]
    t = np.linspace(0, 1.2, 400)
    tau = 0.3
    for r, c in ((0.2, bs.RED), (1.0, bs.ORANGE), (3.0, bs.BLUE)):
        n = np.exp(-r / 1.0) * np.exp(-t / tau)
        ax.semilogy(t, n, color=c, lw=1.3, label=f"$r={r}$ mm")
    ax.set_xlabel("时间（ms）")
    ax.set_ylabel("准粒子密度（归一化）")
    ax.set_xlim(0, 1.2)
    ax.set_ylim(1e-3, 1.4)
    ax.legend(loc="upper right", fontsize=7.4, handlelength=1.6)
    ax.text(0.06, 2.2e-3, r"$n\propto e^{-r/L}e^{-t/\tau}$", fontsize=8.4, color="#33414f")
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    r = np.linspace(0, 5, 300)
    for L, c in ((0.5, bs.GREEN), (1.0, bs.ORANGE), (2.0, bs.BLUE)):
        ax.plot(r, 0.5 * np.exp(-r / L), color=c, lw=1.3, label=f"$L={L}$ mm")
    ax.set_xlabel("两个比特的间距（mm）")
    ax.set_ylabel("同时出错的概率")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 0.55)
    ax.legend(loc="upper right", fontsize=7.4, handlelength=1.6)
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_shield()
    fig_event()
