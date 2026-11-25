"""第四章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

import bookstyle as bs

bs.use("foundations")

CH = "04"
h = 6.62607015e-34
e = 1.602176634e-19
me = 9.1093837015e-31
mp = 1.67262192369e-27


def fig_wavelength():
    U = np.logspace(-1, 5, 400)  # 加速电压 V
    lam_e = h / np.sqrt(2 * me * e * U) * 1e9   # nm
    lam_p = h / np.sqrt(2 * mp * e * U) * 1e9
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.loglog(U, lam_e, color=bs.BLUE, lw=1.5, label="电子")
    ax.loglog(U, lam_p, color=bs.RED, lw=1.5, label="质子")
    ax.axhline(0.15, color=bs.GRAY, lw=0.8, ls=(0, (4, 3)))
    ax.text(0.13, 0.17, "典型原子间距 0.15 nm", fontsize=7.8, color=bs.GRAY, va="bottom")
    ax.set_xlabel("加速电压 (V)")
    ax.set_ylabel("德布罗意波长 (nm)")
    ax.set_xlim(0.1, 1e5)
    ax.set_ylim(1e-5, 3)
    ax.legend(loc="lower left", handlelength=1.6)
    ax.annotate("100 V 的电子，波长 0.12 nm", xy=(100, 0.1226), xytext=(1.6, 0.0055),
                fontsize=7.8, color=bs.BLUE,
                arrowprops=dict(arrowstyle="-|>", color=bs.BLUE, lw=0.7, connectionstyle="arc3,rad=-0.25"))
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_buildup():
    lam = 50e-12      # 电子波长 50 pm
    d = 12.5e-6       # 双缝间距 12.5 μm
    L = 0.5           # 屏幕距离 0.5 m
    a = 3.0e-6        # 缝宽
    rng = np.random.default_rng(20240501)
    xmax = 9e-6

    def pdf(x):
        th = np.arctan(x / L)
        beta = np.pi * a * np.sin(th) / lam
        alpha = np.pi * d * np.sin(th) / lam
        return np.sinc(beta / np.pi) ** 2 * np.cos(alpha) ** 2

    xs = np.linspace(-xmax, xmax, 4000)
    p = pdf(xs)
    p = p / p.sum()
    cdf = np.cumsum(p)
    sigma_y = 3.0e-6

    counts = [20, 200, 2000, 20000]
    fig, axes = plt.subplots(1, 4, figsize=(7.0, 2.35), sharey=True)
    for ax, N in zip(axes, counts):
        u = rng.random(N)
        x = np.interp(u, cdf, xs)
        y = rng.normal(0, sigma_y, N)
        ax.scatter(x * 1e6, y * 1e6, s=1.6, color="#1f2a37", alpha=0.55, linewidths=0)
        ax.set_xlim(-9, 9)
        ax.set_ylim(-9, 9)
        ax.set_xticks([-8, 0, 8])
        ax.set_yticks([])
        ax.set_xlabel(f"{N} 个电子", fontsize=8)
        ax.tick_params(labelsize=7.5)
        for s in ["top", "right", "left"]:
            ax.spines[s].set_visible(False)
        if ax is not axes[0]:
            ax.spines["left"].set_visible(False)
    axes[0].set_ylabel("屏幕竖直方向 (μm)", fontsize=8)
    fig.text(0.5, 0.02, "屏幕水平方向 (μm)", ha="center", fontsize=8.5)
    fig.subplots_adjust(bottom=0.30, wspace=0.12)
    bs.save(fig, CH, "fig02")


def fig_bragg():
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.35, 5.0)
    ax.axis("off")

    y1, y2 = 2.75, 1.35
    for yy in [y1, y2]:
        ax.plot([0.9, 9.3], [yy, yy], color="#b9c3cf", lw=0.9)
        for xx in np.arange(1.05, 9.4, 0.7):
            ax.add_patch(Circle((xx, yy), 0.095, facecolor="#4a6fa5", edgecolor="none"))

    xa = 3.75
    A = (xa, y1)
    B = (xa, y2)
    ax.plot([xa, xa], [y2 - 0.55, y1 + 0.75], color="#8a95a3", lw=0.7, ls=(0, (2.5, 2.5)))
    ax.text(xa + 0.12, y1 + 0.60, "法线", fontsize=7.6, color="#8a95a3")

    dx, dy = 1.55, 1.55
    ax.annotate("", xy=A, xytext=(A[0] - dx, A[1] + dy),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.5, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=B, xytext=(B[0] - dx, B[1] + dy),
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.0, ls=(0, (3.5, 2.2)), shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(A[0] + dx, A[1] + dy), xytext=A,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.5, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(B[0] + dx, B[1] + dy), xytext=B,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.0, ls=(0, (3.5, 2.2)), shrinkA=0, shrinkB=0))

    ax.text(A[0] - dx - 0.12, A[1] + dy + 0.08, "入射", fontsize=8.2, color=bs.ORANGE, ha="right")
    ax.text(A[0] + dx + 0.12, A[1] + dy + 0.08, "散射", fontsize=8.2, color=bs.RED, ha="left")

    ax.add_patch(Arc(A, 1.0, 1.0, theta1=90, theta2=135, color="#4a5563", lw=0.8))
    ax.text(A[0] - 0.34, A[1] + 0.52, r"$\theta$", fontsize=9.5, color="#4a5563", ha="center", va="center")

    ax.annotate("", xy=(xa + 1.85, y2), xytext=(xa + 1.85, y1),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GREEN, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(xa + 1.96, (y1 + y2) / 2, "$d$", fontsize=9, color=bs.GREEN, va="center")

    ax.text(0.95, 0.80, "光程差为 $2d\\sin\\theta$，等于波长的整数倍时散射加强", fontsize=8.2, color="#33414f")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_wavelength()
    fig_buildup()
    fig_bragg()
