import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def show(start, end):
    for i in range(start, end):
        if 0 <= i < len(lines):
            print(f'{i+1}: {lines[i]}', end='')

print('=== 1. Top Navbar (150-165) ===')
show(149, 163)

print('\n=== 2. Mobile Menu (180-192) ===')
show(179, 192)

print('\n=== 3. Hero Quick Bar (285-296) ===')
show(284, 296)

print('\n=== 4. Dashboard Cards 5 & 6 (450-520) ===')
show(450, 520)

print('\n=== 5. Chat Suggested Chips (1220-1238) ===')
show(1220, 1238)

print('\n=== 6. End of Schemes Module & Modal (2290-2315) ===')
show(2290, 2315)
