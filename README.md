# 方城特产百珍坊

方城（河南南阳）地方特产展示型静态站点，主打**方城黄石砚**，兼营美食、文玩与养生品类。

纯静态 HTML / CSS / JavaScript，**无构建步骤、无依赖、无包管理器**。克隆下来即可直接由任意静态服务器托管。

## 页面构成

| 分类 | 文件 |
|---|---|
| 首页 | `index.html` |
| 类目页 | `cat-gongyi.html`（工艺收藏）、`cat-meishi.html`（方城美食）、`cat-wenfang.html`（文房雅器）、`cat-yangsheng.html`（养生滋补） |
| 黄石砚商品页 | `detail-product1.html` ~ `detail-product8.html` |
| 其他商品页 | `detail-brush`（毛笔）、`detail-danshen`（丹参）、`detail-fan`（折扇）、`detail-guokui`（锅盔）、`detail-huimian`（烩面）、`detail-ink`（徽墨）、`detail-jade`（玉器）、`detail-mushroom`（菌菇）、`detail-peanut`（花生）、`detail-pear`（梨）、`detail-shihou`（石雕）、`detail-silk`（蚕丝被） |
| 交易与竞拍 | `auction.html`、`auction-result.html`、`cart.js`、`sku.js` |
| 账号与会员 | `login.html`、`admin-login.html`、`member-center.html` |
| 品牌与增值服务 | `brand-story.html`、`craft.html`、`custom-gift.html`、`contact.html`、`baizhen-collection.html` |
| 共享资源 | `shared-pages.css`、`collection-redesign.css`、`detail-floating-nav.css`、`site-fixes.css`、`favorites.js`、`lightbox.js` |
| 图片 | `uploads/`（约 11 MB） |

各页面样式以内联 `<style>` 为主，辅以上述共享样式表。

## 本地预览

```sh
python -m http.server 8000
```

然后访问 <http://localhost:8000/>。用浏览器直接打开 `index.html` 也可，但部分页面依赖同源 JavaScript，建议走 HTTP。

## 部署

由 GitHub Pages 托管，通过 Actions 自动部署（`.github/workflows/deploy-pages.yml`），推送到 `main` 即触发。

部署时只发布站点实际提供的文件：`_normalize/` 被显式排除，因为它是维护脚本而非站点内容。

## CI

`.github/scripts/check-site.mjs` 在每次 push 与 PR 时运行，**失败条件**：

- 文本文件包含非法 UTF-8 字节
- 出现 `?/tag>` 形式的损坏闭合标签（`<` 被吞掉）——`<title>` 未闭合会让**整页渲染空白**，这类故障不会报错，只会静默变白
- 某个 HTML 缺少合法的 `<title>`
- 任意本地 `href` / `src` / `url()` 指向不存在的文件
- 使用了根绝对路径（`/x.css`），它会破坏项目级 Pages 的子路径部署

残留的 `U+FFFD` 替换字符只产生**警告**、不使构建失败——它记录的是下述历史损坏，而不是新增缺陷。

## `_normalize/`

存放一次性维护脚本（Python）与注入用的 CSS/HTML 片段，用于当初生成和修订这些页面。**它不是构建流程**，部署时不需要运行，全部读写操作都显式声明了 `encoding='utf-8'`。

---

## 已知问题：13 个页面的字符损坏

### 起因

13 个页面经历过一次编码事故：**UTF-8 字节被误当作 cp936（GBK）解码，之后又存回 UTF-8**。变换机制已通过往返实验证实（例如 `方城` 的字节经该变换必然产生 `鏂瑰煄`）。

同时，解码器把无效字节对替换成 `?` 或写入私有区（U+E000–F8FF），**这一过程会吞掉字节**，因此损坏无法通过逆向编码完全还原。

`_normalize/` 内的脚本经逐一核查**均使用了正确的 `encoding='utf-8'`**，不是本次事故的成因；肇事工具未能确定。

### 后果

- **350 处闭合标签的 `<` 被吞掉**（`</title>`、`</p>`、`</div>`、`</strong>`、`</li>`、`</h1>` 等）。其中 `<title>` 未闭合会把文档剩余部分全部吞进标题，导致页面**渲染为空白**。
- 大量中文字符被不可逆破坏。

### 已修复

- **结构 100% 修复**，35 个页面全部可正常解析与渲染（经 HTML5 解析器逐页验证）。
- **13 个页面标题完整恢复**。
- 可依据证据确定的标点已恢复。

### 仍未恢复

**5784 个 `U+FFFD`**，其中：

- **1951 个**位于注释与内联样式中，**不影响渲染**
- **3833 个**位于可见标记中（含正文、`style=`、`aria-label=`、`alt` 等属性）

这些字符在事故发生时已被销毁，**无法由程序还原**，需要人工依据上下文逐处校对。

| 文件 | 残留 `U+FFFD` | 其中可见 |
|---|---:|---:|
| `admin-login.html` | 30 | 7 |
| `detail-brush.html` | 511 | 310 |
| `detail-danshen.html` | 471 | 320 |
| `detail-fan.html` | 467 | 317 |
| `detail-guokui.html` | 467 | 316 |
| `detail-huimian.html` | 458 | 308 |
| `detail-ink.html` | 496 | 312 |
| `detail-jade.html` | 493 | 308 |
| `detail-mushroom.html` | 464 | 314 |
| `detail-peanut.html` | 461 | 311 |
| `detail-pear.html` | 461 | 311 |
| `detail-shihou.html` | 540 | 384 |
| `detail-silk.html` | 465 | 315 |

`index.html`、`member-center.html`、`auction.html`、`detail-product1..8.html` 等其余 22 个页面**未受影响**。
