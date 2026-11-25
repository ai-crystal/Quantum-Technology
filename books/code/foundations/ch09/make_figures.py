"""第九章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("foundations")

CH = "09"


def fig_malus():
    th = np.linspace(0, 180, 600)
    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    ax.plot(th, np.cos(np.deg2rad(th)) ** 2, color=bs.BLUE, lw=1.5, label="经典光强")
    rng = np.random.default_rng(7)
    sample = np.arange(0, 181, 15)
    counts = rng.poisson(200 * np.cos(np.deg2rad(sample)) ** 2)
    ax.errorbar(sample, counts / 200.0, yerr=np.sqrt(counts) / 200.0, fmt="o", ms=3.2,
                color=bs.RED, ecolor=bs.RED, elinewidth=0.8, capsize=2, label="单光子计数（模拟）")
    ax.set_xlabel(r"偏振片转角 $\theta$ (度)")
    ax.set_ylabel("相对强度 / 计数率")
    ax.set_xlim(0, 180)
    ax.set_ylim(-0.04, 1.12)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.legend(loc="upper right", handlelength=1.6)
    ax.annotate(r"$\cos^2\theta$", xy=(45, 0.5), xytext=(58, 0.72), fontsize=9, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_mzi():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.6, 6.6)
    ax.axis("off")

    y1, y2 = 2.6, 4.8
    ax.annotate("", xy=(3.0, y1), xytext=(0.7, y1),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.6, shrinkA=0, shrinkB=0))
    ax.text(0.7, y1 + 0.16, "单光子源", fontsize=8.2, color=bs.RED, ha="left", va="bottom")

    ax.plot([3.0, 6.6], [y1, y1], color=bs.RED, lw=1.4)
    ax.plot([3.0, 3.0], [y1, y2], color=bs.RED, lw=1.4)
    ax.plot([3.0, 6.6], [y2, y2], color=bs.RED, lw=1.4)
    ax.plot([6.6, 6.6], [y1, y2], color=bs.RED, lw=1.4)
    ax.annotate("", xy=(8.8, y2), xytext=(6.6, y2),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.4, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(6.6, 5.7), xytext=(6.6, y2),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.4, shrinkA=0, shrinkB=0))

    def mirror(x, y, label, lx, ly, ha="left"):
        ax.plot([x - 0.20, x + 0.20], [y - 0.20, y + 0.20], color="#33414f", lw=2.6)
        ax.text(lx, ly, label, fontsize=7.8, color="#33414f", ha=ha, va="center")

    def beamsplitter(x, y, label, lx, ly, ha="center"):
        ax.plot([x - 0.20, x + 0.20], [y - 0.20, y + 0.20], color="#7d93aa", lw=1.4, ls=(0, (3, 2)))
        ax.text(lx, ly, label, fontsize=7.8, color="#33414f", ha=ha, va="center")

    mirror(3.0, y2, "M1", 2.72, y2 + 0.30, ha="right")
    mirror(6.6, y1, "M2", 6.86, y1 - 0.28, ha="left")
    beamsplitter(3.0, y1, "BS1", 2.62, y1 - 0.30, ha="right")
    beamsplitter(6.6, y2, "BS2", 6.86, y2 + 0.26, ha="left")

    for x, y, lab, lx, ly, ha in [(9.0, y2, "D1", 9.28, y2, "left"),
                                  (6.6, 5.85, "D2", 6.86, 5.85, "left")]:
        ax.add_patch(Rectangle((x - 0.22, y - 0.16), 0.44, 0.32, facecolor="#f5f8fc",
                               edgecolor="#33414f", lw=1.0))
        ax.text(lx, ly, lab, fontsize=7.8, color="#33414f", ha=ha, va="center")

    ax.text(4.8, y2 - 0.22, "路径 1", fontsize=7.8, color=bs.RED, ha="center", va="top")
    ax.text(4.8, y1 + 0.20, "路径 2", fontsize=7.8, color=bs.RED, ha="center", va="bottom")
    ax.text(0.7, 1.05, r"相位差 $\varphi$ 由两条路径的长度差决定", fontsize=8.2, color="#4a5563",
            ha="left", va="center")
    bs.save(fig, CH, "fig02")


def fig_counting():
    phi = np.arange(0, 361, 20)
    rng = np.random.default_rng(11)
    rate = 0.5 * (1 + np.cos(np.deg2rad(phi)))
    N = 400
    counts = rng.binomial(N, rate)
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.bar(phi, counts, width=12, color="#9db8d2", edgecolor="#5c7f9f", linewidth=0.5,
           yerr=np.sqrt(np.maximum(counts, 1)), error_kw=dict(ecolor="#33414f", lw=0.8, capsize=2))
    ax.plot(phi, N * rate, color=bs.RED, lw=1.4)
    ax.set_xlabel(r"相位差 $\varphi$ (度)")
    ax.set_ylabel("每 10 秒计数")
    ax.set_xlim(-10, 370)
    ax.set_ylim(0, 460)
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.text(120, 425, r"柱高为实测计数，曲线为 $N\cos^2(\varphi/2)$", fontsize=7.8, color="#4a5563")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_malus()
    fig_mzi()
    fig_counting()
