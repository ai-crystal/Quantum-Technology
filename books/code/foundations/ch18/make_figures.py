"""第十八章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("foundations")

CH = "18"

C = 2.998e8


def fig_coherence():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = GridSpec(1, 2, width_ratios=[1.15, 1.0], wspace=0.30, figure=fig)

    # 左：条纹对比度随臂长差衰减
    ax = fig.add_subplot(gs[0])
    dL = np.logspace(-7, 10, 600)
    srcs = [
        (1.0, "稳频激光，1 Hz", bs.BLUE),
        (1e6, "单频氦氖，1 MHz", bs.GREEN),
        (1e7, "半导体激光，10 MHz", bs.ORANGE),
        (1.4e14, "白光，$10^{14}$ Hz", bs.RED),
    ]
    for dv, label, color in srcs:
        ax.plot(dL, np.exp(-dL / (C / dv)), color=color, lw=1.3, label=label)
    ax.set_xscale("log")
    ax.set_xlim(1e-7, 1e10)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("两臂长度差 $\\Delta L$（米）")
    ax.set_ylabel("条纹对比度")
    ax.legend(loc="lower left", fontsize=7.2, handlelength=1.5, borderaxespad=0.3)
    bs.clean(ax, grid_axis="y")

    # 右：相干长度与谱宽
    ax2 = fig.add_subplot(gs[1])
    dv = np.logspace(-1, 15, 500)
    ax2.plot(dv, C / dv, color=bs.BLUE, lw=1.4)
    marks = [
        (1.0, "1 Hz", 2.0, 2e9),
        (1e6, "1 MHz", 6e3, 8.0),
        (1e7, "10 MHz", 3e7, 800.0),
        (1.4e14, "白光", 1e11, 1.2e-6),
    ]
    for xv, txt, tx, ty in marks:
        ax2.plot([xv], [C / xv], "o", ms=3.4, color=bs.RED, zorder=5)
        ax2.annotate(txt, xy=(xv, C / xv), xytext=(tx, ty), fontsize=7.4, color=bs.RED,
                     ha="left", va="center",
                     arrowprops=dict(arrowstyle="-", color="#c99a8f", lw=0.7))
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(1e-1, 1e15)
    ax2.set_ylim(1e-6, 1e10)
    ax2.set_xlabel("谱宽 $\\Delta\\nu$（赫兹）")
    ax2.set_ylabel("相干长度 $L_c$（米）")
    bs.clean(ax2)

    bs.save(fig, CH, "fig01")


def airy(x_mhz, R, fsr=1500.0):
    F = 4 * R / (1 - R) ** 2
    return 1.0 / (1 + F * np.sin(np.pi * x_mhz / fsr) ** 2)


def fig_fabry():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = GridSpec(1, 2, width_ratios=[1.5, 1.0], wspace=0.28, figure=fig)

    ax = fig.add_subplot(gs[0])
    x = np.linspace(-2000, 2000, 4000)
    for R, color in [(0.5, "#9fb3c8"), (0.9, bs.GREEN), (0.99, bs.BLUE)]:
        ax.plot(x, airy(x, R), color=color, lw=1.2, label="$R=%.2f$" % R)
    ax.annotate("", xy=(1500, 1.17), xytext=(0, 1.17),
                arrowprops=dict(arrowstyle="<|-|>", color="#6b7785", lw=0.8, mutation_scale=7))
    ax.text(750, 1.04, "自由光谱范围 1.5 GHz", fontsize=7.6, color="#4a5563",
            ha="center", va="bottom")
    ax.set_xlim(-2000, 2000)
    ax.set_ylim(0, 1.35)
    ax.set_xlabel("相对谐振频率（兆赫兹）")
    ax.set_ylabel("透射率")
    ax.set_yticks([0, 0.5, 1.0])
    ax.legend(loc="upper left", bbox_to_anchor=(0.13, 0.99), fontsize=7.4,
              handlelength=1.4, borderaxespad=0.2)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[1])
    xi = np.linspace(-10, 10, 1500)
    ax2.plot(xi, airy(xi, 0.99), color=bs.BLUE, lw=1.3)
    ax2.axhline(0.5, color="#c9d2dc", lw=0.7, ls=(0, (2, 3)))
    ax2.annotate("", xy=(2.4, 0.5), xytext=(-2.4, 0.5),
                 arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, mutation_scale=7))
    ax2.plot([-2.4, 2.4], [0.5, 0.5], "o", ms=2.6, color=bs.RED)
    ax2.text(0, 1.08, "半高全宽 4.8 MHz", fontsize=7.8, color=bs.RED, ha="center")
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(0, 1.22)
    ax2.set_xticks([-10, -5, 0, 5, 10])
    ax2.set_yticks([0, 0.5, 1.0])
    ax2.set_xlabel("相对谐振频率（兆赫兹）")
    bs.clean(ax2, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_coherence()
    fig_fabry()
