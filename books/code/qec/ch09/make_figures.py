"""第九章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "09"

P_TH = 0.006


def fig_threshold_cross():
    p = np.logspace(-4, np.log10(0.02), 400)
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    dists = [3, 5, 7, 9]
    cols = ["#9db4cc", "#7f9cbb", bs.BLUE, "#27496d"]
    anchors = [2e-4, 6e-5, 2e-5, 6e-6]
    for d, c, ya in zip(dists, cols, anchors):
        pl = 0.1 * (p / P_TH) ** ((d + 1) / 2.0)
        ax.loglog(p, pl, color=c, lw=1.4)
        x_lab = P_TH * (ya / 0.1) ** (2.0 / (d + 1))
        ax.text(x_lab * 0.74, ya * 0.42, f"$d={d}$", fontsize=7.8, color=c,
                ha="right", va="top")

    ax.axvline(P_TH, color=bs.RED, lw=1.0, ls=(0, (3, 2.5)))
    ax.text(P_TH * 1.05, 3e-8, "阈值", fontsize=8.0, color=bs.RED)
    ax.text(1.1e-4, 0.33, "所有码距在此相交", fontsize=7.8, color="#4a5563")

    ax.set_xlabel("物理错误率 $p$")
    ax.set_ylabel("每周期逻辑错误率 $p_L$")
    ax.set_xlim(1.0e-4, 0.02)
    ax.set_ylim(1e-8, 1.0)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_noise_models():
    fig, ax = plt.subplots(figsize=(5.9, 2.75))
    rows = [
        ("码容量噪声", 0.103, None, "#9db4cc"),
        ("现象学噪声", 0.029, None, "#7f9cbb"),
        ("电路级噪声", 0.006, 0.010, bs.BLUE),
    ]
    for k, (name, lo, hi, col) in enumerate(rows):
        y = len(rows) - 1 - k
        if hi is None:
            ax.plot([lo], [y], "o", ms=8, mfc=col, mec="white", mew=1.0, zorder=3)
            ax.text(lo * 1.14, y, f"{lo*100:.1f}%", fontsize=8.0, color="#33414f",
                    va="center")
        else:
            ax.plot([lo, hi], [y, y], color=col, lw=6.0, solid_capstyle="butt", zorder=3)
            ax.text(hi * 1.14, y, f"{lo*100:.1f}% 至 {hi*100:.1f}%", fontsize=8.0,
                    color="#33414f", va="center")
    ax.axvline(0.003, color=bs.RED, lw=1.1, ls=(0, (3, 2.5)), zorder=4)
    ax.text(0.0038, -0.52, "今天最好的超导器件", fontsize=7.6, color=bs.RED,
            ha="left", va="center")

    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_xscale("log")
    ax.set_xlim(0.0022, 0.30)
    ax.set_ylim(-0.85, 2.55)
    ax.set_xlabel("表面码的阈值（按错误率计）")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    bs.clean(ax, grid_axis="x")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_threshold_cross()
    fig_noise_models()
