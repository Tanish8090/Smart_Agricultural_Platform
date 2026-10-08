import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import disease_analyzer
    print("[SUCCESS] disease_analyzer imported cleanly! All syntax valid.")
except Exception as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)
