"""第 6 章插图：后量子方案的密钥与签名尺寸、破解 RSA-2048 的规模估算。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("network")

CH = "06"


def fig_sizes():
    names = ["ECDH P-256", "RSA-2048", "ML-KEM-768", "ML-DSA-65", "SLH-DSA-128s"]
    public = np.array([64, 256, 1184, 1952, 32])
    other = np.array([64, 256, 1088, 3309, 7856])

    y = np.arange(len(names))[::-1]
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    h = 0.34
    ax.barh(y + h / 2, public, height=h, color=bs.BLUE, label="公钥", alpha=0.9)
    ax.barh(y - h / 2, other, height=h, color=bs.ORANGE, label="密文或签名", alpha=0.9)

    for yy, v in zip(y + h / 2, public):
        ax.text(v * 1.12, yy, f"{v} B", va="center", fontsize=7.6, color=bs.BLUE)
    for yy, v in zip(y - h / 2, other):
        ax.text(v * 1.12, yy, f"{v} B", va="center", fontsize=7.6, color=bs.ORANGE)

    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xscale("log")
    ax.set_xlim(20, 22000)
    ax.set_xlabel("字节数（对数刻度）")
    ax.legend(loc="upper right")
    bs.clean(ax, grid_axis="x")
    bs.save(fig, CH, "fig01")


def fig_qubits():
    d = np.array([17, 19, 21, 23, 25, 27])
    logical = 4096
    phys = logical * 2 * d ** 2

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    idx = np.arange(len(d))
    ax.vlines(idx, 200, phys, color=bs.PURPLE, lw=2.2, alpha=0.55)
    ax.plot(idx, phys, "o", ms=6, color=bs.PURPLE)
    for i, v in enumerate(phys):
        ax.text(i, v * 1.22, f"{v/1e6:.1f} M", ha="center", fontsize=7.8,
                color="#4a5563")

    ax.axhline(1e3, color=bs.RED, lw=1.0, ls=(0, (5, 3)))
    ax.text(-0.42, 1.40e3, "目前最大的超导处理器，约一千个物理比特", fontsize=8,
            color=bs.RED, bbox=dict(facecolor="white", edgecolor="none", pad=1.2))

    ax.set_yscale("log")
    ax.set_ylim(200, 2.2e7)
    ax.set_xlim(-0.6, 5.6)
    ax.set_xticks(idx)
    ax.set_xticklabels([f"$d={k}$" for k in d])
    ax.set_xlabel("表面码的码距")
    ax.set_ylabel("所需物理比特")
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_sizes()
    fig_qubits()
