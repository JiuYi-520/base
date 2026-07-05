(function (window) {
  'use strict';

  var AUCTION_STORAGE_KEY = 'baizhenfang-phase4-auction-v1';

  var PRODUCTS = [
    {
      id: 'bzf-inkstone-qingshi-001',
      name: '方城黄石砚 · 青石山水纹',
      category: '文房雅器',
      image: 'uploads/stone-qingshi.jpg',
      price: 399,
      startPrice: 1280,
      currentPrice: 1680,
      bidStep: 120,
      material: '方城青石',
      size: '18 × 12 × 3cm',
      origin: '河南南阳方城',
      status: '竞拍中',
      sellingPoint: '石纹如山水铺展，适合书房陈设与收藏级商务雅礼。',
      detailUrl: 'detail-product1.html',
      lotNo: 'LOT 01',
      endOffsetMinutes: 420,
      initialHistory: [
        { bidder: '藏家 1027', amount: 1680, time: '刚刚' },
        { bidder: '方城客商', amount: 1560, time: '12 分钟前' },
        { bidder: '书房买手', amount: 1440, time: '28 分钟前' }
      ]
    },
    {
      id: 'bzf-inkstone-fengyan-002',
      name: '黄石砚 · 峰岩纹藏砚',
      category: '文房雅器',
      image: 'uploads/stone-fengyan.jpg',
      price: 688,
      startPrice: 1880,
      currentPrice: 2260,
      bidStep: 180,
      material: '黄石原石',
      size: '21 × 14 × 3.5cm',
      origin: '方城石材工坊',
      status: '竞拍中',
      sellingPoint: '峰岩肌理清晰，适合文化空间、会所陈列与高端礼赠。',
      detailUrl: 'detail-product2.html',
      lotNo: 'LOT 02',
      endOffsetMinutes: 760,
      initialHistory: [
        { bidder: '南阳藏友', amount: 2260, time: '6 分钟前' },
        { bidder: '雅集会员', amount: 2080, time: '19 分钟前' },
        { bidder: '企业礼赠', amount: 1880, time: '43 分钟前' }
      ]
    },
    {
      id: 'bzf-shihou-craft-003',
      name: '方城石猴 · 案头守福摆件',
      category: '工艺收藏',
      image: 'uploads/product-shihou.jpg',
      price: 299,
      startPrice: 980,
      currentPrice: 1280,
      bidStep: 100,
      material: '地方石料手作',
      size: '高 11cm',
      origin: '方城民间工艺坊',
      status: '竞拍中',
      sellingPoint: '造型朴拙有趣，适合案头陈设、纪念礼与地方文化收藏。',
      detailUrl: 'detail-shihou.html',
      lotNo: 'LOT 03',
      endOffsetMinutes: 1100,
      initialHistory: [
        { bidder: '礼盒采购', amount: 1280, time: '5 分钟前' },
        { bidder: '工艺玩家', amount: 1180, time: '24 分钟前' },
        { bidder: '百珍会员', amount: 1080, time: '51 分钟前' }
      ]
    },
    {
      id: 'bzf-jade-craft-004',
      name: '独山玉件 · 温润平安牌',
      category: '工艺收藏',
      image: 'uploads/product-jade.jpg',
      price: 568,
      startPrice: 1680,
      currentPrice: 1680,
      bidStep: 150,
      material: '独山玉',
      size: '6 × 4cm',
      origin: '南阳玉器供应链',
      status: '已结束',
      sellingPoint: '温润雅致的小件玉牌，可作为商务赠礼和收藏陈列。',
      detailUrl: 'detail-jade.html',
      lotNo: 'LOT 04',
      endOffsetMinutes: -60,
      initialHistory: [
        { bidder: '玉器藏客', amount: 1680, time: '已成交' },
        { bidder: '企业礼赠', amount: 1530, time: '1 小时前' },
        { bidder: '南阳买手', amount: 1380, time: '2 小时前' }
      ]
    },
    {
      id: 'bzf-ink-stick-005',
      name: '手作墨锭 · 松烟雅墨',
      category: '文房雅器',
      image: 'uploads/product-ink.jpg',
      price: 128,
      startPrice: 0,
      currentPrice: 128,
      bidStep: 0,
      material: '松烟墨料',
      size: '单锭约 31g',
      origin: '文房供应链精选',
      status: '现货',
      sellingPoint: '与砚台成套陈列，提升文房礼盒完整度与仪式感。',
      detailUrl: 'detail-ink.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-guokui-food-006',
      name: '方城锅盔 · 传统酥香装',
      category: '方城美食',
      image: 'uploads/product-guokui.jpg',
      price: 39,
      startPrice: 0,
      currentPrice: 39,
      bidStep: 0,
      material: '小麦粉、芝麻、地方配方',
      size: '6 枚礼袋装',
      origin: '河南方城',
      status: '现货',
      sellingPoint: '地方烟火气代表，适合家庭分享与伴手礼组合。',
      detailUrl: 'detail-guokui.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-danshen-health-007',
      name: '方城丹参 · 养生切片礼罐',
      category: '养生滋补',
      image: 'uploads/product-danshen.jpg',
      price: 168,
      startPrice: 0,
      currentPrice: 168,
      bidStep: 0,
      material: '丹参干制切片',
      size: '250g 礼罐',
      origin: '方城周边种植基地',
      status: '现货',
      sellingPoint: '面向长辈与养生场景的稳重型礼品，适合节庆组合。',
      detailUrl: 'detail-danshen.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-silk-gift-008',
      name: '丝织雅礼 · 轻奢披肩',
      category: '礼盒定制',
      image: 'uploads/product-silk.jpg',
      price: 218,
      startPrice: 0,
      currentPrice: 218,
      bidStep: 0,
      material: '桑蚕丝混纺',
      size: '180 × 65cm',
      origin: '中原丝织供应链',
      status: '展示品',
      sellingPoint: '轻量高质感礼品，可进入企业礼赠和女士雅礼组合。',
      detailUrl: 'detail-silk.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-huimian-food-009',
      name: '方城烩面 · 家庭分享装',
      category: '方城美食',
      image: 'uploads/product-huimian.jpg',
      price: 59,
      startPrice: 0,
      currentPrice: 59,
      bidStep: 0,
      material: '小麦面饼、汤料包',
      size: '4 人份',
      origin: '河南方城',
      status: '现货',
      sellingPoint: '经典地方味道，适合家庭餐桌和美食礼盒搭配。',
      detailUrl: 'detail-huimian.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-pear-health-010',
      name: '方城梨膏 · 润养礼盒',
      category: '养生滋补',
      image: 'uploads/product-pear.jpg',
      price: 96,
      startPrice: 0,
      currentPrice: 96,
      bidStep: 0,
      material: '秋梨、蜂蜜、草本配方',
      size: '180g × 2 瓶',
      origin: '方城果品加工合作社',
      status: '现货',
      sellingPoint: '换季常备型礼品，适合长辈关怀和家庭滋补。',
      detailUrl: 'detail-pear.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-brush-studio-011',
      name: '兼毫毛笔 · 文房配套款',
      category: '文房雅器',
      image: 'uploads/product-brush.jpg',
      price: 86,
      startPrice: 0,
      currentPrice: 86,
      bidStep: 0,
      material: '兼毫、竹杆',
      size: '中楷',
      origin: '文房供应链精选',
      status: '展示品',
      sellingPoint: '适合与砚台、墨锭组成入门文房套装，提升客单价。',
      detailUrl: 'detail-brush.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    },
    {
      id: 'bzf-mushroom-health-012',
      name: '山野香菇 · 干货礼袋',
      category: '养生滋补',
      image: 'uploads/product-mushroom.jpg',
      price: 78,
      startPrice: 0,
      currentPrice: 78,
      bidStep: 0,
      material: '干香菇',
      size: '300g 礼袋',
      origin: '伏牛山周边产区',
      status: '现货',
      sellingPoint: '家常实用型干货，适合节庆礼盒与家庭补货。',
      detailUrl: 'detail-mushroom.html',
      lotNo: '',
      endOffsetMinutes: 0,
      initialHistory: []
    }
  ];

  function getAuctionProducts() {
    return PRODUCTS.filter(function (product) {
      return product.lotNo && product.startPrice > 0;
    });
  }

  function getFeaturedProducts(limit) {
    var safeLimit = Number(limit) > 0 ? Number(limit) : 6;
    return PRODUCTS.slice(0, safeLimit);
  }

  window.BaizhenfangCatalog = {
    auctionStorageKey: AUCTION_STORAGE_KEY,
    products: PRODUCTS,
    getAuctionProducts: getAuctionProducts,
    getFeaturedProducts: getFeaturedProducts
  };
})(window);
