"""第十八章插图：量子核的线路结构、我们自己做的小规模对照实验。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import bookstyle as bs

bs.use("computing")
CH = "18"

N_QUBIT = 4


def ry(state, q, th, n):
    idx = np.arange(1 << n)
    m = (idx >> q) & 1
    i0, i1 = idx[m == 0], idx[m == 1]
    c, s = np.cos(th / 2), np.sin(th / 2)
    a0, a1 = state[i0].copy(), state[i1].copy()
    state[i0] = c * a0 + s * a1
    state[i1] = -s * a0 + c * a1


def rz_diag(state, q, th, n):
    idx = np.arange(1 << n)
    sign = 1 - 2 * ((idx >> q) & 1)
    state *= np.exp(-0.5j * th * sign)


def zz_diag(state, a, b, th, n):
    idx = np.arange(1 << n)
    za = 1 - 2 * ((idx >> a) & 1)
    zb = 1 - 2 * ((idx >> b) & 1)
    state *= np.exp(-0.5j * th * za * zb)


def feature_state(x, n=N_QUBIT, reps=2):
    """ZZ 特征映射，两个特征轮流上传到 n 个比特上。"""
    dim = 1 << n
    state = np.zeros(dim, dtype=complex)
    state[0] = 1.0
    for _ in range(reps):
        for q in range(n):
            ry(state, q, np.pi / 2, n)
            rz_diag(state, q, 2.0 * x[q % len(x)], n)
        for a in range(n - 1):
            zz_diag(state, a, a + 1, (np.pi - x[a % len(x)]) * (np.pi - x[(a + 1) % len(x)]), n)
    return state


def kernel_matrix(X):
    V = np.array([feature_state(x) for x in X])
    K = np.abs(V.conj() @ V.T) ** 2
    return K


def rbf_matrix(X, Y=None, gamma=None):
    if Y is None:
        Y = X
    d2 = ((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1)
    if gamma is None:
        med = np.median(d2[d2 > 0])
        gamma = 1.0 / med
    return np.exp(-gamma * d2)


def moons(n, noise=0.09, seed=0):
    rng = np.random.default_rng(seed)
    half = n // 2
    t1 = np.linspace(0, np.pi, half)
    t2 = np.linspace(0, np.pi, n - half)
    x1 = np.stack([np.cos(t1), np.sin(t1)], 1) + rng.normal(0, noise, (half, 2))
    x2 = np.stack([1 - np.cos(t2), 0.5 - np.sin(t2)], 1) + rng.normal(0, noise, (n - half, 2))
    X = np.vstack([x1, x2])
    y = np.array([0] * half + [1] * (n - half))
    perm = rng.permutation(n)
    return X[perm], y[perm]


def fig_circuit():
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9),
                             gridspec_kw={"width_ratios": [1.22, 1.0]})

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.3, 4.6)
    ax.axis("off")
    for q in range(N_QUBIT):
        y = 4.0 - q
        ax.plot([0.9, 8.9], [y, y], color="#5c6b7a", lw=1.0)
        ax.text(0.62, y, rf"$q_{q}$", fontsize=8.0, ha="right", va="center", color="#33414f")

    def block(x, w, label, fc, ec):
        ax.add_patch(FancyBboxPatch((x - w / 2, 0.45), w, 3.4,
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=fc, edgecolor=ec, lw=1.0, zorder=3))
        ax.text(x, 2.15, label, fontsize=9.6, ha="center", va="center", zorder=4)

    block(2.55, 1.55, r"$U_\Phi(x)$", "#eaf1f9", "#4a6f9c")
    block(5.55, 1.75, r"$U_\Phi^{\dagger}(x')$", "#eef3ee", "#5f7d5f")
    ax.add_patch(FancyBboxPatch((7.05 - 0.55, 0.45), 1.1, 3.4,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#f6f1e6", edgecolor="#8a7a55", lw=1.0, zorder=3))
    ax.text(7.05, 2.15, "测量", fontsize=8.4, ha="center", va="center", zorder=4)
    ax.text(5.0, 0.02, r"$p(0\cdots0)=|\langle\varphi(x)|\varphi(x')\rangle|^2$", fontsize=8.4,
            ha="center", va="center")
    ax.text(1.0, 4.55, "初态 $|0\\rangle$；每层先 $R_y(\\pi/2)$ 与 $R_z(2x_i)$，再加一圈 $ZZ$ 纠缠", fontsize=7.0,
            ha="left", va="center", color="#6b7785")

    ax = axes[1]
    X, y = moons(24, seed=3)
    Xs = X * 1.0
    K = kernel_matrix(Xs)
    order = np.argsort(y, kind="stable")
    K = K[np.ix_(order, order)]
    im = ax.imshow(K, cmap="Blues", vmin=0, vmax=1)
    ax.set_xlabel("样本序号")
    ax.set_ylabel("样本序号")
    ax.set_xticks([0, 12, 23])
    ax.set_yticks([0, 12, 23])
    ax.axhline(11.5, color="#8a3a25", lw=0.8, ls=(0, (3, 3)))
    ax.axvline(11.5, color="#8a3a25", lw=0.8, ls=(0, (3, 3)))
    ax.text(5.0, -1.6, "类 0", fontsize=7.0, ha="center", color="#8a3a25")
    ax.text(17.5, -1.6, "类 1", fontsize=7.0, ha="center", color="#8a3a25")
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_label("核值", fontsize=7.6)
    cb.ax.tick_params(labelsize=7.0)

    fig.tight_layout(w_pad=1.0)
    bs.save(fig, CH, "fig01")


def kernel_ridge_predict(K_train, y_train, K_test, lam=1e-3):
    Y = np.zeros((len(y_train), 2))
    Y[np.arange(len(y_train)), y_train] = 1.0
    alpha = np.linalg.solve(K_train + lam * np.eye(len(K_train)), Y)
    return np.argmax(K_test @ alpha, axis=1)


def fig_accuracy():
    X, y = moons(120, seed=1)
    X = (X - X.mean(0)) / X.std(0)
    Xq = (X - X.min(0)) / (X.max(0) - X.min(0)) * np.pi
    Kq = kernel_matrix(Xq)
    Kc = rbf_matrix(X)

    sizes = [8, 16, 24, 32, 40]
    res_q, res_c = [], []
    rng = np.random.default_rng(5)
    for m in sizes:
        aq, ac = [], []
        for _ in range(25):
            perm = rng.permutation(len(y))
            tr, te = perm[:m], perm[m:m + 40]
            pred = kernel_ridge_predict(Kq[np.ix_(tr, tr)], y[tr], Kq[np.ix_(te, tr)])
            aq.append(np.mean(pred == y[te]))
            pred = kernel_ridge_predict(Kc[np.ix_(tr, tr)], y[tr], Kc[np.ix_(te, tr)])
            ac.append(np.mean(pred == y[te]))
        res_q.append(np.mean(aq))
        res_c.append(np.mean(ac))
        print(f"训练 {m}: 量子核 {res_q[-1]:.3f}, 经典核 {res_c[-1]:.3f}")

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(sizes, res_q, "-o", ms=3.6, lw=1.3, color=bs.BLUE, label="量子核（4 比特特征映射）")
    ax.plot(sizes, res_c, "-s", ms=3.4, lw=1.3, color=bs.GREEN, label="经典 RBF 核")
    ax.set_xlabel("训练样本数")
    ax.set_ylabel("测试集准确率")
    ax.set_xticks(sizes)
    ax.set_xlim(6, 42)
    ax.set_ylim(0.6, 1.02)
    ax.legend(loc="lower right", fontsize=7.4, handlelength=1.8)
    ax.text(0.03, 0.08, "两月牙数据，各 60 个样本，25 次随机划分", transform=ax.transAxes,
            fontsize=6.9, color="#6b7785")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_circuit()
    fig_accuracy()
