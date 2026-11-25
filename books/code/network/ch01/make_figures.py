"""第 1 章插图：破解大数分解的代价、一次性密码本的密钥消耗。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "01"


def fig_cost():
    n = np.linspace(512, 8192, 500)
    nb = n * np.log(2.0)
    # 数域筛法的启发式复杂度 L_n = exp(1.923 n^(1/3) (ln n)^(2/3))
    ops_classical = np.exp(1.923 * nb ** (1 / 3) * np.log(nb) ** (2 / 3))
    # Shor 算法：模幂运算的门数与位数三次方成正比，取 72 n^3
    ops_quantum = 72.0 * n ** 3

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    ax.semilogy(n, ops_classical, color=bs.RED, lw=1.5, label="经典数域筛法")
    ax.semilogy(n, ops_quantum, color=bs.BLUE, lw=1.5, label="Shor 算法")
    for mark in (2048, 4096):
        ax.axvline(mark, color="#c3ccd6", lw=0.7, ls=(0, (4, 3)), zorder=0)
        ax.text(mark + 70, 3e8, f"{mark} 位", fontsize=8, color="#4a5563")

    ax.set_xlim(500, 8200)
    ax.set_ylim(1e7, 1e70)
    ax.set_xlabel("模数位数")
    ax.set_ylabel("破解所需的运算次数")
    ax.set_xticks([512, 1024, 2048, 4096, 6144, 8192])
    ax.legend(loc="upper left")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


def fig_otp():
    data_mb = np.logspace(0, 6, 300)  # 1 MB 到 1 TB
    key_otp = data_mb
    key_aes = np.full_like(data_mb, 32.0 / 1048576.0)  # 32 字节换算成 MB

    fig, ax = plt.subplots(figsize=(6.0, 3.1))
    ax.loglog(data_mb, key_otp, color=bs.RED, lw=1.6, label="一次性密码本，密钥与数据等长")
    ax.loglog(data_mb, key_aes, color=bs.BLUE, lw=1.6, label="AES-256，固定 32 字节密钥")
    ax.set_xlim(1, 1e6)
    ax.set_ylim(1e-6, 1e7)
    ax.set_xlabel("需要加密的数据量（MB）")
    ax.set_ylabel("需要的密钥量（MB）")

    ax.plot([1e6], [1e6], "o", ms=4.5, color=bs.RED)
    ax.annotate("1 TB 数据\n需要 1 TB 密钥", xy=(1e6, 1e6), xytext=(3e3, 2.4e5),
                fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    ax.plot([1e6], [32 / 1048576], "o", ms=4.5, color=bs.BLUE)
    ax.annotate("同样 1 TB 数据\n密钥仍是 32 字节", xy=(1e6, 32 / 1048576), xytext=(2.2e3, 2e-4),
                fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-", color="#8a97a6", lw=0.7))
    ax.legend(loc="upper left")
    bs.clean(ax, grid_axis="both")
    bs.save(fig, CH, "fig01")


if __name__ == "__main__":
    fig_cost()
    fig_otp()
