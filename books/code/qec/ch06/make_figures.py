"""第六章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "06"

G1T = 1.0e-3  # 一个门时间里 Γ1·t


def fig_bias():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3),
                             gridspec_kw={"width_ratios": [1.15, 1.0], "wspace": 0.28})

    ax = axes[0]
    x = np.logspace(-1.3, 1.5, 400)  # T1 / Tφ
    p_xy = G1T / 4 * np.ones_like(x)
    p_z = G1T / 4 + G1T * x / 2
    ax.loglog(x, p_z, color=bs.RED, lw=1.6)
    ax.loglog(x, p_xy, color=bs.BLUE, lw=1.6)
    ax.text(0.07, 1.6e-3, "相位翻转 $Z$", fontsize=7.6, color=bs.RED)
    ax.text(0.07, 1.9e-4, "比特翻转 $X$ 与 $Y$", fontsize=7.6, color=bs.BLUE)
    ax.annotate("偏置很小", xy=(0.125, 9.8e-4), xytext=(0.058, 3.4e-3),
                fontsize=7.4, color="#6b7785",
                arrowprops=dict(arrowstyle="-|>", color="#9aa5b1", lw=0.8))
    ax.annotate("偏置很大", xy=(9.0, 5.6e-3), xytext=(2.6, 1.6e-2),
                fontsize=7.4, color="#6b7785",
                arrowprops=dict(arrowstyle="-|>", color="#9aa5b1", lw=0.8))
    ax.set_xlabel("$T_1/T_\\varphi$")
    ax.set_ylabel("单次门内的错误概率")
    ax.set_xlim(0.05, 32)
    ax.set_ylim(1.3e-4, 4e-2)
    bs.clean(ax, grid_axis="both")
    ax.text(0.055, 2.6e-2, "(a)", fontsize=10, color=bs.INK)

    ax = axes[1]
    ratios = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    px = np.array([G1T / 4] * len(ratios))
    pz = np.array([G1T / 4 + G1T * r / 2 for r in ratios])
    tot = 2 * px + pz
    fx, fy, fz = px / tot, px / tot, pz / tot
    xs = np.arange(len(ratios))
    ax.bar(xs, fx, width=0.66, color=bs.BLUE, edgecolor="none", label="$X$")
    ax.bar(xs, fy, bottom=fx, width=0.66, color="#9db4cc", edgecolor="none", label="$Y$")
    ax.bar(xs, fz, bottom=fx + fy, width=0.66, color=bs.RED, edgecolor="none", label="$Z$")
    for i, r in enumerate(ratios):
        ax.text(i, 1.035, f"{1 + 2 * r:.0f}", fontsize=7.2, color="#4a5563", ha="center")
    ax.set_xticks(xs)
    ax.set_xticklabels(["0.1", "0.3", "1", "3", "10", "30"])
    ax.set_xlabel("$T_1/T_\\varphi$")
    ax.set_ylabel("三种错误所占的比例")
    ax.set_ylim(0, 1.2)
    ax.set_yticks([0, 0.5, 1.0])
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=7.6,
              handlelength=0.9, borderaxespad=0.1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(-0.86, 1.16, "(b)", fontsize=10, color=bs.INK)

    bs.save(fig, CH, "fig01")


def fig_erasure():
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    x = np.logspace(-3, np.log10(0.62), 500)
    dep_cols = ["#a8bed6", "#6f93b8", bs.BLUE]
    era_cols = ["#a9c7b4", "#6fa287", bs.GREEN]
    for d, cd, ce in zip((3, 5, 7), dep_cols, era_cols):
        k = (d + 1) / 2.0
        ax.loglog(x, 0.1 * (x / 0.103) ** k, color=cd, lw=1.4)
        ax.loglog(x, 0.1 * (x / 0.50) ** k, color=ce, lw=1.4, ls=(0, (5, 2.5)))

    ax.axvline(0.103, color=bs.BLUE, lw=0.9, ls=(0, (2, 2.5)))
    ax.axvline(0.50, color=bs.GREEN, lw=0.9, ls=(0, (2, 2.5)))
    ax.text(0.113, 2.2e-9, "去极化阈值\n10.3%", fontsize=7.4, color=bs.BLUE, va="bottom")
    ax.text(0.52, 2.2e-9, "擦除阈值\n50%", fontsize=7.4, color=bs.GREEN, va="bottom")

    ax.axvline(0.01, color="#c2cad3", lw=0.8, ls=(0, (1.5, 2.5)))
    ax.text(1.15e-2, 0.46, "1% 的物理错误", fontsize=7.4, color="#6b7785",
            va="center")

    handles = [Line2D([], [], color=bs.BLUE, lw=1.4),
               Line2D([], [], color=bs.GREEN, lw=1.4, ls=(0, (5, 2.5)))]
    ax.legend(handles, ["去极化，错误方向未知", "擦除，错误位置已知"],
              loc="lower left", fontsize=7.4, handlelength=1.6,
              borderpad=0.5, labelspacing=0.45, framealpha=0.92,
              edgecolor="none")

    ax.set_xlabel("每比特每轮的物理错误率")
    ax.set_ylabel("每轮逻辑错误率 $p_L$")
    ax.set_xlim(1e-3, 0.62)
    ax.set_ylim(1e-9, 1.2)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bias()
    fig_erasure()
