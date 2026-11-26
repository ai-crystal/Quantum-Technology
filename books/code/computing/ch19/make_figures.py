"""第十九章插图：工具链的层次、GHZ 态保真度随两比特门错误率的下降。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.sparse import csr_matrix

import bookstyle as bs

bs.use("computing")
CH = "19"


def box(ax, x, y, w, h, text, fc="#eaf1f9", ec="#4a6f9c", fs=8.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, lw=1.0, zorder=3))
    ax.text(x, y, text, fontsize=fs, ha="center", va="center", zorder=4, linespacing=1.5)


def arrow(ax, p0, p1):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10,
                                 color="#6b7785", lw=1.0, shrinkA=2, shrinkB=2))


def fig_stack():
    fig, ax = plt.subplots(figsize=(6.4, 3.15))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    box(ax, 2.85, 6.3, 2.45, 0.72, "Qiskit", fs=8.4)
    box(ax, 5.6, 6.3, 2.45, 0.72, "Cirq", fs=8.4)
    box(ax, 8.35, 6.3, 2.65, 0.72, "Quil / QASM 3", fs=8.2)
    ax.text(0.12, 6.3, "线路", fontsize=7.2, color="#6b7785", ha="left", va="center")

    box(ax, 5.0, 4.9, 7.4, 0.78, "转译：门分解、比特映射、路由、优化级别", fc="#eef3ee", ec="#5f7d5f")
    for x in (2.85, 5.6, 8.35):
        arrow(ax, (x, 5.93), (x * 0.55 + 2.3, 5.31))

    box(ax, 2.55, 3.1, 3.6, 0.95, "模拟器\n态矢量 / 密度矩阵 / 稳定子 / MPS", fc="#f6f1e6", ec="#8a7a55", fs=7.8)
    box(ax, 7.35, 3.1, 3.6, 0.95, "硬件后端\nISA 指令、调度、脉冲波形", fc="#f6f1e6", ec="#8a7a55", fs=7.8)
    arrow(ax, (3.9, 4.5), (2.9, 3.62))
    arrow(ax, (6.2, 4.5), (7.1, 3.62))

    box(ax, 5.0, 1.55, 6.2, 0.8, "云端服务：排队、批处理、校准数据", fc="#f4f1f8", ec="#7a6396")
    arrow(ax, (2.55, 2.61), (3.4, 1.99))
    arrow(ax, (7.35, 2.61), (6.6, 1.99))

    box(ax, 5.0, 0.42, 6.2, 0.68, "结果：计数、期望值、误差棒", fc="#f8fafc", ec="#6b7785")
    arrow(ax, (5.0, 1.13), (5.0, 0.78))

    ax.text(0.15, 3.1, "执行", fontsize=7.4, color="#6b7785", ha="left", va="center")
    ax.text(0.15, 0.42, "取回", fontsize=7.4, color="#6b7785", ha="left", va="center")
    bs.save(fig, CH, "fig01")


def pauli_maps(n, a, b):
    """两个比特上 15 个非恒等泡利串：返回 (索引重排, 符号向量)。"""
    dim = 1 << n
    idx = np.arange(dim)
    maps = []
    for p1 in range(4):
        for p2 in range(4):
            if p1 == 0 and p2 == 0:
                continue
            perm = idx.copy()
            sign = np.ones(dim, dtype=complex)
            for q, code in ((a, p1), (b, p2)):
                bit = (perm >> q) & 1
                if code == 1:
                    perm = perm ^ (1 << q)
                elif code == 2:
                    perm = perm ^ (1 << q)
                    sign = sign * np.where(bit == 0, 1j, -1j)
                elif code == 3:
                    sign = sign * np.where(bit == 0, 1.0, -1.0)
            maps.append((perm, sign))
    return maps


def cnot_mat(n, c, t):
    dim = 1 << n
    M = np.zeros((dim, dim))
    for s in range(dim):
        M[s, s if not ((s >> c) & 1) else s ^ (1 << t)] = 1.0
    return M


def hadamard0(n):
    dim = 1 << n
    M = np.zeros((dim, dim))
    for s in range(dim):
        if (s >> 0) & 1 == 0:
            M[s, s] = 1 / np.sqrt(2)
            M[s ^ 1, s] = 1 / np.sqrt(2)
    return M


def ghz(n):
    psi = np.zeros(1 << n)
    psi[0] = 1 / np.sqrt(2)
    psi[-1] = 1 / np.sqrt(2)
    return psi


def fig_ghz():
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ps = np.logspace(-4, -1, 19)
    for n, color in [(4, bs.GREEN), (6, bs.BLUE), (8, bs.RED)]:
        dim = 1 << n
        H0 = hadamard0(n)
        rho0 = np.zeros((dim, dim), dtype=complex)
        rho0[0, 0] = 1.0
        g = ghz(n)
        fid = []
        for p in ps:
            rho = H0 @ rho0 @ H0.T
            for q in range(1, n):
                M = cnot_mat(n, 0, q)
                rho = M @ rho @ M.T
                rho = (1 - p) * rho
                acc = np.zeros_like(rho)
                for perm, sign in pauli_maps(n, 0, q):
                    acc += np.outer(sign, sign.conj()) * rho[np.ix_(perm, perm)]
                rho = rho + (p / 15.0) * acc
            fid.append(float(np.real(g @ rho @ g)))
        ax.semilogx(ps, fid, "-", lw=1.4, color=color, label=rf"$n={n}$")
        print(f"n={n}: p=1e-3 保真度 {fid[9]:.3f}, p=1e-2 保真度 {fid[15]:.3f}, p=1e-4 {fid[0]:.3f}")

    ax.set_xlabel("两比特门错误率 $p$")
    ax.set_ylabel("GHZ 态保真度")
    ax.set_xlim(1e-4, 1e-1)
    ax.set_ylim(0.25, 1.02)
    ax.legend(loc="lower left", fontsize=7.6, handlelength=1.8)
    ax.text(0.97, 0.07, "去极化噪声，每个 CNOT 后施加", transform=ax.transAxes,
            fontsize=6.9, color="#6b7785", ha="right")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_stack()
    fig_ghz()
