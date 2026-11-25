"""第十七章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
from circuit import Circuit

CH = "08"


def fig_qft():
    fig, ax = plt.subplots(figsize=(7.0, 2.4))
    c = Circuit(ax, 3, 7, labels=[r"$q_0$", r"$q_1$", r"$q_2$"])
    c.gate(0, 0, "H")
    c.cphase(1, 1, 0, r"$\pi/2$")
    c.cphase(2, 2, 0, r"$\pi/4$")
    c.gate(3, 1, "H")
    c.cphase(4, 2, 1, r"$\pi/2$")
    c.gate(5, 2, "H")
    c.swap(6, 0, 2)
    c.annotate(0.3, "逐位处理", dy=0.40, qubit=0)
    c.annotate(6, "交换输出顺序", dy=0.40, qubit=0)
    bs.save(fig, CH, "fig01")


def fig_phase_est():
    phi = 0.3
    n = 5
    N = 2 ** n
    k = np.arange(N)
    amp = np.exp(2j * np.pi * k * phi) * np.exp(-2j * np.pi * k * k / N * 0)  # 相位
    # 有限精度下的分布：Dirichlet 核
    with np.errstate(divide="ignore", invalid="ignore"):
        num = 1 - np.exp(2j * np.pi * (phi - k / N) * N)
        den = 1 - np.exp(2j * np.pi * (phi - k / N))
        p = np.where(np.abs(den) < 1e-12, 1.0, np.abs(num / (N * den)) ** 2)
    fig, ax = plt.subplots(figsize=(6.2, 2.7))
    ax.bar(k, p, width=0.8, color="#9db8d2", edgecolor="#5c7f9f", linewidth=0.4)
    ax.axvline(phi * N, color=bs.RED, lw=0.9, ls=(0, (3, 2)))
    ax.text(phi * N + 0.5, 0.55, r"真实相位 $\varphi = 0.3$", fontsize=8, color=bs.RED)
    ax.axvline(round(phi * N), color=bs.GREEN, lw=0.9, ls=(0, (3, 2)))
    ax.text(round(phi * N) - 0.5, 0.28, "最可能的读数", fontsize=8, color=bs.GREEN, ha="right")
    ax.set_xlabel(r"测量结果 $k$（共 $2^n$ 个取值，$n = 5$）")
    ax.set_ylabel("概率")
    ax.set_xlim(-0.6, N - 0.4)
    ax.set_ylim(0, 0.72)
    bs.clean(ax)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_qft()
    fig_phase_est()
