/**
 * Smart Agriculture Platform (SAP) — Kisan Bot Module
 * All chatbot questions are processed directly by the live Google Gemini API via /api/chat.
 * Static predefined responses, keyword-matching engines, and canned answer dictionaries have been removed.
 */

// Stubs preserved for backwards compatibility with any legacy script references
const LOCAL_KISAN_KNOWLEDGE = {};

function isHindiMessage(text) {
  return /[\u0900-\u097F]/.test(text || '');
}

if (typeof window !== 'undefined') {
  window.LOCAL_KISAN_KNOWLEDGE = LOCAL_KISAN_KNOWLEDGE;
  window.isHindiMessage = isHindiMessage;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    LOCAL_KISAN_KNOWLEDGE,
    isHindiMessage
  };
}
