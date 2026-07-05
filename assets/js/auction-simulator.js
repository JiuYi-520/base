(function (window, document) {
  'use strict';

  var MAX_HISTORY_LENGTH = 12;
  var catalog = window.BaizhenfangCatalog || { auctionStorageKey: 'baizhenfang-phase4-auction-v1', getAuctionProducts: function () { return []; } };
  var renderer = window.BaizhenfangRenderer || { formatMoney: function (value) { return '¥' + Number(value || 0).toLocaleString('zh-CN'); } };
  var auctionProducts = catalog.getAuctionProducts();
  var state = { activeId: auctionProducts[0] ? auctionProducts[0].id : '', lots: {} };
  var countdownTimer = 0;

  function safeNow() {
    return Date.now();
  }

  function getDefaultEndAt(product) {
    var minutes = Number(product.endOffsetMinutes || 0);
    return safeNow() + minutes * 60 * 1000;
  }

  function cloneHistory(history) {
    return (history || []).map(function (item) {
      return { bidder: item.bidder || '匿名买家', amount: Number(item.amount || 0), time: item.time || '刚刚' };
    }).slice(0, MAX_HISTORY_LENGTH);
  }

  function normalizeLot(product, savedLot) {
    var safeSavedLot = savedLot || {};
    return {
      currentPrice: Number(safeSavedLot.currentPrice || product.currentPrice || product.startPrice || 0),
      endAt: Number(safeSavedLot.endAt || getDefaultEndAt(product)),
      history: cloneHistory(safeSavedLot.history && safeSavedLot.history.length ? safeSavedLot.history : product.initialHistory)
    };
  }

  function loadState() {
    try {
      var rawState = window.localStorage.getItem(catalog.auctionStorageKey);
      if (rawState) {
        var parsedState = JSON.parse(rawState);
        if (parsedState && parsedState.lots) {
          state = { activeId: parsedState.activeId || state.activeId, lots: parsedState.lots || {} };
        }
      }
    } catch (error) {
      state = { activeId: auctionProducts[0] ? auctionProducts[0].id : '', lots: {} };
    }

    auctionProducts.forEach(function (product) {
      state.lots[product.id] = normalizeLot(product, state.lots[product.id]);
    });
    if (!auctionProducts.some(function (product) { return product.id === state.activeId; })) {
      state.activeId = auctionProducts[0] ? auctionProducts[0].id : '';
    }
    saveState();
  }

  function saveState() {
    try {
      window.localStorage.setItem(catalog.auctionStorageKey, JSON.stringify(state));
    } catch (error) {
      state.memoryOnly = true;
    }
  }

  function getProductById(productId) {
    return auctionProducts.find(function (product) { return product.id === productId; }) || auctionProducts[0] || null;
  }

  function getActiveLot() {
    var product = getProductById(state.activeId);
    if (!product) {
      return null;
    }
    var lotState = normalizeLot(product, state.lots[product.id]);
    state.lots[product.id] = lotState;
    return { product: product, lotState: lotState };
  }

  function isEnded(product, lotState) {
    return product.status === '已结束' || lotState.endAt <= safeNow();
  }

  function setText(selector, value) {
    var node = document.querySelector(selector);
    if (node) {
      node.textContent = value;
    }
  }

  function renderCountdown(lotState) {
    var remaining = Math.max(0, lotState.endAt - safeNow());
    var day = Math.floor(remaining / 86400000);
    var hour = Math.floor((remaining % 86400000) / 3600000);
    var minute = Math.floor((remaining % 3600000) / 60000);
    var second = Math.floor((remaining % 60000) / 1000);
    setText('[data-time-day]', String(day).padStart(2, '0'));
    setText('[data-time-hour]', String(hour).padStart(2, '0'));
    setText('[data-time-minute]', String(minute).padStart(2, '0'));
    setText('[data-time-second]', String(second).padStart(2, '0'));
  }

  function renderLotList() {
    var lotList = document.querySelector('[data-lot-list]');
    if (!lotList) {
      return;
    }
    lotList.innerHTML = auctionProducts.map(function (product) {
      var lotState = state.lots[product.id] || normalizeLot(product, null);
      var activeClass = product.id === state.activeId ? ' active' : '';
      return [
        '<button class="lot-card' + activeClass + '" type="button" data-lot-id="' + product.id + '">',
        '<img src="' + product.image + '" alt="' + product.name + '">',
        '<span><small>' + (product.lotNo || 'LOT') + ' · ' + product.status + '</small>',
        '<h3>' + product.name + '</h3>',
        '<div class="amount">' + renderer.formatMoney(lotState.currentPrice) + '</div></span>',
        '</button>'
      ].join('');
    }).join('');

    Array.prototype.slice.call(lotList.querySelectorAll('[data-lot-id]')).forEach(function (button) {
      button.addEventListener('click', function () {
        state.activeId = button.getAttribute('data-lot-id') || state.activeId;
        saveState();
        renderAuction();
      });
    });
  }

  function renderBidHistory(lotState) {
    var historyNode = document.querySelector('[data-bid-history]');
    if (!historyNode) {
      return;
    }
    if (!lotState.history.length) {
      historyNode.innerHTML = '<div class="bid-row"><span>暂无出价记录</span><strong>--</strong></div>';
      return;
    }
    historyNode.innerHTML = lotState.history.slice(0, MAX_HISTORY_LENGTH).map(function (item) {
      return '<div class="bid-row"><span>' + item.bidder + ' · ' + item.time + '</span><strong>' + renderer.formatMoney(item.amount) + '</strong></div>';
    }).join('');
  }

  function renderAuction() {
    var activeLot = getActiveLot();
    if (!activeLot) {
      return;
    }
    var product = activeLot.product;
    var lotState = activeLot.lotState;
    var minimumBid = lotState.currentPrice + Number(product.bidStep || 0);
    var ended = isEnded(product, lotState);
    var imageNode = document.querySelector('[data-auction-image]');
    var inputNode = document.querySelector('[data-bid-input]');
    var submitNode = document.querySelector('[data-bid-submit]');
    var statusText = ended ? '已结束' : product.status;

    if (imageNode) {
      imageNode.src = product.image;
      imageNode.alt = product.name;
    }
    setText('[data-auction-badge]', product.lotNo || 'LOT');
    setText('[data-auction-category]', product.category + ' · ' + product.material);
    setText('[data-auction-status]', statusText);
    setText('[data-auction-title]', product.name);
    setText('[data-auction-desc]', product.sellingPoint + ' 来源：' + product.origin + '；规格：' + product.size + '。');
    setText('[data-current-bid]', renderer.formatMoney(lotState.currentPrice));
    setText('[data-minimum-bid]', renderer.formatMoney(minimumBid));
    setText('[data-bid-step]', renderer.formatMoney(product.bidStep || 0));

    if (inputNode) {
      inputNode.min = String(minimumBid);
      inputNode.placeholder = ended ? '拍品已结束' : '最低 ' + renderer.formatMoney(minimumBid);
      inputNode.disabled = ended;
    }
    if (submitNode) {
      submitNode.disabled = ended;
      submitNode.textContent = ended ? '已结束' : '立即出价';
    }
    renderCountdown(lotState);
    renderLotList();
    renderBidHistory(lotState);
    saveState();
  }

  function bindBidForm() {
    var formNode = document.querySelector('[data-bid-form]');
    if (!formNode) {
      return;
    }
    formNode.addEventListener('submit', function (event) {
      event.preventDefault();
      var activeLot = getActiveLot();
      var inputNode = document.querySelector('[data-bid-input]');
      var helpNode = document.querySelector('[data-bid-help]');
      if (!activeLot || !inputNode || !helpNode) {
        return;
      }
      var product = activeLot.product;
      var lotState = activeLot.lotState;
      var bidAmount = Number(inputNode.value);
      var minimumBid = lotState.currentPrice + Number(product.bidStep || 0);
      helpNode.className = 'bid-help';

      if (isEnded(product, lotState)) {
        helpNode.textContent = '这件拍品已结束，不能继续出价。';
        helpNode.classList.add('error');
        renderAuction();
        return;
      }
      if (!Number.isFinite(bidAmount) || bidAmount <= 0) {
        helpNode.textContent = '请输入有效的人民币出价金额。';
        helpNode.classList.add('error');
        return;
      }
      if (bidAmount < minimumBid) {
        helpNode.textContent = '出价不得低于当前价加最小加价幅度：' + renderer.formatMoney(minimumBid) + '。';
        helpNode.classList.add('error');
        return;
      }

      lotState.currentPrice = Math.round(bidAmount);
      lotState.history = [{ bidder: '本机买家', amount: lotState.currentPrice, time: '刚刚' }].concat(lotState.history).slice(0, MAX_HISTORY_LENGTH);
      state.lots[product.id] = lotState;
      inputNode.value = '';
      helpNode.textContent = '出价成功，当前价和记录已保存到本机 localStorage。';
      helpNode.classList.add('success');
      saveState();
      renderAuction();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.querySelector('[data-auction-room]')) {
      return;
    }
    loadState();
    bindBidForm();
    renderAuction();
    countdownTimer = window.setInterval(function () {
      var activeLot = getActiveLot();
      if (activeLot) {
        renderCountdown(activeLot.lotState);
        setText('[data-auction-status]', isEnded(activeLot.product, activeLot.lotState) ? '已结束' : activeLot.product.status);
      }
    }, 1000);
  });

  window.BaizhenfangAuction = {
    renderAuction: renderAuction,
    storageKey: catalog.auctionStorageKey,
    stop: function () { window.clearInterval(countdownTimer); }
  };
})(window, document);
