#!/usr/bin/env python3
"""KDP Dashboard — publish console + book shelf for the kdp-team bundle.

Views:
  /<token>/                shelf: one card per book-*, status auto-derived
  /<token>/<slug>/         book detail: manuscript + publish cards
  /<token>/<slug>/publish  rendered publish runbook
  /<token>/raw/...         whitelisted downloads

Status machine (derived from files, no manual config):
  SETUP -> RESEARCHED -> WRITING -> QA -> READY TO UPLOAD -> LIVE
stdlib only. Token-gated, LAN-oriented.
"""
import argparse, glob, html, os, re, secrets, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote, unquote

ROOT = os.path.expanduser('~/kdp')
TOKEN_FILE = os.path.join(ROOT, 'dashboard.token')
SLUG_RE = re.compile(r'^book-[a-z0-9][a-z0-9-]*$')

def get_token():
    try:
        return open(TOKEN_FILE).read().strip()
    except FileNotFoundError:
        tok = secrets.token_urlsafe(18)
        os.makedirs(ROOT, exist_ok=True)
        open(TOKEN_FILE, 'w').write(tok)
        os.chmod(TOKEN_FILE, 0o600)
        return tok

# ---------- book model ----------

def books():
    out = []
    if not os.path.isdir(ROOT):
        return out
    for d in sorted(os.listdir(ROOT)):
        if d.startswith('book-') and os.path.isdir(os.path.join(ROOT, d)) and SLUG_RE.match(d):
            out.append(d)
    return out

def read1(path):
    try:
        return open(path, encoding='utf-8').read()
    except OSError:
        return ''

def book_stats(slug):
    b = os.path.join(ROOT, slug)
    chaps = sorted(glob.glob(os.path.join(b, 'manuscript/chapters/ch*.md')))
    words = sum(len(read1(f).split()) for f in chaps)
    price, asin = None, None
    for line in read1(os.path.join(b, 'sales/log.csv')).splitlines()[1:]:
        p = [c.strip() for c in line.split(',')]
        if len(p) >= 5:
            if p[3]: price = '$' + p[3].lstrip('$')
            if p[2] and p[2] != 'PENDING': asin = p[2]
    return {'chapters': len(chaps), 'words': words, 'price': price or '—', 'asin': asin}

def book_status(slug):
    b = os.path.join(ROOT, slug)
    st = book_stats(slug)
    if st['asin']:
        return 'LIVE', 'live'
    qa = read1(os.path.join(b, 'qa/report.md'))
    if 'Verdict' in qa and '**PASS**' in qa:
        if os.path.isfile(os.path.join(b, 'manuscript/book.epub')) and os.path.isfile(os.path.join(b, 'cover/cover.jpg')):
            return 'READY TO UPLOAD', 'ready'
    if os.path.isfile(os.path.join(b, 'qa/report.md')):
        return 'IN QA', 'qa'
    if st['chapters'] > 0:
        return ('WRITING' if not os.path.isfile(os.path.join(b, 'manuscript/book.epub')) else 'PACKAGING'), 'writing'
    if os.path.isfile(os.path.join(b, 'research/decision.md')):
        return 'RESEARCHED', 'researched'
    return 'SETUP', 'setup'

def book_title(slug):
    m = re.search(r'\*\*Title:\*\*\s*(.+)', read1(os.path.join(ROOT, slug, 'seo/listing.md')))
    if m: return m.group(1).strip()
    m = re.search(r'^# (KDP Niche Decision[^\n]*)', read1(os.path.join(ROOT, slug, 'research/decision.md')))
    return slug.replace('-', ' ').title()

# ---------- page shell ----------

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KDP Console</title><style>
:root{--teal:#1F5F5B;--teal-d:#16433f;--cream:#FAF5EE;--terra:#D96C47;--gold:#D9A441;
--ink:#232323;--mut:#6b7280;--line:#e7e1d6;--card:#fff;
--green:#1a6b52;--greenbg:#e6f2ee;--amber:#b0501f;--amberbg:#fdf0e7}
*{box-sizing:border-box;margin:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
background:var(--cream);color:var(--ink);line-height:1.55}
.topbar{background:var(--teal);color:#fff;padding:18px 24px;display:flex;align-items:center;gap:12px}
.topbar .logo{width:34px;height:34px;border-radius:8px;background:var(--terra);display:flex;
align-items:center;justify-content:center;font-weight:800;font-size:1rem;flex:none}
.topbar h1{font-size:1.02rem;font-weight:650;letter-spacing:.2px}
.topbar .sub{font-size:.8rem;opacity:.75}
main{max-width:880px;margin:0 auto;padding:28px 20px 60px}
.backlink{display:inline-block;margin-bottom:18px;color:var(--teal-d);text-decoration:none;
font-size:.88rem;font-weight:600}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;
box-shadow:0 1px 3px rgba(35,35,35,.06);overflow:hidden;margin-bottom:26px}
.card-hd{padding:16px 22px;border-bottom:1px solid var(--line);display:flex;
justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.card-hd h2{font-size:.95rem;font-weight:700;color:var(--teal-d);letter-spacing:.3px}
.chip{font-size:.72rem;font-weight:700;letter-spacing:.5px;padding:4px 11px;border-radius:99px;white-space:nowrap}
.chip.live{background:var(--greenbg);color:var(--green);border:1px solid #c4e0d6}
.chip.ready{background:#fdf3d7;color:#8a6100;border:1px solid #eeddA0}
.chip.qa{background:#fdeed6;color:#8a5a00;border:1px solid #f0d9a8}
.chip.writing{background:#e7eef8;color:#2c5aa0;border:1px solid #cad9ef}
.chip.researched{background:#ece9e2;color:#6b6154;border:1px solid #dcd6c9}
.book-grid{display:flex;gap:24px;padding:22px;flex-wrap:wrap}
.cover-box{flex:0 0 168px}
.cover-box img{width:168px;height:auto;border-radius:8px;border:1px solid var(--line);
box-shadow:0 4px 14px rgba(31,95,91,.22);display:block}
.cover-ph{width:168px;aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;
background:linear-gradient(135deg,var(--teal),var(--teal-d));color:#fff;border-radius:8px;
font-weight:800;font-size:1.6rem;letter-spacing:1px}
.book-info{flex:1;min-width:240px;display:flex;flex-direction:column}
.kicker{font-size:.72rem;font-weight:800;letter-spacing:1.2px;color:var(--terra);text-transform:uppercase}
.book-info h3{font-size:1.5rem;line-height:1.2;margin:6px 0 4px;font-weight:750}
.book-info h3 a{color:inherit;text-decoration:none}
.book-info .subtitle{font-size:.92rem;color:var(--mut);margin-bottom:16px}
.stats{display:flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:18px}
.stat{flex:1;text-align:center;padding:10px 4px;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font-size:1.05rem;font-weight:750;color:var(--teal-d)}
.stat span{font-size:.7rem;color:var(--mut);letter-spacing:.4px;text-transform:uppercase}
.dl-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border-radius:9px;
font-size:.9rem;font-weight:650;text-decoration:none;transition:filter .15s}
.btn:hover{filter:brightness(1.08)}
.btn.primary{background:var(--terra);color:#fff;box-shadow:0 2px 8px rgba(217,108,71,.35)}
.btn.ghost{background:#fff;color:var(--teal-d);border:1.5px solid var(--teal)}
.btn.small{padding:7px 13px;font-size:.82rem}
.sec-note{font-size:.8rem;color:var(--mut);padding:0 22px 18px}
.doc{padding:6px 26px 26px}
.doc h1{font-size:1.15rem;margin:22px 0 10px;color:var(--teal-d)}
.doc h2{font-size:1rem;margin:20px 0 8px;color:var(--teal-d);padding-bottom:5px;border-bottom:2px solid var(--terra)}
.doc h3{font-size:.92rem;margin:14px 0 6px}
.doc p{margin:8px 0;font-size:.9rem}
.doc li{margin:5px 0 5px 18px;font-size:.9rem}
.doc code{background:#f1ece2;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:.82rem}
.doc pre{background:#17332f;color:#e8f2ef;border-radius:8px;padding:14px;overflow-x:auto;font-size:.8rem;margin:10px 0}
.doc table{border-collapse:collapse;width:100%;font-size:.84rem;margin:10px 0}
.doc th{background:var(--teal);color:#fff;text-align:left;padding:7px 10px;font-weight:650}
.doc td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.doc tr:nth-child(even) td{background:#faf7f0}
footer{text-align:center;font-size:.75rem;color:var(--mut);padding-bottom:30px}
.empty{padding:40px 20px;text-align:center;color:var(--mut)}
@media(max-width:560px){.book-grid{flex-direction:column;align-items:center}
.cover-box{flex:none}.book-info{width:100%}.doc{padding:6px 16px 20px}}
</style></head><body>
<div class="topbar"><div class="logo">KM</div>
<div><h1>KDP Console</h1><div class="sub">@@TODAY@@</div></div></div>
@@BODY@@
<footer>KDP Dashboard · part of the kdp-team bundle · LAN only · token-gated</footer></body></html>'''

def render_page(body, today=None):
    return (PAGE.replace('@@TODAY@@', today or time.strftime('%d %b %Y'))
                .replace('@@BODY@@', body))

# ---------- markdown ----------

def esc(s):
    return html.escape(str(s), quote=False)

def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+?)`', r'<code>\1</code>', s)
    return s

def render_md(text):
    lines = text.splitlines()
    out, i, in_pre = [], 0, False
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            out.append('</pre>' if in_pre else '<pre>')
            in_pre = not in_pre; i += 1; continue
        if in_pre:
            out.append(esc(line)); i += 1; continue
        if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i+1].strip()):
            hdr = [c.strip() for c in line.strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            th = ''.join(f'<th>{inline(c)}</th>' for c in hdr)
            trs = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows)
            out.append(f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>')
            continue
        m = re.match(r'^(#{1,4}) (.+)$', line)
        if m:
            out.append(f'<h{len(m.group(1)) + 1}>{inline(m.group(2))}</h{len(m.group(1)) + 1}>'); i += 1; continue
        if re.match(r'^\s*[-*] ', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*] ', lines[i]):
                items.append('<li>' + inline(re.sub(r'^\s*[-*] ', '', lines[i])) + '</li>')
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>'); continue
        m = re.match(r'^\s*(\d+)\. ', line)
        if m:
            items = []
            while i < len(lines) and re.match(r'^\s*(\d+)\. ', lines[i]):
                mm = re.match(r'^\s*(\d+)\. (.+)$', lines[i])
                items.append(f'<li>{inline(mm.group(2))}</li>')
                i += 1
            out.append('<ol>' + ''.join(items) + '</ol>'); continue
        if line.strip().startswith('>'):
            out.append(f'<div class="md-warn" style="background:#fdf0e7;border-left:4px solid var(--terra);padding:10px 14px;border-radius:0 8px 8px 0;margin:10px 0">{inline(line.strip().lstrip("> "))}</div>')
            i += 1; continue
        if not line.strip():
            i += 1; continue
        out.append(f'<p>{inline(line)}</p>'); i += 1
    if in_pre: out.append('</pre>')
    return '\n'.join(out)

# ---------- views ----------

def human(n):
    for u in ('B', 'KB', 'MB'):
        if n < 1024:
            return f'{n:.0f} {u}' if u == 'B' else f'{n:.1f} {u}'
        n /= 1024
    return f'{n:.1f} GB'

def cover_initials(title):
    words = [w for w in re.split(r'[^A-Za-z0-9]+', title) if w]
    return ''.join(w[0].upper() for w in words[:2]) or 'KB'

def shelf_view():
    slugs = books()
    if not slugs:
        return '<main><div class="card empty">No books yet. Run the kdp-team pipeline to create book-001.</div></main>'
    cards = []
    for slug in slugs:
        st = book_stats(slug)
        status, cls = book_status(slug)
        title = book_title(slug)
        prev = os.path.join(ROOT, slug, 'cover/preview_400.png')
        cover = (f'<img src="/{TOKEN}/img/{slug}/cover/preview_400.png" alt="cover">'
                 if os.path.isfile(prev) else f'<div class="cover-ph">{esc(cover_initials(title))}</div>')
        epub = os.path.isfile(os.path.join(ROOT, slug, 'manuscript/book.epub'))
        dl = (f'<a class="btn primary small" href="/{TOKEN}/raw/{slug}/manuscript/book.epub">⬇ .epub</a>'
              if epub else '')
        asin_bit = f'<div class="stat"><b style="font-size:.85rem">{esc(st["asin"])}</b><span>ASIN</span></div>' if st['asin'] else ''
        cards.append(f'''
<div class="card">
  <div class="card-hd"><h2>{esc(slug.upper())}</h2><span class="chip {cls}">{esc(status)}</span></div>
  <div class="book-grid">
    <div class="cover-box">{cover}</div>
    <div class="book-info">
      <div class="kicker">Kindle eBook{(' · ' + esc(st['price'])) if st["price"] != '—' else ''}</div>
      <h3><a href="/{TOKEN}/{slug}/">{esc(title)}</a></h3>
      <div class="stats">
        <div class="stat"><b>{st['words']:,}</b><span>words</span></div>
        <div class="stat"><b>{st['chapters']}</b><span>chapters</span></div>{asin_bit}
      </div>
      <div class="dl-row">
        <a class="btn ghost small" href="/{TOKEN}/{slug}/">Open book →</a>{dl}
      </div>
    </div>
  </div>
</div>''')
    return '<main>' + ''.join(cards) + '</main>'

def book_page(slug):
    b = os.path.join(ROOT, slug)
    st = book_stats(slug)
    status, cls = book_status(slug)
    title = book_title(slug)
    epub = os.path.join(b, 'manuscript/book.epub')
    cover = os.path.join(b, 'cover/cover.jpg')
    prev = os.path.join(b, 'cover/preview_400.png')
    pkg = os.path.join(b, 'publish/package.md')

    cover_html = (f'<img src="/{TOKEN}/img/{slug}/cover/preview_400.png" alt="cover">'
                  if os.path.isfile(prev) else f'<div class="cover-ph">{esc(cover_initials(title))}</div>')
    dl_epub = (f'<a class="btn primary" href="/{TOKEN}/raw/{slug}/manuscript/book.epub">⬇ Download manuscript (.epub)</a>'
               if os.path.isfile(epub) else
               '<span class="sec-note">manuscript not built yet</span>')
    dl_cover = (f'<a class="btn ghost" href="/{TOKEN}/raw/{slug}/cover/cover.jpg">⬇ Cover (1600×2560)</a>'
                if os.path.isfile(cover) else '')
    stats = f'''
      <div class="stats">
        <div class="stat"><b>{st['words']:,}</b><span>words</span></div>
        <div class="stat"><b>{st['chapters']}</b><span>chapters</span></div>
        <div class="stat"><b>{human(os.path.getsize(epub)) if os.path.isfile(epub) else '—'}</b><span>epub</span></div>
        <div class="stat"><b>{esc(st['price'])}</b><span>launch</span></div>
      </div>'''
    if st['asin']:
        stats += f'''
      <div class="stats" style="margin-top:-10px">
        <div class="stat"><b style="font-size:.9rem">{esc(st['asin'])}</b><span>ASIN — live</span></div>
        <div class="stat"><a href="https://www.amazon.com/dp/{esc(st['asin'])}" style="font-size:.85rem">view on Amazon ↗</a></div>
      </div>'''
    publish_chip = ('<span class="chip live">LIVE · ' + esc(st['asin']) + '</span>' if st['asin'] else
                    '<span class="chip ready">READY TO UPLOAD · ~20 MIN</span>' if status == 'READY TO UPLOAD' else
                    f'<span class="chip {cls}">{esc(status)}</span>')
    publish_open = (f'<a class="btn primary" href="/{TOKEN}/{slug}/publish">📄 Open publish runbook</a>'
                    if os.path.isfile(pkg) else '<span class="sec-note">runbook not written yet</span>')
    asin_block = ''
    if st['asin']:
        asin_block = f'''
      <div class="dl-row">
        <a class="btn ghost" href="https://www.amazon.com/dp/{esc(st['asin'])}">↗ amazon.com/dp/{esc(st['asin'])}</a>
        <span class="sec-note" style="padding:0">sales tracking active · weekly digest · 30-day review {esc((live_date(slug) and time.strftime('%Y-%m-%d', time.localtime(time.mktime(time.strptime(live_date(slug), "%Y-%m-%d"))) + 30*86400)) or '')}</span>
      </div>'''
    elif status in ('READY TO UPLOAD', 'LIVE') or os.path.isfile(pkg):
        asin_block = f'''
      <form method="post" action="/{TOKEN}/{slug}/set-asin" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:4px">
        <input name="asin" required placeholder="ASIN after live (B0…)" pattern="B0[A-Z0-9]{{8}}"
               style="padding:11px 14px;border:1.5px solid var(--teal);border-radius:9px;font-size:.9rem;width:230px;text-transform:uppercase">
        <button class="btn primary" type="submit">Activate LIVE + tracking</button>
      </form>
      <div class="sec-note" style="padding:8px 0 0">Paste the ASIN from your KDP Bookshelf once the book is live. This arms the weekly sales digest and the 30-day review.</div>'''
    body = f'''
<main>
<a class="backlink" href="/{TOKEN}/">← Shelf</a>
<div class="card">
  <div class="card-hd"><h2>MANUSCRIPT</h2><span class="chip {cls}">{esc(status)}</span></div>
  <div class="book-grid">
    <div class="cover-box">{cover_html}</div>
    <div class="book-info">
      <div class="kicker">Kindle eBook</div>
      <h3>{esc(title)}</h3>
      <div class="subtitle">{esc(slug)} · managed by kdp-team</div>
      {stats}
      <div class="dl-row">{dl_epub}{dl_cover}</div>
      {asin_block}
    </div>
  </div>
</div>
<div class="card">
  <div class="card-hd"><h2>PUBLISH</h2>{publish_chip}</div>
  <div class="book-grid" style="padding:18px 22px">
    <div class="book-info">
      <p style="font-size:.9rem">All KDP dashboard fields are final in the runbook — copy-paste
      at kdp.amazon.com (Bookshelf → Create → Kindle eBook). Includes the mandatory
      AI-content disclosure answer.</p>
      <div class="dl-row">{publish_open}</div>
    </div>
  </div>
  <div class="sec-note">Live in ~72 h after publish. Then report the ASIN back to nano.</div>
</div>
</main>'''
    return body

def publish_page(slug):
    pkg = os.path.join(ROOT, slug, 'publish/package.md')
    if not os.path.isfile(pkg):
        return '<main><div class="card empty">No publish package yet for ' + esc(slug) + '.</div></main>'
    back = (f'<main><a class="backlink" href="/{TOKEN}/{slug}/">← {esc(slug)}</a>'
            f'<div class="card"><div class="card-hd"><h2>PUBLISH RUNBOOK — package.md</h2>'
            f'<a class="btn ghost" href="/{TOKEN}/raw/{slug}/publish/package.md">⬇ download</a></div>'
            f'<div class="doc">{render_md(read1(pkg))}</div></div></main>')
    return back

# ---------- server ----------

def safe_files(slug):
    b = os.path.join(ROOT, slug)
    cands = ['manuscript/book.epub', 'cover/cover.jpg', 'cover/preview_400.png',
             'publish/package.md', 'seo/listing.md', 'cover/brief.md', 'qa/report.md']
    return {os.path.normpath(os.path.join(b, rel)) for rel in cands
            if os.path.isfile(os.path.join(b, rel))}


def set_asin(slug, asin):
    log = os.path.join(ROOT, slug, 'sales/log.csv')
    os.makedirs(os.path.dirname(log), exist_ok=True)
    if not os.path.isfile(log):
        with open(log, 'w') as f: f.write('date,slug,asin,price,notes\n')
    txt = open(log).read()
    lines = txt.rstrip('\n').split('\n')
    now = time.strftime('%Y-%m-%d %H:%M')
    for i in range(len(lines) - 1, 0, -1):
        cols = lines[i].split(',')
        if len(cols) >= 3 and (cols[2] == 'PENDING' or not cols[2]):
            cols[2] = asin
            if len(cols) < 5: cols += [''] * (5 - len(cols))
            cols[4] = (cols[4] + ' | ' if cols[4] else '') + f'ASIN set {now}'
            lines[i] = ','.join(cols)
            open(log, 'w').write('\n'.join(lines) + '\n')
            return True
    lines.append(f'{time.strftime("%Y-%m-%d")},{slug},{asin},,{f"ASIN set {now}"}')
    open(log, 'w').write('\n'.join(lines) + '\n')
    return True

def live_date(slug):
    for line in read1(os.path.join(ROOT, slug, 'sales/log.csv')).splitlines()[1:]:
        cols = [c.strip() for c in line.split(',')]
        if len(cols) >= 5 and cols[2] and cols[2] != 'PENDING':
            return cols[0]
    return None

def armed(slug):
    return read1(os.path.join(ROOT, slug, f'.tracking-armed')).strip() == '1'

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write('[kdp-dash] %s\n' % (fmt % args))

    def _send(self, code, body, ctype='text/html; charset=utf-8', extra=None):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        parts = [p for p in unquote(self.path).split('/') if p]
        if not parts or parts[0] != TOKEN:
            self._send(404, b'404'); return
        rest = parts[1:]
        if len(rest) == 2 and rest[1] == 'set-asin' and SLUG_RE.match(rest[0]) and rest[0] in books():
            slug = rest[0]
            length = int(self.headers.get('Content-Length', 0))
            form = self.rfile.read(length).decode('utf-8', 'replace')
            m = re.search(r'(?:^|&)asin=([A-Z0-9]{10})(&|$)', form)
            if not m:
                self._send(400, b'bad asin'); return
            asin = m.group(1)
            set_asin(slug, asin)
            open(os.path.join(ROOT, slug, '.tracking-armed'), 'w').write('1')
            live = live_date(slug) or time.strftime('%Y-%m-%d')
            self._send(200, render_page(f'<main><div class="card empty">ASIN {esc(asin)} activated for {esc(slug)} '
                                        f'(live date {esc(live)}). Tracking armed: weekly digest + 30-day review on '
                                        '{esc((time.strptime(live, "%Y-%m-%d") and (time.mktime(time.strptime(live, "%Y-%m-%d")) + 30*86400) and time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.strptime(live, "%Y-%m-%d"))) + 30*86400)))}.'
                                        f'<br><br><a class="btn primary" href="/{TOKEN}/{slug}/">← Back to book</a></div></main>').encode())
            return
        self._send(404, b'404')

    def do_GET(self):
        parts = [p for p in unquote(self.path).split('/') if p]
        if not parts or parts[0] != TOKEN:
            self._send(404, render_page('<main><div class="card empty">404</div></main>').encode()); return
        rest = parts[1:]

        if not rest:
            self._send(200, render_page(shelf_view()).encode()); return

        if rest[0] in ('raw', 'img'):
            if len(rest) < 3:
                self._send(404, render_page('<main><div class="card empty">404</div></main>').encode()); return
            slug = rest[1]
            if not SLUG_RE.match(slug) or slug not in books():
                self._send(404, render_page('<main><div class="card empty">404 — unknown book</div></main>').encode()); return
            f = os.path.normpath(os.path.join(ROOT, slug, '/'.join(rest[2:])))
            if f not in safe_files(slug):
                self._send(404, b'not found'); return
            data = open(f, 'rb').read()
            ext = os.path.splitext(f)[1].lower()
            if rest[0] == 'img' or ext in ('.jpg', '.png'):
                self._send(200, data, 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'); return
            ct = {'.epub': 'application/epub+zip', '.md': 'text/markdown; charset=utf-8',
                  '.csv': 'text/csv'}.get(ext, 'application/octet-stream')
            extra = {'Content-Disposition': f'attachment; filename="{os.path.basename(f)}"'} if ext in ('.epub', '.csv') else {}
            self._send(200, data, ct, extra); return

        slug = rest[0]
        if not SLUG_RE.match(slug) or slug not in books():
            self._send(404, render_page('<main><div class="card empty">404 — unknown book</div></main>').encode()); return

        if len(rest) == 1:
            self._send(200, render_page(book_page(slug)).encode()); return

        if len(rest) == 2 and rest[1] == 'publish':
            self._send(200, render_page(publish_page(slug)).encode()); return

        if rest[1] in ('raw', 'img') and len(rest) > 2:
            f = os.path.normpath(os.path.join(ROOT, '/'.join(rest[2:])))
            if f not in safe_files(slug):
                self._send(404, b'not found'); return
            data = open(f, 'rb').read()
            ext = os.path.splitext(f)[1].lower()
            if rest[1] == 'img' or ext in ('.jpg', '.png'):
                self._send(200, data, 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'); return
            ct = {'.epub': 'application/epub+zip', '.md': 'text/markdown; charset=utf-8',
                  '.csv': 'text/csv'}.get(ext, 'application/octet-stream')
            extra = {'Content-Disposition': f'attachment; filename="{os.path.basename(f)}"'} if ext in ('.epub', '.csv') else {}
            self._send(200, data, ct, extra); return

        self._send(404, render_page('<main><div class="card empty">404</div></main>').encode())

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=8791)
    ap.add_argument('--root', default=None)
    a = ap.parse_args()
    if a.root: ROOT = os.path.expanduser(a.root)
    TOKEN = get_token()
    srv = ThreadingHTTPServer(('0.0.0.0', a.port), Handler)
    print(f'KDP dashboard on :{a.port} (token {len(TOKEN)} chars)')
    srv.serve_forever()
