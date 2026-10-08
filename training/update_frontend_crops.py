import re
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("Starting frontend crop standardization...")

# Standardized options HTML
OPTIONS_10_CROPS = '''              <option value="Wheat" data-lang-en="🌾 Wheat (Yellow Rust / Healthy)" data-lang-hi="🌾 गेहूं (पीला रतुआ / स्वस्थ)">🌾 Wheat (Yellow Rust / Healthy)</option>
              <option value="Cotton" data-lang-en="🌱 Cotton (Bacterial Blight / Healthy)" data-lang-hi="🌱 कपास (जीवाणु झुलसा / स्वस्थ)">🌱 Cotton (Bacterial Blight / Healthy)</option>
              <option value="Sugarcane" data-lang-en="🎋 Sugarcane (Red Rot / Healthy)" data-lang-hi="🎋 गन्ना (लाल सड़न / स्वस्थ)">🎋 Sugarcane (Red Rot / Healthy)</option>
              <option value="Potato" data-lang-en="🥔 Potato (Early Blight / Late Blight / Healthy)" data-lang-hi="🥔 आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)">🥔 Potato (Early Blight / Late Blight / Healthy)</option>
              <option value="Rice" data-lang-en="🌾 Rice (Blast / Brown Spot / Healthy)" data-lang-hi="🌾 धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)">🌾 Rice (Blast / Brown Spot / Healthy)</option>
              <option value="Soybean" data-lang-en="🌿 Soybean (Rust / Healthy)" data-lang-hi="🌿 सोयाबीन (रस्ट / स्वस्थ)">🌿 Soybean (Rust / Healthy)</option>
              <option value="Tomato" data-lang-en="🍅 Tomato (Early Blight / Late Blight / Healthy)" data-lang-hi="🍅 टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)">🍅 Tomato (Early Blight / Late Blight / Healthy)</option>
              <option value="Corn" data-lang-en="🌽 Corn / Maize (Common Rust / Leaf Blight / Healthy)" data-lang-hi="🌽 मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)">🌽 Corn / Maize (Common Rust / Leaf Blight / Healthy)</option>
              <option value="Apple" data-lang-en="🍎 Apple (Scab / Healthy)" data-lang-hi="🍎 सेब (स्कैब / स्वस्थ)">🍎 Apple (Scab / Healthy)</option>
              <option value="Grape" data-lang-en="🍇 Grape (Black Rot / Healthy)" data-lang-hi="🍇 अंगूर (ब्लैक रॉट / स्वस्थ)">🍇 Grape (Black Rot / Healthy)</option>'''

OPTIONS_WITH_AUTO = '''              <option value="Auto" data-lang-en="🔍 Auto Detect (General)" data-lang-hi="🔍 स्वचालित पहचान (सामान्य)">🔍 Auto Detect (General)</option>
''' + OPTIONS_10_CROPS

# 1. Update index.html
html_path = 'final sap project/final sap project/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add crops.js to <head> if not present
if 'crops.js' not in html:
    html = html.replace('<script src="translations.js"></script>', '<script src="crops.js"></script>\n  <script src="translations.js"></script>')
    print("[✓] Added <script src='crops.js'></script> to index.html")

# Replace options for #headerCropSelect
pat_header = r'(<select[^>]*id="headerCropSelect"[^>]*>)[\s\S]*?(<\/select>)'
html = re.sub(pat_header, rf'\1\n{OPTIONS_10_CROPS}\n            \2', html)
print("[✓] Updated #headerCropSelect")

# Replace options for #diseaseCropSelect
pat_disease = r'(<select[^>]*id="diseaseCropSelect"[^>]*>)[\s\S]*?(<\/select>)'
html = re.sub(pat_disease, rf'\1\n{OPTIONS_WITH_AUTO}\n              \2', html)
print("[✓] Updated #diseaseCropSelect")

# Replace options for #fertCropSelect
pat_fert = r'(<select[^>]*id="fertCropSelect"[^>]*>)[\s\S]*?(<\/select>)'
html = re.sub(pat_fert, rf'\1\n{OPTIONS_10_CROPS}\n              \2', html)
print("[✓] Updated #fertCropSelect")

# Replace options for #ctxCropSelect
pat_ctx = r'(<select[^>]*id="ctxCropSelect"[^>]*>)[\s\S]*?(<\/select>)'
html = re.sub(pat_ctx, rf'\1\n{OPTIONS_10_CROPS}\n            \2', html)
print("[✓] Updated #ctxCropSelect")

# Replace options for #modalCropSelect
pat_modal = r'(<select[^>]*id="modalCropSelect"[^>]*>)[\s\S]*?(<\/select>)'
html = re.sub(pat_modal, rf'\1\n{OPTIONS_10_CROPS}\n            \2', html)
print("[✓] Updated #modalCropSelect")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("[✓] Saved index.html")


# 2. Update translations.js
trans_path = 'final sap project/final sap project/translations.js'
with open(trans_path, 'r', encoding='utf-8') as f:
    tjs = f.read()

# Update CROP_TRANSLATIONS
crop_trans_block = '''const CROP_TRANSLATIONS = {
  auto: { en: '🔍 Auto Detect (General)', hi: '🔍 स्वचालित पहचान (सामान्य)' },
  wheat: { en: 'Wheat (Yellow Rust / Healthy)', hi: 'गेहूं (पीला रतुआ / स्वस्थ)' },
  cotton: { en: 'Cotton (Bacterial Blight / Healthy)', hi: 'कपास (जीवाणु झुलसा / स्वस्थ)' },
  sugarcane: { en: 'Sugarcane (Red Rot / Healthy)', hi: 'गन्ना (लाल सड़न / स्वस्थ)' },
  potato: { en: 'Potato (Early Blight / Late Blight / Healthy)', hi: 'आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
  rice: { en: 'Rice (Blast / Brown Spot / Healthy)', hi: 'धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)' },
  soybean: { en: 'Soybean (Rust / Healthy)', hi: 'सोयाबीन (रस्ट / स्वस्थ)' },
  tomato: { en: 'Tomato (Early Blight / Late Blight / Healthy)', hi: 'टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
  corn: { en: 'Corn / Maize (Common Rust / Leaf Blight / Healthy)', hi: 'मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)' },
  apple: { en: 'Apple (Scab / Healthy)', hi: 'सेब (स्कैब / स्वस्थ)' },
  grape: { en: 'Grape (Black Rot / Healthy)', hi: 'अंगूर (ब्लैक रॉट / स्वस्थ)' }
};'''

tjs = re.sub(r'const CROP_TRANSLATIONS = \{[\s\S]*?\};', crop_trans_block, tjs)
print("[✓] Updated CROP_TRANSLATIONS in translations.js")

# Add disease aliases if not present
if "'Rice___Blast':" not in tjs:
    tjs = tjs.replace("'Rice___Leaf_blast':", "'Rice___Blast': {\n    name_en: 'Rice Blast',\n    name_hi: 'धान का ब्लास्ट (झोंका रोग)',\n    crop_en: 'Rice',\n    crop_hi: 'धान',\n    symptoms_en: 'Spindle-shaped elliptical lesions with gray-white centers and reddish-brown margins on leaf blades.',\n    symptoms_hi: 'पत्तियों पर नाव या धुरी के आकार के धब्बे बनते हैं जिनका केंद्र भूरा-सफेद और किनारे लाल-भूरे होते हैं।',\n    cause_en: 'Magnaporthe oryzae (Pyricularia oryzae) fungus under high relative humidity (>90%) and 25-28°C.',\n    cause_hi: 'मैग्नापोर्थे ओराइजी फंगस, जो 90% से अधिक आर्द्रता और 25-28°C में तेजी से फैलता है।',\n    organic_en: 'Foliar spray with Pseudomonas fluorescens @ 5 g/L or fermented cow urine-neem extract.',\n    organic_hi: 'स्यूडोमोनास फ्लोरोसेंस (5 ग्राम/लीटर) या पंचगव्य और नीम अर्क का छिड़काव करें।',\n    chemical_en: 'Spray Tricyclazole 75% WP @ 0.6 g/L (120 g/acre) or Isoprothiolane 40% EC @ 1.5 ml/L.',\n    chemical_hi: 'ट्राइसाइक्लाज़ोल 75% WP (0.6 ग्राम/लीटर) या कासुगामाइसिन का छिड़काव करें।',\n    prevention_en: 'Avoid excessive nitrogen fertilization; use certified treated seeds; practice proper water drainage.',\n    prevention_hi: 'नाइट्रोजन (यूरिया) का अत्यधिक प्रयोग न करें; प्रमाणित बीजों का ही उपयोग करें।',\n    is_healthy: false\n  },\n  'Rice___Leaf_blast':")
    print("[✓] Added Rice___Blast disease key to translations.js")

if "'Corn___Leaf_blight':" not in tjs:
    tjs = tjs.replace("'Corn___Northern_leaf_blight':", "'Corn___Leaf_blight': {\n    name_en: 'Corn Leaf Blight (Northern Blight)',\n    name_hi: 'मक्का का पत्ती झुलसा (लीफ ब्लाइट)',\n    crop_en: 'Corn / Maize',\n    crop_hi: 'मक्का',\n    symptoms_en: 'Long elliptical grayish-green or tan lesions (cigar-shaped) expanding parallel to leaf veins.',\n    symptoms_hi: 'पत्तियों पर सिगार के आकार के लंबे भूरे-हरे या भूरे धब्बे बनते हैं जो पत्तियों को सुखा देते हैं।',\n    cause_en: 'Exserohilum turcicum fungus favored by moderate temperatures (18-27°C) and heavy dew.',\n    cause_hi: 'एक्सरोहिलम टर्सिकम कवक, जो 18-27°C तापमान और पत्तियों पर नमी रहने पर फैलता है।',\n    organic_en: 'Spray Trichoderma viride foliar wash @ 5 g/L; apply neem oil formulation (3 ml/L).',\n    organic_hi: 'ट्राइकोडर्मा विरिडी (5 ग्राम/लीटर) या नीम तेल का छिड़काव करें।',\n    chemical_en: 'Foliar spray with Mancozeb 75% WP (2.5 g/L) or Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).',\n    chemical_hi: 'मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या एजोक्सीस्ट्रोबिन का छिड़काव करें।',\n    prevention_en: 'Destroy infected crop residues after harvest; follow 2-year crop rotation; plant resistant hybrids.',\n    prevention_hi: 'फसल अवशेषों को नष्ट करें, फसल चक्र अपनाएं और रोग प्रतिरोधी संकर बीज लगाएं।',\n    is_healthy: false\n  },\n  'Corn___Northern_leaf_blight':")
    print("[✓] Added Corn___Leaf_blight disease key to translations.js")

# Update applyTranslations() in translations.js to update all 5 selectors dynamically
apply_trans_crops = '''  // 6. Update All Standardized Crop Dropdowns Across Application
  const isHiMode = (typeof currentLanguage !== 'undefined' ? currentLanguage : state.lang) === 'hi';
  
  const standardizedOptions = [
    { val: 'Wheat', en: '🌾 Wheat (Yellow Rust / Healthy)', hi: '🌾 गेहूं (पीला रतुआ / स्वस्थ)' },
    { val: 'Cotton', en: '🌱 Cotton (Bacterial Blight / Healthy)', hi: '🌱 कपास (जीवाणु झुलसा / स्वस्थ)' },
    { val: 'Sugarcane', en: '🎋 Sugarcane (Red Rot / Healthy)', hi: '🎋 गन्ना (लाल सड़न / स्वस्थ)' },
    { val: 'Potato', en: '🥔 Potato (Early Blight / Late Blight / Healthy)', hi: '🥔 आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
    { val: 'Rice', en: '🌾 Rice (Blast / Brown Spot / Healthy)', hi: '🌾 धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)' },
    { val: 'Soybean', en: '🌿 Soybean (Rust / Healthy)', hi: '🌿 सोयाबीन (रस्ट / स्वस्थ)' },
    { val: 'Tomato', en: '🍅 Tomato (Early Blight / Late Blight / Healthy)', hi: '🍅 टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
    { val: 'Corn', en: '🌽 Corn / Maize (Common Rust / Leaf Blight / Healthy)', hi: '🌽 मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)' },
    { val: 'Apple', en: '🍎 Apple (Scab / Healthy)', hi: '🍎 सेब (स्कैब / स्वस्थ)' },
    { val: 'Grape', en: '🍇 Grape (Black Rot / Healthy)', hi: '🍇 अंगूर (ब्लैक रॉट / स्वस्थ)' }
  ];

  const autoOption = { val: 'Auto', en: '🔍 Auto Detect (General)', hi: '🔍 स्वचालित पहचान (सामान्य)' };

  // Helper to re-render a select maintaining its selected value
  function populateSelect(selectId, includeAuto) {
    const el = document.getElementById(selectId);
    if (!el) return;
    const curVal = el.value;
    const list = includeAuto ? [autoOption, ...standardizedOptions] : standardizedOptions;
    el.innerHTML = list.map(opt => `<option value="${opt.val}">${isHiMode ? opt.hi : opt.en}</option>`).join('');
    if (curVal && (list.some(o => o.val === curVal))) {
      el.value = curVal;
    }
  }

  populateSelect('diseaseCropSelect', true);
  populateSelect('headerCropSelect', false);
  populateSelect('fertCropSelect', false);
  populateSelect('ctxCropSelect', false);
  populateSelect('modalCropSelect', false);'''

tjs = re.sub(r'  \/\/ 6\. Update Target Crop Selector Dropdown in Scanner[\s\S]*?if \(currentVal\) cropSelect\.value = currentVal;\s*\}', apply_trans_crops, tjs)
print("[✓] Updated applyTranslations() in translations.js")

with open(trans_path, 'w', encoding='utf-8') as f:
    f.write(tjs)
print("[✓] Saved translations.js")

# Copy crops.js
shutil.copyfile('config/crops.js', 'final sap project/final sap project/crops.js')
shutil.copyfile('config/crops.js', 'final sap project/crops.js')
shutil.copyfile('config/crops.js', 'final sap project/final sap project/final sap project/crops.js')
shutil.copyfile('config/crops.js', 'crops.js')
print("[✓] Copied crops.js to all project directories")

# Sync index.html and translations.js to mirrors
for tgt in ['final sap project', 'final sap project/final sap project/final sap project']:
    shutil.copyfile(html_path, f'{tgt}/index.html')
    shutil.copyfile(trans_path, f'{tgt}/translations.js')
    print(f"[✓] Synced to {tgt}")

shutil.copyfile(trans_path, 'translations.js')
print("[✓] Synced translations.js to root directory")

print("Frontend crop standardization complete!")
