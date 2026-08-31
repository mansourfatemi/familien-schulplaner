import re

with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. CSS VARIABLES ─────────────────────────────────────────────────────
html = html.replace(
    "    --jasmin-color: #FF9800;",
    "    --jasmin-color: #FF9800;\n    --zainab-color: #9B59B6;\n    --mansoor-color: #1ABC9C;",
    1
)

# ── 2. TAB active color rules ─────────────────────────────────────────────
html = html.replace(
    '  .tab.active[data-child="all"] { color: var(--green); }',
    '  .tab.active[data-child="all"] { color: var(--green); }\n  .tab.active[data-child="zainab"] { color: var(--zainab-color); }\n  .tab.active[data-child="mansoor"] { color: var(--mansoor-color); }',
    1
)

# ── 3. TAB avatar colors ──────────────────────────────────────────────────
html = html.replace(
    '  .tab[data-child="all"] .avatar { background: var(--green); }',
    '  .tab[data-child="all"] .avatar { background: var(--green); }\n  .tab[data-child="zainab"] .avatar { background: var(--zainab-color); }\n  .tab[data-child="mansoor"] .avatar { background: var(--mansoor-color); }',
    1
)

# ── 4. TABS HTML ──────────────────────────────────────────────────────────
html = html.replace(
    "  <div class=\"tab\" data-child=\"jasmin\" onclick=\"switchTab('jasmin')\">\n    <div class=\"avatar\">JF</div> Jasmin\n  </div>\n</div>",
    "  <div class=\"tab\" data-child=\"jasmin\" onclick=\"switchTab('jasmin')\">\n    <div class=\"avatar\">JF</div> Jasmin\n  </div>\n  <div class=\"tab\" data-child=\"zainab\" onclick=\"switchTab('zainab')\">\n    <div class=\"avatar\">ZF</div> Zainab\n  </div>\n  <div class=\"tab\" data-child=\"mansoor\" onclick=\"switchTab('mansoor')\">\n    <div class=\"avatar\">MF</div> Mansoor\n  </div>\n</div>",
    1
)

# ── 5. PANELS HTML ────────────────────────────────────────────────────────
zainab_mansoor_panels = """
  <!-- ZAINAB PANEL -->
  <div class="panel" id="panel-zainab">
    <div class="child-info">
      <div class="ci-avatar" style="background:var(--zainab-color)">ZF</div>
      <div>
        <div class="ci-name">Zainab Fatemi</div>
        <div class="ci-detail">&#x1F3EB; Abendgymnasium</div>
      </div>
    </div>
    <div class="section-title">&#x1F4C5; Stundenplan</div>
    <div class="schedule-grid" id="schedule-zainab"></div>
    <div class="section-title">&#x1F4DD; Hausaufgaben</div>
    <div class="hw-section" id="hw-zainab"></div>
    <div class="section-title">&#x1F4CA; Tagesbericht</div>
    <div class="hw-section" id="report-day-zainab"></div>
    <div class="section-title">&#x1F4C8; Wochenbericht</div>
    <div class="hw-section" id="report-week-zainab"></div>
  </div>

  <!-- MANSOOR PANEL -->
  <div class="panel" id="panel-mansoor">
    <div class="child-info">
      <div class="ci-avatar" style="background:var(--mansoor-color)">MF</div>
      <div>
        <div class="ci-name">Mansoor Fatemi</div>
        <div class="ci-detail">&#x1F4D6; Pers&#246;nliches Lernen &mdash; Mathe &bull; Quran &bull; Englisch &bull; Deutsch</div>
      </div>
    </div>
    <div class="section-title">&#x1F4DD; T&#228;gliche Lernaufgaben</div>
    <div class="hw-section" id="hw-mansoor"></div>
    <div class="section-title">&#x1F4CA; Tagesbericht</div>
    <div class="hw-section" id="report-day-mansoor"></div>
    <div class="section-title">&#x1F4C8; Wochenbericht</div>
    <div class="hw-section" id="report-week-mansoor"></div>
  </div>
"""

# Insert before </div>\n\n<script>
html = html.replace(
    "</div>\n\n<script>",
    zainab_mansoor_panels + "\n</div>\n\n<script>",
    1
)

# ── 6. CHILDREN JS ────────────────────────────────────────────────────────
html = html.replace(
    "  jasmin: {\n    name: 'Jasmin', color: '#FF9800', grade: '2. Klasse',\n    subjects: ['Mathematik','Deutsch','Sachunterricht','Musik','Sport','Religion','Bildnerische Erziehung','Werken','Quran']\n  }\n};",
    "  jasmin: {\n    name: 'Jasmin', color: '#FF9800', grade: '2. Klasse',\n    subjects: ['Mathematik','Deutsch','Sachunterricht','Musik','Sport','Religion','Bildnerische Erziehung','Werken','Quran']\n  },\n  zainab: {\n    name: 'Zainab', color: '#9B59B6', grade: 'Abendgymnasium',\n    subjects: ['Mathematik','Deutsch','Englisch','Geschichte','Geographie','Biologie','Physik','Chemie','Sport','Religion','Informatik','Quran']\n  },\n  mansoor: {\n    name: 'Mansoor', color: '#1ABC9C', grade: 'Pers\u00f6nliches Lernen',\n    subjects: ['Mathematik','Quran','Englisch','Deutsch']\n  }\n};",
    1
)

# ── 7. changeDate all-refresh list ────────────────────────────────────────
html = html.replace(
    "['ibrahim','hosna','jasmin'].forEach(c => { buildHomework(c); buildDayReport(c); buildWeekReport(c); }); }",
    "['ibrahim','hosna','jasmin','zainab','mansoor'].forEach(c => { buildHomework(c); buildDayReport(c); buildWeekReport(c); }); }",
)  # replaces both changeDate and jumpToDate

# ── 8. Overview loop ──────────────────────────────────────────────────────
html = html.replace(
    "  ['ibrahim','hosna','jasmin'].forEach(child => {",
    "  ['ibrahim','hosna','jasmin','zainab','mansoor'].forEach(child => {",
    1
)

# ── 9. Overview stats: 3 Kinder → 5 Mitglieder ───────────────────────────
html = html.replace(
    "'<div class=\"stat-card\"><div class=\"stat-num\">3</div><div class=\"stat-label\">Kinder</div></div>'",
    "'<div class=\"stat-card\"><div class=\"stat-num\">5</div><div class=\"stat-label\">Mitglieder</div></div>'",
    1
)

# ── 10. init() ────────────────────────────────────────────────────────────
html = html.replace(
    "  ['ibrahim','hosna','jasmin'].forEach(child => { buildSchedule(child); buildHomework(child); });\n  buildOverview();\n  buildAllReports();",
    "  ['ibrahim','hosna','jasmin','zainab'].forEach(child => { buildSchedule(child); buildHomework(child); });\n  buildHomework('mansoor');\n  buildOverview();\n  buildAllReports();",
    1
)

# ── 11. buildAllReports ───────────────────────────────────────────────────
html = html.replace(
    "  ['ibrahim','hosna','jasmin'].forEach(child => {\n    buildDayReport(child);\n    buildWeekReport(child);\n  });",
    "  ['ibrahim','hosna','jasmin','zainab','mansoor'].forEach(child => {\n    buildDayReport(child);\n    buildWeekReport(child);\n  });",
    1
)

# ── 12. Firebase sync loop ────────────────────────────────────────────────
html = html.replace(
    "    ['ibrahim','hosna','jasmin'].forEach(child => {",
    "    ['ibrahim','hosna','jasmin','zainab','mansoor'].forEach(child => {",
    1
)

# ── 13. getSubjectColor: add Chemie + Informatik ─────────────────────────
html = html.replace(
    "'Quran':'#059669' };",
    "'Chemie':'#f97316','Informatik':'#06b6d4','Quran':'#059669' };",
    1
)

# Write
with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("DONE")
checks = ['--zainab-color','--mansoor-color','panel-zainab','panel-mansoor',"zainab: {",'mansoor: {',"'zainab','mansoor'",'Abendgymnasium','Pers\u00f6nliches Lernen','5</div><div class="stat-label">Mitglieder']
for c in checks:
    print(f"  {'OK' if c in html else 'MISSING'}: {c}")
