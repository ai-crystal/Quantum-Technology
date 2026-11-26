"""第 13 章插图：星地几何与损耗预算，以及一次过境的成码率。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "13"

R_E = 6371.0     # 地球半径 km
LAM = 850e-9     # 波长 m
D_T = 0.15       # 发射口径 m
D_R = 1.0        # 接收口径 m
ETA_DET = 0.20   # 单光子探测器效率
ETA_OPT = 0.60   # 收发光学效率
ETA_FIL = 0.50   # 滤波透过率
ETA_POINT = 0.50  # 跟瞄误差造成的耦合损失
ETA_TIME = 0.50  # 时间同步门控
NU = 1.0e8       # 脉冲重复率 Hz
MU = 0.8         # 平均光子数


def slant(el_deg, h):
    el = np.radians(el_deg)
    r = R_E + h
    return np.sqrt(r ** 2 - (R_E * np.cos(el)) ** 2) - R_E * np.sin(el)


def eta_geo(z_km):
    spot = 1.22 * LAM * z_km * 1e3 / D_T
    return np.clip((D_R / spot) ** 2, 1e-12, 1.0)


def eta_atm(el_deg):
    return np.exp(-0.15 * (1.0 / np.sin(np.radians(el_deg)) - 1.0))


def eta_total(el_deg, h=600.0):
    z = slant(el_deg, h)
    return eta_geo(z) * eta_atm(el_deg) * ETA_POINT * ETA_OPT * ETA_FIL * ETA_DET * ETA_TIME


def h2(e):
    e = np.clip(e, 1e-12, 1 - 1e-12)
    return -e * np.log2(e) - (1 - e) * np.log2(1 - e)


def rate(el_deg, h=600.0, bg=1e-4, e_opt=0.012):
    eta = eta_total(el_deg, h)
    sig = MU * eta
    e = (0.5 * bg + e_opt * sig) / (sig + bg)
    r = 0.5 * NU * sig * (1 - h2(e))
    return np.maximum(r, 0.0)


def fig_geometry():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.18], "wspace": 0.34})

    ax = axes[0]
    el = np.linspace(10, 90, 200)
    for h, color, label in [(500, bs.GREEN, "500 km"), (600, bs.BLUE, "600 km"),
                            (1200, bs.RED, "1200 km")]:
        ax.plot(el, slant(el, h), color=color, lw=1.5, label=label)
    ax.set_xlabel("地面仰角（度）")
    ax.set_ylabel("星地斜距（km）")
    ax.set_xlim(10, 90)
    ax.set_ylim(400, 3200)
    ax.set_xticks([10, 30, 50, 70, 90])
    ax.legend(loc="upper right", fontsize=7.4, title="轨道高度", title_fontsize=7.4)
    ax.text(48, 1330, "仰角越低，斜距越长", fontsize=7.2, color="#4a5563")
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    el0, h0 = 30.0, 600.0
    z0 = slant(el0, h0)
    items = [
        ("几何扩散", 10 * np.log10(eta_geo(z0))),
        ("大气透过", 10 * np.log10(eta_atm(el0))),
        ("跟瞄误差", 10 * np.log10(ETA_POINT)),
        ("收发光学", 10 * np.log10(ETA_OPT)),
        ("窄带滤波", 10 * np.log10(ETA_FIL)),
        ("探测效率", 10 * np.log10(ETA_DET)),
        ("时间门控", 10 * np.log10(ETA_TIME)),
    ]
    names = [n for n, _ in items][::-1]
    vals = np.array([v for _, v in items][::-1])
    ypos = np.arange(len(names))
    ax.barh(ypos, -vals, color=bs.BLUE, alpha=0.75, height=0.62, zorder=3)
    for y, v in zip(ypos, vals):
        ax.text(-v + 0.6, y, f"{v:.1f}", va="center", fontsize=7.4, color="#33414f")
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=7.8)
    ax.set_xlabel("损耗（dB，负值）")
    ax.set_xlim(0, 23)
    total = vals.sum()
    ax.text(22.4, ypos[-1] + 0.72, "合计 %.1f dB，约 %.0e" % (total, 10 ** (total / 10)),
            fontsize=7.6, color="#4a5563", ha="right")
    bs.clean(ax, grid_axis="x")

    bs.save(fig, CH, "fig01")


def fig_pass():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0),
                             gridspec_kw={"width_ratios": [1.0, 1.15], "wspace": 0.32})

    ax = axes[0]
    el = np.linspace(10, 90, 220)
    ax.semilogy(el, rate(el, bg=1e-4), color=bs.BLUE, lw=1.5, label="夜间")
    ax.semilogy(el, rate(el, bg=2e-3), color=bs.ORANGE, lw=1.5, label="白天")
    ax.set_xlabel("地面仰角（度）")
    ax.set_ylabel("成码率（bit/s）")
    ax.set_xlim(10, 90)
    ax.set_ylim(20, 2e5)
    ax.set_xticks([10, 30, 50, 70, 90])
    ax.legend(loc="lower right", fontsize=7.4)
    ax.text(31, 3.2e4, "白天的背景光\n把误码顶上去", fontsize=7.2, color=bs.ORANGE)
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    t = np.linspace(0, 10, 600)
    el_t = np.clip(70.0 * np.cos(np.pi * (t - 5) / 10.0), 0, 90)
    ax.plot(t, el_t, color=bs.GRAY, lw=1.2, ls=(0, (4, 2)))
    ax.set_xlabel("过境时间（min）")
    ax.set_ylabel("仰角（度）")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 80)
    ax.set_yticks([0, 20, 40, 60, 80])

    ax2 = ax.twinx()
    vis = el_t >= 10
    r = np.where(vis, rate(el_t, bg=1e-4), np.nan)
    ax2.fill_between(t, 10, r, where=vis, color=bs.BLUE, alpha=0.16, lw=0)
    ax2.semilogy(t, r, color=bs.BLUE, lw=1.7)
    ax2.set_ylabel("成码率（bit/s）", color=bs.BLUE)
    ax2.set_ylim(10, 1e5)
    ax2.tick_params(axis="y", colors=bs.BLUE)
    ax2.spines["right"].set_visible(True)
    ax2.spines["top"].set_visible(False)

    total = np.trapezoid(np.where(vis, r, 0.0), t * 60.0)
    print("  一次过境密钥量 Mbit", round(total / 1e6, 2))
    bs.clean(ax)

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_geometry()
    fig_pass()
    for e in (10, 20, 30, 60, 90):
        print(e, round(slant(e, 600), 1), f"{rate(e):.3g}", f"{rate(e, bg=2e-3):.3g}")
