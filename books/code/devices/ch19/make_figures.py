"""第 19 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "19"


def fig_cooling():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    t = np.logspace(np.log10(0.01), np.log10(20), 300)
    for eta, col, lab in [(0.3, bs.GREEN, "卡诺效率的 30%"),
                          (0.1, bs.BLUE, "卡诺效率的 10%"),
                          (0.03, bs.RED, "卡诺效率的 3%")]:
        cop = t / (300.0 - t)
        ax.loglog(t, 1.0 / (cop * eta), color=col, lw=1.3, label=lab)
    ax.set_xlim(0.01, 20)
    ax.set_ylim(10, 1e7)
    ax.set_xlabel("冷板温度（K）")
    ax.set_ylabel("每带走 1 W 热量的电功耗（W）")
    ax.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax, grid_axis="both")

    ax2 = fig.add_subplot(gs[0, 1])
    p = np.logspace(-3, 2, 400)  # mW per channel
    for cap, col, lab in [(15000.0, bs.RED, "4 K 级，15 W"),
                          (20.0, bs.BLUE, "1 K 级，20 mW"),
                          (0.02, bs.GREEN, "100 mK 级，20 $\\mu$W")]:
        ax2.loglog(p, cap / p, color=col, lw=1.3, label=lab)
    ax2.axhline(1000, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax2.text(1.15e-3, 1500, "1000 通道", fontsize=7.2, color="#4a5563")
    ax2.set_xlim(1e-3, 1e2)
    ax2.set_ylim(1e-2, 1e5)
    ax2.set_xlabel("每通道功耗（mW）")
    ax2.set_ylabel("可容纳的通道数")
    ax2.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax2, grid_axis="both")
    bs.save(fig, CH, "fig01")


def cost(x, y):
    return -(np.exp(-((x - 0.36) ** 2 + (y - 0.63) ** 2) / 0.018)
             + 0.62 * np.exp(-((x - 0.76) ** 2 + (y - 0.24) ** 2) / 0.05))


def search_grid(n=6, ref=9):
    xs = np.linspace(0.05, 0.95, n)
    best = (None, None, 1e9)
    path = []
    for x in xs:
        for y in xs:
            c = cost(x, y)
            path.append((x, y, c))
            if c < best[2]:
                best = (x, y, c)
    pts = [(b[0], b[1]) for b in path]
    bx, by, bc = best
    for k in range(ref):
        h = 0.18 / (2 ** k)
        for x in np.linspace(bx - h, bx + h, 5):
            for y in np.linspace(by - h, by + h, 5):
                c = cost(x, y)
                path.append((x, y, c))
                if c < bc:
                    bx, by, bc = x, y, c
        pts.append((bx, by))
    return pts, path


def search_coord(n=9, npts=40):
    x, y = 0.06, 0.94
    pts = [(x, y)]
    vals = [cost(x, y)]
    for k in range(n):
        xs = np.linspace(0.02, 0.98, npts)
        cy = np.array([cost(xx, y) for xx in xs])
        x = xs[np.argmin(cy)]
        pts.append((x, y))
        vals.append(cy.min())
        ys = np.linspace(0.02, 0.98, npts)
        cx = np.array([cost(x, yy) for yy in ys])
        y = ys[np.argmin(cx)]
        pts.append((x, y))
        vals.append(cx.min())
        if k > 3 and abs(vals[-1] - vals[-3]) < 1e-7:
            break
    return pts


def search_random(seed=7, iters=260, sig=0.2):
    rng = np.random.default_rng(seed)
    x, y = 0.06, 0.94
    best = cost(x, y)
    pts = [(x, y)]
    curve = [best]
    for _ in range(iters):
        nx = np.clip(x + rng.normal(0, sig), 0.02, 0.98)
        ny = np.clip(y + rng.normal(0, sig), 0.02, 0.98)
        c = cost(nx, ny)
        if c < best:
            x, y, best = nx, ny, c
            pts.append((x, y))
        curve.append(best)
    return pts, np.array(curve)


def fig_calibration():
    fig = plt.figure(figsize=(7.0, 2.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.1], wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    xs = np.linspace(0, 1, 300)
    X, Y = np.meshgrid(xs, xs)
    Z = cost(X, Y)
    cs = ax.contourf(X, Y, Z, levels=14, cmap="Blues_r", alpha=0.85)
    ax.contour(X, Y, Z, levels=14, colors="#7c8896", linewidths=0.3)
    g_pts, _ = search_grid()
    c_pts = search_coord()
    r_pts, _ = search_random()
    ax.plot(*zip(*c_pts), color=bs.RED, lw=1.2, marker="o", ms=2.2, label="坐标轮换")
    ax.plot(*zip(*g_pts[:36]), color=bs.ORANGE, lw=0, marker="+", ms=3.2,
            label="网格穷举")
    ax.plot(*zip(*r_pts), color=bs.GREEN, lw=1.0, marker=".", ms=3.0,
            label="随机搜索")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("脉冲幅度（标幺值）")
    ax.set_ylabel("脉冲失谐（标幺值）")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, fontsize=7.2)
    bs.clean(ax)

    ax2 = fig.add_subplot(gs[0, 1])
    _, gpath = search_grid()
    gvals = np.minimum.accumulate(np.array([p[2] for p in gpath]))
    ax2.plot(np.arange(1, len(gvals) + 1), gvals, color=bs.ORANGE, lw=1.2,
             label="网格穷举")
    cvals = np.array([cost(x, y) for x, y in search_coord()])
    cbest = np.minimum.accumulate(cvals)
    ax2.plot(np.arange(1, len(cbest) + 1) * 40, cbest, color=bs.RED, lw=1.2,
             label="坐标轮换")
    _, rcurve = search_random()
    ax2.plot(np.arange(1, len(rcurve) + 1), rcurve, color=bs.GREEN, lw=1.2,
             label="随机搜索")
    ax2.set_xlim(1, 400)
    ax2.set_ylim(-1.7, -0.75)
    ax2.set_xlabel("测量次数")
    ax2.set_ylabel("当前最优代价")
    ax2.legend(loc="upper right", fontsize=7.2)
    bs.clean(ax2, grid_axis="both")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_cooling()
    fig_calibration()
