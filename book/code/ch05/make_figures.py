"""第五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "05"
hbar = 1.054571817e-34
e = 1.602176634e-19


def fig_wavepacket():
    sigma = 1.0
    x = np.linspace(-5, 5, 800)
    psi = (2 * np.pi * sigma ** 2) ** -0.25 * np.exp(-x ** 2 / (4 * sigma ** 2))
    prob = psi ** 2
    sp = hbar / (2 * sigma)
    p = np.linspace(-4, 4, 800)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.55))
    ax = axes[0]
    ax.plot(x, psi, color=bs.BLUE, lw=1.3, label=r"$\psi(x)$")
    ax.plot(x, prob, color=bs.RED, lw=1.5, label=r"$|\psi(x)|^2$")
    ax.fill_between(x, 0, prob, color=bs.RED, alpha=0.10)
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("振幅 / 概率密度")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.05, 0.75)
    ax.legend(loc="upper left", handlelength=1.4)
    ax.text(0.15, 0.52, r"$\Delta x$", fontsize=9, color=bs.RED, ha="center")
    ax.annotate("", xy=(-1, 0.36), xytext=(1, 0.36),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.8, shrinkA=0, shrinkB=0))

    ax = axes[1]
    prof = np.exp(-p ** 2 / (2 * 0.5 ** 2))
    ax.plot(p, prof, color=bs.GREEN, lw=1.5, label=r"$|\phi(p)|^2$")
    ax.fill_between(p, 0, prof, color=bs.GREEN, alpha=0.10)
    ax.set_xlabel("动量 $p$（任意单位）")
    ax.set_ylabel("概率密度")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc="upper right", handlelength=1.4)
    axes[1].annotate("", xy=(-0.5, 0.62), xytext=(0.5, 0.62),
                     arrowprops=dict(arrowstyle="<|-|>", color=bs.GREEN, lw=0.8, shrinkA=0, shrinkB=0))
    axes[1].text(0, 0.66, r"$\Delta p$", fontsize=9, color=bs.GREEN, ha="center")
    bs.clean(axes[0], grid_axis="y")
    bs.clean(axes[1], grid_axis="y")
    fig.subplots_adjust(wspace=0.32)
    bs.save(fig, CH, "fig01")


def fig_uncertainty():
    dx = np.logspace(-11, -6, 300)   # 米
    dp = hbar / (2 * dx)
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    ax.loglog(dx * 1e9, dp, color=bs.BLUE, lw=1.6, label=r"$\Delta x\,\Delta p = \hbar/2$")

    points = [
        (0.1e-9, "原子中的电子\n$\\Delta x \\approx 0.1$ nm", bs.RED),
        (100e-9, "电子束中的电子\n$\\Delta x \\approx 100$ nm", bs.GREEN),
    ]
    for xv, label, color in points:
        yv = hbar / (2 * xv)
        ax.plot([xv * 1e9], [yv], "o", ms=4.2, color=color, zorder=5)
        ax.annotate(label, xy=(xv * 1e9, yv), xytext=(xv * 1e9 * 1.1, yv * 4.5),
                    fontsize=7.8, color=color,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=0.7))
    ax.set_xlabel(r"位置不确定度 $\Delta x$ (nm)")
    ax.set_ylabel(r"动量不确定度 $\Delta p$ (kg·m/s)")
    ax.set_xlim(0.03, 1000)
    ax.set_ylim(1e-27, 1e-22)
    ax.legend(loc="upper right", handlelength=1.8)
    ax.text(0.06, 1.6e-23, "允许区域在曲线之上", fontsize=7.8, color="#5a6674")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


def fig_lifetime():
    x = np.linspace(-22, 22, 2000)
    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    cases = [(1.0, 0.0, bs.BLUE, "寿命 1 ns"), (8.0, 1.25, bs.RED, "寿命 0.125 ns")]
    for gamma, off, color, label in cases:
        y = (gamma / 2) ** 2 / (x ** 2 + (gamma / 2) ** 2)
        ax.plot(x, y + off, color=color, lw=1.4, label=label)
        ax.annotate("", xy=(-gamma / 2, 0.5 + off), xytext=(gamma / 2, 0.5 + off),
                    arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.9, shrinkA=0, shrinkB=0))
        ax.text(gamma / 2 + 0.4, 0.52 + off, r"$\Gamma$", fontsize=9, color=color, va="center")
    ax.set_xlabel("能量（以第一组线宽为单位）")
    ax.set_ylabel("相对强度")
    ax.set_xlim(-22, 22)
    ax.set_ylim(0, 2.45)
    ax.set_yticks([])
    ax.legend(loc="upper right", handlelength=1.6)
    bs.clean(ax)
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_wavepacket()
    fig_uncertainty()
    fig_lifetime()
