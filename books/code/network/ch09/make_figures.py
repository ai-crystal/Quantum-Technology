"""第 9 章插图：三种组网拓扑与端到端密钥率，标准化进程的时间线。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import bookstyle as bs

bs.use("network")

CH = "09"


def node(ax, x, y, label, color="#33414f", fc="#eef2f7", w=0.20, h=0.16, fs=7.6):
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle="round,pad=0,rounding_size=0.012",
                         fc=fc, ec=color, lw=0.9, zorder=4)
    ax.add_patch(box)
    ax.text(x, y, label, fontsize=fs, ha="center", va="center", color=color, zorder=5)


def link(ax, p, q, color="#5b6a7a", lw=1.2, ls="-"):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=2,
            solid_capstyle="round")


def fig_topology():
    fig, axes = plt.subplots(1, 3, figsize=(6.4, 2.05),
                             gridspec_kw={"wspace": 0.08})

    titles = ["点对点", "可信中继链", "环网"]
    for ax, t in zip(axes, titles):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        ax.set_title(t, fontsize=8.6, color="#33414f", pad=3)

    # 点对点
    ax = axes[0]
    node(ax, 0.18, 0.52, "A")
    node(ax, 0.82, 0.52, "B")
    link(ax, (0.28, 0.52), (0.72, 0.52), bs.BLUE, 1.6)
    ax.text(0.50, 0.62, "一条链路", fontsize=7.4, ha="center", color=bs.BLUE)
    ax.text(0.50, 0.30, "密钥率 $r$", fontsize=7.4, ha="center", color="#4a5563")

    # 可信中继链
    ax = axes[1]
    xs = [0.08, 0.37, 0.63, 0.92]
    names = ["A", "R1", "R2", "B"]
    for x, nm in zip(xs, names):
        node(ax, x, 0.52, nm, color=bs.RED if nm.startswith("R") else "#33414f",
             fc="#fdf1ee" if nm.startswith("R") else "#eef2f7", w=0.16)
    for i in range(3):
        link(ax, (xs[i] + 0.08, 0.52), (xs[i + 1] - 0.08, 0.52), "#5b6a7a", 1.2)
        ax.text((xs[i] + xs[i + 1]) / 2, 0.395, "$r$", fontsize=7.4,
                ha="center", va="bottom", color="#4a5563")
    ax.text(0.50, 0.71, "每跳解密再加密", fontsize=7.4, ha="center", color=bs.RED)
    ax.text(0.50, 0.24, "端到端 $\\approx r/3$", fontsize=7.4, ha="center", color="#4a5563")

    # 环网
    ax = axes[2]
    pts = [(0.30, 0.26), (0.74, 0.26), (0.74, 0.74), (0.30, 0.74)]
    tags = ["A", "C", "D", "B"]
    for (x, y), tg in zip(pts, tags):
        node(ax, x, y, tg, w=0.16, h=0.14)
    link(ax, pts[0], pts[1], "#c3ccd6", 1.2, ls=(0, (3, 2)))
    ax.plot([0.52], [0.26], "x", ms=5.5, color=bs.RED, zorder=6)
    for i in [1, 2, 3]:
        link(ax, pts[i], pts[(i + 1) % 4], bs.GREEN, 1.7)
    ax.text(0.52, 0.86, "绕行路径", fontsize=7.2, ha="center", color=bs.GREEN)
    ax.text(0.52, 0.10, "断一条还有另一条", fontsize=7.4, ha="center", color="#4a5563")

    bs.save(fig, CH, "fig01")


def fig_rate_and_standards():
    fig = plt.figure(figsize=(6.3, 3.8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.9], hspace=0.66)

    ax = fig.add_subplot(gs[0])
    k = np.arange(1, 13)
    ax.semilogy(k, 1e4 / k, color=bs.BLUE, lw=1.5, marker="o", ms=3.4,
                label="每跳链路 10 kbps")
    ax.semilogy(k, 2e3 / k, color=bs.ORANGE, lw=1.5, marker="s", ms=3.2,
                label="每跳链路 2 kbps")
    ax.set_xlabel("端到端经过的跳数")
    ax.set_ylabel("端到端密钥率（bit/s）")
    ax.set_xlim(1, 12)
    ax.set_ylim(80, 3e4)
    ax.set_xticks([1, 2, 4, 6, 8, 10, 12])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.legend(loc="upper right", fontsize=7.6)
    ax.text(2.45, 155, "十跳之后\n只剩十分之一", fontsize=7.6, ha="left", color="#4a5563")
    bs.clean(ax, grid_axis="y")

    ax = fig.add_subplot(gs[1])
    ax.set_xlim(2006.5, 2025.0)
    ax.set_ylim(0.195, 1.03)
    ax.plot([2006.5, 2025.0], [0.52, 0.52], color="#c3ccd6", lw=1.1)
    for x in [2008, 2012, 2016, 2020, 2024]:
        ax.plot([x, x], [0.465, 0.52], color="#c3ccd6", lw=0.9)
        ax.text(x, 0.435, str(x), fontsize=7.0, ha="center", va="top", color="#6b7785")

    events = [
        (2008, 1, 1, "ETSI 成立 QKD 标准组", bs.BLUE),
        (2010, -1, 1, "GS QKD 004 应用接口", bs.BLUE),
        (2019, 1, 1, "GS QKD 014 密钥接口", bs.BLUE),
        (2021, -1, 1, "Y.3803 密钥管理", bs.GREEN),
        (2023, 1, 2, "ISO 23837 安全与测评", bs.PURPLE),
    ]
    for year, side, level, text, color in events:
        y_end = 0.52 + side * (0.20 + 0.18 * (level - 1))
        ax.plot([year], [0.52], "o", ms=4.6, color=color, zorder=5)
        ax.plot([year, year], [0.52, y_end], color=color, lw=0.8)
        ax.text(year, y_end + side * 0.03, text, fontsize=7.4, ha="center",
                va="bottom" if side > 0 else "top", color=color)

    ax.set_axis_off()
    ax.set_title("标准落地的时间顺序", fontsize=8.6, color="#33414f", pad=2, loc="left")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_topology()
    fig_rate_and_standards()
