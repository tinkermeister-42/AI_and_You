#!/usr/bin/env python3
"""Build images/Unit_2/2.8_feature_visualization.jpg from the hero sprite of
"Feature Visualization" (Olah, Mordvintsev, Schubert, Distill 2017, CC BY 4.0).
Source: github.com/distillpub/post--feature-visualization, public/images/sprite_hero.png
(5 columns: edges, textures, patterns, parts, objects; 6 rows; 200 px tiles).
Usage: make-feature-figure.py path/to/sprite_hero.png"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
src = Image.open(sys.argv[1]).convert("RGB")
T, S, G = 200, 170, 8                       # tile in sprite, tile out, gap
PICK = {0: [0, 2, 4], 1: [0, 1, 4], 2: [0, 1, 5], 3: [1, 4, 3], 4: [0, 5, 3]}   # rows per column (no eyes or spiders)
NAMES = ["Edges", "Textures", "Patterns", "Parts", "Objects"]
top, bottom, side = 46, 64, 10
W = side * 2 + 5 * S + 4 * G * 2
H = top + 3 * S + 2 * G + bottom
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
ink = (44, 62, 80)
for c in range(5):
    x = side + c * (S + 2 * G)
    w = d.textlength(NAMES[c], font=bold)
    d.text((x + (S - w) / 2, 12), NAMES[c], font=bold, fill=ink)
    for r, row in enumerate(PICK[c]):
        tile = src.crop((c * T, row * T, c * T + T, row * T + T)).resize((S, S), Image.LANCZOS)
        img.paste(tile, (x, top + r * (S + G)))
# arrow: early layers -> later layers
y = top + 3 * S + 2 * G + 22
x0, x1 = side + 10, W - side - 10
d.line((x0, y, x1 - 14, y), fill=ink, width=4)
d.polygon([(x1, y), (x1 - 18, y - 10), (x1 - 18, y + 10)], fill=ink)
for txt, xx, anchor in [("early layers", x0, "la"), ("later layers", x1, "ra")]:
    d.text((xx, y + 12), txt, font=small, fill=ink, anchor=anchor)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "Unit_2", "2.8_feature_visualization.jpg")
img.save(out, quality=88, optimize=True)
print(out, img.size, os.path.getsize(out) // 1024, "KB")
