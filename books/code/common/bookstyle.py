"""全书插图统一样式与输出工具。

所有图的标题都写在正文图题里，图内不放标题，避免与图题重复。
线图存为量化 PNG，热图/照片类存为 JPEG，控制整书体积。
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

CH = None  # 由各章脚本设置

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BOOK = "intro"
IMG_DIR = os.path.join(ROOT, "books", BOOK, "images")


def use(book):
    """切换当前分册，插图输出到 books/<book>/images。"""
    global BOOK, IMG_DIR
    BOOK = book
    IMG_DIR = os.path.join(ROOT, "books", book, "images")

BLUE = "#2b5c94"
RED = "#b4462f"
GREEN = "#3d7a5a"
ORANGE = "#c07a1e"
PURPLE = "#6a4b8f"
GRAY = "#6b7785"
LIGHT = "#dfe6ee"
INK = "#1f2a37"

rcParams.update({
    "font.family": "Microsoft YaHei",
    "font.size": 9,
    "axes.labelsize": 9.5,
    "axes.titlesize": 9.5,
    "legend.fontsize": 8,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#4a5563",
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": "#4a5563",
    "ytick.color": "#4a5563",
    "axes.grid": False,
    "grid.color": "#d9e0e8",
    "grid.linewidth": 0.6,
    "legend.frameon": False,
    "axes.unicode_minus": False,
    "mathtext.fontset": "dejavusans",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
    "figure.dpi": 200,
})


def clean(ax, grid_axis=None, top=False, right=False):
    ax.spines["top"].set_visible(top)
    ax.spines["right"].set_visible(right)
    if grid_axis:
        ax.grid(True, axis=grid_axis, alpha=0.55, zorder=0)
        ax.set_axisbelow(True)
    return ax


def save(fig, chapter, name, kind="line", dpi=200, max_kb=260):
    """保存图片到 book/images/<chapter>/<name>.<ext>，并压缩到体积上限内。"""
    from PIL import Image

    folder = os.path.join(IMG_DIR, chapter)
    os.makedirs(folder, exist_ok=True)
    base = os.path.join(folder, name)
    png_tmp = base + "_raw.png"
    fig.savefig(png_tmp, dpi=dpi, facecolor="white")
    plt.close(fig)

    if kind == "photo":
        ext = ".jpg"
        img = Image.open(png_tmp).convert("RGB")
        quality = 84
        img.save(base + ext, "JPEG", quality=quality, optimize=True, progressive=True)
        while os.path.getsize(base + ext) > max_kb * 1024 and quality > 50:
            quality -= 6
            img.save(base + ext, "JPEG", quality=quality, optimize=True, progressive=True)
    else:
        ext = ".png"
        img = Image.open(png_tmp).convert("RGB")
        if img.width > 1500:
            img = img.resize((1500, round(img.height * 1500 / img.width)), Image.LANCZOS)
        colors = 192
        while True:
            q = img.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE)
            q.save(base + ext, "PNG", optimize=True)
            if os.path.getsize(base + ext) <= max_kb * 1024 or colors <= 32:
                break
            colors = max(32, colors // 2)
    os.remove(png_tmp)
    size_kb = os.path.getsize(base + ext) / 1024.0
    print(f"  {os.path.relpath(base + ext, ROOT)}  {size_kb:.0f} KB")
    return base + ext
