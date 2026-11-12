"""第二十章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "20"


def fig_dressed():
    delta = np.linspace(-4, 4, 800)
    g = 1.0
    Ep = delta / 2 + np.sqrt(delta ** 2 / 4 + g ** 2)
    Em = delta / 2 - np.sqrt(delta ** 2 / 4 + g ** 2)
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.plot(delta, Ep, color=bs.BLUE, lw=1.5, label=r"$|+\rangle$ 缀饰态")
    ax.plot(delta, Em, color=bs.RED, lw=1.5, label=r"$|-\rangle$ 缀饰态")
    ax.plot(delta, delta, color="#c3ccd6", lw=0.8, ls=(0, (3, 3)))
    ax.axhline(0, color="#c3ccd6", lw=0.8, ls=(0, (3, 3)))
    ax.annotate("", xy=(0, g), xytext=(0, -g),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.GREEN, lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(0.16, 0, r"$2g$", fontsize=9, color=bs.GREEN, va="center")
    ax.set_xlabel(r"失谐 $\Delta = \omega_a - \omega_c$（单位 $g$）")
    ax.set_ylabel("能量（单位 $g$）")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4.2, 4.2)
    ax.legend(loc="upper left", handlelength=1.4)
    ax.text(1.4, -3.6, "失谐大时，能级趋于原子与腔的裸态", fontsize=7.6, color="#6b7785")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def fig_vacuum_rabi():
    w = np.linspace(-3, 3, 1200)
    kappa = 0.22
    lor = lambda x, x0: (1 / np.pi) * (kappa / 2) / ((x - x0) ** 2 + (kappa / 2) ** 2)
    empty = lor(w, 0)
    split = 0.55 * lor(w, -1) + 0.55 * lor(w, 1)
    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    ax.plot(w, empty / empty.max(), color=bs.GRAY, lw=1.2, ls=(0, (4, 3)), label="腔内无原子")
    ax.plot(w, split / split.max(), color=bs.BLUE, lw=1.5, label="原子与腔强耦合")
    ax.annotate("", xy=(1, 0.62), xytext=(-1, 0.62),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.RED, lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(0, 0.66, r"$2g$", fontsize=9, color=bs.RED, ha="center")
    ax.set_xlabel(r"探测频率（以耦合强度为单位）")
    ax.set_ylabel("归一化透射")
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 1.08)
    ax.legend(loc="upper right", handlelength=1.8)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_dressed()
    fig_vacuum_rabi()
