"""第十六章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
from circuit import Circuit

CH = "07"


def fig_dj():
    fig, ax = plt.subplots(figsize=(7.0, 2.3))
    c = Circuit(ax, 3, 7, labels=[r"$q_0$", r"$q_1$", r"$q_2$"])
    c.gate(0, 0, "H")
    c.gate(0, 1, "H")
    c.gate(0, 2, "X")
    c.gate(1, 2, "H")
    c.multi(2.5, 0, 2, r"oracle $U_f$", width=0.8, rotate=90)
    c.gate(4, 0, "H")
    c.gate(4, 1, "H")
    c.barrier(5)
    c.measure(5.6, 0)
    c.measure(5.6, 1)
    c.annotate(0.5, "制备叠加", dy=0.40, qubit=0)
    c.annotate(2.5, "一次查询", dy=0.40, qubit=0)
    c.annotate(5.6, "测量输入寄存器", dy=0.40, qubit=0)
    bs.save(fig, CH, "fig01")


def fig_grover():
    N = 1024
    theta = np.arcsin(1 / np.sqrt(N))
    ks = np.arange(0, 40)
    p = np.sin((2 * ks + 1) * theta) ** 2
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.plot(ks, p, "o-", ms=3.4, lw=1.0, color=bs.BLUE)
    kmax = int(np.floor(np.pi / (4 * theta) - 0.5))
    ax.plot([kmax], [p[kmax]], "o", ms=7, mfc="none", mec=bs.RED, mew=1.4)
    ax.annotate(f"最优迭代次数约 {kmax} 次", xy=(kmax, p[kmax]), xytext=(kmax + 2.5, 0.62),
                fontsize=8, color=bs.RED,
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=0.7, connectionstyle="arc3,rad=0.2"))
    ax.set_xlabel("Grover 迭代次数 $k$")
    ax.set_ylabel("找到目标的概率")
    ax.set_xlim(-1, 39)
    ax.set_ylim(0, 1.06)
    ax.text(16, 0.16, r"$N = 1024$，$\theta = \arcsin(1/\sqrt{N})$", fontsize=7.8, color="#4a5563")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_dj()
    fig_grover()
