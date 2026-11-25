"""第九章插图：变分算法的迭代流程。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import bookstyle as bs

bs.use("computing")
CH = "09"


def box(ax, x, y, w, h, text, fc="#eaf1f9", ec="#4a6f9c"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, lw=1.0))
    ax.text(x, y, text, fontsize=8.6, color="#1f2a37", ha="center", va="center")


def arrow(ax, p0, p1, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10,
                                 color="#6b7785", lw=1.0,
                                 connectionstyle=f"arc3,rad={rad}"))


def fig_loop():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    box(ax, 5.0, 4.3, 2.6, 0.85, "参数 $\\theta$")
    box(ax, 8.0, 2.6, 2.6, 0.85, "量子线路 $U(\\theta)$")
    box(ax, 5.0, 0.9, 2.6, 0.85, "测量期望值 $\\langle H\\rangle$")
    box(ax, 2.0, 2.6, 2.6, 0.85, "经典优化器", fc="#f5f1e8", ec="#8a7a55")

    arrow(ax, (6.35, 4.15), (7.4, 3.15), rad=-0.15)
    arrow(ax, (7.7, 2.1), (6.3, 1.25), rad=-0.15)
    arrow(ax, (3.7, 1.25), (2.3, 2.1), rad=-0.15)
    arrow(ax, (3.3, 3.05), (4.4, 3.95), rad=-0.15)
    ax.text(5.0, 2.6, "循环", fontsize=9, color="#6b7785", ha="center", va="center")
    bs.save(fig, CH, "fig01")


if __name__ == "__main__":
    fig_loop()
