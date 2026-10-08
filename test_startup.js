
const fs = require('fs');
const vm = require('vm');

// Mock browser environment
const localStorageData = {};
const mockLocalStorage = {
  getItem: (k) => localStorageData[k] || null,
  setItem: (k, v) => { localStorageData[k] = String(v); },
  removeItem: (k) => { delete localStorageData[k]; }
};

const domListeners = {};
const elements = {};

function createElement(tag, id = '', className = '') {
  return {
    tagName: tag.toUpperCase(),
    id: id,
    className: className,
    classList: {
      _classes: new Set(className.split(' ').filter(Boolean)),
      add: function(...c) { c.forEach(x => this._classes.add(x)); },
      remove: function(...c) { c.forEach(x => this._classes.delete(x)); },
      contains: function(c) { return this._classes.has(c); },
      toggle: function(c) { if (this.contains(c)) this.remove(c); else this.add(c); }
    },
    style: {},
    children: [],
    attributes: {},
    getAttribute: function(k) { return this.attributes[k] || null; },
    setAttribute: function(k, v) { this.attributes[k] = String(v); },
    addEventListener: () => {},
    appendChild: function(c) { this.children.push(c); },
    querySelectorAll: () => [],
    querySelector: () => null
  };
}

const mockDoc = {
  documentElement: createElement('html', '', 'light'),
  body: createElement('body', '', 'bg-slate-50'),
  addEventListener: (event, cb) => {
    if (!domListeners[event]) domListeners[event] = [];
    domListeners[event].push(cb);
  },
  getElementById: (id) => elements[id] || (elements[id] = createElement('div', id)),
  querySelectorAll: (sel) => {
    if (sel === '.tab-view') return [
      mockDoc.getElementById('view-dashboard'),
      mockDoc.getElementById('view-weather'),
      mockDoc.getElementById('view-disease'),
      mockDoc.getElementById('view-fertilizer'),
      mockDoc.getElementById('view-market'),
      mockDoc.getElementById('view-bot')
    ];
    if (sel === '.tab-btn') return [];
    if (sel === '.android-nav-item') return [];
    return [];
  },
  querySelector: () => null
};

const ctx = {
  window: {
    localStorage: mockLocalStorage,
    addEventListener: () => {},
    scrollTo: () => {},
    Capacitor: {
      isNativePlatform: () => true,
      getPlatform: () => 'android',
      Plugins: { App: { addListener: () => {} } }
    }
  },
  document: mockDoc,
  localStorage: mockLocalStorage,
  console: console,
  setTimeout: setTimeout,
  clearTimeout: clearTimeout,
  setInterval: setInterval,
  clearInterval: clearInterval,
  fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }),
  navigator: { onLine: true, userAgent: 'Android' }
};
ctx.window.document = mockDoc;
vm.createContext(ctx);

const files = [
  'www/config.js',
  'www/crops.js',
  'www/translations.js',
  'www/disease_knowledge.js',
  'www/kisan_bot_local.js',
  'www/location_data.js',
  'www/fertilizer_engine.js',
  'www/mandi_data.js',
  'www/app.js'
];

try {
  for (const f of files) {
    const code = fs.readFileSync(f, 'utf8');
    vm.runInContext(code, ctx);
    console.log('Loaded:', f);
  }

  console.log('Triggering DOMContentLoaded...');
  if (domListeners['DOMContentLoaded']) {
    for (const cb of domListeners['DOMContentLoaded']) {
      cb();
    }
  }
  console.log('SUCCESS! DOMContentLoaded executed without error.');
  console.log('Active tab in state:', ctx.state.activeTab);
  console.log('body data-active-tab:', mockDoc.body.getAttribute('data-active-tab'));
  console.log('body classes:', Array.from(mockDoc.body.classList._classes));
  console.log('view-dashboard style.display:', mockDoc.getElementById('view-dashboard').style.display);
  console.log('view-dashboard classList:', Array.from(mockDoc.getElementById('view-dashboard').classList._classes));
} catch(e) {
  console.error('CRASH ERROR:', e);
}
