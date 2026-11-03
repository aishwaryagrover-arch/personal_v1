#!/usr/bin/env python3
"""
MahaPAR APAR form simplification: summary deck for GAD.

Built on the IDinsight template. Content slides use the component library
(HTML-fidelity mode) so each card is one editable group with its text in its
own frame, rather than a shape with a separate text box stacked on it.
"""
import copy, sys

SKILL = "/root/.claude/skills/synced/5cc2c782-1bf3-481e-943e-8e6ddab8d220_b0b95a4d-9f00-46d0-a9dc-081549cb06cc/idinsight-pptx"
sys.path.insert(0, f"{SKILL}/references")

from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.ns import qn
from components import *                     # noqa: F403
from components import _r

OUT = "/home/user/personal_v1/MahaPAR_form_simplification_summary.pptx"

prs = Presentation(f"{SKILL}/assets/template.pptx")
for sid in list(prs.slides._sldIdLst):       # drop the 15 demo slides
    rid = sid.get(qn("r:id"))
    if rid:
        prs.part.drop_rel(rid)
    prs.slides._sldIdLst.remove(sid)

BLANK = prs.slide_layouts[0]
n = 0


def num():
    global n
    n += 1
    return n


# ───────────────────────────────── 1 · title
s = prs.slides.add_slide(prs.slide_layouts[2])
s.placeholders[0].text = "Simplifying Maharashtra's APAR"
s.placeholders[3].text = "What changes, and what it saves"
s.placeholders[1].text = "IDinsight with GAD"

# ───────────────────────────────── 2 · agenda
a = prs.slides.add_slide(prs.slide_layouts[1])
a.placeholders[0].text = "Agenda"
a.placeholders[1].text = ("1. What simplification delivers\n"
                          "2. Stage by stage\n"
                          "3. What it saves in time\n"
                          "4. MahaPAR user experience\n"
                          "5. Next steps")

# ───────────────────────────────── 3 · the headline
s = content_slide(prs, BLANK, "What simplification delivers",
                  "Counted from Maharashtra's current forms against the draft Forms A and B", num())
w4 = col_w(4)
stat_callout(s, col_x(0, 4), 132, w4, 104, "6 → 2", "forms for general cadres", DB)
stat_callout(s, col_x(1, 4), 132, w4, 104, "17 → 7", "items the reporting officer grades", DB)
stat_callout(s, col_x(2, 4), 132, w4, 104, "10 → 2", "pages, Group A and B form", DB)
stat_callout(s, col_x(3, 4), 132, w4, 104, "~70%", "less time per APAR, modelled", GR)

accent_bar_list(s, MARGIN, 252, CONTENT_W, [
    ("Less to fill",
     "Forms 1 and 3 to 6 collapse into a two-page Form A; Form 2 becomes a one-page Form B. "
     "Identity, leave, reporting chain and trainings are pre-filled."),
    ("Better to use",
     "Seven defined dimensions in place of 17 undefined items, each anchored to a written descriptor, "
     "with system data and memos visible at the point of grading."),
    ("Faster to run",
     "The overall grade is calculated, stages forward automatically when a deadline passes, and "
     "disclosure and representation happen in MahaPAR."),
], item_h=50, gap=6)

callout_bar(s, MARGIN, 430, CONTENT_W, 34, "Scope:  ",
            "Forms A and B cover the general cadres. The four technical-cadre forms "
            "(engineering, public health doctors, medical and veterinary faculty, other faculty) "
            "are a separate workstream, covered under next steps.")

# ───────────────────────────────── 4 · self-appraisal
s = content_slide(prs, BLANK, "Self-appraisal: what the officer has to do",
                  "Group A and B · current Form 1 against draft Form A", num())
real_table(s, MARGIN, 130, CONTENT_W, 214,
           ["", "Now", "After"],
           [["Questions", "7", "6, of which 3 optional or pre-filled"],
            ["Free-text boxes to write", "5", "1 compulsory, 1 optional"],
            ["Words to draft", "250 to 300", "100, up to 150"],
            ["Table cells to fill", "12 (3 tasks × 4 columns)", "6, only where targets were set"],
            ["Fields pre-filled by the system", "none", "identity, leave, reporting chain, trainings"]],
           col_widths=[300, 268, 328])

accent_bar_list(s, MARGIN, 360, CONTENT_W, [
    ("Three questions removed outright",
     "Assets and liabilities statement · whether an annual work plan was prepared · "
     "difficulties faced in not achieving targets, reframed as an optional, neutral question"),
], item_h=46, gap=0)

callout_bar(s, MARGIN, 416, CONTENT_W, 46, "The work log changes the task:  ",
            "officers record noteworthy work through the year in MahaPAR and pull it into the "
            "self-appraisal, instead of reconstructing twelve months from memory in April.")

# ───────────────────────────────── 5 · reporting officer
s = content_slide(prs, BLANK, "Reporting officer: the biggest single cut",
                  "Group A and B · current Form 1 Section 3 against draft Form A Part 3", num())
w3 = col_w(3)
stat_callout(s, col_x(0, 3), 130, w3, 96, "17 → 7", "items the reporting officer grades", DB)
stat_callout(s, col_x(1, 3), 130, w3, 96, "9 → 5", "questions in the reporting section", DB)
stat_callout(s, col_x(2, 3), 130, w3, 96, "6 → 2", "free-text boxes, one only if disagreeing", DB)

bx, by, bw, bh = zone_column(s, MARGIN, 240, col_w(2), 170,
                             "REMOVED FROM THE REPORTING SECTION", DB, WH, LG)
checklist(s, bx + 14, by + 10, bw - 28,
          ["State of health",
           "Four domain recommendations for the next posting",
           "Agreement with skill upgradation needs",
           "Remarks on noteworthy works",
           "The overall grade entered by hand"],
          mark="—", mark_col=MG, gap=24, size=8)

bx, by, bw, bh = zone_column(s, col_x(1, 2), 240, col_w(2), 170,
                             "ADDED IN ITS PLACE", GR, WH, LG)
checklist(s, bx + 14, by + 10, bw - 28,
          ["Annexure 3 descriptors for every dimension",
           "iGOT hours, eOffice use and attendance shown while grading",
           "Memos attachable where the grade is below benchmark",
           "A grade of 1-2 or 9-10 cannot be signed without a reason",
           "The overall grade calculated by MahaPAR"],
          mark="+", mark_col=GR, gap=24, size=8)

callout_bar(s, MARGIN, 428, CONTENT_W, 34, "Why it matters most here:  ",
            "a reporting officer fills this once per reportee, so the saving multiplies "
            "with the number of officers mapped to them.")

# ───────────────────────────────── 6 · reviewing officer
s = content_slide(prs, BLANK, "Reviewing officer: from a second appraisal to a decision",
                  "Group A and B · current Form 1 Section 4B against draft Form A Part 4", num())
real_table(s, MARGIN, 130, CONTENT_W, 182,
           ["", "Now", "After"],
           [["Questions", "6", "1 if agreeing, 2 if not"],
            ["Free-text boxes", "2, including a 100-word assessment", "none if agreeing, one 30-word reason if not"],
            ["Domain recommendations", "4 entries", "removed"],
            ["Overall grade", "entered by hand", "carried forward, or replaced with a reason"]],
           col_widths=[300, 268, 328])

accent_bar_list(s, MARGIN, 328, CONTENT_W, [
    ("Agreeing is now two clicks",
     "The reviewing officer is asked about the overall grade, not the individual dimensions. "
     "Dimension-wise grades are not revised."),
    ("One stage fewer in the chain, subject to confirmation",
     "Removing the Collector and Divisional Commissioner stage for Group A officers is still "
     "to be settled with GAD."),
], item_h=50, gap=6)

callout_bar(s, MARGIN, 448, CONTENT_W, 30, "Group C goes furthest:  ",
            "14 graded items become 6, and the self-appraisal becomes optional.", kind="warn")

# ───────────────────────────────── 7 · narrative to evidence
s = content_slide(prs, BLANK, "From narrative to evidence",
                  "A 1 to 10 grade with no definition behind it is not an objective grade", num())
items = [
    ("1", "Grades are anchored", "Annexure 3 sets out what each dimension looks like in a "
     "desk post and in a field post. There is no descriptor in the current form."),
    ("2", "Evidence sits beside the grade", "iGOT learning hours, eOffice use and attendance are "
     "shown while grading. Memos issued during the year can be attached where the grade is below 6."),
    ("3", "Extremes must be justified", "A grade of 1-2 or 9-10 cannot be signed without the "
     "specific accomplishment or failure behind it."),
    ("4", "The score is computed, not declared", "MahaPAR calculates the weighted average. "
     "Timeliness marks are generated from the system's own record."),
]
y = 132
for i, (num_, title, desc) in enumerate(items):
    ladder_rung(s, MARGIN, y, CONTENT_W, 72, num_, title, desc, DB if i % 2 == 0 else DB2)
    y += 78

callout_bar(s, MARGIN, 452, CONTENT_W, 30, "The shift:  ",
            "the appraisal stops being an opinion recorded once a year and becomes a judgement "
            "the record can support.")

# ───────────────────────────────── 8 · time
s = content_slide(prs, BLANK, "What it saves in time",
                  "Modelled from the form content, not yet measured", num())
real_table(s, MARGIN, 128, 560, 152,
           ["Per APAR", "Now", "Forms", "Forms + portal"],
           [["Self-appraisal", "~35 min", "~12 min", "~10 min"],
            ["Reporting officer", "~30 min", "~10 min", "~9 min"],
            ["Reviewing officer", "~14 min", "~4 min", "~2 min"]],
           col_widths=[200, 120, 120, 120])

bx, by, bw, bh = zone_column(s, 608, 128, 320, 152, "THE NUMBER THAT LANDS", DB, WH, PB)
box = rect(s, bx + 12, by + 10, bw - 24, bh - 22, fill=WH, radius=0.06)
shape_text(box, [[_r("5 hours → 1.5 hours", 15, DB, True)],
                 [_r("for a reporting officer with ten reportees, per cycle", 8, DG)]],
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2, space_after=6,
           m_left=10, m_right=10)

bx, by, bw, bh = zone_column(s, MARGIN, 298, col_w(2), 136, "HOW THE MODEL IS BUILT", MG, WH, LG)
checklist(s, bx + 14, by + 10, bw - 28,
          ["Drafting considered prose: 2 minutes per 50 words",
           "A structured input (grade, tick, drop-down): 20 seconds",
           "Manual arithmetic across three groups: 4 minutes",
           "Retrieving records the form asks for: 10 minutes, now zero"],
          mark="·", mark_col=DB, gap=24, size=8)

bx, by, bw, bh = zone_column(s, col_x(1, 2), 298, col_w(2), 136, "WHAT THE PORTAL ADDS", DB2, WH, LG)
checklist(s, bx + 14, by + 10, bw - 28,
          ["No printing, signing or movement between offices",
           "Reminders and auto-forwarding instead of chasing",
           "Disclosure and representation online",
           "Pendency visible as it builds, not at year end"],
          mark="·", mark_col=DB2, gap=24, size=8)

callout_bar(s, MARGIN, 448, CONTENT_W, 32, "To be validated:  ",
            "a short round of consultations with officers would turn these modelled times into "
            "observed ones.", kind="warn")

# ───────────────────────────────── 9 · process
s = content_slide(prs, BLANK, "How we got here",
                  "Four steps, from Maharashtra's own forms to the drafts in front of you", num())
nw, gap = 206, 24
xs = [MARGIN + i * (nw + gap) for i in range(4)]
labels = [
    ["1", "Review the current forms", "All six forms read against structure, questions, "
     "grading, narrative load and timelines"],
    ["2", "Benchmark", "AIS guidance and the forms of Goa, Manipur, Rajasthan, Madhya Pradesh, "
     "Gujarat, Nagaland and Odisha, on 35+ parameters"],
    ["3", "Map precedent", "Each recommendation marked as having clear precedent, partial "
     "precedent, or as a new design choice for Maharashtra"],
    ["4", "Draft and test", "40 recommendations translated into Forms A and B and into the "
     "MahaPAR user flows"],
]
for i, (num_, head, body) in enumerate(labels):
    card = rect(s, xs[i], 136, nw, 196, fill=LG, radius=0.06)
    rect(s, xs[i], 136, nw, 5, fill=DB)
    shape_text(card, [[_r(num_, 20, LB, True)],
                      [_r(head, 10, DB, True)],
                      [_r(body, 8, DG)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.2, space_after=6,
               m_left=14, m_right=12, m_top=16, m_bottom=10)
    if i < 3:
        arrow(s, xs[i] + nw, 210, gap, 40)

accent_bar_list(s, MARGIN, 348, CONTENT_W, [
    ("Simplification does not cost the appraisal anything",
     "Comparator states run shorter forms while keeping self-appraisal, assessment, integrity "
     "and review intact."),
    ("Form and portal have to be designed together",
     "The most consequential changes are about how the APAR moves, what is pre-filled and what "
     "happens when a deadline passes."),
], item_h=50, gap=6)

# ───────────────────────────────── 10 · UI and UX
s = content_slide(prs, BLANK, "MahaPAR user experience: where we are",
                  "The revised forms translated into screens, built as working prototypes", num())
bx, by, bw, bh = zone_column(s, MARGIN, 130, col_w(2), 200, "BUILT AND WALKED THROUGH", DB, WH, LG)
checklist(s, bx + 14, by + 12, bw - 28,
          ["Official: self-appraisal, work log and memos",
           "Reporting officer: self-appraisal, system data and memos on one screen",
           "Reviewing officer: agree in two clicks, or record your own grade",
           "Custodian: mapping, pendency tracking, reminders and disclosure",
           "A technical-cadre module that opens KPIs for the designation"],
          mark="✓", mark_col=GR, gap=34, size=8)

bx, by, bw, bh = zone_column(s, col_x(1, 2), 130, col_w(2), 200, "IN PROGRESS", AM, WH, LG)
checklist(s, bx + 14, by + 12, bw - 28,
          ["Landing page and navigation, with the GAD design team",
           "Monitoring screens for the Cadre and Sub Department Monitoring Authorities",
           "State-level view for the Super Admin",
           "Review of the NIC dashboard prototypes",
           "Role and responsibility reference for the Government Resolution"],
          mark="·", mark_col=AM, gap=34, size=8)

callout_bar(s, MARGIN, 350, CONTENT_W, 34, "Design principle:  ",
            "every question an official answers should be one they can answer from the record, "
            "on one screen, without toggling between tabs.")

accent_bar_list(s, MARGIN, 396, CONTENT_W, [
    ("Live prototypes, not mock-ups",
     "The walkthroughs are interactive: grading changes the score, a below-benchmark grade opens "
     "the memo panel, and the reviewing officer's screen updates with it."),
], item_h=50, gap=0)

# ───────────────────────────────── 11 · next steps
s = content_slide(prs, BLANK, "Next steps",
                  "Two tracks, running in parallel", num())
bx, by, bw, bh = zone_column(s, MARGIN, 128, col_w(2), 320,
                             "TRACK 1 · FORM SIMPLIFICATION", DB, WH, LG)
inner = rect(s, bx + 12, by + 10, bw - 24, 128, fill=WH, radius=0.06)
shape_text(inner, [[_r("IMMEDIATE · NEXT FEW WEEKS", 7.5, MG, True)],
                   [_r("Close the open design questions on Forms A and B with GAD: weights, "
                       "deadlines, the accepting and Collector stages.", 8, DG)],
                   [_r("Begin quick consultations with position holders in the technical cadres, "
                       "on the questions that fit their work and on whether measurable KPI data "
                       "already exists in the department.", 8, DG)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.18, space_after=5,
           m_left=12, m_right=10, m_top=10, m_bottom=8)
inner = rect(s, bx + 12, by + 148, bw - 24, 130, fill=WH, radius=0.06)
shape_text(inner, [[_r("INTERMEDIATE · NEXT FEW MONTHS", 7.5, MG, True)],
                   [_r("Decide the technical-cadre approach: separate forms for engineering, "
                       "health and teaching, or one common form with a cadre module.", 8, DG)],
                   [_r("Rationalise the four technical forms, which today grade 20 to 25 items "
                       "each, around measurable outputs for those roles.", 8, DG)],
                   [_r("Finalise the forms and the instructions for the Government Resolution.", 8, DG)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.18, space_after=5,
           m_left=12, m_right=10, m_top=10, m_bottom=8)

bx, by, bw, bh = zone_column(s, col_x(1, 2), 128, col_w(2), 320,
                             "TRACK 2 · UI AND UX", DB2, WH, LG)
inner = rect(s, bx + 12, by + 10, bw - 24, 128, fill=WH, radius=0.06)
shape_text(inner, [[_r("IMMEDIATE · NEXT FEW WEEKS", 7.5, MG, True)],
                   [_r("Finalise the MahaPAR screens for the user layer: official, reporting "
                       "officer and reviewing officer.", 8, DG)],
                   [_r("Finalise the monitoring layer: custodian, Cadre Monitoring Authority, "
                       "Sub Department Monitoring Authority and State Administrator.", 8, DG)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.18, space_after=5,
           m_left=12, m_right=10, m_top=10, m_bottom=8)
inner = rect(s, bx + 12, by + 148, bw - 24, 130, fill=WH, radius=0.06)
shape_text(inner, [[_r("INTERMEDIATE · NEXT FEW MONTHS", 7.5, MG, True)],
                   [_r("Hand the finalised screens to the NIC team and work with them through "
                       "development and deployment on MahaPAR.", 8, DG)],
                   [_r("Support the cycle as it opens on the new forms.", 8, DG)]],
           anchor=MSO_ANCHOR.TOP, line_spacing=1.18, space_after=5,
           m_left=12, m_right=10, m_top=10, m_bottom=8)

callout_bar(s, MARGIN, 460, CONTENT_W, 30, "Running alongside:  ",
            "onboarding of users onto MahaPAR, led by the MahaPAR team.")

# ───────────────────────────────── 12 · close
s = prs.slides.add_slide(prs.slide_layouts[6])
s.placeholders[0].text = "Thank you"

prs.save(OUT)
print("wrote", OUT, "·", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
