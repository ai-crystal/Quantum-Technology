"""第 14 章插图：三种协议的距离，与设备无关方案的效率门限。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "14"

ALPHA = 0.2
NU = 1e8
MU = 0.5
E0 = 0.01
P_DC = 1e-6
LEAK = 1e-7
ETA_TH = 2.0 / 3.0     # 无漏洞贝尔检验的效率门限
ETA_CHSH = 0.828


def h2(e):
    e = np.clip(e, 1e-12, 1 - 1e-12)
    return -e * np.log2(e) - (1 - e) * np.log2(1 - e)


def r_bb84(L, eta_det=0.6):
    eta = eta_det * 10.0 ** (-ALPHA * L / 10.0)
    e = (E0 * eta + 0.5 * P_DC) / (eta + P_DC)
    return 0.5 * NU * MU * eta * (1 - h2(e)) - LEAK


def r_mdi(L, eta_det=0.6):
    eta = eta_det * 10.0 ** (-ALPHA * L / 10.0)
    e = (E0 + 0.5 * P_DC / (MU * eta ** 2)) / (1 + P_DC / (MU * eta ** 2))
    return 0.5 * NU * MU ** 2 * eta ** 2 * (1 - h2(e)) - LEAK


def r_di(L, eta_det=0.85):
    eta = eta_det * 10.0 ** (-ALPHA * L / 10.0)
    e = 0.5 * (1 - 0.95 * eta)
    r = 0.1 * NU * MU * eta * (1 - h2(e)) - LEAK
    return np.where(eta >= ETA_TH, np.maximum(r, 0.0), 0.0)


def fig_protocols():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.05),
                             gridspec_kw={"wspace": 0.34})

    ax = axes[0]
    L = np.logspace(np.log10(1.0), np.log10(200), 400)
    ax.semilogy(L, r_bb84(L), color=bs.BLUE, lw=1.5)
    ax.semilogy(L, r_mdi(L), color=bs.GREEN, lw=1.5)
    ax.semilogy(L, r_di(L), color=bs.RED, lw=1.6)
    ax.set_xlabel("光纤长度（km）")
    ax.set_ylabel("成码率（bit/s）")
    ax.set_xscale("log")
    ax.set_xlim(1, 200)
    ax.set_ylim(1e-2, 5e7)
    ax.set_xticks([1, 5, 10, 50, 100, 200])
    ax.set_xticklabels(["1", "5", "10", "50", "100", "200"])
    ax.text(52, 7.5e6, "诱骗态 BB84", fontsize=7.4, color=bs.BLUE)
    ax.text(17, 1.1e4, "测量设备无关", fontsize=7.4, color=bs.GREEN)
    ax.text(1.05, 3.4e6, "设备无关", fontsize=7.4, color=bs.RED)
    ax.text(5.9, 6e3, "五公里处归零", fontsize=7.2, color=bs.RED)
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    eta_det = np.linspace(0.60, 1.0, 200)
    for th, color, label in [(ETA_TH, bs.BLUE, "Eberhard 型，0.667"),
                             (ETA_CHSH, bs.ORANGE, "CHSH，0.828")]:
        with np.errstate(divide="ignore"):
            Lmax = np.where(eta_det >= th,
                            10.0 / ALPHA * np.log10(eta_det / th), np.nan)
        ax.plot(eta_det * 100, Lmax, color=color, lw=1.6, label=label)
    ax.set_xlabel("单光子探测器效率（%）")
    ax.set_ylabel("无漏洞贝尔检验的最大距离（km）")
    ax.set_xlim(60, 100)
    ax.set_ylim(0, 20)
    ax.set_xticks([60, 70, 80, 90, 100])
    ax.legend(loc="upper left", fontsize=7.2, title="效率门限", title_fontsize=7.2)
    ax.text(61.5, 7.4, "效率九成时 CHSH 型\n也只到七公里", fontsize=7.2, color="#4a5563")
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig01")


def fig_stats():
    ds = np.logspace(np.log10(0.02), np.log10(0.6), 240)
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    for k, color, label in [(3, bs.BLUE, "三倍标准差"), (5, bs.RED, "五倍标准差")]:
        N = (k * 3.0 / ds) ** 2
        ax.loglog(ds, N, color=color, lw=1.6, label=label)

    ax.set_xlabel(r"贝尔量超出定域上界的幅度 $S-2$")
    ax.set_ylabel("需要的纠缠对数")
    ax.set_xlim(0.02, 0.6)
    ax.set_ylim(50, 5e7)
    ax.set_xticks([0.02, 0.05, 0.1, 0.2, 0.4])
    ax.set_xticklabels(["0.02", "0.05", "0.1", "0.2", "0.4"])
    ax.minorticks_off()
    ax.legend(loc="upper right", fontsize=7.4)

    ax2 = ax.twinx()
    ax2.set_yscale("log")
    ax2.set_ylim(50 / 1e3, 5e7 / 1e3)
    ax2.set_ylabel("按每秒一千对折算的时间（s）", labelpad=6)
    ax2.spines["right"].set_visible(True)
    ax2.spines["top"].set_visible(False)
    ax2.minorticks_off()

    ax.plot([0.1], [(5 * 3.0 / 0.1) ** 2], "o", ms=5, mfc="none", mew=1.2, color=bs.RED)
    ax.annotate("0.1 的违背要两万对", xy=(0.1, (5 * 3.0 / 0.1) ** 2),
                xytext=(0.13, 4.5e6), fontsize=7.2, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_protocols()
    fig_stats()
    for L in (0.5, 2, 5, 10, 20):
        print(L, "BB84 %.3g" % r_bb84(L), "MDI %.3g" % r_mdi(L), "DI %.3g" % r_di(L))
    for e in (0.8, 0.85, 0.9, 0.95):
        print("eta", e, "Lmax th", round(10 / ALPHA * np.log10(e / ETA_TH), 2),
              "CHSH", round(10 / ALPHA * np.log10(e / ETA_CHSH), 2))
