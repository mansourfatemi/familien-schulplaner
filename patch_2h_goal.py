with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. CSS: add 2-hour goal bar styles ───────────────────────────────────
goal_css = """
  /* 2-Hour Daily Goal */
  .goal-bar-wrap {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 16px;
  }
  .goal-bar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    font-size: 0.9em;
    font-weight: 600;
  }
  .goal-bar-label { color: var(--text); }
  .goal-bar-time { font-size: 1.05em; font-weight: 700; }
  .goal-bar-track {
    width: 100%;
    height: 18px;
    background: #e8ecf1;
    border-radius: 9px;
    overflow: hidden;
    margin-bottom: 6px;
  }
  .goal-bar-fill {
    height: 100%;
    border-radius: 9px;
    transition: width 0.4s ease;
  }
  .goal-bar-status {
    font-size: 0.82em;
    font-weight: 600;
    margin-top: 4px;
  }
  .goal-bar-status.reached { color: #059669; }
  .goal-bar-status.partial { color: #d97706; }
  .goal-bar-status.low { color: #dc2626; }
  .goal-bar-status.notime { color: #6b7280; }

  /* Overview goal mini-badges */
  .ov-goal-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8em;
    font-weight: 700;
  }
  .ov-goal-badge.reached { background: #d1fae5; color: #065f46; }
  .ov-goal-badge.partial  { background: #fef3c7; color: #92400e; }
  .ov-goal-badge.low      { background: #fee2e2; color: #991b1b; }
  .ov-goal-badge.notime   { background: #f3f4f6; color: #6b7280; }
"""

html = html.replace(
    "  @media (max-width: 700px) {",
    goal_css + "\n  @media (max-width: 700px) {",
    1
)

# ── 2. JS: helper function calcStudyMinutes + buildGoalBar ───────────────
goal_js = """
// ======= 2-HOUR DAILY GOAL =======
const DAILY_GOAL_MIN = 120; // 2 hours

function calcStudyMinutes(items) {
  let mins = 0;
  let hasTime = false;
  items.forEach(item => {
    if (item.timeFrom && item.timeTo) {
      const f = item.timeFrom.split(':').map(Number);
      const t = item.timeTo.split(':').map(Number);
      const diff = (t[0]*60+t[1]) - (f[0]*60+f[1]);
      if (diff > 0) { mins += diff; hasTime = true; }
    } else if (item.timeFrom) {
      mins += 30; hasTime = true;
    }
  });
  return { mins, hasTime };
}

function minsToStr(m) {
  const h = Math.floor(m/60), min = m%60;
  return h > 0 ? h + ' Std ' + (min > 0 ? min + ' Min' : '') : min + ' Min';
}

function buildGoalBar(child, items) {
  const { mins, hasTime } = calcStudyMinutes(items);
  const color = CHILDREN[child].color;
  const pct = Math.min(100, Math.round(mins / DAILY_GOAL_MIN * 100));
  const remaining = DAILY_GOAL_MIN - mins;

  let statusClass, statusMsg, barColor;
  if (!hasTime && items.length === 0) {
    statusClass = 'notime';
    statusMsg = '&#x1F4AC; Noch keine Aufgaben f\u00fcr heute eingetragen.';
    barColor = '#d1d5db';
  } else if (!hasTime) {
    statusClass = 'notime';
    statusMsg = '&#x26A0;&#xFE0F; Keine Zeiten eingetragen \u2014 bitte <em>von/bis</em> ausf\u00fcllen f\u00fcr Zeiterfassung.';
    barColor = '#d1d5db';
  } else if (mins >= DAILY_GOAL_MIN) {
    statusClass = 'reached';
    statusMsg = '&#x1F3C6; Tagesziel erreicht! <strong>' + minsToStr(mins) + '</strong> gelernt \u2014 super!';
    barColor = '#34d399';
  } else if (pct >= 50) {
    statusClass = 'partial';
    statusMsg = '&#x23F3; Noch <strong>' + minsToStr(remaining) + '</strong> bis zum 2-Stunden-Ziel (' + pct + '% geschafft)';
    barColor = '#fbbf24';
  } else {
    statusClass = 'low';
    statusMsg = '&#x1F4A1; Erst <strong>' + minsToStr(mins) + '</strong> von 2 Stunden \u2014 weiter so!';
    barColor = '#ef4444';
  }

  return '<div class="goal-bar-wrap">'
    + '<div class="goal-bar-header">'
    + '<span class="goal-bar-label">&#x1F3AF; Tagesziel: 2 Stunden Lernen</span>'
    + '<span class="goal-bar-time" style="color:' + (mins >= DAILY_GOAL_MIN ? '#059669' : color) + '">'
    + minsToStr(mins) + ' / 2 Std</span>'
    + '</div>'
    + '<div class="goal-bar-track">'
    + '<div class="goal-bar-fill" style="width:' + pct + '%;background:' + barColor + '"></div>'
    + '</div>'
    + '<div class="goal-bar-status ' + statusClass + '">' + statusMsg + '</div>'
    + '</div>';
}

function goalBadgeHtml(items) {
  const { mins, hasTime } = calcStudyMinutes(items);
  const pct = Math.min(100, Math.round(mins / DAILY_GOAL_MIN * 100));
  if (!hasTime && items.length === 0) return '<span class="ov-goal-badge notime">&#x23F0; keine Daten</span>';
  if (!hasTime) return '<span class="ov-goal-badge notime">&#x26A0; Zeit fehlt</span>';
  if (mins >= DAILY_GOAL_MIN) return '<span class="ov-goal-badge reached">&#x2705; ' + minsToStr(mins) + '</span>';
  if (pct >= 50) return '<span class="ov-goal-badge partial">&#x1F7E1; ' + minsToStr(mins) + '</span>';
  return '<span class="ov-goal-badge low">&#x1F534; ' + minsToStr(mins) + '</span>';
}

"""

# Insert before the first // ======= TAGESBERICHT
html = html.replace(
    "// ======= TAGESBERICHT (Daily Report) =======",
    goal_js + "// ======= TAGESBERICHT (Daily Report) =======",
    1
)

# ── 3. buildHomework: inject goal bar at top of hw section ───────────────
# After building the date nav, insert goal bar
old_hw_ul = "  html += '<ul class=\"hw-list\">';"
new_hw_ul = """  // Goal bar above homework list
  html += buildGoalBar(child, items);
  html += '<ul class="hw-list">';"""
html = html.replace(old_hw_ul, new_hw_ul, 1)

# ── 4. buildOverview: add goal badge next to each child's name ────────────
old_ov_name = "    cardsHtml += '<div class=\"hw-section\" style=\"border-left:3px solid ' + info.color + '\">'\\n      + '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:10px\">'\n      + '<strong style=\"color:' + info.color + '\">' + info.name + ' (' + info.grade + ')</strong>'\n      + '<span style=\"color:var(--text-dim);font-size:0.85em\">' + done + '/' + total + ' erledigt</span></div>'"

new_ov_name = """    cardsHtml += '<div class="hw-section" style="border-left:3px solid ' + info.color + '">'
      + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
      + '<strong style="color:' + info.color + '">' + info.name + ' (' + info.grade + ')</strong>'
      + '<span style="color:var(--text-dim);font-size:0.85em">' + done + '/' + total + ' erledigt</span></div>'
      + '<div style="margin-bottom:10px">' + goalBadgeHtml(items) + '</div>'"""

html = html.replace(
    "    cardsHtml += '<div class=\"hw-section\" style=\"border-left:3px solid ' + info.color + '\">'",
    "    cardsHtml += '<div class=\"hw-section\" style=\"border-left:3px solid ' + info.color + '\">'",
    1  # no change yet — do targeted replacement below
)

# More surgical approach for the overview card header
old_ov_block = (
    "    cardsHtml += '<div class=\"hw-section\" style=\"border-left:3px solid ' + info.color + '\">'\n"
    "      + '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:10px\">'\n"
    "      + '<strong style=\"color:' + info.color + '\">' + info.name + ' (' + info.grade + ')</strong>'\n"
    "      + '<span style=\"color:var(--text-dim);font-size:0.85em\">' + done + '/' + total + ' erledigt</span></div>'"
)
new_ov_block = (
    "    cardsHtml += '<div class=\"hw-section\" style=\"border-left:3px solid ' + info.color + '\">'\n"
    "      + '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:6px\">'\n"
    "      + '<strong style=\"color:' + info.color + '\">' + info.name + ' (' + info.grade + ')</strong>'\n"
    "      + '<span style=\"color:var(--text-dim);font-size:0.85em\">' + done + '/' + total + ' erledigt</span></div>'\n"
    "      + '<div style=\"margin-bottom:10px\">' + goalBadgeHtml(items) + '</div>'"
)
html = html.replace(old_ov_block, new_ov_block, 1)

# ── 5. buildDayReport: replace manual studyMinutes calc with shared helper ─
old_study_calc = (
    "  // Calculate study time from timeFrom/timeTo fields\n"
    "  let studyMinutes = 0;\n"
    "  items.forEach(item => {\n"
    "    if (item.timeFrom && item.timeTo) {\n"
    "      const f = item.timeFrom.split(':').map(Number);\n"
    "      const t = item.timeTo.split(':').map(Number);\n"
    "      const diff = (t[0] * 60 + t[1]) - (f[0] * 60 + f[1]);\n"
    "      if (diff > 0) studyMinutes += diff;\n"
    "    } else if (item.timeFrom) {\n"
    "      studyMinutes += 30; // estimated if no end time\n"
    "    }\n"
    "  });\n"
    "  const studyH = Math.floor(studyMinutes / 60);\n"
    "  const studyM = studyMinutes % 60;\n"
    "  const studyStr = studyH > 0 ? studyH + ' Std ' + studyM + ' Min' : studyM + ' Min';"
)
new_study_calc = (
    "  // Calculate study time using shared helper\n"
    "  const { mins: studyMinutes } = calcStudyMinutes(items);\n"
    "  const studyStr = minsToStr(studyMinutes);"
)
html = html.replace(old_study_calc, new_study_calc, 1)

# ── 6. buildDayReport: add goal bar below summary cards ───────────────────
old_day_subj = "  // Per-subject bars\n  html += '<div style=\"margin-top:12px;font-weight:600;font-size:0.9em\">F"
new_day_subj = "  // Goal progress in day report\n  html += buildGoalBar(child, items);\n\n  // Per-subject bars\n  html += '<div style=\"margin-top:12px;font-weight:600;font-size:0.9em\">F"
html = html.replace(old_day_subj, new_day_subj, 1)

# ── 7. buildWeekReport: replace manual totalStudyMin with shared helper ───
old_week_study = (
    "    // Study time per day from timeFrom/timeTo\n"
    "    items.forEach(item => {\n"
    "      if (item.timeFrom && item.timeTo) {\n"
    "        const f = item.timeFrom.split(':').map(Number);\n"
    "        const t = item.timeTo.split(':').map(Number);\n"
    "        const diff = (t[0] * 60 + t[1]) - (f[0] * 60 + f[1]);\n"
    "        if (diff > 0) totalStudyMin += diff;\n"
    "      } else if (item.timeFrom) {\n"
    "        totalStudyMin += 30;\n"
    "      }\n"
    "    });"
)
new_week_study = (
    "    // Study time per day from timeFrom/timeTo\n"
    "    const { mins: dayMins } = calcStudyMinutes(items);\n"
    "    totalStudyMin += dayMins;"
)
html = html.replace(old_week_study, new_week_study, 1)

# ── 8. buildWeekReport: add weekly goal summary (how many days hit 2h) ────
old_week_studystr = (
    "  const totalStudyH = Math.floor(totalStudyMin / 60);\n"
    "  const totalStudyM = totalStudyMin % 60;\n"
    "  const studyStr = totalStudyH > 0 ? totalStudyH + ' Std ' + totalStudyM + ' Min' : totalStudyM + ' Min';"
)
new_week_studystr = (
    "  const studyStr = minsToStr(totalStudyMin);"
)
html = html.replace(old_week_studystr, new_week_studystr, 1)

# Add weekly days-goal-met count in week report (after weekTotal/weekDone calc)
old_week_if_zero = "  if (weekTotal === 0) {"
new_week_if_zero = """  // Count days where 2h goal was met
  let goalDays = 0, goalDaysStr = '';
  weekDays.forEach(d => {
    const di = loadHomework(child, d);
    const { mins } = calcStudyMinutes(di);
    if (mins >= DAILY_GOAL_MIN) goalDays++;
  });
  const goalDayColor = goalDays >= 5 ? '#059669' : goalDays >= 3 ? '#d97706' : '#dc2626';
  const goalEmoji = goalDays >= 5 ? '&#x1F3C6;' : goalDays >= 3 ? '&#x1F7E1;' : '&#x1F534;';

  if (weekTotal === 0) {"""
html = html.replace(old_week_if_zero, new_week_if_zero, 1)

# Add goal-days card to weekly summary cards
old_week_summary_end = (
    "    + '<div class=\"rs-item\"><div class=\"rs-num\" style=\"color:#2563eb\">' + studyStr + '</div><div class=\"rs-label\">Lernzeit gesamt</div></div>'\n"
    "    + '</div>';"
)
new_week_summary_end = (
    "    + '<div class=\"rs-item\"><div class=\"rs-num\" style=\"color:#2563eb\">' + studyStr + '</div><div class=\"rs-label\">Lernzeit gesamt</div></div>'\n"
    "    + '<div class=\"rs-item\"><div class=\"rs-num\" style=\"color:' + goalDayColor + '\">' + goalEmoji + ' ' + goalDays + '/7</div><div class=\"rs-label\">Tage mit 2h-Ziel</div></div>'\n"
    "    + '</div>';"
)
html = html.replace(old_week_summary_end, new_week_summary_end, 1)

with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("DONE")
checks = [
    'goal-bar-wrap',
    'DAILY_GOAL_MIN',
    'calcStudyMinutes',
    'buildGoalBar',
    'goalBadgeHtml',
    'minsToStr',
    'Tagesziel: 2 Stunden',
    'goalDays',
    'Tage mit 2h-Ziel',
    'ov-goal-badge',
]
for c in checks:
    print(f"  {'OK' if c in html else 'MISSING'}: {c}")
