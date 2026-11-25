"""第 7 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "07"

ALPHA = -200.0  # 非谐性，单位 MHz，|2> 在 |1> 以下


def envelope(t, sigma):
    return np.exp(-t ** 2 / (2 * sigma ** 2))


def fig_pulse():
    sigma = 3.6
    t = np.linspace(-11, 11, 2001)
    g = envelope(t, sigma)
    drag = -0.55 * (t / sigma) * g
    square = np.where(np.abs(t) < 2 * sigma, 1.0, 0.0)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw={"wspace": 0.30})
    ax = axes[0]
    ax.plot(t, square, color=bs.GRAY, lw=1.2, ls=(0, (3, 2)), label="方波")
    ax.plot(t, g, color=bs.BLUE, lw=1.4, label="高斯")
    ax.plot(t, np.hypot(g, drag), color=bs.RED, lw=1.4, label="高斯加导数项")
    ax.annotate("陡边带来高频分量", xy=(-2 * sigma, 0.62), xytext=(-10.4, 1.2), ha="left",
                fontsize=7.8, color="#4a5563",
                arrowprops=dict(arrowstyle="-|>", color="#4a5563", lw=0.7,
                                connectionstyle="arc3,rad=-0.18"))
    ax.set_xlim(-11, 11)
    ax.set_ylim(-0.05, 1.26)
    ax.set_xlabel("时间（纳秒）")
    ax.set_ylabel("归一化幅度")
    ax.legend(loc="upper right", handlelength=1.8)
    bs.clean(ax)

    ax = axes[1]
    ax.plot(t, g, color=bs.BLUE, lw=1.4, label="同相分量 $I(t)$")
    ax.plot(t, drag, color=bs.RED, lw=1.3, ls=(0, (5, 2)), label="正交分量 $Q(t)$")
    ax.axhline(0, color="#c9d2dc", lw=0.7)
    ax.axvline(0, color="#c9d2dc", lw=0.7)
    ax.set_xlim(-11, 11)
    ax.set_ylim(-0.62, 1.2)
    ax.set_xlabel("时间（纳秒）")
    ax.set_ylabel("归一化幅度")
    ax.annotate(r"$Q\propto \dfrac{dI}{dt}$", xy=(-2.6, -0.42), fontsize=9.5, color=bs.RED)
    ax.legend(loc="upper right", handlelength=2.0)
    bs.clean(ax)
    bs.save(fig, CH, "fig01")


def n_thermal(temp, freq_ghz=6.0):
    h = 6.62607015e-34
    kB = 1.380649e-23
    x = h * freq_ghz * 1e9 / (kB * temp)
    return 1.0 / (np.expm1(x))


def fig_cold_chain():
    stages = [300.0, 50.0, 4.0, 0.8, 0.1, 0.01]
    labels = ["室温\n300 K", "50 K 板", "4 K 板", "0.8 K 板", "100 mK 板", "10 mK 板"]
    att_db = [0.0, 20.0, 20.0, 10.0, 10.0, 6.0]

    n = np.zeros(len(stages))
    n[0] = n_thermal(stages[0])
    for i in range(1, len(stages)):
        gain = 10 ** (-att_db[i] / 10)
        n[i] = n[i - 1] * gain + n_thermal(stages[i]) * (1 - gain)

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    x = np.arange(len(stages))
    ax.semilogy(x, n, color=bs.BLUE, lw=1.4, marker="o", ms=3.6, mfc="white", mew=1.0)
    ax.fill_between(x, n, 1e-6, color=bs.BLUE, alpha=0.06)

    for i in range(len(stages)):
        y = n[i]
        txt = f"{y:.3g}" if y >= 1e-3 else f"{y:.1e}"
        ax.annotate(txt, (x[i], y), textcoords="offset points", xytext=(0, 10),
                    fontsize=7.8, color="#2b5c94", ha="center")
        if att_db[i] > 0:
            ax.annotate(f"−{att_db[i]:.0f} dB", ((x[i - 1] + x[i]) / 2, np.sqrt(n[i - 1] * n[i])),
                        textcoords="offset points", xytext=(0, 12), fontsize=7.4,
                        color="#6b7785", ha="center")

    ax.axhline(0.05, color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(-0.18, 0.032, "0.05 光子", fontsize=7.6, color=bs.RED, va="top", ha="left")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.6)
    ax.set_xlim(-0.28, len(stages) - 0.58)
    ax.set_ylim(8e-4, 4e4)
    ax.set_ylabel("折算到芯片端的热光子数")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_pulse()
    fig_cold_chain()
