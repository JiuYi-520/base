#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalize navigation bar and profile sidebar across all HTML pages
to match index.html exactly.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NORM = os.path.join(ROOT, '_normalize')

def read_norm(name):
    with open(os.path.join(NORM, name), 'r', encoding='utf-8', newline='') as f:
        return f.read()

NAV_CSS = read_norm('nav_css.txt')
SIDEBAR_CSS = read_norm('sidebar_css.txt')
NAV_HTML_TPL = read_norm('nav_html.txt')
SIDEBAR_HTML = read_norm('sidebar_html.txt')
SIDEBAR_JS = read_norm('sidebar_js.txt')

# ------------------------------------------------------------------
# Files to process. Skip admin-login.html (separate layout) and
# detail-*.html files (different structure).
# ------------------------------------------------------------------
TARGETS = [
    'auction.html',
    'baizhen-collection.html',
    'brand-story.html',
    'cat-gongyi.html',
    'cat-meishi.html',
    'cat-wenfang.html',
    'cat-yangsheng.html',
    'contact.html',
    'custom-gift.html',
    'member-center.html',
]

ACTIVE_RULES = {
    'index.html': '首页',
    'baizhen-collection.html': '百珍荟萃',
}

def get_active_label(filename):
    if filename == 'index.html':
        return '首页'
    if filename == 'baizhen-collection.html' or filename.startswith('cat-') or filename.startswith('detail-'):
        return '百珍荟萃'
    return None


def make_nav_html(filename):
    """Customize NAV_HTML_TPL for the given page."""
    html = NAV_HTML_TPL
    # On non-index pages, the brand and 首页 link go to index.html (not #top)
    if filename != 'index.html':
        # brand href
        html = html.replace('<a class="brand" href="#top"', '<a class="brand" href="index.html"')
        # 首页 link
        html = html.replace('<a href="#top">首页</a>', '<a href="index.html">首页</a>')
    # Apply active class
    label = get_active_label(filename)
    if label == '首页':
        html = html.replace('<a href="index.html">首页</a>',
                            '<a href="index.html" class="active">首页</a>')
        html = html.replace('<a href="#top">首页</a>',
                            '<a href="#top" class="active">首页</a>')
    elif label == '百珍荟萃':
        html = html.replace('<a href="baizhen-collection.html">百珍荟萃</a>',
                            '<a href="baizhen-collection.html" class="active">百珍荟萃</a>')
    return html


# ------------------------------------------------------------------
# CSS removal: remove existing rules covering nav and sidebar selectors.
# We strip top-level rules (and their full body block) whose selector
# list contains any of the listed prefixes.
# ------------------------------------------------------------------
NAV_SELECTORS = [
    '.topbar', '.nav ', '.nav{', '.nav,', '.nav>', '.nav.', '.nav:',
    '.brand', '.brand-mark', '.navlinks', '.nav-avatar',
]
SIDEBAR_SELECTORS = [
    '.profile-overlay', '.profile-sidebar', '.profile-sidebar-header',
    '.profile-close', '.profile-user-block', '.profile-avatar-large',
    '.profile-username', '.profile-tag', '.profile-upload-input',
    '.profile-menu', '.profile-panel', '.profile-balance',
    '.balance-', '.topup-', '.account-balance', '.account-section-title',
    '.account-info-', '.order-card', '.order-status', '.order-product',
    '.order-logistics', '.logistics-track', '.logistics-step',
    '.logistics-dot',
]


def selector_matches(selector_text, prefixes):
    """Return True if any selector in the comma-separated list starts with one of the prefixes."""
    parts = [p.strip() for p in selector_text.split(',')]
    for p in parts:
        # Each individual selector. Check if it begins with one of the prefixes,
        # or contains the prefix as a class token directly attached.
        for pref in prefixes:
            pref_clean = pref.rstrip(' {,>:.').rstrip()
            if not pref_clean:
                continue
            # exact prefix match at start of selector
            # selector might have leading "*" or "html" — we want it to start with the class
            if p.startswith(pref_clean):
                # ensure boundary: next char is space, ., :, [, >, +, ~, end, comma, {
                rest = p[len(pref_clean):]
                if rest == '' or rest[0] in ' .:[,{>+~()*':
                    return True
            # Or class anywhere as a standalone token (e.g. ".foo .topbar")
            # match " .topbar" boundary
            idx = p.find(pref_clean)
            while idx != -1:
                left_ok = idx == 0 or p[idx-1] in ' >+~,'
                rest = p[idx+len(pref_clean):]
                right_ok = rest == '' or rest[0] in ' .:[,{>+~()*'
                if left_ok and right_ok:
                    return True
                idx = p.find(pref_clean, idx+1)
    return False


def strip_css_rules(css, prefixes):
    """Walk the CSS string and remove top-level rules whose selector list matches."""
    out = []
    i = 0
    n = len(css)
    while i < n:
        # Find next selector start (skip whitespace)
        # We process one rule at a time. A rule is selector { body }.
        # Also handle @media / @supports — recursively process inside.
        # For simplicity, we treat @-rules with blocks as units and recurse on their body.

        # Skip whitespace
        ws_start = i
        while i < n and css[i] in ' \t\r\n':
            i += 1

        if i >= n:
            out.append(css[ws_start:])
            break

        # Comment
        if css.startswith('/*', i):
            end = css.find('*/', i+2)
            if end == -1:
                out.append(css[ws_start:])
                break
            out.append(css[ws_start:end+2])
            i = end + 2
            continue

        # Find next '{' at this nesting level, or ';' (for @import etc.)
        rule_start = i
        # Now scan to find the start of the next block or end
        depth = 0
        j = i
        first_brace = -1
        semi = -1
        while j < n:
            ch = css[j]
            if ch == '/' and j+1 < n and css[j+1] == '*':
                end = css.find('*/', j+2)
                if end == -1:
                    j = n
                    break
                j = end + 2
                continue
            if ch == '"' or ch == "'":
                # skip string
                quote = ch
                j += 1
                while j < n and css[j] != quote:
                    if css[j] == '\\':
                        j += 2
                        continue
                    j += 1
                j += 1
                continue
            if ch == '{':
                first_brace = j
                break
            if ch == ';' and depth == 0:
                semi = j
                break
            j += 1

        if first_brace == -1 and semi == -1:
            # nothing left
            out.append(css[ws_start:])
            break

        if semi != -1 and (first_brace == -1 or semi < first_brace):
            # @-rule like @import / @charset
            out.append(css[ws_start:semi+1])
            i = semi + 1
            continue

        # We have a rule: selector text from rule_start to first_brace
        selector_text = css[rule_start:first_brace].strip()
        # Find matching close brace
        depth = 1
        k = first_brace + 1
        while k < n and depth > 0:
            ch = css[k]
            if ch == '/' and k+1 < n and css[k+1] == '*':
                end = css.find('*/', k+2)
                if end == -1:
                    k = n
                    break
                k = end + 2
                continue
            if ch == '"' or ch == "'":
                quote = ch
                k += 1
                while k < n and css[k] != quote:
                    if css[k] == '\\':
                        k += 2
                        continue
                    k += 1
                k += 1
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            k += 1
        rule_end = k  # one past the closing brace

        # If selector starts with @media / @supports / @keyframes — recurse on body
        if selector_text.startswith('@'):
            # For @keyframes, the body has selectors like 0%, 100% — leave as-is
            if selector_text.startswith('@media') or selector_text.startswith('@supports'):
                inner = css[first_brace+1:rule_end-1]
                cleaned_inner = strip_css_rules(inner, prefixes)
                # If cleaned_inner is essentially empty, drop the whole @-rule
                if cleaned_inner.strip() == '':
                    # discard preceding whitespace too
                    i = rule_end
                    continue
                out.append(css[ws_start:first_brace+1])
                out.append(cleaned_inner)
                out.append('}')
                i = rule_end
                continue
            else:
                # leave @keyframes etc. untouched
                out.append(css[ws_start:rule_end])
                i = rule_end
                continue

        # Plain rule
        if selector_matches(selector_text, prefixes):
            # discard
            i = rule_end
            continue

        out.append(css[ws_start:rule_end])
        i = rule_end

    return ''.join(out)


def normalize_style_block(style_content):
    """Remove existing nav + sidebar rules, then append the canonical blocks."""
    cleaned = strip_css_rules(style_content, NAV_SELECTORS + SIDEBAR_SELECTORS)
    # Trim trailing whitespace, then append canonical blocks
    cleaned = cleaned.rstrip() + '\n\n    ' + NAV_CSS.strip() + '\n\n    ' + SIDEBAR_CSS.strip() + '\n  '
    return cleaned


# ------------------------------------------------------------------
# HTML helpers
# ------------------------------------------------------------------
def remove_existing_header(html):
    """Remove every <header ...>...</header> block whose class contains 'topbar' or 'header'.
    Detail pages use <header class="header"> while main pages use <header class="topbar">."""
    # Walk and remove any <header ...>..</header> block. Detail/main pages
    # only ever have one header that we want replaced anyway.
    out = []
    i = 0
    n = len(html)
    while i < n:
        m = re.search(r'<header\b[^>]*>', html[i:], flags=re.IGNORECASE)
        if not m:
            out.append(html[i:])
            break
        start = i + m.start()
        out.append(html[i:start])
        # find matching </header>
        end_m = re.search(r'</header\s*>', html[i+m.end():], flags=re.IGNORECASE)
        if not end_m:
            out.append(html[start:])
            break
        block_end = i + m.end() + end_m.end()
        # Skip the block (and any trailing whitespace)
        i = block_end
        while i < n and html[i] in ' \t\r\n':
            i += 1
    return ''.join(out)


def remove_existing_sidebar_html(html):
    """Remove the comment + overlay + aside.profile-sidebar block(s)."""
    # Remove the comment line if present (just before overlay)
    html = re.sub(r'<!--\s*个人中心侧边栏\s*-->\s*', '', html)
    # Remove overlay div
    html = re.sub(
        r'<div\s+class="profile-overlay"[^>]*>\s*</div>\s*',
        '',
        html,
        flags=re.IGNORECASE,
    )
    # Remove aside.profile-sidebar (handle nested by greedy until matching close)
    # Use a stateful walker since asides can contain nested divs.
    out_parts = []
    i = 0
    while i < len(html):
        m = re.search(r'<aside\s+class="profile-sidebar"[^>]*>',
                      html[i:], flags=re.IGNORECASE)
        if not m:
            out_parts.append(html[i:])
            break
        start = i + m.start()
        out_parts.append(html[i:start])
        # find matching </aside>
        depth = 1
        j = i + m.end()
        while j < len(html) and depth > 0:
            open_m = re.search(r'<aside\b[^>]*>', html[j:], flags=re.IGNORECASE)
            close_m = re.search(r'</aside\s*>', html[j:], flags=re.IGNORECASE)
            if not close_m:
                # malformed; bail
                j = len(html)
                break
            if open_m and open_m.start() < close_m.start():
                depth += 1
                j += open_m.end()
            else:
                depth -= 1
                j += close_m.end()
        i = j
    cleaned = ''.join(out_parts)
    # Strip extra blank lines left behind
    cleaned = re.sub(r'\n[\t ]*\n[\t ]*\n+', '\n\n', cleaned)
    return cleaned


def remove_existing_sidebar_scripts(html):
    """Remove every <script> block that references profileSidebar / navAvatar / topupConfirm / sidebarAvatarImg / panelAccount etc.
    Only removes scripts that contain those identifiers."""
    markers = [
        'profileSidebar', 'profileOverlay', 'navAvatar',
        'topupConfirm', 'sidebarAvatarImg', 'panelAccount',
        'panelOrders', 'avatarUpload',
    ]
    out_parts = []
    i = 0
    pattern = re.compile(r'<script\b[^>]*>', re.IGNORECASE)
    while i < len(html):
        m = pattern.search(html, i)
        if not m:
            out_parts.append(html[i:])
            break
        out_parts.append(html[i:m.start()])
        # find matching </script>
        end_m = re.search(r'</script\s*>', html[m.end():], flags=re.IGNORECASE)
        if not end_m:
            out_parts.append(html[m.start():])
            break
        block_end = m.end() + end_m.end()
        block_text = html[m.start():block_end]
        # Decide: drop or keep
        body = html[m.end():m.end()+end_m.start()]
        if any(mk in body for mk in markers):
            # drop. Also swallow any leading whitespace already pushed.
            if out_parts and out_parts[-1].endswith('\n'):
                # leave it
                pass
            i = block_end
            # also swallow trailing whitespace
            while i < len(html) and html[i] in ' \t\r\n':
                i += 1
            continue
        else:
            out_parts.append(block_text)
            i = block_end
    cleaned = ''.join(out_parts)
    cleaned = re.sub(r'\n[\t ]*\n[\t ]*\n+', '\n\n', cleaned)
    return cleaned


def insert_header(html, nav_html):
    """Insert nav_html right after <body>."""
    # Find the first <body...> tag
    m = re.search(r'<body[^>]*>', html, flags=re.IGNORECASE)
    if not m:
        return html
    insertion = '\n  ' + nav_html.strip() + '\n'
    return html[:m.end()] + insertion + html[m.end():]


def insert_sidebar(html, sidebar_html, sidebar_js):
    """Insert SIDEBAR_HTML and a standalone <script>SIDEBAR_JS</script> right before </body>."""
    m = re.search(r'</body\s*>', html, flags=re.IGNORECASE)
    if not m:
        return html
    insertion = '\n\n<!-- 个人中心侧边栏 -->\n' + sidebar_html.strip() + '\n\n<script>\n' + sidebar_js.strip() + '\n</script>\n'
    return html[:m.start()] + insertion + html[m.start():]


def normalize_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        raw = f.read()
    # Detect / strip BOM
    bom = ''
    if raw.startswith('\ufeff'):
        bom = '\ufeff'
        raw = raw[1:]
    # Detect CRLF
    use_crlf = '\r\n' in raw
    if use_crlf:
        raw = raw.replace('\r\n', '\n')

    original = raw

    # 1) Process every <style>...</style> block: strip nav+sidebar rules,
    #    and append canonical blocks ONLY to the FIRST style block.
    style_blocks = list(re.finditer(r'<style[^>]*>(.*?)</style>',
                                    raw, flags=re.DOTALL | re.IGNORECASE))
    if style_blocks:
        new_pieces = []
        prev_end = 0
        for idx, sb in enumerate(style_blocks):
            new_pieces.append(raw[prev_end:sb.start()])
            tag_open_end = raw.find('>', sb.start()) + 1
            tag_open = raw[sb.start():tag_open_end]
            inner = raw[tag_open_end:sb.end()-len('</style>')]
            cleaned = strip_css_rules(inner, NAV_SELECTORS + SIDEBAR_SELECTORS)
            if idx == 0:
                cleaned = cleaned.rstrip() + '\n\n    ' + NAV_CSS.strip() + '\n\n    ' + SIDEBAR_CSS.strip() + '\n  '
            new_pieces.append(tag_open + cleaned + '</style>')
            prev_end = sb.end()
        new_pieces.append(raw[prev_end:])
        raw = ''.join(new_pieces)
    else:
        # No style block — insert one in head with canonical CSS only.
        head_close = re.search(r'</head\s*>', raw, flags=re.IGNORECASE)
        if head_close:
            inj = '<style>\n    ' + NAV_CSS.strip() + '\n\n    ' + SIDEBAR_CSS.strip() + '\n  </style>\n'
            raw = raw[:head_close.start()] + inj + raw[head_close.start():]

    # 2) Remove existing nav header
    raw = remove_existing_header(raw)
    # 3) Remove existing sidebar HTML
    raw = remove_existing_sidebar_html(raw)
    # 4) Remove existing sidebar scripts
    raw = remove_existing_sidebar_scripts(raw)

    # 5) Insert canonical nav after <body>
    nav_html = make_nav_html(filename)
    raw = insert_header(raw, nav_html)

    # 6) Insert canonical sidebar HTML + JS before </body>
    raw = insert_sidebar(raw, SIDEBAR_HTML, SIDEBAR_JS)

    # Reapply line endings
    if use_crlf:
        raw = raw.replace('\n', '\r\n')
    raw = bom + raw

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(raw)


def verify(filepath):
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        s = f.read()
    body_count = len(re.findall(r'</body\s*>', s, flags=re.IGNORECASE))
    html_count = len(re.findall(r'</html\s*>', s, flags=re.IGNORECASE))
    topbar_count = s.count('<header class="topbar"')
    overlay_count = s.count('<div class="profile-overlay"')
    sidebar_count = s.count('<aside class="profile-sidebar"')
    js_count = s.count("getElementById('profileSidebar')")
    panel_return = s.count('if (!panel) return')
    return {
        'size': len(s),
        'topbar': topbar_count,
        'overlay': overlay_count,
        'sidebar': sidebar_count,
        'getSB': js_count,
        'body': body_count,
        'html': html_count,
        'panelret': panel_return,
    }


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------
def main():
    print('Normalizing files...\n')
    for fname in TARGETS:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            print(f'  SKIP {fname} (not found)')
            continue
        before = verify(path)
        normalize_file(path, fname)
        after = verify(path)
        print(f'  {fname}')
        print(f'    before: {before}')
        print(f'    after:  {after}')

    # detail-* files: process if they contain <body>; many do
    detail_files = sorted([f for f in os.listdir(ROOT)
                           if f.startswith('detail-') and f.endswith('.html')])
    print('\nDetail files (these don\'t currently have nav/sidebar — adding):')
    for fname in detail_files:
        path = os.path.join(ROOT, fname)
        before = verify(path)
        # Only normalize if the file already has a substantial structure.
        # Detail files often lack a <style> block; that's OK.
        normalize_file(path, fname)
        after = verify(path)
        print(f'  {fname}: before={before} after={after}')

    # admin-login.html — separate layout. Skip.
    print('\nadmin-login.html: skipped (separate layout)')

    print('\nDone.')


if __name__ == '__main__':
    main()
