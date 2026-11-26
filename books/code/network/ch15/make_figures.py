"""第 15 章插图：时间同步的精度阶梯，传感的标度，跨域调度的拒绝率。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "15"


def fig_sync_and_sensing():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.95),
                             gridspec_kw={"wspace": 0.36})

    ax = axes[0]
    items = [
        ("卫星单向授时", 3.0e-8, bs.GRAY),
        ("卫星共视比对", 5.0e-9, bs.GRAY),
        ("光纤双向比对", 1.0e-10, bs.BLUE),
        ("白兔协议", 5.0e-11, bs.BLUE),
        ("纠缠增强演示", 1.0e-12, bs.GREEN),
    ]
    y = np.arange(len(items))
    for i, (name, val, color) in enumerate(items):
        ax.barh(i, val, height=0.55, color=color, alpha=0.75, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([n for n, _, _ in items], fontsize=7.8)
    ax.set_xscale("log")
    ax.set_xlim(1e-13, 1e-6)
    ax.set_xlabel("同步误差（s）")
    ax.set_xticks([1e-12, 1e-10, 1e-8, 1e-6])
    ax.set_xticklabels(["1 ps", "100 ps", "10 ns", "1 μs"])
    ax.invert_yaxis()
    bs.clean(ax, grid_axis="x")

    ax = axes[1]
    N = np.logspace(0, 4, 200)
    ax.loglog(N, 1 / np.sqrt(N), color=bs.GRAY, lw=1.4, label="标准量子极限")
    ax.loglog(N, 1 / (np.sqrt(N) * 10 ** (10 / 20)), color=bs.BLUE, lw=1.4,
              label="压缩 10 dB")
    ax.loglog(N, 1 / N, color=bs.RED, lw=1.4, label="海森堡极限")
    ax.set_xlabel("平均光子数 N")
    ax.set_ylabel("相位灵敏度（相对值）")
    ax.set_xlim(1, 1e4)
    ax.set_ylim(1e-5, 1.5)
    ax.legend(loc="lower left", fontsize=7.2)
    ax.text(45, 8e-3, "压缩光把整条线\n平移下来", fontsize=7.2, color=bs.BLUE)
    bs.clean(ax, grid_axis="y")

    bs.save(fig, CH, "fig01")


def demand_profile(t):
    return (0.002
            + 0.020 * np.exp(-((t / 3600.0 - 10.5) / 1.5) ** 2)
            + 0.024 * np.exp(-((t / 3600.0 - 14.5) / 1.8) ** 2)
            + 0.008 * np.exp(-((t / 3600.0 - 20.0) / 2.2) ** 2))


def run(caps, domains=1, rate=0.010, scenarios=40, seed=3):
    rng = np.random.default_rng(seed)
    T = 86400
    t = np.arange(T, dtype=float)
    prof = demand_profile(t)
    nC = len(caps)
    level = np.repeat(caps[None, :], scenarios, axis=0) * 0.6
    deficit = np.zeros((scenarios, nC))
    total = np.zeros((scenarios, nC))
    frac = np.zeros((scenarios, nC, domains))
    noise = np.exp(rng.normal(0, 0.35, size=(scenarios, domains)))
    for i in range(T):
        noise += (-noise + 1.0) * (1.0 / 300.0) + rng.normal(0, 0.035, size=(scenarios, domains))
        d = prof[i] * noise.mean(axis=1)
        for k in range(domains):
            dl = prof[i] * noise[:, k]
            avail = level + (rate - dl)[:, None]
            hit = np.clip(-avail, 0, None)
            level = np.clip(avail, 0, None)
            level = np.minimum(level, caps[None, :])
            frac[:, :, k] += hit
        total += d[:, None]
    f = 1 - np.prod(1 - frac / np.maximum(total[:, :, None], 1e-12), axis=2)
    return f.mean(axis=0)


def fig_schedule():
    caps = np.array([10, 15, 20, 30, 40, 60, 80, 120, 160, 240, 320, 480, 640], dtype=float)
    fig, ax = plt.subplots(figsize=(5.7, 3.0))
    for domains, color, label in [(1, bs.BLUE, "单域"),
                                  (2, bs.ORANGE, "两域串联"),
                                  (3, bs.RED, "三域串联")]:
        y = run(caps, domains) * 100
        ax.semilogx(caps, y, color=color, lw=1.5, marker="o", ms=3.2, label=label)
        print(label, np.round(y, 2))
    ax.set_xlabel("每个域的密钥池容量（Mb）")
    ax.set_ylabel("请求被拒的比例（%）")
    ax.set_xlim(8, 900)
    ax.set_ylim(-1, 40)
    ax.set_xticks([10, 40, 160, 640])
    ax.set_xticklabels(["10", "40", "160", "640"])
    ax.axhline(1.0, color="#8a97a6", lw=0.8, ls=(0, (4, 2)))
    ax.text(200, 1.7, "百分之一的承诺线", fontsize=7.2, color="#4a5563")
    ax.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_sync_and_sensing()
    fig_schedule()
