"""第十三章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "13"


def fig_tanner():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.45),
                             gridspec_kw={"width_ratios": [1.0, 1.25], "wspace": 0.05})

    ax = axes[0]
    nx, ny = 5, 5
    for i in range(nx - 1):
        for j in range(ny - 1):
            cx, cy = i + 0.5, j + 0.5
            ax.add_patch(plt.Rectangle((cx - 0.15, cy - 0.15), 0.30, 0.30,
                                       facecolor="#f3ece0", edgecolor="#a8927a", lw=0.8,
                                       zorder=3))
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                ax.plot([cx + dx * 0.20, cx + dx * 0.30], [cy + dy * 0.20, cy + dy * 0.30],
                        color="#b7c6d6", lw=0.6, zorder=2)
    for i in range(nx):
        for j in range(ny):
            ax.plot([i], [j], "o", ms=4.6, mfc="white", mec=bs.BLUE, mew=0.9, zorder=4)
    ax.set_xlim(-0.8, nx - 0.2)
    ax.set_ylim(-0.75, ny - 0.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0.5, -0.09, "近邻耦合", transform=ax.transAxes, fontsize=8.4,
            color="#33414f", ha="center", va="top")

    ax = axes[1]
    rng = np.random.default_rng(7)
    nv, nc = 12, 6
    vx = np.linspace(0.0, 9.0, nv)
    cxs = np.linspace(0.75, 8.25, nc)
    for i in range(nv):
        for c in rng.choice(nc, size=3, replace=False):
            ax.plot([vx[i], cxs[c]], [1.0, 0.0], color="#c3b6a8", lw=0.65, alpha=0.9, zorder=2)
    ax.plot(vx, np.ones(nv), "o", ms=5.4, mfc="white", mec=bs.BLUE, mew=1.0, zorder=4)
    ax.plot(cxs, np.zeros(nc), "s", ms=5.6, mfc="#f3ece0", mec="#a8927a", mew=1.0, zorder=4)
    ax.text(-0.55, 1.0, "变量", fontsize=7.8, color="#4a5563", ha="right", va="center")
    ax.text(-0.55, 0.0, "校验", fontsize=7.8, color="#4a5563", ha="right", va="center")
    ax.set_xlim(-2.3, 9.6)
    ax.set_ylim(-0.62, 1.45)
    ax.axis("off")
    ax.text(0.42, -0.09, "长程耦合的 Tanner 图", transform=ax.transAxes,
            fontsize=8.4, color="#33414f", ha="center", va="top")

    bs.save(fig, CH, "fig01")


def fig_overhead():
    p = np.logspace(-5, np.log10(3e-3), 400)
    pth = 6e-3
    target = 1e-12

    d_surf = 2 * np.log(0.1 / target) / np.log(pth / p) - 1
    d_ldpc = 2 * np.log(0.1 / target) / np.log(pth / p)
    n_surf = 4 * np.maximum(d_surf, 3) ** 2
    n_ldpc = np.maximum(d_ldpc, 3)

    fig, ax = plt.subplots(figsize=(6.1, 3.4))
    ax.loglog(p, n_surf, color=bs.BLUE, lw=1.6)
    ax.loglog(p, n_ldpc, color=bs.RED, lw=1.6)

    ax.text(1.4e-5, 520, "表面码", fontsize=8.4, color=bs.BLUE, ha="left", va="top")
    ax.text(3.2e-5, 3.6, "qLDPC", fontsize=8.4, color=bs.RED, ha="left", va="bottom")

    ax.plot([1e-3], [2980], "o", ms=5.0, mfc=bs.BLUE, mec="white", mew=0.8, zorder=5)
    ax.plot([1e-3], [28], "o", ms=5.0, mfc=bs.RED, mec="white", mew=0.8, zorder=5)
    ax.axvline(1e-3, color="#b8c3cf", lw=0.8, ls=(0, (2, 2.5)))
    ax.text(1.18e-3, 780, "今天的器件", fontsize=7.4, color="#6b7785", ha="left",
            va="center")

    ax.set_xlabel("物理错误率 $p$")
    ax.set_ylabel("每个逻辑比特的物理比特数")
    ax.set_xlim(1e-5, 3e-3)
    ax.set_ylim(3, 2e4)
    ax.set_yticks([10, 100, 1000, 10000])
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_tanner()
    fig_overhead()
