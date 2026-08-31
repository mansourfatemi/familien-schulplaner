f = open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', encoding='utf-8')
html = f.read()
f.close()

# 1. Add PWA meta tags after <title>
title_end = html.find('</title>') + len('</title>')
pwa_meta = '''
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#2563eb">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="Schulplaner">
  <link rel="apple-touch-icon" href="icon-192.png">'''

if 'manifest.json' not in html:
    html = html[:title_end] + pwa_meta + html[title_end:]
    print('PWA meta tags added')
else:
    print('PWA meta tags already present')

# 2. Add Firebase + sync code before </body>
firebase_code = '''
  <!-- Firebase PWA + Sync -->
  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
    import { getDatabase, ref, set, get, onValue } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-database.js";

    const firebaseConfig = {
      apiKey: "AIzaSyCmZNTGXyf36bbUBy2UgnDukerdJW1dOl8",
      authDomain: "fatemi-schulplaner.firebaseapp.com",
      databaseURL: "https://fatemi-schulplaner-default-rtdb.europe-west1.firebasedatabase.app",
      projectId: "fatemi-schulplaner",
      storageBucket: "fatemi-schulplaner.firebasestorage.app",
      messagingSenderId: "269419033986",
      appId: "1:269419033986:web:26e853c5db62eaa8a8cb9b"
    };

    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);
    window._fbDb = db;
    window._fbRef = ref;
    window._fbSet = set;
    window._fbGet = get;
    window._fbOnValue = onValue;

    // Override localStorage with Firebase
    const FAMILY_KEY = 'fatemi';

    function fbPath(key) {
      return FAMILY_KEY + '/' + key.replace(/\//g, '_');
    }

    // Save to both localStorage (offline cache) and Firebase
    window.fbSave = function(key, value) {
      localStorage.setItem(key, JSON.stringify(value));
      const r = ref(db, fbPath(key));
      set(r, value).catch(e => console.warn('Firebase save error:', e));
    };

    // Load from Firebase (with localStorage fallback)
    window.fbLoad = function(key, callback) {
      const r = ref(db, fbPath(key));
      get(r).then(snap => {
        if (snap.exists()) {
          const val = snap.val();
          localStorage.setItem(key, JSON.stringify(val));
          callback(val);
        } else {
          // Try localStorage fallback
          const local = localStorage.getItem(key);
          callback(local ? JSON.parse(local) : null);
        }
      }).catch(() => {
        const local = localStorage.getItem(key);
        callback(local ? JSON.parse(local) : null);
      });
    };

    // Real-time listener — auto-refresh UI when another device changes data
    window.fbListen = function(key, callback) {
      const r = ref(db, fbPath(key));
      return onValue(r, snap => {
        if (snap.exists()) {
          const val = snap.val();
          localStorage.setItem(key, JSON.stringify(val));
          callback(val);
        }
      });
    };

    // Patch saveHomework and loadHomework to use Firebase
    const _origSave = window.saveHomework;
    const _origLoad = window.loadHomework;

    window.saveHomework = function(child, date, items) {
      const key = 'hw_' + child + '_' + date.toISOString().split('T')[0];
      window.fbSave(key, items);
    };

    window.loadHomework = function(child, date) {
      const key = 'hw_' + child + '_' + date.toISOString().split('T')[0];
      const local = localStorage.getItem(key);
      return local ? JSON.parse(local) : [];
    };

    // Patch saveSchedule and loadSchedule
    window.saveSchedule = function(child, data) {
      window.fbSave('schedule_' + child, data);
    };

    window.loadSchedule = function(child) {
      const local = localStorage.getItem('schedule_' + child);
      return local ? JSON.parse(local) : {};
    };

    // Real-time sync for homework — listen to all 3 children
    function setupRealtimeSync() {
      ['ibrahim','hosna','jasmin'].forEach(child => {
        // Listen to all homework entries for this child
        const r = ref(db, FAMILY_KEY + '/hw_' + child);
        onValue(r, snap => {
          if (!snap.exists()) return;
          // Update localStorage cache
          const data = snap.val();
          Object.entries(data).forEach(([dateKey, items]) => {
            localStorage.setItem('hw_' + child + '_' + dateKey, JSON.stringify(items));
          });
          // Refresh UI if visible
          try {
            if (typeof buildHomework === 'function') buildHomework(child);
            if (typeof buildOverview === 'function') buildOverview();
            if (typeof buildDayReport === 'function') buildDayReport(child);
            if (typeof buildWeekReport === 'function') buildWeekReport(child);
          } catch(e) {}
        });

        // Schedule sync
        const rs = ref(db, FAMILY_KEY + '/schedule_' + child);
        onValue(rs, snap => {
          if (!snap.exists()) return;
          localStorage.setItem('schedule_' + child, JSON.stringify(snap.val()));
          try { if (typeof buildSchedule === 'function') buildSchedule(child); } catch(e) {}
        });
      });
    }

    // Wait for page to be ready
    if (document.readyState === 'complete') {
      setupRealtimeSync();
    } else {
      window.addEventListener('load', setupRealtimeSync);
    }

    // Show sync status
    window.addEventListener('load', () => {
      const indicator = document.createElement('div');
      indicator.id = 'sync-indicator';
      indicator.style.cssText = 'position:fixed;bottom:12px;right:12px;background:#2563eb;color:white;padding:6px 12px;border-radius:20px;font-size:0.75em;z-index:9999;opacity:0;transition:opacity 0.3s';
      indicator.textContent = '☁️ Syncing...';
      document.body.appendChild(indicator);

      window._showSync = (msg, color) => {
        indicator.textContent = msg;
        indicator.style.background = color || '#2563eb';
        indicator.style.opacity = '1';
        setTimeout(() => indicator.style.opacity = '0', 2000);
      };
    });
  </script>

  <!-- Service Worker Registration -->
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('./sw.js')
        .then(() => console.log('SW registered'))
        .catch(e => console.warn('SW error:', e));
    }
  </script>'''

if 'firebase-app.js' not in html:
    html = html.replace('</body>', firebase_code + '\n</body>')
    print('Firebase code added')
else:
    print('Firebase already present')

# Write
tmp = r'C:\Users\sayefate\Desktop\Familien Schulplaner\index_patched.html'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(html)

import os
os.replace(tmp, r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html')
print('Done! index.html updated')
