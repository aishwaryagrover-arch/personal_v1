#!/usr/bin/env python3
"""
Stakeholder consultation structure and discussion guides for the Maharashtra
APAR general forms (Form A and Form B).

Kept short on purpose: what the consultations need to answer, who we speak to,
how a session runs, and the questions by role.
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

OUT = "/home/user/personal_v1/MahaPAR_stakeholder_consultation_plan.docx"

NAVY = RGBColor(0x1B, 0x3A, 0x6B)
GREY = RGBColor(0x44, 0x4B, 0x55)
HDR_FILL = "DCE6F1"

doc = Document()
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Inches(0.85)
sec.top_margin = sec.bottom_margin = Inches(0.8)
st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(10)
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.line_spacing = 1.1


def shade(cell, hexfill):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hexfill)
    cell._tc.get_or_add_tcPr().append(el)


def fixed_layout(t, widths):
    """Pin column widths; Word and LibreOffice both autofit without this."""
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblPr.append(lay)
    grid = t._tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tblPr.addnext(grid)
    for gc in list(grid):
        grid.remove(gc)
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w.inches * 1440)))
        grid.append(gc)


def h1(txt, before=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(12.5)
    r.font.color.rgb = NAVY


def h2(txt, before=9, size=10.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = NAVY


def para(txt, italic=False, size=10, colour=None):
    p = doc.add_paragraph()
    r = p.add_run(txt)
    r.italic = italic
    r.font.size = Pt(size)
    if colour:
        r.font.color.rgb = colour
    return p


def numbered(items, start=1):
    """Numbered by hand: Word's List Number style keeps counting across lists."""
    for i, it in enumerate(items, start=start):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        r = p.add_run("%d.  " % i)
        r.bold = True
        p.add_run(it)


def bullets(items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.add_run(it)


def table(headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, head in enumerate(headers):
        cell = t.rows[0].cells[c]
        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(head)
        r.bold = True
        r.font.size = Pt(9.5)
        shade(cell, HDR_FILL)
        cell.width = widths[c]
    for row in rows:
        cells = t.add_row().cells
        for c, val in enumerate(row):
            cells[c].text = ""
            p = cells[c].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            cells[c].width = widths[c]
    fixed_layout(t, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


# ══════════════════════════════════════════════════════════ title
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("APAR forms: stakeholder consultations")
r.bold = True
r.font.size = Pt(15)
r.font.color.rgb = NAVY
para("Structure and discussion guides for Form A and Form B · IDinsight with GAD",
     italic=True, size=9.5, colour=GREY)

# ══════════════════════════════════════════════════════════ 1
h1("1. What the consultations need to answer", before=9)
numbered([
    "Do the draft forms work? Whether each question is understood as intended, whether anything "
    "needed is missing, and whether anything we removed is missed.",
    "Do they save time? Whether the new form reduces the time spent thinking and writing at "
    "each stage.",
    "What else makes APAR filing difficult today? Problems in the process and the system that a "
    "shorter form on its own will not fix.",
    "Would officers value a place to reflect on their own growth? Whether a short reflection "
    "would be used, and what they would want to record in it.",
    "Would upward feedback work? Whether officers would use it, and what would make it safe to "
    "answer honestly.",
    "How far have departments defined KRAs and KPIs? Whether role-wise KRAs and measurable KPIs "
    "exist for posts today, and who holds that data.",
])

# ══════════════════════════════════════════════════════════ 2
h1("2. Who we speak to")
para("Five groups, covering both forms and every stage of the cycle.")
table(["Group", "What we can learn from them"],
      [("Officers filling the self-appraisal\n(Group A and Group B gazetted)",
        "Whether Part 2 captures their year, whether targets were ever set for their post, and "
        "what they would want to record about their own growth."),
       ("Group B (non-gazetted) and Group C employees\n(Form B)",
        "Whether an optional self-appraisal would be filled, whether the graded items describe "
        "their work, and what they know of the process today."),
       ("Reporting officers",
        "Whether the seven dimensions let them distinguish between officers, whether they would "
        "issue memos during the year, and what makes a low grade defensible."),
       ("Reviewing officers",
        "Whether agreeing with the overall grade is enough at this stage, and what would make "
        "them look at an APAR more closely."),
       ("Custodians and establishment staff",
        "Where the cycle gets stuck, whether officers mapping their own authorities would work, "
        "and how they follow up today."),
       ],
      [Inches(2.3), Inches(4.3)])

# ══════════════════════════════════════════════════════════ 3
h1("3. Session structure")
para("Forty-five minutes. The session opens without the form in front of them, so the first "
     "answers are about their own experience rather than our proposal. Share the form at the "
     "start of the walkthrough.")
table(["Minutes", "Part", "Themes to explore"],
      [("0–12", "A. Role and current experience",
        "What they fill and for how many officers. What is difficult about the APAR in their "
        "role, where the time goes, what works today and what does not."),
       ("12–42", "B. Walking through the draft, field by field",
        "For each field: does this help you; does it cut the time you spend thinking or "
        "writing; and are there gaps, meaning anything missing that should be added or "
        "anything that should be dropped. Questions on the reflection field and on upward "
        "feedback are asked at the field they relate to."),
       ("42–45", "C. Close",
        "One thing they would change. Anything not covered."),
       ],
      [Inches(0.85), Inches(2.1), Inches(3.65)])
para("Opening line for the walkthrough: ‘Fill this as if it were for the year just gone, "
     "and say what you are thinking as you go, including anything that is unclear. We are "
     "testing the form, not you.’", italic=True, size=9.5)

# ══════════════════════════════════════════════════════════ 4
h1("4. Detailed discussion guides")

h2("4.1  Officers filling the self-appraisal (Form A, Part 2)")
numbered([
    "What is difficult about filling your APAR today, and where does the time go?",
    "2.1 Were targets or KRAs ever set for your post? If not, what would you write here?",
    "2.2 One significant contribution in 100 words. Is that enough space?",
    "Alongside 2.2, would you want a short space to record how you have grown this year: what "
    "you can do now that you could not a year ago, what was difficult, and what work or support "
    "you would like next year? Would you fill it, and could the work log be set up to make it "
    "easier?",
    "2.3 Systemic factors. Would you answer this honestly, knowing your reporting officer sees "
    "it?",
    "2.4 Does your iGOT record match the training you actually completed?",
    "2.7 Feedback for your reporting officer. How would a question like this be received in your "
    "office, would you answer it honestly, and what would make it safe to do so?",
    "Is there anything in the current form you would want kept that this draft drops?",
    "Do you know who your reporting and reviewing officer were for the whole year? Could you "
    "record it yourself, with dates?",
    "If your APAR were shown to you with 15 days to respond, would you use it?",
])
h2("Additional questions for Form B fillers", before=7, size=10)
bullets([
    "The self-appraisal is optional in Form B. Would you fill it, and what would make it worth "
    "filling?",
    "Do the six graded items describe your work? Is anything missing?",
    "‘Dealing with the public’ can be marked not applicable. Is that right for your "
    "post?",
    "Do you know whether an APAR is written for you each year, and have you seen one?",
])

h2("4.2  Reporting officers (Form A, Part 3)")
numbered([
    "What is difficult about writing APARs today, and how long does one take you?",
    "Grade one officer on the draft, without naming them.",
    "Do the seven dimensions let you tell two officers apart? Do any of them overlap?",
    "Annexure 3 describes what each dimension looks like for different kinds of post. Does it "
    "fit the posts you report on?",
    "A grade below the benchmark asks you to attach memos. Have you ever issued one, and what "
    "would stop you?",
    "Would you record a concern during the year if the portal allowed it? What would you not put "
    "in writing?",
    "3.3 asks for strengths, an area to develop and any significant failure. Which is hardest to "
    "write, and why?",
    "If the officer recorded a short reflection on how they had grown and what support they "
    "want, would that help you write this section?",
    "Would feedback from the officers who report to you be useful to you, and in what form?",
    "Are KRAs or KPIs defined for the posts you supervise, and who holds that data?",
])
h2("Additional questions for reporting officers using Form B", before=7, size=10)
bullets([
    "Form B has six graded items and a fitness judgment rather than seven dimensions. Does that "
    "work for the staff you report on?",
    "Do you expect Group C employees to fill the optional self-appraisal?",
])

h2("4.3  Reviewing officers (Form A, Part 4)")
numbered([
    "What does the reviewing stage add today, in your experience?",
    "How many APARs do you review in a cycle, and how long does each take?",
    "You currently re-grade every dimension. How often do your grades differ from the reporting "
    "officer’s?",
    "The draft asks only whether you agree with the overall grade. Is that enough at this stage?",
    "When you disagree, is one overall grade and a 30-word reason enough to record why?",
    "What would make you look at a particular APAR more closely?",
    "Are there gaps at this stage: anything that should be added, or anything that should be "
    "dropped?",
])
h2("Additional question for reviewing officers using Form B", before=7, size=10)
bullets([
    "In Form B you also record agreement with the fitness judgment. Does that need anything more "
    "than a yes or no?",
])

h2("4.4  Custodians and establishment staff")
numbered([
    "Walk us through a cycle as you run it. Where does it get stuck most often?",
    "How do you establish who reported on whom, and what do you do when it is disputed?",
    "The draft has officers record their own reporting and reviewing authority for you to "
    "validate. Does that help you, or create work?",
    "How many APARs in your last cycle had no reporting officer in position for part of the "
    "year?",
    "How do you follow up a pending stage today, and how many rounds does it take?",
    "What would you want a pendency dashboard to show you first?",
    "What happens when a Departmental Promotion Committee asks for APARs?",
])

# ══════════════════════════════════════════════════════════ 5
h1("5. Confidentiality considerations")
bullets([
    "Say at the start that no names go into the notes, nothing is attributed, nothing is shared "
    "with anyone’s reporting chain, and the purpose is to improve the form.",
    "Do not schedule an officer and their own reporting or reviewing officer in the same visit.",
    "Ask what people have done rather than what they would do: ‘when did you last issue a "
    "memo’ works better than ‘do you issue memos’.",
    "Do not rush the respondent. The answers are more useful when people have had a moment to "
    "think.",
])

doc.save(OUT)
print("wrote", OUT)
