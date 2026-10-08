import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def show(start, end):
    for i in range(start, end):
        if 0 <= i < len(lines):
            print(f'{i+1}: {lines[i]}', end='')

print('=== 1. Top Navbar (around 150-165) ===')
show(148, 165)

print('\n=== 2. Mobile Menu (around 180-195) ===')
show(180, 195)

print('\n=== 3. Hero Quick Bar (around 285-298) ===')
show(282, 298)

print('\n=== 4. Dashboard Cards (around 450-530) ===')
show(452, 530)

print('\n=== 5. Chat Suggested Chips in HTML (around 1220-1245) ===')
show(1220, 1245)

print('\n=== 6. Schemes Module & Modal (around 1990-2020) ===')
show(1990, 2020)

print('\n=== 7. Footer (around 2675-2725) ===')
show(2675, 2725)
