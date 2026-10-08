/**
 * Smart Agriculture Platform (SAP) — Local Indian Agricultural Location Database
 * 100% On-Device Offline Search (No Geocoding API required)
 * Supports: City, District, State, State Code, and 6-Digit PIN Codes
 */

const INDIAN_LOCATIONS = {
  "kanpur": {
    "key": "kanpur",
    "city": "Kanpur",
    "district": "Kanpur Nagar",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "208001",
    "lat": 26.4499,
    "lon": 80.3319,
    "pincodes": ["208001", "208002", "208003", "208004", "208005", "208006", "208007", "208008", "208010", "208012", "208017", "208020", "208024", "208025", "208027"],
    "aliases": ["kanpur", "kanpur nagar", "kanpur dehat", "cawnpore", "कानपुर"]
  },
  "bhopal": {
    "key": "bhopal",
    "city": "Bhopal",
    "district": "Bhopal",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "462001",
    "lat": 23.2599,
    "lon": 77.4126,
    "pincodes": ["462001", "462002", "462003", "462010", "462011", "462016", "462021", "462022", "462023", "462026", "462030", "462038", "462042"],
    "aliases": ["bhopal", "भोपाल"]
  },
  "indore": {
    "key": "indore",
    "city": "Indore",
    "district": "Indore",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "452001",
    "lat": 22.7196,
    "lon": 75.8577,
    "pincodes": ["452001", "452002", "452003", "452005", "452006", "452007", "452008", "452009", "452010", "452012", "452016", "452018", "452020"],
    "aliases": ["indore", "indur", "इंदौर"]
  },
  "lucknow": {
    "key": "lucknow",
    "city": "Lucknow",
    "district": "Lucknow",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "226001",
    "lat": 26.8467,
    "lon": 80.9462,
    "pincodes": ["226001", "226002", "226003", "226004", "226005", "226006", "226010", "226012", "226016", "226020", "226021", "226022", "226024"],
    "aliases": ["lucknow", "लखनौ", "लखनऊ"]
  },
  "ludhiana": {
    "key": "ludhiana",
    "city": "Ludhiana",
    "district": "Ludhiana",
    "state": "Punjab",
    "state_code": "PB",
    "pincode": "141001",
    "lat": 30.9010,
    "lon": 75.8573,
    "pincodes": ["141001", "141002", "141003", "141004", "141007", "141008", "141010", "141012"],
    "aliases": ["ludhiana", "लुधियाना"]
  },
  "patna": {
    "key": "patna",
    "city": "Patna",
    "district": "Patna",
    "state": "Bihar",
    "state_code": "BR",
    "pincode": "800001",
    "lat": 25.5941,
    "lon": 85.1376,
    "pincodes": ["800001", "800002", "800003", "800004", "800006", "800007", "800008", "800013", "800020"],
    "aliases": ["patna", "patliputra", "पटना"]
  },
  "nashik": {
    "key": "nashik",
    "city": "Nashik",
    "district": "Nashik",
    "state": "Maharashtra",
    "state_code": "MH",
    "pincode": "422001",
    "lat": 19.9975,
    "lon": 73.7898,
    "pincodes": ["422001", "422002", "422003", "422005", "422007", "422009", "422010", "422011", "422013"],
    "aliases": ["nashik", "nasik", "नाशिक", "नासिक"]
  },
  "varanasi": {
    "key": "varanasi",
    "city": "Varanasi",
    "district": "Varanasi",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "221001",
    "lat": 25.3176,
    "lon": 82.9739,
    "pincodes": ["221001", "221002", "221005", "221008", "221010"],
    "aliases": ["varanasi", "banaras", "kashi", "वाराणसी", "बनारस"]
  },
  "meerut": {
    "key": "meerut",
    "city": "Meerut",
    "district": "Meerut",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "250001",
    "lat": 28.9845,
    "lon": 77.7064,
    "pincodes": ["250001", "250002", "250003", "250004", "250005"],
    "aliases": ["meerut", "मेरठ"]
  },
  "agra": {
    "key": "agra",
    "city": "Agra",
    "district": "Agra",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "282001",
    "lat": 27.1767,
    "lon": 78.0081,
    "pincodes": ["282001", "282002", "282003", "282004", "282005"],
    "aliases": ["agra", "आगरा"]
  },
  "prayagraj": {
    "key": "prayagraj",
    "city": "Prayagraj",
    "district": "Prayagraj",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "211001",
    "lat": 25.4358,
    "lon": 81.8463,
    "pincodes": ["211001", "211002", "211003", "211004", "211005", "211006"],
    "aliases": ["prayagraj", "allahabad", "प्रयागराज", "इलाहाबाद"]
  },
  "gorakhpur": {
    "key": "gorakhpur",
    "city": "Gorakhpur",
    "district": "Gorakhpur",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "273001",
    "lat": 26.7606,
    "lon": 83.3732,
    "pincodes": ["273001", "273002", "273003", "273004", "273005"],
    "aliases": ["gorakhpur", "गोरखपुर"]
  },
  "bareilly": {
    "key": "bareilly",
    "city": "Bareilly",
    "district": "Bareilly",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "243001",
    "lat": 28.3670,
    "lon": 79.4304,
    "pincodes": ["243001", "243002", "243003", "243004"],
    "aliases": ["bareilly", "बरेली"]
  },
  "aligarh": {
    "key": "aligarh",
    "city": "Aligarh",
    "district": "Aligarh",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "202001",
    "lat": 27.8974,
    "lon": 78.0880,
    "pincodes": ["202001", "202002"],
    "aliases": ["aligarh", "अलीगढ़"]
  },
  "jhansi": {
    "key": "jhansi",
    "city": "Jhansi",
    "district": "Jhansi",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "284001",
    "lat": 25.4484,
    "lon": 78.5685,
    "pincodes": ["284001", "284002", "284003"],
    "aliases": ["jhansi", "झांसी"]
  },
  "muzaffarnagar": {
    "key": "muzaffarnagar",
    "city": "Muzaffarnagar",
    "district": "Muzaffarnagar",
    "state": "Uttar Pradesh",
    "state_code": "UP",
    "pincode": "251001",
    "lat": 29.4727,
    "lon": 77.7085,
    "pincodes": ["251001", "251002"],
    "aliases": ["muzaffarnagar", "मुजफ्फरनगर"]
  },
  "jabalpur": {
    "key": "jabalpur",
    "city": "Jabalpur",
    "district": "Jabalpur",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "482001",
    "lat": 23.1815,
    "lon": 79.9864,
    "pincodes": ["482001", "482002", "482003", "482004"],
    "aliases": ["jabalpur", "जबलपुर"]
  },
  "gwalior": {
    "key": "gwalior",
    "city": "Gwalior",
    "district": "Gwalior",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "474001",
    "lat": 26.2183,
    "lon": 78.1828,
    "pincodes": ["474001", "474002", "474003", "474004"],
    "aliases": ["gwalior", "ग्वालियर"]
  },
  "ujjain": {
    "key": "ujjain",
    "city": "Ujjain",
    "district": "Ujjain",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "456001",
    "lat": 23.1765,
    "lon": 75.7885,
    "pincodes": ["456001", "456006", "456010"],
    "aliases": ["ujjain", "उज्जैन"]
  },
  "sagar": {
    "key": "sagar",
    "city": "Sagar",
    "district": "Sagar",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "470001",
    "lat": 23.8388,
    "lon": 78.7378,
    "pincodes": ["470001", "470002", "470003"],
    "aliases": ["sagar", "सागर"]
  },
  "vidisha": {
    "key": "vidisha",
    "city": "Vidisha",
    "district": "Vidisha",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "464001",
    "lat": 23.5251,
    "lon": 77.8081,
    "pincodes": ["464001"],
    "aliases": ["vidisha", "विदिशा"]
  },
  "sehore": {
    "key": "sehore",
    "city": "Sehore",
    "district": "Sehore",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "466001",
    "lat": 23.2031,
    "lon": 77.0844,
    "pincodes": ["466001"],
    "aliases": ["sehore", "सीहोर"]
  },
  "hoshangabad": {
    "key": "hoshangabad",
    "city": "Hoshangabad",
    "district": "Narmadapuram",
    "state": "Madhya Pradesh",
    "state_code": "MP",
    "pincode": "461001",
    "lat": 22.7519,
    "lon": 77.7289,
    "pincodes": ["461001"],
    "aliases": ["hoshangabad", "narmadapuram", "होशंगाबाद", "नर्मदापुरम"]
  },
  "amritsar": {
    "key": "amritsar",
    "city": "Amritsar",
    "district": "Amritsar",
    "state": "Punjab",
    "state_code": "PB",
    "pincode": "143001",
    "lat": 31.6340,
    "lon": 74.8723,
    "pincodes": ["143001", "143002", "143006"],
    "aliases": ["amritsar", "अमृतसर"]
  },
  "jalandhar": {
    "key": "jalandhar",
    "city": "Jalandhar",
    "district": "Jalandhar",
    "state": "Punjab",
    "state_code": "PB",
    "pincode": "144001",
    "lat": 31.3260,
    "lon": 75.5762,
    "pincodes": ["144001", "144002", "144003"],
    "aliases": ["jalandhar", "जालंधर"]
  },
  "bathinda": {
    "key": "bathinda",
    "city": "Bathinda",
    "district": "Bathinda",
    "state": "Punjab",
    "state_code": "PB",
    "pincode": "151001",
    "lat": 30.2110,
    "lon": 74.9455,
    "pincodes": ["151001", "151002"],
    "aliases": ["bathinda", "bhatinda", "बठिंडा"]
  },
  "patiala": {
    "key": "patiala",
    "city": "Patiala",
    "district": "Patiala",
    "state": "Punjab",
    "state_code": "PB",
    "pincode": "147001",
    "lat": 30.3398,
    "lon": 76.3869,
    "pincodes": ["147001", "147002"],
    "aliases": ["patiala", "पटियाला"]
  },
  "karnal": {
    "key": "karnal",
    "city": "Karnal",
    "district": "Karnal",
    "state": "Haryana",
    "state_code": "HR",
    "pincode": "132001",
    "lat": 29.6857,
    "lon": 76.9905,
    "pincodes": ["132001", "132002"],
    "aliases": ["karnal", "करनाल"]
  },
  "hisar": {
    "key": "hisar",
    "city": "Hisar",
    "district": "Hisar",
    "state": "Haryana",
    "state_code": "HR",
    "pincode": "125001",
    "lat": 29.1492,
    "lon": 75.7217,
    "pincodes": ["125001", "125004"],
    "aliases": ["hisar", "हिसार"]
  },
  "rohtak": {
    "key": "rohtak",
    "city": "Rohtak",
    "district": "Rohtak",
    "state": "Haryana",
    "state_code": "HR",
    "pincode": "124001",
    "lat": 28.8955,
    "lon": 76.6066,
    "pincodes": ["124001"],
    "aliases": ["rohtak", "रोहतक"]
  },
  "ambala": {
    "key": "ambala",
    "city": "Ambala",
    "district": "Ambala",
    "state": "Haryana",
    "state_code": "HR",
    "pincode": "134003",
    "lat": 30.3782,
    "lon": 76.7767,
    "pincodes": ["134003", "133001"],
    "aliases": ["ambala", "अंबाला"]
  },
  "jaipur": {
    "key": "jaipur",
    "city": "Jaipur",
    "district": "Jaipur",
    "state": "Rajasthan",
    "state_code": "RJ",
    "pincode": "302001",
    "lat": 26.9124,
    "lon": 75.7873,
    "pincodes": ["302001", "302002", "302003", "302004", "302006", "302012"],
    "aliases": ["jaipur", "जयपुर"]
  },
  "jodhpur": {
    "key": "jodhpur",
    "city": "Jodhpur",
    "district": "Jodhpur",
    "state": "Rajasthan",
    "state_code": "RJ",
    "pincode": "342001",
    "lat": 26.2389,
    "lon": 73.0243,
    "pincodes": ["342001", "342002", "342003"],
    "aliases": ["jodhpur", "जोधपुर"]
  },
  "kota": {
    "key": "kota",
    "city": "Kota",
    "district": "Kota",
    "state": "Rajasthan",
    "state_code": "RJ",
    "pincode": "324001",
    "lat": 25.2138,
    "lon": 75.8648,
    "pincodes": ["324001", "324002", "324005"],
    "aliases": ["kota", "कोटा"]
  },
  "ganganagar": {
    "key": "ganganagar",
    "city": "Sri Ganganagar",
    "district": "Sri Ganganagar",
    "state": "Rajasthan",
    "state_code": "RJ",
    "pincode": "335001",
    "lat": 29.9094,
    "lon": 73.8799,
    "pincodes": ["335001"],
    "aliases": ["ganganagar", "sri ganganagar", "गंगानगर", "श्री गंगानगर"]
  },
  "gaya": {
    "key": "gaya",
    "city": "Gaya",
    "district": "Gaya",
    "state": "Bihar",
    "state_code": "BR",
    "pincode": "823001",
    "lat": 24.7914,
    "lon": 85.0002,
    "pincodes": ["823001", "823002"],
    "aliases": ["gaya", "गया"]
  },
  "muzaffarpur": {
    "key": "muzaffarpur",
    "city": "Muzaffarpur",
    "district": "Muzaffarpur",
    "state": "Bihar",
    "state_code": "BR",
    "pincode": "842001",
    "lat": 26.1209,
    "lon": 85.3647,
    "pincodes": ["842001", "842002"],
    "aliases": ["muzaffarpur", "मुजफ्फरपुर"]
  },
  "pune": {
    "key": "pune",
    "city": "Pune",
    "district": "Pune",
    "state": "Maharashtra",
    "state_code": "MH",
    "pincode": "411001",
    "lat": 18.5204,
    "lon": 73.8567,
    "pincodes": ["411001", "411002", "411004", "411005", "411014", "411038"],
    "aliases": ["pune", "poona", "पुणे"]
  },
  "nagpur": {
    "key": "nagpur",
    "city": "Nagpur",
    "district": "Nagpur",
    "state": "Maharashtra",
    "state_code": "MH",
    "pincode": "440001",
    "lat": 21.1458,
    "lon": 79.0882,
    "pincodes": ["440001", "440002", "440010", "440012"],
    "aliases": ["nagpur", "नागपुर"]
  },
  "chhatrapati_sambhajinagar": {
    "key": "chhatrapati_sambhajinagar",
    "city": "Chhatrapati Sambhajinagar",
    "district": "Chhatrapati Sambhajinagar",
    "state": "Maharashtra",
    "state_code": "MH",
    "pincode": "431001",
    "lat": 19.8762,
    "lon": 75.3433,
    "pincodes": ["431001", "431002", "431003", "431005"],
    "aliases": ["aurangabad", "chhatrapati sambhajinagar", "sambhajinagar", "औरंगाबाद", "छत्रपती संभाजीनगर"]
  },
  "ahmedabad": {
    "key": "ahmedabad",
    "city": "Ahmedabad",
    "district": "Ahmedabad",
    "state": "Gujarat",
    "state_code": "GJ",
    "pincode": "380001",
    "lat": 23.0225,
    "lon": 72.5714,
    "pincodes": ["380001", "380002", "380006", "380009", "380015"],
    "aliases": ["ahmedabad", "amdavad", "अहमदाबाद"]
  },
  "surat": {
    "key": "surat",
    "city": "Surat",
    "district": "Surat",
    "state": "Gujarat",
    "state_code": "GJ",
    "pincode": "395001",
    "lat": 21.1702,
    "lon": 72.8311,
    "pincodes": ["395001", "395002", "395003"],
    "aliases": ["surat", "सूरत"]
  },
  "rajkot": {
    "key": "rajkot",
    "city": "Rajkot",
    "district": "Rajkot",
    "state": "Gujarat",
    "state_code": "GJ",
    "pincode": "360001",
    "lat": 22.3039,
    "lon": 70.8022,
    "pincodes": ["360001", "360002", "360004"],
    "aliases": ["rajkot", "राजकोट"]
  },
  "bengaluru": {
    "key": "bengaluru",
    "city": "Bengaluru",
    "district": "Bengaluru Urban",
    "state": "Karnataka",
    "state_code": "KA",
    "pincode": "560001",
    "lat": 12.9716,
    "lon": 77.5946,
    "pincodes": ["560001", "560002", "560003", "560004", "560025"],
    "aliases": ["bengaluru", "bangalore", "बेंगलुरु", "बैंगलोर"]
  },
  "hyderabad": {
    "key": "hyderabad",
    "city": "Hyderabad",
    "district": "Hyderabad",
    "state": "Telangana",
    "state_code": "TS",
    "pincode": "500001",
    "lat": 17.3850,
    "lon": 78.4867,
    "pincodes": ["500001", "500002", "500003", "500004"],
    "aliases": ["hyderabad", "हैदराबाद"]
  },
  "vijayawada": {
    "key": "vijayawada",
    "city": "Vijayawada",
    "district": "NTR",
    "state": "Andhra Pradesh",
    "state_code": "AP",
    "pincode": "520001",
    "lat": 16.5062,
    "lon": 80.6480,
    "pincodes": ["520001", "520002"],
    "aliases": ["vijayawada", "विजयवाड़ा"]
  },
  "coimbatore": {
    "key": "coimbatore",
    "city": "Coimbatore",
    "district": "Coimbatore",
    "state": "Tamil Nadu",
    "state_code": "TN",
    "pincode": "641001",
    "lat": 11.0168,
    "lon": 76.9558,
    "pincodes": ["641001", "641002"],
    "aliases": ["coimbatore", "कोयंबटूर"]
  },
  "kolkata": {
    "key": "kolkata",
    "city": "Kolkata",
    "district": "Kolkata",
    "state": "West Bengal",
    "state_code": "WB",
    "pincode": "700001",
    "lat": 22.5726,
    "lon": 88.3639,
    "pincodes": ["700001", "700002", "700006"],
    "aliases": ["kolkata", "calcutta", "कोलकाता"]
  },
  "raipur": {
    "key": "raipur",
    "city": "Raipur",
    "district": "Raipur",
    "state": "Chhattisgarh",
    "state_code": "CG",
    "pincode": "492001",
    "lat": 21.2514,
    "lon": 81.6296,
    "pincodes": ["492001", "492002"],
    "aliases": ["raipur", "रायपुर"]
  },
  "ranchi": {
    "key": "ranchi",
    "city": "Ranchi",
    "district": "Ranchi",
    "state": "Jharkhand",
    "state_code": "JH",
    "pincode": "834001",
    "lat": 23.3441,
    "lon": 85.3096,
    "pincodes": ["834001", "834002"],
    "aliases": ["ranchi", "रांची"]
  },
  "bhubaneswar": {
    "key": "bhubaneswar",
    "city": "Bhubaneswar",
    "district": "Khordha",
    "state": "Odisha",
    "state_code": "OD",
    "pincode": "751001",
    "lat": 20.2961,
    "lon": 85.8245,
    "pincodes": ["751001", "751002"],
    "aliases": ["bhubaneswar", "भुवनेश्वर"]
  },
  "shimla": {
    "key": "shimla",
    "city": "Shimla",
    "district": "Shimla",
    "state": "Himachal Pradesh",
    "state_code": "HP",
    "pincode": "171001",
    "lat": 31.1048,
    "lon": 77.1734,
    "pincodes": ["171001", "171002"],
    "aliases": ["shimla", "शिमला"]
  },
  "dehradun": {
    "key": "dehradun",
    "city": "Dehradun",
    "district": "Dehradun",
    "state": "Uttarakhand",
    "state_code": "UK",
    "pincode": "248001",
    "lat": 30.3165,
    "lon": 78.0322,
    "pincodes": ["248001", "248002"],
    "aliases": ["dehradun", "देहरादून"]
  },
  "delhi": {
    "key": "delhi",
    "city": "Delhi",
    "district": "New Delhi",
    "state": "Delhi",
    "state_code": "DL",
    "pincode": "110001",
    "lat": 28.6139,
    "lon": 77.2090,
    "pincodes": ["110001", "110002", "110003", "110005"],
    "aliases": ["delhi", "new delhi", "दिल्ली", "नई दिल्ली"]
  }
};

/**
 * Searches local Indian location database case-insensitively.
 * Supports: City name, District name, State name, State abbreviation (UP, MP, MH, PB, BR, etc.), and PIN codes.
 */
function searchIndianLocations(rawQuery) {
  if (!rawQuery) return [];
  const query = String(rawQuery).toLowerCase().trim();
  if (!query) return [];

  // Remove commas, punctuation, and extra whitespace
  const cleanQuery = query.replace(/[,()\/\\-]/g, ' ').replace(/\s+/g, ' ').trim();
  const tokens = cleanQuery.split(' ').filter(Boolean);

  const results = [];
  const seenKeys = new Set();

  // If query is pure digits (PIN code search)
  const isPin = /^\d{3,6}$/.test(cleanQuery);

  for (const [key, loc] of Object.entries(INDIAN_LOCATIONS)) {
    let score = 0;
    const cLower = loc.city.toLowerCase();
    const dLower = loc.district.toLowerCase();
    const sLower = loc.state.toLowerCase();
    const scLower = loc.state_code.toLowerCase();

    if (isPin) {
      if (loc.pincode === cleanQuery) score += 100;
      else if (loc.pincodes && loc.pincodes.includes(cleanQuery)) score += 95;
      else if (loc.pincode.startsWith(cleanQuery)) score += 50;
      else if (loc.pincodes && loc.pincodes.some(p => p.startsWith(cleanQuery))) score += 40;
    } else {
      // Exact match on city or alias
      if (cLower === cleanQuery || key === cleanQuery) {
        score += 100;
      } else if (loc.aliases && loc.aliases.some(a => a.toLowerCase() === cleanQuery)) {
        score += 95;
      } else if (cLower.startsWith(cleanQuery)) {
        score += 80;
      } else if (cLower.includes(cleanQuery)) {
        score += 65;
      }

      // District match
      if (dLower === cleanQuery) score += 90;
      else if (dLower.includes(cleanQuery)) score += 50;

      // Token matches (e.g. "Kanpur, UP" -> token "kanpur" + token "up")
      let matchedTokens = 0;
      for (const t of tokens) {
        let tMatched = false;
        if (cLower.includes(t) || key.includes(t)) {
          score += 40;
          tMatched = true;
        }
        if (dLower.includes(t)) {
          score += 30;
          tMatched = true;
        }
        if (sLower.includes(t)) {
          score += 25;
          tMatched = true;
        }
        if (scLower === t) {
          score += 35;
          tMatched = true;
        }
        if (loc.aliases && loc.aliases.some(a => a.toLowerCase().includes(t))) {
          score += 30;
          tMatched = true;
        }
        if (tMatched) matchedTokens++;
      }

      if (tokens.length > 1 && matchedTokens === tokens.length) {
        score += 50; // Bonus for multi-word full match
      }
    }

    if (score > 0 && !seenKeys.has(key)) {
      seenKeys.add(key);
      results.push({
        score,
        key: loc.key || key,
        city: loc.city,
        district: loc.district,
        state: loc.state,
        state_code: loc.state_code,
        pincode: loc.pincode,
        lat: loc.lat,
        lon: loc.lon
      });
    }
  }

  // Sort descending by match score
  results.sort((a, b) => b.score - a.score);
  return results;
}

/**
 * Resolves 6-digit Indian PIN code from local database.
 * Returns location object if found, or null if not found.
 */
function findLocationByPincode(pincode) {
  const pin = String(pincode).replace(/\s+/g, '').trim();
  if (!/^\d{6}$/.test(pin)) return null;

  for (const [key, loc] of Object.entries(INDIAN_LOCATIONS)) {
    if (loc.pincode === pin || (loc.pincodes && loc.pincodes.includes(pin))) {
      return {
        key: loc.key || key,
        city: loc.city,
        district: loc.district,
        state: loc.state,
        state_code: loc.state_code,
        pincode: pin,
        lat: loc.lat,
        lon: loc.lon
      };
    }
  }

  return null;
}

/**
 * Finds nearest known location by latitude and longitude using Haversine distance.
 */
function findNearestLocation(lat, lon) {
  if (typeof lat !== 'number' || typeof lon !== 'number') return null;

  let bestLoc = null;
  let minDistanceKm = Infinity;

  const R = 6371; // Earth radius in km
  for (const loc of Object.values(INDIAN_LOCATIONS)) {
    const dLat = (loc.lat - lat) * Math.PI / 180;
    const dLon = (loc.lon - lon) * Math.PI / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat * Math.PI / 180) * Math.cos(loc.lat * Math.PI / 180) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const d = R * c;

    if (d < minDistanceKm) {
      minDistanceKm = d;
      bestLoc = loc;
    }
  }

  return {
    location: bestLoc,
    distanceKm: Math.round(minDistanceKm)
  };
}

/**
 * Retrieves location object by canonical key (e.g. 'kanpur', 'bhopal', 'indore', 'lucknow', 'ludhiana', 'patna', 'nashik').
 */
function getLocationByKey(key) {
  if (!key) return null;
  const k = String(key).toLowerCase().trim();
  return INDIAN_LOCATIONS[k] || null;
}

// Attach to window for global browser/Capacitor availability
if (typeof window !== 'undefined') {
  window.INDIAN_LOCATIONS = INDIAN_LOCATIONS;
  window.searchIndianLocations = searchIndianLocations;
  window.findLocationByPincode = findLocationByPincode;
  window.findNearestLocation = findNearestLocation;
  window.getLocationByKey = getLocationByKey;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    INDIAN_LOCATIONS,
    searchIndianLocations,
    findLocationByPincode,
    findNearestLocation,
    getLocationByKey
  };
}
