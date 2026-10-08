import json
import re

# Comprehensive dictionary of every string found in index.html
TRANSLATION_MAP = {
  "1 Hectare / 2.5 Acre)": "1 हेक्टेयर / 2.5 एकड़)",
  "1,250 Tonnes": "1,250 टन",
  "10 km": "10 किमी",
  "100 km": "100 किमी",
  "18 Schemes": "18 योजनाएं",
  "24/7 AI": "24/7 एआई",
  "24/7 Smart Advisor": "24/7 स्मार्ट परामर्शदाता",
  "25 km": "25 किमी",
  "28°C · Rain 0%": "28°C · बारिश 0%",
  "42% (Moderate)": "42% (मध्यम)",
  "50 km (Nearby)": "50 किमी (निकटतम)",
  "7-Day Trend": "7-दिवसीय रुझान",
  "95% Match": "95% उपयुक्त",
  "AI Disease Scanner": "एआई फसल रोग स्कैनर",
  "AI Engine": "एआई इंजन",
  "AI Kisan Assistant Bot": "किसान एआई सहायक बॉट",
  "AI recommendations and market information are decision-support tools. Verify critical agricultural decisions with local agricultural authorities and official sources.": "एआई सिफारिशें और मंडी भाव निर्णय सहायता उपकरण हैं। महत्वपूर्ण निर्णयों के लिए स्थानीय कृषि अधिकारियों से परामर्श करें।",
  "APMC Yard": "कृषि उपज मंडी (APMC)",
  "Acre (एकड़)": "एकड़",
  "Affected Area: 0%": "प्रभावित क्षेत्र: 0%",
  "Agronomy": "सस्य विज्ञान (एग्रोनॉमी)",
  "All Available": "सभी उपलब्ध",
  "All States (Central Schemes)": "सभी राज्य (केंद्रीय योजनाएं)",
  "Alluvial / Loam": "जलोढ़ / दोमट",
  "Alluvial / Loam Soil (जलोढ़ / दोमट मिट्टी)": "जलोढ़ / दोमट मिट्टी",
  "Alluvial Soil": "जलोढ़ मिट्टी",
  "Analyzing humidity & temperature...": "आर्द्रता एवं तापमान का विश्लेषण जारी...",
  "Analyzing live weather data...": "लाइव मौसम डेटा का विश्लेषण जारी...",
  "Ask AI Bot about Selling Here →": "यहाँ बेचने के बारे में एआई से पूछें →",
  "Ask with 1-Click:": "1-क्लिक में पूछें:",
  "Balanced nutrition guidance loaded.": "संतुलित पोषण मार्गदर्शन लोड हुआ।",
  "Bhopal (462001)": "भोपाल (462001)",
  "Bigha (बीघा)": "बीघा",
  "Bihar": "बिहार",
  "Black Soil (काली / चिकनी मिट्टी)": "काली / चिकनी मिट्टी",
  "Browse Files": "फाइल चुनें",
  "Calculate exact bag requirements for Urea, DAP, MOP, and bio-fertilizers customized to your field size.": "अपने खेत के क्षेत्रफल अनुसार यूरिया, डीएपी, एमओपी और जैविक खादों की सटीक बोरियों की आवश्यकता जानें।",
  "Canal (नहर)": "नहर",
  "Category": "श्रेणी",
  "Center plant leaf inside frame": "पत्ती को फ्रेम के बीच में रखें",
  "Central": "केंद्रीय",
  "Checking wind & spray suitability...": "हवा की गति और छिड़काव की अनुकूलता जांची जा रही है...",
  "Checking...": "जांच जारी...",
  "Clay / Heavy Soil (मटियार मिट्टी)": "मटियार / भारी मिट्टी",
  "Clear Sky · 10% Rain Risk": "साफ आसमान · 10% बारिश का जोखिम",
  "Click any leaf to run instant AI vision scan": "तुरंत एआई जांच के लिए किसी भी पत्ती पर क्लिक करें",
  "Close": "बंद करें",
  "Closest Distance 📍": "निकटतम दूरी 📍",
  "Common Rust": "सामान्य रतुआ",
  "Compare prices across Unnao, Bindki, Fatehpur, and Lucknow APMC yards within 50 km.": "50 किमी के भीतर उन्नाव, बिंदकी, फतेहपुर और लखनऊ मंडियों के भावों की तुलना करें।",
  "Concentrated target-board brown spots observed on foliage.": "पत्तियों पर संकेंद्रित छल्लेदार भूरे धब्बे देखे गए।",
  "Crop & Fertilizer Advisor": "फसल एवं उर्वरक सलाहकार",
  "Crop & Stage:": "फसल एवं अवस्था:",
  "Crop: Wheat": "फसल: गेहूं",
  "Daily Arrival": "दैनिक आवक",
  "Detects 38+ plant diseases with chemical & organic spray schedules": "38+ फसल रोगों की पहचान और रासायनिक व जैविक छिड़काव कार्यक्रम",
  "Early Blight": "अगेती झुलसा",
  "Favorable weather for field operations today. Light irrigation recommended before upcoming sunny intervals.": "आज कृषि कार्यों के लिए मौसम अनुकूल है। धूप खिलने से पहले हल्की सिंचाई की सलाह दी जाती है।",
  "Good Morning, Farmer 👋": "सुप्रभात, अन्नदाता किसान साथी 👋",
  "Good Afternoon, Farmer 👋": "शुभ दोपहर, किसान साथी 👋",
  "Good Evening, Farmer 👋": "शुभ संध्या, किसान साथी 👋",
  "Here is today's real-time agricultural intelligence for your active landholding.": "यहाँ आपकी सक्रिय कृषि भूमि के लिए आज की रीयल-टाइम कृषि सलाह, मौसम और मंडी भाव हैं।",
  "Instant diagnosis for Blight, Rust, Rot & Mildew": "झुलसा, रतुआ, सड़न और फफूंद का तुरंत निदान",
  "Live": "लाइव",
  "Live Weather & Forecast": "लाइव मौसम एवं पूर्वानुमान",
  "Loading Location...": "स्थान लोड हो रहा है...",
  "Loading weather data...": "मौसम डेटा लोड हो रहा है...",
  "MSP: ₹2,275 · (+₹116 Premium)": "एमएसपी: ₹2,275 · (+₹116 अधिक)",
  "Market": "मंडी बाजार",
  "Nitrogen Top-Dressing (Urea)": "नाइट्रोजन टॉप-ड्रेसिंग (यूरिया)",
  "Nutrient Focus:": "पोषक तत्व प्राथमिकता:",
  "PM-KISAN & PMFBY": "पीएम-किसान एवं फसल बीमा",
  "Prune lower diseased foliage and ensure proper plant spacing.": "रोगग्रस्त निचली पत्तियों को छांटें और पौधों के बीच उचित दूरी रखें।",
  "Soil Type:": "मिट्टी का प्रकार:",
  "Spray Copper Oxychloride 3g/L or Mancozeb 2g/L.": "कॉपर ऑक्सीक्लोराइड 3 ग्राम/लीटर या मैंकोज़ेब 2 ग्राम/लीटर का छिड़काव करें।",
  "Spray Neem oil 5ml/L or Trichoderma viride.": "नीम का तेल 5 मिली/लीटर या ट्राइकोडर्मा विरिडी का छिड़काव करें।",
  "Supports Voice Input in Hindi, English & Hinglish": "हिंदी, अंग्रेजी और हिंग्लिश में वॉयस इनपुट समर्थित",
  "Vision AI": "विजन एआई",
  "Wheat · Kanpur APMC": "गेहूं · कानपुर मंडी",
  "Wheat (Vegetative)": "गेहूं (वानस्पतिक अवस्था)",
  "₹6,000/yr direct income support & comprehensive crop loss compensation at 1.5–2% premium.": "₹6,000/वर्ष प्रत्यक्ष आय सहायता एवं 1.5–2% प्रीमियम पर व्यापक फसल सुरक्षा बीमा।",
  "🚜 Tractor Subsidy": "🚜 ट्रैक्टर सब्सिडी",
  "☀️ Solar Pumps": "☀️ सोलर पंप",
  "💳 KCC Loans": "💳 केसीसी ऋण",
  "🌾 आज सिंचाई या दवा छिड़काव करें?": "🌾 आज सिंचाई या दवा छिड़काव करें?",
  "🚜 ट्रैक्टर व कृषि यंत्रों पर सब्सिडी कैसे मिलेगी?": "🚜 ट्रैक्टर व कृषि यंत्रों पर सब्सिडी कैसे मिलेगी?",
  "Feels like: --°C": "महसूस: --°C",
  "Fetching location...": "स्थान प्राप्त किया जा रहा है...",
  "Today": "आज",
  "Today's Mandi Rate": "आज का मंडी भाव",
  "High Severity": "गंभीर संक्रमण",
  "Moderate Severity": "मध्यम संक्रमण",
  "Low Severity": "हल्का संक्रमण",
  "Healthy Leaf": "स्वस्थ पत्ती",
  "Clear": "हटाएं",
  "Search": "खोजें",
  "Search Mandi": "मंडी खोजें",
  "Search Schemes": "योजनाएं खोजें",
  "Weather Intelligence": "मौसम पूर्वानुमान",
  "AI Disease Scanner": "एआई फसल रोग स्कैनर",
  "Fertilizer Advisor": "उर्वरक सलाह",
  "Mandi Prices": "मंडी भाव",
  "Govt Schemes": "सरकारी योजनाएं",
  "AI Kisan Bot": "किसान एआई बॉट",
  "Dashboard": "डैशबोर्ड",
  "Weather": "मौसम"
}

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace plain texts with data-lang attributes
count = 0
for en_text, hi_text in TRANSLATION_MAP.items():
    # Only replace if not already wrapped in data-lang-en
    # Try exact match with tag: e.g. >en_text<
    pattern1 = f'>{en_text}<'
    if pattern1 in html:
        replacement1 = f' data-lang-en="{en_text}" data-lang-hi="{hi_text}">{en_text}<'
        # Wait, if we replace >text< with <span ...>text</span>
        # It's cleaner to replace >text< with ><span data-lang-en="{en_text}" data-lang-hi="{hi_text}">{en_text}</span><
        html = html.replace(pattern1, f'><span data-lang-en="{en_text}" data-lang-hi="{hi_text}">{en_text}</span><')
        count += 1

print(f"Applied {count} translation tags to index.html!")

# Save to all locations
paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]
for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved: {p} ({len(html)} bytes)")
