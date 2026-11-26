"""第 18 章插图：技术炒作曲线与基础设施的时间尺度。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

import bookstyle as bs

bs.use("intro")

CH = "18"


def fig_hype():
    t = np.linspace(2010, 2037, 600)
    knots_t = [2010, 2014, 2018, 2020.5, 2023, 2026, 2030, 2034, 2037]
    knots_y = [0.03, 0.20, 0.72, 1.00, 0.55, 0.38, 0.52, 0.66, 0.70]
    y = PchipInterpolator(knots_t, knots_y)(t)

    fig, ax = plt.subplots(figsize=(6.5, 3.3))
    ax.plot(t, y, color=bs.BLUE, lw=1.8, zorder=4)
    ax.fill_between(t, 0, y, color=bs.BLUE, alpha=0.07, zorder=1)

    edges = [2010, 2013.2, 2019.0, 2024.5, 2029.5, 2037]
    names = ["技术触发", "期望膨胀", "回落", "爬坡", "平台期"]
    for e in edges[1:-1]:
        ax.axvline(e, color="#c3ccd8", lw=0.7, ls=(0, (3, 3)), zorder=2)
    for i, name in enumerate(names):
        mid = (edges[i] + edges[i + 1]) / 2
        ax.text(mid, 1.10, name, fontsize=7.2, color="#6b7785", ha="center")

    marks = [(2026, 0.38, "量子计算", 10, -20, "left"),
             (2031, 0.56, "量子通信", -9, 13, "right"),
             (2035.0, 0.68, "量子测量", 2, -22, "center")]
    for x0, y0, name, dx, dy, ha in marks:
        ax.plot([x0], [y0], "o", ms=4.6, color=bs.RED, mec="white", mew=0.7, zorder=6)
        ax.annotate(name, (x0, y0), textcoords="offset points", xytext=(dx, dy),
                    fontsize=7.6, color="#7a2a1a", ha=ha, zorder=6)

    ax.set_xlim(2010, 2037)
    ax.set_ylim(0, 1.22)
    ax.set_yticks([])
    ax.set_xticks([2010, 2015, 2020, 2025, 2030, 2035])
    ax.set_xlabel("年份")
    ax.set_ylabel("公众期望")
    bs.clean(ax)

    bs.save(fig, CH, "fig01")


def fig_timeline():
    items = [
        ("铁路", 1825, 1870, "45 年"),
        ("电话", 1876, 1920, "44 年"),
        ("电力", 1882, 1935, "53 年"),
        ("半导体", 1947, 1971, "24 年"),
        ("光伏", 1954, 2010, "56 年"),
        ("互联网", 1969, 1995, "26 年"),
        ("移动通信", 1973, 1995, "22 年"),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for i, (name, a, b, lab) in enumerate(items):
        y = len(items) - i
        ax.barh(y, b - a, left=a, height=0.52, color=bs.BLUE, alpha=0.72,
                edgecolor="white", linewidth=0.6)
        ax.text(b + 2.5, y, lab, va="center", fontsize=7.2, color="#4a5563")

    yq = 0
    ax.barh(yq, 2050 - 1994, left=1994, height=0.52, color="none",
            edgecolor=bs.RED, linewidth=1.1, linestyle=(0, (4, 2.5)))
    ax.text(2046, yq + 0.56, "何年到来看不出来", va="center", ha="right",
            fontsize=7.0, color="#7a2a1a")

    ax.axvline(2026, color="#8a95a6", lw=0.8, ls=(0, (2, 3)))
    ax.text(2026.8, len(items) + 0.55, "现在", fontsize=7.2, color="#6b7785")

    ax.set_yticks([len(items) - i for i in range(len(items))] + [0])
    ax.set_yticklabels([n for n, *_ in items] + ["量子计算"], fontsize=8.0)
    ax.set_ylim(-0.75, len(items) + 0.95)
    ax.set_xlim(1818, 2062)
    ax.set_xlabel("年份")
    ax.set_xticks([1820, 1880, 1940, 2000, 2060])
    bs.clean(ax, grid_axis="x")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_hype()
    fig_timeline()
