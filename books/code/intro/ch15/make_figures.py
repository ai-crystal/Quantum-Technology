"""第 15 章插图：算法加速的量级与资源边界。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("intro")

CH = "15"


def fig_speedup():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    fig.subplots_adjust(wspace=0.32)

    # 左：Grover 的平方根加速
    ax = axes[0]
    N = np.logspace(2, 12, 240)
    ax.plot(N, N / 2.0, color=bs.RED, lw=1.3, label="经典逐个试")
    ax.plot(N, np.pi / 4 * np.sqrt(N), color=bs.BLUE, lw=1.5, label="Grover 搜索")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e2, 1e12)
    ax.set_ylim(1e2, 1e13)
    ax.set_xlabel("搜索空间的元素个数 $N$")
    ax.set_ylabel("需要的查询次数")
    ax.legend(loc="upper left", handlelength=1.6)
    ax.text(2.2e6, 1.15e2, "在 $N=10^{12}$ 处相差约 64 万倍",
            fontsize=7.2, color="#4a5563", va="bottom")
    ax.annotate("", xy=(1e12, 5e11), xytext=(1e12, 7.9e5),
                arrowprops=dict(arrowstyle="<->", color="#8a95a6", lw=0.9,
                                shrinkA=1, shrinkB=1))
    ax.text(6.0e11, 2.2e8, "6 个数量级", fontsize=7.0, color="#6b7785",
            rotation=90, va="center", ha="right")
    bs.clean(ax, grid_axis="both")

    # 右：Shor 把指数变成多项式
    ax = axes[1]
    n = np.linspace(32, 2048, 300)
    L = np.exp(1.923 * n ** (1 / 3) * np.log(n) ** (2 / 3))
    ax.plot(n, L, color=bs.RED, lw=1.4, label="经典数域筛")
    ax.plot(n, 0.3 * n ** 3, color=bs.BLUE, lw=1.5, label="Shor 算法")
    ax.set_yscale("log")
    ax.set_xlim(32, 2048)
    ax.set_ylim(1e2, 1e45)
    ax.set_xlabel("要分解的整数位数")
    ax.set_ylabel("操作数的渐进量级")
    ax.legend(loc="upper left", handlelength=1.6)
    ax.text(760, 3e3, "多项式", fontsize=7.4, color=bs.BLUE, ha="left")
    ax.text(760, 3e22, "亚指数", fontsize=7.4, color=bs.RED, ha="left")
    ax.set_xticks([32, 256, 512, 1024, 2048])
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig01")


def fig_map():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(8, 2e5)
    ax.set_ylim(1e2, 2e10)

    ax.add_patch(Rectangle((10, 1e2), 990, 2e4, facecolor="#dfe8f3", alpha=0.70,
                           edgecolor="#9fb3c8", lw=0.7, zorder=0))
    ax.text(11.5, 3.6e2, "当前设备够得着的范围", fontsize=7.4, color="#3d5a78",
            va="bottom", ha="left", zorder=4)

    ax.add_patch(Rectangle((1e3, 1e5), 1.99e5, 2e5 * 1e5, facecolor="#f4e4d8", alpha=0.60,
                           edgecolor="#c9a58e", lw=0.7, zorder=0))
    ax.text(1.35e3, 2.6e5, "容错机器才能进入", fontsize=7.4, color="#8a5636",
            va="bottom", ha="left", zorder=4)

    pts = [
        (12, 1.2e3, "VQE 算小分子", 9, 4, "left"),
        (110, 2.6e3, "QAOA 组合优化", 9, 5, "left"),
        (36, 2.0e6, "Grover 搜 40 比特", 9, 5, "left"),
        (30, 3.0e7, "HHL 解稀疏方程组", 9, 5, "left"),
        (120, 4.0e8, "相位估计 化学精度", -9, 5, "right"),
        (4.2e3, 6.0e9, "Shor 分解 2048 位", -9, -3, "right"),
    ]
    for x, y, name, dx, dy, ha in pts:
        ax.plot([x], [y], "o", ms=5.0, color=bs.BLUE, mec="white", mew=0.8, zorder=5)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(dx, dy),
                    fontsize=7.3, color="#25313f", ha=ha, va="center", zorder=6)

    ax.set_xlabel("逻辑比特数")
    ax.set_ylabel("线路深度（门层数）")
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_speedup()
    fig_map()
