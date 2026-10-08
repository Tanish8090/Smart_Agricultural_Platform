import zipfile
import os

zip_path = 'final sap project.zip'

with zipfile.ZipFile(zip_path, 'r') as z:
    orig_js = z.read('final sap project/app.js').decode('utf-8', errors='replace')

# 1. Update initLanguage, toggleLanguage, updateLanguageUI
old_lang_block = """function initLanguage() {
  updateLanguageUI();
}

function toggleLanguage() {
  state.lang = state.lang === 'en' ? 'hi' : 'en';
  localStorage.setItem('sap_lang', state.lang);
  updateLanguageUI();
  if (state.weatherData) {
    renderWeatherUI(state.weatherData);
  }
  syncFarmerContext();
  syncFertilizerContext();
}

function updateLanguageUI() {
  const isHi = state.lang === 'hi';
  const langBtn = document.getElementById('langBtnText');
  if (langBtn) langBtn.textContent = isHi ? 'English' : 'हिंदी';

  // Toggle all elements with data-lang-en and data-lang-hi attributes
  document.querySelectorAll('[data-lang-en]').forEach(el => {
    const text = isHi ? el.getAttribute('data-lang-hi') : el.getAttribute('data-lang-en');
    if (text) {
      el.textContent = text;
    }
  });

  // Update input placeholder for chat & search
  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.placeholder = isHi
      ? 'खेती से जुड़ा कोई भी सवाल पूछें या बोलें... (जैसे: गेहूं में कौन सी खाद डालें)'
      : 'Type or speak in Hindi, English, or Hinglish... (e.g. gehu me konsi khad dalein)';
  }

  const pinInput = document.getElementById('pincodeInput');
  if (pinInput) {
    pinInput.placeholder = isHi
      ? 'पिन कोड या शहर (उदा. 208001, Kanpur)'
      : 'Enter PIN or City (e.g. 208001, Kanpur)';
  }

  const fertSymptomInput = document.getElementById('fertSymptomsInput');
  if (fertSymptomInput) {
    fertSymptomInput.placeholder = isHi
      ? 'लक्षण या सवाल लिखें (उदा. निचली पत्तियां नोक से पीली हो रही हैं, क्या बारिश से पहले यूरिया डालें?)'
      : 'e.g. Lower leaves are turning pale yellow from the tip, should I spray urea or NPK 19:19:19 before tomorrow\\'s rain?';
  }

  updateLocationHeroUI();
}"""

new_lang_block = """function initLanguage() {
  state.lang = localStorage.getItem('sap_language') || localStorage.getItem('sap_lang') || 'en';
  if (typeof currentLanguage !== 'undefined') {
    currentLanguage = state.lang;
  }
  updateLanguageUI();
}

function toggleLanguage() {
  state.lang = state.lang === 'en' ? 'hi' : 'en';
  if (typeof currentLanguage !== 'undefined') {
    currentLanguage = state.lang;
  }
  localStorage.setItem('sap_lang', state.lang);
  localStorage.setItem('sap_language', state.lang);

  if (typeof setLanguage === 'function') {
    setLanguage(state.lang);
  } else {
    updateLanguageUI();
  }

  if (state.weatherData) {
    renderWeatherUI(state.weatherData);
  }
  syncFarmerContext();
  syncFertilizerContext();
  if (window.lastDiagnosisResult) {
    renderDiseaseResults(window.lastDiagnosisResult);
  }
}

function updateLanguageUI() {
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

if old_lang_block in orig_js:
    orig_js = orig_js.replace(old_lang_block, new_lang_block)
    print("Replaced language block successfully!")
else:
    print("[WARN] old_lang_block exact match not found")

# 2. Update loadSampleDiseasePhoto
old_sample_fn = """async function loadSampleDiseasePhoto(filePath, diseaseName) {
  try {
    switchTab('disease');
    showToast(state.lang === 'hi' ? `${diseaseName} का नमूना लोड हो रहा है...` : `Loading sample ${diseaseName}...`, 'info');

    // Fetch the sample image file and convert to base64
    const response = await fetch(filePath);
    if (!response.ok) throw new Error(`Failed to load ${filePath}`);
    const blob = await response.blob();

    const reader = new FileReader();
    reader.onloadend = () => {
      selectedImageBase64 = reader.result;

      const previewCard = document.getElementById('diseasePreviewCard');
      const previewImg = document.getElementById('leafImagePreview');
      const previewName = document.getElementById('previewFileName');
      const scanImgCopy = document.getElementById('scanningImageCopy');

      if (previewCard) previewCard.classList.remove('hidden');
      if (previewImg) previewImg.src = selectedImageBase64;
      if (scanImgCopy) scanImgCopy.src = selectedImageBase64;
      if (previewName) previewName.textContent = diseaseName;

      // Automatically run disease analysis
      analyzePlantDisease();
    };
    reader.readAsDataURL(blob);
  } catch (err) {
    console.error('Error loading sample image:', err);
    showToast(state.lang === 'hi' ? 'नमूना फोटो लोड करने में त्रुटि' : 'Could not load sample image', 'error');
  }
}"""

new_sample_fn = """function handleCropSelectionChange() {
  const cropSelect = document.getElementById('diseaseCropSelect');
  if (cropSelect) {
    const val = cropSelect.value;
    if (val !== 'Auto') {
      state.crop = val;
      localStorage.setItem('sap_crop', val);
    }
  }
}

async function loadSampleDiseasePhoto(filePath, diseaseName, cropHint) {
  try {
    switchTab('disease');

    // Auto-select corresponding crop in Target Crop dropdown
    const cropSelect = document.getElementById('diseaseCropSelect');
    if (cropSelect) {
      if (cropHint) {
        cropSelect.value = cropHint;
      } else if (diseaseName) {
        const lower = diseaseName.toLowerCase();
        if (lower.includes('potato')) cropSelect.value = 'Potato';
        else if (lower.includes('corn') || lower.includes('maize')) cropSelect.value = 'Corn';
        else if (lower.includes('sugarcane')) cropSelect.value = 'Sugarcane';
        else if (lower.includes('wheat')) cropSelect.value = 'Wheat';
        else if (lower.includes('cotton')) cropSelect.value = 'Cotton';
        else if (lower.includes('rice')) cropSelect.value = 'Rice';
        else if (lower.includes('soybean')) cropSelect.value = 'Soybean';
      }
    }

    showToast(state.lang === 'hi' ? `${diseaseName} का नमूना लोड हो रहा है...` : `Loading sample ${diseaseName}...`, 'info');

    // Fetch the sample image file and convert to base64
    const response = await fetch(filePath);
    if (!response.ok) throw new Error(`Failed to load ${filePath}`);
    const blob = await response.blob();

    const reader = new FileReader();
    reader.onloadend = () => {
      selectedImageBase64 = reader.result;

      const previewCard = document.getElementById('diseasePreviewCard');
      const previewImg = document.getElementById('leafImagePreview');
      const previewName = document.getElementById('previewFileName');
      const scanImgCopy = document.getElementById('scanningImageCopy');

      if (previewCard) previewCard.classList.remove('hidden');
      if (previewImg) previewImg.src = selectedImageBase64;
      if (scanImgCopy) scanImgCopy.src = selectedImageBase64;
      if (previewName) previewName.textContent = diseaseName;

      // Automatically run disease analysis
      analyzePlantDisease();
    };
    reader.readAsDataURL(blob);
  } catch (err) {
    console.error('Error loading sample image:', err);
    showToast(state.lang === 'hi' ? 'नमूना फोटो लोड करने में त्रुटि' : 'Could not load sample image', 'error');
  }
}"""

if old_sample_fn in orig_js:
    orig_js = orig_js.replace(old_sample_fn, new_sample_fn)
    print("Replaced loadSampleDiseasePhoto successfully!")
else:
    print("[WARN] old_sample_fn exact match not found")

# 3. Replace analyzePlantDisease & renderDiseaseResults
p_start = orig_js.find('async function analyzePlantDisease()')
p_end = orig_js.find('// ─── AI KISAN ASSISTANT CHAT ENGINE (TAB 6)', p_start)

new_analysis_and_render = """async function analyzePlantDisease() {
  if (!selectedImageBase64) {
    showToast(state.lang === 'hi' ? 'कृपया पहले पत्ती की फोटो चुनें' : 'Please select or capture a leaf photo first', 'warning');
    return;
  }

  const loader = document.getElementById('scanningLoader');
  const resultCard = document.getElementById('diseaseResultContainer');
  const scanBtn = document.getElementById('scanButton');

  if (loader) loader.classList.remove('hidden');
  if (resultCard) resultCard.classList.add('hidden');
  if (scanBtn) scanBtn.disabled = true;

  try {
    const cropSelect = document.getElementById('diseaseCropSelect');
    const selectedCrop = cropSelect ? cropSelect.value : (state.crop || 'Wheat');

    // Call real AI backend endpoint
    const response = await fetch(`${API_BASE}/api/disease/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image: selectedImageBase64,
        crop: selectedCrop,
        language: state.lang || 'en'
      })
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    window.lastDiagnosisResult = data;
    renderDiseaseResults(data);

    if (data.is_leaf === false) {
      showToast(state.lang === 'hi' ? 'कोई पौधे की पत्ती नहीं पाई गई' : 'No plant leaf detected', 'warning');
    } else if (data.prediction === 'DATASET_NOT_READY' || data.success === false) {
      showToast(state.lang === 'hi' ? 'इस फसल के लिए AI मॉडल अभी उपलब्ध नहीं है' : 'AI model for this crop is currently unavailable', 'warning');
    } else {
      showToast(state.lang === 'hi' ? 'रोग निदान और उपचार प्राप्त!' : 'Disease Diagnosis Complete!', 'success');
    }
  } catch (err) {
    console.error("Inference Error:", err);
    showToast(state.lang === 'hi' ? `जांच विफल: ${err.message}` : `Scan failed: ${err.message}`, 'error');
  } finally {
    if (loader) loader.classList.add('hidden');
    if (scanBtn) scanBtn.disabled = false;
  }
}

function renderDiseaseResults(data) {
  const resultCard = document.getElementById('diseaseResultContainer');
  if (!resultCard || !data) return;

  const isHi = (state.lang === 'hi' || (typeof currentLanguage !== 'undefined' && currentLanguage === 'hi'));
  const notLeafCard = document.getElementById('diagNotLeafCard');
  const modelUnavailCard = document.getElementById('diagModelUnavailableCard');
  const headerCard = document.getElementById('diagHeaderCard');
  const heatmapSection = document.getElementById('diagHeatmapSection');
  const treatmentGrid = document.getElementById('diagTreatmentGrid');
  const top5Container = document.getElementById('diagTop5Container');

  // Case 1: Out-of-domain rejection (Not_A_Leaf)
  if (data.is_leaf === false || data.prediction === 'Not_A_Leaf') {
    if (notLeafCard) {
      notLeafCard.classList.remove('hidden');
      const msgEl = document.getElementById('diagNotLeafMessage');
      if (msgEl) {
        msgEl.innerText = isHi
          ? 'अपलोड की गई फोटो में कोई पौधे की पत्ती नहीं पाई गई। कृपया फसल की पत्ती की स्पष्ट फोटो अपलोड करें।'
          : (data.message || 'No plant leaf detected. Please upload a clear photo of a crop leaf.');
      }
    }
    if (modelUnavailCard) modelUnavailCard.classList.add('hidden');
    if (headerCard) headerCard.classList.add('hidden');
    if (heatmapSection) heatmapSection.classList.add('hidden');
    if (treatmentGrid) treatmentGrid.classList.add('hidden');
    if (top5Container && top5Container.parentElement) top5Container.parentElement.classList.add('hidden');

    resultCard.classList.remove('hidden');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  // Case 2: Model Unavailable / DATASET_NOT_READY
  if (data.prediction === 'DATASET_NOT_READY' || data.success === false) {
    if (modelUnavailCard) {
      modelUnavailCard.classList.remove('hidden');
      const msgEl = document.getElementById('diagModelUnavailableMessage');
      if (msgEl) {
        msgEl.innerText = isHi
          ? 'इस फसल के लिए AI मॉडल अभी उपलब्ध नहीं है। कृपया गेहूं, कपास, गन्ना, आलू, धान अथवा सोयाबीन चुनें।'
          : (data.message || 'AI model for this crop is currently unavailable. Please select Wheat, Cotton, Sugarcane, Potato, Rice, or Soybean.');
      }
    }
    if (notLeafCard) notLeafCard.classList.add('hidden');
    if (headerCard) headerCard.classList.add('hidden');
    if (heatmapSection) heatmapSection.classList.add('hidden');
    if (treatmentGrid) treatmentGrid.classList.add('hidden');
    if (top5Container && top5Container.parentElement) top5Container.parentElement.classList.add('hidden');

    resultCard.classList.remove('hidden');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  // Case 3: Valid Crop Leaf Diagnosed
  if (notLeafCard) notLeafCard.classList.add('hidden');
  if (modelUnavailCard) modelUnavailCard.classList.add('hidden');
  if (headerCard) headerCard.classList.remove('hidden');
  if (treatmentGrid) treatmentGrid.classList.remove('hidden');
  if (top5Container && top5Container.parentElement) top5Container.parentElement.classList.remove('hidden');

  // Look up localized disease info
  const localizedInfo = (typeof tDisease === 'function') ? tDisease(data.prediction) : {};
  const cropLocalized = (typeof tCrop === 'function') ? tCrop(data.crop) : (data.crop || 'Crop');

  // Badges
  const cropBadge = document.getElementById('diagCropBadge');
  const sevBadge = document.getElementById('diagSeverityBadge');

  if (cropBadge) {
    cropBadge.innerText = `${isHi ? 'फसल:' : 'Crop:'} ${cropLocalized} (YOLO11-cls + GradCAM)`;
  }

  const affectedArea = typeof data.affected_area_percent === 'number' ? data.affected_area_percent : 0;
  const isHealthy = data.is_healthy || (data.prediction && data.prediction.toLowerCase().includes('healthy')) || localizedInfo.is_healthy;

  if (sevBadge) {
    if (isHealthy) {
      sevBadge.innerText = isHi ? 'पूरी तरह स्वस्थ' : 'Healthy Leaf';
      sevBadge.className = "bg-emerald-500/20 text-emerald-300 text-xs font-bold px-3 py-1 rounded-full border border-emerald-500/30";
    } else if (affectedArea > 35) {
      sevBadge.innerText = isHi ? 'गंभीर संक्रमण' : 'High Severity';
      sevBadge.className = "bg-rose-500/20 text-rose-300 text-xs font-bold px-3 py-1 rounded-full border border-rose-500/30";
    } else {
      sevBadge.innerText = isHi ? 'मध्यम संक्रमण' : 'Moderate Severity';
      sevBadge.className = "bg-amber-500/20 text-amber-300 text-xs font-bold px-3 py-1 rounded-full border border-amber-500/30";
    }
  }

  // Titles
  const titleEn = document.getElementById('diagTitleEn');
  const titleHi = document.getElementById('diagTitleHi');
  const confVal = document.getElementById('diagConfidenceValue');

  const diseaseEn = localizedInfo.disease_name && !isHi ? localizedInfo.disease_name : (data.disease_name_en || data.display_name || data.prediction);
  const diseaseHi = localizedInfo.disease_name && isHi ? localizedInfo.disease_name : (data.disease_name_hi || data.display_name || data.prediction);

  if (titleEn) titleEn.innerText = isHi ? diseaseHi : diseaseEn;
  if (titleHi) titleHi.innerText = isHi ? diseaseEn : diseaseHi;

  const confPercent = typeof data.confidence === 'number'
    ? (data.confidence <= 1.0 ? (data.confidence * 100).toFixed(1) : data.confidence.toFixed(1))
    : data.confidence;
  if (confVal) confVal.innerText = `${confPercent}%`;

  // Severity Progress Bar & Lesion Coverage
  const sevPercentText = document.getElementById('diagSeverityPercentText');
  const sevProgressBar = document.getElementById('diagSeverityProgressBar');

  if (sevPercentText) {
    sevPercentText.innerText = `${affectedArea}% (${isHi ? 'प्रभावित क्षेत्र' : 'Lesion Coverage'})`;
  }
  if (sevProgressBar) {
    sevProgressBar.style.width = `${Math.min(100, Math.max(isHealthy ? 1 : 5, affectedArea))}%`;
  }

  // Grad-CAM Visual Heatmap Section
  if (heatmapSection) {
    if (data.highlight_image) {
      heatmapSection.classList.remove('hidden');
      const origImgEl = document.getElementById('diagOriginalLeafImg');
      const heatmapOverlayEl = document.getElementById('diagHeatmapOverlayImg');
      const affBadge = document.getElementById('diagAffectedAreaBadge');

      if (origImgEl && selectedImageBase64) origImgEl.src = selectedImageBase64;
      if (heatmapOverlayEl) heatmapOverlayEl.src = data.highlight_image;
      if (affBadge) affBadge.innerText = `${isHi ? 'प्रभावित क्षेत्र:' : 'Affected Area:'} ${affectedArea}%`;
    } else {
      heatmapSection.classList.add('hidden');
    }
  }

  // Agronomic Treatments (Localized)
  const symptomsEl = document.getElementById('diagSymptomsText');
  const organicEl = document.getElementById('diagOrganicText');
  const chemicalEl = document.getElementById('diagChemicalText');
  const preventionEl = document.getElementById('diagPreventionText');

  if (symptomsEl) symptomsEl.innerText = isHi ? (localizedInfo.symptoms || data.symptoms_hi || data.symptoms_en) : (localizedInfo.symptoms || data.symptoms_en || data.symptoms_hi);
  if (organicEl) organicEl.innerText = isHi ? (localizedInfo.organic_remedy || data.organic_remedy_hi || data.organic_remedy_en) : (localizedInfo.organic_remedy || data.organic_remedy_en || data.organic_remedy_hi);
  if (chemicalEl) chemicalEl.innerText = isHi ? (localizedInfo.chemical_treatment || data.chemical_treatment_hi || data.chemical_treatment_en) : (localizedInfo.chemical_treatment || data.chemical_treatment_en || data.chemical_treatment_hi);
  if (preventionEl) preventionEl.innerText = isHi ? (localizedInfo.prevention || data.prevention_hi || data.prevention_en) : (localizedInfo.prevention || data.prevention_en || data.prevention_hi);

  // Top 5 Probabilities Container
  if (top5Container && data.top_predictions) {
    top5Container.innerHTML = data.top_predictions.map(pred => {
      const predLoc = (typeof tDisease === 'function') ? tDisease(pred.class || pred.disease_en) : {};
      const name = isHi ? (pred.disease_hi || predLoc.disease_name || pred.class) : (pred.disease_en || predLoc.disease_name || pred.class);
      const conf = typeof pred.confidence === 'number' ? (pred.confidence <= 1 ? (pred.confidence * 100).toFixed(1) : pred.confidence.toFixed(1)) : pred.confidence;
      return `
        <div class="space-y-1 text-xs">
          <div class="flex justify-between font-semibold text-slate-700 dark:text-slate-300">
            <span>${name}</span>
            <span class="font-bold text-emerald-600 dark:text-emerald-400">${conf}%</span>
          </div>
          <div class="w-full h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full bg-emerald-500 rounded-full" style="width: ${conf}%"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  resultCard.classList.remove('hidden');
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

"""

if p_start != -1 and p_end != -1:
    orig_js = orig_js[:p_start] + new_analysis_and_render + '\n\n' + orig_js[p_end:]
    print("Replaced analyzePlantDisease & renderDiseaseResults successfully!")
else:
    print(f"[ERROR] Could not find markers: p_start={p_start}, p_end={p_end}")

# Write to target files
targets = [
    'final sap project/final sap project/app.js',
    'final sap project/final sap project/final sap project/app.js',
    'final sap project/app.js'
]
for p in targets:
    d = os.path.dirname(p)
    if os.path.exists(d):
        with open(p, 'w', encoding='utf-8') as f:
            f.write(orig_js)
        print(f"Saved: {p} ({len(orig_js)} bytes)")

print("Successfully restored and synchronized app.js across all locations!")
