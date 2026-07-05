# -*- coding: utf-8 -*-
"""把 detail-product1.html 重做成 黄石砚 三板块详情页：
   1) 背景介绍   2) 工艺流程   3) 砚林集珍 (产品)
保留现有 <head>/<style>、顶部 <header>、底部侧边栏与脚本。
"""
import io, re, sys

PATH = r"D:\2\Kimi_Agent_黄石砚商城模型\baizhenfang-site\detail-product1.html"

with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

# 锚点：保留 head 到 </header>；保留 <script></script><!-- 个人中心侧边栏 --> 到结尾
m_head = re.search(r"</header>", src)
m_sb = re.search(r"<script>\s*</script>\s*<!-- 个人中心侧边栏 -->", src)
if not m_head or not m_sb:
    print("anchor not found"); sys.exit(1)

head = src[: m_head.end()]
tail = src[m_sb.start():]

# ----- 新增 CSS（注入到 </style> 之前）-----
EXTRA_CSS = r"""
/* ============= 黄石砚详情页 v3 ============= */
.hs-main{background:#F6F0E6;padding-bottom:80px;color:var(--text);}
.hs-main a{text-decoration:none;color:inherit;}

/* 面包屑 */
.hs-crumb{background:#1c1812;padding:14px 0;color:rgba(255,249,237,.5);font-size:12px;letter-spacing:2px;}
.hs-crumb .shell{max-width:1240px;margin:0 auto;padding:0 24px;}
.hs-crumb a{color:rgba(255,249,237,.5);transition:color .2s;}
.hs-crumb a:hover{color:#B9975B;}
.hs-crumb .sep{margin:0 10px;color:rgba(255,249,237,.25);}
.hs-crumb .cur{color:#B9975B;}

/* HERO */
.hs-hero{position:relative;padding:90px 0 80px;
  background:linear-gradient(rgba(20,15,10,.62),rgba(20,15,10,.78)),url("uploads/stone-qingshi.jpg") center/cover;
  color:#FFF9ED;}
.hs-hero .shell{max-width:1240px;margin:0 auto;padding:0 24px;}
.hs-hero-eyebrow{display:inline-block;padding:6px 14px;border:1px solid rgba(185,151,91,.55);
  color:#B9975B;font-family:"Playfair Display",serif;font-size:12px;letter-spacing:6px;text-transform:uppercase;font-weight:600;}
.hs-hero h1{margin-top:24px;font-size:clamp(40px,5.5vw,72px);letter-spacing:8px;font-weight:900;line-height:1.1;}
.hs-hero h1 em{font-style:normal;color:#B9975B;}
.hs-hero p.lead{margin-top:22px;max-width:680px;font-size:16px;line-height:2;color:rgba(255,249,237,.78);letter-spacing:1.5px;}
.hs-hero-tags{margin-top:34px;display:flex;flex-wrap:wrap;gap:12px;}
.hs-hero-tags span{padding:8px 16px;background:rgba(255,249,237,.06);border:1px solid rgba(185,151,91,.35);
  color:#B9975B;font-size:12px;letter-spacing:2px;font-weight:600;border-radius:2px;}
.hs-hero-tags span i{font-style:normal;margin-right:6px;}

/* 通用 section */
.hs-section{padding:80px 0;}
.hs-section .shell{max-width:1240px;margin:0 auto;padding:0 24px;}
.hs-section-head{text-align:center;margin-bottom:54px;}
.hs-section-head .eyebrow{color:#A85F3D;font-family:"Playfair Display",serif;font-size:13px;letter-spacing:6px;text-transform:uppercase;font-weight:700;}
.hs-section-head h2{margin-top:14px;font-size:36px;letter-spacing:6px;font-weight:900;color:#171411;}
.hs-section-head .sub{margin:14px auto 0;max-width:620px;color:#766D61;font-size:14px;line-height:2;letter-spacing:1.5px;}

/* 板块一：背景介绍 */
.hs-bg{background:#F6F0E6;}
.hs-bg-grid{display:grid;grid-template-columns:1.05fr 1fr;gap:60px;align-items:center;}
@media (max-width:980px){.hs-bg-grid{grid-template-columns:1fr;gap:40px;}}
.hs-bg-text h3{font-size:26px;letter-spacing:4px;font-weight:800;color:#171411;margin-bottom:18px;}
.hs-bg-text h3::before{content:"";display:inline-block;width:36px;height:2px;background:#B9975B;vertical-align:middle;margin-right:14px;}
.hs-bg-text p{color:#3a322a;font-size:15px;line-height:2.1;letter-spacing:1px;margin-bottom:14px;text-indent:2em;}
.hs-bg-quotes{margin-top:30px;padding:22px 26px;background:rgba(185,151,91,.08);border-left:3px solid #B9975B;
  font-style:italic;color:#766D61;font-size:14px;line-height:1.95;letter-spacing:1px;}
.hs-bg-quotes em{color:#A85F3D;font-style:normal;font-weight:700;}

.hs-bg-figure{position:relative;}
.hs-bg-figure .main{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:2px;
  box-shadow:24px 24px 0 rgba(185,151,91,.15);}
.hs-bg-figure .small{position:absolute;bottom:-30px;left:-30px;width:46%;aspect-ratio:1;object-fit:cover;
  border:6px solid #F6F0E6;box-shadow:0 16px 40px rgba(20,15,10,.18);}
.hs-bg-figure .seal{position:absolute;top:24px;right:24px;width:78px;height:78px;border-radius:50%;
  background:#A85F3D;color:#FFF9ED;display:flex;align-items:center;justify-content:center;flex-direction:column;
  font-size:11px;letter-spacing:2px;font-weight:700;line-height:1.4;text-align:center;}
.hs-bg-figure .seal small{display:block;font-family:"Playfair Display",serif;font-size:9px;letter-spacing:1px;color:rgba(255,249,237,.7);font-weight:600;}

.hs-bg-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:60px;
  padding:36px 0;border-top:1px solid rgba(23,20,17,.12);border-bottom:1px solid rgba(23,20,17,.12);}
@media (max-width:680px){.hs-bg-stats{grid-template-columns:repeat(2,1fr);}}
.hs-bg-stat{text-align:center;}
.hs-bg-stat strong{display:block;color:#A85F3D;font-family:"Playfair Display",serif;font-size:42px;font-weight:700;line-height:1;letter-spacing:.5px;}
.hs-bg-stat strong small{font-size:18px;margin-left:2px;font-weight:600;}
.hs-bg-stat span{display:block;margin-top:10px;color:#766D61;font-size:13px;letter-spacing:3px;}

/* 板块二：工艺流程 */
.hs-craft{background:#1c1812;color:#FFF9ED;}
.hs-craft .hs-section-head h2{color:#FFF9ED;}
.hs-craft .hs-section-head .eyebrow{color:#B9975B;}
.hs-craft .hs-section-head .sub{color:rgba(255,249,237,.6);}

.hs-craft-flow{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
@media (max-width:980px){.hs-craft-flow{grid-template-columns:repeat(2,1fr);}}
@media (max-width:560px){.hs-craft-flow{grid-template-columns:1fr;}}
.hs-craft-card{position:relative;padding:36px 28px 32px;background:rgba(255,249,237,.04);
  border:1px solid rgba(185,151,91,.18);border-radius:2px;transition:all .35s;}
.hs-craft-card:hover{transform:translateY(-6px);border-color:#B9975B;background:rgba(185,151,91,.08);
  box-shadow:0 20px 50px rgba(0,0,0,.4);}
.hs-craft-num{position:absolute;top:-22px;right:24px;
  font-family:"Playfair Display",serif;font-size:88px;font-weight:700;color:rgba(185,151,91,.18);line-height:1;letter-spacing:-2px;}
.hs-craft-ico{width:54px;height:54px;border-radius:50%;background:rgba(185,151,91,.15);
  display:flex;align-items:center;justify-content:center;color:#B9975B;margin-bottom:18px;position:relative;}
.hs-craft-card h4{font-size:20px;letter-spacing:4px;font-weight:800;margin-bottom:10px;color:#FFF9ED;}
.hs-craft-card p{color:rgba(255,249,237,.65);font-size:13px;line-height:1.95;letter-spacing:1px;margin-bottom:14px;}
.hs-craft-card ul{list-style:none;padding:18px 0 0;border-top:1px dashed rgba(185,151,91,.22);}
.hs-craft-card ul li{position:relative;padding:6px 0 6px 20px;color:rgba(255,249,237,.5);font-size:12px;letter-spacing:1px;}
.hs-craft-card ul li::before{content:"◆";position:absolute;left:0;top:7px;color:#B9975B;font-size:9px;}
.hs-craft-card .duration{margin-top:20px;padding-top:16px;border-top:1px dashed rgba(185,151,91,.22);
  display:flex;justify-content:space-between;align-items:center;}
.hs-craft-card .duration small{color:rgba(255,249,237,.4);font-size:11px;letter-spacing:2px;}
.hs-craft-card .duration strong{color:#B9975B;font-family:"Playfair Display",serif;font-size:18px;font-weight:700;letter-spacing:1px;}

.hs-craft-strip{margin-top:60px;padding:30px 32px;background:rgba(185,151,91,.08);border:1px dashed rgba(185,151,91,.3);
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:18px;}
.hs-craft-strip h5{color:#B9975B;font-size:18px;letter-spacing:4px;font-weight:800;margin-bottom:6px;}
.hs-craft-strip p{color:rgba(255,249,237,.6);font-size:13px;letter-spacing:1px;}
.hs-craft-strip .btn{padding:12px 28px;background:#B9975B;color:#1c1812;font-size:13px;letter-spacing:3px;font-weight:800;
  border-radius:2px;text-decoration:none;transition:background .2s;}
.hs-craft-strip .btn:hover{background:#d4b876;}

/* 板块三：砚林集珍 */
.hs-coll{background:#F6F0E6;}
.hs-coll-toolbar{display:flex;justify-content:space-between;align-items:center;
  padding:18px 0;margin-bottom:30px;border-top:1px solid rgba(23,20,17,.12);border-bottom:1px solid rgba(23,20,17,.12);}
.hs-coll-filters{display:flex;gap:6px;flex-wrap:wrap;}
.hs-coll-filter{padding:8px 18px;background:transparent;border:1px solid transparent;color:#766D61;font-size:13px;letter-spacing:2px;cursor:pointer;
  border-radius:2px;font-family:inherit;transition:all .2s;}
.hs-coll-filter:hover{color:#171411;}
.hs-coll-filter.active{background:#171411;color:#FFF9ED;border-color:#171411;}
.hs-coll-sort{color:#766D61;font-size:12px;letter-spacing:2px;}
.hs-coll-sort em{color:#A85F3D;font-style:normal;font-weight:700;font-family:"Playfair Display",serif;font-size:14px;}

.hs-coll-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}
@media (max-width:1080px){.hs-coll-grid{grid-template-columns:repeat(3,1fr);}}
@media (max-width:780px){.hs-coll-grid{grid-template-columns:repeat(2,1fr);}}
@media (max-width:480px){.hs-coll-grid{grid-template-columns:1fr;}}
.hs-prod{background:#fff;border:1px solid rgba(23,20,17,.08);border-radius:2px;overflow:hidden;
  display:flex;flex-direction:column;text-decoration:none;color:inherit;
  transition:transform .35s,box-shadow .35s,border-color .35s;}
.hs-prod:hover{transform:translateY(-6px);border-color:#B9975B;box-shadow:0 22px 40px rgba(20,15,10,.14);}
.hs-prod-img{position:relative;aspect-ratio:1;overflow:hidden;background:#E8DCC8;}
.hs-prod-img img{width:100%;height:100%;object-fit:cover;transition:transform .6s;}
.hs-prod:hover .hs-prod-img img{transform:scale(1.06);}
.hs-prod-tag{position:absolute;top:12px;left:12px;padding:4px 10px;background:#171411;color:#B9975B;
  font-size:10px;letter-spacing:2px;font-weight:700;border-radius:2px;}
.hs-prod-tag.gold{background:#B9975B;color:#1c1812;}
.hs-prod-tag.clay{background:#A85F3D;color:#fff;}
.hs-prod-tag.pine{background:#596C58;color:#fff;}
.hs-prod-fav{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:50%;
  background:rgba(255,249,237,.92);display:flex;align-items:center;justify-content:center;color:#A85F3D;cursor:pointer;
  transition:all .2s;}
.hs-prod-fav:hover{background:#A85F3D;color:#fff;}
.hs-prod-body{padding:18px 18px 20px;display:flex;flex-direction:column;flex:1;}
.hs-prod-id{color:#A85F3D;font-family:"Playfair Display",serif;font-size:11px;letter-spacing:3px;font-weight:700;text-transform:uppercase;}
.hs-prod-name{margin-top:6px;color:#171411;font-size:15px;letter-spacing:1.5px;font-weight:800;line-height:1.4;}
.hs-prod-meta{margin-top:8px;color:#766D61;font-size:12px;letter-spacing:1px;line-height:1.6;flex:1;}
.hs-prod-spec{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;}
.hs-prod-spec span{padding:2px 8px;background:rgba(185,151,91,.1);color:#A85F3D;font-size:11px;letter-spacing:.5px;border-radius:2px;}
.hs-prod-foot{margin-top:14px;padding-top:14px;border-top:1px dashed rgba(23,20,17,.1);
  display:flex;justify-content:space-between;align-items:flex-end;}
.hs-prod-price{color:#A85F3D;font-family:"Playfair Display",serif;font-size:22px;font-weight:700;letter-spacing:.5px;line-height:1;}
.hs-prod-price small{font-size:13px;font-weight:600;margin-right:1px;}
.hs-prod-sold{color:#766D61;font-size:11px;letter-spacing:.5px;text-align:right;}
.hs-prod-sold em{color:#171411;font-style:normal;font-family:"Playfair Display",serif;font-weight:700;}

.hs-coll-cta{margin-top:50px;text-align:center;}
.hs-coll-cta a{display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:#171411;color:#FFF9ED;
  font-size:13px;letter-spacing:4px;font-weight:800;text-decoration:none;border-radius:2px;transition:background .2s;}
.hs-coll-cta a:hover{background:#A85F3D;}
"""

# 把 EXTRA_CSS 注入到原 head 的最后一个 </style> 之前
last_style_close = head.rfind("</style>")
if last_style_close == -1:
    print("</style> not found in head"); sys.exit(1)
head = head[:last_style_close] + EXTRA_CSS + "\n" + head[last_style_close:]

# ----- 新增 BODY 内容 -----
BODY = r"""
<main class="hs-main">

  <!-- 面包屑 -->
  <div class="hs-crumb">
    <div class="shell">
      <a href="index.html">首页</a>
      <span class="sep">/</span>
      <a href="cat-wenfang.html">文房雅器</a>
      <span class="sep">/</span>
      <span class="cur">方城黄石砚</span>
    </div>
  </div>

  <!-- HERO -->
  <section class="hs-hero">
    <div class="shell">
      <span class="hs-hero-eyebrow">HUANG SHI YAN · FANGCHENG</span>
      <h1>方城<em>黄石砚</em><br>千年砚林 文房至宝</h1>
      <p class="lead">出方城黄石山者，质细而润，发墨如油，敲之声若清磬，磨之毫不滞笔。曾与端、歙、洮、澄并列，宋时已为宫廷贡品，今承非遗匠艺，刀痕入古意，方寸见山河。</p>
      <div class="hs-hero-tags">
        <span><i>◆</i>河南省非物质文化遗产</span>
        <span><i>◆</i>千年贡砚 / 文人案头</span>
        <span><i>◆</i>百珍坊鉴定保真</span>
      </div>
    </div>
  </section>

  <!-- 板块一：背景介绍 -->
  <section class="hs-section hs-bg" id="hs-bg">
    <div class="shell">
      <div class="hs-section-head">
        <span class="eyebrow">Heritage &amp; Origin</span>
        <h2>千年砚史 · 一石入墨</h2>
        <p class="sub">从北宋《砚谱》到当代非遗，黄石砚穿越九百年烟火，依然安静躺在文人的案头与墨香里，等候每一笔落下。</p>
      </div>

      <div class="hs-bg-grid">
        <div class="hs-bg-text">
          <h3>方城黄石 · 何以入砚</h3>
          <p>方城黄石砚，又称葛仙翁砚，以方城县独有的黄石山石料制成。石质细腻，色泽温润，质地坚致而不滞墨，自唐代被发现，北宋时已贡入宫廷，与端、歙、洮、澄齐名，史称"四大名砚"之一。</p>
          <p>其石中含天然云纹、山水纹、紫袍玉带纹，每方砚石皆为孤品。一砚一相，匠人因石施工，依纹布局，刀下不只是砚台，更是一方可手握的山河。</p>
          <div class="hs-bg-quotes">
            "方城黄石，质如美玉，发墨如油，<em>磨之不滑，贮水不渗</em>，文房至宝也。"<br>
            <small>— 北宋 · 米芾《砚史》节选</small>
          </div>
        </div>
        <div class="hs-bg-figure">
          <img class="main" src="uploads/stone-qingshi.jpg" alt="方城黄石砚原石">
          <img class="small" src="uploads/stone-zishi.jpg" alt="紫袍玉带纹">
          <div class="seal">非遗<br>砚艺<small>HERITAGE</small></div>
        </div>
      </div>

      <div class="hs-bg-stats">
        <div class="hs-bg-stat">
          <strong>900<small>+</small></strong>
          <span>年砚石史</span>
        </div>
        <div class="hs-bg-stat">
          <strong>5</strong>
          <span>大天然纹路</span>
        </div>
        <div class="hs-bg-stat">
          <strong>72</strong>
          <span>道手工工序</span>
        </div>
        <div class="hs-bg-stat">
          <strong>12</strong>
          <span>位非遗匠人</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 板块二：工艺流程 -->
  <section class="hs-section hs-craft" id="hs-craft">
    <div class="shell">
      <div class="hs-section-head">
        <span class="eyebrow">Craftsmanship</span>
        <h2>七十二道 · 砚成于刀</h2>
        <p class="sub">从黄石山头采石，到墨香入案，一方砚台需匠人耗时数月。手与石之间，是火候、是耐心，更是世代相传的肌肉记忆。</p>
      </div>

      <div class="hs-craft-flow">
        <div class="hs-craft-card">
          <span class="hs-craft-num">01</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 17l6-6 4 4 8-8"/><path d="M21 7v6h-6"/></svg>
          </div>
          <h4>采石选材</h4>
          <p>匠人深入方城黄石山脉，于裸岩深处依纹路、声响、色泽辨石。一块原石需静养三月，去其浮气。</p>
          <ul>
            <li>沿山势开采，避雨季</li>
            <li>石声清脆者为上品</li>
            <li>含云纹、山水纹优先</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>约 3 个月</strong></div>
        </div>
        <div class="hs-craft-card">
          <span class="hs-craft-num">02</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
          </div>
          <h4>开料制坯</h4>
          <p>原石依匠人构思切割成坯，依石中纹理布局砚池、砚堂、砚额。一刀走错，整石作废。</p>
          <ul>
            <li>手工锯解，不伤纹</li>
            <li>留石形之天然</li>
            <li>大小依用途分级</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>5 - 7 天</strong></div>
        </div>
        <div class="hs-craft-card">
          <span class="hs-craft-num">03</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M5 19l3-3M16 8l3-3"/></svg>
          </div>
          <h4>砚堂深雕</h4>
          <p>核心工序，在砚堂处依纹饰雕琢龙凤、山水、花鸟纹样。每一刀深浅有度，老匠人凭手感与呼吸。</p>
          <ul>
            <li>线刻 / 浅浮 / 透雕</li>
            <li>纹样依石之天然走</li>
            <li>失误率高达 30%</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>30 - 60 天</strong></div>
        </div>
        <div class="hs-craft-card">
          <span class="hs-craft-num">04</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <h4>细磨抛光</h4>
          <p>从砂轮粗磨到水牛皮抛光，72 道打磨工序逐级递进，让石面在光下泛出温润如玉的光泽。</p>
          <ul>
            <li>金刚砂 → 牛皮 → 鹿皮</li>
            <li>水抛 + 蜡养</li>
            <li>检验滴水不渗</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>10 - 15 天</strong></div>
        </div>
        <div class="hs-craft-card">
          <span class="hs-craft-num">05</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z"/></svg>
          </div>
          <h4>开光验墨</h4>
          <p>由非遗传承人亲自开光，研徽墨一锭于砚堂，验下墨之顺、聚墨之久、宿墨之鲜，三试通过方得入匣。</p>
          <ul>
            <li>试徽墨 / 油烟墨</li>
            <li>下墨速度 ≥ 标准</li>
            <li>三日不干为佳品</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>3 - 5 天</strong></div>
        </div>
        <div class="hs-craft-card">
          <span class="hs-craft-num">06</span>
          <div class="hs-craft-ico">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
          </div>
          <h4>题铭入匣</h4>
          <p>匠人于砚底刻下年款、铭文与匠人款识，再由楠木或锦盒珍藏，附鉴定证书与匠人手书。</p>
          <ul>
            <li>篆 / 隶 / 行 三体可选</li>
            <li>楠木匣 / 织锦套</li>
            <li>含传承谱系卡</li>
          </ul>
          <div class="duration"><small>耗时</small><strong>2 - 3 天</strong></div>
        </div>
      </div>

      <div class="hs-craft-strip">
        <div>
          <h5>非遗工坊 · 实地探访</h5>
          <p>预约百珍坊方城工坊，实地观看原石开采、雕刻、抛光全流程，并由匠人带您选一方独属于您的石。</p>
        </div>
        <a class="btn" href="contact.html">预约探访 →</a>
      </div>
    </div>
  </section>

  <!-- 板块三：砚林集珍 -->
  <section class="hs-section hs-coll" id="hs-coll">
    <div class="shell">
      <div class="hs-section-head">
        <span class="eyebrow">Collection</span>
        <h2>砚林集珍</h2>
        <p class="sub">百珍坊精选八方黄石砚珍品，每方均由非遗传承人亲制，附鉴真证书与匠人手书铭文，可即购、可预订、可入拍。</p>
      </div>

      <div class="hs-coll-toolbar">
        <div class="hs-coll-filters">
          <button class="hs-coll-filter active" data-cat="all">全部</button>
          <button class="hs-coll-filter" data-cat="classic">经典款</button>
          <button class="hs-coll-filter" data-cat="rare">珍藏款</button>
          <button class="hs-coll-filter" data-cat="modern">现代款</button>
          <button class="hs-coll-filter" data-cat="gift">商务礼品</button>
        </div>
        <div class="hs-coll-sort">合计 <em>8</em> 件 · 默认按珍稀度排序</div>
      </div>

      <div class="hs-coll-grid" id="hsCollGrid">
        <a class="hs-prod" href="detail-product1.html" data-cat="classic">
          <div class="hs-prod-img">
            <img src="uploads/product1.jpg" alt="云龙纹砚台">
            <span class="hs-prod-tag">经典</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 001</span>
            <h4 class="hs-prod-name">方城黄石砚 · 云龙纹砚台</h4>
            <p class="hs-prod-meta">浮雕云龙环绕砚池，气韵磅礴，石中天然山水纹清晰可见。</p>
            <div class="hs-prod-spec">
              <span>20×14cm</span><span>原石</span><span>浮雕</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>3,680</div>
              <div class="hs-prod-sold">已售 <em>128</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product2.html" data-cat="classic">
          <div class="hs-prod-img">
            <img src="uploads/product2.jpg" alt="墨池澄心砚">
            <span class="hs-prod-tag pine">文人</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 002</span>
            <h4 class="hs-prod-name">方城黄石砚 · 墨池澄心砚</h4>
            <p class="hs-prod-meta">圆润端庄，发墨如油，文人雅士书斋首选。</p>
            <div class="hs-prod-spec">
              <span>16×12cm</span><span>圆形</span><span>素面</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>2,880</div>
              <div class="hs-prod-sold">已售 <em>96</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product3.html" data-cat="modern">
          <div class="hs-prod-img">
            <img src="uploads/product3.jpg" alt="方形君子砚">
            <span class="hs-prod-tag clay">新品</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 003</span>
            <h4 class="hs-prod-name">方城黄石砚 · 方形君子砚</h4>
            <p class="hs-prod-meta">四方端正，朴素无华，含君子如玉之意，馈赠首选。</p>
            <div class="hs-prod-spec">
              <span>15×15cm</span><span>方形</span><span>素雕</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>1,980</div>
              <div class="hs-prod-sold">已售 <em>156</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product4.html" data-cat="rare">
          <div class="hs-prod-img">
            <img src="uploads/product4.jpg" alt="龙凤呈祥珍藏版">
            <span class="hs-prod-tag gold">限量</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 004</span>
            <h4 class="hs-prod-name">方城黄石砚 · 龙凤呈祥珍藏版</h4>
            <p class="hs-prod-meta">非遗传承人亲制，全球限量 18 方，附传承谱系卡。</p>
            <div class="hs-prod-spec">
              <span>22×16cm</span><span>透雕</span><span>限量18</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>12,800</div>
              <div class="hs-prod-sold">已售 <em>14</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product5.html" data-cat="modern">
          <div class="hs-prod-img">
            <img src="uploads/stone-zishi.jpg" alt="竹节纹砚台">
            <span class="hs-prod-tag pine">文人</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 005</span>
            <h4 class="hs-prod-name">方城黄石砚 · 竹节纹砚台</h4>
            <p class="hs-prod-meta">仿竹节造型，节节高升，含君子有节之寓意。</p>
            <div class="hs-prod-spec">
              <span>18×10cm</span><span>仿竹</span><span>浅浮</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>2,280</div>
              <div class="hs-prod-sold">已售 <em>78</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product6.html" data-cat="gift">
          <div class="hs-prod-img">
            <img src="uploads/stone-qingzishi.jpg" alt="兰亭序砚台">
            <span class="hs-prod-tag">经典</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 006</span>
            <h4 class="hs-prod-name">方城黄石砚 · 兰亭序砚台</h4>
            <p class="hs-prod-meta">砚背阴刻王羲之《兰亭集序》全文，文气盎然。</p>
            <div class="hs-prod-spec">
              <span>20×13cm</span><span>线刻</span><span>含礼盒</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>3,280</div>
              <div class="hs-prod-sold">已售 <em>62</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product7.html" data-cat="rare">
          <div class="hs-prod-img">
            <img src="uploads/stone-fengyan.jpg" alt="太极八卦砚">
            <span class="hs-prod-tag gold">限量</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 007</span>
            <h4 class="hs-prod-name">方城黄石砚 · 太极八卦砚</h4>
            <p class="hs-prod-meta">圆形砚体外刻八卦图，内含太极池，藏家级珍品。</p>
            <div class="hs-prod-spec">
              <span>Ø18cm</span><span>透雕</span><span>限量36</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>5,680</div>
              <div class="hs-prod-sold">已售 <em>22</em></div>
            </div>
          </div>
        </a>
        <a class="hs-prod" href="detail-product8.html" data-cat="gift">
          <div class="hs-prod-img">
            <img src="uploads/stone-moshi.jpg" alt="麒麟献瑞砚">
            <span class="hs-prod-tag clay">新品</span>
            <span class="hs-prod-fav">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </span>
          </div>
          <div class="hs-prod-body">
            <span class="hs-prod-id">NO. 008</span>
            <h4 class="hs-prod-name">方城黄石砚 · 麒麟献瑞砚</h4>
            <p class="hs-prod-meta">高浮雕麒麟献瑞，气势恢宏，乔迁开业首选贺礼。</p>
            <div class="hs-prod-spec">
              <span>24×18cm</span><span>高浮</span><span>含锦盒</span>
            </div>
            <div class="hs-prod-foot">
              <div class="hs-prod-price"><small>¥</small>6,680</div>
              <div class="hs-prod-sold">已售 <em>34</em></div>
            </div>
          </div>
        </a>
      </div>

      <div class="hs-coll-cta">
        <a href="cat-wenfang.html">查看更多文房雅器
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      </div>
    </div>
  </section>

</main>

<script>
  // 砚林集珍：分类筛选
  (function(){
    var btns = document.querySelectorAll('.hs-coll-filter');
    var cards = document.querySelectorAll('#hsCollGrid .hs-prod');
    btns.forEach(function(b){
      b.addEventListener('click', function(){
        btns.forEach(function(x){x.classList.remove('active');});
        b.classList.add('active');
        var cat = b.getAttribute('data-cat');
        var visible = 0;
        cards.forEach(function(c){
          var ok = (cat === 'all' || c.getAttribute('data-cat') === cat);
          c.style.display = ok ? '' : 'none';
          if (ok) visible++;
        });
        var sortNode = document.querySelector('.hs-coll-sort em');
        if (sortNode) sortNode.textContent = visible;
      });
    });
  })();
</script>

"""

new_src = head + "\n" + BODY + "\n" + tail

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(new_src)

print("[OK] detail-product1.html rebuilt, size =", len(new_src))
