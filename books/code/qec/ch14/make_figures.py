"""第十四章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

import bookstyle as bs

bs.use("qec")

CH = "14"

C_PREP = "#dfe6ee"
C_1Q = "#9db4cc"
C_2Q = "#a8c4b0"
C_T = "#e2a596"
C_MEAS = "#e8d3a8"
C_DEC = "#d8d8d8"


def fig_spacetime():
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    Y = {"L1": 3, "L2": 2, "L3": 1, "DEC": 0}
    h = 0.46

    def one(y, x0, x1, color, alpha=0.95, hatch=None):
        ax.add_patch(Rectangle((x0, y - h / 2), x1 - x0, h, facecolor=color,
                               edgecolor="white", lw=1.2, alpha=alpha, hatch=hatch,
                               zorder=3))

    def two(ya, yb, x0, x1, color):
        lo, hi = min(ya, yb), max(ya, yb)
        ax.add_patch(Rectangle((x0, lo - h / 2), x1 - x0, (hi - lo) + h,
                               facecolor=color, edgecolor="white", lw=1.2, zorder=3))

    one(Y["L1"], 0.0, 0.5, C_PREP)
    one(Y["L1"], 0.5, 1.1, C_1Q)
    two(Y["L1"], Y["L2"], 1.1, 3.1, C_2Q)
    one(Y["L1"], 3.1, 3.7, C_T)
    two(Y["L2"], Y["L3"], 3.7, 5.7, C_2Q)
    one(Y["L3"], 5.7, 6.3, C_MEAS)
    one(Y["DEC"], 5.7, 7.5, C_DEC, hatch="///")
    one(Y["L1"], 7.5, 8.1, C_1Q)
    two(Y["L1"], Y["L2"], 8.1, 10.1, C_2Q)

    ax.annotate("", xy=(7.55, 3.0), xytext=(7.4, 0.42),
                arrowprops=dict(arrowstyle="->", color="#8a97a6", lw=1.0,
                                connectionstyle="arc3,rad=-0.18"))

    ax.text(6.6, -0.42, "解码延迟", fontsize=7.4, color="#6b7785", ha="center",
            va="top")
    ax.text(3.4, 3.44, "T 注入要等工厂", fontsize=7.2, color="#a4604c", ha="center",
            va="bottom")
    ax.text(7.8, 3.44, "条件修正", fontsize=7.2, color="#4a6f9c", ha="center",
            va="bottom")

    ax.set_yticks([3, 2, 1, 0])
    ax.set_yticklabels(["$L_1$", "$L_2$", "$L_3$", "解码"])
    ax.set_ylim(-1.05, 3.85)
    ax.set_xlim(-0.2, 10.4)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xlabel("时间（以码距 $d$ 为单位）")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", alpha=0.45)
    ax.set_axisbelow(True)
    bs.clean(ax, grid_axis="x")

    handles = [
        Patch(facecolor=C_PREP, edgecolor="white", label="制备"),
        Patch(facecolor=C_1Q, edgecolor="white", label="单比特门"),
        Patch(facecolor=C_2Q, edgecolor="white", label="双比特手术"),
        Patch(facecolor=C_T, edgecolor="white", label="T 注入"),
        Patch(facecolor=C_MEAS, edgecolor="white", label="逻辑测量"),
        Patch(facecolor=C_DEC, edgecolor="white", hatch="///", label="解码与反馈"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.28),
              ncol=3, frameon=False, fontsize=7.4, handlelength=1.4,
              columnspacing=1.6, handletextpad=0.6)
    bs.save(fig, CH, "fig01")


def fig_window():
    w = np.arange(3, 16)
    ratio = 1.0 + 3.0 * np.exp(-(w - 4.0) / 3.0)
    delay = w * 1.0

    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    ax.plot(w, ratio, color=bs.BLUE, lw=1.6, marker="o", ms=3.4)

    ax2 = ax.twinx()
    ax2.plot(w, delay, color=bs.ORANGE, lw=1.3, ls=(0, (5, 2.5)))
    ax2.set_ylabel("解码延迟（测量周期）", color=bs.ORANGE)
    ax2.tick_params(axis="y", colors=bs.ORANGE)
    ax2.set_ylim(0, 17)
    ax2.spines["top"].set_visible(False)

    ax.axvline(7, color="#b8c3cf", lw=0.9, ls=(0, (3, 2.5)))
    ax.text(7.35, 4.55, "$w=d$", fontsize=7.8, color="#6b7785", ha="left", va="center")

    ax.set_xlabel("解码窗口长度 $w$（测量周期）")
    ax.set_ylabel("相对逻辑错误率", color=bs.BLUE)
    ax.tick_params(axis="y", colors=bs.BLUE)
    ax.set_xlim(2.5, 15.5)
    ax.set_ylim(0.95, 5.15)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.spines["top"].set_visible(False)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_spacetime()
    fig_window()
