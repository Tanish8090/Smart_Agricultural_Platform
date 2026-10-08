import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_path = 'final sap project/final sap project/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CHAT_SUGGESTED_CHIPS and renderChatSuggestedChips() right before sendQuickPrompt
chips_code = '''const CHAT_SUGGESTED_CHIPS = [
  {
    icon: '🌾',
    enLabel: 'Fertilizer advice',
    hiLabel: 'खाद की सलाह',
    enPrompt: 'What is the recommended fertilizer dosage and application schedule for my crop?',
    hiPrompt: 'गेहूं में खाद (यूरिया, डीएपी) की सही मात्रा और डालने का समय क्या है?'
  },
  {
    icon: '🍂',
    enLabel: 'Yellow leaves issue',
    hiLabel: 'पत्तियों का पीलापन',
    enPrompt: 'Why are leaves turning yellow on my crop and what is the remedy?',
    hiPrompt: 'मेरी फसल में पत्तियां पीली क्यों हो रही हैं और इसका क्या इलाज है?'
  },
  {
    icon: '💧',
    enLabel: 'Irrigation advice',
    hiLabel: 'सिंचाई सलाह',
    enPrompt: 'Should I irrigate my crops today based on current weather?',
    hiPrompt: 'क्या वर्तमान मौसम के अनुसार आज फसल में पानी देना चाहिए?'
  },
  {
    icon: '🌦',
    enLabel: 'Weather forecast',
    hiLabel: 'मौसम का पूर्वानुमान',
    enPrompt: 'What is the weather forecast for my location today?',
    hiPrompt: 'आज और कल मेरे क्षेत्र का मौसम कैसा रहेगा?'
  },
  {
    icon: '🐛',
    enLabel: 'Pest control',
    hiLabel: 'कीट नियंत्रण',
    enPrompt: 'How can I prevent and control pests in my crop?',
    hiPrompt: 'फसल में कीड़े लग गए हैं, रोकथाम के उपाय बताएं'
  },
  {
    icon: '💰',
    enLabel: 'Mandi prices',
    hiLabel: 'मंडी भाव',
    enPrompt: 'What are the current mandi market prices for my crop?',
    hiPrompt: 'मेरी फसल का आज का ताजा मंडी भाव बताओ'
  },
  {
    icon: '🏛',
    enLabel: 'Govt schemes',
    hiLabel: 'सरकारी योजनाएं',
    enPrompt: 'What government agriculture schemes can I apply for?',
    hiPrompt: 'किसानों के लिए प्रमुख सरकारी योजनाएं बताइए'
  }
];

function renderChatSuggestedChips() {
  const container = document.getElementById('chatSuggestedChipsContainer');
  if (!container) return;
  const isHi = (state.lang === 'hi' || (typeof currentLanguage !== 'undefined' && currentLanguage === 'hi'));

  container.innerHTML = CHAT_SUGGESTED_CHIPS.map(c => {
    const label = isHi ? c.hiLabel : c.enLabel;
    const prompt = isHi ? c.hiPrompt : c.enPrompt;
    return `
      <button type="button" onclick="sendQuickPrompt('${escapeAttribute(prompt)}')" class="chat-chip whitespace-nowrap bg-white dark:bg-slate-700 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 text-slate-700 dark:text-slate-200 text-xs font-semibold px-3 py-1.5 rounded-full border border-slate-300 dark:border-slate-600 transition shadow-sm flex items-center space-x-1.5">
        <span>${c.icon}</span><span>${escapeHTML(label)}</span>
      </button>
    `;
  }).join('');
}

'''

if 'CHAT_SUGGESTED_CHIPS' not in code:
    code = code.replace('function sendQuickPrompt(promptText) {', chips_code + 'function sendQuickPrompt(promptText) {')
    print("Added CHAT_SUGGESTED_CHIPS and renderChatSuggestedChips")

# 2. Update handleChatSubmit to pass language and localized messages
old_submit_block = """  try {
    const response = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage,
        context: chatState.farmerContext,
        history: historyPayload,
        image: attachedImg
      })
    });"""

new_submit_block = """  try {
    const currentLang = state.lang || 'en';
    const cropVal = (chatState.farmerContext && chatState.farmerContext.crop) || state.crop || 'Wheat';
    const locVal = (chatState.farmerContext && chatState.farmerContext.location) || (state.location && state.location.city) || 'Kanpur';
    const soilVal = (chatState.farmerContext && chatState.farmerContext.soilType) || 'Alluvial / Loam';

    const chatPayload = {
      message: userMessage,
      language: currentLang,
      crop: cropVal,
      location: locVal,
      soil: soilVal,
      context: Object.assign({}, chatState.farmerContext, {
        language: currentLang,
        crop: cropVal,
        location: locVal,
        soil: soilVal
      }),
      history: historyPayload,
      image: attachedImg
    };

    const response = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(chatPayload)
    });"""

if old_submit_block in code:
    code = code.replace(old_submit_block, new_submit_block)
    print("Updated handleChatSubmit payload")
else:
    print("[WARN] old_submit_block not matched in app.js")

# 3. Update setChatGenerating to update #chatTypingText dynamically
old_set_gen = """function setChatGenerating(isGenerating) {
  chatState.isGenerating = isGenerating;
  const indicator = document.getElementById('chatTypingIndicator');
  const sendBtn = document.getElementById('chatSendBtn');

  if (indicator) {
    if (isGenerating) indicator.classList.remove('hidden');
    else indicator.classList.add('hidden');
  }

  if (sendBtn) {
    sendBtn.disabled = isGenerating;
  }
}"""

new_set_gen = """function setChatGenerating(isGenerating) {
  chatState.isGenerating = isGenerating;
  const indicator = document.getElementById('chatTypingIndicator');
  const typingText = document.getElementById('chatTypingText');
  const sendBtn = document.getElementById('chatSendBtn');
  const isHi = (state.lang === 'hi' || (typeof currentLanguage !== 'undefined' && currentLanguage === 'hi'));

  if (typingText) {
    typingText.textContent = isHi ? 'उत्तर तैयार किया जा रहा है...' : 'Generating response...';
  }

  if (indicator) {
    if (isGenerating) indicator.classList.remove('hidden');
    else indicator.classList.add('hidden');
  }

  if (sendBtn) {
    sendBtn.disabled = isGenerating;
  }
}"""

if old_set_gen in code:
    code = code.replace(old_set_gen, new_set_gen)
    print("Updated setChatGenerating")
else:
    print("[WARN] old_set_gen not matched in app.js")

# 4. Update initChatState to call renderChatSuggestedChips()
old_init_chat = """function initChatState() {
  syncFarmerContext();
  initVoiceRecognition();
  updateChatVoiceIcon();
}"""

new_init_chat = """function initChatState() {
  syncFarmerContext();
  initVoiceRecognition();
  updateChatVoiceIcon();
  if (typeof renderChatSuggestedChips === 'function') {
    renderChatSuggestedChips();
  }
}"""

if old_init_chat in code:
    code = code.replace(old_init_chat, new_init_chat)
    print("Updated initChatState")
else:
    print("[WARN] old_init_chat not matched in app.js")

# 5. In updateLanguageUI, call renderChatSuggestedChips() and set placeholder
old_update_lang = """function updateLanguageUI() {
  if (typeof applyTranslations === 'function') {
    applyTranslations();
  } else {
    const isHi = state.lang === 'hi';
    const langBtn = document.getElementById('langBtnText');
    if (langBtn) langBtn.textContent = isHi ? 'English' : 'हिंदी';
    document.querySelectorAll('[data-lang-en]').forEach(el => {
      const text = isHi ? el.getAttribute('data-lang-hi') : el.getAttribute('data-lang-en');
      if (text) el.textContent = text;
    });
  }
  updateLocationHeroUI();
}"""

new_update_lang = """function updateLanguageUI() {
  if (typeof applyTranslations === 'function') {
    applyTranslations();
  } else {
    const isHi = state.lang === 'hi';
    const langBtn = document.getElementById('langBtnText');
    if (langBtn) langBtn.textContent = isHi ? 'English' : 'हिंदी';
    document.querySelectorAll('[data-lang-en]').forEach(el => {
      const text = isHi ? el.getAttribute('data-lang-hi') : el.getAttribute('data-lang-en');
      if (text) el.textContent = text;
    });
  }
  updateLocationHeroUI();

  const isHi = (state.lang === 'hi' || (typeof currentLanguage !== 'undefined' && currentLanguage === 'hi'));
  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.placeholder = isHi
      ? 'फसल, खाद, रोग, मौसम या मंडी भाव के बारे में कुछ भी पूछें...'
      : 'Ask anything about crops, diseases, fertilizers, weather & mandis...';
  }

  if (typeof renderChatSuggestedChips === 'function') {
    renderChatSuggestedChips();
  }
}"""

if old_update_lang in code:
    code = code.replace(old_update_lang, new_update_lang)
    print("Updated updateLanguageUI")
else:
    print("[WARN] old_update_lang not matched in app.js")

# Write out to all app.js paths
paths = [
    'final sap project/final sap project/app.js',
    'final sap project/app.js',
    'final sap project/final sap project/final sap project/app.js'
]
for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Saved {p}")

print("Frontend app.js update complete!")
