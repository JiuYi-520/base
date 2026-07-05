/* 百珍坊 · 商品灯箱 lightbox.js
   Task B2: 点击商品图片全屏灯箱展示
   在 detail-*.html 页面 </body> 前引入即可自动初始化
*/
(function () {
  'use strict';

  var images = [];
  var currentIndex = 0;
  var lbEl = null;
  var touchStartX = 0;

  function buildLightbox() {
    if (document.getElementById('bzLightbox')) return;
    var el = document.createElement('div');
    el.id = 'bzLightbox';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-label', '图片灯箱');
    el.style.cssText = [
      'display:none',
      'position:fixed',
      'inset:0',
      'z-index:9500',
      'background:rgba(0,0,0,.94)',
      'flex-direction:column',
      'align-items:center',
      'justify-content:center',
    ].join(';');
    el.innerHTML = [
      '<button id="lbClose" aria-label="关闭" style="position:absolute;top:18px;right:22px;background:none;border:none;color:rgba(255,249,237,.6);font-size:28px;cursor:pointer;z-index:2;line-height:1;transition:color .2s;">&times;</button>',
      '<button id="lbPrev" aria-label="上一张" style="position:absolute;left:18px;top:50%;transform:translateY(-50%);background:rgba(255,249,237,.08);border:1px solid rgba(255,249,237,.18);color:rgba(255,249,237,.72);font-size:22px;width:44px;height:44px;cursor:pointer;border-radius:2px;z-index:2;transition:all .2s;">&#8249;</button>',
      '<div id="lbImgWrap" style="flex:1;display:flex;align-items:center;justify-content:center;width:100%;padding:60px 80px;">',
        '<img id="lbImg" src="" alt="" style="max-width:90vw;max-height:80vh;object-fit:contain;opacity:0;transition:opacity .25s;display:block;">',
      '</div>',
      '<button id="lbNext" aria-label="下一张" style="position:absolute;right:18px;top:50%;transform:translateY(-50%);background:rgba(255,249,237,.08);border:1px solid rgba(255,249,237,.18);color:rgba(255,249,237,.72);font-size:22px;width:44px;height:44px;cursor:pointer;border-radius:2px;z-index:2;transition:all .2s;">&#8250;</button>',
      '<div id="lbThumbs" style="display:flex;gap:8px;padding:0 24px 20px;flex-wrap:nowrap;overflow-x:auto;max-width:100%;"></div>',
    ].join('');
    document.body.appendChild(el);
    lbEl = el;

    document.getElementById('lbClose').addEventListener('click', close);
    document.getElementById('lbPrev').addEventListener('click', function() { navigate(-1); });
    document.getElementById('lbNext').addEventListener('click', function() { navigate(1); });

    el.addEventListener('click', function(e) {
      if (e.target === el) close();
    });
    document.addEventListener('keydown', onKey);

    // Touch swipe
    el.addEventListener('touchstart', function(e) { touchStartX = e.touches[0].clientX; }, { passive: true });
    el.addEventListener('touchend', function(e) {
      var delta = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 50) navigate(delta > 0 ? -1 : 1);
    });
  }

  function showImg(idx) {
    if (!images.length) return;
    idx = (idx + images.length) % images.length;
    currentIndex = idx;
    var img = document.getElementById('lbImg');
    img.style.opacity = '0';
    img.onload = function() { img.style.opacity = '1'; };
    img.onerror = function() { img.style.opacity = '0.3'; };
    img.src = images[idx].src;
    img.alt = images[idx].alt || '';

    // Update nav visibility
    var prev = document.getElementById('lbPrev');
    var next = document.getElementById('lbNext');
    if (prev) prev.style.display = images.length > 1 ? '' : 'none';
    if (next) next.style.display = images.length > 1 ? '' : 'none';

    // Update thumbs
    var thumbsEl = document.getElementById('lbThumbs');
    if (thumbsEl) {
      thumbsEl.style.display = images.length > 1 ? 'flex' : 'none';
      Array.prototype.forEach.call(thumbsEl.querySelectorAll('[data-lb-idx]'), function(t) {
        var active = parseInt(t.dataset.lbIdx, 10) === idx;
        t.style.borderColor = active ? '#B9975B' : 'transparent';
        t.style.opacity = active ? '1' : '0.55';
      });
    }
  }

  function navigate(dir) { showImg(currentIndex + dir); }

  function open(idx) {
    if (!lbEl) buildLightbox();
    // Rebuild thumbs
    var thumbsEl = document.getElementById('lbThumbs');
    if (thumbsEl) {
      thumbsEl.innerHTML = images.map(function(img, i) {
        return '<img data-lb-idx="' + i + '" src="' + img.src + '" alt="" style="width:52px;height:52px;object-fit:cover;cursor:pointer;border-radius:3px;border:2px solid transparent;flex-shrink:0;transition:all .2s;">';
      }).join('');
      thumbsEl.querySelectorAll('[data-lb-idx]').forEach(function(t) {
        t.addEventListener('click', function() { showImg(parseInt(t.dataset.lbIdx, 10)); });
      });
    }
    lbEl.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    showImg(idx || 0);
    setTimeout(function() { var closeBtn = document.getElementById('lbClose'); if (closeBtn) closeBtn.focus(); }, 50);
  }

  function close() {
    if (lbEl) lbEl.style.display = 'none';
    document.body.style.overflow = '';
  }

  function onKey(e) {
    if (!lbEl || lbEl.style.display === 'none') return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
  }

  function init() {
    buildLightbox();
    // Collect gallery images
    var selectors = ['.product-gallery img', '.au-visual img', '.detail-gallery img', 'figure img', '.product-img img'];
    var seen = new Set ? new Set() : { _s: [], has: function(v){ return this._s.indexOf(v) > -1; }, add: function(v){ this._s.push(v); } };
    images = [];
    selectors.forEach(function(sel) {
      Array.prototype.forEach.call(document.querySelectorAll(sel), function(img) {
        if (!img.src || seen.has(img.src)) return;
        seen.add(img.src);
        images.push({ src: img.src, alt: img.alt || '' });
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', function() {
          var idx = images.findIndex ? images.findIndex(function(i) { return i.src === img.src; }) : images.indexOf(images.filter(function(i){ return i.src === img.src; })[0]);
          open(Math.max(0, idx));
        });
      });
    });

    // Fallback: attach to any img with data-lightbox attribute
    document.querySelectorAll('[data-lightbox]').forEach(function(img) {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', function() {
        images = [{ src: img.src || img.dataset.lightbox, alt: img.alt || '' }];
        open(0);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.BzLightbox = { open: open, close: close };
})();
