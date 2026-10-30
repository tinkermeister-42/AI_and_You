#!/usr/bin/env python3
"""Render the Chinese text for the Chinese Room (Lesson 1.3) to small PDFs.

pdflatex cannot set Chinese characters without packages this book does not
use, so the text is drawn once here and included as pictures:
    figures/Unit_1/cjk/<name>.pdf
Both the web figure and the printable sheet use these files. Run it again only
if the Chinese text changes:  python3 scripts/make-cjk.py
Needs matplotlib and a Chinese font (WenQuanYi Zen Hei or Noto Sans CJK SC).
"""
import pathlib
import matplotlib
matplotlib.use("pdf")
matplotlib.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

FONTS = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc"]
font = next((f for f in FONTS if pathlib.Path(f).exists()), None)
if font is None:
    raise SystemExit("No Chinese font found. Install fonts-wqy-zenhei.")
fp = FontProperties(fname=font)

# name: Chinese text.  The rule book pairs q<n> (a note that comes in) with
# a<n> (the reply that goes out).  English is in the lesson, not here.
TEXT = {
    "q1": "你好吗？",           "a1": "我很好，谢谢。",
    "q2": "你叫什么名字？",     "a2": "我叫小明。",
    "q3": "你喜欢吃什么？",     "a3": "我喜欢吃饺子。",
    "q4": "今天天气怎么样？",   "a4": "今天天气很好。",
    "q5": "你几岁？",           "a5": "我十五岁。",
    "q6": "你会说中文吗？",     "a6": "会，我会说中文。",
}
out = pathlib.Path(__file__).resolve().parent.parent / "figures" / "Unit_1" / "cjk"
out.mkdir(parents=True, exist_ok=True)
for name, s in TEXT.items():
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, s, fontproperties=fp, fontsize=20)
    fig.savefig(out / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02, transparent=True)
    plt.close(fig)
print("wrote", len(TEXT), "files to", out)
