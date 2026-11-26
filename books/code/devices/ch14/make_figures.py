"""第 14 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from scipy.special import gammaln

import bookstyle as bs

bs.use("devices")

CH = "14"


def spectrum(EJ, EC, EL, phiext, span=3.4 * np.pi, N=9000, nev=4):
    """一维相位方程数值对角化，能级单位 GHz。"""
    phi = np.linspace(-span, span, N)
    d = phi[1] - phi[0]
    U = -EJ * np.cos(phi - phiext) + 0.5 * EL * phi ** 2
    K = -4.0 * EC / d ** 2
    w, v = eigh_tridiagonal(-2.0 * K + U, K * np.ones(N - 1),
                            select="i", select_range=(0, nev - 1))
    return phi, U, w, v


def f01(EJ, EC, EL, phiext, span=3.4 * np.pi, N=9000):
    phi = np.linspace(-span, span, N)
    d = phi[1] - phi[0]
    U = -EJ * np.cos(phi - phiext) + 0.5 * EL * phi ** 2
    K = -4.0 * EC / d ** 2
    w, _ = eigh_tridiagonal(-2.0 * K + U, K * np.ones(N - 1),
                            select="i", select_range=(0, 1))
    return w[1] - w[0]


def charge_dispersion(ratio):
    """Koch 2007 的电荷色散公式，返回 |eps_1|/E01。"""
    eps = 2.0 ** 9 / np.sqrt(np.pi / 2) * ratio ** 1.25 * np.exp(-np.sqrt(8 * ratio))
    e01 = np.sqrt(8 * ratio) - 1.0
    return eps / e01


def fig_potential():
    phi, U, w, v = spectrum(8.5, 1.0, 0.5, np.pi)
    fig = plt.figure(figsize=(7.0, 2.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.34)

    ax = fig.add_subplot(gs[0, 0])
    ax.plot(phi, U, color=bs.INK, lw=1.2)
    labels = {0: r"$|0\rangle$ 与 $|1\rangle$", 2: r"$|2\rangle$ 与 $|3\rangle$"}
    for n in range(4):
        y = w[n]
        amp = 1.2 * np.abs(v[:, n]) ** 2 / np.abs(v[:, n]).max() ** 2
        col = bs.BLUE if n < 2 else bs.RED
        ax.plot(phi, y + amp, color=col, lw=1.0)
        if n in labels:
            ax.plot([-1.55 * np.pi, 1.6 * np.pi], [y, y], color=col, lw=0.6,
                    ls=(0, (4, 3)))
            ax.text(0.35 * np.pi, y - 1.5, labels[n], fontsize=7.8, color=col)
    ax.set_xlim(-1.55 * np.pi, 1.6 * np.pi)
    ax.set_ylim(-8.5, 9.5)
    ax.set_xticks([-np.pi, 0, np.pi])
    ax.set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
    ax.set_xlabel(r"相位 $\varphi$")
    ax.set_ylabel("能量（GHz）")
    bs.clean(ax)

    ax2 = fig.add_subplot(gs[0, 1])
    r = np.logspace(np.log10(10), np.log10(300), 300)
    ax2.loglog(r, charge_dispersion(r), color=bs.RED, lw=1.3, label="电荷色散")
    ax2.loglog(r, 1.0 / (np.sqrt(8 * r) - 1), color=bs.BLUE, lw=1.3,
               label="相对非谐性")
    for x, lab in [(10, "早期器件"), (50, "transmon"), (200, "高比值")]:
        ax2.axvline(x, color="#c9d2dc", lw=0.7, ls=(0, (3, 3)), zorder=0)
        ax2.text(x * 1.07, 2e-8, lab, fontsize=7.2, rotation=90, color="#4a5563",
                 va="bottom", ha="left")
    ax2.set_xlim(10, 300)
    ax2.set_ylim(1e-8, 1.0)
    ax2.set_xlabel(r"$E_J/E_C$")
    ax2.set_ylabel("占跃迁频率的比例")
    ax2.legend(loc="lower left", fontsize=7.6)
    bs.clean(ax2, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_flux_dispersion():
    fig = plt.figure(figsize=(7.0, 2.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.36)

    ax = fig.add_subplot(gs[0, 0])
    flux = np.linspace(0, 1, 90)
    for EJ, col, lab in [(3.0, bs.RED, "3"), (8.5, bs.BLUE, "8.5"), (16.0, bs.GREEN, "16")]:
        y = np.array([f01(EJ, 1.0, 0.5, f * np.pi, N=5000) for f in flux])
        ax.semilogy(flux, y, color=col, lw=1.3, label=r"$E_J/h=%s$ GHz" % lab)
    ax.set_xlim(0, 1)
    ax.set_ylim(5e-4, 20)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel(r"归一化磁通 $\Phi/\Phi_0$")
    ax.set_ylabel("跃迁频率（GHz）")
    ax.legend(loc="lower left", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    fam = [
        ("库珀对盒", 4.0, 5e-3, 5e-2, bs.GRAY, "right"),
        ("相位比特", 1.0, 3e-2, 3e-1, bs.ORANGE, "right"),
        ("磁通比特", 1.5, 1.0, 10.0, bs.RED, "right"),
        ("transmon", 0.2, 60.0, 350.0, bs.BLUE, "left"),
        ("fluxonium", 5.0, 20.0, 120.0, bs.GREEN, "left"),
    ]
    for name, alpha, t_lo, t_hi, col, side in fam:
        ax2.plot([t_lo, t_hi], [alpha, alpha], color=col, lw=1.6, alpha=0.5,
                 solid_capstyle="round")
        ax2.plot(np.sqrt(t_lo * t_hi), alpha, "o", color=col, ms=5.0, zorder=3)
        if side == "right":
            ax2.text(t_hi * 1.4, alpha, name, fontsize=7.6, color=col, va="center",
                     ha="left")
        else:
            ax2.text(t_lo * 0.68, alpha, name, fontsize=7.6, color=col, va="center",
                     ha="right")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(1e-3, 2e3)
    ax2.set_ylim(0.1, 9)
    ax2.set_yticks([0.2, 0.5, 1, 2, 5])
    ax2.set_yticklabels(["0.2", "0.5", "1", "2", "5"])
    ax2.yaxis.set_minor_formatter(plt.NullFormatter())
    ax2.set_xlabel(r"相干时间（$\mu$s）")
    ax2.set_ylabel(r"非谐性 $\alpha/h$（GHz）")
    bs.clean(ax2, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_potential()
    fig_flux_dispersion()
