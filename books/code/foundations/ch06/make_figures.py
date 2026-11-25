"""第六章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("foundations")

CH = "06"


def fig_whichpath():
    phi = np.linspace(-3 * np.pi, 3 * np.pi, 1200)
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    for D, color, label in [(0.0, bs.BLUE, "没有路径信息"), (0.5, bs.ORANGE, "部分路径信息"), (1.0, bs.RED, "完全知道走哪条缝")]:
        y = 1 + (1 - D) * np.cos(phi)
        ax.plot(phi / np.pi, y, color=color, lw=1.3, label=label)
    ax.set_xlabel(r"相位差 $\varphi/\pi$")
    ax.set_ylabel("相对强度")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.05, 2.25)
    ax.legend(loc="upper center", ncol=3, handlelength=1.4, columnspacing=1.2, fontsize=7.8)
    ax.axhline(1.0, color="#d5dce5", lw=0.6, ls=(0, (3, 3)))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_visibility():
    t = np.linspace(0, 5, 800)
    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    ax.plot(t, np.exp(-t), color=bs.BLUE, lw=1.5, label=r"$e^{-t/T_2}$（纯退相位）")
    ax.plot(t, np.exp(-(t ** 2) / 2), color=bs.RED, lw=1.5, ls=(0, (4, 3)), label=r"$e^{-t^2/2T_2^2}$（高斯型噪声）")
    ax.axvline(1.0, color=bs.GRAY, lw=0.8, ls=(0, (2, 2)))
    ax.text(1.06, 0.18, r"$t=T_2$", fontsize=8.4, color=bs.GRAY)
    ax.set_xlabel(r"演化时间 $t/T_2$")
    ax.set_ylabel("干涉条纹可见度")
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.03, 1.05)
    ax.legend(loc="upper right", handlelength=2.0)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_whichpath()
    fig_visibility()
