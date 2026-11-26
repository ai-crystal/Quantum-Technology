"""第 11 章插图：中继链的端到端速率，以及一次端到端连接的速率预算。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "11"

ALPHA = 0.2      # dB/km
ETA_M = 0.9      # 存储器存取效率
ETA_B = 0.5      # 线性光学贝尔态测量成功率
MODES = 100      # 多模式数
C_FIB = 2.0e8    # 光纤中光速 m/s
NSET = (2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)


def rate_chain(L_km, N, tau, alpha=ALPHA, eta_m=ETA_M, eta_b=ETA_B, modes=MODES):
    """一条 N 段链路的端到端速率（比特每秒）。"""
    L0 = L_km / N
    p0 = eta_m ** 2 * 10.0 ** (-alpha * L0 / 10.0)
    t_rt = 2.0 * L0 * 1e3 / C_FIB
    t_wait = t_rt / (modes * p0) * np.sum(1.0 / np.arange(1, N + 1))
    return eta_b ** (N - 1) * np.exp(-t_wait / tau) / t_wait


def best_rate(L_km, tau):
    return max(rate_chain(L_km, n, tau) for n in NSET)


def fig_distance():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.05),
                             gridspec_kw={"wspace": 0.33})

    taus = [(0.01, bs.RED, "10 ms"), (0.1, bs.ORANGE, "100 ms"),
            (1.0, bs.BLUE, "1 s"), (10.0, bs.GREEN, "10 s")]

    ax = axes[0]
    L = np.linspace(100, 2000, 96)
    lo = np.array([best_rate(x, 0.01) for x in L])
    hi = np.array([best_rate(x, 10.0) for x in L])
    mid = np.array([best_rate(x, 1.0) for x in L])
    ax.fill_between(L, lo, hi, color=bs.BLUE, alpha=0.13, lw=0,
                    label="量子中继，寿命 10 ms 至 10 s")
    ax.semilogy(L, mid, color=bs.BLUE, lw=1.5, label="量子中继，寿命 1 s")
    ax.semilogy(L, 2e3 / (L / 100.0), color="#5b6a7a", lw=1.2, ls=(0, (5, 2)),
                label="可信中继，每跳 2 kbps")
    ax.set_xlabel("端到端距离（km）")
    ax.set_ylabel("成码率（bit/s）")
    ax.set_xlim(100, 2000)
    ax.set_ylim(1e-5, 2e4)
    ax.set_xticks([100, 600, 1100, 1600, 2000])
    ax.legend(loc="lower left", fontsize=6.9, handlelength=1.6, labelspacing=0.32)
    ax.text(1180, 0.35, "量子中继", fontsize=7.4, color=bs.BLUE)
    ax.text(560, 190, "可信中继", fontsize=7.4, color="#4a5563")

    ax = axes[1]
    N = np.array(NSET)
    for tau, color, label in taus:
        y = np.array([rate_chain(1000.0, n, tau) for n in N])
        ax.loglog(N, y, color=color, lw=1.4, marker="o", ms=2.8,
                  label="寿命 " + label)
        j = int(np.argmax(y))
        ax.plot(N[j], y[j], "o", ms=6.5, mfc="none", mew=1.2, color=color)
    ax.set_xlabel("分段数 N（总长 1000 km）")
    ax.set_ylabel("成码率（bit/s）")
    ax.set_xlim(2, 64)
    ax.set_ylim(1e-7, 2e4)
    ax.set_xticks([2, 4, 8, 16, 32, 64])
    ax.set_xticklabels(["2", "4", "8", "16", "32", "64"])
    ax.minorticks_off()
    ax.annotate("交换次数压垮链路", xy=(48, 2e-6), xytext=(10, 3e-5),
                fontsize=7.0, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    ax.text(2.4, 4e3, "空心圈为最优点", fontsize=7.0, color="#4a5563")
    bs.clean(axes[0], grid_axis="y")
    bs.clean(axes[1], grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_budget():
    steps = [8.0e4, 75.4, 0.589, 0.581]
    names = ["每秒基本尝试", "乘每段成功率", "乘七次交换", "乘寿命因子"]
    texts = ["$8.0\\times10^{4}$", "75.4", "0.589", "0.581 bit/s"]
    notes = ["$M\\,c/2L_0$", "$p_0/H_8$", "$(1/2)^7$", "$e^{-T_w/\\tau}$"]
    colors = ["#9fb3c8", bs.BLUE, bs.ORANGE, bs.GREEN]

    fig, ax = plt.subplots(figsize=(5.6, 2.85))
    x = np.arange(4)
    base = 1e-2
    for i, (v, c, tg) in enumerate(zip(steps, colors, texts)):
        ax.bar(x[i], v - base, bottom=base, width=0.52, color=c, alpha=0.85,
               edgecolor="white", lw=0.6, zorder=3)
        ax.text(x[i], v * 1.5, tg, fontsize=8.6, ha="center", va="bottom",
                color="#33414f")
        if i:
            ax.plot([x[i - 1] + 0.26, x[i] - 0.26], [steps[i - 1], steps[i - 1]],
                    color="#8a97a6", lw=0.8, ls=(0, (3, 2)), zorder=2)
            ax.text((x[i - 1] + x[i]) / 2, steps[i - 1] * 1.18, notes[i],
                    fontsize=7.8, ha="center", va="bottom", color="#4a5563")
    ax.set_yscale("log")
    ax.set_ylim(base, 4e6)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8.2)
    ax.set_xlim(-0.65, 3.65)
    ax.set_ylabel("每秒事件数")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_distance()
    fig_budget()
