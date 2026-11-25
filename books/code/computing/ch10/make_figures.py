"""第十章插图：拓扑映射前后的线路、不同连接方式下的深度增长。"""
import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
from circuit import Circuit

CH = "10"

rng = np.random.default_rng(1010)


def fig_routing():
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 3.5))
    fig.subplots_adjust(hspace=0.62)

    ax = axes[0]
    c = Circuit(ax, 5, 4, labels=[rf"$q_{i}$" for i in range(5)])
    c.gate(0, 0, "H")
    c.cnot(1, 0, 4)
    c.measure(2.6, 0)
    c.measure(2.6, 4)
    c.annotate(1, "两端不相邻", dy=0.45, qubit=0)
    ax.text(-1.05, 1.02, "(a) 逻辑线路", fontsize=8.6, color="#33414f")

    ax = axes[1]
    c = Circuit(ax, 5, 6, labels=[rf"$q_{i}$" for i in range(5)])
    c.gate(0, 0, "H")
    c.swap(1, 0, 1)
    c.swap(2, 1, 2)
    c.swap(3, 2, 3)
    c.cnot(4, 3, 4)
    c.measure(5.2, 3)
    c.measure(5.2, 4)
    c.annotate(2, "用三次交换把态搬到相邻位置", dy=0.45, qubit=0)
    ax.text(-1.05, 1.02, "(b) 映射到五比特链", fontsize=8.6, color="#33414f")
    bs.save(fig, CH, "fig01")


def line(n):
    return {i: [j for j in (i - 1, i + 1) if 0 <= j < n] for i in range(n)}


def grid(rows, cols):
    g = {}
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            nb = []
            if r > 0:
                nb.append(i - cols)
            if r < rows - 1:
                nb.append(i + cols)
            if c > 0:
                nb.append(i - 1)
            if c < cols - 1:
                nb.append(i + 1)
            g[i] = nb
    return g


def complete(n):
    return {i: [j for j in range(n) if j != i] for i in range(n)}


def bfs_path(g, src, dst):
    prev = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in g[u]:
            if v not in prev:
                prev[v] = u
                q.append(v)
    path = []
    u = dst
    while u is not None:
        path.append(u)
        u = prev[u]
    return path[::-1]


def run(ops, g, n):
    """把逻辑线路映射到给定连接图上，返回深度与两比特门数。"""
    pos = list(range(n))
    occ = list(range(n))
    last = [0] * n
    two = 0

    def two_q(p, q):
        nonlocal two
        t = max(last[p], last[q]) + 1
        last[p] = last[q] = t
        two += 1

    for op in ops:
        if op[0] == "1q":
            last[pos[op[1]]] += 1
            continue
        a, b = op[1], op[2]
        while pos[b] not in g[pos[a]]:
            path = bfs_path(g, pos[a], pos[b])
            p, q = path[0], path[1]
            for _ in range(3):
                two_q(p, q)
            la, lb = occ[p], occ[q]
            pos[la], pos[lb] = q, p
            occ[p], occ[q] = lb, la
        two_q(pos[a], pos[b])
    return max(last), two


def random_ops(n, depth, gen):
    ops = []
    for _ in range(depth):
        for q in range(n):
            if gen.random() < 0.6:
                ops.append(("1q", q))
        a, b = gen.choice(n, size=2, replace=False)
        ops.append(("cnot", int(a), int(b)))
    return ops


def fig_depth():
    n = 6
    layers = np.array([5, 10, 15, 20, 25, 30])
    devices = [
        (complete(n), "全连接", bs.BLUE, "o"),
        (grid(2, 3), "2×3 网格", bs.GREEN, "s"),
        (line(n), "六比特链", bs.RED, "^"),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    for g, name, color, mk in devices:
        ds = []
        for L in layers:
            vals = []
            for seed in range(8):
                ops = random_ops(n, int(L), np.random.default_rng(1000 * int(L) + seed))
                vals.append(run(ops, g, n)[0])
            ds.append(np.mean(vals))
            print(name, int(L), round(float(np.mean(vals)), 1))
        ax.plot(layers, ds, mk + "-", ms=3.4, lw=1.1, color=color, label=name)
    ax.set_xlabel("随机线路的层数")
    ax.set_ylabel("映射后的线路深度")
    ax.legend(loc="upper left")
    ax.text(0.42, 0.06, "六比特，每层一个随机两比特门，每点取 8 条线路平均",
            transform=ax.transAxes, fontsize=7.4, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_routing()
    fig_depth()
