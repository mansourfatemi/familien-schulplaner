import os, re

SRC = r"C:\Users\sayefate\Desktop\Familien Schulplaner\index.html"
TMP = SRC + ".tmp_nosched2"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ============================================================
# 1) Remove each Stundenplan section-title + schedule-grid block
#    Pattern uses &#x1F4C5; entity
# ============================================================
pattern = r'[ \t]*<div class="section-title">&#x1F4C5; Stundenplan</div>\s*<div class="schedule-grid">.*?</div>\s*'
matches = re.findall(pattern, html, flags=re.DOTALL)
print(f"Stundenplan blocks found: {len(matches)}")
for i, m in enumerate(matches[:2]):
    print(f"  [{i}] length={len(m)}, starts: {repr(m[:60])}")

html = re.sub(pattern, '', html, flags=re.DOTALL)
remaining = html.count('Stundenplan')
print(f"✓ Removed {len(matches)} blocks. Remaining 'Stundenplan' refs: {remaining}")

# ============================================================
# 2) Update page title
# ============================================================
html = html.replace(
    '<title>Fatemi Family \u2014 Stundenplan &amp; Hausaufgaben</title>',
    '<title>Fatemi Family \u2014 Hausaufgaben &amp; Verlauf</title>'
)
html = html.replace(
    '<title>Fatemi Family \u2014 Stundenplan & Hausaufgaben</title>',
    '<title>Fatemi Family \u2014 Hausaufgaben &amp; Verlauf</title>'
)
print("✓ Title updated")

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
