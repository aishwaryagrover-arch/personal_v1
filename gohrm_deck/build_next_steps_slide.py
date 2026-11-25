#!/usr/bin/env python3
"""
Next steps slide for the quality rubrics section of the GO-HRM deck.

Uses the same gold numeral tab and navy heading bar as the deck's existing
next steps slide, so it sits in the same section without re-styling.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(os.path.dirname(HERE), "mahapar_deck", "lib")
sys.path.insert(0, SKILL)

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

OUT = "/home/user/personal_v1/GOHRM_next_steps_slide.pptx"

W, H = 960, 540
PAD = 38
CW = W - 2 * PAD

NAVY = RGBColor(0x1B, 0x34, 0x58)
GOLD = RGBColor(0xE0, 0xA8, 0x1C)
BLUE_XL = RGBColor(0xA8, 0xC8, 0xE4)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
GREYLN = RGBColor(0xDC, 0xDF, 0xE4)
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

rect(s, 0, 0, W, 72, fill=NAVY)
rect(s, 0, 72, W, 3, fill=GOLD)
text(s, PAD, 14, CW - 130, 26, [[_r("Next steps", pt(21), WHITE, True)]], anchor=MSO_ANCHOR.TOP)
text(s, PAD, 43, CW - 130, 20,
     [[_r("Refining the rubrics, building the tool, and putting both to use", pt(12),
          BLUE_XL, True)]], anchor=MSO_ANCHOR.TOP)
text(s, PAD, 16, CW, 20, [[_r("IDinsight", pt(13), WHITE, True)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)
text(s, PAD, H - 24, CW, 14, [[_r("25", pt(9.5), RGBColor(0x9A, 0xA4, 0xB2))]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

STEPS = [
    ("I", "Refine the rubrics through stakeholder consultations",
     ["Test the goal cascade and PRAC rubrics with the people who will apply them, and with "
      "government counterparts.",
      "Check whether the parameters hold across departments and across different kinds of "
      "position.",
      "Revise the parameters, levels and weightages on what comes back."]),
    ("II", "Develop and deploy the AI enabled assessment tool",
     ["Train the tool on the rubrics and the reviewer guidance note.",
      "Test its scores against reviewer scores on outputs we have already assessed.",
      "Settle where a reviewer stays in the loop, then release it for use."]),
    ("III", "Socialise both, and find where they can be used",
     ["Share the evaluation framework and the rubrics across IDinsight teams and with "
      "consortium partners.",
      "Identify engagements where either can be applied, in our work and in partners’ "
      "GO-HRM implementations.",
      "Carry the learning from each use back into the framework and the rubrics."]),
]

TABW, BARH = 40, 32
BODYW = CW - TABW - 44
CPL = 108                      # characters per line at 10.5pt in BODYW


def nlines(txt):
    return max(1, -(-len(txt) // CPL))


y = 96
for num, head, points in STEPS:
    # size the body from the lines each bullet really takes, not from a flat
    # per-bullet allowance, which left a gap under short blocks and overflowed
    # the long one
    bh = 12 + sum(nlines(p_) * 15 + 9 for p_ in points) + 4
    tab = rect(s, PAD, y, TABW, BARH, fill=GOLD)
    shape_text(tab, [[_r(num, pt(13), WHITE, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
    bar = rect(s, PAD + TABW + 6, y, CW - TABW - 6, BARH, fill=NAVY)
    shape_text(bar, [[_r(head, pt(13), WHITE, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=14, m_right=10)
    rect(s, PAD + TABW + 6, y + BARH, CW - TABW - 6, bh, fill=GREY, line=GREYLN)
    py = y + BARH + 10
    for ptxt in points:
        ln = nlines(ptxt)
        text(s, PAD + TABW + 22, py, BODYW, ln * 15 + 6,
             [[_r("\u2022  ", pt(10.5), GOLD, True), _r(ptxt, pt(10.5), INK)]],
             anchor=MSO_ANCHOR.TOP, line_spacing=1.18)
        py += ln * 15 + 9
    y += BARH + bh + 12

text(s, PAD + TABW + 6, y + 2, CW - TABW - 6, 20,
     [[_r("Timelines for each of these will be set with partners once the consultations are "
          "scheduled.", pt(10), MUT, ital=True)]], anchor=MSO_ANCHOR.TOP)

prs.save(OUT)
print("wrote", OUT)
