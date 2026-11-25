"""第 12 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "12"

C = 2.99792458e8
H = 6.62607015e-34
HBAR = 1.054571817e-34
KB = 1.380649e-23

LAM0 = 780e-9
GAMMA = 2 * np.pi * 6.07e6
ER_KB = 0.096e-6      # 反冲温度，开尔文


def detuning(lam):
    return 2 * np.pi * C * (1 / LAM0 - 1 / lam)


def depth(P, w0, lam):
    w0f = 2 * np.pi * C / LAM0
    A = 3 * np.pi * C ** 2 * GAMMA / (2 * w0f ** 3 * detuning(lam))
    I = 2 * P / (np.pi * w0 ** 2)
    return A * I / KB


def heating(depth_k, lam):
    rate = (depth_k * KB / HBAR) * GAMMA / detuning(lam)
    return rate * 2 * ER_KB * 1e6


def fig_tweezer():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"wspace": 0.30})

    ax = axes[0]
    w0 = np.linspace(0.5e-6, 3.0e-6, 300)
    for P, c in ((2e-3, bs.BLUE), (10e-3, bs.ORANGE), (50e-3, bs.RED)):
        ax.plot(w0 * 1e6, depth(P, w0, 1064e-9) * 1e3, color=c, lw=1.4,
                label=f"{P * 1e3:.0f} mW")
    ax.set_xlabel("束腰 $w_0$（µm）")
    ax.set_ylabel("阱深（mK）")
    ax.set_yscale("log")
    ax.set_xlim(0.5, 3.0)
    ax.set_ylim(3e-3, 3e1)
    ax.legend(loc="upper right", fontsize=7.4, handlelength=1.6, title="1064 nm", title_fontsize=7.2)
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    d = np.linspace(0.03e-3, 3e-3, 300)
    for lam, name, c in ((852e-9, "852 nm", bs.GREEN), (1064e-9, "1064 nm", bs.ORANGE),
                         (1560e-9, "1560 nm", bs.BLUE)):
        ax.plot(d * 1e3, heating(d, lam), color=c, lw=1.4, label=name)
    ax.set_xlabel("阱深（mK）")
    ax.set_ylabel("加热率（µK/s）")
    ax.set_xlim(0, 3.0)
    ax.set_ylim(0, 16)
    ax.legend(loc="upper left", fontsize=7.4, handlelength=1.6)
    ax.text(2.05, 3.2, "失谐越小\n散射越强", fontsize=7.2, color="#6b7785", ha="center")
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig02")


def fig_vacuum():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"wspace": 0.30})

    ax = axes[0]
    t = np.logspace(0, 6, 400)
    p_unbaked = np.maximum(3e-7 * 200 / (t + 200), 3e-9)
    p_baked = 6e-12 + 4e-10 * (1 + t / 300.0) ** -1.0
    ax.loglog(t, p_unbaked, color=bs.GRAY, lw=1.4, ls=(0, (5, 2)), label="未烘烤")
    ax.loglog(t, p_baked, color=bs.BLUE, lw=1.5, label="200 ℃ 烘烤 48 小时")
    ax.axhline(1e-11, color=bs.RED, lw=0.9, ls=(0, (4, 3)))
    ax.text(1.6, 1.25e-11, "离子阱工作压力", fontsize=7.2, color=bs.RED, va="bottom")

    ax.set_xlabel("抽气时间（s）")
    ax.set_ylabel("压力（mbar）")
    ax.set_xlim(1, 1e6)
    ax.set_ylim(1e-12, 1e-6)
    ax.legend(loc="upper right", fontsize=7.4, handlelength=1.8)
    bs.clean(ax, grid_axis="both")

    ax = axes[1]
    p_mbar = np.logspace(-6, -12, 300)
    n = p_mbar * 100.0 / (KB * 300.0)
    sigma = 1e-18
    v = 300.0
    tau = 1.0 / (n * sigma * v)
    ax.loglog(p_mbar, tau, color=bs.BLUE, lw=1.5)
    for pp in (1e-9, 1e-11):
        nn = pp * 100.0 / (KB * 300.0)
        tt = 1.0 / (nn * sigma * v)
        ax.plot([pp], [tt], marker="o", ms=4.0, mfc="white", mew=1.1, color=bs.RED, zorder=4)
    ax.annotate("两分钟", xy=(1e-9, 1.4e2), textcoords="offset points", xytext=(-8, 12),
                fontsize=7.2, color=bs.RED, ha="right")
    ax.annotate("四小时", xy=(1e-11, 1.0 / (1e-11 * 100 / (KB * 300) * sigma * v)),
                textcoords="offset points", xytext=(10, -14), fontsize=7.2, color=bs.RED,
                ha="left")
    ax.set_xlabel("背景气体压力（mbar）")
    ax.set_ylabel("离子寿命（s）")
    ax.set_xlim(1e-6, 1e-12)
    ax.set_ylim(1e-2, 1e6)
    bs.clean(ax, grid_axis="both")

    bs.save(fig, CH, "fig01")


if __name__ == "__main__":
    fig_tweezer()
    fig_vacuum()
