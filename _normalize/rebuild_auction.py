# -*- coding: utf-8 -*-
"""Rebuild auction.html: replace CSS + main content with optimized version."""
import io, re, sys

PATH = r"D:\2\Kimi_Agent_黄石砚商城模型\baizhenfang-site\auction.html"

with io.open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# === New auction-specific CSS (replaces lines 9-43, the .auction-room ... block) ===
NEW_AUCTION_CSS = r"""
    /* ======= 拍卖中心 v2 全新样式 ======= */
    :root { --pine: #4a8d75; --crimson: #a84d34; }
    .au-main { background: var(--paper); padding-bottom: 80px; }
    .au-main a { text-decoration: none; }

    /* 面包屑 */
    .au-crumb { background: #1c1812; padding: 14px 0; color: rgba(255,249,237,.55); font-size: 12px; letter-spacing: 2px; }
    .au-crumb a { color: rgba(255,249,237,.55); transition: color .2s; }
    .au-crumb a:hover { color: var(--gold); }
    .au-crumb .sep { margin: 0 10px; color: rgba(255,249,237,.25); }
    .au-crumb .cur { color: var(--gold); }

    /* HERO */
    .au-hero { padding: 60px 0 70px; background: linear-gradient(135deg, #1c1812 0%, #2a1f15 60%, #1c1812 100%); color: var(--cream); position: relative; overflow: hidden; }
    .au-hero::before { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 80% 30%, rgba(185,151,91,.18), transparent 55%), radial-gradient(circle at 15% 80%, rgba(168,77,52,.14), transparent 55%); pointer-events: none; }
    .au-hero-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; align-items: center; position: relative; }
    @media (max-width: 980px) { .au-hero-grid { grid-template-columns: 1fr; } }
    .au-hero-eyebrow { display: inline-block; padding: 6px 14px; border: 1px solid rgba(185,151,91,.5); color: var(--gold); font-size: 12px; letter-spacing: 4px; margin-bottom: 18px; }
    .au-hero h1 { font-size: clamp(38px, 5vw, 64px); letter-spacing: 6px; line-height: 1.15; font-weight: 900; margin-bottom: 20px; }
    .au-hero h1 em { color: var(--gold); font-style: normal; }
    .au-hero p.lead { color: rgba(255,249,237,.72); font-size: 15px; line-height: 2; letter-spacing: 1.5px; max-width: 520px; margin-bottom: 28px; }
    .au-hero-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 36px; }
    .au-btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 26px; font-size: 13px; letter-spacing: 3px; font-weight: 700; border-radius: 2px; transition: all .25s; }
    .au-btn-pri { background: var(--gold); color: #1c1812; border: 1px solid var(--gold); }
    .au-btn-pri:hover { background: #e0c485; border-color: #e0c485; }
    .au-btn-ghost { color: var(--cream); border: 1px solid rgba(255,249,237,.4); }
    .au-btn-ghost:hover { border-color: var(--gold); color: var(--gold); }
    .au-hero-tags { display: flex; gap: 18px; flex-wrap: wrap; color: rgba(255,249,237,.5); font-size: 12px; letter-spacing: 2px; }
    .au-hero-tags i { color: var(--gold); margin-right: 6px; font-style: normal; }

    .au-hero-visual { position: relative; aspect-ratio: 4/5; max-width: 420px; margin-left: auto; }
    .au-hero-visual img { position: absolute; object-fit: cover; box-shadow: 0 30px 80px rgba(0,0,0,.5); }
    .au-hero-visual img:nth-child(1) { width: 80%; height: 80%; top: 0; right: 0; border: 1px solid rgba(185,151,91,.4); }
    .au-hero-visual img:nth-child(2) { width: 55%; height: 55%; bottom: 0; left: 0; border: 1px solid rgba(185,151,91,.5); }
    .au-hero-seal { position: absolute; right: -16px; bottom: -16px; width: 110px; height: 110px; border-radius: 50%; background: var(--gold); color: #1c1812; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 900; letter-spacing: 3px; font-size: 13px; line-height: 1.5; box-shadow: 0 12px 30px rgba(185,151,91,.4); }
    .au-hero-seal small { font-family: var(--latin); font-size: 11px; opacity: .8; letter-spacing: 2px; }

    /* 数据条 */
    .au-stats { background: #fff; border-bottom: 1px solid var(--line); }
    .au-stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); }
    @media (max-width: 760px) { .au-stats-grid { grid-template-columns: repeat(2, 1fr); } }
    .au-stat { padding: 30px 24px; text-align: center; border-right: 1px solid var(--line); }
    .au-stat:last-child { border-right: none; }
    @media (max-width: 760px) { .au-stat:nth-child(2) { border-right: none; } .au-stat:nth-child(-n+2) { border-bottom: 1px solid var(--line); } }
    .au-stat strong { display: block; font-family: var(--latin); font-size: 36px; font-weight: 700; color: var(--clay); letter-spacing: 1px; line-height: 1; margin-bottom: 8px; }
    .au-stat strong em { font-size: 16px; color: var(--smoke); font-style: normal; margin-right: 2px; }
    .au-stat span { display: block; color: var(--smoke); font-size: 12px; letter-spacing: 3px; }

    /* 通用 section head */
    .au-section { padding: 60px 0 0; }
    .au-section-head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 28px; gap: 16px; flex-wrap: wrap; }
    .au-eyebrow { display: inline-block; color: var(--clay); font-family: var(--latin); font-size: 13px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 6px; }
    .au-section-head h2 { color: var(--ink); font-size: 28px; letter-spacing: 5px; font-weight: 800; }
    .au-section-head p { color: var(--smoke); font-size: 13px; letter-spacing: 1.5px; max-width: 460px; line-height: 1.8; }

    /* 主拍场 stage */
    .au-stage-grid { display: grid; grid-template-columns: minmax(0, 1.6fr) 1fr; gap: 22px; }
    @media (max-width: 1080px) { .au-stage-grid { grid-template-columns: 1fr; } }
    .au-stage { display: grid; grid-template-columns: 1fr 1fr; min-height: 580px; background: #fff; border: 1px solid var(--line); box-shadow: 18px 18px 0 rgba(168,95,61,.08); overflow: hidden; }
    @media (max-width: 880px) { .au-stage { grid-template-columns: 1fr; } }
    .au-visual { position: relative; overflow: hidden; background: #1c1812; min-height: 380px; }
    .au-visual img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s; }
    .au-visual:hover img { transform: scale(1.04); }
    .au-lot-badge { position: absolute; left: 20px; top: 20px; padding: 8px 14px; background: rgba(23,20,17,.85); color: var(--gold); border: 1px solid rgba(185,151,91,.5); font-weight: 900; letter-spacing: 3px; font-size: 12px; }
    .au-lot-watermark { position: absolute; right: 20px; bottom: 20px; color: rgba(255,249,237,.18); font-family: var(--latin); font-size: 80px; font-weight: 900; letter-spacing: 4px; pointer-events: none; line-height: 1; }
    .au-lot-thumbs { position: absolute; left: 20px; bottom: 20px; display: flex; gap: 8px; }
    .au-lot-thumbs span { width: 56px; height: 56px; border-radius: 4px; background-size: cover; background-position: center; border: 2px solid transparent; cursor: pointer; opacity: .65; transition: all .2s; }
    .au-lot-thumbs span.active { border-color: var(--gold); opacity: 1; }
    .au-lot-thumbs span:hover { opacity: 1; }

    .au-detail { padding: 32px 30px; display: flex; flex-direction: column; gap: 18px; background: linear-gradient(180deg, #fff 0%, #fbf6ec 100%); }
    .au-detail-meta { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
    .au-detail-cat { color: var(--smoke); font-size: 12px; letter-spacing: 3px; }
    .au-detail-status { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; background: var(--pine); color: #fff; font-size: 11px; letter-spacing: 2px; font-weight: 800; border-radius: 2px; }
    .au-detail-status.live::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: #fff; animation: auBlink 1s infinite; }
    @keyframes auBlink { 0%,100% { opacity: 1; } 50% { opacity: .3; } }
    .au-detail h2 { font-size: clamp(26px, 3vw, 36px); letter-spacing: 4px; line-height: 1.15; color: var(--ink); }
    .au-detail-desc { color: var(--smoke); font-size: 13px; line-height: 1.9; letter-spacing: 1px; }
    .au-spec-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; padding: 14px 0; border-top: 1px dashed var(--line); border-bottom: 1px dashed var(--line); }
    .au-spec-row > div { text-align: center; padding: 4px 8px; border-right: 1px solid var(--line); }
    .au-spec-row > div:last-child { border-right: none; }
    .au-spec-row small { display: block; color: var(--smoke); font-size: 11px; letter-spacing: 1.5px; margin-bottom: 4px; }
    .au-spec-row strong { color: var(--ink); font-size: 13px; letter-spacing: 1px; font-weight: 700; }

    .au-price-row { display: flex; justify-content: space-between; align-items: flex-end; gap: 14px; }
    .au-price-now small { display: block; color: var(--smoke); font-size: 11px; letter-spacing: 3px; margin-bottom: 4px; }
    .au-price-now strong { color: var(--clay); font-family: var(--latin); font-size: clamp(40px, 5vw, 58px); font-weight: 700; line-height: 1; letter-spacing: 1px; }
    .au-price-now strong i { font-size: 18px; color: var(--smoke); font-style: normal; margin-right: 4px; }
    .au-price-step { color: var(--smoke); font-size: 12px; letter-spacing: 1.5px; text-align: right; }
    .au-price-step em { color: var(--clay); font-style: normal; font-family: var(--latin); font-weight: 700; }

    .au-time-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .au-time-box { padding: 14px 8px; background: #1c1812; color: var(--cream); text-align: center; border-radius: 2px; }
    .au-time-box strong { display: block; font-family: var(--latin); font-size: 28px; font-weight: 700; color: var(--gold); line-height: 1; letter-spacing: 1px; }
    .au-time-box span { display: block; margin-top: 6px; font-size: 11px; letter-spacing: 2px; color: rgba(255,249,237,.55); }

    .au-bid-form { display: grid; grid-template-columns: 1fr auto; border: 1px solid var(--clay); background: #fff; border-radius: 2px; overflow: hidden; }
    .au-bid-form input { min-width: 0; height: 56px; padding: 0 18px; border: 0; outline: 0; background: transparent; color: var(--ink); font-family: var(--latin); font-size: 24px; letter-spacing: 1px; font-weight: 700; }
    .au-bid-form button { min-width: 140px; border: 0; background: var(--clay); color: #fff; cursor: pointer; font-weight: 900; letter-spacing: 4px; font-size: 13px; transition: background .2s; }
    .au-bid-form button:hover { background: #8a3e2a; }
    .au-quick-bids { display: flex; gap: 6px; flex-wrap: wrap; }
    .au-quick-bids button { padding: 6px 14px; background: rgba(168,95,61,.08); color: var(--clay); border: 1px solid rgba(168,95,61,.25); font-size: 12px; letter-spacing: 1px; cursor: pointer; border-radius: 2px; transition: all .2s; font-family: var(--latin); }
    .au-quick-bids button:hover { background: var(--clay); color: #fff; border-color: var(--clay); }
    .au-bid-help { min-height: 22px; color: var(--smoke); font-size: 12px; line-height: 1.6; letter-spacing: .5px; }
    .au-bid-help.error { color: var(--crimson); }
    .au-bid-help.success { color: var(--pine); }

    /* 拍卖侧边栏 */
    .au-side { display: flex; flex-direction: column; gap: 16px; }
    .au-lot-list { display: flex; flex-direction: column; gap: 10px; }
    .au-lot-card { display: grid; grid-template-columns: 90px 1fr; gap: 14px; padding: 12px; background: #fff; border: 1px solid var(--line); cursor: pointer; transition: all .25s; text-align: left; align-items: center; }
    .au-lot-card:hover, .au-lot-card.active { border-color: var(--gold); transform: translateX(-3px); box-shadow: -6px 6px 0 rgba(185,151,91,.18); }
    .au-lot-card.active { background: rgba(185,151,91,.06); }
    .au-lot-card img { width: 90px; height: 90px; object-fit: cover; border-radius: 2px; }
    .au-lot-card small { color: var(--clay); font-family: var(--latin); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; }
    .au-lot-card h3 { margin-top: 4px; color: var(--ink); font-size: 14px; letter-spacing: 1.5px; font-weight: 700; line-height: 1.3; }
    .au-lot-card .au-lot-bid { margin-top: 6px; color: var(--clay); font-family: var(--latin); font-size: 18px; font-weight: 700; line-height: 1; }
    .au-lot-card .au-lot-tag { display: inline-block; margin-top: 4px; padding: 1px 6px; font-size: 10px; letter-spacing: 1px; font-weight: 700; border-radius: 2px; }
    .au-lot-card .au-lot-tag.live { background: var(--pine); color: #fff; }
    .au-lot-card .au-lot-tag.soon { background: var(--gold); color: #1c1812; }

    .au-history { padding: 22px; background: #1c1812; color: var(--cream); border: 1px solid rgba(185,151,91,.2); }
    .au-history-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,249,237,.1); }
    .au-history-head h3 { color: var(--cream); font-size: 16px; letter-spacing: 3px; font-weight: 800; }
    .au-history-head em { color: var(--pine); font-style: normal; font-size: 11px; letter-spacing: 2px; }
    .au-history-head em::before { content: "● "; }
    .au-history-list { display: flex; flex-direction: column; gap: 10px; max-height: 280px; overflow-y: auto; padding-right: 4px; }
    .au-history-list::-webkit-scrollbar { width: 4px; }
    .au-history-list::-webkit-scrollbar-thumb { background: rgba(185,151,91,.35); }
    .au-history-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px dashed rgba(255,249,237,.08); }
    .au-history-row:last-child { border-bottom: none; }
    .au-history-row .who { color: rgba(255,249,237,.78); font-size: 13px; letter-spacing: 1px; }
    .au-history-row .who small { display: block; margin-top: 2px; color: rgba(255,249,237,.4); font-size: 11px; letter-spacing: .5px; font-family: var(--latin); }
    .au-history-row strong { color: var(--gold); font-family: var(--latin); font-size: 18px; font-weight: 700; letter-spacing: .5px; }
    .au-history-row.win strong { color: var(--pine); }
    .au-history-row.win::after { content: "领先"; padding: 1px 6px; font-size: 10px; letter-spacing: 1px; background: var(--pine); color: #fff; border-radius: 2px; font-weight: 700; }

    /* 拍卖日历 */
    .au-cal { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
    @media (max-width: 980px) { .au-cal { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 540px) { .au-cal { grid-template-columns: 1fr; } }
    .au-cal-card { display: flex; flex-direction: column; padding: 22px 20px; background: #fff; border: 1px solid var(--line); border-top: 3px solid var(--gold); transition: all .25s; }
    .au-cal-card:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(168,95,61,.1); }
    .au-cal-date { display: flex; align-items: baseline; gap: 8px; margin-bottom: 14px; padding-bottom: 14px; border-bottom: 1px dashed var(--line); }
    .au-cal-date strong { color: var(--ink); font-family: var(--latin); font-size: 38px; font-weight: 700; line-height: 1; }
    .au-cal-date small { color: var(--smoke); font-size: 12px; letter-spacing: 2px; }
    .au-cal-card h4 { color: var(--ink); font-size: 17px; letter-spacing: 3px; font-weight: 800; margin-bottom: 8px; }
    .au-cal-card p { color: var(--smoke); font-size: 12px; letter-spacing: 1px; line-height: 1.7; flex: 1; }
    .au-cal-foot { margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--line); display: flex; justify-content: space-between; align-items: center; }
    .au-cal-foot small { color: var(--clay); font-size: 12px; letter-spacing: 1.5px; }
    .au-cal-foot a { color: var(--ink); font-size: 12px; letter-spacing: 1.5px; font-weight: 700; }
    .au-cal-foot a:hover { color: var(--clay); }
    .au-cal-card.past { opacity: .65; border-top-color: var(--smoke); }
    .au-cal-card.past .au-cal-foot small { color: var(--smoke); }

    /* 流程 */
    .au-flow { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; position: relative; }
    @media (max-width: 980px) { .au-flow { grid-template-columns: repeat(2, 1fr); } }
    .au-flow-step { padding: 24px 18px; background: #fff; border: 1px solid var(--line); position: relative; transition: all .25s; }
    .au-flow-step:hover { border-color: var(--gold); transform: translateY(-3px); }
    .au-flow-num { display: inline-block; width: 36px; height: 36px; border-radius: 50%; background: var(--ink); color: var(--gold); font-family: var(--latin); font-weight: 700; font-size: 15px; line-height: 36px; text-align: center; margin-bottom: 14px; }
    .au-flow-step h4 { color: var(--ink); font-size: 15px; letter-spacing: 2px; font-weight: 800; margin-bottom: 8px; }
    .au-flow-step p { color: var(--smoke); font-size: 12px; line-height: 1.8; letter-spacing: .5px; }

    /* 历史成交 */
    .au-past { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    @media (max-width: 880px) { .au-past { grid-template-columns: 1fr; } }
    .au-past-card { display: grid; grid-template-columns: 110px 1fr; gap: 16px; padding: 16px; background: #fff; border: 1px solid var(--line); transition: all .25s; align-items: center; }
    .au-past-card:hover { border-color: var(--gold); box-shadow: 0 12px 24px rgba(168,95,61,.1); }
    .au-past-card img { width: 110px; height: 110px; object-fit: cover; border-radius: 2px; }
    .au-past-card small { color: var(--smoke); font-size: 11px; letter-spacing: 1.5px; }
    .au-past-card h4 { color: var(--ink); font-size: 15px; letter-spacing: 2px; font-weight: 800; margin: 4px 0 8px; }
    .au-past-card .au-past-price { color: var(--clay); font-family: var(--latin); font-size: 22px; font-weight: 700; letter-spacing: .5px; }
    .au-past-card .au-past-price em { font-size: 12px; color: var(--smoke); font-style: normal; margin-left: 6px; }
    .au-past-card .au-past-buyer { display: inline-block; margin-top: 8px; padding: 2px 8px; background: rgba(185,151,91,.15); color: var(--clay); font-size: 11px; letter-spacing: 1px; }

    /* 信任徽章 */
    .au-trust { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; padding: 30px; background: linear-gradient(135deg, #fbf6ec, #fff); border: 1px solid var(--line); }
    @media (max-width: 880px) { .au-trust { grid-template-columns: repeat(2, 1fr); padding: 20px; } }
    .au-trust-item { display: flex; gap: 14px; align-items: flex-start; padding: 14px; }
    .au-trust-ico { width: 44px; height: 44px; border-radius: 50%; background: var(--ink); color: var(--gold); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
    .au-trust-item h4 { color: var(--ink); font-size: 14px; letter-spacing: 2px; font-weight: 800; margin-bottom: 6px; }
    .au-trust-item p { color: var(--smoke); font-size: 12px; line-height: 1.7; }

    /* FAQ */
    .au-faq { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 24px; }
    @media (max-width: 880px) { .au-faq { grid-template-columns: 1fr; } }
    .au-faq-item { padding: 18px 22px; background: #fff; border: 1px solid var(--line); transition: all .25s; cursor: pointer; }
    .au-faq-item:hover { border-color: var(--gold); }
    .au-faq-item h4 { color: var(--ink); font-size: 14px; letter-spacing: 2px; font-weight: 800; margin-bottom: 10px; padding-left: 22px; position: relative; }
    .au-faq-item h4::before { content: "Q"; position: absolute; left: 0; top: -1px; width: 18px; height: 18px; line-height: 18px; text-align: center; background: var(--gold); color: #1c1812; font-family: var(--latin); font-size: 11px; border-radius: 50%; font-weight: 900; }
    .au-faq-item p { color: var(--smoke); font-size: 13px; line-height: 1.8; padding-left: 22px; position: relative; letter-spacing: .5px; }
    .au-faq-item p::before { content: "A"; position: absolute; left: 0; top: 1px; width: 18px; height: 18px; line-height: 18px; text-align: center; background: var(--clay); color: #fff; font-family: var(--latin); font-size: 11px; border-radius: 50%; font-weight: 900; }

    /* CTA */
    .au-cta { margin-top: 60px; padding: 50px 40px; background: linear-gradient(135deg, #1c1812 0%, #2a1f15 100%); color: var(--cream); text-align: center; border-radius: 2px; position: relative; overflow: hidden; }
    .au-cta::before { content: ""; position: absolute; inset: 0; background: radial-gradient(circle at 50% 100%, rgba(185,151,91,.18), transparent 70%); pointer-events: none; }
    .au-cta > * { position: relative; }
    .au-cta h3 { font-size: 26px; letter-spacing: 5px; font-weight: 800; margin-bottom: 14px; }
    .au-cta p { color: rgba(255,249,237,.65); font-size: 14px; line-height: 1.9; max-width: 540px; margin: 0 auto 24px; letter-spacing: 1px; }
    .au-cta-actions { display: inline-flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
"""

# Find the auction CSS block: from ".auction-room { display: grid;" to right before "/* 个人中心侧边栏 */"
css_start = html.find('.auction-room { display: grid;')
css_end = html.find('/* 个人中心侧边栏 */')
if css_start == -1 or css_end == -1:
    sys.exit("[FAIL] cannot locate CSS block")
# trim back any leading whitespace before /* 个人中心侧边栏 */
old_css = html[css_start:css_end]
html = html.replace(old_css, NEW_AUCTION_CSS + "\n      ")

# === New main content ===
# Find <main>...</main> block, replace
main_match = re.search(r"<main>.*?</main>", html, re.DOTALL)
if not main_match:
    sys.exit("[FAIL] cannot find <main>")

NEW_MAIN = r"""<main class="au-main">

    <!-- 面包屑 -->
    <div class="au-crumb">
      <div class="shell">
        <a href="index.html">首页</a>
        <span class="sep">/</span>
        <span class="cur">拍卖中心</span>
      </div>
    </div>

    <!-- HERO -->
    <section class="au-hero">
      <div class="shell au-hero-grid">
        <div>
          <span class="au-hero-eyebrow">FANGCHENG AUCTION HOUSE</span>
          <h1>方城百珍 · <em>春拍专场</em><br>风物入瓯，珍品入场</h1>
          <p class="lead">从书房文房到工艺收藏，从地方风味到独山玉雕，方城百珍坊将散落民间的精品集结于此，依匠人脉络与市场公允透明竞拍，让每一件珍品都遇见真正懂它的人。</p>
          <div class="au-hero-actions">
            <a class="au-btn au-btn-pri" href="#au-stage">进入拍场
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
            <a class="au-btn au-btn-ghost" href="#au-flow">参拍流程</a>
          </div>
          <div class="au-hero-tags">
            <span><i>◆</i>每周三、六 20:00 开槌</span>
            <span><i>◆</i>方城非遗工艺甄选</span>
            <span><i>◆</i>百珍坊鉴定保真</span>
          </div>
        </div>
        <div class="au-hero-visual">
          <img src="uploads/stone-qingshi.jpg" alt="黄石砚">
          <img src="uploads/product-shihou.jpg" alt="石猴">
          <div class="au-hero-seal">春拍<br>开槌<small>SPRING 2024</small></div>
        </div>
      </div>
    </section>

    <!-- 数据条 -->
    <section class="au-stats">
      <div class="shell au-stats-grid">
        <div class="au-stat">
          <strong>3</strong>
          <span>正在拍卖</span>
        </div>
        <div class="au-stat">
          <strong>128</strong>
          <span>注册藏家</span>
        </div>
        <div class="au-stat">
          <strong><em>¥</em>86,420</strong>
          <span>累计成交额</span>
        </div>
        <div class="au-stat">
          <strong><em>¥</em>12,800</strong>
          <span>最高单笔成交</span>
        </div>
      </div>
    </section>

    <!-- 主拍场 -->
    <section class="au-section" id="au-stage">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">Live Auction</span>
            <h2>今日主拍</h2>
          </div>
          <p>切换右侧拍品后，倒计时、当前价和出价记录会即时更新。本机数据仅作演示，正式上线后接入会员账户与保证金。</p>
        </div>

        <div class="au-stage-grid">
          <!-- 主舞台 -->
          <article class="au-stage">
            <figure class="au-visual">
              <img id="auctionImage" src="uploads/stone-qingshi.jpg" alt="竞拍拍品图片">
              <figcaption class="au-lot-badge" id="auctionBadge">LOT 01</figcaption>
              <span class="au-lot-watermark">FC</span>
            </figure>
            <div class="au-detail">
              <div class="au-detail-meta">
                <span class="au-detail-cat" id="auctionCategory">文房雅器 · 黄石砚</span>
                <strong class="au-detail-status live" id="auctionStatus">竞拍中</strong>
              </div>
              <h2 id="auctionTitle">方城黄石砚 · 山水纹藏砚</h2>
              <p class="au-detail-desc" id="auctionDesc">纹理有山水走势，适合书房陈设与收藏赠礼。</p>

              <div class="au-spec-row">
                <div><small>产地</small><strong>河南方城</strong></div>
                <div><small>年代</small><strong>当代精品</strong></div>
                <div><small>认证</small><strong>百珍鉴真</strong></div>
              </div>

              <div class="au-price-row">
                <div class="au-price-now">
                  <small>当前出价 / CURRENT</small>
                  <strong><i>¥</i><span id="currentBid">3680</span></strong>
                </div>
                <div class="au-price-step">
                  最低加价 <em id="priceStep">¥200</em><br>
                  共 <em id="bidCount">3</em> 次出价
                </div>
              </div>

              <div class="au-time-grid">
                <div class="au-time-box"><strong id="timeDay">00</strong><span>天</span></div>
                <div class="au-time-box"><strong id="timeHour">00</strong><span>时</span></div>
                <div class="au-time-box"><strong id="timeMinute">00</strong><span>分</span></div>
                <div class="au-time-box"><strong id="timeSecond">00</strong><span>秒</span></div>
              </div>

              <form id="bidForm">
                <label class="au-bid-form">
                  <input id="bidInput" type="number" min="0" step="1" aria-label="输入出价金额" placeholder="输入你的出价">
                  <button type="submit">立即出价</button>
                </label>
              </form>
              <div class="au-quick-bids" id="quickBids"></div>
              <p class="au-bid-help" id="bidHelp">按最低加价出价，刷新页面也会保留本机记录。</p>
            </div>
          </article>

          <!-- 侧边 -->
          <aside class="au-side">
            <div class="au-lot-list" id="lotList" aria-label="拍品列表"></div>
            <div class="au-history">
              <div class="au-history-head">
                <h3>实时出价</h3>
                <em>LIVE</em>
              </div>
              <div class="au-history-list" id="bidHistory" aria-live="polite"></div>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <!-- 拍卖日历 -->
    <section class="au-section">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">Auction Calendar</span>
            <h2>拍卖日程</h2>
          </div>
          <a class="au-btn au-btn-ghost" style="color:var(--ink);border-color:var(--ink);" href="#">订阅日历 →</a>
        </div>
        <div class="au-cal">
          <div class="au-cal-card">
            <div class="au-cal-date"><strong>06.22</strong><small>周六 · 20:00</small></div>
            <h4>文房雅器专场</h4>
            <p>方城黄石砚、笔墨纸砚精品 14 件，含名家题铭与限量首发。</p>
            <div class="au-cal-foot"><small>● 即将开拍</small><a href="#au-stage">查看 →</a></div>
          </div>
          <div class="au-cal-card">
            <div class="au-cal-date"><strong>06.26</strong><small>周三 · 20:00</small></div>
            <h4>独山玉夜场</h4>
            <p>独山玉精品 9 件，温润平安牌、把玩件、商务赠礼皆备。</p>
            <div class="au-cal-foot"><small>● 火热预约</small><a href="#">提醒 →</a></div>
          </div>
          <div class="au-cal-card">
            <div class="au-cal-date"><strong>06.29</strong><small>周六 · 20:00</small></div>
            <h4>工艺民俗专场</h4>
            <p>方城石猴、烙画葫芦、民俗手作 18 件，记录方城烟火气。</p>
            <div class="au-cal-foot"><small>● 接受预拍</small><a href="#">提醒 →</a></div>
          </div>
          <div class="au-cal-card past">
            <div class="au-cal-date"><strong>06.15</strong><small>周六 · 已结拍</small></div>
            <h4>春季首拍 · 已结束</h4>
            <p>10 件精品全部成交，总成交额 ¥12.8 万，溢价率 +18%。</p>
            <div class="au-cal-foot"><small>● 已成交</small><a href="#au-past">回顾 →</a></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 参拍流程 -->
    <section class="au-section" id="au-flow">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">How to Bid</span>
            <h2>参拍流程</h2>
          </div>
          <p>从注册认证到成交付款，5 步完成一次完整的拍卖体验，所有过程可追溯、可监督。</p>
        </div>
        <div class="au-flow">
          <div class="au-flow-step">
            <div class="au-flow-num">01</div>
            <h4>实名注册</h4>
            <p>使用手机号实名注册百珍坊会员账户，绑定常用收货地址。</p>
          </div>
          <div class="au-flow-step">
            <div class="au-flow-num">02</div>
            <h4>缴纳保证金</h4>
            <p>按拍品起拍价的 10% 冻结保证金，未中拍立即解冻。</p>
          </div>
          <div class="au-flow-step">
            <div class="au-flow-num">03</div>
            <h4>实时出价</h4>
            <p>开槌后按系统加价幅度出价，最后 60 秒延时机制防止抢拍。</p>
          </div>
          <div class="au-flow-step">
            <div class="au-flow-num">04</div>
            <h4>支付尾款</h4>
            <p>成交后 48 小时内完成尾款支付，保证金自动抵扣。</p>
          </div>
          <div class="au-flow-step">
            <div class="au-flow-num">05</div>
            <h4>鉴定发货</h4>
            <p>百珍坊出具鉴定证书，专人打包顺丰保价直送，支持 7 日复鉴。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 历史成交 -->
    <section class="au-section" id="au-past">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">Past Records</span>
            <h2>历史成交</h2>
          </div>
          <a class="au-btn au-btn-ghost" style="color:var(--ink);border-color:var(--ink);" href="#">全部记录 →</a>
        </div>
        <div class="au-past">
          <div class="au-past-card">
            <img src="uploads/product1.jpg" alt="">
            <div>
              <small>2024.06.15 · LOT 03</small>
              <h4>方城黄石砚 · 紫袍玉带</h4>
              <div class="au-past-price">¥ 12,800<em>溢价 +52%</em></div>
              <span class="au-past-buyer">藏家 · 沪上书坊</span>
            </div>
          </div>
          <div class="au-past-card">
            <img src="uploads/product-jade.jpg" alt="">
            <div>
              <small>2024.06.08 · LOT 07</small>
              <h4>独山玉 · 福寿牌</h4>
              <div class="au-past-price">¥ 6,420<em>溢价 +28%</em></div>
              <span class="au-past-buyer">藏家 · 京华雅集</span>
            </div>
          </div>
          <div class="au-past-card">
            <img src="uploads/product-shihou.jpg" alt="">
            <div>
              <small>2024.05.25 · LOT 12</small>
              <h4>方城石猴 · 守福组合</h4>
              <div class="au-past-price">¥ 3,680<em>溢价 +18%</em></div>
              <span class="au-past-buyer">藏家 · 南阳张府</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 信任保障 -->
    <section class="au-section">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">Trust &amp; Guarantee</span>
            <h2>信任保障</h2>
          </div>
          <p>百珍坊为每件拍品提供专业鉴定、资金托管、原物保险与七日复鉴四重保障。</p>
        </div>
        <div class="au-trust">
          <div class="au-trust-item">
            <div class="au-trust-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg></div>
            <div>
              <h4>专家鉴真</h4>
              <p>每件拍品经方城非遗专家、文物鉴定师双签复核，附鉴定证书。</p>
            </div>
          </div>
          <div class="au-trust-item">
            <div class="au-trust-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg></div>
            <div>
              <h4>资金托管</h4>
              <p>保证金与尾款均由第三方银行托管，未交付前买家资金安全锁定。</p>
            </div>
          </div>
          <div class="au-trust-item">
            <div class="au-trust-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M21 16V8l-9-5-9 5v8l9 5z"/><path d="M3.27 6.96 12 12.01l8.73-5.05"/></svg></div>
            <div>
              <h4>原物保险</h4>
              <p>从打包到签收全程顺丰保价直送，含碎件全额理赔保险。</p>
            </div>
          </div>
          <div class="au-trust-item">
            <div class="au-trust-ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 12a9 9 0 0 1 9-9 9 9 0 0 1 6.5 2.7L21 3"/><path d="M21 3v6h-6"/></svg></div>
            <div>
              <h4>七日复鉴</h4>
              <p>签收后 7 日内可申请第三方机构复鉴，鉴定不符全额退款并赔付。</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="au-section">
      <div class="shell">
        <div class="au-section-head">
          <div>
            <span class="au-eyebrow">FAQ</span>
            <h2>常见问题</h2>
          </div>
          <a class="au-btn au-btn-ghost" style="color:var(--ink);border-color:var(--ink);" href="contact.html">人工客服 →</a>
        </div>
        <div class="au-faq">
          <div class="au-faq-item">
            <h4>保证金怎么收？是否会被冻结？</h4>
            <p>按起拍价 10% 冻结，最低 ¥200。未中拍闭场后 1 小时内自动解冻；中拍后保证金自动抵扣尾款。</p>
          </div>
          <div class="au-faq-item">
            <h4>最后几秒能否抢拍？</h4>
            <p>系统启用延时机制，最后 60 秒内任意一次有效出价都会重置倒计时为 60 秒，确保公平。</p>
          </div>
          <div class="au-faq-item">
            <h4>拍下后多久必须付款？</h4>
            <p>成交后 48 小时内须完成尾款支付，逾期视为自动放弃，保证金不予退还，并影响信用评级。</p>
          </div>
          <div class="au-faq-item">
            <h4>如何确认拍品真伪？</h4>
            <p>每件拍品附《百珍坊鉴定证书》和高清细节图；签收后 7 日内可申请第三方复鉴，全程留痕可追溯。</p>
          </div>
          <div class="au-faq-item">
            <h4>是否可以委托代拍？</h4>
            <p>钻石及以上会员可申请专属管家代拍服务，提前提交心理价位，由百珍坊客服严格执行。</p>
          </div>
          <div class="au-faq-item">
            <h4>发货与运输如何保障？</h4>
            <p>百珍坊统一打包为防震礼盒，全程顺丰保价直送，重要拍品可申请专人专车押运至同城。</p>
          </div>
        </div>

        <!-- CTA -->
        <div class="au-cta">
          <h3>成为百珍坊认证藏家</h3>
          <p>注册即可订阅每周拍卖预告、独享会员专享场次，钻石会员更可获得专属藏品鉴赏与管家代拍服务。</p>
          <div class="au-cta-actions">
            <a class="au-btn au-btn-pri" href="member-center.html">免费注册</a>
            <a class="au-btn au-btn-ghost" href="contact.html">联系客服</a>
          </div>
        </div>
      </div>
    </section>

  </main>"""

html = html.replace(main_match.group(0), NEW_MAIN)

# Remove old single-line footer if present (the duplicate one)
html = re.sub(r'\s*<footer class="footer"><div class="shell footer-grid"><div><h2>方城百珍坊</h2>.*?</footer>', '', html, count=1, flags=re.DOTALL)

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] auction.html rebuilt, size =", len(html))
