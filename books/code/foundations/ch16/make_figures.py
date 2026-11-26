"""第十六章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.optimize import brentq

import bookstyle as bs

bs.use("foundations")

CH = "16"

HBAR = 1.055e-34
ME = 9.109e-31
QE = 1.602e-19
A = 2e-9          # 阱宽 2 nm
V0 = 1.0          # 阱深 1 eV


def infinite_levels(n_max=4):
    return np.array([(n ** 2 * np.pi ** 2 * HBAR ** 2) / (2 * ME * A ** 2) / QE
                     for n in range(1, n_max + 1)])


def finite_states():
    """解有限深阱，返回 (能量 eV, 波数 k, 衰减常数 kappa, 宇称)。"""
    k0 = np.sqrt(2 * ME * V0 * QE) / HBAR
    out = []
    n = 0
    while True:
        lo = n * np.pi / 2 + 1e-9
        hi = min((n + 1) * np.pi / 2 - 1e-9, k0 * A / 2 - 1e-9)
        if lo >= hi:
            break
        if n % 2 == 0:
            f = lambda z: z * np.tan(z) - np.sqrt((k0 * A / 2) ** 2 - z ** 2)
        else:
            f = lambda z: -z / np.tan(z) - np.sqrt((k0 * A / 2) ** 2 - z ** 2)
        if f(lo) * f(hi) >= 0:
            break
        z = brentq(f, lo, hi)
        k = 2 * z / A
        kappa = np.sqrt(k0 ** 2 - k ** 2)
        energy = (HBAR * k) ** 2 / (2 * ME) / QE
        out.append((energy, k, kappa, n % 2 == 0))
        n += 1
    return out


def finite_psi(xs, k, kappa, even):
    inside = np.abs(xs) <= A / 2
    psi = np.zeros_like(xs)
    if even:
        psi[inside] = np.cos(k * xs[inside])
        edge = np.cos(k * A / 2)
    else:
        psi[inside] = np.sin(k * xs[inside])
        edge = np.sin(k * A / 2)
    out = ~inside
    tail = edge * np.exp(-kappa * (np.abs(xs[out]) - A / 2))
    psi[out] = tail * np.sign(xs[out]) ** (0 if even else 1)
    return psi


def fig_wells():
    fig = plt.figure(figsize=(7.0, 3.1))
    gs = GridSpec(1, 2, wspace=0.26, figure=fig)

    # 左：无限深阱
    ax = fig.add_subplot(gs[0])
    x = np.linspace(-A / 2, A / 2, 700)
    levels = infinite_levels()
    gaps = np.diff(levels).tolist() + [0.42]
    for i, E in enumerate(levels):
        n = i + 1
        psi = np.sin(n * np.pi * (x + A / 2) / A)
        amp = 0.30 * gaps[i]
        y = E + amp * psi
        ax.plot(x * 1e9, y, color=bs.BLUE, lw=1.1)
        ax.plot([-A / 2 * 1e9, A / 2 * 1e9], [E, E], color="#b9c4d1", lw=0.7, ls=(0, (3, 3)))
    top = 1.72
    ax.plot([-A / 2 * 1e9, -A / 2 * 1e9], [0, top], color="#4a5563", lw=1.4)
    ax.plot([A / 2 * 1e9, A / 2 * 1e9], [0, top], color="#4a5563", lw=1.4)
    ax.plot([-1.45, A / 2 * 1e9], [0, 0], color="#4a5563", lw=1.0)
    ax.text(0, top + 0.06, "阱壁无限高", fontsize=7.6, color="#4a5563", ha="center")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-0.05, 1.95)
    ax.set_xlabel("位置（纳米）")
    ax.set_ylabel("能量（电子伏特）")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks(levels)
    ax.set_yticklabels(["$n=%d$" % (i + 1) for i in range(len(levels))], fontsize=7.6,
                       color="#33414f")
    bs.clean(ax, grid_axis="y")

    # 右：有限深阱
    ax2 = fig.add_subplot(gs[1])
    for side in (-1, 1):
        ax2.add_patch(plt.Rectangle((0.5 * side, 0), 1.0 * side, V0,
                                    facecolor="#edf1f6", edgecolor="none", zorder=0))
    ax2.plot([-A / 2 * 1e9, -A / 2 * 1e9], [0, V0], color="#4a5563", lw=1.4)
    ax2.plot([A / 2 * 1e9, A / 2 * 1e9], [0, V0], color="#4a5563", lw=1.4)
    ax2.plot([-1.45, -A / 2 * 1e9], [V0, V0], color="#4a5563", lw=1.4)
    ax2.plot([A / 2 * 1e9, 1.45], [V0, V0], color="#4a5563", lw=1.4)
    ax2.plot([-A / 2 * 1e9, A / 2 * 1e9], [0, 0], color="#4a5563", lw=1.0)
    ax2.text(0, 1.05, "阱深 1 电子伏特", fontsize=7.6, color="#4a5563", ha="center")

    xs = np.linspace(-1.45, 1.45, 1600) * 1e-9
    states = finite_states()
    es = [s[0] for s in states]
    gaps = np.diff(es).tolist() + [0.30]
    colors = ["#2b5c94", "#3d7a5a", "#c07a1e", "#6a4b8f"]
    for i, (E, k, kappa, even) in enumerate(states):
        psi = finite_psi(xs, k, kappa, even)
        psi = psi / np.max(np.abs(psi)) * 0.26 * gaps[i]
        ax2.plot(xs * 1e9, E + psi, color=colors[i], lw=1.1)
        ax2.plot([-A / 2 * 1e9, A / 2 * 1e9], [E, E], color="#c6cfd9", lw=0.7, ls=(0, (3, 3)))
    ax2.set_yticks(es)
    ax2.set_yticklabels(["%.2f" % e for e in es], fontsize=7.4, color="#4a5563")
    ax2.set_xlim(-1.45, 1.45)
    ax2.set_ylim(-0.05, 1.22)
    ax2.set_xlabel("位置（纳米）")
    ax2.set_xticks([-1, 0, 1])
    bs.clean(ax2)

    bs.save(fig, CH, "fig01")
    return es


def fig_bands():
    fig = plt.figure(figsize=(7.0, 2.9))
    gs = GridSpec(1, 2, wspace=0.28, figure=fig)

    # 左：紧束缚能带
    ax = fig.add_subplot(gs[0])
    kx = np.linspace(-1, 1, 500)
    E = -2 * np.cos(kx * np.pi)
    ax.plot(kx, E, color=bs.BLUE, lw=1.5)
    ax.axhline(0, color="#c9d2dc", lw=0.7)
    for s in (-1, 1):
        ax.plot([s, s], [-2, 2], color="#b9c4d1", lw=0.8, ls=(0, (3, 3)))
    ax.annotate("", xy=(1.13, 2.0), xytext=(1.13, -2.0),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GREEN, lw=0.9, mutation_scale=7))
    ax.text(1.21, 0, "带宽 $4t$", fontsize=8, color=bs.GREEN, rotation=90, va="center")
    ax.set_xlim(-1.1, 1.55)
    ax.set_ylim(-2.7, 2.7)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["$-\\pi/a$", "0", "$\\pi/a$"])
    ax.set_xlabel("波数 $k$")
    ax.set_ylabel("能量（$t$ 为单位）")
    bs.clean(ax, grid_axis="y")

    # 右：折叠的抛物线在布里渊区边界劈开
    ax2 = fig.add_subplot(gs[1])
    a = 0.4e-9

    def efree(k):
        return (HBAR * k) ** 2 / (2 * ME) / QE

    kk = np.linspace(-np.pi / a, np.pi / a, 900)
    G = np.array([-2 * np.pi / a, 0.0, 2 * np.pi / a])
    es = np.sort(np.array([efree(kk + g) for g in G]), axis=0)
    VG = 0.55
    lower = es[0]
    upper = es[1] + 2 * VG
    ax2.plot(kk * a / np.pi, lower, color=bs.BLUE, lw=1.4)
    ax2.plot(kk * a / np.pi, upper, color=bs.BLUE, lw=1.4)
    e_bound = efree(np.pi / a)
    ax2.annotate("", xy=(1.0, e_bound + 2 * VG), xytext=(1.0, e_bound),
                 arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, mutation_scale=7))
    ax2.text(0.93, e_bound + VG, "带隙\n$2|V_G|$", fontsize=7.6, color=bs.RED,
             ha="right", va="center")
    ax2.axvline(1.0, color="#b9c4d1", lw=0.8, ls=(0, (3, 3)))
    ax2.annotate("下带", xy=(-0.75, 1.32), xytext=(-0.34, 0.52), fontsize=7.8, color=bs.BLUE,
                 ha="center", arrowprops=dict(arrowstyle="-", lw=0.7, color="#8b98a8"))
    ax2.annotate("上带", xy=(0.88, 3.98), xytext=(0.42, 3.02), fontsize=7.8, color=bs.BLUE,
                 ha="center", arrowprops=dict(arrowstyle="-", lw=0.7, color="#8b98a8"))
    ax2.set_xlim(-1.05, 1.05)
    ax2.set_ylim(0, 6.2)
    ax2.set_xticks([-1, 0, 1])
    ax2.set_xticklabels(["$-\\pi/a$", "0", "$\\pi/a$"])
    ax2.set_xlabel("波数 $k$")
    ax2.set_ylabel("能量（电子伏特）")
    bs.clean(ax2, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    print("有限深阱能级：", ["%.3f" % e for e in fig_wells()])
    print("无限深阱能级：", ["%.3f" % e for e in infinite_levels()])
    fig_bands()
