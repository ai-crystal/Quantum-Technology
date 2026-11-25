"""第六章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("qec")

CH = "06"


def fig_progress():
    d = np.array([3, 5])
    p = np.array([3.03, 1.04]) / 100
    lam = p[0] / p[1]
    dd = np.linspace(3, 7, 100)
    fit = p[0] * lam ** (-(dd - 3) / 2)

    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.semilogy(dd, fit, color=bs.BLUE, lw=1.4, ls=(0, (4, 2)))
    ax.semilogy(d, p, "o", ms=6.5, mfc=bs.BLUE, mec="white", mew=1.1, zorder=4)
    for x, y in zip(d, p):
        ax.annotate(f"{100 * y:.2f}%", xy=(x, y), xytext=(6, 6), textcoords="offset points",
                    fontsize=7.8, color="#33414f")
    ax.set_xlabel("码距 $d$")
    ax.set_ylabel("每周期逻辑错误率")
    ax.set_xlim(2.6, 7.4)
    ax.set_ylim(3e-3, 6e-2)
    ax.set_xticks([3, 4, 5, 6, 7])
    ax.set_yticks([3e-3, 1e-2, 3e-2, 6e-2])
    ax.set_yticklabels(["0.3%", "1%", "3%", "6%"])
    ax.minorticks_off()
    ax.text(3.15, 4.3e-2,
            f"每加 2 个码距，错误率降为 $1/{lam:.2f}$",
            fontsize=7.8, color="#4a5563")
    ax.text(4.05, 5.2e-3,
            "2024 年的器件把这条线\n推到 $d=7$，抑制因子约 2.1",
            fontsize=7.8, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_overhead():
    pth = 6e-3
    p = np.logspace(-4, np.log10(2e-3), 400)
    need = -11.0 / np.log10(p / pth)
    d = 2 * np.ceil((need - 1) / 2) + 1
    qubits = 2 * d ** 2 - 1

    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    ax.semilogx(p, d, color=bs.BLUE, lw=1.6)
    ax.set_xlabel("物理错误率 $p$")
    ax.set_ylabel("所需码距 $d$", color=bs.BLUE)
    ax.set_ylim(0, 95)
    ax.set_yticks([10, 20, 30, 50, 70, 90])
    ax.axvline(1e-3, color=bs.RED, lw=0.9, ls=(0, (3, 2)))
    ax.plot([1e-3], [27], "o", ms=5, color=bs.BLUE, zorder=5)
    ax.annotate("$p=10^{-3}$ 时\n$d=27$，约 1400 个物理比特", xy=(1e-3, 27), xytext=(1.5e-4, 62),
                fontsize=7.6, color="#33414f",
                arrowprops=dict(arrowstyle="-", color="#8f9aa8", lw=0.8))

    ax2 = ax.twinx()
    ax2.semilogx(p, qubits, color=bs.GREEN, lw=1.3, ls=(0, (4, 2)))
    ax2.set_ylabel("每个逻辑比特的物理比特数", color=bs.GREEN)
    ax2.set_ylim(0, 5200)
    ax2.set_yticks([1000, 2000, 3000, 4000, 5000])
    ax2.spines["top"].set_visible(False)
    ax.spines["top"].set_visible(False)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_progress()
    fig_overhead()
