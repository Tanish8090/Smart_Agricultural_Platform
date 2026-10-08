import os

# Check environment variable
key = os.getenv('GEMINI_API_KEY', '')

# Also check .env file manually
if not key and os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('GEMINI_API_KEY='):
                key = line.split('=', 1)[1].strip().strip('"').strip("'")
                break

print("GEMINI_API_KEY present:", bool(key), "Length:", len(key) if key else 0)
if key:
    print("Prefix:", key[:6], "...")
