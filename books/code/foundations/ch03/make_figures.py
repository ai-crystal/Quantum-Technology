"""第三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

import bookstyle as bs

bs.use("foundations")

CH = "03"
h = 6.62607015e-34
e = 1.602176634e-19
c = 2.99792458e8
me = 9.1093837015e-31


def fig_phototube():
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    tube = FancyBboxPatch((2.2, 2.0), 5.8, 2.4, boxstyle="round,pad=0.02,rounding_size=0.35",
                          linewidth=1.0, edgecolor="#5c6b7a", facecolor="#f5f8fc")
    ax.add_patch(tube)
    ax.text(5.1, 4.62, "真空管", fontsize=8.4, color="#5c6b7a", ha="center")

    ax.plot([3.35, 3.35], [2.45, 3.95], color="#3a4a5c", lw=4.0, solid_capstyle="butt")
    ax.text(3.35, 2.28, "阴极 K", fontsize=8.4, color="#3a4a5c", ha="center", va="top")
    ax.plot([6.85, 6.85], [2.45, 3.95], color="#3a4a5c", lw=2.2, solid_capstyle="butt")
    ax.text(6.85, 2.28, "阳极 A", fontsize=8.4, color="#3a4a5c", ha="center", va="top")

    ax.annotate("", xy=(3.15, 3.55), xytext=(0.55, 3.55),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.5, shrinkA=0, shrinkB=0))
    ax.text(0.55, 3.75, "入射光", fontsize=8.4, color=bs.ORANGE, ha="left", va="bottom")
    ax.text(0.55, 3.30, r"频率 $\nu$", fontsize=8.0, color=bs.ORANGE, ha="left", va="top")

    for yy in [3.15, 3.55]:
        ax.annotate("", xy=(4.55, yy), xytext=(3.55, yy),
                    arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(4.05, 3.36, "光电子", fontsize=7.8, color=bs.BLUE, ha="center", va="bottom")

    ax.plot([3.35, 3.35], [2.45, 1.25], color="#3a4a5c", lw=1.0)
    ax.plot([3.35, 4.35], [1.25, 1.25], color="#3a4a5c", lw=1.0)
    ax.plot([6.85, 6.85], [2.45, 1.25], color="#3a4a5c", lw=1.0)
    ax.plot([5.65, 6.85], [1.25, 1.25], color="#3a4a5c", lw=1.0)

    ax.plot([4.35, 4.35], [1.10, 1.40], color="#3a4a5c", lw=2.4)
    ax.plot([4.72, 4.72], [1.10, 1.40], color="#3a4a5c", lw=2.4)
    ax.plot([4.35, 4.72], [1.25, 1.25], color="#3a4a5c", lw=0.8, ls=(0, (1, 1)))
    ax.text(4.53, 0.92, "可调电压", fontsize=8.0, color="#3a4a5c", ha="center", va="top")
    ax.text(4.10, 1.40, "$-$", fontsize=9, color="#3a4a5c", ha="right", va="bottom")
    ax.text(4.98, 1.40, "$+$", fontsize=9, color="#3a4a5c", ha="left", va="bottom")

    ax.add_patch(Circle((5.65, 1.25), 0.20, facecolor="white", edgecolor="#3a4a5c", lw=1.0))
    ax.text(5.65, 1.25, "A", fontsize=7.5, color="#3a4a5c", ha="center", va="center")
    ax.text(5.65, 1.60, "电流表", fontsize=8.0, color="#3a4a5c", ha="center", va="bottom")
    bs.save(fig, CH, "fig01")


def fig_stopping():
    nu = np.linspace(3.0e14, 15.0e14, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    metals = [("钠  $W = 2.28$ eV", 2.28, bs.BLUE), ("锌  $W = 4.30$ eV", 4.30, bs.RED)]
    for label, W, color in metals:
        V = (h * nu / e) - W
        ax.plot(nu / 1e14, V, color=color, lw=1.5, label=label)
        nu0 = W * e / h
        ax.plot([nu0 / 1e14], [0], "o", ms=3.6, color=color, zorder=5)
    ax.axhline(0, color="#b9c3cf", lw=0.8)
    ax.set_xlim(3, 15)
    ax.set_ylim(-2.0, 3.6)
    ax.set_xlabel(r"入射光频率 $\nu$ ($10^{14}$ Hz)")
    ax.set_ylabel(r"遏止电压 $V_0$ (V)")
    ax.legend(loc="upper left", handlelength=1.6)
    ax.annotate("红限频率", xy=(5.51, 0), xytext=(6.6, -1.35), fontsize=8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, connectionstyle="arc3,rad=-0.25"))
    ax.annotate("斜率 $h/e$", xy=(10.6, 2.10), xytext=(11.9, 2.75), fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-|>", color="#8a95a3", lw=0.7))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


def fig_compton():
    theta = np.linspace(0, np.pi, 400)
    lam_c = h / (me * c)
    dla = lam_c * (1 - np.cos(theta)) * 1e12
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.plot(theta * 180 / np.pi, dla, color=bs.BLUE, lw=1.5)
    ax.plot([180], [2 * lam_c * 1e12], "o", ms=3.6, color=bs.BLUE, zorder=5)
    ax.text(178, 2 * lam_c * 1e12 + 0.10, r"$2\lambda_C = 4.85$ pm", fontsize=8,
            color=bs.BLUE, ha="right", va="bottom")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 6.0)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"散射角 $\theta$ (度)")
    ax.set_ylabel(r"波长偏移 $\Delta\lambda$ (pm)")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_phototube()
    fig_stopping()
    fig_compton()
