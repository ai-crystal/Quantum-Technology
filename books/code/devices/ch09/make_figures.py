"""第 9 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("devices")

CH = "09"


def fig_ladder():
    fig = plt.figure(figsize=(7.2, 3.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.34)

    # 左：分级结构
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 6.3)
    ax.set_ylim(0.75, 11.75)
    ax.axis("off")

    stages = [
        (9.9, "300 K 室温法兰", "无冷量"),
        (8.5, "50 K 级", "40 W"),
        (7.1, "4 K 级", "1.5 W"),
        (5.7, "1 K 罐", "20 mW"),
        (4.2, "100 mK 级", "400 µW"),
        (2.6, "10 mK 混合室", "4 µW"),
    ]

    # 同轴线，先画在冷板后面
    for x in (2.8, 3.5, 4.2):
        ax.plot([x, x], [9.9, 2.6], color="#b9c3cf", lw=0.7, zorder=1)

    for y, name, power in stages:
        ax.add_patch(Rectangle((0.5, y - 0.09), 5.4, 0.18,
                               facecolor="#e3e9f0", edgecolor="#8a97a6", lw=0.8, zorder=2))
        ax.text(0.5, y + 0.33, name, fontsize=7.4, color="#33414f", ha="left", va="bottom",
                zorder=4)
        ax.text(5.9, y + 0.33, power, fontsize=7.4, color=bs.RED, ha="right", va="bottom", zorder=4)
        for x in (2.8, 3.5, 4.2):
            ax.add_patch(Rectangle((x - 0.13, y - 0.045), 0.26, 0.09,
                                   facecolor="#b08d57", edgecolor="none", zorder=3))

    ax.text(0.5, 11.02, "真空夹层与多层绝热，同轴线逐层热锚", fontsize=7.2, color="#6b7785",
            ha="left")
    ax.text(3.2, 1.45, "每根同轴线在每层冷板上用铜夹与铟箔热锚", fontsize=7.0,
            color="#6b7785", ha="center")

    # 右：冷量阶梯
    ax = fig.add_subplot(gs[0, 1])
    T = np.array([0.01, 0.1, 1.0, 4.0, 50.0])
    Q = np.array([4e-6, 4e-4, 2e-2, 1.5, 40.0])
    ax.loglog(T, Q, color=bs.BLUE, lw=1.3, marker="o", ms=4.2, mfc="white", mew=1.1)

    labels = ["10 mK　4 µW", "100 mK　400 µW", "1 K　20 mW", "4 K　1.5 W", "50 K　40 W"]
    offs = [(9, -15), (7, -16), (8, -17), (9, -18), (-8, 9)]
    has = ["left", "left", "left", "left", "right"]
    for t, q, lab, off, ha in zip(T, Q, labels, offs, has):
        ax.annotate(lab, (t, q), textcoords="offset points", xytext=off,
                    fontsize=7.2, color="#33414f", ha=ha)

    Td = np.logspace(-2.1, np.log10(0.8), 200)
    ax.plot(Td, 4e-4 * (Td / 0.1) ** 2, color=bs.RED, lw=1.0, ls=(0, (4, 3)))

    ax.set_xlim(4e-3, 6e2)
    ax.set_ylim(5e-7, 3e2)
    ax.set_xlabel("温度（K）")
    ax.set_ylabel("可用冷量（W）")
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig01")


def fig_budget():
    cats = ["线缆导热", "辐射与支撑", "衰减器与放大器", "其他"]
    stages = ["4 K 级", "0.8 K 级", "100 mK 级", "10 mK 级"]
    cap = np.array([1.5, 2e-2, 4e-4, 4e-6])
    load = np.array([
        [100e-3, 150e-3, 32e-3, 20e-3],
        [3e-3, 2e-3, 0.2e-3, 0.3e-3],
        [100e-6, 45e-6, 5e-6, 10e-6],
        [1.4e-6, 0.6e-6, 0.3e-6, 0.3e-6],
    ])
    colors = [bs.BLUE, bs.ORANGE, bs.GREEN, bs.GRAY]

    fig = plt.figure(figsize=(7.2, 3.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.65, 1.0], wspace=0.30)

    ax = fig.add_subplot(gs[0, 0])
    x = np.arange(len(cats))
    w = 0.19
    for j, name in enumerate(stages):
        y = load[j]
        ax.bar(x + (j - 1.5) * w, y, w * 0.92, color=colors[j], label=name,
               edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=7.8)
    ax.set_ylim(2e-7, 3.0)
    ax.set_ylabel("热负载（W）")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.16), fontsize=7.4,
              handlelength=1.1, columnspacing=1.2, handletextpad=0.5)
    bs.clean(ax, grid_axis="y")

    ax = fig.add_subplot(gs[0, 1])
    frac = load.sum(axis=1) / cap * 100
    ypos = np.arange(len(stages))[::-1]
    ax.barh(ypos, frac, height=0.52, color=[colors[i] for i in range(4)],
            edgecolor="white", linewidth=0.5, zorder=3)
    ax.axvline(100, color=bs.RED, lw=1.0, ls=(0, (4, 3)), zorder=4)
    ax.text(92, 1.5, "冷量上限", fontsize=7.2, color=bs.RED, ha="center", va="center",
            rotation=90)
    for yy, f in zip(ypos, frac):
        ax.text(f + 3, yy, f"{f:.0f}%", fontsize=7.6, color="#33414f", va="center")
    ax.set_yticks(ypos)
    ax.set_yticklabels(stages, fontsize=7.8)
    ax.set_xlim(0, 128)
    ax.set_xlabel("已占冷量（%）")
    bs.clean(ax, grid_axis="x")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_ladder()
    fig_budget()
