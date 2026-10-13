#!/usr/bin/env python3
"""
Version 2 of the dashboard note.

Changes from v1:
  - plain, short sentences throughout (government reading, not consulting prose)
  - changes marked ON the screenshot in GAD's own annotation style
    (coloured dashed boxes with numbered callouts), not described beside it
  - a second part proposing new sections and structure for the four
    monitoring levels and the four user windows

Output: one HTML page that also prints cleanly to PDF.
Annotation box coordinates are percentages of the cropped screenshot and were
set by reading each crop; they are approximate by design, as they only need to
point NIC at the right part of the screen.
"""

OUT = "/home/user/personal_v1/mahapar_review_assets/dashboard_note_v2.html"

import base64, os
_CACHE = {}
def src(name):
    """Inline the screenshot as a data URI so the HTML is one self-contained file."""
    if name in _CACHE: return _CACHE[name]
    d = os.path.dirname(os.path.abspath(__file__))
    jpg = os.path.join(d, "j_" + name.replace(".png", ".jpg"))
    path = jpg if os.path.exists(jpg) else os.path.join(d, name)
    mime = "jpeg" if path.endswith(".jpg") else "png"
    with open(path, "rb") as f:
        _CACHE[name] = f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()
    return _CACHE[name]



RED, AMB, GRN, BLU = "#DC2626", "#E8820C", "#15803D", "#1D4ED8"

# ---------------------------------------------------------------- PART 1
# box = (left%, top%, width%, height%, colour, number, label-side)
P1 = [
dict(id=1, grp="A", shot="s44.png",
 title="Make the status word match the band it falls in",
 boxes=[(0.5,22,24,30,RED,1,"tl"), (82,11,13,41,GRN,2,"tr")],
 notes=["This card says GOOD at 66.88%", "But the filter says 60–79.9% is Warning"],
 now="The filter sets four bands: Excellent 95%+, Good 80–94.9%, Warning 60–79.9%, Poor below 60%. Cards showing 60% to 77% are labelled GOOD.",
 chg="Pick the word from the same four bands. 66.88% should read <b>Warning</b>.",
 why="The reader sees the word before the number.",
 eff="Very low"),

dict(id=2, grp="A", shot="s41.png",
 title="Say ‘APARs initiated’, not ‘performance’",
 boxes=[(66.5,9,16.5,18,RED,1,"tl"), (70.5,36,7.5,60,RED,2,"tr")],
 notes=["This is a filing figure, not officer performance", "Same for this column"],
 now="The count of APARs started is headed <b>PAR GENERATED PERFORMANCE</b>, and the column beside it is headed <b>PERFORMANCE</b>. Both measure filing progress.",
 chg="Rename the tile to <b>APARs initiated (%)</b> and the column to <b>Filing status</b>. Figures stay the same.",
 why="Removes any chance of a filing figure being read as an assessment of officers.",
 eff="Very low"),

dict(id=3, grp="A", shot="s51.png",
 title="State the eligibility rule the DPC report actually uses",
 boxes=[(80.5,37,18.5,57,AMB,1,"tl"), (0.5,93.5,99,5.5,RED,2,"tl")],
 notes=["Officers pass at 27.52 and 27.31", "But the note says ‘≥ 30 are marked eligible’"],
 now="The note says officers with a total grade of 30 or above are eligible. Officers are being marked eligible at 27.52.",
 chg="Correct the note to the rule in use, once GAD confirms it. For example: <b>‘Officers with a total grade of 27 or above are marked eligible.’</b>",
 why="This report may go before a promotion committee. The note should match the calculation.",
 eff="Very low · needs GAD to confirm the rule"),

dict(id=4, grp="A", shot="s42.png",
 title="Bring the ‘pending with’ columns to the front",
 boxes=[(65.5,3,34,92,RED,1,"tl")],
 notes=["Seven ‘Pending’ columns sit here, reached only by scrolling sideways"],
 now="Seven columns record where each APAR is pending. All sit to the right and need sideways scrolling. Several show zero for every row.",
 chg="Move them next to the organisation name, move the count columns right, and hide any column that is zero for every row.",
 why="‘With whom is it pending’ is the question asked most often in review meetings.",
 eff="Low"),

dict(id=5, grp="A", shot="s43b.png",
 title="Explain why the two officer counts differ",
 boxes=[(16.5,1,15,17,AMB,1,"tl"), (36,88,10,10,AMB,2,"bl")],
 notes=["Tile shows 616", "Table total shows 611"],
 now="The tile shows 616 officers. The table below totals 611. APARs (868) also exceed officers (611), as some officers have more than one reporting period.",
 chg="Reconcile the two counts, or add one line below the table: <b>‘An officer with more than one reporting period has an APAR for each period.’</b>",
 why="Saves a repeated query to NIC and GAD.",
 eff="Low"),

dict(id=6, grp="B", shot="s43b.png",
 title="Open on the Officer-wise view",
 boxes=[(0.5,20,99,78,GRN,1,"tl")],
 notes=["This view fits the screen — make it the one that opens first"],
 now="Two views are offered. Officer-wise has seven columns and fits the screen. PAR-wise has about fourteen, most shortened. PAR-wise opens first.",
 chg="Open on Officer-wise. Keep PAR-wise one click away.",
 why="Most users want the position at a glance.",
 eff="Very low"),

dict(id=7, grp="B", shot="s44.png",
 title="Show the lowest services first",
 boxes=[(0.5,20,99,76,BLU,1,"tl")],
 notes=["About 70 cards, in alphabetical order"],
 now="The 70 service cards are in alphabetical order. The services needing attention are found only by scrolling.",
 chg="Sort by completion, lowest first. Keep an A–Z option.",
 why="Turns a list into a priority list, using figures already on the card.",
 eff="Very low"),

dict(id=8, grp="B", shot="s46.png",
 title="Give each ‘Pending Officer’ column its own name",
 boxes=[(66.5,47,33,46,RED,1,"tl")],
 notes=["Five columns, all reading ‘Pending Officer …’"],
 now="Five columns next to each other all shorten to <b>Pending Officer …</b> and cannot be told apart.",
 chg="Rename them: <b>Pending with · Designation · Office · Pending since (days) · Contact</b>.",
 why="This report holds exactly what GAD needs for follow-up.",
 eff="Very low"),

dict(id=9, grp="B", shot="s46.png",
 title="Let the pending report run for all officers",
 boxes=[(32.5,8,18.5,24,RED,1,"tl")],
 notes=["Officer name is compulsory, so the report runs one officer at a time"],
 now="<b>Employee Search</b> is compulsory. A pendency report therefore returns a single officer, and only if the user already knows the name.",
 chg="Make the name optional. Show all officers in the selected service and year by default.",
 why="This single change turns a record lookup into the monitoring report the cadre and service authorities need.",
 eff="Low to moderate"),

dict(id=10, grp="B", shot="s46.png",
 title="Use process words for the stage",
 boxes=[(60.5,47,6.5,46,AMB,1,"tl")],
 notes=["‘OFFICER REPORTED UPON’ is system wording"],
 now="The stage reads <b>Pending at Level: OFFICER REPORTED UPON</b>.",
 chg="Use the words of the process: <b>Awaiting self-appraisal by the officer</b>, <b>Awaiting assessment by the reporting authority</b>, <b>Awaiting review by the reviewing authority</b>.",
 why="The same words then appear in the circular, on the dashboard and in the report.",
 eff="Very low"),

dict(id=11, grp="B", shot="s48.png",
 title="Bring ‘Select Columns’ into view",
 boxes=[(15,20,36,13,GRN,1,"tl")],
 notes=["A useful control, hidden inside a dropdown"],
 now="The report already lets the user choose which columns are shown. The control sits inside a dropdown and is easily missed.",
 chg="Place <b>Select columns</b> beside Export to PDF and Export to Excel.",
 why="The facility is already built. Only its position needs changing.",
 eff="Very low"),

dict(id=12, grp="C", shot="s50.png",
 title="Say why the table is empty",
 boxes=[(30,55,40,22,RED,1,"tl"), (91,80,8,18,AMB,2,"tr")],
 notes=["‘No data available’ before any selection is made", "Download button is live over an empty table"],
 now="Several screens show <b>No data available</b> with 0 of 0 — before a selection is made, where no records exist, and where a stage is still pending. All three look the same.",
 chg="Name the reason: <b>Select a DPC and service to begin</b> · <b>No officers are mapped to this role at present</b> · <b>Pen picture not yet recorded</b>. Grey the export button until rows appear.",
 why="These screens are the ones seen in demonstrations.",
 eff="Low"),

dict(id=13, grp="C", shot="s47.png",
 title="Explain a blank grade",
 boxes=[(66.5,67,33,31,RED,1,"tl")],
 notes=["Reviewing authority grade is shown only as ‘-’"],
 now="The reviewing authority's grade shows as <b>-</b> for both periods. The report does not say whether the review is pending or not required.",
 chg="Show the position instead: <b>Not yet recorded — reviewing stage pending since 30 Sep 2026</b>.",
 why="This is the most important field in the record.",
 eff="Low"),

dict(id=14, grp="C", shot="s41.png",
 title="Show how old the figures are",
 boxes=[(83,9,16.5,18,AMB,1,"tl")],
 notes=["Read on 8 October; figures are from 26 September"],
 now="The screen carries a <b>Last Updated</b> stamp. It read 26 September while being viewed on 8 October. The gap is not pointed out.",
 chg="Add the age beside it: <b>Last updated 26 Sep 2026 (12 days ago)</b>, in amber once it passes the interval GAD sets.",
 why="These figures are used in review meetings.",
 eff="Very low · needs GAD to set the interval"),

dict(id=15, grp="C", shot="s40.png",
 title="Show placeholder years as ‘Not available’",
 boxes=[(82,28,13,68,AMB,1,"tl")],
 notes=["One officer shows allotment year 1900"],
 now="Allotment year shows as <b>1900</b> for some officers. This appears to be a placeholder carried from the source record.",
 chg="Show such values as <b>Not available</b>, and give GAD a count of the records affected.",
 why="Keeps an evident placeholder out of reports seen by senior officers.",
 eff="Low"),

dict(id=16, grp="D", shot="s37.png",
 title="Split ‘My Pendency’ into what the officer must do",
 boxes=[(0.3,12,24,43,RED,1,"tl"), (49,12,50,43,AMB,2,"tr"), (25,12,23,43,BLU,3,"tl")],
 notes=["One figure, no indication of what it contains",
        "Signature and IP address tiles take the top of the screen",
        "IPR is a separate return, not APAR"],
 now="The officer sees <b>My Pendancy: 87</b> as one figure, beside tiles for eSign and DSC transactions and the IP addresses used.",
 chg="Show two figures — <b>Awaiting my action</b> and <b>Awaiting action by others</b> — each opening the list. Group the signature tiles lower down under <b>Signature activity</b>.",
 why="Tells the officer what to do today, which is what the window is for.",
 eff="Low to moderate"),

dict(id=17, grp="D", shot="s37.png",
 title="Correct three spellings",
 boxes=[(0.3,24,14,10,RED,1,"bl"), (25,25,18,14,RED,2,"tr")],
 notes=["‘My Pendancy’", "‘Not Submimtted’, ‘Sumbimtted’"],
 now="The officer's window reads <b>My Pendancy</b>, <b>Not Submimtted</b> and <b>Sumbimtted</b>.",
 chg="Correct to <b>My Pendency</b>, <b>Not submitted</b> and <b>Submitted</b>.",
 why="These are the first things noticed in a demonstration.",
 eff="Very low"),

dict(id=18, grp="D", shot="s38.png",
 title="Show only the roles the user holds",
 boxes=[(0.5,54,49,43,BLU,1,"tl")],
 notes=["Eleven roles listed; the user holds one"],
 now="The <b>One-Click Switch Role</b> panel lists eleven roles near the top. The officer's own information sits below it.",
 chg="Show the roles held. Keep the rest behind <b>View All Roles</b>, which already exists.",
 why="Returns the top of the screen to the officer's own position.",
 eff="Very low"),

dict(id=19, grp="E", shot="s53.png",
 title="Do not place the same officer in both authority roles",
 boxes=[(24,66,49,31,RED,1,"tl"), (74,66,15,31,AMB,2,"tr")],
 notes=["Same officer defaulted as reporting and reviewing authority", "Both target dates are the same"],
 now="On the Channel of Submission step the same officer appears as both <b>Reporting Authority</b> and <b>Reviewing Authority</b>, and both target dates default to 31/10/2026.",
 chg="Leave the reviewing authority blank for the custodian to choose. Show a confirmation message if the same officer is picked for both. Set the reviewing date after the reporting date.",
 why="The two-stage check is the main safeguard in the APAR process, and workflows are created in bulk.",
 eff="Low"),
]

GRP = {
 "A": ("Clarity of information", "#B45309"),
 "B": ("Navigation", "#1D4ED8"),
 "C": ("When data is awaited", "#0F766E"),
 "D": ("Officer's own window", "#7C3AED"),
 "E": ("Workflow creation", "#BE123C"),
}

# ---------------------------------------------------------------- PART 2
P2 = [
dict(id="S1", title="One stage strip on every screen",
 who="All four monitoring levels · all four user windows",
 gap="Each screen counts APARs differently — generated, closed, partially completed, workflow created. None shows the cycle as the six stages that the GR describes.",
 add="A single strip at the top of every dashboard and every user window: <b>Self-appraisal → Reporting → Reviewing → Disclosure → Representation → Closed</b>, with the count and the closing date under each stage. The same strip everywhere, filtered to whatever the user is allowed to see.",
 val="Custodian, cadre authority, service authority and ACS then read the same picture. An officer sees where their own APAR sits in the same six boxes.",
 eff="Moderate · one component, reused",
 mock="""<div class='stagestrip'>
   <div class='st done'><b>Self-appraisal</b><span>1,109 of 1,197</span><i>closed 31 May</i></div>
   <div class='st now'><b>Reporting</b><span>612 of 1,197</span><i>due 31 Jul</i></div>
   <div class='st'><b>Reviewing</b><span>—</span><i>due 30 Sep</i></div>
   <div class='st'><b>Disclosure</b><span>—</span><i>due 31 Oct</i></div>
   <div class='st'><b>Representation</b><span>—</span><i>15 days</i></div>
   <div class='st'><b>Closed</b><span>—</span><i>30 Nov</i></div></div>"""),

dict(id="S2", title="Show how long APARs have been pending, not only how many",
 who="Cadre monitoring authority · service monitoring authority · GAD",
 gap="Pendency is shown as a count. A count does not say whether the delay is of a week or of four months, so it does not say where to intervene.",
 add="Add age bands beside each pendency figure: <b>0–15 days · 16–30 · 31–60 · over 60</b>. The dates needed are already recorded against each stage.",
 val="A region with 40 APARs pending for 60 days and one with 40 pending for a week need different action. At present they look the same.",
 eff="Low to moderate · a date difference on existing fields",
 mock="""<table class='mock'><tr><th>REGION</th><th>0–15 d</th><th>16–30 d</th><th>31–60 d</th><th>Over 60 d</th></tr>
 <tr><td>MH-LR-AURANGABAD</td><td>12</td><td>9</td><td class='a'>14</td><td class='r'>5</td></tr>
 <tr><td>MH-LR-NASHIK</td><td>31</td><td>6</td><td>0</td><td>0</td></tr></table>
 <div class='cap'>Same totals as today, separated by how long they have been waiting.</div>"""),

dict(id="S3", title="An ‘action required by you’ block at the top of every user window",
 who="Officer · reporting authority · reviewing authority · custodian",
 gap="Each window opens on counts and system information. None opens on what the user has to do, or by when.",
 add="A single block at the top of each window: what is due from this user, how many, and the date. One line per item, each opening the relevant form.",
 val="Most delay is not refusal; it is not knowing an action is due. This is the cheapest way to reduce pendency.",
 eff="Low to moderate · uses counts the system already holds",
 mock="""<div class='action'><b>Action required by you</b>
   <div class='ar'><span>Your self-appraisal for 2025-26</span><i class='r'>due in 4 days</i></div>
   <div class='ar'><span>12 assessments as reporting authority</span><i class='a'>due 31 Jul</i></div>
   <div class='ar'><span>3 reviews as reviewing authority</span><i>due 30 Sep</i></div></div>"""),

dict(id="S4", title="An exceptions panel in the custodian window",
 who="Custodian and establishment officer",
 gap="Cases that block the cycle — no reporting authority mapped, workflow not created, a stage forwarded automatically, an NRC awaiting issue — are spread across different tables and have to be looked for.",
 add="One panel listing the exceptions with a count against each, every count opening the list of officers concerned.",
 val="The custodian is the only person who can clear these, and at present must know where to look.",
 eff="Low to moderate · brings together checks the system already makes",
 mock="""<div class='exc'>
   <div class='e'><b class='r'>4</b><span>Officers with no reporting authority mapped</span></div>
   <div class='e'><b class='a'>41</b><span>Workflow not yet created</span></div>
   <div class='e'><b class='a'>88</b><span>Stages forwarded automatically</span></div>
   <div class='e'><b>3</b><span>No Report Certificates awaiting issue</span></div></div>"""),

dict(id="S5", title="Let a monitoring authority compare its own units",
 who="Cadre monitoring authority · service monitoring authority",
 gap="The authority sees a flat table of its units with no indication of which are behind, or of how the service as a whole is placed.",
 add="Order the units by completion and show the service average as a line. Keep the table below it unchanged.",
 val="The authority's first question is which of its units need a reminder. This answers it without reading every row.",
 eff="Low · a sort and a reference line on figures already shown",
 mock="""<div class='bars'>
  <div class='b'><span>Nagpur</span><i style='width:81%'></i><em>81%</em></div>
  <div class='b'><span>Pune</span><i style='width:76%'></i><em>76%</em></div>
  <div class='b'><span>Amravati</span><i style='width:70%'></i><em>70%</em></div>
  <div class='b'><span>Aurangabad</span><i class='amb' style='width:64%'></i><em>64%</em></div>
  <div class='b'><span>Settlement Comm.</span><i class='red' style='width:56%'></i><em>56%</em></div>
  <div class='avg'>Service average 66.9%</div></div>"""),

dict(id="S6", title="A one-screen summary for GAD and the ACS",
 who="GAD · Additional Chief Secretary",
 gap="At State level the screen shows 70 service cards in alphabetical order. The position of the State as a whole has to be assembled by the reader.",
 add="One screen above the cards: the six stages with State totals, the ten services furthest behind, and the number of APARs that will not close by the cycle date if the present rate continues.",
 val="Gives the ACS the three things a review meeting asks for, without scrolling.",
 eff="Moderate · a summary built from figures already held",
 mock="""<div class='sumtiles'>
   <div class='s1'><b>29,831</b><span>APARs initiated of 71,364 officers</span></div>
   <div class='s1'><b>751</b><span>Closed</span></div>
   <div class='s1 warn'><b>14</b><span>Services below 60%</span></div></div>
 <table class='mock' style='margin-top:8px'><tr><th>FURTHEST BEHIND</th><th>%</th><th>PENDING OVER 60 DAYS</th></tr>
 <tr><td>MH-XXX</td><td class='r'>41.2%</td><td>212</td></tr>
 <tr><td>MAHA-YYY</td><td class='r'>48.7%</td><td>168</td></tr></table>"""),

dict(id="S7", title="Track disclosure and representation",
 who="Custodian · GAD",
 gap="The dashboards presently end at ‘closed’. Disclosure to the officer and the fifteen-day representation window are part of the process but are not counted anywhere.",
 add="A section showing: disclosed to officer, awaiting disclosure, representations received, representations pending decision, and days remaining in each window.",
 val="Disclosure and representation carry a statutory timeline. They need to be visible to be monitored.",
 eff="Moderate · a new section on stages the system already records",
 mock="""<table class='mock'><tr><th>STAGE</th><th>COUNT</th><th>OLDEST</th></tr>
 <tr><td>Awaiting disclosure</td><td>214</td><td class='a'>22 days</td></tr>
 <tr><td>Disclosed, within 15-day window</td><td>96</td><td>9 days</td></tr>
 <tr><td>Representations received</td><td>11</td><td>—</td></tr>
 <tr><td>Representations pending decision</td><td class='r'>7</td><td class='r'>34 days</td></tr></table>"""),

dict(id="S8", title="A timeliness register",
 who="All levels · required by the new forms",
 gap="The draft forms give five per cent of the final score to timeliness, and treat a stage forwarded automatically as late. Nothing on the present dashboards records this.",
 add="A register per officer: own stage submitted on time or late, stages submitted as reporting authority, stages submitted as reviewing authority, and the resulting marks.",
 val="Without it the timeliness provision in the forms cannot be applied or defended.",
 eff="Moderate · new, and dependent on the eHRMS reporting-chain mapping",
 mock="""<table class='mock'><tr><th>STAGE</th><th>POSITION</th><th>MARKS</th></tr>
 <tr><td>Own self-appraisal</td><td>Submitted 28 Apr, due 30 Apr</td><td class='g'>On time</td></tr>
 <tr><td>As reporting authority (24)</td><td>2 forwarded automatically</td><td class='r'>2 late</td></tr>
 <tr><td>As reviewing authority (9)</td><td>All signed before due date</td><td class='g'>On time</td></tr>
 <tr><td><b>Timeliness marks</b></td><td>5% of final score</td><td class='r'>−0.2</td></tr></table>"""),

dict(id="S9", title="A memo register",
 who="Reporting authority · custodian · GAD",
 gap="The point raised in the GAD discussion is that reporting authorities hesitate to grade below the benchmark because nothing was recorded during the year.",
 add="A register of memos issued during the assessment year, with the officer's reply or the absence of one, shown to the reporting authority at the time of grading. For the custodian and GAD, counts only — including the number of reporting authorities who issued none.",
 val="Gives the reporting authority a record to rely on, and lets GAD see where no record is being kept at all.",
 eff="Moderate · a new facility, discussed separately",
 mock="""<table class='mock'><tr><th>REPORTING AUTHORITY</th><th>SUBORDINATES</th><th>MEMOS ISSUED</th><th>NO REPLY</th></tr>
 <tr><td>S. S. Nair</td><td>24</td><td>6</td><td>2</td></tr>
 <tr><td>A. K. Desai</td><td>18</td><td class='r'>0</td><td>—</td></tr></table>
 <div class='cap'>Contents are not shown to the custodian — only whether a record exists.</div>"""),

dict(id="S10", title="Make every figure open the list behind it",
 who="All four monitoring levels",
 gap="One screen already allows a regional figure to be opened into the list of officers concerned, with Excel and CSV. Most other figures on most other screens cannot be opened.",
 add="Apply the same behaviour to every count on every dashboard, with the same export options.",
 val="A figure that cannot be opened cannot be acted upon. The pattern is already built and working on one screen.",
 eff="Low to moderate · extending an existing pattern",
 mock="""<div class='drill'><div class='d1'>204 <span>APARs not initiated</span></div>
 <div class='arrowdn'>↓ click</div>
 <table class='mock'><tr><th>OFFICER</th><th>DESIGNATION</th><th>STATUS</th></tr>
 <tr><td>Haribhau B. Santanse</td><td>Dy Supdt of Land Records</td><td>Not initiated</td></tr>
 <tr><td>Nitin B. Ganapure</td><td>Dy Supdt of Land Records</td><td>Not initiated</td></tr></table>
 <div class='toolbar' style='margin-top:6px'><span class='btn ghost'>Excel</span><span class='btn ghost'>CSV</span></div></div>"""),
]

RETAIN = [
 ("Opening a figure into the list of officers",
  "A regional figure opens into the named officers behind it, with Excel and CSV. This is what makes the dashboard usable, and it already works.",
  "s40.png"),
 ("The four-step workflow wizard",
  "Numbered steps, bulk selection, and Not Started / In Process / Completed filters. A sound pattern, worth using on other multi-step screens.",
  "s55.png"),
 ("The DPC report's method note",
  "The report states how the weighted grade is worked out, and lets the user hover to see which earlier years were used. Useful for a report placed before a committee.",
  "s51.png"),
]

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,sans-serif;color:#15233D;background:#EEF1F6;font-size:14px;line-height:1.55}
button{font-family:inherit;cursor:pointer;border:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 60px}

.mast{background:#15233D;color:#fff;padding:26px 0 22px}
.mast .in{max-width:1180px;margin:0 auto;padding:0 20px}
.mast .eye{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:#F3A43B;font-weight:600}
.mast h1{font-size:26px;font-weight:700;margin:8px 0 8px;max-width:800px;line-height:1.25}
.mast p{font-size:14px;color:#C2CFE2;max-width:760px}
.mast .meta{display:flex;gap:30px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.18);margin-top:16px;padding-top:13px;font-size:12px;color:#C2CFE2}
.mast .meta b{display:block;color:#fff;font-size:12.5px;margin-bottom:2px}
.chipdraft{display:inline-block;border:1px solid #F3A43B;color:#F3A43B;font-size:9.5px;letter-spacing:.1em;padding:3px 9px;border-radius:3px;text-transform:uppercase}

.bar{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #DDE3EF;box-shadow:0 1px 3px rgba(16,24,40,.06)}
.bar .in{max-width:1180px;margin:0 auto;padding:8px 20px;display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.bar .lab{font-size:12px;color:#64748B}
.fchip{border:1px solid #DDE3EF;background:#fff;border-radius:99px;padding:6px 13px;font-size:12.5px;color:#475569}
.fchip.on{background:#15233D;border-color:#15233D;color:#fff;font-weight:600}
.fchip .c{opacity:.65;margin-left:4px;font-size:11px}

.sec{margin:28px 0 14px;border-left:5px solid #E8820C;padding-left:13px}
.sec h2{font-size:21px;color:#15233D}
.sec p{font-size:13px;color:#64748B;margin-top:3px;max-width:780px}
.intro{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:18px 20px;margin-top:20px}
.intro h3{font-size:15px;margin-bottom:6px}
.intro ul{margin-left:18px;font-size:13px;color:#334155}
.intro li{margin-bottom:5px}
.legendrow{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px;font-size:12px;color:#475569;border-top:1px solid #E2E8F0;padding-top:10px}
.lg{display:flex;align-items:center;gap:6px}
.lg i{width:22px;height:11px;border:2px dashed;border-radius:2px;display:inline-block}

/* summary table */
table.sum{width:100%;border-collapse:collapse;font-size:12.5px;background:#fff}
table.sum th{background:#15233D;color:#fff;text-align:left;padding:7px 9px;font-size:10.5px;letter-spacing:.05em;text-transform:uppercase}
table.sum td{padding:7px 9px;border-bottom:1px solid #E2E8F0}
table.sum tr:hover td{background:#EFF5FF;cursor:pointer}
table.sum .n{font-weight:700;width:26px}
table.sum a{color:#1D4ED8;text-decoration:none}
.gtag{font-size:9.5px;font-weight:700;color:#fff;padding:2px 7px;border-radius:3px;white-space:nowrap}
.ef{font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px;background:#DCFCE7;color:#166534;white-space:nowrap}
.ef.m{background:#FEF3C7;color:#92400E}

/* cards */
.card{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:18px 20px;margin-bottom:18px;scroll-margin-top:64px}
.card .hd{display:flex;gap:10px;align-items:center;margin-bottom:10px}
.card .num{background:#15233D;color:#fff;width:25px;height:25px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;flex:0 0 auto}
.card h3{font-size:17px;color:#15233D;flex:1;line-height:1.3}

/* annotated screenshot */
.annoshot{position:relative;display:block;border:1px solid #CBD5E1;border-radius:5px;overflow:hidden;background:#fff}
.annoshot img{width:100%;display:block}
.anno{position:absolute;border:2.5px dashed;border-radius:3px;pointer-events:none}
.anno .tag{position:absolute;width:19px;height:19px;border-radius:50%;color:#fff;font-size:11.5px;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.anno .tag.tl{left:-10px;top:-10px}
.anno .tag.tr{right:-10px;top:-10px}
.anno .tag.bl{left:-10px;bottom:-10px}
.notelist{display:flex;gap:16px;flex-wrap:wrap;margin:8px 0 12px;font-size:12px;color:#334155}
.notelist .nl{display:flex;gap:6px;align-items:center}
.notelist .nl b{width:18px;height:18px;border-radius:50%;color:#fff;font-size:11px;display:flex;align-items:center;justify-content:center;flex:0 0 auto}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}
.blk .t{font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:#64748B;font-weight:700;margin-bottom:4px}
.blk p{font-size:13px;color:#334155}
.blk.now{border-left:3px solid #CBD5E1;padding-left:11px}
.blk.chg{border-left:3px solid #16A34A;padding-left:11px}
.whyline{background:#F1F5F9;border-radius:6px;padding:8px 11px;font-size:12.5px;margin-top:11px;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap}
.whyline b{color:#15233D}

/* part 2 */
.s2card{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:18px 20px;margin-bottom:18px}
.s2card .hd{display:flex;gap:10px;align-items:center;margin-bottom:3px}
.s2card .sid{background:#0F766E;color:#fff;border-radius:5px;padding:3px 9px;font-size:11.5px;font-weight:700}
.s2card h3{font-size:17px;flex:1}
.who{font-size:11.5px;color:#0F766E;font-weight:600;margin-bottom:11px}
.s2grid{display:grid;grid-template-columns:1fr 1.05fr;gap:18px;align-items:start}

/* mocks */
.mockbox{border:1px dashed #94A3B8;border-radius:6px;padding:11px;background:#FCFDFF}
table.mock{width:100%;border-collapse:collapse;font-size:11px;background:#fff}
table.mock th{background:#1F5C9E;color:#fff;padding:5px 7px;text-align:left;font-size:10px;border:1px solid #1A4E87}
table.mock td{padding:5px 7px;border:1px solid #DDE3EF;color:#334155}
td.g{color:#166534;font-weight:600}td.a{color:#B45309;font-weight:600}td.r{color:#B91C1C;font-weight:600}
.cap{font-size:11px;color:#64748B;font-style:italic;margin-top:6px}
.stagestrip{display:flex;gap:4px}
.stagestrip .st{flex:1;border:1px solid #DDE3EF;border-radius:5px;padding:7px 6px;background:#F8FAFC;text-align:center}
.stagestrip .st b{font-size:10px;display:block;color:#15233D}
.stagestrip .st span{font-size:11px;font-weight:700;color:#1F3B73;display:block;margin:2px 0}
.stagestrip .st i{font-size:9px;color:#64748B;font-style:normal}
.stagestrip .st.done{background:#ECFDF3;border-color:#BBF7D0}
.stagestrip .st.now{background:#FFF7ED;border-color:#FED7AA}
.action{border:1px solid #FDE68A;background:#FFFBEB;border-radius:7px;padding:11px 13px}
.action>b{font-size:12.5px;color:#92400E;display:block;margin-bottom:7px}
.ar{display:flex;justify-content:space-between;gap:10px;font-size:12px;padding:5px 0;border-top:1px solid #FDE68A}
.ar i{font-style:normal;font-weight:600;color:#475569}
.ar i.r{color:#B91C1C}.ar i.a{color:#B45309}
.exc{display:grid;gap:6px}
.exc .e{display:flex;gap:10px;align-items:center;border:1px solid #DDE3EF;border-radius:6px;padding:7px 10px;background:#fff;font-size:12px}
.exc .e b{font-size:17px;min-width:32px;color:#15233D}
.exc .e b.r{color:#B91C1C}.exc .e b.a{color:#B45309}
.bars .b{display:flex;align-items:center;gap:8px;font-size:11px;margin-bottom:5px}
.bars .b span{width:95px;color:#334155}
.bars .b i{height:13px;background:#1F5C9E;border-radius:2px;display:block}
.bars .b i.amb{background:#E8820C}.bars .b i.red{background:#DC2626}
.bars .b em{font-style:normal;font-weight:700;color:#1F3B73;font-size:11px}
.bars .avg{font-size:10.5px;color:#64748B;border-top:1px dashed #94A3B8;padding-top:5px;margin-top:3px}
.sumtiles{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.sumtiles .s1{border:1px solid #DDE3EF;border-radius:6px;padding:8px 10px;background:#fff}
.sumtiles .s1 b{font-size:19px;color:#1F3B73;display:block}
.sumtiles .s1 span{font-size:10px;color:#64748B}
.sumtiles .s1.warn{background:#FFFBEB;border-color:#FDE68A}
.drill .d1{border:1px solid #DDE3EF;border-radius:6px;padding:8px 11px;font-size:19px;font-weight:700;color:#1F3B73;background:#fff;display:inline-block}
.drill .d1 span{font-size:11px;font-weight:400;color:#64748B;margin-left:6px}
.arrowdn{font-size:11px;color:#64748B;margin:5px 0}
.toolbar{display:flex;gap:6px}
.btn{background:#1F5C9E;color:#fff;border-radius:4px;padding:3px 11px;font-size:10.5px;font-weight:600}
.btn.ghost{background:#EFF5FF;color:#1F5C9E}
.retainweb{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.retainweb .r{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:14px}
.retainweb .r img{width:100%;border:1px solid #CBD5E1;border-radius:5px;margin-bottom:9px;display:block}
.retainweb .r h4{font-size:13.5px;margin-bottom:4px}
.retainweb .r p{font-size:12px;color:#475569}
.next{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:20px;display:grid;grid-template-columns:1.1fr 1fr;gap:20px}
.next ol{margin-left:17px;font-size:13px;color:#334155}
.next li{margin-bottom:7px}
.nbox{border:1px solid #E2E8F0;border-left:3px solid #E8820C;border-radius:0 7px 7px 0;padding:11px 13px;font-size:12.5px;color:#334155;margin-bottom:11px}
.nbox b{display:block;color:#15233D;margin-bottom:3px}
.foot{text-align:center;font-size:12px;color:#94A3B8;padding:24px 0 0;border-top:1px solid #DDE3EF;margin-top:30px}
.lb{position:fixed;inset:0;background:rgba(13,25,48,.93);display:none;align-items:center;justify-content:center;z-index:100;padding:24px;cursor:zoom-out}
.lb.on{display:flex}
.lb img{max-width:100%;max-height:100%}
.hidden{display:none !important}
@media(max-width:900px){.grid2,.s2grid,.next,.retainweb{grid-template-columns:1fr}}
@media print{
 body{background:#fff}.bar{display:none}.card,.s2card{page-break-inside:avoid;border:1px solid #CBD5E1}
 .mast{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 @page{size:A4 portrait;margin:12mm}
}
"""

def anno_html(r):
    out = []
    for (l, t, w, h, c, n, side) in r["boxes"]:
        out.append(f"<div class='anno' style='left:{l}%;top:{t}%;width:{w}%;height:{h}%;border-color:{c}'>"
                   f"<span class='tag {side}' style='background:{c}'>{n}</span></div>")
    return "".join(out)

def notes_html(r):
    out = []
    for (bx, note) in zip(r["boxes"], r["notes"]):
        c, n = bx[4], bx[5]
        out.append(f"<div class='nl'><b style='background:{c}'>{n}</b><span>{note}</span></div>")
    return f"<div class='notelist'>{''.join(out)}</div>"

rows = "".join(
    f"<tr onclick=\"jump('p{r['id']}')\"><td class='n'>{r['id']}</td>"
    f"<td><span class='gtag' style='background:{GRP[r['grp']][1]}'>{GRP[r['grp']][0]}</span></td>"
    f"<td><a href='#p{r['id']}'>{r['title']}</a></td>"
    f"<td><span class='ef{' m' if 'moderate' in r['eff'].lower() else ''}'>{r['eff'].split(' · ')[0]}</span></td></tr>"
    for r in P1)

cards = "".join(f"""
<article class='card' id='p{r['id']}' data-g='{r['grp']}'>
  <div class='hd'><span class='num'>{r['id']}</span><h3>{r['title']}</h3>
    <span class='gtag' style='background:{GRP[r['grp']][1]}'>{GRP[r['grp']][0]}</span></div>
  <div class='annoshot' onclick="zoom(this.querySelector('img').src)"><img src='{src(r['shot'])}'>{anno_html(r)}</div>
  {notes_html(r)}
  <div class='grid2'>
    <div class='blk now'><div class='t'>On the screen now</div><p>{r['now']}</p></div>
    <div class='blk chg'><div class='t'>Suggested change</div><p>{r['chg']}</p></div>
  </div>
  <div class='whyline'><span><b>Why:</b> {r['why']}</span><span><b>Effort:</b> {r['eff']}</span></div>
</article>""" for r in P1)

s2 = "".join(f"""
<article class='s2card' id='{s['id']}'>
  <div class='hd'><span class='sid'>{s['id']}</span><h3>{s['title']}</h3></div>
  <div class='who'>For: {s['who']}</div>
  <div class='s2grid'>
    <div>
      <div class='blk now' style='margin-bottom:11px'><div class='t'>What is missing today</div><p>{s['gap']}</p></div>
      <div class='blk chg'><div class='t'>Section proposed</div><p>{s['add']}</p></div>
    </div>
    <div><div class='t' style='font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:#64748B;font-weight:700;margin-bottom:4px'>Indicative form</div>
      <div class='mockbox'>{s['mock']}</div></div>
  </div>
  <div class='whyline'><span><b>Why:</b> {s['val']}</span><span><b>Effort:</b> {s['eff']}</span></div>
</article>""" for s in P2)

retain = "".join(f"<div class='r'><img src='{src(sh)}' onclick=\"zoom(this.src)\"><h4>{t}</h4><p>{d}</p></div>"
                 for t, d, sh in RETAIN)

counts = {k: sum(1 for r in P1 if r["grp"] == k) for k in GRP}
chips = "".join(f"<button class='fchip' data-f='{k}' onclick=\"filt('{k}')\">{v[0]}<span class='c'>{counts[k]}</span></button>"
                for k, v in GRP.items())

HTML = f"""<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>APAR dashboards — suggested changes</title>
<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' rel='stylesheet'>
<style>{CSS}</style></head><body>

<header class='mast'><div class='in'>
<span class='eye'>Government of Maharashtra · General Administration Department</span>
<h1>APAR dashboards: suggested changes</h1>
<p>Part 1 marks small changes of wording and placement directly on the screens, in the manner GAD has been using.
Part 2 proposes new sections for the four monitoring levels and the four user windows.</p>
<div class='meta'>
<div><b>Prepared for</b>GAD, and thereafter for NIC</div>
<div><b>Prepared by</b>IDinsight</div>
<div><b>Based on</b>19 screens of the SPARROW<br>APAR application, October 2026</div>
<div><b>Status</b><span class='chipdraft'>Draft for discussion</span></div>
</div></div></header>

<nav class='bar'><div class='in'>
<span class='lab'>Show</span>
<button class='fchip on' data-f='all' onclick="filt('all')">All 19<span class='c'>19</span></button>
{chips}
<button class='fchip' style='margin-left:auto' onclick="window.print()">Print</button>
</div></nav>

<div class='wrap'>

<div class='intro'>
<h3>How to read this note</h3>
<ul>
<li><b>Part 1 — small changes.</b> 19 points. Each is marked on the screen itself. These are changes of wording,
order or placement. None needs a new screen or new data.</li>
<li><b>Part 2 — new sections.</b> 10 proposals for sections that do not exist today. These need development work,
and are offered for GAD to decide on before NIC is approached.</li>
<li><b>Effort shown against each point is our reading of the screens,</b> not NIC's estimate. NIC is best placed to
confirm it.</li>
</ul>
<div class='legendrow'>
<span style='font-weight:600;color:#15233D'>Marking on the screens:</span>
<span class='lg'><i style='border-color:#DC2626'></i> needs correcting</span>
<span class='lg'><i style='border-color:#E8820C'></i> needs explaining</span>
<span class='lg'><i style='border-color:#1D4ED8'></i> move or re-order</span>
<span class='lg'><i style='border-color:#15803D'></i> already available, bring forward</span>
</div>
</div>

<div class='sec'><h2>Part 1 — Small changes to the existing screens</h2>
<p>Wording, order and placement. Nothing here changes the figures or the design.</p></div>

<table class='sum'><tr><th></th><th>Group</th><th>Suggested change</th><th>Effort</th></tr>{rows}</table>

<div style='height:20px'></div>
{cards}

<div class='sec'><h2>Part 2 — Sections that could be added</h2>
<p>These do not exist today. They follow from the way the APAR process is being organised — four monitoring levels
(custodian, cadre monitoring authority, service monitoring authority, GAD and the ACS) and four user windows
(officer, reporting authority, reviewing authority, custodian). Each needs development work, so these are for GAD to
consider before approaching NIC.</p></div>
{s2}

<div class='sec'><h2>Features that should be kept as they are</h2>
<p>Noted so that they are not changed while the points above are taken up.</p></div>
<div class='retainweb'>{retain}</div>

<div class='sec'><h2>Next steps</h2><p>For GAD first, and thereafter for discussion with NIC.</p></div>
<div class='next'>
<div><ol>
<li><b>GAD to mark the list.</b> Which of the 19 small changes to take up, and which of the 10 new sections are wanted.</li>
<li><b>Two rules need a GAD decision</b> before NIC can act: the DPC eligibility rule (point 3), and how old dashboard
figures may be before they are flagged (point 14).</li>
<li><b>Then NIC.</b> Part 1 first, as it needs no new data. NIC to confirm the effort and say what fits the current release.</li>
<li><b>Part 2 separately.</b> The new sections need development time and should be sequenced after Part 1.</li>
<li><b>Review together</b> once Part 1 is live, before taking up the rest.</li>
</ol></div>
<div>
<div class='nbox'><b>For GAD's decision</b>The DPC eligibility rule is a departmental matter, not a technical one. NIC cannot
correct the note until it is confirmed. The same applies to the age at which dashboard figures should be flagged.</div>
<div class='nbox'><b>Not covered here</b>This note covers the dashboard and report screens only. The APAR forms, the
officer's filing experience and the source data are being taken up separately.</div>
<div class='nbox'><b>Acknowledgement</b>The screens reviewed cover officer, service, instance and departmental levels,
workflow creation and a set of reports. The suggestions here are made in that context.</div>
</div></div>

<div class='foot'>MahaPAR · Suggested changes to the SPARROW APAR dashboards · IDinsight with GAD · Draft for discussion</div>
</div>

<div class='lb' id='lb' onclick='closeZoom()'><img id='lbimg'></div>
<script>
function filt(f){{
 document.querySelectorAll('.fchip[data-f]').forEach(b=>b.classList.toggle('on',b.dataset.f===f));
 document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.g!==f));
}}
function jump(id){{filt('all');const e=document.getElementById(id);e.scrollIntoView({{behavior:'smooth'}});
 e.style.boxShadow='0 0 0 3px #BFD4F6';setTimeout(()=>e.style.boxShadow='',1400);}}
function zoom(s){{document.getElementById('lbimg').src=s;document.getElementById('lb').classList.add('on');}}
function closeZoom(){{document.getElementById('lb').classList.remove('on');}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeZoom();}});
</script></body></html>"""

open(OUT, "w").write(HTML)
print("wrote", OUT, "·", len(P1), "small changes ·", len(P2), "new sections")
