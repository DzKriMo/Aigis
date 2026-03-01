from pathlib import Path

from fastapi import APIRouter, Response
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter()
LOGO_PATH = Path(__file__).resolve().parents[3] / "logo.png"


@router.get("/dashboard/logo.png")
def dashboard_logo():
    if not LOGO_PATH.exists():
        return Response(status_code=404)
    return FileResponse(LOGO_PATH, media_type="image/png")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html_doc = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Aegis Control Center</title>
        <style>
          :root {
            --bg: #070b14;
            --ink: #e6eefb;
            --muted: #92a3c4;
            --panel: #0f1626d9;
            --panel-solid: #111a2d;
            --line: #24324a;
            --primary: #38bdf8;
            --primary-ink: #082033;
            --ok: #34d399;
            --warn: #f59e0b;
            --danger: #f87171;
            --shadow: 0 14px 30px rgba(0, 0, 0, 0.42);
          }

          * { box-sizing: border-box; }

          body {
            margin: 0;
            color: var(--ink);
            font-family: "Space Grotesk", "IBM Plex Sans", "Segoe UI", sans-serif;
            background:
              radial-gradient(900px 500px at -10% -10%, #123456 0%, transparent 60%),
              radial-gradient(1000px 600px at 110% 0%, #10233f 0%, transparent 60%),
              linear-gradient(180deg, #060b16 0%, #0b1220 100%);
            min-height: 100vh;
          }

          .topbar {
            position: sticky;
            top: 0;
            z-index: 20;
            backdrop-filter: blur(12px);
            background: #0a1222cc;
            border-bottom: 1px solid var(--line);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
          }

          .brand { display: flex; align-items: center; gap: 10px; }
          .logo {
            width: 30px;
            height: 30px;
            border-radius: 10px;
            background: url('/v1/dashboard/logo.png') center/cover no-repeat;
            border: 1px solid #314768;
            box-shadow: 0 8px 14px rgba(0, 0, 0, 0.35);
            animation: pulse 2.8s infinite;
          }

          @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.08); }
          }

          .brand h1 {
            margin: 0;
            font-size: 18px;
            letter-spacing: 0.2px;
          }

          .status {
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 12px;
            background: #111a2d;
          }

          .topbar-right { display: flex; gap: 8px; align-items: center; }

          .btn {
            border: 1px solid var(--line);
            background: #111a2d;
            color: var(--ink);
            border-radius: 10px;
            padding: 8px 12px;
            cursor: pointer;
            font-weight: 600;
          }

          .btn.primary {
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            border-color: #0ea5e9;
            color: #04253c;
          }

          .shell {
            max-width: 1360px;
            margin: 0 auto;
            padding: 14px;
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 14px;
          }

          .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: var(--shadow);
          }

          .sidebar {
            padding: 12px;
            display: flex;
            flex-direction: column;
            min-height: calc(100vh - 90px);
            max-height: calc(100vh - 90px);
          }

          .content {
            padding: 12px;
            min-height: calc(100vh - 90px);
          }

          .section-title {
            margin: 8px 0;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--muted);
            font-weight: 700;
          }

          .input, .select {
            width: 100%;
            padding: 9px 10px;
            border-radius: 10px;
            border: 1px solid var(--line);
            background: #0d1527;
            color: var(--ink);
          }

          .stack-sm { height: 8px; }
          .stack-md { height: 14px; }

          .sessions {
            overflow: auto;
            flex: 1;
            padding-right: 2px;
          }

          .session {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--panel-solid);
            padding: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
          }

          .session:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(0, 0, 0, 0.34);
          }

          .session.active {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px #1b3b5c;
          }

          .session .meta {
            margin-top: 4px;
            color: var(--muted);
            font-size: 12px;
          }

          .grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
          }

          .kpi {
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 10px;
            background: var(--panel-solid);
          }

          .kpi .label {
            color: var(--muted);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
          }

          .kpi .value {
            margin-top: 6px;
            font-size: 20px;
            font-weight: 700;
          }

          .row {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 10px;
            margin-top: 10px;
          }

          .box {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--panel-solid);
            padding: 10px;
          }

          .inline {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
          }

          .pill {
            border: 1px solid var(--line);
            background: #0d1527;
            border-radius: 999px;
            padding: 3px 8px;
            font-size: 11px;
          }

          .pill.ok { color: #5eead4; border-color: #1f6a5f; background: #0b2626; }
          .pill.warn { color: #fbbf24; border-color: #75470f; background: #2a1b08; }
          .pill.block { color: #fca5a5; border-color: #7f1d1d; background: #2a1111; }

          .timeline {
            margin-top: 10px;
            display: grid;
            gap: 8px;
            max-height: 62vh;
            overflow: auto;
            padding-right: 2px;
          }

          .event {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: #101a2e;
            overflow: hidden;
          }

          .event-head {
            padding: 9px 10px;
            border-bottom: 1px solid var(--line);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
          }

          .event-left {
            display: flex;
            gap: 8px;
            align-items: center;
          }

          .tag {
            font-size: 11px;
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 2px 7px;
            background: #0d1527;
          }

          .tag.block { border-color: #7f1d1d; background: #2a1111; color: #fca5a5; }
          .tag.warn { border-color: #75470f; background: #2a1b08; color: #fbbf24; }
          .tag.ok { border-color: #1f6a5f; background: #0b2626; color: #5eead4; }

          .event pre {
            margin: 0;
            padding: 10px;
            background: #0b1220;
            border-top: 1px solid var(--line);
            max-height: 320px;
            overflow: auto;
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 12px;
            color: #c7d6f0;
          }

          .event pre.hidden { display: none; }

          .composer {
            margin-top: 10px;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: #0f1729;
            padding: 10px;
          }

          .textarea {
            width: 100%;
            min-height: 92px;
            resize: vertical;
            padding: 10px;
            border: 1px solid var(--line);
            border-radius: 10px;
            font-family: "IBM Plex Mono", Consolas, monospace;
            font-size: 13px;
            color: var(--ink);
            background: #0b1220;
          }

          .terminal {
            margin-top: 8px;
            padding: 10px;
            border: 1px solid var(--line);
            border-radius: 10px;
            background: #0f172a;
            color: #dbeafe;
            min-height: 84px;
            max-height: 220px;
            overflow: auto;
            white-space: pre-wrap;
            word-break: break-word;
            font-family: "IBM Plex Mono", Consolas, monospace;
            font-size: 12px;
          }

          .empty {
            padding: 16px;
            text-align: center;
            color: var(--muted);
          }

          .tiny { color: var(--muted); font-size: 12px; }

          @media (max-width: 1100px) {
            .shell { grid-template-columns: 1fr; }
            .sidebar { min-height: auto; max-height: none; }
            .row { grid-template-columns: 1fr; }
            .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          }

          @media (max-width: 680px) {
            .topbar { padding: 12px; }
            .brand h1 { font-size: 16px; }
            .grid { grid-template-columns: 1fr; }
          }
        </style>
      </head>
      <body>
        <header class="topbar">
          <div class="brand">
            <div class="logo"></div>
            <h1>Aegis Guardrail Control Center</h1>
          </div>
          <div class="topbar-right">
            <span class="status" id="status">Disconnected</span>
            <button class="btn" onclick="refreshAll()">Refresh</button>
          </div>
        </header>

        <div class="shell">
          <aside class="panel sidebar">
            <div class="section-title">Access</div>
            <input id="apiKey" class="input" placeholder="x-api-key" />
            <div class="stack-sm"></div>
            <button class="btn primary" onclick="saveKey()">Save Key</button>
            <div class="stack-md"></div>

            <div class="section-title">Sessions</div>
            <input id="sessionSearch" class="input" placeholder="Search session id" oninput="renderSessions()" />
            <div class="stack-sm"></div>
            <div id="sessions" class="sessions"></div>
          </aside>

          <main class="panel content">
            <section class="grid">
              <article class="kpi"><div class="label">Selected Session</div><div class="value" id="sessionId">None</div></article>
              <article class="kpi"><div class="label">Events</div><div class="value" id="eventCount">0</div></article>
              <article class="kpi"><div class="label">Risk Events</div><div class="value" id="riskCount">0</div></article>
              <article class="kpi"><div class="label">Last Update</div><div class="value" id="lastUpdate">-</div></article>
            </section>

            <section class="row">
              <div class="box">
                <div class="section-title">Event Stream</div>
                <div class="inline">
                  <select id="stageFilter" class="select" style="max-width:220px" onchange="renderEvents()">
                    <option value="">All stages</option>
                    <option value="prellm">prellm</option>
                    <option value="postllm">postllm</option>
                    <option value="tool_pre">tool_pre</option>
                    <option value="tool_exec">tool_exec</option>
                    <option value="tool_post">tool_post</option>
                    <option value="llm_classification">llm_classification</option>
                    <option value="prellm.network">prellm.network</option>
                  </select>
                  <input id="eventSearch" class="input" style="max-width:280px" placeholder="Search event JSON" oninput="renderEvents()" />
                  <label class="tiny"><input type="checkbox" id="autoRefresh" checked onchange="toggleAutoRefresh()" /> live</label>
                  <span class="tiny" id="autoRefreshInfo">10s</span>
                </div>
                <div id="events" class="timeline"></div>
                <div class="composer">
                  <div class="section-title">Test Guarded Message</div>
                  <textarea id="testMessage" class="textarea" placeholder="Type a user message to run through Aegis guardrails..."></textarea>
                  <div class="stack-sm"></div>
                  <div class="inline">
                    <button class="btn primary" id="sendTestBtn" onclick="sendTestMessage()">Send To Guardrail</button>
                    <span class="tiny" id="testState">idle</span>
                  </div>
                  <pre id="testResponse" class="terminal">No test requests yet.</pre>
                </div>
              </div>

              <div class="box">
                <div class="section-title">Risk Snapshot</div>
                <div class="inline">
                  <span class="pill ok" id="okCount">ok: 0</span>
                  <span class="pill warn" id="warnCount">warn: 0</span>
                  <span class="pill block" id="blockCount">block: 0</span>
                </div>
                <div class="stack-md"></div>
                <div class="section-title">LLM Classification</div>
                <div id="llmTags" class="tiny">No LLM classifications yet</div>
                <div class="stack-sm"></div>
                <div id="llmTime" class="tiny"></div>
                <div id="llmErr" class="tiny"></div>
              </div>
            </section>
          </main>
        </div>

        <script>
          const apiBase = '/v1';
          let currentSession = null;
          let sessionData = null;
          let sessionList = [];
          let autoRefreshTimer = null;

          function getKey() {
            return localStorage.getItem('aegis_api_key') || '';
          }

          function setStatus(ok, msg) {
            const el = document.getElementById('status');
            el.textContent = msg || (ok ? 'Connected' : 'Disconnected');
            if (ok) {
              el.style.color = '#5eead4';
              el.style.background = '#0b2626';
              el.style.borderColor = '#1f6a5f';
            } else {
              el.style.color = '#fca5a5';
              el.style.background = '#2a1111';
              el.style.borderColor = '#7f1d1d';
            }
          }

          function saveKey() {
            const key = document.getElementById('apiKey').value.trim();
            localStorage.setItem('aegis_api_key', key);
            refreshAll();
          }

          async function api(path, options = {}) {
            const key = getKey();
            const headers = Object.assign({}, options.headers || {}, {'x-api-key': key});
            const res = await fetch(apiBase + path, { ...options, headers });
            if (!res.ok) {
              throw new Error('API error: ' + res.status);
            }
            return res.json();
          }

          function normalizeTs(ts) {
            if (!ts) return "";
            try {
              return new Date(ts * 1000).toLocaleString();
            } catch {
              return "";
            }
          }

          function renderSessions() {
            const el = document.getElementById('sessions');
            const query = (document.getElementById('sessionSearch').value || '').toLowerCase();
            const list = sessionList.filter(s => !query || (s.id || '').toLowerCase().includes(query));
            el.innerHTML = '';
            if (!list.length) {
              el.innerHTML = '<div class="empty">No matching sessions</div>';
              return;
            }
            list.forEach(s => {
              const div = document.createElement('div');
              div.className = 'session' + (s.id === currentSession ? ' active' : '');
              div.innerHTML = `<div>${s.id}</div><div class="meta">${s.events} events</div>`;
              div.onclick = () => selectSession(s.id);
              el.appendChild(div);
            });
          }

          async function loadSessions() {
            try {
              const data = await api('/sessions');
              setStatus(true);
              sessionList = data.sessions || [];
              renderSessions();
            } catch (e) {
              setStatus(false, 'Invalid key');
              sessionList = [];
              renderSessions();
            }
          }

          async function selectSession(id) {
            currentSession = id;
            document.getElementById('sessionId').textContent = id;
            await loadSessionDetail();
            renderSessions();
          }

          async function ensureSession() {
            if (currentSession) return currentSession;
            const created = await api('/sessions', { method: 'POST' });
            currentSession = created.session_id;
            document.getElementById('sessionId').textContent = currentSession;
            await loadSessions();
            return currentSession;
          }

          function computeRisk(events) {
            let ok = 0;
            let warn = 0;
            let block = 0;
            for (const e of events) {
              const d = e.decision || {};
              if (d.blocked) block += 1;
              else if (d.warn || d.require_approval) warn += 1;
              else ok += 1;
            }
            return { ok, warn, block };
          }

          function renderRiskSnapshot(events) {
            const { ok, warn, block } = computeRisk(events);
            document.getElementById('okCount').textContent = `ok: ${ok}`;
            document.getElementById('warnCount').textContent = `warn: ${warn}`;
            document.getElementById('blockCount').textContent = `block: ${block}`;
            document.getElementById('riskCount').textContent = String(warn + block);
          }

          function renderLLM() {
            const el = document.getElementById('llmTags');
            const timeEl = document.getElementById('llmTime');
            const errEl = document.getElementById('llmErr');
            const events = (sessionData?.events || []).filter(e => e.stage === 'llm_classification');
            if (!events.length) {
              el.innerHTML = 'No LLM classifications yet';
              timeEl.textContent = '';
              errEl.textContent = '';
              return;
            }
            const latest = events[events.length - 1];
            const cls = latest.classification || {};
            const tags = Object.keys(cls).map(k => {
              const val = cls[k];
              let clsName = 'pill';
              if (k === '__error__') clsName += ' block';
              else if (val === true) clsName += ' warn';
              return `<span class="${clsName}">${k}${val === true ? ':true' : ''}</span>`;
            });
            const hasAlerts = Object.keys(cls).some(k => !k.startsWith('__') && cls[k] === true);
            el.innerHTML = (hasAlerts ? '<span class="pill warn">!!</span> ' : '') + tags.join(' ');
            const llmTs = latest.ts_readable || normalizeTs(latest.ts);
            timeEl.textContent = llmTs ? "LLM time: " + llmTs : "";
            if (cls.__error__) {
              errEl.textContent = 'LLM error: ' + cls.__error__;
            } else if (cls.__raw__) {
              errEl.textContent = 'LLM raw: ' + String(cls.__raw__).slice(0, 180);
            } else {
              errEl.textContent = '';
            }
          }

          function renderEvents() {
            const el = document.getElementById('events');
            const all = sessionData?.events || [];
            const stageFilter = document.getElementById('stageFilter').value;
            const query = (document.getElementById('eventSearch').value || '').toLowerCase();

            let filtered = all.filter(e => !stageFilter || (e.stage || '').startsWith(stageFilter));
            if (query) {
              filtered = filtered.filter(e => JSON.stringify(e).toLowerCase().includes(query));
            }

            if (!filtered.length) {
              el.innerHTML = '<div class="empty">No events match current filters</div>';
              return;
            }

            el.innerHTML = '';
            filtered.slice().reverse().forEach((e, idx) => {
              const div = document.createElement('article');
              div.className = 'event';
              const d = e.decision || {};
              let tag = '<span class="tag ok">ok</span>';
              if (e.stage === 'llm_classification') {
                const cls = e.classification || {};
                const llmErr = Boolean(cls.__error__);
                const llmPositive = Object.keys(cls).some(k => !k.startsWith('__') && cls[k] === true);
                if (llmErr) tag = '<span class="tag block">llm error</span>';
                else if (llmPositive) tag = '<span class="tag warn">llm !!</span>';
                else tag = '<span class="tag ok">llm ok</span>';
              } else if (d.blocked) tag = '<span class="tag block">block</span>';
              else if (d.warn || d.require_approval) tag = '<span class="tag warn">warn</span>';
              const time = e.ts_readable || normalizeTs(e.ts);
              const preId = `ev_${idx}`;

              div.innerHTML = `
                <div class="event-head" onclick="toggleEvent('${preId}')">
                  <div class="event-left">
                    <strong>${e.stage || 'event'}</strong>
                    ${tag}
                    <span class="tiny">${time}</span>
                  </div>
                  <span class="tiny">toggle</span>
                </div>
                <pre id="${preId}" class="hidden">${JSON.stringify(e, null, 2)}</pre>
              `;
              el.appendChild(div);
            });
          }

          function toggleEvent(id) {
            const el = document.getElementById(id);
            if (!el) return;
            el.classList.toggle('hidden');
          }

          async function loadSessionDetail() {
            if (!currentSession) return;
            try {
              const data = await api(`/sessions/${currentSession}`);
              sessionData = data;
              const events = data.events || [];
              document.getElementById('eventCount').textContent = String(events.length);
              document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
              renderRiskSnapshot(events);
              renderEvents();
              renderLLM();
            } catch (e) {
              setStatus(false, 'Fetch error');
            }
          }

          async function refreshAll() {
            await loadSessions();
            if (currentSession) {
              await loadSessionDetail();
            }
          }

          async function sendTestMessage() {
            const btn = document.getElementById('sendTestBtn');
            const state = document.getElementById('testState');
            const out = document.getElementById('testResponse');
            const content = (document.getElementById('testMessage').value || '').trim();
            if (!content) {
              state.textContent = 'message required';
              return;
            }

            btn.disabled = true;
            state.textContent = 'sending...';
            try {
              const sessionId = await ensureSession();
              const payload = {
                content,
                metadata: { source: 'dashboard_test' },
                environment: 'dev',
              };
              const res = await api(`/sessions/${sessionId}/messages`, {
                method: 'POST',
                headers: { 'content-type': 'application/json' },
                body: JSON.stringify(payload),
              });
              out.textContent = JSON.stringify(res, null, 2);
              state.textContent = 'done';
              await loadSessionDetail();
              await loadSessions();
            } catch (e) {
              out.textContent = `Request failed: ${String(e)}`;
              state.textContent = 'failed';
            } finally {
              btn.disabled = false;
            }
          }

          function stopAutoRefresh() {
            if (autoRefreshTimer) {
              clearInterval(autoRefreshTimer);
              autoRefreshTimer = null;
            }
          }

          function startAutoRefresh() {
            stopAutoRefresh();
            autoRefreshTimer = setInterval(async () => {
              await refreshAll();
            }, 10000);
          }

          function toggleAutoRefresh() {
            const checked = document.getElementById('autoRefresh').checked;
            document.getElementById('autoRefreshInfo').textContent = checked ? '10s' : 'off';
            if (checked) startAutoRefresh();
            else stopAutoRefresh();
          }

          document.getElementById('apiKey').value = getKey();
          refreshAll();
          startAutoRefresh();
          window.toggleEvent = toggleEvent;
          window.sendTestMessage = sendTestMessage;
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html_doc)


