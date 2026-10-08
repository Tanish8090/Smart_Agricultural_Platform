import sys

paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove diagTreatmentGrid from line around Image Input Options
    html = html.replace(
        '<!-- Image Input Options (Upload or Camera Capture) -->\n      <div id="diagTreatmentGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        '<!-- Image Input Options (Upload or Camera Capture) -->\n      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    )
    html = html.replace(
        '<!-- Image Input Options (Upload or Camera Capture) -->\r\n      <div id="diagTreatmentGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        '<!-- Image Input Options (Upload or Camera Capture) -->\r\n      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    )

    # 2. Add diagTreatmentGrid to Agronomic Treatment Grid
    html = html.replace(
        '<!-- Agronomic Treatment Grid -->\n          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        '<!-- Agronomic Treatment Grid -->\n          <div id="diagTreatmentGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    )
    html = html.replace(
        '<!-- Agronomic Treatment Grid -->\r\n          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">',
        '<!-- Agronomic Treatment Grid -->\r\n          <div id="diagTreatmentGrid" class="grid grid-cols-1 md:grid-cols-2 gap-6">'
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed diagTreatmentGrid in {p}")
