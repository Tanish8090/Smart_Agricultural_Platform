import json
import os

knowledge = {
    "crops": {
        "wheat": {
            "name_en": "Wheat",
            "name_hi": "गेहूं",
            "irrigation": {
                "en": "Wheat requires 4 to 6 irrigations depending on soil moisture:\n1. Crown Root Initiation (CRI) at 20-25 days after sowing (most critical).\n2. Tillering stage (40-45 days).\n3. Late jointing stage (60-65 days).\n4. Flowering stage (80-85 days).\n5. Milking stage (100-105 days).\n6. Dough stage (115-120 days). Avoid heavy irrigation on windy days to prevent lodging.",
                "hi": "गेहूं की फसल में सामान्यतः 4 से 6 सिंचाइयों की आवश्यकता होती है:\n1. पहली सिंचाई: बुवाई के 20-25 दिन बाद (शिखर जड़ें निकलते समय/CRI) - यह सबसे महत्वपूर्ण है।\n2. दूसरी सिंचाई: कल्ले फूटते समय (40-45 दिन)।\n3. तीसरी सिंचाई: गाभा निकलने/गांठ बनते समय (60-65 दिन)।\n4. चौथी सिंचाई: फूल आने/बाली निकलते समय (80-85 दिन)।\n5. पांचवीं सिंचाई: दूधिया अवस्था (100-105 दिन)।\n6. छठी सिंचाई: दाना भरते समय (115-120 दिन)। तेज हवा वाले दिन सिंचाई न करें जिससे फसल गिरे नहीं।"
            },
            "fertilizer": {
                "en": "Recommended NPK dosage for irrigated timely-sown wheat is 120:60:40 kg/ha:\n- Basal application: Entire Phosphorus (60 kg P2O5 via DAP/SSP), entire Potash (40 kg K2O via MOP), and 1/3rd Nitrogen (40 kg N).\n- First top-dressing: 1/3rd Nitrogen (40 kg N via Urea) at 1st irrigation (21-25 days).\n- Second top-dressing: Remaining 1/3rd Nitrogen at 2nd irrigation/tillering (45 days).\n- Zinc deficiency: Apply 25 kg Zinc Sulfate (21%) per hectare during land preparation.",
                "hi": "गेहूं की सिंचित फसल के लिए अनुशंसित NPK अनुपात 120:60:40 किग्रा/हेक्टेयर है:\n- बुवाई के समय: पूरा फास्फोरस (DAP या सिंगल सुपर फॉस्फेट से 60 किग्रा), पूरा पोटाश (MOP से 40 किग्रा) और 1/3 नाइट्रोजन (लगभग 50 किग्रा यूरिया)।\n- पहली टॉप-ड्रेसिंग: पहली सिंचाई पर (21-25 दिन) 1/3 यूरिया डालें।\n- दूसरी टॉप-ड्रेसिंग: कल्ले फूटते समय (40-45 दिन) बची हुई 1/3 यूरिया डालें।\n- जिंक की कमी होने पर खेत की तैयारी में 25 किग्रा जिंक सल्फेट प्रति हेक्टेयर डालें।"
            },
            "sowing": {
                "en": "Sowing time: Optimal window is November 1 to November 25. Late sowing from November 25 to December 15 reduces yield.\n- Seed rate: 100 kg/ha for timely sown, 125 kg/ha for late sown.\n- Spacing: 20-22.5 cm between rows, depth 4-5 cm.\n- Seed treatment: Treat with Carbendazim @ 2g/kg or Trichoderma @ 5g/kg seed before sowing.",
                "hi": "बुवाई का समय: उचित समय 1 नवंबर से 25 नवंबर है। पछेती बुवाई 25 नवंबर से 15 दिसंबर तक की जा सकती है।\n- बीज दर: सामान्य बुवाई हेतु 100 किग्रा/हेक्टेयर, पछेती बुवाई हेतु 125 किग्रा/हेक्टेयर।\n- कतार से कतार दूरी: 20 से 22.5 सेमी और गहराई 4 से 5 सेमी रखें।\n- बीज उपचार: बुवाई से पहले कार्बेन्डाजिम 2 ग्राम या ट्राइकोडर्मा 5 ग्राम प्रति किग्रा बीज से उपचारित करें।"
            },
            "diseases": {
                "en": "Common wheat diseases:\n- Yellow / Stripe Rust: Yellow powdery pustules in linear stripes. Spray Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole @ 1.25 ml/L.\n- Brown / Leaf Rust: Round orange-brown pustules scattered on leaf blades.\n- Loose Smut: Seed heads turn into black powdery mass. Controlled by seed treatment with Vitavax @ 2.5g/kg.",
                "hi": "गेहूं के प्रमुख रोग:\n- पीला रतुआ (Yellow Rust): पत्तियों पर पीली धारियां बनती हैं। रोकथाम के लिए प्रोपिकोनाज़ोल 25% EC (टिल्ट) @ 1 मिली/लीटर अथवा टेबुकोनाज़ोल @ 1.25 मिली/लीटर पानी में घोलकर छिड़कें।\n- भूरा रतुआ (Brown Rust): पत्तियों पर बिखरे हुए नारंगी-भूरे धब्बे।\n- कंडुआ रोग (Loose Smut): बालियों में काले चूर्ण जैसी फफूंद। बुवाई पूर्व वीटावैक्स से बीज उपचार करें।"
            },
            "pest": {
                "en": "Major pests of wheat:\n- Aphids (Mahoo): Suck sap from leaves and ears. Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Dimethoate 30% EC @ 1.5 ml/L if population exceeds 10-15 aphids/tiller.\n- Termites: Treat seed with Chlorpyriphos 20% EC @ 3-4 ml/kg seed before sowing.",
                "hi": "गेहूं के मुख्य कीट:\n- माहू (Aphids): रस चूसते हैं। 10-15 माहू प्रति टिलर होने पर इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर या डाइमेथोएट 30% EC @ 1.5 मिली/लीटर स्प्रे करें।\n- दीमक (Termite): बुवाई से पहले बीज को क्लोरपायरीफॉस 20% EC @ 3-4 मिली/किग्रा बीज से उपचारित करें।"
            },
            "stages": {
                "en": "Wheat growth stages: Germination (0-7 days) -> Crown Root Initiation (20-25 days) -> Tillering (35-45 days) -> Jointing (55-65 days) -> Booting/Flowering (75-85 days) -> Milk stage (95-105 days) -> Dough stage (110-120 days) -> Maturity (125-140 days).",
                "hi": "गेहूं की फसल अवस्थाएं: अंकुरण (0-7 दिन) -> सीआरआई/शिखर जड़ें (20-25 दिन) -> कल्ले फूटना (35-45 दिन) -> गाभा/गांठ बनना (55-65 दिन) -> फूल व बाली आना (75-85 दिन) -> दूधिया अवस्था (95-105 दिन) -> दाना कड़ा होना (110-120 दिन) -> पकने की अवस्था (125-140 दिन)।"
            }
        },
        "rice": {
            "name_en": "Rice / Paddy",
            "name_hi": "धान",
            "irrigation": {
                "en": "Keep shallow standing water (2-3 cm) for the first 3 weeks after transplanting. Drain water for 2-3 days during maximum tillering to aerate roots. Maintain 5 cm water during panicle initiation and flowering. Drain completely 10-14 days before harvest.",
                "hi": "रोपाई के बाद पहले 3 सप्ताह तक 2-3 सेमी उथला पानी बनाए रखें। कल्ले फूटते समय 2-3 दिन पानी निकालें ताकि जड़ों को हवा मिल सके। बाली निकलने और फूल आने के समय 5 सेमी पानी रखें। कटाई से 10-14 दिन पहले पानी पूरी तरह निकाल दें।"
            },
            "fertilizer": {
                "en": "Recommended NPK: 100-120 kg N, 50-60 kg P2O5, 40-50 kg K2O, and 25 kg Zinc Sulfate per hectare. Apply all P, K, and Zinc as basal. Split Nitrogen in 3 equal parts: basal, active tillering (3 weeks after transplanting), and panicle initiation.",
                "hi": "धान हेतु उर्वरक मात्रा: 100-120 किग्रा नाइट्रोजन, 50-60 किग्रा फास्फोरस, 40-50 किग्रा पोटाश और 25 किग्रा जिंक सल्फेट प्रति हेक्टेयर। फास्फोरस, पोटाश और जिंक बुवाई/रोपाई पर दें। नाइट्रोजन को 3 बराबर भागों में बांटें: रोपाई पर, कल्ले फूटते समय (3 सप्ताह बाद) और बाली निकलते समय।"
            },
            "sowing": {
                "en": "Nursery sowing: May 15 to June 15. Transplanting: June 15 to July 15 with 20-25 days old seedlings. Spacing: 20x15 cm with 2-3 seedlings per hill.",
                "hi": "नर्सरी की बुवाई: 15 मई से 15 जून। रोपाई: 15 जून से 15 जुलाई (20-25 दिन के पौधे)। रोपाई की दूरी 20x15 सेमी रखें तथा एक स्थान पर 2-3 पौधे लगाएं।"
            },
            "diseases": {
                "en": "Common rice diseases:\n- Blast: Spindle-shaped spots with gray center. Spray Tricyclazole 75% WP @ 0.6 g/L or Kasugamycin 3% SL @ 2 ml/L.\n- Brown Spot: Oval brown lesions. Spray Propiconazole 25% EC @ 1 ml/L; ensure balanced potassium application.\n- Bacterial Leaf Blight: Yellowing leaves from tips. Spray Copper Oxychloride (2.5 g/L) + Streptocycline (0.1 g/L).",
                "hi": "धान के प्रमुख रोग:\n- ब्लास्ट (झोंका रोग): पत्तियों पर नाव के आकार के भूरे धब्बे। ट्राइसाइक्लाजोल 75% WP @ 0.6 ग्राम/लीटर या कासुगामाइसिन @ 2 मिली/लीटर का छिड़काव करें।\n- भूरा धब्बा (Brown Spot): प्रोपिकोनाज़ोल 25% EC @ 1 मिली/लीटर स्प्रे करें और पोटाश खाद की कमी न होने दें।\n- जीवाणु झुलसा (BLB): कॉपर ऑक्सीक्लोराइड 2.5 ग्राम + स्ट्रेप्टोसाइक्लिन 1 ग्राम प्रति 10 लीटर पानी में मिलाकर छिड़कें।"
            },
            "pest": {
                "en": "Rice stem borer (dead hearts), brown planthopper (BPH), and leaf folder. For stem borer, apply Cartap Hydrochloride 4G @ 10 kg/acre or spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L. For BPH, avoid excess urea and spray Pymetrozine 50% WG @ 0.6 g/L.",
                "hi": "तना छेदक (डेड हार्ट), भूरा फुदका (BPH) और पत्ता लपेटक मुख्य कीट हैं। तना छेदक के लिए कोरोजन (क्लोरांट्रानिलीप्रोल 18.5% SC) @ 0.3 मिली/लीटर स्प्रे करें या कारटाप हाइड्रोक्लोराइड 4G दानेदार डालें। बीपीएच के लिए पाइमेट्रोज़िन 50% WG @ 0.6 ग्राम/लीटर छिड़कें।"
            },
            "stages": {
                "en": "Rice stages: Nursery (0-25 days) -> Tillering (25-50 days) -> Stem elongation & Panicle initiation (50-75 days) -> Heading & Flowering (75-90 days) -> Milking & Dough (90-115 days) -> Harvest maturity (120-140 days).",
                "hi": "धान की अवस्थाएं: नर्सरी (0-25 दिन) -> कल्ले फूटना (25-50 दिन) -> बाली का बनना (50-75 दिन) -> फूल आना (75-90 दिन) -> दूधिया व दाना भराव (90-115 दिन) -> परिपक्वता व कटाई (120-140 दिन)।"
            }
        },
        "potato": {
            "name_en": "Potato",
            "name_hi": "आलू",
            "irrigation": {
                "en": "Irrigate frequently but moderately. First irrigation after planting before emergence. Subsequent irrigations every 7-10 days. Maintain 65-75% soil moisture during tuber formation. Stop irrigation 10-12 days before digging to harden tuber skins.",
                "hi": "हल्की और नियमित सिंचाई करें। पहली सिंचाई बुवाई के तुरंत बाद। बाद में 7-10 दिन के अंतराल पर सिंचाई करें। कंद बनते समय खेत में नमी 65-75% रहनी चाहिए। आलू खुदाई से 10-12 दिन पहले सिंचाई बंद कर दें ताकि छिलका कड़ा हो सके।"
            },
            "fertilizer": {
                "en": "Recommended NPK: 150-180 kg N, 80-100 kg P2O5, and 120-150 kg K2O per hectare. Potatoes require high Potash (MOP/SOP) for tuber size and starch. Apply all P, K, and 50% N at planting. Top-dress remaining 50% N during first earthing-up (30-35 days).",
                "hi": "आलू हेतु NPK मात्रा: 150-180 किग्रा नाइट्रोजन, 80-100 किग्रा फास्फोरस, 120-150 किग्रा पोटाश प्रति हेक्टेयर। कंदों के अच्छे विकास हेतु पोटाश बहुत आवश्यक है। फास्फोरस, पोटाश और आधी नाइट्रोजन बुवाई पर दें। शेष आधी नाइट्रोजन पहली मिट्टी चढ़ाते समय (30-35 दिन पर) दें।"
            },
            "sowing": {
                "en": "Planting time: Northern plains optimal is October 15 to November 5. Seed rate: 25-30 qtl/ha of cut or whole certified tubers (40-50g each). Spacing: 60 cm between ridges, 20 cm between tubers.",
                "hi": "बुवाई का समय: 15 अक्टूबर से 5 नवंबर। बीज दर: 25-30 क्विंटल/हेक्टेयर (40-50 ग्राम आकार के रोगमुक्त कंद)। दूरी: मेड़ से मेड़ 60 सेमी और कंद से कंद 20 सेमी रखें।"
            },
            "diseases": {
                "en": "Blights of Potato:\n- Early Blight: Dark concentric circular rings. Spray Mancozeb 75% WP @ 2.5 g/L.\n- Late Blight: Devastating water-soaked lesions that blacken leaf edges with white mold underneath. Spray Cymoxanil 8% + Mancozeb 64% (Curzate @ 2.5 g/L) or Dimethomorph 50% WP @ 1 g/L immediately upon detection.",
                "hi": "आलू के झुलसा रोग:\n- अगेती झुलसा: पत्तियों पर गोल छल्लेदार कत्थई धब्बे। मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।\n- पछेती झुलसा (Late Blight): पत्तियों के किनारों पर काले-भूरे जलसिक्त धब्बे जो तेजी से फैलते हैं। साइमोक्सानिल + मैंकोज़ेब (Curzate @ 2.5 ग्राम/लीटर) अथवा डाइमेशोमॉर्फ @ 1 ग्राम/लीटर का तुरंत छिड़काव करें।"
            },
            "pest": {
                "en": "Aphids (virus vectors) and potato tuber moth (PTM). For aphids, spray Imidacloprid 17.8% SL @ 0.5 ml/L. For PTM, earth up well to keep tubers covered and install sex pheromone traps.",
                "hi": "माहू (एफिड) और आलू कंद शलभ (PTM) मुख्य कीट हैं। माहू वायरस फैलाता है, रोकथाम हेतु इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर स्प्रे करें। कंदों पर अच्छी तरह मिट्टी चढ़ाकर रखें ताकि कीट अंदर न जा सकें।"
            },
            "stages": {
                "en": "Sprout development (0-20 days) -> Vegetative growth (20-35 days) -> Tuber initiation (35-50 days) -> Tuber bulking (50-75 days) -> Maturation & skin hardening (75-95 days).",
                "hi": "अंकुरण (0-20 दिन) -> वानस्पतिक बढ़वार (20-35 दिन) -> कंद बनना (35-50 दिन) -> कंद का आकार बढ़ना (50-75 दिन) -> कंद पकना व छिलका सख्त होना (75-95 दिन)।"
            }
        },
        "tomato": {
            "name_en": "Tomato",
            "name_hi": "टमाटर",
            "irrigation": {
                "en": "Use drip irrigation for best results. Keep moisture consistent to avoid blossom end rot and fruit cracking. Avoid overhead watering to reduce fungal disease spread.",
                "hi": "टमाटर में ड्रिप सिंचाई सबसे उत्तम है। मिट्टी में समान नमी बनाए रखें जिससे फल फटने और सड़ांध की समस्या न हो। पौधों के ऊपर से पानी छिड़कने से बचें ताकि फफूंद न फैले।"
            },
            "fertilizer": {
                "en": "NPK 120:80:100 kg/ha. Apply 20 tonnes FYM during bed preparation. Apply all P, half N, and half K at transplanting. Top-dress remaining N and K in 2 splits at flowering and fruit set.",
                "hi": "NPK मात्रा: 120:80:100 किग्रा/हेक्टेयर। बुवाई से पहले 20 टन गोबर की खाद मिलाएं। फास्फोरस पूरा, आधी नाइट्रोजन और आधा पोटाश रोपाई पर दें। शेष नाइट्रोजन व पोटाश को फूल व फल आते समय दो बार में दें।"
            },
            "sowing": {
                "en": "Nursery sowing for Rabi in Sept-Oct; for Kharif in June-July. Transplant seedlings after 25-30 days with spacing of 60x45 cm.",
                "hi": "रबी टमाटर की नर्सरी सितंबर-अक्टूबर में और खरीफ की जून-जुलाई में लगाएं। 25-30 दिन की पौध को 60x45 सेमी की दूरी पर मेड़ बनाकर रोपें।"
            },
            "diseases": {
                "en": "Early Blight and Late Blight on tomato leaves and fruit. Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 23% SC @ 1 ml/L. For leaf curl virus, manage whiteflies.",
                "hi": "अगेती व पछेती झुलसा: पत्तियों पर काले-भूरे धब्बे। मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर अथवा एजोक्सीस्ट्रोबिन @ 1 मिली/लीटर स्प्रे करें। पर्ण कुंचन (लीफ कर्ल) वायरस सफेद मक्खी द्वारा फैलता है, मक्खी पर नियंत्रण रखें।"
            },
            "pest": {
                "en": "Fruit borer (Helicoverpa) and whitefly. Spray Emamectin Benzoate 5% SG @ 0.5 g/L for fruit borer. Spray Imidacloprid @ 0.5 ml/L for whitefly.",
                "hi": "फल छेदक इल्ली और सफेद मक्खी। फल छेदक के लिए इमामेक्टिन बेंजोएट 5% SG @ 0.5 ग्राम/लीटर का छिड़काव करें। सफेद मक्खी हेतु इमिडाक्लोप्रिड @ 0.5 मिली/लीटर स्प्रे करें।"
            },
            "stages": {
                "en": "Nursery (0-30 days) -> Vegetative (30-50 days) -> Flowering & Fruit set (50-75 days) -> Fruit development & Harvesting (75-120 days).",
                "hi": "नर्सरी (0-30 दिन) -> बढ़वार (30-50 दिन) -> फूल व फल आना (50-75 दिन) -> फल विकास व तुड़ाई (75-120 दिन)।"
            }
        },
        "cotton": {
            "name_en": "Cotton",
            "name_hi": "कपास",
            "irrigation": {
                "en": "Cotton is sensitive to waterlogging. Critical stages are flowering (boll formation) and boll development. Ensure good field drainage during heavy rains.",
                "hi": "कपास जलभराव के प्रति संवेदनशील है। फूल आने और गूलर (Boll) बनते समय सिंचाई सबसे महत्वपूर्ण है। अधिक वर्षा में खेत से जल निकासी की व्यवस्था रखें।"
            },
            "fertilizer": {
                "en": "NPK: 120-150 kg N, 60 kg P2O5, 60 kg K2O/ha for Bt cotton. Apply N in 3 splits (squaring, flowering, boll development). Apply 25 kg Zinc Sulfate at sowing.",
                "hi": "बीटी कपास हेतु NPK 120-150:60:60 किग्रा/हेक्टेयर। नाइट्रोजन को 3 भागों में दें (डोडिया बनते, फूल आते और गूलर बनते समय)। खेत की तैयारी में 25 किग्रा जिंक सल्फेट दें।"
            },
            "sowing": {
                "en": "Sowing window: April-May in North India, June with monsoon onset in Central/South India. Spacing: 90x60 cm or 120x45 cm.",
                "hi": "बुवाई का समय: उत्तर भारत में अप्रैल-मई तथा मध्य व दक्षिण भारत में मानसून आने पर (जून)। दूरी 90x60 सेमी अथवा 120x45 सेमी रखें।"
            },
            "diseases": {
                "en": "Bacterial Blight (angular leaf spots and black arm). Spray Copper Oxychloride 50% WP @ 2.5 g/L mixed with Streptocycline @ 0.1 g/L.",
                "hi": "जीवाणु झुलसा (Bacterial Blight): पत्तियों पर कोणीय भूरे-काले धब्बे और तने पर काली धारियां। कॉपर ऑक्सीक्लोराइड 50% WP @ 2.5 ग्राम + स्ट्रेप्टोसाइक्लिन 1 ग्राम प्रति 10 लीटर पानी में मिलाकर छिड़कें।"
            },
            "pest": {
                "en": "Pink bollworm, whiteflies, and aphids. Use pheromone traps (5/acre) for monitoring pink bollworm. Spray Flonicamid 50% WG @ 0.4 g/L for sucking pests.",
                "hi": "गुलाबी सुंडी (Pink Bollworm), सफेद मक्खी व थ्रिप्स। गुलाबी सुंडी निगरानी हेतु फेरोमोन ट्रैप (5 प्रति एकड़) लगाएं। रस चूसक कीटों के लिए फ्लोनिकामिड 50% WG @ 0.4 ग्राम/लीटर छिड़कें।"
            },
            "stages": {
                "en": "Germination (0-10 days) -> Squaring (35-50 days) -> Flowering (55-80 days) -> Boll development (80-120 days) -> Boll bursting & picking (120-170 days).",
                "hi": "अंकुरण (0-10 दिन) -> डोडिया बनना (35-50 दिन) -> फूल आना (55-80 दिन) -> गूलर विकास (80-120 दिन) -> गूलर फटना व चुनाई (120-170 दिन)।"
            }
        },
        "sugarcane": {
            "name_en": "Sugarcane",
            "name_hi": "गन्ना",
            "irrigation": {
                "en": "Water-intensive crop requiring 15-20 irrigations annually. Critical period is tillering and grand growth stage (every 8-10 days in summer; 15-20 days in winter). Use trash mulching to conserve moisture.",
                "hi": "गन्ना अधिक पानी चाहने वाली फसल है। गर्मी में 8-10 दिन और सर्दी में 15-20 दिन पर सिंचाई करें। कल्ले फूटते और तना बढ़ते समय नमी आवश्यक है। पत्ती की मल्चिंग कर नमी बचाएं।"
            },
            "fertilizer": {
                "en": "NPK: 150-200 kg N, 60-80 kg P2O5, 60 kg K2O per hectare. All P and K at planting. Split N: 1/3 at planting, 1/3 at 60 days, and 1/3 at 90-120 days during earthing-up.",
                "hi": "NPK मात्रा: 150-200 किग्रा नाइट्रोजन, 60-80 किग्रा फास्फोरस, 60 किग्रा पोटाश प्रति हेक्टेयर। पूरा फास्फोरस व पोटाश बुवाई पर दें। नाइट्रोजन को तीन बार में (बुवाई पर, 60 दिन पर और 90 दिन पर मिट्टी चढ़ाते समय) दें।"
            },
            "sowing": {
                "en": "Spring planting: Feb-March; Autumn planting: Oct-Nov. Plant 2-3 budded healthy setts at 75-90 cm row distance. Treat setts with Carbendazim (1g/L) for 15 minutes.",
                "hi": "बुवाई का समय: वसंत ऋतु (फरवरी-मार्च) अथवा शरद ऋतु (अक्टूबर-नवंबर)। 75-90 सेमी की कतारों में 2-3 आंख वाले गूलों की बुवाई करें। गूलों को कार्बेन्डाजिम (1 ग्राम/लीटर) घोल में 15 मिनट डुबोकर उपचारित करें।"
            },
            "diseases": {
                "en": "Red Rot: Red discolouration of internal pith with white cross-bands and alcohol odour. Use disease-free setts, hot water treatment (52°C for 30 min), and avoid ratooning infected crop.",
                "hi": "लाल सड़न (Red Rot): गन्ने को चीरने पर अंदर लाल रंग, सफेद धारियां और शराब जैसी बदबू। रोगमुक्त बीज गूलों का प्रयोग करें, 52°C गर्म पानी में 30 मिनट उपचार करें, रोगग्रस्त खेत में पेड़ी न रखें।"
            },
            "pest": {
                "en": "Early shoot borer and top borer. Apply Chlorantraniliprole 0.4% G (Ferterra) @ 7.5 kg/acre during early vegetative stage or spray Coragen @ 0.4 ml/L.",
                "hi": "तना छेदक (Shoot borer) व चोटी बेधक (Top borer)। फेरटेरा (क्लोरांट्रानिलीप्रोल 0.4% G) @ 7.5 किग्रा प्रति एकड़ डालें अथवा कोरोजन @ 0.4 मिली/लीटर का छिड़काव करें।"
            },
            "stages": {
                "en": "Germination (0-40 days) -> Tillering (40-120 days) -> Grand growth & elongation (120-270 days) -> Ripening & maturity (270-360 days).",
                "hi": "अंकुरण (0-40 दिन) -> कल्ले फूटना (40-120 दिन) -> तीव्र बढ़वार (120-270 दिन) -> शर्करा निर्माण व पकना (270-360 दिन)।"
            }
        },
        "corn": {
            "name_en": "Corn / Maize",
            "name_hi": "मक्का",
            "irrigation": {
                "en": "Maize requires 5-6 irrigations if rains fail. Most critical stages are knee-high stage, tasseling, silking, and grain filling. Avoid water stagnation at all costs.",
                "hi": "मक्का में 5-6 हल्की सिंचाइयों की आवश्यकता होती है। घुटने की ऊंचाई, नर मंजरी (Tasseling), भुट्टे के बाल (Silking) और दाना भरते समय नमी अनिवार्य है। खेत में जलभराव बिल्कुल न होने दें।"
            },
            "fertilizer": {
                "en": "NPK: 120 kg N, 60 kg P2O5, 40 kg K2O/ha + 25 kg Zinc Sulfate. Apply full P, K, and 1/3 N at sowing. Top dress remaining N at knee-high (30 days) and tasseling (50 days).",
                "hi": "NPK मात्रा: 120 किग्रा नाइट्रोजन, 60 किग्रा फास्फोरस, 40 किग्रा पोटाश प्रति हेक्टेयर। पूरा फास्फोरस व पोटाश बुवाई पर दें। नाइट्रोजन को 3 भागों में दें: बुवाई पर, घुटने तक ऊंचाई पर (30 दिन) और नर मंजरी निकलते समय (50 दिन)।"
            },
            "sowing": {
                "en": "Kharif sowing: June 15 to July 15. Rabi sowing: October-November. Seed rate: 20 kg/ha. Spacing: 60 cm between rows, 20 cm between plants.",
                "hi": "खरीफ बुवाई: 15 जून से 15 जुलाई। रबी बुवाई: अक्टूबर-नवंबर। बीज दर: 20 किग्रा/हेक्टेयर। कतार से कतार दूरी 60 सेमी और पौधे से पौधा 20 सेमी रखें।"
            },
            "diseases": {
                "en": "Common Rust and Maydis Leaf Blight. Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin @ 1 ml/L at first appearance of disease spots.",
                "hi": "कॉमन रस्ट (Common Rust) और पत्ती झुलसा (Maydis Blight)। पत्तियों पर धब्बे दिखने पर मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर या एजोक्सीस्ट्रोबिन @ 1 मिली/लीटर स्प्रे करें।"
            },
            "pest": {
                "en": "Fall Armyworm (FAW) is the destructive major pest. Spray Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L into the whorls.",
                "hi": "फॉल आर्मीवॉर्म (FAW) मुख्य हानिकारक कीट है जो पत्तियों और गोभ को खाता है। पौधों की गोभ में कोरोजन @ 0.4 मिली/लीटर या इमामेक्टिन बेंजोएट 5% SG @ 0.5 ग्राम/लीटर का घोल डालें।"
            },
            "stages": {
                "en": "Emergence (0-10 days) -> Knee-high (25-35 days) -> Tasseling & Silking (50-65 days) -> Milking & Dough (70-85 days) -> Maturity (90-110 days).",
                "hi": "अंकुरण (0-10 दिन) -> घुटने तक ऊंचाई (25-35 दिन) -> मंजरी व भुट्टा बाल निकलना (50-65 दिन) -> दाना भराव (70-85 दिन) -> पकने की अवस्था (90-110 दिन)।"
            }
        },
        "soybean": {
            "name_en": "Soybean",
            "name_hi": "सोयाबीन",
            "irrigation": {
                "en": "Primarily grown as a rainfed Kharif crop. If monsoon breaks occur, irrigate at flowering (35-40 days) and pod filling stages (55-65 days).",
                "hi": "सोयाबीन मुख्य रूप से वर्षा आधारित फसल है। यदि लंबे समय तक बारिश न हो तो फूल आते समय (35-40 दिन) और फलियां भरते समय (55-65 दिन) हल्की सिंचाई अवश्य करें।"
            },
            "fertilizer": {
                "en": "NPK: 20-30 kg N, 60-80 kg P2O5, 40 kg K2O, and 20 kg Sulfur per hectare. As a legume, soybean fixes atmospheric nitrogen; hence only starter nitrogen is needed. Inoculate with Rhizobium culture.",
                "hi": "NPK मात्रा: 20-30 किग्रा नाइट्रोजन, 60-80 किग्रा फास्फोरस, 40 किग्रा पोटाश और 20 किग्रा गंधक (सल्फर) प्रति हेक्टेयर। दलहनी फसल होने के कारण इसे कम नाइट्रोजन चाहिए। राइजोबियम कल्चर से बीज उपचारित करें।"
            },
            "sowing": {
                "en": "Sowing: June 20 to July 10 after receiving 75-100 mm rainfall. Seed rate: 70-75 kg/ha. Spacing: 45 cm between rows, 5-7 cm between plants at depth 3-4 cm.",
                "hi": "बुवाई का समय: 20 जून से 10 जुलाई (75-100 मिमी वर्षा के बाद)। बीज दर: 70-75 किग्रा/हेक्टेयर। कतार से कतार 45 सेमी और गहराई 3-4 सेमी रखें।"
            },
            "diseases": {
                "en": "Soybean Rust and Yellow Mosaic Virus (YMV). For rust, spray Hexaconazole 5% EC @ 1 ml/L or Tebuconazole @ 1.25 ml/L. For YMV, control whitefly vectors with Thiamethoxam.",
                "hi": "सोयाबीन रस्ट (Rust) और पीला मोज़ेक वायरस (YMV)। रस्ट के लिए हेक्साकोनाज़ोल 5% EC @ 1 मिली/लीटर अथवा टेबुकोनाज़ोल स्प्रे करें। पीला मोज़ेक सफेद मक्खी से फैलता है, रोकथाम हेतु थायमेथोक्सम छिड़कें।"
            },
            "pest": {
                "en": "Girdle beetle, semilooper, and tobacco caterpillar. Spray Chlorantraniliprole 18.5% SC @ 0.3 ml/L or Triazophos 40% EC @ 1.5 ml/L at first notice.",
                "hi": "गर्डल बीटल (चक्र भृंग), सेमीलूपर और तम्बाकू की इल्ली। रोकथाम हेतु कोरोजन @ 0.3 मिली/लीटर या ट्रायजोफॉस 40% EC @ 1.5 मिली/लीटर का छिड़काव करें।"
            },
            "stages": {
                "en": "Emergence (0-7 days) -> Vegetative (7-30 days) -> Flowering (35-50 days) -> Pod formation (50-70 days) -> Seed filling & maturity (75-100 days).",
                "hi": "अंकुरण (0-7 दिन) -> वानस्पतिक विकास (7-30 दिन) -> फूल आना (35-50 दिन) -> फली विकास (50-70 दिन) -> दाना भरना व पकना (75-100 दिन)।"
            }
        },
        "apple": {
            "name_en": "Apple",
            "name_hi": "सेब",
            "irrigation": {
                "en": "Critical irrigation periods are fruit set (April-May) and fruit expansion (June-July). Drip irrigation with mulching is recommended for temperate orchard moisture preservation.",
                "hi": "सेब में फल बनते समय (अप्रैल-मई) और फल के आकार बढ़ने के समय (जून-जुलाई) सिंचाई बहुत महत्वपूर्ण है। ड्रिप सिंचाई और थाले में सूखी घास की मल्चिंग अपनाएं।"
            },
            "fertilizer": {
                "en": "Mature bearing tree (10+ years): 700g N, 350g P2O5, 700g K2O plus 50-60 kg FYM per tree per year. Apply FYM, P, and K in winter (Dec-Jan). Apply N in 2 splits (bud break and fruit set).",
                "hi": "10 वर्ष से बड़े फलदार पेड़ हेतु प्रति वर्ष: 700 ग्राम नाइट्रोजन, 350 ग्राम फास्फोरस, 700 ग्राम पोटाश तथा 50-60 किग्रा सड़ी गोबर खाद। गोबर खाद, फास्फोरस और पोटाश दिसंबर-जनवरी में दें। नाइट्रोजन को दो बार में (कली फूटते व फल बनते समय) दें।"
            },
            "sowing": {
                "en": "Planting: December to February during dormancy. Plant grafted saplings at 4x4m or 3x3m for semi-dwarf rootstocks. Prepare 1x1x1m pits filled with rich soil and FYM.",
                "hi": "रोपाई का समय: दिसंबर से फरवरी (सुप्तावस्था में)। 1x1x1 मीटर के गड्ढे तैयार कर अच्छी मिट्टी व गोबर खाद भरें। 4x4 मीटर की दूरी पर कलमी पौधे लगाएं।"
            },
            "diseases": {
                "en": "Apple Scab (olive green to black velvety spots on leaves and fruit). Spray Dodine 65% WP @ 0.75 g/L or Difenoconazole 25% EC @ 0.3 ml/L at green tip and petal fall stages.",
                "hi": "सेब का स्कैब (Apple Scab): पत्तियों और फलों पर जैतून-हरे से काले मखमली धब्बे। रोकथाम के लिए डोडीन 65% WP @ 0.75 ग्राम/लीटर या डाईफेनोकोनाज़ोल 25% EC @ 0.3 मिली/लीटर का छिड़काव हरी कली और पंखुड़ी झड़ने पर करें।"
            },
            "pest": {
                "en": "San Jose scale, woolly apple aphid, and European red mite. Apply Horticultural Mineral Oil (HMO 2%) in late winter. Spray Spiromesifen @ 1 ml/L for mites.",
                "hi": "सैन जोस स्केल, वूली एफिड और लाल मकड़ी (Mite)। सर्दियों के अंत में 2% हॉर्टीकल्चरल मिनरल ऑयल (HMO) स्प्रे करें। मकड़ी कीट हेतु स्पाइरोमेसिफेन @ 1 मिली/लीटर छिड़कें।"
            },
            "stages": {
                "en": "Dormancy (Dec-Feb) -> Green tip & Pink bud (March-April) -> Full bloom & Petal fall (April-May) -> Fruit development (May-July) -> Harvest (July-Oct).",
                "hi": "सुप्तावस्था (दिसंबर-फरवरी) -> हरी कली व गुलाबी कली (मार्च-अप्रैल) -> फूल आना (अप्रैल-मई) -> फल विकास (मई-जुलाई) -> तुड़ाई (जुलाई-अक्टूबर)।"
            }
        },
        "grape": {
            "name_en": "Grape",
            "name_hi": "अंगूर",
            "irrigation": {
                "en": "Drip irrigation is standard. Higher water during berry development; withhold water 10-15 days before harvest to build sugar and avoid berry cracking.",
                "hi": "अंगूर में ड्रिप सिंचाई प्रणाली सर्वश्रेष्ठ है। दाना बढ़ते समय पर्याप्त पानी दें; तुड़ाई से 10-15 दिन पहले सिंचाई रोक दें ताकि मिठास बढ़े और फल फटे नहीं।"
            },
            "fertilizer": {
                "en": "Annual dose per vine: 300g N, 150g P2O5, 300g K2O. Micronutrients like Boron and Zinc are essential for uniform berry set and bunches. Apply Potash during berry enlargement.",
                "hi": "प्रति बेल प्रति वर्ष: 300 ग्राम नाइट्रोजन, 150 ग्राम फास्फोरस और 300 ग्राम पोटाश। दानों के अच्छे गुच्छे हेतु बोरॉन और जिंक आवश्यक हैं। दाने बड़े होते समय पोटाश की मात्रा बढ़ाएं।"
            },
            "sowing": {
                "en": "Rooted cuttings planted in January-February on Bower / Y-trellis system with 3x1.8m spacing.",
                "hi": "जनवरी-फरवरी में जड़ वाली कटिंग्स की रोपाई करें। बावर (पंडाल) या Y-ट्रेलिस विधि में 3x1.8 मीटर की दूरी रखें।"
            },
            "diseases": {
                "en": "Black Rot and Downy Mildew. For Black rot, spray Mancozeb @ 2.5 g/L or Azoxystrobin @ 1 ml/L. For Downy mildew, spray Metalaxyl + Mancozeb (Ridomil MZ @ 2.5 g/L).",
                "hi": "ब्लैक रॉट (Black Rot) और डाउनी फफूंदी। ब्लैक रॉट के लिए मैंकोज़ेब @ 2.5 ग्राम/लीटर या एजोक्सीस्ट्रोबिन @ 1 मिली/लीटर स्प्रे करें। डाउनी मिल्ड्यू के लिए रिडोमिल एमजेड (मेटालैक्सिल + मैंकोज़ेब @ 2.5 ग्राम/लीटर) छिड़कें।"
            },
            "pest": {
                "en": "Thrips, mealybug, and flea beetle. Spray Imidacloprid 17.8% SL @ 0.5 ml/L for thrips and mealybugs. Release predatory ladybird beetle (Cryptolaemus) for organic biocontrol.",
                "hi": "थ्रिप्स और मिलीबग (Mealybug)। थ्रिप्स व मिलीबग के लिए इमिडाक्लोप्रिड @ 0.5 मिली/लीटर स्प्रे करें। जैविक नियंत्रण हेतु क्रिप्टोलिमस परभक्षी लेडीबर्ड कीट छोड़ें।"
            },
            "stages": {
                "en": "Pruning (Oct/April) -> Bud burst (2-3 weeks) -> Shoot growth & flowering (4-6 weeks) -> Fruit set & berry growth (6-12 weeks) -> Veraison & ripening (12-16 weeks) -> Harvest.",
                "hi": "कटाई-छंटाई (अक्टूबर/अप्रैल) -> कली फूटना (2-3 सप्ताह) -> फूल आना (4-6 सप्ताह) -> दाना विकास (6-12 सप्ताह) -> रंग बदलना व पकना (12-16 सप्ताह) -> तुड़ाई।"
            }
        }
    },
    "topics": {
        "irrigation": {
            "en": "General Irrigation Best Practices:\n- Irrigate based on critical crop growth stages (e.g., CRI in wheat, flowering in vegetables).\n- Drip irrigation saves 40-50% water and prevents fungal leaf blights.\n- Avoid irrigating during strong winds to prevent crop lodging.\n- Stop irrigation 10-14 days before harvest to facilitate harvesting and post-harvest quality.",
            "hi": "सामान्य सिंचाई प्रबंधन नियम:\n- फसल की क्रांतिक अवस्थाओं (जैसे गेहूं में CRI, सब्जियों में फूल आने) पर सिंचाई अवश्य करें।\n- ड्रिप सिंचाई से 40-50% पानी की बचत होती है और पत्तियों पर फफूंद नहीं लगती।\n- तेज हवा के समय सिंचाई न करें ताकि फसल गिरे नहीं।\n- कटाई से 10-14 दिन पूर्व सिंचाई बंद कर दें ताकि खेत सूख सके और उपज की गुणवत्ता बनी रहे।"
        },
        "fertilizer": {
            "en": "Balanced Fertilizer (NPK) Principles:\n- Nitrogen (N) promotes leafy vegetative growth; always split to prevent leaching.\n- Phosphorus (P) fosters vigorous root development; apply full dose as basal at sowing.\n- Potassium (K) enhances disease resistance, drought tolerance, and grain/tuber quality.\n- Incorporate 5-10 tonnes of well-rotted FYM or 2.5 tonnes vermicompost per hectare for soil health.",
            "hi": "संतुलित उर्वरक (NPK) सिद्धांत:\n- नाइट्रोजन (यूरिया) पौधों की हरियाली और बढ़वार के लिए है; इसे हमेशा 2-3 बार में बांटकर दें।\n- फास्फोरस (DAP/SSP) मजबूत जड़ों के विकास के लिए है; इसे हमेशा बुवाई के समय नीचे दें।\n- पोटाश (MOP) फसल को बीमारियों और सूखे से लड़ने की शक्ति देता है तथा दाने व कंद की चमक बढ़ाता है।\n- खेत की उर्वरता हेतु 5-10 टन सड़ी गोबर खाद या 2.5 टन केंचुआ खाद बुवाई से पहले खेत में मिलाएं।"
        },
        "soil": {
            "en": "Soil Health Advice:\n- Test soil every 2-3 years at your local Krishi Vigyan Kendra (KVK).\n- Optimal pH for most crops is 6.5 to 7.5. Apply agricultural gypsum for alkaline/sodic soils and lime for acidic soils.\n- Green manuring with Dhaincha or Sunn hemp restores soil organic carbon effectively.",
            "hi": "मृदा स्वास्थ्य सलाह:\n- प्रत्येक 2-3 वर्ष में अपने नजदीकी कृषि विज्ञान केंद्र (KVK) से मिट्टी की जांच कराएं।\n- अधिकांश फसलों के लिए मिट्टी का पीएच 6.5 से 7.5 सर्वोत्तम है। क्षारीय मिट्टी में जिप्सम और अम्लीय मिट्टी में चूना डालें।\n- ढैंचा या सनई की हरी खाद पलटने से मिट्टी में जीवांश कार्बन तेजी से बढ़ता है।"
        },
        "weather": {
            "en": "Weather-Adaptive Agriculture Advisory:\n- Overcast & humid skies: Heightens risk of rust and blights. Apply preventive Mancozeb spray.\n- Rain forecasted: Postpone irrigation, urea top-dressing, and pesticide spraying immediately.\n- Heat wave/frost warning: Give light evening irrigation to moderate soil temperature.",
            "hi": "मौसम अनुकूल कृषि सलाह:\n- बादल और अधिक नमी: रतुआ और झुलसा जैसी फफूंद बीमारियों का खतरा बढ़ जाता है। बचाव हेतु मैंकोज़ेब का हल्का छिड़काव रखें।\n- बारिश का अनुमान: सिंचाई, यूरिया का भुरकाव और कीटनाशक स्प्रे तुरंत टाल दें।\n- पाला या लू की संभावना: हल्की शाम की सिंचाई करने से मिट्टी का तापमान नियंत्रित रहता है और फसल बचती है।"
        },
        "mandi": {
            "en": "Mandi & MSP (Minimum Support Price) Advisory:\n- Check daily modal prices in your nearby APMC mandis on the app's Mandi tab.\n- Ensure grain moisture is below 12% for cereals before taking produce to mandi to avoid deductions.\n- Register on e-NAM (National Agriculture Market) for transparent multi-buyer electronic bidding.",
            "hi": "मंडी एवं एमएसपी (न्यूनतम समर्थन मूल्य) जानकारी:\n- अपनी नजदीकी कृषि उपज मंडी के दैनिक मॉडल भाव जानने के लिए ऐप के 'Mandi' टैब का उपयोग करें।\n- अनाज को मंडी ले जाने से पहले उसमें नमी 12% से कम रखें ताकि भाव में कटौती न हो।\n- राष्ट्रीय कृषि बाजार (e-NAM) पोर्टल पर पंजीकरण कराएं जिससे आपको पारदर्शी और सही मूल्य मिल सके।"
        },
        "general": {
            "en": "Namaste Kisan Bhai! 🙏 I am your Local Kisan Farming Assistant. I run 100% on-device without internet or cloud APIs. You can ask me about crop diseases, NPK fertilizer dosing, irrigation scheduling, sowing, or pest remedies for Wheat, Rice, Potato, Tomato, Cotton, Sugarcane, Corn, Soybean, Apple, and Grape.",
            "hi": "नमस्ते किसान भाई! 🙏 मैं आपका स्थानीय किसान कृषि सहायक हूँ। मैं 100% बिना इंटरनेट के आपके मोबाइल पर काम करता हूँ। आप मुझसे गेहूं, धान, आलू, टमाटर, कपास, गन्ना, मक्का, सोयाबीन, सेब और अंगूर की फसल में खाद (NPK), सिंचाई, बुवाई, रोग पहचान और कीट रोकथाम के बारे में पूछ सकते हैं।"
        },
        "medical_disclaimer": {
            "en": "I am an agriculture assistant focused on farming-related questions. Please consult a qualified medical professional for health concerns.",
            "hi": "मैं कृषि और खेती से जुड़े सवालों में सहायता करता हूँ। स्वास्थ्य संबंधी समस्या के लिए योग्य चिकित्सक से सलाह लें।"
        }
    }
}

os.makedirs('www', exist_ok=True)
with open('www/kisan_knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(knowledge, f, ensure_ascii=False, indent=2)

with open('kisan_knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(knowledge, f, ensure_ascii=False, indent=2)

os.makedirs('android/app/src/main/assets/public', exist_ok=True)
with open('android/app/src/main/assets/public/kisan_knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(knowledge, f, ensure_ascii=False, indent=2)

print("Generated kisan_knowledge.json in www/, root, and android assets!")
