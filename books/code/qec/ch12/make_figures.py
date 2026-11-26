"""第十二章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import bookstyle as bs

bs.use("qec")

CH = "12"

D = 7
T0 = 5          # 关闭接缝稳定子的时刻
TM = 12         # merge 结束、逻辑读出的时刻
TN = 24


def bar(ax, y, x0, x1, color, alpha=0.9, h=0.52):
    ax.add_patch(Rectangle((x0, y - h / 2), x1 - x0, h, facecolor=color,
                           edgecolor="white", lw=1.2, alpha=alpha, zorder=3))


def fig_surgery_timing():
    fig, ax = plt.subplots(figsize=(6.4, 2.9))

    bar(ax, 2, 0, TN, "#cfdceb")
    bar(ax, 1, 0, T0, "#e3e9f0")
    bar(ax, 1, TM, TN, "#e3e9f0")
    bar(ax, 1, T0, TM, "#e9c9c0")
    ax.text((T0 + TM) / 2, 1.0, "联合稳定子", fontsize=7.6, color="#8d4c3a",
            ha="center", va="center", zorder=5)
    ax.text((T0 + TM) / 2, 1.42, f"$d={D}$ 轮", fontsize=7.6, color="#8d4c3a",
            ha="center", va="bottom")
    ax.text(T0 / 2, 1.0, "边界稳定子", fontsize=7.4, color="#76838f",
            ha="center", va="center", zorder=5)
    ax.text((TM + TN) / 2, 1.0, "边界稳定子", fontsize=7.4, color="#76838f",
            ha="center", va="center", zorder=5)

    ax.plot([TM], [0], "v", ms=8, color=bs.RED, zorder=5)
    ax.annotate("读出 $\\bar Z_1\\bar Z_2$", xy=(TM, 0.09), xytext=(TM + 1.3, -0.42),
                fontsize=7.8, color=bs.RED, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color="#d8a79a", lw=0.7,
                                shrinkA=2, shrinkB=3))

    for x in (T0, TM):
        ax.axvline(x, color="#9aa6b4", lw=0.8, ls=(0, (2, 2.5)), zorder=2)

    ax.text(T0 + 0.3, 0.44, "merge 开始", fontsize=7.4, color="#8a97a6",
            ha="left", va="center")
    ax.text(TM + 0.3, 0.44, "split", fontsize=7.4, color="#8a97a6",
            ha="left", va="center")

    ax.set_xlim(-1.2, TN + 1.0)
    ax.set_ylim(-0.8, 2.55)
    ax.set_yticks([2, 1, 0])
    ax.set_yticklabels(["数据块内部", "接缝", "逻辑读出"])
    ax.set_xlabel("测量周期")
    ax.set_xticks([0, 5, 10, 15, 20, 24])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", alpha=0.45)
    ax.set_axisbelow(True)
    bs.clean(ax, grid_axis="x")
    bs.save(fig, CH, "fig01")


def fig_factory_queue():
    rho = np.linspace(0.02, 0.985, 500)
    w = rho / (1.0 - rho)

    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(rho, w, color=bs.BLUE, lw=1.6)
    ax.fill_between(rho, w, 0, where=(rho > 0.9), color=bs.RED, alpha=0.10, lw=0)
    ax.axhline(4.0, color="#8a97a6", lw=0.8, ls=(0, (3, 2.5)))
    ax.axvline(0.8, color="#8a97a6", lw=0.8, ls=(0, (3, 2.5)))
    ax.plot([0.8], [4.0], "o", ms=5.0, color=bs.BLUE, zorder=5)
    ax.text(0.785, 4.6, "利用率 0.8", fontsize=7.6, color="#6b7785",
            ha="right", va="bottom")
    ax.text(0.945, 13.5, "排队失控", fontsize=7.8, color=bs.RED,
            ha="center", va="bottom")

    ax.set_xlabel("工厂利用率 $\\rho$（需求除以产能）")
    ax.set_ylabel("主电路等待（产出周期）")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 26)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_surgery_timing()
    fig_factory_queue()
