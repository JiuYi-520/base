/* 百珍坊 · SKU 联动选择器 sku.js
   Task B3: 读取页面内联 #skuData JSON → 渲染规格按钮 → 联动价格与购物车
   在 detail-*.html </body> 前引入即可自动初始化
*/
(function () {
  'use strict';

  function init() {
    var dataEl = document.getElementById('skuData');
    if (!dataEl) return; // 页面无 SKU 数据，静默退出

    var data;
    try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
    if (!data || !data.skus || !data.skus.length) return;

    var ctaBar = document.querySelector('.cta-bar');
    if (!ctaBar) return;

    var selectedIdx = -1; // 未选中

    /* ---- 构建选择器 ---- */
    var wrap = document.createElement('div');
    wrap.className = 'sku-wrap';
    wrap.innerHTML = [
      '<div class="sku-label">选择规格</div>',
      '<div class="sku-selector" id="bzSkuSelector">',
        data.skus.map(function (sku, i) {
          var disabled = sku.stock === 0 ? ' sku-btn--disabled' : '';
          return '<button class="sku-btn' + disabled + '" data-idx="' + i + '" type="button">' +
            sku.label +
            (sku.stock === 0 ? '<span class="sku-sold-out">售罄</span>' : '') +
            '</button>';
        }).join(''),
      '</div>',
      '<div class="sku-stock-tip" id="bzSkuStockTip"></div>'
    ].join('');

    ctaBar.parentNode.insertBefore(wrap, ctaBar);
    applySkuStyles();

    /* ---- 按钮点击 ---- */
    var selector = document.getElementById('bzSkuSelector');
    if (selector) {
      selector.addEventListener('click', function (e) {
        var btn = e.target.closest('.sku-btn');
        if (!btn || btn.classList.contains('sku-btn--disabled')) return;
        var idx = parseInt(btn.dataset.idx, 10);
        if (isNaN(idx)) return;

        // 切换选中
        Array.prototype.forEach.call(selector.querySelectorAll('.sku-btn'), function (b) {
          b.classList.remove('sku-btn--active');
        });
        btn.classList.add('sku-btn--active');
        selectedIdx = idx;

        var sku = data.skus[idx];
        updatePrice(sku.price);
        updateStockTip(sku.stock);
        updateBuyBtn(sku, data);
      });
    }

    /* ---- 若只有 1 个 SKU，自动选中 ---- */
    if (data.skus.length === 1 && data.skus[0].stock > 0) {
      var firstBtn = selector && selector.querySelector('.sku-btn:not(.sku-btn--disabled)');
      if (firstBtn) firstBtn.click();
    } else {
      // 未选中时，锁定购买按钮
      lockBuyBtn();
    }
  }

  /* ---- 更新价格显示 ---- */
  function updatePrice(price) {
    var priceEl = document.querySelector('.detail-price');
    if (!priceEl) return;
    var formatted = '¥' + Number(price).toLocaleString('zh-CN');
    // 保留 .unit span 若有
    var unitEl = priceEl.querySelector('.unit');
    var unitText = unitEl ? unitEl.outerHTML : '';
    priceEl.innerHTML = '<small>¥</small>' + Number(price).toLocaleString('zh-CN') + unitText;
    // 动画
    priceEl.style.transition = 'color .25s';
    priceEl.style.color = '#d4ac6b';
    setTimeout(function () { priceEl.style.color = ''; }, 400);
  }

  /* ---- 更新库存提示 ---- */
  function updateStockTip(stock) {
    var tipEl = document.getElementById('bzSkuStockTip');
    if (!tipEl) return;
    if (stock <= 0) {
      tipEl.textContent = '该规格暂时售罄';
      tipEl.style.color = '#a84d34';
    } else if (stock <= 5) {
      tipEl.textContent = '仅剩 ' + stock + ' 件，请尽快下单';
      tipEl.style.color = '#c97d3a';
    } else {
      tipEl.textContent = '库存充足';
      tipEl.style.color = '#6b9b87';
    }
  }

  /* ---- 更新购买按钮属性（衔接 cart.js） ---- */
  function updateBuyBtn(sku, data) {
    var buyBtn = document.querySelector('.btn-buy, .cta-bar button');
    if (!buyBtn) return;
    buyBtn.setAttribute('data-add-to-cart', data.id || 'product-' + Date.now());
    buyBtn.setAttribute('data-name', (data.name || '') + (sku.label ? ' · ' + sku.label : ''));
    buyBtn.setAttribute('data-price', sku.price || 0);
    buyBtn.setAttribute('data-img', data.img || '');
    buyBtn.setAttribute('data-cat', data.cat || '');
    buyBtn.disabled = false;
    buyBtn.style.opacity = '';
    buyBtn.style.cursor = '';
  }

  /* ---- 未选规格时锁定购买 ---- */
  function lockBuyBtn() {
    var buyBtn = document.querySelector('.btn-buy, .cta-bar button');
    if (!buyBtn) return;
    buyBtn.removeAttribute('data-add-to-cart');
    buyBtn.disabled = false; // 保持可点击但无效果
    buyBtn.addEventListener('click', function (e) {
      if (!buyBtn.hasAttribute('data-add-to-cart')) {
        e.stopImmediatePropagation();
        // 高亮选择器提示
        var sel = document.getElementById('bzSkuSelector');
        if (sel) {
          sel.style.outline = '2px solid #c97d3a';
          setTimeout(function () { sel.style.outline = ''; }, 1200);
        }
        var label = document.querySelector('.sku-label');
        if (label) {
          label.style.color = '#c97d3a';
          setTimeout(function () { label.style.color = ''; }, 1200);
        }
      }
    }, true);
  }

  /* ---- 注入 CSS（仅一次） ---- */
  function applySkuStyles() {
    if (document.getElementById('bzSkuStyles')) return;
    var s = document.createElement('style');
    s.id = 'bzSkuStyles';
    s.textContent = [
      '.sku-wrap{margin-bottom:20px;}',
      '.sku-label{font-size:13px;letter-spacing:2px;color:var(--muted,#999);margin-bottom:10px;font-weight:600;}',
      '.sku-selector{display:flex;flex-wrap:wrap;gap:10px;}',
      '.sku-btn{',
        'background:none;',
        'border:1px solid rgba(185,151,91,.35);',
        'color:var(--primary,#3a2e24);',
        'font-size:13px;letter-spacing:1.5px;',
        'padding:8px 18px;border-radius:4px;',
        'cursor:pointer;transition:all .2s;',
        'position:relative;',
      '}',
      '.sku-btn:hover{border-color:#B9975B;color:#B9975B;}',
      '.sku-btn--active{background:#B9975B;border-color:#B9975B;color:#fff;font-weight:700;}',
      '.sku-btn--disabled{opacity:.4;cursor:not-allowed;text-decoration:line-through;}',
      '.sku-sold-out{',
        'position:absolute;top:-8px;right:-8px;',
        'background:#a84d34;color:#fff;',
        'font-size:10px;padding:2px 5px;border-radius:10px;',
        'letter-spacing:1px;',
      '}',
      '.sku-stock-tip{font-size:12px;letter-spacing:1.5px;margin-top:8px;min-height:18px;}',
    ].join('');
    document.head.appendChild(s);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
