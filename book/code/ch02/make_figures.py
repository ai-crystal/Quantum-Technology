"""第二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "02"

h = 6.62607015e-34
c = 2.99792458e8
k = 1.380649e-23
B_WIEN = 2.897771955e-3


def planck(lam, T):
    return 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1)


def fig_blackbody():
    lam = np.linspace(0.2e-6, 12e-6, 2000)
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    for T, color in [(3000, bs.RED), (4000, bs.ORANGE), (5000, bs.BLUE)]:
        y = planck(lam, T) * 1e-12
        ax.plot(lam * 1e6, y, color=color, lw=1.4, label=f"{T} K")
        lm = B_WIEN / T
        ax.plot([lm * 1e6], [planck(lm, T) * 1e-12], "o", ms=3.6, color=color, zorder=5)
        ax.annotate(f"{lm*1e6:.2f} μm", xy=(lm * 1e6, planck(lm, T) * 1e-12),
                    xytext=(lm * 1e6 + 1.6, planck(lm, T) * 1e-12 * 0.66),
                    fontsize=7.6, color=color,
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.6, shrinkA=0, shrinkB=2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.set_xlabel("波长 (μm)")
    ax.set_ylabel("单色辐出度 (10$^{12}$ W·m$^{-3}$)")
    ax.legend(loc="upper right", handlelength=1.6)
    ax.plot([B_WIEN / 3000 * 1e6, B_WIEN / 3000 * 1e6], [0, 0.9], color=bs.RED, lw=0.6, ls=(0, (2, 2)))
    ax.plot([B_WIEN / 4000 * 1e6, B_WIEN / 4000 * 1e6], [0, 4.1], color=bs.ORANGE, lw=0.6, ls=(0, (2, 2)))
    ax.plot([B_WIEN / 5000 * 1e6, B_WIEN / 5000 * 1e6], [0, 12.6], color=bs.BLUE, lw=0.6, ls=(0, (2, 2)))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01", kind="photo")


def fig_uv_catastrophe():
    lam = np.linspace(0.05e-6, 3e-6, 1600)
    T = 5000
    y_planck = planck(lam, T) * 1e-12
    y_rj = 2 * c * k * T / lam ** 4 * 1e-12
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.plot(lam * 1e6, y_planck, color=bs.BLUE, lw=1.5, label="普朗克公式")
    ax.plot(lam * 1e6, y_rj, color=bs.RED, lw=1.2, ls=(0, (4, 3)), label="瑞利-金斯公式")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 30)
    ax.set_xlabel("波长 (μm)")
    ax.set_ylabel("单色辐出度 (10$^{12}$ W·m$^{-3}$)")
    ax.legend(loc="upper right", handlelength=1.8)
    ax.annotate("短波方向急剧上翘，\n实验上并不存在", xy=(0.46, 21.0), xytext=(1.62, 22.2),
                fontsize=7.8, color=bs.RED,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7, connectionstyle="arc3,rad=-0.2"))
    ax.annotate("实测峰值", xy=(0.59, 12.6), xytext=(0.90, 16.2), fontsize=7.8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, connectionstyle="arc3,rad=0.25"))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


def fig_quantum_ladder():
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.7, 4.5)
    ax.axis("off")
    for n in range(5):
        y = n * 0.9
        ax.plot([1.05, 3.2], [y, y], color=bs.BLUE, lw=1.5)
        ax.text(1.0, y, f"$n={n}$", ha="right", va="center", fontsize=8.2, color="#3a4a5c")
    ax.annotate("", xy=(3.55, 0), xytext=(3.55, 0.9),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.ORANGE, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(3.66, 0.45, r"$\Delta E = h\nu$", fontsize=9, color=bs.ORANGE, va="center")
    ax.text(2.1, -0.5, "能量只能取分立值", fontsize=8.2, color=bs.BLUE, ha="center", va="top")

    ax.plot([6.4, 6.4], [-0.2, 3.6], color="#b9c3cf", lw=1.2)
    for yy, al in [(0.4, 0.45), (1.15, 0.55), (2.1, 0.35), (3.05, 0.5)]:
        ax.plot([6.4], [yy], "o", ms=4.6, color=bs.GREEN, alpha=al)
    ax.annotate("", xy=(7.7, 3.6), xytext=(7.7, -0.2),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GREEN, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(7.85, 1.7, "可以停在任何高度", fontsize=8.2, color=bs.GREEN, va="center")
    ax.text(6.4, -0.5, "经典振子", fontsize=8.2, color="#4a5563", ha="center", va="top")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_blackbody()
    fig_uv_catastrophe()
    fig_quantum_ladder()
