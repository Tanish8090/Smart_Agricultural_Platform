/**
 * Smart Agriculture Platform (SAP) — Central Internationalization (i18n) Engine
 * Supported Languages: English (en), Hindi (hi)
 */

let currentLanguage = localStorage.getItem('sap_language') || localStorage.getItem('sap_lang') || 'en';

const TRANSLATIONS = {
  en: {
    // Top Navbar & Branding
    appTitle: 'Smart Agriculture Platform',
    appSubtitle: 'Farm Intelligence & AI Vision',
    neuralEngine: 'Neural Network Vision AI Engine',
    apiConnected: '✓ On-Device AI Model',
    yoloModelActive: 'Local Crop-Specific Model',
    multimodalActive: 'Local Trained Model (Offline)',
    searchPlaceholder: 'Search crops, diseases, weather, mandis...',
    farmerProfile: 'Farmer Profile',
    switchLanguage: 'हिंदी',
    english: 'English',
    hindi: 'हिंदी',

    // Global Navigation
    dashboard: 'Dashboard',
    home: 'Home',
    weather: 'Weather',
    cropHealth: 'Crop Health',
    diseaseDetection: 'Disease Detection',
    fertilizer: 'Fertilizer Calculator',
    fertilizerRecommendation: 'Fertilizer Recommendation',
    marketPrices: 'Market Prices',
    pestPrediction: 'Pest Prediction',
    seedRecommendation: 'Seed Recommendation',
    wasteManagement: 'Waste Management',
    environmentalMonitoring: 'Environmental Monitoring',
    farmingTools: 'Farming Tools',
    notifications: 'Notifications',
    aiFarmingAssistant: 'AI Kisan Assistant',
    profile: 'Profile',
    settings: 'Settings',
    logout: 'Logout',
    login: 'Login',
    register: 'Register',

    // Buttons
    uploadImage: 'Upload Leaf Photo',
    chooseFile: 'Browse Files',
    browseFiles: 'Browse Files',
    liveCamera: 'Launch Camera',
    launchCamera: 'Launch Camera',
    analyze: 'Diagnose Plant Disease',
    diagnosePlantDisease: 'Diagnose Plant Disease',
    scan: 'Scan',
    startScan: 'Start Scan',
    viewReport: 'View Report',
    printReport: 'Print Certificate',
    download: 'Download',
    save: 'Save',
    cancel: 'Cancel',
    close: 'Close',
    retry: 'Retry',
    refresh: 'Refresh',
    submit: 'Submit',
    next: 'Next',
    back: 'Back',
    clear: 'Clear',
    capturePhoto: 'Capture Photo',
    retake: 'Retake',
    usePhoto: 'Use Photo',
    startCamera: 'Start Camera',
    stopCamera: 'Stop Camera',
    switchCamera: 'Switch Camera',
    takePhotoScan: 'Take Photo & Scan',

    // Upload & Scanner UI
    aiCropDiseaseScanner: 'AI Crop Disease Scanner',
    scannerSubtitle: 'Upload a leaf photo or use your camera to diagnose crop diseases, calculate severity, and get organic & chemical remedies.',
    selectTargetCrop: 'Target Crop',
    selectTargetCropSubtitle: 'Routes to crop-specific trained neural network',
    uploadLeafPhoto: 'Upload Leaf Photo',
    uploadLeafPhotoDesc: 'Drag & drop file here or click to browse (JPG, PNG, WEBP)',
    takeLivePhotoCamera: 'Take Live Photo with Camera',
    takeLivePhotoCameraDesc: 'Use phone or laptop camera to scan crop leaf in real time',
    testSampleLeavesTitle: 'Test with Real Sample Leaves (1-Click Demo):',
    clickLeafDemo: 'Click any leaf to run instant AI vision scan',
    selectedImagePreview: 'Selected Image Preview',
    readyForScan: 'Ready for AI vision scan',
    noFileSelected: 'No file selected',
    invalidFile: 'Invalid file format',
    unsupportedImage: 'Unsupported image file',
    imageLoadedSuccess: 'Image loaded successfully',

    // Sample Leaf Presets
    samplePotatoBlight: '🥔 Potato Blight',
    sampleEarlyBlight: 'Early Blight',
    samplePotatoLateBlight: '🥔 Late Blight',
    sampleCornRust: '🌽 Corn Rust',
    sampleCommonRust: 'Common Rust',
    sampleCornBlight: '🌽 Leaf Blight',
    sampleNorthernBlight: 'Northern Blight',
    sampleSugarcane: '🎋 Sugarcane',
    sampleRedRot: 'Red Rot',

    // Scanner Results & Diagnostics
    aiDiagnosticAnalysis: 'AI Diagnostic Analysis',
    diseaseDetected: 'Disease Detected',
    healthyLeaf: 'Healthy Leaf',
    noDiseaseDetected: 'No Disease Detected (Crop is Healthy)',
    noPlantLeafDetected: 'No Plant Leaf Detected',
    notLeafMsg: 'The uploaded image does not contain a recognized plant leaf. Please upload a clear photo of a crop leaf.',
    notLeafTryAgain: 'Try Again with a Crop Leaf',
    modelUnavailable: 'AI model for this crop is currently unavailable.',
    modelUnavailableBadge: 'Model Not Ready',
    modelUnavailableMsg: 'Neural vision weights for this crop are currently being trained or indexed. Please select Wheat, Cotton, Sugarcane, Potato, Rice, or Soybean.',
    confidence: 'AI Confidence',
    affectedArea: 'Affected Area',
    severity: 'Severity',
    pathogen: 'Pathogen',
    cause: 'Cause',
    symptoms: 'Symptoms',
    treatment: 'Treatment',
    organicRemedy: 'Organic & Bio Treatment',
    chemicalTreatment: 'Chemical Fungicide / Pesticide',
    prevention: 'Preventive Guidance',
    recommendedAction: 'Recommended Action',
    infectionSeverityIndex: 'Infection Severity Index',
    observedSymptomsCause: 'Observed Symptoms & Cause',
    neuralProbabilities: 'Neural Class Probabilities (Top 5 Matches)',
    gradcamHeatmapTitle: 'AI Attention & Disease Region Highlighting (Grad-CAM)',
    originalUploadedLeaf: 'Original Uploaded Leaf',
    gradcamActivationHeatmap: 'Grad-CAM Activation Heatmap',
    heatmapCaption: 'Warm colored regions (red/yellow) indicate neural network focus areas with high disease lesion density.',
    moderateSeverity: 'Moderate Severity',
    highSeverity: 'High Severity',
    lowSeverity: 'Low Severity',
    crop: 'Crop',

    // Loading & Status
    loading: 'Loading...',
    scanningLoaderTitle: 'Scanning Leaf with Neural AI Model...',
    scanningLoaderSubtitle: 'Evaluating crop disease patterns, computing lesion density & severity...',
    analyzingImage: 'Analyzing leaf image...',
    detectingLeaf: 'Validating plant leaf presence...',
    runningAiModel: 'Running crop-specific neural AI model...',
    generatingReport: 'Generating diagnostic report and heatmap...',
    pleaseWait: 'Please wait...',

    // Errors
    somethingWentWrong: 'Something went wrong',
    serverError: 'Server error occurred during analysis',
    imageCouldNotBeAnalyzed: 'Image could not be analyzed',
    pleaseUploadValidImage: 'Please upload a valid leaf image file',
    pleaseSelectCrop: 'Please select a crop',
    networkError: 'Network error. Please check your internet connection.',
    tryAgain: 'Try Again',

    // Weather Module
    liveWeatherAdvisory: 'Live Weather & Agronomic Advisory',
    weatherSubtitle: 'Hyper-local weather metrics, rain probability, and crop management recommendations.',
    currentTemperature: 'Temperature',
    humidity: 'Humidity',
    windSpeed: 'Wind Speed',
    rainfallProb: 'Rain Probability',
    agriculturalAdvisory: 'Agricultural Advisory',
    sprayingCondition: 'Spraying Condition',
    irrigationNeed: 'Irrigation Need',
    forecast7Day: '7-Day Weather Forecast',
    heatStressAlert: 'Heat Stress Alert',
    favorableForSpraying: 'Favorable for Spraying',
    unfavorableForSpraying: 'Unfavorable for Spraying (Rain or High Wind)',
    noRainExpected: 'No Rain Expected',
    rainLikely: 'Rain Expected',

    // Market / Mandi Module
    mandiCommodityPrices: 'Live Mandi Commodity Prices',
    mandiSubtitle: 'Real-time market rates from APMC mandis across India with weekly price trends.',
    commodity: 'Commodity',
    mandi: 'Mandi Market',
    stateName: 'State',
    modalPrice: 'Modal Price',
    minPrice: 'Min Price',
    maxPrice: 'Max Price',
    currentPrice: 'Current Price',
    yesterday: 'Yesterday',
    weeklyTrend: 'Weekly Trend',
    nearbyMandi: 'Nearby Mandi',
    transportationCost: 'Transportation Cost',
    marketDistance: 'Market Distance',
    bestSellingTime: 'Best Selling Time',
    searchMandiPlaceholder: 'Search crop or mandi (e.g. Wheat, Kanpur)...',
    perQuintal: '/ Quintal',

    // Fertilizer Module
    fertCalculatorTitle: 'Fertilizer & Nutrition Calculator',
    fertCalculatorSubtitle: 'Precise NPK dose, secondary nutrients, and micronutrient schedules tailored to your soil and growth stage.',
    landAreaAcres: 'Land Area (Acres)',
    soilType: 'Soil Type',
    cropGrowthStage: 'Crop Growth Stage',
    recommendedFertilizer: 'Recommended Fertilizer & Nutrients',
    dosage: 'Dosage',
    applicationTiming: 'Application Timing & Method',
    organicAlternative: 'Organic Alternative',
    chemicalFertilizer: 'Chemical Fertilizer',
    calculateNutritionPlan: 'Calculate Nutrition Plan',

    // AI Assistant (Chatbot)
    aiKisanAssistant: 'AI Kisan Assistant',
    chatSubtitle: '24/7 Smart Advisor · Multilingual',
    chatPlaceholder: 'Type or speak in Hindi, English, or Hinglish... (e.g. What fertilizer should I use for wheat?)',
    clearChat: 'Clear',
    sendMessage: 'Send',
    askVoice: 'Voice Input',
    smartAdvisorBadge: '24/7 Smart Advisor',
    kisanSupportBadge: 'Hindi · English · Hinglish Support',

    // Camera Modal
    liveCameraLeafScanner: 'Live Camera Leaf Scanner',
    centerLeafInsideFrame: 'Center plant leaf inside frame',

    // Print Certificate
    printCertificateHeader: 'Smart Agriculture Platform — Plant Disease Diagnostic Certificate',
    dateOfAnalysis: 'Date of Analysis',
    cropInspected: 'Crop Inspected',
    diagnosticOutcome: 'Diagnostic Outcome',
    confidenceScore: 'AI Confidence Score',
    lesionCoverage: 'Lesion Coverage',
    prescribedTreatmentPlan: 'Prescribed Treatment Plan'
  },

  hi: {
    // Top Navbar & Branding
    appTitle: 'स्मार्ट एग्रीकल्चर प्लेटफॉर्म',
    appSubtitle: 'कृषि बुद्धिमत्ता एवं एआई विजन',
    neuralEngine: 'न्यूरल नेटवर्क विजन एआई इंजन',
    apiConnected: '✓ डिवाइस पर AI मॉडल',
    yoloModelActive: 'स्थानीय फसल-विशिष्ट मॉडल',
    multimodalActive: 'स्थानीय प्रशिक्षित मॉडल (ऑफ़लाइन)',
    searchPlaceholder: 'फसल, रोग, मौसम, मंडी भाव खोजें...',
    farmerProfile: 'किसान प्रोफ़ाइल',
    switchLanguage: 'English',
    english: 'English',
    hindi: 'हिंदी',

    // Global Navigation
    dashboard: 'डैशबोर्ड',
    home: 'होम',
    weather: 'मौसम',
    cropHealth: 'फसल स्वास्थ्य',
    diseaseDetection: 'रोग निदान',
    fertilizer: 'उर्वरक कैलकुलेटर',
    fertilizerRecommendation: 'उर्वरक सिफारिश',
    marketPrices: 'मंडी भाव',
    pestPrediction: 'कीट भविष्यवाणी',
    seedRecommendation: 'बीज सिफारिश',
    wasteManagement: 'अपशिष्ट प्रबंधन',
    environmentalMonitoring: 'पर्यावरण निगरानी',
    farmingTools: 'कृषि उपकरण',
    notifications: 'सूचनाएं',
    aiFarmingAssistant: 'किसान एआई सहायक',
    profile: 'प्रोफ़ाइल',
    settings: 'सेटिंग्स',
    logout: 'लॉगआउट',
    login: 'लॉगिन',
    register: 'पंजीकरण',

    // Buttons
    uploadImage: 'पत्ती की फोटो अपलोड करें',
    chooseFile: 'फाइल चुनें',
    browseFiles: 'फाइल चुनें',
    liveCamera: 'कैमरा चालू करें',
    launchCamera: 'कैमरा चालू करें',
    analyze: 'रोग का निदान करें',
    diagnosePlantDisease: 'रोग का निदान करें',
    scan: 'स्कैन करें',
    startScan: 'स्कैन शुरू करें',
    viewReport: 'रिपोर्ट देखें',
    printReport: 'रिपोर्ट प्रिंट करें',
    download: 'डाउनलोड',
    save: 'सहेजें',
    cancel: 'रद्द करें',
    close: 'बंद करें',
    retry: 'पुनः प्रयास करें',
    refresh: 'ताज़ा करें',
    submit: 'जमा करें',
    next: 'अगला',
    back: 'पीछे',
    clear: 'हटाएं',
    capturePhoto: 'फोटो खींचें',
    retake: 'दोबारा फोटो लें',
    usePhoto: 'फोटो का उपयोग करें',
    startCamera: 'कैमरा शुरू करें',
    stopCamera: 'कैमरा बंद करें',
    switchCamera: 'कैमरा बदलें',
    takePhotoScan: 'फोटो लें और जांचें',

    // Upload & Scanner UI
    aiCropDiseaseScanner: 'एआई फसल रोग जांच केंद्र',
    scannerSubtitle: 'पत्ती की फोटो अपलोड करें या अपने कैमरे से फोटो खींचकर बीमारी का निदान, गंभीरता का स्तर और जैविक व रासायनिक उपचार प्राप्त करें।',
    selectTargetCrop: 'लक्षित फसल',
    selectTargetCropSubtitle: 'फसल-विशिष्ट प्रशिक्षित न्यूरल नेटवर्क को निर्देशित करता है',
    uploadLeafPhoto: 'पत्ती की फोटो अपलोड करें',
    uploadLeafPhotoDesc: 'फाइल यहां खींचें या अपलोड करने के लिए क्लिक करें (JPG, PNG, WEBP)',
    takeLivePhotoCamera: 'कैमरे से तुरंत फोटो खींचें',
    takeLivePhotoCameraDesc: 'खेत में तुरंत जांच के लिए मोबाइल या लैपटॉप कैमरे का उपयोग करें',
    testSampleLeavesTitle: 'वास्तविक पत्ती नमूनों से जांचें (1-क्लिक डेमो):',
    clickLeafDemo: 'तुरंत एआई जांच के लिए किसी भी पत्ती पर क्लिक करें',
    selectedImagePreview: 'चयनित फोटो पूर्वावलोकन',
    readyForScan: 'एआई जांच के लिए तैयार',
    noFileSelected: 'कोई फाइल चयनित नहीं है',
    invalidFile: 'अमान्य फाइल प्रारूप',
    unsupportedImage: 'असमर्थित फोटो फाइल',
    imageLoadedSuccess: 'फोटो सफलतापूर्वक लोड हो गई',

    // Sample Leaf Presets
    samplePotatoBlight: '🥔 आलू झुलसा',
    sampleEarlyBlight: 'अगेती झुलसा',
    samplePotatoLateBlight: '🥔 पछेती झुलसा',
    sampleCornRust: '🌽 मक्का रतुआ',
    sampleCommonRust: 'सामान्य रतुआ',
    sampleCornBlight: '🌽 पत्ती झुलसा',
    sampleNorthernBlight: 'उत्तरी झुलसा',
    sampleSugarcane: '🎋 गन्ना',
    sampleRedRot: 'लाल सड़न (रेड रॉट)',

    // Scanner Results & Diagnostics
    aiDiagnosticAnalysis: 'एआई रोग निदान विश्लेषण',
    diseaseDetected: 'रोग का पता चला',
    healthyLeaf: 'स्वस्थ पत्ती',
    noDiseaseDetected: 'कोई रोग नहीं मिला (फसल स्वस्थ है)',
    noPlantLeafDetected: 'कोई पौधे की पत्ती नहीं पाई गई',
    notLeafMsg: 'अपलोड की गई फोटो में कोई पौधे की पत्ती नहीं पाई गई। कृपया किसी फसल की पत्ती की स्पष्ट फोटो अपलोड करें।',
    notLeafTryAgain: 'फसल की पत्ती के साथ पुनः प्रयास करें',
    modelUnavailable: 'इस फसल के लिए AI मॉडल अभी उपलब्ध नहीं है।',
    modelUnavailableBadge: 'मॉडल तैयार नहीं',
    modelUnavailableMsg: 'इस फसल के न्यूरल विजन मॉडल्स वर्तमान में प्रशिक्षित किए जा रहे हैं। कृपया गेहूं, कपास, गन्ना, आलू, धान अथवा सोयाबीन चुनें।',
    confidence: 'विश्वास स्तर',
    affectedArea: 'प्रभावित क्षेत्र',
    severity: 'गंभीरता',
    pathogen: 'रोगजनक',
    cause: 'कारण',
    symptoms: 'लक्षण',
    treatment: 'उपचार',
    organicRemedy: 'जैविक उपचार',
    chemicalTreatment: 'रासायनिक फफूंदनाशी / कीटनाशक',
    prevention: 'बचाव और सावधानी',
    recommendedAction: 'अनुशंसित कार्रवाई',
    infectionSeverityIndex: 'संक्रमण गंभीरता सूचकांक',
    observedSymptomsCause: 'देखे गए लक्षण और कारण',
    neuralProbabilities: 'संभावित बीमारियां (शीर्ष 5)',
    gradcamHeatmapTitle: 'एआई विजुअल ध्यान एवं प्रभावित क्षेत्र (Grad-CAM)',
    originalUploadedLeaf: 'मूल अपलोड की गई पत्ती',
    gradcamActivationHeatmap: 'Grad-CAM सक्रियण हीटमैप',
    heatmapCaption: 'गर्म रंग वाले क्षेत्र (लाल/पीला) न्यूरल नेटवर्क के उच्च रोग संक्रमण घनत्व वाले फोकस क्षेत्रों को दर्शाते हैं।',
    moderateSeverity: 'मध्यम संक्रमण',
    highSeverity: 'गंभीर संक्रमण',
    lowSeverity: 'हल्का संक्रमण',
    crop: 'फसल',

    // Loading & Status
    loading: 'लोड हो रहा है...',
    scanningLoaderTitle: 'न्यूरल एआई मॉडल द्वारा पत्ती की जांच जारी...',
    scanningLoaderSubtitle: '88 बीमारियों के पैटर्न का मूल्यांकन और रोग घनत्व की गणना की जा रही है...',
    analyzingImage: 'पत्ती की फोटो का विश्लेषण किया जा रहा है...',
    detectingLeaf: 'पौधे की पत्ती की पहचान की जा रही है...',
    runningAiModel: 'फसल-विशिष्ट न्यूरल एआई मॉडल चलाया जा रहा है...',
    generatingReport: 'निदान रिपोर्ट और हीटमैप तैयार किया जा रहा है...',
    pleaseWait: 'कृपया प्रतीक्षा करें...',

    // Errors
    somethingWentWrong: 'कुछ गलत हो गया',
    serverError: 'विश्लेषण के दौरान सर्वर में त्रुटि हुई',
    imageCouldNotBeAnalyzed: 'फोटो का विश्लेषण नहीं किया जा सका',
    pleaseUploadValidImage: 'कृपया एक मान्य पत्ती की फोटो अपलोड करें',
    pleaseSelectCrop: 'कृपया एक लक्षित फसल चुनें',
    networkError: 'नेटवर्क कनेक्शन त्रुटि। कृपया इंटरनेट जांचें।',
    tryAgain: 'पुनः प्रयास करें',

    // Weather Module
    liveWeatherAdvisory: 'लाइव मौसम एवं कृषि सलाह',
    weatherSubtitle: 'स्थानीय मौसम संकेतक, बारिश की संभावना और फसल सुरक्षा परामर्श।',
    currentTemperature: 'तापमान',
    humidity: 'आर्द्रता (नमी)',
    windSpeed: 'हवा की गति',
    rainfallProb: 'बारिश की संभावना',
    agriculturalAdvisory: 'कृषि परामर्श',
    sprayingCondition: 'छिड़काव की स्थिति',
    irrigationNeed: 'सिंचाई की आवश्यकता',
    forecast7Day: '7-दिवसीय मौसम पूर्वानुमान',
    heatStressAlert: 'गर्मी का तनाव अलर्ट',
    favorableForSpraying: 'छिड़काव के लिए अनुकूल मौसम',
    unfavorableForSpraying: 'छिड़काव के लिए प्रतिकूल (बारिश या तेज हवा)',
    noRainExpected: 'बारिश की कोई संभावना नहीं',
    rainLikely: 'बारिश की संभावना',

    // Market / Mandi Module
    mandiCommodityPrices: 'लाइव मंडी जिंस भाव',
    mandiSubtitle: 'भारत भर की प्रमुख कृषि मंडियों से रीयल-टाइम कीमतें और मूल्य रुझान।',
    commodity: 'फसल / जिंस',
    mandi: 'मंडी',
    stateName: 'राज्य',
    modalPrice: 'औसत भाव',
    minPrice: 'न्यूनतम भाव',
    maxPrice: 'अधिकतम भाव',
    currentPrice: 'वर्तमान भाव',
    yesterday: 'कल का भाव',
    weeklyTrend: 'साप्ताहिक रुझान',
    nearbyMandi: 'निकटतम मंडी',
    transportationCost: 'परिवहन लागत',
    marketDistance: 'मंडी की दूरी',
    bestSellingTime: 'बेचने का सबसे अच्छा समय',
    searchMandiPlaceholder: 'फसल या मंडी खोजें (उदा. गेहूं, कानपुर)...',
    perQuintal: '/ क्विंटल',

    // Fertilizer Module
    fertCalculatorTitle: 'उर्वरक एवं पोषण कैलकुलेटर',
    fertCalculatorSubtitle: 'आपकी मिट्टी और फसल की अवस्था के अनुसार सटीक एनपीके और सूक्ष्म पोषक तत्वों का कार्यक्रम।',
    landAreaAcres: 'खेत का क्षेत्रफल (एकड़)',
    soilType: 'मिट्टी का प्रकार',
    cropGrowthStage: 'फसल की वृद्धि अवस्था',
    recommendedFertilizer: 'अनुशंसित खाद एवं पोषक तत्व',
    dosage: 'मात्रा',
    applicationTiming: 'प्रयोग विधि एवं समय',
    organicAlternative: 'जैविक विकल्प',
    chemicalFertilizer: 'रासायनिक उर्वरक',
    calculateNutritionPlan: 'पोषण योजना की गणना करें',

    // AI Assistant (Chatbot)
    aiKisanAssistant: 'किसान एआई सहायक',
    chatSubtitle: '24/7 स्मार्ट कृषि परामर्शदाता · बहुभाषी',
    chatPlaceholder: 'खेती से जुड़ा कोई भी सवाल पूछें या बोलें... (जैसे: गेहूं में कौन सी खाद डालें?)',
    clearChat: 'हटाएं',
    sendMessage: 'भेजें',
    askVoice: 'आवाज से पूछें',
    smartAdvisorBadge: '24/7 स्मार्ट परामर्शदाता',
    kisanSupportBadge: 'हिंदी · इंग्लिश · हिंग्लिश सहायता',

    // Camera Modal
    liveCameraLeafScanner: 'लाइव कैमरा लीफ स्कैनर',
    centerLeafInsideFrame: 'पत्ती को फ्रेम के बीच में रखें',

    // Print Certificate
    printCertificateHeader: 'स्मार्ट एग्रीकल्चर प्लेटफॉर्म — पादप रोग निदान प्रमाणपत्र',
    dateOfAnalysis: 'जांच की तारीख',
    cropInspected: 'जांची गई फसल',
    diagnosticOutcome: 'निदान परिणाम',
    confidenceScore: 'एआई विश्वास स्तर',
    lesionCoverage: 'संक्रमित क्षेत्र',
    prescribedTreatmentPlan: 'निर्धारित उपचार योजना'
  }
};

const CROP_TRANSLATIONS = {
  auto: { en: '🔍 Auto Detect (General)', hi: '🔍 स्वचालित पहचान (सामान्य)' },
  wheat: { en: 'Wheat (Yellow Rust / Healthy)', hi: 'गेहूं (पीला रतुआ / स्वस्थ)' },
  cotton: { en: 'Cotton (Bacterial Blight / Healthy)', hi: 'कपास (जीवाणु झुलसा / स्वस्थ)' },
  sugarcane: { en: 'Sugarcane (Red Rot / Healthy)', hi: 'गन्ना (लाल सड़न / स्वस्थ)' },
  potato: { en: 'Potato (Early Blight / Late Blight / Healthy)', hi: 'आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
  rice: { en: 'Rice (Blast / Brown Spot / Healthy)', hi: 'धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)' },
  soybean: { en: 'Soybean (Rust / Healthy)', hi: 'सोयाबीन (रस्ट / स्वस्थ)' },
  tomato: { en: 'Tomato (Early Blight / Late Blight / Healthy)', hi: 'टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
  corn: { en: 'Corn / Maize (Common Rust / Leaf Blight / Healthy)', hi: 'मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)' },
  apple: { en: 'Apple (Scab / Healthy)', hi: 'सेब (स्कैब / स्वस्थ)' },
  grape: { en: 'Grape (Black Rot / Healthy)', hi: 'अंगूर (ब्लैक रॉट / स्वस्थ)' }
};

const DISEASE_TRANSLATIONS = {
  'Wheat___healthy': {
    name_en: 'Healthy Wheat Leaf',
    name_hi: 'स्वस्थ गेहूं की पत्ती',
    crop_en: 'Wheat',
    crop_hi: 'गेहूं',
    symptoms_en: 'Uniform green leaf blade with intact cell structure, free of rust pustules, lesions, or chlorosis.',
    symptoms_hi: 'पत्ती पूरी तरह हरी, चमकदार और किसी भी प्रकार के रतुआ या धब्बों से मुक्त है।',
    cause_en: 'No pathogen detected. Optimum crop nourishment and healthy chlorophyll content.',
    cause_hi: 'कोई रोगजनक नहीं मिला। फसल पूरी तरह पोषित एवं स्वस्थ है।',
    organic_en: 'Apply bio-fertilizers (Azotobacter @ 2kg/ha) and PSB to sustain plant vigor.',
    organic_hi: 'फसल की मजबूती बनाए रखने हेतु एजोटोबैक्टर व पीएसबी का प्रयोग करें।',
    chemical_en: 'No chemical fungicides needed. Maintain recommended irrigation and NPK split schedule.',
    chemical_hi: 'किसी रासायनिक फफूंदनाशी की आवश्यकता नहीं है। संतुलित सिंचाई रखें।',
    prevention_en: 'Maintain regular field scouting; ensure good soil drainage and balanced nitrogen dosing.',
    prevention_hi: 'नियमित निगरानी रखें और यूरिया का संतुलित मात्रा में ही प्रयोग करें।',
    is_healthy: true
  },
  'Wheat___Yellow_rust': {
    name_en: 'Wheat Yellow Rust (Stripe Rust)',
    name_hi: 'गेहूं का पीला रतुआ (येलो रस्ट)',
    crop_en: 'Wheat',
    crop_hi: 'गेहूं',
    symptoms_en: 'Bright yellow-orange powdery pustules arranged in narrow parallel linear stripes along leaf veins.',
    symptoms_hi: 'पत्तियों की नसों के समानांतर लंबी पीली धारियों में पाउडर जैसे फफोले दिखाई देते हैं।',
    cause_en: 'Puccinia striiformis f. sp. tritici fungus, favored by cool moist weather (10-15°C).',
    cause_hi: 'पक्सीनिया स्ट्राइफॉर्मिस कवक, जो 10-15°C के ठंडे और नम मौसम में तेजी से फैलता है।',
    organic_en: 'Spray fermented sour buttermilk (chhaas) @ 5% mixed with garlic-chilli extract. Apply Trichoderma harzianum.',
    organic_hi: 'खट्टी छाछ (5%) या लहसुन का अर्क स्प्रे करें। ट्राइकोडर्मा हरजिएनम का छिड़काव करें।',
    chemical_en: 'Propiconazole 25% EC (Tilt @ 1 ml/L or 200 ml/acre in 200 L water) or Tebuconazole 25.9% EC.',
    chemical_hi: 'प्रोपिकोनाज़ोल 25% EC (टिल्ट 1 मिली/लीटर पानी) या टेबुकोनाज़ोल का तुरंत छिड़काव करें।',
    prevention_en: 'Plant certified rust-resistant varieties (HD-2967, HD-3086, DBW-187); avoid excess urea.',
    prevention_hi: 'रोग प्रतिरोधी किस्में (HD-2967, DBW-187) बोएं और अत्यधिक यूरिया से बचें।',
    is_healthy: false
  },
  'Wheat___Brown_rust': {
    name_en: 'Wheat Brown Rust (Leaf Rust)',
    name_hi: 'गेहूं का भूरा रतुआ (ब्राउन रस्ट)',
    crop_en: 'Wheat',
    crop_hi: 'गेहूं',
    symptoms_en: 'Small round to oval brown/orange-red scattered pustules primarily on upper leaf surfaces.',
    symptoms_hi: 'पत्तियों की ऊपरी सतह पर गोल या अंडाकार भूरे-नारंगी बिखरे हुए फफोले बनते हैं।',
    cause_en: 'Puccinia triticina fungus, thriving in warm humid temperatures (15-25°C).',
    cause_hi: 'पक्सीनिया ट्रिटिसिना कवक, जो 15-25°C तापमान और उच्च आर्द्रता में सक्रिय होता है।',
    organic_en: 'Neem seed kernel extract (NSKE 5%) foliar spray; apply Pseudomonas fluorescens @ 5 g/L.',
    organic_hi: 'नीम के बीज का अर्क (5%) या स्यूडोमोनास फ्लोरोसेंस का छिड़काव करें।',
    chemical_en: 'Spray Propiconazole 25% EC (1 ml/L) or Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).',
    chemical_hi: 'प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) या एजोक्सीस्ट्रोबिन का छिड़काव करें।',
    prevention_en: 'Timely sowing; practice crop rotation; avoid over-irrigation during canopy closure.',
    prevention_hi: 'समय पर बुवाई करें और फसल चक्र का पालन करें।',
    is_healthy: false
  },
  'Wheat___Septoria': {
    name_en: 'Wheat Septoria Leaf Blight',
    name_hi: 'गेहूं का सेप्टोरिया पत्ती झुलसा',
    crop_en: 'Wheat',
    crop_hi: 'गेहूं',
    symptoms_en: 'Irregular chlorotic yellow-brown flecks developing into rectangular necrotic lesions with tiny black pycnidia dots.',
    symptoms_hi: 'पत्तियों पर पीले-भूरे आयताकार धब्बे जिन पर काले छोटे-छोटे दाने (पिक्नीडिया) दिखाई देते हैं।',
    cause_en: 'Zymoseptoria tritici fungal pathogen transmitted via rain splash and infected stubble.',
    cause_hi: 'ज़ाइमोसेप्टोरिया ट्रिटिसी कवक, जो बारिश के छींटों और फसल अवशेषों से फैलता है।',
    organic_en: 'Foliar spray with copper soap or bio-agent Bacillus subtilis @ 5 ml/L.',
    organic_hi: 'बेसिलस सबटिलिस या कॉपर-युक्त जैविक घोल का छिड़काव करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2.5 g/L) or Tebuconazole 50% + Trifloxystrobin 25% WG (0.6 g/L).',
    chemical_hi: 'मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या टेबुकोनाज़ोल का छिड़काव करें।',
    prevention_en: 'Plough under stubble after harvest; ensure crop spacing for good sunlight penetration.',
    prevention_hi: 'फसल कटाई के बाद अवशेषों को गहरा जोतें और कतारों में उचित दूरी रखें।',
    is_healthy: false
  },
  'Cotton___healthy': {
    name_en: 'Healthy Cotton Leaf',
    name_hi: 'स्वस्थ कपास की पत्ती',
    crop_en: 'Cotton',
    crop_hi: 'कपास',
    symptoms_en: 'Broad palmate dark green foliage with clear vein network, free of water-soaked spots or leaf curling.',
    symptoms_hi: 'कपास की पत्तियां चौड़ी, गहरे हरे रंग की और किसी भी सिकुड़न या धब्बे से मुक्त हैं।',
    cause_en: 'No infection detected. Balanced canopy development with adequate micronutrients.',
    cause_hi: 'कोई संक्रमण नहीं है। फसल पूरी तरह स्वस्थ और पोषण युक्त है।',
    organic_en: 'Apply humic acid @ 2 ml/L or foliar spray 1% 19:19:19 to sustain vegetative health.',
    organic_hi: 'ह्यूमिक एसिड या 19:19:19 का हल्का पर्णीय छिड़काव करें।',
    chemical_en: 'No chemical pesticide required.',
    chemical_hi: 'किसी रासायनिक कीटनाशक की आवश्यकता नहीं है।',
    prevention_en: 'Maintain clean field borders; monitor sucking pest traps regularly.',
    prevention_hi: 'खेत की मेड़ों को साफ रखें और रसचूसक कीटों की निगरानी रखें।',
    is_healthy: true
  },
  'Cotton___Bacterial_blight': {
    name_en: 'Cotton Bacterial Blight (Blackarm)',
    name_hi: 'कपास का जीवाणु झुलसा रोग (ब्लैक आर्म)',
    crop_en: 'Cotton',
    crop_hi: 'कपास',
    symptoms_en: 'Angular water-soaked spots bounded by leaf veinlets, turning dark brown/black. Lesions can extend along main veins.',
    symptoms_hi: 'पत्तियों की नसों के बीच कोणीय गीले धब्बे जो बाद में काले-भूरे होकर सूख जाते हैं।',
    cause_en: 'Xanthomonas citri pv. malvacearum bacterium, spread through wind-blown rain and seed.',
    cause_hi: 'जैंथोमोनास सिट्री जीवाणु, जो बारिश और हवा की नमी से फैलता है।',
    organic_en: 'Seed treatment with Pseudomonas fluorescens; foliar spray of cow urine extract (10%) with neem.',
    organic_hi: 'स्यूडोमोनास से बीजोपचार करें; गोमूत्र (10%) और नीम के अर्क का छिड़काव करें।',
    chemical_en: 'Streptocycline (1 g/10 L) mixed with Copper Oxychloride 50% WP (25 g/10 L). Spray twice at 12-day interval.',
    chemical_hi: 'स्ट्रेप्टोसाइक्लिन (1 ग्राम) + कॉपर ऑक्सीक्लोराइड (25 ग्राम) प्रति 10 लीटर पानी में मिलाकर स्प्रे करें।',
    prevention_en: 'Delint seeds with acid before sowing; destroy infected crop residues; avoid overhead irrigation.',
    prevention_hi: 'प्रमाणित बीजों का प्रयोग करें और खेत में जलभराव न होने दें।',
    is_healthy: false
  },
  'Cotton___Curl_virus': {
    name_en: 'Cotton Leaf Curl Virus (CLCuV)',
    name_hi: 'कपास का पत्ती मरोड़ विषाणु (लीफ कर्ल)',
    crop_en: 'Cotton',
    crop_hi: 'कपास',
    symptoms_en: 'Upward or downward cupping/curling of leaves, vein thickening, and enations (leaf-like outgrowths) on underside.',
    symptoms_hi: 'पत्तियां ऊपर या नीचे की ओर मुड़ जाती हैं, नसें मोटी हो जाती हैं और पत्ती के नीचे उभार बन जाते हैं।',
    cause_en: 'Begomovirus transmitted exclusively by the whitefly vector (Bemisia tabaci).',
    cause_hi: 'बेगोमोवायरस जो मुख्य रूप से सफेद मक्खी (व्हाइटफ्लाई) द्वारा फैलता है।',
    organic_en: 'Install yellow sticky traps (15-20 traps/acre); spray Neem oil 10000 ppm @ 2 ml/L.',
    organic_hi: 'पीले चिपचिपे ट्रैप (15-20 प्रति एकड़) लगाएं; नीम का तेल (2 मिली/लीटर) छिड़कें।',
    chemical_en: 'Control whiteflies: Diafenthiuron 50% WP (1.2 g/L) or Pyriproxyfen 10% + Bifenthrin 10% EC (2 ml/L).',
    chemical_hi: 'सफेद मक्खी नियंत्रण हेतु डायफेंथियूरॉन 50% WP (1.2 ग्राम/लीटर) का छिड़काव करें।',
    prevention_en: 'Rogue out infected plants early; destroy weed hosts like Abutilon; grow CLCuV resistant Bt hybrids.',
    prevention_hi: 'संक्रमित पौधों को उखाड़कर नष्ट करें और मेड़ों से खरपतवार हटाएं।',
    is_healthy: false
  },
  'Sugarcane___healthy': {
    name_en: 'Healthy Sugarcane Leaf',
    name_hi: 'स्वस्थ गन्ने की पत्ती',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Vigorous elongated green leaves with clear white midrib and sharp serrated margins, free from discoloration.',
    symptoms_hi: 'गन्ने की पत्तियां लंबी, गहरे हरे रंग की और सफेद मध्य शिरा वाली पूरी तरह स्वस्थ हैं।',
    cause_en: 'Optimal plant vigor and effective cane canopy management.',
    cause_hi: 'फसल पूरी तरह स्वस्थ एवं रोगमुक्त है।',
    organic_en: 'Trash mulching between rows to conserve moisture and encourage mycorrhizal activity.',
    organic_hi: 'कतारों के बीच पत्तों की मल्चिंग करें जिससे नमी बनी रहे।',
    chemical_en: 'No chemical intervention required.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है।',
    prevention_en: 'Regular irrigation during tillering; trash mulching and earthing up.',
    prevention_hi: 'समय पर सिंचाई और मिट्टी चढ़ाने का कार्य करें।',
    is_healthy: true
  },
  'Sugarcane___Red_rot': {
    name_en: 'Sugarcane Red Rot (Colletotrichum falcatum)',
    name_hi: 'गन्ने का लाल सड़न रोग (रेड रॉट)',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Discoloration of third/fourth leaf, withered spindle with midrib lesions showing dark red spots with white centers.',
    symptoms_hi: 'ऊपरी पत्तियां पीली पड़कर सूखती हैं और मध्य शिरा पर लाल रंग के धब्बे सफेद केंद्र के साथ दिखते हैं।',
    cause_en: 'Colletotrichum falcatum fungal pathogen, the most destructive sugarcane disease in India.',
    cause_hi: 'कोलेटोट्राइकम फैल्केटम कवक, जो गन्ने की सबसे विनाशकारी बीमारी है।',
    organic_en: 'Dip setts in Trichoderma viride culture (10 g/L) for 30 minutes before planting.',
    organic_hi: 'बुवाई से पहले बीज के टुकड़ों को ट्राइकोडर्मा घोल (10 ग्राम/लीटर) में 30 मिनट भिगोएं।',
    chemical_en: 'Sett treatment with Carbendazim 50% WP (1 g/L) or Thiophanate Methyl 70% WP. Spray Thiophanate Methyl 1.5 g/L.',
    chemical_hi: 'कार्बेन्डाजिम (1 ग्राम/लीटर) से बीजोपचार करें अथवा थियोफैनेट मिथाइल (1.5 ग्राम/लीटर) का छिड़काव करें।',
    prevention_en: 'Use certified red rot resistant varieties (Co-0238 replacements); follow 2-year crop rotation; avoid ratoon of infected fields.',
    prevention_hi: 'रोग प्रतिरोधी किस्में लगाएं; पेड़ी फसल न रखें और संक्रमित पौधों को जड़ से उखाड़ें।',
    is_healthy: false
  },
  'Sugarcane___Mosaic': {
    name_en: 'Sugarcane Mosaic Virus',
    name_hi: 'गन्ने का मोज़ेक रोग',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Contrasting islands of normal dark green tissue surrounded by pale green or yellowish chlorotic patches.',
    symptoms_hi: 'पत्तियों पर गहरे और हल्के हरे रंग के चकत्ते (मोज़ेक पैटर्न) दिखाई देते हैं।',
    cause_en: 'Sugarcane Mosaic Potyvirus (SCMV) transmitted by aphids and infected seed cane.',
    cause_hi: 'पॉटीवायरस जो माहू (एफिड्स) और रोगग्रस्त बीज द्वारा फैलता है।',
    organic_en: 'Spray 5% neem extract to suppress aphid populations; treat setts with aerated steam.',
    organic_hi: 'माहू की रोकथाम हेतु नीम का अर्क (5%) स्प्रे करें।',
    chemical_en: 'Foliar spray Imidacloprid 17.8% SL (0.3 ml/L) to control aphid vectors.',
    chemical_hi: 'माहू कीट नियंत्रण के लिए इमिडाक्लोप्रिड (0.3 मिली/लीटर) का छिड़काव करें।',
    prevention_en: 'Plant tissue-culture disease-free seed setts; rogue out mosaic-infected clumps immediately.',
    prevention_hi: 'रोगमुक्त टिशू कल्चर बीज लगाएं और प्रभावित पौधों को निकाल दें।',
    is_healthy: false
  },
  'Sugarcane___Bacterial_blight': {
    name_en: 'Sugarcane Bacterial Blight',
    name_hi: 'गन्ने का जीवाणु झुलसा',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Long water-soaked translucent streaks turning reddish-brown along leaf lamina and sheath.',
    symptoms_hi: 'पत्तियों पर लंबी पारदर्शी धारियां जो बाद में लाल-भूरे रंग में बदल जाती हैं।',
    cause_en: 'Acidovorax avenae bacterial pathogen favored by warm humid weather.',
    cause_hi: 'एसिडोवोरैक्स एवेनी जीवाणु संक्रमण।',
    organic_en: 'Pseudomonas fluorescens spray @ 5 g/L; improve soil drainage.',
    organic_hi: 'स्यूडोमोनास फ्लोरोसेंस का छिड़काव करें और खेत में जल निकासी सुधारें।',
    chemical_en: 'Copper Oxychloride 50% WP (2.5 g/L) + Streptocycline (1 g/10 L).',
    chemical_hi: 'कॉपर ऑक्सीक्लोराइड (2.5 ग्राम/लीटर) + स्ट्रेप्टोसाइक्लिन (1 ग्राम/10 ली) का स्प्रे करें।',
    prevention_en: 'Avoid stagnant water in fields; source disease-free nursery stock.',
    prevention_hi: 'खेत में पानी जमा न होने दें और स्वस्थ बीज का उपयोग करें।',
    is_healthy: false
  },
  'Sugarcane___Red_stripe': {
    name_en: 'Sugarcane Red Stripe',
    name_hi: 'गन्ने की लाल पट्टी रोग',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Narrow, sharply defined dark red longitudinal stripes following leaf veins, occasionally rotting spindle.',
    symptoms_hi: 'पत्ती की नसों के साथ संकरी, स्पष्ट लाल रंग की लंबी धारियां बन जाती हैं।',
    cause_en: 'Acidovorax avenae subsp. avenae bacterium.',
    cause_hi: 'जीवाणु संक्रमण जो गर्म और उमस भरे दिनों में तेजी से फैलता है।',
    organic_en: 'Spray fermented biological butter-milk (5%) with copper bio-chelates.',
    organic_hi: 'खट्टी छाछ (5%) या नीम का अर्क छिड़कें।',
    chemical_en: 'Spray Copper Hydroxide 53.8% DF (2 g/L) or Copper Oxychloride (2.5 g/L).',
    chemical_hi: 'कॉपर हाइड्रोक्साइड (2 ग्राम/लीटर) का पर्णीय छिड़काव करें।',
    prevention_en: 'Avoid high doses of nitrogenous fertilizers in humid season; remove diseased leaves.',
    prevention_hi: 'उमस के मौसम में यूरिया कम डालें और रोगग्रस्त पत्तों को हटाएं।',
    is_healthy: false
  },
  'Sugarcane___Rust': {
    name_en: 'Sugarcane Rust (Puccinia melanocephala)',
    name_hi: 'गन्ने का रतुआ रोग',
    crop_en: 'Sugarcane',
    crop_hi: 'गन्ना',
    symptoms_en: 'Small, elongated yellowish spots on both surfaces, enlarging into reddish-brown pustules that rupture.',
    symptoms_hi: 'पत्तियों पर छोटे पीले धब्बे जो बाद में लाल-भूरे उभरे हुए फफोलों में बदल जाते हैं।',
    cause_en: 'Puccinia melanocephala fungus spread by airborne urediniospores.',
    cause_hi: 'पक्सीनिया मेलानोसेफला कवक, जो हवा द्वारा फैलता है।',
    organic_en: 'Foliar spray with Trichoderma viride (5 g/L) or garlic-mustard oil emulsion.',
    organic_hi: 'ट्राइकोडर्मा (5 ग्राम/लीटर) या लहसुन-सरसों तेल का घोल स्प्रे करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2 g/L) or Pyraclostrobin 20% WG (1 g/L) at first symptom appearance.',
    chemical_hi: 'मैंकोज़ेब (2 ग्राम/लीटर) या पायराक्लोस्ट्रोबिन का छिड़काव करें।',
    prevention_en: 'Cultivate resistant sugarcane cultivars; widen row spacing to 120 cm for ventilation.',
    prevention_hi: 'कतारों की दूरी 120 सेमी रखें ताकि हवा व धूप मिल सके।',
    is_healthy: false
  },
  'Potato___healthy': {
    name_en: 'Healthy Potato Leaf',
    name_hi: 'स्वस्थ आलू की पत्ती',
    crop_en: 'Potato',
    crop_hi: 'आलू',
    symptoms_en: 'Lush dark green compound foliage with intact margins, free of target spots, water-soaking, or leaf curl.',
    symptoms_hi: 'आलू की पत्तियां पूरी तरह स्वस्थ, हरी और किसी भी झुलसा या धब्बे से रहित हैं।',
    cause_en: 'Optimum plant health and effective late blight prevention.',
    cause_hi: 'पौधा पूरी तरह स्वस्थ है और कोई रोग नहीं है।',
    organic_en: 'Apply seaweed extract @ 2 ml/L to enhance tuber bulking vigor.',
    organic_hi: 'कंदों के विकास हेतु समुद्री शैवाल अर्क (2 मिली/लीटर) का प्रयोग करें।',
    chemical_en: 'No chemical fungicide required. Maintain earthing up and irrigation schedule.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है। नियमित मिट्टी चढ़ाएं।',
    prevention_en: 'Use certified pathogen-free seed tubers; scout crops during foggy weather.',
    prevention_hi: 'प्रमाणित रोगमुक्त आलू बीज का उपयोग करें और कोहरे में निगरानी रखें।',
    is_healthy: true
  },
  'Potato___Early_blight': {
    name_en: 'Potato Early Blight (Alternaria solani)',
    name_hi: 'आलू का अगेती झुलसा रोग (अर्ली ब्लाइट)',
    crop_en: 'Potato',
    crop_hi: 'आलू',
    symptoms_en: 'Dark brown to black necrotic spots with characteristic concentric rings (target-board appearance) on mature foliage.',
    symptoms_hi: 'निचली पत्तियों पर गोल भूरे-काले धब्बे बनते हैं जिनमें छल्ले (टारगेट बोर्ड) जैसे घेरे होते हैं।',
    cause_en: 'Alternaria solani fungal pathogen, thriving in alternating dry and wet humid weather.',
    cause_hi: 'अल्टरनेरिया सोलानी कवक, जो सूखे और नम मौसम के उतार-चढ़ाव में फैलता है।',
    organic_en: 'Spray sour curd buttermilk (chhaas) @ 5% with neem oil (3 ml/L). Apply Trichoderma @ 5 g/L.',
    organic_hi: 'खट्टी छाछ (5%) और नीम का तेल (3 मिली/लीटर) मिलाकर स्प्रे करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2.5 g/L) or Chlorothalonil 75% WP (2 g/L) or Azoxystrobin (1 ml/L).',
    chemical_hi: 'मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या क्लोरोथैलोनिल का 10-12 दिन के अंतराल पर छिड़काव करें।',
    prevention_en: 'Maintain balanced potash fertilization; avoid overhead sprinkler irrigation; rotate with non-solanaceous crops.',
    prevention_hi: 'पोटाश का संतुलित प्रयोग करें और आलू के बाद दलहनी फसलें लगाएं।',
    is_healthy: false
  },
  'Potato___Late_blight': {
    name_en: 'Potato Late Blight (Phytophthora infestans)',
    name_hi: 'आलू का पछेती झुलसा रोग (लेट ब्लाइट)',
    crop_en: 'Potato',
    crop_hi: 'आलू',
    symptoms_en: 'Irregular water-soaked pale-to-dark green lesions rapidly turning purplish-black, with delicate white mold on underside in high humidity.',
    symptoms_hi: 'पत्तियों के किनारों पर काले-बैंगनी पानीदार धब्बे जो तेजी से फैलते हैं और पत्ती के नीचे सफेद फफूंद दिखती है।',
    cause_en: 'Phytophthora infestans oomycete, devastating in cloudy foggy weather with temperatures 12-18°C.',
    cause_hi: 'फाइटोफ्थोरा इन्फेस्टन्स कवक, जो कोहरे, ठंड (12-18°C) और बादलों के मौसम में 48 घंटे में पूरी फसल नष्ट कर सकता है।',
    organic_en: 'Preventive foliar spray of Trichoderma harzianum; spray Bordeaux mixture 1% prior to fog onset.',
    organic_hi: 'कोहरा पड़ने से पहले बोर्डो मिश्रण (1%) या ट्राइकोडर्मा का छिड़काव करें।',
    chemical_en: 'Curative: Cymoxanil 8% + Mancozeb 64% WP (Moximate @ 2.5 g/L) or Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ @ 2 g/L) or Dimethomorph (1 g/L).',
    chemical_hi: 'साइमोक्सानिल + मैंकोज़ेब (2.5 ग्राम/लीटर) या रिडोमिल (2 ग्राम/लीटर) का तुरंत छिड़काव करें।',
    prevention_en: 'Earth up deeply to protect tubers; monitor late blight forecasting bulletins; destroy infected haulms.',
    prevention_hi: 'कंदों को ढकने के लिए गहरी मिट्टी चढ़ाएं और मौसम विभाग की चेतावनी पर तुरंत स्प्रे करें।',
    is_healthy: false
  },
  'Rice___healthy': {
    name_en: 'Healthy Rice Leaf',
    name_hi: 'स्वस्थ धान की पत्ती',
    crop_en: 'Rice',
    crop_hi: 'धान (चावल)',
    symptoms_en: 'Clean vibrant green linear blades with sharp tips, completely free from spindle lesions or brown spots.',
    symptoms_hi: 'धान की पत्तियां पूरी तरह स्वस्थ, हरी और किसी भी झुलसा या धब्बे से रहित हैं।',
    cause_en: 'No pathogen detected. Balanced soil fertility and proper standing water management.',
    cause_hi: 'कोई संक्रमण नहीं है। उचित जल प्रबंधन और स्वस्थ फसल।',
    organic_en: 'Inoculate root zone with Azospirillum and Phosphobacteria bio-fertilizers.',
    organic_hi: 'जड़ों में जैव उर्वरक (एज़ोस्पिरिलम व पीएसबी) का प्रयोग करें।',
    chemical_en: 'No chemical fungicide required. Maintain balanced nitrogen-potash split application.',
    chemical_hi: 'किसी रासायनिक फफूंदनाशी की आवश्यकता नहीं है।',
    prevention_en: 'Regularly scout field borders; drain and re-flood fields periodically to aerate root system.',
    prevention_hi: 'खेत की नियमित जांच रखें और समय-समय पर पानी बदलते रहें।',
    is_healthy: true
  },
  'Rice___Brown_spot': {
    name_en: 'Rice Brown Spot (Bipolaris oryzae)',
    name_hi: 'धान का भूरा धब्बा रोग (ब्राउन स्पॉट)',
    crop_en: 'Rice',
    crop_hi: 'धान (चावल)',
    symptoms_en: 'Numerous oval to circular dark brown spots with grey or yellow halos across the leaf blades and glumes.',
    symptoms_hi: 'पत्तियों पर छोटे-बड़े गोल या अंडाकार भूरे रंग के धब्बे जिनके चारों ओर पीला घेरा होता है।',
    cause_en: 'Bipolaris oryzae fungal pathogen, strongly associated with nutrient-deficient or water-stressed soils.',
    cause_hi: 'बाइपोलेरिस ओराइज़ी कवक, जो कमजोर, पोटाश-विहीन अथवा तनावग्रस्त मिट्टी में अधिक लगता है।',
    organic_en: 'Foliar spray with Pseudomonas fluorescens (2 g/L); apply silicon fertilizers (silica @ 2 kg/acre).',
    organic_hi: 'स्यूडोमोनास फ्लोरोसेंस (2 ग्राम/लीटर) या सिलिकॉन खाद का प्रयोग करें।',
    chemical_en: 'Spray Propiconazole 25% EC (1 ml/L) or Tricyclazole 75% WP (0.6 g/L) or Mancozeb 75% WP (2 g/L).',
    chemical_hi: 'प्रोपिकोनाज़ोल 25% EC (1 मिली/लीटर) या ट्राइसाइक्लाजोल का छिड़काव करें।',
    prevention_en: 'Correct soil nutrient deficiencies (apply Zinc & Potassium); avoid prolonged drought stress in paddy.',
    prevention_hi: 'खेत में जिंक और पोटाश की कमी दूर करें और खेत में सूखा न पड़ने दें।',
    is_healthy: false
  },
  'Rice___Blast': {
    name_en: 'Rice Blast',
    name_hi: 'धान का ब्लास्ट (झोंका रोग)',
    crop_en: 'Rice',
    crop_hi: 'धान',
    symptoms_en: 'Spindle-shaped elliptical lesions with gray-white centers and reddish-brown margins on leaf blades.',
    symptoms_hi: 'पत्तियों पर नाव या धुरी के आकार के धब्बे बनते हैं जिनका केंद्र भूरा-सफेद और किनारे लाल-भूरे होते हैं।',
    cause_en: 'Magnaporthe oryzae (Pyricularia oryzae) fungus under high relative humidity (>90%) and 25-28°C.',
    cause_hi: 'मैग्नापोर्थे ओराइजी फंगस, जो 90% से अधिक आर्द्रता और 25-28°C में तेजी से फैलता है।',
    organic_en: 'Foliar spray with Pseudomonas fluorescens @ 5 g/L or fermented cow urine-neem extract.',
    organic_hi: 'स्यूडोमोनास फ्लोरोसेंस (5 ग्राम/लीटर) या पंचगव्य और नीम अर्क का छिड़काव करें।',
    chemical_en: 'Spray Tricyclazole 75% WP @ 0.6 g/L (120 g/acre) or Isoprothiolane 40% EC @ 1.5 ml/L.',
    chemical_hi: 'ट्राइसाइक्लाज़ोल 75% WP (0.6 ग्राम/लीटर) या कासुगामाइसिन का छिड़काव करें।',
    prevention_en: 'Avoid excessive nitrogen fertilization; use certified treated seeds; practice proper water drainage.',
    prevention_hi: 'नाइट्रोजन (यूरिया) का अत्यधिक प्रयोग न करें; प्रमाणित बीजों का ही उपयोग करें।',
    is_healthy: false
  },
  'Rice___Leaf_blast': {
    name_en: 'Rice Leaf Blast (Magnaporthe oryzae)',
    name_hi: 'धान का पत्ती झुलसा / ब्लास्ट रोग',
    crop_en: 'Rice',
    crop_hi: 'धान (चावल)',
    symptoms_en: 'Spindle-shaped (eye-shaped) lesions with greyish-white centers and reddish-brown margins, coalescing into full blight.',
    symptoms_hi: 'पत्तियों पर आंख या नाव के आकार के धब्बे जिनका केंद्र धूसर-सफेद और किनारे भूरे-लाल होते हैं।',
    cause_en: 'Magnaporthe oryzae fungal pathogen, triggered by high relative humidity (>90%) and excess nitrogen.',
    cause_hi: 'मैग्नापोर्थे ओराइज़ी कवक, जो उच्च आर्द्रता और अत्यधिक यूरिया डालने से फैलता है।',
    organic_en: 'Foliar spray with Pseudomonas fluorescens (2 g/L) or Kasugamycin bio-formulation (1.5 ml/L).',
    organic_hi: 'स्यूडोमोनास (2 ग्राम/लीटर) या खट्टी छाछ का छिड़काव करें।',
    chemical_en: 'Spray Tricyclazole 75% WP (Beam @ 0.6 g/L or 120 g/acre) or Isoprothiolane 40% EC (1.5 ml/L).',
    chemical_hi: 'ट्राइसाइक्लाजोल 75% WP (0.6 ग्राम/लीटर) या आइसोप्रोपियोलेन (1.5 मिली/लीटर) का तुरंत स्प्रे करें।',
    prevention_en: 'Avoid split application of nitrogen during peak tillering; maintain adequate standing water.',
    prevention_hi: 'यूरिया का अत्यधिक उपयोग न करें और खेत में पानी का स्तर बनाए रखें।',
    is_healthy: false
  },
  'Soybean___healthy': {
    name_en: 'Healthy Soybean Leaf',
    name_hi: 'स्वस्थ सोयाबीन की पत्ती',
    crop_en: 'Soybean',
    crop_hi: 'सोयाबीन',
    symptoms_en: 'Trifoliate dark green foliage with clean veins, free from rust pustules or yellow mosaic mottling.',
    symptoms_hi: 'सोयाबीन की पत्तियां पूरी तरह स्वस्थ, हरी और रोगमुक्त हैं।',
    cause_en: 'Optimal nodulation and healthy legume canopy development.',
    cause_hi: 'पौधा पूरी तरह स्वस्थ है।',
    organic_en: 'Inoculate seeds with Rhizobium japonicum before sowing for biological nitrogen fixation.',
    organic_hi: 'राइजोबियम कल्चर से बीजोपचार करें।',
    chemical_en: 'No chemical fungicide required.',
    chemical_hi: 'किसी रासायनिक दवा की आवश्यकता नहीं है।',
    prevention_en: 'Maintain weed-free conditions during initial 45 days after sowing.',
    prevention_hi: 'शुरुआती 45 दिनों तक खेत को खरपतवार मुक्त रखें।',
    is_healthy: true
  },
  'Soybean___Rust': {
    name_en: 'Soybean Rust (Phakopsora pachyrhizi)',
    name_hi: 'सोयाबीन का गेरूई / रस्ट रोग',
    crop_en: 'Soybean',
    crop_hi: 'सोयाबीन',
    symptoms_en: 'Tiny chlorotic pinhead spots on upper leaf surfaces corresponding to raised tan/brown pustules on underside, causing rapid defoliation.',
    symptoms_hi: 'पत्ती की निचली सतह पर छोटे भूरे-भूरे उभरे हुए फफोले बनते हैं और समय से पहले पत्ते झड़ जाते हैं।',
    cause_en: 'Phakopsora pachyrhizi fungal pathogen, highly aggressive in warm moist conditions.',
    cause_hi: 'फैकोस्पोरा पैकीराइज़ी कवक, जो गर्म और नम मौसम में बहुत तेजी से फैलता है।',
    organic_en: 'Foliar spray with garlic bulb extract (5%) or Neem oil formulation (3000 ppm @ 3 ml/L).',
    organic_hi: 'लहसुन का अर्क (5%) या नीम का तेल (3 मिली/लीटर) का छिड़काव करें।',
    chemical_en: 'Spray Hexaconazole 5% EC (2 ml/L) or Tebuconazole 25.9% EC (1.5 ml/L) or Propiconazole (1 ml/L).',
    chemical_hi: 'हेक्साकोनाज़ोल 5% EC (2 मिली/लीटर) या टेबुकोनाज़ोल (1.5 मिली/लीटर) का तुरंत छिड़काव करें।',
    prevention_en: 'Early sowing; wider row spacing (45 cm) for canopy aeration; rogue out alternate legume weed hosts.',
    prevention_hi: 'उचित दूरी (45 सेमी) पर बुवाई करें ताकि हवा व धूप का आवागमन बना रहे।',
    is_healthy: false
  },
  'Corn___Common_rust': {
    name_en: 'Corn Common Rust (Puccinia sorghi)',
    name_hi: 'मक्के का सामान्य रतुआ (कॉमन रस्ट)',
    crop_en: 'Corn',
    crop_hi: 'मक्का',
    symptoms_en: 'Oval to elongate cinnamon-brown powdery pustules scattered across both leaf surfaces.',
    symptoms_hi: 'पत्तियों के दोनों तरफ दालचीनी जैसे भूरे रंग के उभरे हुए पाउडर वाले फफोले दिखाई देते हैं।',
    cause_en: 'Puccinia sorghi fungus spread via windborne spores in moderate temperatures (16-25°C).',
    cause_hi: 'पक्सीनिया सोरघाई कवक जो 16-25°C तापमान और नमी में तेजी से फैलता है।',
    organic_en: 'Foliar spray with Trichoderma viride (5 g/L) or fermented sour buttermilk (5%).',
    organic_hi: 'ट्राइकोडर्मा (5 ग्राम/लीटर) या खट्टी छाछ (5%) का छिड़काव करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2 g/L) or Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).',
    chemical_hi: 'मैंकोज़ेब 75% WP (2 ग्राम/लीटर) या एजोक्सीस्ट्रोबिन का छिड़काव करें।',
    prevention_en: 'Plant certified rust-resistant corn hybrids; early sowing to escape peak spore flight.',
    prevention_hi: 'रोग प्रतिरोधी संकर किस्में लगाएं और समय पर बुवाई करें।',
    is_healthy: false
  },
  'Corn___Leaf_blight': {
    name_en: 'Corn Leaf Blight (Northern Blight)',
    name_hi: 'मक्का का पत्ती झुलसा (लीफ ब्लाइट)',
    crop_en: 'Corn / Maize',
    crop_hi: 'मक्का',
    symptoms_en: 'Long elliptical grayish-green or tan lesions (cigar-shaped) expanding parallel to leaf veins.',
    symptoms_hi: 'पत्तियों पर सिगार के आकार के लंबे भूरे-हरे या भूरे धब्बे बनते हैं जो पत्तियों को सुखा देते हैं।',
    cause_en: 'Exserohilum turcicum fungus favored by moderate temperatures (18-27°C) and heavy dew.',
    cause_hi: 'एक्सरोहिलम टर्सिकम कवक, जो 18-27°C तापमान और पत्तियों पर नमी रहने पर फैलता है।',
    organic_en: 'Spray Trichoderma viride foliar wash @ 5 g/L; apply neem oil formulation (3 ml/L).',
    organic_hi: 'ट्राइकोडर्मा विरिडी (5 ग्राम/लीटर) या नीम तेल का छिड़काव करें।',
    chemical_en: 'Foliar spray with Mancozeb 75% WP (2.5 g/L) or Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).',
    chemical_hi: 'मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) या एजोक्सीस्ट्रोबिन का छिड़काव करें।',
    prevention_en: 'Destroy infected crop residues after harvest; follow 2-year crop rotation; plant resistant hybrids.',
    prevention_hi: 'फसल अवशेषों को नष्ट करें, फसल चक्र अपनाएं और रोग प्रतिरोधी संकर बीज लगाएं।',
    is_healthy: false
  },
  'Corn___Northern_leaf_blight': {
    name_en: 'Corn Northern Leaf Blight (Exserohilum turcicum)',
    name_hi: 'मक्के का उत्तरी पत्ती झुलसा',
    crop_en: 'Corn',
    crop_hi: 'मक्का',
    symptoms_en: 'Long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 to 15 cm long) on foliage.',
    symptoms_hi: 'पत्तियों पर सिगार के आकार के लंबे (2.5 से 15 सेमी) धूसर-हरे या भूरे रंग के बड़े धब्बे बनते हैं।',
    cause_en: 'Exserohilum turcicum fungus, favored by moderate temperatures (18-27°C) and heavy dews.',
    cause_hi: 'एक्सरोहिलम टर्सिकम कवक, जो भारी ओस और मध्यम तापमान में तेजी से फैलता है।',
    organic_en: 'Spray Bacillus subtilis bio-fungicide @ 5 ml/L; spray neem oil 5 ml/L.',
    organic_hi: 'बेसिलस सबटिलिस या नीम के तेल (5 मिली/लीटर) का छिड़काव करें।',
    chemical_en: 'Spray Pyraclostrobin 20% WG (1 g/L) or Mancozeb 75% WP (2.5 g/L) at tasseling stage.',
    chemical_hi: 'पायराक्लोस्ट्रोबिन (1 ग्राम/लीटर) या मैंकोज़ेब का छिड़काव करें।',
    prevention_en: 'Deep ploughing to bury corn residues; 2-year crop rotation with non-host crops (soybean/pulses).',
    prevention_hi: 'फसल कटाई के बाद गहरी जुताई करें और सोयाबीन या दलहन के साथ फसल चक्र अपनाएं।',
    is_healthy: false
  },
  'Corn___healthy': {
    name_en: 'Healthy Corn Leaf',
    name_hi: 'स्वस्थ मक्के की पत्ती',
    crop_en: 'Corn',
    crop_hi: 'मक्का',
    symptoms_en: 'Broad arching green leaf blades with strong midrib and clean lamina, free of pustules or cigar lesions.',
    symptoms_hi: 'मक्के की पत्तियां चौड़ी, गहरे हरे रंग की और रोगमुक्त हैं।',
    cause_en: 'Optimal corn vegetative growth and balanced soil nutrition.',
    cause_hi: 'फसल पूरी तरह स्वस्थ है।',
    organic_en: 'Side-dress with farmyard manure or vermicompost prior to tasseling.',
    organic_hi: 'वर्मीकम्पोस्ट या गोबर की खाद डालें।',
    chemical_en: 'No chemical treatment needed.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है।',
    prevention_en: 'Maintain balanced nitrogen and zinc nutrition.',
    prevention_hi: 'जिंक और नाइट्रोजन का संतुलित प्रयोग करें।',
    is_healthy: true
  },
  'Tomato___Early_blight': {
    name_en: 'Tomato Early Blight (Alternaria solani)',
    name_hi: 'टमाटर का अगेती झुलसा (अर्ली ब्लाइट)',
    crop_en: 'Tomato',
    crop_hi: 'टमाटर',
    symptoms_en: 'Concentric rings (target pattern) on lower leaves, surrounded by yellow chlorotic halo.',
    symptoms_hi: 'निचली पत्तियों पर गोल छल्लेदार (टारगेट पैटर्न) भूरे धब्बे जिनके चारों ओर पीला घेरा होता है।',
    cause_en: 'Alternaria solani fungal pathogen, active in warm humid periods.',
    cause_hi: 'अल्टरनेरिया सोलानी कवक संक्रमण।',
    organic_en: 'Spray baking soda solution (5 g/L) or sour buttermilk (5%) + neem oil (3 ml/L).',
    organic_hi: 'बेकिंग सोडा (5 ग्राम/लीटर) या खट्टी छाछ और नीम तेल का स्प्रे करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2.5 g/L) or Chlorothalonil 75% WP (2 g/L).',
    chemical_hi: 'मैंकोज़ेब 75% WP (2.5 ग्राम/लीटर) का छिड़काव करें।',
    prevention_en: 'Prune bottom leaves; stake plants to avoid contact with soil; drip irrigation.',
    prevention_hi: 'पौधों को सहारा (स्टेकिंग) दें और ड्रिप सिंचाई का प्रयोग करें।',
    is_healthy: false
  },
  'Tomato___Late_blight': {
    name_en: 'Tomato Late Blight (Phytophthora infestans)',
    name_hi: 'टमाटर का पछेती झुलसा (लेट ब्लाइट)',
    crop_en: 'Tomato',
    crop_hi: 'टमाटर',
    symptoms_en: 'Dark, water-soaked lesions on leaves and stems, with white fungal growth on leaf undersides in high humidity.',
    symptoms_hi: 'पत्तियों और तनों पर काले, गीले धब्बे और पत्ती की निचली सतह पर सफेद फफूंद।',
    cause_en: 'Phytophthora infestans oomycete.',
    cause_hi: 'फाइटोफ्थोरा इन्फेस्टन्स कवक, जो ठंडे और कोहरे वाले मौसम में फैलता है।',
    organic_en: 'Spray Bordeaux mixture 1% or copper soap before disease progression.',
    organic_hi: 'बोर्डो मिश्रण (1%) का छिड़काव करें।',
    chemical_en: 'Spray Metalaxyl + Mancozeb (2 g/L) or Cymoxanil + Mancozeb (2.5 g/L).',
    chemical_hi: 'रिडोमिल (2 ग्राम/लीटर) या साइमोक्सानिल का छिड़काव करें।',
    prevention_en: 'Avoid planting next to potato fields; remove infected plants immediately.',
    prevention_hi: 'आलू के खेत के पास टमाटर न लगाएं और रोगग्रस्त पौधों को नष्ट करें।',
    is_healthy: false
  },
  'Tomato___healthy': {
    name_en: 'Healthy Tomato Leaf',
    name_hi: 'स्वस्थ टमाटर की पत्ती',
    crop_en: 'Tomato',
    crop_hi: 'टमाटर',
    symptoms_en: 'Crisp green serrated leaflets free of target spots, curling, or white powdery coatings.',
    symptoms_hi: 'टमाटर की पत्तियां पूरी तरह स्वस्थ, हरी और रोगमुक्त हैं।',
    cause_en: 'Healthy solanaceous canopy development.',
    cause_hi: 'फसल पूरी तरह स्वस्थ है।',
    organic_en: 'Apply compost tea or Panchagavya (3%) as foliar tonic.',
    organic_hi: 'पंचगव्य (3%) का पर्णीय छिड़काव करें।',
    chemical_en: 'No chemical fungicide required.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है।',
    prevention_en: 'Mulch around root base to prevent soil splash on leaves.',
    prevention_hi: 'मिट्टी से पत्तों पर छींटे रोकने के लिए मल्चिंग करें।',
    is_healthy: true
  },
  'Apple___Scab': {
    name_en: 'Apple Scab (Venturia inaequalis)',
    name_hi: 'सेब का स्कैब रोग',
    crop_en: 'Apple',
    crop_hi: 'सेब',
    symptoms_en: 'Olive-green to velvety brown-black spots on leaves and fruit, causing leaf distortion and premature drop.',
    symptoms_hi: 'पत्तियों और फलों पर जैतून जैसे हरे या मखमली काले धब्बे जो बाद में पपड़ीदार हो जाते हैं।',
    cause_en: 'Venturia inaequalis fungus, spread by spring rains.',
    cause_hi: 'वेन्चुरिया इनेकैलिस कवक, जो वसंत ऋतु की बारिश में फैलता है।',
    organic_en: 'Spray wettable sulphur (3 g/L) or potassium bicarbonate (4 g/L).',
    organic_hi: 'सल्फर (3 ग्राम/लीटर) का छिड़काव करें।',
    chemical_en: 'Spray Captan 50% WP (2 g/L) or Difenoconazole 25% EC (0.5 ml/L).',
    chemical_hi: 'कैप्टान (2 ग्राम/लीटर) या डाइफेनोकोनाज़ोल का छिड़काव करें।',
    prevention_en: 'Rake and burn fallen leaves in winter; prune trees for light and air circulation.',
    prevention_hi: 'गिरे हुए पत्तों को नष्ट करें और पेड़ों की उचित छंटाई करें।',
    is_healthy: false
  },
  'Apple___healthy': {
    name_en: 'Healthy Apple Leaf',
    name_hi: 'स्वस्थ सेब की पत्ती',
    crop_en: 'Apple',
    crop_hi: 'सेब',
    symptoms_en: 'Vibrant green ovate leaves with serrated margins, free of olive scab lesions or powdery mildew.',
    symptoms_hi: 'सेब की पत्तियां पूरी तरह स्वस्थ और हरी हैं।',
    cause_en: 'Healthy orchard canopy management.',
    cause_hi: 'फसल पूरी तरह स्वस्थ है।',
    organic_en: 'Apply bio-stimulants and foliar micronutrient spray.',
    organic_hi: 'पोषक तत्वों का छिड़काव करें।',
    chemical_en: 'No chemical intervention needed.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है।',
    prevention_en: 'Monitor early spring shoot growth.',
    prevention_hi: 'नियमित निगरानी रखें।',
    is_healthy: true
  },
  'Grape___Black_rot': {
    name_en: 'Grape Black Rot (Guignardia bidwellii)',
    name_hi: 'अंगूर का ब्लैक रॉट रोग',
    crop_en: 'Grape',
    crop_hi: 'अंगूर',
    symptoms_en: 'Reddish-brown circular spots with dark margins on leaves with tiny black pycnidia; shriveled black mummified berries.',
    symptoms_hi: 'पत्तियों पर लाल-भूरे गोल धब्बे और अंगूर के दानों का सिकुड़कर काला पड़ जाना।',
    cause_en: 'Guignardia bidwellii fungal pathogen.',
    cause_hi: 'गिगनार्डिया बिडवेलाई कवक संक्रमण।',
    organic_en: 'Foliar spray with Copper Hydroxide or Bordeaux mixture (1%).',
    organic_hi: 'बोर्डो मिश्रण (1%) या कॉपर का छिड़काव करें।',
    chemical_en: 'Spray Mancozeb 75% WP (2 g/L) or Myclobutanil 10% WP (1 g/L).',
    chemical_hi: 'माइक्लोबुटानिल (1 ग्राम/लीटर) या मैंकोज़ेब का छिड़काव करें।',
    prevention_en: 'Remove mummified berries from vines; maintain canopy training for rapid drying.',
    prevention_hi: 'सूखे हुए रोगग्रस्त अंगूरों को बेल से हटाएं और धूप-हवा का प्रबंधन रखें।',
    is_healthy: false
  },
  'Grape___healthy': {
    name_en: 'Healthy Grape Leaf',
    name_hi: 'स्वस्थ अंगूर की पत्ती',
    crop_en: 'Grape',
    crop_hi: 'अंगूर',
    symptoms_en: 'Heart-shaped lobed deep green foliage with clean veins and healthy tendrils.',
    symptoms_hi: 'अंगूर की पत्तियां पूरी तरह स्वस्थ, हरी और रोगमुक्त हैं।',
    cause_en: 'Healthy vineyard management.',
    cause_hi: 'फसल पूरी तरह स्वस्थ है।',
    organic_en: 'Apply seaweed fertilizer spray during flowering.',
    organic_hi: 'फूल आते समय जैविक अर्क का छिड़काव करें।',
    chemical_en: 'No chemical intervention required.',
    chemical_hi: 'किसी दवा की आवश्यकता नहीं है।',
    prevention_en: 'Ensure proper trellising and cane pruning.',
    prevention_hi: 'बेलों की उचित छंटाई रखें।',
    is_healthy: true
  },
  'Not_A_Leaf': {
    name_en: 'Not A Plant Leaf',
    name_hi: 'कोई पौधे की पत्ती नहीं',
    crop_en: 'Unknown',
    crop_hi: 'अज्ञात',
    symptoms_en: 'Out-of-domain object or non-botanical entity detected.',
    symptoms_hi: 'अपलोड की गई फोटो में कोई मान्यता प्राप्त पौधे की पत्ती नहीं पाई गई।',
    cause_en: 'The uploaded image appears to be a person, vehicle, building, animal, or non-crop object.',
    cause_hi: 'अपलोड की गई तस्वीर किसी व्यक्ति, वाहन, भवन या गैर-कृषि वस्तु की प्रतीत होती है।',
    organic_en: 'Please upload a clear, focused photograph of a plant or crop leaf.',
    organic_hi: 'कृपया किसी पौधे या फसल की पत्ती की स्पष्ट फोटो अपलोड करें।',
    chemical_en: 'N/A',
    chemical_hi: 'लागू नहीं',
    prevention_en: 'N/A',
    prevention_hi: 'लागू नहीं',
    is_healthy: false
  }
};

/**
 * Global Translation Helper Function
 * @param {string} key - translation key
 * @returns {string} - translated string in current language
 */
function t(key) {
  const lang = currentLanguage || 'en';
  if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key] !== undefined) {
    return TRANSLATIONS[lang][key];
  }
  if (TRANSLATIONS['en'] && TRANSLATIONS['en'][key] !== undefined) {
    return TRANSLATIONS['en'][key];
  }
  return key;
}

/**
 * Translate Crop Name
 * @param {string} cropKey - crop key/name
 * @returns {string} - translated crop name
 */
function tCrop(cropKey) {
  if (!cropKey) return t('crop');
  const k = cropKey.toLowerCase().trim();
  const lang = currentLanguage || 'en';
  if (CROP_TRANSLATIONS[k] && CROP_TRANSLATIONS[k][lang]) {
    return CROP_TRANSLATIONS[k][lang];
  }
  return cropKey;
}

/**
 * Translate Disease Information
 * @param {string} classId - model class identifier (e.g. Wheat___Yellow_rust)
 * @returns {object} - localized disease details
 */
function tDisease(classId) {
  const lang = currentLanguage || 'en';
  const entry = DISEASE_TRANSLATIONS[classId];

  if (!entry) {
    // Fallback: humanize classId
    const parts = (classId || '').split('___');
    const crop = parts[0] || 'Crop';
    const disease = (parts[1] || 'Unknown').replace(/_/g, ' ');
    return {
      disease_name: disease,
      crop_name: crop,
      symptoms: lang === 'hi' ? 'लक्षणों की जांच की जा रही है।' : 'Observed symptoms under diagnostic review.',
      cause: lang === 'hi' ? 'कवक या जीवाणु संक्रमण।' : 'Fungal or bacterial pathogen.',
      organic_remedy: lang === 'hi' ? 'नीम का तेल (3-5 मिली/लीटर) या ट्राइकोडर्मा का छिड़काव करें।' : 'Spray neem oil (3-5 ml/L) or Trichoderma viride.',
      chemical_treatment: lang === 'hi' ? 'सटीक रासायनिक दवा हेतु कृषि विशेषज्ञ से परामर्श करें।' : 'Consult agricultural extension officer for specific chemical fungicide.',
      prevention: lang === 'hi' ? 'खेत में स्वच्छता बनाए रखें और प्रमाणित बीज का उपयोग करें।' : 'Maintain field sanitation and use certified disease-free seeds.',
      is_healthy: classId && classId.toLowerCase().includes('healthy')
    };
  }

  return {
    disease_name: lang === 'hi' ? entry.name_hi : entry.name_en,
    crop_name: lang === 'hi' ? entry.crop_hi : entry.crop_en,
    symptoms: lang === 'hi' ? entry.symptoms_hi : entry.symptoms_en,
    cause: lang === 'hi' ? entry.cause_hi : entry.cause_en,
    organic_remedy: lang === 'hi' ? entry.organic_hi : entry.organic_en,
    chemical_treatment: lang === 'hi' ? entry.chemical_hi : entry.chemical_en,
    prevention: lang === 'hi' ? entry.prevention_hi : entry.prevention_en,
    is_healthy: entry.is_healthy
  };
}

/**
 * Set Global Language
 * @param {string} lang - 'en' or 'hi'
 */
function setLanguage(lang) {
  currentLanguage = (lang === 'hi') ? 'hi' : 'en';
  localStorage.setItem('sap_language', currentLanguage);
  localStorage.setItem('sap_lang', currentLanguage);

  if (typeof state !== 'undefined') {
    state.lang = currentLanguage;
  }

  applyTranslations();
}

/**
 * Toggle Global Language
 */
function toggleLanguage() {
  const nextLang = (currentLanguage === 'en') ? 'hi' : 'en';
  setLanguage(nextLang);
}

/**
 * Apply Translations Across Entire DOM & State
 */
function applyTranslations() {
  const isHi = (currentLanguage === 'hi');

  // 1. Update Global Toggle Button Text
  const langBtn = document.getElementById('langBtnText');
  if (langBtn) {
    langBtn.textContent = isHi ? 'English' : 'हिंदी';
  }
  const globalToggle = document.getElementById('globalLangToggleBtn');
  if (globalToggle) {
    globalToggle.title = isHi ? 'Switch to English' : 'हिंदी में बदलें';
  }

  // 2. Translate Elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translated = t(key);
    if (translated && translated !== key) {
      el.textContent = translated;
    }
  });

  // 3. Translate Elements with legacy data-lang-en and data-lang-hi
  document.querySelectorAll('[data-lang-en]').forEach(el => {
    const text = isHi ? el.getAttribute('data-lang-hi') : el.getAttribute('data-lang-en');
    if (text) {
      el.textContent = text;
    }
  });

  // 4. Translate Input Placeholders with data-i18n-placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const translated = t(key);
    if (translated && translated !== key) {
      el.placeholder = translated;
    }
  });

  // 5. Update specific inputs
  const chatInput = document.getElementById('chatMessageInput');
  if (chatInput) {
    chatInput.placeholder = t('chatPlaceholder');
  }

  const pinInput = document.getElementById('pincodeInput');
  if (pinInput) {
    pinInput.placeholder = isHi ? 'पिन कोड या शहर (उदा. 208001, Kanpur)' : 'Enter PIN or City (e.g. 208001, Kanpur)';
  }

  const fertSymptomInput = document.getElementById('fertSymptomsInput');
  if (fertSymptomInput) {
    fertSymptomInput.placeholder = isHi
      ? 'लक्षण या सवाल लिखें (उदा. निचली पत्तियां पीली हो रही हैं, क्या यूरिया डालें?)'
      : 'e.g. Lower leaves are turning pale yellow, should I spray urea or NPK?';
  }

  const mandiSearchInput = document.getElementById('mandiSearchInput');
  if (mandiSearchInput) {
    mandiSearchInput.placeholder = t('searchMandiPlaceholder');
  }

  // 6. Update All Standardized Crop Dropdowns Across Application
  const isHiMode = (typeof currentLanguage !== 'undefined' ? currentLanguage : state.lang) === 'hi';
  
  const standardizedOptions = [
    { val: 'Wheat', en: '🌾 Wheat (Yellow Rust / Healthy)', hi: '🌾 गेहूं (पीला रतुआ / स्वस्थ)' },
    { val: 'Cotton', en: '🌱 Cotton (Bacterial Blight / Healthy)', hi: '🌱 कपास (जीवाणु झुलसा / स्वस्थ)' },
    { val: 'Sugarcane', en: '🎋 Sugarcane (Red Rot / Healthy)', hi: '🎋 गन्ना (लाल सड़न / स्वस्थ)' },
    { val: 'Potato', en: '🥔 Potato (Early Blight / Late Blight / Healthy)', hi: '🥔 आलू (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
    { val: 'Rice', en: '🌾 Rice (Blast / Brown Spot / Healthy)', hi: '🌾 धान (ब्लास्ट / भूरा धब्बा / स्वस्थ)' },
    { val: 'Soybean', en: '🌿 Soybean (Rust / Healthy)', hi: '🌿 सोयाबीन (रस्ट / स्वस्थ)' },
    { val: 'Tomato', en: '🍅 Tomato (Early Blight / Late Blight / Healthy)', hi: '🍅 टमाटर (अगेती झुलसा / पछेती झुलसा / स्वस्थ)' },
    { val: 'Corn', en: '🌽 Corn / Maize (Common Rust / Leaf Blight / Healthy)', hi: '🌽 मक्का (कॉमन रस्ट / लीफ ब्लाइट / स्वस्थ)' },
    { val: 'Apple', en: '🍎 Apple (Scab / Healthy)', hi: '🍎 सेब (स्कैब / स्वस्थ)' },
    { val: 'Grape', en: '🍇 Grape (Black Rot / Healthy)', hi: '🍇 अंगूर (ब्लैक रॉट / स्वस्थ)' }
  ];

  const autoOption = { val: 'Auto', en: '🔍 Auto Detect (General)', hi: '🔍 स्वचालित पहचान (सामान्य)' };

  // Helper to re-render a select maintaining its selected value
  function populateSelect(selectId, includeAuto) {
    const el = document.getElementById(selectId);
    if (!el) return;
    const curVal = el.value;
    const list = includeAuto ? [autoOption, ...standardizedOptions] : standardizedOptions;
    el.innerHTML = list.map(opt => `<option value="${opt.val}">${isHiMode ? opt.hi : opt.en}</option>`).join('');
    if (curVal && (list.some(o => o.val === curVal))) {
      el.value = curVal;
    }
  }

  populateSelect('diseaseCropSelect', true);
  populateSelect('headerCropSelect', false);
  populateSelect('fertCropSelect', false);
  populateSelect('ctxCropSelect', false);
  populateSelect('modalCropSelect', false);

  // 7. Re-render active Diagnostic Report if visible
  if (window.lastDiagnosisResult && typeof renderDiseaseResults === 'function') {
    renderDiseaseResults(window.lastDiagnosisResult);
  }

  // 8. Re-render Weather UI if loaded
  if (typeof state !== 'undefined' && state.weatherData && typeof renderWeatherUI === 'function') {
    renderWeatherUI(state.weatherData);
  }

  // 9. Sync Farmer & Fertilizer contexts
  if (typeof syncFarmerContext === 'function') syncFarmerContext();
  if (typeof syncFertilizerContext === 'function') syncFertilizerContext();
  if (typeof updateLocationHeroUI === 'function') updateLocationHeroUI();
  if (typeof updateDiseaseModelBadge === 'function') updateDiseaseModelBadge();
  if (typeof renderChatSuggestedChips === 'function') renderChatSuggestedChips();
}

// Automatically apply translations on DOM load
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTranslations);
  } else {
    setTimeout(applyTranslations, 10);
  }
}
