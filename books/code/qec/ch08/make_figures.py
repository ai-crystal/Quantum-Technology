"""第八章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.special import eval_genlaguerre, gammaln, erfc

import bookstyle as bs

bs.use("qec")

CH = "08"

A = 2 * np.sqrt(np.pi)


def gkp_field(q, p, sigma=0.115, span=2):
    out = np.zeros_like(q)
    for k in range(-span, span + 1):
        for l in range(-span, span + 1):
            out += np.exp(-((q - k * A) ** 2 + (p - l * A) ** 2) / (2 * sigma ** 2))
    return out


def fig_gkp():
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.2),
                             gridspec_kw={"width_ratios": [1.0, 1.12], "wspace": 0.26})

    ax = axes[0]
    lim = 5.3
    v = np.linspace(-lim, lim, 620)
    Q, P = np.meshgrid(v, v)
    F = gkp_field(Q, P)
    ax.imshow(F, cmap="YlGnBu", origin="lower", extent=(-lim, lim, -lim, lim),
              vmin=0, vmax=F.max() * 0.45, interpolation="bilinear", zorder=1)
    for m in range(-1, 2):
        ax.axhline(m * A, color="#8a95a1", lw=0.6, ls=(0, (2, 2.5)), zorder=2)
        ax.axvline(m * A, color="#8a95a1", lw=0.6, ls=(0, (2, 2.5)), zorder=2)
    h = A / 2
    ax.add_patch(Rectangle((-h, -h), 2 * h, 2 * h, facecolor="none",
                           edgecolor=bs.RED, lw=1.1, zorder=4))
    ax.annotate("", xy=(0.66 * h, 0.62 * h), xytext=(0.05, 0.05),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.2,
                                shrinkA=2, shrinkB=1), zorder=5)
    ax.text(h * 1.06, h * 1.02, "可纠正范围", fontsize=7.2, color=bs.RED,
            ha="left", va="bottom")
    ax.set_xlabel("$q$（以 $\sqrt{\pi}$ 为单位）")
    ax.set_ylabel("$p$（以 $\sqrt{\pi}$ 为单位）")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([-A, 0, A])
    ax.set_xticklabels(["$-2\sqrt{\pi}$", "0", "$2\sqrt{\pi}$"])
    ax.set_yticks([-A, 0, A])
    ax.set_yticklabels(["$-2\sqrt{\pi}$", "0", "$2\sqrt{\pi}$"])
    ax.tick_params(labelsize=7.6)
    bs.clean(ax)
    ax.text(-lim * 0.95, lim * 0.92, "(a)", fontsize=10, color="#33414f")

    ax = axes[1]
    sig = np.linspace(0.14, 1.0, 600)
    p_l = 2 * erfc(1.0 / (np.sqrt(2) * sig))
    ax.semilogy(sig, p_l, color=bs.BLUE, lw=1.6)
    ax.axhline(1e-3, color=bs.GRAY, lw=0.8, ls=(0, (4, 3)))
    ax.text(0.60, 1.6e-3, "千分之一", fontsize=7.4, color=bs.GRAY)
    ax.set_xlabel("位移噪声的标准差 $\sigma$（以 $\sqrt{\pi}$ 为单位）")
    ax.set_ylabel("逻辑错误率")
    ax.set_xlim(0.14, 1.0)
    ax.set_ylim(1e-10, 1.0)
    ax.set_yticks([1e-8, 1e-6, 1e-4, 1e-2, 1])
    bs.clean(ax, grid_axis="y")
    ax.text(0.17, 0.32, "(b)", fontsize=10, color=bs.INK)

    bs.save(fig, CH, "fig01")


def coherent(alpha, N):
    n = np.arange(N)
    lg = gammaln(n + 1)
    return alpha ** n * np.exp(-abs(alpha) ** 2 / 2) / np.sqrt(np.exp(lg))


def wigner(rho):
    """按 |n><m| 的 Wigner 函数逐项求和，alpha=(q+ip)/sqrt2 无量纲。"""
    N = rho.shape[0]
    lim = 4.0
    v = np.linspace(-lim, lim, 200)
    X, Y = np.meshgrid(v, v)
    alpha = (X + 1j * Y) / np.sqrt(2)
    two_a2 = 2 * np.abs(alpha) ** 2
    W = np.zeros(X.shape, dtype=complex)
    for n in range(N):
        for m in range(n, N):
            c = rho[n, m]
            if abs(c) < 1e-13:
                continue
            d = m - n
            base = (2 / np.pi) * np.exp(-two_a2) * np.sqrt(np.exp(gammaln(n + 1) - gammaln(m + 1)))
            val = base * (2 * np.conj(alpha)) ** d * eval_genlaguerre(n, d, 2 * two_a2) * (-1) ** n
            W += c * val
            if m != n:
                W += rho[m, n] * np.conj(val)
    return X, Y, W.real


def cat_density(alpha, N):
    psi = np.zeros(N, dtype=complex)
    for k in range(4):
        psi += coherent(alpha * np.exp(1j * k * np.pi / 2), N)
    psi /= np.linalg.norm(psi)
    return np.outer(psi, psi.conj())


def loss(rho, eta, N, kmax=36):
    a = np.diag(np.sqrt(np.arange(1, N)), 1).astype(complex)
    damp = np.diag(eta ** (np.arange(N) / 2.0))
    out = np.zeros_like(rho)
    ak = np.eye(N, dtype=complex)
    for k in range(kmax):
        coef = (1 - eta) ** k / np.exp(gammaln(k + 1))
        M = damp @ ak
        out += coef * (M @ rho @ M.conj().T)
        ak = a @ ak
    return out


def fig_cat():
    N = 54
    alpha = 1.6
    rho = cat_density(alpha, N)
    rho_l = loss(rho, 0.85, N)

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.3), gridspec_kw={"wspace": 0.26})
    Ws = [wigner(r) for r in (rho, rho_l)]
    lim = 0.42 * max(np.abs(Ws[0][2]).max(), np.abs(Ws[1][2]).max())
    for ax, ((X, Y, W), name) in zip(axes, zip(Ws, ["理想猫态", "损耗 15% 之后"])):
        ax.pcolormesh(X, Y, W, cmap="RdBu_r", vmin=-lim, vmax=lim, shading="auto",
                      rasterized=True)
        ax.set_aspect("equal")
        ax.set_xlim(-2.95, 2.95)
        ax.set_ylim(-2.95, 2.95)
        ax.axhline(0, color="#c9d2dc", lw=0.5, zorder=0)
        ax.axvline(0, color="#c9d2dc", lw=0.5, zorder=0)
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
        ax.tick_params(labelsize=7.4)
        ax.set_xlabel("$x$", fontsize=9)
        ax.set_title(name, fontsize=8.2, pad=3)
    axes[0].set_ylabel("$p$", fontsize=9)
    axes[1].set_yticklabels([])
    bs.save(fig, CH, "fig02", kind="photo")


if __name__ == "__main__":
    fig_gkp()
    fig_cat()
