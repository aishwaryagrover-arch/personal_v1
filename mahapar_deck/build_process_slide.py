#!/usr/bin/env python3
"""
The process-and-system changes slide, on its own.

Kept separate from build_reco_slides.py so this one slide can be rebuilt and
handed over without regenerating the whole deck.
"""
import os
import sys

SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.insert(0, SKILL)

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

OUT = "/home/user/personal_v1/MahaPAR_process_and_system_changes.pptx"

W, H = 960, 540
PAD = 38
CW = W - 2 * PAD

NAVY = RGBColor(0x1B, 0x3A, 0x6B)
NAVY2 = RGBColor(0x11, 0x27, 0x4A)
GOLD = RGBColor(0xF0, 0xA5, 0x00)
MUT = RGBColor(0x5A, 0x65, 0x75)
BODY2 = RGBColor(0x2A, 0x34, 0x41)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BANDBG = RGBColor(0xDC, 0xE8, 0xF8)

SMLB, SMBG = RGBColor(0xB3, 0x53, 0x09), RGBColor(0xFB, 0xE3, 0xCE)
ADLB, ADBG = RGBColor(0x19, 0xA0, 0x5B), RGBColor(0xE7, 0xF4, 0xEC)
ENLB, ENBG = RGBColor(0x5B, 0x6B, 0x7F), RGBColor(0xEE, 0xF1, 0xF5)


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
rect(s, 0, 0, W, 6, fill=GOLD)
text(s, PAD, 20, CW - 112, 34,
     [[_r("Process and system changes carry the rest of the gain", pt(25), NAVY, True)]],
     anchor=MSO_ANCHOR.TOP)
text(s, PAD, 16, CW, 20, [[_r("IDinsight", pt(13), NAVY, True)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)
rect(s, PAD, 80, CW, 2.5, fill=GOLD)
text(s, PAD, H - 26, CW, 16, [[_r("10", pt(11), RGBColor(0x9A, 0xA4, 0xB2))]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

b = rect(s, PAD, 92, CW, 30, fill=BANDBG)
rect(s, PAD, 92, 5, 30, fill=NAVY)
shape_text(b, [[_r("Four changes to the rules of the cycle, four to what MahaPAR does.",
                   pt(13), NAVY2, True),
                _r("  Four of the eight follow a precedent in AIS guidance or another state.",
                   pt(13), NAVY2)]],
           anchor=MSO_ANCHOR.MIDDLE, m_left=14, m_right=12)

text(s, PAD, 128, CW, 14,
     [[_r("●", pt(10), NAVY, True), _r(" state precedent     ", pt(11), RGBColor(0x44, 0x53, 0x6B)),
       _r("○", pt(10), NAVY, True), _r(" GAD suggestion", pt(11), RGBColor(0x44, 0x53, 0x6B))]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)

PROCESS = [
    ("Officers map their own reporting and reviewing authority; the custodian validates", None),
    ("An APAR is auto-forwarded when a stage passes its deadline, and the delay is recorded "
     "against its holder", "AIS \u00b7 Gujarat \u00b7 Odisha"),
    ("Timeliness marks factored into the gradation scores \u2014 timely completion earns +0.5 in "
     "the APAR score", "Gujarat"),
    ("Additional monitoring layers: custodian, cadre monitoring authority, sub-department "
     "monitoring authority and GAD leadership", None),
]
SYSTEM = [
    ("Official details, leave and completed iGOT trainings pre-filled from Sevaarth, PMIS, "
     "eHRMS and iGOT", "Gujarat \u00b7 Odisha"),
    ("MahaPAR auto-calculates the overall grade from the dimension grades", "Goa \u00b7 Nagaland"),
    ("Real-time pendency dashboards, with automatic reminders and escalation, for all "
     "monitoring layers", None),
    ("The work log and memos are open round the year in eHRMS, and are reflected in the MahaPAR "
     "portal at the time of filing", None),
]
ENHANCED = [
    ("Departmental enquiry data shown to the reporting officer", None),
    ("eOffice use shown to the reporting officer while grading", None),
]

LABW, CHIPW, RH = 112, 152, 30
y = 148
BANDS = [("Process\nchanges", SMLB, SMBG, PROCESS),
         ("System\nchanges", ADLB, ADBG, SYSTEM),
         ("Enhanced\n(longer run)", ENLB, ENBG, ENHANCED)]
for title, lb, bg, items in BANDS:
    bh = RH * len(items) + 12
    rect(s, PAD + LABW, y, CW - LABW, bh, fill=bg)
    shape_text(rect(s, PAD, y, LABW, bh, fill=lb, radius=0.02),
               [[_r(title, pt(12.5), WHITE, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=6, m_right=6)
    ry = y + 6
    for n, (body_txt, prec) in enumerate(items):
        text(s, PAD + LABW + 12, ry, CW - LABW - 24 - CHIPW, RH,
             [[_r(body_txt, pt(11.5), BODY2)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.06)
        label = prec if prec else "GAD suggestion"
        cwid = len(label) * 4.4 + 14
        cx = PAD + CW - 12 - cwid
        c = rect(s, cx, ry + 8, cwid, 14, fill=NAVY if prec else WHITE,
                 line=None if prec else NAVY, line_w=1.25, radius=0.5)
        shape_text(c, [[_r(label, pt(8.5), WHITE if prec else NAVY, True)]],
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=2, m_right=2)
        ry += RH
        if n < len(items) - 1:
            rect(s, PAD + LABW + 12, ry - 1, CW - LABW - 24, 0.6, fill=WHITE)
    y += bh + 8

text(s, PAD, y + 2, CW, 24,
     [[_r("Precedents are those recorded in the state benchmarking note.", pt(9.5), BODY2, True)]],
     anchor=MSO_ANCHOR.TOP)

prs.save(OUT)
print("wrote", OUT)
