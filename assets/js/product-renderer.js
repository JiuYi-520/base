(function (window, document) {
  'use strict';

  function formatMoney(value) {
    var amount = Number(value);
    if (!Number.isFinite(amount)) {
      amount = 0;
    }
    return new Intl.NumberFormat('zh-CN', {
      style: 'currency',
      currency: 'CNY',
      maximumFractionDigits: 0
    }).format(amount);
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>'"]/g, function (character) {
      var map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' };
      return map[character];
    });
  }

  function getDisplayPrice(product) {
    if (product.status === '竞拍中' || product.status === '已结束') {
      return '当前价 ' + formatMoney(product.currentPrice);
    }
    return formatMoney(product.price);
  }

  function createProductCard(product) {
    var statusClass = product.status === '竞拍中' ? ' is-auction' : '';
    return [
      '<a class="product-card" href="' + escapeHtml(product.detailUrl || 'auction.html') + '" data-product-id="' + escapeHtml(product.id) + '">',
      '<img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '" loading="lazy">',
      '<div class="product-meta">',
      '<small>' + escapeHtml(product.category) + '</small>',
      '<h3>' + escapeHtml(product.name) + '</h3>',
      '<p>' + escapeHtml(product.sellingPoint) + '</p>',
      '<div class="product-spec">' + escapeHtml(product.material) + ' · ' + escapeHtml(product.origin) + '</div>',
      '<div class="product-foot"><span class="price">' + getDisplayPrice(product) + '</span><span class="product-status' + statusClass + '">' + escapeHtml(product.status) + '</span></div>',
      '</div>',
      '</a>'
    ].join('');
  }

  function renderFeaturedProducts() {
    var container = document.querySelector('[data-product-grid]');
    if (!container || !window.BaizhenfangCatalog) {
      return;
    }
    var products = window.BaizhenfangCatalog.getFeaturedProducts(6);
    container.innerHTML = products.map(createProductCard).join('');
  }

  function renderAuctionTeaser() {
    var teaser = document.querySelector('[data-auction-teaser]');
    if (!teaser || !window.BaizhenfangCatalog) {
      return;
    }
    var auctionProducts = window.BaizhenfangCatalog.getAuctionProducts();
    var activeLot = auctionProducts[0];
    if (!activeLot) {
      return;
    }
    var priceNode = teaser.querySelector('[data-auction-current]');
    var titleNode = teaser.querySelector('[data-auction-title]');
    var descNode = teaser.querySelector('[data-auction-desc]');
    var imageNode = teaser.querySelector('[data-auction-image]');
    var statusNode = teaser.querySelector('[data-auction-status]');
    var countNode = teaser.querySelector('[data-auction-count]');

    if (priceNode) priceNode.textContent = formatMoney(activeLot.currentPrice);
    if (titleNode) titleNode.textContent = activeLot.name;
    if (descNode) descNode.textContent = activeLot.sellingPoint + ' 本地模拟竞拍，不连接真实拍卖、支付或订单系统。';
    if (imageNode) {
      imageNode.src = activeLot.image;
      imageNode.alt = activeLot.name;
    }
    if (statusNode) statusNode.textContent = activeLot.status;
    if (countNode) countNode.textContent = String(auctionProducts.length);
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderFeaturedProducts();
    renderAuctionTeaser();
  });

  window.BaizhenfangRenderer = {
    formatMoney: formatMoney,
    renderFeaturedProducts: renderFeaturedProducts,
    renderAuctionTeaser: renderAuctionTeaser
  };
})(window, document);
