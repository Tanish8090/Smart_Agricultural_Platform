import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== Lines 200 - 260 ===")
for i in range(198, 260):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

print("\n=== Lines 2705 - 2730 ===")
for i in range(2704, min(len(lines), 2730)):
    print(f"{i+1}: {lines[i]}", end='')
