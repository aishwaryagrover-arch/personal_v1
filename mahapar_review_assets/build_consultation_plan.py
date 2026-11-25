#!/usr/bin/env python3
"""
Stakeholder consultation plan and discussion guides for the APAR form drafts.

Written as a working document for the team running the consultations, not as a
client deliverable: it carries the sample, the running order of a session, the
guides by respondent type, and what gets recorded.
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
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
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 1.12


def shade(cell, hexfill):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hexfill)
    cell._tc.get_or_add_tcPr().append(el)


def fixed_layout(table, widths):
    """Pin column widths; Word and LibreOffice both autofit without this."""
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


def h1(txt, space_before=16):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = NAVY


def h2(txt):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = NAVY


def para(txt, italic=False, size=10, colour=None):
    p = doc.add_paragraph()
    r = p.add_run(txt)
    r.italic = italic
    r.font.size = Pt(size)
    if colour:
        r.font.color.rgb = colour
    return p


def bullets(items, style="List Bullet"):
    for it in items:
        p = doc.add_paragraph(style=style)
        p.paragraph_format.space_after = Pt(3)
        if isinstance(it, tuple):
            r = p.add_run(it[0])
            r.bold = True
            p.add_run(" " + it[1])
        else:
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
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ══════════════════════════════════════════════════════════ title
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("APAR simplification: stakeholder consultations")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = NAVY
para("Plan and discussion guides · IDinsight with GAD · draft for discussion",
     italic=True, size=9.5, colour=GREY)

# ══════════════════════════════════════════════════════════ 1 purpose
h1("1. What the consultations need to answer", space_before=10)
para("The draft forms are ready and the recommendations are settled enough to test. Three "
     "questions remain open, and each needs a different kind of evidence.")
bullets([
    ("Do the forms work?", "Whether each question is understood as intended, whether anything "
     "needed is missing, and whether anything removed is missed. Tested by watching officers "
     "fill a draft, not by asking whether they like it."),
    ("How long do they actually take?", "The 45–60 → 20–30 minute figures are "
     "modelled. A timed fill, with a real year's work in mind, converts them into observed "
     "numbers that can be quoted to GAD."),
    ("What else breaks in APAR filing?", "Process and system problems the desk review could not "
     "see — and the wider HR-reform frustrations officers raise once the subject is open."),
])
para("A fourth question applies only to technical cadres: whether role-wise KPIs exist, are "
     "measurable, and who holds the data.")

# ══════════════════════════════════════════════════════════ 2 who
h1("2. Who we speak to, and what only they can tell us")
table(["Respondent group", "What only this group can answer"],
      [("Group A and Group B (gazetted) officers",
        "Whether Part 2 captures a year's work; whether targets and KRAs were ever set for "
        "their post; what they would want their reporting officer to see."),
       ("Reporting officers\n(Deputy Secretary / Joint Secretary, and field equivalents)",
        "Whether seven dimensions discriminate between officers; whether they would issue "
        "memos during the year; what makes a low grade defensible in practice."),
       ("Reviewing officers\n(Joint Secretary and above)",
        "Whether agreeing to an overall grade is enough oversight, or whether it turns the "
        "stage into a formality."),
       ("Group B (non-gazetted) and Group C employees",
        "Whether an optional self-appraisal reads as ‘do not bother’; whether the six "
        "graded items describe their work; what they understand of the process today."),
       ("Custodians and establishment staff",
        "Where the cycle actually stalls; whether officers mapping their own authorities is "
        "workable; what they chase and how."),
       ("Technical cadre officers\n(engineering, health, teaching)",
        "Whether KPIs exist for the post, whether they are measurable, who holds the data, and "
        "what the common form fails to capture."),
       ("CMA and sub-department monitoring points of contact",
        "What monitoring they would use, and what they are able to act on."),
       ("GAD and MahaPAR process owners, NIC",
        "What the portal can carry, in what order, and by when."),
       ],
      [Inches(2.3), Inches(4.3)])

# ══════════════════════════════════════════════════════════ 3 sample
h1("3. Sample and format")
para("Sizes below are a working proposal for a short round. They are deliberately small: the "
     "purpose is to find problems with the drafts, not to measure opinion.")
table(["Group", "Sessions", "Format", "Length"],
      [("Group A / B gazetted officers", "6–8", "Individual", "45 min"),
       ("Reporting officers", "4–5", "Individual", "45 min"),
       ("Reviewing officers", "2–3", "Individual", "30 min"),
       ("Group C employees", "2–3 groups of 4–6", "Group discussion", "60 min"),
       ("Custodians / establishment staff", "3–4", "Individual", "45 min"),
       ("Technical cadre officers", "1 group per cadre", "Group discussion", "75 min"),
       ("CMA / SDMA points of contact", "2–3", "Individual", "30 min"),
       ("GAD, MahaPAR, NIC", "As required", "Working session", "60 min"),
       ],
      [Inches(2.4), Inches(1.5), Inches(1.6), Inches(1.1)])
para("Four design choices behind this:", size=10)
bullets([
    ("Mantralaya and at least one district.", "File-based work in the Secretariat and "
     "field work in a Collectorate or Zilla Parishad are different jobs. A form tested only in "
     "Mantralaya will fail in the field."),
    ("Group C in groups, officers individually.", "Group C employees speak more freely among "
     "peers than across a desk from a senior officer."),
    ("Never pair an officer with their own reporting officer.", "Nobody will discuss grading "
     "candidly if the person who grades them is in the building for the same exercise."),
    ("Two interviewers where possible.", "One to run the conversation, one to take notes and "
     "keep time on the fill exercise."),
])

# ══════════════════════════════════════════════════════════ 4 session shape
h1("4. How a session runs")
para("The same shape for every group, so that what is heard in one can be compared with "
     "another. Timings are for a 45-minute individual session.")
table(["Minutes", "Section", "Purpose"],
      [("0–5", "Opening and role",
        "What they fill, for how many people, and when they last did it. Confidentiality stated."),
       ("5–15", "Last year, start to finish",
        "Walk me through your last APAR. Open, no draft on the table yet."),
       ("15–35", "The draft form, filled aloud",
        "Hand over the printed draft. They fill it while talking. Note where they stop, re-read "
        "or ask a question. Time it."),
       ("35–43", "Process and system",
        "Mapping, deadlines, memos, disclosure, and what they would want to see in MahaPAR."),
       ("43–45", "Closing",
        "One thing you would change. Anything we did not ask about."),
       ],
      [Inches(0.9), Inches(2.0), Inches(3.7)])
para("Open the fill exercise in the respondent's own words: ‘Fill this as if it were for "
     "the year just gone. Say what you are thinking as you go, including anything that is "
     "unclear. There is no wrong answer — we are testing the form, not you.’",
     italic=True)

# ══════════════════════════════════════════════════════════ 5 guides
h1("5. Discussion guides")

h2("5.1  Officers filling the self-appraisal (Form A, Part 2)")
para("Last year, start to finish", size=10).runs[0].bold = True
bullets([
    "When did you last fill an APAR, and how long did it take you in one sitting?",
    "What did you have to look up or ask someone for before you could fill it?",
    "Which question took the longest, and why?",
    "Did you see your completed APAR afterwards? If yes, how?",
])
para("Filling the draft", size=10).runs[0].bold = True
bullets([
    "2.1 Were targets ever set for your post? By whom, and when? If none were set, what would "
    "you put here?",
    "2.2 One significant contribution in 100 words — is that enough space? Too much?",
    "2.3 Systemic factors: would you answer this honestly, knowing your reporting officer sees "
    "it? What would stop you?",
    "2.4 Does your iGOT record match what you actually completed this year?",
    "2.7 Feedback for your reporting officer — ask how they would feel about it being asked, "
    "before asking whether they would answer it. Then: what would have to be true for you to "
    "write something honest here?",
    "Anything you used to report that this form no longer asks for?",
])
para("Process and system", size=10).runs[0].bold = True
bullets([
    "Do you know who your reporting and reviewing officer were for the whole of last year? "
    "Would you be able to record it yourself, with dates?",
    "Were you ever told during the year that something in your work needed to improve? How?",
    "If your APAR were disclosed to you with 15 days to respond, would you use it?",
])

h2("5.2  Reporting officers (Form A, Part 3)")
bullets([
    "How many officers do you report on? How long does one APAR take you?",
    "When do you start thinking about an officer's APAR — through the year, or when the "
    "form arrives?",
    "Filling the draft: grade one real officer, without naming them. Watch for whether the "
    "grades spread or cluster.",
    "Do the seven dimensions let you tell two officers apart? Which two overlap?",
    "Annexure 3 describes each dimension by kind of post. Does the description fit the posts "
    "you report on?",
    "A grade below 6 asks you to attach memos. Have you ever issued one? What would stop you?",
    "Would you record a concern during the year if the portal let you? What would you not put "
    "in writing?",
    "3.3 asks for strengths, one area to develop and any significant failure. Which of these do "
    "you find hardest to write, and why?",
    "What would you want to see on screen while grading that you do not have today?",
])

h2("5.3  Reviewing officers (Form A, Part 4)")
bullets([
    "How many APARs do you review in a cycle? How much time does each take?",
    "In the current form you re-grade every dimension. How often do your grades differ from the "
    "reporting officer's?",
    "In the draft you are asked only whether you agree with the overall grade. Is that enough "
    "oversight, or does it make the stage a formality?",
    "When you disagree, is one overall grade and 30 words enough to record why?",
    "What would make you look harder at a particular APAR?",
])

h2("5.4  Group B (non-gazetted) and Group C employees (Form B)")
para("Run as a group discussion. Start with the process, not the form.", italic=True, size=9.5)
bullets([
    "Do you know whether an APAR is written for you each year? Have you seen one?",
    "Has anyone ever asked you to write something about your own work?",
    "The draft makes the self-appraisal optional. If it is optional, would you fill it? What "
    "would make it worth filling?",
    "Read out the six graded items. Do these describe your work? What is missing?",
    "‘Dealing with the public’ can be marked not applicable. Is that the right call for "
    "your post?",
    "Fitness for promotion is recorded. Do you know how it is used?",
    "If your APAR were shown to you, what would you want to be able to say in response?",
])

h2("5.5  Custodians and establishment staff")
bullets([
    "Walk us through a cycle as you run it. Where does it get stuck most often?",
    "How do you establish who reported on whom? What do you do when it is disputed?",
    "The draft has officers record their own reporting and reviewing authority, for you to "
    "validate. Does that help you, or create work?",
    "How many APARs in your last cycle had no reporting officer in position for part of the year?",
    "How do you chase a pending stage today? How many rounds does it take?",
    "What would you want a pendency dashboard to show you first?",
    "What happens when a Departmental Promotion Committee asks for APARs?",
])

h2("5.6  Technical cadre officers (engineering, health, teaching)")
para("The one group where the question is not only about the form.", italic=True, size=9.5)
bullets([
    "What does the current technical proforma ask that the common form would not capture?",
    "Are there measurable targets for your post today — works completed, cases seen, "
    "classes taken? Who records them, and where?",
    "If MahaPAR offered a menu of 3–5 KPIs for your designation, could you pick from it at "
    "the start of the year?",
    "Who would verify the year-end status against the record?",
    "Is a mid-year progress check realistic? What would make you revise a target?",
    "What proportion of your work would these KPIs actually cover?",
])

h2("5.7  Monitoring authorities, GAD and NIC")
bullets([
    "What do you monitor today, and what do you do when an APAR is pending?",
    "What would you act on, if you could see it — by officer, stage, cadre, department?",
    "Where does the escalation stop? Who can compel a stage to be completed?",
    "For NIC: what of this is buildable for the coming cycle, and what needs a later release?",
])

# ══════════════════════════════════════════════════════════ 6 what is recorded
h1("6. What gets recorded")
para("Two records come out of every session, so that a small sample still produces something "
     "countable alongside the quotations.")
table(["Record", "What goes in it"],
      [("Fill log\n(one row per respondent)",
        "Time taken to fill the draft; questions where they stopped, re-read or asked for help; "
        "questions left blank; questions answered in a way the form did not intend."),
       ("Section rating\n(asked at the end)",
        "For each part of the form: clear or unclear; keep, drop or change. Gives counts such as "
        "‘9 of 12 found 2.1 unclear’ rather than only impressions."),
       ("Session note",
        "Written up the same day, against the guide's headings, with direct quotations marked. "
        "No names; role and department only."),
       ],
      [Inches(1.8), Inches(4.8)])

# ══════════════════════════════════════════════════════════ 7 candour
h1("7. Confidentiality, and getting a candid answer")
para("APAR is a sensitive subject in a hierarchy. Officers will not criticise their reporting "
     "officer, and reporting officers will not admit to grading everyone alike, unless the "
     "setting makes it safe.")
bullets([
    "State at the start: no names in any note, nothing attributed, nothing shared with anyone's "
    "reporting chain, and the purpose is to improve the form.",
    "Never schedule an officer and their own reporting or reviewing officer in the same visit.",
    "Ask about behaviour, not intent: ‘when did you last issue a memo’, not ‘do "
    "you issue memos’.",
    "For the upward-feedback question, ask how it would be received before asking whether they "
    "would use it. The second question invites a polite yes.",
    "Let silences run. The most useful answers in an APAR conversation come after a pause.",
])

# ══════════════════════════════════════════════════════════ 8 open points
h1("8. Open points for GAD")
bullets([
    "Access and a covering letter: which departments and districts, and who introduces us.",
    "Timing: the consultations need to finish before the forms are issued, and before the next "
    "cycle opens.",
    "Whether Group C employees can be met without their reporting officers present.",
    "Which technical cadres are in scope for this round, and who convenes them.",
    "Whether the session notes are shared with GAD in full, or only as findings.",
])

doc.save(OUT)
print("wrote", OUT)
