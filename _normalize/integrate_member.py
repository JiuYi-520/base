# -*- coding: utf-8 -*-
"""
Integrate the new member-center HTML body and CSS into member-center.html.
- Replaces the existing <main class="mc-main">...</main> block.
- Replaces the existing .mc-* CSS block (from "/* ====== 会员中心主体样式" to just before </style>).
"""
import re
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "member-center.html")
NEW_HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "member_main.html")
NEW_CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "member_css.css")


def read(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def main():
    src = read(TARGET)
    new_html = read(NEW_HTML_PATH).strip()
    new_css = read(NEW_CSS_PATH).strip()

    # 1) Replace <main class="mc-main"> ... </main>
    main_re = re.compile(r"<main\s+class=\"mc-main\".*?</main>", re.DOTALL)
    if not main_re.search(src):
        sys.stderr.write("[ERROR] mc-main block not found\n")
        sys.exit(1)
    src2 = main_re.sub(new_html, src, count=1)

    # 2) Replace the .mc-* CSS block.
    #    Locate from the marker "/* ====== 会员中心主体样式" up to (and excluding) "</style>".
    #    We keep everything before the marker and replace from marker to "</style>".
    css_marker = "/* ====== 会员中心主体样式"
    style_close = "</style>"
    idx_marker = src2.find(css_marker)
    if idx_marker < 0:
        sys.stderr.write("[ERROR] CSS marker not found\n")
        sys.exit(1)
    idx_close = src2.find(style_close, idx_marker)
    if idx_close < 0:
        sys.stderr.write("[ERROR] </style> not found after CSS marker\n")
        sys.exit(1)

    # Indent the new CSS so it aligns with surrounding 4-space indentation? The original CSS in the file
    # appears to be within a <style> block at variable indentation. We'll indent each non-empty line 4 spaces.
    indented_css = "\n".join(("    " + ln) if ln.strip() else "" for ln in new_css.splitlines())

    src3 = src2[:idx_marker] + indented_css + "\n  " + src2[idx_close:]

    write(TARGET, src3)
    print("[OK] integrated. file size:", len(src3))


if __name__ == "__main__":
    main()
