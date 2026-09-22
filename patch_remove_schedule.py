import os, re

SRC = r"C:\Users\sayefate\Desktop\Familien Schulplaner\index.html"
TMP = SRC + ".tmp_nosched"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ============================================================
# 1) Remove "Stundenplan" section-title + schedule-grid from each child panel
#    The pattern: <div class="section-title">...Stundenplan...</div>
#    followed by <div class="schedule-grid">...</div>
#    We'll use regex to remove these blocks
# ============================================================

# Remove section title for Stundenplan and the grid that follows
# Pattern: section-title containing Stundenplan + the schedule-grid div block
pattern = r'<div class="section-title"[^>]*>.*?Stundenplan.*?</div>\s*<div class="schedule-grid">.*?</div>\s*'
matches = re.findall(pattern, html, flags=re.DOTALL)
print(f"Stundenplan blocks found: {len(matches)}")
for i, m in enumerate(matches):
    print(f"  [{i}] {repr(m[:80])}...")

html = re.sub(pattern, '', html, flags=re.DOTALL)
print("✓ Stundenplan section blocks removed")

# ============================================================
# 2) Remove schedule-related CSS classes
#    .schedule-grid { ... } block
# ============================================================
css_pattern = r'\s*\.schedule-grid \{[^}]*\}[^}]*\}[^}]*\}[^}]*\}'
# More precise: find the full .schedule-grid ruleset
css_pattern2 = r'  \.schedule-grid \{.*?\n  \}\n'
css_matches = re.findall(css_pattern2, html, flags=re.DOTALL)
print(f"schedule-grid CSS blocks found: {len(css_matches)}")

html = re.sub(css_pattern2, '', html, flags=re.DOTALL)

# Also remove .schedule-grid .cell rules
cell_pattern = r'  \.schedule-grid \.cell.*?\n  \}\n'
html = re.sub(cell_pattern, '', html, flags=re.DOTALL)

# Remove .cell .subject-input rules
subj_pattern = r'  \.cell \.subject-input.*?\n  \}\n'
html = re.sub(subj_pattern, '', html, flags=re.DOTALL)

print("✓ CSS cleaned")

# ============================================================
# 3) Remove buildSchedule / loadSchedule / saveSchedule JS calls
#    and schedule-related function calls in switchTab
# ============================================================
# Remove lines calling buildSchedule
html = re.sub(r'\n.*?buildSchedule\([^)]*\);', '', html)
print("✓ buildSchedule calls removed")

# ============================================================
# 4) Remove the buildSchedule function definition itself
# ============================================================
sched_fn = r'\n  function buildSchedule\(child\) \{.*?\n  \}\n'
matches_fn = re.findall(sched_fn, html, flags=re.DOTALL)
print(f"buildSchedule function found: {len(matches_fn)}")
html = re.sub(sched_fn, '\n', html, flags=re.DOTALL)
print("✓ buildSchedule function removed")

# ============================================================
# Write output atomically
# ============================================================
with open(TMP, "w", encoding="utf-8") as f:
    f.write(html)

with open(TMP, encoding="utf-8") as f:
    check = f.read()
assert check == html, "Round-trip failed!"

os.replace(TMP, SRC)
print(f"✓ index.html written — {original_len} -> {len(html)} chars (removed {original_len - len(html)})")
