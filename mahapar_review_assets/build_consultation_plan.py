#!/usr/bin/env python3
"""
Stakeholder consultation plan and discussion guides for the APAR form drafts.

A working document for the team running the consultations: the flow of a
45-minute session, the guides by respondent type at 7 to 10 questions each, and
the draft reflection prompts we want to put in front of officers.
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
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.line_spacing = 1.12


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


def h1(txt, before=15):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = NAVY


def h2(txt, before=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = NAVY


def para(txt, italic=False, size=10, colour=None, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(txt)
    r.italic = italic
    r.bold = bold
    r.font.size = Pt(size)
    if colour:
        r.font.color.rgb = colour
    return p


def numbered(items):
    """Numbered by hand. Word's List Number style keeps counting across lists,
    which left the second list in a section starting at 7."""
    for i, it in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.32)
        p.paragraph_format.first_line_indent = Inches(-0.32)
        r = p.add_run("%d.  " % i)
        r.bold = True
        p.add_run(it)


def bullets(items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
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


# ══════════════════════════════════════════════════════════ title
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("APAR simplification: stakeholder consultations")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = NAVY
para("Plan and discussion guides for Form A and Form B · IDinsight with GAD · draft",
     italic=True, size=9.5, colour=GREY)

# ══════════════════════════════════════════════════════════ 1
h1("1. What the consultations need to answer", before=10)
numbered([
    "Do the draft forms work? Whether each question is understood as intended, whether "
    "anything needed is missing, and whether anything removed is missed.",
    "Do they save time? The 45 to 60 minute and 20 to 30 minute figures are modelled. "
    "Watching officers fill a draft turns them into observed numbers.",
    "What else breaks in APAR filing? The process and system problems a desk review cannot "
    "see, and the wider HR frustrations officers raise once the subject is open.",
    "Would officers value a space to reflect? Whether a short, better version of the pen "
    "picture is something they would use, and what they would want to say in it.",
    "Would upward feedback be safe to give? Whether officers would use it, and what would "
    "have to be true for them to answer honestly.",
    "For technical cadres: whether role-wise KPIs exist, are measurable, and who holds the "
    "data.",
])

# ══════════════════════════════════════════════════════════ 2
h1("2. Who we speak to, and what only they can tell us")
table(["Respondent group", "What only this group can answer"],
      [("Group A and Group B (gazetted) officers",
        "Whether Part 2 captures a year's work; whether targets were ever set for their post; "
        "what they would want to say about their own growth."),
       ("Reporting officers\n(Deputy Secretary / Joint Secretary, and field equivalents)",
        "Whether seven dimensions discriminate between officers; whether they would issue "
        "memos during the year; what makes a low grade defensible."),
       ("Reviewing officers\n(Joint Secretary and above)",
        "Whether agreeing to an overall grade is enough oversight, or turns the stage into a "
        "formality."),
       ("Group B (non-gazetted) and Group C employees",
        "Whether an optional self-appraisal reads as ‘do not bother’; whether the "
        "graded items describe their work."),
       ("Custodians and establishment staff",
        "Where the cycle stalls; whether officers mapping their own authorities is workable; "
        "what they chase and how."),
       ("Technical cadre officers\n(engineering, health, teaching)",
        "Whether KPIs exist for the post, whether they are measurable, who holds the data, and "
        "what the common form fails to capture."),
       ("Monitoring authorities, GAD and NIC",
        "What monitoring they would act on, and what the portal can carry."),
       ],
      [Inches(2.3), Inches(4.3)])

# ══════════════════════════════════════════════════════════ 3
h1("3. Sample and format")
table(["Group", "Sessions", "Format", "Mode", "Length"],
      [("Group A / B gazetted officers", "6–8", "Individual", "Virtual", "45 min"),
       ("Reporting officers", "4–5", "Individual", "Virtual", "45 min"),
       ("Reviewing officers", "2–3", "Individual", "Virtual", "30 min"),
       ("Group C employees", "2–3 groups of 4–6", "Group discussion",
        "In person if at all possible", "60 min"),
       ("Custodians / establishment staff", "3–4", "Individual", "Virtual", "45 min"),
       ("Technical cadre officers", "1 group per cadre", "Group discussion", "Virtual",
        "75 min"),
       ("Monitoring authorities, GAD, NIC", "As required", "Working session", "Virtual",
        "60 min"),
       ],
      [Inches(1.95), Inches(0.85), Inches(1.35), Inches(1.6), Inches(0.85)])
bullets([
    ("Mantralaya and at least one district.", "Secretariat file work and field work are "
     "different jobs. A form tested only in Mantralaya will fail in the field. Virtual sessions make reaching districts easier, so use that."),
    ("Group C in groups, officers individually.", "Group C employees speak more freely among "
     "peers than across a desk from a senior officer."),
    ("Never pair an officer with their own reporting officer.", "Nobody discusses grading "
     "candidly if the person who grades them is part of the same exercise."),
    ("Two interviewers where possible.", "One runs the conversation, one takes notes and keeps "
     "time on the fill."),
])

# ══════════════════════════════════════════════════════════ 4
h1("4. How a 45-minute session runs")
para("Most sessions will be virtual. The shape below works either way, and it opens without "
     "the form in front of them, so the first answers are not shaped by what we are proposing. "
     "Section 4.1 covers what changes on a call.")
table(["Minutes", "Part", "What happens"],
      [("0–5", "A. Opening",
        "Role, what they fill, for how many people, and when they last did it. "
        "Confidentiality stated."),
       ("5–15", "B. Open-ended: what is wrong today",
        "No form on the table. What is difficult about the APAR in your role? Where does it "
        "take time? What does it fail to capture? Let them name the problems first."),
       ("15–35", "C. Walk through the draft",
        "Share the draft on screen, or send it in the chat and ask them to share theirs. "
        "Go part by part, with the same three probes on each. Time how long the fill takes."),
       ("35–42", "D. The new ideas",
        "Reflection and growth, upward feedback, and a richer work log. Show the draft prompts "
        "in section 7."),
       ("42–45", "E. Close",
        "One thing you would change. Anything we did not ask about."),
       ],
      [Inches(0.85), Inches(1.9), Inches(3.85)])

h2("The three probes, used on every field in Part C")
para("Ask these on each part of the form rather than inventing new questions. Consistency is "
     "what lets us count answers across twenty sessions.")
numbered([
    "Does this help you? Is it asking for something you can actually answer?",
    "Does it cut the time you spend thinking or writing, compared with the current form?",
    "What could go wrong with it? Where could this be misused, or give a misleading picture?",
])
para("Opening line for the fill: ‘Fill this as if it were for the year just gone. Say what "
     "you are thinking as you go, including anything that is unclear. We are testing the form, "
     "not you.’", italic=True)

# ══════════════════════════════════════════════════════════ 5 guides
h2("4.1  Running these virtually")
para("Most of these will be video calls, which changes the walkthrough more than anything else. "
     "A respondent cannot be handed a printed form, and a think-aloud is harder to sustain on a "
     "call. Six things to settle in advance.")
bullets([
    ("Send the form at the start of the call, not before.", "A fillable PDF in the chat window. "
     "Sending it a day ahead usually means it is not read, and occasionally means it is read "
     "closely, which spoils the first reaction."),
    ("Decide who holds the form.", "Best: the respondent shares their screen and fills it while "
     "talking. Acceptable: we share, scroll on their instruction, and type what they dictate. "
     "Agree which at the start, so the first five minutes are not lost to it."),
    ("Walk through two or three parts, not the whole form.", "Twenty minutes of walkthrough on a "
     "call covers less than it does across a desk. Pick the parts that matter most for that "
     "respondent, and say so."),
    ("Treat virtual timings as indicative.", "People multitask on calls. Record the elapsed time, "
     "but validate the completion-time claim against two or three in-person sessions before it "
     "is quoted to GAD."),
    ("Ask permission to record, and say what happens to it.", "A recording makes the fill log "
     "far easier to write up. If permission is refused, the second interviewer takes the time "
     "stamps by hand."),
    ("Have a phone fallback.", "District connectivity will fail at least once. Keep a dial-in "
     "number, and a version of the questions that works without the form on screen."),
])
para("One thing virtual cannot fix: a group discussion with Group C employees. On a video call "
     "you cannot see who else is in the room, and juniors will not speak freely if a supervisor "
     "is within earshot. If these have to be virtual, run them in groups of three or four, ask "
     "each person to join individually rather than from a shared room, and treat the findings "
     "as weaker than the rest.", italic=True)

h1("5. Discussion guides")
para("Seven to ten questions each, to fit the time. Parts B and D of the session are the same "
     "for everyone; what changes is the walkthrough in Part C.")

h2("5.1  Officers filling the self-appraisal (Form A, Part 2)")
numbered([
    "What is difficult about filling your APAR today? Where does the time go?",
    "What does the current form fail to capture about your year?",
    "2.1 Were targets ever set for your post? If none were set, what would you put here?",
    "2.2 One significant contribution in 100 words. Enough space, or too much?",
    "2.3 Systemic factors. Would you answer this honestly, knowing your reporting officer sees "
    "it? What would stop you?",
    "2.4 Does your iGOT record match what you actually completed?",
    "Across Part 2, does this cut your thinking and writing time? Where does it not?",
    "Is anything you used to report no longer asked for, that you would want back?",
    "Do you know who your reporting and reviewing officer were for the whole year? Could you "
    "record it yourself, with dates?",
    "If your APAR were disclosed to you with 15 days to respond, would you use it?",
])

h2("5.2  Reporting officers (Form A, Part 3)")
numbered([
    "What is difficult about writing APARs today? How long does one take you?",
    "When do you start thinking about an officer's APAR: through the year, or when the form "
    "arrives?",
    "Grade one real officer on the draft, without naming them. (Watch whether grades spread or "
    "cluster.)",
    "Do the seven dimensions let you tell two officers apart? Which two overlap?",
    "Annexure 3 describes each dimension by kind of post. Does it fit the posts you report on?",
    "A grade below 6 asks you to attach memos. Have you ever issued one? What would stop you?",
    "Would you record a concern during the year if the portal let you? What would you not put "
    "in writing?",
    "3.3 asks for strengths, an area to develop and any significant failure. Which is hardest "
    "to write, and why?",
    "What would you want on screen while grading that you do not have today?",
])

h2("5.3  Reviewing officers (Form A, Part 4)")
numbered([
    "What does the reviewing stage add today, in your experience?",
    "How many APARs do you review in a cycle, and how long does each take?",
    "You currently re-grade every dimension. How often do your grades differ from the reporting "
    "officer's?",
    "The draft asks only whether you agree with the overall grade. Is that enough oversight?",
    "When you disagree, is one overall grade and 30 words enough to record why?",
    "What would make you look harder at a particular APAR?",
    "What could go wrong with an agree-only stage?",
])

h2("5.4  Group B (non-gazetted) and Group C employees (Form B)")
para("Run as a group discussion, and start with the process rather than the form.",
     italic=True, size=9.5)
numbered([
    "Do you know whether an APAR is written for you each year? Have you seen one?",
    "Has anyone ever asked you to write something about your own work?",
    "The draft makes the self-appraisal optional. Would you fill it? What would make it worth "
    "filling?",
    "Read out the six graded items. Do these describe your work? What is missing?",
    "‘Dealing with the public’ can be marked not applicable. Is that right for your "
    "post?",
    "Fitness for promotion is recorded. Do you know how it is used?",
    "If your APAR were shown to you, what would you want to be able to say in response?",
    "Would you want a place to record what you learned or did differently this year?",
])

h2("5.5  Custodians and establishment staff")
numbered([
    "Walk us through a cycle as you run it. Where does it get stuck most often?",
    "How do you establish who reported on whom? What do you do when it is disputed?",
    "The draft has officers record their own authorities, for you to validate. Does that help, "
    "or create work?",
    "How many APARs last cycle had no reporting officer in position for part of the year?",
    "How do you chase a pending stage today? How many rounds does it take?",
    "What would you want a pendency dashboard to show you first?",
    "What happens when a Departmental Promotion Committee asks for APARs?",
])

h2("5.6  Technical cadre officers (engineering, health, teaching)")
numbered([
    "What does your current proforma ask that the common form would not capture?",
    "Are there measurable targets for your post today? Who records them, and where?",
    "If MahaPAR offered a menu of three to five KPIs for your designation, could you pick from "
    "it at the start of the year?",
    "Who would verify the year-end status against the record?",
    "Is a mid-year progress check realistic? What would make you revise a target?",
    "What share of your work would these KPIs actually cover?",
    "What could go wrong with being graded on KPIs?",
])

h2("5.7  Monitoring authorities, GAD and NIC")
numbered([
    "What do you monitor today, and what do you do when an APAR is pending?",
    "What would you act on, if you could see it: by officer, stage, cadre, department?",
    "Where does escalation stop? Who can compel a stage to be completed?",
    "For NIC: what is buildable for the coming cycle, and what needs a later release?",
])

# ══════════════════════════════════════════════════════════ 6 new ideas
h1("6. Part D: the three new ideas, and how to test them")
para("These are the parts of the design we are least sure about, so they get their own slot "
     "rather than being buried in the walkthrough. Show the draft wording, then ask.")

h2("6.1  Reflection and growth: a better pen picture")
para("The current form has no place for an officer to say how they have grown. The proposal is "
     "a short reflection of three or four prompts, not a long narrative. Draft wording to show:",
     size=10)
table(["Prompt", "Why it is there"],
      [("What can you do now that you could not do a year ago?",
        "Growth in plain terms. Easier to answer than ‘what skills did you acquire’."),
       ("What was the hardest thing you handled this year, and what did you take from it?",
        "Challenge and learning, without asking anyone to admit failure."),
       ("What kind of work or exposure would you like in the year ahead?",
        "Aspiration, and something the reporting officer can act on."),
       ("What support from your reporting officer would help you get there?",
        "Turns the reflection into a specific ask rather than a wish."),
       ],
      [Inches(3.0), Inches(3.6)])
numbered([
    "Would you want a place in the APAR to write this? Would you actually fill it?",
    "Is four prompts about right, or is even that too many?",
    "Who should see it: your reporting officer, your reviewing officer, or only you?",
    "What could go wrong with asking this in an appraisal form?",
])

h2("6.2  Upward feedback on the reporting officer")
para("Show Part 2.7 as drafted: five areas rated one to five, plus fifty words.", size=10)
numbered([
    "How would a question like this be received, in your office?",
    "Would you answer it honestly? What would have to be true for you to do so?",
    "Responses are pooled across everyone reporting to an officer and shared anonymously. Is "
    "that enough? What else would be needed?",
    "When should it reach the reporting officer: with the APAR, or after the cycle closes?",
])
para("Ask how it would be received before asking whether they would use it. The second question "
     "asked first gets a polite yes from everyone.", italic=True, size=9.5)

h2("6.3  A work log with more in it")
para("The work log today records noteworthy work. The question is whether a little more "
     "structure would make it useful for the reflection above, without making it a chore. One "
     "option to put to them: each entry carries a tag and an optional line.", size=10)
bullets([
    ("Tag:", "routine work, something new, something difficult, something I learned from."),
    ("Optional line:", "what this taught me, or what I would do differently."),
])
numbered([
    "Do you keep any record of your work through the year today? In what form?",
    "Would tagging an entry be useful to you, or just more work?",
    "At the end of the year, what would you want the log to give you when you sit down to fill "
    "the form?",
])

# ══════════════════════════════════════════════════════════ 7
h1("7. What gets recorded")
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

# ══════════════════════════════════════════════════════════ 8
h1("8. Confidentiality, and getting a candid answer")
bullets([
    "State at the start: no names in any note, nothing attributed, nothing shared with anyone's "
    "reporting chain, and the purpose is to improve the form.",
    "Never schedule an officer and their own reporting or reviewing officer in the same visit.",
    "Ask about behaviour, not intent: ‘when did you last issue a memo’, not ‘do "
    "you issue memos’.",
    "Let silences run. The most useful answers in an APAR conversation come after a pause.",
])

# ══════════════════════════════════════════════════════════ 9
h1("9. Open points for GAD")
bullets([
    "Access and a covering letter: which departments and districts, and who introduces us.",
    "Timing: the consultations need to finish before the forms are issued and the next cycle "
    "opens.",
    "Whether Group C employees can be met without their reporting officers present.",
    "Which technical cadres are in scope, and who convenes them.",
    "Whether session notes are shared with GAD in full, or only as findings.",
])

doc.save(OUT)
print("wrote", OUT)
