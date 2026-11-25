#!/usr/bin/env python3
"""
One slide for the GO-HRM evaluation framework deck: the link between the
evaluation framework and the quality rubrics.

It reuses the deck's own furniture - the navy header with the gold rule, the
five-step chevron from the evaluation design note recap, and the light-blue and
gold palette - so it can be pasted in after the recap section.

The argument runs down the slide: at step 3 teams shortlist indicators; one
group of those indicators measures the quality of GO-HRM's key outputs; output
quality is what carries the intermediate and final outcomes; but nobody has
defined what low, medium and high quality mean; the rubrics are that definition.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(os.path.dirname(HERE), "mahapar_deck", "lib")
sys.path.insert(0, SKILL)

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

OUT = "/home/user/personal_v1/GOHRM_why_quality_rubrics_slide.pptx"

W, H = 960, 540
PAD = 38
CW = W - 2 * PAD

# palette taken from the deck
NAVY = RGBColor(0x1B, 0x34, 0x58)
NAVY_T = RGBColor(0x2A, 0x58, 0x94)
BLUE_M = RGBColor(0x3C, 0x6F, 0xA8)
BLUE_L = RGBColor(0x6F, 0x9F, 0xCB)
BLUE_XL = RGBColor(0xA8, 0xC8, 0xE4)
PALE = RGBColor(0xD6, 0xE4, 0xF7)
PALER = RGBColor(0xEB, 0xF2, 0xFB)
GOLD = RGBColor(0xC9, 0xA1, 0x35)
GOLD_D = RGBColor(0xA5, 0x7C, 0x16)
PEACH = RGBColor(0xFB, 0xE8, 0xD5)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
INK = RGBColor(0x23, 0x2B, 0x38)
MUT = RGBColor(0x5A, 0x65, 0x75)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def pt(px):
    return round(px * 0.75, 1)


prs = Presentation(f"{SKILL}/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)

s = prs.slides.add_slide(prs.slide_layouts[0])
canvas(s, WHITE)

# ── header, as in the deck
rect(s, 0, 0, W, 72, fill=NAVY)
rect(s, 0, 72, W, 3, fill=GOLD)
text(s, PAD, 14, CW - 130, 26,
     [[_r("Why quality rubrics: giving the quality indicators a definition", pt(21), WHITE, True)]],
     anchor=MSO_ANCHOR.TOP)
text(s, PAD, 42, CW - 130, 20,
     [[_r("The evaluation framework already counts quality. It does not say what quality is.",
          pt(12), BLUE_XL)]], anchor=MSO_ANCHOR.TOP)
text(s, PAD, 16, CW, 20, [[_r("IDinsight", pt(13), WHITE, True)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)
text(s, PAD, H - 24, CW, 14, [[_r("7", pt(9.5), RGBColor(0x9A, 0xA4, 0xB2))]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ══════════════════════════════════════ 1 · the journey, with step 3 picked out
text(s, PAD, 86, CW, 16,
     [[_r("THE EVALUATION DESIGN NOTE LAYS OUT THE JOURNEY", pt(10), MUT, True)]],
     anchor=MSO_ANCHOR.TOP)

STEPS = [("1. Identify learning\npriorities", NAVY),
         ("2. Assess context\nand constraints", NAVY_T),
         ("3. Shortlist relevant\nindicators", BLUE_M),
         ("4. Finalise measurement\napproach", BLUE_L),
         ("5. Develop tools and\nimplementation plan", BLUE_XL)]
CHY, CHH = 106, 46
OVER = 14                                   # chevrons overlap by their point
cw_ = (CW + OVER * (len(STEPS) - 1)) / len(STEPS)
for i, (label, col) in enumerate(STEPS):
    x = PAD + (cw_ - OVER) * i
    sp = rect(s, x, CHY, cw_, CHH, fill=col, shape=MSO_SHAPE.CHEVRON)
    shape_text(sp, [[_r(label, pt(10.5), WHITE if i < 4 else NAVY, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
               m_left=10, m_right=4, line_spacing=1.05)

# the one step this slide is about
X3 = PAD + (cw_ - OVER) * 2
rect(s, X3 - 2, CHY - 3, cw_ + 4, CHH + 6, fill=None, line=GOLD, line_w=2.25,
     shape=MSO_SHAPE.CHEVRON)
tag = rect(s, X3 + 22, CHY + CHH + 4, 92, 15, fill=GOLD, radius=0.5)
shape_text(tag, [[_r("THIS SLIDE", pt(8.5), WHITE, True)]],
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=2, m_right=2)
# connector dropping out of step 3 into the chain below
rect(s, X3 + cw_ / 2 - 1, CHY + CHH + 19, 2, 14, fill=GOLD)

# ══════════════════════════════════════ 2 · what those indicators carry
CY, CH = 180, 130
rect(s, PAD, CY, CW, CH, fill=PALER, line=PALE, radius=0.02)
text(s, PAD + 16, CY + 10, CW - 32, 16,
     [[_r("ONE GROUP OF THOSE INDICATORS MEASURES THE QUALITY OF GO-HRM’S KEY OUTPUTS",
          pt(10), NAVY, True)]], anchor=MSO_ANCHOR.TOP)

LINKS = [
    (NAVY, "Quality of key outputs",
     "% of positions with SMART goal cascades\n% of positions with low / med / high quality PRACs"),
    (NAVY_T, "Intermediate outcomes",
     "Role clarity · clarity on the skills a post needs\nsupervisors using KPIs to monitor"),
    (BLUE_M, "Final outcomes",
     "Visibility into performance · improved performance\nimproved competency"),
]
bw = (CW - 32 - 2 * 44) / 3
for i, (col, head, body) in enumerate(LINKS):
    x = PAD + 16 + (bw + 44) * i
    rect(s, x, CY + 32, bw, 72, fill=WHITE, line=PALE, radius=0.03)
    rect(s, x, CY + 32, bw, 4, fill=col)
    text(s, x + 11, CY + 42, bw - 22, 16, [[_r(head, pt(12), col, True)]], anchor=MSO_ANCHOR.TOP)
    text(s, x + 11, CY + 61, bw - 22, 42, [[_r(body, pt(9.5), MUT)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.2)
    if i < 2:
        text(s, x + bw, CY + 32, 44, 72, [[_r("→", pt(18), GOLD_D, True)]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

text(s, PAD + 16, CY + CH - 18, CW - 32, 14,
     [[_r("If the outputs are weak, the outcomes do not move — and the evaluation cannot "
          "say whether the design failed or the outputs did.", pt(9.5), INK, ital=True)]],
     anchor=MSO_ANCHOR.TOP)

# ══════════════════════════════════════ 3 · the gap
GY, GH = 318, 72
rect(s, PAD, GY, CW, GH, fill=PEACH)
rect(s, PAD, GY, 5, GH, fill=GOLD_D)
text(s, PAD + 18, GY + 11, 150, 18, [[_r("THE GAP", pt(10.5), GOLD_D, True)]],
     anchor=MSO_ANCHOR.TOP)
text(s, PAD + 18, GY + 30, CW - 36, 40,
     [[_r("Nothing says what low, medium or high quality actually means.", pt(13), INK, True)],
      [_r("Every reviewer, partner and department applies their own standard, so the scores are "
          "not comparable — across positions, across departments, or across states.",
          pt(11), INK)]],
     anchor=MSO_ANCHOR.TOP, line_spacing=1.15, space_after=pt(3))

# ══════════════════════════════════════ 4 · what the rubrics do
AY, AH = 398, 100
rect(s, PAD, AY, CW, AH, fill=NAVY, radius=0.015)
text(s, PAD + 18, AY + 12, 220, 18, [[_r("WHAT THE RUBRICS DO", pt(10.5), GOLD, True)]],
     anchor=MSO_ANCHOR.TOP)
text(s, PAD + 18, AY + 31, CW - 300, 44,
     [[_r("The rubrics are that definition — one standard, applied the same way by everyone "
          "who judges a goal cascade or a PRAC.", pt(13), WHITE, True)]],
     anchor=MSO_ANCHOR.TOP, line_spacing=1.2)
text(s, PAD + 18, AY + AH - 30, CW - 300, 24,
     [[_r("That is what makes the quality indicators comparable, and the evaluation able to "
          "explain what it finds.", pt(10), BLUE_XL, ital=True)]], anchor=MSO_ANCHOR.TOP)

USERS = ["IDinsight\nevaluation teams", "Implementing\npartners", "Government\ndepartments"]
uw = 78
for i, u in enumerate(USERS):
    x = PAD + CW - 18 - (uw + 10) * (3 - i)
    c = rect(s, x, AY + 26, uw, 52, fill=NAVY_T, radius=0.06)
    shape_text(c, [[_r(u, pt(9.5), WHITE, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
               m_left=4, m_right=4, line_spacing=1.1)
text(s, PAD + CW - 18 - (uw + 10) * 3, AY + AH - 26, (uw + 10) * 3 - 10, 18,
     [[_r("the same score, whoever applies it", pt(9), BLUE_XL, ital=True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)

prs.save(OUT)
print("wrote", OUT)
