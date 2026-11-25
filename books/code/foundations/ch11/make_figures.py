"""第十一章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("foundations")

CH = "11"

ME = 9.1093837015e-31
HBAR = 1.054571817e-34
QE = 1.602176634e-19

E0 = 1.0
V0 = 1.2
L = 0.45
K = np.sqrt(2 * ME * E0 * QE) / HBAR * 1e-9
KAP = np.sqrt(2 * ME * (V0 - E0) * QE) / HBAR * 1e-9


def solve_barrier():
    """方势垒两侧与内部的系数，入射振幅取 1。"""
    a = np.exp(KAP * L)
    b = np.exp(-KAP * L)
    ph = np.exp(1j * K * L)
    M = np.array([
        [1.0, -1.0, -1.0, 0.0],
        [-1j * K, -KAP, KAP, 0.0],
        [0.0, a, b, -ph],
        [0.0, KAP * a, -KAP * b, -1j * K * ph],
    ], dtype=complex)
    rhs = np.array([-1.0, -1j * K, 0.0, 0.0], dtype=complex)
    r, A, B, t = np.linalg.solve(M, rhs)
    return r, A, B, t


def fig_barrier():
    r, A, B, t = solve_barrier()
    x = np.linspace(-2.35, 1.55, 2200)

    def psi(xv):
        out = np.empty_like(xv, dtype=complex)
        m1 = xv < 0
        m2 = (xv >= 0) & (xv <= L)
        m3 = xv > L
        out[m1] = np.exp(1j * K * xv[m1]) + r * np.exp(-1j * K * xv[m1])
        out[m2] = A * np.exp(KAP * xv[m2]) + B * np.exp(-KAP * xv[m2])
        out[m3] = t * np.exp(1j * K * xv[m3])
        return out

    y = psi(x)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(6.2, 3.7), sharex=True,
        gridspec_kw={"height_ratios": [1.0, 1.35], "hspace": 0.12})

    ax2.axvspan(0, L, color="#e8edf4", zorder=0)
    ax1.axvspan(0, L, ymin=0, ymax=V0 / 1.65, color="#e8edf4", zorder=0)

    ax1.plot([-2.35, 1.55], [E0, E0], color=bs.RED, lw=1.0, ls=(0, (4, 2.5)))
    ax1.plot([0, L], [V0, V0], color="#4a5563", lw=1.2)
    ax1.plot([0, 0], [0, V0], color="#4a5563", lw=1.2)
    ax1.plot([L, L], [0, V0], color="#4a5563", lw=1.2)
    ax1.text(-0.04, E0 + 0.06, "$E$", fontsize=8.6, ha="right", va="bottom", color=bs.RED)
    ax1.text(L + 0.06, V0 - 0.02, "$V_0$", fontsize=8.6, ha="left", va="center", color="#3a4a5c")
    ax1.set_ylim(0, 1.65)
    ax1.set_yticks([0, 0.5, 1.0])
    ax1.set_ylabel("能量（eV）")
    bs.clean(ax1)

    ax1.text(0.24, 0.42, "禁区", fontsize=8.0, ha="center", va="center", color="#6b7785")

    ax2.plot(x, y.real, color=bs.BLUE, lw=1.2)
    ax2.axhline(0, color="#c2ccd8", lw=0.7)
    ax2.set_ylim(-2.0, 2.0)
    ax2.set_xlim(-2.35, 1.55)
    ax2.set_xlabel("位置 $x$（nm）")
    ax2.set_ylabel(r"$\mathrm{Re}\,\psi$")
    bs.clean(ax2)
    ax2.text(-2.28, 1.55, "入射与反射", fontsize=8.0, color="#4a5563", ha="left")
    ax2.text(0.62, 1.55, "透射", fontsize=8.0, color=bs.BLUE, ha="left")
    ax2.text(0.12, 1.18, "$e^{-\\kappa x}$", fontsize=8.6, color="#4a5563")

    bs.save(fig, CH, "fig01")


def fig_transmission():
    Ls = np.linspace(0.01, 1.6, 700)
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    E = 0.5
    for V, c, name in [(1.0, bs.BLUE, "1.0"), (3.0, bs.ORANGE, "3.0"), (5.0, bs.RED, "5.0")]:
        kap = np.sqrt(2 * ME * (V - E) * QE) / HBAR * 1e-9
        T = 1.0 / (1.0 + V ** 2 * np.sinh(kap * Ls) ** 2 / (4 * E * (V - E)))
        ax.semilogy(Ls, T, color=c, lw=1.3, label=f"$V_0={name}$ eV")

    ax.set_xlim(0, 1.6)
    ax.set_ylim(1e-7, 1.5)
    ax.set_xlabel("势垒宽度 $L$（nm）")
    ax.set_ylabel("透射系数 $T$")
    ax.legend(loc="upper right")
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_barrier()
    fig_transmission()
