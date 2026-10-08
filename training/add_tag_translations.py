import re
import os

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map of ID -> (en, hi)
ID_TRANSLATIONS = {
    'dashboardGreeting': ("Good Morning, Farmer 👋", "सुप्रभात, किसान साथी 👋"),
    'dashboardSubtext': ("Here is today's real-time agricultural intelligence for your active landholding.", "यहाँ आपकी सक्रिय कृषि भूमि के लिए आज की रीयल-टाइम कृषि सलाह और मौसम जानकारी है।"),
    'dashWeatherGlanceText': ("🌤 28°C · Clear Sky", "🌤 28°C · साफ आसमान"),
    'dashWeatherConditionText': ("Clear Sky · 10% Rain Risk", "साफ आसमान · 10% बारिश का जोखिम"),
    'dashWeatherAdvisorySnippet': ("Favorable weather for field operations today. Light irrigation recommended before upcoming sunny intervals.", "आज कृषि कार्यों के लिए मौसम अनुकूल है। धूप खिलने से पहले हल्की सिंचाई की सलाह दी जाती है।"),
    'pincodeBadgeText': ("Location...", "स्थान..."),
    'currentLocationName': ("Fetching location...", "स्थान प्राप्त किया जा रहा है..."),
    'currentDateText': ("Today", "आज"),
    'weatherConditionText': ("Loading weather data...", "मौसम डेटा लोड हो रहा है..."),
    'feelsLikeText': ("Feels like: --°C", "महसूस: --°C"),
    'sprayStatus': ("Checking...", "जांच जारी..."),
    'advisoryCropName': ("Wheat", "गेहूं"),
    'diagAffectedAreaBadge': ("Affected Area: 0%", "प्रभावित क्षेत्र: 0%"),
    'diagSymptomsText': ("Concentrated target-board brown spots observed on foliage.", "पत्तियों पर संकेंद्रित छल्लेदार भूरे धब्बे देखे गए।"),
    'diagOrganicText': ("Spray Neem oil 5ml/L or Trichoderma viride.", "नीम का तेल 5 मिली/लीटर या ट्राइकोडर्मा विरिडी का छिड़काव करें।"),
    'diagChemicalText': ("Spray Copper Oxychloride 3g/L or Mancozeb 2g/L.", "कॉपर ऑक्सीक्लोराइड 3 ग्राम/लीटर या मैंकोज़ेब 2 ग्राम/लीटर का छिड़काव करें।"),
    'diagPreventionText': ("Prune lower diseased foliage and ensure proper plant spacing.", "रोगग्रस्त निचली पत्तियों को छांटें और पौधों के बीच उचित दूरी रखें।"),
    'diagSeverityPercentText': ("42% (Moderate)", "42% (मध्यम)"),
    'locationTitle': ("Loading Location...", "स्थान लोड हो रहा है..."),
    'locationSubtext': ("State: -- | District: -- | Block: --", "राज्य: -- | जिला: -- | ब्लॉक: --")
}

for elem_id, (en_val, hi_val) in ID_TRANSLATIONS.items():
    # Find tag with this id
    pattern = rf'(<[a-zA-Z0-9]+[^>]*\bid=["\']{elem_id}["\'][^>]*)(>)'
    def replacer(m):
        tag_start = m.group(1)
        if 'data-lang-en' not in tag_start:
            return f'{tag_start} data-lang-en="{en_val}" data-lang-hi="{hi_val}">'
        return m.group(0)
    html = re.sub(pattern, replacer, html)

# Global Text Replacements on tags
TEXT_REPLACEMENTS = [
    # Top Navbar Logo & Header
    (r'<span class="text-lg font-extrabold[^>]*>SAP</span>', '<span class="text-lg font-extrabold bg-gradient-to-r from-emerald-700 to-teal-600 dark:from-emerald-400 dark:to-teal-300 bg-clip-text text-transparent" data-lang-en="SAP" data-lang-hi="एसएपी">SAP</span>'),
    
    # Dashboard Card 1: Weather Glance
    (r'<span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Live</span>', '<span class="text-xs font-bold text-slate-500 uppercase tracking-wider" data-lang-en="Live" data-lang-hi="लाइव">Live</span>'),
    (r'<span class="text-xs font-bold uppercase tracking-wider text-emerald-400">Live Weather & Forecast</span>', '<span class="text-xs font-bold uppercase tracking-wider text-emerald-400" data-lang-en="Live Weather & Forecast" data-lang-hi="लाइव मौसम एवं पूर्वानुमान">Live Weather & Forecast</span>'),

    # Dashboard Card 2: AI Vision
    (r'<span class="text-xs font-bold uppercase tracking-wider text-emerald-400">Vision AI</span>', '<span class="text-xs font-bold uppercase tracking-wider text-emerald-400" data-lang-en="Vision AI" data-lang-hi="विजन एआई">Vision AI</span>'),
    (r'<div class="text-base font-extrabold text-white">Instant diagnosis for Blight, Rust, Rot & Mildew</div>', '<div class="text-base font-extrabold text-white" data-lang-en="Instant diagnosis for Blight, Rust, Rot & Mildew" data-lang-hi="झुलसा, रतुआ, सड़न और फफूंद का तुरंत निदान">Instant diagnosis for Blight, Rust, Rot & Mildew</div>'),
    (r'<span class="text-xs text-slate-300">Detects 38\+ plant diseases with chemical & organic spray schedules</span>', '<span class="text-xs text-slate-300" data-lang-en="Detects 38+ plant diseases with chemical & organic spray schedules" data-lang-hi="38+ फसल रोगों की पहचान और रासायनिक व जैविक छिड़काव कार्यक्रम">Detects 38+ plant diseases with chemical & organic spray schedules</span>'),

    # Dashboard Card 3: Agronomy & Fertilizer
    (r'<span class="text-xs font-bold uppercase tracking-wider text-indigo-400">Agronomy</span>', '<span class="text-xs font-bold uppercase tracking-wider text-indigo-400" data-lang-en="Agronomy" data-lang-hi="सस्य विज्ञान">Agronomy</span>'),
    (r'<span class="text-slate-400">Crop & Stage:</span>', '<span class="text-slate-400" data-lang-en="Crop & Stage:" data-lang-hi="फसल एवं अवस्था:">Crop & Stage:</span>'),
    (r'<span class="text-slate-400">Soil Type:</span>', '<span class="text-slate-400" data-lang-en="Soil Type:" data-lang-hi="मिट्टी का प्रकार:">Soil Type:</span>'),
    (r'<span class="text-slate-400">Nutrient Focus:</span>', '<span class="text-slate-400" data-lang-en="Nutrient Focus:" data-lang-hi="पोषक तत्व प्राथमिकता:">Nutrient Focus:</span>'),
    (r'<span class="font-bold text-slate-200">Wheat \(Vegetative\)</span>', '<span class="font-bold text-slate-200" data-lang-en="Wheat (Vegetative)" data-lang-hi="गेहूं (वानस्पतिक)">Wheat (Vegetative)</span>'),
    (r'<span class="font-bold text-slate-200">Alluvial / Loam</span>', '<span class="font-bold text-slate-200" data-lang-en="Alluvial / Loam" data-lang-hi="जलोढ़ / दोमट">Alluvial / Loam</span>'),
    (r'<span class="font-bold text-slate-200">Nitrogen Top-Dressing \(Urea\)</span>', '<span class="font-bold text-slate-200" data-lang-en="Nitrogen Top-Dressing (Urea)" data-lang-hi="यूरिया छिड़काव (नाइट्रोजन)">Nitrogen Top-Dressing (Urea)</span>'),
    (r'<p class="text-xs text-slate-300">Calculate exact bag requirements for Urea, DAP, MOP, and bio-fertilizers customized to your field size\.</p>', '<p class="text-xs text-slate-300" data-lang-en="Calculate exact bag requirements for Urea, DAP, MOP, and bio-fertilizers customized to your field size." data-lang-hi="अपने खेत के क्षेत्रफल अनुसार यूरिया, डीएपी, एमओपी और जैविक खादों की सटीक बोरियों की आवश्यकता जानें।">Calculate exact bag requirements for Urea, DAP, MOP, and bio-fertilizers customized to your field size.</p>'),

    # Dashboard Card 4: Market
    (r'<span class="text-xs font-bold uppercase tracking-wider text-blue-400">Market</span>', '<span class="text-xs font-bold uppercase tracking-wider text-blue-400" data-lang-en="Market" data-lang-hi="मंडी">Market</span>'),
    (r'<span class="text-sm font-extrabold text-white">Wheat · Kanpur APMC</span>', '<span class="text-sm font-extrabold text-white" data-lang-en="Wheat · Kanpur APMC" data-lang-hi="गेहूं · कानपुर मंडी">Wheat · Kanpur APMC</span>'),
    (r'<div class="text-xs text-slate-300 mt-1">MSP: ₹2,275 · \(\+₹116 Premium\)</div>', '<div class="text-xs text-slate-300 mt-1" data-lang-en="MSP: ₹2,275 · (+₹116 Premium)" data-lang-hi="एमएसपी: ₹2,275 · (+₹116 अधिक)">MSP: ₹2,275 · (+₹116 Premium)</div>'),
    (r'<span class="text-xs text-slate-300">7-Day Trend</span>', '<span class="text-xs text-slate-300" data-lang-en="7-Day Trend" data-lang-hi="7-दिवसीय रुझान">7-Day Trend</span>'),
    (r'<p class="text-xs text-slate-300">Compare prices across Unnao, Bindki, Fatehpur, and Lucknow APMC yards within 50 km\.</p>', '<p class="text-xs text-slate-300" data-lang-en="Compare prices across Unnao, Bindki, Fatehpur, and Lucknow APMC yards within 50 km." data-lang-hi="50 किमी के भीतर उन्नाव, बिंदकी, फतेहपुर और लखनऊ मंडियों के भावों की तुलना करें।">Compare prices across Unnao, Bindki, Fatehpur, and Lucknow APMC yards within 50 km.</p>'),

    # Dashboard Card 5: Schemes
    (r'<span class="text-xs font-bold uppercase tracking-wider text-teal-400">18 Schemes</span>', '<span class="text-xs font-bold uppercase tracking-wider text-teal-400" data-lang-en="18 Schemes" data-lang-hi="18 योजनाएं">18 Schemes</span>'),
    (r'<span class="text-sm font-extrabold text-white">PM-KISAN & PMFBY</span>', '<span class="text-sm font-extrabold text-white" data-lang-en="PM-KISAN & PMFBY" data-lang-hi="पीएम-किसान एवं फसल बीमा">PM-KISAN & PMFBY</span>'),
    (r'<span class="text-xs text-emerald-400 font-bold bg-emerald-500/20 px-2 py-0\.5 rounded-full">95% Match</span>', '<span class="text-xs text-emerald-400 font-bold bg-emerald-500/20 px-2 py-0.5 rounded-full" data-lang-en="95% Match" data-lang-hi="95% उपयुक्त">95% Match</span>'),
    (r'<div class="text-xs text-slate-300 leading-relaxed">₹6,000/yr direct income support & comprehensive crop loss compensation at 1\.5–2% premium\.</div>', '<div class="text-xs text-slate-300 leading-relaxed" data-lang-en="₹6,000/yr direct income support & comprehensive crop loss compensation at 1.5–2% premium." data-lang-hi="₹6,000/वर्ष प्रत्यक्ष आय सहायता एवं 1.5–2% प्रीमियम पर व्यापक फसल सुरक्षा बीमा।">₹6,000/yr direct income support & comprehensive crop loss compensation at 1.5–2% premium.</div>'),

    # Dashboard Card 6: AI Kisan Bot Quick Card
    (r'<span class="text-xs font-bold uppercase tracking-wider text-violet-400">24/7 AI</span>', '<span class="text-xs font-bold uppercase tracking-wider text-violet-400" data-lang-en="24/7 AI" data-lang-hi="24/7 एआई">24/7 AI</span>'),
    (r'<span class="text-xs font-bold text-slate-300">Ask with 1-Click:</span>', '<span class="text-xs font-bold text-slate-300" data-lang-en="Ask with 1-Click:" data-lang-hi="1-क्लिक में पूछें:">Ask with 1-Click:</span>'),
    (r'<span class="text-xs text-slate-400">Supports Voice Input in Hindi, English & Hinglish</span>', '<span class="text-xs text-slate-400" data-lang-en="Supports Voice Input in Hindi, English & Hinglish" data-lang-hi="हिंदी, अंग्रेजी और हिंग्लिश में वॉयस इनपुट समर्थित">Supports Voice Input in Hindi, English & Hinglish</span>'),

    # Test Sample Leaves (Buttons in Scanner)
    (r'<span class="text-\[11px\] font-bold text-slate-800 dark:text-slate-200 block truncate w-full">🥔 Potato Blight</span>', '<span class="text-[11px] font-bold text-slate-800 dark:text-slate-200 block truncate w-full" data-lang-en="🥔 Potato Blight" data-lang-hi="🥔 आलू झुलसा">🥔 Potato Blight</span>'),
    (r'<span class="text-\[9px\] text-emerald-600 dark:text-emerald-400 font-semibold">Early Blight</span>', '<span class="text-[9px] text-emerald-600 dark:text-emerald-400 font-semibold" data-lang-en="Early Blight" data-lang-hi="अगेती झुलसा">Early Blight</span>'),
    (r'<span class="text-\[11px\] font-bold text-slate-800 dark:text-slate-200 block truncate w-full">🥔 Late Blight</span>', '<span class="text-[11px] font-bold text-slate-800 dark:text-slate-200 block truncate w-full" data-lang-en="🥔 Late Blight" data-lang-hi="🥔 पछेती झुलसा">🥔 Late Blight</span>'),
    (r'<span class="text-\[9px\] text-rose-500 font-semibold">High Severity</span>', '<span class="text-[9px] text-rose-500 font-semibold" data-lang-en="High Severity" data-lang-hi="गंभीर संक्रमण">High Severity</span>'),
    (r'<span class="text-\[11px\] font-bold text-slate-800 dark:text-slate-200 block truncate w-full">🌽 Corn Rust</span>', '<span class="text-[11px] font-bold text-slate-800 dark:text-slate-200 block truncate w-full" data-lang-en="🌽 Corn Rust" data-lang-hi="🌽 मक्का रतुआ">🌽 Corn Rust</span>'),
    (r'<span class="text-\[9px\] text-amber-500 font-semibold">Common Rust</span>', '<span class="text-[9px] text-amber-500 font-semibold" data-lang-en="Common Rust" data-lang-hi="सामान्य रतुआ">Common Rust</span>'),
    (r'<span class="text-\[11px\] font-bold text-slate-800 dark:text-slate-200 block truncate w-full">🌽 Leaf Blight</span>', '<span class="text-[11px] font-bold text-slate-800 dark:text-slate-200 block truncate w-full" data-lang-en="🌽 Leaf Blight" data-lang-hi="🌽 पत्ती झुलसा">🌽 Leaf Blight</span>'),
    (r'<span class="text-\[9px\] text-indigo-500 font-semibold">Northern Blight</span>', '<span class="text-[9px] text-indigo-500 font-semibold" data-lang-en="Northern Blight" data-lang-hi="उत्तरी झुलसा">Northern Blight</span>'),
    (r'<span class="text-\[11px\] font-bold text-slate-800 dark:text-slate-200 block truncate w-full">🎋 Sugarcane</span>', '<span class="text-[11px] font-bold text-slate-800 dark:text-slate-200 block truncate w-full" data-lang-en="🎋 Sugarcane" data-lang-hi="🎋 गन्ना">🎋 Sugarcane</span>'),
    (r'<span class="text-\[9px\] text-rose-600 font-semibold">Red Rot</span>', '<span class="text-[9px] text-rose-600 font-semibold" data-lang-en="Red Rot" data-lang-hi="लाल सड़न (रेड रॉट)">Red Rot</span>'),

    # Browse & Launch Buttons in Scanner
    (r'<span class="badge-emerald inline-flex items-center">\s*<i class="fa-solid fa-folder-open mr-1\.5"></i> Browse Files\s*</span>', '<span class="badge-emerald inline-flex items-center"><i class="fa-solid fa-folder-open mr-1.5"></i> <span data-lang-en="Browse Files" data-lang-hi="फाइल चुनें">Browse Files</span></span>'),
    (r'<span class="badge-emerald inline-flex items-center">\s*<i class="fa-solid fa-video mr-1\.5"></i> Launch Camera\s*</span>', '<span class="badge-emerald inline-flex items-center"><i class="fa-solid fa-video mr-1.5"></i> <span data-lang-en="Launch Camera" data-lang-hi="कैमरा चालू करें">Launch Camera</span></span>'),

    # Print button title
    (r'title="Print Certificate"', 'title="Print Certificate" data-lang-en="Print Certificate" data-lang-hi="रिपोर्ट प्रिंट करें"'),

    # Top Navbar Language Button
    (r'<span id="langBtnText">हिंदी</span>', '<span id="langBtnText">हिंदी</span>')
]

for pat, repl in TEXT_REPLACEMENTS:
    html = re.sub(pat, repl, html)

# Write to all paths
paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]
for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated: {p} ({len(html)} bytes)")

print("Successfully applied full tag-level translations!")
