"""第二十四章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs
from circuit import Circuit

CH = "24"


def fig_three_qubit():
    fig, ax = plt.subplots(figsize=(7.4, 2.7))
    c = Circuit(ax, 4, 10, labels=[r"$q_0$", r"$q_1$", r"$q_2$", r"$q_a$"])
    c.cnot(0, 0, 1)
    c.cnot(1, 0, 2)
    c.barrier(2.2)
    c.gate(3, 1, "X", color="#f8ecec", edge="#a5675a")
    c.barrier(4)
    c.cnot(5, 0, 1)
    c.cnot(6, 0, 2)
    c.controls(7.8, [1, 2], 3)
    c.measure(9, 3)
    c.annotate(0.5, "编码", dy=0.42, qubit=0)
    c.annotate(3, "错误", dy=0.42, qubit=0)
    c.annotate(5.5, "解码", dy=0.42, qubit=0)
    c.annotate(7.8, "纠错", dy=0.42, qubit=0)
    bs.save(fig, CH, "fig01")


def fig_threshold():
    p = np.logspace(-4, -1.3, 400)
    pth = 1e-2
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    for d, color in [(3, "#9db8d2"), (5, "#5c86ad"), (7, "#2b5c94")]:
        pl = 0.1 * (p / pth) ** ((d + 1) / 2)
        ax.loglog(p, np.clip(pl, 1e-12, 1), color=color, lw=1.5, label=f"码距 $d={d}$")
    ax.axvline(pth, color=bs.RED, lw=0.9, ls=(0, (3, 2)))
    ax.text(pth * 1.06, 3e-9, "阈值", fontsize=8, color=bs.RED)
    ax.set_xlabel("物理错误率 $p$")
    ax.set_ylabel("逻辑错误率 $p_L$")
    ax.set_xlim(1e-4, 5e-2)
    ax.set_ylim(1e-12, 1)
    ax.legend(loc="lower right", handlelength=1.6)
    ax.text(1.1e-4, 2e-2, "物理错误率低于阈值时，\n码距越大，逻辑错误率越低", fontsize=7.6, color="#4a5563")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_three_qubit()
    fig_threshold()
