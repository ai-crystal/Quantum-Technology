"""第十六章插图：Jordan-Wigner 展开后的泡利项数、活性空间的希尔伯特空间维数。"""
import os
import sys
from math import comb

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("computing")
CH = "16"

I_, X_, Y_, Z_ = 1, 2, 3, 4
MUL = {
    (X_, Y_): (1j, Z_), (Y_, X_): (-1j, Z_),
    (Y_, Z_): (1j, X_), (Z_, Y_): (-1j, X_),
    (Z_, X_): (1j, Y_), (X_, Z_): (-1j, Y_),
}


def mul(a, b):
    """两个泡利串相乘，a、b 是 (系数, {位置: 字母}) 的二元组。"""
    ca, pa = a
    cb, pb = b
    out = dict(pa)
    coef = ca * cb
    for k, v in pb.items():
        u = out.get(k, I_)
        if u == I_:
            out[k] = v
        elif v == I_:
            pass
        elif u == v:
            out[k] = I_
        else:
            ph, w = MUL[(u, v)]
            coef *= ph
            out[k] = w
    return coef, {k: v for k, v in out.items() if v != I_}


def term_strings(factors):
    """把一串因子的乘积展开成泡利串之和。"""
    acc = [(1.0, {})]
    for f in factors:
        nxt = []
        for a in acc:
            for b in f:
                nxt.append(mul(a, b))
        acc = nxt
    return acc


def op_a(j, dagger):
    """Jordan-Wigner 下的 a_j（dagger=False）或 a_j^dagger。"""
    z = (1.0, {k: Z_ for k in range(j)})
    s = -1j if dagger else 1j          # (X ∓ iY)/2 里的虚数部分
    x = (0.5, {j: X_})
    y = (0.5 * s, {j: Y_})
    return [mul(z, x), mul(z, y)]


def count_terms(n, seed=0):
    rng = np.random.default_rng(seed)
    h1 = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h1 = 0.5 * (h1 + h1.conj().T)
    h2 = rng.normal(size=(n, n, n, n)) + 1j * rng.normal(size=(n, n, n, n))
    h2 = 0.25 * (h2 + h2.transpose(1, 0, 3, 2) + h2.conj().transpose(3, 2, 1, 0)
                 + h2.conj().transpose(2, 3, 0, 1))

    out = {}

    def add(strings, coef):
        for c, p in strings:
            key = tuple(sorted(p.items()))
            out[key] = out.get(key, 0.0) + coef * c

    for p in range(n):
        for q in range(n):
            add(term_strings([op_a(p, True), op_a(q, False)]), h1[p, q])
    for p in range(n):
        for q in range(n):
            for r in range(n):
                for s in range(n):
                    c = h2[p, q, r, s]
                    if abs(c) < 1e-12:
                        continue
                    add(term_strings([op_a(p, True), op_a(q, True),
                                      op_a(r, False), op_a(s, False)]), c)
    return sum(1 for v in out.values() if abs(v) > 1e-10)


def fig_terms():
    ns = np.array([4, 6, 8, 10, 12, 14, 16])
    counts = [count_terms(int(n)) for n in ns]
    for n, c in zip(ns, counts):
        print(f"N={n}: {c} 项, 与 N^4 之比 {c / n ** 4:.2f}")

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.loglog(ns, counts, "-o", ms=3.4, lw=1.3, color=bs.BLUE, label="Jordan-Wigner 展开")
    ref = counts[0] * (ns / ns[0]) ** 4
    ax.loglog(ns, ref, "--", lw=1.0, color=bs.GRAY, label=r"按 $N^4$ 标度")
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns])
    ax.minorticks_off()
    ax.set_xlim(3.6, 17.5)
    ax.set_xlabel("自旋轨道数 $N$")
    ax.set_ylabel("泡利项数（系数非零）")
    ax.legend(loc="upper left", fontsize=7.8, handlelength=1.8)
    ax.text(0.97, 0.06, "随机一、二体系数，取 $|c|>10^{-10}$", transform=ax.transAxes,
            fontsize=7.0, color="#6b7785", ha="right")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


def format_big(v):
    if v < 1e5:
        return "%d" % int(round(v))
    exp = int(np.floor(np.log10(v)))
    mant = v / 10 ** exp
    return f"{mant:.1f} $\\times10^{{{exp}}}$"


def fig_cas():
    cases = [("N$_2$", 6, 6), ("H$_2$O", 8, 8), ("Cr$_2$", 12, 12),
             ("N$_2$ 大基组", 14, 14), ("FeMoco", 54, 54)]
    vals = [float(comb(2 * c[1], c[2])) for c in cases]
    fig, ax = plt.subplots(figsize=(5.9, 3.2))
    colors = [bs.BLUE] * (len(cases) - 1) + [bs.ORANGE]
    ax.bar(range(len(cases)), vals, width=0.58, color=colors, edgecolor="white", lw=0.6)
    for i, v in enumerate(vals):
        ax.text(i, v * 3.2, format_big(v), fontsize=7.2, ha="center", color=bs.INK)
    ax.set_yscale("log")
    ax.set_ylim(1e2, 1e34)
    ax.set_xticks(range(len(cases)))
    ax.set_xticklabels([c[0] + "\n" + f"CAS({c[1]},{c[2]})" for c in cases], fontsize=7.2)
    ax.set_ylabel("行列式个数")
    ax.axhline(1e9, color="#8a97a6", lw=0.8, ls=(0, (4, 3)))
    ax.text(0.55, 8e10, r"虚线是 $10^{9}$ 维，一个复向量就要 16 GB", fontsize=6.9,
            color="#6b7785", ha="left")
    bs.clean(ax)
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_terms()
    fig_cas()
