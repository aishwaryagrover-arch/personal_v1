#!/usr/bin/env python3
"""
MahaPAR APAR reforms: progress update.

Structure follows the GAD progress-update deck (action titles, the
stage-wise effort table, and the same four buckets on every stage slide);
content comes from the IDinsight HTML deck and the v5 form drafts. Visual
language is the HTML deck's.

Geometry: the HTML slide is 1280x720, the PPTX slide is 10in wide on the
component library's 960px grid, so positions scale 0.75 and font sizes
convert at 72/128 pt per HTML px.
"""
import sys

SKILL = ("/root/.claude/skills/synced/"
         "5cc2c782-1bf3-481e-943e-8e6ddab8d220_b0b95a4d-9f00-46d0-a9dc-081549cb06cc/idinsight-pptx")
sys.path.insert(0, f"{SKILL}/references")

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, _r

OUT = "/home/user/personal_v1/MahaPAR_APAR_Reforms_Progress_Update.pptx"

NAVY   = RGBColor(0x1C, 0x3C, 0x6E)
BLUE   = RGBColor(0x25, 0x63, 0xEB)
BLUELT = RGBColor(0xDB, 0xEA, 0xFE)
RED    = RGBColor(0xDC, 0x26, 0x26)
REDLT  = RGBColor(0xFE, 0xE2, 0xE2)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
GREENLT= RGBColor(0xDC, 0xFC, 0xE7)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
AMBERLT= RGBColor(0xFE, 0xF3, 0xC7)
GREY   = RGBColor(0xF8, 0xF9, 0xFB)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
TEXT   = RGBColor(0x1E, 0x29, 0x3B)
DIM    = RGBColor(0x64, 0x74, 0x8B)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
TITLEBG= RGBColor(0xF4, 0xF8, 0xFE)
HDRMUT = RGBColor(0x8A, 0x93, 0xA5)
WHDIM  = RGBColor(0xA9, 0xB7, 0xCE)
WHFAINT= RGBColor(0x7F, 0x90, 0xAD)
SLATE  = RGBColor(0x47, 0x55, 0x69)

S = 0.75
def h(v):  return v * S
def pt(v): return round(v * 72 / 128, 1)

W, H = 960, 540
HDR_H, FTR_H = h(52), h(30)
PAD = h(48)
CW = W - 2 * PAD
BODY_T = HDR_H + h(26)
BODY_B = H - FTR_H - h(18)

prs = Presentation(f"{SKILL}/assets/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)
BLANK = prs.slide_layouts[0]


def new_slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    canvas(s, bg)
    return s


def header(s, title, meta):
    band = rect(s, 0, 0, W, HDR_H, fill=NAVY)
    shape_text(band, [[_r(title, pt(17), WHITE, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=h(300))
    text(s, PAD, 0, CW, HDR_H, [[_r(meta, pt(12), WHDIM)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def footer(s, n, dark=False):
    bar = rect(s, 0, H - FTR_H, W, FTR_H,
               fill=RGBColor(0x16, 0x2F, 0x56) if dark else GREY)
    fg = WHFAINT if dark else DIM
    shape_text(bar, [[_r("IDinsight · Confidential", pt(11), fg)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=0)
    text(s, PAD, H - FTR_H, CW, FTR_H, [[_r(str(n), pt(11), fg)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def callout(s, y, runs, hgt=h(44)):
    box = rect(s, PAD, y, CW, hgt, fill=BLUELT)
    rect(s, PAD, y, h(4), hgt, fill=BLUE)
    shape_text(box, [runs], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4,
               m_left=h(14), m_right=h(14))


def chip(s, x, y, w, hgt, label, before, after):
    """One summary chip: what the metric is, then before and after."""
    box = rect(s, x, y, w, hgt, fill=GREY, line=BORDER, radius=0.08)
    shape_text(box,
               [[_r(label.upper(), pt(10), DIM, True)],
                [_r(before, pt(15), RED, True), _r("  →  ", pt(13), DIM),
                 _r(after, pt(15), GREEN, True)]],
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2, space_after=pt(3),
               m_left=h(14), m_right=h(10))


def bucket(s, x, y, w, hgt, head, items, colr, bg):
    """One of the four buckets: coloured band plus bullet lines, all in the
    card's own frame."""
    card = rect(s, x, y, w, hgt, fill=bg, line=BORDER, radius=0.05)
    band = rect(s, x, y, w, h(26), fill=colr)
    shape_text(band, [[_r(head.upper(), pt(10.5), WHITE, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=h(14), m_right=h(10))
    body = rect(s, x, y + h(26), w, hgt - h(26), fill=None)
    shape_text(body, [[_r("· ", pt(11), colr, True), _r(t, pt(11), TEXT)]
                      for t in items],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.35, space_after=pt(7),
               m_left=h(12), m_right=h(10), m_top=h(10))


def stage_slide(n, title, meta, chips, buckets):
    s = new_slide()
    header(s, title, meta)
    cw3 = (CW - 2 * h(12)) / 3
    ch = h(58)
    for i, (lab, b, a) in enumerate(chips):
        chip(s, PAD + (cw3 + h(12)) * i, BODY_T, cw3, ch, lab, b, a)
    gy = BODY_T + ch + h(16)
    bw = (CW - 3 * h(10)) / 4
    bh = BODY_B - gy
    for i, (head_, items, colr, bg) in enumerate(buckets):
        bucket(s, PAD + (bw + h(10)) * i, gy, bw, bh, head_, items, colr, bg)
    footer(s, n)


# ═══════════════════════════════════════════════════════════ 1 · title
s = new_slide(TITLEBG)
rect(s, W - h(380), 0, h(380), H, fill=NAVY)
text(s, PAD, 0, CW - h(380), HDR_H,
     [[_r("Government of Maharashtra — General Administration Department",
          pt(12), HDRMUT)]], anchor=MSO_ANCHOR.MIDDLE)
tag = rect(s, h(80), h(140), h(230), h(26), fill=BLUELT, radius=0.5)
shape_text(tag, [[_r("APAR REFORMS · PROGRESS UPDATE", pt(11), BLUE, True)]],
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
text(s, h(80), h(180), h(560), h(140),
     [[_r("Simplifying Maharashtra's", pt(40), NAVY, True)],
      [_r("APAR ", pt(40), NAVY, True), _r("Process", pt(40), BLUE, True)]],
     line_spacing=1.1, space_after=0)
text(s, h(80), h(306), h(540), h(44),
     [[_r("Shorter forms, clearer judgement, and a portal that carries the "
          "cycle end to end.", pt(16), DIM)]], line_spacing=1.5)
text(s, h(80), h(392), h(560), h(90),
     [[_r("GAD owners:  ", pt(13), NAVY, True),
       _r("Smt. Suchita Mahadik · Shri Vishal Dhole · Shri Uttam Patro", pt(13), DIM)],
      [_r("Partner organisations:  ", pt(13), NAVY, True),
       _r("IDinsight · CEGIS", pt(13), DIM)],
      [_r("Presented by:  ", pt(13), NAVY, True),
       _r("IDinsight team", pt(13), DIM)]],
     line_spacing=1.45, space_after=pt(4))
ax = W - h(380)
for i, (big, lbl) in enumerate([("6 → 2", "Forms consolidated"),
                                ("17 → 7", "Rated dimensions"),
                                ("60 → 20", "Minutes per officer")]):
    sy = h(150) + h(124) * i
    text(s, ax, sy, h(380), h(60), [[_r(big, pt(44), WHITE, True)]],
         align=PP_ALIGN.CENTER, space_after=0)
    text(s, ax, sy + h(54), h(380), h(20), [[_r(lbl, pt(12), WHDIM)]],
         align=PP_ALIGN.CENTER)
    if i < 2:
        rect(s, ax + h(170), sy + h(92), h(40), 1, fill=RGBColor(0x4A, 0x62, 0x8C))
text(s, PAD, H - h(70), CW - h(380), h(20), [[_r("November 2026", pt(12), HDRMUT)]])

# ═══════════════════════════════════════════════════════════ 2 · agenda
s = new_slide()
header(s, "What this update covers", "MahaPAR — APAR reforms")
agenda = [
    ("The effort the redesigned forms save", "Across the three stages of the cycle"),
    ("Stage by stage: what was retained, simplified, added",
     "Self-appraisal, reporting officer, reviewing officer"),
    ("Platform and process enhancements",
     "What MahaPAR itself does to move the cycle along"),
    ("How we got here", "Benchmarking, field inventory, precedent, drafts"),
    ("Portal design: where we are", "What has been built, and what is in progress"),
    ("Next steps", "Immediate and medium-term"),
]
cw2, gap, ih = (CW - h(10)) / 2, h(10), h(90)
ty = BODY_T + ((BODY_B - BODY_T) - (3 * ih + 2 * gap)) / 2
for i, (t, d) in enumerate(agenda):
    x = PAD + (cw2 + gap) * (i % 2)
    y = ty + (ih + gap) * (i // 2)
    card = rect(s, x, y, cw2, ih, fill=GREY, line=BORDER, radius=0.06)
    shape_text(card, [[_r(t, pt(13.5), NAVY, True)], [_r(d, pt(11.5), DIM)]],
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.35, space_after=pt(3),
               m_left=h(50), m_right=h(16))
    text(s, x + h(18), y, h(28), ih,
         [[_r(str(i + 1), pt(20), RGBColor(0xB5, 0xC8, 0xF5), True)]],
         anchor=MSO_ANCHOR.MIDDLE)
footer(s, 2)

# ══════════════════════════════════════════════ 3 · effort across stages
s = new_slide()
header(s, "The redesigned forms cut effort at every stage of the cycle",
       "Counted from the current forms against drafts A and B")

# ---- four headline boxes -------------------------------------------------
HEAD = [("11 → 2", "Pages in the form",
         "Form A, Group A and B.  Form B: 8 → 1 for Group C"),
        ("17–25 → 7", "Dimensions appraised",
         "Form A.  Form B: 14 → 6"),
        ("13 → 3", "Open-ended fields",
         "Across all three stages of the APAR"),
        ("60–90 → 25–35", "Minutes per APAR",
         "All three stages together")]
bw = (CW - 3 * h(12)) / 4
bh_ = h(126)
for i, (big, lab, sub) in enumerate(HEAD):
    x = PAD + (bw + h(12)) * i
    card = rect(s, x, BODY_T, bw, bh_, fill=GREY, line=BORDER, radius=0.06)
    rect(s, x, BODY_T, bw, h(4), fill=BLUE)
    b, a = big.split(" → ")
    shape_text(card,
               [[_r(lab.upper(), pt(10.5), DIM, True)],
                [_r(b, pt(26), RED, True), _r("  →  ", pt(18), DIM),
                 _r(a, pt(26), GREEN, True)],
                [_r(sub, pt(10.5), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.2, space_after=pt(6),
               m_left=h(14), m_right=h(12), m_top=h(16), m_bottom=h(10))

# ---- stage-wise table ----------------------------------------------------
COLS = [h(250), h(180), h(200), h(160), h(240), h(154)]
HEADS = ["APAR stage", "Questions / fields", "Open-ended questions",
         "Pages in the form", "Completion time", "Time saved"]
ROWS = [("Self-appraisal", "7 → 6", "5 → 1", "2 → ½", "45–60 min → 15–20 min", "~65%"),
        ("Reporting officer", "9 → 5", "6 → 2", "4 → 1", "30–45 min → 10–15 min", "~67%"),
        ("Reviewing officer", "6 → 1", "2 → 0", "1 → ⅕", "15–20 min → 2–5 min", "~80%")]

ty = BODY_T + bh_ + h(16)
hh, rh = h(34), h(54)
cx = PAD
for i, (cwid, lab) in enumerate(zip(COLS, HEADS)):
    cell = rect(s, cx, ty, cwid, hh, fill=NAVY)
    shape_text(cell, [[_r(lab, pt(11), WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE,
               align=PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER,
               m_left=h(12), m_right=h(8))
    cx += cwid
ry = ty + hh
for r, row in enumerate(ROWS):
    cx = PAD
    bg = WHITE if r % 2 == 0 else RGBColor(0xFA, 0xFB, 0xFD)
    for i, (cwid, val) in enumerate(zip(COLS, row)):
        cell = rect(s, cx, ry, cwid, rh, fill=bg, line=BORDER, line_w=0.5)
        if i == 0:
            shape_text(cell, [[_r(val, pt(13), NAVY, True)]],
                       anchor=MSO_ANCHOR.MIDDLE, m_left=h(12), m_right=h(6))
        elif i == 5:
            shape_text(cell, [[_r(val, pt(14), GREEN, True)]],
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                       m_left=h(4), m_right=h(4))
        else:
            b, a = val.split(" → ")
            shape_text(cell, [[_r(b, pt(12.5), RED, True), _r("  →  ", pt(11), DIM),
                               _r(a, pt(12.5), GREEN, True)]],
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                       m_left=h(4), m_right=h(4))
        cx += cwid
    ry += rh

# ---- what is driving the saving -----------------------------------------
dy = ry + h(16)
dh = BODY_B - (dy + h(22))
drivers = [
    ("Shorter, sharper forms", BLUE,
     "Six forms become two. Rated items consolidated under the existing weights. "
     "Narrative kept only where it carries weight."),
    ("Data that fills itself", GREEN,
     "Identity, leave and training pre-filled from Sevaarth, eHRMS and iGOT. "
     "The overall grade calculated by MahaPAR."),
    ("Process and interface", AMBER,
     "One screen per stage, automatic forwarding and reminders, agreement in two "
     "clicks, pendency visible as it builds."),
]
dw = (CW - 2 * h(12)) / 3
for i, (title, colr, body) in enumerate(drivers):
    x = PAD + (dw + h(12)) * i
    card = rect(s, x, dy + h(22), dw, dh, fill=WHITE, line=BORDER, radius=0.06)
    rect(s, x, dy + h(22), h(4), dh, fill=colr)
    shape_text(card, [[_r(title, pt(12.5), NAVY, True)], [_r(body, pt(11), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.38, space_after=pt(5),
               m_left=h(18), m_right=h(14), m_top=h(12))
text(s, PAD, dy, CW, h(18),
     [[_r("WHAT DRIVES THE SAVING", pt(10.5), DIM, True)]])
footer(s, 3)

# ══════════════════════════════════════════════════ 4 · self-appraisal
stage_slide(
    4,
    "Self-appraisal shifts from end-of-year recall to a shorter, work-linked account",
    "Part 2 · the official fills",
    [("Questions / fields", "7", "6"),
     ("Open-ended questions", "5", "1"),
     ("Completion time", "45–60 min", "15–20 min")],
    [("Retained",
      ["The official's own account of the year, in their words",
       "Targets and achievements, where targets were set for the post",
       "The most significant work of the year",
       "Training the official feels they need"],
      SLATE, GREY),
     ("Simplified or removed",
      ["4 to 5 noteworthy works at 100 words each becomes one or two contributions in 100 words",
       "'Difficulties in not achieving targets' becomes an optional, neutral question on systemic factors",
       "The 50-word duty description, the annual work plan question and the property return are removed",
       "Two free-text training boxes become a tick-box list"],
      RED, REDLT),
     ("Added",
      ["A technical cadre module that opens only for engineering, health and teaching cadres",
       "A 30-day window to correct anything pre-filled",
       "A year-round work log the official can draw on when the cycle opens"],
      GREEN, GREENLT),
     ("On MahaPAR",
      ["Identity and leave pre-filled from Sevaarth and eHRMS",
       "Trainings completed pre-filled from iGOT",
       "The whole of Part 2 on one screen, signed with DSC or eSign"],
      BLUE, BLUELT)])

# ═════════════════════════════════════════════════ 5 · reporting officer
stage_slide(
    5,
    "Reporting officers assess through a shorter, more structured and evidence-linked form",
    "Part 3 · the reporting officer fills",
    [("Rated dimensions", "17–25", "7"),
     ("Open-ended questions", "6", "2"),
     ("Completion time", "30–45 min", "10–15 min")],
    [("Retained",
      ["Grading on a 1 to 10 scale, against officers at the same level",
       "The integrity question",
       "A compulsory overall assessment in 100 words",
       "Agreement, or not, with the official's self-appraisal"],
      SLATE, GREY),
     ("Simplified or removed",
      ["17 to 25 rated items become 7 dimensions under the existing weights",
       "Four or more domain recommendations for the next posting are removed",
       "The state-of-health question and the separate remarks on noteworthy works are removed",
       "The weighted average is no longer computed by hand"],
      RED, REDLT),
     ("Added",
      ["Annexure 3 descriptors: what each dimension looks like in a desk post and a field post",
       "A grade of 1–2 or 9–10 cannot be signed without the specific accomplishment or failure",
       "Memos issued during the year can be attached where the grade is below the benchmark",
       "Up to three training nominations of the officer's own"],
      GREEN, GREENLT),
     ("On MahaPAR",
      ["The overall grade is calculated by the system",
       "Self-appraisal, system data and the memo record sit on one screen",
       "iGOT hours, eOffice use and attendance shown for reference, not scored separately"],
      BLUE, BLUELT)])

# ═════════════════════════════════════════════════ 6 · reviewing officer
stage_slide(
    6,
    "Reviewing officers can close an aligned review quickly, and still differ where they must",
    "Part 4 · the reviewing officer fills",
    [("Questions / fields", "6", "1"),
     ("Open-ended questions", "2", "0"),
     ("Completion time", "15–20 min", "2–5 min")],
    [("Retained",
      ["An independent review of the reporting officer's assessment",
       "The power to differ on the outcome",
       "Signature on the record"],
      SLATE, GREY),
     ("Simplified or removed",
      ["Re-grading all 17 dimensions is removed; dimension-wise grades are not revised",
       "The separate 100-word overall assessment is removed",
       "Four or more domain recommendations are removed",
       "The Collector and Divisional Commissioner stage, subject to GAD's confirmation"],
      RED, REDLT),
     ("Added",
      ["One explicit question: agree with the overall grade, or not",
       "Where differing, the reviewing officer's own overall grade and a 30-word reason",
       "A grade of 1–2 or 9–10 needs the specific accomplishment or failure behind it"],
      GREEN, GREENLT),
     ("On MahaPAR",
      ["Agreeing takes two clicks",
       "Group averages and the overall grade shown in one summary",
       "On signing, the APAR moves to the custodian for disclosure"],
      BLUE, BLUELT)])

# ═══════════════════════════════════════ 7 · platform and process
s = new_slide()
header(s, "Platform and process enhancements strengthen the efficiency of the cycle",
       "What MahaPAR does, over and above the form")
blocks = [
    ("1", "Workflow automation",
     ["Each stage forwards automatically to the next officer when a deadline passes",
      "System-generated reminders before and after every deadline",
      "Pending APARs escalate through the monitoring chain"]),
    ("2", "Digital enablement and data integration",
     ["Single sign-on, removing the NIC email barrier",
      "Identity, leave and training pre-filled from Sevaarth, eHRMS and iGOT",
      "iGOT hours, eOffice use and attendance shown to the reporting officer"]),
    ("3", "Timeliness score",
     ["Five per cent of the final score, up to plus or minus 0.5",
      "Counted for every role an official holds: own self-appraisal, assessments, reviews",
      "An auto-forwarded stage counts as late"]),
    ("4", "Monitoring and accountability",
     ["Role-wise tracking of status and pendency, office by office and cadre by cadre",
      "Defined deadlines for every stage of the cycle",
      "Disclosure and representation recorded in the system"]),
]
cw2 = (CW - h(12)) / 2
bh = (BODY_B - BODY_T - h(12)) / 2
for i, (num, title, items) in enumerate(blocks):
    x = PAD + (cw2 + h(12)) * (i % 2)
    y = BODY_T + (bh + h(12)) * (i // 2)
    card = rect(s, x, y, cw2, bh, fill=GREY, line=BORDER, radius=0.05)
    rect(s, x, y, h(4), bh, fill=BLUE)
    band = rect(s, x + h(4), y, cw2 - h(4), h(30), fill=None)
    shape_text(band, [[_r(num + ".  ", pt(14), BLUE, True),
                       _r(title, pt(14), NAVY, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=h(14), m_right=h(10))
    body = rect(s, x + h(4), y + h(30), cw2 - h(4), bh - h(30), fill=None)
    shape_text(body, [[_r("· ", pt(12), BLUE, True), _r(t, pt(12), TEXT)] for t in items],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.4, space_after=pt(6),
               m_left=h(14), m_right=h(12), m_top=h(4))
footer(s, 7)

# ═══════════════════════════════════════════════════ 8 · how we got here
s = new_slide()
header(s, "How we got here", "Four steps from Maharashtra's own forms to drafts A and B")
steps = [
    ("Step 1", "State benchmarking",
     "APAR forms compared across AIS and 7 states on 35+ parameters: structure, "
     "self-appraisal, reporting, reviewing, process and records.", "9 systems · 35+ parameters"),
    ("Step 2", "Maharashtra field inventory",
     "Every field in all six current forms mapped: who fills it, response type, word "
     "limit, whether the data already exists in Sevaarth or eHRMS.", "6 forms · field by field"),
    ("Step 3", "Precedent mapping",
     "Each proposed change classified as having clear precedent, partial precedent, a "
     "new design choice for Maharashtra, or a GAD decision.", "Change by change"),
    ("Step 4", "Drafts A and B, with CEGIS",
     "A recommendations note, then Form A for Group A and B and Form B for Group C, "
     "shaped by GAD workshop feedback.", "Current stage"),
]
sw = (CW - 3 * h(20)) / 4
sh_ = h(210)
for i, (num, title, desc, badge) in enumerate(steps):
    x = PAD + (sw + h(20)) * i
    card = rect(s, x, BODY_T + h(20), sw, sh_, fill=BLUELT,
                line=RGBColor(0xA9, 0xC6, 0xF7), radius=0.05)
    shape_text(card, [[_r(num.upper(), pt(10), BLUE, True)],
                      [_r(title, pt(13), NAVY, True)],
                      [_r(desc, pt(11), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.4, space_after=pt(5),
               m_left=h(16), m_right=h(16), m_top=h(16), m_bottom=h(38))
    pill = rect(s, x + h(16), BODY_T + h(20) + sh_ - h(32), sw - h(32), h(20),
                fill=AMBERLT, line=RGBColor(0xEB, 0xC8, 0x82), radius=0.5)
    shape_text(pill, [[_r(badge, pt(10), AMBER, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
    if i < 3:
        text(s, x + sw, BODY_T + h(20) + sh_ / 2 - h(16), h(20), h(32),
             [[_r("→", pt(18), BLUE)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
callout(s, BODY_B - h(52),
        [_r("What the benchmarking showed:  ", pt(12.5), NAVY, True),
         _r("comparable states run far shorter forms while keeping self-appraisal, "
            "assessment, integrity and review intact. Form and portal have to be "
            "designed together.", pt(12.5), NAVY)], hgt=h(52))
footer(s, 8)

# ═══════════════════════════════════════════════ 9 · portal design status
s = new_slide()
header(s, "Portal design: what has been built, and what is in progress",
       "Parallel workstream — how the APAR is filed, not only what is filed")
uiux = [
    ("Pain-point mapping across user types", "Done",
     "Every existing MahaPAR window reviewed for friction across the official, reporting "
     "officer and establishment officer: the NIC email barrier at login, no pendency view, "
     "and workflow friction at each stage."),
    ("Redesigned landing page", "With GAD",
     "Developed with the GAD team to address login, navigation and visibility. Presented to "
     "Radha ma'am and Vishal sir; Harshvardhan is translating it into Figma."),
    ("User windows for every stage", "In review",
     "Interactive walkthroughs of the revised Form A as end-to-end journeys: custodian, "
     "self-appraisal, reporting officer and reviewing officer. Presented to GAD and being "
     "updated on their feedback."),
    ("Internet and intranet architecture", "With NIC",
     "Deployment options analysed. Recommendation: a public landing page with an "
     "authenticated backend. Awaiting NIC confirmation on policy."),
]
cw2 = (CW - h(12)) / 2
uh = (BODY_B - h(52) - h(12) - BODY_T - h(12)) / 2
for i, (t, status, d) in enumerate(uiux):
    x = PAD + (cw2 + h(12)) * (i % 2)
    y = BODY_T + (uh + h(12)) * (i // 2)
    card = rect(s, x, y, cw2, uh, fill=GREY, line=BORDER, radius=0.06)
    rect(s, x, y, h(4), uh, fill=NAVY)
    shape_text(card, [[_r(t, pt(13), NAVY, True)], [_r(d, pt(11.5), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.42, space_after=pt(5),
               m_left=h(22), m_right=h(96), m_top=h(14), m_bottom=h(10))
    pill = rect(s, x + cw2 - h(86), y + h(12), h(72), h(20), fill=AMBERLT,
                line=RGBColor(0xEB, 0xC8, 0x82), radius=0.5)
    shape_text(pill, [[_r(status, pt(10), AMBER, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
callout(s, BODY_B - h(52),
        [_r("Next in this track:  ", pt(12.5), NAVY, True),
         _r("Figma wireframes for the monitoring dashboards at custodian, cadre and "
            "sub-department level, to be shared with NIC for development alignment.",
            pt(12.5), NAVY)], hgt=h(52))
footer(s, 9)

# ═════════════════════════════════════════════════════ 10 · next steps
s = new_slide()
header(s, "Next steps", "Immediate, and medium-term by December")
cols = [
    ("Next 2–3 weeks", BLUE, [
        ("Incorporate GAD walkthrough feedback",
         "Update Forms A and B and the user windows from the review session."),
        ("Technical cadre and CADA drafts",
         "Complete with CEGIS and share with GAD. Decide between separate technical "
         "forms and one common form with a cadre module."),
        ("Stakeholder consultations, round 1",
         "Pain points in the current process and feedback on the general drafts, with "
         "the stakeholder pool agreed with Vishal sir."),
        ("Figma wireframes with Harsh",
         "Landing page, user windows, and monitoring dashboards at custodian, cadre and "
         "sub-department level."),
    ]),
    ("Medium-term — by December", AMBER, [
        ("Stakeholder consultations, round 2",
         "All form drafts, plus adoption levers to inform what goes into the GRs."),
        ("Enhanced APAR recommendations",
         "The next phase: KPI linkage and competency linkage, for the streamlining stage."),
        ("Portal development support",
         "Support GAD and NIC from user onboarding through to submission across all "
         "stages. Onboarding itself is run by the MahaPAR team."),
        ("KPI framework with CEGIS",
         "Begin with priority positions and build the evidence base for linking KPIs "
         "to the APAR."),
    ]),
]
cw2b = (CW - h(20)) / 2
for i, (head_, colr, items) in enumerate(cols):
    x = PAD + (cw2b + h(20)) * i
    text(s, x, BODY_T, cw2b, h(20), [[_r(head_.upper(), pt(12), colr, True)]])
    rect(s, x, BODY_T + h(22), cw2b, h(2), fill=colr)
    paras = []
    for t, d in items:
        paras.append([_r(t, pt(13), NAVY, True)])
        paras.append([_r(d, pt(11.5), DIM)])
    body = rect(s, x, BODY_T + h(34), cw2b, BODY_B - (BODY_T + h(34)), fill=None)
    shape_text(body, paras, anchor=MSO_ANCHOR.TOP, line_spacing=1.4,
               space_after=pt(7), m_left=0, m_right=h(6), m_top=0)
footer(s, 10)

# ═══════════════════════════════════════════════════════════ 11 · close
s = new_slide(NAVY)
band = rect(s, 0, 0, W, HDR_H, fill=RGBColor(0x16, 0x2F, 0x56))
shape_text(band, [[_r("MahaPAR — APAR reforms", pt(12), WHDIM)]],
           anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=0)
text(s, PAD, 0, CW, HDR_H, [[_r("November 2026", pt(12), WHDIM)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(240), W, h(90), [[_r("Thank you.", pt(64), WHITE, True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(340), W, h(30), [[_r("Questions and discussion welcome", pt(18), WHDIM)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(430), W, h(50),
     [[_r("Aishwarya Grover", pt(16), WHITE, True)],
      [_r("aishwarya.grover@idinsight.org · MahaPAR engagement · IDinsight", pt(13), WHFAINT)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4, space_after=pt(3))
footer(s, 11, dark=True)

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
