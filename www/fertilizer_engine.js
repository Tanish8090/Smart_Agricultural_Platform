/**
 * Smart Agriculture Platform (SAP) — Local Crop & Fertilizer Advisor Engine
 * 100% On-Device Agronomic Intelligence (Zero API, Offline-Ready)
 */

const LOCAL_FERTILIZER_DATABASE = {
  "wheat": {
    "crop_en": "Wheat", "crop_hi": "गेहूं",
    "general_npk_ratio": "120:60:40 kg/ha",
    "general_guidance_en": "Standard general recommendation for irrigated timely-sown wheat is 120 kg Nitrogen (N), 60 kg Phosphorus (P2O5), and 40 kg Potassium (K2O) per hectare. Apply full P and K along with 1/3 N at sowing (basal), and remaining N in two equal splits at CRI and tillering.",
    "general_guidance_hi": "सिंचित समय पर बोई गई गेहूं के लिए सामान्य अनुशंसित NPK अनुपात 120:60:40 किग्रा/हेक्टेयर है। पूरा फास्फोरस और पोटाश तथा एक-तिहाई नाइट्रोजन बुवाई के समय (बेसल) डालें। शेष नाइट्रोजन दो बार में (CRI शिखर जड़ें और कल्ले फूटते समय) दें।",
    "stages": {
      "Sowing / Basal": {
        "en": "Apply full Phosphorus (DAP/SSP), full Potash (MOP), and 1/3rd Nitrogen (Urea) at drilling/sowing.",
        "hi": "बुवाई के समय पूरा फास्फोरस (DAP/SSP), पूरा पोटाश (MOP) और 1/3 नाइट्रोजन (यूरिया) खेत की तैयारी या बुवाई के समय दें।"
      },
      "Vegetative": {
        "en": "First top-dressing of Nitrogen (40 kg N/ha, ~50 kg Urea/ha) at 21-25 days after sowing during first irrigation (CRI stage). Second top-dressing at 40-45 days during tillering.",
        "hi": "बुवाई के 21-25 दिन बाद पहली सिंचाई (CRI अवस्था) पर पहली टॉप-ड्रेसिंग (लगभग 50 किग्रा यूरिया) दें। दूसरी टॉप-ड्रेसिंग 40-45 दिन बाद कल्ले फूटते समय दें।"
      },
      "Flowering": {
        "en": "Maintain soil moisture. Avoid soil broadcast of urea. Foliar spray of 1% Potassium Nitrate (13-0-45) improves grain filling and heat tolerance.",
        "hi": "खेत में नमी बनाए रखें। यूरिया न बुरकें। दाना भराव और गर्मी से बचाव के लिए 1% पोटेशियम नाइट्रेट (13-0-45) का छिड़काव करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Maintain light irrigation during milk/dough stages. Foliar zinc (0.5% ZnSO4) can be applied if leaves show chlorosis.",
        "hi": "दूधिया अवस्था में हल्की सिंचाई बनाए रखें। पत्तियों में पीलापन दिखे तो 0.5% जिंक सल्फेट का पर्णीय छिड़काव करें।"
      },
      "Harvest": {
        "en": "Stop all fertilizer applications. Withhold irrigation 10-15 days before harvest to allow uniform ripening.",
        "hi": "उर्वरक प्रयोग पूरी तरह बंद करें। कटाई से 10-15 दिन पूर्व सिंचाई रोक दें ताकि फसल समान रूप से पक सके।"
      }
    },
    "irrigation_relation_en": "Always apply top-dressed urea in moist soil or immediately before a light irrigation. Avoid broadcasting fertilizer in dry soil or right before heavy rainfall.",
    "irrigation_relation_hi": "यूरिया की टॉप-ड्रेसिंग हमेशा पर्याप्त नमी वाली मिट्टी में या हल्की सिंचाई से तुरंत पहले करें। सूखे खेत में या भारी बारिश की संभावना होने पर खाद न डालें।",
    "deficiencies": {
      "nitrogen": {
        "symptom_en": "Uniform yellowing of older lower leaves starting from tips.",
        "symptom_hi": "पुरानी निचली पत्तियों का सिरे से पीछे की ओर पीला पड़ना।",
        "action_en": "Top-dress 25-30 kg Urea per acre or spray 2% Urea solution in clear weather.",
        "action_hi": "प्रति एकड़ 25-30 किग्रा यूरिया की टॉप-ड्रेसिंग करें या 2% यूरिया घोल का छिड़काव करें।"
      },
      "zinc": {
        "symptom_en": "White/yellow chlorotic streaks in leaves, stunted tillers.",
        "symptom_hi": "पत्तियों में सफेद या पीली धारियां और कल्ले कम फूटना।",
        "action_en": "Foliar spray of 0.5% Zinc Sulfate + 0.25% slaked lime.",
        "action_hi": "0.5% जिंक सल्फेट + 0.25% बुझा हुआ चूना मिलाकर छिड़काव करें।"
      },
      "potassium": {
        "symptom_en": "Marginal scorching and brown necrosis of leaf margins.",
        "symptom_hi": "पत्तियों के किनारों का झुलसना और भूरा होना।",
        "action_en": "Apply 15-20 kg MOP per acre or foliar spray 1% SOP (0-0-50).",
        "action_hi": "15-20 किग्रा MOP प्रति एकड़ डालें या 1% पोटेशियम सल्फेट (0-0-50) का छिड़काव करें।"
      }
    }
  },
  "rice": {
    "crop_en": "Rice / Paddy", "crop_hi": "धान / चावल",
    "general_npk_ratio": "120:50:50 kg/ha",
    "general_guidance_en": "Standard general recommendation for high-yielding rice is 120 kg N, 50 kg P2O5, and 50 kg K2O/ha. Apply full P and half K as basal at puddling. Split N into 3 doses: basal, active tillering (21 DAT), and panicle initiation (40-45 DAT).",
    "general_guidance_hi": "उन्नत धान के लिए सामान्य अनुशंसित NPK अनुपात 120:50:50 किग्रा/हेक्टेयर है। लेह करते समय पूरा फास्फोरस व आधा पोटाश दें। नाइट्रोजन को 3 बराबर भागों में बांटकर दें (रोपाई, कल्ले फूटते समय, और बाली बनते समय)।",
    "stages": {
      "Sowing / Basal": {
        "en": "Incorporate full DAP/SSP and half MOP into puddle soil before transplanting.",
        "hi": "रोपाई से पहले लेह में पूरा DAP/SSP और आधा MOP अच्छी तरह मिला दें।"
      },
      "Vegetative": {
        "en": "Apply 1/3rd Nitrogen (Urea) at active tillering (20-25 days after transplanting). Apply 25 kg/ha Zinc Sulfate.",
        "hi": "रोपाई के 20-25 दिन बाद कल्ले फूटते समय 1/3 नाइट्रोजन (यूरिया) दें। 25 किग्रा जिंक सल्फेट प्रति हेक्टेयर डालें।"
      },
      "Flowering": {
        "en": "Apply final 1/3rd Nitrogen at Panicle Initiation (PI) stage. Maintain 3-5 cm standing water.",
        "hi": "बाली निकलने की शुरुआत (PI अवस्था) पर अंतिम 1/3 नाइट्रोजन दें। खेत में 3-5 सेमी पानी बनाए रखें।"
      },
      "Fruit/Grain Formation": {
        "en": "Avoid urea broadcast. Maintain shallow water during grain filling. Spray 13-0-45 if needed for grain weight.",
        "hi": "यूरिया न डालें। दाना भरते समय खेत में नमी बनाए रखें। दाने के वजन के लिए 13-0-45 का छिड़काव उपयोगी है।"
      },
      "Harvest": {
        "en": "Drain standing water 10 days prior to harvest.",
        "hi": "कटाई से 10 दिन पहले खेत से अतिरिक्त पानी निकाल दें।"
      }
    },
    "irrigation_relation_en": "Apply nitrogen when water level is reduced, then irrigate after 24-48 hours to prevent ammonia loss.",
    "irrigation_relation_hi": "खेत में पानी का स्तर कम होने पर यूरिया डालें, फिर 24-48 घंटे बाद पानी दें ताकि खाद सुरक्षित रहे।",
    "deficiencies": {
      "zinc": {
        "symptom_en": "Khaira disease: rust-brown spots on lower leaves 2-3 weeks after transplanting.",
        "symptom_hi": "खैरा रोग: रोपाई के 2-3 सप्ताह बाद निचली पत्तियों पर कत्थई/भूरे धब्बे बनना।",
        "action_en": "Foliar spray of 5 kg Zinc Sulfate + 2.5 kg Slaked Lime per hectare in 500L water.",
        "action_hi": "5 किग्रा जिंक सल्फेट + 2.5 किग्रा चूना 500 लीटर पानी में घोलकर प्रति हेक्टेयर छिड़कें।"
      }
    }
  },
  "potato": {
    "crop_en": "Potato", "crop_hi": "आलू",
    "general_npk_ratio": "150:80:100 kg/ha",
    "general_guidance_en": "General recommendation for potato is 150 kg N, 80 kg P2O5, and 100 kg K2O/ha. Potassium is critical for tuber enlargement and starch synthesis. Apply 50% N, full P, and full K at planting. Top-dress remaining 50% N at first earthing up (30-35 days).",
    "general_guidance_hi": "आलू की फसल के लिए सामान्य NPK अनुशंसा 150:80:100 किग्रा/हेक्टेयर है। कंद के विकास और गुणवत्ता के लिए पोटाश बेहद जरूरी है। बुवाई पर 50% N, पूरा P व पूरा K दें। शेष 50% N पहली मिट्टी चढ़ाते समय दें।",
    "stages": {
      "Sowing / Basal": {
        "en": "Apply full DAP/SSP, full Potash, and half Urea in planting furrows below tuber level.",
        "hi": "बुवाई की नालियों में कंद के नीचे पूरा DAP/SSP, पूरा पोटाश और आधी यूरिया मिट्टी में मिलाएं।"
      },
      "Vegetative": {
        "en": "Top-dress remaining nitrogen along with earthing-up operation at 30-35 days after planting.",
        "hi": "बुवाई के 30-35 दिन बाद मिट्टी चढ़ाते समय बची हुई नाइट्रोजन की टॉप-ड्रेसिंग करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Tuber bulking: Spray 0:0:50 (Potassium Sulfate) @ 1.5% to boost tuber weight and dry matter.",
        "hi": "कंद फुलाव अवस्था: कंद का आकार और वजन बढ़ाने के लिए 0:0:50 का 1.5% छिड़काव करें।"
      }
    },
    "irrigation_relation_en": "Maintain consistent furrow soil moisture without waterlogging. Moisture stress during tuber initiation causes split tubers.",
    "irrigation_relation_hi": "नालियों में समान नमी बनाए रखें। कंद बनते समय पानी की कमी से आलू फटने लगते हैं।",
    "deficiencies": {
      "potassium": {
        "symptom_en": "Dark bronze spotting, marginal leaf curling, and small tuber size.",
        "symptom_hi": "पत्तियों पर कांस्य जैसे धब्बे, किनारे मुड़ना और आलू का आकार छोटा रहना।",
        "action_en": "Spray Potassium Sulfate (0:0:50) @ 10g per liter water.",
        "action_hi": "पोटेशियम सल्फेट (0:0:50) का 10 ग्राम प्रति लीटर पानी में घोलकर छिड़काव करें।"
      }
    }
  },
  "tomato": {
    "crop_en": "Tomato", "crop_hi": "टमाटर",
    "general_npk_ratio": "120:80:100 kg/ha",
    "general_guidance_en": "General recommendation is 120 kg N, 80 kg P2O5, and 100 kg K2O/ha. Calcium and Boron are vital to prevent blossom end rot and fruit cracking. Apply full P, 1/3 N, and 1/3 K at transplanting.",
    "general_guidance_hi": "टमाटर के लिए सामान्य NPK अनुशंसा 120:80:100 किग्रा/हेक्टेयर है। फल फटने और सड़ांध रोकने के लिए कैल्शियम और बोरॉन आवश्यक हैं। रोपाई पर पूरा P, 1/3 N और 1/3 K दें।",
    "stages": {
      "Sowing / Basal": {
        "en": "Incorporate FYM (20-25 t/ha) + basal NPK (30:80:30 kg/ha) in beds before transplanting.",
        "hi": "रोपाई से पहले क्यारियों में 20-25 टन सड़ी गोबर खाद और बेसल NPK (30:80:30) मिलाएं।"
      },
      "Vegetative": {
        "en": "Apply nitrogen and potash split (30 kg N + 25 kg K2O/ha) at 30 days after transplanting.",
        "hi": "रोपाई के 30 दिन बाद 30 किग्रा N और 25 किग्रा K2O की टॉप-ड्रेसिंग करें।"
      },
      "Flowering": {
        "en": "Foliar spray of Solubor (Boron 0.1%) and Calcium Nitrate (0.5%) to enhance fruit set.",
        "hi": "फूल झड़ने से रोकने और फल बनने के लिए बोरॉन (0.1%) और कैल्शियम नाइट्रेट (0.5%) का छिड़काव करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Apply 0:0:50 or 13:0:45 foliar spray at fruit enlargement for firm, shiny, red fruits.",
        "hi": "फलों के विकास पर 0:0:50 या 13:0:45 का छिड़काव करें जिससे फल ठोस, चमकदार और लाल बनें।"
      }
    },
    "irrigation_relation_en": "Adopt drip irrigation where possible. Irregular watering causes severe blossom end rot and fruit skin cracking.",
    "irrigation_relation_hi": "ड्रिप सिंचाई अपनाएं। अनियमित पानी देने से फलों के निचले हिस्से में सड़न और छिलका फटने की समस्या आती है।",
    "deficiencies": {
      "calcium": {
        "symptom_en": "Blossom End Rot (BER): black sunken leathery patch at bottom of fruit.",
        "symptom_hi": "ब्लॉसम एंड रॉट: फल के निचले हिस्से का काला और चपटा होकर सड़ना।",
        "action_en": "Foliar spray of Calcium Nitrate @ 5g/L water every 10 days during fruit set.",
        "action_hi": "फल बनने के समय 5 ग्राम प्रति लीटर कैल्शियम नाइट्रेट का 10 दिन के अंतराल पर छिड़काव करें।"
      }
    }
  },
  "cotton": {
    "crop_en": "Cotton", "crop_hi": "कपास",
    "general_npk_ratio": "120:60:60 kg/ha",
    "general_guidance_en": "Standard general recommendation for Bt Cotton is 120:60:60 kg NPK/ha. Split nitrogen in 3 doses: basal, square formation, and peak boll development. Avoid excess N which leads to excessive leafy vegetative growth.",
    "general_guidance_hi": "बीटी कपास के लिए सामान्य अनुशंसा 120:60:60 किग्रा NPK/हेक्टेयर है। नाइट्रोजन को 3 बार में दें (बुवाई, डोडी बनते समय, और गूलर विकास पर)। अधिक यूरिया से पौधे अनावश्यक लंबे होते हैं।",
    "stages": {
      "Sowing / Basal": {
        "en": "Apply full P, 1/3 N, and 1/3 K along with FYM during field preparation.",
        "hi": "खेत की तैयारी के समय पूरा P, 1/3 N और 1/3 K गोबर की खाद के साथ दें।"
      },
      "Vegetative": {
        "en": "Top-dress 1/3rd Nitrogen at squaring stage (40-45 DAS). Foliar spray Magnesium Sulfate (1%).",
        "hi": "डोडी बनने की अवस्था (40-45 दिन) पर 1/3 नाइट्रोजन दें। मैग्नीशियम सल्फेट (1%) का छिड़काव करें।"
      },
      "Flowering": {
        "en": "Spray 13:0:45 (2%) and Boron (0.1%) during peak flowering to prevent square and boll dropping.",
        "hi": "फूल आते समय डोडी और गूलर झड़ने से रोकने के लिए 13:0:45 (2%) और बोरॉन (0.1%) का छिड़काव करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Apply remaining Nitrogen and Potash during boll development for heavy fiber weight.",
        "hi": "गूलर के विकास पर बची हुई नाइट्रोजन और पोटाश दें ताकि रेशे का वजन और चमक बढ़े।"
      }
    },
    "irrigation_relation_en": "Avoid water stagnation in black soil. Maintain critical irrigation during squaring and boll development.",
    "irrigation_relation_hi": "काली मिट्टी में जलभराव न होने दें। डोडी और गूलर बनते समय उचित सिंचाई अवश्य करें।",
    "deficiencies": {
      "magnesium": {
        "symptom_en": "Reddening of cotton leaves between veins, purplish tint on older leaves.",
        "symptom_hi": "कपास की पत्तियों का नसों के बीच लाल या बैंगनी रंग का हो जाना।",
        "action_en": "Foliar spray of Magnesium Sulfate @ 10g per liter water.",
        "action_hi": "मैग्नीशियम सल्फेट 10 ग्राम प्रति लीटर पानी में घोलकर छिड़काव करें।"
      }
    }
  },
  "sugarcane": {
    "crop_en": "Sugarcane", "crop_hi": "गन्ना",
    "general_npk_ratio": "250:80:80 kg/ha",
    "general_guidance_en": "Sugarcane requires high nutrition: 250 kg N, 80 kg P2O5, and 80 kg K2O/ha. Complete nitrogen application within 90-120 days of planting; late nitrogen reduces sucrose recovery.",
    "general_guidance_hi": "गन्ने को अधिक पोषण की आवश्यकता होती है: 250 किग्रा N, 80 किग्रा P2O5 और 80 किग्रा K2O/हेक्टेयर। बुवाई के 90-120 दिनों के भीतर पूरा नाइट्रोजन दे दें; देर से खाद देने पर चीनी की मात्रा घटती है।",
    "stages": {
      "Sowing / Basal": {
        "en": "Apply full P, 1/3rd K, and 1/4th N in planting furrows under setts.",
        "hi": "बुवाई की नाली में टुकड़ों के नीचे पूरा P, 1/3 K और 1/4 N डालें।"
      },
      "Vegetative": {
        "en": "Tillering & formative stage (45 & 90 DAS): Apply remaining N in two splits with earthing up.",
        "hi": "कल्ले निकलते और बढ़वार के समय (45 व 90 दिन): बची हुई नाइट्रोजन दो बार में मिट्टी चढ़ाते हुए दें।"
      },
      "Fruit/Grain Formation": {
        "en": "Grand growth stage: Apply remaining Potash (MOP) to boost cane girth and sugar content.",
        "hi": "मुख्य बढ़वार अवस्था: गन्ने की मोटाई और मिठास बढ़ाने के लिए शेष पोटाश (MOP) दें।"
      }
    },
    "irrigation_relation_en": "Irrigate immediately after fertilizer application. Water stress in formative phase severely reduces cane yield.",
    "irrigation_relation_hi": "खाद देने के तुरंत बाद सिंचाई करें। शुरुआती बढ़वार में पानी की कमी से गन्ने की पैदावार बहुत घट जाती है।",
    "deficiencies": {
      "iron": {
        "symptom_en": "Interveinal chlorosis in young top leaves, turning bleached white.",
        "symptom_hi": "गन्ने की ऊपरी नई पत्तियों का नसों के बीच पीला होकर पूरी तरह सफेद पड़ना।",
        "action_en": "Spray 1% Ferrous Sulfate + 0.1% Citric Acid.",
        "action_hi": "1% फेरस सल्फेट + 0.1% साइट्रिक एसिड मिलाकर छिड़कें।"
      }
    }
  },
  "corn": {
    "crop_en": "Corn / Maize", "crop_hi": "मक्का",
    "general_npk_ratio": "120:60:40 kg/ha",
    "general_guidance_en": "Standard general recommendation for hybrid maize is 120 kg N, 60 kg P2O5, and 40 kg K2O/ha. Split N: 1/3 basal, 1/3 knee-high (30 DAS), and 1/3 tasseling/silking (55 DAS).",
    "general_guidance_hi": "संकर मक्का के लिए सामान्य अनुशंसा 120:60:40 किग्रा NPK/हेक्टेयर है। नाइट्रोजन को 3 बार में दें: 1/3 बुवाई पर, 1/3 घुटने तक ऊंचाई पर (30 दिन), और 1/3 भुट्टा/मंजरी आते समय (55 दिन)।",
    "stages": {
      "Sowing / Basal": {
        "en": "Apply full P, full K, and 1/3 N 5 cm below seed level.",
        "hi": "बुवाई के समय बीज से 5 सेमी नीचे पूरा P, पूरा K और 1/3 N डालें।"
      },
      "Vegetative": {
        "en": "Knee-high stage (30 DAS): Top-dress 1/3rd Urea in bands 10 cm away from crop rows.",
        "hi": "घुटने तक ऊंचाई (30 दिन): 1/3 यूरिया कतारों से 10 सेमी दूर मिट्टी में दें।"
      },
      "Flowering": {
        "en": "Tasseling/Silking stage: Apply final 1/3rd Nitrogen. Critical moisture phase.",
        "hi": "मंजरी और रेशे निकलते समय अंतिम 1/3 नाइट्रोजन दें। इस समय नमी अनिवार्य है।"
      }
    },
    "irrigation_relation_en": "Maize is highly sensitive to waterlogging and drought during tasseling and silking.",
    "irrigation_relation_hi": "मक्का में फूल और भुट्टा आते समय न तो खेत में पानी ठहरना चाहिए और न ही सूखा पड़ना चाहिए।",
    "deficiencies": {
      "phosphorus": {
        "symptom_en": "Purplish red coloration along edges of lower leaves and slow root growth.",
        "symptom_hi": "निचली पत्तियों के किनारों का बैंगनी-लाल होना और जड़ें कमजोर रहना।",
        "action_en": "Ensure proper basal DAP application; spray 1% 12:61:00 (MAP).",
        "action_hi": "शुरुआत में DAP दें; आपात स्थिति में 1% 12:61:00 (MAP) का छिड़काव करें।"
      }
    }
  },
  "soybean": {
    "crop_en": "Soybean", "crop_hi": "सोयाबीन",
    "general_npk_ratio": "30:60:40:20 (NPK+S) kg/ha",
    "general_guidance_en": "As a legume, soybean fixes atmospheric nitrogen. Only a starter nitrogen dose of 20-30 kg N/ha is needed. Sulfur (20 kg/ha) and Phosphorus (60 kg P2O5/ha) are vital for root nodules and high oil content.",
    "general_guidance_hi": "दलहनी फसल होने के कारण सोयाबीन वायुमंडलीय नाइट्रोजन स्वयं स्थिर करती है। केवल 20-30 किग्रा N शुरुआती खुराक चाहिए। ग्रंथियों और तेल की मात्रा के लिए सल्फर (20 किग्रा) और फास्फोरस (60 किग्रा) सबसे जरूरी हैं।",
    "stages": {
      "Sowing / Basal": {
        "en": "Seed inoculation with Rhizobium & PSB. Apply 20 kg N, 60 kg P2O5, 40 kg K2O, and 20 kg Sulfur at sowing.",
        "hi": "राइजोबियम और PSB से बीज शोधन करें। बुवाई पर 20 kg N, 60 kg P, 40 kg K और 20 kg सल्फर बेसल दें।"
      },
      "Flowering": {
        "en": "Flower initiation (35-40 DAS): Foliar spray of 2% DAP or 19:19:19 to prevent flower drop.",
        "hi": "फूल आने पर (35-40 दिन): 2% DAP या 19:19:19 का छिड़काव करें जिससे फूल न झड़ें।"
      },
      "Fruit/Grain Formation": {
        "en": "Pod filling stage (55-60 DAS): Spray 0:0:50 @ 1.5% for bold, high-oil seeds.",
        "hi": "फली भरते समय (55-60 दिन): दानों को पुष्ट और चमकदार बनाने के लिए 0:0:50 का 1.5% छिड़काव करें।"
      }
    },
    "irrigation_relation_en": "Soybean requires well-drained soil. Water stagnation causes nodule death and root rot.",
    "irrigation_relation_hi": "सोयाबीन के खेत में जल-निकासी अच्छी होनी चाहिए। पानी भरने से गांठों के जीवाणु मर जाते हैं।",
    "deficiencies": {
      "sulfur": {
        "symptom_en": "Uniform yellowing of younger upper leaves, reduced nodules.",
        "symptom_hi": "ऊपरी नई पत्तियों का पीला पड़ना और दानों में तेल की कमी।",
        "action_en": "Apply 20-25 kg elemental sulfur or gypsum @ 200 kg/ha at sowing.",
        "action_hi": "बुवाई पर 20-25 किग्रा सल्फर या 200 किग्रा जिप्सम प्रति हेक्टेयर डालें।"
      }
    }
  },
  "apple": {
    "crop_en": "Apple", "crop_hi": "सेब",
    "general_npk_ratio": "500:250:500 g/bearing tree",
    "general_guidance_en": "For mature bearing apple trees (10+ years), apply 500g N, 250g P2O5, and 500-700g K2O per tree in circular basin. Apply organic manure (40-50 kg FYM) in December-January during dormancy.",
    "general_guidance_hi": "10 वर्ष से बड़े फलदार सेब के पेड़ के लिए 500g N, 250g P2O5 और 500-700g K2O प्रति पेड़ तौलिए में दें। दिसंबर-जनवरी में 40-50 किग्रा गोबर खाद डालें।",
    "stages": {
      "Vegetative": {
        "en": "Silver tip / green tip stage (Feb-March): Apply 1/2 Nitrogen and full P & K in basin.",
        "hi": "सिल्वर टिप अवस्था (फरवरी-मार्च): आधी नाइट्रोजन और पूरा P व K पेड़ के तौलिए में दें।"
      },
      "Flowering": {
        "en": "Pink bud stage: Spray Boron (0.1%) to enhance pollination and fruit set.",
        "hi": "पिंक बड अवस्था: परागण और फल ठहराव के लिए बोरॉन (0.1%) का छिड़काव करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Fruit development (May-June): Foliar spray of Calcium Chloride (0.5%) to prevent bitter pit.",
        "hi": "फल विकास (मई-जून): बिटर पिट से बचाव के लिए कैल्शियम क्लोराइड (0.5%) का छिड़काव करें।"
      }
    },
    "irrigation_relation_en": "Regular basin watering or drip is critical during May-June fruit development to prevent drop.",
    "irrigation_relation_hi": "मई-जून में फल विकास के दौरान पानी की कमी न होने दें, नहीं तो फल झड़ सकते हैं।",
    "deficiencies": {
      "calcium": {
        "symptom_en": "Bitter pit: brown sunken corky spots on fruit flesh and skin.",
        "symptom_hi": "बिटर पिट: सेब के फल की त्वचा और गूदे पर छोटे भूरे धब्बे और कड़वापन।",
        "action_en": "Spray Calcium Nitrate @ 4-5g per liter water 4 to 5 times from petal fall to harvest.",
        "action_hi": "पत्ती झड़ने से लेकर कटाई तक 4-5 ग्राम प्रति लीटर कैल्शियम नाइट्रेट का छिड़काव करें।"
      }
    }
  },
  "grape": {
    "crop_en": "Grape", "crop_hi": "अंगूर",
    "general_npk_ratio": "300:200:400 kg/ha",
    "general_guidance_en": "Grapes are heavy potassium feeders. Apply 1/3rd N and full P after back pruning (April). After forward pruning (October), apply remaining N and 80% of Potash in split fertigation through drip.",
    "general_guidance_hi": "अंगूर को पोटाश की बहुत अधिक आवश्यकता होती है। अप्रैल छंटाई के बाद 1/3 N और पूरा P दें। अक्टूबर फल छंटाई के बाद शेष N और 80% पोटाश ड्रिप फर्टिगेशन से किस्तों में दें।",
    "stages": {
      "Vegetative": {
        "en": "Post April pruning: Apply FYM (25 t/ha) + Single Super Phosphate (SSP) + 1/3rd Urea.",
        "hi": "अप्रैल छंटाई के बाद: 25 टन सड़ी गोबर खाद + SSP + 1/3 यूरिया दें।"
      },
      "Flowering": {
        "en": "Pre-bloom stage: Spray Boric acid (0.1%) and Zinc Sulfate (0.1%) for uniform bunch formation.",
        "hi": "फूल आने से पहले: बोरिक एसिड (0.1%) और जिंक सल्फेट का छिड़काव करें।"
      },
      "Fruit/Grain Formation": {
        "en": "Berry development to veraison: Feed Potassium Nitrate (13-0-45) and SOP (0-0-50).",
        "hi": "दाने के विकास से रंग बदलने तक: 13-0-45 और 0-0-50 ड्रिप द्वारा दें ताकि मिठास बढ़े।"
      }
    },
    "irrigation_relation_en": "Reduce irrigation slightly at veraison to concentrate sugars and enhance berry crispness.",
    "irrigation_relation_hi": "अंगूर में रंग बदलने के बाद पानी थोड़ा कम करें ताकि दानों में मिठास और चमक बढ़े।",
    "deficiencies": {
      "potassium": {
        "symptom_en": "Marginal leaf chlorosis and burn; uneven ripening and sour berries.",
        "symptom_hi": "पत्तियों के किनारों का जलना, गुच्छों का असमान पकना और दानों में खट्टापन रहना।",
        "action_en": "Fertigate Potassium Sulfate (0:0:50) @ 25 kg/ha per week through drip.",
        "action_hi": "ड्रिप द्वारा प्रति सप्ताह 25 किग्रा पोटेशियम सल्फेट (0:0:50) दें।"
      }
    }
  }
};

/**
 * Normalizes input crop name string to standard database key
 */
function normalizeFertilizerCrop(raw) {
  if (!raw) return 'wheat';
  const s = String(raw).toLowerCase().trim();
  if (s.includes('wheat') || s.includes('गेहूं')) return 'wheat';
  if (s.includes('rice') || s.includes('धान') || s.includes('paddy')) return 'rice';
  if (s.includes('potato') || s.includes('आलू')) return 'potato';
  if (s.includes('tomato') || s.includes('टमाटर')) return 'tomato';
  if (s.includes('cotton') || s.includes('कपास')) return 'cotton';
  if (s.includes('sugar') || s.includes('गन्ना')) return 'sugarcane';
  if (s.includes('corn') || s.includes('maize') || s.includes('मक्का')) return 'corn';
  if (s.includes('soy') || s.includes('सोयाबीन')) return 'soybean';
  if (s.includes('apple') || s.includes('सेब')) return 'apple';
  if (s.includes('grape') || s.includes('अंगूर')) return 'grape';
  return 'wheat';
}

/**
 * Main On-Device Fertilizer Recommendation Generator
 */
function generateLocalFertilizerRecommendation(payload) {
  const isHi = payload.lang === 'hi' || (typeof state !== 'undefined' && state.lang === 'hi');
  const cropKey = normalizeFertilizerCrop(payload.crop);
  const data = LOCAL_FERTILIZER_DATABASE[cropKey] || LOCAL_FERTILIZER_DATABASE['wheat'];
  const stage = payload.cropStage || 'Vegetative';
  const soilType = payload.soilType || 'Alluvial / Loam Soil';
  const area = parseFloat(payload.area) || 2.0;
  const unit = payload.areaUnit || 'acre';
  const soilTest = payload.soilTest || {};

  // Check if any genuine soil test values were entered
  const hasSoilTest = Boolean(
    (soilTest.ph && soilTest.ph.trim()) ||
    (soilTest.nitrogen && soilTest.nitrogen.trim()) ||
    (soilTest.phosphorus && soilTest.phosphorus.trim()) ||
    (soilTest.potassium && soilTest.potassium.trim()) ||
    (soilTest.organic_carbon && soilTest.organic_carbon.trim())
  );

  const stageInfo = data.stages[stage] || data.stages['Vegetative'] || data.stages['Sowing / Basal'];
  const stageAdvice = isHi ? stageInfo.hi : stageInfo.en;

  // Build Primary Dose List
  const primaryDoses = [];
  if (cropKey === 'wheat') {
    primaryDoses.push({
      nutrient: 'Nitrogen (N)',
      fertilizer_name: 'Urea (46% N)',
      dose: (50 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'पहली सिंचाई पर (21-25 दिन)' : 'First Irrigation (21-25 days)',
      method: isHi ? 'खेत में बुरकाव (ब्रॉडकास्ट)' : 'Broadcast in moist soil'
    });
    primaryDoses.push({
      nutrient: 'Phosphorus (P2O5)',
      fertilizer_name: 'DAP (18-46-0)',
      dose: (55 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'बुवाई के समय (बेसल)' : 'Basal at Sowing',
      method: isHi ? 'बीज के साथ ड्रिलिंग' : 'Seed drill application'
    });
    primaryDoses.push({
      nutrient: 'Potassium (K2O)',
      fertilizer_name: 'MOP (0-0-60)',
      dose: (20 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'बुवाई के समय (बेसल)' : 'Basal at Sowing',
      method: isHi ? 'मिट्टी में मिलाना' : 'Soil incorporation'
    });
  } else if (cropKey === 'potato') {
    primaryDoses.push({
      nutrient: 'Nitrogen (N)',
      fertilizer_name: 'Urea (46% N)',
      dose: (60 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'मिट्टी चढ़ाते समय (30 दिन)' : 'Earthing up (30 days)',
      method: isHi ? 'कतारों के किनारे टॉप-ड्रेसिंग' : 'Side band placement'
    });
    primaryDoses.push({
      nutrient: 'Potassium (K2O)',
      fertilizer_name: 'SOP (0-0-50) / MOP',
      dose: (40 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'कंद बनते समय' : 'Tuber bulking',
      method: isHi ? 'पर्णीय छिड़काव / मिट्टी' : 'Foliar spray / soil'
    });
  } else if (cropKey === 'rice') {
    primaryDoses.push({
      nutrient: 'Nitrogen (N)',
      fertilizer_name: 'Urea (46% N)',
      dose: (45 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'कल्ले फूटते समय (20-25 दिन)' : 'Active tillering (20-25 DAT)',
      method: isHi ? 'पानी घटाकर बुरकाव' : 'Broadcast after draining'
    });
    primaryDoses.push({
      nutrient: 'Zinc (Zn)',
      fertilizer_name: 'Zinc Sulfate (21%)',
      dose: (10 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'रोपाई के 2-3 सप्ताह बाद' : '2-3 weeks after transplanting',
      method: isHi ? 'खेत में मिलाना' : 'Soil broadcast'
    });
  } else {
    primaryDoses.push({
      nutrient: 'Balanced NPK',
      fertilizer_name: 'NPK 19:19:19 / 12:32:16',
      dose: (50 * area).toFixed(0),
      unit: 'kg',
      timing: isHi ? 'सक्रिय बढ़वार अवस्था' : 'Active growth stage',
      method: isHi ? 'नालियों में देना' : 'Furrow/Drip application'
    });
  }

  // Micronutrients
  const micronutrients = [
    {
      name: isHi ? 'जिंक सल्फेट (21%)' : 'Zinc Sulfate (21%)',
      dose: `${(5 * area).toFixed(0)} kg`,
      timing: isHi ? 'बुवाई / कल्ले फूटते समय' : 'Basal / Tillering',
      benefit: isHi ? 'पत्तियों में पीलापन रोकता है और कल्लों की संख्या बढ़ाता है' : 'Prevents chlorosis, enhances enzymatic root growth'
    },
    {
      name: isHi ? 'बोरॉन (20%)' : 'Boron (20% Solubor)',
      dose: `${(1 * area).toFixed(1)} kg`,
      timing: isHi ? 'फूल आने से पहले' : 'Pre-flowering spray',
      benefit: isHi ? 'फूल और फल झड़ने से रोकता है, परागण सुधारता है' : 'Improves flower retention and prevents fruit cracking'
    }
  ];

  // Weather safety check
  let weatherNotice = isHi
    ? 'वर्तमान मौसम कृषि कार्यों के लिए उपयुक्त है। यूरिया देने के बाद हल्की सिंचाई अवश्य करें।'
    : 'Current weather context is favorable for fertilizer application. Ensure light irrigation after broadcasting.';

  if (payload.weather && payload.weather.current) {
    const cur = payload.weather.current;
    if (cur.rain_probability > 40 || (cur.description && cur.description.toLowerCase().includes('rain'))) {
      weatherNotice = isHi
        ? '⚠️ सावधानी: अगले 24-48 घंटों में बारिश की संभावना है। यूरिया या घुलनशील उर्वरकों का बुरकाव टालें ताकि खाद बह न जाए।'
        : '⚠️ Caution: Rain is forecasted in the next 24-48 hours. Postpone broadcasting of urea or water-soluble fertilizers to prevent leaching and surface runoff.';
    }
  }

  // Soil Test Note (Explicit User Requirement: Do NOT invent soil data!)
  let soilNote = '';
  let confidence = '';

  if (hasSoilTest) {
    confidence = isHi ? 'उच्च (मृदा परीक्षण आधारित)' : 'High (Soil-Test Calibrated)';
    soilNote = isHi
      ? `आपके दर्ज किए गए मृदा परीक्षण (pH: ${soilTest.ph || 'सामान्य'}, N: ${soilTest.nitrogen || 'मध्यम'}, P: ${soilTest.phosphorus || 'मध्यम'}, K: ${soilTest.potassium || 'मध्यम'}) के अनुसार खुराक को संतुलित किया गया है।`
      : `Fertilizer application calibrated according to your soil test parameters (pH: ${soilTest.ph || 'Neutral'}, N: ${soilTest.nitrogen || 'Med'}, P: ${soilTest.phosphorus || 'Med'}, K: ${soilTest.potassium || 'Med'}).`;
  } else {
    confidence = isHi ? 'मानक (सामान्य कृषि अनुशंसा)' : 'Standard (General Agronomic Recommendation)';
    soilNote = isHi
      ? 'अधिक सटीक सलाह के लिए मिट्टी की जानकारी दर्ज करें।'
      : 'Enter soil information for more precise advice.';
  }

  const summary = isHi
    ? `🌾 **${data.crop_hi} फसल पोषण मार्गदर्शन (${stage}):**\n\n${stageAdvice}\n\n📌 **सामान्य NPK अनुपात:** ${data.general_npk_ratio}।\n\n💧 **सिंचाई व उर्वरक संबंध:** ${data.irrigation_relation_hi}\n\n${soilNote}`
    : `🌾 **${data.crop_en} Nutrition Advisory (${stage}):**\n\n${stageAdvice}\n\n📌 **General NPK Ratio:** ${data.general_npk_ratio}.\n\n💧 **Irrigation & Nutrient Interaction:** ${data.irrigation_relation_en}\n\n${soilNote}`;

  // Resolve offline rules from database or loaded rules
  const rulesDb = (typeof FERTILIZER_RULES !== 'undefined' && FERTILIZER_RULES) || (typeof window !== 'undefined' && window.FERTILIZER_RULES) || {};
  const cropRule = rulesDb[cropKey] || {};

  const nitrogenText = isHi
    ? (cropRule.nitrogen_hi || data.general_guidance_hi || '120 किग्रा नाइट्रोजन प्रति हेक्टेयर 3 विभाजित खुराकों में दें (बुवाई, पहली सिंचाई व कल्ले फूटते समय)।')
    : (cropRule.nitrogen || data.general_guidance_en || 'Apply 120 kg N/ha in 3 split doses (at sowing, first irrigation, and active tillering).');

  const phosphorusText = isHi
    ? (cropRule.phosphorus_hi || '60 किग्रा P2O5 प्रति हेक्टेयर (DAP/SSP) बुवाई के समय पूरा बेसल खुराक के रूप में बीज के नीचे दें।')
    : (cropRule.phosphorus || 'Apply 60 kg P2O5/ha (DAP / SSP) 100% as basal dose placed below seed depth at sowing.');

  const potassiumText = isHi
    ? (cropRule.potassium_hi || '40-50 किग्रा K2O प्रति हेक्टेयर (MOP) बुवाई के समय दें ताकि फसल मजबूत रहे और रोग प्रतिरोधक क्षमता बढ़े।')
    : (cropRule.potassium || 'Apply 40-50 kg K2O/ha (MOP) at sowing time to enhance stem vigor and disease resistance.');

  const organicText = isHi
    ? (cropRule.organic_suggestion_hi || 'खेत की अंतिम जुताई में प्रति एकड़ 4-5 टन अच्छी सड़ी गोबर की खाद (FYM) या 1.5 टन वर्मीकम्पोस्ट मिलाएं।')
    : (cropRule.organic_suggestion || 'Incorporate 4-5 tonnes/acre of well-rotted Farmyard Manure (FYM) or 1.5 tonnes vermicompost during land preparation.');

  const irrigationText = isHi
    ? (cropRule.irrigation_advice_hi || data.irrigation_relation_hi || 'मिट्टी में उचित नमी होने पर ही खाद दें। यूरिया देने के बाद हल्की सिंचाई अवश्य करें।')
    : (cropRule.irrigation_advice || data.irrigation_relation_en || 'Apply fertilizers only when soil has adequate moisture. Follow urea broadcasting with a light irrigation.');

  const recObj = {
    summary: summary,
    possible_issue: isHi ? 'संतुलित पोषण एवं अवस्था-आधारित उर्वरक प्रबंधन' : 'Balanced stage-wise agronomic nutrient management',
    is_disease_suspected: false,
    confidence: confidence,
    crop: data.crop_en,
    stage: stage,
    soil: soilType,
    nitrogen: nitrogenText,
    phosphorus: phosphorusText,
    potassium: potassiumText,
    organic_suggestion: organicText,
    irrigation_advice: irrigationText,
    nutrient_focus: [
      `Nitrogen (N): ${cropRule.nitrogen_short || (isHi ? 'यूरिया' : 'Urea (46% N)')}`,
      `Phosphorus (P): ${cropRule.phosphorus_short || (isHi ? 'डीएपी / एसएसपी' : 'DAP / SSP')}`,
      `Potassium (K): ${cropRule.potassium_short || (isHi ? 'एमओपी पोटाश' : 'MOP Potash')}`
    ],
    fertilizer_categories: [
      {
        name: isHi ? 'नाइट्रोजन उर्वरक (यूरिया)' : 'Nitrogenous Fertilizer (Urea / CAN)',
        type: isHi ? 'टॉप-ड्रेसिंग' : 'Top Dressing / Split Dose',
        purpose: isHi ? 'वानस्पतिक बढ़वार और कल्ले निकलने हेतु' : 'Promotes foliage and vegetative growth',
        guideline: nitrogenText
      },
      {
        name: isHi ? 'फास्फोरस उर्वरक (DAP / SSP)' : 'Phosphatic Fertilizer (DAP / SSP)',
        type: isHi ? 'बेसल बुवाई खुराक' : 'Basal Application',
        purpose: isHi ? 'मजबूत जड़ें और कल्ले विकसित करने हेतु' : 'Root elongation, early vigor & crop establishment',
        guideline: phosphorusText
      },
      {
        name: isHi ? 'पोटाश उर्वरक (MOP / SOP)' : 'Potassic Fertilizer (MOP / SOP)',
        type: isHi ? 'बेसल / दाना भराव' : 'Basal & Grain / Fruit Filling',
        purpose: isHi ? 'रोग प्रतिरोधक क्षमता और दाने/फल का वजन व चमक' : 'Disease resistance, drought tolerance & grain/fruit weight',
        guideline: potassiumText
      }
    ],
    application_timing: isHi
      ? `${stageAdvice}। खेत में पर्याप्त नमी होने पर ही खाद दें।`
      : `${stageAdvice}. Apply when soil has adequate moisture.`,
    weather_advice: weatherNotice,
    organic_options: [
      organicText,
      isHi ? 'वर्मीकम्पोस्ट (केंचुआ खाद) @ 1.5 टन प्रति एकड़' : 'Vermicompost @ 1.5 tonnes/acre during land preparation',
      isHi ? 'बायोफर्टिलाइजर (एज़ोटोबैक्टर + पीएसबी) @ 2 किग्रा/एकड़' : 'Biofertilizers (Azotobacter + PSB) @ 2 kg/acre'
    ],
    precautions: [
      isHi ? 'तेज धूप या दोपहर के समय उर्वरक का बुरकाव न करें।' : 'Avoid fertilizer broadcasting during extreme heat or midday.',
      isHi ? 'यूरिया देने के तुरंत बाद हल्की सिंचाई अवश्य करें।' : 'Provide light irrigation immediately after broadcasting urea.',
      isHi ? 'असंगत उर्वरकों को आपस में मिलाकर न रखें।' : 'Do not mix incompatible fertilizers (e.g. Urea + SSP).'
    ]
  };

  return {
    status: 'success',
    crop: data.crop_en,
    crop_hi: data.crop_hi,
    cropStage: stage,
    soilType: soilType,
    engine: 'Local Agronomic Database (ICAR Rules)',
    recommendation: recObj,
    summary: summary,
    nitrogen: nitrogenText,
    phosphorus: phosphorusText,
    potassium: potassiumText,
    organic_suggestion: organicText,
    irrigation_advice: irrigationText,
    primary_doses: primaryDoses,
    micronutrients: micronutrients,
    weather_safety: weatherNotice
  };
}

// Preload fertilizer_rules.json if available in browser
if (typeof window !== 'undefined') {
  try {
    fetch('fertilizer_rules.json')
      .then(res => res.ok ? res.json() : null)
      .then(rules => {
        if (rules) {
          window.FERTILIZER_RULES = rules;
          console.log('[Fertilizer Engine] Preloaded fertilizer_rules.json successfully.');
        }
      })
      .catch(() => {});
  } catch (e) {}

  window.LOCAL_FERTILIZER_DATABASE = LOCAL_FERTILIZER_DATABASE;
  window.generateLocalFertilizerRecommendation = generateLocalFertilizerRecommendation;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    LOCAL_FERTILIZER_DATABASE,
    generateLocalFertilizerRecommendation
  };
}
