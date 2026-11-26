"""第 16 章插图：工程链与布线瓶颈。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

import bookstyle as bs

bs.use("intro")

CH = "16"


def fig_chain():
    fig = plt.figure(figsize=(6.2, 4.3))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12.6)
    ax.axis("off")

    stages = [
        ("芯片与工艺", "一片能测的芯片", "界面损耗、结的均一性"),
        ("低温制冷", "十毫开尔文的稳定环境", "热负载、氦三供应"),
        ("微波测控", "几百路低噪声脉冲", "通道密度、相位漂移"),
        ("固件与编译", "从线路到脉冲的软件栈", "抽象层与硬件细节的耦合"),
        ("校准与运维", "每天都能用的机器", "参数漂移、值班人力"),
        ("应用与云平台", "可调用、可计费的服务", "找到真正比经典快的任务"),
    ]

    top = 10.9
    step = 1.72
    for i, (name, deliver, hard) in enumerate(stages):
        cy = top - i * step
        ax.add_patch(Rectangle((0.5, cy - 0.52), 3.1, 1.04, facecolor="#e6ecf4",
                               edgecolor="#7d8ea3", lw=0.9, zorder=2))
        ax.text(2.05, cy, name, fontsize=8.6, color="#1f2a37", ha="center",
                va="center", zorder=3)
        ax.text(3.95, cy + 0.10, deliver, fontsize=7.5, color="#25313f",
                ha="left", va="center", zorder=3)
        ax.text(8.55, cy + 0.10, hard, fontsize=7.2, color=bs.RED,
                ha="left", va="center", zorder=3)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((2.05, cy - 0.56), (2.05, cy - step + 0.58),
                                         arrowstyle="-|>", mutation_scale=8,
                                         color="#8a95a6", lw=0.9, zorder=1))

    ax.text(3.95, top + 0.75, "交付物", fontsize=7.4, color="#6b7785")
    ax.text(8.55, top + 0.75, "最难的地方", fontsize=7.4, color=bs.RED)
    ax.text(0.5, 0.30, "上一环的指标是下一环的起点，整体节拍由最慢的一环决定",
            fontsize=7.4, color="#5a6674")

    bs.save(fig, CH, "fig01")


def fig_wiring():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    N = np.logspace(1, 5, 300)
    ax.plot(N, 2 * N, color=bs.BLUE, lw=1.6, label="每比特两根线，共 $2N$")
    ax.axhline(200, color=bs.RED, lw=1.1, ls=(0, (5, 3)))
    ax.text(1.15e1, 2.9e2, "芯片四边最多引出约 200 根", fontsize=7.4,
            color=bs.RED, va="bottom")
    ax.axhline(800, color="#9a8b6a", lw=1.0, ls=(0, (2, 3)))
    ax.text(1.15e1, 1.15e3, "四层堆叠加硅通孔，约 800 根", fontsize=7.4,
            color="#7c6b4a", va="bottom")

    ax.plot([1e2], [2e2], "o", ms=5.2, color=bs.INK, zorder=5)
    ax.annotate("约 100 比特就撞墙", (1e2, 2e2), textcoords="offset points",
                xytext=(8, -22), fontsize=7.6, color="#25313f")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e1, 1e5)
    ax.set_ylim(1e1, 3e6)
    ax.set_xlabel("比特数 $N$")
    ax.set_ylabel("需要引出的线数")
    ax.legend(loc="upper left", handlelength=1.8)
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_chain()
    fig_wiring()
