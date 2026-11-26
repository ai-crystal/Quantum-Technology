"""第 16 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "16"

LAM = 1.55  # 微米


def v_number(a, n1, n2, lam=LAM):
    return 2 * np.pi * a / lam * np.sqrt(n1 ** 2 - n2 ** 2)


def mfd(a, n1, n2):
    v = v_number(a, n1, n2)
    return 2 * a * (0.65 + 1.619 * v ** -1.5 + 2.879 * v ** -6)


def fig_mode():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    a = np.linspace(0.04, 1.05, 500)
    for n1, n2, col, lab in [(3.48, 1.44, bs.BLUE, "硅"),
                             (2.20, 1.44, bs.ORANGE, "薄膜铌酸锂"),
                             (2.00, 1.44, bs.GREEN, "氮化硅")]:
        v = v_number(a, n1, n2)
        m = mfd(a, n1, n2)
        m = np.where(v < 2.405, m, np.nan)
        ax.semilogy(a, m, color=col, lw=1.3, label=lab)
        a_sm = 2.405 * LAM / (2 * np.pi * np.sqrt(n1 ** 2 - n2 ** 2))
        ax.plot(a_sm, mfd(a_sm, n1, n2), "o", color=col, ms=4.0)
    ax.axhline(10.4, color="#8a97a6", lw=0.8, ls=(0, (4, 3)))
    ax.text(0.30, 11.5, "标准单模光纤 10.4 $\\mu$m", fontsize=7.2, color="#4a5563")
    ax.set_xlim(0.04, 1.05)
    ax.set_ylim(0.2, 14)
    ax.set_xlabel(r"芯层半宽 $a$（$\mu$m）")
    ax.set_ylabel(r"模场直径（$\mu$m）")
    ax.legend(loc="center right", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    r = np.linspace(1, 200, 500)
    for loss0, r0, col, lab in [(0.01, 0.65, bs.BLUE, "硅"),
                                (0.01, 2.5, bs.ORANGE, "薄膜铌酸锂"),
                                (0.01, 13.0, bs.GREEN, "氮化硅")]:
        r_ref = {"硅": 5.0, "薄膜铌酸锂": 15.0, "氮化硅": 60.0}[lab]
        ax2.semilogy(r, loss0 * np.exp(-(r - r_ref) / r0), color=col, lw=1.3,
                     label=lab)
    ax2.axhline(0.01, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax2.text(120, 0.012, "0.01 dB", fontsize=7.2, color="#4a5563")
    ax2.set_xlim(1, 200)
    ax2.set_ylim(1e-4, 20)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"弯曲半径（$\mu$m）")
    ax2.set_ylabel("每圈损耗（dB）")
    ax2.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig01")


def fig_coupling():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    dx = np.linspace(0, 4, 400)
    for w, col, lab in [(4.2, bs.BLUE, "光栅耦合器"), (1.2, bs.GREEN, "端面耦合器")]:
        ax.plot(dx, -4.343 * (dx / w) ** 2, color=col, lw=1.3, label=lab)
    ax.axhline(-1.0, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax.text(3.1, -1.9, "1 dB", fontsize=7.2, color="#4a5563")
    ax.axhline(-3.0, color="#8a97a6", lw=0.7, ls=(0, (1, 2)))
    ax.text(3.1, -3.9, "3 dB", fontsize=7.2, color="#4a5563")
    ax.set_xlim(0, 4)
    ax.set_ylim(-14, 0)
    ax.set_xlabel(r"横向失准（$\mu$m）")
    ax.set_ylabel("耦合效率（dB）")
    ax.legend(loc="lower left", fontsize=7.4)
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    lam = np.linspace(1480, 1620, 500)
    ax2.plot(lam, -4.343 * (lam - 1550) ** 2 / (2 * 25.0 ** 2), color=bs.BLUE,
             lw=1.3, label="光栅耦合器")
    ax2.plot(lam, -4.343 * (lam - 1550) ** 2 / (2 * 160.0 ** 2), color=bs.GREEN,
             lw=1.3, label="端面耦合器")
    ax2.axhline(-1.0, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax2.text(1484, -2.5, "1 dB", fontsize=7.2, color="#4a5563")
    ax2.set_xlim(1480, 1620)
    ax2.set_ylim(-6, 0.4)
    ax2.set_xlabel("波长（nm）")
    ax2.set_ylabel("耦合效率（dB）")
    ax2.legend(loc="lower center", fontsize=7.4)
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_mode()
    fig_coupling()
