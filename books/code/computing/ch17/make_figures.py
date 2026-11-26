"""第十七章插图：QAOA 在随机三正则图上的近似比、梯度方差随比特数的衰减。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

import bookstyle as bs

bs.use("computing")
CH = "17"


def random_regular(n, d=3, rng=None):
    """配置模型生成随机 d 正则图，重试直到没有自环和重边。"""
    while True:
        stubs = np.repeat(np.arange(n), d)
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for k in range(0, len(stubs), 2):
            a, b = int(stubs[k]), int(stubs[k + 1])
            if a == b:
                ok = False
                break
            edges.add((min(a, b), max(a, b)))
        if ok and len(edges) == n * d // 2:
            return sorted(edges)


def cut_values(n, edges):
    idx = np.arange(1 << n)
    bits = ((idx[:, None] >> np.arange(n)) & 1)
    val = np.zeros(1 << n)
    for a, b in edges:
        val += bits[:, a] != bits[:, b]
    return val


def qaoa(n, edges, p, params):
    """返回 QAOA 态的振幅。"""
    dim = 1 << n
    idx = np.arange(dim)
    bits = ((idx[:, None] >> np.arange(n)) & 1) * 1.0
    zz = np.zeros(dim)
    for a, b in edges:
        zz += (1 - 2 * bits[:, a]) * (1 - 2 * bits[:, b])

    state = np.full(dim, 1.0 / np.sqrt(dim), dtype=complex)
    for layer in range(p):
        gamma, beta = params[2 * layer], params[2 * layer + 1]
        state = state * np.exp(-1j * gamma * zz)
        c, s = np.cos(beta), -1j * np.sin(beta)
        for q in range(n):
            m = (idx >> q) & 1
            i0, i1 = idx[m == 0], idx[m == 1]
            a0, a1 = state[i0].copy(), state[i1].copy()
            state[i0] = c * a0 + s * a1
            state[i1] = s * a0 + c * a1
    return state


def qaoa_ratio(n, edges, p, rng, restarts=24):
    cut = cut_values(n, edges)
    best_cut = float(cut.max())
    dim = 1 << n

    def neg(params):
        st = qaoa(n, edges, p, params)
        return -float((np.abs(st) ** 2 * cut).sum()) / best_cut

    best = 0.0
    for _ in range(restarts):
        x0 = np.concatenate([[rng.uniform(0, np.pi), rng.uniform(0, np.pi / 2)] for _ in range(p)])
        res = minimize(neg, x0, method="Nelder-Mead",
                       options={"maxiter": 3000, "xatol": 1e-8, "fatol": 1e-10})
        best = max(best, -res.fun)
    return best


def fig_qaoa():
    rng = np.random.default_rng(7)
    ps = [1, 2, 3]
    res = {p: [] for p in ps}
    for _ in range(6):
        edges = random_regular(12, 3, rng)
        for p in ps:
            res[p].append(qaoa_ratio(12, edges, p, rng))
    for p in ps:
        print(f"p={p}: 平均 {np.mean(res[p]):.3f}, 范围 {min(res[p]):.3f}-{max(res[p]):.3f}")

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    means = [np.mean(res[p]) for p in ps]
    lo = [np.mean(res[p]) - np.min(res[p]) for p in ps]
    hi = [np.max(res[p]) - np.mean(res[p]) for p in ps]
    ax.errorbar(ps, means, yerr=[lo, hi], fmt="o-", ms=4.5, lw=1.3, capsize=3.0,
                color=bs.BLUE, ecolor="#9aa7b5", elinewidth=0.9, label="QAOA")
    ax.axhline(0.8786, color=bs.RED, lw=1.0, ls=(0, (5, 3)))
    ax.text(1.02, 0.892, "Goemans-Williamson 0.878", fontsize=7.0, color="#8a3a25")
    ax.set_xlabel("QAOA 层数 $p$")
    ax.set_ylabel("近似比（相对精确最优解）")
    ax.set_xticks(ps)
    ax.set_xlim(0.6, 3.4)
    ax.set_ylim(0.55, 1.02)
    ax.text(0.03, 0.06, "12 顶点随机三正则图，6 张图求平均，误差棒为极值", transform=ax.transAxes,
            fontsize=6.9, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig01")


def random_circuit_state(n, angles, depth, rng):
    dim = 1 << n
    idx = np.arange(dim)
    state = np.zeros(dim, dtype=complex)
    state[0] = 1.0
    for layer in range(depth):
        for q in range(n):
            th = angles[layer, q]
            c, s = np.cos(th / 2), np.sin(th / 2)
            m = (idx >> q) & 1
            i0, i1 = idx[m == 0], idx[m == 1]
            a0, a1 = state[i0].copy(), state[i1].copy()
            state[i0] = c * a0 + s * a1
            state[i1] = -s * a0 + c * a1
        for q in range(n - 1):
            sel = idx[((idx >> q) & 1) == 1]
            tgt = sel ^ (1 << (q + 1))
            tmp = state[sel].copy()
            state[sel] = state[tgt]
            state[tgt] = tmp
    return state


def cost_value(state, n):
    idx = np.arange(1 << n)
    par = np.ones(1 << n)
    for q in range(n):
        par *= 1 - 2 * ((idx >> q) & 1)
    return float((np.abs(state) ** 2 * par).sum())


def fig_gradient():
    ns = np.arange(4, 13)
    rng = np.random.default_rng(11)
    var = []
    for n in ns:
        depth = n
        grads = []
        for _ in range(30):
            angles = rng.uniform(0, 2 * np.pi, size=(depth, n))
            base = angles.copy()
            angles[0, 0] = base[0, 0] + np.pi / 2
            plus = cost_value(random_circuit_state(n, angles, depth, rng), n)
            angles[0, 0] = base[0, 0] - np.pi / 2
            minus = cost_value(random_circuit_state(n, angles, depth, rng), n)
            grads.append((plus - minus) / 2)
        var.append(np.var(grads))
        print(f"n={n}: 方差 {var[-1]:.3e}")

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.semilogy(ns, var, "o", ms=4.2, color=bs.RED, label="实测方差")
    fit = np.polyfit(ns, np.log10(var), 1)
    ax.semilogy(ns, 10 ** (fit[0] * ns + fit[1]), "-", lw=1.0, color=bs.GRAY,
                label=f"拟合斜率 {fit[0]:.2f}")
    ax.set_xlabel("比特数 $n$")
    ax.set_ylabel("梯度方差")
    ax.set_xticks(ns)
    ax.set_xlim(3.5, 12.5)
    ax.legend(loc="lower left", fontsize=7.6, handlelength=1.8)
    ax.text(0.97, 0.94, "随机线路，全局代价 $Z^{\\otimes n}$", transform=ax.transAxes,
            fontsize=6.9, color="#6b7785", ha="right")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_qaoa()
    fig_gradient()
