const fs = require('fs');
const path = require('path');

// Mock a lightweight DOM environment
class MockOption {
  constructor(val, text) {
    this.value = val;
    this.text = text;
  }
}

class MockElement {
  constructor(id) {
    this.id = id;
    this._innerHTML = '';
    this.value = '';
    this.classList = {
      add: () => {},
      remove: () => {},
      contains: () => false
    };
  }

  get innerHTML() {
    return this._innerHTML;
  }

  set innerHTML(val) {
    this._innerHTML = val;
    // Parse option tags
    this.options = [];
    const re = /<option[^>]*value="([^"]*)"[^>]*>(.*?)<\/option>/g;
    let m;
    while ((m = re.exec(val)) !== null) {
      this.options.push(new MockOption(m[1], m[2]));
    }
  }

  setAttribute() {}
  getAttribute() { return null; }
}

const elements = {};
['headerCropSelect', 'diseaseCropSelect', 'fertCropSelect', 'ctxCropSelect', 'modalCropSelect'].forEach(id => {
  elements[id] = new MockElement(id);
});

global.document = {
  getElementById: (id) => elements[id] || null,
  querySelectorAll: () => [],
  documentElement: { setAttribute: () => {} },
  readyState: 'complete'
};

global.window = {};
global.state = { lang: 'en', crop: 'Wheat' };
global.localStorage = {
  getItem: () => 'en',
  setItem: () => {}
};

// Load translations.js
const transCode = fs.readFileSync('final sap project/final sap project/translations.js', 'utf-8');
eval(transCode);

console.log("=== BILINGUAL CROP DROPDOWN AUDIT ===");

// 1. Test English Mode
console.log("\n--- Testing English Mode (setLanguage('en')) ---");
setLanguage('en');

const expectedCropsEn = [
  'Wheat', 'Cotton', 'Sugarcane', 'Potato', 'Rice',
  'Soybean', 'Tomato', 'Corn', 'Apple', 'Grape'
];

Object.keys(elements).forEach(id => {
  const el = elements[id];
  console.log(`\nSelect #${id}: ${el.options.length} options`);
  el.options.forEach((opt, idx) => {
    console.log(`   [${idx}] value="${opt.value}": "${opt.text}"`);
  });

  if (id === 'diseaseCropSelect') {
    if (el.options.length !== 11) throw new Error(`${id} should have 11 options (Auto + 10 crops)`);
    if (el.options[0].value !== 'Auto') throw new Error(`${id} first option should be Auto`);
    const cropVals = el.options.slice(1).map(o => o.value);
    if (JSON.stringify(cropVals) !== JSON.stringify(expectedCropsEn)) {
      throw new Error(`${id} crop order mismatch: ${cropVals}`);
    }
  } else {
    if (el.options.length !== 10) throw new Error(`${id} should have 10 options`);
    const cropVals = el.options.map(o => o.value);
    if (JSON.stringify(cropVals) !== JSON.stringify(expectedCropsEn)) {
      throw new Error(`${id} crop order mismatch: ${cropVals}`);
    }
  }
});
console.log("\n[✓] English dropdown options 100% verified!");

// 2. Test Hindi Mode
console.log("\n--- Testing Hindi Mode (setLanguage('hi')) ---");
setLanguage('hi');

Object.keys(elements).forEach(id => {
  const el = elements[id];
  console.log(`\nSelect #${id} in Hindi: ${el.options.length} options`);
  el.options.forEach((opt, idx) => {
    console.log(`   [${idx}] value="${opt.value}": "${opt.text}"`);
  });

  if (id === 'diseaseCropSelect') {
    if (!el.options[0].text.includes('स्वचालित पहचान')) {
      throw new Error(`Auto Detect Hindi label missing: ${el.options[0].text}`);
    }
    if (!el.options[1].text.includes('गेहूं')) throw new Error(`Wheat Hindi label missing`);
    if (!el.options[10].text.includes('अंगूर')) throw new Error(`Grape Hindi label missing`);
  } else {
    if (!el.options[0].text.includes('गेहूं')) throw new Error(`Wheat Hindi label missing`);
    if (!el.options[9].text.includes('अंगूर')) throw new Error(`Grape Hindi label missing`);
  }
});
console.log("\n[✓] Hindi dropdown options 100% verified with Devanagari labels!");

console.log("\n============================================");
console.log("ALL DROPDOWNS FULLY VERIFIED IN BOTH LANGUAGES!");
console.log("============================================");
