import zipfile
import os

zip_path = 'final sap project.zip'
target_html_path = 'final sap project/final sap project/index.html'

with zipfile.ZipFile(zip_path, 'r') as z:
    orig_html = z.read('final sap project/index.html').decode('utf-8', errors='replace')

# 1. Insert translations.js script before app.js
if '<script src="translations.js"></script>' not in orig_html:
    orig_html = orig_html.replace(
        '<script src="app.js"></script>',
        '<script src="translations.js"></script>\n  <script src="app.js"></script>'
    )

# 2. Update view-disease banner title: ensure AI Crop Disease Scanner
orig_html = orig_html.replace(
    'data-lang-en="AI Plant Disease Scanner" data-lang-hi="एआई फसल रोग जांच केंद्र">\n            AI Plant Disease Scanner',
    'data-lang-en="AI Crop Disease Scanner" data-lang-hi="एआई फसल रोग जांच केंद्र" data-i18n="aiCropDiseaseScanner">\n            AI Crop Disease Scanner'
)

# 3. Add Target Crop selector in view-disease right below the header banner
crop_selector_html = """
      <!-- Target Crop Selector for Crop-Specific Neural Models -->
      <div class="agri-card p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-500 flex items-center justify-center text-lg">
            <i class="fa-solid fa-seedling"></i>
          </div>
          <div>
            <h4 class="text-sm font-bold text-slate-800 dark:text-slate-100" data-i18n="selectTargetCrop" data-lang-en="Target Crop" data-lang-hi="लक्षित फसल">Target Crop</h4>
            <p class="text-xs text-slate-500 dark:text-slate-400" data-i18n="selectTargetCropSubtitle" data-lang-en="Routes to crop-specific trained neural network" data-lang-hi="फसल-विशिष्ट प्रशिक्षित न्यूरल नेटवर्क को निर्देशित करता है">Routes to crop-specific trained neural network</p>
          </div>
        </div>
        <select id="diseaseCropSelect" onchange="handleCropSelectionChange()" class="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-100 rounded-xl px-4 py-2.5 text-sm font-bold focus:ring-2 focus:ring-emerald-500 focus:outline-none">
          <option value="Auto">✨ Auto Detect (General)</option>
          <option value="Wheat">🌾 Wheat (Yellow Rust / Healthy)</option>
          <option value="Cotton">🌱 Cotton (Bacterial Blight / Healthy)</option>
          <option value="Sugarcane">🎋 Sugarcane (Red Rot / Healthy)</option>
          <option value="Potato">🥔 Potato (Early / Late Blight / Healthy)</option>
          <option value="Rice">🌾 Rice (Blast / Brown Spot / Healthy)</option>
          <option value="Soybean">🌿 Soybean (Rust / Healthy)</option>
          <option value="Tomato">🍅 Tomato (Early / Late Blight)</option>
          <option value="Corn">🌽 Corn (Rust / Leaf Blight)</option>
          <option value="Apple">🍎 Apple (Scab / Healthy)</option>
          <option value="Grape">🍇 Grape (Black Rot / Healthy)</option>
        </select>
      </div>
"""

target_marker = '<!-- Image Input Options (Upload or Camera Capture) -->'
if 'id="diseaseCropSelect"' not in orig_html:
    orig_html = orig_html.replace(target_marker, crop_selector_html + '\n      ' + target_marker)

# 4. In diseaseResultContainer, insert diagNotLeafCard, diagModelUnavailableCard, diagHeatmapSection
diag_extensions = """
          <!-- Out-of-Domain / Not-A-Leaf Alert Card -->
          <div id="diagNotLeafCard" class="hidden bg-rose-500/10 border-2 border-rose-500/40 rounded-2xl p-6 text-center space-y-3">
            <div class="w-14 h-14 mx-auto rounded-2xl bg-rose-500/20 text-rose-500 flex items-center justify-center text-2xl">
              <i class="fa-solid fa-ban"></i>
            </div>
            <h3 class="text-lg font-black text-rose-500 dark:text-rose-400" data-i18n="noPlantLeafDetected" data-lang-en="No Plant Leaf Detected" data-lang-hi="कोई पौधे की पत्ती नहीं पाई गई">No Plant Leaf Detected</h3>
            <p id="diagNotLeafMessage" class="text-xs font-semibold text-slate-600 dark:text-slate-300 max-w-md mx-auto" data-i18n="notLeafMsg">
              The uploaded image does not contain a recognized plant leaf. Please upload a clear photo of a crop leaf.
            </p>
            <div class="pt-2">
              <button onclick="clearSelectedImage()" class="px-5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs shadow transition">
                <i class="fa-solid fa-arrow-rotate-left mr-1.5"></i> <span data-i18n="notLeafTryAgain">Try Again with a Crop Leaf</span>
              </button>
            </div>
          </div>

          <!-- Model Unavailable Alert Card -->
          <div id="diagModelUnavailableCard" class="hidden bg-amber-500/10 border-2 border-amber-500/40 rounded-2xl p-6 text-center space-y-3">
            <div class="w-14 h-14 mx-auto rounded-2xl bg-amber-500/20 text-amber-500 flex items-center justify-center text-2xl">
              <i class="fa-solid fa-triangle-exclamation"></i>
            </div>
            <h3 class="text-lg font-black text-amber-500 dark:text-amber-400" data-i18n="modelUnavailable" data-lang-en="AI model for this crop is currently unavailable." data-lang-hi="इस फसल के लिए AI मॉडल अभी उपलब्ध नहीं है।">AI model for this crop is currently unavailable.</h3>
            <p id="diagModelUnavailableMessage" class="text-xs font-semibold text-slate-600 dark:text-slate-300 max-w-md mx-auto" data-i18n="modelUnavailableMsg">
              Neural vision weights for this crop are currently being trained. Please select Wheat, Cotton, Sugarcane, Potato, Rice, or Soybean.
            </p>
          </div>

          <!-- Real AI Visual Problem Highlighting (Grad-CAM Attention Heatmap) -->
          <div id="diagHeatmapSection" class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
              <div class="flex items-center space-x-2 text-emerald-600 dark:text-emerald-400 font-bold text-sm">
                <i class="fa-solid fa-fire-flame-curved text-lg"></i>
                <h4 data-i18n="gradcamHeatmapTitle" data-lang-en="AI Attention & Disease Region Highlighting (Grad-CAM)" data-lang-hi="एआई विजुअल ध्यान एवं प्रभावित क्षेत्र (Grad-CAM)">AI Attention & Disease Region Highlighting (Grad-CAM)</h4>
              </div>
              <span id="diagAffectedAreaBadge" class="bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 text-xs font-extrabold px-3 py-1 rounded-full">
                Affected Area: 0%
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-1.5 text-center">
                <span class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider" data-i18n="originalUploadedLeaf">Original Uploaded Leaf</span>
                <div class="w-full h-64 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center">
                  <img id="diagOriginalLeafImg" src="" alt="Original Leaf" class="w-full h-full object-contain">
                </div>
              </div>
              <div class="space-y-1.5 text-center">
                <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center justify-center space-x-1">
                  <span data-i18n="gradcamActivationHeatmap">Grad-CAM Activation Heatmap</span>
                  <i class="fa-solid fa-wand-magic-sparkles text-[10px]"></i>
                </span>
                <div class="w-full h-64 rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border-2 border-emerald-500/40 flex items-center justify-center shadow-inner">
                  <img id="diagHeatmapOverlayImg" src="" alt="Grad-CAM Heatmap" class="w-full h-full object-contain">
                </div>
              </div>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400 text-center italic" data-i18n="heatmapCaption">
              Warm colored regions (red/yellow) indicate neural network focus areas with high disease lesion density.
            </p>
          </div>
"""

result_marker = '<!-- Agronomic Treatment Grid -->'
if 'id="diagNotLeafCard"' not in orig_html:
    orig_html = orig_html.replace(result_marker, diag_extensions + '\n          ' + result_marker)

# Ensure diagTreatmentGrid has id
if 'id="diagTreatmentGrid"' not in orig_html:
    orig_html = orig_html.replace(
        '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        '<div id="diagTreatmentGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        1
    )

# 5. Add data-i18n attributes to navigation buttons
nav_replacements = [
    ('id="tab-dashboard"', 'id="tab-dashboard" data-i18n-tab="dashboard"'),
    ('id="tab-weather"', 'id="tab-weather" data-i18n-tab="weather"'),
    ('id="tab-disease"', 'id="tab-disease" data-i18n-tab="diseaseDetection"'),
    ('id="tab-fertilizer"', 'id="tab-fertilizer" data-i18n-tab="fertilizer"'),
    ('id="tab-market"', 'id="tab-market" data-i18n-tab="marketPrices"'),
    ('id="tab-schemes"', 'id="tab-schemes" data-i18n-tab="governmentSchemes"'),
    ('id="tab-bot"', 'id="tab-bot" data-i18n-tab="aiFarmingAssistant"')
]
for old, new in nav_replacements:
    orig_html = orig_html.replace(old, new)

# 6. Global Language Toggle button
orig_html = orig_html.replace(
    '<button onclick="toggleLanguage()" class="px-2.5 py-1.5 rounded-full bg-emerald-100',
    '<button onclick="toggleLanguage()" id="globalLangToggleBtn" class="px-2.5 py-1.5 rounded-full bg-emerald-100'
)

# 7. Write to target files
for p in [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]:
    d = os.path.dirname(p)
    if os.path.exists(d):
        with open(p, 'w', encoding='utf-8') as f:
            f.write(orig_html)
        print(f"Saved: {p} ({len(orig_html)} bytes)")

print("Successfully restored index.html across all locations!")
