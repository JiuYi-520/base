# -*- coding: utf-8 -*-
"""Enhance detail-product1.html with more sections and richer content."""
import codecs, re, os

PATH = r"D:\2\Kimi_Agent_黄石砚商城模型\baizhenfang-site\detail-product1.html"

with codecs.open(PATH, "r", "utf-8") as f:
    html = f.read()

# ============ 1. 注入额外 CSS（在 </style> 之前）============
EXTRA_CSS = r"""
/* ======= 黄石砚增强补充样式 v2 ======= */
/* 锚点导航 */
.hs-anchor{position:sticky;top:76px;z-index:30;background:rgba(28,24,18,.96);backdrop-filter:blur(14px);
  border-bottom:1px solid rgba(185,151,91,.18);padding:0;}
.hs-anchor .shell{max-width:1240px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:0;overflow-x:auto;}
.hs-anchor a{flex-shrink:0;padding:16px 22px;color:rgba(255,249,237,.6);font-size:13px;letter-spacing:3px;
  border-bottom:2px solid transparent;transition:all .25s;white-space:nowrap;}
.hs-anchor a:hover{color:#B9975B;}
.hs-anchor a.active{color:#B9975B;border-bottom-color:#B9975B;}
.hs-anchor .anc-num{font-family:"Playfair Display",serif;font-size:11px;letter-spacing:2px;margin-right:8px;color:#A85F3D;}

/* 时间轴（背景区） */
.hs-timeline{margin-top:60px;padding:30px 0;border-top:1px dashed rgba(23,20,17,.18);border-bottom:1px dashed rgba(23,20,17,.18);}
.hs-timeline-track{display:grid;grid-template-columns:repeat(5,1fr);gap:0;position:relative;}
.hs-timeline-track::before{content:"";position:absolute;left:5%;right:5%;top:38px;height:2px;
  background:linear-gradient(90deg,rgba(185,151,91,.15) 0%,#B9975B 50%,rgba(185,151,91,.15) 100%);}
.hs-tl-node{position:relative;text-align:center;padding-top:0;}
.hs-tl-dot{width:14px;height:14px;border-radius:50%;background:#B9975B;border:3px solid #F6F0E6;margin:32px auto 0;
  box-shadow:0 0 0 3px rgba(185,151,91,.25);position:relative;z-index:2;}
.hs-tl-era{margin-top:12px;color:#A85F3D;font-family:"Playfair Display",serif;font-size:14px;letter-spacing:2px;font-weight:700;}
.hs-tl-year{display:block;margin-top:2px;color:#766D61;font-size:11px;letter-spacing:1.5px;}
.hs-tl-desc{margin-top:10px;color:#3a322a;font-size:12px;line-height:1.7;letter-spacing:.5px;padding:0 8px;}
@media (max-width:780px){.hs-timeline-track{grid-template-columns:repeat(2,1fr);gap:30px;}
  .hs-timeline-track::before{display:none;}}

/* 五大纹路（背景区） */
.hs-stone-types{margin-top:70px;}
.hs-stone-head{text-align:center;margin-bottom:34px;}
.hs-stone-head h3{font-size:22px;letter-spacing:5px;font-weight:800;color:#171411;}
.hs-stone-head h3::before{content:"";display:inline-block;width:30px;height:1px;background:#B9975B;
  vertical-align:middle;margin-right:14px;}
.hs-stone-head h3::after{content:"";display:inline-block;width:30px;height:1px;background:#B9975B;
  vertical-align:middle;margin-left:14px;}
.hs-stone-head small{display:block;margin-top:10px;color:#766D61;font-size:13px;letter-spacing:2px;}
.hs-stone-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;}
@media (max-width:980px){.hs-stone-grid{grid-template-columns:repeat(2,1fr);}}
.hs-stone-card{background:#fff;border:1px solid rgba(23,20,17,.08);overflow:hidden;
  transition:all .3s;display:flex;flex-direction:column;}
.hs-stone-card:hover{transform:translateY(-4px);border-color:#B9975B;box-shadow:0 18px 32px rgba(168,95,61,.1);}
.hs-stone-card .img{aspect-ratio:1;background-size:cover;background-position:center;background-color:#1c1812;}
.hs-stone-card .body{padding:18px 16px 20px;}
.hs-stone-card h5{font-size:15px;letter-spacing:3px;font-weight:800;color:#171411;margin-bottom:6px;}
.hs-stone-card small{color:#A85F3D;font-family:"Playfair Display",serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:700;}
.hs-stone-card p{margin-top:10px;color:#766D61;font-size:12px;line-height:1.7;letter-spacing:.5px;}
.hs-stone-card .rare{display:inline-block;margin-top:10px;padding:2px 8px;background:rgba(185,151,91,.12);
  color:#A85F3D;font-size:10px;letter-spacing:1.5px;font-weight:700;}

/* 工艺：匠人（深色） */
.hs-master{margin-top:70px;display:grid;grid-template-columns:1.3fr 1fr;gap:50px;align-items:center;
  padding:50px;background:rgba(255,249,237,.03);border:1px solid rgba(185,151,91,.18);}
@media (max-width:980px){.hs-master{grid-template-columns:1fr;padding:40px 28px;}}
.hs-master-text .eye{color:#B9975B;font-family:"Playfair Display",serif;font-size:12px;letter-spacing:4px;font-weight:700;text-transform:uppercase;}
.hs-master-text h3{margin:14px 0 18px;font-size:30px;letter-spacing:5px;font-weight:900;color:#FFF9ED;line-height:1.3;}
.hs-master-text h3 em{color:#B9975B;font-style:normal;}
.hs-master-text .quote{padding:20px 24px;background:rgba(185,151,91,.06);border-left:3px solid #B9975B;
  color:rgba(255,249,237,.78);font-size:14px;line-height:2;letter-spacing:1px;margin-bottom:24px;font-style:italic;}
.hs-master-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
.hs-master-meta div{padding:14px;background:rgba(255,249,237,.04);border:1px solid rgba(185,151,91,.18);}
.hs-master-meta strong{display:block;color:#B9975B;font-family:"Playfair Display",serif;font-size:24px;font-weight:700;}
.hs-master-meta span{display:block;margin-top:6px;color:rgba(255,249,237,.5);font-size:11px;letter-spacing:2px;}
.hs-master-fig{position:relative;aspect-ratio:4/5;background:#0e0c09 center/cover;
  border:1px solid rgba(185,151,91,.25);overflow:hidden;}
.hs-master-fig img{width:100%;height:100%;object-fit:cover;filter:saturate(.9) brightness(.94);}
.hs-master-fig .badge{position:absolute;left:18px;bottom:18px;padding:8px 14px;background:rgba(28,24,18,.85);
  border:1px solid rgba(185,151,91,.4);color:#B9975B;font-size:11px;letter-spacing:3px;font-weight:700;}

/* 工艺：质量保障（深色） */
.hs-craft-quality{margin-top:60px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
@media (max-width:880px){.hs-craft-quality{grid-template-columns:repeat(2,1fr);}}
.hs-quality-item{padding:24px 22px;background:rgba(255,249,237,.04);border:1px solid rgba(185,151,91,.18);
  transition:all .25s;}
.hs-quality-item:hover{border-color:#B9975B;transform:translateY(-3px);}
.hs-quality-item .num{color:#B9975B;font-family:"Playfair Display",serif;font-size:30px;font-weight:700;line-height:1;}
.hs-quality-item h5{margin:12px 0 6px;color:#FFF9ED;font-size:14px;letter-spacing:3px;font-weight:800;}
.hs-quality-item p{color:rgba(255,249,237,.55);font-size:12px;line-height:1.7;letter-spacing:.5px;}

/* 砚林集珍：尺寸指南 */
.hs-size-guide{margin-top:70px;padding:36px;background:#fff;border:1px solid rgba(23,20,17,.08);
  display:grid;grid-template-columns:1fr 1.2fr;gap:50px;align-items:center;}
@media (max-width:880px){.hs-size-guide{grid-template-columns:1fr;padding:28px;}}
.hs-size-text h3{font-size:20px;letter-spacing:4px;font-weight:800;margin-bottom:14px;color:#171411;}
.hs-size-text h3 small{display:block;margin-top:6px;color:#A85F3D;font-family:"Playfair Display",serif;
  font-size:12px;letter-spacing:3px;text-transform:uppercase;font-weight:700;}
.hs-size-text p{color:#3a322a;font-size:13px;line-height:2;letter-spacing:.5px;margin-bottom:14px;}
.hs-size-table{width:100%;border-collapse:collapse;font-size:13px;}
.hs-size-table th,.hs-size-table td{padding:12px 14px;text-align:left;letter-spacing:1px;}
.hs-size-table thead th{background:#171411;color:#B9975B;font-size:12px;letter-spacing:2.5px;font-weight:700;}
.hs-size-table tbody tr{border-bottom:1px dashed rgba(23,20,17,.1);}
.hs-size-table tbody tr:nth-child(even){background:rgba(185,151,91,.04);}
.hs-size-table td:first-child{color:#A85F3D;font-weight:700;letter-spacing:2px;}
.hs-size-table td:nth-child(3){font-family:"Playfair Display",serif;color:#171411;font-weight:600;}

/* 砚林集珍：用户评价 */
.hs-reviews{margin-top:70px;}
.hs-reviews-head{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:24px;flex-wrap:wrap;gap:14px;}
.hs-reviews-head h3{font-size:22px;letter-spacing:4px;font-weight:800;color:#171411;}
.hs-reviews-head h3::before{content:"";display:inline-block;width:30px;height:2px;background:#B9975B;
  vertical-align:middle;margin-right:14px;}
.hs-reviews-stat{color:#766D61;font-size:13px;letter-spacing:2px;}
.hs-reviews-stat strong{color:#A85F3D;font-family:"Playfair Display",serif;font-size:22px;font-weight:700;letter-spacing:1px;margin-right:4px;}
.hs-reviews-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
@media (max-width:880px){.hs-reviews-grid{grid-template-columns:1fr;}}
.hs-review{padding:24px 22px;background:#fff;border:1px solid rgba(23,20,17,.08);transition:all .25s;}
.hs-review:hover{border-color:#B9975B;box-shadow:0 14px 28px rgba(168,95,61,.08);}
.hs-review-head{display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:14px;border-bottom:1px dashed rgba(23,20,17,.1);}
.hs-review-avt{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#B9975B,#d4b876);
  display:flex;align-items:center;justify-content:center;color:#1c1812;font-weight:700;font-size:14px;letter-spacing:1px;flex-shrink:0;}
.hs-review-info{flex:1;min-width:0;}
.hs-review-info strong{display:block;color:#171411;font-size:14px;letter-spacing:1.5px;}
.hs-review-info small{color:#766D61;font-size:11px;letter-spacing:1px;}
.hs-review-stars{color:#B9975B;font-size:13px;letter-spacing:1px;}
.hs-review p{color:#3a322a;font-size:13px;line-height:1.9;letter-spacing:.5px;}
.hs-review .item{margin-top:14px;padding-top:14px;border-top:1px dashed rgba(23,20,17,.1);
  display:flex;justify-content:space-between;color:#766D61;font-size:11px;letter-spacing:1px;}
.hs-review .item em{color:#A85F3D;font-style:normal;font-family:"Playfair Display",serif;font-weight:700;font-size:12px;}

/* FAQ */
.hs-faq{margin-top:70px;display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
@media (max-width:780px){.hs-faq{grid-template-columns:1fr;}}
.hs-faq-item{padding:22px 26px;background:#fff;border:1px solid rgba(23,20,17,.08);
  transition:all .25s;cursor:pointer;}
.hs-faq-item:hover{border-color:#B9975B;}
.hs-faq-item h5{display:flex;justify-content:space-between;align-items:center;font-size:15px;letter-spacing:2px;
  font-weight:800;color:#171411;margin-bottom:10px;}
.hs-faq-item h5 .q{color:#A85F3D;font-family:"Playfair Display",serif;font-size:14px;margin-right:10px;}
.hs-faq-item p{color:#766D61;font-size:13px;line-height:1.9;letter-spacing:.5px;}

/* 最终 CTA */
.hs-final-cta{margin-top:80px;padding:60px 50px;background:linear-gradient(135deg,#1c1812 0%,#2a2118 100%);
  color:#FFF9ED;display:grid;grid-template-columns:1.4fr 1fr;gap:50px;align-items:center;
  border:1px solid rgba(185,151,91,.25);position:relative;overflow:hidden;}
@media (max-width:880px){.hs-final-cta{grid-template-columns:1fr;padding:40px 28px;}}
.hs-final-cta::before{content:"";position:absolute;right:-100px;top:-100px;width:300px;height:300px;
  border-radius:50%;background:radial-gradient(circle,rgba(185,151,91,.18) 0%,transparent 70%);}
.hs-final-cta h3{font-size:28px;letter-spacing:5px;font-weight:900;line-height:1.3;margin-bottom:18px;color:#FFF9ED;position:relative;}
.hs-final-cta h3 em{color:#B9975B;font-style:normal;}
.hs-final-cta p{color:rgba(255,249,237,.68);font-size:14px;line-height:1.95;letter-spacing:1px;margin-bottom:24px;position:relative;}
.hs-final-cta-actions{display:flex;gap:12px;flex-wrap:wrap;position:relative;}
.hs-final-cta-actions a{padding:14px 28px;font-size:13px;letter-spacing:3px;font-weight:800;
  display:inline-flex;align-items:center;gap:8px;transition:all .2s;}
.hs-final-cta-actions .pri{background:#B9975B;color:#1c1812;}
.hs-final-cta-actions .pri:hover{background:#d4b876;}
.hs-final-cta-actions .ghost{border:1px solid rgba(185,151,91,.45);color:#FFF9ED;}
.hs-final-cta-actions .ghost:hover{border-color:#B9975B;background:rgba(185,151,91,.08);}
.hs-final-cta-fig{position:relative;}
.hs-final-cta-fig img{width:100%;aspect-ratio:1;object-fit:cover;border:1px solid rgba(185,151,91,.3);}
.hs-final-cta-fig .seal{position:absolute;top:14px;right:14px;width:62px;height:62px;border-radius:50%;
  background:rgba(28,24,18,.8);border:1px solid #B9975B;color:#B9975B;
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:11px;letter-spacing:1px;font-weight:800;}

/* 服务保障条 */
.hs-service{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:70px;
  background:#fff;border:1px solid rgba(23,20,17,.08);}
@media (max-width:780px){.hs-service{grid-template-columns:repeat(2,1fr);}}
.hs-svc{padding:26px 22px;border-right:1px solid rgba(23,20,17,.06);text-align:center;}
.hs-svc:last-child{border-right:none;}
@media (max-width:780px){.hs-svc:nth-child(2){border-right:none;}.hs-svc:nth-child(-n+2){border-bottom:1px solid rgba(23,20,17,.06);}}
.hs-svc .ico{width:42px;height:42px;border-radius:50%;background:rgba(185,151,91,.12);color:#A85F3D;
  display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px;}
.hs-svc h6{color:#171411;font-size:14px;letter-spacing:2.5px;font-weight:800;margin-bottom:4px;}
.hs-svc small{color:#766D61;font-size:11px;letter-spacing:1px;}
"""

html = html.replace("</style>\n", EXTRA_CSS + "\n</style>\n", 1)

# ============ 2. 在 hs-main 之后插入锚点导航 ============
ANCHOR_NAV = """
  <!-- 锚点导航 -->
  <div class="hs-anchor">
    <div class="shell">
      <a href="#hs-bg" class="active"><span class="anc-num">01</span>砚石溯源</a>
      <a href="#hs-craft"><span class="anc-num">02</span>古法工艺</a>
      <a href="#hs-coll"><span class="anc-num">03</span>砚林集珍</a>
      <a href="#hs-reviews"><span class="anc-num">04</span>藏家评说</a>
      <a href="#hs-faq"><span class="anc-num">05</span>常见问题</a>
    </div>
  </div>
"""

html = html.replace("<main class=\"hs-main\">", "<main class=\"hs-main\">\n" + ANCHOR_NAV, 1)

# ============ 3. 在背景板块的 </section> 之前追加：时间轴 + 五大纹路 ============
TIMELINE_AND_STONES = """
      <!-- 千年时间轴 -->
      <div class="hs-timeline">
        <div class="hs-timeline-track">
          <div class="hs-tl-node">
            <div class="hs-tl-dot"></div>
            <div class="hs-tl-era">唐</div>
            <span class="hs-tl-year">公元 700+</span>
            <p class="hs-tl-desc">方城黄石被发现于葛仙翁山，初为文人案头。</p>
          </div>
          <div class="hs-tl-node">
            <div class="hs-tl-dot"></div>
            <div class="hs-tl-era">北宋</div>
            <span class="hs-tl-year">1086 年</span>
            <p class="hs-tl-desc">米芾《砚史》盛赞，列为皇家贡砚，与端歙齐名。</p>
          </div>
          <div class="hs-tl-node">
            <div class="hs-tl-dot"></div>
            <div class="hs-tl-era">明清</div>
            <span class="hs-tl-year">1450 - 1840</span>
            <p class="hs-tl-desc">书院制度兴盛，黄石砚成为江南文人首选。</p>
          </div>
          <div class="hs-tl-node">
            <div class="hs-tl-dot"></div>
            <div class="hs-tl-era">近代</div>
            <span class="hs-tl-year">1980+</span>
            <p class="hs-tl-desc">列入河南省非物质文化遗产，匠艺再兴。</p>
          </div>
          <div class="hs-tl-node">
            <div class="hs-tl-dot"></div>
            <div class="hs-tl-era">当代</div>
            <span class="hs-tl-year">2024</span>
            <p class="hs-tl-desc">百珍坊集结非遗匠人，砚石入云、入网、入礼。</p>
          </div>
        </div>
      </div>

      <!-- 五大天然纹路 -->
      <div class="hs-stone-types">
        <div class="hs-stone-head">
          <h3>五大天然纹路</h3>
          <small>NATURAL TEXTURES OF FANGCHENG STONE</small>
        </div>
        <div class="hs-stone-grid">
          <div class="hs-stone-card">
            <div class="img" style="background-image:url(uploads/stone-qingshi.jpg)"></div>
            <div class="body">
              <small>NO. 01</small>
              <h5>云龙纹</h5>
              <p>石中天然流动云线，似飞龙穿云，气韵磅礴，最为名贵。</p>
              <span class="rare">★★★★★ 极珍</span>
            </div>
          </div>
          <div class="hs-stone-card">
            <div class="img" style="background-image:url(uploads/stone-zishi.jpg)"></div>
            <div class="body">
              <small>NO. 02</small>
              <h5>紫袍玉带</h5>
              <p>紫色石身中横贯白玉带状纹路，富贵端庄，藏家专属。</p>
              <span class="rare">★★★★★ 极珍</span>
            </div>
          </div>
          <div class="hs-stone-card">
            <div class="img" style="background-image:url(uploads/stone-qingzishi.jpg)"></div>
            <div class="body">
              <small>NO. 03</small>
              <h5>青紫晕</h5>
              <p>青紫色调自然过渡，墨色淡雅如远山黛影，文人气韵。</p>
              <span class="rare">★★★★ 上品</span>
            </div>
          </div>
          <div class="hs-stone-card">
            <div class="img" style="background-image:url(uploads/stone-fengyan.jpg)"></div>
            <div class="body">
              <small>NO. 04</small>
              <h5>凤眼纹</h5>
              <p>石面散布如凤眼般的金色斑点，灵动有神，为名匠所好。</p>
              <span class="rare">★★★★ 上品</span>
            </div>
          </div>
          <div class="hs-stone-card">
            <div class="img" style="background-image:url(uploads/stone-moshi.jpg)"></div>
            <div class="body">
              <small>NO. 05</small>
              <h5>墨黛底</h5>
              <p>纯净墨色为底，质地最细，发墨最快，初学者推荐。</p>
              <span class="rare">★★★ 经典</span>
            </div>
          </div>
        </div>
      </div>
"""

# 在第一个 </section> 之前注入（即 hs-bg 区段结尾前）
# 寻找 hs-bg-stats 之后的 </section>
m = re.search(r'(<div class="hs-bg-stats">[\s\S]+?</div>\s*)\n(\s*</section>)', html)
if m:
    html = html.replace(m.group(0), m.group(1) + "\n" + TIMELINE_AND_STONES + "\n" + m.group(2))

# ============ 4. 在工艺板块的 hs-craft-strip 之前插入：匠人 + 质量保障 ============
MASTER_AND_QUALITY = """
      <!-- 非遗匠人 -->
      <div class="hs-master">
        <div class="hs-master-text">
          <span class="eye">Heritage Master</span>
          <h3>非遗传承人 · <em>王廷光</em><br>四十二载，刀下生山河</h3>
          <div class="quote">"一方好砚，从来不是刻出来的，是石头自己长出来的。匠人能做的，只是看见它本来的样子。"</div>
          <div class="hs-master-meta">
            <div><strong>42</strong><span>从艺年限</span></div>
            <div><strong>2,800<small>+</small></strong><span>亲制砚台</span></div>
            <div><strong>16</strong><span>授业弟子</span></div>
          </div>
        </div>
        <div class="hs-master-fig">
          <img src="uploads/banner1.jpg" alt="非遗传承人王廷光">
          <span class="badge">河南省非遗代表传承人</span>
        </div>
      </div>

      <!-- 四重质量保障 -->
      <div class="hs-craft-quality">
        <div class="hs-quality-item">
          <div class="num">01</div>
          <h5>原石溯源</h5>
          <p>每方原石附产地坐标与开采记录，二维码扫描可查全程。</p>
        </div>
        <div class="hs-quality-item">
          <div class="num">02</div>
          <h5>匠人签章</h5>
          <p>砚底铭刻匠人姓名、年款及编号，附匠人手书证书。</p>
        </div>
        <div class="hs-quality-item">
          <div class="num">03</div>
          <h5>百珍鉴真</h5>
          <p>由百珍坊与省非遗中心双重鉴定，附鉴定证书。</p>
        </div>
        <div class="hs-quality-item">
          <div class="num">04</div>
          <h5>终身质保</h5>
          <p>非人为损伤终身免费修复，七日复鉴不符全额退款。</p>
        </div>
      </div>
"""

# 在 hs-craft-strip 之前插入
html = html.replace(
    '<div class="hs-craft-strip">',
    MASTER_AND_QUALITY + "\n      <div class=\"hs-craft-strip\">",
    1
)

# ============ 5. 在砚林集珍板块末尾追加：尺寸指南 + 评价 + FAQ + 服务保障 + Final CTA ============
COLL_EXTRA = """
      <!-- 尺寸 / 规格指南 -->
      <div class="hs-size-guide">
        <div class="hs-size-text">
          <h3>规格指南<small>SIZE &amp; USE GUIDE</small></h3>
          <p>不同尺寸的砚台对应不同的书写场景与藏家需求。从案头小品到镇室重宝，百珍坊为您备齐五档规格选择。</p>
          <p>初学者建议从中号入手，平衡握感与发墨；藏家级则推荐 22cm 以上限量款，纹路完整、刀工繁复。</p>
        </div>
        <table class="hs-size-table">
          <thead>
            <tr>
              <th>规格</th><th>尺寸</th><th>重量</th><th>适用</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>小</td><td>14×10 cm</td><td>0.6 kg</td><td>案头小品 / 旅行携带</td></tr>
            <tr><td>中</td><td>18×12 cm</td><td>1.2 kg</td><td>日常临帖 / 入门首选</td></tr>
            <tr><td>大</td><td>22×16 cm</td><td>2.4 kg</td><td>书房常用 / 创作书法</td></tr>
            <tr><td>特大</td><td>26×18 cm</td><td>3.8 kg</td><td>商务赠礼 / 藏家级</td></tr>
            <tr><td>巨制</td><td>30 cm+</td><td>5 kg+</td><td>限量定制 / 镇室之宝</td></tr>
          </tbody>
        </table>
      </div>

      <!-- 服务保障 -->
      <div class="hs-service">
        <div class="hs-svc">
          <div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg></div>
          <h6>百珍鉴真</h6>
          <small>非遗中心双重鉴定</small>
        </div>
        <div class="hs-svc">
          <div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="6" width="18" height="14" rx="1"/><path d="M3 10h18"/></svg></div>
          <h6>顺丰保价</h6>
          <small>全程保价直送到家</small>
        </div>
        <div class="hs-svc">
          <div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 12a9 9 0 0 1 9-9 9 9 0 0 1 6.5 2.7L21 3"/><path d="M21 3v6h-6"/></svg></div>
          <h6>七日复鉴</h6>
          <small>不符全额退款</small>
        </div>
        <div class="hs-svc">
          <div class="ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
          <h6>专家咨询</h6>
          <small>1对1选砚顾问</small>
        </div>
      </div>

      <!-- 藏家评说 -->
      <div class="hs-reviews" id="hs-reviews">
        <div class="hs-reviews-head">
          <h3>藏家评说</h3>
          <div class="hs-reviews-stat"><strong>4.9</strong>分 · 共 <strong>328</strong> 条真实评价 · 好评率 99.2%</div>
        </div>
        <div class="hs-reviews-grid">
          <div class="hs-review">
            <div class="hs-review-head">
              <div class="hs-review-avt">沈</div>
              <div class="hs-review-info">
                <strong>沈先生 · 上海</strong>
                <small>资深书法藏家 · 已购 3 方</small>
              </div>
              <span class="hs-review-stars">★★★★★</span>
            </div>
            <p>云龙纹这方收到后非常惊艳，纹路清晰流畅，发墨极快。配的楠木匣子做工考究，书房气场拉满。</p>
            <div class="item">
              <span>云龙纹砚台</span>
              <em>2024.05.12</em>
            </div>
          </div>
          <div class="hs-review">
            <div class="hs-review-head">
              <div class="hs-review-avt">陈</div>
              <div class="hs-review-info">
                <strong>陈先生 · 北京</strong>
                <small>企业商务赠礼</small>
              </div>
              <span class="hs-review-stars">★★★★★</span>
            </div>
            <p>买了 12 方麒麟献瑞砚送日本客户，对方反馈非常喜欢中国文化的含义，包装精美，完全提升了品牌形象。</p>
            <div class="item">
              <span>麒麟献瑞砚 × 12</span>
              <em>2024.04.28</em>
            </div>
          </div>
          <div class="hs-review">
            <div class="hs-review-head">
              <div class="hs-review-avt">林</div>
              <div class="hs-review-info">
                <strong>林女士 · 杭州</strong>
                <small>书法老师</small>
              </div>
              <span class="hs-review-stars">★★★★★</span>
            </div>
            <p>送给学生的兰亭序砚台真是好物，背面刻字工整漂亮，孩子拿到爱不释手，说要好好临帖了。</p>
            <div class="item">
              <span>兰亭序砚台</span>
              <em>2024.04.15</em>
            </div>
          </div>
        </div>
      </div>

      <!-- 常见问题 -->
      <div class="hs-faq" id="hs-faq">
        <div class="hs-faq-item">
          <h5><span><span class="q">Q1</span>方城黄石砚和端砚、歙砚有什么区别？</span></h5>
          <p>三者并称四大名砚。黄石砚石质温润，发墨最快，颜色丰富以紫黄为主；端砚石眼名贵，色泽偏紫；歙砚以金星金晕著称，色偏青黑。</p>
        </div>
        <div class="hs-faq-item">
          <h5><span><span class="q">Q2</span>新砚买回来需要"开砚"吗？怎么操作？</span></h5>
          <p>建议开砚。用新蜡涂抹砚堂、温水浸泡 10 分钟、清水冲洗后试墨即可。前 3 次研墨建议轻磨，让石面与墨条充分契合。</p>
        </div>
        <div class="hs-faq-item">
          <h5><span><span class="q">Q3</span>砚台日常如何保养？</span></h5>
          <p>用后及时用清水冲洗，软布擦干。不可使用洗洁精或硬物刮擦。久置不用时建议涂少量植物油保养，防止开裂。</p>
        </div>
        <div class="hs-faq-item">
          <h5><span><span class="q">Q4</span>每方砚台都附鉴定证书吗？</span></h5>
          <p>是的。每方砚台均附《百珍坊鉴真证书》和河南省非遗中心《非遗工艺认证》，含匠人手书签名、原石溯源二维码。</p>
        </div>
        <div class="hs-faq-item">
          <h5><span><span class="q">Q5</span>限量款卖完还会再产吗？</span></h5>
          <p>不会。限量款由非遗传承人亲制，编号唯一，售完不再补单。藏家可关注百珍坊拍卖中心，参与稀缺款竞拍。</p>
        </div>
        <div class="hs-faq-item">
          <h5><span><span class="q">Q6</span>能否定制铭文或私人款识？</span></h5>
          <p>可以。¥3,000 以上款式支持砚底刻字（含篆/隶/行三体），¥10,000 以上珍藏款可申请匠人专属定制设计。</p>
        </div>
      </div>

      <!-- 最终 CTA -->
      <div class="hs-final-cta">
        <div>
          <h3>方寸之间，<br>承一段<em>九百年</em>文脉</h3>
          <p>从黄石山头，到您书房案上，每一方砚台都是一段时间的旅行。百珍坊愿您在墨香中，与古人遥相对望。</p>
          <div class="hs-final-cta-actions">
            <a class="pri" href="#hs-coll">浏览砚林集珍
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
            <a class="ghost" href="contact.html">预约工坊探访</a>
            <a class="ghost" href="auction.html">查看在拍珍品</a>
          </div>
        </div>
        <div class="hs-final-cta-fig">
          <img src="uploads/stone-qingshi.jpg" alt="方城黄石砚">
          <span class="seal">非遗<br>砚艺</span>
        </div>
      </div>
"""

# 在 hs-coll-cta 之前插入
html = html.replace(
    '<div class="hs-coll-cta">',
    COLL_EXTRA + "\n\n      <div class=\"hs-coll-cta\">",
    1
)

# ============ 6. 注入锚点滚动 spy 脚本 ============
SPY_JS = r"""
<script>
// 锚点导航滚动联动
(function(){
  var anchors = document.querySelectorAll('.hs-anchor a');
  var sections = ['hs-bg','hs-craft','hs-coll','hs-reviews','hs-faq']
    .map(function(id){ return document.getElementById(id); }).filter(Boolean);
  function onScroll(){
    var top = window.scrollY + 200;
    var current = sections[0] && sections[0].id;
    sections.forEach(function(s){
      if (s.offsetTop <= top) current = s.id;
    });
    anchors.forEach(function(a){
      a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  // 平滑滚动
  anchors.forEach(function(a){
    a.addEventListener('click', function(e){
      var id = a.getAttribute('href').slice(1);
      var node = document.getElementById(id);
      if (node) {
        e.preventDefault();
        window.scrollTo({ top: node.offsetTop - 130, behavior: 'smooth' });
      }
    });
  });
})();
</script>
"""

# 在 </main> 之后追加（在已有 collection filter script 之后）
html = html.replace("</main>\n", "</main>\n" + SPY_JS + "\n", 1)

with codecs.open(PATH, "w", "utf-8") as f:
    f.write(html)

print("[OK] enhanced. size =", len(html))
