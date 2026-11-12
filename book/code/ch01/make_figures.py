"""第一章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
from matplotlib.gridspec import GridSpec

import bookstyle as bs

CH = "01"


def fig_spectrum():
    bands = [
        ("伽马射线", 1e-13, 1e-11, "#8f6bb0", True),
        ("X 射线", 1e-11, 1e-8, "#5f7fb8", True),
        ("紫外", 1e-8, 3.8e-7, "#4f8fc0", True),
        ("可见光", 3.8e-7, 7.5e-7, "#3f9c6a", False),
        ("红外", 7.5e-7, 1e-3, "#c07a1e", True),
        ("微波", 1e-3, 1e-1, "#a85a3c", True),
        ("无线电波", 1e-1, 1e4, "#7a6a5c", True),
    ]
    fig = plt.figure(figsize=(7.0, 2.5))
    gs = GridSpec(2, 1, height_ratios=[1.0, 0.55], hspace=0.62, figure=fig)
    ax = fig.add_subplot(gs[0])
    ax.set_xscale("log")
    ax.set_xlim(1e-13, 1e4)
    ax.set_ylim(0, 1.35)
    ax.axis("off")

    y0, h = 0.42, 0.34
    for name, lo, hi, color, inside in bands:
        ax.add_patch(Rectangle((lo, y0), hi - lo, h, facecolor=color, edgecolor="white", linewidth=0.9))
        mid = np.sqrt(lo * hi)
        if inside:
            ax.text(mid, y0 + h / 2, name, ha="center", va="center", color="white", fontsize=8)
        else:
            ax.annotate(name, xy=(hi, y0 + h), xytext=(1.6e-6, 0.98), ha="left", va="center",
                        fontsize=8, color="#33414f",
                        arrowprops=dict(arrowstyle="-|>", color="#8a95a3", lw=0.7,
                                        connectionstyle="angle,angleA=0,angleB=90,rad=0",
                                        shrinkA=2, shrinkB=1))

    ax.text(1e-13, y0 - 0.10, "波长 $10^{-13}$ m", fontsize=7.6, color="#66737f", ha="left", va="top")
    ax.text(1e4, y0 - 0.10, "$10^{4}$ m", fontsize=7.6, color="#66737f", ha="right", va="top")
    ax.annotate("", xy=(1e2, 0.07), xytext=(1e-9, 0.07),
                arrowprops=dict(arrowstyle="-|>", color="#9aa6b4", lw=0.9, shrinkA=0, shrinkB=0))
    ax.text(5e-4, 0.13, "频率升高", fontsize=7.6, color="#66737f", ha="center", va="bottom")

    ax2 = fig.add_subplot(gs[1])
    ax2.set_xlim(380, 750)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    for w in np.arange(380, 750, 0.5):
        if w < 440:
            r, g, b = (440 - w) / 60.0, 0.0, 1.0
        elif w < 490:
            r, g, b = 0.0, (w - 440) / 50.0, 1.0
        elif w < 510:
            r, g, b = 0.0, 1.0, (510 - w) / 20.0
        elif w < 580:
            r, g, b = (w - 510) / 70.0, 1.0, 0.0
        elif w < 645:
            r, g, b = 1.0, (645 - w) / 65.0, 0.0
        else:
            r, g, b = 1.0, 0.0, 0.0
        ax2.add_patch(Rectangle((w, 0.46), 0.55, 0.30, facecolor=(r, g, b), edgecolor="none"))
    for w, t in [(410, "紫"), (470, "蓝"), (530, "绿"), (585, "黄"), (665, "红")]:
        ax2.text(w, 0.30, t, ha="center", fontsize=7.8, color="#33414f")
    ax2.text(380, 0.86, "380 nm", fontsize=7.4, color="#66737f", ha="left")
    ax2.text(750, 0.86, "750 nm", fontsize=7.4, color="#66737f", ha="right")
    bs.save(fig, CH, "fig01")


def fig_double_slit():
    lam = 633e-9
    d = 0.12e-3
    a = 0.030e-3
    L = 1.2
    x = np.linspace(-12e-3, 12e-3, 4000)
    theta = np.arctan(x / L)
    beta = np.pi * a * np.sin(theta) / lam
    alpha = np.pi * d * np.sin(theta) / lam
    env = np.sinc(beta / np.pi) ** 2
    inten = env * np.cos(alpha) ** 2
    inten = inten / inten.max()

    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.plot(x * 1e3, inten, color=bs.RED, lw=1.1)
    ax.plot(x * 1e3, env, color=bs.GRAY, lw=0.9, ls=(0, (4, 3)))
    ax.axhline(0, color="#c9d2dc", lw=0.7)
    ax.set_xlabel("屏幕上位置 $x$ (mm)")
    ax.set_ylabel("相对光强")
    ax.set_xlim(-12, 12)
    ax.set_ylim(-0.03, 1.22)
    ax.annotate("单缝衍射包络", xy=(1.62, 0.55), xytext=(4.6, 0.72), fontsize=8, color="#4a5563",
                arrowprops=dict(arrowstyle="-|>", color="#8a95a3", lw=0.7, connectionstyle="arc3,rad=0.2"))
    ax.annotate("", xy=(0, 1.12), xytext=(6.33, 1.12),
                arrowprops=dict(arrowstyle="<|-|>", color=bs.BLUE, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(3.15, 1.15, "相邻明纹间距 6.3 mm", ha="center", va="bottom", fontsize=8, color=bs.BLUE)
    bs.clean(ax, grid_axis="y")
    bs.save(fig, CH, "fig02")


def fig_refraction():
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.85, 0.95)
    ax.axis("off")

    ax.add_patch(Rectangle((-1.1, -0.85), 2.2, 0.85, facecolor="#e9f2fa", edgecolor="none"))
    ax.plot([-1.1, 1.1], [0, 0], color=bs.BLUE, lw=1.3)
    ax.text(-1.04, 0.09, "空气  $n_1 = 1.00$", fontsize=8.4, color="#3a4a5c")
    ax.text(-1.04, -0.20, "水  $n_2 = 1.33$", fontsize=8.4, color="#3a4a5c")

    p_in = (-0.70, 0.83)
    ax.annotate("", xy=(0, 0), xytext=p_in,
                arrowprops=dict(arrowstyle="-|>", color=bs.ORANGE, lw=1.7, shrinkA=0, shrinkB=0))
    ax.text(p_in[0] - 0.02, p_in[1] + 0.06, "入射光", fontsize=8.4, color=bs.ORANGE, ha="left")

    ax.annotate("", xy=(0.60, -0.715), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=bs.RED, lw=1.7, shrinkA=0, shrinkB=0))
    ax.text(0.62, -0.78, "折射光", fontsize=8.4, color=bs.RED, ha="left")

    ax.plot([0, 0], [0.90, -0.80], color="#7b8794", lw=0.8, ls=(0, (2.5, 2.5)))
    ax.text(0.04, 0.80, "法线", fontsize=8.2, color="#7b8794")

    r = 0.42
    ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=90, theta2=125, color=bs.ORANGE, lw=0.9))
    ax.text(-0.30, 0.50, r"$\theta_1$", fontsize=9.5, color=bs.ORANGE, ha="center", va="center")
    ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=270, theta2=308, color=bs.RED, lw=0.9))
    ax.text(0.30, -0.52, r"$\theta_2$", fontsize=9.5, color=bs.RED, ha="center", va="center")

    ax.text(-1.02, -0.64, "入射角 45°，折射角 32°", fontsize=8.2, color="#4a5563", ha="left", va="center")
    bs.save(fig, CH, "fig03")


if __name__ == "__main__":
    fig_spectrum()
    fig_double_slit()
    fig_refraction()
