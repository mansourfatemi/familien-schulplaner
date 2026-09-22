import os, re

SRC = r"C:\Users\sayefate\Desktop\Familien Schulplaner\index.html"
TMP = SRC + ".tmp_nosched3"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# Remove: section-title Stundenplan + empty schedule-grid div
# for each child: ibrahim, hosna, jasmin, zainab
children = ['ibrahim', 'hosna', 'jasmin', 'zainab']
removed = 0
for child in children:
    old = (
        '\n    <div class="section-title">&#x1F4C5; Stundenplan</div>\n'
        '    <div class="schedule-grid" id="schedule-' + child + '"></div>'
    )
    count = html.count(old)
    print(f"  {child}: found {count}")
    if count == 1:
        html = html.replace(old, '')
        removed += 1

print(f"✓ Removed {removed} Stundenplan blocks")

# Also remove saveSchedule / loadSchedule patches in Firebase section
# They reference schedule sync but since we removed the UI, they are dead code
# Remove the 3-line schedule sync block in setupRealtimeSync
old_sched_sync = (
    "\n        // Schedule sync\n"
    "        const rs = ref(db, FAMILY_KEY + '/schedule_' + child);\n"
    "        onValue(rs, snap => {\n"
    "          if (!snap.exists()) return;\n"
    "          localStorage.setItem('schedule_' + child, JSON.stringify(snap.val()));\n"
    "          try { if (typeof buildSchedule === 'function') buildSchedule(child); } catch(e) {}\n"
    "        });"
)
count_sync = html.count(old_sched_sync)
print(f"  schedule sync block found: {count_sync}")
if count_sync == 1:
    html = html.replace(old_sched_sync, '')
    print("✓ Schedule Firebase sync block removed")

# Update page title
old_title = '<title>Fatemi Family \u2014 Stundenplan &amp; Hausaufgaben</title>'
new_title = '<title>Fatemi Family \u2014 Hausaufgaben &amp; Verlauf</title>'
if html.count(old_title) == 1:
    html = html.replace(old_title, new_title)
    print("✓ Title updated")

remaining = html.count('Stundenplan')
print(f"Remaining 'Stundenplan' references: {remaining}")

# Write atomically
with open(TMP, "w", encoding="utf-8") as f:
    f.write(html)
with open(TMP, encoding="utf-8") as f:
    check = f.read()
assert check == html
os.replace(TMP, SRC)
print(f"✓ Done — {original_len} -> {len(html)} chars (removed {original_len - len(html)})")
