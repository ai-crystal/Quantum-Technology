"""第十三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")

CH = "04"


def fig_chsh():
    bp = np.linspace(-np.pi, np.pi, 1600)
    E = lambda x, y: -np.cos(x - y)
    a1, a2 = 0.0, np.pi / 2
    b1 = np.pi / 4
    S = np.abs(E(a1, b1) - E(a1, bp) + E(a2, b1) + E(a2, bp))
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.plot(bp * 180 / np.pi, S, color=bs.BLUE, lw=1.5)
    ax.axhline(2.0, color=bs.RED, lw=1.0, ls=(0, (4, 3)))
    ax.axhline(2 * np.sqrt(2), color=bs.GREEN, lw=0.9, ls=(0, (2, 2)))
    ax.text(-176, 2 * np.sqrt(2) + 0.06, r"$2\sqrt{2}\approx 2.83$", fontsize=7.8, color=bs.GREEN)
    ax.text(-176, 2.06, "经典上限 2", fontsize=7.8, color=bs.RED)
    ax.text(-176, 2.72, r"量子预言 $|S(b')|$", fontsize=7.8, color=bs.BLUE)
    ax.plot([-45], [2 * np.sqrt(2)], "o", ms=4.0, color=bs.BLUE)
    ax.annotate(r"$b' = -45^\circ$", xy=(-45, 2 * np.sqrt(2)), xytext=(-16, 2.42), fontsize=7.8,
                color=bs.BLUE, arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7))
    ax.set_xlabel(r"$b'$ 的测量角度（度）")
    ax.set_ylabel(r"$|S|$")
    ax.set_xlim(-180, 180)
    ax.set_ylim(0, 3.2)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_correlation():
    th = np.linspace(0, np.pi, 900)
    q = np.abs(np.cos(th))
    c = np.abs(1 - 2 * th / np.pi)
    x = th * 180 / np.pi
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    ax.plot(x, q, color=bs.BLUE, lw=1.5, label="纠缠态的量子关联")
    ax.plot(x, c, color=bs.RED, lw=1.2, ls=(0, (4, 3)), label="局域隐变量模型可达的上界")
    ax.fill_between(x, c, q, where=(q > c), color=bs.BLUE, alpha=0.10)
    ax.set_xlabel(r"两个测量方向的夹角 $\theta$ (度)")
    ax.set_ylabel(r"关联强度 $|E(\theta)|$")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1.08)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.legend(loc="upper right", handlelength=1.8)
    ax.text(52, 0.80, "量子关联超出经典上界", fontsize=7.8, color=bs.BLUE)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_chsh()
    fig_correlation()
