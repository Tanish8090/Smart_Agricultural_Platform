/**
 * Smart Agriculture Platform (SAP) — Client Application Logic
 * Modular JavaScript handling weather intelligence, geocoding, AI Plant Disease Scanner,
 * Smart Crop & Fertilizer Advisor, and AI Kisan Assistant Chatbot with Multilingual & Voice Support.
 */

// ─── API Configuration ───────────────────────────────────────────────────────
// Automatically route API requests to python3 server.py (port 8080) if opened from
// VS Code Live Server (port 5500), another dev server port, or file protocol.
const API_BASE = (window.location.protocol === 'file:' || (window.location.port && window.location.port !== '8080'))
  ? 'http://localhost:8080'
  : '';

// ─── Global App State ────────────────────────────────────────────────────────
function loadInitialFarmLocation() {
  try {
    const saved = localStorage.getItem('sap_farm_location');
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed && typeof parsed.lat === 'number' && typeof parsed.lon === 'number') {
        return parsed;
      }
    }
  } catch (e) {
    console.warn('Could not parse sap_farm_location:', e);
  }
  return {
    lat: parseFloat(localStorage.getItem('sap_lat')) || 26.4499, // Default: Kanpur
    lon: parseFloat(localStorage.getItem('sap_lon')) || 80.3319,
    pincode: localStorage.getItem('sap_pincode') || '208001',
    city: localStorage.getItem('sap_city') || 'Kanpur',
    state: localStorage.getItem('sap_state') || 'Uttar Pradesh',
    district: localStorage.getItem('sap_district') || 'Kanpur Nagar',
    block: localStorage.getItem('sap_block') || '',
    country: localStorage.getItem('sap_country') || 'India',
  };
}

const state = {
  lang: localStorage.getItem('sap_lang') || 'en', // 'en' or 'hi'
  theme: localStorage.getItem('sap_theme') || 'light', // 'light' or 'dark'
  crop: localStorage.getItem('sap_crop') || 'Wheat',
  location: loadInitialFarmLocation(),
  weatherData: null,
  weatherCache: {}, // In-memory cache { "lat,lon,crop": { timestamp, data } }
  activeTab: 'dashboard',
  activeLocModalTab: 'pincode',
  isDetectingGPS: false,
  isLoadingWeather: false,
};

// ─── Smart Crop & Fertilizer Advisor State ──────────────────────────────────
const fertState = {
  crop: localStorage.getItem('sap_fert_crop') || 'Wheat',
  stage: localStorage.getItem('sap_fert_stage') || 'Vegetative',
  soil: localStorage.getItem('sap_fert_soil') || 'Alluvial / Loam Soil',
  area: localStorage.getItem('sap_fert_area') || '2',
  areaUnit: localStorage.getItem('sap_fert_unit') || 'acre',
  irrigation: localStorage.getItem('sap_fert_irrigation') || 'Tube Well / Borewell',
  attachedImageBase64: null,
  attachedImageName: null,
  lastRecommendation: null,
  isLoading: false,
};

// ─── Mandi Prices State ───────────────────────────────────────────────────────
const mandiState = {
  commodity: localStorage.getItem('sap_mandi_commodity') || 'Wheat',
  radius: localStorage.getItem('sap_mandi_radius') || '50',
  sortBy: 'distance', // 'distance', 'highest_price', 'lowest_price'
  searchQuery: '',
  data: null,
  isLoading: false,
};

// ─── AI Kisan Chatbot State ──────────────────────────────────────────────────
const chatState = {
  messages: [], // Array of { id, role, text, timestamp, image, intent, disease_scan, suggested_actions }
  farmerContext: {
    location: 'Bhopal, Madhya Pradesh',
    pincode: '462001',
    crop: 'Wheat',
    cropStage: localStorage.getItem('sap_crop_stage') || 'Vegetative / Growth',
    soilType: localStorage.getItem('sap_soil_type') || 'Alluvial / Loam Soil',
    irrigationType: localStorage.getItem('sap_irrigation_type') || 'Tube-well / Flood',
    acreage: localStorage.getItem('sap_acreage') || '2 Acres',
    weather: null,
  },
  attachedImageBase64: null,
  attachedImageName: null,
  isGenerating: false,
  isRecording: false,
  speechRecognition: null,
  autoVoiceEnabled: localStorage.getItem('sap_auto_voice') === 'true',
  currentlySpeakingBtn: null,
};

// Weather Icon Map (OWM icon code → FontAwesome class)
const weatherIconMap = {
  '01d': 'fa-sun text-amber-400',
  '01n': 'fa-moon text-slate-300',
  '02d': 'fa-cloud-sun text-amber-300',
  '02n': 'fa-cloud-moon text-slate-300',
  '03d': 'fa-cloud text-slate-300',
  '03n': 'fa-cloud text-slate-400',
  '04d': 'fa-clouds text-slate-400',
  '04n': 'fa-clouds text-slate-500',
  '09d': 'fa-cloud-showers-heavy text-blue-400',
  '09n': 'fa-cloud-showers-heavy text-blue-400',
  '10d': 'fa-cloud-sun-rain text-blue-300',
  '10n': 'fa-cloud-moon-rain text-blue-400',
  '11d': 'fa-cloud-bolt text-amber-500',
  '11n': 'fa-cloud-bolt text-amber-500',
  '13d': 'fa-snowflake text-cyan-300',
  '13n': 'fa-snowflake text-cyan-300',
  '50d': 'fa-smog text-slate-300',
  '50n': 'fa-smog text-slate-400',
};


// ─── Initialization ───────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLanguage();
  initCropSelectors();
  updateDiseaseModelBadge();
  initChatState();
  initFertilizerTab();
  updateLocationHeroUI();
  // Load weather for persisted location without prompting GPS
  loadWeatherForCurrentState();
});


// ─── Theme Management ─────────────────────────────────────────────────────────
function initTheme() {
  if (state.theme === 'dark') {
    document.documentElement.classList.add('dark');
    document.documentElement.classList.remove('light');
    const icon = document.getElementById('themeIcon');
    if (icon) icon.className = 'fa-solid fa-sun text-amber-300';
  } else {
    document.documentElement.classList.remove('dark');
    document.documentElement.classList.add('light');
    const icon = document.getElementById('themeIcon');
    if (icon) icon.className = 'fa-solid fa-moon';
  }
}

function toggleDarkMode() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('sap_theme', state.theme);
  initTheme();
}


// ─── Language Switcher (Bilingual Support) ──────────────────────────────────
function initLanguage() {
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
}


// ─── Navigation Tabs ──────────────────────────────────────────────────────────
function switchTab(tabId) {
  state.activeTab = tabId;

  // Highlight active nav button
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  const activeBtn = document.getElementById(`tab-${tabId}`);
  if (activeBtn) activeBtn.classList.add('active');

  // Hide all tab views
  document.querySelectorAll('.tab-view').forEach(view => {
    view.classList.add('hidden');
  });

  if (tabId === 'dashboard') {
    const dashView = document.getElementById('view-dashboard');
    if (dashView) {
      dashView.classList.remove('hidden');
      renderDashboardOverview();
    }
  } else if (tabId === 'weather') {
    const weatherView = document.getElementById('view-weather');
    if (weatherView) weatherView.classList.remove('hidden');
  } else if (tabId === 'disease') {
    const diseaseView = document.getElementById('view-disease');
    if (diseaseView) diseaseView.classList.remove('hidden');
  } else if (tabId === 'fertilizer') {
    const fertView = document.getElementById('view-fertilizer');
    if (fertView) {
      fertView.classList.remove('hidden');
      initFertilizerTab();
    }
  } else if (tabId === 'market') {
    const marketView = document.getElementById('view-market');
    if (marketView) {
      marketView.classList.remove('hidden');
      initMandiTab();
    }
  } else if (tabId === 'bot') {
    const botView = document.getElementById('view-bot');
    if (botView) {
      botView.classList.remove('hidden');
      syncFarmerContext();
      scrollChatToBottom();
    }
  }
}

function renderDashboardOverview() {
  const isHi = state.lang === 'hi';
  const hour = new Date().getHours();
  let greeting = 'Good Morning';
  let greetingHi = 'सुप्रभात';
  if (hour >= 12 && hour < 17) {
    greeting = 'Good Afternoon';
    greetingHi = 'शुभ दोपहर';
  } else if (hour >= 17) {
    greeting = 'Good Evening';
    greetingHi = 'शुभ संध्या';
  }

  const greetingEl = document.getElementById('dashboardGreeting');
  if (greetingEl) {
    greetingEl.textContent = isHi ? `${greetingHi}, किसान साथी 👋` : `${greeting}, Farmer 👋`;
  }

  const subtextEl = document.getElementById('dashboardSubtext');
  if (subtextEl) {
    const locName = state.location.city || state.location.district || 'Kanpur';
    const stateName = state.location.state || 'Uttar Pradesh';
    subtextEl.textContent = isHi 
      ? `आपके सक्रिय कृषि क्षेत्र (${locName}, ${stateName}) के लिए आज का वास्तविक समय कृषि विश्लेषण।`
      : `Here is today's real-time agricultural intelligence for your active landholding in ${locName}, ${stateName}.`;
  }

  const activeCropEl = document.getElementById('dashActiveCropText');
  if (activeCropEl) {
    activeCropEl.textContent = `🌾 ${state.crop || 'Wheat'} (${fertState.stage || 'Vegetative'})`;
  }

  const wData = state.weatherData;
  if (wData && wData.current) {
    const cur = wData.current;
    const glanceEl = document.getElementById('dashWeatherGlanceText');
    if (glanceEl) glanceEl.textContent = `🌤 ${cur.temp}°C · ${cur.description}`;

    const tempEl = document.getElementById('dashWeatherTempText');
    if (tempEl) tempEl.textContent = `${cur.temp}°C`;

    const condEl = document.getElementById('dashWeatherConditionText');
    if (condEl) condEl.textContent = `${cur.description} · ${cur.rain_probability || 10}% Rain Risk`;

    const iconPreview = document.getElementById('dashWeatherIconPreview');
    if (iconPreview && cur.icon) {
      const faClass = weatherIconMap[cur.icon] || 'fa-sun text-amber-400';
      iconPreview.innerHTML = `<i class="fa-solid ${faClass}"></i>`;
    }

    const advSnippet = document.getElementById('dashWeatherAdvisorySnippet');
    if (advSnippet && wData.agri_advisory) {
      advSnippet.textContent = isHi ? (wData.agri_advisory.crop_impact_hi || wData.agri_advisory.irrigation_hi || wData.agri_advisory.crop_impact) : (wData.agri_advisory.crop_impact || wData.agri_advisory.irrigation);
    }
  }

  if (mandiState.data && mandiState.data.results && mandiState.data.results.length > 0) {
    const top = mandiState.data.results[0];
    const mandiPriceEl = document.getElementById('dashMandiPriceText');
    if (mandiPriceEl) {
      mandiPriceEl.innerHTML = `₹${top.modal_price.toLocaleString('en-IN')} <span class="text-xs font-normal text-slate-500">/qtl</span>`;
    }
  }
}

function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  if (menu) menu.classList.toggle('hidden');
}


// ─── Location Management (Method 1: GPS, Method 2: PIN, Method 3: City) ──────

function updateLocationHeroUI() {
  const isHi = state.lang === 'hi';
  const loc = state.location;

  // Header Badge (top navigation)
  const headerBadge = document.getElementById('pincodeBadgeText');
  if (headerBadge) {
    if (loc.pincode && loc.pincode !== 'GPS' && loc.pincode !== 'City') {
      headerBadge.textContent = `PIN: ${loc.pincode} (${loc.city || 'Farm'})`;
    } else {
      headerBadge.textContent = `📍 ${loc.city || 'Farm'} (${loc.state || 'India'})`;
    }
  }

  // Location Hero Title & Subtext
  const titleEl = document.getElementById('locationTitle');
  if (titleEl) {
    if (loc.city && loc.city !== 'My Farm (GPS)') {
      titleEl.textContent = `My Farm — ${loc.city}${loc.state ? ', ' + loc.state : ''}`;
    } else if (loc.pincode === 'GPS' || loc.city === 'My Farm (GPS)') {
      titleEl.textContent = `My Farm (GPS)${loc.state ? ', ' + loc.state : ''}`;
    } else {
      titleEl.textContent = `${loc.city || 'Farm Location'}${loc.state ? ', ' + loc.state : ''}`;
    }
  }

  const subEl = document.getElementById('locationSubtext');
  if (subEl) {
    const pinPart = (loc.pincode && loc.pincode !== 'GPS' && loc.pincode !== 'City') ? `PIN: ${loc.pincode}` : '';
    const distPart = loc.district ? `District: ${loc.district}` : '';
    const statePart = loc.state ? `State: ${loc.state}` : 'State: India';

    if (isHi) {
      const parts = [
        statePart.replace('State:', 'राज्य:'),
        distPart ? distPart.replace('District:', 'जिला:') : '',
        pinPart ? pinPart.replace('PIN:', 'पिन:') : ''
      ].filter(Boolean);
      subEl.textContent = parts.join(' | ');
    } else {
      const parts = [statePart, distPart, pinPart].filter(Boolean);
      subEl.textContent = parts.join(' | ');
    }
  }

  syncFertilizerContext();
}

function saveLocationToStorage() {
  localStorage.setItem('sap_farm_location', JSON.stringify(state.location));
  localStorage.setItem('sap_lat', state.location.lat);
  localStorage.setItem('sap_lon', state.location.lon);
  localStorage.setItem('sap_pincode', state.location.pincode || '');
  localStorage.setItem('sap_city', state.location.city || '');
  localStorage.setItem('sap_state', state.location.state || '');
  localStorage.setItem('sap_district', state.location.district || '');
  localStorage.setItem('sap_block', state.location.block || '');
  localStorage.setItem('sap_country', state.location.country || 'India');
}

/**
 * Applies a full location object to active profile, hero UI, storage and triggers fresh weather
 */
function applyLocationObject(loc) {
  if (!loc) return;

  state.location.lat = roundCoord(loc.lat);
  state.location.lon = roundCoord(loc.lon);
  state.location.city = loc.city;
  state.location.state = loc.state || '';
  state.location.district = loc.district || loc.city;
  state.location.pincode = loc.pincode || 'City';
  state.location.block = loc.block || '';
  state.location.country = 'India';

  saveLocationToStorage();
  updateLocationHeroUI();
  renderDashboardOverview();
  loadWeatherForCurrentState(true);
  syncFarmerContext();
  syncFertilizerContext();

  showToast(
    state.lang === 'hi'
      ? `स्थान सेट किया गया: ${loc.city}${loc.state ? ', ' + loc.state : ''}`
      : `Location set: ${loc.city}${loc.state ? ', ' + loc.state : ''}`,
    'success'
  );
}

// ─── Method 1: GPS Geolocation with Native Capacitor & Browser Fallback ─────
async function detectGPSLocation() {
  if (state.isDetectingGPS) return;

  state.isDetectingGPS = true;
  setGpsLoadingState(true);
  showToast(state.lang === 'hi' ? '📍 जीपीएस स्थान खोजा जा रहा है...' : '📍 Detecting live GPS location...', 'info');

  const onGpsSuccess = async (lat, lon) => {
    state.location.lat = roundCoord(lat);
    state.location.lon = roundCoord(lon);
    state.location.pincode = 'GPS';

    // 1. Try local nearest location lookup first (100% offline capable)
    let resolvedCity = 'My Farm (GPS)';
    let resolvedState = state.location.state || 'Uttar Pradesh';
    let resolvedDistrict = 'GPS Coordinates';

    if (typeof findNearestLocation === 'function') {
      const nearest = findNearestLocation(lat, lon);
      if (nearest && nearest.location && nearest.distanceKm <= 50) {
        resolvedCity = nearest.location.city;
        resolvedState = nearest.location.state;
        resolvedDistrict = nearest.location.district || nearest.location.city;
      }
    }

    // 2. If online and API_BASE is reachable, attempt reverse geocode
    if (navigator.onLine && API_BASE) {
      try {
        const res = await fetch(`${API_BASE}/api/reverse-geocode?lat=${lat}&lon=${lon}`);
        if (res.ok) {
          const data = await res.json();
          if (data.status === 'success' && data.city) {
            resolvedCity = data.city;
            resolvedState = data.state || resolvedState;
            resolvedDistrict = data.district || resolvedDistrict;
          }
        }
      } catch (e) {
        console.warn('Reverse geocode error:', e);
      }
    }

    state.location.city = resolvedCity;
    state.location.state = resolvedState;
    state.location.district = resolvedDistrict;
    state.location.country = 'India';

    saveLocationToStorage();
    updateLocationHeroUI();
    renderDashboardOverview();
    loadWeatherForCurrentState(true);
    syncFarmerContext();
    syncFertilizerContext();

    setGpsLoadingState(false);
    state.isDetectingGPS = false;

    showToast(
      state.lang === 'hi'
        ? `सटीक जीपीएस स्थान मिला: ${state.location.city} (${lat.toFixed(4)}, ${lon.toFixed(4)})`
        : `GPS location resolved: ${state.location.city} (${lat.toFixed(4)}, ${lon.toFixed(4)})`,
      'success'
    );
  };

  const onGpsError = (err) => {
    console.warn('Geolocation error:', err);
    setGpsLoadingState(false);
    state.isDetectingGPS = false;

    const isDenied = (err && (err.code === 1 || String(err).includes('PERMISSION_DENIED') || String(err.message).includes('denied')));
    const msg = isDenied
      ? (state.lang === 'hi'
          ? 'आपके वर्तमान खेत का स्थान पता करने के लिए लोकेशन अनुमति आवश्यक है।'
          : 'Location permission is required to detect your current farm location.')
      : (state.lang === 'hi'
          ? 'जीपीएस स्थान प्राप्त करने में समस्या हुई। कृपया मैन्युअल रूप से स्थान दर्ज करें।'
          : 'Could not detect location. Please enter your PIN code or city manually.');

    showToast(msg, 'warning');
    openPincodeModal();
  };

  // Check Capacitor native plugin first
  if (window.Capacitor && window.Capacitor.isPluginAvailable && window.Capacitor.isPluginAvailable('OnnxInference')) {
    try {
      const loc = await window.Capacitor.Plugins.OnnxInference.getCurrentLocation();
      if (loc && typeof loc.latitude === 'number' && typeof loc.longitude === 'number') {
        await onGpsSuccess(loc.latitude, loc.longitude);
        return;
      }
    } catch (pluginErr) {
      if (String(pluginErr).includes('PERMISSION_DENIED')) {
        onGpsError({ code: 1, message: 'Permission denied' });
        return;
      }
      console.warn('Native GPS plugin call returned error, trying browser geolocation:', pluginErr);
    }
  }

  // Browser navigator.geolocation fallback
  if (!navigator.geolocation) {
    onGpsError({ code: 2, message: 'Not supported' });
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => onGpsSuccess(pos.coords.latitude, pos.coords.longitude),
    (err) => onGpsError(err),
    { enableHighAccuracy: true, timeout: 12000, maximumAge: 60000 }
  );
}

function setGpsLoadingState(isLoading) {
  const btn = document.getElementById('heroGpsBtn');
  const icon = document.getElementById('heroGpsIcon');
  const text = document.getElementById('heroGpsText');

  if (btn) btn.disabled = isLoading;
  if (icon) {
    if (isLoading) icon.className = 'fa-solid fa-spinner fa-spin text-amber-300';
    else icon.className = 'fa-solid fa-crosshairs text-amber-300';
  }
  if (text) {
    if (isLoading) text.textContent = state.lang === 'hi' ? 'खोज रहे हैं...' : 'Detecting...';
    else text.textContent = state.lang === 'hi' ? 'जीपीएस स्थान' : 'Use My Location';
  }
}

// ─── Unified Search (PIN Code or City Name) ──────────────────────────────────
function handleLocationSearchSubmit() {
  const inputEl = document.getElementById('pincodeInput');
  if (!inputEl) return;
  const raw = inputEl.value.trim();

  if (!raw) {
    showToast(state.lang === 'hi' ? 'कृपया पिन कोड या शहर का नाम दर्ज करें' : 'Please enter a PIN code or city name', 'warning');
    return;
  }

  const cleanDigits = raw.replace(/\s+/g, '');
  if (/^\d{6}$/.test(cleanDigits)) {
    // 6-digit Indian PIN Code
    let match = null;
    if (typeof findLocationByPincode === 'function') {
      match = findLocationByPincode(cleanDigits);
    }
    if (match) {
      applyLocationObject(match);
      inputEl.value = '';
    } else {
      showToast(
        state.lang === 'hi'
          ? 'PIN नहीं मिला। कृपया शहर/जिला स्वयं दर्ज करें।'
          : 'PIN not found. Please enter city/district manually.',
        'warning'
      );
      openPincodeModal();
      switchLocationModalTab('city');
    }
  } else if (/^\d+$/.test(cleanDigits)) {
    showToast(
      state.lang === 'hi'
        ? 'कृपया 6 अंकों का सही भारतीय पिन कोड दर्ज करें (जैसे 208001)'
        : 'Please enter a valid 6-digit Indian PIN code (e.g. 208001)',
      'warning'
    );
  } else {
    // City or District query (Case-insensitive local search)
    let results = [];
    if (typeof searchIndianLocations === 'function') {
      results = searchIndianLocations(raw);
    }
    if (results && results.length > 0) {
      applyLocationObject(results[0]);
      inputEl.value = '';
    } else {
      showToast(
        state.lang === 'hi'
          ? `"${raw}" के लिए कोई स्थान नहीं मिला। कृपया प्रमुख शहरों में से चुनें।`
          : `No locations found for "${raw}". Please select from agricultural hubs.`,
        'warning'
      );
      openPincodeModal();
      switchLocationModalTab('city');
      const modalInput = document.getElementById('modalCitySearchInput');
      if (modalInput) {
        modalInput.value = raw;
        executeModalCitySearch();
      }
    }
  }
}

// ─── Method 2: PIN Code Geocoding ───────────────────────────────────────────
async function fetchLocationByPincode(pincode) {
  const cleanPin = String(pincode).replace(/\s+/g, '').trim();
  if (!/^\d{6}$/.test(cleanPin)) {
    showToast(state.lang === 'hi' ? 'कृपया 6 अंकों का सही पिन कोड दर्ज करें' : 'Please enter a valid 6-digit Indian PIN Code', 'warning');
    return;
  }

  // 1. Check local Indian locations database first (Offline-ready)
  if (typeof findLocationByPincode === 'function') {
    const localMatch = findLocationByPincode(cleanPin);
    if (localMatch) {
      applyLocationObject(localMatch);
      closePincodeModal();
      return;
    }
  }

  // 2. If online and API_BASE is available, try server
  if (navigator.onLine && API_BASE) {
    try {
      showToast(state.lang === 'hi' ? `पिन कोड ${cleanPin} खोजा जा रहा है...` : `Resolving PIN code ${cleanPin}...`, 'info');
      const res = await fetch(`${API_BASE}/api/geocode?pincode=${cleanPin}`);
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.status === 'success') {
        applyLocationObject({
          lat: data.lat,
          lon: data.lon,
          city: data.city || 'Farm Area',
          state: data.state || '',
          district: data.district || '',
          pincode: cleanPin
        });
        closePincodeModal();
        return;
      }
    } catch (err) {
      console.warn('Server PIN lookup error:', err);
    }
  }

  showToast(
    state.lang === 'hi'
      ? 'PIN नहीं मिला। कृपया शहर/जिला स्वयं दर्ज करें।'
      : 'PIN not found. Please enter city/district manually.',
    'warning'
  );
  switchLocationModalTab('city');
}

// ─── Method 3: City / District Geocoding ─────────────────────────────────────
async function fetchLocationByCity(cityName) {
  const cleanCity = String(cityName).trim();
  if (!cleanCity) {
    showToast(state.lang === 'hi' ? 'कृपया शहर या जिले का नाम लिखें' : 'Please enter a city or district name', 'warning');
    return;
  }

  // 1. Check local Indian locations database first (Offline-ready)
  if (typeof searchIndianLocations === 'function') {
    const localResults = searchIndianLocations(cleanCity);
    if (localResults && localResults.length > 0) {
      applyLocationObject(localResults[0]);
      closePincodeModal();
      return;
    }
  }

  // 2. If online and API_BASE is available, try server
  if (navigator.onLine && API_BASE) {
    try {
      showToast(state.lang === 'hi' ? `शहर खोजा जा रहा है: ${cleanCity}...` : `Searching location: ${cleanCity}...`, 'info');
      const res = await fetch(`${API_BASE}/api/geocode?q=${encodeURIComponent(cleanCity)}`);
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.status === 'success' && data.lat && data.lon) {
        applyLocationObject({
          lat: data.lat,
          lon: data.lon,
          city: data.city,
          state: data.state || '',
          district: data.district || data.city,
          pincode: 'City'
        });
        closePincodeModal();
        return;
      }
    } catch (err) {
      console.warn('Server city lookup error:', err);
    }
  }

  showToast(
    state.lang === 'hi'
      ? `"${cleanCity}" के लिए कोई स्थान नहीं मिला। कृपया प्रमुख शहरों में से चुनें।`
      : `No locations found for "${cleanCity}". Please select from popular hubs.`,
    'warning'
  );
}

// ─── Tabbed Location Modal Logic ────────────────────────────────────────────
function openPincodeModal() {
  const modal = document.getElementById('pincodeModal');
  if (!modal) return;

  const pinInput = document.getElementById('modalPincodeInput');
  if (pinInput && state.location.pincode && state.location.pincode !== 'GPS' && state.location.pincode !== 'City') {
    pinInput.value = state.location.pincode;
  }

  const cropSel = document.getElementById('modalCropSelect');
  if (cropSel) cropSel.value = state.crop;

  modal.classList.remove('hidden');
}

function closePincodeModal() {
  const modal = document.getElementById('pincodeModal');
  if (modal) modal.classList.add('hidden');
}

function switchLocationModalTab(tabId) {
  state.activeLocModalTab = tabId;

  const tabs = ['Pin', 'City', 'Gps'];
  tabs.forEach(t => {
    const btn = document.getElementById(`locTabBtn${t}`);
    const pane = document.getElementById(`locTabPane${t}`);
    if (btn && pane) {
      if (t.toLowerCase() === tabId.toLowerCase()) {
        btn.className = 'py-2 rounded-xl transition bg-white dark:bg-slate-700 text-emerald-600 dark:text-emerald-300 shadow-sm flex items-center justify-center space-x-1 font-bold';
        pane.classList.remove('hidden');
      } else {
        btn.className = 'py-2 rounded-xl transition text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white flex items-center justify-center space-x-1';
        pane.classList.add('hidden');
      }
    }
  });
}

function executeModalCitySearch() {
  const input = document.getElementById('modalCitySearchInput');
  const resultsContainer = document.getElementById('modalCityResultsList');
  if (!input || !resultsContainer) return;

  const query = input.value.trim();
  if (!query) {
    showToast(state.lang === 'hi' ? 'कृपया शहर का नाम दर्ज करें' : 'Please enter a city name to search', 'warning');
    return;
  }

  const cleanDigits = query.replace(/\s+/g, '');
  if (/^\d{6}$/.test(cleanDigits)) {
    let pinMatch = null;
    if (typeof findLocationByPincode === 'function') {
      pinMatch = findLocationByPincode(cleanDigits);
    }
    if (pinMatch) {
      resultsContainer.classList.remove('hidden');
      resultsContainer.innerHTML = `
        <button onclick="applySelectedCityMatch(${pinMatch.lat}, ${pinMatch.lon}, '${escapeAttribute(pinMatch.city)}', '${escapeAttribute(pinMatch.state || '')}', '${escapeAttribute(pinMatch.district || pinMatch.city)}', '${cleanDigits}')" class="w-full text-left p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 hover:bg-emerald-50 dark:hover:bg-emerald-950 border border-slate-200 dark:border-slate-700 transition flex items-center justify-between text-xs">
          <div>
            <span class="font-bold text-slate-900 dark:text-slate-100">${escapeHTML(pinMatch.city)}</span>
            <span class="text-slate-500 text-[11px]">${pinMatch.district ? ' (' + escapeHTML(pinMatch.district) + ')' : ''}, ${escapeHTML(pinMatch.state || '')} — PIN: ${cleanDigits}</span>
          </div>
          <span class="text-emerald-600 dark:text-emerald-400 font-bold text-[11px]">Select →</span>
        </button>
      `;
      return;
    } else {
      resultsContainer.classList.remove('hidden');
      resultsContainer.innerHTML = `<div class="text-xs text-amber-600 dark:text-amber-400 p-2 text-center font-semibold">${state.lang === 'hi' ? 'PIN नहीं मिला। कृपया शहर/जिला स्वयं दर्ज करें।' : 'PIN not found. Please enter city/district manually.'}</div>`;
      return;
    }
  }

  let results = [];
  if (typeof searchIndianLocations === 'function') {
    results = searchIndianLocations(query);
  }

  resultsContainer.classList.remove('hidden');

  if (!results || results.length === 0) {
    resultsContainer.innerHTML = `<div class="text-xs text-rose-500 p-2 text-center font-semibold">${state.lang === 'hi' ? `"${escapeHTML(query)}" के लिए कोई स्थान नहीं मिला` : `No locations found for "${escapeHTML(query)}"`}</div>`;
    return;
  }

  resultsContainer.innerHTML = results.slice(0, 6).map(r => `
    <button onclick="applySelectedCityMatch(${r.lat}, ${r.lon}, '${escapeAttribute(r.city)}', '${escapeAttribute(r.state || '')}', '${escapeAttribute(r.district || r.city)}', '${escapeAttribute(r.pincode || '')}')" class="w-full text-left p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 hover:bg-emerald-50 dark:hover:bg-emerald-950 border border-slate-200 dark:border-slate-700 transition flex items-center justify-between text-xs">
      <div>
        <span class="font-bold text-slate-900 dark:text-slate-100">${escapeHTML(r.city)}</span>
        <span class="text-slate-500 text-[11px]">${r.district && r.district !== r.city ? ' (' + escapeHTML(r.district) + ')' : ''}${r.state ? ', ' + escapeHTML(r.state) : ''}</span>
      </div>
      <span class="text-emerald-600 dark:text-emerald-400 font-bold text-[11px]">Select →</span>
    </button>
  `).join('');
}

/**
 * Popular Agricultural Hub Buttons (Kanpur, Bhopal, Indore, Lucknow, Ludhiana, Patna, Nashik)
 * Immediately sets city, state, district, saves to storage, updates hero UI and triggers fresh weather
 */
function selectCityQuickChip(cityName) {
  let loc = null;
  if (typeof getLocationByKey === 'function') {
    loc = getLocationByKey(cityName);
  }
  if (!loc && typeof searchIndianLocations === 'function') {
    const results = searchIndianLocations(cityName);
    if (results && results.length > 0) loc = results[0];
  }

  if (loc) {
    applyLocationObject(loc);
    closePincodeModal();
  } else {
    fetchLocationByCity(cityName);
  }
}

function applySelectedCityMatch(lat, lon, city, stateName, district, pincode) {
  applyLocationObject({
    lat,
    lon,
    city,
    state: stateName,
    district: district || city,
    pincode: pincode || 'City'
  });
  closePincodeModal();
}

function applyModalLocation() {
  const cropSel = document.getElementById('modalCropSelect');
  if (cropSel && cropSel.value) {
    state.crop = cropSel.value;
    localStorage.setItem('sap_crop', state.crop);
    initCropSelectors();
    updateDiseaseModelBadge(state.crop);
  }

  if (state.activeLocModalTab === 'pincode') {
    const pin = document.getElementById('modalPincodeInput').value.trim();
    if (pin) {
      fetchLocationByPincode(pin);
    } else {
      closePincodeModal();
      loadWeatherForCurrentState(true);
    }
  } else if (state.activeLocModalTab === 'city') {
    const city = document.getElementById('modalCitySearchInput').value.trim();
    if (city) {
      fetchLocationByCity(city);
    } else {
      closePincodeModal();
      loadWeatherForCurrentState(true);
    }
  } else {
    closePincodeModal();
    loadWeatherForCurrentState(true);
  }
}

function initCropSelectors() {
  const sel = document.getElementById('headerCropSelect');
  if (sel) sel.value = state.crop;
  const modalCrop = document.getElementById('modalCropSelect');
  if (modalCrop) modalCrop.value = state.crop;
  const ctxCrop = document.getElementById('ctxCropSelect');
  if (ctxCrop) ctxCrop.value = state.crop;
  const fertCrop = document.getElementById('fertCropSelect');
  if (fertCrop) fertCrop.value = state.crop;
  const diseaseCrop = document.getElementById('diseaseCropSelect');
  if (diseaseCrop && diseaseCrop.value !== 'Auto') diseaseCrop.value = state.crop;
}

function updateFarmerProfile() {
  const newCrop = document.getElementById('headerCropSelect').value;
  state.crop = newCrop;
  localStorage.setItem('sap_crop', newCrop);
  initCropSelectors();
  updateDiseaseModelBadge(newCrop);
  const advCrop = document.getElementById('advisoryCropName');
  if (advCrop) advCrop.textContent = newCrop;
  loadWeatherForCurrentState(true);
  syncFarmerContext();
  syncFertilizerContext();
}

const CROP_HINDI_NAMES = {
  'Wheat': 'गेहूं',
  'Rice': 'धान',
  'Potato': 'आलू',
  'Tomato': 'टमाटर',
  'Cotton': 'कपास',
  'Sugarcane': 'गन्ना',
  'Corn': 'मक्का',
  'Soybean': 'सोयाबीन',
  'Apple': 'सेब',
  'Grape': 'अंगूर',
  'Auto': 'सभी फसलें'
};

/**
 * Dynamically displays the local ONNX model name in Disease Scanner UI
 * Replaces any misleading API or Gemini status
 */
function updateDiseaseModelBadge(cropName) {
  const crop = cropName || state.crop || 'Wheat';
  const isHi = state.lang === 'hi' || (typeof currentLanguage !== 'undefined' && currentLanguage === 'hi');
  const badge = document.getElementById('aiEngineBadgeText');
  const subBadge = document.getElementById('aiEngineSubBadge');
  const onDeviceBadge = document.getElementById('onDeviceModelBadge');

  const hiCrop = CROP_HINDI_NAMES[crop] || crop;

  if (badge) {
    if (crop === 'Auto') {
      badge.textContent = isHi ? 'मॉडल: स्थानीय बहु-फसल ONNX मॉडल' : 'Model: Multi-Crop Local ONNX Model';
    } else {
      badge.textContent = isHi ? `मॉडल: ${hiCrop} — स्थानीय ONNX मॉडल` : `Model: ${crop} — Local ONNX Model`;
    }
  }

  if (subBadge) {
    subBadge.textContent = isHi ? 'स्थानीय फसल-विशिष्ट मॉडल' : 'Local Crop-Specific Model';
  }

  if (onDeviceBadge) {
    onDeviceBadge.textContent = isHi ? '✓ डिवाइस पर AI मॉडल' : '✓ On-Device AI Model';
  }
}

// ─── Weather Data Fetching, 10-Min Caching & UI Rendering ────────────────────

function refreshWeatherNow() {
  const refreshIcon = document.getElementById('weatherRefreshIcon');
  if (refreshIcon) refreshIcon.classList.add('fa-spin');

  showToast(state.lang === 'hi' ? 'मौसम डाटा रीफ्रेश किया जा रहा है...' : 'Refreshing live weather data...', 'info');

  loadWeatherForCurrentState(true).finally(() => {
    setTimeout(() => {
      if (refreshIcon) refreshIcon.classList.remove('fa-spin');
    }, 800);
  });
}

function renderWeatherUnavailable() {
  const isHi = state.lang === 'hi';
  state.weatherData = null;

  // Header Location
  const locEl = document.getElementById('currentLocationName');
  if (locEl) {
    locEl.textContent = `${state.location.city || 'Your Farm'}${state.location.state ? ', ' + state.location.state : ''}`;
  }

  // Dashboard Overview
  const glanceEl = document.getElementById('dashWeatherGlanceText');
  if (glanceEl) glanceEl.textContent = isHi ? 'मौसम उपलब्ध नहीं है' : 'Weather unavailable';

  const tempEl = document.getElementById('dashWeatherTempText');
  if (tempEl) tempEl.textContent = '--°C';

  const condEl = document.getElementById('dashWeatherConditionText');
  if (condEl) condEl.textContent = isHi ? 'लाइव मौसम के लिए इंटरनेट आवश्यक है' : 'Live weather requires internet';

  const advSnippet = document.getElementById('dashWeatherAdvisorySnippet');
  if (advSnippet) advSnippet.textContent = isHi ? 'लाइव मौसम की जानकारी के लिए इंटरनेट कनेक्शन आवश्यक है।' : 'Live weather requires an internet connection.';

  // Main Weather Tab values
  const tempVal = document.getElementById('tempValue');
  if (tempVal) tempVal.textContent = '--';

  const feelsEl = document.getElementById('feelsLikeText');
  if (feelsEl) feelsEl.textContent = isHi ? 'लाइव मौसम के लिए इंटरनेट कनेक्शन आवश्यक है।' : 'Live weather requires an internet connection.';

  const mainCondEl = document.getElementById('weatherConditionText');
  if (mainCondEl) mainCondEl.textContent = isHi ? 'मौसम उपलब्ध नहीं है' : 'Weather unavailable';

  const windVal = document.getElementById('windValue');
  if (windVal) windVal.textContent = '--';

  const humVal = document.getElementById('humidityValue');
  if (humVal) humVal.textContent = '--';

  const visVal = document.getElementById('visibilityValue');
  if (visVal) visVal.textContent = '--';

  const rainVal = document.getElementById('rainValue');
  if (rainVal) rainVal.textContent = '--';

  const aqiVal = document.getElementById('aqiValue');
  if (aqiVal) aqiVal.textContent = '--';

  const cloudVal = document.getElementById('cloudValue');
  if (cloudVal) cloudVal.textContent = '--';

  const sprayStatus = document.getElementById('sprayStatus');
  if (sprayStatus) {
    sprayStatus.textContent = isHi ? 'उपलब्ध नहीं' : 'Unavailable';
    sprayStatus.className = 'text-lg font-bold text-slate-500';
  }
  const spraySubtext = document.getElementById('spraySubtext');
  if (spraySubtext) spraySubtext.textContent = isHi ? 'लाइव मौसम के लिए इंटरनेट कनेक्शन आवश्यक है।' : 'Live weather requires an internet connection.';

  const advIrr = document.getElementById('advIrrigation');
  if (advIrr) advIrr.textContent = isHi ? 'लाइव मौसम उपलब्ध नहीं है।' : 'Live weather data unavailable.';

  const advDis = document.getElementById('advDisease');
  if (advDis) advDis.textContent = isHi ? 'लाइव मौसम उपलब्ध नहीं है।' : 'Live weather data unavailable.';

  const advFld = document.getElementById('advField');
  if (advFld) advFld.textContent = isHi ? 'लाइव मौसम उपलब्ध नहीं है।' : 'Live weather data unavailable.';

  const forecastContainer = document.getElementById('forecastContainer');
  if (forecastContainer) {
    forecastContainer.innerHTML = `<div class="col-span-full py-6 text-center text-xs text-slate-400 font-semibold">${isHi ? 'लाइव मौसम के लिए इंटरनेट कनेक्शन आवश्यक है।' : 'Live weather requires an internet connection.'}</div>`;
  }

  const alertContainer = document.getElementById('weatherAlertContainer');
  if (alertContainer) alertContainer.innerHTML = '';

  syncFarmerContext();
  syncFertilizerContext();
}

async function loadWeatherForCurrentState(forceRefresh = false) {
  const { lat, lon } = state.location;
  if (!lat || !lon) return;

  const cacheKey = `${lat.toFixed(3)},${lon.toFixed(3)},${state.crop}`;
  const now = Date.now();
  const cacheTTL = 10 * 60 * 1000; // 10 minutes

  // Use cached data if available and fresh
  if (!forceRefresh && state.weatherCache[cacheKey] && (now - state.weatherCache[cacheKey].timestamp < cacheTTL)) {
    const cachedData = state.weatherCache[cacheKey].data;
    state.weatherData = cachedData;
    renderWeatherUI(cachedData);
    renderDashboardOverview();
    syncFarmerContext();
    syncFertilizerContext();
    return;
  }

  // If device is offline, show clear offline message without faking values
  if (typeof navigator !== 'undefined' && navigator.onLine === false) {
    renderWeatherUnavailable();
    showToast(
      state.lang === 'hi'
        ? 'लाइव मौसम की जानकारी के लिए इंटरनेट कनेक्शन आवश्यक है।'
        : 'Live weather requires an internet connection.',
      'warning'
    );
    return;
  }

  if (state.isLoadingWeather) return;
  state.isLoadingWeather = true;

  try {
    let weatherData = null;

    // 1. Try local FastAPI server if available
    if (API_BASE) {
      try {
        const res = await fetch(`${API_BASE}/api/weather?lat=${lat}&lon=${lon}&crop=${encodeURIComponent(state.crop)}`, { signal: AbortSignal.timeout(2500) });
        if (res.ok) {
          const data = await res.json();
          if (data && data.status === 'success') {
            weatherData = data;
          }
        }
      } catch (e) {
        // Fallback to direct client fetch
      }
    }

    // 2. Direct client-side fetch from OpenWeatherMap using selected coordinates
    if (!weatherData) {
      weatherData = await fetchDirectOpenWeatherMap(lat, lon, state.crop);
    }

    // 3. Fallback to Open-Meteo
    if (!weatherData) {
      weatherData = await fetchDirectOpenMeteo(lat, lon, state.crop);
    }

    if (!weatherData) {
      throw new Error('Weather service unavailable');
    }

    state.weatherData = weatherData;
    state.weatherCache[cacheKey] = { timestamp: now, data: weatherData };

    renderWeatherUI(weatherData);
    renderDashboardOverview();
    syncFarmerContext();
    syncFertilizerContext();

  } catch (err) {
    console.warn('Weather fetch notice:', err.message);
    renderWeatherUnavailable();
    showToast(
      state.lang === 'hi'
        ? 'लाइव मौसम की जानकारी के लिए इंटरनेट कनेक्शन आवश्यक है।'
        : 'Live weather requires an internet connection.',
      'warning'
    );
  } finally {
    state.isLoadingWeather = false;
  }
}

async function fetchDirectOpenWeatherMap(lat, lon, crop) {
  const OWM_KEY = 'd938b5a2fafaba32b6647319db0354de';
  const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${OWM_KEY}`;
  const forecastUrl = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${OWM_KEY}`;

  const [wRes, fRes] = await Promise.all([
    fetch(weatherUrl, { signal: AbortSignal.timeout(6000) }),
    fetch(forecastUrl, { signal: AbortSignal.timeout(6000) })
  ]);

  if (!wRes.ok) throw new Error(`Weather fetch failed (HTTP ${wRes.status})`);
  const curData = await wRes.json();
  const fData = fRes.ok ? await fRes.json() : null;

  const current = {
    temp: roundCoord(curData.main.temp),
    feels_like: roundCoord(curData.main.feels_like),
    temp_max: roundCoord(curData.main.temp_max),
    temp_min: roundCoord(curData.main.temp_min),
    humidity: curData.main.humidity,
    wind_speed: roundCoord((curData.wind.speed || 0) * 3.6),
    visibility: curData.visibility || 10000,
    clouds: curData.clouds ? curData.clouds.all : 0,
    rain_1h: (curData.rain && curData.rain['1h']) ? roundCoord(curData.rain['1h']) : 0.0,
    weather_main: curData.weather[0] ? curData.weather[0].main : 'Clear',
    weather_desc: curData.weather[0] ? curData.weather[0].description : 'Clear sky',
    weather_icon: curData.weather[0] ? curData.weather[0].icon : '01d',
    city_name: state.location.city || curData.name || 'Your Farm',
    rain_probability: 0
  };

  const forecast_daily = [];
  if (fData && fData.list) {
    const dailyMap = {};
    const todayStr = new Date().toISOString().split('T')[0];

    fData.list.forEach(item => {
      const dateStr = item.dt_txt.split(' ')[0];
      if (!dailyMap[dateStr]) dailyMap[dateStr] = [];
      dailyMap[dateStr].push(item);
    });

    const dates = Object.keys(dailyMap).sort().slice(0, 5);
    dates.forEach(dateStr => {
      const items = dailyMap[dateStr];
      const maxT = Math.max(...items.map(it => it.main.temp_max));
      const minT = Math.min(...items.map(it => it.main.temp_min));
      const maxPop = Math.max(...items.map(it => it.pop || 0));
      const mid = items[Math.floor(items.length / 2)];
      const dtObj = new Date(dateStr + 'T12:00:00');
      const isToday = (dateStr === todayStr);

      forecast_daily.push({
        date: dateStr,
        day_name: isToday ? (state.lang === 'hi' ? 'आज' : 'Today') : dtObj.toLocaleDateString(state.lang === 'hi' ? 'hi-IN' : 'en-US', { weekday: 'short' }),
        date_formatted: dtObj.toLocaleDateString(state.lang === 'hi' ? 'hi-IN' : 'en-US', { day: 'numeric', month: 'short' }),
        temp_max: Math.round(maxT),
        temp_min: Math.round(minT),
        weather_main: mid.weather[0] ? mid.weather[0].main : 'Clear',
        weather_desc: mid.weather[0] ? mid.weather[0].description : 'Clear',
        weather_icon: mid.weather[0] ? mid.weather[0].icon : '01d',
        rain_probability: Math.round(maxPop * 100)
      });
    });

    if (forecast_daily.length > 0) {
      current.rain_probability = forecast_daily[0].rain_probability;
    }
  }

  const advisories = generateLocalAgriAdvisories(current, forecast_daily, crop);
  const alerts = generateLocalWeatherAlerts(current);

  return {
    status: 'success',
    current,
    forecast: forecast_daily,
    air_quality: {
      aqi: 2,
      aqi_label: 'Moderate',
      aqi_label_hi: 'मध्यम',
      pm25: 35.0,
      pm10: 55.0
    },
    alerts,
    advisories
  };
}

async function fetchDirectOpenMeteo(lat, lon, crop) {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,cloud_cover&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto`;
  const res = await fetch(url, { signal: AbortSignal.timeout(6000) });
  if (!res.ok) throw new Error(`Open-Meteo fetch failed (HTTP ${res.status})`);
  const data = await res.json();

  const cur = data.current;
  const current = {
    temp: roundCoord(cur.temperature_2m),
    feels_like: roundCoord(cur.apparent_temperature),
    temp_max: data.daily ? roundCoord(data.daily.temperature_2m_max[0]) : roundCoord(cur.temperature_2m + 3),
    temp_min: data.daily ? roundCoord(data.daily.temperature_2m_min[0]) : roundCoord(cur.temperature_2m - 4),
    humidity: Math.round(cur.relative_humidity_2m),
    wind_speed: roundCoord(cur.wind_speed_10m),
    visibility: 10000,
    clouds: Math.round(cur.cloud_cover || 0),
    rain_1h: roundCoord(cur.precipitation || 0),
    weather_main: getWeatherDescFromWmo(cur.weather_code).main,
    weather_desc: getWeatherDescFromWmo(cur.weather_code).desc,
    weather_icon: getWeatherDescFromWmo(cur.weather_code).icon,
    city_name: state.location.city || 'Your Farm',
    rain_probability: data.daily && data.daily.precipitation_probability_max ? data.daily.precipitation_probability_max[0] : 0
  };

  const forecast_daily = [];
  if (data.daily && data.daily.time) {
    for (let i = 0; i < Math.min(5, data.daily.time.length); i++) {
      const dStr = data.daily.time[i];
      const dtObj = new Date(dStr + 'T12:00:00');
      const wInfo = getWeatherDescFromWmo(data.daily.weather_code[i]);
      forecast_daily.push({
        date: dStr,
        day_name: i === 0 ? (state.lang === 'hi' ? 'आज' : 'Today') : dtObj.toLocaleDateString(state.lang === 'hi' ? 'hi-IN' : 'en-US', { weekday: 'short' }),
        date_formatted: dtObj.toLocaleDateString(state.lang === 'hi' ? 'hi-IN' : 'en-US', { day: 'numeric', month: 'short' }),
        temp_max: Math.round(data.daily.temperature_2m_max[i]),
        temp_min: Math.round(data.daily.temperature_2m_min[i]),
        weather_main: wInfo.main,
        weather_desc: wInfo.desc,
        weather_icon: wInfo.icon,
        rain_probability: data.daily.precipitation_probability_max ? data.daily.precipitation_probability_max[i] : 0
      });
    }
  }

  const advisories = generateLocalAgriAdvisories(current, forecast_daily, crop);
  const alerts = generateLocalWeatherAlerts(current);

  return {
    status: 'success',
    current,
    forecast: forecast_daily,
    air_quality: {
      aqi: 2,
      aqi_label: 'Moderate',
      aqi_label_hi: 'मध्यम',
      pm25: 35.0,
      pm10: 55.0
    },
    alerts,
    advisories
  };
}

function generateLocalAgriAdvisories(current, forecast, crop) {
  const temp = current.temp;
  const wind = current.wind_speed;
  const rain = current.rain_1h;
  const humidity = current.humidity;
  const rainChance = (forecast && forecast[0]) ? forecast[0].rain_probability : 0;

  // Spray suitability
  const isSpraySafe = wind < 20 && rain < 1.0 && temp < 36 && rainChance < 40;
  let sprayReasonEn = 'Calm winds and low precipitation risk make spraying conditions suitable.';
  let sprayReasonHi = 'हवा की धीमी गति और वर्षा की कम संभावना के कारण छिड़काव के लिए स्थिति अनुकूल है।';

  if (wind >= 20) {
    sprayReasonEn = `Wind speed ${wind} km/h is too high. Spray drift risk.`;
    sprayReasonHi = `हवा की गति (${wind} किमी/घंटा) अधिक है। दवा उड़ने का खतरा है, छिड़काव टालें।`;
  } else if (rain >= 1.0 || rainChance >= 40) {
    sprayReasonEn = 'Rain detected or anticipated. Spraying will wash off chemicals.';
    sprayReasonHi = 'बारिश की संभावना है। छिड़काव करने से दवा धुल जाएगी, मौसम साफ होने की प्रतीक्षा करें।';
  } else if (temp >= 36) {
    sprayReasonEn = `High temperature (${temp}°C) causes rapid droplet evaporation.`;
    sprayReasonHi = `उच्च तापमान (${temp}°C) से दवा तेजी से वाष्पीकृत हो जाएगी। सुबह या शाम को छिड़काव करें।`;
  }

  // Irrigation advisory
  let irrEn = 'Maintain optimal moisture based on current crop growth stage.';
  let irrHi = 'फसल की वर्तमान अवस्था के अनुसार खेत में पर्याप्त नमी बनाए रखें।';
  if (rainChance > 50 || rain > 2.0) {
    irrEn = 'Postpone irrigation as rain is likely in the forecast.';
    irrHi = 'बारिश की संभावना को देखते हुए आगामी 1-2 दिन सिंचाई स्थगित करें।';
  } else if (temp > 34 && humidity < 45) {
    irrEn = 'High temperature and evaporation. Irrigate timely to avoid moisture stress.';
    irrHi = 'उच्च तापमान और वाष्पीकरण के कारण फसल को नमी तनाव से बचाने के लिए हल्की सिंचाई करें।';
  }

  // Disease risk
  let disEn = 'Low fungal pressure. Inspect crop canopy periodically.';
  let disHi = 'मौसम शुष्क है, फफूंद जनित रोगों का दबाव कम है। सामान्य निगरानी रखें।';
  if (humidity > 70 && temp >= 18 && temp <= 30) {
    disEn = `High humidity (${humidity}%) elevates risk of foliar blight and rust. Inspect lower leaves.`;
    disHi = `उच्च आर्द्रता (${humidity}%) के कारण पत्तियों पर झुलसा और रतुआ रोग का जोखिम बढ़ सकता है।`;
  }

  // Field operations
  let fldEn = 'Soil conditions suitable for weeding, fertilizing and intercultural operations.';
  let fldHi = 'खेत में निराई-गुड़ाई, खाद देने और सामान्य कृषि कार्यों के लिए मौसम अनुकूल है।';
  if (rain > 2.0) {
    fldEn = 'Wet soil conditions. Avoid heavy machinery in fields to prevent soil compaction.';
    fldHi = 'खेत में अधिक नमी है। मिट्टी के सख्त होने से बचने के लिए भारी ट्रैक्टर या मशीनरी न चलाएं।';
  }

  return {
    spray_suitable: isSpraySafe,
    spray_reason_en: sprayReasonEn,
    spray_reason_hi: sprayReasonHi,
    irrigation: { text_en: irrEn, text_hi: irrHi },
    disease: { text_en: disEn, text_hi: disHi },
    field: { text_en: fldEn, text_hi: fldHi }
  };
}

function generateLocalWeatherAlerts(current) {
  const alerts = [];
  const temp = current.temp;
  const wind = current.wind_speed;
  const rain = current.rain_1h;

  if (temp >= 40) {
    alerts.push({
      title_en: 'Heat Wave Warning',
      title_hi: 'लू की चेतावनी',
      desc_en: `Temperature ${temp}°C is dangerously high. Protect crops with light irrigation and mulching.`,
      desc_hi: `तापमान ${temp}°C बहुत अधिक है। मल्चिंग और हल्की सिंचाई से फसल को बचाएं।`,
      severity: 'extreme',
      icon: 'fa-temperature-arrow-up'
    });
  } else if (temp >= 37) {
    alerts.push({
      title_en: 'High Temperature Alert',
      title_hi: 'उच्च तापमान चेतावनी',
      desc_en: `Temperature ${temp}°C. Avoid midday fieldwork and ensure adequate root moisture.`,
      desc_hi: `तापमान ${temp}°C है। दोपहर में खेत में काम से बचें और जड़ों में नमी बनाए रखें।`,
      severity: 'high',
      icon: 'fa-temperature-high'
    });
  }

  if (rain >= 10) {
    alerts.push({
      title_en: 'Heavy Rainfall Warning',
      title_hi: 'भारी बारिश की चेतावनी',
      desc_en: `Rainfall rate ${rain} mm/h detected. Ensure field drainage channels are open.`,
      desc_hi: `भारी बारिश (${rain} मिमी/घंटा) दर्ज। खेत से अतिरिक्त जल निकासी की व्यवस्था करें।`,
      severity: 'high',
      icon: 'fa-cloud-showers-heavy'
    });
  }

  if (wind >= 30) {
    alerts.push({
      title_en: 'High Wind Advisory',
      title_hi: 'तेज़ हवा की चेतावनी',
      desc_en: `Wind speed ${wind} km/h. Avoid foliar chemical sprays and support tall plants.`,
      desc_hi: `तेज हवा (${wind} किमी/घंटा) चल रही है। किसी भी प्रकार का छिड़काव न करें।`,
      severity: 'high',
      icon: 'fa-wind'
    });
  }

  return alerts;
}

function getWeatherDescFromWmo(code) {
  if (code === 0) return { main: 'Clear', desc: 'Clear sky', icon: '01d' };
  if (code === 1 || code === 2) return { main: 'Partly Cloudy', desc: 'Partly cloudy', icon: '02d' };
  if (code === 3) return { main: 'Overcast', desc: 'Overcast clouds', icon: '04d' };
  if (code >= 45 && code <= 48) return { main: 'Fog', desc: 'Foggy conditions', icon: '50d' };
  if (code >= 51 && code <= 55) return { main: 'Drizzle', desc: 'Light drizzle', icon: '09d' };
  if (code >= 61 && code <= 65) return { main: 'Rain', desc: 'Rain showers', icon: '10d' };
  if (code >= 71 && code <= 77) return { main: 'Snow', desc: 'Snowfall', icon: '13d' };
  if (code >= 80 && code <= 82) return { main: 'Rain', desc: 'Heavy showers', icon: '09d' };
  if (code >= 95) return { main: 'Thunderstorm', desc: 'Thunderstorm', icon: '11d' };
  return { main: 'Clear', desc: 'Clear weather', icon: '01d' };
}

function renderWeatherUI(data) {
  if (!data || !data.current) return;

  const isHi = state.lang === 'hi';
  const c = data.current;
  const aq = data.air_quality || {};

  // Location & Date Header
  const locEl = document.getElementById('currentLocationName');
  if (locEl) {
    locEl.textContent = `${state.location.city || c.city_name || 'Your Farm'}${state.location.state ? ', ' + state.location.state : ''}`;
  }

  const dateEl = document.getElementById('currentDateText');
  if (dateEl) {
    dateEl.textContent = new Date().toLocaleDateString(
      isHi ? 'hi-IN' : 'en-US',
      { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' }
    );
  }

  // Temperature & Condition
  const tempVal = document.getElementById('tempValue');
  if (tempVal) tempVal.textContent = Math.round(c.temp);

  const feelsEl = document.getElementById('feelsLikeText');
  if (feelsEl) {
    feelsEl.textContent = isHi
      ? `महसूस होता है: ${Math.round(c.feels_like)}°C (अधिकतम: ${Math.round(c.temp_max)}° / न्यूनतम: ${Math.round(c.temp_min)}°)`
      : `Feels like: ${Math.round(c.feels_like)}°C (High: ${Math.round(c.temp_max)}° / Low: ${Math.round(c.temp_min)}°)`;
  }

  const condEl = document.getElementById('weatherConditionText');
  if (condEl) condEl.textContent = capitalize(c.weather_desc);

  // Submetrics
  const windVal = document.getElementById('windValue');
  if (windVal) windVal.textContent = `${c.wind_speed} km/h`;

  const humVal = document.getElementById('humidityValue');
  if (humVal) humVal.textContent = `${c.humidity}%`;

  const visVal = document.getElementById('visibilityValue');
  if (visVal) {
    const visKm = (c.visibility / 1000).toFixed(1);
    visVal.textContent = `${visKm} km`;
  }

  const iconContainer = document.getElementById('weatherIconContainer');
  if (iconContainer) {
    const iconClass = weatherIconMap[c.weather_icon] || 'fa-cloud-sun text-amber-300';
    iconContainer.innerHTML = `<i class="fa-solid ${iconClass}"></i>`;
  }

  // Key Metric 1: Rainfall
  const rainVal = document.getElementById('rainValue');
  if (rainVal) rainVal.textContent = c.rain_1h > 0 ? c.rain_1h : '0.0';

  // Key Metric 2: Air Quality
  const aqiVal = document.getElementById('aqiValue');
  if (aqiVal) aqiVal.textContent = aq.aqi || '--';

  const aqiBadge = document.getElementById('aqiBadge');
  if (aqiBadge) {
    aqiBadge.textContent = isHi ? aq.aqi_label_hi : aq.aqi_label;
    aqiBadge.className = `text-[10px] font-extrabold px-2 py-0.5 ml-1 rounded ${getAQIBadgeClass(aq.aqi)}`;
  }

  const aqiSub = document.getElementById('aqiSubtext');
  if (aqiSub) aqiSub.textContent = `PM2.5: ${aq.pm25} µg/m³`;

  // Key Metric 3: Cloud Cover
  const cloudVal = document.getElementById('cloudValue');
  if (cloudVal) cloudVal.textContent = `${c.clouds}%`;

  // Key Metric 4: Spraying Suitability
  const sprayStatus = document.getElementById('sprayStatus');
  const spraySubtext = document.getElementById('spraySubtext');

  if (sprayStatus && spraySubtext && data.advisories) {
    if (data.advisories.spray_suitable) {
      sprayStatus.textContent = isHi ? 'उपयुक्त (Safe)' : 'Suitable';
      sprayStatus.className = 'text-lg font-bold text-emerald-600 dark:text-emerald-400';
    } else {
      sprayStatus.textContent = isHi ? 'अनुपयुक्त (Avoid)' : 'Unsuitable';
      sprayStatus.className = 'text-lg font-bold text-rose-600 dark:text-rose-400';
    }
    spraySubtext.textContent = isHi ? data.advisories.spray_reason_hi : data.advisories.spray_reason_en;
  }

  // Render Alerts
  renderWeatherAlerts(data.alerts);

  // Agronomic Advisories
  const advCrop = document.getElementById('advisoryCropName');
  if (advCrop) advCrop.textContent = state.crop;

  if (data.advisories) {
    const adv = data.advisories;
    const irrEl = document.getElementById('advIrrigation');
    if (irrEl) irrEl.textContent = isHi ? adv.irrigation.text_hi : adv.irrigation.text_en;

    const disEl = document.getElementById('advDisease');
    if (disEl) disEl.textContent = isHi ? adv.disease.text_hi : adv.disease.text_en;

    const fldEl = document.getElementById('advField');
    if (fldEl) fldEl.textContent = isHi ? adv.field.text_hi : adv.field.text_en;
  }

  // 5-Day Forecast Grid
  renderForecastGrid(data.forecast);
}

function renderWeatherAlerts(alerts) {
  const container = document.getElementById('weatherAlertContainer');
  if (!container) return;
  container.innerHTML = '';

  const isHi = state.lang === 'hi';

  if (!alerts || alerts.length === 0) {
    const safeBanner = document.createElement('div');
    safeBanner.className = 'rounded-2xl px-4 py-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200 flex items-center justify-between text-xs font-semibold';
    safeBanner.innerHTML = `
      <div class="flex items-center space-x-2">
        <i class="fa-solid fa-circle-check text-emerald-600 dark:text-emerald-400 text-base"></i>
        <span>${isHi ? '✓ कोई गंभीर मौसम चेतावनी नहीं। कृषि कार्य सामान्य रूप से जारी रख सकते हैं।' : '✓ No major weather alerts. Farm operations can proceed normally.'}</span>
      </div>
      <span class="text-[10px] text-emerald-600 dark:text-emerald-400 uppercase font-bold tracking-wider">Live Radar Clean</span>
    `;
    container.appendChild(safeBanner);
    return;
  }

  alerts.forEach(alert => {
    const card = document.createElement('div');
    const bgClass = alert.severity === 'extreme'
      ? 'bg-rose-50 dark:bg-rose-950/50 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-200'
      : 'bg-amber-50 dark:bg-amber-950/50 border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200';

    card.className = `rounded-2xl p-4 border shadow-sm flex items-start space-x-3 transition ${bgClass}`;
    card.innerHTML = `
      <div class="text-2xl pt-0.5"><i class="fa-solid ${alert.icon || 'fa-triangle-exclamation'}"></i></div>
      <div class="flex-grow">
        <div class="flex items-center justify-between">
          <h4 class="font-bold text-sm sm:text-base">${isHi ? alert.title_hi : alert.title_en}</h4>
          <span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-black/10">${alert.severity}</span>
        </div>
        <p class="text-xs mt-0.5 leading-relaxed">${isHi ? alert.desc_hi : alert.desc_en}</p>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderForecastGrid(forecastList) {
  const container = document.getElementById('forecastContainer');
  if (!container) return;
  container.innerHTML = '';
  if (!forecastList || forecastList.length === 0) return;

  forecastList.forEach(day => {
    const iconClass = weatherIconMap[day.weather_icon] || 'fa-cloud text-slate-400';
    const card = document.createElement('div');
    card.className = 'agri-subcard p-3.5 text-center flex flex-col justify-between hover:shadow-md transition';

    card.innerHTML = `
      <div>
        <span class="text-xs font-extrabold text-slate-800 dark:text-slate-200 block">${day.day_name}</span>
        <span class="text-[10px] text-slate-400 block">${day.date_formatted}</span>
      </div>
      <div class="my-3 text-3xl filter drop-shadow-sm">
        <i class="fa-solid ${iconClass}"></i>
      </div>
      <div>
        <div class="flex items-center justify-center space-x-1.5 text-xs font-bold">
          <span class="text-slate-900 dark:text-slate-100">${Math.round(day.temp_max)}°</span>
          <span class="text-slate-400 font-normal text-[11px]">${Math.round(day.temp_min)}°</span>
        </div>
        <p class="text-[10px] text-slate-500 truncate mt-0.5">${capitalize(day.weather_desc)}</p>
        ${day.rain_probability > 0 ? `
          <div class="mt-1.5 inline-flex items-center space-x-1 text-[10px] font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/60 px-1.5 py-0.5 rounded-full">
            <i class="fa-solid fa-droplet text-[9px]"></i>
            <span>${day.rain_probability}%</span>
          </div>
        ` : `
          <div class="mt-1.5 text-[10px] text-slate-400">0% rain</div>
        `}
      </div>
    `;
    container.appendChild(card);
  });
}

function getAQIBadgeClass(aqi) {
  switch (aqi) {
    case 1: return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300';
    case 2: return 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300';
    case 3: return 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300';
    case 4: return 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300';
    case 5: return 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300';
    default: return 'bg-slate-100 text-slate-800';
  }
}

function roundCoord(val) {
  return Math.round(parseFloat(val) * 10000) / 10000;
}

function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}


// ─── Toast Notification System ────────────────────────────────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');

  const bgColors = {
    info: 'bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900',
    success: 'bg-emerald-600 text-white',
    warning: 'bg-amber-500 text-white',
    error: 'bg-rose-600 text-white',
  };

  toast.className = `${bgColors[type] || bgColors.info} px-4 py-2.5 rounded-xl shadow-xl text-xs font-bold transition-all duration-300 transform translate-y-2 opacity-0 pointer-events-auto flex items-center space-x-2`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}


// ─── SMART CROP & FERTILIZER ADVISOR ENGINE (TAB 3) ──────────────────────────

function initFertilizerTab() {
  syncFertilizerContext();

  const cropSel = document.getElementById('fertCropSelect');
  if (cropSel) cropSel.value = fertState.crop || state.crop || 'Wheat';

  const stageSel = document.getElementById('fertStageSelect');
  if (stageSel) stageSel.value = fertState.stage;

  const soilSel = document.getElementById('fertSoilSelect');
  if (soilSel) soilSel.value = fertState.soil;

  const areaInput = document.getElementById('fertAreaInput');
  if (areaInput) areaInput.value = fertState.area;

  const unitSel = document.getElementById('fertAreaUnitSelect');
  if (unitSel) unitSel.value = fertState.areaUnit;

  const irrSel = document.getElementById('fertIrrigationSelect');
  if (irrSel) irrSel.value = fertState.irrigation;
}

function syncFertilizerContext() {
  const isHi = state.lang === 'hi';
  const loc = state.location;

  const locEl = document.getElementById('fertActiveLocationText');
  if (locEl) {
    locEl.textContent = `${loc.city || 'Farm Area'}${loc.state ? ', ' + loc.state : ''}`;
  }

  const weatherEl = document.getElementById('fertActiveWeatherText');
  if (weatherEl) {
    if (state.weatherData && state.weatherData.current) {
      const c = state.weatherData.current;
      const rainChance = (state.weatherData.forecast && state.weatherData.forecast[0]) ? state.weatherData.forecast[0].rain_probability : 0;
      weatherEl.textContent = `${Math.round(c.temp)}°C · ${c.weather_main}${rainChance > 40 ? ` (${rainChance}% Rain)` : ''}`;
    } else {
      weatherEl.textContent = isHi ? 'मौसम सिंक हो रहा है...' : 'Weather Synced';
    }
  }
}

function handleFertCropChange() {
  const sel = document.getElementById('fertCropSelect');
  const customInput = document.getElementById('fertCustomCropInput');
  if (!sel || !customInput) return;

  if (sel.value === 'Other') {
    customInput.classList.remove('hidden');
    customInput.focus();
  } else {
    customInput.classList.add('hidden');
    fertState.crop = sel.value;
    localStorage.setItem('sap_fert_crop', sel.value);
  }
}

function appendFertSymptom(symptomText) {
  const textarea = document.getElementById('fertSymptomsInput');
  if (!textarea) return;

  const current = textarea.value.trim();
  if (!current) {
    textarea.value = symptomText;
  } else if (!current.includes(symptomText)) {
    textarea.value = current + "; " + symptomText;
  }
  textarea.focus();
}

function toggleSoilTestDrawer() {
  const body = document.getElementById('soilTestDrawerBody');
  const icon = document.getElementById('soilTestDrawerIcon');
  if (!body) return;

  const isHidden = body.classList.contains('hidden');
  if (isHidden) {
    body.classList.remove('hidden');
    if (icon) icon.classList.add('rotate-180');
  } else {
    body.classList.add('hidden');
    if (icon) icon.classList.remove('rotate-180');
  }
}

function handleFertImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith('image/')) {
    showToast(state.lang === 'hi' ? 'कृपया केवल फोटो फाइल अपलोड करें' : 'Please upload an image file', 'error');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      // Compress to max 1024px for quick transfer
      const canvas = document.createElement('canvas');
      let width = img.width;
      let height = img.height;
      const maxDim = 1024;

      if (width > height && width > maxDim) {
        height = Math.round((height * maxDim) / width);
        width = maxDim;
      } else if (height > maxDim) {
        width = Math.round((width * maxDim) / height);
        height = maxDim;
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);

      fertState.attachedImageBase64 = canvas.toDataURL('image/jpeg', 0.85);
      fertState.attachedImageName = file.name || 'Leaf Photo';

      const thumb = document.getElementById('fertImageThumb');
      const nameEl = document.getElementById('fertImageName');
      const strip = document.getElementById('fertImagePreviewStrip');
      const placeholder = document.getElementById('fertImageUploadPlaceholder');

      if (thumb) thumb.src = fertState.attachedImageBase64;
      if (nameEl) nameEl.textContent = `${fertState.attachedImageName} (${Math.round(fertState.attachedImageBase64.length / 1024)} KB)`;
      if (strip) strip.classList.remove('hidden');
      if (placeholder) placeholder.classList.add('hidden');

      showToast(state.lang === 'hi' ? 'पत्ती की फोटो अटैच की गई!' : 'Leaf photo attached!', 'success');
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function removeFertAttachedImage() {
  fertState.attachedImageBase64 = null;
  fertState.attachedImageName = null;

  const fileInput = document.getElementById('fertLeafImageInput');
  if (fileInput) fileInput.value = '';

  const strip = document.getElementById('fertImagePreviewStrip');
  const placeholder = document.getElementById('fertImageUploadPlaceholder');

  if (strip) strip.classList.add('hidden');
  if (placeholder) placeholder.classList.remove('hidden');
}

function resetFertilizerForm() {
  const form = document.getElementById('fertilizerForm');
  if (form) form.reset();

  removeFertAttachedImage();

  const customInput = document.getElementById('fertCustomCropInput');
  if (customInput) customInput.classList.add('hidden');

  const resContainer = document.getElementById('fertilizerResultContainer');
  if (resContainer) resContainer.classList.add('hidden');

  initFertilizerTab();
  showToast(state.lang === 'hi' ? 'फॉर्म रीसेट किया गया' : 'Form reset to defaults', 'info');
}

function sendFertilizerQuickPrompt(promptType) {
  const cropSel = document.getElementById('fertCropSelect');
  const stageSel = document.getElementById('fertStageSelect');
  const symptomInput = document.getElementById('fertSymptomsInput');

  if (promptType === 'wheat_npk') {
    if (cropSel) cropSel.value = 'Wheat';
    if (stageSel) stageSel.value = 'Vegetative';
    if (symptomInput) symptomInput.value = 'Provide complete stage-wise NPK schedule for wheat, including basal and top dressing timing.';
  } else if (promptType === 'rice_topdress') {
    if (cropSel) cropSel.value = 'Rice';
    if (stageSel) stageSel.value = 'Vegetative';
    if (symptomInput) symptomInput.value = 'When and how should I apply urea top-dressing and zinc in paddy / rice crop?';
  } else if (promptType === 'yellow_leaves') {
    if (symptomInput) symptomInput.value = 'Lower leaves are turning pale yellow starting from the leaf tips. What nutrient deficiency is this and how to treat it?';
  } else if (promptType === 'rain_check') {
    if (symptomInput) symptomInput.value = 'Rainfall is expected soon. Is it safe to broadcast urea or water-soluble fertilizer right now?';
  } else if (promptType === 'potato_potash') {
    if (cropSel) cropSel.value = 'Potato';
    if (stageSel) stageSel.value = 'Fruit/Grain Formation';
    if (symptomInput) symptomInput.value = 'What is the potassium (MOP / SOP) requirement for potato tuber enlargement and quality?';
  } else if (promptType === 'organic_fym') {
    if (symptomInput) symptomInput.value = 'What organic manures (FYM, Vermicompost, Bio-fertilizers) should I apply for balanced soil health?';
  }

  handleFertilizerSubmit(new Event('submit'));
}

async function handleFertilizerSubmit(event) {
  if (event) event.preventDefault();

  if (fertState.isLoading) return;

  const cropSel = document.getElementById('fertCropSelect');
  const customCrop = document.getElementById('fertCustomCropInput');
  const stageSel = document.getElementById('fertStageSelect');
  const soilSel = document.getElementById('fertSoilSelect');
  const areaInput = document.getElementById('fertAreaInput');
  const unitSel = document.getElementById('fertAreaUnitSelect');
  const irrSel = document.getElementById('fertIrrigationSelect');
  const symptomsInput = document.getElementById('fertSymptomsInput');

  let targetCrop = cropSel ? cropSel.value : 'Wheat';
  if (targetCrop === 'Other' && customCrop && customCrop.value.trim()) {
    targetCrop = customCrop.value.trim();
  }

  const payload = {
    crop: targetCrop,
    cropStage: stageSel ? stageSel.value : 'Vegetative',
    soilType: soilSel ? soilSel.value : 'Alluvial / Loam Soil',
    area: areaInput ? areaInput.value : '2',
    areaUnit: unitSel ? unitSel.value : 'acre',
    irrigation: irrSel ? irrSel.value : 'Tube Well / Borewell',
    soilTest: {
      ph: document.getElementById('fertSoilPh')?.value.trim() || '',
      nitrogen: document.getElementById('fertSoilN')?.value.trim() || '',
      phosphorus: document.getElementById('fertSoilP')?.value.trim() || '',
      potassium: document.getElementById('fertSoilK')?.value.trim() || '',
      organic_carbon: document.getElementById('fertSoilOC')?.value.trim() || '',
    },
    symptoms: symptomsInput ? symptomsInput.value.trim() : '',
    image: fertState.attachedImageBase64,
    location: state.location,
    weather: state.weatherData,
    lang: state.lang,
  };

  // Save preferences
  localStorage.setItem('sap_fert_crop', targetCrop);
  localStorage.setItem('sap_fert_stage', payload.cropStage);
  localStorage.setItem('sap_fert_soil', payload.soilType);
  localStorage.setItem('sap_fert_area', payload.area);
  localStorage.setItem('sap_fert_unit', payload.areaUnit);
  localStorage.setItem('sap_fert_irrigation', payload.irrigation);

  // Show loading indicator
  fertState.isLoading = true;
  const loader = document.getElementById('fertLoader');
  const resContainer = document.getElementById('fertilizerResultContainer');
  const submitBtn = document.getElementById('fertSubmitBtn');

  if (loader) loader.classList.remove('hidden');
  if (resContainer) resContainer.classList.add('hidden');
  if (submitBtn) submitBtn.disabled = true;

  try {
    const response = await fetch(`${API_BASE}/api/fertilizer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    if (data.status !== 'success' || !data.recommendation) {
      throw new Error(data.message || 'Unable to generate recommendation');
    }

    renderFertilizerResult(data);
    showToast(state.lang === 'hi' ? 'उर्वरक एवं फसल पोषण सलाह तैयार!' : 'Fertilizer & Crop Nutrition Advice Ready!', 'success');
  } catch (err) {
    console.error("Fertilizer Advisor Error:", err);
    showToast(
      state.lang === 'hi'
        ? `सलाह तैयार करने में समस्या: ${err.message}`
        : `Advisor Notice: ${err.message}`,
      'error'
    );
  } finally {
    fertState.isLoading = false;
    if (loader) loader.classList.add('hidden');
    if (submitBtn) submitBtn.disabled = false;
  }
}

function renderFertilizerResult(data) {
  const resContainer = document.getElementById('fertilizerResultContainer');
  if (!resContainer) return;

  const rec = data.recommendation;
  fertState.lastRecommendation = rec;
  const isHi = state.lang === 'hi';

  // Badges
  const cropBadge = document.getElementById('fertResultCropBadge');
  if (cropBadge) cropBadge.textContent = `🌾 ${isHi ? 'फसल:' : 'Crop:'} ${data.crop}`;

  const stageBadge = document.getElementById('fertResultStageBadge');
  if (stageBadge) stageBadge.textContent = `🌿 ${isHi ? 'अवस्था:' : 'Stage:'} ${data.cropStage}`;

  const soilBadge = document.getElementById('fertResultSoilBadge');
  if (soilBadge) soilBadge.textContent = `🧱 ${data.soilType}`;

  // Confidence Badge
  const confBadge = document.getElementById('fertConfidenceBadge');
  if (confBadge) confBadge.textContent = `${rec.confidence || 'Calibrated'} (${data.engine || 'AI Kisan'})`;

  // Summary Text
  const summaryEl = document.getElementById('fertSummaryText');
  if (summaryEl) summaryEl.textContent = rec.summary;

  // Issue / Deficiency Text
  const issueEl = document.getElementById('fertIssueText');
  if (issueEl) issueEl.textContent = rec.possible_issue || 'Balanced nutrient maintenance schedule.';

  // Disease Alert Box
  const disAlert = document.getElementById('fertDiseaseAlert');
  if (disAlert) {
    if (rec.is_disease_suspected) {
      disAlert.classList.remove('hidden');
    } else {
      disAlert.classList.add('hidden');
    }
  }

  // Key Nutrient Focus Tags
  const focusContainer = document.getElementById('fertNutrientFocusContainer');
  if (focusContainer && rec.nutrient_focus) {
    focusContainer.innerHTML = rec.nutrient_focus.map(n => `
      <span class="bg-emerald-50 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-200 border border-emerald-300 dark:border-emerald-800 text-xs font-extrabold px-3 py-1.5 rounded-2xl flex items-center space-x-1.5 shadow-sm">
        <i class="fa-solid fa-circle-check text-emerald-600 dark:text-emerald-400 text-[10px]"></i>
        <span>${escapeHTML(n)}</span>
      </span>
    `).join('');
  }

  // Recommended Fertilizer Options Grid
  const catContainer = document.getElementById('fertCategoriesContainer');
  if (catContainer && rec.fertilizer_categories) {
    catContainer.innerHTML = rec.fertilizer_categories.map(cat => `
      <div class="bg-slate-50 dark:bg-slate-800/80 p-4 sm:p-5 rounded-2xl border border-slate-200 dark:border-slate-700/80 space-y-2 hover:shadow-md transition">
        <div class="flex items-center justify-between">
          <h5 class="font-extrabold text-slate-900 dark:text-slate-100 text-sm sm:text-base flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
            <span>${escapeHTML(cat.name)}</span>
          </h5>
          <span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
            ${escapeHTML(cat.type || 'Standard')}
          </span>
        </div>
        <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
          <strong class="text-slate-800 dark:text-slate-200">${isHi ? 'उद्देश्य:' : 'Purpose:'}</strong> ${escapeHTML(cat.purpose)}
        </p>
        <div class="bg-white dark:bg-slate-900 p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-[11px] text-emerald-800 dark:text-emerald-300 font-semibold leading-relaxed">
          <i class="fa-solid fa-circle-info mr-1 text-emerald-600"></i>
          <span>${escapeHTML(cat.guideline)}</span>
        </div>
      </div>
    `).join('');
  }

  // Timing
  const timingEl = document.getElementById('fertTimingText');
  if (timingEl) timingEl.textContent = rec.application_timing || 'Apply when soil has adequate moisture.';

  // Weather Advice
  const weatherEl = document.getElementById('fertWeatherAdviceText');
  if (weatherEl) weatherEl.textContent = rec.weather_advice || 'Weather conditions are currently normal.';

  // Organic Alternatives
  const organicContainer = document.getElementById('fertOrganicContainer');
  if (organicContainer && rec.organic_options) {
    organicContainer.innerHTML = rec.organic_options.map(org => `
      <div class="flex items-start space-x-2">
        <i class="fa-solid fa-leaf text-teal-600 dark:text-teal-400 text-xs mt-0.5 flex-shrink-0"></i>
        <span>${escapeHTML(org)}</span>
      </div>
    `).join('');
  }

  // Precautions
  const precContainer = document.getElementById('fertPrecautionsContainer');
  if (precContainer && rec.precautions) {
    precContainer.innerHTML = rec.precautions.map(p => `
      <div class="flex items-start space-x-2">
        <i class="fa-solid fa-check text-amber-700 dark:text-amber-400 text-xs mt-0.5 flex-shrink-0"></i>
        <span>${escapeHTML(p)}</span>
      </div>
    `).join('');
  }

  resContainer.classList.remove('hidden');
  resContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function askBotAboutFertilizer() {
  if (!fertState.lastRecommendation) return;

  const cropSel = document.getElementById('fertCropSelect');
  const stageSel = document.getElementById('fertStageSelect');
  const crop = cropSel ? cropSel.value : 'Wheat';
  const stage = stageSel ? stageSel.value : 'Vegetative';
  const isHi = state.lang === 'hi';

  const prompt = isHi
    ? `मुझे मेरी ${crop} की फसल (${stage} अवस्था) के लिए उर्वरक सलाह प्राप्त हुई है। क्या आप मुझे इस संबंध में और विस्तार से समझा सकते हैं?`
    : `I received a fertilizer recommendation for my ${crop} crop (${stage} stage). Can you provide more practical tips and guidance on this?`;

  switchTab('bot');

  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.value = prompt;
    handleChatSubmit(new Event('submit'));
  }
}


// ══════════════════════════════════════════════════════════════════════════════
// MANDI PRICES ENGINE (TAB 4)
// ══════════════════════════════════════════════════════════════════════════════

function initMandiTab() {
  syncMandiContext();

  // Sync commodity pill UI
  document.querySelectorAll('.mandi-comm-pill').forEach(pill => {
    if (pill.getAttribute('data-commodity') === mandiState.commodity) {
      pill.className = 'mandi-comm-pill active bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-full whitespace-nowrap shadow-sm transition flex items-center space-x-1.5 flex-shrink-0';
    } else {
      pill.className = 'mandi-comm-pill bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs font-bold px-4 py-2 rounded-full whitespace-nowrap shadow-sm transition flex items-center space-x-1.5 flex-shrink-0';
    }
  });

  const radiusSel = document.getElementById('mandiRadiusSelect');
  if (radiusSel) radiusSel.value = mandiState.radius;

  const sortSel = document.getElementById('mandiSortSelect');
  if (sortSel) sortSel.value = mandiState.sortBy;

  fetchMandiPrices();
}

function syncMandiContext() {
  const loc = state.location;
  const pillText = document.getElementById('mandiLocationPillText');
  if (pillText) {
    const locName = loc.city || loc.district || 'Kanpur';
    const stateName = loc.state ? `, ${loc.state}` : ', UP';
    const radText = mandiState.radius === 'all' ? 'All India' : `${mandiState.radius} km Radius`;
    pillText.textContent = `${locName}${stateName} · ${radText}`;
  }
}

function setMandiCommodity(commodity) {
  mandiState.commodity = commodity;
  localStorage.setItem('sap_mandi_commodity', commodity);

  document.querySelectorAll('.mandi-comm-pill').forEach(pill => {
    if (pill.getAttribute('data-commodity') === commodity) {
      pill.className = 'mandi-comm-pill active bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-full whitespace-nowrap shadow-sm transition flex items-center space-x-1.5 flex-shrink-0';
    } else {
      pill.className = 'mandi-comm-pill bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs font-bold px-4 py-2 rounded-full whitespace-nowrap shadow-sm transition flex items-center space-x-1.5 flex-shrink-0';
    }
  });

  const searchInput = document.getElementById('mandiSearchInput');
  if (searchInput) searchInput.value = '';
  mandiState.searchQuery = '';

  fetchMandiPrices();
}

function handleMandiRadiusChange() {
  const sel = document.getElementById('mandiRadiusSelect');
  if (sel) {
    mandiState.radius = sel.value;
    localStorage.setItem('sap_mandi_radius', sel.value);
    syncMandiContext();
    fetchMandiPrices();
  }
}

function handleMandiSortChange() {
  const sel = document.getElementById('mandiSortSelect');
  if (sel) {
    mandiState.sortBy = sel.value;
    if (mandiState.data && mandiState.data.results) {
      renderMandiResults(mandiState.data);
    }
  }
}

function handleMandiSearchKeyup(event) {
  if (event.key === 'Enter') {
    const input = document.getElementById('mandiSearchInput');
    if (input) {
      const q = input.value.trim();
      if (q) {
        mandiState.commodity = q;
      }
      fetchMandiPrices();
    }
  }
}

async function fetchMandiPrices() {
  const grid = document.getElementById('mandiCardsGrid');
  const isHi = state.lang === 'hi';

  if (grid) {
    grid.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-400 text-xs">
        <i class="fa-solid fa-spinner fa-spin text-2xl mb-2 text-blue-500"></i>
        <p>${isHi ? 'ताजा मंडी भाव लोड हो रहे हैं...' : 'Loading real-time mandi prices...'}</p>
      </div>
    `;
  }

  const payload = {
    commodity: mandiState.commodity || state.crop || 'Wheat',
    state: state.location.state || 'Uttar Pradesh',
    district: state.location.district || state.location.city || 'Kanpur Nagar',
    lat: state.location.lat || 26.4499,
    lon: state.location.lon || 80.3319,
    radius: mandiState.radius || 50
  };

  try {
    mandiState.isLoading = true;
    const resp = await fetch(`${API_BASE}/api/mandi`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    mandiState.data = data;
    renderMandiResults(data);
    renderDashboardOverview();
  } catch (err) {
    console.error('[!] Error fetching mandi rates:', err);
    if (grid) {
      grid.innerHTML = `
        <div class="col-span-full py-8 text-center bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 rounded-3xl p-6 text-xs text-red-600 dark:text-red-300 space-y-2">
          <i class="fa-solid fa-circle-exclamation text-2xl"></i>
          <p class="font-bold">${isHi ? 'मंडी भाव प्राप्त करने में असमर्थ' : 'Mandi prices temporarily unavailable'}</p>
          <p class="text-[11px] text-red-500">${isHi ? 'कृपया अपना इंटरनेट कनेक्शन जांचें या पुनः प्रयास करें।' : 'Please check your connection and try again.'}</p>
          <button onclick="fetchMandiPrices()" class="mt-2 bg-red-600 text-white font-bold px-4 py-1.5 rounded-xl shadow-sm hover:bg-red-700 transition">
            ${isHi ? 'पुनः प्रयास करें' : 'Try Again'}
          </button>
        </div>
      `;
    }
  } finally {
    mandiState.isLoading = false;
  }
}

function renderMandiResults(data) {
  if (!data || !data.results) return;

  const isHi = state.lang === 'hi';
  let results = [...data.results];

  // Apply sorting
  if (mandiState.sortBy === 'highest_price') {
    results.sort((a, b) => b.modal_price - a.modal_price);
  } else if (mandiState.sortBy === 'lowest_price') {
    results.sort((a, b) => a.modal_price - b.modal_price);
  } else {
    // Default: distance
    results.sort((a, b) => a.distance_km - b.distance_km);
  }

  // 1. Render KPIs & Insights
  const ins = data.insights || {};
  const highestPriceEl = document.getElementById('kpiHighestPrice');
  if (highestPriceEl) highestPriceEl.textContent = ins.highest_price ? `₹${ins.highest_price.toLocaleString('en-IN')} / qtl` : '₹-- / qtl';

  const highestMarketEl = document.getElementById('kpiHighestMarket');
  if (highestMarketEl) highestMarketEl.textContent = ins.highest_market || '--';

  const spreadEl = document.getElementById('kpiPriceSpread');
  if (spreadEl) spreadEl.textContent = ins.spread ? `₹${ins.spread.toLocaleString('en-IN')} / qtl` : '₹-- / qtl';

  const trendStatusEl = document.getElementById('kpiTrendStatus');
  if (trendStatusEl) {
    const commPct = results[0] ? results[0].trend_pct : 0;
    if (commPct > 0) {
      trendStatusEl.innerHTML = `<span class="text-emerald-600 dark:text-emerald-400 font-black">+${commPct}% ▲</span>`;
    } else if (commPct < 0) {
      trendStatusEl.innerHTML = `<span class="text-rose-600 dark:text-rose-400 font-black">${commPct}% ▼</span>`;
    } else {
      trendStatusEl.textContent = isHi ? 'स्थिर (Steady)' : 'Steady';
    }
  }

  const mspNoteEl = document.getElementById('kpiMspNote');
  if (mspNoteEl) {
    const msp = results[0] ? results[0].msp : null;
    mspNoteEl.textContent = msp ? `Govt MSP: ₹${msp.toLocaleString('en-IN')}/qtl` : (isHi ? 'बाजार आधारित मूल्य' : 'Market-determined price');
  }

  const advTextEl = document.getElementById('mandiAdvisoryText');
  if (advTextEl && ins.advisory) advTextEl.textContent = ins.advisory;

  // 2. Render Leaderboard
  const leaderList = document.getElementById('mandiLeaderboardList');
  const leaderCount = document.getElementById('mandiLeaderboardCount');
  if (leaderCount) leaderCount.textContent = `${results.length} mandis compared`;

  if (leaderList) {
    if (results.length === 0) {
      leaderList.innerHTML = `<div class="text-center py-3 text-xs text-slate-400">${isHi ? 'कोई निकटवर्ती मंडी नहीं मिली।' : 'No nearby mandis found within selected radius.'}</div>`;
    } else {
      const maxPrice = Math.max(...results.map(r => r.modal_price));
      const minPrice = Math.min(...results.map(r => r.modal_price));

      leaderList.innerHTML = results.slice(0, 5).map(m => {
        const isHighest = (m.modal_price === maxPrice && results.length > 1);
        const barWidth = Math.max(20, Math.min(100, ((m.modal_price / maxPrice) * 100)));

        return `
          <div class="p-2.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 hover:bg-blue-50/50 dark:hover:bg-blue-950/20 transition flex items-center justify-between gap-3 text-xs">
            <div class="w-2/5 min-w-[140px]">
              <div class="font-extrabold text-slate-900 dark:text-slate-100 truncate flex items-center space-x-1.5">
                <span>${escapeHTML(m.market)}</span>
                ${isHighest ? `<span class="bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 font-black text-[9px] px-2 py-0.5 rounded-full border border-amber-400/30">Highest Reported</span>` : ''}
              </div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 flex items-center space-x-2">
                <span>${escapeHTML(m.district)}</span>
                <span>•</span>
                <span class="text-blue-600 dark:text-blue-400 font-semibold">📍 ${m.distance_km} km</span>
              </div>
            </div>
            
            <div class="w-1/3 hidden sm:block">
              <div class="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                <div class="h-full ${isHighest ? 'bg-gradient-to-r from-amber-500 to-emerald-500' : 'bg-blue-500'}" style="width: ${barWidth}%"></div>
              </div>
            </div>

            <div class="text-right flex-shrink-0">
              <div class="font-black text-sm text-slate-900 dark:text-slate-100">
                ₹${m.modal_price.toLocaleString('en-IN')}
                <span class="text-[10px] font-normal text-slate-500">/qtl</span>
              </div>
              <div class="text-[10px] text-slate-400">
                Min ₹${m.min_price} · Max ₹${m.max_price}
              </div>
            </div>
          </div>
        `;
      }).join('');
    }
  }

  // 3. Render Detailed Cards Grid
  const cardsGrid = document.getElementById('mandiCardsGrid');
  const cardsCount = document.getElementById('mandiCardsCount');
  if (cardsCount) cardsCount.textContent = `${results.length} markets reported`;

  if (cardsGrid) {
    if (results.length === 0) {
      cardsGrid.innerHTML = `
        <div class="col-span-full py-12 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 text-xs text-slate-500 space-y-3">
          <i class="fa-solid fa-store-slash text-3xl text-slate-400"></i>
          <p class="font-bold text-slate-700 dark:text-slate-300">${isHi ? 'इस फसल / दायरे के लिए कोई मंडी भाव नहीं मिला।' : 'No current mandi price was found for this commodity/location.'}</p>
          <p class="text-[11px] text-slate-400">${isHi ? 'कृपया खोज दायरा (Radius) बढ़ाएं या अन्य फसल चुनें।' : 'Try expanding the search radius or selecting another nearby commodity.'}</p>
          <button onclick="setMandiCommodity('Wheat')" class="bg-blue-600 text-white font-bold px-4 py-2 rounded-xl shadow transition">
            ${isHi ? 'गेहूं के भाव देखें' : 'View Wheat Prices'}
          </button>
        </div>
      `;
    } else {
      cardsGrid.innerHTML = results.map(m => {
        // Build 7-day sparkline dots
        const historyDots = (m.history_7d || []).map((h, i) => `
          <div class="flex flex-col items-center space-y-1">
            <span class="text-[9px] font-bold text-slate-700 dark:text-slate-300">₹${h.price}</span>
            <div class="w-2.5 h-2.5 rounded-full ${i === m.history_7d.length - 1 ? 'bg-blue-600 ring-2 ring-blue-300' : 'bg-slate-300 dark:bg-slate-600'}"></div>
            <span class="text-[8px] text-slate-400 whitespace-nowrap">${h.date}</span>
          </div>
        `).join('');

        const isUp = (m.trend === 'up');
        const isDown = (m.trend === 'down');
        const trendBadgeClass = isUp ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300' : (isDown ? 'bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300');
        const trendIcon = isUp ? 'fa-arrow-trend-up' : (isDown ? 'fa-arrow-trend-down' : 'fa-minus');

        return `
          <div class="agri-card p-5 space-y-4 flex flex-col justify-between">
            <div class="space-y-3">
              <!-- Top Row: Market Name & Distance -->
              <div class="flex items-start justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                <div>
                  <span class="badge-blue uppercase tracking-wider">
                    ${escapeHTML(m.type || 'APMC Yard')}
                  </span>
                  <h4 class="text-base font-black text-slate-900 dark:text-slate-100 mt-1">
                    ${escapeHTML(m.market)}
                  </h4>
                  <p class="text-xs text-slate-500 flex items-center space-x-1.5 mt-0.5">
                    <i class="fa-solid fa-location-dot text-emerald-500"></i>
                    <span>${escapeHTML(m.district)}, ${escapeHTML(m.state)}</span>
                  </p>
                </div>
                <div class="agri-subcard px-2.5 py-1 text-xs font-extrabold flex-shrink-0 flex items-center space-x-1">
                  <i class="fa-solid fa-route text-blue-500"></i>
                  <span>${m.distance_km} km</span>
                </div>
              </div>

              <!-- Main Modal Price Display -->
              <div class="agri-subcard p-4 flex items-center justify-between">
                <div>
                  <div class="text-[10px] font-bold text-slate-500 uppercase" data-lang-en="Modal / Average Rate" data-lang-hi="मॉडल / औसत भाव">Modal / Average Rate</div>
                  <div class="text-2xl font-black text-slate-900 dark:text-white">
                    ₹${m.modal_price.toLocaleString('en-IN')}
                    <span class="text-xs font-semibold text-slate-500">/ quintal</span>
                  </div>
                  <div class="text-[11px] text-slate-500 mt-0.5">
                    Variety: <strong class="text-slate-700 dark:text-slate-300">${escapeHTML(m.variety)}</strong>
                  </div>
                </div>
                <div class="${trendBadgeClass} text-xs font-black px-3 py-1.5 rounded-xl flex items-center space-x-1">
                  <i class="fa-solid ${trendIcon}"></i>
                  <span>${isUp ? `+${m.trend_pct}%` : (isDown ? `${m.trend_pct}%` : 'Stable')}</span>
                </div>
              </div>

              <!-- Min, Max, and Arrival Grid -->
              <div class="grid grid-cols-3 gap-2 text-center text-xs">
                <div class="agri-subcard p-2">
                  <div class="text-[10px] text-slate-400">Min Rate</div>
                  <div class="font-bold text-slate-800 dark:text-slate-200 mt-0.5">₹${m.min_price}</div>
                </div>
                <div class="agri-subcard p-2">
                  <div class="text-[10px] text-slate-400">Max Rate</div>
                  <div class="font-bold text-slate-800 dark:text-slate-200 mt-0.5">₹${m.max_price}</div>
                </div>
                <div class="agri-subcard p-2">
                  <div class="text-[10px] text-slate-400">Daily Arrival</div>
                  <div class="font-bold text-slate-800 dark:text-slate-200 mt-0.5">${escapeHTML(m.arrival_quantity)}</div>
                </div>
              </div>

              <!-- 7-Day History Sparkline -->
              <div class="space-y-1 pt-1">
                <div class="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center justify-between">
                  <span>7-Day Price History</span>
                  <span class="text-blue-500">₹/quintal</span>
                </div>
                <div class="agri-subcard p-2.5 flex items-center justify-between overflow-x-auto">
                  ${historyDots}
                </div>
              </div>
            </div>

            <!-- Footer: Source, Date & Action -->
            <div class="border-t border-slate-100 dark:border-slate-800 pt-3 flex items-center justify-between gap-2 text-[10px] text-slate-400">
              <span class="flex items-center space-x-1 truncate max-w-[150px]">
                <i class="fa-solid fa-clock-rotate-left"></i>
                <span>Updated: ${m.date}</span>
              </span>
              <button onclick="openMandiDetailModal('${escapeAttribute(m.market)}')" class="bg-blue-50 dark:bg-blue-950/80 hover:bg-blue-100 text-blue-700 dark:text-blue-300 font-extrabold text-[11px] px-3 py-1.5 rounded-xl border border-blue-200 dark:border-blue-800 transition flex items-center space-x-1">
                <span>View Details & Freight</span>
                <i class="fa-solid fa-arrow-right text-[9px]"></i>
              </button>
            </div>
          </div>
        `;
      }).join('');
    }
  }
}

let selectedMandiMarket = null;

function openMandiDetailModal(marketName) {
  const results = (mandiState.data && mandiState.data.results) ? mandiState.data.results : [];
  const market = results.find(m => m.market === marketName) || results[0];
  if (!market) return;

  selectedMandiMarket = market;

  const titleEl = document.getElementById('modalMandiTitle');
  if (titleEl) titleEl.textContent = market.market;

  const subEl = document.getElementById('modalMandiSubtitle');
  if (subEl) subEl.textContent = `${market.district}, ${market.state}`;

  const typeBadge = document.getElementById('modalMandiTypeBadge');
  if (typeBadge) typeBadge.textContent = market.type || 'APMC Yard';

  const distBadge = document.getElementById('modalMandiDistanceBadge');
  if (distBadge) distBadge.textContent = `📍 ${market.distance_km} km`;

  const priceEl = document.getElementById('modalMandiPrice');
  if (priceEl) priceEl.innerHTML = `₹${market.modal_price.toLocaleString('en-IN')} <span class="text-xs font-semibold text-slate-500">/ quintal</span>`;

  const varietyEl = document.getElementById('modalMandiVariety');
  if (varietyEl) varietyEl.innerHTML = `Variety: <strong class="text-slate-700 dark:text-slate-300">${escapeHTML(market.variety)}</strong>`;

  const minEl = document.getElementById('modalMandiMinPrice');
  if (minEl) minEl.textContent = `₹${market.min_price}`;

  const maxEl = document.getElementById('modalMandiMaxPrice');
  if (maxEl) maxEl.textContent = `₹${market.max_price}`;

  const arrEl = document.getElementById('modalMandiArrival');
  if (arrEl) arrEl.textContent = market.arrival_quantity;

  const trendEl = document.getElementById('modalMandiTrendBadge');
  if (trendEl) {
    const isUp = (market.trend === 'up');
    const isDown = (market.trend === 'down');
    trendEl.className = isUp ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 text-xs font-black px-3 py-1.5 rounded-xl' : (isDown ? 'bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 text-xs font-black px-3 py-1.5 rounded-xl' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-black px-3 py-1.5 rounded-xl');
    trendEl.textContent = isUp ? `+${market.trend_pct}% ▲` : (isDown ? `${market.trend_pct}% ▼` : 'Steady');
  }

  const distInput = document.getElementById('mandiCalcDistance');
  if (distInput) distInput.value = Math.max(5, Math.round(market.distance_km));

  recalculateMandiTransport();

  const modal = document.getElementById('mandiDetailModal');
  if (modal) modal.classList.remove('hidden');
}

function closeMandiDetailModal() {
  const modal = document.getElementById('mandiDetailModal');
  if (modal) modal.classList.add('hidden');
}

function recalculateMandiTransport() {
  if (!selectedMandiMarket) return;

  const distInput = document.getElementById('mandiCalcDistance');
  const qtyInput = document.getElementById('mandiCalcQuantity');

  const dist = parseFloat(distInput ? distInput.value : 15) || 15;
  const qty = parseFloat(qtyInput ? qtyInput.value : 20) || 20;
  const rate = selectedMandiMarket.modal_price || 2300;

  const grossVal = Math.round(rate * qty);
  const freight = Math.round(dist * 3.5 * qty);
  const cess = Math.round(grossVal * 0.015);
  const netVal = Math.max(0, grossVal - freight - cess);
  const netPerQtl = qty > 0 ? Math.round(netVal / qty) : rate;

  const grossEl = document.getElementById('mandiCalcGross');
  if (grossEl) grossEl.textContent = `₹${grossVal.toLocaleString('en-IN')}`;

  const freightEl = document.getElementById('mandiCalcFreight');
  if (freightEl) freightEl.textContent = `-₹${freight.toLocaleString('en-IN')}`;

  const cessEl = document.getElementById('mandiCalcCess');
  if (cessEl) cessEl.textContent = `-₹${cess.toLocaleString('en-IN')}`;

  const netEl = document.getElementById('mandiCalcNet');
  if (netEl) netEl.textContent = `₹${netVal.toLocaleString('en-IN')} (₹${netPerQtl.toLocaleString('en-IN')}/qtl)`;
}

function askBotAboutSpecificMandi() {
  if (!selectedMandiMarket) return;
  const m = selectedMandiMarket;
  const isHi = state.lang === 'hi';
  closeMandiDetailModal();

  const prompt = isHi
    ? `मुझे ${m.market} (${m.district}) में ${mandiState.commodity || 'फसल'} बेचने के लिए क्या प्रक्रिया और सुझाव देंगे? आज का भाव ₹${m.modal_price}/क्विंटल है।`
    : `What advice do you have for selling my ${mandiState.commodity || 'crop'} at ${m.market} (${m.district})? The current modal rate is ₹${m.modal_price}/quintal.`;

  switchTab('bot');

  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.value = prompt;
    handleChatSubmit(new Event('submit'));
  }
}

function askBotAboutMandi() {
  const comm = mandiState.commodity || 'Wheat';
  const loc = state.location.city || 'Kanpur';
  const isHi = state.lang === 'hi';

  const prompt = isHi
    ? `आज ${loc} और आसपास की मंडियों में ${comm} का क्या भाव चल रहा है? मुझे फसल बेचने के लिए क्या सलाह देंगे?`
    : `What are current mandi rates and trends for ${comm} in and around ${loc}? When is the best time to sell?`;

  switchTab('bot');

  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.value = prompt;
    handleChatSubmit(new Event('submit'));
  }
}

function handleCropSelectionChange() {
  const cropSelect = document.getElementById('diseaseCropSelect');
  if (cropSelect) {
    const val = cropSelect.value;
    if (val !== 'Auto') {
      state.crop = val;
      localStorage.setItem('sap_crop', val);
    }
    updateDiseaseModelBadge(val);
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
      updateDiseaseModelBadge(cropSelect.value);
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
}


// ─── AI Disease Scanner Frontend Engine (Tab 2) ──────────────────────────────
let selectedImageBase64 = null;
let cameraStream = null;
let cameraFacing = 'environment';

function triggerFileInput() {
  const input = document.getElementById('diseaseImageInput');
  if (input) input.click();
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  processSelectedFile(file);
}

function processSelectedFile(file) {
  if (!file.type.startsWith('image/')) {
    showToast(state.lang === 'hi' ? 'कृपया केवल फोटो फाइल अपलोड करें' : 'Please upload a valid image file', 'error');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    selectedImageBase64 = e.target.result;

    const leafImg = document.getElementById('leafImagePreview');
    const scanningImg = document.getElementById('scanningImageCopy');
    const fileNameEl = document.getElementById('previewFileName');

    if (leafImg) leafImg.src = selectedImageBase64;
    if (scanningImg) scanningImg.src = selectedImageBase64;
    if (fileNameEl) fileNameEl.innerText = file.name || 'Captured Leaf Photo';

    const prevCard = document.getElementById('diseasePreviewCard');
    if (prevCard) prevCard.classList.remove('hidden');
    const resCard = document.getElementById('diseaseResultContainer');
    if (resCard) resCard.classList.add('hidden');
    const loader = document.getElementById('scanningLoader');
    if (loader) loader.classList.add('hidden');

    showToast(state.lang === 'hi' ? 'फोटो चयन सफल! अब जांच बटन दबाएं' : 'Image loaded! Click Diagnose to scan.', 'success');
  };
  reader.readAsDataURL(file);
}

function clearSelectedImage() {
  selectedImageBase64 = null;
  const input = document.getElementById('diseaseImageInput');
  if (input) input.value = '';

  const prevCard = document.getElementById('diseasePreviewCard');
  if (prevCard) prevCard.classList.add('hidden');
  const resCard = document.getElementById('diseaseResultContainer');
  if (resCard) resCard.classList.add('hidden');
  const loader = document.getElementById('scanningLoader');
  if (loader) loader.classList.add('hidden');
}

async function openCameraModal() {
  const modal = document.getElementById('cameraModal');
  const video = document.getElementById('cameraVideo');
  if (!modal || !video) return;
  modal.classList.remove('hidden');

  try {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
    const constraints = {
      video: {
        facingMode: cameraFacing,
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    };
    cameraStream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = cameraStream;
  } catch (err) {
    console.error("Camera access error:", err);
    showToast(state.lang === 'hi' ? 'कैमरा खोलने में असमर्थ। कृपया अनुमति जांचें।' : 'Unable to access camera. Please check permissions.', 'error');
    closeCameraModal();
  }
}

function closeCameraModal() {
  const modal = document.getElementById('cameraModal');
  if (modal) modal.classList.add('hidden');
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
}

function switchCameraFacing() {
  cameraFacing = cameraFacing === 'environment' ? 'user' : 'environment';
  openCameraModal();
}

function captureCameraPhoto() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  if (!video || !canvas) return;

  const ctx = canvas.getContext('2d');
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  selectedImageBase64 = canvas.toDataURL('image/jpeg', 0.9);

  const leafImg = document.getElementById('leafImagePreview');
  const scanningImg = document.getElementById('scanningImageCopy');
  const fileNameEl = document.getElementById('previewFileName');

  if (leafImg) leafImg.src = selectedImageBase64;
  if (scanningImg) scanningImg.src = selectedImageBase64;
  if (fileNameEl) fileNameEl.innerText = 'Live Camera Snapshot';

  const prevCard = document.getElementById('diseasePreviewCard');
  if (prevCard) prevCard.classList.remove('hidden');
  const resCard = document.getElementById('diseaseResultContainer');
  if (resCard) resCard.classList.add('hidden');
  const loader = document.getElementById('scanningLoader');
  if (loader) loader.classList.add('hidden');

  closeCameraModal();
  showToast(state.lang === 'hi' ? 'कैमरा फोटो ली गई! अब जांच बटन दबाएं' : 'Camera snapshot captured!', 'success');
}

async function analyzePlantDisease() {
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

    // Run 100% on-device local ML inference (Zero server, No FastAPI, No Gemini API)
    const data = await analyzeLeafLocally(selectedImageBase64, selectedCrop);
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
    cropBadge.innerText = isHi
      ? `मॉडल: ${cropLocalized} — स्थानीय ONNX मॉडल`
      : `Model: ${cropLocalized} — Local ONNX Model`;
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
      if (affBadge) {
        const labelText = isHi ? (data.highlight_label_hi || 'संभावित प्रभावित क्षेत्र') : (data.highlight_label || 'Suspected affected region');
        affBadge.innerText = `${labelText}: ${affectedArea}%`;
      }
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



// ─── AI KISAN ASSISTANT CHAT ENGINE (TAB 6) ─────────────────────────────────

function initChatState() {
  syncFarmerContext();
  initVoiceRecognition();
  updateChatVoiceIcon();
  if (typeof renderChatSuggestedChips === 'function') {
    renderChatSuggestedChips();
  }
}

function syncFarmerContext() {
  const loc = state.location;
  chatState.farmerContext.location = `${loc.city || 'Farm Location'}${loc.state ? ', ' + loc.state : ''}`;
  chatState.farmerContext.pincode = loc.pincode || '';
  chatState.farmerContext.crop = state.crop;
  chatState.farmerContext.weather = state.weatherData;

  // Update banner UI elements
  const locBadge = document.getElementById('chatCtxLocation');
  if (locBadge) {
    locBadge.textContent = `${loc.city || 'Farm'}${loc.pincode && loc.pincode !== 'GPS' && loc.pincode !== 'City' ? ' (' + loc.pincode + ')' : ''}`;
  }

  const cropBadge = document.getElementById('chatCtxCrop');
  if (cropBadge) {
    cropBadge.textContent = `${state.crop} (${chatState.farmerContext.cropStage.split(' ')[0]})`;
  }

  const weatherBadge = document.getElementById('chatCtxWeather');
  if (weatherBadge) {
    if (state.weatherData && state.weatherData.current) {
      const c = state.weatherData.current;
      weatherBadge.textContent = `${Math.round(c.temp)}°C · ${c.weather_main}`;
    } else {
      weatherBadge.textContent = 'Weather Loading...';
    }
  }

  const soilBadge = document.getElementById('chatCtxSoil');
  if (soilBadge) {
    soilBadge.textContent = chatState.farmerContext.soilType.split(' ')[0] + ' Soil';
  }
}

// ─── Farm Context Modal Handlers ────────────────────────────────────────────
function openFarmContextModal() {
  const modal = document.getElementById('farmContextModal');
  if (!modal) return;

  const cropSel = document.getElementById('ctxCropSelect');
  if (cropSel) cropSel.value = chatState.farmerContext.crop;

  const stageSel = document.getElementById('ctxStageSelect');
  if (stageSel) stageSel.value = chatState.farmerContext.cropStage;

  const soilSel = document.getElementById('ctxSoilSelect');
  if (soilSel) soilSel.value = chatState.farmerContext.soilType;

  const irrSel = document.getElementById('ctxIrrigationSelect');
  if (irrSel) irrSel.value = chatState.farmerContext.irrigationType;

  const acreInput = document.getElementById('ctxAcreageInput');
  if (acreInput) acreInput.value = chatState.farmerContext.acreage;

  modal.classList.remove('hidden');
}

function closeFarmContextModal() {
  const modal = document.getElementById('farmContextModal');
  if (modal) modal.classList.add('hidden');
}

function saveFarmContext() {
  const crop = document.getElementById('ctxCropSelect').value;
  const stage = document.getElementById('ctxStageSelect').value;
  const soil = document.getElementById('ctxSoilSelect').value;
  const irr = document.getElementById('ctxIrrigationSelect').value;
  const acre = document.getElementById('ctxAcreageInput').value.trim();

  chatState.farmerContext.crop = crop;
  chatState.farmerContext.cropStage = stage;
  chatState.farmerContext.soilType = soil;
  chatState.farmerContext.irrigationType = irr;
  chatState.farmerContext.acreage = acre || 'Standard Acreage';

  localStorage.setItem('sap_crop_stage', stage);
  localStorage.setItem('sap_soil_type', soil);
  localStorage.setItem('sap_irrigation_type', irr);
  localStorage.setItem('sap_acreage', acre);

  // Sync with global app crop if changed
  if (crop !== state.crop) {
    state.crop = crop;
    localStorage.setItem('sap_crop', crop);
    initCropSelectors();
    loadWeatherForCurrentState(true);
  }

  syncFarmerContext();
  syncFertilizerContext();
  closeFarmContextModal();
  showToast(state.lang === 'hi' ? 'कृषि प्रोफाइल सफलतापूर्वक अपडेट की गई!' : 'Farm profile context updated!', 'success');
}

// ─── Image Attachment & Canvas Compression ──────────────────────────────────
function toggleAttachmentMenu() {
  const menu = document.getElementById('attachmentMenu');
  if (menu) menu.classList.toggle('hidden');
}

function triggerChatUpload() {
  const input = document.getElementById('chatFileInput');
  if (input) input.click();
}

function triggerChatCamera() {
  const mobileInput = document.getElementById('chatMobileCameraInput');
  if (mobileInput) {
    mobileInput.click();
  }
}

function handleChatFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  compressAndAttachImage(file);
}

function handleChatMobileCamera(event) {
  const file = event.target.files[0];
  if (!file) return;
  compressAndAttachImage(file);
}

function compressAndAttachImage(file) {
  if (!file.type.startsWith('image/')) {
    showToast(state.lang === 'hi' ? 'कृपया केवल फोटो फाइल चुनें' : 'Please choose a valid image file', 'error');
    return;
  }

  showToast(state.lang === 'hi' ? 'फोटो लोड हो रही है...' : 'Processing image...', 'info');

  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      // Resize to max 1024px for rapid transmission & optimal token usage
      const canvas = document.createElement('canvas');
      let width = img.width;
      let height = img.height;
      const maxDim = 1024;

      if (width > height && width > maxDim) {
        height = Math.round((height * maxDim) / width);
        width = maxDim;
      } else if (height > maxDim) {
        width = Math.round((width * maxDim) / height);
        height = maxDim;
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);

      chatState.attachedImageBase64 = canvas.toDataURL('image/jpeg', 0.88);
      chatState.attachedImageName = file.name || 'Leaf Photo';

      const thumb = document.getElementById('chatAttachedImgThumbnail');
      const nameEl = document.getElementById('chatAttachedImgName');
      const strip = document.getElementById('chatImagePreviewStrip');

      if (thumb) thumb.src = chatState.attachedImageBase64;
      if (nameEl) nameEl.textContent = `${chatState.attachedImageName} (${Math.round(chatState.attachedImageBase64.length / 1024)} KB)`;
      if (strip) strip.classList.remove('hidden');

      showToast(state.lang === 'hi' ? 'फोटो अटैच की गई! अब सवाल भेजें' : 'Photo attached! Click Send to ask.', 'success');
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function removeChatAttachedImage() {
  chatState.attachedImageBase64 = null;
  chatState.attachedImageName = null;

  const fileInput = document.getElementById('chatFileInput');
  if (fileInput) fileInput.value = '';
  const camInput = document.getElementById('chatMobileCameraInput');
  if (camInput) camInput.value = '';

  const strip = document.getElementById('chatImagePreviewStrip');
  if (strip) strip.classList.add('hidden');
}

// ─── Web Speech Recognition (Voice Input) ───────────────────────────────────
function initVoiceRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    return;
  }

  const rec = new SpeechRec();
  rec.continuous = false;
  rec.interimResults = true;

  rec.onstart = () => {
    chatState.isRecording = true;
    const micBtn = document.getElementById('chatMicBtn');
    if (micBtn) micBtn.classList.add('mic-recording-pulse');
    const visualizer = document.getElementById('chatVoiceVisualizer');
    if (visualizer) visualizer.classList.remove('hidden');
  };

  rec.onresult = (event) => {
    let transcript = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      transcript += event.results[i][0].transcript;
    }
    const input = document.getElementById('chatMessageInput');
    if (input && transcript) {
      input.value = transcript;
      autoResizeTextarea(input);
    }
  };

  rec.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    stopVoiceRecording();
    if (event.error === 'not-allowed') {
      showToast(state.lang === 'hi' ? 'माइक्रोफोन अनुमति अस्वीकार की गई' : 'Microphone access denied', 'warning');
    }
  };

  rec.onend = () => {
    stopVoiceRecording();
  };

  chatState.speechRecognition = rec;
}

function toggleVoiceRecording() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    showToast(
      state.lang === 'hi'
        ? 'आपके ब्राउज़र में वॉइस इनपुट उपलब्ध नहीं है। कृपया टाइप करें।'
        : 'Voice input is not supported in this browser. Please type your question.',
      'warning'
    );
    return;
  }

  if (chatState.isRecording) {
    stopVoiceRecording();
  } else {
    try {
      if (!chatState.speechRecognition) initVoiceRecognition();
      chatState.speechRecognition.lang = state.lang === 'hi' ? 'hi-IN' : 'en-IN';
      chatState.speechRecognition.start();
    } catch (e) {
      console.warn("Speech start error:", e);
      stopVoiceRecording();
    }
  }
}

function stopVoiceRecording() {
  chatState.isRecording = false;
  const micBtn = document.getElementById('chatMicBtn');
  if (micBtn) micBtn.classList.remove('mic-recording-pulse');
  const visualizer = document.getElementById('chatVoiceVisualizer');
  if (visualizer) visualizer.classList.add('hidden');

  if (chatState.speechRecognition) {
    try { chatState.speechRecognition.stop(); } catch (e) {}
  }
}

// ─── Text-to-Speech (TTS) Voice Synthesis ───────────────────────────────────
function toggleChatAutoVoice() {
  chatState.autoVoiceEnabled = !chatState.autoVoiceEnabled;
  localStorage.setItem('sap_auto_voice', chatState.autoVoiceEnabled);
  updateChatVoiceIcon();
  showToast(
    chatState.autoVoiceEnabled
      ? (state.lang === 'hi' ? 'ऑटो वॉइस चालू (उत्तर बोलकर सुनाया जाएगा)' : 'Auto Voice ON (Answers will be spoken)')
      : (state.lang === 'hi' ? 'ऑटो वॉइस बंद' : 'Auto Voice OFF'),
    'info'
  );
}

function updateChatVoiceIcon() {
  const icon = document.getElementById('chatVoiceToggleIcon');
  if (icon) {
    icon.className = chatState.autoVoiceEnabled
      ? 'fa-solid fa-volume-high text-xs text-emerald-300'
      : 'fa-solid fa-volume-xmark text-xs text-white/50';
  }
}

function speakTextMessage(rawText, btnElement) {
  if (!('speechSynthesis' in window)) {
    showToast(state.lang === 'hi' ? 'स्पीच सिंथेसिस उपलब्ध नहीं है' : 'Speech synthesis not supported', 'warning');
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (chatState.currentlySpeakingBtn) {
      chatState.currentlySpeakingBtn.innerHTML = `<i class="fa-solid fa-volume-high"></i> <span>${state.lang === 'hi' ? 'सुनें' : 'Listen'}</span>`;
      chatState.currentlySpeakingBtn = null;
    }
    if (btnElement && btnElement === chatState.currentlySpeakingBtn) {
      return;
    }
  }

  // Clean markdown syntax for natural speech
  let cleanText = rawText
    .replace(/[#*_`~>-]/g, ' ')
    .replace(/\[IMAGE ANALYSIS.*?\]/gs, ' ')
    .replace(/http\S+/g, '')
    .replace(/\s+/g, ' ')
    .trim();

  if (!cleanText) return;

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.rate = 0.95;
  utterance.pitch = 1.0;

  // Language auto selection
  const isHindiText = /[\u0900-\u097F]/.test(cleanText);
  utterance.lang = isHindiText ? 'hi-IN' : 'en-IN';

  const voices = window.speechSynthesis.getVoices();
  const matchedVoice = voices.find(v => v.lang.startsWith(isHindiText ? 'hi' : 'en'));
  if (matchedVoice) utterance.voice = matchedVoice;

  if (btnElement) {
    chatState.currentlySpeakingBtn = btnElement;
    btnElement.innerHTML = `<i class="fa-solid fa-stop text-rose-500 animate-pulse"></i> <span>${state.lang === 'hi' ? 'रोकें' : 'Stop'}</span>`;
  }

  utterance.onend = () => {
    if (btnElement) {
      btnElement.innerHTML = `<i class="fa-solid fa-volume-high"></i> <span>${state.lang === 'hi' ? 'सुनें' : 'Listen'}</span>`;
    }
    chatState.currentlySpeakingBtn = null;
  };

  utterance.onerror = () => {
    if (btnElement) {
      btnElement.innerHTML = `<i class="fa-solid fa-volume-high"></i> <span>${state.lang === 'hi' ? 'सुनें' : 'Listen'}</span>`;
    }
    chatState.currentlySpeakingBtn = null;
  };

  window.speechSynthesis.speak(utterance);
}

// ─── Input & Submission Handlers ────────────────────────────────────────────
function autoResizeTextarea(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function handleChatInputKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    handleChatSubmit(event);
  }
}

const CHAT_SUGGESTED_CHIPS = [
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

function sendQuickPrompt(promptText) {
  const input = document.getElementById('chatMessageInput');
  if (input) {
    input.value = promptText;
    handleChatSubmit(new Event('submit'));
  }
}

async function handleChatSubmit(event) {
  if (event) event.preventDefault();

  if (chatState.isGenerating) return;

  const inputEl = document.getElementById('chatMessageInput');
  const userMessage = inputEl ? inputEl.value.trim() : '';
  const attachedImg = chatState.attachedImageBase64;

  if (!userMessage && !attachedImg) {
    showToast(state.lang === 'hi' ? 'कृपया कोई सवाल लिखें या फोटो जोड़ें' : 'Please type a question or attach a photo', 'warning');
    return;
  }

  // 1. Clear input & staged image UI
  if (inputEl) {
    inputEl.value = '';
    inputEl.style.height = 'auto';
  }
  removeChatAttachedImage();

  // 2. Add User message to stream
  const userMsgId = 'msg-' + Date.now();
  const userMsgObj = {
    id: userMsgId,
    role: 'user',
    text: userMessage,
    image: attachedImg,
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  };
  chatState.messages.push(userMsgObj);
  renderChatMessage(userMsgObj);

  // 3. Show Typing Indicator
  setChatGenerating(true);
  scrollChatToBottom();

  // 4. Prepare API Payload
  const historyPayload = chatState.messages
    .slice(-8, -1) // Exclude current user message
    .map(m => ({
      role: m.role === 'user' ? 'user' : 'model',
      content: m.text
    }));

  try {
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

    // 100% Local Rule-Based Kisan AI Assistant (Strictly NO Gemini API, NO Cloud API, Offline)
    const data = (typeof generateLocalKisanBotReply === 'function')
      ? generateLocalKisanBotReply(userMessage, chatPayload.context, currentLang)
      : { status: 'success', reply: currentLang === 'hi' ? 'स्थानीय सहायक सक्रिय है।' : 'Local Kisan Assistant is active.', intent: 'general' };

    // 5. Append Assistant Message
    const assistantMsgObj = {
      id: 'msg-' + Date.now(),
      role: 'assistant',
      text: data.reply,
      intent: data.intent,
      disease_scan: data.disease_scan,
      suggested_actions: data.suggested_actions,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    chatState.messages.push(assistantMsgObj);
    renderChatMessage(assistantMsgObj);

    // 6. Optional Auto Voice
    if (chatState.autoVoiceEnabled && data.reply) {
      speakTextMessage(data.reply);
    }

  } catch (err) {
    console.error("Chat Error:", err);
    const errorMsgObj = {
      id: 'msg-err-' + Date.now(),
      role: 'error',
      text: state.lang === 'hi'
        ? `स्थानीय कृषि सहायक सेवा से संपर्क करने में समस्या हुई (${err.message})। कृपया पुनः प्रयास करें।`
        : `An error occurred while generating agricultural advice (${err.message}). Please try again.`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      retryPrompt: userMessage
    };
    renderChatMessage(errorMsgObj);
  } finally {
    setChatGenerating(false);
    scrollChatToBottom();
  }
}

function setChatGenerating(isGenerating) {
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
}

function scrollChatToBottom() {
  const container = document.getElementById('chatMessagesContainer');
  if (container) {
    requestAnimationFrame(() => {
      container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
    });
  }
}

// ─── Chat Message Renderer ──────────────────────────────────────────────────
function renderChatMessage(msg) {
  const list = document.getElementById('chatMessagesList');
  if (!list) return;

  const isHi = state.lang === 'hi';
  const msgEl = document.createElement('div');
  msgEl.className = 'chat-bubble-enter flex flex-col space-y-1';
  msgEl.id = msg.id;

  if (msg.role === 'user') {
    msgEl.innerHTML = `
      <div class="flex items-start justify-end space-x-2.5 max-w-[90%] sm:max-w-[80%] ml-auto">
        <div class="space-y-1 text-right">
          <div class="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-3.5 sm:p-4 rounded-3xl rounded-tr-sm shadow-md text-xs sm:text-sm leading-relaxed text-left font-medium">
            ${msg.image ? `
              <div class="mb-2 rounded-2xl overflow-hidden border border-white/20 max-w-[200px] shadow">
                <img src="${msg.image}" alt="Attached leaf" class="w-full h-auto object-cover">
              </div>
            ` : ''}
            <div>${escapeHTML(msg.text)}</div>
          </div>
          <span class="text-[10px] text-slate-400 font-semibold px-2">${msg.timestamp} · ${isHi ? 'आप (किसान)' : 'You'}</span>
        </div>
        <div class="w-8 h-8 rounded-full bg-emerald-700 text-white flex items-center justify-center text-xs font-bold shadow flex-shrink-0">
          👨🌾
        </div>
      </div>
    `;
  } else if (msg.role === 'assistant') {
    const formattedHTML = renderMarkdownToHTML(msg.text);

    // Build Disease Card if disease_scan data is attached
    let diseaseCardHTML = '';
    if (msg.disease_scan && msg.disease_scan.status === 'success') {
      const d = msg.disease_scan;
      const isSevere = d.severity_score > 60;
      const sevClass = isSevere ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border-amber-500/30';

      diseaseCardHTML = `
        <div class="my-3 p-4 rounded-2xl bg-slate-900 text-white border border-emerald-500/40 shadow-lg space-y-3">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2">
            <div class="flex items-center space-x-2">
              <span class="text-emerald-400 text-base">🔬</span>
              <span class="font-extrabold text-xs sm:text-sm text-emerald-300">${isHi ? d.disease_name_hi : d.disease_name_en}</span>
            </div>
            <span class="text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${sevClass}">${d.severity_level} (${d.confidence}%)</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
            <div class="bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/60">
              <span class="text-emerald-400 font-bold block mb-0.5"><i class="fa-solid fa-leaf mr-1"></i>${isHi ? 'जैविक उपचार' : 'Organic Remedy'}</span>
              <span class="text-slate-300">${isHi ? d.organic_remedy_hi : d.organic_remedy_en}</span>
            </div>
            <div class="bg-slate-800/80 p-2.5 rounded-xl border border-slate-700/60">
              <span class="text-indigo-400 font-bold block mb-0.5"><i class="fa-solid fa-vial mr-1"></i>${isHi ? 'रासायनिक दवा' : 'Chemical Spray'}</span>
              <span class="text-slate-300">${isHi ? d.chemical_treatment_hi : d.chemical_treatment_en}</span>
            </div>
          </div>
        </div>
      `;
    }

    // Build suggested follow-up chips and deep-links
    let suggestionsHTML = '';
    let actionButtonsHTML = '';

    if (msg.intent === 'mandi' || (msg.text && /mandi|bhav|market price/i.test(msg.text))) {
      actionButtonsHTML += `
        <button onclick="switchTab('market')" class="chat-chip text-[11px] font-bold bg-blue-50 dark:bg-blue-950/60 hover:bg-blue-100 text-blue-700 dark:text-blue-300 px-3 py-1.5 rounded-xl border border-blue-200 dark:border-blue-800 transition flex items-center space-x-1.5">
          <i class="fa-solid fa-chart-line text-blue-500"></i>
          <span>${isHi ? 'ताजा मंडी भाव डैशबोर्ड देखें →' : 'View Mandi Prices Dashboard →'}</span>
        </button>
      `;
    }

    if (actionButtonsHTML || (msg.suggested_actions && msg.suggested_actions.length > 0)) {
      suggestionsHTML = `
        <div class="pt-2.5 flex flex-wrap gap-1.5">
          ${actionButtonsHTML}
          ${(msg.suggested_actions || []).map(s => `
            <button onclick="sendQuickPrompt('${escapeAttribute(s)}')" class="chat-chip text-[11px] font-semibold bg-emerald-50 dark:bg-emerald-950/60 hover:bg-emerald-100 text-emerald-800 dark:text-emerald-200 px-2.5 py-1 rounded-full border border-emerald-200 dark:border-emerald-800 transition">
              ${escapeHTML(s)}
            </button>
          `).join('')}
        </div>
      `;
    }

    msgEl.innerHTML = `
      <div class="flex items-start space-x-2.5 max-w-[92%] sm:max-w-[85%]">
        <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-400 text-slate-950 flex items-center justify-center text-xs font-extrabold shadow flex-shrink-0">
          🌱
        </div>
        <div class="space-y-1 flex-1">
          <div class="bg-white dark:bg-slate-800/90 text-slate-800 dark:text-slate-100 p-4 sm:p-5 rounded-3xl rounded-tl-sm border border-slate-200 dark:border-slate-700/80 shadow-md text-xs sm:text-sm leading-relaxed chat-markdown">
            ${diseaseCardHTML}
            <div>${formattedHTML}</div>
            ${suggestionsHTML}
          </div>
          <div class="flex items-center justify-between px-2 text-[10px] text-slate-400">
            <span>${msg.timestamp} · AI Kisan Assistant</span>
            <div class="flex items-center space-x-2">
              <button onclick="copyMessageText('${msg.id}')" class="hover:text-emerald-600 transition flex items-center space-x-1">
                <i class="fa-regular fa-copy"></i>
                <span>${isHi ? 'कॉपी' : 'Copy'}</span>
              </button>
              <button onclick="speakChatMessage('${msg.id}', this)" class="hover:text-emerald-600 transition flex items-center space-x-1">
                <i class="fa-solid fa-volume-high"></i>
                <span>${isHi ? 'सुनें' : 'Listen'}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  } else if (msg.role === 'error') {
    msgEl.innerHTML = `
      <div class="flex items-start space-x-2.5 max-w-[90%] sm:max-w-[80%]">
        <div class="w-8 h-8 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-600 flex items-center justify-center text-xs font-bold shadow flex-shrink-0">
          <i class="fa-solid fa-triangle-exclamation"></i>
        </div>
        <div class="space-y-1">
          <div class="bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 p-4 rounded-2xl border border-rose-200 dark:border-rose-900 shadow-sm text-xs font-medium space-y-2">
            <p>${escapeHTML(msg.text)}</p>
            ${msg.retryPrompt ? `
              <button onclick="sendQuickPrompt('${escapeAttribute(msg.retryPrompt)}')" class="bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs px-3 py-1.5 rounded-xl transition shadow flex items-center space-x-1">
                <i class="fa-solid fa-rotate-right"></i>
                <span>${isHi ? 'पुनः प्रयास करें' : 'Retry Question'}</span>
              </button>
            ` : ''}
          </div>
        </div>
      </div>
    `;
  }

  list.appendChild(msgEl);
}

function clearChatHistory() {
  chatState.messages = [];
  const list = document.getElementById('chatMessagesList');
  if (list) list.innerHTML = '';
  if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  showToast(state.lang === 'hi' ? 'बातचीत इतिहास साफ किया गया' : 'Chat conversation cleared', 'info');
}

function copyMessageText(msgId) {
  const msgObj = chatState.messages.find(m => m.id === msgId);
  if (msgObj && msgObj.text) {
    navigator.clipboard.writeText(msgObj.text);
    showToast(state.lang === 'hi' ? 'उत्तर कॉपी किया गया!' : 'Message copied to clipboard!', 'success');
  }
}

function speakChatMessage(msgId, btnElement) {
  const msgObj = chatState.messages.find(m => m.id === msgId);
  if (msgObj && msgObj.text) {
    speakTextMessage(msgObj.text, btnElement);
  }
}

// ─── Markdown to Semantic HTML Converter ────────────────────────────────────
function renderMarkdownToHTML(text) {
  if (!text) return '';

  let html = text
    // Replace Markdown headers
    .replace(/^### (.*$)/gim, '<h4 class="text-sm font-bold text-emerald-700 dark:text-emerald-400 mt-3 mb-1">$1</h4>')
    .replace(/^## (.*$)/gim, '<h3 class="text-base font-extrabold text-emerald-800 dark:text-emerald-300 mt-4 mb-1.5">$1</h3>')
    .replace(/^# (.*$)/gim, '<h2 class="text-lg font-extrabold text-slate-900 dark:text-white mt-4 mb-2">$1</h2>')
    // Bold
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-bold text-slate-900 dark:text-slate-100">$1</strong>')
    // Italic
    .replace(/\*(.*?)\*/gim, '<em class="italic">$1</em>')
    // Bullet points
    .replace(/^\s*[\-\*]\s+(.*$)/gim, '<li class="ml-4 list-disc text-xs leading-relaxed my-0.5">$1</li>')
    // Numbered lists
    .replace(/^\s*(\d+)\.\s+(.*$)/gim, '<li class="ml-4 list-decimal text-xs leading-relaxed my-0.5">$2</li>')
    // Blockquotes
    .replace(/^\> (.*$)/gim, '<blockquote class="border-l-4 border-emerald-500 pl-3 py-1 my-2 bg-emerald-50/50 dark:bg-emerald-950/30 rounded-r-lg italic text-xs">$1</blockquote>')
    // Horizontal rule
    .replace(/^---$/gim, '<hr class="my-3 border-slate-200 dark:border-slate-700">')
    // Double newlines to paragraph breaks
    .replace(/\n\n+/g, '<div class="my-2"></div>')
    // Single newlines to line breaks
    .replace(/\n/g, '<br>');

  return html;
}

function escapeHTML(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function escapeAttribute(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

// ─── Drag & Drop Event Listeners ─────────────────────────────────────────────
// ─── Drag & Drop & Global Modal Event Listeners ─────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const dropZone = document.getElementById('dropZone');
  if (dropZone) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('border-emerald-500', 'bg-emerald-50/50', 'dark:bg-emerald-950/40');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('border-emerald-500', 'bg-emerald-50/50', 'dark:bg-emerald-950/40');
      }, false);
    });

    dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        processSelectedFile(files[0]);
      }
    }, false);
  }

  // Global Escape Key Listener to dismiss any active modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closePincodeModal();
      closeFarmContextModal();
      closeCameraModal();
      closeMandiDetailModal();
    }
  });

  // Modal Backdrop Click Listeners
  ['pincodeModal', 'farmContextModal', 'cameraModal', 'mandiDetailModal'].forEach(modalId => {
    const modalEl = document.getElementById(modalId);
    if (modalEl) {
      modalEl.addEventListener('click', (e) => {
        if (e.target === modalEl) {
          modalEl.classList.add('hidden');
        }
      });
    }
  });
});
