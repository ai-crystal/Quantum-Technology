"""第十章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

CH = "10"


def fig_bloch():
    fig = plt.figure(figsize=(5.2, 4.4))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 70)
    v = np.linspace(0, np.pi, 36)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color="#ccd8e5", linewidth=0.35, rstride=4, cstride=4)

    ax.plot([0, 0], [0, 0], [-1.12, 1.12], color="#8a95a3", lw=0.9)
    ax.plot([-1.12, 1.12], [0, 0], [0, 0], color="#dde3ea", lw=0.6, ls=(0, (2, 2)))
    ax.plot([0, 0], [-1.12, 1.12], [0, 0], color="#dde3ea", lw=0.6, ls=(0, (2, 2)))

    th, ph = np.deg2rad(58), np.deg2rad(32)
    vx, vy, vz = np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)
    ax.plot([0, vx], [0, vy], [0, vz], color=bs.RED, lw=2.4, solid_capstyle="round")
    ax.plot([vx], [vy], [vz], "o", ms=4.5, color=bs.RED)

    ax.plot([0, vx], [0, vy], [vz, vz], color="#9aa7b5", lw=0.6, ls=(0, (3, 2)))
    ax.plot([vx, vx], [vy, vy], [0, vz], color="#9aa7b5", lw=0.6, ls=(0, (3, 2)))
    ax.plot([0, vx], [0, vy], [0, 0], color="#9aa7b5", lw=0.6, ls=(0, (3, 2)))

    ax.text(0, 0, 1.28, r"$|0\rangle$", fontsize=11, color=bs.BLUE, ha="center")
    ax.text(0, 0, -1.36, r"$|1\rangle$", fontsize=11, color=bs.BLUE, ha="center")
    ax.text(vx * 1.24, vy * 1.24, vz * 1.24, r"$|\psi\rangle$", fontsize=11, color=bs.RED,
            ha="left", va="bottom")
    ax.text(vx * 0.14, vy * 0.14, vz * 0.72, r"$\theta$", fontsize=10, color="#4a5563", ha="center")
    ax.text(vx * 0.60, vy * 0.60, 0.08, r"$\varphi$", fontsize=10, color="#4a5563", ha="center")

    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=128)
    bs.save(fig, CH, "fig01")


def fig_theta():
    th = np.linspace(0, np.pi, 500)
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    ax.plot(th / np.pi, np.cos(th / 2) ** 2, color=bs.BLUE, lw=1.6, label=r"$P(0)=\cos^2(\theta/2)$")
    ax.plot(th / np.pi, np.sin(th / 2) ** 2, color=bs.RED, lw=1.4, ls=(0, (4, 3)),
            label=r"$P(1)=\sin^2(\theta/2)$")
    ax.axvline(0.5, color="#b9c3cf", lw=0.8, ls=(0, (2, 2)))
    ax.text(0.52, 0.88, r"$\theta=\pi/2$，两种结果各一半", fontsize=7.8, color="#4a5563")
    ax.set_xlabel(r"极角 $\theta/\pi$")
    ax.set_ylabel("测量概率")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.08)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.legend(loc="lower center", ncol=2, handlelength=1.8)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_bloch()
    fig_theta()
