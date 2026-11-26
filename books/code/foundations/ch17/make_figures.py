"""第十七章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("foundations")

CH = "17"

GAMMA = 6.07     # 自然线宽，MHz
DOPPLER = 570.0  # 多普勒宽度，MHz


def lorentz(x, w):
    return 1.0 / (1.0 + (2 * x / w) ** 2)


def gauss(x, w):
    return np.exp(-4 * np.log(2) * (x / w) ** 2)


def fig_lines():
    fig = plt.figure(figsize=(7.0, 2.75))
    gs = GridSpec(1, 2, width_ratios=[1.0, 1.15], wspace=0.30, figure=fig)

    # 左：近看自然线宽
    ax = fig.add_subplot(gs[0])
    x = np.linspace(-22, 22, 800)
    ax.plot(x, lorentz(x, GAMMA), color=bs.BLUE, lw=1.4)
    ax.annotate("", xy=(GAMMA / 2, 0.5), xytext=(-GAMMA / 2, 0.5),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, mutation_scale=7))
    ax.plot([-GAMMA / 2, GAMMA / 2], [0.5, 0.5], "o", ms=2.6, color=bs.RED)
    ax.text(-21, 0.60, "6.07 MHz", fontsize=8, color=bs.RED, ha="left")
    ax.axhline(0.5, color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax.set_xlim(-22, 22)
    ax.set_ylim(0, 1.06)
    ax.set_xlabel("相对中心频率（兆赫兹）")
    ax.set_ylabel("吸收截面（归一化）")
    ax.set_xticks([-20, -10, 0, 10, 20])
    bs.clean(ax, grid_axis="y")

    # 右：多普勒展宽下的全貌
    ax2 = fig.add_subplot(gs[1])
    x2 = np.linspace(-1500, 1500, 3000)
    ax2.plot(x2, gauss(x2, DOPPLER), color=bs.GREEN, lw=1.4, label="多普勒展宽（高斯）")
    ax2.plot(x2, lorentz(x2, GAMMA), color=bs.BLUE, lw=1.2, label="自然线宽（洛伦兹）")
    ax2.annotate("", xy=(DOPPLER / 2, 0.5), xytext=(-DOPPLER / 2, 0.5),
                 arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, mutation_scale=7))
    ax2.annotate("570 MHz", xy=(288, 0.51), xytext=(340, 0.40), fontsize=8, color=bs.RED,
                 arrowprops=dict(arrowstyle="-", color=bs.RED, lw=0.7))
    ax2.axhline(0.5, color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax2.annotate("自然线宽在这里", xy=(30, 0.06), xytext=(210, 0.30), fontsize=7.4,
                 color=bs.BLUE,
                 arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, mutation_scale=7))
    ax2.set_xlim(-1500, 1500)
    ax2.set_ylim(0, 1.06)
    ax2.set_xlabel("相对中心频率（兆赫兹）")
    ax2.set_yticks([])
    ax2.legend(loc="upper right", handlelength=1.4)
    bs.clean(ax2, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_saturation():
    s = np.logspace(-2, 3, 500)

    fig = plt.figure(figsize=(7.0, 2.65))
    gs = GridSpec(1, 2, wspace=0.30, figure=fig)

    ax = fig.add_subplot(gs[0])
    rho = s / (2 * (1 + s))
    ax.plot(s, rho, color=bs.BLUE, lw=1.5)
    ax.axhline(0.5, color="#c9d2dc", lw=0.8, ls=(0, (4, 3)))
    ax.text(0.03, 0.53, "上限 0.5", fontsize=7.6, color="#4a5563")
    ax.plot(s, s / 2, color=bs.GRAY, lw=0.8, ls=(0, (3, 3)))
    ax.text(0.30, 0.025, "虚线是弱光近似 $s/2$", fontsize=7.2, color=bs.GRAY)
    ax.axvline(1.0, color="#c9d2dc", lw=0.8)
    ax.text(1.2, 0.06, "$s=1$", fontsize=7.6, color="#4a5563")
    ax.set_xscale("log")
    ax.set_xlim(1e-2, 1e3)
    ax.set_ylim(0, 0.58)
    ax.set_xlabel("饱和参数 $s=I/I_{\\mathrm{sat}}$")
    ax.set_ylabel("激发态布居 $\\rho_{22}$")
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[1])
    ax2.plot(s, np.sqrt(1 + s), color=bs.ORANGE, lw=1.5)
    ax2.axhline(1.0, color="#c9d2dc", lw=0.8, ls=(0, (4, 3)))
    ax2.axvline(1.0, color="#c9d2dc", lw=0.8)
    for sv, txt in [(1.0, "1.41$\\Gamma$"), (100.0, "10$\\Gamma$")]:
        ax2.plot([sv], [np.sqrt(1 + sv)], "o", ms=3.4, color=bs.ORANGE, zorder=5)
        ax2.annotate(txt, xy=(sv, np.sqrt(1 + sv)), xytext=(sv * 1.5, np.sqrt(1 + sv) + 1.6),
                     fontsize=7.4, color=bs.ORANGE,
                     arrowprops=dict(arrowstyle="-", color="#c99a5f", lw=0.7))
    ax2.set_xscale("log")
    ax2.set_xlim(1e-2, 1e3)
    ax2.set_ylim(0.9, 26)
    ax2.set_yscale("log")
    ax2.set_yticks([1, 2, 5, 10, 20])
    ax2.set_yticklabels(["1", "2", "5", "10", "20"])
    ax2.set_xlabel("饱和参数 $s=I/I_{\\mathrm{sat}}$")
    ax2.set_ylabel("线宽 $\\Gamma'/\\Gamma$")
    bs.clean(ax2, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_lines()
    fig_saturation()
