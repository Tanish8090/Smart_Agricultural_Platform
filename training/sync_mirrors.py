import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_trans = 'final sap project/final sap project/translations.js'
src_html = 'final sap project/final sap project/index.html'
src_app = 'final sap project/final sap project/app.js'
src_crops = 'config/crops.js'

trans_targets = [
    'translations.js',
    'final sap project/translations.js',
    'final sap project/final sap project/final sap project/translations.js'
]
for t in trans_targets:
    shutil.copyfile(src_trans, t)
    print(f"[OK] Synced {t}")

html_targets = [
    'final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html'
]
for t in html_targets:
    shutil.copyfile(src_html, t)
    print(f"[OK] Synced {t}")

app_targets = [
    'app.js',
    'final sap project/app.js',
    'final sap project/final sap project/final sap project/app.js'
]
for t in app_targets:
    shutil.copyfile(src_app, t)
    print(f"[OK] Synced {t}")

crop_targets = [
    'crops.js',
    'final sap project/crops.js',
    'final sap project/final sap project/crops.js',
    'final sap project/final sap project/final sap project/crops.js'
]
for t in crop_targets:
    shutil.copyfile(src_crops, t)
    print(f"[OK] Synced {t}")

print("\nAll frontend mirrors synchronized successfully.")
