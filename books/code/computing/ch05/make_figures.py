"""第十四章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")

CH = "05"


def fig_bloch_shrink():
    t = np.linspace(0, 3, 600)
    fig, ax = plt.subplots(figsize=(5.8, 2.8))
    ax.plot(t, np.exp(-t / 2.0), color=bs.BLUE, lw=1.5, label=r"$z$ 分量（$T_1$ 弛豫，$T_1=2T_2$）")
    ax.plot(t, np.exp(-t), color=bs.RED, lw=1.5, ls=(0, (4, 3)), label=r"横向分量（$T_2$ 退相位）")
    ax.set_xlabel(r"时间（单位 $T_2$）")
    ax.set_ylabel("归一化幅值")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", handlelength=2.0, fontsize=7.6)
    ax.axvline(1.0, color="#c9d2dc", lw=0.8, ls=(0, (2, 2)))
    ax.text(1.04, 0.06, r"$t=T_2$", fontsize=8, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_ramsey():
    t = np.linspace(0, 6, 1600)
    delta = 2 * np.pi * 1.6
    env = np.exp(-(t / 3.0) ** 2)
    p = 0.5 * (1 + env * np.cos(delta * t))
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    ax.plot(t, p, color=bs.BLUE, lw=1.2)
    ax.plot(t, 0.5 * (1 + env), color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.plot(t, 0.5 * (1 - env), color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.set_xlabel(r"自由演化时间 $\tau$（任意单位）")
    ax.set_ylabel("激发态概率")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1.05)
    ax.annotate("包络由退相位决定", xy=(3.9, 0.88), xytext=(4.1, 0.55), fontsize=8, color=bs.RED,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7, connectionstyle="arc3,rad=-0.2"))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bloch_shrink()
    fig_ramsey()
