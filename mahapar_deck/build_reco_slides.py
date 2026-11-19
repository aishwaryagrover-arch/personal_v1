#!/usr/bin/env python3
"""
Five slides for the GAD limitations-and-recommendations deck, built to the same
design as mahapar_deck/slide_mockups.html so they can be imported into Google
Slides and edited there.

Geometry is 1:1 with the mockup's CSS pixels (960 x 540), and font sizes are the
CSS px x 0.75, which is the same conversion the deck itself uses.
"""
import math
import os
import sys

SKILL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
sys.path.insert(0, SKILL)

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from components import rect, text, shape_text, canvas, X, _r

OUT = "/home/user/personal_v1/MahaPAR_APAR_recommendation_slides.pptx"

W, H = 960, 540
NAVY   = RGBColor(0x1B, 0x3A, 0x6B)
NAVY2  = RGBColor(0x11, 0x27, 0x4A)
GOLD   = RGBColor(0xF0, 0xA5, 0x00)
MUT    = RGBColor(0x5A, 0x65, 0x75)
BODY   = RGBColor(0x3A, 0x46, 0x54)
BODY2  = RGBColor(0x2A, 0x34, 0x41)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BANDBG = RGBColor(0xDC, 0xE8, 0xF8)

FORMBG, FORMLN = RGBColor(0xEE, 0xF4, 0xFD), RGBColor(0xC4, 0xD8, 0xF3)
PROCBG, PROCLN, PROCLB = RGBColor(0xFF, 0xF8, 0xE8), RGBColor(0xF0, 0xDB, 0xA4), RGBColor(0xB5, 0x73, 0x0B)
DIGBG,  DIGLN,  DIGLB  = RGBColor(0xED, 0xF6, 0xF0), RGBColor(0xC2, 0xE2, 0xD1), RGBColor(0x1E, 0x7F, 0x52)

RMLB, RMBG = RGBColor(0x76, 0x76, 0x76), RGBColor(0xEC, 0xEC, 0xEC)
SMLB, SMBG = RGBColor(0xB3, 0x53, 0x09), RGBColor(0xFB, 0xE3, 0xCE)
ADLB, ADBG = RGBColor(0x19, 0xA0, 0x5B), RGBColor(0xE7, 0xF4, 0xEC)
TILEBG, TILELN = RGBColor(0xF4, 0xF7, 0xFB), RGBColor(0xD8, 0xE2, 0xEE)
HAIR = RGBColor(0xD5, 0xDC, 0xE6)

PAD = 38
CW = W - 2 * PAD


def pt(px):
    """CSS pixel to point, at the 96dpi the 960x540 grid assumes."""
    return round(px * 0.75, 1)


prs = Presentation(f"{SKILL}/template.pptx")
for sid in list(prs.slides._sldIdLst):
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)
BLANK = prs.slide_layouts[0]


def frame(title, page, sub=None):
    s = prs.slides.add_slide(BLANK)
    canvas(s, WHITE)
    rect(s, 0, 0, W, 6, fill=GOLD)
    text(s, PAD, 20, CW - 112, 34, [[_r(title, pt(25), NAVY, True)]], anchor=MSO_ANCHOR.TOP)
    text(s, PAD, 16, CW, 20, [[_r("IDinsight", pt(13), NAVY, True)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)
    if sub:
        text(s, PAD, 55, CW, 20, [[_r(sub, pt(14), MUT, ital=True)]], anchor=MSO_ANCHOR.TOP)
    rect(s, PAD, 80, CW, 2.5, fill=GOLD)
    text(s, PAD, H - 26, CW, 16, [[_r(str(page), pt(11), RGBColor(0x9A, 0xA4, 0xB2))]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    return s


def band(s, bold, rest=""):
    b = rect(s, PAD, 92, CW, 30, fill=BANDBG)
    rect(s, PAD, 92, 5, 30, fill=NAVY)
    runs = [_r(bold, pt(13), NAVY2, True)]
    if rest:
        runs.append(_r(" " + rest, pt(13), NAVY2))
    shape_text(b, [runs], anchor=MSO_ANCHOR.MIDDLE, m_left=14, m_right=12)


# ══════════════════════════════════════════════ three-column slides
COLT, COLB = 128, H - 24
COLH = COLB - COLT
COLW = (CW - 28) / 3


def column(s, i, bg, ln, head, lead=None):
    x = PAD + (COLW + 14) * i
    rect(s, x, COLT, COLW, COLH, fill=bg, line=ln, radius=0.03)
    lb = NAVY if i == 0 else (PROCLB if i == 1 else DIGLB)
    runs = []
    if lead:
        runs.append(_r(lead + "  ", pt(15), RGBColor(0x9B, 0xAF, 0xCB), True))
    runs.append(_r(head, pt(16), lb, True))
    text(s, x + 13, COLT + 9, COLW - 26, 22, [runs], anchor=MSO_ANCHOR.TOP)
    rect(s, x + 13, COLT + 33, COLW - 26, 1, fill=RGBColor(0xC8, 0xD3, 0xE3))
    return x, lb


def bullets(s, x, y, w, items, accent, pitch=74):
    """Four bullets per column on a fixed pitch.

    Estimating each bullet's height from its character count drifted and let the
    last one collide with the footer, so every bullet now gets an equal slot and
    the columns line up across the slide.
    """
    for label, detail in items:
        paras = [[_r(label, pt(13.5), accent, True)]]
        if detail:
            paras.append([_r(detail, pt(11.5), BODY)])
        text(s, x, y, w, pitch - 6, paras, anchor=MSO_ANCHOR.TOP,
             line_spacing=1.08, space_after=pt(3))
        y += pitch
    return y


def sowhat(s, x, w, line):
    rect(s, x, COLB - 40, w, 1, fill=RGBColor(0xC8, 0xD3, 0xE3))
    text(s, x, COLB - 35, w, 32, [[_r(line, pt(11.5), RGBColor(0x4C, 0x58, 0x6A), ital=True)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.14)


# ══════════════════════════════════════════════ 1 · limitations
s = frame("Where the current APAR loses time and value", 2)
band(s, "Limitations run across the form, the process rules and the digital system",
     "— the recommendations address all three.")

LIMS = [
    (FORMBG, FORMLN, "Form design", "01", NAVY,
     [("Six separate cadre-wise forms",
       "10\u201312 pages each, with overlapping content and no common core."),
      ("Long and repetitive",
       "Data the state already holds is re-entered, plus fields unrelated to performance."),
      ("Overlapping grading dimensions",
       "17\u201325 similar attributes rated separately, adding effort but not information."),
      ("No descriptors, benchmark or evidence standard",
       "Dimensions are undefined, no grade is set as adequate, adverse grades need no proof.")],
     "The form takes long to complete, and the grades do not discriminate."),

    (PROCBG, PROCLN, "Process", "02", PROCLB,
     [("The reporting chain is settled late",
       "Reconstructed at appraisal time, so disputes surface at the end of the cycle."),
      ("Assessment is duplicated across stages",
       "Reviewing authorities re-grade dimensions, and Group A carries an extra Collector stage."),
      ("No consequence for delay, no fallback for a gap",
       "A missed deadline costs nothing; a vacant reporting post stalls the APAR."),
      ("Concerns surface only at year-end",
       "Nothing is on record during the year, and monitoring roles are undefined.")],
     "Nobody is accountable for moving the APAR, and nobody can see where it is."),

    (DIGBG, DIGLN, "Digital interface", "03", DIGLB,
     [("Little is pre-filled, and onboarding is slow",
       "Details, leave and training are keyed in every cycle; NIC email IDs hold up access."),
      ("No system of record for the reporting chain",
       "eHRMS carries no complete organogram, so mapping cannot be auto-populated."),
      ("The system neither computes nor moves anything",
       "Grades, timeliness, reminders, escalation and disclosure are all handled by hand."),
      ("No dashboards and no cycle-level MIS",
       "Monitoring layers cannot see pendency; no grade or timeliness patterns.")],
     "Every rule the process relies on has to be enforced by a person."),
]
for i, (bg, ln, head, num, accent, items, foot) in enumerate(LIMS):
    x, _ = column(s, i, bg, ln, head, num)
    bullets(s, x + 14, COLT + 46, COLW - 28, items, accent)
    sowhat(s, x + 14, COLW - 28, foot)


# ══════════════════════════════════════════════ 2 · recommendations + what they save
s = frame("Forty-nine recommendations, and what they save", 5)
band(s, "Thirty-seven follow a precedent in AIS guidance or another state.",
     "The rest are design choices for Maharashtra.")

LX, LW = PAD, 300                      # left panel: the recommendations
RX = PAD + LW + 20                     # right panel: what they add up to
RW = PAD + CW - RX
TOP, BOT = 134, H - 26

LH = 262
rect(s, LX, TOP, LW, LH, fill=RGBColor(0xF4, 0xF7, 0xFB), line=RGBColor(0xD8, 0xE2, 0xEE),
     radius=0.03)
text(s, LX + 16, TOP + 11, LW - 32, 20,
     [[_r("WHAT CHANGES", pt(11.5), MUT, True)]], anchor=MSO_ANCHOR.TOP)

BUCKETS = [("30", "Redesigning forms", "23 with a state precedent", NAVY),
           ("13", "Streamlining processes", "11 with a state precedent", PROCLB),
           ("6", "Integrating data systems", "3 with a state precedent", DIGLB)]
by = TOP + 40
for num, name, prec, accent in BUCKETS:
    text(s, LX + 16, by, 54, 40, [[_r(num, pt(30), accent, True)]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    text(s, LX + 80, by + 2, LW - 96, 18, [[_r(name, pt(13.5), accent, True)]],
         anchor=MSO_ANCHOR.TOP)
    text(s, LX + 80, by + 20, LW - 96, 16, [[_r(prec, pt(11), BODY)]], anchor=MSO_ANCHOR.TOP)
    by += 56

rect(s, LX + 16, TOP + LH - 50, LW - 32, 1, fill=RGBColor(0xC8, 0xD3, 0xE3))
text(s, LX + 16, TOP + LH - 42, LW - 32, 34,
     [[_r("49 in all", pt(13.5), NAVY, True),
       _r("  \u00b7  37 follow a precedent, 12 are new for Maharashtra", pt(11.5), BODY)]],
     anchor=MSO_ANCHOR.TOP, line_spacing=1.15)

# ── right panel: the headline numbers, then stage by stage
text(s, RX, TOP + 2, RW, 18, [[_r("WHAT THEY ADD UP TO", pt(11.5), MUT, True)]],
     anchor=MSO_ANCHOR.TOP)
HEAD = [("8\u201311 \u2192 2", "Total pages"), ("12 \u2192 4", "Free-text questions"),
        ("17\u201325 \u2192 7", "Dimensions graded"), ("90\u2013125 \u2192 40\u201355", "Minutes \u00b7 all stages")]
tw = (RW - 3 * 10) / 4
for i, (big, small) in enumerate(HEAD):
    x = RX + (tw + 10) * i
    rect(s, x, TOP + 24, tw, 48, fill=RGBColor(0xF4, 0xF7, 0xFB), line=RGBColor(0xD8, 0xE2, 0xEE),
         radius=0.04)
    rect(s, x, TOP + 24, tw, 3.5, fill=NAVY)
    text(s, x + 9, TOP + 31, tw - 18, 22, [[_r(big, pt(13), NAVY, True)]], anchor=MSO_ANCHOR.TOP)
    text(s, x + 9, TOP + 53, tw - 18, 14, [[_r(small.upper(), pt(9.5), MUT)]], anchor=MSO_ANCHOR.TOP)

COLS = [RW * 0.26, RW * 0.14, RW * 0.14, RW * 0.11, RW * 0.23, RW * 0.12]
HDRS = ["APAR stage", "Questions", "Free-text", "Pages", "Completion time", "Saved"]
TABY = TOP + 88
rect(s, RX, TABY, RW, 24, fill=NAVY)
cx = RX
for k, h in enumerate(HDRS):
    text(s, cx + 8, TABY, COLS[k] - 10, 24, [[_r(h, pt(10), WHITE, True)]], anchor=MSO_ANCHOR.MIDDLE)
    cx += COLS[k]

STAGES = [("Self-appraisal", "7 \u2192 6", "5 \u2192 1", "2 \u2192 \u00bd", "45\u201360 \u2192 20\u201330 min", "~52%"),
          ("Reporting officer", "9 \u2192 5", "6 \u2192 2", "4 \u2192 1", "30\u201345 \u2192 15\u201320 min", "~53%"),
          ("Reviewing officer", "6 \u2192 1", "2 \u2192 0", "2 \u2192 \u00bd", "15\u201320 \u2192 5 min", "~71%")]
ry = TABY + 24
for n, row in enumerate(STAGES):
    rect(s, RX, ry, RW, 30, fill=RGBColor(0xFF, 0xFF, 0xFF) if n % 2 else RGBColor(0xF4, 0xF7, 0xFB))
    rect(s, RX, ry + 30, RW, 0.75, fill=RGBColor(0xDD, 0xE4, 0xEE))
    cx = RX
    for k, v in enumerate(row):
        col = NAVY if k == 0 else (RGBColor(0x16, 0x8A, 0x4F) if k == 5 else BODY2)
        text(s, cx + 8, ry, COLS[k] - 10, 30, [[_r(v, pt(10.5), col, k in (0, 5))]],
             anchor=MSO_ANCHOR.MIDDLE)
        cx += COLS[k]
    ry += 30

text(s, RX, ry + 10, RW, 30,
     [[_r("Form A covers Group A and Group B (gazetted); Form B covers Group B (non-gazetted) and "
          "Group C. Completion times are modelled estimates, to be checked with a short round of "
          "officer consultations.", pt(9.5), MUT, ital=True)]],
     anchor=MSO_ANCHOR.TOP, line_spacing=1.2)


# ══════════════════════════════════════════════ stage slides
def stage_slide(title, sub, page, stats, bands_):
    s = frame(title, page, sub)
    tw = (CW - 28) / 3
    for i, (big, small) in enumerate(stats):
        x = PAD + (tw + 14) * i
        rect(s, x, 96, tw, 48, fill=TILEBG, line=TILELN, radius=0.03)
        rect(s, x, 96, tw, 4, fill=NAVY)
        text(s, x + 13, 103, tw - 26, 26, [[_r(big, pt(22), NAVY, True)]], anchor=MSO_ANCHOR.TOP)
        text(s, x + 13, 128, tw - 26, 14, [[_r(small.upper(), pt(10.5), MUT)]], anchor=MSO_ANCHOR.TOP)

    text(s, PAD, 156, CW, 14,
         [[_r("●", pt(10), NAVY, True), _r(" state precedent     ", pt(11), RGBColor(0x44, 0x53, 0x6B)),
           _r("○", pt(10), NAVY, True), _r(" new for Maharashtra", pt(11), RGBColor(0x44, 0x53, 0x6B))]],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.TOP)

    y = 176
    for label, lb, bg, rows in bands_:
        bh = 14 + len(rows) * 22
        rect(s, PAD, y, 108, bh, fill=lb, radius=0.03)
        rect(s, PAD + 108, y, CW - 108, bh, fill=bg)
        shape_text(rect(s, PAD, y, 108, bh, fill=lb, radius=0.03),
                   [[_r(label, pt(13), WHITE, True)]],
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=5, m_right=5)
        ry = y + 7
        for n, (body_txt, chip, is_prec) in enumerate(rows):
            text(s, PAD + 121, ry + 2, CW - 121 - 170, 20, [[_r(body_txt, pt(12), BODY2)]],
                 anchor=MSO_ANCHOR.TOP, line_spacing=1.1)
            cw_ = len(chip) * 4.6 + 16
            cx = PAD + CW - 13 - cw_
            c = rect(s, cx, ry + 2, cw_, 15,
                     fill=NAVY if is_prec else WHITE,
                     line=None if is_prec else NAVY, line_w=1.25, radius=0.5)
            shape_text(c, [[_r(chip, pt(9), WHITE if is_prec else NAVY, True)]],
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, m_left=2, m_right=2)
            ry += 22
            if n < len(rows) - 1:
                rect(s, PAD + 121, ry - 3, CW - 134, 0.75, fill=HAIR)
        y += bh + 9
    return s


stage_slide(
    "Self-appraisal shifts to a shorter, data-linked reflection",
    "Current proforma 1, Section 2  →  Form A, Part 2", 6,
    [("7 → 6", "Questions / fields"), ("5 → 1", "Free-text fields"),
     ("45–60 → 20–30 min", "Completion time (estimated)")],
    [("Removed", RMLB, RMBG, [
        ("Property and assets declaration, and preparing annual work plans for subordinates",
         "Odisha · Nagaland · Manipur", True),
        ("For Group C, separate fields on duties of the post and allocated tasks", "IDinsight", False),
        ("Separate near-term and long-term training-needs fields", "IDinsight", False)]),
     ("Simplified /\nimproved", SMLB, SMBG, [
        ("Work-plan table → key activities, targets and achievements, only where targets were set",
         "Rajasthan · Nagaland", True),
        ("4–5 noteworthy works → 1–2 significant contributions, with word limits",
         "AIS · Goa · Gujarat", True),
        ("“Difficulties in achieving targets” → optional question on systemic constraints",
         "AIS · Goa · Gujarat", True),
        ("Open-ended training needs → structured categories for nominations", "Gujarat", True),
        ("Group C self-appraisal → optional, lighter reflection on noteworthy work", "Odisha", True)]),
     ("Added /\nintegrated", ADLB, ADBG, [
        ("Identity, MahaID, leave and trainings pre-filled from Sevaarth, eHRMS and iGOT",
         "Gujarat · Odisha", True),
        ("Officer maps their own reporting and reviewing authority; custodian validates",
         "GAD feedback", False),
        ("Memos and work log open year-round, attached to the APAR", "GAD feedback", False)])])

stage_slide(
    "Reporting officers assess through a shorter, evidence-linked form",
    "Current proforma 1, Section 3  →  Form A, Part 3", 7,
    [("17–25 → 7", "Dimensions graded"), ("6 → 2", "Free-text questions"),
     ("30–45 → 15–20 min", "Completion time (estimated)")],
    [("Removed", RMLB, RMBG, [
        ("Separate fitness-for-promotion question and technical accuracy check", "IDinsight", False),
        ("State of health, domain recommendations, and the manually entered overall grade",
         "AIS · Goa · Gujarat · Rajasthan", True)]),
     ("Simplified /\nimproved", SMLB, SMBG, [
        ("Rated dimensions cut from 17–25 to 7, with role-specific descriptors in Annexure 3",
         "Odisha · Rajasthan · Gujarat", True),
        ("Grades of 1–2 or 9–10 must be justified by a specific accomplishment or failure",
         "Nagaland · Gujarat", True),
        ("Memos issued during the year attach as justification for a below-benchmark grade",
         "Odisha", True),
        ("Overall assessment structured with prompts: strengths, area to develop, failure", "AIS", True),
        ("Agreement with the self-appraisal asked after the officer's own grading, to reduce anchoring",
         "IDinsight", False)]),
     ("Added /\nintegrated", ADLB, ADBG, [
        ("Training nominations — validate the officer's request and add up to three, each typed",
         "GAD feedback", False),
        ("System data for reference — iGOT hours, eOffice use and attendance, mapped to dimensions",
         "Odisha", True),
        ("Departmental KRAs for the post, shown with the targets recorded in Part 2",
         "GAD feedback", False)])])

stage_slide(
    "Reviewing officers move to exception-based oversight",
    "Current proforma 1, Section 4B  →  Form A, Part 4", 8,
    [("6 → 1–2", "Questions / fields"), ("17 → 0", "Dimensions re-graded"),
     ("15–20 → 5 min", "Completion time (estimated)")],
    [("Removed", RMLB, RMBG, [
        ("No re-grading of individual dimensions, and no repeat of fields already assessed",
         "AIS · Goa · Gujarat · Nagaland", True),
        ("The reviewing officer's separate narrative assessment", "Goa · Gujarat", True),
        ("The Collector / Divisional Commissioner stage for Group A (subject to GAD confirmation)",
         "IDinsight", False)]),
     ("Simplified /\nimproved", SMLB, SMBG, [
        ("The reviewing officer only agrees or disagrees with the overall grade — one click and a signature",
         "AIS · Goa · Gujarat · Nagaland", True),
        ("On disagreement, one alternate overall grade with a 30-word reason; dimension grades are not revised",
         "AIS · Nagaland", True)]),
     ("Added /\nintegrated", ADLB, ADBG, [
        ("Extreme grade justification — a revised grade of 1–2 or 9–10 needs the reason behind it",
         "Nagaland · Gujarat", True),
        ("Timeliness at this stage counts towards the reviewing officer's own APAR score",
         "Gujarat", True)])])


# ══════════════════════════════════════════════ 6 · Form B (Group C)
stage_slide(
    "Form B gives Group C a lighter, fitness-focused appraisal",
    "Current proforma 2  \u2192  Form B, Parts 1 to 4", 9,
    [("8 \u2192 2", "Pages in the form"), ("14 \u2192 6", "Items graded"),
     ("60\u201390 \u2192 25\u201335 min", "Completion time (estimated)")],
    [("Removed", RMLB, RMBG, [
        ("The question on the period for which the officer was observed", "IDinsight", False),
        ("Separate fields on duties of the post and allocated tasks", "IDinsight", False)]),
     ("Simplified /\nimproved", SMLB, SMBG, [
        ("Self-appraisal becomes optional \u2014 noteworthy work only, in 50 words", "Odisha", True),
        ("14 items \u2192 6, in two domains at 60/40, with MahaPAR calculating the overall grade",
         "Nagaland \u00b7 MP", True),
        ("Integrity recorded through set options, plus a fitness-for-promotion judgment",
         "Gujarat \u00b7 Nagaland \u00b7 Odisha", True),
        ("Remarks required only for \u2018Not fit\u2019, extreme grades, or \u2018Fit\u2019 with doubtful integrity",
         "Odisha \u00b7 AIS \u00b7 Nagaland", True),
        ("Reviewing officer revises only the grade or fitness judgment they disagree with",
         "AIS \u00b7 Goa \u00b7 Gujarat \u00b7 Nagaland", True)]),
     ("Added /\nintegrated", ADLB, ADBG, [
        ("The same Part 1 as Form A: pre-filled details, mapped chain and NRC",
         "Gujarat \u00b7 Odisha", True),
        ("Memos attachable where the overall grade is below the benchmark", "Odisha", True),
        ("System data, timeliness for those who report on others, and disclosure of every outcome",
         "Gujarat \u00b7 Odisha \u00b7 AIS", True)])])

# ══════════════════════════════════════════════ 7 · process and system
stage_slide(
    "Process and system changes carry the rest of the gain",
    "Thirteen process recommendations and six on data integration", 10,
    [("13", "Process recommendations"), ("6", "Data-integration recommendations"),
     ("14 of 19", "Follow a state precedent")],
    [("Who does\nwhat", RMLB, RMBG, [
        ("Officers map their own authorities; the custodian validates, and eHRMS pre-populates later",
         "GAD feedback", False),
        ("NRC auto-generated on two grounds, with the reason recorded", "Odisha", True),
        ("Accepting authority acts only where a stage is missing; the Collector stage is removed",
         "Gujarat \u00b7 Odisha", True)]),
     ("Keeping the\ncycle moving", SMLB, SMBG, [
        ("A fixed closure date, online filing only, signed with DSC or eSign",
         "AIS \u00b7 Odisha \u00b7 Nagaland", True),
        ("A stage auto-forwards 15 days past its deadline, and the delay is recorded",
         "AIS \u00b7 Gujarat \u00b7 Odisha", True),
        ("Timeliness marks worth 5% of the score, computed from the dates each stage was signed",
         "Gujarat", True),
        ("Memos through the year; monitoring layers above the custodian; disclosure and representation",
         "Odisha \u00b7 Gujarat \u00b7 AIS", True)]),
     ("What the\nsystem does", ADLB, ADBG, [
        ("Pre-fill from Sevaarth and eHRMS; iGOT hours, eOffice use and attendance shown while grading",
         "Gujarat \u00b7 Odisha", True),
        ("Work log open year-round, feeding the self-appraisal; departmental KRAs shown to the grader",
         "GAD feedback", False),
        ("Departmental enquiry record for the reporting officer, once the DE module is live",
         "Future direction", False)])])


# ══════════════════════════════════════════════ 8 · how the recommendations were arrived at
# Replaces the four-step process slide; step 3 (the MahaPAR portal review) is new.
s = frame("How the recommendations were arrived at", 4)

STEPS = [
    ("Step 1", "State benchmarking study",
     "APAR forms compared across AIS guidance and seven states on 35+ parameters: structure, "
     "self-appraisal, reporting, reviewing, process and records.", False),
    ("Step 2", "Maharashtra field inventory",
     "Every field in all six current forms mapped: who fills it, the response type, the word "
     "limit, and whether the data already sits in Sevaarth or eHRMS.", False),
    ("Step 3", "MahaPAR portal review",
     "The portal walked through end to end to find where the cycle stalls: what is keyed in by "
     "hand, what MahaPAR could compute or move on its own, and which records in Sevaarth, eHRMS "
     "and iGOT could be drawn in rather than re-entered.", True),
    ("Step 4", "Precedent mapping",
     "Each proposed change classified as having clear precedent, partial precedent, a new design "
     "choice for Maharashtra, or a decision for GAD.", False),
    ("Step 5", "Drafts and portal design",
     "A recommendations note, Form A and Form B drafts, and the MahaPAR user windows \u2014 "
     "refined with GAD feedback and partner inputs.", False),
]

BOXW, GAP = 155, 27
BY, BH = 112, 212
for i, (step, head, bodytxt, is_new) in enumerate(STEPS):
    x = PAD + (BOXW + GAP) * i
    bg = RGBColor(0xDC, 0xE8, 0xF8) if is_new else RGBColor(0xE9, 0xF1, 0xFC)
    ln = NAVY if is_new else RGBColor(0xC4, 0xD8, 0xF3)
    rect(s, x, BY, BOXW, BH, fill=bg, line=ln, line_w=1.75 if is_new else 1, radius=0.03)
    text(s, x + 12, BY + 12, BOXW - 24, 14,
         [[_r(step.upper(), pt(10.5), NAVY if is_new else RGBColor(0x6E, 0x84, 0xA6), True)]],
         anchor=MSO_ANCHOR.TOP)
    text(s, x + 12, BY + 30, BOXW - 24, 54, [[_r(head, pt(12.5), NAVY, True)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.12)
    text(s, x + 12, BY + 88, BOXW - 24, BH - 100, [[_r(bodytxt, pt(9.5), BODY)]],
         anchor=MSO_ANCHOR.TOP, line_spacing=1.22)
    if i < len(STEPS) - 1:
        text(s, x + BOXW, BY, GAP, BH, [[_r("\u2192", pt(16), NAVY, True)]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

text(s, PAD, BY + BH + 14, CW, 20,
     [[_r("Step 3 is new: the portal review is what separates the form recommendations from the "
          "process and data-integration ones.", pt(10.5), MUT, ital=True)]], anchor=MSO_ANCHOR.TOP)


prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides._sldIdLst), "slides")
