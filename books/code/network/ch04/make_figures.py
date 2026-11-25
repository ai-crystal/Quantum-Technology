"""第 4 章插图：光纤损耗与透射率、一次卫星过境的链路损耗。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "04"


def fig_fibre():
    L = np.linspace(0, 600, 500)
    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    for alpha, color, name in [(0.2, bs.BLUE, "0.2 dB/km，普通单模光纤"),
                               (0.15, bs.GREEN, "0.15 dB/km，超低损耗光纤")]:
        eta = 10 ** (-alpha * L / 10)
        ax.semilogy(L, eta, color=color, lw=1.6, label=name)

    for km in (100, 200, 400):
        ax.axvline(km, color="#c3ccd6", lw=0.7, ls=(0, (4, 3)), zorder=0)
        ax.text(km + 6, 3e-11, f"{km} km\n{0.2 * km:.0f} dB", fontsize=7.8, color="#4a5563")
    ax.axhline(1e-4, color=bs.RED, lw=0.9, ls=(0, (2, 3)))
    ax.text(8, 1.4e-4, "万分之一", fontsize=7.8, color=bs.RED)

    ax.set_xlim(0, 600)
    ax.set_ylim(1e-12, 2)
    ax.set_xlabel("光纤长度（km）")
    ax.set_ylabel("透射率 $\\eta$")
    ax.legend(loc="upper right")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_pass():
    t = np.linspace(-300, 300, 500)
    el = 10 + 80 * (1 - (t / 300.0) ** 2)  # 度
    zr = np.deg2rad(90 - el)

    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    for h, color, name in [(500.0, bs.BLUE, "轨道高度 500 km"),
                           (1000.0, bs.ORANGE, "轨道高度 1000 km")]:
        d = h / np.sin(np.deg2rad(el))
        eta_diff = np.minimum(1.0, (0.3 * 0.6 / (800e-9 * d * 1e3)) ** 2)
        tau_atm = 0.15 / np.cos(zr)
        loss = -10 * np.log10(eta_diff * np.exp(-tau_atm))
        ax.plot(t, loss, color=color, lw=1.6, label=name)

    ax.axhline(30, color=bs.RED, lw=0.9, ls=(0, (5, 3)))
    ax.text(70, 31.4, "链路损耗 30 dB", fontsize=8, color=bs.RED)
    ax.set_xlim(-300, 300)
    ax.set_ylim(0, 45)
    ax.set_xlabel("过境时间（s）")
    ax.set_ylabel("链路损耗（dB）")
    ax.set_xticks([-300, -200, -100, 0, 100, 200, 300])
    ax.legend(loc="upper center")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_fibre()
    fig_pass()
