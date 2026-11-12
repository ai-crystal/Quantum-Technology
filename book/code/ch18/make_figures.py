"""第十八章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.special import hermite, factorial

import bookstyle as bs

CH = "18"


def fig_oscillator():
    x = np.linspace(-5, 5, 900)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    for n in range(4):
        psi = (2 ** n * factorial(n) * np.sqrt(np.pi)) ** -0.5 * hermite(n)(x) * np.exp(-x ** 2 / 2)
        y = n + 0.9 + 0.75 * psi
        ax.plot(x, y, color=bs.BLUE, lw=1.1)
        ax.fill_between(x, y, n + 0.9, where=(psi > 0), color=bs.BLUE, alpha=0.10)
        ax.plot([-5, 5], [n + 0.9, n + 0.9], color="#d5dce5", lw=0.7, ls=(0, (3, 3)))
        ax.text(-4.9, n + 1.02, f"$n={n}$", fontsize=8.2, color="#33414f")
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 4.9)
    ax.set_xlabel(r"位置 $x$（以零点宽度为单位）")
    ax.set_yticks([])
    ax.set_ylabel("能级与波函数")
    bs.clean(ax)
    bs.save(fig, CH, "fig01")


def wigner_coherent(X, P, x0, p0, sx=1.0):
    return (2 / np.pi) * np.exp(-2 * ((X - x0) ** 2 + (P - p0) ** 2))


def wigner_squeezed(X, P, r):
    a = np.exp(-2 * r)
    b = np.exp(2 * r)
    return (2 / np.pi) * np.exp(-2 * (a * X ** 2 + b * P ** 2))


def wigner_n1(X, P):
    r2 = X ** 2 + P ** 2
    return (2 / np.pi) * (4 * r2 - 1) * np.exp(-2 * r2)


def fig_wigner():
    lim = 4.0
    v = np.linspace(-lim, lim, 320)
    X, P = np.meshgrid(v, v)
    panels = [
        (wigner_coherent(X, P, 2.0, 0.0), "相干态"),
        (wigner_squeezed(X, P, 0.9), "压缩真空态"),
        (wigner_n1(X, P), "单光子态"),
    ]
    fig = plt.figure(figsize=(7.0, 2.5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.32)
    for i, (W, name) in enumerate(panels):
        ax = fig.add_subplot(gs[0, i])
        m = np.abs(W).max()
        im = ax.pcolormesh(X, P, W, cmap="RdBu_r", vmin=-m, vmax=m, shading="auto", rasterized=True)
        ax.contour(X, P, W, levels=[0], colors="#4a5563", linewidths=0.7)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
        ax.tick_params(labelsize=7.4)
        ax.axhline(0, color="#c9d2dc", lw=0.5)
        ax.axvline(0, color="#c9d2dc", lw=0.5)
        if i == 0:
            ax.set_ylabel(r"$p$", fontsize=9)
        else:
            ax.set_yticklabels([])
        ax.set_xlabel(r"$x$", fontsize=9)
    bs.save(fig, CH, "fig02", kind="photo")


if __name__ == "__main__":
    fig_oscillator()
    fig_wigner()
