#!/usr/bin/env python3
"""
One table of the additional recommendations that came out of GAD feedback and
are already reflected in the latest Form A / Form B drafts and the MahaPAR
walkthrough. Formatted to be pasted straight into the recommendations table in
the APAR Simplification Note, so the columns and tone match that note.
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

OUT = "/home/user/personal_v1/MahaPAR_additional_recommendations.docx"

NAVY = RGBColor(0x1C, 0x3C, 0x6E)
HDR_FILL = "DCE6F1"

# (#, Section, Recommendation, Precedent)
ROWS = [
    ("41", "1.1",
     "Map authorities in two stages. In the short term the officer records their own "
     "reporting and reviewing authority with the tenure of each, and the custodian "
     "validates it or issues a correction. In the longer term the mapping is "
     "pre-populated from the eHRMS organogram once it is complete and integrated with "
     "MahaPAR, leaving the custodian only to validate. Process to be confirmed.",
     "No state precedent"),

    ("42", "2.2",
     "Give officers a work log, open through the year, from which entries can be drawn "
     "into the significant contribution reported in 2.2, so that noteworthy work is "
     "recorded when it happens rather than recalled at the end of the year.",
     "No state precedent"),

    ("43", "2.7",
     "Add one optional open field (50 to 100 words) in which the officer may share "
     "feedback with their reporting officer, anchored to the work and the conditions "
     "that would support it. Responses are pooled across everyone reporting to that "
     "officer and shared anonymously; they are not graded, are not seen by the "
     "reviewing officer, and form no part of the APAR record. Safeguards and the point "
     "at which the pooled feedback is shared to be confirmed.",
     "No state precedent"),

    ("44", "3.1",
     "Provide an annexure describing what each dimension looks like in different kinds "
     "of post, so that an officer is assessed on what their own work involves. "
     "Illustrative draft, to be finalised with inputs from the Karmayogi Competency "
     "Model and CEGIS.",
     "Not applicable"),

    ("45", "3.1",
     "Show the reporting officer the departmental KRAs attached to the post, with the "
     "targets and achievement recorded in 2.1, to anchor the grading of delivery and "
     "quality of work. Dependent on departments completing the KRA-defining exercise; "
     "integration with MahaPAR to be confirmed.",
     "No state precedent"),

    ("46", "Part 3",
     "Show the reporting officer the departmental enquiry record for the officer, drawn "
     "from the departmental enquiry portal: status, what the enquiry is about, case "
     "reference, date initiated, current stage and last update. Shown for reference "
     "while recording integrity; an enquiry that has not concluded is not a finding and "
     "is not by itself a ground for an adverse grade. Particulars to be confirmed.",
     "No state precedent"),

    ("47", "Process",
     "Allow the reporting officer to issue memos to an officer at any point during the "
     "year, recording where performance fell short and what improvement is expected. "
     "The officer may respond to each memo, and both the memo and the response are "
     "available to the reporting officer at the time of assessment, to substantiate a "
     "grade where needed.",
     "Odisha (adverse remarks must be substantiated)"),

    ("48", "Process",
     "Add monitoring layers above the custodian: the cadre monitoring authority and the "
     "sub-department monitoring authority follow up pendency with custodians and with "
     "each other, and GAD leadership follows up with both.",
     "Gujarat (defaulters flagged to the cadre authority)"),
]

doc = Document()

# page setup: landscape-ish margins so the table has room on A4 portrait
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Inches(0.6)
st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(9.5)

h = doc.add_paragraph()
r = h.add_run("Additional recommendations from GAD feedback")
r.bold = True
r.font.size = Pt(13)
r.font.color.rgb = NAVY

p = doc.add_paragraph()
r = p.add_run(
    "Changes deliberated with GAD following the initial recommendations, and already "
    "reflected in the latest Form A and Form B drafts and the MahaPAR user windows. "
    "Numbering continues from the existing recommendations table; items marked "
    "'to be confirmed' remain subject to GAD's decision."
)
r.font.size = Pt(9.5)
r.font.color.rgb = RGBColor(0x44, 0x4B, 0x55)

tbl = doc.add_table(rows=1, cols=4)
tbl.style = "Table Grid"
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

WIDTHS = [Inches(0.4), Inches(0.85), Inches(4.9), Inches(1.6)]


def fixed_layout(table, widths):
    """Pin column widths; without w:tblLayout + w:tblGrid, Word and LibreOffice
    autofit and ignore the per-cell widths."""
    tblPr = table._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    grid = table._tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tblPr.addnext(grid)
    for gc in list(grid):
        grid.remove(gc)
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w.inches * 1440)))
        grid.append(gc)


def shade(cell, hexfill):
    """Table-cell background; python-docx has no API for this."""
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hexfill)
    cell._tc.get_or_add_tcPr().append(el)


def put(cell, text, bold=False, width=None):
    cell.text = ""
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run(text)
    run.bold = bold
    run.font.size = Pt(9.5)
    run.font.name = "Arial"
    if width is not None:
        cell.width = width


hdr = tbl.rows[0].cells
for c, (label, w) in enumerate(zip(["#", "Section", "Recommendation", "Precedent"], WIDTHS)):
    put(hdr[c], label, bold=True, width=w)
    shade(hdr[c], HDR_FILL)

for num, section, rec, prec in ROWS:
    cells = tbl.add_row().cells
    for c, val in enumerate((num, section, rec, prec)):
        put(cells[c], val, width=WIDTHS[c])

fixed_layout(tbl, WIDTHS)

doc.add_paragraph()
n = doc.add_paragraph()
r = n.add_run(
    "Note: recommendations 7, 8, 10, 13, 15, 17, 18, 22, 24 and 33 in the existing "
    "table also need amending to match the latest drafts, in particular the No Report "
    "Certificate grounds, the reviewing officer's role and the Form B items and weights. "
    "Those are revisions to existing rows rather than additions, and are listed separately."
)
r.italic = True
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(0x5A, 0x62, 0x6E)

doc.save(OUT)
print("wrote", OUT)
