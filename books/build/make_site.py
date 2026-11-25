# -*- coding: utf-8 -*-
"""生成系列首页、根侧栏与各册 README。"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BOOKS = os.path.join(ROOT, "books")
OUT = os.path.join(ROOT, "output")

ORDER = ["intro", "foundations", "computing", "devices", "qec", "network"]


def load(name):
    d = os.path.join(BOOKS, name)
    meta = json.load(open(os.path.join(d, "book.json"), encoding="utf-8"))
    st = json.load(open(os.path.join(d, "structure.json"), encoding="utf-8"))
    chapters = []
    for part in st["parts"]:
        for ch in part["chapters"]:
            p = os.path.join(d, "chapters", ch + ".md")
            title = ch
            if os.path.exists(p):
                first = open(p, encoding="utf-8").readline().strip()
                m = re.match(r"#\s*(.+)", first)
                if m:
                    title = m.group(1).strip()
            chapters.append((ch, title))
    pages = None
    pdf = os.path.join(OUT, meta["pdf"])
    if os.path.exists(pdf):
        try:
            import pymupdf
            pages = len(pymupdf.open(pdf))
        except Exception:
            pages = None
    return meta, chapters, pages


def main():
    data = []
    for name in ORDER:
        if os.path.isdir(os.path.join(BOOKS, name)):
            data.append((name,) + load(name))

    # 根侧栏：系列导航
    lines = ["- [系列首页](/README.md)", ""]
    for name, meta, chapters, pages in data:
        lines.append("- **%s %s**" % (meta["volume"], meta["title"]))
        lines.append("  - [本册首页](/books/%s/README.md)" % name)
        for ch, title in chapters:
            lines.append("  - [%s](/books/%s/chapters/%s.md)" % (title, name, ch))
        lines.append("  - [下载 PDF](/output/%s)" % meta["pdf"])
    open(os.path.join(ROOT, "_sidebar.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # 首页
    rows = []
    for name, meta, chapters, pages in data:
        rows.append("| %s | %s | %s | %s | [阅读](/books/%s/README.md) | [PDF](/output/%s) |" % (
            meta["volume"], meta["title"], meta["subtitle"],
            str(pages) + " 页" if pages else "待生成", name, meta["pdf"]))
    readme = """# 量子学技术

> 一套讲量子技术的书　·　作者 Dr. Dezeming

量子技术不只是量子计算。它还包括量子通信、量子精密测量、量子器件与量子纠错。这套书按这个范围展开，一册入门铺全貌，其余各册钻进具体方向。

## 分册

| 册 | 书名 | 副标题 | 篇幅 | 在线阅读 | 下载 |
|---|---|---|---|---|---|
%s

## 怎么读

第一册是入门，从黑体辐射讲到量子芯片，把整个领域的脉络走一遍，不深究细节。后面几册各自独立，可以按兴趣挑着读，不必按顺序。

每一册的正文都在 `books/<册名>/chapters/`，插图在 `books/<册名>/images/`，绘图代码在 `books/code/<册名>/`。站点直接引用这些文件，没有第二份副本。

## 构建

双击根目录的 `build.bat` 构建全部，或 `build-<册名>.bat` 只构建某一册。
""" % "\n".join(rows)
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)

    # 各册首页
    for name, meta, chapters, pages in data:
        first = chapters[0][0] if chapters else "ch01"
        items = "\n".join("- [%s](chapters/%s.md)" % (t, c) for c, t in chapters)
        book_readme = """# %s

> %s　·　%s

%s

## 在线阅读

- [从第 1 章开始](chapters/%s.md)
- [下载本册 PDF](/output/%s)

## 目录

%s
""" % (meta["title"], meta["volume"], meta["subtitle"],
            meta.get("blurb", ""), first, meta["pdf"], items)
        open(os.path.join(BOOKS, name, "README.md"), "w", encoding="utf-8").write(book_readme)

    print("站点文件已生成：%d 册" % len(data))


if __name__ == "__main__":
    main()
