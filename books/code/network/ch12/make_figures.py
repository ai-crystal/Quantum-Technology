"""第 12 章插图：双路由的共缆代价，以及密钥池一天的进出账。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "12"

LAM100 = 0.15    # 光缆中断次数，每百公里每年
MTTR = 8.0       # 平均修复时间，小时
HOURS = 8760.0


def downtime_minutes(share):
    """两条 100 km 路径共享 share 公里的同一条缆，返回年停机分钟数。"""
    lam_s = LAM100 * share / 100.0
    lam_p = LAM100 * (100.0 - share) / 100.0
    u_s = lam_s * MTTR / HOURS
    u_p = lam_p * MTTR / HOURS
    return 525600.0 * (u_s + u_p * u_p)


def fig_cable():
    share = np.linspace(0, 100, 600)
    y = np.array([downtime_minutes(s) for s in share])

    fig, ax = plt.subplots(figsize=(5.9, 3.05))
    ax.semilogy(share, y, color=bs.BLUE, lw=1.6)

    for val, tag, color in [(5.26, "五个九，5.3 min", bs.GREEN),
                            (52.6, "四个九，53 min", bs.ORANGE)]:
        ax.axhline(val, color=color, lw=0.9, ls=(0, (4, 2)))
        ax.text(46, val * 1.18, tag, fontsize=7.2, color=color, ha="left")

    ax.set_xlim(0, 100)
    ax.set_ylim(5e-3, 3e2)
    ax.set_xlabel("两条 100 km 路由共享同一缆的长度（km）")
    ax.set_ylabel("双路同时中断的年停机（min）")
    ax.set_xticks([0, 20, 40, 60, 80, 100])

    ax.annotate("独缆双路由", xy=(1.0, 1.1e-2), xytext=(13, 6e-2),
                fontsize=7.4, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    ax.plot([7.3], [5.26], "o", ms=4.5, mfc="none", mew=1.1, color=bs.GREEN)
    ax.text(9.5, 1.3, "守住五个九，同缆不能超过 7 km",
            fontsize=7.2, color="#4a5563")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def demand(t):
    return (2.0
            + 20.0 * np.exp(-((t - 10.5) / 1.5) ** 2)
            + 24.0 * np.exp(-((t - 14.5) / 1.8) ** 2)
            + 8.0 * np.exp(-((t - 20.0) / 2.2) ** 2))


def pool(t, gen, cap=400.0, start=150.0):
    level = start
    out = []
    dt = t[1] - t[0]
    for i, tt in enumerate(t):
        level = min(cap, level + (gen(tt) - demand(tt)) * dt * 3.6)
        level = max(0.0, level)
        out.append(level)
    return np.array(out)


def fig_pool():
    t = np.linspace(0, 24, 2401)
    d = demand(t)

    fig, axes = plt.subplots(2, 1, figsize=(6.2, 3.7), sharex=True,
                             gridspec_kw={"height_ratios": [1.0, 1.15], "hspace": 0.18})

    ax = axes[0]
    ax.plot(t, d, color=bs.RED, lw=1.4, label="业务占用的密钥率")
    ax.plot(t, np.full_like(t, 10.0), color=bs.BLUE, lw=1.3,
            label="链路稳态生成 10 kbps")
    ax.plot([13, 17], [10, 10], color="white", lw=3.2)
    ax.plot([13, 17], [10, 10], color=bs.GRAY, lw=1.3, ls=(0, (3, 2)))
    ax.annotate("链路检修，生成中断", xy=(15, 10), xytext=(15.4, 33),
                fontsize=7.2, color=bs.GRAY,
                arrowprops=dict(arrowstyle="-", color=bs.GRAY, lw=0.7))
    ax.set_ylabel("速率（kbps）")
    ax.set_ylim(0, 46)
    ax.legend(loc="upper left", fontsize=7.2, ncol=2, columnspacing=1.0)
    bs.clean(ax, grid_axis="y")

    ax = axes[1]
    scenarios = [
        (lambda x: 10.0, bs.BLUE, "全天正常"),
        (lambda x: 0.0 if 13 <= x <= 17 else 10.0, bs.ORANGE, "中断四小时"),
        (lambda x: 0.0 if 12 <= x <= 20 else 10.0, bs.RED, "中断八小时"),
    ]
    for gen, color, label in scenarios:
        ax.plot(t, pool(t, gen), color=color, lw=1.4, label=label)
    ax.axhline(40, color="#8a97a6", lw=0.8, ls=(0, (4, 2)))
    ax.text(1.0, 52, "低位告警 40 Mb", fontsize=7.0, color="#4a5563")
    ax.axhline(400, color="#8a97a6", lw=0.8, ls=(0, (1, 2)))
    ax.text(23.4, 372, "池容量上限 400 Mb", fontsize=7.0, color="#4a5563", ha="right")
    ax.set_xlabel("时刻（h）")
    ax.set_ylabel("密钥池存量（Mb）")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 520)
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.legend(loc="upper left", fontsize=7.2, ncol=3, columnspacing=1.0,
              handlelength=1.5, borderpad=0.2)
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_cable()
    fig_pool()
