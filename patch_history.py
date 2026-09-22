import os

SRC = r"C:\Users\sayefate\Desktop\Familien Schulplaner\index.html"
TMP = SRC + ".tmp_history"

with open(SRC, encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1) Add "Verlauf" tab after the Mansoor tab
# ============================================================
OLD_TABS_END = '''  <div class="tab" data-child="mansoor" onclick="switchTab('mansoor')">
    <div class="avatar">MF</div> Mansoor
  </div>
</div>'''

NEW_TABS_END = '''  <div class="tab" data-child="mansoor" onclick="switchTab('mansoor')">
    <div class="avatar">MF</div> Mansoor
  </div>
  <div class="tab" data-child="history" onclick="switchTab('history')" style="color:#6366f1">
    <span class="avatar" style="background:#6366f1;font-size:0.7em">&#x1F4CB;</span> Verlauf
  </div>
</div>'''

assert html.count(OLD_TABS_END) == 1, f"Tab anchor count={html.count(OLD_TABS_END)}"
html = html.replace(OLD_TABS_END, NEW_TABS_END)
print("✓ Tab added")

# ============================================================
# 2) Add CSS for history panel (before existing drink tracker css comment)
# ============================================================
CSS_ANCHOR = "  /* ======= DRINK TRACKER ======= */"
CSS_NEW = """  /* ======= HISTORY / VERLAUF ======= */
  .history-toolbar {
    display: flex; gap: 10px; flex-wrap: wrap;
    align-items: center; margin-bottom: 18px;
  }
  .history-toolbar select, .history-toolbar input[type="date"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 0.9em;
  }
  .history-toolbar button {
    background: #6366f1;
    border: none;
    color: #fff;
    padding: 7px 16px;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    font-size: 0.88em;
  }
  .history-toolbar button:hover { filter: brightness(1.1); }
  .history-summary {
    display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 18px;
  }
  .history-summary .hsum-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 18px;
    text-align: center;
    flex: 1; min-width: 110px;
  }
  .hsum-card .hsum-num { font-size: 1.7em; font-weight: 800; }
  .hsum-card .hsum-label { font-size: 0.75em; color: var(--text-dim); margin-top: 2px; }
  .history-table-wrap {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    overflow-x: auto;
  }
  .history-table {
    width: 100%; border-collapse: collapse;
    font-size: 0.88em; min-width: 520px;
  }
  .history-table thead tr {
    background: #eef1f5;
    border-bottom: 2px solid var(--border);
  }
  .history-table th {
    padding: 10px 14px; text-align: left;
    font-weight: 700; color: var(--text);
  }
  .history-table tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }
  .history-table tbody tr:hover { background: #f5f7fa; }
  .history-table td { padding: 9px 14px; color: var(--text); }
  .history-table .badge-done {
    background: #d1fae5; color: #065f46;
    padding: 2px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 700;
  }
  .history-table .badge-open {
    background: #fef3c7; color: #92400e;
    padding: 2px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 700;
  }
  .history-table .child-dot {
    display: inline-block;
    width: 10px; height: 10px; border-radius: 50%;
    margin-right: 6px; vertical-align: middle;
  }
  .history-empty {
    text-align: center; padding: 40px;
    color: var(--text-dim); font-size: 0.95em;
  }

  /* ======= DRINK TRACKER ======= */"""

assert html.count(CSS_ANCHOR) == 1, f"CSS anchor count={html.count(CSS_ANCHOR)}"
html = html.replace(CSS_ANCHOR, CSS_NEW)
print("✓ CSS added")

# ============================================================
# 3) Add History panel HTML (before the panels content area ends)
#    Insert before <div class="content"> opening (panels come after)
#    Actually insert just before <!-- Firebase PWA + Sync --> comment
# ============================================================
PANEL_ANCHOR = "<!-- Firebase PWA + Sync -->"

HISTORY_PANEL_HTML = """<!-- HISTORY / VERLAUF PANEL -->
<div class="panel" id="panel-history">
  <div class="content">
    <div class="section-title" style="color:#6366f1">&#x1F4CB; Verlauf der Hausaufgaben</div>
    <div class="history-toolbar">
      <select id="hist-child">
        <option value="all">Alle Kinder</option>
        <option value="ibrahim">Ibrahim</option>
        <option value="hosna">Hosna</option>
        <option value="jasmin">Jasmin</option>
        <option value="zainab">Zainab</option>
      </select>
      <select id="hist-range">
        <option value="7">Diese Woche (7 Tage)</option>
        <option value="14">Letzte 2 Wochen</option>
        <option value="30">Dieser Monat (30 Tage)</option>
        <option value="90">Letzte 3 Monate</option>
        <option value="custom">Eigener Zeitraum...</option>
      </select>
      <input type="date" id="hist-from" style="display:none" placeholder="Von">
      <input type="date" id="hist-to" style="display:none" placeholder="Bis">
      <button onclick="buildHistory()">&#x1F50D; Anzeigen</button>
    </div>
    <div class="history-summary" id="hist-summary"></div>
    <div class="history-table-wrap">
      <table class="history-table">
        <thead>
          <tr>
            <th>&#x1F4C5; Datum</th>
            <th>&#x1F476; Kind</th>
            <th>&#x1F4DA; Fach</th>
            <th>&#x1F4DD; Aufgabe</th>
            <th>&#x2705; Status</th>
          </tr>
        </thead>
        <tbody id="hist-tbody"></tbody>
      </table>
      <div class="history-empty" id="hist-empty" style="display:none">
        Keine Eintr&#228;ge f&#252;r den gew&#228;hlten Zeitraum.
      </div>
    </div>
  </div>
</div>

<!-- Firebase PWA + Sync -->"""

assert html.count(PANEL_ANCHOR) == 1, f"Panel anchor count={html.count(PANEL_ANCHOR)}"
html = html.replace(PANEL_ANCHOR, HISTORY_PANEL_HTML)
print("✓ History panel HTML added")

# ============================================================
# 4) Patch switchTab to call buildHistory when history is selected
# ============================================================
OLD_SWITCH = "  if (child === 'all') buildOverview();\n  if (child ==="
NEW_SWITCH = "  if (child === 'all') buildOverview();\n  if (child === 'history') buildHistory();\n  if (child ==="

assert html.count(OLD_SWITCH) == 1, f"switchTab anchor count={html.count(OLD_SWITCH)}"
html = html.replace(OLD_SWITCH, NEW_SWITCH)
print("✓ switchTab patched")

# ============================================================
# 5) Add buildHistory() function before closing </script> of main script block
#    Find the last </script> before </body>
# ============================================================
JS_ANCHOR = "  if ('serviceWorker' in navigator)"

HISTORY_JS = """  // ============================================================
  // HISTORY / VERLAUF — display homework history from localStorage
  // ============================================================
  var HIST_CHILD_COLORS = {
    ibrahim: '#4A90D9', hosna: '#E91E8C',
    jasmin: '#FF9800', zainab: '#9B59B6', mansoor: '#1ABC9C'
  };
  var HIST_CHILD_NAMES = {
    ibrahim: 'Ibrahim', hosna: 'Hosna',
    jasmin: 'Jasmin', zainab: 'Zainab', mansoor: 'Mansoor'
  };

  function buildHistory() {
    var childFilter = document.getElementById('hist-child').value;
    var rangeVal    = document.getElementById('hist-range').value;
    var fromInput   = document.getElementById('hist-from');
    var toInput     = document.getElementById('hist-to');

    if (rangeVal === 'custom') {
      fromInput.style.display = 'inline-block';
      toInput.style.display   = 'inline-block';
    } else {
      fromInput.style.display = 'none';
      toInput.style.display   = 'none';
    }

    var today = new Date();
    var fromDate, toDate = new Date(today);
    toDate.setHours(23,59,59,999);

    if (rangeVal === 'custom') {
      if (!fromInput.value || !toInput.value) return;
      fromDate = new Date(fromInput.value);
      toDate   = new Date(toInput.value);
      toDate.setHours(23,59,59,999);
    } else {
      fromDate = new Date(today);
      fromDate.setDate(today.getDate() - parseInt(rangeVal) + 1);
      fromDate.setHours(0,0,0,0);
    }

    var children = childFilter === 'all'
      ? ['ibrahim','hosna','jasmin','zainab','mansoor']
      : [childFilter];

    var rows = [];
    var cur = new Date(fromDate);
    while (cur <= toDate) {
      var dateStr = cur.toISOString().split('T')[0];
      children.forEach(function(child) {
        var key   = 'hw_' + child + '_' + dateStr;
        var local = localStorage.getItem(key);
        if (!local) return;
        var items;
        try { items = JSON.parse(local); } catch(e) { return; }
        if (!Array.isArray(items)) return;
        items.forEach(function(item) {
          rows.push({
            date:    dateStr,
            child:   child,
            subject: item.subject || '',
            text:    item.text    || '',
            done:    !!item.done
          });
        });
      });
      cur.setDate(cur.getDate() + 1);
    }

    rows.sort(function(a,b) {
      return b.date.localeCompare(a.date) || a.child.localeCompare(b.child);
    });

    var total = rows.length;
    var done  = rows.filter(function(r){ return r.done; }).length;
    var open  = total - done;
    var daysSet = {};
    rows.forEach(function(r){ daysSet[r.date] = 1; });
    var dayCount = Object.keys(daysSet).length;

    var sumEl = document.getElementById('hist-summary');
    sumEl.innerHTML =
      '<div class="hsum-card"><div class="hsum-num" style="color:#6366f1">' + total + '</div><div class="hsum-label">Aufgaben gesamt</div></div>' +
      '<div class="hsum-card"><div class="hsum-num" style="color:#34d399">' + done  + '</div><div class="hsum-label">Erledigt</div></div>' +
      '<div class="hsum-card"><div class="hsum-num" style="color:#ef4444">' + open  + '</div><div class="hsum-label">Offen</div></div>' +
      '<div class="hsum-card"><div class="hsum-num" style="color:#f59e0b">' + dayCount + '</div><div class="hsum-label">Tage mit Eintr\u00e4gen</div></div>';

    var tbody = document.getElementById('hist-tbody');
    var empty = document.getElementById('hist-empty');
    tbody.innerHTML = '';

    if (rows.length === 0) {
      empty.style.display = 'block';
      return;
    }
    empty.style.display = 'none';

    rows.forEach(function(r) {
      var clr  = HIST_CHILD_COLORS[r.child] || '#888';
      var nm   = HIST_CHILD_NAMES[r.child]  || r.child;
      var p    = r.date.split('-');
      var dstr = p[2] + '.' + p[1] + '.' + p[0];
      var tr   = document.createElement('tr');
      tr.innerHTML =
        '<td>' + dstr + '</td>' +
        '<td><span class="child-dot" style="background:' + clr + '"></span>' + nm + '</td>' +
        '<td>' + r.subject + '</td>' +
        '<td>' + r.text + '</td>' +
        '<td>' + (r.done
          ? '<span class="badge-done">&#x2713; Erledigt</span>'
          : '<span class="badge-open">&#x23F3; Offen</span>') + '</td>';
      tbody.appendChild(tr);
    });
  }

  // wire up range selector to show/hide date pickers
  document.addEventListener('DOMContentLoaded', function() {
    var rangeEl = document.getElementById('hist-range');
    if (rangeEl) {
      rangeEl.addEventListener('change', function() {
        var v = rangeEl.value;
        document.getElementById('hist-from').style.display = v === 'custom' ? 'inline-block' : 'none';
        document.getElementById('hist-to').style.display   = v === 'custom' ? 'inline-block' : 'none';
      });
    }
  });

  if ('serviceWorker' in navigator)"""

assert html.count(JS_ANCHOR) == 1, f"JS anchor count={html.count(JS_ANCHOR)}"
html = html.replace(JS_ANCHOR, HISTORY_JS)
print("✓ buildHistory() JS added")

# ============================================================
# Write output atomically
# ============================================================
with open(TMP, "w", encoding="utf-8") as f:
    f.write(html)

with open(TMP, encoding="utf-8") as f:
    check = f.read()
assert check == html, "Round-trip verification failed!"

os.replace(TMP, SRC)
print("✓ index.html written successfully —", len(html), "chars")
