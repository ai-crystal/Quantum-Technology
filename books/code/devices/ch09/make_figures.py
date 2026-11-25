"""第 9 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "09"


def fig_scaling():
    n = np.logspace(1, 5, 400)
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.85), gridspec_kw={"wspace": 0.30})

    ax = axes[0]
    for y, color, name in [(0.99, bs.RED, "99.0%"), (0.995, bs.BLUE, "99.5%"),
                           (0.999, bs.GREEN, "99.9%")]:
        ax.loglog(n, y ** n, color=color, lw=1.4, label=f"单比特良率 {name}")
    ax.axhline(0.5, color="#c9d2dc", lw=0.8, ls=(0, (4, 3)))
    ax.set_xlim(10, 1e5)
    ax.set_ylim(1e-6, 1.4)
    ax.set_xlabel("芯片上的比特数")
    ax.set_ylabel("整片全部合格的概率")
    ax.legend(loc="lower left", handlelength=1.8)
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    mux = [1, 4, 16]
    for m, color in zip(mux, [bs.RED, bs.BLUE, bs.GREEN]):
        ax.loglog(n, n / m, color=color, lw=1.4, label=f"复用因子 {m}")
    ax.set_xlim(10, 1e5)
    ax.set_ylim(1, 1e5)
    ax.set_xlabel("芯片上的比特数")
    ax.set_ylabel("从室温引出的控制线数")
    ax.legend(loc="upper left", handlelength=1.8)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_threshold():
    p = np.logspace(np.log10(2e-4), np.log10(2e-2), 400)
    pth = 1e-2
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    for d, color in zip([3, 5, 7], [bs.ORANGE, bs.BLUE, bs.PURPLE]):
        pl = 0.1 * (p / pth) ** ((d + 1) / 2)
        ax.loglog(p * 100, pl, color=color, lw=1.4, label=f"码距 $d={d}$")
    ax.axvline(pth * 100, color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(pth * 100 * 1.08, 3e-6, "阈值 1%", fontsize=7.6, color=bs.RED, rotation=90, va="bottom")
    ax.set_xlim(0.02, 2)
    ax.set_ylim(1e-6, 1.0)
    ax.set_xlabel("物理错误率（%）")
    ax.set_ylabel("逻辑错误率")
    ax.legend(loc="upper left", handlelength=1.8)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_scaling()
    fig_threshold()
