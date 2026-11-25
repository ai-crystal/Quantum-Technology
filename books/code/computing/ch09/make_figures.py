"""第九章插图：态层析的统计误差、影子层析的样本量。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
CH = "09"

rng = np.random.default_rng(20261125)


def tomo_error(shots, state, trials=400):
    """对若干测量次数，估计三个泡利分量的均方根误差。"""
    r = np.array(state, dtype=float)
    errs = []
    for n in shots:
        # 单个分量的估计方差约为 (1 - <P>^2) / n
        var = (1.0 - r ** 2) / n
        draw = rng.normal(0.0, np.sqrt(var), size=(trials, 3))
        errs.append(np.sqrt(np.mean(draw ** 2)))
    return np.array(errs)


def fig_tomo():
    shots = np.logspace(np.log10(50), np.log10(200000), 24).astype(int)
    cases = [
        ((0.0, 0.0, 1.0), r"纯态 $|0\rangle$", bs.BLUE, "o"),
        ((0.62, -0.32, 0.24), r"混合态 $|\vec r|=0.74$", bs.RED, "s"),
        ((0.0, 0.0, 0.0), r"完全混合态", bs.GREEN, "^"),
    ]
    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    for state, label, color, mk in cases:
        e = tomo_error(shots, state)
        ax.loglog(shots, e, mk + "-", ms=2.8, lw=1.0, color=color, label=label)
    ref = 0.42 / np.sqrt(shots)
    ax.loglog(shots, ref, ls=(0, (4, 3)), lw=0.9, color="#8a97a6")
    ax.text(1.2e5, 0.42 / np.sqrt(1.2e5) * 0.58, r"参考斜率 $1/\sqrt{N}$", fontsize=7.8,
            color="#6b7785", ha="right")
    ax.set_xlabel("每个测量基的重复次数 $N$")
    ax.set_ylabel(r"布洛赫分量的均方根误差")
    ax.set_ylim(6e-4, 0.2)
    ax.legend(loc="lower left", ncol=1, handlelength=2.2)
    ax.text(420, 0.055, "三个分量的误差取平均\n每个点重复 400 次", fontsize=7.6, color="#6b7785")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_shadow():
    n = np.arange(2, 13)
    eps = 0.1
    fig, ax = plt.subplots(figsize=(6.3, 3.1))
    full = 4.0 ** n
    ax.semilogy(n, full, "o-", ms=3.2, lw=1.2, color=bs.RED,
                label=r"完整层析（参数个数 $4^n$）")
    for k, color, mk in [(1, bs.BLUE, "s"), (2, bs.GREEN, "^"), (4, bs.PURPLE, "d")]:
        m = 3.0 ** k / eps ** 2
        ax.semilogy(n, np.full_like(n, m, dtype=float), mk + "--", ms=3.0, lw=0.9,
                    color=color, label=rf"影子层析，$k={k}$ 点关联")
    ax.set_xlabel("比特数 $n$")
    ax.set_ylabel("估计误差 0.1 所需的样本数")
    ax.set_xticks(n)
    ax.set_ylim(10, 3e9)
    ax.legend(loc="upper left", fontsize=7.8, handlelength=2.4)
    ax.annotate("", xy=(11.6, 2.6e7), xytext=(11.6, 1300),
                arrowprops=dict(arrowstyle="<->", color="#6b7785", lw=0.8))
    ax.text(11.3, 3.2e7, "两端相差四个数量级", fontsize=7.6, color="#6b7785", ha="right")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_tomo()
    fig_shadow()
