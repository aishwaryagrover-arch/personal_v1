#!/usr/bin/env python3
"""
Two slides for the GO-HRM rubrics deck:

  1. How this comes together: the scoring sheet, the reviewer guidance note and
     the AI assessment tool that is still being built.
  2. Discussion: the prompts to put to the consortium.

Built on the deck's own furniture: navy header with the gold rule, navy block
headings on light grey bodies, and the green and grey status bars used on the
"Building quality rubrics" slide.
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

OUT = "/home/user/personal_v1/GOHRM_operationalising_and_discussion.pptx"

W, H = 960, 540
PAD = 38
CW = W - 2 * PAD

NAVY = RGBColor(0x1B, 0x34, 0x58)
NAVY_T = RGBColor(0x2A, 0x58, 0x94)
GOLD = RGBColor(0xC9, 0xA1, 0x35)
BLUE_XL = RGBColor(0xA8, 0xC8, 0xE4)
PALE = RGBColor(0xE8, 0xF0, 0xFA)
GREY = RGBColor(0xF2, 0xF2, 0xF2)
GREYLN = RGBColor(0xDC, 0xDF, 0xE4)
GREEN = RGBColor(0x5B, 0xA8, 0x5A)
GREYBAR = RGBColor(0xC9, 0xCD, 0xD3)
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


def frame(title, sub, page):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    canvas(s, WHITE)
    rect(s, 0, 0, W, 72, fill=NAVY)
    rect(s, 0, 72, W, 3, fill=GOLD)
    text(s, PAD, 14, CW - 130, 26, [[_r(title, pt(21), WHITE, True)]], anchor=MSO_ANCHOR.TOP)
    if sub:
        text(s, PAD, 43, CW - 130, 20, [[_r(sub, pt(12), BLUE_XL, True)]], anchor=MSO_ANCHOR.TOP)
    text(s, PAD, 16, CW, 20, [[_r("IDinsight", pt(13), WHITE, True)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)
    text(s, PAD, H - 24, CW, 14, [[_r(str(page), pt(9.5), RGBColor(0x9A, 0xA4, 0xB2))]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    return s


# ══════════════════════════════════════════════ 1 · how this comes together
s = frame("How this comes together",
          "What makes the rubrics usable in practice",
          23)

BLOCKS = [
    ("1", "Scoring sheet",
     "An automated sheet that turns scores into a rating.",
     ["The reviewer records a score against each parameter, at each level of the rubric.",
      "Level weightages are applied in the background to produce a composite score.",
      "The sheet returns the corresponding rating of low, medium or high.",
      "No manual calculation is required at any point."],
     "Built", GREEN),
    ("2", "Reviewer guidance note",
     "How to work through the rubric, and the judgement it calls for.",
     ["Sets out how to navigate the rubric and how to read each level.",
      "Draws out the nuances behind parameters that the rubric alone does not carry.",
      "Identifies where contextual knowledge of the department\u2019s work is essential to "
      "score well, such as contextual relevance.",
      "Supports more informed and more consistent judgement across reviewers."],
     "Built", GREEN),
    ("3", "AI enabled assessment",
     "Support for assessment where outputs are produced at scale.",
     ["Goal cascades and PRACs are typically developed team wide or department wide, which "
      "makes reviewing each one manually impractical.",
      "A quality assessment tool is being trained on the rubrics and the guidance note.",
      "It draws on inputs from the reviewer, such as programme documents and subject matter "
      "context.",
      "Intended to widen adoption of the rubrics across use cases."],
     "Under development", GREYBAR),
]

BY, BH = 100, 330
bw = (CW - 2 * 18) / 3
for i, (num, head, lead, points, status, scol) in enumerate(BLOCKS):
    x = PAD + (bw + 18) * i
    rect(s, x, BY, bw, BH, fill=GREY, line=GREYLN, radius=0.02)
    rect(s, x, BY, bw, 44, fill=NAVY)
    n = rect(s, x + 12, BY + 11, 22, 22, fill=GOLD, radius=0.1)
    shape_text(n, [[_r(num, pt(12), WHITE, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
    text(s, x + 42, BY + 13, bw - 54, 20, [[_r(head, pt(13.5), WHITE, True)]],
         anchor=MSO_ANCHOR.TOP)
    text(s, x + 14, BY + 54, bw - 28, 36, [[_r(lead, pt(11.5), NAVY, True)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.14)
    y = BY + 94
    for ptxt in points:
        lines = -(-len(ptxt) // 38)
        text(s, x + 14, y, bw - 28, lines * 14 + 8,
             [[_r("•  ", pt(10), GOLD, True), _r(ptxt, pt(10), INK)]],
             anchor=MSO_ANCHOR.TOP, line_spacing=1.16)
        y += lines * 14 + 10
    sb = rect(s, x + 14, BY + BH - 34, bw - 28, 22, fill=scol, radius=0.08)
    shape_text(sb, [[_r(status, pt(10), WHITE if scol == GREEN else NAVY, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=4, m_right=4)

text(s, PAD, BY + BH + 12, CW, 20,
     [[_r("Together these take the rubric from a standard on paper to something that can be "
          "applied consistently, and at the scale these outputs are produced.",
          pt(11), MUT, ital=True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)


# ══════════════════════════════════════════════ 2 · discussion
s = frame("Discussion", "What we would like your views on", 26)

PROMPTS = [
    ("Refining the rubrics",
     "Looking at the parameters and the levels, what would you change, add or drop? "
     "Is anything being scored that does not matter, or missing that does?"),
    ("Where these could be used",
     "Is there work coming up where you could use these rubrics? What would you need "
     "from us to make that possible?"),
    ("Getting the same score from different reviewers",
     "Two people scoring the same PRAC should land in the same place. What would it take "
     "for your teams to get there, and what training or support would help?"),
    ("What a score should lead to",
     "If a department's PRACs average 1.4 out of 3, what should happen next, and who acts "
     "on it? Should the rubric say, or is that for each context to decide?"),
    ("Who runs the review",
     "Who is best placed to do quality checks: the implementing team, a reviewer inside "
     "government, or an external evaluator? What does each one get right, and get wrong?"),
    ("On the AI enabled tool",
     "We are early in building this. What would make you trust a score it produces, and where "
     "would you want a reviewer to stay in the loop? Are there documents or use cases you could "
     "help us test it on?"),
    ("Building the assessment rubric",
     "Given how technical it is, are there resources or partner engagements we can draw on "
     "for a competency assessment rubric, or for validating the two we have?"),
]

PY, PH, GAPX, GAPY = 94, 98, 20, 10
pw = (CW - GAPX) / 2
for i, (head, body) in enumerate(PROMPTS):
    col, row = i % 2, i // 2
    x = PAD + (pw + GAPX) * col
    y = PY + (PH + GAPY) * row
    rect(s, x, y, pw, PH, fill=GREY, line=GREYLN, radius=0.02)
    rect(s, x, y, 6, PH, fill=NAVY)
    text(s, x + 18, y + 11, pw - 34, 20, [[_r(head, pt(12), NAVY, True)]],
         anchor=MSO_ANCHOR.TOP)
    text(s, x + 18, y + 34, pw - 34, PH - 44, [[_r(body, pt(10.5), INK)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.18)

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
