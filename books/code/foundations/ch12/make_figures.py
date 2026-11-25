"""第十二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("foundations")

CH = "12"


def fig_statistics():
    x = np.linspace(-4, 6, 800)
    fig, ax = plt.subplots(figsize=(6.0, 2.95))

    ax.plot(x, 1 / (np.exp(x) + 1), color=bs.BLUE, lw=1.5, label="费米-狄拉克")
    ax.plot(x, np.exp(-x), color=bs.GRAY, lw=1.1, ls=(0, (4, 2.5)), label="麦克斯韦-玻尔兹曼")
    xb = np.linspace(0.55, 6, 500)
    ax.plot(xb, 1 / (np.exp(xb) - 1), color=bs.RED, lw=1.5, label="玻色-爱因斯坦")

    ax.axvline(0, color="#c2ccd8", lw=0.8, ls=(0, (3, 3)))
    ax.axhline(0.5, color="#e0e6ee", lw=0.6)
    ax.set_xlim(-4, 6)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel(r"$(E-\mu)/kT$")
    ax.set_ylabel("平均占据数")
    ax.set_yticks([0, 0.5, 1.0])
    ax.legend(loc="upper right")
    bs.clean(ax)

    ax.text(0.12, 0.60, "费米能", fontsize=7.8, color="#4a5563", ha="left", va="bottom")

    bs.save(fig, CH, "fig01")


def fig_shells():
    levels = [
        ("1s", 2, 0.0, bs.BLUE),
        ("2s", 2, 1.05, bs.BLUE),
        ("2p", 6, 1.55, bs.GREEN),
        ("3s", 2, 2.55, bs.BLUE),
        ("3p", 6, 3.05, bs.GREEN),
        ("4s", 2, 3.95, bs.BLUE),
        ("3d", 10, 4.45, bs.ORANGE),
        ("4p", 6, 4.95, bs.GREEN),
    ]

    fig, ax = plt.subplots(figsize=(5.8, 3.1))
    for name, cap, y, color in levels:
        ax.barh(y, 0.26 * cap, height=0.34, color=color, alpha=0.28,
                edgecolor=color, lw=1.0, left=1.05)
        ax.text(0.95, y, name, fontsize=8.4, ha="right", va="center", color="#33414f")
        ax.text(1.12 + 0.26 * cap, y, str(cap), fontsize=8.0, ha="left", va="center",
                color=color)

    ax.set_ylim(-0.55, 5.55)
    ax.set_yticks([])
    ax.set_xticks([0, 2, 4])
    ax.set_xlim(0, 6.3)
    ax.set_xlabel("一个亚层的容量")
    bs.clean(ax)

    groups = [(2.95, 3.85, "第 1 周期", "2 种"), (2.30, 2.95, "第 2 周期", "8 种"),
              (3.50, 3.85, "第 3 周期", "8 种"), (4.95, 5.55, "第 4 周期", "18 种")]
    seps = [0.52, 1.80, 3.30]
    for ys in seps:
        ax.plot([4.05, 6.05], [ys, ys], color="#c9d2dc", lw=0.7, ls=(0, (3, 3)))

    labels = [("第 1 周期  2 种", 0.00), ("第 2 周期  8 种", 1.30),
              ("第 3 周期  8 种", 2.80), ("第 4 周期  18 种", 4.45)]
    for text, yv in labels:
        ax.text(4.10, yv, text, fontsize=7.8, ha="left", va="center", color="#4a5563")

    ax.text(0.30, 5.36, "填充顺序自下而上", fontsize=7.6, ha="left", va="center",
            color="#6b7785")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_statistics()
    fig_shells()
