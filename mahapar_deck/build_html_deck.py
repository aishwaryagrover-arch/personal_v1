#!/usr/bin/env python3
"""
PPTX replica of the MahaPAR APAR Simplification HTML deck.

The HTML slide is 1280x720. The PPTX slide is 10in wide, and the component
library works on a 960px grid where 1px = 9525 EMU, so geometry scales by
0.75 and font sizes convert at 72/128 pt per HTML px. Both conversions are
exact, so the layout ports 1:1.

Every card carries its own text in its own frame, so one click selects the
card and its text together.
"""
import copy, sys

SKILL = ("/root/.claude/skills/synced/"
         "5cc2c782-1bf3-481e-943e-8e6ddab8d220_b0b95a4d-9f00-46d0-a9dc-081549cb06cc/idinsight-pptx")
sys.path.insert(0, f"{SKILL}/references")

from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from components import rect, text, shape_text, canvas, X, _r

OUT = "/home/user/personal_v1/MahaPAR_APAR_Simplification_Deck.pptx"

# ── palette, straight from the stylesheet ──────────────────────────────────
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
TITLEBG= RGBColor(0xF4, 0xF8, 0xFE)        # flat stand-in for the 135deg wash
HDRMUT = RGBColor(0x8A, 0x93, 0xA5)
WHDIM  = RGBColor(0xA9, 0xB7, 0xCE)        # white at ~60% on navy
WHFAINT= RGBColor(0x7F, 0x90, 0xAD)

S = 0.75                                    # HTML px  ->  960-grid px
def h(v):  return v * S                     # geometry
def pt(v): return round(v * 72 / 128, 1)    # HTML px  ->  points

W, H = 960, 540
HDR_H, FTR_H = h(52), h(30)
PAD = h(48)                                 # left / right gutter
CW = W - 2 * PAD                            # content width
BODY_T = HDR_H + h(26)
BODY_B = H - FTR_H - h(18)

prs = Presentation(f"{SKILL}/assets/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)
BLANK = prs.slide_layouts[0]


# ── chrome ─────────────────────────────────────────────────────────────────
def new_slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    canvas(s, bg)
    return s


def header(s, title, meta, fill=NAVY, fg=WHITE, meta_fg=None):
    band = rect(s, 0, 0, W, HDR_H, fill=fill)
    shape_text(band, [[_r(title, pt(18), fg, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=0)
    text(s, PAD, 0, CW, HDR_H, [[_r(meta, pt(12), meta_fg or WHDIM)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    return band


def footer(s, n, dark=False):
    bar = rect(s, 0, H - FTR_H, W, FTR_H,
               fill=RGBColor(0x16, 0x2F, 0x56) if dark else GREY)
    fg = WHFAINT if dark else DIM
    shape_text(bar, [[_r("IDinsight · Confidential", pt(11), fg)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=0)
    text(s, PAD, H - FTR_H, CW, FTR_H, [[_r(str(n), pt(11), fg)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def callout(s, y, body_runs, hgt=h(44)):
    box = rect(s, PAD, y, CW, hgt, fill=BLUELT, radius=0.0)
    rect(s, PAD, y, h(4), hgt, fill=BLUE)
    shape_text(box, [body_runs], anchor=MSO_ANCHOR.MIDDLE,
               line_spacing=1.4, m_left=h(14), m_right=h(14))
    return box


def note(s, y, runs, hgt=h(40), fill=AMBERLT, line=RGBColor(0xEB, 0xC8, 0x82)):
    box = rect(s, PAD, y, CW, hgt, fill=fill, line=line, radius=0.08)
    shape_text(box, [runs], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4,
               m_left=h(14), m_right=h(14))


def ba_column(s, x, y, w, hgt, head, items, kind):
    """One before/after column: heading plus title+description pairs, all in
    the column's own text frame."""
    fill, bd, fg = ((REDLT, RGBColor(0xEF, 0xA8, 0xA8), RED) if kind == "before"
                    else (GREENLT, RGBColor(0x9A, 0xDC, 0xB4), GREEN))
    col = rect(s, x, y, w, hgt, fill=fill, line=bd, radius=0.05)
    paras = [[_r(head.upper(), pt(11), fg, True)]]
    for t, d in items:
        paras.append([_r(t, pt(12.5), TEXT, True)])
        paras.append([_r(d, pt(11.5), DIM)])
    shape_text(col, paras, anchor=MSO_ANCHOR.TOP, line_spacing=1.35,
               space_after=pt(5), m_left=h(18), m_right=h(18),
               m_top=h(14), m_bottom=h(10))
    return col


def tile(s, x, y, w, hgt, title, desc, accent=None, fill=GREY,
         line=BORDER, t_size=13, d_size=12):
    card = rect(s, x, y, w, hgt, fill=fill, line=line, radius=0.06)
    if accent:
        rect(s, x, y, h(4), hgt, fill=accent)
    shape_text(card, [[_r(title, pt(t_size), NAVY, True)],
                      [_r(desc, pt(d_size), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.42, space_after=pt(4),
               m_left=h(16) + (h(6) if accent else 0), m_right=h(16),
               m_top=h(13), m_bottom=h(8))
    return card


def cmp_table(s, x, y, w, rows, hdr=("Metric", "Current (Forms 1–6)",
                                     "Simplified (Form A / Form B)")):
    """The HTML .cmp-table: grey / red / green header, red and green tinted
    cells, a hairline under every row."""
    lw, cw_ = h(300), (w - h(300)) / 2
    hh, rh = h(28), h(30)
    BEF_BG, AFT_BG = RGBColor(0xFD, 0xF6, 0xF6), RGBColor(0xF6, 0xFC, 0xF8)
    for i, (bg, fg, label) in enumerate([(GREY, DIM, hdr[0]), (REDLT, RED, hdr[1]),
                                         (GREENLT, GREEN, hdr[2])]):
        cx = x if i == 0 else x + lw + cw_ * (i - 1)
        cwid = lw if i == 0 else cw_
        cell = rect(s, cx, y, cwid, hh, fill=bg)
        shape_text(cell, [[_r(label, pt(11), fg, True)]],
                   anchor=MSO_ANCHOR.MIDDLE, m_left=h(12), m_right=h(8))
    rect(s, x, y + hh, w, h(2), fill=BORDER)
    ry = y + hh + h(2)
    for lab, bef, aft in rows:
        for i, (bg, fg, val) in enumerate([(WHITE, DIM, lab), (BEF_BG, RED, bef),
                                           (AFT_BG, GREEN, aft)]):
            cx = x if i == 0 else x + lw + cw_ * (i - 1)
            cwid = lw if i == 0 else cw_
            cell = rect(s, cx, ry, cwid, rh, fill=bg)
            shape_text(cell, [[_r(val, pt(12.5), fg, i > 0)]],
                       anchor=MSO_ANCHOR.MIDDLE, m_left=h(12), m_right=h(8))
        rect(s, x, ry + rh, w, 1, fill=BORDER)
        ry += rh + 1
    return ry


# ═══════════════════════════════════════════════════════ 1 · title
s = new_slide(TITLEBG)
rect(s, W - h(380), 0, h(380), H, fill=NAVY)
text(s, PAD, 0, CW - h(380), HDR_H,
     [[_r("Government of Maharashtra — General Administration Department",
          pt(12), HDRMUT)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, PAD, 0, CW - h(380) - h(12), HDR_H, [[_r("November 2026", pt(12), HDRMUT)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

tag = rect(s, h(80), h(150), h(210), h(26), fill=BLUELT, radius=0.5)
shape_text(tag, [[_r("MAHAPAR REFORM INITIATIVE", pt(12), BLUE, True)]],
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
text(s, h(80), h(190), h(520), h(130),
     [[_r("Simplifying APAR", pt(52), NAVY, True)],
      [_r("for ", pt(52), NAVY, True), _r("Maharashtra", pt(52), BLUE, True)]],
     line_spacing=1.08, space_after=0)
text(s, h(80), h(330), h(520), h(70),
     [[_r("A leaner, fairer, and more efficient Annual Performance Appraisal "
          "system — reducing burden while improving data quality.", pt(17), DIM)]],
     line_spacing=1.55)
text(s, h(80), h(430), h(240), h(50),
     [[_r("Aishwarya Grover", pt(14), NAVY, True)], [_r("IDinsight", pt(13), DIM)]],
     line_spacing=1.3, space_after=1)
text(s, h(330), h(430), h(300), h(50),
     [[_r("In collaboration with", pt(14), NAVY, True)],
      [_r("CEGIS · GAD Maharashtra", pt(13), DIM)]], line_spacing=1.3, space_after=1)

ax = W - h(380)
stats = [("6 → 2", "Forms consolidated"), ("17 → 7", "Rated dimensions"),
         ("60 → 20", "Minutes per officer")]
sy = h(150)
for i, (big, lbl) in enumerate(stats):
    text(s, ax, sy, h(380), h(60), [[_r(big, pt(44), WHITE, True)]],
         align=PP_ALIGN.CENTER, space_after=0)
    text(s, ax, sy + h(54), h(380), h(20), [[_r(lbl, pt(12), WHDIM)]],
         align=PP_ALIGN.CENTER)
    if i < 2:
        rect(s, ax + h(170), sy + h(92), h(40), 1, fill=RGBColor(0x4A, 0x62, 0x8C))
    sy += h(124)
footer(s, 1)

# ═══════════════════════════════════════════════════════ 2 · agenda
s = new_slide()
header(s, "Agenda", "MahaPAR — APAR Simplification")
agenda = [
    ("The efficiency case at a glance",
     "Time savings, form consolidation, and key metrics before and after"),
    ("Self-appraisal — what changed",
     "Officer stage: Part 2 of Form A vs current Forms 1–6"),
    ("Reporting officer — what changed",
     "Dimensions, training split, role descriptors, auto-grade"),
    ("Reviewing officer — what changed",
     "Agree/disagree model, 30-word reason, state precedents"),
    ("How the portal amplifies the gains",
     "Login, pre-fill, auto-forwarding, dashboards, timeliness marks"),
    ("Our process and next steps",
     "Benchmarking → inventory → drafts → consultations → GR"),
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
    text(s, x + h(18), y, h(28), ih, [[_r(str(i + 1), pt(20), RGBColor(0xB5, 0xC8, 0xF5), True)]],
         anchor=MSO_ANCHOR.MIDDLE)
footer(s, 2)

# ═══════════════════════════════════════════════════════ 3 · summary
s = new_slide()
header(s, "The efficiency case at a glance", "Before and after APAR simplification")
cards = [("6 → 2", "Forms consolidated\n(one per group, not per cadre)"),
         ("10 → 2", "Average pages per form\n(Group A/B: 11 → 2)"),
         ("12 → 4", "Free-text fields per APAR\nacross all three stages"),
         ("17 → 7", "Rated dimensions\n(Form A; Group C: 25 → 6)")]
cw4 = (CW - 3 * h(12)) / 4
for i, (val, lbl) in enumerate(cards):
    x = PAD + (cw4 + h(12)) * i
    card = rect(s, x, BODY_T, cw4, h(100), fill=GREY, line=BORDER, radius=0.06)
    rect(s, x, BODY_T, cw4, h(3), fill=BLUE)
    l1, l2 = lbl.split("\n")
    shape_text(card, [[_r(val, pt(28), NAVY, True)],
                      [_r(l1, pt(11.5), DIM)], [_r(l2, pt(11.5), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.25, space_after=pt(3),
               m_left=h(18), m_right=h(14), m_top=h(14))

ty = BODY_T + h(100) + h(20)
CALL_H = h(46)
tbl_end = cmp_table(s, PAD, ty, CW,
          [("Officer time to complete", "45–60 minutes", "15–20 minutes"),
           ("Reporting officer time", "30–45 minutes", "10–15 minutes"),
           ("Reviewing officer time", "15–20 minutes", "2–5 minutes (agree/disagree)"),
           ("Overall grade computation", "Manually computed by RO", "Auto-calculated by MahaPAR"),
           ("Identity and training data", "Entered manually by officer",
            "Pre-filled from Sevaarth / iGOT")])
callout(s, tbl_end + h(14),
        [_r("Time saving across 65,000 Group A/B officers: ", pt(12.5), NAVY, True),
         _r("~60–90 min (current) → ~25–35 min (simplified) per APAR cycle — "
            "approximately 40–45 lakh officer-minutes saved per cycle.", pt(12.5), NAVY)],
        hgt=CALL_H)
footer(s, 3)

# ═══════════════════════════════════════════════ 4 · self-appraisal
s = new_slide()
header(s, "Self-appraisal — what changed", "Part 2 of the form · Officer fills")
cw2 = (CW - h(14)) / 2
CALL4 = h(46)
colh = BODY_B - CALL4 - h(12) - BODY_T
ba_column(s, PAD, BODY_T, cw2, colh, "Current — Forms 1 to 6", [
    ("Duty description", "50-word free-text field across all six forms"),
    ("Work plan / targets", "Open table, self-reported with no predefined KRAs"),
    ("Noteworthy works", "4–5 entries at 100 words each — the heaviest free-text block"),
    ("Difficulties question", "Framed around failures, one free-text field per form"),
    ("Training fields", "Two free-text boxes — current training and future needs"),
    ("Property return and training record", "Manually entered in Section 1 table every year"),
], "before")
ba_column(s, PAD + cw2 + h(14), BODY_T, cw2, colh, "Simplified — Form A / Form B", [
    ("2.1 KRA table (conditional)",
     "Only where targets were set. Pre-filled once role mapping complete. Otherwise skip to 2.2."),
    ("2.2 Significant contribution",
     "One or two pieces of work, 100 words maximum. No attachments required."),
    ("2.3 Systemic factors (optional)",
     "50 words max. Neutral framing. Completely optional — no blame framing."),
    ("2.4 Trainings completed",
     "Pre-filled from iGOT once linked. Officer has 30 days to amend if needed."),
    ("2.5 Additional training (optional)",
     "Tick-box list — no free text. Up to three areas selected."),
    ("2.6 Technical cadre module",
     "Conditional — opens only for engineering, health, and teaching cadres."),
], "after")
callout(s, BODY_T + colh + h(12),
        [_r("Net effect: ", pt(12.5), NAVY, True),
         _r("Free-text burden cut by ~70%. Property and training entry eliminated via "
            "pre-fill. Constraints field reframed as optional — removing blame from the form.",
            pt(12.5), NAVY)], hgt=CALL4)
footer(s, 4)

# ═══════════════════════════════════════════ 5 · reporting officer
s = new_slide()
header(s, "Reporting officer — what changed", "Part 3 of the form · Reporting officer fills")
ba_column(s, PAD, BODY_T, cw2, colh, "Current — Forms 1 to 6", [
    ("17–25 rated dimensions",
     "No role-specific descriptors; no inflation safeguard beyond a general note"),
    ("Agreement with self-appraisal", "Yes/No question at start of section"),
    ("Domain and career ticks", "At least 4 domains in Form 1 and Forms 3–6"),
    ("Training — validate only",
     "RO agrees or disagrees with officer's list, no ability to add own recommendations"),
    ("100-word overall narrative", "Mandatory, completely open-ended, no structured prompts"),
    ("Manual grade computation", "RO manually computes weighted average — error-prone"),
], "before")
ba_column(s, PAD + cw2 + h(14), BODY_T, cw2, colh, "Simplified — Form A / Form B", [
    ("7 dimensions with role-specific descriptors",
     "Annexure 3 gives role-specific guidance (e.g. 'collaboration' differs for "
     "file-processing vs public-facing). Grades 1–2 or 9–10 must be justified."),
    ("Training: validate and nominate",
     "3.5(a) agree or amend officer's request. 3.5(b) add up to 3 own training "
     "recommendations (iGOT or other)."),
    ("3.3 Overall assessment (structured)",
     "100 words with prompts: strengths, area to develop, significant failure, "
     "attitude to weaker sections."),
    ("Auto-calculated overall grade",
     "MahaPAR computes weighted average from 7 dimension grades automatically."),
    ("iGOT, eOffice and attendance visible",
     "System data shown in Part 6 for reference — not scored by the RO directly."),
], "after")
callout(s, BODY_T + colh + h(12),
        [_r("Net effect: ", pt(12.5), NAVY, True),
         _r("Dimensions cut by more than half. Role-specific descriptors reduce "
            "subjectivity. Training nominations shift from validation to active "
            "development. Auto-grade removes arithmetic errors.", pt(12.5), NAVY)], hgt=CALL4)
footer(s, 5)

# ═══════════════════════════════════════════ 6 · reviewing officer
s = new_slide()
header(s, "Reviewing officer — what changed", "Part 4 of the form · Reviewing officer fills")
CALL6, NOTE6 = h(44), h(52)
colh6 = BODY_B - NOTE6 - h(10) - CALL6 - h(12) - BODY_T
ba_column(s, PAD, BODY_T, cw2, colh6, "Current — Form 1", [
    ("Full re-grade on all 17 dimensions",
     "Reviewing officer re-grades every dimension regardless of whether they agree or disagree"),
    ("Yes/No agreement + reasons",
     "Agreement with reporting officer's overall assessment in open free-text"),
    ("100-word overall assessment", "Separate narrative, mandatory and open-ended"),
    ("Domain and career ticks", "Reviewing officer also required to tick 4+ domains"),
], "before")
ba_column(s, PAD + cw2 + h(14), BODY_T, cw2, colh6, "Simplified — Form A / Form B", [
    ("Agree or disagree on overall grade only",
     "4.1: one tick. If agree → sign and done. No dimension-wise re-grading required."),
    ("If disagree: composite score + 30-word reason",
     "4.2: overall grade (1–10) and brief reason in 30 words. Dimension scores are not revised."),
    ("Extreme grades must be justified",
     "If reviewing officer's grade is 1–2 or 9–10, must state the specific "
     "accomplishment or failure."),
], "after")
callout(s, BODY_T + colh6 + h(12),
        [_r("Net effect: ", pt(12.5), NAVY, True),
         _r("Reviewing stage cut from 15–20 min to 2–5 min for agreeing reviews. "
            "Reviewing officer focuses on the composite picture, not re-scoring every "
            "dimension.", pt(12.5), NAVY)], hgt=CALL6)
note(s, BODY_B - NOTE6,
     [_r("State precedents: ", pt(12), AMBER, True),
      _r("AIS PAR rules require reviewing grades only where the reviewing officer "
         "disagrees (Guideline 5.1). Gujarat, Nagaland, and Goa follow the same "
         "agree/disagree model — this is a well-established approach, not a new departure.",
         pt(12), TEXT)], hgt=NOTE6)
footer(s, 6)

# ═══════════════════════════════════════════════════════ 7 · portal
s = new_slide()
header(s, "How the portal amplifies the gains",
       "Simplified forms + improved MahaPAR portal — compounding effect")
portal = [
    ("Single login — no NIC email barrier",
     "Current MahaPAR requires a NIC email ID, blocking many officers. "
     "SACCESS-authenticated portal removes this friction entirely and broadens access."),
    ("Pre-fill from Sevaarth, iGOT and eHRMS",
     "Identity, training hours, and leave data pre-populated. Officers verify rather "
     "than re-enter — eliminating the single biggest time drain in Section 1."),
    ("Auto-forwarding at missed deadlines",
     "Stages forward automatically when a deadline lapses, removing the need for "
     "manual chasing by custodians and establishment officers."),
    ("Real-time pendency dashboard for EOs",
     "Establishment officers can see where each APAR is stuck — by officer, stage, "
     "and department — without calling or emailing."),
    ("Auto-calculated overall grade",
     "MahaPAR computes the weighted average from dimension grades automatically — "
     "eliminating manual arithmetic errors and standardising the output."),
    ("Timeliness marks — built-in accountability",
     "Late completion by a reporting officer is recorded in their own APAR. Creates a "
     "self-enforcing mechanism without a separate enforcement step."),
]
CALL7 = h(46)
ph = (BODY_B - CALL7 - h(12) - BODY_T - 2 * h(10)) / 3
for i, (t, d) in enumerate(portal):
    x = PAD + (cw2 + h(10)) * (i % 2)
    y = BODY_T + (ph + h(10)) * (i // 2)
    tile(s, x, y, cw2, ph, t, d, accent=BLUE)
callout(s, BODY_B - CALL7,
        [_r("Combined effect: ", pt(12.5), NAVY, True),
         _r("Form simplification reduces cognitive load per actor. Portal improvements "
            "reduce friction to complete. Together they address both 'it takes too long' "
            "and 'I don't know where it's stuck'.", pt(12.5), NAVY)], hgt=h(40))
footer(s, 7)

# ═══════════════════════════════════════════════════════ 8 · process
s = new_slide()
header(s, "How we got here — our process", "APAR form simplification approach")
steps = [
    ("Step 1", "State Benchmarking",
     "Compared APAR forms across 9 states (AIS, Gujarat, Odisha, Nagaland, Goa, "
     "Rajasthan, MP, Manipur) on 35+ parameters: structure, self-appraisal, reporting, "
     "reviewing, process, and records.", "9 states · 35+ parameters"),
    ("Step 2", "Maharashtra Field Inventory",
     "Mapped every field in all 6 current Maharashtra APAR forms — who fills it, "
     "response type, word limit, whether data exists in Sevaarth/eHRMS, and an initial "
     "keep/simplify/remove view.", "6 forms · field-by-field"),
    ("Step 3", "Precedent Mapping",
     "For every proposed change in Form A and Form B, identified which states have done "
     "something similar. Classified as: Has precedent · Partial · New · GAD decision · "
     "No precedent needed.", "Change-by-change analysis"),
]
sw = (CW - 2 * h(32)) / 3
sh_ = h(176)
for i, (num, title, desc, badge) in enumerate(steps):
    x = PAD + (sw + h(32)) * i
    card = rect(s, x, BODY_T, sw, sh_, fill=BLUELT,
                line=RGBColor(0xA9, 0xC6, 0xF7), radius=0.05)
    shape_text(card, [[_r(num.upper(), pt(10), BLUE, True)],
                      [_r(title, pt(13), NAVY, True)],
                      [_r(desc, pt(11), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.4, space_after=pt(4),
               m_left=h(16), m_right=h(16), m_top=h(14), m_bottom=h(34))
    pill = rect(s, x + h(16), BODY_T + sh_ - h(30), sw - h(32), h(20),
                fill=AMBERLT, line=RGBColor(0xEB, 0xC8, 0x82), radius=0.5)
    shape_text(pill, [[_r(badge, pt(10), AMBER, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
    if i < 2:
        text(s, x + sw, BODY_T + sh_ / 2 - h(16), h(32), h(32),
             [[_r("→", pt(20), BLUE)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

jy = BODY_T + sh_
for i in range(3):
    rect(s, PAD + (sw + h(32)) * i + sw / 2, jy, 1.5, h(18), fill=BORDER)
rect(s, PAD + sw / 2, jy + h(18), (sw + h(32)) * 2, 1.5, fill=BORDER)
rect(s, W / 2, jy + h(18), 1.5, h(16), fill=BORDER)
text(s, W / 2 - h(12), jy + h(30), h(24), h(20), [[_r("↓", pt(18), BLUE)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

ry = jy + h(54)
steps2 = [
    ("Step 4", "Recommendations Note + CEGIS Alignment",
     "Produced a structured recommendations note covering Form A and Form B changes. "
     "Shared with CEGIS for inputs on technical cadre considerations.", "Shared with partners"),
    ("Step 5", "Draft Forms A and B (v5)",
     "Form A — Group A/B, all cadres, 2 pages. Form B — Group C, 2 pages. Incorporates "
     "GAD workshop feedback and discussions with Vishal sir and Uttam sir.",
     "Current stage → next: consultations"),
]
sh2 = h(196)
x0 = PAD + sw / 2
for i, (num, title, desc, badge) in enumerate(steps2):
    x = x0 + (sw + h(32)) * i
    card = rect(s, x, ry, sw, sh2, fill=RGBColor(0xEF, 0xF6, 0xFF),
                line=RGBColor(0xBF, 0xDB, 0xFE), radius=0.05)
    shape_text(card, [[_r(num.upper(), pt(10), BLUE, True)],
                      [_r(title, pt(13), NAVY, True)],
                      [_r(desc, pt(11), DIM)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.4, space_after=pt(4),
               m_left=h(16), m_right=h(16), m_top=h(14), m_bottom=h(38))
    pill = rect(s, x + h(16), ry + sh2 - h(26), sw - h(32), h(20),
                fill=AMBERLT, line=RGBColor(0xEB, 0xC8, 0x82), radius=0.5)
    shape_text(pill, [[_r(badge, pt(10), AMBER, True)]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=0, m_right=0)
    if i < 1:
        text(s, x + sw, ry + sh2 / 2 - h(16), h(32), h(32),
             [[_r("→", pt(20), BLUE)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 8)

# ═══════════════════════════════════════════════════════ 9 · UI / UX
s = new_slide()
header(s, "MahaPAR portal UI/UX — progress to date",
       "Parallel workstream — improving how APAR is filed, not just what is filed")
uiux = [
    ("UI/UX pain-point mapping",
     "Studied all existing MahaPAR portal windows to map friction across user types: "
     "officer, reporting officer, and establishment officer. Identified the login barrier "
     "(NIC email), absent pendency dashboard, and workflow friction at every stage."),
    ("Redesigned landing page",
     "Iteratively developed a new landing page with the GAD team addressing login, "
     "navigation, and visibility gaps. Presented to Radha ma'am and Vishal sir. "
     "Harshvardhan (GAD developer) now translating to Figma."),
    ("User window templates — all APAR stages",
     "Developed HTML mockups replicating updated Form A as end-to-end digital journeys "
     "across: custodian, self-appraisal, reporting officer, and reviewing officer stages. "
     "Presented to GAD; feedback now being incorporated."),
    ("Internet vs intranet architecture study",
     "Analysed deployment options for the MahaPAR portal. Recommendation: public internet "
     "landing page with SACCESS-authenticated backend. Awaiting NIC confirmation on policy."),
]
CALL9 = h(46)
uh = (BODY_B - CALL9 - h(12) - BODY_T - h(10)) / 2
for i, (t, d) in enumerate(uiux):
    x = PAD + (cw2 + h(10)) * (i % 2)
    y = BODY_T + (uh + h(10)) * (i // 2)
    tile(s, x, y, cw2, uh, t, d, accent=NAVY)
callout(s, BODY_B - CALL9,
        [_r("Upcoming: ", pt(12.5), NAVY, True),
         _r("Figma wireframes for monitoring dashboards (custodian, CADA, "
            "service-controlling levels) in coordination with Harsh. To be shared with NIC "
            "next week for development alignment.", pt(12.5), NAVY)], hgt=CALL9)
footer(s, 9)

# ═══════════════════════════════════════════════════ 10 · next steps
s = new_slide()
header(s, "Next steps", "Immediate (2–3 weeks) and medium-term (by December)")
cols = [
    ("Next 2–3 weeks", BLUE, [
        ("Incorporate GAD walkthrough feedback",
         "Update Form A and Form B PDFs and user window templates based on GAD's "
         "review session feedback."),
        ("Technical and CADA form drafts",
         "Complete with CEGIS; share with GAD by next week. Run 2–3 stakeholder "
         "consultations in parallel to refine field-level inputs."),
        ("Stakeholder consultations — Round 1",
         "Pain points in current process; feedback on general form drafts. Coordinate "
         "with Vishal sir to identify stakeholder pool and agree timeline."),
        ("Figma wireframes with Harsh",
         "Landing page (in progress) + user windows + monitoring dashboards at custodian, "
         "CADA, and service-controlling levels."),
    ]),
    ("Medium-term — by December", AMBER, [
        ("Stakeholder consultations — Round 2",
         "Broader consultations on all form drafts and inputs on adoption levers — "
         "gamification, reinforcements, incentives — to inform what goes into the GRs."),
        ("Enhanced APAR recommendations document",
         "Medium-term vision covering next-phase changes (KPI linkage, competency linkage) "
         "for incorporation into GRs during the streamlining phase."),
        ("MahaPAR portal development support",
         "Support GAD and NIC in end-to-end portal development from user onboarding "
         "through APAR submission across all stages."),
        ("KPI framework (with CEGIS)",
         "Begin KPI framework for priority IAS officer positions; build the evidence base "
         "for KPI linkage with APAR in coordination with CEGIS."),
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

# ═══════════════════════════════════════════════════════ 11 · close
s = new_slide(NAVY)
band = rect(s, 0, 0, W, HDR_H, fill=RGBColor(0x16, 0x2F, 0x56))
shape_text(band, [[_r("MahaPAR — APAR Simplification", pt(12), WHDIM)]],
           anchor=MSO_ANCHOR.MIDDLE, m_left=PAD, m_right=0)
text(s, PAD, 0, CW, HDR_H, [[_r("November 2026", pt(12), WHDIM)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(230), W, h(90), [[_r("Thank you.", pt(64), WHITE, True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(330), W, h(30), [[_r("Questions and discussion welcome", pt(18), WHDIM)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0, h(420), W, h(50),
     [[_r("Aishwarya Grover", pt(16), WHITE, True)],
      [_r("aishwarya.grover@idinsight.org · MahaPAR Engagement · IDinsight",
          pt(13), WHFAINT)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.4, space_after=pt(3))
footer(s, 11, dark=True)

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
