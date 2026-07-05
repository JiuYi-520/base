# -*- coding: utf-8 -*-
"""
统一替换 --latin 字体为 Playfair Display
- shared-pages.css 中的 :root --latin
- 所有 HTML 内联 <style> 中的 --latin
- 给所有页面注入 Google Fonts 引用 (Playfair Display 400/600/700)
- 给数字元素加上 tabular-nums + lining-nums
"""
import os, re, glob, io, codecs

ROOT = r"D:\2\Kimi_Agent_黄石砚商城模型\baizhenfang-site"

OLD_LATIN = '"Cormorant Garamond", "Georgia", serif'
NEW_LATIN = '"Playfair Display", "Cormorant Garamond", "Georgia", serif'

GOOGLE_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&display=swap" rel="stylesheet">'
)

# 在每个页面注入一段 CSS，让所有数字字体自动应用 tabular-nums + lining-nums
NUM_FEATURE_CSS = """
<style id="num-feature-fix">
  /* 让数字字体（--latin）使用整齐的等宽 lining 数字 */
  body { font-feature-settings: "kern" 1, "liga" 1; }
  [class*="num"], [class*="price"], [class*="amount"], [class*="bid"],
  .number, strong, .au-history-amt, .mc-card-num em, .au-detail-cat,
  .mc-progress-head strong, .mc-stat-body strong, .au-time-box strong,
  .au-cal-date strong, .au-stat strong, .mc-points-now > div strong,
  .mc-coupon-l strong, .mc-os-num, .mc-tool-dot, .mc-points-list .add,
  .mc-points-list .sub, .au-price-now strong, .au-history-rank {
    font-feature-settings: "tnum" 1, "lnum" 1, "ss01" 1;
    font-variant-numeric: tabular-nums lining-nums;
  }
</style>
"""

def update_shared_css():
    p = os.path.join(ROOT, "shared-pages.css")
    if not os.path.exists(p): return False
    with codecs.open(p, "r", "utf-8") as f:
        txt = f.read()
    new_txt = txt.replace(
        '--latin: "Cormorant Garamond", "Georgia", serif;',
        '--latin: "Playfair Display", "Cormorant Garamond", "Georgia", serif;'
    )
    # 添加全局数字特性规则
    if 'font-feature-settings' not in new_txt:
        new_txt = new_txt.replace(
            'overflow-x: hidden;\n}',
            'overflow-x: hidden;\n  font-feature-settings: "kern" 1, "liga" 1;\n}',
            1
        )
    if new_txt != txt:
        with codecs.open(p, "w", "utf-8") as f:
            f.write(new_txt)
        return True
    return False

def update_html(p):
    with codecs.open(p, "r", "utf-8") as f:
        txt = f.read()
    orig = txt

    # 1) 替换 --latin 变量定义（多种写法）
    txt = re.sub(
        r'(--latin\s*:\s*)"Cormorant Garamond"(\s*,\s*"Georgia"\s*,\s*serif)\s*;',
        r'\1"Playfair Display", "Cormorant Garamond"\2;',
        txt
    )

    # 2) 添加 Google Fonts <link>
    if 'Playfair+Display' not in txt:
        # 在 <head> 内的 <title> 之后插入
        m = re.search(r'(</title>)', txt)
        if m:
            txt = txt[:m.end()] + "\n  " + GOOGLE_FONT_LINK + txt[m.end():]

    # 3) 注入数字特性 CSS（避免重复）
    if 'id="num-feature-fix"' not in txt:
        # 放在 </head> 之前
        m = re.search(r'</head>', txt)
        if m:
            txt = txt[:m.start()] + NUM_FEATURE_CSS + "\n" + txt[m.start():]

    if txt != orig:
        with codecs.open(p, "w", "utf-8") as f:
            f.write(txt)
        return True
    return False

def main():
    changed = []
    if update_shared_css():
        changed.append("shared-pages.css")
    for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        if update_html(p):
            changed.append(os.path.basename(p))
    print("changed: %d files" % len(changed))
    for c in changed:
        print(" - " + c)

if __name__ == "__main__":
    main()
