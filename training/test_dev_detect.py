import os
import sys
sys.path.insert(0, '.')
import legacy_helpers

# Test is_mostly_devanagari logic
sample_hinglish = "Namaste Kisan Bhai! Aapki gehu ki fasal me urea dalein."
sample_hindi = "नमस्ते किसान भाई! 🙏 आपकी गेहूं की फसल के लिए यूरिया की अनुशंसित मात्रा..."

dev_count = sum(1 for ch in sample_hindi if '\u0900' <= ch <= '\u097f')
lat_count = sum(1 for ch in sample_hindi if 'a' <= ch.lower() <= 'z')
print(f"Hindi sample - Dev: {dev_count}, Lat: {lat_count}")

dev_count_h = sum(1 for ch in sample_hinglish if '\u0900' <= ch <= '\u097f')
lat_count_h = sum(1 for ch in sample_hinglish if 'a' <= ch.lower() <= 'z')
print(f"Hinglish sample - Dev: {dev_count_h}, Lat: {lat_count_h}")
