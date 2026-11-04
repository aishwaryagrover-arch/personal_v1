#!/usr/bin/env python3
"""
Five ways to show the forms before and after, built so they can be compared
side by side before one is chosen for the deck.

Images are rendered from the source PDFs: the current Form 1 (GR annexure,
11 pages) and Form A draft v5 (2 pages).
"""
import sys

# The IDinsight pptx skill was unsynced mid-session; a local copy of its
# component library and template now lives in ./lib so builds stay reproducible.
import os
SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.insert(0, SKILL)

from PIL import Image
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

SCR = "/tmp/claude-0/-home-user-personal-v1/9b715f77-b654-5d38-be81-49173dc191a2/scratchpad"
OUT = "/home/user/personal_v1/MahaPAR_form_snapshot_options.pptx"

NAVY  = RGBColor(0x1C, 0x3C, 0x6E)
BLUE  = RGBColor(0x25, 0x63, 0xEB)
BLUELT= RGBColor(0xDB, 0xEA, 0xFE)
RED   = RGBColor(0xDC, 0x26, 0x26)
REDLT = RGBColor(0xFE, 0xE2, 0xE2)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
GREENLT=RGBColor(0xDC, 0xFC, 0xE7)
AMBER = RGBColor(0xD9, 0x77, 0x06)
AMBERLT=RGBColor(0xFE, 0xF3, 0xC7)
GREY  = RGBColor(0xF8, 0xF9, 0xFB)
BORDER= RGBColor(0xE2, 0xE8, 0xF0)
TEXT  = RGBColor(0x1E, 0x29, 0x3B)
DIM   = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SLATE = RGBColor(0x47, 0x55, 0x69)
WHDIM = RGBColor(0xA9, 0xB7, 0xCE)

S = 0.75
def h(v):  return v * S
def pt(v): return round(v * 72 / 128, 1)

W, H = 960, 540
HDR_H, FTR_H = h(52), h(30)
PAD = h(48)
CW = W - 2 * PAD
BODY_T = HDR_H + h(26)
BODY_B = H - FTR_H - h(18)

prs = Presentation(f"{SKILL}/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)
BLANK = prs.slide_layouts[0]


def slide(title, meta):
    s = prs.slides.add_slide(BLANK)
    canvas(s, WHITE)
    band = rect(s, 0, 0, W, HDR_H, fill=NAVY)
    shape_text(band, [[_r(title, pt(17), WHITE, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=h(300))
    text(s, PAD, 0, CW, HDR_H, [[_r(meta, pt(12), WHDIM)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    return s


def footer(s, n, verdict):
    bar = rect(s, 0, H - FTR_H, W, FTR_H, fill=GREY)
    shape_text(bar, [[_r("Option " + str(n) + " · ", pt(11), NAVY, True),
                      _r(verdict, pt(11), DIM)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=h(60))
    text(s, PAD, H - FTR_H, CW, FTR_H, [[_r(str(n), pt(11), DIM)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def pic(s, path, x, y, w=None, hh=None):
    """Place an image inside a box, preserving aspect and centring it."""
    im = Image.open(path)
    iw, ih = im.size
    if w and hh:
        sc = min(w / iw, hh / ih)
        pw, ph = iw * sc, ih * sc
        px, py = x + (w - pw) / 2, y + (hh - ph) / 2
    elif w:
        pw, ph = w, ih * (w / iw)
        px, py = x, y
    else:
        ph, pw = hh, iw * (hh / ih)
        px, py = x, y
    s.shapes.add_picture(path, X(px), X(py), X(pw), X(ph))
    return px, py, pw, ph


def label(s, x, y, w, txt, colr, bg):
    tagw = w
    box = rect(s, x, y, tagw, h(26), fill=bg, radius=0.3)
    shape_text(box, [[_r(txt.upper(), pt(10.5), colr, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=h(8), m_right=h(8))


def arrow(s, x, y, w, hh):
    text(s, x, y, w, hh, [[_r("→", pt(26), BLUE, True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ══════════════════════════════════ 1 · page silhouettes
s = slide("Option 1 · Page silhouettes", "Volume, not reading")
text(s, PAD, BODY_T, CW, h(26),
     [[_r("Every page of the current form against Form A, at the same scale. "
          "Deliberately unreadable: the eye reads area, not text.", pt(12), DIM)]])

gy = BODY_T + h(34)
# Four columns of three rows fills the body; tiles stay at one shared scale so
# the old and new stacks are directly comparable by area.
tilew, gap = h(112), h(7)
cols = 4
TILE_H = tilew * 1.413
label(s, PAD, gy, h(250), "Current · Form 1 · 11 pages", RED, REDLT)
for i in range(11):
    x = PAD + (tilew + gap) * (i % cols)
    y = gy + h(34) + (TILE_H + gap) * (i // cols)
    pic(s, f"{SCR}/crops/sil_old_{i+1}.png", x, y, w=tilew)

nx = PAD + (tilew + gap) * cols + h(40)
label(s, nx, gy, h(220), "Form A · 2 pages", GREEN, GREENLT)
for i in range(2):
    pic(s, f"{SCR}/crops/sil_new_{i+1}.png", nx + (tilew + gap) * i, gy + h(34), w=tilew)

note = rect(s, nx, gy + h(34) + TILE_H + h(26), h(560), h(150),
            fill=GREY, line=BORDER, radius=0.06)
shape_text(note, [[_r("What this does well", pt(12), NAVY, True)],
                  [_r("The scale of the cut is unmistakable in one look, and nothing "
                      "pretends to be legible. Works for the whole form, for either group.",
                      pt(11), DIM)],
                  [_r("What it cannot do", pt(12), NAVY, True)],
                  [_r("It says nothing about what changed inside the form.", pt(11), DIM)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.35, space_after=pt(4),
           m_left=h(16), m_right=h(14), m_top=h(12))
footer(s, 1, "best for the whole-form view; pairs with a slide that explains the content")

# ══════════════════════════════════ 2 · three stage rows
s = slide("Option 2 · Three stage rows on one slide", "Legibility test")
rows = [("Self-appraisal", "old_self", "new_self"),
        ("Reporting officer", "old_rep", "new_rep"),
        ("Reviewing officer", "old_rev", "new_rev")]
rh = (BODY_B - BODY_T - 2 * h(8)) / 3
for i, (stage, o, n) in enumerate(rows):
    y = BODY_T + (rh + h(8)) * i
    rect(s, PAD, y, CW, rh, fill=GREY, line=BORDER, radius=0.04)
    text(s, PAD + h(10), y, h(110), rh, [[_r(stage, pt(11.5), NAVY, True)]],
         anchor=MSO_ANCHOR.MIDDLE)
    pic(s, f"{SCR}/crops/{o}.png", PAD + h(120), y + h(6), w=h(300), hh=rh - h(12))
    arrow(s, PAD + h(430), y, h(40), rh)
    pic(s, f"{SCR}/crops/{n}.png", PAD + h(476), y + h(6), w=h(390), hh=rh - h(12))
footer(s, 2, "shows all three stages, but nothing on it can actually be read")

# ══════════════════════════════════ 3 · one stage per slide, whole snapshot
# Same construction three times, once per stage, each showing the complete
# before and after snapshot rather than a crop of it.
STAGES = [
    ("Self-appraisal", "old_self", "new_self",
     "Current · Form 1, Section 2", "Form A · Part 2",
     "The officer wrote free prose under open headings and repeated details the "
     "department already holds. Form A asks for targets against achievement, one "
     "significant contribution, and systemic factors — in set fields, with the "
     "officer's own details pre-filled."),
    ("Reporting officer", "old_rep", "new_rep",
     "Current · Form 1, Section 3 · 17 rated items", "Form A · Part 3.1 · 7 dimensions",
     "Three tables of 17 rows, each graded by hand and averaged by hand, become one "
     "table of seven dimensions with written descriptors, and MahaPAR calculates the "
     "weighted overall grade."),
    ("Reviewing officer", "old_rev", "new_rev",
     "Current · Form 1, Section 4B", "Form A · Part 4",
     "The reviewing officer re-graded every dimension a second time. In Form A they "
     "record agreement or disagreement with the reporting officer's overall grade and "
     "their own overall grade, with reasons required only where they differ."),
]
for i, (stage, o, n, olab, nlab, cap_txt) in enumerate(STAGES):
    s = slide("Option 3 · One stage per slide · " + stage,
              "Whole snapshot, before and after")
    CAPH = h(104)
    IMG_T = BODY_T + h(36)
    IMG_H = BODY_B - CAPH - h(14) - IMG_T
    LW, AW = h(400), h(44)
    RW = CW - LW - AW
    label(s, PAD, BODY_T, LW, olab, RED, REDLT)
    pic(s, f"{SCR}/crops/{o}.png", PAD, IMG_T, w=LW, hh=IMG_H)
    arrow(s, PAD + LW, IMG_T, AW, IMG_H)
    nx = PAD + LW + AW
    label(s, nx, BODY_T, RW, nlab, GREEN, GREENLT)
    pic(s, f"{SCR}/crops/{n}.png", nx, IMG_T, w=RW, hh=IMG_H)
    cap = rect(s, PAD, BODY_B - CAPH, CW, CAPH, fill=GREY, line=BORDER, radius=0.04)
    shape_text(cap, [[_r("What the audience sees", pt(12), NAVY, True)],
                     [_r(cap_txt, pt(11), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.35, space_after=pt(4),
               m_left=h(16), m_right=h(16), m_top=h(12))
    footer(s, 3, "the only option where the audience can actually read the change · "
                 + stage + " (" + str(i + 1) + " of 3)")

# ══════════════════════════════════ 4 · page with callout zooms
s = slide("Option 4 · Full page with callout zooms", "Context plus detail")
# The page is scaled to the full body height so the callouts have something
# substantial to point at; PGH/PGW are then used to place the red boxes on it.
PGH = BODY_B - BODY_T - h(36)
_, _, PGW, _ = pic(s, f"{SCR}/crops/page_old06.png", PAD, BODY_T, hh=PGH)
label(s, PAD, BODY_B - h(26), PGW, "Current · Form 1, page 6 of the form", RED, REDLT)
rect(s, PAD + PGW * 0.07, BODY_T + PGH * 0.13, PGW * 0.86, PGH * 0.22,
     fill=None, line=RED, line_w=1.5)
rect(s, PAD + PGW * 0.07, BODY_T + PGH * 0.48, PGW * 0.86, PGH * 0.34,
     fill=None, line=RED, line_w=1.5)
CX = PAD + PGW + h(14)
text(s, CX, BODY_T + PGH * 0.20, h(40), h(24), [[_r("→", pt(20), RED, True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, CX, BODY_T + PGH * 0.60, h(40), h(24), [[_r("→", pt(20), RED, True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
CL = CX + h(48)                      # left edge of the callout column
CWID = (PAD + CW) - CL               # callout width, flush to the right margin
CARD = h(176)
c1 = rect(s, CL, BODY_T, CWID, CARD, fill=GREY, line=BORDER, radius=0.05)
shape_text(c1, [[_r("Work completion · 3 items, graded and averaged by hand", pt(12), NAVY, True)],
                [_r("In Form A this becomes dimensions 1 and 2, and MahaPAR does the "
                    "arithmetic. Two of the three items collapse into 'delivery of "
                    "planned work'.", pt(11), DIM)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.35, space_after=pt(4),
           m_left=h(16), m_right=h(14), m_top=h(14))
c2 = rect(s, CL, BODY_T + CARD + h(16), CWID, CARD, fill=GREY, line=BORDER, radius=0.05)
shape_text(c2, [[_r("Personal attributes · 8 items", pt(12), NAVY, True)],
                [_r("Overall bearing, emotional stability, moral courage and leadership "
                    "are judged separately today. Form A folds them into two dimensions "
                    "with written descriptors behind each.", pt(11), DIM)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.35, space_after=pt(4),
           m_left=h(16), m_right=h(14), m_top=h(14))
WY = BODY_T + 2 * CARD + h(32)
warn = rect(s, CL, WY, CWID, BODY_B - WY, fill=AMBERLT,
            line=RGBColor(0xEB, 0xC8, 0x82), radius=0.06)
shape_text(warn, [[_r("The catch:  ", pt(11.5), AMBER, True),
                   _r("the callouts carry the message, not the page. The page behind "
                      "them is decoration, and a bilingual form needs each callout "
                      "translated to be useful.", pt(11.5), TEXT)]],
           anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4, m_left=h(16), m_right=h(14))
footer(s, 4, "familiar consulting device, but the page itself does no work")

# ══════════════════════════════════ 5 · structural stack
s = slide("Option 5 · Structural stack, no screenshot at all",
          "Block height is proportional to real length")

OLD = [("Part 1 · officer details, chain, leave", 2, SLATE, "Kept, now pre-filled"),
       ("Part 2 · self-appraisal", 2, AMBER, "Cut to about half a page"),
       ("Part 3 · reporting officer", 4, AMBER, "Cut to about one page"),
       ("Part 4A · Collector / Div. Commissioner", 1, RED, "Removed, subject to GAD"),
       ("Part 4B · reviewing officer", 2, RED, "Cut to three lines")]
NEW = [("Part 1", 0.3, SLATE), ("Part 2", 0.5, AMBER), ("Part 3", 0.7, AMBER),
       ("Part 4", 0.12, GREEN), ("Part 5", 0.1, GREEN), ("Part 6", 0.28, GREEN)]

UNIT = h(40)          # grid height of one page of the old form
gy = BODY_T + h(30)
label(s, PAD, BODY_T, h(320), "Current · Form 1 · 11 pages", RED, REDLT)
y = gy
for name, pages, colr, fate in OLD:
    bh = UNIT * pages
    blk = rect(s, PAD, y, h(320), bh - h(3), fill=colr, radius=0.04)
    shape_text(blk, [[_r(name, pt(10.5), WHITE, True)],
                     [_r(str(pages) + (" page" if pages == 1 else " pages"), pt(9.5),
                         RGBColor(0xDD, 0xE4, 0xEE))]],
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2, space_after=pt(2),
               m_left=h(12), m_right=h(10))
    text(s, PAD + h(332), y, h(220), bh - h(3), [[_r(fate, pt(10.5), DIM)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += bh

nx = PAD + h(580)
label(s, nx, BODY_T, h(250), "Form A · 2 pages", GREEN, GREENLT)
y = gy
# Blocks stay proportional, but their labels sit in a side column on a minimum
# pitch so the thin parts (4, 5, 6) do not print on top of one another.
LAB_H, last_lab = h(17), None
for name, pages, colr in NEW:
    bh = UNIT * pages
    blk = rect(s, nx, y, h(250), max(bh - h(3), h(7)), fill=colr, radius=0.04)
    if bh > h(26):
        shape_text(blk, [[_r(name, pt(10), WHITE, True)]],
                   anchor=MSO_ANCHOR.MIDDLE, m_left=h(12), m_right=h(10))
    else:
        ly = y + bh / 2 - LAB_H / 2
        if last_lab is not None and ly < last_lab + LAB_H:
            ly = last_lab + LAB_H
        text(s, nx + h(258), ly, h(200), LAB_H, [[_r(name, pt(9.5), DIM)]],
             anchor=MSO_ANCHOR.MIDDLE)
        last_lab = ly
    y += bh
rect(s, nx, y + h(8), h(250), h(1.5), fill=BORDER)
text(s, nx, y + h(14), h(250), h(20),
     [[_r("Everything below this line is new ground the old form never covered",
          pt(9.5), DIM, ital=True)]])

leg = rect(s, PAD, BODY_B - h(40), h(790), h(40), fill=GREY, line=BORDER, radius=0.06)
shape_text(leg, [[_r("Kept   ", pt(10.5), SLATE, True),
                  _r("·   Simplified   ", pt(10.5), AMBER, True),
                  _r("·   Removed   ", pt(10.5), RED, True),
                  _r("·   New in Form A        ", pt(10.5), GREEN, True),
                  _r("Block height is proportional to the real length of each part.",
                     pt(10.5), DIM)]],
           anchor=MSO_ANCHOR.MIDDLE, m_left=h(16), m_right=h(14))
footer(s, 5, "readable, shows volume and shows what happened to each part")

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
