import os
import sys
import io
import json
import base64
import numpy as np
from PIL import Image
try:
    import torch
    import cv2
    import torch.nn.functional as F
    from ultralytics import YOLO
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    cv2 = None
    F = None
    YOLO = None
    TORCH_AVAILABLE = False

sys.stdout.reconfigure(encoding='utf-8')

# Global cache for loaded YOLO models
_LOADED_MODELS = {}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model_config.json')

def load_config():
    default_config = {
        "not_a_leaf_model": "models/not_a_leaf/best.pt",
        "not_a_leaf_threshold": 0.50,
        "min_confidence_threshold": 0.35,
        "crop_models": {
            "wheat": "models/wheat/best.pt",
            "cotton": "models/cotton/best.pt",
            "sugarcane": "models/sugarcane/best.pt",
            "potato": "models/potato/best.pt",
            "rice": "models/rice/best.pt",
            "soybean": "models/soybean/best.pt",
            "tomato": "models/tomato/best.pt",
            "corn": "models/corn/best.pt",
            "apple": "models/apple/best.pt",
            "grape": "models/grape/best.pt"
        },
        "not_ready_crops": []
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                default_config.update(cfg)
        except Exception as e:
            print(f"[WARN] Error reading {CONFIG_PATH}: {e}")
    return default_config

def get_model(weights_path):
    if weights_path in _LOADED_MODELS:
        return _LOADED_MODELS[weights_path]
    if not os.path.exists(weights_path):
        return None
    try:
        model = YOLO(weights_path)
        _LOADED_MODELS[weights_path] = model
        return model
    except Exception as e:
        print(f"[ERROR] Failed to load model from {weights_path}: {e}")
        return None

def compute_gradcam_overlay(yolo_model, orig_img_rgb):
    """
    Compute Grad-CAM activation heatmap for Ultralytics YOLO classification model.
    Returns: (overlay_bgr, affected_area_percent, top_idx, conf, pred_name)
    """
    orig_w, orig_h = orig_img_rgb.size

    # 1. Get canonical prediction and confidence directly from YOLO
    yolo_res = yolo_model.predict(orig_img_rgb, imgsz=224, verbose=False)[0]
    top_idx = int(yolo_res.probs.top1)
    conf = float(yolo_res.probs.top1conf)
    pred_name = yolo_model.names[top_idx]

    # 2. Setup Grad-CAM forward and backward pass
    torch_model = yolo_model.model
    torch_model.eval()
    for p in torch_model.parameters():
        p.requires_grad = True

    device = next(torch_model.parameters()).device
    img_resized = orig_img_rgb.resize((224, 224))
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))
    tensor = torch.tensor(arr, dtype=torch.float32, device=device, requires_grad=True).unsqueeze(0)

    feats = []
    def hook_fn(module, inp, outp):
        feats.append(outp)
        outp.retain_grad()

    target_layer = torch_model.model[9]
    handle = target_layer.register_forward_hook(hook_fn)

    try:
        with torch.enable_grad():
            out = torch_model(tensor)
            logits = out[0] if isinstance(out, (tuple, list)) else out
            score = logits[0, top_idx]
            torch_model.zero_grad()
            score.backward()

        f_map = feats[0]
        grads = f_map.grad
        if grads is not None:
            weights = torch.mean(grads, dim=(2, 3), keepdim=True)
            cam = torch.relu(torch.sum(weights * f_map, dim=1, keepdim=True))
        else:
            cam = torch.mean(f_map, dim=1, keepdim=True)

        cam = F.interpolate(cam, size=(orig_h, orig_w), mode='bilinear', align_corners=False)
        cam = cam.squeeze().detach().cpu().numpy()
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min + 1e-8)
        else:
            cam = np.zeros_like(cam)

        is_healthy = 'healthy' in pred_name.lower() or 'plant_leaf' in pred_name.lower()
        if is_healthy:
            # Low activation for healthy leaves
            affected_area = round(float(np.mean(cam > 0.70) * 100 * 0.1), 1)
        else:
            affected_mask = cam > 0.40
            affected_area = round(float(np.mean(affected_mask) * 100), 1)

        # Generate color heatmap
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        orig_bgr = cv2.cvtColor(np.array(orig_img_rgb), cv2.COLOR_RGB2BGR)

        # Blend
        overlay_bgr = cv2.addWeighted(orig_bgr, 0.65, heatmap, 0.35, 0)

        return overlay_bgr, affected_area, top_idx, conf, pred_name
    finally:
        handle.remove()

def format_display_name(class_name):
    """Format raw class name (e.g. Potato___Late_blight) into human readable label."""
    if '___' in class_name:
        crop_part, dis_part = class_name.split('___', 1)
        return f"{crop_part} {dis_part.replace('_', ' ').title()}"
    return class_name.replace('_', ' ').title()

AGRONOMIC_KNOWLEDGE = {
    "Wheat___Yellow_rust": {
        "disease_name_en": "Wheat Stripe / Yellow Rust (Puccinia striiformis)",
        "disease_name_hi": "गेहूं का पीला रतुआ (येलो रस्ट)",
        "symptoms_en": "Linear yellow-orange stripes of urediniospore pustules develop parallel to leaf veins. Pustules rupture the epidermis, causing rapid leaf drying.",
        "symptoms_hi": "पत्तियों की नसों के समानांतर चमकीली पीली-नारंगी धारियां और पाउडर जैसी फुंसियां। पत्तियों का तेजी से सूखना।",
        "organic_remedy_en": "Spray Neem seed kernel extract (NSKE 5%) or Trichoderma harzianum (5g/L). Dust sulfur (25 kg/ha) in early stage.",
        "organic_remedy_hi": "नीम बीज का अर्क (NSKE 5%) या ट्राइकोडर्मा हरजियनम (5 ग्राम/लीटर) का छिड़काव करें।",
        "chemical_treatment_en": "Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole 25.9% EC @ 1.25 ml/L at first appearance of yellow pustules.",
        "chemical_treatment_hi": "प्रोपिकोनाज़ोल 25% EC (टिल्ट) 1 मिली/लीटर अथवा टेबुकोनाज़ोल 1.25 मिली/लीटर पानी में मिलाकर स्प्रे करें।",
        "prevention_en": "Sow rust-resistant wheat varieties (HD-3086, DBW-187, DBW-222). Avoid excess nitrogen; avoid late sowing.",
        "prevention_hi": "प्रतिरोधी किस्में (HD-3086, DBW-187) बोएं। अत्यधिक यूरिया से बचें और समय पर बुवाई करें।"
    },
    "Wheat___healthy": {
        "disease_name_en": "Healthy Wheat Crop",
        "disease_name_hi": "स्वस्थ गेहूं की फसल",
        "symptoms_en": "Lush green foliage with uniform chlorophyll pigmentation, clean turgid leaves, and no pathogenic lesions.",
        "symptoms_hi": "पत्तियां पूरी तरह स्वस्थ, हरी-भरी और किसी भी प्रकार के रोग धब्बों से मुक्त हैं।",
        "organic_remedy_en": "Maintain soil organic matter with compost or vermicompost. Spray Panchagavya 3% as a plant growth tonic.",
        "organic_remedy_hi": "गोबर की खाद या वर्मीकम्पोस्ट डालें। वृद्धि के लिए 3% पंचगव्य का छिड़काव करें।",
        "chemical_treatment_en": "No chemical fungicide required. Maintain balanced NPK nutrition (120:60:40 kg/ha).",
        "chemical_treatment_hi": "किसी रासायनिक दवा की आवश्यकता नहीं है। संतुलित पोषक तत्व बनाए रखें।",
        "prevention_en": "Schedule regular field monitoring; ensure proper crown root initiation irrigation at 21 days.",
        "prevention_hi": "नियमित रूप से खेत की निगरानी करें और समय पर सिंचाई करें।"
    },
    "Cotton___Bacterial_blight": {
        "disease_name_en": "Cotton Bacterial Blight (Xanthomonas citri pv. malvacearum)",
        "disease_name_hi": "कपास का जीवाणु झुलसा (एंगुलर लीफ स्पॉट)",
        "symptoms_en": "Angular water-soaked leaf spots bounded by small veinlets, turning reddish-brown to dark black lesions. Can cause blackarm stage on stems.",
        "symptoms_hi": "पत्तियों की नसों से घिरे कोणीय जलसिक्त धब्बे जो बाद में गहरे भूरे/काले हो जाते हैं।",
        "organic_remedy_en": "Seed bio-priming with Pseudomonas fluorescens (10g/kg seed). Spray cow dung slurry filtrate (10%) with turmeric.",
        "organic_remedy_hi": "स्यूडोमोनास फ्लोरोसेंस (10 ग्राम/किग्रा) से बीजोपचार करें। नीम के तेल का छिड़काव करें।",
        "chemical_treatment_en": "Copper Oxychloride 50% WP (2.5 g/L) mixed with Streptocycline or Plantomycin (100 mg/L) sprayed twice at 12-day interval.",
        "chemical_treatment_hi": "कॉपर ऑक्सीक्लोराइड (2.5 ग्राम/लीटर) + स्ट्रेप्टोसाइक्लिन (100 मिग्रा/लीटर) का घोल बनाकर छिड़कें।",
        "prevention_en": "Acid delinting of cotton seeds; practice crop rotation with cereals; rogue out infected plant debris.",
        "prevention_hi": "प्रमाणित बीजों का उपयोग करें, फसल चक्र अपनाएं और संक्रमित अवशेष नष्ट करें।"
    },
    "Cotton___healthy": {
        "disease_name_en": "Healthy Cotton Leaf",
        "disease_name_hi": "स्वस्थ कपास की पत्ती",
        "symptoms_en": "Robust palmately lobed green leaves without angular water-soaking, necrotic veins, or curling.",
        "symptoms_hi": "पत्तियां सामान्य हरी, चमकदार और जीवाणु या कीट के प्रकोप से मुक्त हैं।",
        "organic_remedy_en": "Apply Jeevamrutha through irrigation; spray diluted cow urine (5%) as natural repellent.",
        "organic_remedy_hi": "जीवामृत का प्रयोग करें और नीम अर्क का हल्का छिड़काव रखें।",
        "chemical_treatment_en": "No chemical fungicide required. Monitor for sucking pests (whiteflies, thrips).",
        "chemical_treatment_hi": "किसी फफूंदनाशी की जरूरत नहीं। कीट निगरानी बनाए रखें।",
        "prevention_en": "Ensure adequate potassium nutrition to enhance natural plant defense mechanisms.",
        "prevention_hi": "पोटाश की उचित मात्रा दें ताकि पौधों की रोग प्रतिरोधक क्षमता मजबूत रहे।"
    },
    "Sugarcane___Red_rot": {
        "disease_name_en": "Sugarcane Red Rot (Colletotrichum falcatum)",
        "disease_name_hi": "गन्ने का लाल सड़न रोग (रेड रॉट)",
        "symptoms_en": "Yellowing and drying of crown leaves. Characteristic red discoloration of midrib with white cross-bands; internal stalk tissues show red pith with alcohol smell.",
        "symptoms_hi": "पत्तियों की मुख्य शिरा (मिडरिब) पर लाल रंग के धब्बे और सफेद आड़ी पट्टियां। तने को चीरने पर अंदर लाल गूदा।",
        "organic_remedy_en": "Dip setts in Trichoderma viride culture (10g/L) for 30 minutes before planting. Apply bio-fertilizers.",
        "organic_remedy_hi": "बुवाई से पूर्व गूलों को ट्राइकोडर्मा विरिडी (10 ग्राम/लीटर) के घोल में 30 मिनट उपचारित करें।",
        "chemical_treatment_en": "Carbendazim 50% WP (1g/L) or Thiophanate Methyl 70% WP (1g/L) sett dip treatment. Foliar spray of Carbendazim + Mancozeb (2g/L).",
        "chemical_treatment_hi": "कार्बेन्डाजिम (1 ग्राम/लीटर) घोल में गूलों का उपचार करें। खड़ी फसल में मैंकोजेब (2 ग्राम/लीटर) स्प्रे करें।",
        "prevention_en": "Use certified disease-free setts; implement hot water sett treatment at 52°C for 30 min; avoid ratoon of infected fields.",
        "prevention_hi": "स्वस्थ बीजों का चयन करें, 52°C गर्म पानी में 30 मिनट उपचार करें, रोगग्रस्त खेत में पेड़ी न लें।"
    },
    "Sugarcane___healthy": {
        "disease_name_en": "Healthy Sugarcane Foliage",
        "disease_name_hi": "स्वस्थ गन्ने की पत्ती",
        "symptoms_en": "Vibrant emerald green elongate leaves with clear white central midrib, free of lesions or spindle rot.",
        "symptoms_hi": "पत्तियां पूरी तरह हरी, चमकदार और मध्य शिरा साफ-सुथरी है।",
        "organic_remedy_en": "Incorporate pressmud compost or farmyard manure (FYM @ 10 t/ha).",
        "organic_remedy_hi": "प्रेसमड या सड़ी गोबर खाद डालें।",
        "chemical_treatment_en": "No chemical fungicide required. Apply nitrogen in splits to maintain vegetative vigor.",
        "chemical_treatment_hi": "किसी रासायनिक दवा की आवश्यकता नहीं।",
        "prevention_en": "Ensure proper field drainage during monsoon to prevent water stagnation.",
        "prevention_hi": "वर्षा के मौसम में जल निकासी की समुचित व्यवस्था रखें।"
    },
    "Potato___Late_blight": {
        "disease_name_en": "Potato Late Blight (Phytophthora infestans)",
        "disease_name_hi": "आलू का पिछेता झुलसा (लेट ब्लाइट)",
        "symptoms_en": "Irregular dark water-soaked lesions on leaf margins and tips, rapidly enlarging into purplish-brown necrotic patches. White cottony fungal growth on leaf undersides in high humidity.",
        "symptoms_hi": "पत्तियों के किनारों पर जलसिक्त धब्बे जो तेजी से गहरे कत्थई/काले हो जाते हैं। नमी में पत्ती के नीचे सफेद फफूंद।",
        "organic_remedy_en": "Foliar spray with Bordeaux mixture (1%) or copper hydroxide (2.5 g/L). Apply bio-formulations of Bacillus subtilis.",
        "organic_remedy_hi": "बोर्डो मिश्रण (1%) या कॉपर हाइड्रॉक्साइड (2.5 ग्राम/लीटर) का छिड़काव करें।",
        "chemical_treatment_en": "Cymoxanil 8% + Mancozeb 64% WP (Curzate @ 2.5 g/L) or Dimethomorph 50% WP (1g/L) + Mancozeb (2g/L).",
        "chemical_treatment_hi": "साइमोक्सानिल + मैंकोजेब (2.5 ग्राम/लीटर) अथवा डाइमेशोमॉर्फ (1 ग्राम/लीटर) का तुरंत छिड़काव करें।",
        "prevention_en": "Plant certified blight-resistant tubers (Kufri Pukhraj, Kufri Jyoti); destroy volunteer potatoes; avoid sprinkler irrigation.",
        "prevention_hi": "प्रमाणित बीज लगाएं, कतारों में मिट्टी चढ़ाएं और शाम को सिंचाई से बचें।"
    },
    "Potato___healthy": {
        "disease_name_en": "Healthy Potato Leaf",
        "disease_name_hi": "स्वस्थ आलू की पत्ती",
        "symptoms_en": "Compound dark green foliage without necrotic margins, purplish water-soaked edges, or wilt.",
        "symptoms_hi": "आलू की पत्तियां पूरी तरह स्वस्थ, हरी और किसी भी झुलसा या मोजैक रोग से मुक्त हैं।",
        "organic_remedy_en": "Apply vermiwash spray (5%) to boost foliar micronutrient absorption.",
        "organic_remedy_hi": "पोषक तत्वों के लिए वर्मीवाश (5%) का छिड़काव करें।",
        "chemical_treatment_en": "No chemical treatment required. Preventive spray of Mancozeb 75% WP (2 g/L) before foggy weather.",
        "chemical_treatment_hi": "रोग नहीं है। कोहरे वाले मौसम से पहले बचाव हेतु केवल हल्का मैंकोजेब छिड़क सकते हैं।",
        "prevention_en": "Maintain regular ridging and earthing up to protect tubers from surface exposure.",
        "prevention_hi": "उचित मिट्टी चढ़ाएं ताकि कंद सुरक्षित रहें।"
    },
    "Rice___Blast": {
        "disease_name_en": "Rice Leaf Blast (Magnaporthe oryzae / Pyricularia oryzae)",
        "disease_name_hi": "धान का झोंका / ब्लास्ट रोग",
        "symptoms_en": "Spindle-shaped / diamond-shaped lesions with grayish-white centers and dark brown or reddish borders. Lesions coalesce causing total leaf death (leaf blast).",
        "symptoms_hi": "पत्तियों पर आंख या नाव के आकार के धब्बे जिनका केंद्र धूसर-सफेद और किनारे भूरे-लाल होते हैं।",
        "organic_remedy_en": "Foliar spray with Pseudomonas fluorescens (0.2%) or Kasugamycin bio-ferment. Apply fermented butter-milk (chhaas) @ 5%.",
        "organic_remedy_hi": "स्यूडोमोनास फ्लोरोसेंस (2 ग्राम/लीटर) या खट्टी छाछ (5%) का छिड़काव करें।",
        "chemical_treatment_en": "Tricyclazole 75% WP (Beam @ 0.6 g/L) or Isoprothiolane 40% EC (1.5 ml/L) or Azoxystrobin + Difenoconazole (1 ml/L).",
        "chemical_treatment_hi": "ट्राइसाइक्लाजोल 75% WP (0.6 ग्राम/लीटर) अथवा आइसोप्रोपियोलेन (1.5 मिली/लीटर) पानी में घोलकर स्प्रे करें।",
        "prevention_en": "Avoid excessive nitrogen fertilizers; maintain standing water layer in paddy fields; burn infected straw.",
        "prevention_hi": "यूरिया का अत्यधिक उपयोग न करें, खेत में जल का स्तर बनाए रखें और रोगग्रस्त पुआल नष्ट करें।"
    },
    "Rice___healthy": {
        "disease_name_en": "Healthy Rice Leaf",
        "disease_name_hi": "स्वस्थ धान की पत्ती",
        "symptoms_en": "Uniform linear emerald green blade with sharp apex, free from spindle lesions or sheath rot.",
        "symptoms_hi": "पत्तियां पूरी तरह स्वस्थ, हरी और किसी भी धब्बे या झुलसा से रहित हैं।",
        "organic_remedy_en": "Apply Azospirillum and Phosphobacteria bio-fertilizers in root zone.",
        "organic_remedy_hi": "जड़ों में जैव उर्वरक (एज़ोस्पिरिलम) का प्रयोग करें।",
        "chemical_treatment_en": "No chemical fungicide required. Maintain balanced nitrogen-potash split application.",
        "chemical_treatment_hi": "किसी रासायनिक फफूंदनाशी की आवश्यकता नहीं।",
        "prevention_en": "Regularly scout borders; drain and re-flood fields periodically to aerate root system.",
        "prevention_hi": "खेत की नियमित जांच रखें और समय-समय पर पानी बदलते रहें।"
    },
    "Soybean___Rust": {
        "disease_name_en": "Soybean Rust (Phakopsora pachyrhizi)",
        "disease_name_hi": "सोयाबीन का गेरूई / रस्ट रोग",
        "symptoms_en": "Tiny chlorotic pinhead spots on upper leaf surface corresponding to raised brown/tan uredinia pustules on the lower leaf surface, leading to rapid defoliation.",
        "symptoms_hi": "पत्ती की निचली सतह पर छोटे भूरे-भूरे उभरे हुए फफोले (पस्ट्यूल्स) और समय से पहले पत्तों का झड़ना।",
        "organic_remedy_en": "Foliar spray with garlic bulb extract (5%) or Neem formulation (3000 ppm @ 3 ml/L).",
        "organic_remedy_hi": "लहसुन का अर्क (5%) या नीम का तेल (3 मिली/लीटर) का छिड़काव करें।",
        "chemical_treatment_en": "Hexaconazole 5% EC (2 ml/L) or Tebuconazole 25.9% EC (1.5 ml/L) or Propiconazole 25% EC (1 ml/L) at first sign.",
        "chemical_treatment_hi": "हेक्साकोनाज़ोल 5% EC (2 मिली/लीटर) या टेबुकोनाज़ोल (1.5 मिली/लीटर) का तुरंत छिड़काव करें।",
        "prevention_en": "Early sowing; wider row spacing (45 cm) for canopy aeration; rogue alternate legume hosts.",
        "prevention_hi": "उचित दूरी (45 सेमी) पर बुवाई करें ताकि हवा का आवागमन बना रहे।"
    },
    "Soybean___healthy": {
        "disease_name_en": "Healthy Soybean Leaf",
        "disease_name_hi": "स्वस्थ सोयाबीन की पत्ती",
        "symptoms_en": "Trifoliate rich green leaves with intact lamina and veins, showing no pustules or mosaic mottling.",
        "symptoms_hi": "सोयाबीन की पत्तियां पूरी तरह स्वस्थ, हरी और रोगमुक्त हैं।",
        "organic_remedy_en": "Inoculate seeds with Rhizobium japonicum before sowing for nitrogen fixation.",
        "organic_remedy_hi": "राइजोबियम कल्चर से बीजोपचार करें।",
        "chemical_treatment_en": "No chemical fungicide required.",
        "chemical_treatment_hi": "किसी रासायनिक दवा की आवश्यकता नहीं।",
        "prevention_en": "Maintain weed-free conditions during initial 45 days after sowing.",
        "prevention_hi": "शुरुआती 45 दिनों तक खेत को खरपतवार मुक्त रखें।"
    },
    "Potato___Early_blight": {
        "disease_name_en": "Potato Early Blight (Alternaria solani)",
        "disease_name_hi": "आलू का अगेती झुलसा (अल्टरनेरिया सोलेनाई)",
        "symptoms_en": "Dark brown to black necrotic spots with characteristic concentric rings (target board pattern) starting on older lower leaves. Surrounding tissue turns chlorotic yellow.",
        "symptoms_hi": "पत्तियों पर गहरे भूरे-काले संकेंद्री छल्ले (टारगेट बोर्ड जैसे छल्ले) बनते हैं। धब्बों के आसपास पत्ती पीली पड़ जाती है।",
        "organic_remedy_en": "Spray Trichoderma viride @ 5g/L or 5% neem seed kernel extract (NSKE). Apply copper soap spray.",
        "organic_remedy_hi": "ट्राइकोडर्मा विरिडी (5 ग्राम/लीटर) या नीम अर्क (5%) का छिड़काव करें। कॉपर सल्फेट आधारित जैव घोल उपयोगी है।",
        "chemical_treatment_en": "Mancozeb 75% WP @ 2.5 g/L or Chlorothalonil 75% WP @ 2 g/L. In severe cases, Azoxystrobin 23% SC @ 1 ml/L.",
        "chemical_treatment_hi": "मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या क्लोरोथैलोनिल (2 ग्राम/लीटर) का 10-12 दिन के अंतराल पर छिड़काव करें।",
        "prevention_en": "Practice 3-year crop rotation with non-solanaceous crops; maintain balanced nitrogen and potassium fertilization.",
        "prevention_hi": "3 वर्षीय फसल चक्र अपनाएं, संतुलित पोटाश दें और अत्यधिक नमी से बचें।"
    },
    "Rice___Brown_spot": {
        "disease_name_en": "Rice Brown Spot (Bipolaris oryzae / Helminthosporium oryzae)",
        "disease_name_hi": "धान का भूरा धब्बा रोग (ब्राउन स्पॉट)",
        "symptoms_en": "Small circular to oval brown spots with dark reddish-brown margins and grey or yellowish centers across leaf blades and glumes.",
        "symptoms_hi": "पत्तियों और दानों पर गोल अथवा अंडाकार भूरे धब्बे, जिनके केंद्र में धूसर व किनारों पर गहरा लाल-भूरा घेरा होता है।",
        "organic_remedy_en": "Seed treatment with Pseudomonas fluorescens @ 10g/kg. Foliar spray of fermented cow urine with neem extract.",
        "organic_remedy_hi": "स्यूडोमोनास फ्लोरोसेंस (10 ग्राम/किग्रा) से बीजोपचार करें। नीम अर्क युक्त जीवामृत का छिड़काव करें।",
        "chemical_treatment_en": "Propiconazole 25% EC @ 1 ml/L or Mancozeb 75% WP @ 2 g/L or Edifenphos 50% EC @ 1 ml/L.",
        "chemical_treatment_hi": "प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) या मैंकोज़ेब (2 ग्राम/लीटर) का छिड़काव करें।",
        "prevention_en": "Soil testing to correct nutrient deficiencies (especially potassium, zinc, and silicon); avoid drought stress.",
        "prevention_hi": "पोटाश व जिंक की कमी दूर करें; खेत में पर्याप्त नमी बनाए रखें।"
    },
    "Tomato___Early_blight": {
        "disease_name_en": "Tomato Early Blight (Alternaria solani)",
        "disease_name_hi": "टमाटर का अगेती झुलसा (अल्टरनेरिया)",
        "symptoms_en": "Brown to black lesions with concentric rings (target-like pattern) surrounded by a yellow halo on lower mature leaves, progressing upward.",
        "symptoms_hi": "निचली पुरानी पत्तियों पर संकेंद्री छल्लेदार (टारगेट बोर्ड) काले-भूरे धब्बे जिनके चारों ओर पीला घेरा होता है।",
        "organic_remedy_en": "Foliar spray with Bacillus subtilis @ 5g/L or copper oxychloride formulation with neem oil (3 ml/L).",
        "organic_remedy_hi": "बैसिलस सबटिलिस (5 ग्राम/लीटर) या कॉपर ऑक्सीक्लोराइड व नीम तेल का छिड़काव करें।",
        "chemical_treatment_en": "Chlorothalonil 75% WP @ 2 g/L or Difenoconazole 25% EC @ 0.5 ml/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L.",
        "chemical_treatment_hi": "क्लोरोथैलोनिल 75% WP (2 ग्राम/लीटर) या डाइफेनोकोनाज़ोल (0.5 मिली/लीटर) का छिड़काव करें।",
        "prevention_en": "Mulch soil around plants; stake tomato vines off the ground; avoid overhead sprinkler watering.",
        "prevention_hi": "मल्चिंग करें, पौधों को सहारा देकर जमीन से ऊपर रखें और ड्रिप सिंचाई का प्रयोग करें।"
    },
    "Tomato___Late_blight": {
        "disease_name_en": "Tomato Late Blight (Phytophthora infestans)",
        "disease_name_hi": "टमाटर का पछेती झुलसा (फाइटोफ्थोरा)",
        "symptoms_en": "Large irregular pale green to greasy water-soaked spots rapidly turning dark brown or black on leaves and stems. White downy mold on undersides in humid conditions.",
        "symptoms_hi": "पत्तियों और तनों पर तेजी से फैलने वाले काले-भूरे जलसिक्त धब्बे। अधिक नमी में पत्ती के नीचे सफेद फफूंद दिखती है।",
        "organic_remedy_en": "Bordeaux mixture 1% spray; preventive applications of Trichoderma harzianum or bio-copper.",
        "organic_remedy_hi": "बोर्डो मिश्रण 1% का छिड़काव करें। ट्राइकोडर्मा हरजिएनम का सुरक्षात्मक स्प्रे करें।",
        "chemical_treatment_en": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold @ 2.5 g/L) or Dimethomorph 50% WP @ 1 g/L.",
        "chemical_treatment_hi": "मेटालेक्सिल + मैंकोज़ेब (2.5 ग्राम/लीटर) या डाइमेशोमॉर्फ (1 ग्राम/लीटर) का तुरंत छिड़काव करें।",
        "prevention_en": "Destroy cull piles; maintain wide row spacing for good air circulation; use resistant hybrids.",
        "prevention_hi": "उचित दूरी पर रोपाई करें ताकि हवा का आवागमन बना रहे; रोगग्रस्त पौधों को तुरंत हटा दें।"
    },
    "Tomato___healthy": {
        "disease_name_en": "Healthy Tomato Plant",
        "disease_name_hi": "स्वस्थ टमाटर का पौधा",
        "symptoms_en": "Deep green compound leaves, firm turgid leaflets, healthy blossom clusters, free of blight spots, curl, or wilting.",
        "symptoms_hi": "पत्तियां गहरी हरी, मजबूत और किसी भी प्रकार के झुलसा, मरोड़िया या सड़न से पूर्णतः मुक्त हैं।",
        "organic_remedy_en": "Apply vermicompost and foliar spray Panchagavya 3% every 15 days.",
        "organic_remedy_hi": "वर्मीकम्पोस्ट और 3% पंचगव्य का नियमित छिड़काव रखें।",
        "chemical_treatment_en": "No chemical treatment required. Maintain balanced calcium and potassium fertilization to prevent blossom end rot.",
        "chemical_treatment_hi": "किसी रासायनिक दवा की जरूरत नहीं। कैल्शियम व पोटाश की संतुलित मात्रा दें।",
        "prevention_en": "Proper staking, pruning suckers, and uniform drip irrigation.",
        "prevention_hi": "उचित सहारा दें और नियमित ड्रिप सिंचाई बनाए रखें।"
    },
    "Corn___Common_rust": {
        "disease_name_en": "Corn Common Rust (Puccinia sorghi)",
        "disease_name_hi": "मक्का का कॉमन रस्ट (रतुआ रोग)",
        "symptoms_en": "Golden-brown to cinnamon-brown powdery pustules scattered prominently on both upper and lower leaf surfaces, erupting through leaf epidermis.",
        "symptoms_hi": "पत्तियों की दोनों सतहों पर सुनहरे-भूरे से दालचीनी जैसे रंग के फफोलेदार पाउडर वाले धब्बे बनते हैं।",
        "organic_remedy_en": "Spray fermented sour buttermilk (chhaas) @ 5% with garlic extract; apply bio-fungicide Bacillus amyloliquefaciens.",
        "organic_remedy_hi": "खट्टी छाछ (5%) व लहसुन का अर्क स्प्रे करें। जैव कवकनाशी बैसिलस का प्रयोग करें।",
        "chemical_treatment_en": "Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L or Pyraclostrobin 20% WG.",
        "chemical_treatment_hi": "मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या एजोक्सीस्ट्रोबिन + डाइफेनोकोनाज़ोल (1 मिली/लीटर) का छिड़काव करें।",
        "prevention_en": "Plant resistant maize hybrids; sow early in the season to escape late rust build-up.",
        "prevention_hi": "रोग प्रतिरोधी संकर बीज लगाएं और समय पर बुवाई करें।"
    },
    "Corn___Leaf_blight": {
        "disease_name_en": "Corn Leaf Blight / Northern Corn Leaf Blight (Exserohilum turcicum)",
        "disease_name_hi": "मक्का का पत्ती झुलसा (उत्तरी लीफ ब्लाइट)",
        "symptoms_en": "Long elliptical / cigar-shaped grayish-green to tan lesions parallel to leaf veins, expanding up to 15 cm and causing severe blighting of leaves.",
        "symptoms_hi": "पत्तियों पर सिगार के आकार के लंबे भूरे-धूसर धब्बे जो नसों के समानांतर बढ़ते हैं और पत्ती को सुखा देते हैं।",
        "organic_remedy_en": "Foliar spray with Trichoderma viride @ 5g/L or 5% neem seed kernel extract (NSKE).",
        "organic_remedy_hi": "ट्राइकोडर्मा विरिडी (5 ग्राम/लीटर) या 5% नीम के बीज का अर्क छिड़कें।",
        "chemical_treatment_en": "Mancozeb 75% WP @ 2.5 g/L or Propiconazole 25% EC @ 1 ml/L at first appearance of lesions.",
        "chemical_treatment_hi": "मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) का तुरंत छिड़काव करें।",
        "prevention_en": "Deep plow crop residues after harvest; practice 2-year crop rotation with non-grasses.",
        "prevention_hi": "कटाई के बाद गहरी जुताई करें और गैर-घास कुल की फसलों के साथ चक्र अपनाएं।"
    },
    "Corn___healthy": {
        "disease_name_en": "Healthy Corn / Maize Leaf",
        "disease_name_hi": "स्वस्थ मक्का की पत्ती",
        "symptoms_en": "Broad, vibrant green arching leaf blades with clean midribs and no rust pustules, blighting, or streaking.",
        "symptoms_hi": "पत्तियां पूरी तरह हरी, चमकदार, चौड़ी और किसी भी रतुआ या झुलसा रोग से मुक्त हैं।",
        "organic_remedy_en": "Apply Jeevamrutha through irrigation; spray zinc sulfate (0.5%) + lime to ensure micronutrient adequacy.",
        "organic_remedy_hi": "जीवामृत दें और जिंक सल्फेट (0.5%) का सुरक्षात्मक छिड़काव करें।",
        "chemical_treatment_en": "No chemical fungicide required. Maintain split nitrogen application (basal, knee-high, and tasseling stages).",
        "chemical_treatment_hi": "किसी रासायनिक दवा की जरूरत नहीं। संतुलित यूरिया तीन चरणों में दें।",
        "prevention_en": "Ensure proper field drainage and balanced NPK + zinc nutrition.",
        "prevention_hi": "खेत में जल निकास अच्छा रखें और जिंक की कमी न होने दें।"
    },
    "Apple___Scab": {
        "disease_name_en": "Apple Scab (Venturia inaequalis)",
        "disease_name_hi": "सेब का स्कैब रोग (वेन्चुरिया इनइक्वलिस)",
        "symptoms_en": "Olive-green to dull black velvety spots on leaf surfaces and fruit skins, with margins turning irregular and tissues puckering or curling.",
        "symptoms_hi": "पत्तियों और फलों पर जैतूनी-हरे से मखमली काले धब्बे बनते हैं, जिससे पत्तियां मुड़कर विकृत हो जाती हैं।",
        "organic_remedy_en": "Foliar spray with wettable sulfur @ 3g/L or lime-sulfur mixture during green tip stage; spray bio-formulation of Bacillus subtilis.",
        "organic_remedy_hi": "घुलनशील गंधक (3 ग्राम/लीटर) या चूना-गंधक का छिड़काव करें। बैसिलस सबटिलिस का प्रयोग करें।",
        "chemical_treatment_en": "Difenoconazole 25% EC @ 0.3 ml/L or Captan 50% WP @ 2.5 g/L or Dodine 65% WP @ 1 g/L.",
        "chemical_treatment_hi": "डाइफेनोकोनाज़ोल 25% EC (0.3 मिली/लीटर) या कैप्टान (2.5 ग्राम/लीटर) का छिड़काव करें।",
        "prevention_en": "Collect and destroy fallen leaf litter in autumn; prune tree canopy to maximize sunlight and airflow.",
        "prevention_hi": "पतझड़ में गिरी पत्तियां नष्ट करें और पेड़ों की उचित छंटाई करें ताकि धूप व हवा मिल सके।"
    },
    "Apple___healthy": {
        "disease_name_en": "Healthy Apple Foliage",
        "disease_name_hi": "स्वस्थ सेब की पत्ती",
        "symptoms_en": "Serrated, firm dark green leaves without velvety olive lesions, powdery coating, or rust spots.",
        "symptoms_hi": "पत्तियां पूरी तरह स्वस्थ, गहरे हरे रंग की और किसी भी प्रकार के स्कैब या फफूंद धब्बों से मुक्त हैं।",
        "organic_remedy_en": "Apply well-rotted farmyard manure and seaweed bio-extract as a foliar tonic.",
        "organic_remedy_hi": "सड़ी गोबर खाद और समुद्री शैवाल अर्क का छिड़काव करें।",
        "chemical_treatment_en": "No chemical treatment required. Apply regular horticultural mineral oil in dormant phase.",
        "chemical_treatment_hi": "रोग नहीं है। सुप्त अवस्था में केवल हॉर्टीकल्चरल मिनरल ऑयल का स्प्रे करें।",
        "prevention_en": "Annual winter pruning, tree sanitation, and balanced boron/calcium nutrition.",
        "prevention_hi": "सर्दियों में छंटाई और बोरॉन व कैल्शियम का उचित संतुलन रखें।"
    },
    "Grape___Black_rot": {
        "disease_name_en": "Grape Black Rot (Guignardia bidwellii / Phyllosticta ampelicida)",
        "disease_name_hi": "अंगूर का ब्लैक रॉट (काला सड़न रोग)",
        "symptoms_en": "Circular reddish-brown necrotic spots with distinct dark brown margins on leaves; tiny black speck-like pycnidia fruiting bodies embedded within lesions. Berries turn into hard black shriveled mummies.",
        "symptoms_hi": "पत्तियों पर लाल-भूरे गोल धब्बे जिनके किनारों पर गहरा भूरा घेरा और अंदर काले बिंदु होते हैं। अंगूर के दाने सूखकर काले पड़ जाते हैं।",
        "organic_remedy_en": "Bordeaux mixture 1% spray; foliar application of copper hydroxide @ 2 g/L or Trichoderma viride.",
        "organic_remedy_hi": "1% बोर्डो मिश्रण या कॉपर हाइड्रॉक्साइड (2 ग्राम/लीटर) का छिड़काव करें।",
        "chemical_treatment_en": "Mancozeb 75% WP @ 2.5 g/L or Myclobutanil 10% WP @ 1 g/L or Azoxystrobin 23% SC @ 1 ml/L.",
        "chemical_treatment_hi": "मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या माइक्लोबुटानिल (1 ग्राम/लीटर) का छिड़काव करें।",
        "prevention_en": "Prune out and burn all infected mummified berry clusters and dead canes; improve canopy aeration.",
        "prevention_hi": "सूखे रोगग्रस्त दानों और शाखाओं को काटकर जलाएं; बेलों में हवा का बहाव सुधारें।"
    },
    "Grape___healthy": {
        "disease_name_en": "Healthy Grape Leaf",
        "disease_name_hi": "स्वस्थ अंगूर की पत्ती",
        "symptoms_en": "Broad, intact palmately veined green grapevine leaves without necrotic brown spots, downy patches, or shriveled margins.",
        "symptoms_hi": "पत्तियां पूरी तरह हरी, चमकदार और किसी भी ब्लैक रॉट, डाउनी मिल्ड्यू या कीट प्रकोप से मुक्त हैं।",
        "organic_remedy_en": "Foliar spray with vermiwash (5%) and apply Trichoderma to root zone.",
        "organic_remedy_hi": "वर्मीवाश का छिड़काव करें और जड़ क्षेत्र में ट्राइकोडर्मा डालें।",
        "chemical_treatment_en": "No chemical treatment required. Maintain micronutrient spray schedule (magnesium and zinc).",
        "chemical_treatment_hi": "किसी रासायनिक दवा की जरूरत नहीं। मैग्नीशियम व जिंक का संतुलित पोषण रखें।",
        "prevention_en": "Canopy management through shoot thinning and trellising to avoid microclimatic humidity.",
        "prevention_hi": "बेलों की छंटाई और सही मचान व्यवस्था रखें ताकि अत्यधिक नमी न बने।"
    },
}

def analyze_plant_disease(image_bytes, crop_name="general"):
    """
    Main disease analysis entrypoint.
    1. Validates image bytes.
    2. Runs Not_A_Leaf model to detect out-of-domain objects.
    3. Runs crop-specific trained model with Grad-CAM visual highlighting.
    """
    if not TORCH_AVAILABLE:
        return {
            "success": False,
            "error": "TORCH_UNAVAILABLE",
            "message": "Neural network dependencies (PyTorch/YOLO) are not installed on this server instance."
        }
    cfg = load_config()

    try:
        orig_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception as e:
        return {
            "success": False,
            "error": f"Invalid image file: {str(e)}",
            "message": "Could not decode uploaded image."
        }

    # Normalize crop name
    clean_crop = crop_name.lower().strip() if crop_name else 'general'

    # Stage 1: Out-of-domain / Not_A_Leaf check
    nl_weights = cfg.get("not_a_leaf_model", "models/not_a_leaf/best.pt")
    if not os.path.isabs(nl_weights):
        nl_weights = os.path.join(os.path.dirname(__file__), nl_weights)

    nl_model = get_model(nl_weights)
    if nl_model:
        try:
            # Predict with Not_A_Leaf model
            nl_res = nl_model.predict(orig_img, imgsz=224, verbose=False)
            top1_idx = int(nl_res[0].probs.top1)
            pred_class = nl_model.names[top1_idx]
            nl_conf = float(nl_res[0].probs.top1conf)

            threshold = cfg.get("not_a_leaf_threshold", 0.50)
            if pred_class == "Not_A_Leaf" and nl_conf >= threshold:
                return {
                    "success": True,
                    "is_leaf": False,
                    "crop": clean_crop.capitalize(),
                    "prediction": "Not_A_Leaf",
                    "display_name": "Not A Plant Leaf",
                    "confidence": round(nl_conf, 4),
                    "affected_area_percent": 0.0,
                    "model_type": "classification",
                    "highlight_image": None,
                    "message": "No plant leaf detected. Please upload a clear photo of a crop leaf."
                }
        except Exception as e:
            print(f"[WARN] Error in Not_A_Leaf detection: {e}")

    CROP_ALIASES = {
        'corn / maize': 'corn',
        'corn/maize': 'corn',
        'maize': 'corn',
        'corn': 'corn',
        'wheat': 'wheat',
        'cotton': 'cotton',
        'sugarcane': 'sugarcane',
        'potato': 'potato',
        'rice': 'rice',
        'soybean': 'soybean',
        'tomato': 'tomato',
        'apple': 'apple',
        'grape': 'grape',
    }
    if clean_crop in CROP_ALIASES:
        clean_crop = CROP_ALIASES[clean_crop]

    # Stage 2: Check if requested crop is DATASET_NOT_READY
    not_ready = [c.lower() for c in cfg.get("not_ready_crops", [])]
    if clean_crop in not_ready:
        return {
            "success": False,
            "is_leaf": True,
            "crop": clean_crop.capitalize(),
            "prediction": "DATASET_NOT_READY",
            "display_name": f"{clean_crop.capitalize()} (Model Not Ready)",
            "confidence": 0.0,
            "affected_area_percent": 0.0,
            "model_type": "classification",
            "highlight_image": None,
            "message": f"Model for {clean_crop.capitalize()} is currently not ready."
        }

    # Stage 3: Load crop-specific model or Auto-Detect across all 10 crop models
    crop_weights_map = cfg.get("crop_models", {})
    crop_model = None
    crop_weights = None

    if clean_crop in ['general', 'auto', 'autodetect', 'auto_detect', 'all', '']:
        best_candidate = None
        best_score = -1.0
        for cand_crop in ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean', 'tomato', 'corn', 'apple', 'grape']:
            cand_weights = crop_weights_map.get(cand_crop, os.path.join(os.path.dirname(__file__), 'models', cand_crop, 'best.pt'))
            if not os.path.exists(cand_weights):
                continue
            c_model = get_model(cand_weights)
            if not c_model:
                continue
            try:
                res = c_model.predict(orig_img, imgsz=224, verbose=False)[0]
                top_i = int(res.probs.top1)
                c_conf = float(res.probs.top1conf)
                c_pred = c_model.names[top_i]
                is_c_healthy = 'healthy' in c_pred.lower()
                effective_score = c_conf if not is_c_healthy else (c_conf * 0.88)
                if effective_score > best_score:
                    best_score = effective_score
                    best_candidate = (cand_crop, cand_weights, c_model)
            except Exception as e:
                continue
        if best_candidate:
            clean_crop = best_candidate[0]
            crop_weights = best_candidate[1]
            crop_model = best_candidate[2]

    if not crop_model:
        crop_weights = crop_weights_map.get(clean_crop)
        if not crop_weights:
            cand = os.path.join(os.path.dirname(__file__), 'models', clean_crop, 'best.pt')
            if os.path.exists(cand):
                crop_weights = cand

        if not crop_weights or not os.path.exists(crop_weights):
            available_list = [k.capitalize() for k in crop_weights_map.keys() if os.path.exists(crop_weights_map[k])]
            return {
                "success": False,
                "is_leaf": True,
                "crop": clean_crop.capitalize(),
                "prediction": "MODEL_UNAVAILABLE",
                "display_name": f"{clean_crop.capitalize()} (Model Not Found)",
                "confidence": 0.0,
                "affected_area_percent": 0.0,
                "model_type": "classification",
                "highlight_image": None,
                "message": f"No trained model found for {clean_crop.capitalize()}. Available crops: {', '.join(available_list)}"
            }

        crop_model = get_model(crop_weights)
        if not crop_model:
            return {
                "success": False,
                "is_leaf": True,
                "crop": clean_crop.capitalize(),
                "error": "MODEL_LOAD_FAILED",
                "message": f"Failed to initialize neural network for {clean_crop.capitalize()}."
            }

    # Stage 4: Run Grad-CAM inference
    try:
        overlay_bgr, affected_area, top_idx, conf, pred_name = compute_gradcam_overlay(crop_model, orig_img)
        
        # Check low confidence
        min_conf = cfg.get("min_confidence_threshold", 0.35)
        is_low_conf = conf < min_conf

        display_name = format_display_name(pred_name)
        is_healthy = 'healthy' in pred_name.lower()

        if is_healthy:
            msg = f"{clean_crop.capitalize()} leaf appears healthy. No significant disease detected."
        else:
            msg = f"Disease identified: {display_name} with {conf * 100:.1f}% confidence."

        if is_low_conf:
            msg += " [Warning: Low model confidence. Please verify with a sharper close-up photograph.]"

        # Encode overlay to base64
        _, enc = cv2.imencode('.jpg', overlay_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
        b64_str = base64.b64encode(enc).decode('utf-8')
        highlight_data_url = f"data:image/jpeg;base64,{b64_str}"

        # Retrieve agronomic treatment info
        agro = AGRONOMIC_KNOWLEDGE.get(pred_name, {})
        severity_score = int(round(affected_area)) if not is_healthy else 0
        if severity_score > 60:
            sev_level = "High"
        elif severity_score > 25:
            sev_level = "Moderate"
        else:
            sev_level = "Low"

        ret = {
            "success": True,
            "status": "success",
            "crop": clean_crop.capitalize(),
            "prediction": pred_name,
            "display_name": display_name,
            "confidence": round(conf, 4),
            "affected_area_percent": affected_area,
            "is_leaf": True,
            "is_healthy": is_healthy,
            "model_type": "classification",
            "highlight_image": highlight_data_url,
            "message": msg,
            "severity_score": severity_score,
            "severity_level": sev_level,
            "disease_name_en": agro.get("disease_name_en", display_name),
            "disease_name_hi": agro.get("disease_name_hi", display_name),
            "symptoms_en": agro.get("symptoms_en", "Visual lesions observed on leaf surface."),
            "symptoms_hi": agro.get("symptoms_hi", "पत्ती पर रोग के लक्षण देखे गए हैं।"),
            "organic_remedy_en": agro.get("organic_remedy_en", "Apply organic bio-fungicide or neem-based spray."),
            "organic_remedy_hi": agro.get("organic_remedy_hi", "जैविक कीटनाशक या नीम का तेल का छिड़काव करें।"),
            "chemical_treatment_en": agro.get("chemical_treatment_en", "Consult local agricultural officer for approved fungicide."),
            "chemical_treatment_hi": agro.get("chemical_treatment_hi", "अनुशंसित फफूंदनाशी का छिड़काव करें।"),
            "prevention_en": agro.get("prevention_en", "Practice crop rotation and avoid excess nitrogen fertilization."),
            "prevention_hi": agro.get("prevention_hi", "फसल चक्र अपनाएं और संतुलित उर्वरक का प्रयोग करें।")
        }
        return ret
    except Exception as e:
        print(f"[ERROR] Inference error for {clean_crop}: {e}")
        return {
            "success": False,
            "is_leaf": True,
            "crop": clean_crop.capitalize(),
            "error": str(e),
            "message": f"Diagnostic inference failed: {str(e)}"
        }
