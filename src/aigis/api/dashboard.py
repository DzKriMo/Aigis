from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html_doc = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Aigis Dashboard</title>
        <style>
          :root {
            --bg: #0b0f14;
            --panel: #111827;
            --panel-2: #0f172a;
            --text: #e5e7eb;
            --muted: #94a3b8;
            --accent: #38bdf8;
            --accent-2: #22c55e;
            --danger: #ef4444;
            --warn: #f59e0b;
            --border: #1f2937;
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            font-family: "Segoe UI", system-ui, sans-serif;
            background: radial-gradient(1200px 600px at 10% 0%, #0f172a 0%, #0b0f14 50%, #070a0f 100%);
            color: var(--text);
          }
          header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            background: rgba(10, 14, 20, 0.8);
            position: sticky;
            top: 0;
            z-index: 10;
          }
          header h1 { margin: 0; font-size: 18px; letter-spacing: 0.5px; }
          header .right { display: flex; gap: 10px; align-items: center; }
          .pill { font-size: 12px; padding: 4px 8px; border-radius: 999px; border: 1px solid var(--border); color: var(--muted); }

          .layout { display: grid; grid-template-columns: 300px 1fr; height: calc(100vh - 58px); }
          .sidebar {
            border-right: 1px solid var(--border);
            background: var(--panel);
            padding: 14px;
            overflow: auto;
          }
          .content {
            padding: 16px;
            overflow: auto;
          }

          .section-title { font-size: 11px; text-transform: uppercase; color: var(--muted); margin: 8px 0; letter-spacing: 1px; }
          .input {
            width: 100%;
            padding: 8px 10px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0b1220;
            color: var(--text);
          }
          .btn {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0b1220;
            color: var(--text);
            cursor: pointer;
          }
          .btn.primary { background: #0ea5e9; border-color: #0ea5e9; color: #001018; }
          .btn.ghost { background: transparent; }

          .session {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            background: var(--panel-2);
          }
          .session.active { outline: 2px solid var(--accent); }
          .session small { color: var(--muted); }

          .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
          .card {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            background: rgba(10, 14, 20, 0.6);
          }

          .toolbar { display: flex; gap: 8px; align-items: center; margin: 12px 0; }
          .toolbar select { background: #0b1220; color: var(--text); border: 1px solid var(--border); padding: 6px; border-radius: 8px; }

          .event {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            background: #0c131d;
          }
          .event .meta { display: flex; gap: 10px; align-items: center; }
          .badge { font-size: 11px; padding: 2px 6px; border-radius: 6px; border: 1px solid var(--border); }
          .badge.block { color: #fecaca; border-color: #7f1d1d; background: #3f0f0f; }
          .badge.warn { color: #fde68a; border-color: #92400e; background: #3b2306; }
          .badge.ok { color: #bbf7d0; border-color: #14532d; background: #0b2213; }
          pre { white-space: pre-wrap; word-break: break-word; color: #cbd5e1; }
          .ts { color: var(--muted); font-size: 12px; }

          .llm-panel {
            border: 1px solid #1b2a3a;
            background: #0b1220;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
          }
          .llm-tag {
            display: inline-block;
            padding: 2px 6px;
            margin: 3px 4px 3px 0;
            border-radius: 6px;
            background: #122033;
            border: 1px solid #1f2a37;
            font-size: 12px;
          }
          .llm-tag.on { background: #1d3b2a; border-color: #14532d; color: #bbf7d0; }
          .llm-tag.err { background: #3b0f0f; border-color: #7f1d1d; color: #fecaca; }

          .empty { color: var(--muted); padding: 16px; text-align: center; }
        </style>
      </head>
      <body>
        <header>
          <h1>Aigis Guardrail Dashboard</h1>
          <div class="right">
            <span class="pill" id="status">disconnected</span>
            <button class="btn ghost" onclick="refreshAll()">Refresh</button>
          </div>
        </header>

        <div class="layout">
          <aside class="sidebar">
            <div class="section-title">API Key</div>
            <input id="apiKey" class="input" placeholder="x-api-key" />
            <div style="height: 8px"></div>
            <button class="btn primary" onclick="saveKey()">Save Key</button>
            <div style="height: 16px"></div>

            <div class="section-title">Sessions</div>
            <div id="sessions"></div>
          </aside>

          <main class="content">
            <div class="stats">
              <div class="card"><div class="section-title">Selected Session</div><div id="sessionId">None</div></div>
              <div class="card"><div class="section-title">Events</div><div id="eventCount">0</div></div>
              <div class="card"><div class="section-title">Last Update</div><div id="lastUpdate">—</div></div>
            </div>

            <div class="toolbar">
              <label>Filter stage:</label>
              <select id="stageFilter" onchange="renderEvents()">
                <option value="">All</option>
                <option value="prellm">prellm</option>
                <option value="postllm">postllm</option>
                <option value="tool_pre">tool_pre</option>
                <option value="tool_exec">tool_exec</option>
                <option value="tool_post">tool_post</option>
                <option value="llm_classification">llm_classification</option>
              </select>
            </div>

            <div class="llm-panel">
              <div class="section-title">LLM Classification (Latest)</div>
              <div id="llmTags" class="muted">No LLM classifications yet</div>
              <div id="llmTime" class="ts"></div>
              <div id="llmErr" class="ts"></div>
            </div>

            <div id="events"></div>
          </main>
        </div>

        <script>
          const apiBase = '/v1';
          let currentSession = null;
          let sessionData = null;

          function getKey() {
            return localStorage.getItem('aigis_api_key') || '';
          }
          function setStatus(ok, msg) {
            const el = document.getElementById('status');
            el.textContent = msg || (ok ? 'connected' : 'disconnected');
            el.style.borderColor = ok ? '#14532d' : '#7f1d1d';
            el.style.color = ok ? '#bbf7d0' : '#fecaca';
            el.style.background = ok ? '#0b2213' : '#3f0f0f';
          }

          function saveKey() {
            const key = document.getElementById('apiKey').value.trim();
            localStorage.setItem('aigis_api_key', key);
            refreshAll();
          }

          async function api(path, options = {}) {
            const key = getKey();
            const headers = Object.assign({}, options.headers || {}, {'x-api-key': key});
            const res = await fetch(apiBase + path, { ...options, headers });
            if (!res.ok) throw new Error('API error: ' + res.status);
            return res.json();
          }

          async function loadSessions() {
            try {
              const data = await api('/sessions');
              setStatus(true);
              const list = data.sessions || [];
              const el = document.getElementById('sessions');
              el.innerHTML = '';
              if (list.length === 0) {
                el.innerHTML = '<div class="empty">No sessions</div>';
                return;
              }
              list.forEach(s => {
                const div = document.createElement('div');
                div.className = 'session' + (s.id === currentSession ? ' active' : '');
                div.innerHTML = `<div>${s.id}</div><small>${s.events} events</small>`;
                div.onclick = () => selectSession(s.id);
                el.appendChild(div);
              });
            } catch (e) {
              setStatus(false, 'invalid key');
            }
          }

          async function selectSession(id) {
            currentSession = id;
            document.getElementById('sessionId').textContent = id;
            await loadSessionDetail();
            await loadSessions();
          }

          async function loadSessionDetail() {
            if (!currentSession) return;
            const data = await api(`/sessions/${currentSession}`);
            sessionData = data;
            document.getElementById('eventCount').textContent = (data.events || []).length;
            document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
            renderEvents();
            renderLLM();
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
              const on = cls[k] ? 'on' : '';
              const err = k === '__error__' ? 'err' : '';
              return `<span class="llm-tag ${on} ${err}">${k}${cls[k] === true ? ':true' : ''}</span>`;
            });
            el.innerHTML = tags.join('');
            if (latest.ts) {
              const d = new Date(latest.ts * 1000);
              timeEl.textContent = 'LLM time: ' + d.toLocaleTimeString();
            }
            if (cls.__error__) {
              errEl.textContent = 'LLM error: ' + cls.__error__;
            } else if (cls.__raw__) {
              errEl.textContent = 'LLM raw: ' + cls.__raw__.slice(0, 160);
            } else {
              errEl.textContent = '';
            }
          }

          function renderEvents() {
            const el = document.getElementById('events');
            if (!sessionData || !(sessionData.events || []).length) {
              el.innerHTML = '<div class="empty">No events yet</div>';
              return;
            }
            const filter = document.getElementById('stageFilter').value;
            const events = (sessionData.events || []).filter(e => !filter || (e.stage || '').startsWith(filter));
            el.innerHTML = '';
            events.forEach(e => {
              const div = document.createElement('div');
              div.className = 'event';
              const decision = e.decision || {};
              const badges = [];
              if (decision.blocked) badges.push('<span class="badge block">block</span>');
              if (decision.warn) badges.push('<span class="badge warn">warn</span>');
              if (!decision.blocked && !decision.warn) badges.push('<span class="badge ok">ok</span>');
              const ts = e.ts ? new Date(e.ts * 1000).toLocaleTimeString() : '';
              div.innerHTML = `
                <div class="meta">
                  <strong>${e.stage || 'event'}</strong>
                  ${badges.join('')}
                  <span class="ts">${ts}</span>
                </div>
                <pre>${JSON.stringify(e, null, 2)}</pre>
              `;
              el.appendChild(div);
            });
          }

          async function refreshAll() {
            await loadSessions();
            if (currentSession) await loadSessionDetail();
          }

          document.getElementById('apiKey').value = getKey();
          refreshAll();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html_doc)
