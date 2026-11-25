"""第 6 章插图：光子到达时间的熵，以及贝尔随机数的熵界与速率量级。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("network")

CH = "06"


def fig_timing():
    rate = 10.0      # 光子率 MHz
    window = 400.0   # 采样窗口 ns
    lam_tau = rate * window * 1e-3   # 无量纲

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.85),
                             gridspec_kw={"width_ratios": [1.1, 1.0], "wspace": 0.30})

    ax = axes[0]
    nb = 20
    edges = np.linspace(0, window, nb + 1)
    w = np.diff(edges) * rate * 1e-3
    edges_lam = edges * rate * 1e-3
    p = np.exp(-edges_lam[:-1]) - np.exp(-edges_lam[1:])
    ax.bar(edges[:-1], p, width=np.diff(edges), align="edge",
           color=bs.BLUE, alpha=0.55, ec="none", label="各区间落点的概率")
    tau = np.linspace(0, window, 400)
    ax.plot(tau, np.exp(-rate * tau * 1e-3) * (1 - np.exp(-lam_tau / nb)),
            color=bs.RED, lw=1.3, label="泊松过程的指数衰减")
    ax.set_xlabel("相邻两个光子的时间间隔（ns）")
    ax.set_ylabel("概率")
    ax.set_xlim(0, window)
    ax.set_ylim(0, 0.245)
    ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
    ax.set_xticks([0, 100, 200, 300, 400])
    ax.legend(loc="upper right", fontsize=7.4)
    ax.text(215, 0.098, "间隔越短越常见\n分布很不均匀", fontsize=7.4, color="#4a5563")
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    N = np.arange(2, 257)
    hmin = -np.log2(1 - np.exp(-lam_tau / N))
    ax.plot(N, np.log2(N), color="#b8c2ce", lw=1.0, ls=(0, (4, 3)), label="平均每样本的理想上限")
    ax.plot(N, hmin, color=bs.BLUE, lw=1.6, label="最小熵下界")
    ax.set_xscale("log", base=2)
    ax.minorticks_off()
    ax.set_xlim(2, 256)
    ax.set_ylim(0, 8.6)
    ax.set_xticks([2, 4, 8, 16, 32, 64, 128, 256])
    ax.set_xticklabels(["2", "4", "8", "16", "32", "64", "128", "256"], fontsize=7.6)
    ax.set_xlabel("把窗口切成的档数 $N$")
    ax.set_ylabel("每个样本的比特数")
    ax.plot([16], [2.18], "o", ms=4.2, color=bs.RED, zorder=5)
    ax.annotate("2.18", xy=(16, 2.18), xytext=(14.2, 2.62),
                fontsize=7.6, color=bs.RED, ha="right",
                bbox=dict(fc="white", ec="none", pad=1.2))
    ax.legend(loc="lower right", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_bell():
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.85),
                             gridspec_kw={"width_ratios": [1.05, 1.0], "wspace": 0.36})

    ax = axes[0]
    S = np.linspace(2.0, 2 * np.sqrt(2), 400)
    H = 1 - np.log2(1 + np.sqrt(np.clip(2 - S ** 2 / 4, 0, None)))
    ax.plot(S, H, color=bs.BLUE, lw=1.7)
    for s, txt, dy in [(2.2, "0.08", 0.0), (2.6, "0.36", 0.0)]:
        h = 1 - np.log2(1 + np.sqrt(2 - s ** 2 / 4))
        ax.plot([s, s], [0, h], color=bs.RED, lw=0.7, ls=(0, (2, 2)))
        ax.plot([s], [h], "o", ms=3.8, color=bs.RED, zorder=4)
        ax.annotate(txt, xy=(s, h), xytext=(s - 0.10, h + 0.09),
                    fontsize=7.6, color=bs.RED, ha="right")
    ax.text(2.02, 0.90, "经典上限 $S=2$ 处熵为零", fontsize=7.4, color="#4a5563")
    ax.set_xlim(2.0, 2.84)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("贝尔不等式违反量 $S$")
    ax.set_ylabel("每轮的最小熵（比特）")
    ax.set_xticks([2.0, 2.2, 2.4, 2.6, 2.8])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    rows = [
        ("设备无关发生器", 1.0, 1e2, bs.RED),
        ("商用随机数板卡", 1e6, 1.6e7, bs.BLUE),
        ("集成到芯片", 1e7, 1e9, bs.GREEN),
    ]
    names = []
    for i, (name, lo, hi, c) in enumerate(rows):
        y = len(rows) - 1 - i
        names.append((y, name))
        ax.plot([lo, hi], [y, y], color=c, lw=5.5, solid_capstyle="butt", alpha=0.55)
        ax.plot([lo, hi], [y, y], "|", color=c, ms=10, mew=1.4)
        ax.text(lo, y + 0.26, name, fontsize=7.5, va="bottom", ha="left",
                color="#33414f")
    ax.set_xscale("log")
    ax.minorticks_off()
    ax.set_xlim(0.6, 3e9)
    ax.set_ylim(-0.45, 2.75)
    ax.set_yticks([])
    ax.set_xticks([1e0, 1e3, 1e6, 1e9])
    ax.set_xticklabels(["1", "1k", "1M", "1G"])
    ax.set_xlabel("每秒产生的比特数（量级）")
    ax.tick_params(axis="y", length=0)
    bs.clean(ax, grid_axis="x")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_timing()
    fig_bell()
