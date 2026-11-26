"""第十四章插图：MPS 的键维结构、纠缠熵的增长与二维收缩的代价。

模型为一维海森堡链加次近邻耦合（J1=1, J2=0.4），初始态取奈尔态，
淬火后纠缠熵线性增长再饱和，这是非可积模型的典型行为。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

import bookstyle as bs

bs.use("computing")
CH = "14"


def heisenberg(n, J1=1.0, J2=0.4):
    """H = Σ J1 S_i·S_{i+1} + Σ J2 S_i·S_{i+2}。"""
    dim = 1 << n
    idx = np.arange(dim)
    sz = np.array([np.where(((idx >> i) & 1) == 0, 0.5, -0.5) for i in range(n)])
    diag = np.zeros(dim)
    rows, cols, vals = [], [], []

    def bond(i, j, c):
        diag[:] += c * sz[i] * sz[j]
        diff = ((idx >> i) & 1) != ((idx >> j) & 1)
        rows.append(idx[diff])
        cols.append(idx[diff] ^ (1 << i) ^ (1 << j))
        vals.append(np.full(int(diff.sum()), 0.5 * c))

    for i in range(n - 1):
        bond(i, i + 1, J1)
    for i in range(n - 2):
        bond(i, i + 2, J2)
    rows.append(idx)
    cols.append(idx)
    vals.append(diag)
    return csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                      shape=(dim, dim))


def neel(n):
    psi = np.zeros(1 << n)
    for s in range(1 << n):
        bits = [(s >> i) & 1 for i in range(n)]
        if bits[0] == 0 and all(bits[i] != bits[i + 1] for i in range(n - 1)):
            psi[s] = 1.0
    return psi / np.linalg.norm(psi)


def schmidt(psi, n):
    s = np.linalg.svd(psi.reshape(1 << (n // 2), -1), compute_uv=False)
    return np.sort(s ** 2)[::-1]


def entropy(p):
    q = p[p > 1e-14]
    return float(-(q * np.log2(q)).sum())


def fig_mps():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.95),
                             gridspec_kw={"width_ratios": [1.18, 1.0]})

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    n = 5
    xs = np.linspace(2.35, 9.1, n)
    ax.text(0.75, 1.96, r"$|\psi\rangle$", fontsize=10.5, color="#1f2a37", ha="center", va="center")
    ax.text(1.42, 1.96, "=", fontsize=9.5, color="#1f2a37", ha="center", va="center")
    for i, x in enumerate(xs):
        ax.add_patch(FancyBboxPatch((x - 0.38, 1.55), 0.76, 0.82,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor="#eaf1f9", edgecolor="#4a6f9c", lw=1.0, zorder=3))
        ax.text(x, 1.96, rf"$A^{{[{i + 1}]}}$", fontsize=8.0, ha="center", va="center", zorder=4)
        ax.plot([x, x], [2.38, 3.02], color="#5c6b7a", lw=1.0)
        ax.plot([x], [3.09], "o", ms=3.0, color="#5c6b7a")
        ax.text(x, 3.24, r"$d$", fontsize=7.6, color="#5c6b7a", ha="center")
        if i < n - 1:
            ax.plot([x + 0.40, xs[i + 1] - 0.40], [1.96, 1.96], color="#b0703a", lw=1.2)
            ax.text((x + xs[i + 1]) / 2, 2.10, r"$\chi$", fontsize=7.6, color="#b0703a", ha="center")
    ax.text(5.0, 0.72, r"$|\psi\rangle=\sum_{s_1\cdots s_n}A^{[1]}_{s_1}A^{[2]}_{s_2}\cdots A^{[n]}_{s_n}\,|s_1\cdots s_n\rangle$",
            fontsize=8.6, color="#1f2a37", ha="center", va="center")
    ax.text(5.0, 0.12, "竖线是物理指标，横线是键，每条键上留 $\\chi$ 个数", fontsize=7.2,
            color="#6b7785", ha="center", va="center")

    ax = axes[1]
    n = 16
    psi0 = neel(n)
    H = heisenberg(n)
    for t, color, label in [(2, bs.GREEN, "$t=2$"), (5, bs.BLUE, "$t=5$"), (9, bs.RED, "$t=9$")]:
        p = schmidt(expm_multiply(-1j * t * H, psi0), n)
        chi = np.arange(1, len(p) + 1)
        disc = 1.0 - np.cumsum(p)
        ax.loglog(chi, np.maximum(disc, 1e-14), "-", lw=1.3, color=color,
                  label=label + rf"（$S={entropy(p):.1f}$ 比特）")
    ax.set_xlabel("保留的键维 $\\chi$")
    ax.set_ylabel("截断误差 $1-\\sum_{i\\leq\\chi}\\lambda_i^2$")
    ax.set_xlim(1, 400)
    ax.set_ylim(1e-13, 1.2)
    ax.legend(loc="lower left", fontsize=7.0, handlelength=1.5)
    bs.clean(ax, grid_axis="y")

    fig.tight_layout(w_pad=1.0)
    bs.save(fig, CH, "fig01")


def fig_cost():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0))

    ax = axes[0]
    times = np.arange(0, 17)
    for n, color in [(12, bs.GREEN), (14, bs.BLUE), (16, bs.RED), (18, bs.PURPLE)]:
        psi0 = neel(n)
        H = heisenberg(n)
        S = [entropy(schmidt(expm_multiply(-1j * t * H, psi0), n)) for t in times]
        print(f"n={n}: max S={max(S):.2f} at t={times[int(np.argmax(S))]}")
        ax.plot(times, S, "-o", ms=2.4, lw=1.2, color=color, label=rf"$n={n}$")
    ax.set_xlabel("演化时间 $t$（$J_1=1$）")
    ax.set_ylabel("半链纠缠熵 $S$（比特）")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.4)
    ax.legend(loc="lower right", fontsize=7.2, handlelength=1.8, ncol=2, columnspacing=1.0)
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    L = np.arange(2, 15)
    for chi, color in [(4, bs.GREEN), (8, bs.BLUE), (16, bs.PURPLE), (32, bs.ORANGE)]:
        ax.semilogy(L, chi ** (2.0 * L), "-", lw=1.2, color=color, label=rf"$\chi={chi}$")
    ax.axhline(1e24, color="#8a97a6", lw=0.8, ls=(0, (4, 3)))
    ax.text(3.0, 4.5e24, r"百亿亿次超算跑一天（约 $10^{24}$ 次乘加）", fontsize=6.8, color="#6b7785",
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))
    ax.set_xlabel("格点宽度 $L$")
    ax.set_ylabel("收缩所需的乘加次数")
    ax.set_xlim(2, 14)
    ax.set_ylim(1e4, 1e42)
    ax.legend(loc="lower right", fontsize=7.2, handlelength=1.6, ncol=2, columnspacing=1.0)
    bs.clean(ax, grid_axis="y")

    fig.tight_layout(w_pad=1.0)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_mps()
    fig_cost()
