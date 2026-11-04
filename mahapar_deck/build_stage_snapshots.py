#!/usr/bin/env python3
"""
Stage-wise before/after form snapshots on plain white slides.

One slide per stage. The "before" side carries the full pages of the current
form that cover that stage (legibility is not the point there — volume is); the
"after" side carries the corresponding section of Form A draft v5.

Page mapping of the current form (Form 1, 11 pages), read off the PDF:
  p1-p2   Section 1   establishment details, training, CR history
  p3-p4   Section 2   self-appraisal
  p5      Section 3   reporting officer's remarks on the self-appraisal
  p6-p7   Section 3   the graded dimensions (work completion, personal
                      attributes, efficiency)
  p8      Section 3   integrity, overall gradation, recommendations
  p9      Section 4A  Collector / Divisional Commissioner
  p10-p11 Section 4B  reviewing officer
"""
import os
import sys

SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.insert(0, SKILL)

from PIL import Image
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

SCR = ("/tmp/claude-0/-home-user-personal-v1/"
       "9b715f77-b654-5d38-be81-49173dc191a2/scratchpad")
OUT = "/home/user/personal_v1/MahaPAR_stage_snapshots.pptx"

NAVY   = RGBColor(0x1C, 0x3C, 0x6E)
BLUE   = RGBColor(0x25, 0x63, 0xEB)
RED    = RGBColor(0xDC, 0x26, 0x26)
REDLT  = RGBColor(0xFE, 0xE2, 0xE2)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
GREENLT= RGBColor(0xDC, 0xFC, 0xE7)
BORDER = RGBColor(0xD8, 0xDF, 0xE8)
DIM    = RGBColor(0x64, 0x74, 0x8B)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

S = 0.75
def h(v):  return v * S
def pt(v): return round(v * 72 / 128, 1)

W, H = 960, 540
PAD = h(44)
CW = W - 2 * PAD

FOOT = ("Current form: Form 1, the Group A / Group B gazetted proforma now in use, "
        "shown in Marathi with English in parentheses as it is issued today.   ·   "
        "After: Form A draft v5. The draft is written in English; the issued form "
        "will be bilingual, Marathi and English, like the present one.")

prs = Presentation(f"{SKILL}/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)
BLANK = prs.slide_layouts[0]


def pic(s, path, x, y, w=None, hh=None, top=False):
    """Place an image inside a box, preserving aspect.

    Centred in the box by default; top=True pins it to the top of the box and
    centres it horizontally, which is what the side-by-side panels want.
    """
    im = Image.open(path)
    iw, ih = im.size
    if w and hh:
        sc = min(w / iw, hh / ih)
    elif w:
        sc = w / iw
    else:
        sc = hh / ih
    pw, ph = iw * sc, ih * sc
    px = x + ((w - pw) / 2 if w else 0)
    py = y if top else y + ((hh - ph) / 2 if hh else 0)
    s.shapes.add_picture(path, X(px), X(py), X(pw), X(ph))
    return px, py, pw, ph


def label(s, x, y, w, txt, colr, bg):
    box = rect(s, x, y, w, h(26), fill=bg, radius=0.3)
    shape_text(box, [[_r(txt.upper(), pt(10.5), colr, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
               m_left=h(8), m_right=h(8))


# Each stage: title, the current-form pages to show, the Form A crop, the
# caption under the "after" side.
STAGES = [
    dict(title="Self-appraisal by the officer",
         old=["old-03", "old-04"], new="new_self_full",
         olab="Current form · Section 2 · 2 pages",
         nlab="Form A · Part 2 · self-appraisal",
         cap="Open prose under free headings becomes key activities against "
             "achievement, one significant contribution, and systemic factors."),
    dict(title="Reporting officer · the graded dimensions",
         old=["old-06", "old-07"], new="new_rep",
         olab="Current form · Section 3 · all graded items",
         nlab="Form A · Part 3.1 · 7 dimensions",
         cap="Three tables of 17 items, each graded and averaged by hand, become "
             "one table of seven dimensions, with MahaPAR calculating the "
             "weighted overall grade."),
    dict(title="Reviewing officer",
         old=["old-10", "old-11"], new="new_rev_full",
         olab="Current form · Section 4B · 2 pages",
         nlab="Form A · Part 4 · reviewing officer",
         cap="Instead of re-grading every dimension, the reviewing officer records "
             "agreement or disagreement with the reporting officer's overall grade "
             "and gives their own, with reasons required only where they differ."),
]

for st in STAGES:
    s = prs.slides.add_slide(BLANK)
    canvas(s, WHITE)

    text(s, PAD, h(26), CW, h(30),
         [[_r(st["title"], pt(19), NAVY, True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, PAD, h(56), CW, h(22),
         [[_r("Before and after · the current proforma against Form A draft v5",
              pt(11.5), DIM)]])

    LAB_Y = h(92)
    IMG_T = LAB_Y + h(34)
    IMG_B = H - h(78)
    IMG_H = IMG_B - IMG_T

    # ── before: the full pages, side by side at one shared scale
    n_old = len(st["old"])
    GAPO = h(10)
    OW = h(460)                                   # width of the whole before block
    pw_each = (OW - GAPO * (n_old - 1)) / n_old
    label(s, PAD, LAB_Y, OW, st["olab"], RED, REDLT)
    for i, p in enumerate(st["old"]):
        x = PAD + (pw_each + GAPO) * i
        # Top-aligned, width-driven: the pages are here for volume, not reading,
        # so the after side gets the spare width.
        px, py, pwd, phd = pic(s, f"{SCR}/src_pages/{p}.png", x, IMG_T, w=pw_each)
        rect(s, px, py, pwd, phd, fill=None, line=BORDER, line_w=0.75)

    AX = PAD + OW
    AW = h(50)
    text(s, AX, IMG_T, AW, IMG_H, [[_r("→", pt(28), BLUE, True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ── after: the matching section of Form A
    nx = AX + AW
    nw = (PAD + CW) - nx
    label(s, nx, LAB_Y, nw, st["nlab"], GREEN, GREENLT)
    # Bounded in both directions so a tall section (Part 2) cannot run off the
    # slide, with room left under it for the caption.
    npx, npy, npw, nph = pic(s, f"{SCR}/crops/{st['new']}.png", nx, IMG_T,
                             w=nw, hh=IMG_H - h(74), top=True)
    rect(s, npx, npy, npw, nph, fill=None, line=BORDER, line_w=0.75)
    text(s, nx, npy + nph + h(16), nw, h(90),
         [[_r(st["cap"], pt(11.5), DIM)]], anchor=MSO_ANCHOR.TOP)

    # ── footnote
    rect(s, PAD, H - h(62), CW, h(1), fill=BORDER)
    text(s, PAD, H - h(56), CW, h(44), [[_r(FOOT, pt(9.5), DIM)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.3)

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
