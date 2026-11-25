"""入门册插图：每章一张，统一生成。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import bookstyle as bs

bs.use("intro")

h = 6.62607015e-34
c = 2.99792458e8
k = 1.380649e-23


def fig_timeline():
    events = [
        (1900, "能量子"), (1926, "量子力学"), (1947, "晶体管"), (1960, "激光"),
        (1984, "BB84"), (1994, "Shor 算法"), (2019, "量子优越性"), (2023, "表面码纠错"),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 2.3))
    ax.set_xlim(1895, 2030)
    ax.set_ylim(-1.0, 1.0)
    ax.axis("off")
    ax.plot([1895, 2030], [0, 0], color="#8a95a3", lw=1.2)
    for i, (year, name) in enumerate(events):
        up = i % 2 == 0
        y = 0.55 if up else -0.55
        ax.plot([year, year], [0, y * 0.55], color="#b9c3cf", lw=0.8)
        ax.plot([year], [0], "o", ms=4.2, color=bs.BLUE if year < 1980 else bs.RED, zorder=5)
        ax.text(year, y, name, fontsize=7.6, ha="center",
                va="bottom" if up else "top",
                color="#33414f" if year < 1980 else "#7a2a1a")
        ax.text(year, -0.06 if up else 0.06, str(year), fontsize=6.8, ha="center",
                va="top" if up else "bottom", color="#6b7785")
    bs.save(fig, "01", "fig01")


def fig_blackbody():
    lam = np.linspace(0.2e-6, 10e-6, 1200)
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    for T, color in [(3000, bs.RED), (4500, bs.ORANGE), (6000, bs.BLUE)]:
        y = 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * k * T)) - 1) * 1e-12
        ax.plot(lam * 1e6, y, color=color, lw=1.4, label=f"{T} K")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.set_xlabel("波长 (μm)")
    ax.set_ylabel("单色辐出度 (10$^{12}$ W·m$^{-3}$)")
    ax.legend(loc="upper right", handlelength=1.5)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, "02", "fig01")


def fig_buildup():
    lam, d, L, a = 50e-12, 12.5e-6, 0.5, 3.0e-6
    rng = np.random.default_rng(2024)
    xmax = 9e-6
    xs = np.linspace(-xmax, xmax, 3000)

    def pdf(x):
        th = np.arctan(x / L)
        beta = np.pi * a * np.sin(th) / lam
        alpha = np.pi * d * np.sin(th) / lam
        return np.sinc(beta / np.pi) ** 2 * np.cos(alpha) ** 2

    p = pdf(xs)
    p = p / p.sum()
    cdf = np.cumsum(p)
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.2), sharey=True)
    for ax, N in zip(axes, [300, 30000]):
        x = np.interp(rng.random(N), cdf, xs)
        y = rng.normal(0, 3.0e-6, N)
        ax.scatter(x * 1e6, y * 1e6, s=1.2, color="#1f2a37", alpha=0.5, linewidths=0)
        ax.set_xlim(-9, 9)
        ax.set_ylim(-9, 9)
        ax.set_xticks([-8, 0, 8])
        ax.set_yticks([])
        ax.set_xlabel(f"{N} 个电子", fontsize=8)
        for s in ["top", "right", "left"]:
            ax.spines[s].set_visible(False)
    axes[0].set_ylabel("竖直方向 (μm)", fontsize=8)
    fig.text(0.5, 0.01, "水平方向 (μm)", ha="center", fontsize=8.4)
    fig.subplots_adjust(bottom=0.3, wspace=0.1)
    bs.save(fig, "03", "fig01")


def fig_bloch():
    fig = plt.figure(figsize=(4.4, 3.8))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color="#ccd8e5", linewidth=0.35, rstride=4, cstride=4)
    ax.plot([0, 0], [0, 0], [-1.1, 1.1], color="#8a95a3", lw=0.8)
    th, ph = np.deg2rad(60), np.deg2rad(30)
    vx, vy, vz = np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)
    ax.plot([0, vx], [0, vy], [0, vz], color=bs.RED, lw=2.2)
    ax.plot([vx], [vy], [vz], "o", ms=4, color=bs.RED)
    ax.text(0, 0, 1.24, r"$|0\rangle$", fontsize=10, color=bs.BLUE, ha="center")
    ax.text(0, 0, -1.3, r"$|1\rangle$", fontsize=10, color=bs.BLUE, ha="center")
    ax.text(vx * 1.22, vy * 1.22, vz * 1.22, r"$|\psi\rangle$", fontsize=10, color=bs.RED,
            ha="left", va="bottom")
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=128)
    bs.save(fig, "04", "fig01")


def fig_clock():
    years = [1955, 1975, 1995, 2010, 2020]
    acc = [1e-10, 1e-13, 1e-15, 1e-17, 1e-18]
    labels = ["铯束钟", "商品铯钟", "铯喷泉钟", "光钟", "光钟（最新）"]
    fig, ax = plt.subplots(figsize=(6.0, 2.7))
    ax.semilogy(years, acc, "o-", ms=4, lw=1.2, color=bs.BLUE)
    for x, y, t in zip(years, acc, labels):
        ax.annotate(t, xy=(x, y), xytext=(x, y * 6), fontsize=7.4, color="#4a5563", ha="center")
    ax.set_xlabel("年份")
    ax.set_ylabel("相对频率不确定度")
    ax.set_xlim(1950, 2026)
    ax.set_ylim(1e-19, 1e-8)
    ax.text(1958, 3e-19, "点越低代表越准", fontsize=7.6, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, "05", "fig01")


def fig_state_space():
    n = np.arange(0, 61)
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    ax.semilogy(n, 2.0 ** n, color=bs.BLUE, lw=1.5)
    for nn, txt in [(10, "$10^3$"), (30, "$10^9$"), (50, "$10^{15}$")]:
        ax.plot([nn], [2.0 ** nn], "o", ms=3.6, color=bs.RED)
        ax.annotate(txt, xy=(nn, 2.0 ** nn), xytext=(nn + 1.5, 2.0 ** nn * 0.25),
                    fontsize=7.6, color=bs.RED)
    ax.set_xlabel("量子比特数 $n$")
    ax.set_ylabel("概率幅个数 $2^n$")
    ax.set_xlim(0, 60)
    ax.set_ylim(1, 1e19)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, "06", "fig01")


def fig_grover():
    N = np.logspace(1, 12, 300)
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    ax.loglog(N, N, color=bs.GRAY, lw=1.2, ls=(0, (4, 3)), label="经典搜索")
    ax.loglog(N, np.pi / 4 * np.sqrt(N), color=bs.BLUE, lw=1.5, label="Grover 搜索")
    ax.set_xlabel("数据库规模 $N$")
    ax.set_ylabel("查询次数")
    ax.legend(loc="upper left", handlelength=1.8)
    ax.annotate("平方根加速", xy=(1e8, 8e3), xytext=(1e6, 3e5), fontsize=7.8, color="#4a5563",
                arrowprops=dict(arrowstyle="-|>", color="#8a95a3", lw=0.7, connectionstyle="arc3,rad=0.2"))
    bs.clean(ax, grid_axis="both")
    bs.save(fig, "07", "fig01")


def fig_bb84():
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    for x, name in [(1.6, "Alice"), (8.4, "Bob")]:
        ax.text(x, 5.05, name, fontsize=9, ha="center")
        ax.plot([x, x], [0.6, 4.7], color="#b9c3cf", lw=1.0, ls=(0, (4, 3)))
    rows = [(4.1, 1.6, 8.4, "发送量子态", bs.RED), (3.3, 8.4, 1.6, "公布测量基", "#4a5568"),
            (2.5, 8.4, 1.6, "保留基一致的比特", "#4a5568"), (1.7, 1.6, 8.4, "抽样估计误码", "#4a5568")]
    for y, x0, x1, txt, color in rows:
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.1, shrinkA=0, shrinkB=0))
        ax.text(5.0, y + 0.08, txt, fontsize=7.8, color=color, ha="center", va="bottom")
    ax.annotate("", xy=(8.4, 0.95), xytext=(1.6, 0.95),
                arrowprops=dict(arrowstyle="-|>", color=bs.GREEN, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(5.0, 1.03, "双方得到相同的密钥", fontsize=7.8, color=bs.GREEN, ha="center", va="bottom")
    bs.save(fig, "08", "fig01")


def fig_limit():
    N = np.logspace(0, 6, 300)
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    ax.loglog(N, 1 / np.sqrt(N), color=bs.BLUE, lw=1.5, label="标准量子极限 $1/\\sqrt{N}$")
    ax.loglog(N, 1 / N, color=bs.RED, lw=1.5, label="海森堡极限 $1/N$")
    ax.set_xlabel("粒子数 $N$")
    ax.set_ylabel("相位不确定度")
    ax.legend(loc="lower left", handlelength=2.0)
    bs.clean(ax, grid_axis="both")
    bs.save(fig, "09", "fig01")


def fig_threshold():
    p = np.logspace(-4, -1.4, 400)
    pth = 1e-2
    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    for d, color in [(3, "#9db8d2"), (5, "#5c86ad"), (7, "#2b5c94")]:
        pl = 0.1 * (p / pth) ** ((d + 1) / 2)
        ax.loglog(p, np.clip(pl, 1e-12, 1), color=color, lw=1.4, label=f"码距 $d={d}$")
    ax.axvline(pth, color=bs.RED, lw=0.9, ls=(0, (3, 2)))
    ax.text(pth * 1.06, 3e-9, "阈值", fontsize=8, color=bs.RED)
    ax.set_xlabel("物理错误率 $p$")
    ax.set_ylabel("逻辑错误率 $p_L$")
    ax.set_xlim(1e-4, 5e-2)
    ax.set_ylim(1e-12, 1)
    ax.legend(loc="lower right", handlelength=1.4)
    ax.text(1.1e-4, 3e-2, "低于阈值时，码距越大越可靠", fontsize=7.6, color="#4a5563")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, "11", "fig01")


if __name__ == "__main__":
    fig_timeline()
    fig_blackbody()
    fig_buildup()
    fig_bloch()
    fig_clock()
    fig_state_space()
    fig_grover()
    fig_bb84()
    fig_limit()
    fig_threshold()
