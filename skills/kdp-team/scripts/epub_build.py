#!/usr/bin/env python3
"""Build a valid EPUB-3 from chapters. stdlib only.

Usage: epub_build.py --title "T" --author "A" --out book.epub chapter1.md chapter2.md ...
Chapters: simple markdown (h1 title, paragraphs, h2/h3, ul/ol, bold/italic).
"""
import argparse, html, re, zipfile, uuid, datetime, sys

MD = [
    (r'^# (.+)$', 'h1'), (r'^## (.+)$', 'h2'), (r'^### (.+)$', 'h3'),
]
INLINE = [(r'\*\*(.+?)\*\*', r'<strong>\1</strong>'), (r'\*(.+?)\*', r'<em>\1</em>')]

def md_line(line):
    line = line.rstrip()
    for pat, tag in MD:
        m = re.match(pat, line)
        if m:
            return f'<{tag}>{html.escape(m.group(1))}</{tag}>'
    if re.match(r'^[-*] (.+)$', line):
        return f'<li>{html.escape(re.match(r"^[-*] (.+)$", line).group(1))}</li>'
    if not line.strip():
        return ''
    out = html.escape(line)
    for pat, rep in INLINE:
        out = re.sub(pat, rep, out)
    return f'<p>{out}</p>'

def chapter_xhtml(title, md_text):
    body, in_list = [], False
    for line in md_text.splitlines():
        is_li = bool(re.match(r'^[-*] ', line))
        if is_li and not in_list:
            body.append('<ul>'); in_list = True
        if not is_li and in_list:
            body.append('</ul>'); in_list = False
        x = md_line(line)
        if x and not (is_li and x.endswith('</li>') is False):
            body.append(x)
    if in_list:
        body.append('</ul>')
    xhtml = ('<?xml version="1.0" encoding="utf-8"?>\n'
             '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'
             '<head><meta charset="utf-8"/><title>' + html.escape(title) + '</title>'
             '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
             '<body>\n' + '\n'.join(body) + '\n</body>\n</html>\n')
    return xhtml

def build(title, author, out, chapters):
    book_id = str(uuid.uuid4())
    nav_items, files = [], []
    for i, (chap_title, md_text) in enumerate(chapters, 1):
        fn = f'chap{i:02d}.xhtml'
        files.append((fn, chapter_xhtml(chap_title, md_text)))
        nav_items.append(f'<navPoint id="np{i}"><navLabel><text>{html.escape(chap_title)}</text></navLabel><content src="{fn}"/></navPoint>')
    manifest = '\n'.join(
        f'<item id="c{i:02d}" href="{fn}" media-type="application/xhtml+xml"/>'
        for i, (fn, _) in enumerate(files, 1))
    spine = '\n'.join(f'<itemref idref="c{i:02d}"/>' for i in range(1, len(files) + 1))
    opf = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">\n'
           f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           f'<dc:identifier id="bookid">urn:uuid:{book_id}</dc:identifier>\n'
           f'<dc:title>{html.escape(title)}</dc:title>\n'
           f'<dc:creator>{html.escape(author)}</dc:creator>\n'
           f'<dc:language>en</dc:language>\n'
           f'<meta property="dcterms:modified">{datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>\n'
           '</metadata>\n<manifest>\n'
           '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
           '<item id="css" href="style.css" media-type="text/css"/>\n'
           f'{manifest}\n</manifest>\n<spine>\n{spine}\n</spine>\n</package>\n')
    nav = ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
           '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
           '<head><title>Contents</title></head><body>\n<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>\n'
           + '\n'.join(f'<li><a href="{fn}">{html.escape(t)}</a></li>' for fn, t in
                       [(fn, t) for (fn, _), (t, _) in zip(files, chapters)]) +
           '\n</ol></nav>\n</body>\n</html>\n')
    css = 'body{font-family:serif;line-height:1.5;margin:5%%}h1,h2,h3{font-family:sans-serif;line-height:1.2}\n'
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml',
                   '<?xml version="1.0"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>\n</container>\n')
        z.writestr('OEBPS/content.opf', opf)
        z.writestr('OEBPS/nav.xhtml', nav)
        z.writestr('OEBPS/style.css', css)
        for fn, xhtml in files:
            z.writestr(f'OEBPS/{fn}', xhtml)

def parse_md_file(path):
    lines = open(path, encoding='utf-8').read().splitlines()
    title = 'Chapter'
    for ln in lines:
        if ln.startswith('# '):
            title = ln[2:].strip(); break
    return title, '\n'.join(lines)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--author', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('chapters', nargs='+')
    a = ap.parse_args()
    chaps = [parse_md_file(p) for p in a.chapters]
    build(a.title, a.author, a.out, chaps)
    print(f'OK {a.out}: {len(chaps)} chapters')
