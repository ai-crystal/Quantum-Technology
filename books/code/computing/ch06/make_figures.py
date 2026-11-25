"""第十五章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
from circuit import Circuit

CH = "06"


def fig_bell_circuit():
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    c = Circuit(ax, 2, 6, labels=[r"$q_0$", r"$q_1$"])
    c.gate(0, 0, "H")
    c.cnot(1, 0, 1)
    c.barrier(2)
    c.measure(3, 0)
    c.measure(3, 1)
    c.annotate(0, "叠加", dy=0.42, qubit=0)
    c.annotate(1, "纠缠", dy=0.42, qubit=0)
    c.annotate(3.0, "测量", dy=0.42, qubit=0)
    bs.save(fig, CH, "fig01")


def fig_rb():
    m = np.arange(0, 60, 2)
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    for err, color, label in [(1e-3, bs.BLUE, "单比特门错误率 $10^{-3}$"),
                              (1e-2, bs.RED, "错误率 $10^{-2}$")]:
        p = 1 - 2 * err
        y = 0.5 * p ** m + 0.5
        ax.semilogy(m, y, "o-", ms=3.0, lw=1.0, color=color, label=label)
    ax.set_xlabel("随机 Clifford 序列长度 $m$")
    ax.set_ylabel("存活概率（对数）")
    ax.set_ylim(0.48, 1.02)
    ax.legend(loc="lower left", handlelength=1.6, fontsize=7.8)
    ax.text(30, 0.62, "曲线的指数衰减率给出平均门错误率", fontsize=7.8, color="#4a5563")
    bs.clean(ax)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bell_circuit()
    fig_rb()
