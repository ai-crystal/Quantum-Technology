"""第 8 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from scipy.special import erfc

import bookstyle as bs

bs.use("devices")

CH = "08"


def fig_dot_readout():
    fig = plt.figure(figsize=(7.0, 2.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.28)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    layers = [
        (0.30, 0.72, "#eef1f5", "Si 衬底"),
        (1.02, 0.76, "#dfe8f2", "SiGe 缓冲层"),
        (1.78, 0.34, "#9db8d2", "应变 Si 量子阱"),
        (2.12, 0.92, "#dfe8f2", "SiGe 间隔层"),
    ]
    for y0, h, color, name in layers:
        ax.add_patch(Rectangle((0.4, y0), 9.2, h, facecolor=color, edgecolor="#8a97a6", lw=0.7))
        ax.text(9.45, y0 + h / 2, name, fontsize=7.0, color="#4a5563", va="center", ha="right")

    gates = [(1.0, 1.1, "G1"), (3.1, 1.1, "G2"), (5.2, 1.0, "G3"), (7.3, 1.1, "G4")]
    for x0, w, name in gates:
        ax.add_patch(Rectangle((x0, 3.04), w, 0.40, facecolor="#c9c2b4", edgecolor="#8a8271", lw=0.8))
        ax.text(x0 + w / 2, 3.55, name, fontsize=7.4, color="#4a5563", ha="center")

    for x in [2.6, 6.8]:
        ax.add_patch(Circle((x, 1.95), 0.12, facecolor=bs.ORANGE, edgecolor="#8a5a12", lw=0.7))
    ax.annotate("电子自旋", xy=(6.8, 2.10), xytext=(6.9, 4.40), fontsize=7.6, color="#8a5a12",
                ha="center", arrowprops=dict(arrowstyle="-|>", color="#8a5a12", lw=0.7))
    ax.annotate("传感点", xy=(2.6, 1.82), xytext=(2.5, 4.40), fontsize=7.6, color="#4a5563",
                ha="center", arrowprops=dict(arrowstyle="-|>", color="#4a5563", lw=0.7))

    ax = fig.add_subplot(gs[0, 1])
    snr = 2.9
    sigma = 1.0
    mu = snr * 2 * sigma / 2 * 2 / 2  # 两个峰间距 = snr*2*sigma
    mu = snr * sigma
    x = np.linspace(-5, 5, 700)
    p0 = np.exp(-(x + mu) ** 2 / (2 * sigma ** 2))
    p1 = np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))
    ax.fill_between(x, 0, p0, color=bs.BLUE, alpha=0.22, lw=0)
    ax.fill_between(x, 0, p1, color=bs.RED, alpha=0.22, lw=0)
    ax.plot(x, p0, color=bs.BLUE, lw=1.2)
    ax.plot(x, p1, color=bs.RED, lw=1.2)
    ax.axvline(0, color="#4a5563", lw=0.8, ls=(0, (4, 3)))
    ax.text(0.12, 1.02, "判决阈值", fontsize=7.4, color="#4a5563", rotation=90, va="top")
    ax.text(-mu, 1.06, "$|\\uparrow\\rangle$", fontsize=9, color=bs.BLUE, ha="center")
    ax.text(mu, 1.06, "$|\\downarrow\\rangle$", fontsize=9, color=bs.RED, ha="center")

    fid = 1 - 0.5 * erfc(snr / np.sqrt(2))
    ax.text(-4.7, 0.62, f"信噪比 {snr}\n保真度 {fid * 100:.1f}%", fontsize=8, color="#33414f",
            va="top")
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 1.22)
    ax.set_yticks([])
    ax.set_xlabel("传感器电流（归一化）")
    ax.set_ylabel("计数")
    bs.clean(ax)
    bs.save(fig, CH, "fig01", kind="photo")


def fig_isotope():
    c = np.logspace(np.log10(2e-5), np.log10(0.05), 400)
    k = 1.5e-6 * np.sqrt(0.047)
    t2 = k / np.sqrt(c)

    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    ax.loglog(c * 100, t2 * 1e6, color=bs.BLUE, lw=1.5)
    ax.fill_between(c * 100, t2 * 1e6, 1e-1, color=bs.BLUE, alpha=0.06)

    for xv, name, color in [(4.7, "天然硅", bs.RED), (0.08, "纯化硅", bs.GREEN)]:
        ax.axvline(xv, color=color, lw=0.9, ls=(0, (4, 3)))
        yy = k / np.sqrt(xv / 100) * 1e6
        ax.plot([xv], [yy], marker="o", ms=4.0, color=color, mfc="white", mew=1.1)
        ax.annotate(name, (xv, yy), textcoords="offset points",
                    xytext=(8 if xv < 1 else -8, 10), fontsize=8, color=color,
                    ha="left" if xv < 1 else "right")

    ax.text(0.02, 0.30, "$T_2^* \\propto c^{-1/2}$", fontsize=10, color=bs.BLUE)
    ax.set_xlim(0.002, 6)
    ax.set_ylim(0.3, 200)
    ax.set_xlabel("$^{29}$Si 浓度（%）")
    ax.set_ylabel("退相位时间 $T_2^*$（微秒）")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_dot_readout()
    fig_isotope()
