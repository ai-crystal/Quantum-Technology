"""第 18 章插图。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "common"))

import numpy as np
import matplotlib.pyplot as plt

import bookstyle as bs

bs.use("devices")

CH = "18"

KB = 8.617333e-5  # eV/K


def lorentz(x, gamma):
    return (gamma / np.pi) / (x ** 2 + gamma ** 2)


def fig_map():
    v = np.linspace(-0.32, 0.32, 500)
    b = np.linspace(0, 2.0, 400)
    V, B = np.meshgrid(v, b)
    delta = 0.22
    bc = 1.0
    gam = 0.018

    ea = np.clip(delta * (1 - (B / bc) ** 1.4), 0.0, delta)
    topo = 1.0 / (1.0 + np.exp(-(B - bc) / 0.07))
    delta_b = delta * (1 - 0.45 * topo)

    g = 0.55 * (lorentz(V - delta_b, gam) + lorentz(V + delta_b, gam))
    g += 0.40 * (lorentz(V - ea, gam * 1.6) + lorentz(V + ea, gam * 1.6)) * (1 - topo)
    g += 1.5 * topo * lorentz(V, gam)

    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    m = g.max()
    im = ax.pcolormesh(V, B, g, cmap="magma", vmin=0, vmax=m * 0.75, shading="auto",
                       rasterized=True)
    ax.axhline(bc, color="#e8eef6", lw=0.7, ls=(0, (4, 3)))
    ax.text(-0.31, bc + 0.05, r"$B_c$", fontsize=8, color="#e8eef6")
    ax.set_xlim(-0.32, 0.32)
    ax.set_ylim(0, 2.0)
    ax.set_xlabel("偏压（meV）")
    ax.set_ylabel("平行磁场（T）")
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("微分电导（任意单位）", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    bs.save(fig, CH, "fig01", kind="photo")


def fig_quantization():
    fig = plt.figure(figsize=(7.0, 2.8))
    gs = fig.add_gridspec(1, 2, wspace=0.32)

    ax = fig.add_subplot(gs[0, 0])
    ratio = np.logspace(-2, 2, 400)
    g = 4 * ratio / (1 + ratio) ** 2
    ax.semilogx(ratio, g, color=bs.BLUE, lw=1.4)
    ax.axhline(1.0, color="#8a97a6", lw=0.7, ls=(0, (4, 3)))
    ax.text(0.02, 1.04, r"$2e^2/h$", fontsize=8, color="#4a5563")
    ax.set_xlim(1e-2, 1e2)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel(r"两端耦合强度之比 $\Gamma_L/\Gamma_R$")
    ax.set_ylabel(r"零偏压电导 $G/G_0$")
    bs.clean(ax, grid_axis="y")

    ax2 = fig.add_subplot(gs[0, 1])
    v = np.linspace(-0.12, 0.12, 600)
    gam_mev = 0.012
    e = np.linspace(-0.4, 0.4, 4000)
    peak0 = lorentz(0.0, gam_mev)
    for t_mk, col in [(20, bs.BLUE), (60, bs.GREEN), (120, bs.ORANGE), (250, bs.RED)]:
        kt = KB * t_mk * 1e-3 * 1e3  # meV
        dfdv = 1.0 / (4 * kt) / np.cosh((e[None, :] - v[:, None]) / (2 * kt)) ** 2
        gg = np.trapezoid(lorentz(e, gam_mev)[None, :] * dfdv, e, axis=1)
        ax2.plot(v * 1e3, gg / peak0, color=col, lw=1.3, label="%d mK" % t_mk)
    ax2.set_xlim(-120, 120)
    ax2.set_ylim(0, 1.05)
    ax2.set_xlabel(r"偏压（$\mu$eV）")
    ax2.set_ylabel(r"峰高（相对零温值）")
    ax2.legend(loc="upper right", fontsize=7.4)
    bs.clean(ax2, grid_axis="y")
    bs.save(fig, CH, "fig02")


if __name__ == "__main__":
    fig_map()
    fig_quantization()
