"""第八章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("foundations")

CH = "08"
c = 2.99792458e8


def draw_levels(ax, energies, labels, pump_from, pump_to, decay_to, emit_from, emit_to):
    ax.set_xlim(0, 5.4)
    ax.set_ylim(-0.6, 4.9)
    ax.axis("off")
    for E, lab in zip(energies, labels):
        ax.plot([0.9, 4.16], [E, E], color=bs.BLUE, lw=1.6, solid_capstyle="butt")
        ax.text(0.82, E, lab, ha="right", va="center", fontsize=8.4)

    ax.annotate("", xy=(1.6, pump_to - 0.08), xytext=(1.6, pump_from + 0.08),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.5, shrinkA=0, shrinkB=0))
    ax.text(1.6, 4.32, "抽运", fontsize=8.2, color=bs.ORANGE, ha="center", va="bottom")

    ax.annotate("", xy=(2.95, decay_to + 0.06), xytext=(2.95, pump_to - 0.06),
                arrowprops=dict(arrowstyle="-|>", color=bs.GRAY, lw=1.0, ls=(0, (3, 2)), shrinkA=0, shrinkB=0))
    ax.text(3.08, (decay_to + pump_to) / 2, "快速无辐射", fontsize=7.6, color="#5a6674",
            va="center", ha="left")

    ax.annotate("", xy=(4.05, emit_to + 0.08), xytext=(4.05, emit_from - 0.08),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.5, shrinkA=0, shrinkB=0))
    ax.text(4.18, (emit_from + emit_to) / 2, "受激辐射", fontsize=7.6, color=bs.RED,
            va="center", ha="left")


def fig_levels():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax = axes[0]
    draw_levels(ax, [0.2, 2.2, 3.9], ["$E_1$", "$E_2$", "$E_3$"], 0.2, 3.9, 2.2, 2.2, 0.2)
    ax.text(2.6, -0.45, "三能级", fontsize=8.6, color="#33414f", ha="center", va="top")

    ax = axes[1]
    draw_levels(ax, [0.2, 1.3, 2.5, 4.0], ["$E_0$", "$E_1$", "$E_2$", "$E_3$"], 0.2, 4.0, 2.5, 2.5, 1.3)
    ax.text(2.6, -0.45, "四能级", fontsize=8.6, color="#33414f", ha="center", va="top")
    fig.subplots_adjust(wspace=0.24, bottom=0.14)
    bs.save(fig, CH, "fig01")


def fig_cavity():
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.8)
    ax.axis("off")

    ax.add_patch(Rectangle((3.0, 1.2), 4.0, 1.5, facecolor="#e8f0f8", edgecolor="#7d93aa", lw=1.0))
    ax.text(5.0, 1.95, "增益介质", fontsize=8.6, color="#33414f", ha="center", va="center")

    for x, label in [(2.85, "全反射镜"), (7.15, "部分反射镜")]:
        ax.plot([x, x], [1.0, 2.9], color="#33414f", lw=3.0)
        ax.text(x, 0.82, label, fontsize=7.8, color="#33414f", ha="center", va="top")

    ax.annotate("", xy=(8.95, 1.95), xytext=(7.3, 1.95),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=2.2, shrinkA=0, shrinkB=0))
    ax.text(8.1, 2.12, "激光输出", fontsize=8.2, color=bs.RED, ha="center", va="bottom")

    ax.annotate("", xy=(5.0, 1.15), xytext=(5.0, 0.30),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.5, shrinkA=0, shrinkB=0))
    ax.text(5.15, 0.55, "泵浦能量", fontsize=8.0, color=bs.ORANGE, ha="left", va="center")

    ax.plot([3.3, 6.4], [2.45, 2.45], color=bs.BLUE, lw=0.9, ls=(0, (4, 3)))
    ax.plot([3.6, 6.7], [1.42, 1.42], color=bs.BLUE, lw=0.9, ls=(0, (4, 3)))
    ax.annotate("", xy=(6.35, 2.45), xytext=(5.6, 2.45),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.9, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(3.65, 1.42), xytext=(4.4, 1.42),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.9, shrinkA=0, shrinkB=0))
    bs.save(fig, CH, "fig02")


def fig_coherence():
    dnu = np.logspace(2, 14, 600)
    L = c / (np.pi * dnu)
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.loglog(dnu, L, color=bs.BLUE, lw=1.5)
    for nu, lab in [(1e3, "1 kHz"), (1e6, "1 MHz"), (1e9, "1 GHz"), (1e12, "1 THz")]:
        Lv = c / (np.pi * nu)
        ax.plot([nu], [Lv], "o", ms=3.8, color=bs.RED, zorder=5)
        ax.annotate(lab, xy=(nu, Lv), xytext=(nu * 2.2, Lv * 0.22), fontsize=7.6, color="#4a5563",
                    ha="left",
                    arrowprops=dict(arrowstyle="-", color="#b9c3cf", lw=0.6))
    ax.set_xlabel(r"线宽 $\Delta\nu$ (Hz)")
    ax.set_ylabel(r"相干长度 $L_c$ (m)")
    ax.set_xlim(1e2, 1e14)
    ax.set_ylim(1e-7, 1e7)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_levels()
    fig_cavity()
    fig_coherence()
