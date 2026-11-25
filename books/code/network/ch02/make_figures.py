"""第 2 章插图：BB84 的四种偏振态、截获比例与误码率。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "02"


def fig_states():
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.0))
    th = np.linspace(0, 2 * np.pi, 400)

    panels = [
        (0, "Z 基", [(90, r"$|1\rangle$"), (0, r"$|0\rangle$")], bs.BLUE),
        (45, "X 基", [(135, r"$|-\rangle$"), (45, r"$|+\rangle$")], bs.RED),
    ]
    for ax, (base, name, states, color) in zip(axes, panels):
        ax.plot(np.cos(th), np.sin(th), color="#d5dce5", lw=0.9)
        ax.axhline(0, color="#e3e9f0", lw=0.8, zorder=0)
        ax.axvline(0, color="#e3e9f0", lw=0.8, zorder=0)
        for deg, label in states:
            a = np.deg2rad(deg)
            ax.annotate("", xy=(0.94 * np.cos(a), 0.94 * np.sin(a)), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7,
                                        shrinkA=0, shrinkB=0, mutation_scale=13))
            ax.text(1.10 * np.cos(a), 1.10 * np.sin(a), label, fontsize=10,
                    color=color, ha="center", va="center")
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.30)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(0.0, -1.28, name, fontsize=9.5, color="#33414f", ha="center")

    axes[0].text(1.28, 1.15, "猜错基时，结果随机", fontsize=8, color="#6b7785",
                 ha="right")
    fig.subplots_adjust(wspace=0.05)
    bs.save(fig, CH, "fig01")


def fig_qber():
    f = np.linspace(0, 1, 300)
    qber = f / 4.0

    fig, ax = plt.subplots(figsize=(5.8, 3.1))
    ax.plot(f, qber * 100, color=bs.BLUE, lw=1.6, label="截获重发攻击下的误码率")
    ax.axhline(11, color=bs.RED, lw=1.1, ls=(0, (5, 3)))
    ax.text(0.02, 12.6, "安全阈值 11%", fontsize=8.5, color=bs.RED)

    ax.plot([0.44], [11], "o", ms=5, color=bs.RED, zorder=5)
    ax.annotate("截获 44% 的脉冲\n误码率已达阈值", xy=(0.44, 11), xytext=(0.52, 5.0),
                fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))

    ax.plot([1.0], [25], "o", ms=4.5, color=bs.BLUE)
    ax.annotate("全部截获\n误码率 25%", xy=(1.0, 25), xytext=(0.58, 27.0),
                fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))

    ax.set_xlim(0, 1.04)
    ax.set_ylim(0, 30)
    ax.set_xlabel("Eve 截获并重发的脉冲比例")
    ax.set_ylabel("量子误码率 QBER（%）")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_states()
    fig_qber()
