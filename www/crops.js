/**
 * ══════════════════════════════════════════════════════════════════════════════
 * CENTRAL CROP CONFIGURATION (SAP STANDARDIZED CROP SYSTEM)
 * ══════════════════════════════════════════════════════════════════════════════
 * Exactly 10 standardized crops in fixed sequence:
 * 1. Wheat       (Yellow Rust / Healthy)
 * 2. Cotton      (Bacterial Blight / Healthy)
 * 3. Sugarcane   (Red Rot / Healthy)
 * 4. Potato      (Early Blight / Late Blight / Healthy)
 * 5. Rice        (Blast / Brown Spot / Healthy)
 * 6. Soybean     (Rust / Healthy)
 * 7. Tomato      (Early Blight / Late Blight / Healthy)
 * 8. Corn/Maize  (Common Rust / Leaf Blight / Healthy)
 * 9. Apple       (Scab / Healthy)
 * 10. Grape      (Black Rot / Healthy)
 */

const SAP_CROPS = [
  {
    id: 'wheat',
    value: 'Wheat',
    name_en: 'Wheat',
    name_hi: 'गेहूं',
    display_en: 'Wheat (Yellow Rust / Healthy)',
    display_hi: 'गेहूं (पीला रतुआ / स्वस्थ)',
    icon: '🌾',
    model_name: 'Wheat Model',
    model_file: 'wheat.onnx',
    model_dir: 'models/wheat',
    classes: ['Wheat___Yellow_rust', 'Wheat___healthy']
  },
  {
    id: 'cotton',
    value: 'Cotton',
    name_en: 'Cotton',
    name_hi: 'कपास',
    display_en: 'Cotton (Bacterial Blight / Healthy)',
    display_hi: 'कपास (जीवाणु झुलसा / स्वस्थ)',
    icon: '🌱',
    model_name: 'Cotton Model',
    model_file: 'cotton.onnx',
    model_dir: 'models/cotton',
    classes: ['Cotton___Bacterial_blight', 'Cotton___healthy']
  },
  {
    id: 'sugarcane',
    value: 'Sugarcane',
    name_en: 'Sugarcane',
    name_hi: 'गन्ना',
    display_en: 'Sugarcane (Red Rot / Healthy)',
    display_hi: 'गन्ना (लाल सड़न / स्वस्थ)',
    icon: '🎋',
    model_name: 'Sugarcane Model',
    model_file: 'sugarcane.onnx',
    model_dir: 'models/sugarcane',
    classes: ['Sugarcane___Red_rot', 'Sugarcane___healthy']
  },
  {
    id: 'potato',
    value: 'Potato',
    name_en: 'Potato',
    name_hi: 'आलू',
    display_en: 'Potato (Early Blight / Late Blight / Healthy)',
    display_hi: 'आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)',
    icon: '🥔',
    model_name: 'Potato Model',
    model_file: 'potato.onnx',
    model_dir: 'models/potato',
    classes: ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
  },
  {
    id: 'rice',
    value: 'Rice',
    name_en: 'Rice',
    name_hi: 'धान',
    display_en: 'Rice (Blast / Brown Spot / Healthy)',
    display_hi: 'धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)',
    icon: '🌾',
    model_name: 'Rice Model',
    model_file: 'rice.onnx',
    model_dir: 'models/rice',
    classes: ['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']
  },
  {
    id: 'soybean',
    value: 'Soybean',
    name_en: 'Soybean',
    name_hi: 'सोयाबीन',
    display_en: 'Soybean (Rust / Healthy)',
    display_hi: 'सोयाबीन (रस्ट / स्वस्थ)',
    icon: '🌿',
    model_name: 'Soybean Model',
    model_file: 'soybean.onnx',
    model_dir: 'models/soybean',
    classes: ['Soybean___Rust', 'Soybean___healthy']
  },
  {
    id: 'tomato',
    value: 'Tomato',
    name_en: 'Tomato',
    name_hi: 'टमाटर',
    display_en: 'Tomato (Early Blight / Late Blight / Healthy)',
    display_hi: 'टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)',
    icon: '🍅',
    model_name: 'Tomato Model',
    model_file: 'tomato.onnx',
    model_dir: 'models/tomato',
    classes: ['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']
  },
  {
    id: 'corn',
    value: 'Corn',
    name_en: 'Corn / Maize',
    name_hi: 'मक्का',
    display_en: 'Corn / Maize (Common Rust / Leaf Blight / Healthy)',
    display_hi: 'मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)',
    icon: '🌽',
    model_name: 'Corn Model',
    model_file: 'corn.onnx',
    model_dir: 'models/corn',
    classes: ['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']
  },
  {
    id: 'apple',
    value: 'Apple',
    name_en: 'Apple',
    name_hi: 'सेब',
    display_en: 'Apple (Scab / Healthy)',
    display_hi: 'सेब (स्कैब / स्वस्थ)',
    icon: '🍎',
    model_name: 'Apple Model',
    model_file: 'apple.onnx',
    model_dir: 'models/apple',
    classes: ['Apple___Scab', 'Apple___healthy']
  },
  {
    id: 'grape',
    value: 'Grape',
    name_en: 'Grape',
    name_hi: 'अंगूर',
    display_en: 'Grape (Black Rot / Healthy)',
    display_hi: 'अंगूर (ब्लैक रॉट / स्वस्थ)',
    icon: '🍇',
    model_name: 'Grape Model',
    model_file: 'grape.onnx',
    model_dir: 'models/grape',
    classes: ['Grape___Black_rot', 'Grape___healthy']
  }
];

if (typeof window !== 'undefined') {
  window.SAP_CROPS = SAP_CROPS;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SAP_CROPS };
}
