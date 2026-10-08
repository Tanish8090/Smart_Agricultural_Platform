/**
 * Smart Agriculture Platform (SAP) — Global Configuration
 * 
 * Rules:
 * 1. For development: http://localhost:8080
 * 2. For Android production APK: deployed HTTPS backend URL.
 * 3. Never use localhost, 127.0.0.1, or 10.0.2.2 in native Android build.
 * 4. Full offline resilience: All core features work locally if backend is unreachable.
 */

// Production deployed HTTPS backend for SAP (Permanent cloud endpoint)
const PRODUCTION_BACKEND_URL = 'https://sap-agriculture-backend.onrender.com';
const DEVELOPMENT_BACKEND_URL = 'http://localhost:8080';

function getEnvironmentApiBaseUrl() {
  // Check if farmer or developer set a custom backend URL in localStorage
  try {
    if (typeof localStorage !== 'undefined') {
      const customUrl = localStorage.getItem('sap_backend_url');
      if (customUrl && customUrl.trim()) {
        const clean = customUrl.trim().replace(/\/+$/, '');
        // On native Android, guard against accidentally leaving localhost in storage
        const isCapacitor = (typeof window !== 'undefined' && window.Capacitor && typeof window.Capacitor.isNativePlatform === 'function' && window.Capacitor.isNativePlatform());
        if (isCapacitor && (clean.includes('localhost') || clean.includes('127.0.0.1') || clean.includes('10.0.2.2'))) {
          console.warn('[SAP Config] Ignoring localhost URL on native Android device. Using production HTTPS backend.');
          return PRODUCTION_BACKEND_URL;
        }
        return clean;
      }
    }
  } catch (e) {
    console.warn('[SAP Config] Error reading localStorage:', e);
  }

  // Detect Capacitor Native Android Platform
  const isNative = (
    typeof window !== 'undefined' &&
    window.Capacitor &&
    typeof window.Capacitor.isNativePlatform === 'function' &&
    window.Capacitor.isNativePlatform()
  );

  if (isNative) {
    // Native Android APK: Strictly HTTPS production endpoint
    return PRODUCTION_BACKEND_URL;
  }

  // Running in Desktop Browser
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    // Development environment
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '') {
      return DEVELOPMENT_BACKEND_URL;
    }
    // Deployed Web environment
    if (window.location.protocol === 'https:' || window.location.protocol === 'http:') {
      return window.location.origin;
    }
  }

  return PRODUCTION_BACKEND_URL;
}

const API_BASE_URL = getEnvironmentApiBaseUrl();

// Expose globally for both browser scripts and modules
if (typeof window !== 'undefined') {
  window.API_BASE_URL = API_BASE_URL;
  window.PRODUCTION_BACKEND_URL = PRODUCTION_BACKEND_URL;
  window.DEVELOPMENT_BACKEND_URL = DEVELOPMENT_BACKEND_URL;
  window.getEnvironmentApiBaseUrl = getEnvironmentApiBaseUrl;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    API_BASE_URL,
    PRODUCTION_BACKEND_URL,
    DEVELOPMENT_BACKEND_URL,
    getEnvironmentApiBaseUrl
  };
}
