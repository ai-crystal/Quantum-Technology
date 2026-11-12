"""第七章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "07"
RY = 13.605693


def fig_levels():
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    for n in [1, 2, 3, 4]:
        E = -RY / n ** 2
        ax.plot([1.0, 3.0], [E, E], color=bs.BLUE, lw=1.5)
        ax.text(0.92, E, f"$n={n}$", ha="right", va="center", fontsize=8.2, color="#3a4a5c")
        ax.text(3.08, E, f"{E:.2f}", ha="left", va="center", fontsize=7.8, color="#6b7785")

    ax.add_patch(plt.Rectangle((1.0, 0), 2.0, 1.1, facecolor="#dfe8f2", edgecolor="none"))
    ax.plot([1.0, 3.0], [0, 0], color="#9aa6b4", lw=0.8, ls=(0, (3, 3)))
    ax.text(2.0, 0.32, "连续区", fontsize=8, color="#5a6674", ha="center")
    ax.text(3.08, 0.0, "0", ha="left", va="center", fontsize=7.8, color="#6b7785")


    trans = [(3.9, -RY / 3 ** 2, "Hα  656 nm"), (5.15, -RY / 4 ** 2, "Hβ  486 nm")]
    for xv, E1, label in trans:
        ax.annotate("", xy=(xv, -RY / 4), xytext=(xv, E1),
                    arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.2, shrinkA=0, shrinkB=0))
        ax.plot([xv, xv], [-RY / 4 - 0.1, -5.3], color=bs.RED, lw=0.6, ls=(0, (2, 2)))
        ax.text(xv, -5.6, label, fontsize=7.8, color=bs.RED, ha="center", va="top")

    ax.set_xlim(0.0, 6.6)
    ax.set_ylim(-15.2, 1.3)
    ax.set_ylabel("能量 (eV)")
    ax.set_xticks([])
    bs.clean(ax)
    ax.spines["bottom"].set_visible(False)
    bs.save(fig, CH, "fig01")


def fig_balmer():
    lines = [(3, "Hα", 656.3, 0.72), (4, "Hβ", 486.1, 0.72), (5, "Hγ", 434.0, 0.72), (6, "Hδ", 410.2, 0.94)]
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.set_xlim(380, 700)
    ax.set_ylim(0, 1.20)
    for w in np.arange(380, 700, 0.5):
        if w < 440:
            r, g, b = (440 - w) / 60.0, 0.0, 1.0
        elif w < 490:
            r, g, b = 0.0, (w - 440) / 50.0, 1.0
        elif w < 510:
            r, g, b = 0.0, 1.0, (510 - w) / 20.0
        elif w < 580:
            r, g, b = (w - 510) / 70.0, 1.0, 0.0
        elif w < 645:
            r, g, b = 1.0, (645 - w) / 55.0, 0.0
        else:
            r, g, b = 1.0, 0.0, 0.0
        rgb = tuple(min(1.0, max(0.0, v)) for v in (r, g, b))
        ax.add_patch(plt.Rectangle((w, 0.40), 0.5, 0.16, facecolor=rgb, edgecolor="none", alpha=0.55))
    for n, name, wl, yl in lines:
        ax.plot([wl, wl], [0.28, 0.66], color="#1f2a37", lw=2.0)
        ax.plot([wl, wl], [0.66, yl - 0.03], color="#8a95a3", lw=0.6)
        ax.text(wl, yl, f"{name}  {wl:.0f}", fontsize=7.6, color="#1f2a37", ha="center", va="bottom")
    ax.set_yticks([])
    ax.set_xlabel("波长 (nm)")
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    bs.save(fig, CH, "fig02")


def fig_radial():
    r = np.linspace(0, 20, 1600)  # 以 a0 为单位
    p1s = 4 * r ** 2 * np.exp(-2 * r)
    p2s = 4 * r ** 2 * (1 / 8) * (2 - r) ** 2 * np.exp(-r)
    p2p = 4 * r ** 2 * (1 / 24) * r ** 2 * np.exp(-r)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.plot(r, p1s, color=bs.BLUE, lw=1.5, label=r"$1s$")
    ax.plot(r, p2s, color=bs.RED, lw=1.4, label=r"$2s$")
    ax.plot(r, p2p, color=bs.GREEN, lw=1.4, label=r"$2p$")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 0.62)
    ax.set_xlabel(r"到核的距离 $r$（单位 $a_0 = 0.053$ nm）")
    ax.set_ylabel("径向概率密度")
    ax.legend(loc="upper right", handlelength=1.6)
    ax.annotate(r"$1s$ 最可能半径约 $a_0$", xy=(1.0, 4 * np.exp(-2)), xytext=(3.4, 0.50),
                fontsize=7.8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, connectionstyle="arc3,rad=0.2"))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_levels()
    fig_balmer()
    fig_radial()
