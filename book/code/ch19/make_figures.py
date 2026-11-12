"""第十九章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import bookstyle as bs

CH = "19"


def fig_system_bath():
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    ax.add_patch(FancyBboxPatch((0.6, 1.3), 2.6, 2.0, boxstyle="round,pad=0.05,rounding_size=0.2",
                                facecolor="#eaf1f9", edgecolor="#4a6f9c", lw=1.2))
    ax.text(1.9, 2.3, "量子系统", fontsize=8.8, color="#1f2a37", ha="center", va="center")
    ax.text(1.9, 1.85, "$H_S$", fontsize=8.4, color="#4a6f9c", ha="center", va="center")

    ax.add_patch(Rectangle((5.4, 0.7), 4.2, 3.2, facecolor="#f4f6f4", edgecolor="#7d8f7d", lw=1.0))
    ax.text(7.5, 3.62, "环境（热库）", fontsize=8.6, color="#3f5240", ha="center", va="center")
    rng = np.random.default_rng(3)
    for i in range(14):
        x = 5.7 + rng.random() * 3.6
        y = 0.95 + rng.random() * 2.2
        ax.add_patch(plt.Circle((x, y), 0.09, facecolor="#a9bfa9", edgecolor="none", alpha=0.9))
    ax.text(7.5, 0.42, "$H_E$，自由度极多", fontsize=8.2, color="#5a6b5a", ha="center", va="center")

    for y in [1.9, 2.7]:
        ax.annotate("", xy=(5.35, y), xytext=(3.3, y),
                    arrowprops=dict(arrowstyle="<|-|>", color=bs.ORANGE, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(4.3, 2.95, "耦合", fontsize=8.2, color=bs.ORANGE, ha="center")
    ax.text(4.3, 1.62, "$H_{SE}$", fontsize=8.2, color=bs.ORANGE, ha="center")
    bs.save(fig, CH, "fig01")


def fig_noise():
    f = np.logspace(-2, 7, 900)
    pink = 1e-3 / f
    white = np.full_like(f, 2e-6)
    total = pink + white
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.loglog(f, total, color=bs.BLUE, lw=1.5, label="总噪声谱")
    ax.loglog(f, pink, color=bs.RED, lw=0.9, ls=(0, (4, 3)), label=r"$1/f$ 分量")
    ax.loglog(f, white, color=bs.GRAY, lw=0.9, ls=(0, (1, 2)), label="白噪声本底")
    ax.set_xlabel("频率 (Hz)")
    ax.set_ylabel(r"噪声谱密度 $S(\omega)$（任意单位）")
    ax.set_xlim(1e-2, 1e7)
    ax.set_ylim(1e-7, 1e0)
    ax.legend(loc="lower left", handlelength=2.0, fontsize=7.6)
    ax.axvspan(1e-2, 1e0, color="#f2e6d8", alpha=0.45)
    ax.text(0.014, 2.2e-1, "低频漂移区", fontsize=7.8, color="#8a6a3a")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_system_bath()
    fig_noise()
