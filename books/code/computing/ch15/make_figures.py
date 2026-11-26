"""第十五章插图：Trotter 误差的阶，以及三条路线的查询次数标度。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

import bookstyle as bs

bs.use("computing")
CH = "15"


def terms(n=4, J=1.0, g=0.8):
    """四比特横场伊辛链，返回哈密顿量的逐项矩阵列表。"""
    dim = 1 << n
    out = []
    for i in range(n - 1):
        M = np.zeros((dim, dim))
        for s in range(dim):
            zi = 1 - 2 * ((s >> i) & 1)
            zj = 1 - 2 * ((s >> (i + 1)) & 1)
            M[s, s] = -J * zi * zj
        out.append(M)
    for i in range(n):
        M = np.zeros((dim, dim))
        for s in range(dim):
            M[s ^ (1 << i), s] = -g
        out.append(M)
    return out


def trotter(n, T):
    dim = 1 << n

    def first(tau):
        M = np.eye(dim, dtype=complex)
        for h in T:
            M = expm(-1j * h * tau) @ M
        return M

    def second(tau):
        M = np.eye(dim, dtype=complex)
        for h in T:
            M = expm(-1j * h * tau / 2) @ M
        for h in reversed(T):
            M = expm(-1j * h * tau / 2) @ M
        return M

    s = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))

    def fourth(tau):
        A = second(s * tau)
        return A @ A @ second((1 - 4 * s) * tau) @ A @ A

    return first, second, fourth


def fig_trotter():
    n = 4
    T = terms(n)
    H = sum(T)
    t = 2.0
    U = expm(-1j * H * t)
    first, second, fourth = trotter(n, T)
    rs = 2 ** np.arange(1, 10)

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    for name, f, color in [("一阶", first, bs.BLUE), ("二阶", second, bs.GREEN), ("四阶", fourth, bs.PURPLE)]:
        errs = []
        for r in rs:
            M = np.eye(1 << n, dtype=complex)
            for _ in range(int(r)):
                M = f(t / r) @ M
            errs.append(np.linalg.norm(M - U, 2))
        ax.loglog(rs, errs, "-o", ms=3.0, lw=1.3, color=color, label=name)
        slope = (np.log(errs[1]) - np.log(errs[-1])) / (np.log(rs[1]) - np.log(rs[-1]))
        print(f"{name}: 斜率 {slope:.2f}, 末误差 {errs[-1]:.2e}")

    ax.set_xlabel("Trotter 步数 $r$")
    ax.set_ylabel(r"$\|U_{\mathrm{exact}}-U_{\mathrm{Trotter}}\|_2$")
    ax.set_xlim(2, 300)
    ax.set_ylim(1e-11, 4)
    ax.legend(loc="lower left", fontsize=8, handlelength=1.8)
    ax.text(0.97, 0.93, "4 比特链，$t=2$，$\\lambda t=12.4$", transform=ax.transAxes,
            fontsize=7.2, color="#6b7785", ha="right")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_scaling():
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0))

    ax = axes[0]
    eps = np.logspace(-3, -10, 60)
    lt = 1e4
    ax.loglog(eps, (lt ** 2) / eps, "-", lw=1.3, color=bs.BLUE, label="一阶 Trotter")
    ax.loglog(eps, (lt ** 1.5) / np.sqrt(eps), "-", lw=1.3, color=bs.GREEN, label="二阶 Trotter")
    ax.loglog(eps, lt + np.log2(1 / eps), "-", lw=1.3, color=bs.RED, label="qubitization")
    ax.set_xlabel(r"目标误差 $\varepsilon$")
    ax.set_ylabel(r"哈密顿量查询次数（$\lambda t=10^{4}$）")
    ax.set_xlim(1e-3, 1e-10)
    ax.set_ylim(1e2, 1e18)
    ax.invert_xaxis()
    ax.legend(loc="upper right", fontsize=7.6, handlelength=1.8)
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    lt = np.logspace(2, 6, 60)
    eps = 1e-3
    ax.loglog(lt, (lt ** 2) / eps, "-", lw=1.3, color=bs.BLUE, label="一阶 Trotter")
    ax.loglog(lt, (lt ** 1.5) / np.sqrt(eps), "-", lw=1.3, color=bs.GREEN, label="二阶 Trotter")
    ax.loglog(lt, lt + np.log2(1 / eps), "-", lw=1.3, color=bs.RED, label="qubitization")
    ax.set_xlabel(r"$\lambda t$")
    ax.set_ylabel(r"哈密顿量查询次数（$\varepsilon=10^{-3}$）")
    ax.set_xlim(1e2, 1e6)
    ax.set_ylim(1e2, 1e16)
    ax.legend(loc="upper left", fontsize=7.6, handlelength=1.8)
    bs.clean(ax, grid_axis="both")

    fig.tight_layout(w_pad=1.2)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_trotter()
    fig_scaling()
