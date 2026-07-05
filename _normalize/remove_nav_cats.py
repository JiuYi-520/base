# -*- coding: utf-8 -*-
"""
Remove the 4 category nav links from <nav class="navlinks">:
  文房雅器 / 美食特产 / 工艺民俗 / 养生珍品
Keep: 首页 / 百珍荟萃 / 拍卖中心
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# anchors to delete (match href, robust to surrounding whitespace)
KILL_HREFS = [
    "cat-wenfang.html",
    "cat-meishi.html",
    "cat-gongyi.html",
    "cat-yangsheng.html",
]

def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()

    # find every <nav class="navlinks" ...> ... </nav> and clean inside
    pattern = re.compile(r'(<nav\s+class="navlinks"[^>]*>)(.*?)(</nav>)', re.DOTALL)

    def clean_nav(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        new_body = body
        for href in KILL_HREFS:
            # remove <a ...href="cat-xxx.html"...>...</a> with optional class active and surrounding whitespace
            ax = re.compile(
                r'\s*<a\b[^>]*href="' + re.escape(href) + r'"[^>]*>.*?</a>\s*',
                re.DOTALL,
            )
            new_body = ax.sub("\n        ", new_body)
        return head + new_body + tail

    new_s = pattern.sub(clean_nav, s)

    if new_s != s:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_s)
        return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    changed = 0
    for fp in files:
        if process_file(fp):
            changed += 1
            print("updated:", os.path.basename(fp))
    print("total changed:", changed, "/", len(files))


if __name__ == "__main__":
    main()
