"""第 10 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

import bookstyle as bs

bs.use("devices")

CH = "10"

SUB = "#eef1f5"
SUB_E = "#8a97a6"
RES_L = "#d8dee8"
RES_U = "#c3ccdb"
ALU = "#b9c6d6"
ALU_E = "#6f7f92"


def _substrate(ax):
    ax.add_patch(Rectangle((0.15, 0.35), 3.7, 0.6, facecolor=SUB, edgecolor=SUB_E, lw=0.8))
    ax.text(0.2, 0.65, "衬底", fontsize=6.6, color="#4a5563", va="center", ha="left")


def _mask(ax):
    # 下层 MAA，横向退得多
    for x0, x1 in ((0.15, 1.02), (2.98, 3.85)):
        ax.add_patch(Rectangle((x0, 0.95), x1 - x0, 0.95, facecolor=RES_L,
                               edgecolor="#98a3b3", lw=0.7))
    # 上层 PMMA，向中间伸出，形成屋檐
    for x0, x1 in ((0.15, 1.32), (2.68, 3.85)):
        ax.add_patch(Rectangle((x0, 1.90), x1 - x0, 0.80, facecolor=RES_U,
                               edgecolor="#98a3b3", lw=0.7))


def fig_dolan():
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.5), gridspec_kw={"wspace": 0.08})
    for ax in axes:
        ax.set_xlim(0, 4.0)
        ax.set_ylim(0, 4.2)
        ax.axis("off")

    # (a) 双层胶与屋檐
    ax = axes[0]
    _substrate(ax)
    _mask(ax)
    ax.text(0.22, 2.30, "PMMA", fontsize=6.6, color="#33414f", va="center")
    ax.text(0.22, 1.42, "MAA", fontsize=6.6, color="#33414f", va="center")
    ax.annotate("屋檐", xy=(1.30, 1.90), xytext=(1.55, 3.30), fontsize=6.6,
                color=bs.RED, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7))

    # (b) 第一角度蒸发
    ax = axes[1]
    _substrate(ax)
    _mask(ax)
    ax.add_patch(Polygon([[0.95, 0.95], [2.30, 0.95], [2.30, 1.32], [1.10, 1.32]],
                         closed=True, facecolor=ALU, edgecolor=ALU_E, lw=0.8))
    ax.annotate("", xy=(1.15, 2.20), xytext=(0.35, 3.80),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.1))
    ax.text(1.32, 3.42, "Al", fontsize=6.8, color=bs.BLUE, ha="left", va="center")

    # (c) 原位氧化
    ax = axes[2]
    _substrate(ax)
    _mask(ax)
    ax.add_patch(Polygon([[0.95, 0.95], [2.30, 0.95], [2.30, 1.32], [1.10, 1.32]],
                         closed=True, facecolor=ALU, edgecolor=ALU_E, lw=0.8))
    ax.plot([1.06, 2.30], [1.32, 1.32], color=bs.RED, lw=1.6, solid_capstyle="butt")
    for xx in (1.45, 1.85, 2.25):
        ax.plot([xx], [2.55], marker="o", ms=2.6, color=bs.GREEN)
    ax.text(1.85, 2.78, "O$_2$", fontsize=6.8, color=bs.GREEN, ha="center")
    ax.annotate("AlO$_x$ 1–2 nm", xy=(1.90, 1.32), xytext=(2.05, 3.35), fontsize=6.6,
                color=bs.RED, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7))

    # (d) 第二角度蒸发
    ax = axes[3]
    _substrate(ax)
    _mask(ax)
    ax.add_patch(Polygon([[0.95, 0.95], [2.30, 0.95], [2.30, 1.32], [1.10, 1.32]],
                         closed=True, facecolor=ALU, edgecolor=ALU_E, lw=0.8))
    ax.add_patch(Polygon([[1.62, 0.95], [2.95, 0.95], [2.95, 1.32], [1.75, 1.32]],
                         closed=True, facecolor="#9aabbf", edgecolor=ALU_E, lw=0.8))
    ax.plot([1.72, 2.22], [1.32, 1.32], color=bs.RED, lw=1.6, solid_capstyle="butt")
    ax.annotate("", xy=(2.62, 2.25), xytext=(3.30, 3.80),
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=1.1))
    ax.text(2.52, 3.42, "Al", fontsize=6.8, color=bs.BLUE, ha="right", va="center")
    ax.annotate("结", xy=(2.16, 1.36), xytext=(2.36, 1.66), fontsize=7.2, color="#1f2a37",
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-|>", color="#1f2a37", lw=0.7))

    for ax, tag in zip(axes, ["(a)", "(b)", "(c)", "(d)"]):
        ax.text(0.05, 3.95, tag, fontsize=7.6, color="#33414f", ha="left", va="top")

    bs.save(fig, CH, "fig01")


R_Q = 6453.0          # h/4e^2，欧姆
DELTA_MEV = 0.18
EC_GHZ = 0.25


def f01_from_rn(rn):
    delta_over_2h = DELTA_MEV * 1e-3 * 1.602176634e-19 / (2 * 6.62607015e-34) / 1e9
    ej = R_Q / rn * delta_over_2h
    return np.sqrt(8 * ej * EC_GHZ) - EC_GHZ


def fig_spread():
    rng = np.random.default_rng(7)
    rn = 10e3 * np.exp(rng.normal(0.0, 0.08, 4000))
    f = f01_from_rn(rn)

    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.26, width_ratios=[1, 1])

    ax = fig.add_subplot(gs[0, 0])
    ax.hist(rn / 1e3, bins=44, color=bs.BLUE, alpha=0.72, edgecolor="white", linewidth=0.4)
    ax.axvline(10.0, color=bs.RED, lw=1.0, ls=(0, (4, 3)))
    ax.text(7.35, ax.get_ylim()[1] * 0.96, "中位 10 kΩ", fontsize=7.2, color=bs.RED,
            ha="left", va="top")
    ax.set_xlabel("结电阻 $R_N$（kΩ）")
    ax.set_ylabel("计数")
    ax.set_xlim(7.0, 14.0)
    bs.clean(ax, grid_axis="y")

    ax = fig.add_subplot(gs[0, 1])
    ax.hist(f, bins=44, color=bs.GREEN, alpha=0.72, edgecolor="white", linewidth=0.4)
    ax.axvline(5.0, color=bs.RED, lw=1.0, ls=(0, (4, 3)))
    ax.axvspan(5.0 - f.std(), 5.0 + f.std(), color=bs.RED, alpha=0.08, lw=0)
    ax.set_xlabel("比特频率 $f_{01}$（GHz）")
    ax.set_ylabel("计数")
    ax.set_xlim(4.3, 5.8)
    ax.text(4.34, ax.get_ylim()[1] * 0.95,
            f"$\\sigma_f\\approx{f.std() * 1e3:.0f}$ MHz\n非谐性 250 MHz",
            fontsize=7.4, color="#33414f", ha="left", va="top")
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_dolan()
    fig_spread()
