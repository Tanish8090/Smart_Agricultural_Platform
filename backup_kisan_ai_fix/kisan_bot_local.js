/**
 * Smart Agriculture Platform (SAP) — Local Kisan AI Assistant
 * 100% On-Device Local Agricultural Knowledge & Advisory Engine
 * Operates offline / airplane-mode with zero latency.
 * Delivers expert agronomic advisory in fluent Devanagari Hindi & English.
 */

// Comprehensive offline agricultural knowledge base
const LOCAL_KISAN_KNOWLEDGE = {
  crops: {
    wheat: {
      name_en: "Wheat",
      name_hi: "गेहूं",
      cultivation: {
        en: `🌾 **Complete Wheat Cultivation Guide:**
1. **Soil & Climate:** Well-drained fertile loam or clay loam soil with pH 6.5–7.5. Cool growing season (15–20°C) with bright sunny days during grain filling.
2. **Sowing Time:** Optimal window is November 1 to November 25. Late sowing beyond Dec 1 reduces yield significantly.
3. **Seed Rate & Treatment:** 100 kg/ha (40 kg/acre) for timely sown; 125 kg/ha for late sown. Treat seed with Carbendazim 50% WP @ 2g/kg or Trichoderma @ 5g/kg seed.
4. **Spacing:** 20–22.5 cm between rows, depth 4–5 cm.
5. **Fertilizer (NPK 120:60:40 kg/ha):**
   - Basal at sowing: 1/3rd Nitrogen (Urea), full Phosphorus (DAP/SSP), full Potash (MOP).
   - 1st Top Dressing: 1/3rd Urea at first CRI irrigation (21–25 days).
   - 2nd Top Dressing: Remaining 1/3rd Urea at tillering (40–45 days).
   - Zinc: Apply 25 kg Zinc Sulfate (21%) per hectare during final field preparation.
6. **Irrigation Schedule (4–6 irrigations):**
   - 1st CRI Stage (21–25 days): Most critical for root development.
   - 2nd Tillering (40–45 days).
   - 3rd Jointing (60–65 days).
   - 4th Flowering / Booting (80–85 days).
   - 5th Milking (100–105 days).
   - 6th Dough Stage (115–120 days). *Never irrigate on windy days to avoid crop lodging.*
7. **Weed & Disease Management:**
   - Phalaris minor (Gulli Danda): Spray Clodinafop-propargyl 15% WP @ 160g/acre at 30–35 days.
   - Yellow Rust: Spray Propiconazole 25% EC (Tilt) @ 1 ml/L at first notice.
8. **Harvesting:** Harvest when straw turns golden yellow and grain moisture drops below 14%.`,
        hi: `🌾 **गेहूं की खेती की संपूर्ण उन्नत विधि:**
1. **भूमि एवं जलवायु:** उचित जल निकास वाली दोमट या बलुई दोमट मिट्टी, pH 6.5 से 7.5। फसल की बढ़वार के लिए 15-20°C और दाना पकते समय 25°C तापमान उत्तम है।
2. **बुवाई का सर्वोत्तम समय:** 1 नवंबर से 25 नवंबर। 25 नवंबर के बाद पछेती बुवाई करने पर पैदावार में भारी गिरावट आती है।
3. **बीज दर एवं उपचार:** समय पर बुवाई हेतु 100 किग्रा/हेक्टेयर (40 किग्रा/एकड़); पछेती बुवाई हेतु 125 किग्रा/हेक्टेयर। बुवाई पूर्व वीटावैक्स या कार्बेन्डाजिम 2 ग्राम प्रति किग्रा बीज से उपचारित करें।
4. **कतार से कतार दूरी:** 20 से 22.5 सेमी, बुवाई की गहराई 4-5 सेमी रखें।
5. **खाद एवं उर्वरक (NPK 120:60:40 किग्रा/हेक्टेयर):**
   - बुवाई के समय (बेसल): पूरा फास्फोरस (DAP से 60 किग्रा), पूरा पोटाश (MOP से 40 किग्रा) और एक-तिहाई यूरिया (लगभग 50 किग्रा)।
   - पहली टॉप ड्रेसिंग: एक-तिहाई यूरिया पहली सिंचाई (CRI) पर 21-25 दिन में दें।
   - दूसरी टॉप ड्रेसिंग: शेष एक-तिहाई यूरिया कल्ले फूटते समय (40-45 दिन) दें।
   - जिंक: खेत तैयारी में 25 किग्रा जिंक सल्फेट (21%) प्रति हेक्टेयर डालें।
6. **सिंचाई प्रबंधन (4 से 6 सिंचाइयां):**
   - 1. पहली सिंचाई (CRI अवस्था - 21-25 दिन): यह सबसे महत्वपूर्ण सिंचाई है।
   - 2. कल्ले फूटते समय (40-45 दिन)।
   - 3. गांठ बनते समय (60-65 दिन)।
   - 4. फूल व बाली आते समय (80-85 दिन)।
   - 5. दूधिया अवस्था (100-105 दिन)।
   - 6. दाना पकते समय (115-120 दिन)। *तेज हवा में सिंचाई न करें ताकि फसल गिरे नहीं।*
7. **खरपतवार व रोग नियंत्रण:**
   - मंडूसी (गुल्ली डंडा): बुवाई के 30-35 दिन पर क्लोडिनाफॉप 15% WP @ 160 ग्राम/एकड़ का स्प्रे करें।
   - पीला रतुआ: प्रोपिकोनाज़ोल 25% EC (टिल्ट) @ 1 मिली/लीटर तुरंत छिड़कें।
8. **कटाई एवं भंडारण:** बालियां व डंठल सुनहरे पीले होने और दानों में नमी 12-14% रहने पर कटाई करें।`
      },
      irrigation: {
        en: `🌾 **Wheat Irrigation Schedule:**
Wheat typically requires 4 to 6 timely irrigations based on soil moisture:
1. **Crown Root Initiation (CRI) (20-25 days after sowing):** Most critical irrigation for root establishment.
2. **Tillering Stage (40-45 days):** Enhances tiller count and vigorous growth.
3. **Jointing Stage (60-65 days):** Essential for stem elongation.
4. **Booting / Flowering Stage (80-85 days):** Critical for earhead development.
5. **Milking Stage (100-105 days):** Promotes grain development.
6. **Dough Stage (115-120 days):** Final grain filling.
*Caution:* Never irrigate on windy days to prevent crop lodging.`,
        hi: `🌾 **गेहूं की फसल में सिंचाई प्रबंधन:**
गेहूं की अच्छी पैदावार के लिए मिट्टी की नमी और अवस्था के अनुसार 4 से 6 सिंचाइयों की आवश्यकता होती है:
1. **पहली सिंचाई (शिखर जड़ें/CRI अवस्था - 20-25 दिन):** यह सबसे महत्वपूर्ण सिंचाई है, इसमें देरी से उपज घटती है।
2. **दूसरी सिंचाई (कल्ले फूटते समय - 40-45 दिन):** अधिक कल्ले निकलने के लिए।
3. **तीसरी सिंचाई (गांठ बनते समय - 60-65 दिन):** पौधे की बढ़वार के लिए।
4. **चौथी सिंचाई (बाली निकलते व फूल आते समय - 80-85 दिन):** दानों की संख्या तय होती है।
5. **पांचवीं सिंचाई (दूधिया अवस्था - 100-105 दिन):** दाने में दूध भरने के लिए।
6. **छठी सिंचाई (दाना पकते समय - 115-120 दिन):** दाने के वजन के लिए।
*सावधानी:* तेज हवा चलने पर सिंचाई न करें ताकि फसल गिरे नहीं।`
      },
      fertilizer: {
        en: `🌾 **Wheat Fertilizer (NPK) Schedule:**
Recommended NPK dose for irrigated timely-sown wheat is **120:60:40 kg/ha**:
- **Basal at Sowing:** Full Phosphorus (60 kg P2O5 via DAP/SSP), full Potash (40 kg K2O via MOP), and 1/3rd Nitrogen (40 kg N via Urea).
- **First Top Dressing (21-25 days at 1st irrigation):** Apply 1/3rd Nitrogen (40 kg N via Urea).
- **Second Top Dressing (40-45 days at tillering):** Apply remaining 1/3rd Nitrogen (40 kg N via Urea).
- **Micronutrient:** If zinc deficient, apply 25 kg Zinc Sulfate (21%) per hectare during field preparation.`,
        hi: `🌾 **गेहूं में खाद (उर्वरक) प्रबंधन:**
सिंचित समय पर बोई गई गेहूं के लिए अनुशंसित NPK मात्रा **120:60:40 किग्रा/हेक्टेयर** है:
- **बुवाई के समय (बेसल):** पूरा फास्फोरस (DAP या SSP से 60 किग्रा), पूरा पोटाश (MOP से 40 किग्रा) और एक-तिहाई नाइट्रोजन (लगभग 50 किग्रा यूरिया)।
- **पहली टॉप-ड्रेसिंग (21-25 दिन पर पहली सिंचाई के बाद):** एक-तिहाई नाइट्रोजन (लगभग 50 किग्रा यूरिया)।
- **दूसरी टॉप-ड्रेसिंग (40-45 दिन पर कल्ले फूटते समय):** बची हुई एक-तिहाई नाइट्रोजन (लगभग 50 किग्रा यूरिया)।
- **जिंक की कमी:** खेत की अंतिम जुताई में 25 किग्रा जिंक सल्फेट प्रति हेक्टेयर मिलाएं।`
      },
      yellow_leaves: {
        en: `🌾 **Causes & Management of Yellow Leaves in Wheat:**
1. **Nitrogen Deficiency:** Lower/older leaves turn uniformly pale yellow starting from leaf tips. *Action:* Top-dress 25–30 kg Urea per acre or spray 2% Urea solution (20g/L water).
2. **Sulphur / Zinc Deficiency:** Upper/younger leaves turn pale yellow. *Action:* Spray 0.5% Zinc Sulphate (21%) + 1% Urea in water.
3. **Yellow / Stripe Rust (Puccinia striiformis):** Bright yellow-orange powdery pustules form linear stripes parallel to leaf veins. Leaves leave yellow powder on fingers. *Action:* Spray Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole @ 1.25 ml/L immediately.
4. **Waterlogging / Poor Drainage:** Roots suffocate from excess standing water, causing yellowing. *Action:* Drain excess field water immediately.
5. **Termites or Root Aphids:** Plants wilt and yellow in patches. *Action:* Apply Chlorpyriphos 20% EC @ 1–1.5 L/acre with irrigation water.`,
        hi: `🌾 **गेहूं में पत्तियां पीली होने के मुख्य कारण एवं समाधान:**
1. **नाइट्रोजन की कमी:** निचली (पुरानी) पत्तियां नोक से पीली पड़कर सूखती हैं और बढ़वार रुकती है। 👉 *उपाय:* पहली या दूसरी सिंचाई के बाद 25-30 किग्रा यूरिया प्रति एकड़ टॉप-ड्रेस करें, अथवा 2% यूरिया (20 ग्राम/लीटर) का पर्णीय छिड़काव करें।
2. **सल्फर या जिंक की कमी:** ऊपरी (नई) पत्तियां पीली पड़ती हैं। 👉 *उपाय:* 0.5% जिंक सल्फेट (21%) + 1% यूरिया का घोल बनाकर दोपहर बाद छिड़काव करें।
3. **पीला रतुआ रोग (Yellow Rust):** पत्तियों पर नसों के समानांतर हल्दी जैसा पीला पाउडर धारियों में दिखता है और छूने पर हाथ पर पीला रंग लगता है। 👉 *उपाय:* तुरंत प्रोपिकोनाज़ोल 25% EC (टिल्ट) @ 1 मिली/लीटर अथवा टेबुकोनाज़ोल @ 1.25 मिली/लीटर पानी में मिलाकर स्प्रे करें।
4. **जलभराव (खराब जल निकासी):** पहली सिंचाई में खेत में पानी अधिक रुकने से जड़ों को हवा नहीं मिलती और फसल पीली पड़ती है। 👉 *उपाय:* खेत से अतिरिक्त पानी तुरंत निकालें।
5. **दीमक या जड़ कीट:** पौधे मुरझाकर पीले पड़ते हैं और खींचने पर आसानी से उखड़ जाते हैं। 👉 *उपाय:* क्लोरपायरीफॉस 20% EC @ 1 से 1.5 लीटर प्रति एकड़ सिंचाई के पानी के साथ चलाएं।`
      },
      diseases: {
        en: `🌾 **Wheat Disease Management:**
- **Yellow / Stripe Rust:** Linear powdery yellow-orange stripes on leaves. Spray Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole @ 1.25 ml/L.
- **Brown / Leaf Rust:** Scattered orange-brown round pustules. Spray Mancozeb 75% WP @ 2.5 g/L.
- **Loose Smut:** Earhead turns black powdery mass. Controlled via seed treatment with Carboxin/Vitavax @ 2g/kg.`,
        hi: `🌾 **गेहूं के मुख्य रोग व उपचार:**
- **पीला रतुआ (Yellow Rust):** पत्तियों पर नसों के समानांतर पीली-नारंगी पाउडर जैसी धारियां। रोकथाम के लिए प्रोपिकोनाज़ोल 25% EC (टिल्ट) @ 1 मिली/लीटर अथवा टेबुकोनाज़ोल @ 1.25 मिली/लीटर पानी में घोलकर तुरंत स्प्रे करें।
- **भूरा रतुआ (Brown Rust):** पत्तियों पर गोल नारंगी-भूरे धब्बे। मैंकोज़ेब @ 2.5 ग्राम/लीटर छिड़कें।
- **कंडुआ रोग (Loose Smut):** बालियों में काला चूर्ण बन जाता है। वीटावैक्स से बीज उपचार ही मुख्य बचाव है।`
      },
      pest: {
        en: `🌾 **Wheat Pest Management:**
- **Aphids (Mahoo):** Colonies suck plant sap from leaves and young ears. If crossing 10-15 aphids/tiller, spray Imidacloprid 17.8% SL @ 0.5 ml/L.
- **Termites (Deemak):** Attacks roots. Apply Chlorpyriphos 20% EC @ 1 L/acre with irrigation.`,
        hi: `🌾 **गेहूं के कीट व रोकथाम:**
- **माहू (Aphids):** पत्तियों व बालियों का रस चूसते हैं। संख्या 10-15 माहू प्रति टिलर होने पर इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर पानी में मिलाकर छिड़कें।
- **दीमक (Termite):** जड़ों को काटती है। सिंचाई के पानी के साथ क्लोरपायरीफॉस 20% EC @ 1-1.5 लीटर प्रति एकड़ चलाएं।`
      }
    },

    potato: {
      name_en: "Potato",
      name_hi: "आलू",
      cultivation: {
        en: `🥔 **Complete Potato Cultivation Guide:**
1. **Soil & Climate:** Well-drained friable sandy loam rich in organic matter, pH 5.5–6.5. Cool climate (15–20°C for tuber growth).
2. **Improved Varieties:** Kufri Jyoti, Kufri Bahar, Kufri Pukhraj, Kufri Sindhuri, Kufri Chipsona.
3. **Seed Rate & Treatment:** 25–30 quintals/ha of certified disease-free seed tubers (40–50g size with 2–3 sprouted eyes). Dip tubers in Carbendazim @ 2g/L or Trichoderma @ 5g/L for 10 minutes; shade dry.
4. **Planting Time & Spacing:** October 15 to November 5. Ridge to ridge: 60 cm, tuber to tuber: 20 cm at 5–7 cm depth.
5. **Fertilizer Management (NPK 150:80:120 kg/ha):**
   - Basal: 15–20 tonnes FYM, full P (DAP/SSP), full K (MOP), and 50% Nitrogen (Urea) at planting.
   - Top Dressing: Remaining 50% Nitrogen during earthing up (30–35 days).
6. **Irrigation Schedule:** Light, frequent irrigations every 7–10 days. Moisture is critical during tuber initiation (35–45 days) and tuber enlargement (50–65 days). Stop irrigation 10–12 days before harvest.
7. **Earthing-Up:** Mandatory at 30–35 days (crop height 15–20 cm) to cover tubers and prevent greening from sunlight.
8. **Plant Protection:**
   - Early/Late Blight: Preventive spray of Mancozeb @ 2.5 g/L; curative spray of Cymoxanil + Mancozeb @ 2.5 g/L.
   - Aphids & Tuber Moth: Spray Imidacloprid @ 0.5 ml/L; keep tubers well covered with soil.
9. **Harvesting & Curing:** Dehaulm 10 days before harvesting when tops yellow. Dry harvested tubers in shade for 8–10 days for skin hardening.`,
        hi: `🥔 **आलू की खेती का पूरा उन्नत तरीका:**
1. **भूमि एवं जलवायु:** जीवांश युक्त बलुई दोमट मिट्टी, pH 5.5 से 6.5 सबसे उपयुक्त है। कंदों के विकास के लिए 15 से 20°C का ठंडा मौसम आवश्यक है।
2. **उन्नत किस्में:** कुफरी पुखराज (अगेती), कुफरी बहार, कुफरी ज्योति, कुफरी सिंदूरी (पछेती), कुफरी चिपसोना।
3. **बीज चयन एवं उपचार:** 40-50 ग्राम आकार के 2-3 आंख वाले प्रमाणित कंद (25-30 क्विंटल/हेक्टेयर)। बुवाई पूर्व बीज कंदों को कार्बेन्डाजिम 2 ग्राम/लीटर पानी के घोल में 10 मिनट डुबोकर छाया में सुखाएं।
4. **बुवाई का समय एवं दूरी:** 15 अक्टूबर से 5 नवंबर। मेड़ से मेड़ की दूरी 60 सेमी और कंद से कंद की दूरी 20 सेमी रखें (गहराई 5-7 सेमी)।
5. **खाद एवं उर्वरक (NPK 150:80:120 किग्रा/हेक्टेयर):**
   - बेसल (बुवाई पर): 15-20 टन सड़ी गोबर खाद, पूरा फास्फोरस (DAP), पूरा पोटाश (MOP) और आधी नाइट्रोजन (यूरिया)।
   - टॉप ड्रेसिंग: शेष आधी नाइट्रोजन पहली मिट्टी चढ़ाते समय (30-35 दिन पर) दें।
6. **सिंचाई प्रबंधन:** हल्की और नियमित सिंचाई करें (7-10 दिन के अंतराल पर)। कंद बनते और फूलते समय (35 से 65 दिन) खेत में पर्याप्त नमी अनिवार्य है। खुदाई से 10-12 दिन पहले सिंचाई बंद कर दें ताकि छिलका कड़ा हो सके और भंडारण में सड़न न हो।
7. **मिट्टी चढ़ाना (Earthing-up):** बुवाई के 30-35 दिन बाद पौधों पर अच्छी तरह मिट्टी चढ़ाएं ताकि आलू धूप से हरे न हों (हरा आलू जहरीला सोलेनाइन बनाता है)।
8. **रोग एवं कीट नियंत्रण:**
   - झुलसा रोग (अगेती/पछेती): रोकथाम के लिए मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का स्प्रे करें। रोग दिखने पर साइमोक्सानिल + मैंकोज़ेब @ 2.5 ग्राम/लीटर छिड़कें।
   - माहू (एफिड): इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर स्प्रे करें।
9. **खुदाई एवं भंडारण:** खुदाई से 10 दिन पहले पौधों की बेल काट दें (Dihalm)। खुदाई के बाद 8-10 दिन छाया में सुखाकर छिलका पक्का करें।`
      },
      irrigation: {
        en: `🥔 **Potato Irrigation Schedule:**
- Frequency: Light and frequent irrigations every 7 to 10 days depending on soil type and weather.
- Critical Period: Tuber initiation (25-35 days) and tuber enlargement (45-65 days). Inadequate moisture causes small, cracked, or misshapen tubers.
- Stop irrigation completely 10-12 days before harvest to harden the tuber skins and extend storage life.`,
        hi: `🥔 **आलू में सिंचाई प्रबंधन:**
- आलू में उथली जड़ें होती हैं, इसलिए हल्की और नियमित सिंचाई करें (7-10 दिन के अंतराल पर)।
- क्रांतिक अवस्था: कंद बनने (25-35 दिन) और कंदों का आकार बढ़ने (45-65 दिन) के समय खेत में नमी आवश्यक है।
- खुदाई से 10-12 दिन पहले पानी पूरी तरह बंद कर दें ताकि कंदों का छिलका कड़ा हो सके और भंडारण में सड़न न हो।`
      },
      fertilizer: {
        en: `🥔 **Potato Fertilizer (NPK) Schedule:**
- **Recommended Dose:** 150-180 kg N, 80-100 kg P2O5, 120-150 kg K2O per hectare. High Potash is essential for starch accumulation and tuber size.
- **Application:** Apply all P, all K, and 50% N at planting. Top-dress remaining 50% N during earthing up (30-35 days).`,
        hi: `🥔 **आलू में खाद (उर्वरक) प्रबंधन:**
- **मात्रा:** 150-180 किग्रा नाइट्रोजन, 80-100 किग्रा फास्फोरस, 120-150 किग्रा पोटाश प्रति हेक्टेयर। आलू में पोटाश कंद के वजन व चमक के लिए अत्यंत महत्वपूर्ण है।
- **प्रयोग विधि:** पूरा फास्फोरस, पूरा पोटाश और आधा यूरिया बुवाई के समय दें। शेष आधा यूरिया पहली मिट्टी चढ़ाते समय (30-35 दिन पर) दें।`
      },
      yellow_leaves: {
        en: `🥔 **Causes & Remedies for Yellow Leaves in Potato:**
1. **Early/Late Blight Initial Phase:** Yellow halos around brown spots on leaves. Spray Mancozeb @ 2.5 g/L or Curzate @ 2.5 g/L.
2. **Nitrogen Deficiency:** Lower leaves turn pale yellow. Apply Urea top-dressing or spray 1.5% Urea solution.
3. **Over-irrigation / Water Stagnation:** Yellowing from waterlogged ridges. Improve drainage immediately.
4. **Aphid-Transmitted Potato Viruses:** Leaves mottle, curl, and yellow. Control aphids with Imidacloprid @ 0.5 ml/L.`,
        hi: `🥔 **आलू में पीली पत्तियों के कारण एवं रोकथाम:**
1. **झुलसा रोग के शुरुआती लक्षण:** पत्तियों पर कत्थई धब्बों के चारों ओर पीला घेरा। मैंकोज़ेब @ 2.5 ग्राम/लीटर या कर्ज़ेट का छिड़काव करें।
2. **नाइट्रोजन की कमी:** निचली पत्तियां पीली पड़ना। यूरिया की टॉप ड्रेसिंग करें या 1.5% यूरिया का छिड़काव करें।
3. **जलभराव:** क्यारियों में पानी रुकने से जड़ें घुटती हैं और पत्तियां पीली होती हैं। खेत से पानी निकालें।
4. **माहू कीट व वायरस:** माहू रस चूसकर वायरस फैलाता है जिससे पत्तियां पीली व मुड़ जाती हैं। इमिडाक्लोप्रिड @ 0.5 मिली/लीटर स्प्रे करें।`
      },
      diseases: {
        en: `🥔 **Potato Blight Advisory:**
- **Early Blight:** Concentric dark target spots. Spray Mancozeb 75% WP @ 2.5 g/L.
- **Late Blight:** Fast-spreading dark water-soaked lesions with white fungal growth underneath in cool humid weather. Spray Cymoxanil 8% + Mancozeb 64% (Curzate @ 2.5 g/L) or Dimethomorph 50% WP @ 1 g/L immediately.`,
        hi: `🥔 **आलू के झुलसा रोग की रोकथाम:**
- **अगेती झुलसा (Early Blight):** पत्तियों पर गोल छल्लेदार कत्थई धब्बे। मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।
- **पछेती झुलसा (Late Blight):** पत्तियों पर तेजी से फैलने वाले काले-भूरे जलसिक्त धब्बे। तुरंत साइमोक्सानिल + मैंकोज़ेब (Curzate @ 2.5 ग्राम/लीटर) अथवा डाइमेशोमॉर्फ @ 1 ग्राम/लीटर का छिड़काव करें।`
      },
      pest: {
        en: `🥔 **Potato Pests:**
- **Aphids:** Vector for viral degeneration. Spray Imidacloprid 17.8% SL @ 0.5 ml/L.
- **Potato Tuber Moth (PTM):** Keep tubers well covered with soil during earthing up.`,
        hi: `🥔 **आलू के कीट नियंत्रण:**
- **माहू (एफिड):** वायरस फैलाता है। इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर स्प्रे करें।
- **कंद शलभ (PTM):** मिट्टी अच्छी तरह चढ़ाकर रखें ताकि कंद ढके रहें।`
      }
    },

    rice: {
      name_en: "Rice / Paddy",
      name_hi: "धान",
      cultivation: {
        en: `🌾 **Complete Rice Cultivation Guide:**
1. **Soil & Climate:** Heavy clay loam soils with high water retention capacity, pH 5.5–7.0. Hot and humid climate with abundant sunlight.
2. **Nursery Sowing:** May 15 to June 20. Seed rate: 25–30 kg/ha for inbred, 15 kg/ha for hybrids. Treat seed with Carbendazim 2g/kg or salt-water soak.
3. **Transplanting:** 20–25 days old seedlings at 20x15 cm spacing, 2–3 seedlings per hill in puddle field.
4. **Fertilizer Management (NPK 120:60:40 kg/ha + 25 kg Zinc Sulfate):**
   - Basal: Full P, full K, full Zinc, and 1/3rd Nitrogen at transplanting.
   - 1st Top Dressing: 1/3rd Nitrogen at active tillering (21 days).
   - 2nd Top Dressing: 1/3rd Nitrogen at panicle initiation (42–45 days).
5. **Water Management:** Maintain 2–3 cm shallow standing water for 3 weeks after transplanting. Drain for 2 days at maximum tillering. Keep 5 cm water during flowering. Drain completely 10 days before harvest.
6. **Plant Protection:**
   - Blast: Spray Tricyclazole 75% WP @ 0.6 g/L.
   - Stem Borer: Apply Chlorantraniliprole (Coragen) @ 0.3 ml/L or Cartap 4G granules.
7. **Harvesting:** Harvest when 80% panicles turn straw-colored and grain moisture is 18–20%.`,
        hi: `🌾 **धान (चावल) की उन्नत खेती का पूरा तरीका:**
1. **भूमि एवं जलवायु:** मटियार दोमट या भारी मिट्टी जिसमें जल धारण क्षमता अधिक हो, pH 5.5 से 7.0। गर्म और नम जलवायु (25-35°C) सर्वोत्तम है।
2. **नर्सरी तैयारी एवं बुवाई:** 15 मई से 20 जून। बीज दर: सामान्य किस्म 25-30 किग्रा/हेक्टेयर; हाइब्रिड 15 किग्रा/हेक्टेयर। बुवाई पूर्व बीज को नमक के घोल में तैरते हल्के बीज अलग करें तथा कार्बेन्डाजिम 2 ग्राम/किग्रा से उपचारित करें।
3. **रोपाई की विधि:** 20-25 दिन की पौध, लेह (पडलिंग) किए खेत में 20x15 सेमी दूरी पर एक जगह 2-3 पौधे लगाएं।
4. **खाद एवं उर्वरक (NPK 120:60:40 किग्रा + 25 किग्रा जिंक सल्फेट/हेक्टेयर):**
   - बेसल (रोपाई पर): पूरा फास्फोरस (DAP), पूरा पोटाश (MOP), पूरा जिंक सल्फेट और एक-तिहाई यूरिया।
   - पहली टॉप ड्रेसिंग: एक-तिहाई यूरिया कल्ले फूटते समय (21 दिन पर)।
   - दूसरी टॉप ड्रेसिंग: शेष एक-तिहाई यूरिया बाली बनते समय (40-45 दिन पर)।
5. **जल प्रबंधन:** रोपाई के पहले 3 सप्ताह 2-3 सेमी उथला पानी रखें। कल्ले फूटने पर 2 दिन पानी निकालें ताकि जड़ों को हवा मिले। बाली व फूल आते समय 5 सेमी पानी रखें। कटाई से 10-14 दिन पूर्व पानी निकाल दें।
6. **रोग व कीट रोकथाम:**
   - झोंका रोग (ब्लास्ट): ट्राइसाइक्लाजोल 75% WP @ 0.6 ग्राम/लीटर का छिड़काव करें।
   - तना छेदक (Stem Borer): कोरोजन @ 0.3 मिली/लीटर स्प्रे करें या कारटाप हाइड्रोक्लोराइड 4G दानेदार डालें।
7. **कटाई:** जब बालियां सुनहरी पीली हो जाएं और दाने में 18-20% नमी हो तब कटाई करें।`
      },
      irrigation: {
        en: `🌾 **Rice Irrigation Best Practices:**
- Maintain 2-3 cm shallow water for first 3 weeks after transplanting.
- Drain field for 2-3 days at maximum tillering to allow root aeration.
- Maintain 5 cm water during panicle initiation and flowering.
- Drain completely 10-14 days before harvest.`,
        hi: `🌾 **धान में सिंचाई प्रबंधन:**
- रोपाई के शुरुआती 3 सप्ताह तक 2-3 सेमी उथला पानी बनाए रखें ताकि पौधे अच्छी तरह जम सकें।
- कल्ले फूटते समय 2-3 दिन पानी निकालें ताकि जड़ों को ऑक्सीजन मिल सके।
- बाली निकलते और फूल आते समय 5 सेमी पानी का स्तर अनिवार्य है।
- कटाई से 10-14 दिन पहले पानी पूरी तरह निकाल दें।`
      },
      fertilizer: {
        en: `🌾 **Rice Fertilizer (NPK) Schedule:**
- **Dose:** 100-120 kg N, 50-60 kg P2O5, 40-50 kg K2O + 25 kg Zinc Sulfate per hectare.
- **Application:** All P, K, and Zinc at transplanting. Split Nitrogen into 3 equal doses: at transplanting, active tillering (21 days), and panicle initiation (45 days).`,
        hi: `🌾 **धान में खाद (उर्वरक) प्रबंधन:**
- **मात्रा:** 100-120 किग्रा नाइट्रोजन, 50-60 किग्रा फास्फोरस, 40-50 किग्रा पोटाश और 25 किग्रा जिंक सल्फेट प्रति हेक्टेयर।
- **प्रयोग विधि:** पूरा फास्फोरस, पोटाश और जिंक रोपाई के समय दें। नाइट्रोजन को 3 बराबर भागों में बांटें: रोपाई पर, कल्ले फूटते समय (21 दिन) और बाली बनते समय (45 दिन)।`
      },
      yellow_leaves: {
        en: `🌾 **Yellow Leaves in Rice:**
1. **Khaira Disease (Zinc Deficiency):** Rusty brown-yellow pigmentation appears on leaves 2–3 weeks after transplanting. *Remedy:* Spray 5 kg Zinc Sulfate (21%) + 2.5 kg Slaked Lime or 2% Urea per hectare.
2. **Nitrogen Deficiency:** General yellowing of old leaves. Apply top-dress Urea.
3. **Bacterial Leaf Blight (BLB):** Yellow-white wavy stripes from leaf tips downward. Spray Streptocycline 1g/10L + Copper Oxychloride @ 2.5 g/L.`,
        hi: `🌾 **धान में पीली पत्तियों का कारण एवं उपाय:**
1. **खैरा रोग (जिंक की कमी):** रोपाई के 2-3 सप्ताह बाद पत्तियों पर कत्थई-पीले धब्बे बनते हैं। 👉 *उपाय:* 5 किग्रा जिंक सल्फेट + 2.5 किग्रा बुझा चूना या 2% यूरिया 500 लीटर पानी में घोलकर प्रति हेक्टेयर छिड़कें।
2. **नाइट्रोजन की कमी:** पुरानी पत्तियां नीचे से पीली पड़ना। यूरिया की टॉप ड्रेसिंग करें।
3. **जीवाणु झुलसा (BLB):** पत्तियों के किनारे नोक से नीचे की ओर पीले-सफेद लहरदार सूखते हैं। स्ट्रेप्टोसाइक्लिन 1 ग्राम/10 लीटर + कॉपर ऑक्सीक्लोराइड @ 2.5 ग्राम/लीटर का स्प्रे करें।`
      },
      diseases: {
        en: `🌾 **Rice Diseases & Remedies:**
- **Blast:** Diamond-shaped lesions with gray centers. Spray Tricyclazole 75% WP @ 0.6 g/L or Kasugamycin @ 2 ml/L.
- **Brown Spot:** Small oval brown spots. Spray Propiconazole 25% EC @ 1 ml/L.`,
        hi: `🌾 **धान के रोग व रोकथाम:**
- **ब्लास्ट (झोंका रोग):** पत्तियों पर नाव के आकार के भूरे धब्बे। ट्राइसाइक्लाजोल 75% WP @ 0.6 ग्राम/लीटर अथवा कासुगामाइसिन @ 2 मिली/लीटर का छिड़काव करें।
- **भूरा धब्बा (Brown Spot):** प्रोपिकोनाज़ोल 25% EC @ 1 मिली/लीटर स्प्रे करें।`
      },
      pest: {
        en: `🌾 **Rice Pests:**
- **Stem Borer:** Dead hearts and white ears. Spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L or Cartap 4G.
- **Brown Planthopper (BPH):** Hopper burn in patches. Spray Pymetrozine 50% WG @ 0.6 g/L.`,
        hi: `🌾 **धान के कीट व उपचार:**
- **तना छेदक (Stem Borer):** कोरोजन (क्लोरांट्रानिलीप्रोल 18.5% SC) @ 0.3 मिली/लीटर का छिड़काव करें या कारटाप हाइड्रोक्लोराइड 4G दानेदार डालें।
- **भूरा फुदका (BPH):** पाइमेट्रोज़िन 50% WG @ 0.6 ग्राम/लीटर का छिड़काव पौधों के निचले हिस्से में करें।`
      }
    },

    tomato: {
      name_en: "Tomato",
      name_hi: "टमाटर",
      cultivation: {
        en: `🍅 **Complete Tomato Cultivation Guide:**
1. **Soil & Climate:** Well-drained sandy loam rich in organic matter, pH 6.0–7.0. Moderate climate (20–25°C).
2. **Nursery & Seed Rate:** 100–150g hybrid seed per acre. Transplant 25-day-old vigorous seedlings.
3. **Spacing:** 60–75 cm between rows and 45–60 cm between plants on raised beds.
4. **Fertilizer (NPK 120:80:100 kg/ha):** Apply all P, half N, and half K as basal; split balance N and K at flowering and fruit enlargement. Spray Boron (20%) @ 1g/L at flowering to prevent blossom drop.
5. **Irrigation:** Drip irrigation is ideal to avoid wetting foliage and prevent fungal spread.
6. **Staking:** Stake plants with bamboo and twine to keep fruits off the ground.
7. **Plant Protection:** Spray Mancozeb @ 2.5 g/L for blight; Emamectin Benzoate @ 0.5 g/L for fruit borers.`,
        hi: `🍅 **टमाटर की खेती का पूरा उन्नत तरीका:**
1. **भूमि एवं जलवायु:** जीवांश युक्त उचित जल निकास वाली बलुई दोमट मिट्टी, pH 6.0 से 7.0। 20 से 25°C का तापमान सर्वोत्तम है।
2. **नर्सरी एवं बीज दर:** संकर किस्मों के लिए 100-150 ग्राम बीज प्रति एकड़। 25 दिन की स्वस्थ पौध तैयार करें।
3. **रोपाई एवं दूरी:** मेड़ों पर 60-75 सेमी कतार से कतार और 45-60 सेमी पौधे से पौधे की दूरी रखें।
4. **खाद एवं उर्वरक (NPK 120:80:100 किग्रा/हेक्टेयर):** पूरा फास्फोरस, आधा पोटाश और आधी नाइट्रोजन रोपाई पर दें। शेष यूरिया व पोटाश को फूल आते समय (30 दिन) और फल बनते समय (50 दिन) दें। फूल झड़ने से रोकने हेतु बोरॉन (20%) @ 1 ग्राम/लीटर स्प्रे करें।
5. **सिंचाई:** ड्रिप सिंचाई अपनाएं। ऊपर से पानी छिड़कने से बचें ताकि फफूंद न फैले।
6. **सहारा देना (Staking):** पौधों को बांस व सुतली से सहारा दें ताकि फल मिट्टी के संपर्क में आकर सड़ें नहीं।
7. **रोग व कीट:** झुलसा रोग के लिए मैंकोज़ेब @ 2.5 ग्राम/लीटर; फल छेदक इल्ली के लिए एमामेक्टिन बेंजोएट @ 0.5 ग्राम/लीटर का छिड़काव करें।`
      },
      clarification: {
        en: "What specific issue are you facing in your tomato crop—are leaves turning yellow, is there a fungal blight/disease, insect pests, or are flowers and fruits dropping? Please share details so I can recommend exact measures.",
        hi: "टमाटर में समस्या क्या है—पत्तियां पीली हैं, रोग है, कीट हैं या फल नहीं लग रहे? कृपया अपनी समस्या विस्तार से बताएं ताकि मैं सटीक दवा या उपाय बता सकूँ।"
      },
      irrigation: {
        en: "🍅 **Tomato Irrigation:** Use drip irrigation to prevent moisture fluctuation and blossom end rot. Avoid overhead sprinklers to minimize foliar fungal infections.",
        hi: "🍅 **टमाटर में सिंचाई:** ड्रिप सिंचाई अपनाएं जिससे फल फटने की समस्या न हो। ऊपर से पानी छिड़कने से बचें ताकि फफूंद जनित बीमारियां न फैलें।"
      },
      fertilizer: {
        en: "🍅 **Tomato Fertilizer (NPK):** 120:80:100 kg/ha. Apply all P, half N, and half K at transplanting. Top-dress remaining in two splits at flowering and fruit set. Spray Boron (20%) @ 1g/L to prevent fruit cracking.",
        hi: "🍅 **टमाटर में खाद (उर्वरक) प्रबंधन:**\n- **मात्रा:** 120:80:100 किग्रा NPK प्रति हेक्टेयर।\n- **प्रयोग:** पूरा फास्फोरस, आधा पोटाश और आधी नाइट्रोजन रोपाई के समय दें।\n- **टॉप ड्रेसिंग:** शेष नाइट्रोजन व पोटाश को फूल आते समय (30 दिन) और फल बनते समय (50 दिन) दो भागों में दें।\n- **फल फटने व फूल झड़ने से बचाव:** बोरॉन (20%) @ 1 ग्राम प्रति लीटर पानी में मिलाकर स्प्रे करें।"
      },
      yellow_leaves: {
        en: `🍅 **Causes & Remedies for Yellow Leaves in Tomato:**
1. **Tomato Leaf Curl Virus:** Leaves curl upwards, thicken, and yellow with stunted plant growth. Vector is Whitefly. *Remedy:* Rogue out infected plants. Spray Diafenthiuron 50% WP @ 1g/L or Imidacloprid @ 0.5 ml/L to control whiteflies.
2. **Early Blight:** Concentric dark target spots surrounded by yellow halos on lower leaves. Spray Mancozeb @ 2.5 g/L or Azoxystrobin @ 1 ml/L.
3. **Nitrogen Deficiency:** Lower leaves turn pale yellow. Apply balanced NPK fertigation.
4. **Over-watering:** Root rot causes foliage yellowing. Reduce watering frequency.`,
        hi: `🍅 **टमाटर में पीली पत्तियों के कारण एवं रोकथाम:**
1. **लीफ कर्ल वायरस (पर्ण कुंचन रोग):** पत्तियां ऊपर की ओर मुड़ती हैं, खुरदरी व पीली हो जाती हैं और पौधे की बढ़वार रुकती है। यह सफेद मक्खी से फैलता है। 👉 *उपाय:* ग्रसित पौधे उखाड़कर नष्ट करें। सफेद मक्खी की रोकथाम के लिए इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर या डायफेंथियूरॉन 50% WP @ 1 ग्राम/लीटर का छिड़काव करें।
2. **अगेती झुलसा रोग:** पत्तियों पर कत्थई धब्बों के चारों तरफ पीला घेरा। मैंकोज़ेब @ 2.5 ग्राम/लीटर का स्प्रे करें।
3. **नाइट्रोजन की कमी:** निचली पत्तियां पीली पड़ना। यूरिया का हल्का बुरकाव या ड्रिप से 19:19:19 दें।
4. **अधिक पानी:** जलभराव से जड़ें सड़ती हैं और पत्तियां पीली होती हैं। सिंचाई नियंत्रित करें।`
      },
      diseases: {
        en: "🍅 **Tomato Diseases:** Early Blight and Late Blight. Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin @ 1 ml/L. For Leaf Curl Virus, control whiteflies with Imidacloprid.",
        hi: "🍅 **टमाटर के रोग:** अगेती व पछेती झुलसा के लिए मैंकोज़ेब @ 2.5 ग्राम/लीटर या एजोक्सीस्ट्रोबिन @ 1 मिली/लीटर स्प्रे करें। लीफ कर्ल वायरस से बचाव हेतु सफेद मक्खी का नियंत्रण करें।"
      },
      pest: {
        en: "🍅 **Tomato Pests:** Fruit Borer (Helicoverpa). Spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L.",
        hi: "🍅 **टमाटर के कीट:** फल छेदक इल्ली फलों में छेद करके खाती है। कोरोजन (Coragen) @ 0.3 मिली/लीटर अथवा एमामेक्टिन बेंजोएट @ 0.5 ग्राम/लीटर पानी में मिलाकर छिड़कें।"
      }
    },

    cotton: {
      name_en: "Cotton",
      name_hi: "कपास",
      cultivation: {
        en: `🌱 **Cotton Cultivation Guide:** Sowing in April–May. Spacing: 90x60 cm. Balanced NPK (120:60:60 kg/ha). Critical stages for irrigation: flowering and boll development. Control bollworms and sucking pests timely.`,
        hi: `🌱 **कपास की खेती:** बुवाई अप्रैल-मई में करें। दूरी: 90x60 सेमी। NPK (120:60:60 किग्रा/हेक्टेयर)। फूल आने और गूलर बनते समय खेत में नमी रखें। रस चूसक कीटों और सुंडी का समय पर नियंत्रण करें।`
      },
      irrigation: {
        en: "🌱 **Cotton Irrigation:** Flowering and boll formation stages are critical. Avoid water stagnation by providing field drainage.",
        hi: "🌱 **कपास में सिंचाई:** फूल आने और गूलर बनते समय खेत में नमी आवश्यक है। जलभराव बिल्कुल न होने दें।"
      },
      fertilizer: {
        en: "🌱 **Cotton Fertilizer:** 120-150 kg N, 60 kg P2O5, 60 kg K2O/ha. Split Nitrogen into 3 parts (squaring, flowering, boll development).",
        hi: "🌱 **कपास में खाद:** 120-150 किग्रा नाइट्रोजन, 60 किग्रा फास्फोरस, 60 किग्रा पोटाश प्रति हेक्टेयर। नाइट्रोजन को तीन बार में दें।"
      },
      diseases: {
        en: "🌱 **Cotton Bacterial Blight:** Angular leaf spots. Spray Copper Oxychloride 50% WP @ 2.5 g/L + Streptocycline @ 0.1 g/L.",
        hi: "🌱 **कपास का जीवाणु झुलसा:** कॉपर ऑक्सीक्लोराइड @ 2.5 ग्राम + स्ट्रेप्टोसाइक्लिन 1 ग्राम प्रति 10 लीटर पानी में मिलाकर छिड़कें।"
      },
      pest: {
        en: "🌱 **Cotton Sucking Pests & Bollworms:** Spray Imidacloprid @ 0.5 ml/L for jassids/whitefly; Spinetoram 11.7% SC @ 1 ml/L for bollworms.",
        hi: "🌱 **कपास के कीट:** रस चूसक कीटों (तेप, सफेद मक्खी) के लिए इमिडाक्लोप्रिड @ 0.5 मिली/लीटर; गुलाबी सुंडी के लिए स्पिनेटोरम @ 1 मिली/लीटर स्प्रे करें।"
      }
    },

    sugarcane: {
      name_en: "Sugarcane",
      name_hi: "गन्ना",
      cultivation: {
        en: `🎋 **Sugarcane Cultivation Guide:** Autumn planting (Oct) or Spring (Feb–Mar). Furrow spacing 90–120 cm. High nutrient demand: 150–200 kg N, 60–80 kg P2O5, 60 kg K2O/ha. Irrigate every 8–10 days in summer.`,
        hi: `🎋 **गन्ने की उन्नत खेती:** शरदकालीन बुवाई (अक्टूबर) या वसंतकालीन (फरवरी-मार्च)। नालियों की दूरी 90-120 सेमी। 150-200 किग्रा नाइट्रोजन, 60-80 किग्रा फास्फोरस, 60 किग्रा पोटाश प्रति हेक्टेयर डालें।`
      },
      irrigation: {
        en: "🎋 **Sugarcane Irrigation:** Irrigate every 8-10 days in summer and 15-20 days in winter. Grand growth period requires adequate moisture.",
        hi: "🎋 **गन्ने में सिंचाई:** गर्मी में 8-10 दिन और सर्दी में 15-20 दिन के अंतराल पर सिंचाई करें।"
      },
      fertilizer: {
        en: "🎋 **Sugarcane Fertilizer:** 150-200 kg N, 60-80 kg P2O5, 60 kg K2O/ha. Split N into 3 doses up to 120 days of planting.",
        hi: "🎋 **गन्ने में खाद:** 150-200 किग्रा नाइट्रोजन, 60-80 किग्रा फास्फोरस, 60 किग्रा पोटाश प्रति हेक्टेयर।"
      },
      diseases: {
        en: "🎋 **Sugarcane Red Rot:** Use certified disease-free setts, treat setts with Carbendazim (1g/L), and avoid ratooning infected fields.",
        hi: "🎋 **गन्ने का लाल सड़न (Red Rot):** रोगमुक्त बीज गूलों का प्रयोग करें, कार्बेन्डाजिम से उपचार करें, रोगग्रस्त खेत में पेड़ी न रखें।"
      }
    },

    corn: {
      name_en: "Corn / Maize",
      name_hi: "मक्का",
      cultivation: {
        en: `🌽 **Corn Cultivation Guide:** Kharif sowing with onset of monsoon; Rabi in Oct–Nov. Spacing 60x20 cm. NPK 120:60:40 kg/ha. Critical irrigation at knee-high, tasseling, and silking.`,
        hi: `🌽 **मक्का की खेती:** खरीफ में जून-जुलाई तथा रबी में अक्टूबर-नवंबर। दूरी 60x20 सेमी। NPK 120:60:40 किग्रा/हेक्टेयर। घुटने की ऊंचाई, नर मंजरी व भुट्टे के बाल आते समय सिंचाई जरूरी है।`
      },
      irrigation: {
        en: "🌽 **Corn Irrigation:** Knee-high, tasseling, silking, and grain filling are the critical moisture periods.",
        hi: "🌽 **मक्का में सिंचाई:** घुटने की ऊंचाई, नर मंजरी, भुट्टे के बाल निकलने और दाना भरते समय खेत में नमी आवश्यक है।"
      },
      fertilizer: {
        en: "🌽 **Corn Fertilizer:** 120:60:40 kg/ha NPK + 25 kg Zinc Sulfate. Top-dress Nitrogen at knee-high and tasseling stages.",
        hi: "🌽 **मक्का में खाद:** 120:60:40 किग्रा NPK प्रति हेक्टेयर। यूरिया को घुटने तक ऊंचाई और नर मंजरी निकलते समय दें।"
      },
      diseases: {
        en: "🌽 **Corn Common Rust & Blight:** Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin @ 1 ml/L upon seeing initial pustules.",
        hi: "🌽 **मक्का में रस्ट व झुलसा:** मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।"
      }
    },

    soybean: {
      name_en: "Soybean",
      name_hi: "सोयाबीन",
      cultivation: {
        en: `🌿 **Soybean Cultivation Guide:** Sowing in late June with monsoon. Seed rate 70–80 kg/ha, row spacing 45 cm. Treat with Rhizobium. NPK 20:60:40 kg/ha + 20 kg Sulphur.`,
        hi: `🌿 **सोयाबीन की खेती:** जून के अंतिम सप्ताह में मानसून पर बुवाई। बीज दर 70-80 किग्रा/हेक्टेयर, कतार दूरी 45 सेमी। राइजोबियम से उपचार करें। NPK 20:60:40 किग्रा + 20 किग्रा सल्फर डालें।`
      },
      irrigation: {
        en: "🌿 **Soybean Irrigation:** Provide life-saving irrigation at flowering (35-40 days) and pod development (55-65 days) if rains fail.",
        hi: "🌿 **सोयाबीन में सिंचाई:** यदि बारिश न हो तो फूल आते समय (35-40 दिन) और फलियां भरते समय हल्की सिंचाई जरूर करें।"
      },
      fertilizer: {
        en: "🌿 **Soybean Fertilizer:** 20-30 kg N, 60-80 kg P2O5, 40 kg K2O, and 20 kg Sulfur per hectare. Treat seed with Rhizobium.",
        hi: "🌿 **सोयाबीन में खाद:** 20-30 किग्रा नाइट्रोजन, 60-80 किग्रा फास्फोरस, 40 किग्रा पोटाश और 20 किग्रा सल्फर प्रति हेक्टेयर डालें।"
      },
      diseases: {
        en: "🌿 **Soybean Rust:** Spray Hexaconazole 5% EC @ 1 ml/L or Tebuconazole @ 1.25 ml/L at first notice.",
        hi: "🌿 **सोयाबीन का रस्ट रोग:** हेक्साकोनाज़ोल 5% EC @ 1 मिली/लीटर अथवा टेबुकोनाज़ोल का छिड़काव करें।"
      }
    },

    apple: {
      name_en: "Apple",
      name_hi: "सेब",
      irrigation: {
        en: "🍎 **Apple Orchard Irrigation:** Fruit set (April-May) and fruit expansion (June-July) are critical. Use drip irrigation and mulching.",
        hi: "🍎 **सेब में सिंचाई:** फल बनते समय (अप्रैल-मई) और फल बढ़ने के समय (जून-जुलाई) पर्याप्त नमी बनाए रखें।"
      },
      fertilizer: {
        en: "🍎 **Apple Fertilizer:** Mature tree requires 700g N, 350g P2O5, 700g K2O plus 50-60 kg FYM per tree per year.",
        hi: "🍎 **सेब में खाद:** बड़े फलदार पेड़ हेतु प्रति वर्ष 700 ग्राम नाइट्रोजन, 350 ग्राम फास्फोरस, 700 ग्राम पोटाश व 50-60 किग्रा गोबर खाद दें।"
      },
      diseases: {
        en: "🍎 **Apple Scab:** Spray Dodine 65% WP @ 0.75 g/L or Difenoconazole 25% EC @ 0.3 ml/L at green tip and petal fall stages.",
        hi: "🍎 **सेब का स्कैब (Scab):** पत्तियों और फलों पर काले धब्बे। डोडीन 65% WP @ 0.75 ग्राम/लीटर या डाईफेनोकोनाज़ोल @ 0.3 मिली/लीटर का छिड़काव करें।"
      }
    },

    grape: {
      name_en: "Grape",
      name_hi: "अंगूर",
      irrigation: {
        en: "🍇 **Grape Irrigation:** Provide consistent moisture during berry development; withhold water 10-15 days before harvest to build sugars.",
        hi: "🍇 **अंगूर में सिंचाई:** दाना बढ़ते समय पर्याप्त पानी दें; तुड़ाई से 10-15 दिन पहले पानी बंद कर दें ताकि मिठास बढ़े।"
      },
      fertilizer: {
        en: "🍇 **Grape Fertilizer:** 300g N, 150g P2O5, 300g K2O per vine per year. Boost potassium during berry enlargement.",
        hi: "🍇 **अंगूर में खाद:** प्रति बेल 300 ग्राम नाइट्रोजन, 150 ग्राम फास्फोरस और 300 ग्राम पोटाश प्रति वर्ष दें।"
      },
      diseases: {
        en: "🍇 **Grape Black Rot & Downy Mildew:** Spray Mancozeb @ 2.5 g/L or Ridomil MZ (Metalaxyl + Mancozeb) @ 2.5 g/L.",
        hi: "🍇 **अंगूर में ब्लैक रॉट व डाउनी मिल्ड्यू:** मैंकोज़ेब @ 2.5 ग्राम/लीटर अथवा रिडोमिल एमजेड @ 2.5 ग्राम/लीटर का छिड़काव करें।"
      }
    }
  },

  topics: {
    soil_ph: {
      en: `🌍 **What is Soil pH & Why It Matters:**
- **Definition:** Soil pH measures the acidity or alkalinity of your soil on a scale from 0 to 14.
- **Ideal Range for Most Crops:** **6.5 to 7.5** (Neutral). In this range, essential plant nutrients (Nitrogen, Phosphorus, Potassium, Zinc, and Iron) are most readily absorbed by roots.
- **Acidic Soil (pH < 6.0):** Common in high rainfall zones. Locks up phosphorus. *Correction:* Apply agricultural lime (calcium carbonate) or dolomite.
- **Alkaline / Sodic Soil (pH > 8.0):** Causes zinc and iron chlorosis. *Correction:* Apply agricultural gypsum (1–2 tonnes/ha) and incorporate green manure (Dhaincha) or farmyard manure.
- **Action:** Test your soil every 2 years at your nearest Krishi Vigyan Kendra (KVK) to obtain a Soil Health Card.`,
      hi: `🌍 **मृदा पीएच (Soil pH) क्या होता है और इसका महत्व:**
- **परिभाषा:** मिट्टी का पीएच (pH) यह दर्शाता है कि मिट्टी अम्लीय (Acidic) है, क्षारीय (Alkaline) है या सामान्य (उदासीन) है। इसका पैमाना 0 से 14 तक होता है।
- **फसलों के लिए सर्वोत्तम स्तर:** अधिकांश फसलों के लिए **6.5 से 7.5 pH** आदर्श माना जाता है। इस स्तर पर पौधे नाइट्रोजन, फास्फोरस, पोटाश व सूक्ष्म पोषक तत्वों को आसानी से ग्रहण करते हैं।
- **अम्लीय मिट्टी (pH < 6.0):** अधिक वर्षा वाले क्षेत्रों में होती है। फास्फोरस का अवशोषण घटता है। 👉 *सुधार:* खेत में कृषि चूना (Lime) मिलाएं।
- **क्षारीय / उसर मिट्टी (pH > 8.0):** जिंक व लोहे की कमी हो जाती है। 👉 *सुधार:* अंतिम जुताई में जिप्सम (1-2 टन/हेक्टेयर) डालें तथा ढैंचा की हरी खाद या सड़ी गोबर खाद का प्रयोग करें।
- **सुझाव:** अपने नजदीकी कृषि विज्ञान केंद्र (KVK) से मृदा स्वास्थ्य कार्ड (Soil Health Card) अवश्य बनवाएं।`
    },

    yellow_leaves_general: {
      en: `🍃 **What to Do When Crop Leaves Turn Yellow:**
1. **Check Which Leaves Are Yellow:**
   - **Old (Lower) Leaves:** Indicates **Nitrogen deficiency**. Top-dress Urea or foliar spray 1–2% Urea (10–20g/L water).
   - **New (Upper) Leaves:** Indicates **Iron, Sulphur, or Zinc deficiency**. Spray 0.5% Zinc Sulphate + 1% Urea solution.
2. **Inspect for Fungal Diseases:** Check for yellow powdery stripes (Yellow Rust) or spots with yellow halos (Blight). Spray Mancozeb @ 2.5 g/L or Propiconazole @ 1 ml/L.
3. **Check Soil Drainage:** Waterlogged roots suffocate and turn the foliage pale yellow. Provide drainage channels immediately.
4. **Scout for Sap-Sucking Pests:** Aphids, whiteflies, or thrips on the underside of leaves cause yellow speckling and leaf curling. Spray Imidacloprid @ 0.5 ml/L or Neem oil (10,000 ppm) @ 5 ml/L.`,
      hi: `🍃 **फसल की पत्तियां पीली होने पर क्या करें:**
1. **देखें कौन सी पत्तियां पीली हैं:**
   - **निचली (पुरानी) पत्तियां:** यह **नाइट्रोजन की कमी** का संकेत है। यूरिया की टॉप ड्रेसिंग करें या 1-2% यूरिया (10-20 ग्राम/लीटर) का स्प्रे करें।
   - **ऊपरी (नई) पत्तियां:** यह **जिंक या सल्फर की कमी** है। 0.5% जिंक सल्फेट + 1% यूरिया का छिड़काव करें।
2. **फफूंद व रोग की जांच:** यदि पत्तियों पर पीला पाउडर (रतुआ) या धब्बे हैं, तो तुरंत मैंकोज़ेब @ 2.5 ग्राम/लीटर या प्रोपिकोनाज़ोल (टिल्ट) @ 1 मिली/लीटर का छिड़काव करें।
3. **खेत में जल निकास:** जलभराव से जड़ें घुटती हैं और फसल पीली पड़ती है। अतिरिक्त पानी तुरंत बाहर निकालें।
4. **रस चूसक कीटों की जांच:** पत्तियों के नीचे माहू या सफेद मक्खी होने पर इमिडाक्लोप्रिड @ 0.5 मिली/लीटर या 5 मिली नीम तेल प्रति लीटर पानी में मिलाकर छिड़कें।`
    },

    daily_task: {
      en: `🌱 **Daily Farm Inspection Checklist:**
1. **Soil Moisture Check:** Dig 2–3 inches deep near the root zone. Irrigate only if the soil crumbles and fails to form a ball in your hand.
2. **Pest & Disease Scouting:** Check the undersides of leaves and leaf axils for early aphid colonies, mites, or blight lesions.
3. **Weed Management:** Remove weeds while young to prevent them from stealing moisture and fertilizer.
4. **Fertilizer & Spray Timing:** Never spray chemicals or broadcast urea during harsh midday sun or when rain is expected. Early morning or late evening is optimal.
5. **Weather Watch:** Check humidity and temperature trends to anticipate fungal outbreaks or plan irrigation.`,
      hi: `🌱 **आज के लिए दैनिक कृषि कार्य सूची:**
1. **नमी की जांच:** खेत में 2-3 इंच गहराई पर मिट्टी उठाकर देखें। यदि लड्डू न बने तो ही हल्की सिंचाई करें।
2. **कीट व रोग निगरानी:** पत्तियों के निचले हिस्से की जांच करें कि कोई माहू, कीट या धब्बे तो नहीं हैं।
3. **निराई-गुड़ाई:** खरपतवार समय पर निकालें ताकि वे फसल का पोषण न छीनें।
4. **स्प्रे व खाद का सही समय:** तेज धूप या बारिश की संभावना में कीटनाशक स्प्रे या यूरिया बुरकाव न करें; सुबह या शाम का समय सबसे उत्तम है।
5. **मौसम पर नजर:** मौसम पूर्वानुमान देखकर ही सिंचाई या दवा छिड़काव का निर्णय लें।`
    },

    pest_control: {
      en: `🐛 **Pest Management & Crop Protection:**
1. **Sap-Sucking Insects (Aphids, Whiteflies, Thrips):** Cause leaf curling, sticky honeydew, and yellowing.
   - *Chemical Control:* Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25% WG @ 0.5 g/L.
   - *Organic Control:* Spray Neem oil (10,000 ppm) @ 5 ml/L with mild surfactant.
2. **Chewing Caterpillars & Borers (Spodoptera, Fruit/Stem Borer):** Bore into stems, shoots, or fruits and chew leaves.
   - *Remedy:* Spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L.
3. **Application Guidelines:** Spray during calm hours (early morning or late evening) ensuring thorough coverage of both leaf surfaces.`,
      hi: `🐛 **फसल में कीट (कीड़ा) नियंत्रण सलाह:**
1. **रस चूसक कीट (माहू, सफेद मक्खी, थ्रिप्स):** पत्तियां मुड़ती हैं और पीली होती हैं।
   - *रासायनिक दवा:* इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर अथवा थायमेथोक्सम 25% WG @ 0.5 ग्राम/लीटर का छिड़काव करें।
   - *जैविक उपाय:* 5 मिली नीम तेल (10,000 ppm) प्रति लीटर पानी में मिलाकर प्रारंभिक अवस्था में छिड़कें।
2. **इल्ली / सुंडी / छेदक कीट (तना व फल छेदक):** पत्तियों व तनों में छेद करते हैं।
   - *दवा:* क्लोरांट्रानिलीप्रोल 18.5% SC (Coragen) @ 0.3 मिली/लीटर अथवा एमामेक्टिन बेंजोएट 5% SG @ 0.5 ग्राम/लीटर पानी में घोलकर स्प्रे करें।
3. **सावधानी:** दोपहर की तेज धूप में दवा का छिड़काव न करें; सुबह या शाम के समय ही स्प्रे करें।`
    },

    damaged_crop: {
      en: `🌾 **Diagnosing & Treating Damaged Crops:**
Crop deterioration usually stems from one of four primary factors:
1. **Nutrient Starvation:** Yellowing from lower leaves indicates Nitrogen deficiency; yellowing from upper leaves points to Zinc/Sulphur. Apply appropriate foliar sprays.
2. **Fungal or Bacterial Blight:** Dark spots, rotting, or lesions on leaves/stems. Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin @ 1 ml/L.
3. **Pest Attack:** Chewed leaves or curled shoots. Scout for caterpillars or sucking bugs and treat accordingly.
4. **Waterlogging / Poor Aeration:** Heavy soils with standing water suffocate root tips. Ensure proper field drainage immediately.
👉 Please mention your crop name and describe the leaf/stem symptoms for exact treatment.`,
      hi: `🌾 **फसल में खराबी के मुख्य कारण और तुरंत उठाए जाने वाले कदम:**
आपकी फसल में मुख्य रूप से 4 कारणों से खराबी आ सकती है:
1. **पोषक तत्व की कमी:** पत्तियां नीचे से पीली पड़ रही हैं तो नाइट्रोजन की कमी हो सकती है। 1-2% यूरिया का पर्णीय छिड़काव करें।
2. **फफूंद / झुलसा रोग:** पत्तियों पर भूरे, काले या कत्थई धब्बे हैं तो मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर पानी में मिलाकर स्प्रे करें।
3. **कीटों का प्रकोप:** पत्तों के नीचे कीड़े या रस चूसक कीट देखें। आवश्यकतानुसार नीम तेल या कीटनाशक डालें।
4. **जलभराव या नमी की कमी:** जड़ों में पानी रुकने से जड़ें सड़ती हैं। उचित जल निकासी करें।
👉 कृपया फसल का नाम और विशिष्ट लक्षण (पत्तियों का रंग, धब्बे, या कीड़ा) बताएं ताकि सटीक दवा बताई जा सके।`
    },

    general_help: {
      en: `Hello! 🙏 I am your Kisan Agricultural Assistant. I can assist you with:
1. **Crop Cultivation Guides** (Wheat, Rice, Potato, Tomato, Cotton, Sugarcane, Corn, Soybean)
2. **Balanced Fertilizer (NPK) Schedules & Dosage**
3. **Irrigation Timing & Moisture Management**
4. **Pest & Disease Diagnosis and Spray Remedies**
5. **Soil Health & pH Correction**
👉 Please mention which crop you are growing and what question or problem you have!`,
      hi: `नमस्ते किसान भाई! 🙏 मैं आपका AI किसान कृषि सहायक हूँ। मैं निम्नलिखित विषयों में आपकी सहायता कर सकता हूँ:
1. **फसल बुवाई व संपूर्ण खेती विधि** (गेहूं, धान, आलू, टमाटर, कपास, मक्का, गन्ना आदि)
2. **संतुलित खाद प्रबंधन** (यूरिया, डीएपी, पोटाश, सूक्ष्म पोषक तत्व)
3. **सिंचाई का सही समय व जल प्रबंधन**
4. **रोग व कीट नियंत्रण** (झुलसा, रतुआ, इल्ली, माहू की रोकथाम)
5. **मिट्टी स्वास्थ्य व पीएच सुधार**
👉 आप किस फसल और किस समस्या के बारे में जानकारी चाहते हैं?`
    },

    irrigation: {
      en: `💧 **General Irrigation Principles:**
- Always irrigate during critical growth stages (such as CRI in wheat, flowering in vegetables, tuber bulking in potato).
- Drip irrigation saves 40–50% water and prevents foliar fungal infections.
- Avoid irrigating during windy hours to prevent crop lodging.`,
      hi: `💧 **सिंचाई प्रबंधन के मुख्य नियम:**
- फसल की क्रांतिक अवस्थाओं (जैसे गेहूं में CRI, सब्जियों में फूल आने, आलू में कंद बनने) पर सिंचाई अवश्य करें।
- ड्रिप सिंचाई से 40-50% पानी की बचत होती है और पत्तियों पर फफूंद नहीं लगती।
- तेज हवा के समय सिंचाई न करें ताकि फसल गिरे नहीं।`
    },

    fertilizer: {
      en: `🌱 **Balanced Fertilizer (NPK) Principles:**
- **Nitrogen (Urea):** Promotes vegetative growth; split into 2–3 applications to prevent leaching.
- **Phosphorus (DAP/SSP):** Fosters root establishment; apply full dose as basal at sowing.
- **Potash (MOP):** Enhances disease resistance, grain weight, and fruit/tuber quality.`,
      hi: `🌱 **संतुलित उर्वरक (NPK) सिद्धांत:**
- **नाइट्रोजन (यूरिया):** पौधों की बढ़वार के लिए है; इसे 2-3 बार में बांटकर दें।
- **फास्फोरस (DAP/SSP):** मजबूत जड़ों के लिए है; इसे बुवाई के समय नीचे दें।
- **पोटाश (MOP):** फसल को रोगों से लड़ने की शक्ति, दाने के वजन और चमक के लिए आवश्यक है।`
    },

    soil: {
      en: `🌍 **Soil Health Advice:**
- Test soil every 2–3 years at your local KVK.
- Optimal soil pH for most crops is 6.5 to 7.5. Apply gypsum in alkaline/sodic soils and agricultural lime in acidic soils.
- Incorporate 5–10 tonnes of FYM or green manure (Dhaincha) to restore soil organic carbon.`,
      hi: `🌍 **मृदा स्वास्थ्य सलाह:**
- प्रत्येक 2-3 वर्ष में अपने नजदीकी कृषि विज्ञान केंद्र (KVK) से मिट्टी की जांच कराएं।
- अधिकांश फसलों के लिए मिट्टी का पीएच 6.5 से 7.5 सर्वोत्तम है।
- ढैंचा की हरी खाद या सड़ी गोबर खाद मिलाने से मिट्टी की उर्वरता बढ़ती है।`
    },

    weather: {
      en: `⛅ **Weather-Responsive Farming Tips:**
I do not currently have live weather data available.
- **General Advisory:** If overcast or rain is forecasted, withhold irrigation and foliar fertilizer/pesticide sprays immediately.
- Avoid midday spraying under harsh sun; early morning or late evening is optimal.`,
      hi: `⛅ **मौसम आधारित कृषि सलाह:**
मेरे पास अभी लाइव मौसम डेटा उपलब्ध नहीं है।
- **सामान्य सलाह:** यदि आकाश में बादल हों या बारिश की संभावना हो तो सिंचाई और कीटनाशक का छिड़काव तुरंत रोक दें।
- तेज धूप में दोपहर के समय दवा न छिड़कें; सुबह या शाम का समय सबसे उत्तम है।`
    },

    mandi: {
      en: `📊 **Mandi & Market Advisory:**
I do not currently have live mandi price data available. Please check the 'Mandi' tab in the app for latest APMC market rates.
- Ensure grain moisture is below 12% before bringing produce to market for optimal pricing.
- Register on e-NAM for transparent electronic trading.`,
      hi: `📊 **मंडी एवं बाजार भाव सलाह:**
मेरे पास अभी लाइव मंडी भाव डेटा उपलब्ध नहीं है। आप ऐप के 'Mandi' टैब में जाकर अपनी नजदीकी मंडियों के ताज़ा भाव देख सकते हैं।
- अपनी उपज को मंडी ले जाने से पहले अनाज में नमी 12% से कम रखें ताकि सही भाव मिल सके।
- राष्ट्रीय कृषि बाजार (e-NAM) पोर्टल पर पंजीकरण कराएं।`
    }
  }
};

// Precise Hindi / Hinglish token regex with word boundaries
const HINDI_WORD_REGEX = /\b(bhai|ugane|ugana|ugaye|pura|tarika|batao|peeli|peele|pattiyan|pattiya|patte|kyon|kyu|rahi|rahe|hain|hai|kya|karu|kare|karein|kab|dena|chahiye|mere|meri|mera|paani|pani|kitna|kharab|keede|keeda|lag|gaye|gaya|gayi|hota|hote|kheti|kaise|mujhe|baare|mein|sahayata|fasal|khet|kisan|dawa|ilaj|khad|sinchai|sichai|beej|buwai|namaste|pranam|sookh|bhav|bimari|dhabbe|mitti|aalu|gehu|tamatar|dhan|chawal|upay)\b/i;

/**
 * Normalizes input text and identifies language.
 * Returns true if Hindi Devanagari or Hinglish intent.
 */
function isHindiMessage(text, lang) {
  if (lang === 'hi') return true;
  if (/[\u0900-\u097F]/.test(text)) return true;
  return HINDI_WORD_REGEX.test(text || '');
}

/**
 * Detects if the query is an off-topic non-agricultural query, specifically health/medical.
 */
function isMedicalQuery(text) {
  const lower = String(text).toLowerCase();
  const medicalTerms = [
    'pet me dard', 'pet dard', 'stomach pain', 'headache', 'sar dard', 'sir dard',
    'bukhar', 'fever', 'cough', 'khansi', 'vomit', 'ultiyan', 'dast', 'loose motion',
    'doctor', 'hospital', 'aspataal', 'tablet', 'bimar hu', 'tabiyat', 'chest pain',
    'body pain', 'dard hai', 'sick', 'illness', 'medicine for human'
  ];
  return medicalTerms.some(term => lower.includes(term));
}

/**
 * Identifies crop from user message.
 */
function detectCrop(text) {
  const lower = String(text).toLowerCase();
  if (lower.includes('potato') || lower.includes('aalu') || lower.includes('alu') || lower.includes('आलू')) return 'potato';
  if (lower.includes('wheat') || lower.includes('gehu') || lower.includes('gehun') || lower.includes('गेहूं') || lower.includes('कनक')) return 'wheat';
  if (lower.includes('rice') || lower.includes('paddy') || lower.includes('dhan') || lower.includes('chawal') || lower.includes('धान') || lower.includes('चावल')) return 'rice';
  if (lower.includes('tomato') || lower.includes('tamatar') || lower.includes('टमाटर')) return 'tomato';
  if (lower.includes('cotton') || lower.includes('kapas') || lower.includes('कपास')) return 'cotton';
  if (lower.includes('sugar') || lower.includes('ganna') || lower.includes('गन्ना')) return 'sugarcane';
  if (lower.includes('corn') || lower.includes('maize') || lower.includes('makka') || lower.includes('मक्का')) return 'corn';
  if (lower.includes('soy') || lower.includes('soya') || lower.includes('सोयाबीन')) return 'soybean';
  if (lower.includes('apple') || lower.includes('seb') || lower.includes('सेब')) return 'apple';
  if (lower.includes('grape') || lower.includes('angoor') || lower.includes('angur') || lower.includes('अंगूर')) return 'grape';
  return null;
}

/**
 * Identifies intent / topic from user message.
 */
function detectIntent(text) {
  const lower = String(text).toLowerCase();

  // 1. Greetings
  if (/^(hello|hi|hey|namaste|ram ram|pranam|नमस्ते|प्रणाम|राम राम)\b/i.test(lower) ||
      lower.includes('hello bhai') || lower.includes('hi bhai') || lower.includes('namaste bhai')) {
    return 'greeting';
  }

  // 2. Vague single-crop query needing clarification (e.g. "tomato me kya karu?", "aalu me kya karu?")
  if (lower.includes('kya karu') || lower.includes('kya kare') || lower.includes('kya karein') ||
      lower.includes('what should i do in') || lower.includes('me kya kare')) {
    if (lower.includes('tomato') || lower.includes('tamatar') || lower.includes('टमाटर') ||
        lower.includes('potato') || lower.includes('aalu') || lower.includes('wheat') || lower.includes('gehu')) {
      return 'crop_clarification';
    }
  }

  // 3. Complete cultivation / How to grow
  if (lower.includes('pura tarika') || lower.includes('kaise ugaye') || lower.includes('kheti kaise') ||
      lower.includes('how to grow') || lower.includes('cultivat') || lower.includes('ugane ka') ||
      lower.includes('ugaye') || lower.includes('ki kheti') || lower.includes('ugana')) {
    return 'cultivation';
  }

  // 4. Yellow leaves
  if (lower.includes('peeli') || lower.includes('peele') || lower.includes('पीली') || lower.includes('पीले') ||
      lower.includes('yellow') || lower.includes('chlorosis')) {
    return 'yellow_leaves';
  }

  // 5. Fertilizer / NPK / Urea
  if (lower.includes('fertiliz') || lower.includes('khad') || lower.includes('urea') ||
      lower.includes('यूरिया') || lower.includes('खाद') || lower.includes('उर्वरक') ||
      lower.includes('npk') || lower.includes('dap') || lower.includes('potash') ||
      lower.includes('डीएपी') || lower.includes('पोटाश') || lower.includes('poshan') || lower.includes('zinc')) {
    return 'fertilizer';
  }

  // 6. Irrigation / Water
  if (lower.includes('irrigat') || lower.includes('water') || lower.includes('paani') || lower.includes('pani') ||
      lower.includes('पानी') || lower.includes('सिंचाई') || lower.includes('sinchai') || lower.includes('sichai')) {
    return 'irrigation';
  }

  // 7. Pests / Insects
  if (lower.includes('pest') || lower.includes('insect') || lower.includes('keeda') || lower.includes('keede') ||
      lower.includes('कीट') || lower.includes('कीड़ा') || lower.includes('कीड़े') || lower.includes('worm') ||
      lower.includes('borer') || lower.includes('aphid') || lower.includes('माहू') || lower.includes('मक्खी') ||
      lower.includes('caterpillar') || lower.includes('इल्ली') || lower.includes('सुंडी')) {
    return 'pest';
  }

  // 8. Diseases / Blight / Rust / Fungus
  if (lower.includes('diseas') || lower.includes('blight') || lower.includes('rust') || lower.includes('fung') ||
      lower.includes('रोग') || lower.includes('बीमारी') || lower.includes('झुलसा') || lower.includes('रतुआ') ||
      lower.includes('धब्बे') || lower.includes('rot') || lower.includes('spot')) {
    return 'disease';
  }

  // 9. Damaged crop / Dying crop
  if (lower.includes('kharab') || lower.includes('खराब') || lower.includes('sookh') || lower.includes('सूख') ||
      lower.includes('damage') || lower.includes('destroy') || lower.includes('ruin') || lower.includes('dying')) {
    return 'damaged_crop';
  }

  // 10. Soil pH / Soil health
  if (lower.includes('soil ph') || lower.includes('ph kya') || lower.includes('what is soil ph') ||
      lower.includes('mitti') || lower.includes('मिट्टी') || lower.includes('soil') || lower.includes('पीएच')) {
    return 'soil';
  }

  // 11. Daily farm task / What should I do today
  if (lower.includes('what should i do today') || lower.includes('aaj kya karu') || lower.includes('today work') ||
      lower.includes('daily task') || lower.includes('aaj ka kaam')) {
    return 'daily_task';
  }

  // 12. General farming help
  if (lower.includes('help chahiye') || lower.includes('farming help') || lower.includes('sahayata') ||
      lower.includes('kheti ke baare me') || lower.includes('help in farming')) {
    return 'general_help';
  }

  // 13. Weather / Rain / Frost
  if (lower.includes('weather') || lower.includes('mausam') || lower.includes('मौसम') ||
      lower.includes('rain') || lower.includes('barish') || lower.includes('बारिश') ||
      lower.includes('pala') || lower.includes('पाला') || lower.includes('कोहरा')) {
    return 'weather';
  }

  // 14. Mandi / Price / Rates / MSP
  if (lower.includes('mandi') || lower.includes('price') || lower.includes('rate') ||
      lower.includes('bhav') || lower.includes('भाव') || lower.includes('मंडी') || lower.includes('msp')) {
    return 'mandi';
  }

  // 15. Sowing / Seeds / Spacing
  if (lower.includes('sow') || lower.includes('seed') || lower.includes('buwai') || lower.includes('बुवाई') ||
      lower.includes('beej') || lower.includes('बीज') || lower.includes('spacing')) {
    return 'sowing';
  }

  return 'unknown';
}

/**
 * Main Rule-Based Local Kisan Assistant Engine
 * 100% On-Device, Offline, Airplane-Mode Capable
 * NEVER returns null or technical error for ordinary questions.
 */
function generateLocalKisanBotReply(userMessage, context = {}, lang = 'en') {
  const msg = (userMessage || '').trim();
  const isHi = isHindiMessage(msg, lang);
  const langKey = isHi ? 'hi' : 'en';

  // 1. Off-Topic Medical Query Interceptor
  if (isMedicalQuery(msg)) {
    const reply = isHi
      ? "मैं कृषि और खेती से जुड़े सवालों में सहायता करता हूँ। स्वास्थ्य संबंधी समस्या के लिए कृपया योग्य चिकित्सक से सलाह लें।"
      : "I am an agriculture assistant focused on farming-related questions. Please consult a qualified medical professional for health concerns.";
    return { status: 'success', reply, intent: 'medical_disclaimer' };
  }

  // 2. Identify Intent & Crop
  const intent = detectIntent(msg);
  const userDetectedCrop = detectCrop(msg);
  const contextDetectedCrop = context.crop ? detectCrop(context.crop) : null;
  const activeCrop = userDetectedCrop || contextDetectedCrop || 'wheat';
  const cropData = LOCAL_KISAN_KNOWLEDGE.crops[activeCrop] || LOCAL_KISAN_KNOWLEDGE.crops.wheat;

  // 3. Greetings ("Hello bhai")
  if (intent === 'greeting') {
    const reply = isHi
      ? "नमस्ते किसान भाई! 🙏 राम-राम! मैं आपका AI किसान कृषि सहायक हूँ। मैं आपकी खेती और फसलों से जुड़े सभी सवालों में मदद के लिए उपलब्ध हूँ।\n\nआप अपनी किस फसल (जैसे **गेहूं, आलू, धान, टमाटर, कपास, मक्का, गन्ना**) या खेती के विषय (**खाद, सिंचाई, बुवाई, रोग पहचान, कीट रोकथाम, मिट्टी स्वास्थ्य**) के बारे में जानकारी चाहते हैं? कृपया बताएं!"
      : "Hello! 🙏 Greetings! I am your AI Kisan Agricultural Assistant. I am here to help you with all aspects of farming and crop management.\n\nWhich crop (such as **Wheat, Rice, Potato, Tomato, Cotton, Corn, Sugarcane**) or farming topic (**Fertilizer/NPK, Irrigation scheduling, Disease diagnosis, Pest control, Sowing methods, Soil health**) would you like help with today?";
    return { status: 'success', reply, intent: 'greeting' };
  }

  // 4. Clarification for Vague Queries (e.g. "Tomato me kya karu?")
  if (intent === 'crop_clarification') {
    if (activeCrop === 'tomato') {
      const reply = isHi
        ? "टमाटर में समस्या क्या है—पत्तियां पीली हैं, रोग है, कीट हैं या फल नहीं लग रहे? कृपया अपनी समस्या बताएं ताकि मैं आपको सही उपाय व दवा बता सकूँ।"
        : "What specific issue are you facing in your tomato crop—are leaves turning yellow, is there a disease, insect pests, or are fruits/flowers not setting? Please share details so I can guide you.";
      return { status: 'success', reply, intent: 'tomato_clarification' };
    }
    const cropName = isHi ? (cropData.name_hi || 'फसल') : (cropData.name_en || 'crop');
    const reply = isHi
      ? `${cropName} में समस्या क्या है—पत्तियां पीली हैं, खाद/पानी का समय जानना है, कीट या रोग लगा है? कृपया अपनी समस्या बताएं ताकि मैं आपको सही समाधान दे सकूँ।`
      : `What specific issue are you facing in your ${cropName} crop—are leaves turning yellow, do you need fertilizer/irrigation timing, or is there a pest or disease? Please provide more details.`;
    return { status: 'success', reply, intent: 'crop_clarification' };
  }

  // 5. Complete Crop Cultivation ("Aalu ugane ka pura tarika batao", "rice kaise ugaye?")
  if (intent === 'cultivation') {
    // If user asked about a specific supported crop
    if (userDetectedCrop && cropData.cultivation && cropData.cultivation[langKey]) {
      return { status: 'success', reply: cropData.cultivation[langKey], intent: `${userDetectedCrop}_cultivation` };
    }
    // If context crop exists and user didn't mention another crop
    if (!userDetectedCrop && contextDetectedCrop && cropData.cultivation && cropData.cultivation[langKey]) {
      return { status: 'success', reply: cropData.cultivation[langKey], intent: `${contextDetectedCrop}_cultivation` };
    }
    // If unknown crop cultivation requested
    const unknownReply = isHi
      ? "मैं आपकी खेती से जुड़ी इस समस्या में मदद कर सकता हूँ। कृपया फसल का नाम और समस्या थोड़ी विस्तार से बताएं ताकि मैं आपको सटीक समाधान दे सकूँ।"
      : "I can help you with this agricultural question. Please mention the crop name and your specific concern in detail so I can provide precise guidance.";
    return { status: 'success', reply: unknownReply, intent: 'unknown_cultivation' };
  }

  // 6. Yellow Leaves ("गेहूं में पीली पत्तियां क्यों हो रही हैं?", "What should I do if leaves are yellow?")
  if (intent === 'yellow_leaves') {
    if (userDetectedCrop && cropData.yellow_leaves && cropData.yellow_leaves[langKey]) {
      return { status: 'success', reply: cropData.yellow_leaves[langKey], intent: `${userDetectedCrop}_yellow_leaves` };
    }
    if (!userDetectedCrop && contextDetectedCrop && cropData.yellow_leaves && cropData.yellow_leaves[langKey]) {
      return { status: 'success', reply: cropData.yellow_leaves[langKey], intent: `${contextDetectedCrop}_yellow_leaves` };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.yellow_leaves_general[langKey], intent: 'yellow_leaves_general' };
  }

  // 7. Fertilizer ("fertilizer for wheat", "Tomato me fertilizer kab dena chahiye?")
  if (intent === 'fertilizer') {
    if (cropData.fertilizer && cropData.fertilizer[langKey]) {
      return { status: 'success', reply: cropData.fertilizer[langKey], intent: `${activeCrop}_fertilizer` };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.fertilizer[langKey], intent: 'fertilizer_general' };
  }

  // 8. Irrigation ("mere crop me paani kitna dena hai?", "How often should I irrigate potato?")
  if (intent === 'irrigation') {
    if (cropData.irrigation && cropData.irrigation[langKey]) {
      return { status: 'success', reply: cropData.irrigation[langKey], intent: `${activeCrop}_irrigation` };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.irrigation[langKey], intent: 'irrigation_general' };
  }

  // 9. Pest Management ("meri fasal me keede lag gaye hain")
  if (intent === 'pest') {
    if (cropData.pest && cropData.pest[langKey]) {
      return { status: 'success', reply: cropData.pest[langKey], intent: `${activeCrop}_pest` };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.pest_control[langKey], intent: 'pest_general' };
  }

  // 10. Disease Management
  if (intent === 'disease') {
    if (cropData.diseases && cropData.diseases[langKey]) {
      return { status: 'success', reply: cropData.diseases[langKey], intent: `${activeCrop}_disease` };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.damaged_crop[langKey], intent: 'disease_general' };
  }

  // 11. Damaged Crop ("meri fasal kharab ho rahi hai")
  if (intent === 'damaged_crop') {
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.damaged_crop[langKey], intent: 'damaged_crop' };
  }

  // 12. Soil & Soil pH ("soil pH kya hota hai?", "what is soil pH?")
  if (intent === 'soil') {
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.soil_ph[langKey], intent: 'soil_ph' };
  }

  // 13. Daily Farm Inspection Checklist ("what should I do today?")
  if (intent === 'daily_task') {
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.daily_task[langKey], intent: 'daily_task' };
  }

  // 14. General Farming Help ("mujhe farming ke baare me help chahiye")
  if (intent === 'general_help') {
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.general_help[langKey], intent: 'general_help' };
  }

  // 15. Weather-responsive farming
  if (intent === 'weather') {
    if (context.weather && context.weather.current) {
      const cur = context.weather.current;
      const temp = Math.round(cur.temp || 25);
      const desc = cur.description || (isHi ? 'सामान्य मौसम' : 'Normal conditions');
      const rain = cur.rain_probability || 0;
      const locName = (context.locationData && context.locationData.city) || (context.location) || (isHi ? 'आपका क्षेत्र' : 'Your Farm');
      const weatherAdvice = isHi
        ? `⛅ **${locName} मौसम एवं कृषि परामर्श:**\n\n- **वर्तमान तापमान:** ${temp}°C (${desc})\n- **बारिश का अनुमान:** ${rain}%\n\n${rain > 40 ? '⚠️ **सावधानी:** आपके क्षेत्र में बारिश की संभावना है। यूरिया बुरकाव या कीटनाशक स्प्रे टालें ताकि दवा बह न जाए।' : '✅ **सलाह:** वर्तमान मौसम सामान्य है। खेत में निराई-गुड़ाई व अनुशंसित सिंचाई कर सकते हैं।'}\n\nमिट्टी की नमी जांचकर ही अगली सिंचाई का निर्णय लें।`
        : `⛅ **${locName} Weather & Crop Advisory:**\n\n- **Current Temperature:** ${temp}°C (${desc})\n- **Rain Probability:** ${rain}%\n\n${rain > 40 ? '⚠️ **Caution:** Rain expected in the region. Delay spraying pesticides or broadcasting urea.' : '✅ **Advisory:** Weather is favorable for field operations and routine irrigation.'}\n\nCheck soil moisture before irrigating.`;
      return { status: 'success', reply: weatherAdvice, intent: 'weather_context_advisory' };
    }
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.weather[langKey], intent: 'weather_general' };
  }

  // 16. Mandi Prices
  if (intent === 'mandi') {
    return { status: 'success', reply: LOCAL_KISAN_KNOWLEDGE.topics.mandi[langKey], intent: 'mandi_general' };
  }

  // 17. Sowing / Seed
  if (intent === 'sowing') {
    if (cropData.cultivation && cropData.cultivation[langKey]) {
      return { status: 'success', reply: cropData.cultivation[langKey], intent: `${activeCrop}_sowing` };
    }
  }

  // 18. Crop match fallback if a supported crop is mentioned without a specific recognized intent
  if (userDetectedCrop && cropData.cultivation && cropData.cultivation[langKey]) {
    return { status: 'success', reply: cropData.cultivation[langKey], intent: `${userDetectedCrop}_general` };
  }

  // 19. Teacher / Unexpected / Unknown Question Fallback
  // MUST NEVER return empty or technical error!
  const unknownReply = isHi
    ? "मैं आपकी खेती से जुड़ी इस समस्या में मदद कर सकता हूँ। कृपया फसल का नाम और समस्या थोड़ी विस्तार से बताएं ताकि मैं आपको सटीक समाधान दे सकूँ।"
    : "I can help you with this agricultural question. Please mention the crop name and your specific concern in detail so I can provide precise guidance.";

  return {
    status: 'success',
    reply: unknownReply,
    intent: 'unknown_farming_question'
  };
}

if (typeof window !== 'undefined') {
  window.generateLocalKisanBotReply = generateLocalKisanBotReply;
  window.LOCAL_KISAN_KNOWLEDGE = LOCAL_KISAN_KNOWLEDGE;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    generateLocalKisanBotReply,
    LOCAL_KISAN_KNOWLEDGE,
    isHindiMessage,
    detectCrop,
    detectIntent
  };
}
