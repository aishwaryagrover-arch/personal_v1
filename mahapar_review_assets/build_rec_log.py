#!/usr/bin/env python3
"""
A log of every APAR simplification recommendation, with where it came from, so
each one can be kept or dropped before it goes into the deck.

Rows 1-40 are the recommendations in the simplification note, with the Precedent
column copied from the note itself. Rows 41-49 are the additions drafted after
the GAD discussions; those are the ones to decide on.

Source:
  Precedent        a state or AIS precedent exists, named in the note
  Partial          precedent for part of it only; the note says so
  IDinsight        a design choice for Maharashtra; note says 'no state
                   precedent' or 'not applicable'
  GAD discussion   came out of the GAD feedback, not the benchmarking study
Status: Settled, or To confirm where the note or a later discussion left it open.
"""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "/home/user/personal_v1/MahaPAR_recommendation_log.xlsx"

# (#, section, recommendation, precedent as printed in the note, source, status)
ROWS = [
    (1, "Whole form", "Replace Forms 1 and 3-6 with a two-page Form A, and Form 2 with a one-page Form B", "Odisha, Nagaland", "Precedent", "Settled"),
    (2, "Process", "Auto-forward each stage to the next when the notified deadline is missed, and record the delay", "AIS, Gujarat, Odisha", "Precedent", "Settled"),
    (3, "Process", "Close the cycle on a fixed date; accept online filing only, signed with DSC or eSign", "AIS, Odisha, Nagaland; Gujarat, Odisha", "Precedent", "Settled"),
    (4, "Instructions", "Move instructions and examples to a separate page at the end of each form", "Not applicable", "IDinsight", "Settled"),
    (5, "Form A · Part 1", "Pre-fill identity from Sevaarth and leave from eHRMS; establishment officer verifies Part 1", "Gujarat", "Precedent", "Settled"),
    (6, "Form A · Part 1", "Retain the date of appointment to the present post", "Current Maharashtra form", "Precedent", "Settled"),
    (7, "Form A · 1.1", "The officer enters the reporting and reviewing officers; the establishment officer verifies", "No state precedent", "IDinsight", "To confirm"),
    (8, "Form A · 1.2", "Allow a No Report Certificate where service under a reporting officer is under three months", "Odisha", "Precedent", "Settled"),
    (9, "Form A · Part 1", "Remove the property return date and the assets questions", "Odisha, Nagaland, Manipur", "Precedent", "Settled"),
    (10, "Form A · 2.1", "Ask for targets only where they were set; move to a drop-down once KPIs are linked", "Rajasthan, Nagaland", "Precedent", "Settled"),
    (11, "Form A · 2.2", "Replace four to five noteworthy works with one or two significant contributions (100 words)", "AIS, Goa, Gujarat", "Precedent", "Settled"),
    (12, "Form A · 2.3", "Replace 'difficulties faced' with an optional, neutral question on systemic factors", "AIS, Goa, Gujarat", "Precedent", "Settled"),
    (13, "Form A · 2.4", "List trainings completed during the year, pre-filled from iGOT once linked", "Odisha; central DoPT (2025)", "Precedent", "To confirm"),
    (14, "Form A · 2.5", "Ask for additional training needed, up to three areas, from a set category list", "Gujarat (category list is new)", "Partial", "Settled"),
    (15, "Form A · 2.6", "One common form for all cadres, with a toggle opening a cadre-specific module", "Odisha; CPWD, AIIMS, UGC formats", "Precedent", "Settled"),
    (16, "Form A · Part 3", "Remove the question on the period for which the reporting officer observed the work", "Not applicable", "IDinsight", "Settled"),
    (17, "Form A · 3.1", "Consolidate the 17 graded items into dimensions under the existing 40/30/30 weights", "Odisha, Nagaland, Rajasthan, Gujarat; Goa, Nagaland", "Precedent", "To confirm"),
    (18, "Form A · 3.1", "Where the overall grade is below 6, allow memos issued during the year to be attached", "Odisha", "Precedent", "Settled"),
    (19, "Form A · 3.2", "Record integrity through set options, with a confidential note if doubtful", "Gujarat, Nagaland", "Precedent", "Settled"),
    (20, "Form A · 3.3", "Make the overall assessment compulsory; require grades of 1-2 or 9-10 to be justified", "AIS, Nagaland, Gujarat", "Precedent", "Settled"),
    (21, "Form A · 3.4", "Ask whether the reporting officer agrees with the self-appraisal after their own assessment", "No state precedent", "IDinsight", "Settled"),
    (22, "Form A · Part 3", "Remove state of health, domain recommendations, skill-upgradation agreement, manual grade", "AIS, Goa, Gujarat, Rajasthan, Odisha", "Precedent", "Settled"),
    (23, "Form A · Part 3", "Do not add a separate fitness-for-promotion question or a technical accuracy check", "Not applicable", "IDinsight", "Settled"),
    (24, "Form A · 4.1-4.2", "The reviewing officer revises only what they disagree with, with reasons", "AIS, Goa, Gujarat, Nagaland", "Precedent", "Settled"),
    (25, "Form A · Part 4", "Remove the reviewing officer's narrative and the Collector / Divisional Commissioner stage", "Goa, Gujarat; no precedent for removing a Collector stage", "Partial", "To confirm"),
    (26, "Form A · Part 5", "The accepting authority acts only where the reporting or reviewing stage is incomplete", "Gujarat, Odisha", "Precedent", "Settled"),
    (27, "Form A · Part 6", "Timeliness marks of up to +/-0.5, worth 5% of the score, once eHRMS mapping is live", "Gujarat; deduction for delay has no precedent", "Partial", "Settled"),
    (28, "Form A · Part 6", "Show the reporting officer iGOT hours, eOffice use and attendance as reference", "Odisha; eOffice and attendance have no precedent", "Partial", "Settled"),
    (29, "Form A · Part 6", "Disclose the completed APAR through MahaPAR, with a 15-day representation window", "AIS", "Precedent", "Settled"),
    (30, "Form B · Part 1", "Use the same Part 1 as Form A, including the chain and the NRC request", "Gujarat, Odisha", "Precedent", "Settled"),
    (31, "Form B · Part 2", "Make the self-appraisal optional: noteworthy work only, in 50 words", "Odisha", "Precedent", "Settled"),
    (32, "Form B · Part 3", "Remove the question on the period of observation", "Not applicable", "IDinsight", "Settled"),
    (33, "Form B · 3.1", "Grade a short set of items in two domains, with MahaPAR calculating the overall grade", "Nagaland, MP", "Precedent", "To confirm"),
    (34, "Form B · 3.1", "Allow memos to be attached where the overall grade is below 6", "Odisha", "Precedent", "Settled"),
    (35, "Form B · 3.2-3.3", "Record integrity through set options and ask whether the employee is fit for promotion", "Gujarat, Nagaland; Odisha, MP", "Precedent", "Settled"),
    (36, "Form B · 3.4", "Require remarks only for 'Not fit', extreme grades, or 'Fit' with doubtful integrity", "Odisha; AIS, Nagaland, Gujarat; last case has no precedent", "Partial", "Settled"),
    (37, "Form B · Part 4", "The reviewing officer revises only the grades or fitness judgment they disagree with", "AIS, Goa, Gujarat, Nagaland", "Precedent", "Settled"),
    (38, "Form B · Part 5", "The accepting authority acts only when the reporting or reviewing stage is incomplete", "Gujarat, Odisha (partial)", "Partial", "Settled"),
    (39, "Form B · Part 6", "Same system data as Form A; timeliness for those who report on others; disclose every outcome", "Gujarat; Odisha; AIS", "Precedent", "Settled"),
    (40, "Scoring", "Final score is the reporting officer's weighted grade; 95% plus 5% timeliness once live", "Gujarat", "Precedent", "Settled"),

    (41, "Form A/B · 1.1", "Officers map their own authorities, validated by the custodian; eHRMS organogram later", "No state precedent", "GAD discussion", "To confirm"),
    (42, "Process", "Reporting officer may issue memos through the year; the officer may respond on record", "Odisha (for attaching memos)", "GAD discussion", "To confirm"),
    (43, "Process", "Monitoring layers above the custodian: cadre and sub-department authorities, and GAD", "Gujarat (defaulters flagged to cadre authority)", "IDinsight", "Settled"),
    (44, "Form A · 2.2", "A work log open through the year, from which the significant contribution can be drawn", "No state precedent", "IDinsight", "Settled"),
    (45, "Form A · 2.7", "An optional field of feedback for the reporting officer, pooled and shared anonymously", "No state precedent", "GAD discussion", "To confirm"),
    (46, "Form A · 3.1", "An annexure describing what each dimension looks like in different kinds of post", "Not applicable", "IDinsight", "To confirm"),
    (47, "Form A · 3.1", "Show the reporting officer the departmental KRAs attached to the post while grading", "No state precedent", "GAD discussion", "To confirm"),
    (48, "Form A · Part 3", "Show the reporting officer the departmental enquiry record for the officer", "No state precedent", "GAD discussion", "To confirm"),
    (49, "Form B", "Apply the mapping, memos, feedback field and enquiry record to Form B as in Form A", "As for Form A", "IDinsight", "To confirm"),
]

HEAD = ["#", "Section", "Recommendation", "Precedent (as printed in the note)",
        "Source", "Status", "Include? (Y / N)", "Your note"]
WIDTH = [5, 18, 72, 44, 16, 12, 15, 30]

NAVY = "1B3A6B"
FILLS = {"Precedent": "DDEBF7", "Partial": "FFF2CC", "IDinsight": "E2EFDA",
         "GAD discussion": "FCE4D6"}

wb = Workbook()
ws = wb.active
ws.title = "Recommendation log"

thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

ws.append(HEAD)
for c, w in enumerate(WIDTH, start=1):
    ws.column_dimensions[get_column_letter(c)].width = w
    cell = ws.cell(row=1, column=c)
    cell.font = Font(bold=True, color="FFFFFF", size=10)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border = border
ws.row_dimensions[1].height = 32

for r in ROWS:
    ws.append(list(r) + ["", ""])
    row = ws.max_row
    for c in range(1, len(HEAD) + 1):
        cell = ws.cell(row=row, column=c)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = border
        cell.font = Font(size=10)
    ws.cell(row=row, column=5).fill = PatternFill("solid", fgColor=FILLS[r[4]])
    if r[5] == "To confirm":
        ws.cell(row=row, column=6).font = Font(size=10, bold=True, color="B35309")
    # the additions drafted after the GAD discussions start at 41
    if r[0] == 41:
        for c in range(1, len(HEAD) + 1):
            ws.cell(row=row, column=c).border = Border(
                left=thin, right=thin, bottom=thin,
                top=Side(style="medium", color=NAVY))

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEAD))}{ws.max_row}"

# a small summary, off to the side of the log
sm = wb.create_sheet("Summary")
sm.column_dimensions["A"].width = 26
sm.column_dimensions["B"].width = 10
counts = {}
for r in ROWS:
    counts[r[4]] = counts.get(r[4], 0) + 1
sm.append(["Source", "Count"])
for k in ("Precedent", "Partial", "IDinsight", "GAD discussion"):
    sm.append([k, counts.get(k, 0)])
sm.append(["Total", len(ROWS)])
sm.append([])
sm.append(["Status", "Count"])
sm.append(["Settled", len([r for r in ROWS if r[5] == "Settled"])])
sm.append(["To confirm", len([r for r in ROWS if r[5] == "To confirm"])])
for row in sm.iter_rows():
    for cell in row:
        cell.font = Font(size=10, bold=cell.row in (1, 7) or cell.value == "Total")

wb.save(OUT)
print("wrote", OUT, "·", len(ROWS), "recommendations")
for k, v in counts.items():
    print(f"  {k:16} {v}")
