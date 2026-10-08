import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('disease_analyzer.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Agronomic knowledge entries to add
additional_knowledge = '''
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
    },'''

# Insert before closing brace of AGRONOMIC_KNOWLEDGE
pos = code.find('    "Soybean___healthy": {')
end_pos = code.find('\n}\n\ndef ', pos)
if end_pos != -1:
    code = code[:end_pos] + additional_knowledge + code[end_pos:]
    with open('disease_analyzer.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("[✓] Successfully added all 12 missing agronomic disease profiles to disease_analyzer.py!")
else:
    print("[!] Could not locate insertion point in disease_analyzer.py")

