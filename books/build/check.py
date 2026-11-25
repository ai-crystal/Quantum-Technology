"""交付前体检：检查各册链接、图片、标题与 PDF。"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BOOKS = os.path.join(ROOT, "books")
OUT = os.path.join(ROOT, "output")
ORDER = ["intro", "foundations", "computing", "devices", "qec", "network"]

problems = []


def check_links(path, base_dir):
    text = open(path, encoding="utf-8").read()
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = m.group(1)
        if target.startswith(("http", "#", "mailto", "/#")):
            continue
        if target.startswith("/"):
            p = os.path.join(ROOT, target.lstrip("/"))
        else:
            p = os.path.join(base_dir, target.split("#")[0])
        if not os.path.exists(p):
            problems.append("死链 %s -> %s" % (os.path.relpath(path, ROOT), target))


def check_chapters(name):
    d = os.path.join(BOOKS, name)
    st = json.load(open(os.path.join(d, "structure.json"), encoding="utf-8"))
    for part in st["parts"]:
        for ch in part["chapters"]:
            p = os.path.join(d, "chapters", ch + ".md")
            if not os.path.exists(p):
                problems.append("缺章 %s/%s" % (name, ch))
                continue
            text = open(p, encoding="utf-8").read()
            for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
                img = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
                if not os.path.exists(img):
                    problems.append("缺图 %s -> %s" % (os.path.relpath(p, ROOT), m.group(1)))
            for line in text.split("\n"):
                if line.startswith("#"):
                    if re.search(r"[*|$:?]", line):
                        problems.append("标题特殊字符 %s: %s" % (os.path.relpath(p, ROOT), line[:40]))
                    if line.count("*") % 2:
                        problems.append("标题星号不成对 %s" % os.path.relpath(p, ROOT))
            if text.count("```") % 2:
                problems.append("代码块未闭合 %s" % os.path.relpath(p, ROOT))


def main():
    for name in ORDER:
        d = os.path.join(BOOKS, name)
        meta = json.load(open(os.path.join(d, "book.json"), encoding="utf-8"))
        pdf = os.path.join(OUT, meta["pdf"])
        if not os.path.exists(pdf):
            problems.append("缺 PDF %s" % meta["pdf"])
        else:
            try:
                import pymupdf
                doc = pymupdf.open(pdf)
                if len(doc) < 10:
                    problems.append("PDF 页数异常 %s" % meta["pdf"])
                if len(doc.get_toc()) < 5:
                    problems.append("PDF 书签过少 %s" % meta["pdf"])
            except Exception as e:
                problems.append("PDF 打不开 %s: %s" % (meta["pdf"], e))
        check_chapters(name)
        check_links(os.path.join(d, "README.md"), d)
        check_links(os.path.join(d, "_sidebar.md"), d)

    check_links(os.path.join(ROOT, "README.md"), ROOT)
    check_links(os.path.join(ROOT, "_sidebar.md"), ROOT)
    check_links(os.path.join(ROOT, "_coverpage.md"), ROOT)

    if problems:
        print("发现 %d 个问题：" % len(problems))
        for p in problems[:40]:
            print("  -", p)
    else:
        print("体检通过：6 册章节、插图、PDF、站内链接均正常")


if __name__ == "__main__":
    main()
