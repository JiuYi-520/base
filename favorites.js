/* 百珍坊 · 收藏功能 favorites.js
   Task B4: 心形按钮切换收藏 + member-center.html #mc-fav 动态列表
   在 detail-*.html 和 member-center.html </body> 前引入即可自动初始化
*/
(function () {
  'use strict';

  var STORAGE_KEY = 'baizhenfang-favorites';

  /* ---- 数据层 ---- */
  var FavStore = {
    load: function () {
      try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
      catch (e) { return []; }
    },
    save: function (list) {
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); }
      catch (e) {}
      document.dispatchEvent(new CustomEvent('favorites:updated', { detail: list }));
    },
    has: function (id) {
      return FavStore.load().some(function (f) { return f.id === id; });
    },
    add: function (item) {
      var list = FavStore.load();
      if (!list.some(function (f) { return f.id === item.id; })) {
        item.savedAt = new Date().toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }).replace('/', '.');
        list.unshift(item);
        FavStore.save(list);
      }
      return list;
    },
    remove: function (id) {
      var list = FavStore.load().filter(function (f) { return f.id !== id; });
      FavStore.save(list);
      return list;
    },
    toggle: function (item) {
      if (FavStore.has(item.id)) { FavStore.remove(item.id); return false; }
      else { FavStore.add(item); return true; }
    },
    count: function () { return FavStore.load().length; }
  };

  /* ---- detail 页心形按钮 ---- */
  function initDetailFav() {
    var btn = document.querySelector('.btn-fav, [data-fav-btn]');
    if (!btn) return;

    // 从页面读取商品信息
    var skuDataEl = document.getElementById('skuData');
    var skuData = null;
    try { if (skuDataEl) skuData = JSON.parse(skuDataEl.textContent); } catch (e) {}

    var item = {
      id:   (skuData && skuData.id) || window.location.pathname.replace(/.*\//, '').replace('.html', ''),
      name: (skuData && skuData.name) || document.querySelector('.detail-header h1, h1')?.textContent.trim() || '百珍坊商品',
      price: (skuData && skuData.skus && skuData.skus[0] && skuData.skus[0].price) || 0,
      img:  (skuData && skuData.img) || (document.querySelector('.gallery-main') ? document.querySelector('.gallery-main').style.backgroundImage.replace(/url\(['"]?([^'"]+)['"]?\)/, '$1') : ''),
      cat:  (skuData && skuData.cat) || '',
      href: window.location.pathname.replace(/.*\//, '')
    };

    // 同步初始状态
    var isFav = FavStore.has(item.id);
    setFavBtnState(btn, isFav);

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var nowFav = FavStore.toggle(item);
      setFavBtnState(btn, nowFav);
      showFavToast(nowFav);
    });
  }

  function setFavBtnState(btn, active) {
    btn.classList.toggle('btn-fav--active', active);
    // SVG fill 切换
    var svgPath = btn.querySelector('path');
    if (svgPath) {
      svgPath.setAttribute('fill', active ? 'currentColor' : 'none');
    }
    // 文本切换
    var textNode = btn.childNodes[btn.childNodes.length - 1];
    if (textNode && textNode.nodeType === 3) {
      textNode.textContent = active ? ' 已收藏' : ' 加入收藏';
    }
    btn.title = active ? '取消收藏' : '加入收藏';
  }

  function showFavToast(added) {
    var old = document.getElementById('bzFavToast');
    if (old) old.remove();
    var toast = document.createElement('div');
    toast.id = 'bzFavToast';
    toast.textContent = added ? '♥ 已加入收藏' : '已取消收藏';
    toast.style.cssText = [
      'position:fixed', 'bottom:80px', 'left:50%', 'transform:translateX(-50%)',
      'background:rgba(30,24,18,.92)', 'color:rgba(255,249,237,.9)',
      'padding:10px 22px', 'border-radius:30px', 'font-size:13px',
      'letter-spacing:2px', 'z-index:9999', 'pointer-events:none',
      'border:1px solid rgba(185,151,91,.3)', 'transition:opacity .4s'
    ].join(';');
    document.body.appendChild(toast);
    setTimeout(function () { toast.style.opacity = '0'; }, 1800);
    setTimeout(function () { toast.remove(); }, 2400);
  }

  /* ---- member-center.html #mc-fav 动态渲染 ---- */
  function initMcFav() {
    var pane = document.getElementById('mc-fav');
    if (!pane) return;
    renderMcFav(pane);
    document.addEventListener('favorites:updated', function () { renderMcFav(pane); });

    // 更新导航格收藏数量
    var statFav = document.getElementById('statFav');
    if (statFav) statFav.textContent = FavStore.count();
  }

  function renderMcFav(pane) {
    var list = FavStore.load();
    var ul = pane.querySelector('.mc-fav-list');
    if (!ul) return;

    // 更新"查看全部"数量
    var linkEl = pane.querySelector('.mc-pane-head .mc-link');
    if (linkEl) linkEl.textContent = '共 ' + list.length + ' 件 →';

    var statFav = document.getElementById('statFav');
    if (statFav) statFav.textContent = list.length;

    if (!list.length) {
      ul.innerHTML = '<li style="padding:24px 0;text-align:center;color:var(--smoke);font-size:13px;letter-spacing:2px;">暂无收藏商品</li>';
      return;
    }

    // 最多显示6件
    ul.innerHTML = list.slice(0, 6).map(function (f) {
      return [
        '<li>',
          f.img ? '<img src="' + f.img + '" alt="' + f.name + '" onerror="this.style.display=\'none\'">' : '',
          '<div style="flex:1;min-width:0;">',
            '<h5>' + (f.href ? '<a href="' + f.href + '" style="color:inherit;text-decoration:none;">' + f.name + '</a>' : f.name) + '</h5>',
            '<p>' + (f.cat || '百珍坊') + ' · 收藏于 ' + (f.savedAt || '') + '</p>',
          '</div>',
          f.price ? '<strong>¥ ' + Number(f.price).toLocaleString('zh-CN') + '</strong>' : '',
          '<button data-fav-remove="' + f.id + '" aria-label="取消收藏" style="background:none;border:none;color:rgba(0,0,0,.25);cursor:pointer;font-size:18px;padding:4px 8px;transition:color .2s;" title="取消收藏">×</button>',
        '</li>'
      ].join('');
    }).join('');

    // 删除按钮
    ul.querySelectorAll('[data-fav-remove]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        FavStore.remove(btn.dataset.favRemove);
        renderMcFav(pane);
      });
    });
  }

  /* ---- 初始化 ---- */
  function init() {
    if (document.getElementById('mc-fav')) {
      initMcFav();
    } else {
      initDetailFav();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 暴露全局接口
  window.FavStore = FavStore;
})();
