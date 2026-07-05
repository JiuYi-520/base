# -*- coding: utf-8 -*-
"""
Add 拍卖中心 link to navigation across all HTML pages.
Sets active state based on filename.
"""
import io, re, glob, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
files = sorted(glob.glob(os.path.join(ROOT, '*.html')))

# canonical nav with 拍卖中心
def build_nav(active_file):
    """active_file is filename without dir, e.g. 'auction.html' or 'index.html'"""
    items = [
        ('index.html', '首页'),
        ('baizhen-collection.html', '百珍荟萃'),
        ('cat-wenfang.html', '文房雅器'),
        ('cat-meishi.html', '美食特产'),
        ('cat-gongyi.html', '工艺民俗'),
        ('cat-yangsheng.html', '养生珍品'),
        ('auction.html', '拍卖中心'),
    ]
    lines = ['<nav class="navlinks" aria-label="主导航">']
    for href, label in items:
        # match either by filename
        is_active = False
        if active_file == href:
            is_active = True
        # index.html may use href="#top" with active class — handled below
        cls = ' class="active"' if is_active else ''
        # for index page itself, the home link uses #top
        if href == 'index.html' and active_file == 'index.html':
            lines.append('        <a class="active" href="#top">首页</a>')
        else:
            lines.append('        <a%s href="%s">%s</a>' % (cls, href, label))
    lines.append('      </nav>')
    return '\n'.join(lines)

NAV_RE = re.compile(r'<nav class="navlinks"[^>]*>.*?</nav>', re.S)

count = 0
for fp in files:
    name = os.path.basename(fp)
    if name.startswith('_') or name.endswith('.bak'):
        continue
    with io.open(fp, 'r', encoding='utf-8') as f:
        src = f.read()
    new_nav = build_nav(name)
    new_src, n = NAV_RE.subn(new_nav, src, count=1)
    if n == 0:
        print('SKIP (no nav):', name)
        continue
    if new_src != src:
        with io.open(fp, 'w', encoding='utf-8') as f:
            f.write(new_src)
        count += 1

print('updated:', count, 'files')
