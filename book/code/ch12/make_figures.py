"""第十二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "12"


def fig_rabi():
    t = np.linspace(0, 4 * np.pi, 1200)
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    cases = [(1.0, 0.0, bs.BLUE, r"共振 $\Delta = 0$"),
             (1.0, 1.0, bs.RED, r"失谐 $\Delta = \Omega$")]
    for Om, delta, color, label in cases:
        OmR = np.sqrt(Om ** 2 + delta ** 2)
        p1 = (Om / OmR) ** 2 * np.sin(OmR * t / 2) ** 2
        ax.plot(t / np.pi, p1, color=color, lw=1.4, label=label)
    ax.set_xlabel(r"时间（单位 $\pi/\Omega$）")
    ax.set_ylabel("激发态概率")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.06)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.legend(loc="upper right", handlelength=1.6)
    ax.annotate(r"$\pi$ 脉冲", xy=(1.0, 1.0), xytext=(1.25, 0.72), fontsize=8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_trajectory():
    t = np.linspace(0, 2 * np.pi, 800)
    y = -np.sin(t)
    z = np.cos(t)
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, color="#c9d6e4", lw=1.0))
    ax.plot(y, z, color=bs.RED, lw=1.8)
    ax.plot([0], [1], "o", ms=5, color=bs.BLUE)
    ax.plot([0], [-1], "o", ms=5, color=bs.BLUE, alpha=0.4)
    ax.annotate("起点 $|0\\rangle$", xy=(0, 1), xytext=(0.28, 1.06), fontsize=8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.6))
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.25)
    ax.set_aspect("equal")
    ax.axhline(0, color="#e3e9f0", lw=0.8)
    ax.axvline(0, color="#e3e9f0", lw=0.8)
    ax.set_xlabel(r"布洛赫矢量 $y$ 分量")
    ax.set_ylabel(r"布洛赫矢量 $z$ 分量")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    bs.clean(ax)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_rabi()
    fig_trajectory()
