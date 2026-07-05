/* 百珍坊 · 购物车模块 cart.js
   Task B1: 购物车侧滑抽屉
   依赖：shared-pages.css 中的 .cart-drawer 样式
   在所有页面 </body> 前引入即可自动初始化
*/
(function () {
  'use strict';
  var STORAGE_KEY = 'baizhenfang-cart';

  /* ---- 数据层 ---- */
  var CartStore = {
    load: function () {
      try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { items: [] }; }
      catch (e) { return { items: [] }; }
    },
    save: function (cart) {
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(cart)); } catch (e) {}
      document.dispatchEvent(new CustomEvent('cart:updated', { detail: cart }));
    },
    get: function () { return CartStore.load(); },
    add: function (item) {
      var cart = CartStore.load();
      var existing = cart.items.find(function (i) { return i.id === item.id; });
      if (existing) { existing.qty += 1; }
      else { cart.items.push({ id: item.id, name: item.name, price: item.price, qty: 1, img: item.img || '', cat: item.cat || '' }); }
      CartStore.save(cart);
      return cart;
    },
    remove: function (id) {
      var cart = CartStore.load();
      cart.items = cart.items.filter(function (i) { return i.id !== id; });
      CartStore.save(cart);
      return cart;
    },
    updateQty: function (id, delta) {
      var cart = CartStore.load();
      var item = cart.items.find(function (i) { return i.id === id; });
      if (item) {
        item.qty = Math.max(1, (item.qty || 1) + delta);
        CartStore.save(cart);
      }
      return cart;
    },
    getTotal: function () {
      var cart = CartStore.load();
      return cart.items.reduce(function (sum, i) { return sum + (i.price || 0) * (i.qty || 1); }, 0);
    },
    getCount: function () {
      var cart = CartStore.load();
      return cart.items.reduce(function (sum, i) { return sum + (i.qty || 1); }, 0);
    },
    clear: function () { CartStore.save({ items: [] }); }
  };

  /* ---- UI 层 ---- */
  function formatMoney(n) { return '\xA5' + Number(n || 0).toLocaleString('zh-CN'); }

  function buildDrawer() {
    var el = document.createElement('div');
    el.id = 'cartDrawer';
    el.className = 'cart-drawer';
    el.setAttribute('aria-hidden', 'true');
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', '购物车');
    el.innerHTML = [
      '<div class="cart-overlay" id="cartOverlay"></div>',
      '<div class="cart-panel" id="cartPanel" tabindex="-1">',
        '<div class="cart-head">',
          '<h3>购物车</h3>',
          '<div class="cart-head-right">',
            '<span class="cart-badge-head" id="cartBadgeHead">0</span>',
            '<button class="cart-close" id="cartClose" aria-label="关闭购物车">&times;</button>',
          '</div>',
        '</div>',
        '<div class="cart-body" id="cartBody"></div>',
        '<div class="cart-foot" id="cartFoot">',
          '<div class="cart-total-row">',
            '<span class="cart-total-label">合计</span>',
            '<span class="cart-total-price" id="cartTotalPrice">¥0</span>',
          '</div>',
          '<a href="member-center.html#orders" class="cart-checkout" id="cartCheckout">去结算</a>',
        '</div>',
      '</div>'
    ].join('');
    document.body.appendChild(el);
  }

  function renderCart() {
    var cart = CartStore.load();
    var body = document.getElementById('cartBody');
    var badge = document.getElementById('cartBadgeHead');
    var total = document.getElementById('cartTotalPrice');
    var foot = document.getElementById('cartFoot');
    if (!body) return;
    var count = CartStore.getCount();
    if (badge) badge.textContent = count;
    if (total) total.textContent = formatMoney(CartStore.getTotal());
    if (foot) foot.style.display = count > 0 ? '' : 'none';
    updateNavBadge(count);

    if (!cart.items || cart.items.length === 0) {
      body.innerHTML = '<div class="cart-empty"><div class="cart-empty-icon">&#128717;</div><p>购物车暂无商品</p></div>';
      return;
    }
    body.innerHTML = cart.items.map(function (item) {
      return [
        '<div class="cart-item" data-id="' + item.id + '">',
          item.img ? '<img src="' + item.img + '" alt="' + item.name + '">' : '<div style="width:72px;height:72px;background:rgba(185,151,91,.1);border-radius:3px;flex-shrink:0;"></div>',
          '<div class="cart-item-info">',
            '<div class="cart-item-name">' + item.name + '</div>',
            '<div class="cart-item-price">' + formatMoney(item.price) + '</div>',
            '<div class="cart-item-qty">',
              '<button class="cart-qty-btn" data-id="' + item.id + '" data-delta="-1" aria-label="减少数量">&#8722;</button>',
              '<span class="cart-qty-num">' + (item.qty || 1) + '</span>',
              '<button class="cart-qty-btn" data-id="' + item.id + '" data-delta="1" aria-label="增加数量">&#43;</button>',
            '</div>',
          '</div>',
          '<button class="cart-remove" data-remove="' + item.id + '" aria-label="移除商品">&times;</button>',
        '</div>'
      ].join('');
    }).join('');

    body.querySelectorAll('.cart-qty-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        CartStore.updateQty(btn.dataset.id, parseInt(btn.dataset.delta, 10));
        renderCart();
      });
    });
    body.querySelectorAll('.cart-remove').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        CartStore.remove(btn.dataset.remove);
        renderCart();
      });
    });
  }

  function openCart() {
    var drawer = document.getElementById('cartDrawer');
    if (!drawer) return;
    renderCart();
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var panel = document.getElementById('cartPanel');
    if (panel) panel.focus();
  }

  function closeCart() {
    var drawer = document.getElementById('cartDrawer');
    if (!drawer) return;
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function updateNavBadge(count) {
    var badges = document.querySelectorAll('.nav-cart-count');
    badges.forEach(function (b) {
      b.textContent = count;
      b.classList.toggle('visible', count > 0);
    });
  }

  /* ---- 初始化 ---- */
  function init() {
    buildDrawer();
    renderCart();

    // 关闭事件
    document.getElementById('cartClose').addEventListener('click', closeCart);
    document.getElementById('cartOverlay').addEventListener('click', closeCart);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeCart();
    });

    // 购物车图标点击
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.nav-cart-btn');
      if (btn) openCart();
    });

    // 加入购物车按钮
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-add-to-cart]');
      if (!btn) return;
      var item = {
        id:    btn.dataset.addToCart || btn.dataset.id || 'item-' + Date.now(),
        name:  btn.dataset.name  || btn.closest('[data-product-name]')?.dataset.productName || '百珍坊商品',
        price: parseFloat(btn.dataset.price) || 0,
        img:   btn.dataset.img   || '',
        cat:   btn.dataset.cat   || ''
      };
      CartStore.add(item);
      openCart();
    });

    // 监听购物车更新
    document.addEventListener('cart:updated', function () { renderCart(); });

    // 导航栏磨砂玻璃效果 (Task D1)
    var topbar = document.querySelector('.topbar');
    if (topbar) {
      var scrollThreshold = 80;
      function onScroll() {
        topbar.classList.toggle('nav--scrolled', window.scrollY > scrollThreshold);
      }
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露全局接口
  window.CartStore = CartStore;
  window.openCart = openCart;
  window.closeCart = closeCart;
})();
