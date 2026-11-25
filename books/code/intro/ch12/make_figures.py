"""第十二章插图：分子体系所需的量子比特数。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("intro")
CH = "12"


def fig_qubits():
    # 最小基组（STO-3G）下的自旋轨道数，等于量子比特数；
    # 数值来自各分子的基组规模，FeMoco 取文献中的活性空间估算。
    mols = ["H2", "LiH", "BeH2", "H2O", "N2", "FeMoco"]
    qubits = [4, 12, 14, 14, 20, 152]
    colors = [bs.BLUE] * 5 + [bs.RED]
    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    bars = ax.bar(range(len(mols)), qubits, width=0.55, color=colors, alpha=0.85,
                  edgecolor="white", linewidth=0.8)
    for i, v in enumerate(qubits):
        ax.text(i, v * 1.1, str(v), ha="center", fontsize=8, color="#33414f")
    ax.set_yscale("log")
    ax.set_ylim(2, 400)
    ax.set_xticks(range(len(mols)))
    ax.set_xticklabels(mols, fontsize=8.6)
    ax.set_ylabel("所需量子比特数")
    ax.axhline(20, color=bs.GRAY, lw=0.8, ls=(0, (4, 3)))
    ax.text(0.05, 22, "当前逻辑比特量级远低于此线", fontsize=7.4, color="#5a6674")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


if __name__ == "__main__":
    fig_qubits()
