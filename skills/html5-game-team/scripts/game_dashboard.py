#!/usr/bin/env python3
"""Games Dashboard — playtest + publish console for the html5-game-team bundle.

Views:
  /<token>/                shelf: one card per game-*, status auto-derived
  /<token>/<slug>/         detail: GDD + build report + QA verdict + metrics
  /<token>/<slug>/play     playtest frame (game served from build/)
  /<token>/<slug>/publish  publish runbook + package + zip download
  /<token>/<slug>/mark/<state>[?confirm=1]  human gates: playtested/submitted/live
  /<token>/game/<slug>/... static game files from build/ (ES modules + fetch OK)
  /<token>/agents.json     agents panel fragment, polled every 5s

Status machine, derived from artifacts on disk (no manual config), in
precedence order:
  live.flag > submitted.flag > QA 'VERDICT: FAIL' > playtested.flag >
  ship/package.md > QA 'VERDICT: PASS' > qa/report.md > build/index.html >
  design/*.md > research/pick.md > SETUP
  i.e. SETUP -> RESEARCHED -> DESIGNED -> BUILDING -> QA-FIX -> PLAYTEST ->
       READY -> PLAYTESTED -> SUBMITTED -> LIVE
A QA FAIL outranks a finished package so a post-ship fix loop stays visible.

The three flags are HUMAN gates: only a click on this board writes them.
Agents must never create playtested/submitted/live flags — that forges an
approval nothing downstream can detect.

stdlib only. Token-gated, exposed via cloudflared tunnel. Root is $GAMES_ROOT
or ~/games.
"""
import argparse, glob, html, io, os, re, secrets, subprocess, time, zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.expanduser(os.environ.get('GAMES_ROOT') or '~/games')
AGENTS_DIR = os.path.expanduser(
    os.environ.get('AGENTS_LIVE_DIR') or '~/.hermes/cache/delegation/live')
TOKEN_FILE = os.path.join(ROOT, 'dashboard.token')
MIME = {'.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
        '.css': 'text/css', '.md': 'text/plain; charset=utf-8', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.wav': 'audio/wav',
        '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2'}

def get_token():
    os.makedirs(ROOT, exist_ok=True)
    if not os.path.isfile(TOKEN_FILE):
        open(TOKEN_FILE, 'w').write(secrets.token_urlsafe(18))
    return open(TOKEN_FILE).read().strip()

ROLE_MAP = [('RESEARCH', ('RESEARCH',)), ('DESIGN', ('DESIGN',)), ('BUILD', ('BUILD',)),
            ('QA', ('QA',)), ('ASSET', ('ASSET',)), ('SHIP', ('SHIP',))]

# check.js runs a BFS solver per level: ~60s for 100 levels. The agents panel
# polls every 5s, so running it inline would pile up overlapping node processes
# and stall the server. Cache per slug, keyed on the levels dir mtime so a real
# level change invalidates immediately, with a TTL floor as a backstop.
_VERDICT_CACHE = {}
VERDICT_TTL = 300

def check_verdict(slug):
    """Last line of `node tools/check.js` for a slug. Cached; never shells out
    with an interpolated slug (list args, no shell)."""
    build = os.path.join(ROOT, slug, 'build')
    checker = os.path.join(build, 'tools', 'check.js')
    if not os.path.isfile(checker):
        return 'no checker'
    levels = os.path.join(build, 'levels')
    stamp = os.path.getmtime(levels) if os.path.isdir(levels) else 0
    hit = _VERDICT_CACHE.get(slug)
    if hit and hit['stamp'] == stamp and time.time() - hit['at'] < VERDICT_TTL:
        return hit['verdict']
    try:
        r = subprocess.run(['node', 'tools/check.js'], cwd=build, timeout=180,
                           capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip().splitlines()
        verdict = out[-1].strip() if out else 'no output'
    except subprocess.TimeoutExpired:
        verdict = 'check.js timed out'
    except OSError as e:
        verdict = f'check.js not runnable: {e.__class__.__name__}'
    _VERDICT_CACHE[slug] = {'verdict': verdict, 'stamp': stamp, 'at': time.time()}
    return verdict

def normalize_role(raw):
    raw = (raw or '').upper()
    for role, prefixes in ROLE_MAP:
        if any(raw.startswith(p) for p in prefixes):
            return role
    # compound names like "ASSET DESIGNER", "BUILD-VISUAL", "BUILD-CONTINUATION"
    for role, prefixes in ROLE_MAP:
        if any(p in raw for p in prefixes):
            return role
    return ''

def agent_runs():
    """Newest delegation run per pipeline role -> compact status rows."""
    rows = []
    if not os.path.isdir(AGENTS_DIR):
        return rows
    now = time.time()
    for d in sorted(glob.glob(AGENTS_DIR + '/*'), key=os.path.getmtime, reverse=True):
        for lf in sorted(glob.glob(d + '/task-*.log')):
            try:
                txt = open(lf, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            lines = [l for l in txt.splitlines() if l.strip()]
            if not lines:
                continue
            age = now - os.path.getmtime(lf)
            m = re.search(r'You are (?:the|a) ([A-Za-z][A-Za-z -]*?) role', txt)
            role = normalize_role(m.group(1) if m else '')
            if not role:
                continue
            final = [l for l in lines if re.search(r'\bfinal\s+\|.*status=(\w+)', l)]
            if final:
                m2 = re.search(r'status=(\w+)', final[-1])
                st = 'DONE' if m2 and m2.group(1) == 'completed' else 'FAILED'
            else:
                st = 'RUNNING'
            # last activity line: latest tool call or assistant thought (what it's doing NOW)
            act = ''
            for l in reversed(lines):
                mt = re.match(r'\S+\s+tool\s+\|\s+->\s+(\w+)\((.*)\)\s*$', l)
                ma = re.match(r'\S+\s+assistant\|\s+(.*)$', l)
                if mt:
                    arg = mt.group(2).strip()
                    act = f"{mt.group(1)}: {arg[:70]}…" if len(arg) > 70 else f"{mt.group(1)}: {arg}"
                    break
                if ma:
                    act = ma.group(1)[:80] + ('…' if len(ma.group(1)) > 80 else '')
                    break
            slug = ''
            m = re.search(r'games/([a-z0-9-]+)/', txt)
            if m: slug = m.group(1)
            rows.append({'role': role, 'status': st, 'slug': slug, 'age': int(age), 'mtime': lf and os.path.getmtime(lf), 'act': act})
    # newest per role
    newest = {}
    for r in rows:
        if r['role'] not in newest or r['age'] < newest[r['role']]['age']:
            newest[r['role']] = r
    out = [newest[role] for role, _ in ROLE_MAP if role in newest]
    # PARENT-RUN row: parent-executed work never touches delegation logs, so the
    # board showed a stale BUILD FAILED from a dead child. Surface the parent's
    # own verdict instead: newest build-report.md mtime + last check.js line.
    slugs = {r['slug'] for r in out if r['slug']} or set(games())
    for slug in sorted(slugs):
        rep = os.path.join(ROOT, slug, 'build', 'build-report.md')
        if not os.path.isfile(rep):
            continue
        rep_age = now - os.path.getmtime(rep)
        chk = check_verdict(slug)
        if 'ALL CHECKS PASSED' in chk:
            st, act = 'DONE', f'parent-run: {chk}'
        elif 'FAIL' in chk:
            st, act = 'FAILED', f'parent-run: {chk}'
        else:
            st, act = 'RUNNING', f'parent-run: check.js {chk[:60]}'
        out.append({'role': 'PARENT', 'status': st, 'slug': slug,
                    'age': int(min(rep_age, now)), 'mtime': os.path.getmtime(rep), 'act': act})
    return out

def render_agents(rows):
    if not rows:
        return '<p class=muted>no agent runs yet</p>'
    cls = {'RUNNING': 'live', 'DONE': 'ok', 'FAILED': 'warn'}
    dot = {'RUNNING': '🟢', 'DONE': '✅', 'FAILED': '🔴'}
    out = '<table>'
    for r in sorted(rows, key=lambda x: 0 if x['status'] == 'RUNNING' else 1):
        # age is seconds; days = minutes // 1440 (the old `m // 24` divided minutes
        # by hours-per-day and inflated every day figure 60x: 1.2d showed as "72d")
        m = r['age'] // 60
        age = f"{m // 1440}d" if m >= 1440 else (f"{m // 60}h" if m >= 90 else f"{m}m")
        act = html.escape(r.get('act', ''))
        cell = act if act else '<span class=muted>—</span>'
        out += (f"<tr><td>{dot.get(r['status'], '⚪')} <b>{r['role']}</b></td>"
                f"<td><span class='chip {cls.get(r['status'], 'wip')}'>{r['status']}</span></td>"
                f"<td>{html.escape(r['slug'])}</td>"
                f"<td class=act>{cell}</td><td class=muted>{age} ago</td></tr>")
    out += '</table><p class=muted>🟢 working · ✅ done · 🔴 failed — live 5s</p>'
    return out

def games():
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, '*'))):
        slug = os.path.basename(d)
        # research/* counts too, else a game whose only artifact is pick.md is
        # invisible on the shelf and the RESEARCHED state is unreachable
        if os.path.isdir(d) and (glob.glob(d + '/research/*') or
                                 glob.glob(d + '/design/*') or glob.glob(d + '/build/*')):
            out.append(slug)
    return out

def read1(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return ''

def game_status(slug):
    d = os.path.join(ROOT, slug)
    if os.path.isfile(os.path.join(d, 'ship', 'live.flag')):   return 'LIVE'
    if os.path.isfile(os.path.join(d, 'ship', 'submitted.flag')): return 'SUBMITTED'
    qa = read1(os.path.join(d, 'qa', 'report.md'))
    # a FAIL verdict outranks a packaged build: the old order let package.md
    # ratchet the board to READY forever, so a post-Ship fix loop stayed hidden.
    # Already-submitted games keep their flag state (handled above).
    if 'VERDICT: FAIL' in qa: return 'QA-FIX'
    # MEKL's playtest is a mandatory gate but used to leave no trace, so READY
    # meant both "waiting for him to play" and "he approved it". Own flag, own state.
    if os.path.isfile(os.path.join(d, 'ship', 'playtested.flag')): return 'PLAYTESTED'
    if os.path.isfile(os.path.join(d, 'ship', 'package.md')):  return 'READY'
    if 'VERDICT: PASS' in qa: return 'PLAYTEST'
    if os.path.isfile(os.path.join(d, 'qa', 'report.md')):     return 'QA-FIX'
    if os.path.isfile(os.path.join(d, 'build', 'index.html')): return 'BUILDING'
    if glob.glob(os.path.join(d, 'design', '*.md')):           return 'DESIGNED'
    # Research is the pipeline's first stage: without this a finished pick.md
    # still read as SETUP, so the board showed no progress for a whole stage.
    if os.path.isfile(os.path.join(d, 'research', 'pick.md')): return 'RESEARCHED'
    return 'SETUP'

# every state game_status can return needs a chip class — a missing key is a
# KeyError in shelf()/detail(), i.e. a blank dashboard, not a styling glitch
CHIP = {'SETUP': 'wip', 'RESEARCHED': 'wip', 'DESIGNED': 'wip', 'BUILDING': 'wip',
        'QA-FIX': 'warn', 'PLAYTEST': 'ok', 'READY': 'ok', 'PLAYTESTED': 'ok',
        'SUBMITTED': 'ok', 'LIVE': 'live'}

def qa_verdict(slug):
    qa = read1(os.path.join(ROOT, slug, 'qa', 'report.md'))
    if 'VERDICT: PASS' in qa: return 'PASS'
    if 'VERDICT: FAIL' in qa: return 'FAIL'
    return '—'

def game_title(slug):
    gdd = read1(os.path.join(ROOT, slug, 'design', 'gdd.md'))
    m = re.search(r'title:\s*"([^"]+)"', gdd) or re.search(r'# GDD[^"\n]*"([^"]+)"', gdd) or re.search(r'#\s*(.+)', gdd)
    return m.group(1).strip() if m else slug

def build_size(slug):
    total = 0
    b = os.path.join(ROOT, slug, 'build')
    for r, _, fs in os.walk(b):
        for f in fs:
            try: total += os.path.getsize(os.path.join(r, f))
            except OSError: pass
    return total

CSS = """body{background:#101214;color:#d6d6d6;font:15px/1.5 system-ui;margin:0;padding:2rem;max-width:960px;margin-inline:auto}
a{color:#7ab8ff;text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.3rem}h2{font-size:1.05rem;margin-top:1.6rem}
.card{border:1px solid #2a2f36;border-radius:10px;padding:14px 16px;margin:12px 0;background:#16191d}
.card-hd{display:flex;justify-content:space-between;align-items:center}
.chip{padding:2px 10px;border-radius:999px;font-size:.75rem;font-weight:600}
.wip{background:#3a3320;color:#ffd479}.warn{background:#3a2020;color:#ff9c9c}
.ok{background:#1d3324;color:#8fe3a3}.live{background:#173a3a;color:#7ee7e7}
pre{background:#0c0e10;border:1px solid #22262b;border-radius:8px;padding:10px;overflow:auto;font-size:.82rem}
code{background:#0c0e10;padding:1px 5px;border-radius:4px;font-size:.85em}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #2a2f36;padding:4px 8px;text-align:left;font-size:.85rem}
.act{font-size:.8rem;color:#b8bfc7;max-width:340px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.btn{display:inline-block;background:#1d3324;color:#8fe3a3;padding:6px 14px;border-radius:8px;margin:4px 4px 0 0;font-weight:600}
.btn.warn{background:#3a2020;color:#ff9c9c}
iframe{width:100%;height:78vh;border:1px solid #2a2f36;border-radius:10px;background:#000}
.muted{color:#8a9097;font-size:.85rem}footer{margin-top:3rem;color:#5a6067;font-size:.8rem}"""

def page(body, tok):
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>games dashboard</title><style>{CSS}</style>
<body><h1>🎮 games dashboard</h1>{body}
<footer>html5-game-team console · token-gated · <a href="/{tok}/">shelf</a></footer>"""

def md(text):
    text = html.escape(text)
    text = re.sub(r'```(.*?)```', lambda m: '<pre>' + m.group(1).strip() + '</pre>', text, flags=re.S)
    text = re.sub(r'^###### (.*)$', r'<h6>\1</h6>', text, flags=re.M)
    text = re.sub(r'^##### (.*)$', r'<h5>\1</h5>', text, flags=re.M)
    text = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', text, flags=re.M)
    text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', text, flags=re.M)
    text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', text, flags=re.M)
    text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', text, flags=re.M)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'^[-*] (.*)$', r'&nbsp;• \1', text, flags=re.M)
    text = re.sub(r'^\|(.+)\|$', lambda m: '<pre>' + m.group(1).replace('|', ' | ') + '</pre>', text, flags=re.M)
    return '<p>' + re.sub(r'\n{2,}', '</p><p>', text) + '</p>'

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype='text/html; charset=utf-8'):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        tok = get_token()
        parts = [p for p in self.path.split('?')[0].split('/') if p]
        qs = dict(p.split('=', 1) for p in self.path.split('?')[1].split('&') if '=' in p) if '?' in self.path else {}
        if not parts or parts[0] != tok:
            return self._send(404, 'not found')
        p = parts[1:]
        if not p:
            body = self.shelf(tok)
            htmlout = page(body + "<h2>Agents</h2><div id=agents><p class=muted>loading…</p></div>", tok).replace(
                '</footer>', """<script>
// absolute token path: location.pathname has no trailing slash when the shelf is
// opened as /<token>, so pathname + 'agents.json' built '/<token>agents.json',
// which failed the token check and painted the 404 body ("not found") into the panel.
const AGENTS_URL = '/__TOK__/agents.json';
const poll = () => fetch(AGENTS_URL).then(r => {
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.text();
}).then(t => {
  document.getElementById('agents').innerHTML = t;
}).catch(e => {
  document.getElementById('agents').innerHTML =
    '<p class=muted>agents unavailable (' + e.message + ') — retrying</p>';
});
poll(); setInterval(poll, 5000);
</script><span id=endfoot></span><footer>""".replace('__TOK__', tok))
            return self._send(200, htmlout)
        if p == ['agents.json']:
            rows = agent_runs()
            return self._send(200, render_agents(rows))
        slug = p[0] if p[0] in games() else None
        if slug and len(p) == 1:
            return self._send(200, page(self.detail(tok, slug), tok))
        if slug and len(p) == 2 and p[1] == 'play':
            return self._send(200, page(self.play(tok, slug), tok))
        if slug and len(p) == 2 and p[1] == 'publish':
            return self._send(200, page(self.publish(tok, slug), tok))
        if slug and len(p) == 3 and p[1] == 'mark':
            return self._send(200, page(self.mark(tok, slug, p[2], qs), tok))
        if len(p) >= 3 and p[0] == 'raw' and p[1] in games():
            return self.serve_raw(tok, p[1], '/'.join(p[2:]))
        if len(p) >= 2 and p[0] == 'game':
            return self.serve_game(tok, p[1], '/'.join(p[2:]))
        if slug and len(p) == 3 and p[1] == 'dl':
            return self.serve_zip(tok, slug)
        self._send(404, 'not found')

    def shelf(self, tok):
        rows = ''
        for s in games():
            st = game_status(s)
            rows += f"""<div class=card><div class=card-hd><h2><a href="/{tok}/{s}/">{html.escape(game_title(s))}</a></h2>
<span class="chip {CHIP[st]}">{st}</span></div>
<p class=muted>{s} · {build_size(s)//1024} KB · QA: {qa_verdict(s)}</p>
<p><a class=btn href="/{tok}/{s}/play">▶ playtest</a><a class=btn href="/{tok}/{s}/publish">⬆ publish</a><a class=btn href="/{tok}/{s}/">📄 detail</a></p></div>"""
        return rows or '<p class=muted>no games yet — run the html5-game-team pipeline</p>'

    def detail(self, tok, slug):
        d = os.path.join(ROOT, slug)
        st = game_status(slug)
        gdd = read1(os.path.join(d, 'design', 'gdd.md'))
        rep = read1(os.path.join(d, 'build', 'build-report.md'))
        qa = read1(os.path.join(d, 'qa', 'report.md'))
        met = read1(os.path.join(d, 'metrics', 'log.csv'))
        v = qa_verdict(slug)
        body = f"""<div class=card><div class=card-hd><h2>{html.escape(game_title(slug))} <span class=muted>({slug})</span></h2>
<span class="chip {CHIP[st]}">{st}</span></div>
<p><a class=btn href="/{tok}/{slug}/play">▶ playtest</a><a class=btn href="/{tok}/{slug}/publish">⬆ publish</a>
<a class=btn href="/{tok}/game/{slug}/" target=_blank>⛶ fullscreen</a><a class=btn href="/{tok}/{slug}/dl/build.zip">⬇ build.zip</a></p>
<p class=muted>size {build_size(slug)//1024} KB · QA verdict: <b>{v}</b></p></div>
<h2>GDD</h2>{md(gdd) if gdd else '<p class=muted>no GDD yet</p>'}
<h2>Build report</h2>{md(rep) if rep else '<p class=muted>no build report yet</p>'}
<h2>QA report</h2>{md(qa) if qa else '<p class=muted>no QA report yet</p>'}"""
        adir = os.path.join(d, 'assets-out')
        if os.path.isdir(adir):
            imgs = ''.join(
                f'<a href="/{tok}/raw/{slug}/{os.path.basename(f)}"><img src="/{tok}/raw/{slug}/{os.path.basename(f)}" style="max-width:280px;border-radius:8px;margin:4px"></a>'
                for f in sorted(glob.glob(adir + '/*.png')))
            ana = read1(os.path.join(adir, 'analysis.md'))
            body += f"<h2>Assets</h2><div>{imgs}</div>{md(ana) if ana else ''}"
        body += f"""
<h2>Metrics</h2><pre>{html.escape(met) if met else 'no metrics yet — paste portal numbers post-launch'}</pre>"""
        return body

    def play(self, tok, slug):
        qa = read1(os.path.join(ROOT, slug, 'qa', 'report.md'))
        m = re.search(r'# Playtest.*?(?=## |\Z)', qa, re.S) or ''
        checklist = md(m.strip()) if m.strip() else ''
        return f"""<div class=card><div class=card-hd><h2>▶ playtest — {html.escape(game_title(slug))}</h2>
<span class="chip ok">{game_status(slug)}</span></div>
<p><a class=btn href="/{tok}/game/{slug}/" target=_blank>⛶ open fullscreen (better)</a>
<a class=btn href="/{tok}/{slug}/">📄 back to detail</a>
{'<a class=btn href="/' + tok + '/' + slug + '/mark/playtested?confirm=1">✅ playtest OK → unlock submit</a>' if game_status(slug) == 'READY' else ''}</p></div>
<iframe src="/{tok}/game/{slug}/"></iframe>
<div class=card><h2>What to check</h2>{checklist or '<p class=muted>L1 teaches without text · undo after first exit · last level finishable · a level either side of a difficulty jump · rotate window mid-game · sound toggle</p>'}</div>"""

    def publish(self, tok, slug):
        d = os.path.join(ROOT, slug)
        pkg = read1(os.path.join(d, 'ship', 'package.md'))
        run = read1(os.path.join(d, 'ship', 'runbook.md'))
        st = game_status(slug)
        flags = ''
        if st == 'READY':
            # submit stays locked until MEKL's playtest is recorded — the whole
            # point of the gate is that packaging readiness is not quality approval
            flags = (f'<a class=btn href="/{tok}/{slug}/play">▶ playtest first</a>'
                     '<span class=muted> submit unlocks after your playtest verdict</span>')
        elif st == 'PLAYTESTED':
            flags = f'<a class=btn href="/{tok}/{slug}/mark/submitted?confirm=1">✅ mark SUBMITTED</a>'
        elif st == 'SUBMITTED':
            flags = f'<a class=btn href="/{tok}/{slug}/mark/live?confirm=1">🟢 mark LIVE</a>'
        return f"""<div class=card><div class=card-hd><h2>⬆ publish — {html.escape(game_title(slug))}</h2>
<span class="chip {CHIP[st]}">{st}</span></div>
<p><a class=btn href="/{tok}/{slug}/dl/build.zip">⬇ download build.zip</a><a class=btn href="/{tok}/{slug}/">📄 back</a></p>
<p class=muted>uploads happen on the portal (CrazyGames dev portal) with MEKL's account — this page packages everything</p>
<p>{flags}</p></div>
<h2>Package (copy-paste fields)</h2>{md(pkg) if pkg else '<p class=muted>no ship/package.md yet — run the Ship role</p>'}
<h2>Runbook</h2>{md(run) if run else '<p class=muted>no ship/runbook.md yet</p>'}"""

    def mark(self, tok, slug, state, qs):
        # playtested = MEKL's quality gate; submitted/live = his portal actions.
        # All three are MEKL-only transitions, which is why they live behind a
        # confirm click on the board and are never written by an agent.
        if state not in ('playtested', 'submitted', 'live'):
            return self._send(404, 'bad state')
        d = os.path.join(ROOT, slug, 'ship')
        if 'confirm' not in qs:
            return self._send(200, page(f"<div class=card><h2>Mark {slug} as {state.upper()}?</h2>"
                f"<a class=btn href=\"?confirm=1\">confirm</a> <a class=btn href=\"/{tok}/{slug}/publish\">cancel</a></div>", tok))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, state + '.flag'), 'w').write(time.strftime('%Y-%m-%d %H:%M %Z'))
        return self._send(200, page(
            f"<div class=card>Marked {slug} → {state.upper()}. <a href=\"/{tok}/{slug}/publish\">back</a></div>", tok))

    def serve_game(self, tok, slug, rel):
        base = os.path.realpath(os.path.join(ROOT, slug, 'build'))
        full = os.path.realpath(os.path.join(base, rel or 'index.html'))
        if not full.startswith(base + os.sep) and full != base:
            return self._send(403, 'forbidden')
        if not os.path.isfile(full):
            rel2 = os.path.join(rel or '', 'index.html')
            full = os.path.join(base, rel2)
            if not os.path.isfile(full):
                return self._send(404, 'missing')
        ext = os.path.splitext(full)[1].lower()
        ctype = MIME.get(ext, 'application/octet-stream')
        body = open(full, 'rb').read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_raw(self, tok, slug, rel):
        base = os.path.realpath(os.path.join(ROOT, slug, 'assets-out'))
        full = os.path.realpath(os.path.join(base, rel))
        if not full.startswith(base + os.sep) or not os.path.isfile(full):
            return self._send(404, 'missing')
        ext = os.path.splitext(full)[1].lower()
        body = open(full, 'rb').read()
        self.send_response(200)
        self.send_header('Content-Type', MIME.get(ext, 'application/octet-stream'))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_zip(self, tok, slug):
        base = os.path.join(ROOT, slug, 'build')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
            for r, _, fs in os.walk(base):
                for f in fs:
                    fp = os.path.join(r, f)
                    z.write(fp, os.path.relpath(fp, base))
        body = buf.getvalue()
        self.send_response(200)
        self.send_header('Content-Type', 'application/zip')
        self.send_header('Content-Disposition', f'attachment; filename="{slug}-build.zip"')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    global ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8792)
    ap.add_argument('--root', default=ROOT)
    a = ap.parse_args()
    ROOT = a.root
    tok = get_token()
    srv = ThreadingHTTPServer(('127.0.0.1', a.port), H)
    print(f'games dashboard on :{a.port}, token {tok[:6]}..., root {ROOT}', flush=True)
    srv.serve_forever()

if __name__ == '__main__':
    main()
