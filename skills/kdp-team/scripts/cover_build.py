#!/usr/bin/env python3
"""Cover builder for 'Keep the Muscle' — type-forward, teal direction."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 2560
TEAL = (31, 95, 91)        # #1F5F5B
CREAM = (255, 249, 242)    # #FFF9F2
TERRA = (217, 108, 71)     # #D96C47
GOLD = (217, 164, 65)      # #D9A441
CHARCOAL = (43, 43, 43)

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
FONT = _os.environ.get("KDP_FONT", _os.path.join(_HERE, "Montserrat.ttf"))
FONT_R = _os.environ.get("KDP_FONT", _os.path.join(_HERE, "Montserrat.ttf"))

def _f(size):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    return f

def _fr(size):
    f = ImageFont.truetype(FONT_R, size)
    try: f.set_variation_by_name('Medium')
    except Exception: pass
    return f

img = Image.new("RGB", (W, H), TEAL)
d = ImageDraw.Draw(img)

def fit(text, max_w, start_size, font_path=FONT, min_size=40):
    size = start_size
    while size > min_size:
        f = _f(size) if font_path == FONT else ImageFont.truetype(font_path, size)
        if d.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 4
    return _f(min_size) if font_path == FONT else ImageFont.truetype(font_path, min_size)

M = 120  # margin
max_w = W - 2 * M

# --- Title (top third), wrapped ---
title_lines = ["Keep the", "Muscle"]
tf = fit("Keep the Muscle", max_w, 230)
ty = 300
for line in title_lines:
    d.text((M, ty), line, font=tf, fill=CREAM)
    bb = d.textbbox((0, 0), line, font=tf)
    ty += (bb[3] - bb[1]) + 40

# --- Terracotta rule ---
rule_y = ty + 60
d.rectangle([M, rule_y, M + 560, rule_y + 14], fill=TERRA)

# --- Subtitle ---
sub = "GLP-1 Strength Training"
sub2 = "for Women Over 50"
sf = fit(sub, max_w, 96, FONT, 48)
sy = rule_y + 110
d.text((M, sy), sub, font=sf, fill=CREAM)
sf2 = _f(int(sf.size * 0.8)) if hasattr(sf, 'size') else sf
d.text((M, sy + 150), sub2, font=sf2, fill=CREAM)

# --- Dumbbell graphic (clean, minimal), center-lower ---
db_y = 1620
bar_w, bar_h = 640, 26
plate_w, plate_h = 60, 150
db_x = (W - bar_w) // 2
d.rounded_rectangle([db_x, db_y - bar_h // 2, db_x + bar_w, db_y + bar_h // 2], radius=13, fill=CREAM)
for px in (db_x - plate_w + 10, db_x + bar_w - plate_w + 50):
    pass
# plates
d.rounded_rectangle([db_x + 40, db_y - plate_h // 2, db_x + 40 + plate_w, db_y + plate_h // 2], radius=16, fill=GOLD)
d.rounded_rectangle([db_x + bar_w - 40 - plate_w, db_y - plate_h // 2, db_x + bar_w - 40, db_y + plate_h // 2], radius=16, fill=GOLD)

# --- Tagline, letterspaced caps, above bottom margin ---
tag = "A 12-WEEK AT-HOME DUMBBELL PROGRAM"
gf = _fr(46)
spacing = 8
widths = [d.textbbox((0, 0), ch, font=gf)[2] for ch in tag]
total = sum(widths) + spacing * (len(tag) - 1)
tx = (W - total) // 2
ty2 = H - 260
for ch, w in zip(tag, widths):
    d.text((tx, ty2), ch, font=gf, fill=CREAM)
    tx += w + spacing

# nothing inside bottom 6% (153px): tagline bottom = 2560-260+70 = 2370 OK
COVER_OUT = _os.environ.get("KDP_COVER_OUT", _os.path.join(_HERE, "cover.jpg"))
img.save(COVER_OUT, quality=92)
print("saved", img.size)

# thumbnail render for legibility check
thumb = img.resize((100, 160), Image.LANCZOS)
thumb.save(_os.path.join(_os.path.dirname(COVER_OUT), "thumb_100.png"))
# 400px preview
prev = img.resize((400, 640), Image.LANCZOS)
prev.save(_os.path.join(_os.path.dirname(COVER_OUT), "preview_400.png"))
print("thumb + preview saved")
