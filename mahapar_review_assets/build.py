#!/usr/bin/env python3
"""
Builds the MahaPAR / SPARROW dashboard refinement note as an HTML file,
which is then printed to PDF with headless Chromium.

Each recommendation is one landscape page:
  left  = cropped screenshot of the existing NIC screen
  right = observation, suggested refinement, rationale, effort, and a
          small redrawn mock of the proposed element.

Assumption flagged: effort ratings are IDinsight's reading of the screens,
not NIC's estimate. They are stated as such in the document.
"""

OUT = "/home/user/personal_v1/mahapar_review_assets/note.html"

# ---------------------------------------------------------------- content
# Each rec: id, tier, title, shot, observation, suggestion, why, effort, mock(html)

RECS = [
# ---------------------------------------------------------- A. clarity
dict(id=1, tier="A", title="Align the status label with the threshold scale already defined in the filter",
 shot="s44.png",
 obs="The filter on the Instance Dashboard defines four bands: Excellent 95%+, Good 80–94.9%, Warning 60–79.9%, Poor below 60%. The service cards presently display the label <b>GOOD</b> at values between 60% and 77%, which fall in the Warning band by that same scale.",
 sug="Drive the label from the thresholds already written into the filter, so a service at 66.88% is shown as <b>Warning</b> and the card and the filter tell the same story. No new calculation is required; the bands exist.",
 why="A senior officer scanning 70 cards reads the label before the number. Aligning the two means the dashboard can be relied upon at a glance, which is what it is for.",
 eff="Very low — a single mapping between the existing bands and the label.",
 mock="""
 <div class='mockcard'><div class='mr'><b>MAHA-MLR</b><span class='badge amber'>WARNING</span></div>
 <div class='big'>66.88%</div><div class='sm'>616 Officers | 412 Generated | 14 Closed</div>
 <div class='scalebar'><i class='on'></i><span>Warning band 60–79.9%</span></div></div>"""),

dict(id=2, tier="A", title="Distinguish APAR completion from officer performance in the column headings",
 shot="s41.png",
 obs="The measure of how many APARs have been initiated is presently headed <b>PAR GENERATED PERFORMANCE</b>, and the accompanying column is headed <b>PERFORMANCE</b>. Both describe progress in filing, rather than the performance of the officers concerned.",
 sug="Rename the tile to <b>APARs initiated (%)</b> and the column to <b>Filing status</b>. The underlying figures stay exactly as they are.",
 why="It removes any possibility of a filing statistic being read as an assessment of a region's officers, and makes the dashboard's purpose self-evident to a first-time viewer.",
 eff="Very low — label text only.",
 mock="""
 <table class='mock'><tr><th>ORGANISATION</th><th>APARs INITIATED (%)</th><th>FILING STATUS</th></tr>
 <tr><td>MH-LR-NAGPUR REGION</td><td class='g'>81.18%</td><td><span class='badge green'>ON TRACK</span></td></tr>
 <tr><td>MH-LR-AURANGABAD REGION</td><td class='a'>63.89%</td><td><span class='badge amber'>WARNING</span></td></tr>
 <tr><td>MH-LR-SETTLEMENT COMM. OFFICE</td><td class='a'>56.00%</td><td><span class='badge red'>POOR</span></td></tr></table>
 <div class='cap'>Same data, headings that say what is being counted.</div>"""),

dict(id=3, tier="A", title="State the DPC eligibility threshold that the report actually applies",
 shot="s51.png",
 obs="The note below the DPC report reads <i>“Employees with a total grade ≥ 30 are marked eligible.”</i> The Total Grade column is out of 30, and officers are being marked eligible at 27.52 and 27.31. The stated rule and the applied rule appear to differ.",
 sug="Restate the note to match the rule in use — for example <b>“Officers with a total grade of 27 or above across the three years are marked eligible.”</b> If the intended rule is an average rather than a total, say so in the same line.",
 why="The DPC report supports promotion decisions and may be placed before a committee. A note that matches the computation protects the report from question at that stage.",
 eff="Very low — one line of text, once the intended rule is confirmed with GAD.",
 mock="""
 <table class='mock'><tr><th>NAME</th><th>2022-23</th><th>2023-24</th><th>2024-25</th><th>TOTAL (30)</th><th>ELIGIBLE</th></tr>
 <tr><td>Anand Ashok Katake</td><td>9.00</td><td>9.22</td><td>9.30</td><td>27.52</td><td><span class='badge green'>Yes</span></td></tr></table>
 <div class='notebox'><b>Note:</b> Officers with a total grade of 27 or above across the three assessment years
 are marked eligible. Hover over a grade to see which preceding years were used.</div>"""),

dict(id=4, tier="A", title="Bring the pendency columns to the front of the Service Dashboard",
 shot="s42.png",
 obs="The Service Dashboard carries seven columns recording where an APAR is presently pending — with the custodian, the officer, the reporting authority, the reviewing authority, the accepting authority and the CR section. These sit to the right of the table and are reached only by horizontal scrolling, and several hold a value of zero for every row.",
 sug="Place the pendency columns immediately after the organisation name, move the APAR count columns to the right, and suppress any column holding zero for every row in the selected year. A <b>“Pending with”</b> group heading can span them.",
 why="“With whom is the APAR presently lying” is the question the monitoring authorities ask most often. The data is already collected; this simply brings it into first view.",
 eff="Low — column order and a rule to hide all-zero columns. No change to the query.",
 mock="""
 <table class='mock'><tr><th rowspan='2'>ORGANISATION</th><th colspan='3' class='grp'>PENDING WITH</th><th rowspan='2'>INITIATED</th><th rowspan='2'>CLOSED</th></tr>
 <tr><th>Officer</th><th>Reporting</th><th>Reviewing</th></tr>
 <tr><td>MH-LR-AURANGABAD</td><td class='a'>24</td><td class='r'>40</td><td>16</td><td>140</td><td>0</td></tr>
 <tr><td>MH-LR-NASHIK</td><td class='r'>37</td><td>25</td><td>21</td><td>172</td><td>10</td></tr></table>
 <div class='cap'>Columns that were empty for every region are not shown for this year.</div>"""),

dict(id=5, tier="A", title="Reconcile the two officer counts shown on the same screen",
 shot="s43b.png",
 obs="The summary tile reports <b>616</b> total officers while the table total below reports <b>611</b>. Separately, APARs generated (868) exceeds officers posted (611), which is consistent with officers having more than one reporting period in the year, though this is not stated on screen.",
 sug="Reconcile the two counts, or add a single clarifying line beneath the table: <b>“An officer with more than one reporting period in the year has an APAR for each period, so APAR count may exceed officer count.”</b>",
 why="Monitoring authorities are likely to notice the difference and ask. One line settles it, and spares NIC and GAD a recurring query.",
 eff="Low — one explanatory line; reconciliation of the tile requires a check of the counting basis.",
 mock="""
 <div class='mockcard'><div class='mr'><b>TOTAL OFFICERS</b></div><div class='big'>611</div>
 <div class='sm'>As per the regional table below</div></div>
 <div class='notebox'>An officer with more than one reporting period in the year has an APAR for each period.
 APAR count may therefore exceed officer count.</div>"""),

# ------------------------------------------------- B. navigation
dict(id=6, tier="B", title="Open the Service Dashboard on the Officer-wise view",
 shot="s43.png",
 obs="The screen offers two views. <b>Officer-wise Statistics</b> presents seven columns, all fully visible. <b>PAR-wise Statistics</b> presents around fourteen, most abbreviated and requiring horizontal scrolling. The second appears to open first.",
 sug="Make Officer-wise the view that opens by default, with PAR-wise one click away for those who need the detail.",
 why="Most users want the regional position at a glance. Opening on the view that fits the screen gives them that without any navigation.",
 eff="Very low — default tab selection.",
 mock="""
 <div class='tabs'><div class='tab on'>Officer-wise Statistics <span class='dflt'>opens here</span></div><div class='tab'>PAR-wise Statistics</div></div>
 <table class='mock'><tr><th>ORGANISATION</th><th>OFFICERS</th><th>APAR INITIATED</th><th>NOT INITIATED</th><th>%</th></tr>
 <tr><td>MH-LR-AURANGABAD</td><td>108</td><td>69</td><td>39</td><td>63.89%</td></tr>
 <tr><td>MH-LR-PUNE</td><td>96</td><td>73</td><td>23</td><td>76.04%</td></tr></table>"""),

dict(id=7, tier="B", title="Order the service cards by completion, lowest first",
 shot="s44.png",
 obs="The Instance Dashboard presents around 70 service cards in alphabetical order. A viewer looking for the services needing attention must read through the full set.",
 sug="Order the cards by completion percentage, lowest first, so the services requiring follow-up appear at the top. An <b>A–Z</b> option can remain for those looking for a particular service, alongside the search box already provided.",
 why="It turns a reference list into a priority list, using the figures already on each card.",
 eff="Very low — default sort order.",
 mock="""
 <div class='sortrow'>Sort by <b>Lowest completion first</b> &nbsp;|&nbsp; <span class='mut'>A–Z</span></div>
 <div class='minicards'>
   <div class='mc red'><b>MH-XXX</b><span>41.2%</span></div>
   <div class='mc red'><b>MAHA-YYY</b><span>48.7%</span></div>
   <div class='mc amb'><b>MH-ZZZ</b><span>56.0%</span></div>
   <div class='mc amb'><b>MAHA-MLR</b><span>66.9%</span></div>
 </div><div class='cap'>Services needing attention surface first.</div>"""),

dict(id=8, tier="B", title="Give each pendency column a distinct heading",
 shot="s46.png",
 obs="The Officers APAR Pending Report carries five adjacent columns whose headings all abbreviate to <b>“Pending Officer …”</b>. On screen they are indistinguishable from one another.",
 sug="Rename them to describe what each holds: <b>Pending with · Designation · Office · Pending since (days) · Contact</b>.",
 why="This report holds precisely the information GAD needs for follow-up. Distinct headings make it usable without opening the export.",
 eff="Very low — heading text only.",
 mock="""
 <table class='mock'><tr><th>PENDING WITH</th><th>DESIGNATION</th><th>OFFICE</th><th>PENDING SINCE</th><th>CONTACT</th></tr>
 <tr><td>Anand Ashok Katake</td><td>District Deputy Registrar</td><td>MH-COOP-PUNE-HO</td><td class='r'>47 days</td><td>9123034016</td></tr></table>
 <div class='cap'>Same five columns, named for what they carry.</div>"""),

dict(id=9, tier="B", title="Allow the pending and pen-picture reports to run for all officers",
 shot="s48.png",
 obs="<b>Employee Search</b> is a mandatory field on the Officers APAR Pending Report and the Officer Pen Picture Report. A user must therefore know an officer's name before the report will run, and the result returns one officer at a time.",
 sug="Make the officer name optional, with the report defaulting to all officers in the selected service and assessment year. The name can remain as a filter for those who want a single record.",
 why="This is the change that converts a record-lookup facility into the monitoring report that cadre and service authorities have asked for. The query and the export already exist.",
 eff="Low to moderate — removing the mandatory filter and returning a list rather than a single row.",
 mock="""
 <div class='filters'><span>Service <b>MAHA-COR</b></span><span>Assessment Year <b>2025-26</b></span>
 <span>Officer name <i class='mut'>optional</i></span><span class='btn'>View</span></div>
 <table class='mock'><tr><th>OFFICER</th><th>PENDING WITH</th><th>SINCE</th></tr>
 <tr><td>Anand Ashok Katake</td><td>Self-appraisal — officer</td><td class='r'>47 days</td></tr>
 <tr><td>Medha Gopal Wake</td><td>Reporting authority</td><td class='a'>21 days</td></tr>
 <tr><td colspan='3' class='mut'>… 206 officers in this service</td></tr></table>"""),

dict(id=10, tier="B", title="Use administrative wording in the status fields",
 shot="s46.png",
 obs="The status column reads <b>“Pending at Level: OFFICER REPORTED UPON”</b>. This is the system's internal description of the stage rather than the wording used in the APAR instructions.",
 sug="Present the stage in the language of the process — <b>“Awaiting self-appraisal by the officer”</b>, <b>“Awaiting assessment by the reporting authority”</b>, <b>“Awaiting review by the reviewing authority”</b>.",
 why="The same words then appear in the circular, on the dashboard and in the report, which reduces queries to the helpdesk and to GAD.",
 eff="Very low — a wording map for the existing status values.",
 mock="""
 <table class='mock'><tr><th>STAGE (as displayed today)</th><th>SUGGESTED WORDING</th></tr>
 <tr><td class='mut'>OFFICER REPORTED UPON</td><td>Awaiting self-appraisal by the officer</td></tr>
 <tr><td class='mut'>REPORTING AUTHORITY</td><td>Awaiting assessment by the reporting authority</td></tr>
 <tr><td class='mut'>REVIEWING AUTHORITY</td><td>Awaiting review by the reviewing authority</td></tr>
 <tr><td class='mut'>WORKFLOW NOT CREATED</td><td>APAR not yet initiated by the custodian</td></tr></table>"""),

dict(id=11, tier="B", title="Bring the Select Columns facility into view",
 shot="s48.png",
 obs="The Pen Picture Report allows the user to choose which columns are displayed. The facility sits inside a dropdown alongside the column list and is easy to miss.",
 sug="Place <b>Select columns</b> as a visible control beside Export to PDF and Export to Excel, where users already look for table controls.",
 why="A facility that addresses the width of these reports is already built. Making it visible is the whole of the work.",
 eff="Very low — relocation of an existing control.",
 mock="""
 <div class='toolbar'><span class='btn ghost'>Select columns (7 of 12)</span>
 <span class='btn ghost'>Export to PDF</span><span class='btn ghost'>Export to Excel</span>
 <span class='srch'>Search</span></div>
 <div class='cap'>The control already exists; this places it where users look for it.</div>"""),

# ------------------------------------------- C. awaited data
dict(id=12, tier="C", title="Distinguish “no selection made” from “no records yet”",
 shot="s50.png",
 obs="Several screens display <b>“No data available”</b> with pagination reading 0 of 0 — the Role Details window, the DPC Officer's Assessment screen before any selection, and the Pen Picture report. On the Officer's Assessment screen a <b>Download Zip</b> button remains active over the empty table.",
 sug="Use wording that names the reason: <b>“Select a DPC and service to begin”</b> before a selection; <b>“No officers are mapped to this role at present”</b> where the set is genuinely empty; <b>“Pen picture not yet recorded — reporting stage is in progress”</b> where the stage is pending. Export buttons may be greyed until rows are present.",
 why="These screens are the ones most often seen during demonstrations. Wording that explains the position reads as a system working correctly rather than one returning nothing.",
 eff="Low — empty-state text and a condition on the export button.",
 mock="""
 <div class='empty'><b>Select a DPC and service to begin</b>
 <span>Officers eligible for consideration will be listed here once a DPC is selected.</span></div>
 <div class='empty alt'><b>No officers are mapped to this role at present</b>
 <span>Mapping is carried out by the establishment officer.</span></div>
 <div class='toolbar'><span class='btn dis'>Download Zip</span><span class='mut'>available once officers are listed</span></div>"""),

dict(id=13, tier="C", title="Explain a blank grade rather than showing a dash",
 shot="s47.png",
 obs="On the Grade By Officer report the reviewing authority's grade is shown as <b>“-”</b> for both reporting periods, while the reporting authority's grade is recorded. The report does not indicate whether the review is pending or was not required.",
 sug="Replace the dash with the position: <b>“Not yet recorded — reviewing stage pending since 30 Sep 2026”</b>, or <b>“Review not applicable for this period”</b> where that is the case.",
 why="The grade is the single most consequential field in the record. A reader should not have to infer why it is blank.",
 eff="Low — a status message in place of the empty value.",
 mock="""
 <table class='mock'><tr><th>PERIOD</th><th>REPORTING AUTHORITY</th><th>REVIEWING AUTHORITY</th></tr>
 <tr><td>01-04-2025 to 03-07-2025</td><td>P. V. Wankhede — <b>7.50</b></td>
 <td class='pend'>Milind Aakre<br><span>Not yet recorded — pending since 30 Sep 2026</span></td></tr></table>"""),

dict(id=14, tier="C", title="Show how recent the figures are",
 shot="s41.png",
 obs="The dashboards carry a <b>Last Updated</b> stamp. On the screens reviewed it reads 26 September while the screen was being viewed on 8 October, a difference of twelve days, which is not drawn to the viewer's attention.",
 sug="Add the elapsed time beside the stamp — <b>“Last updated 26 Sep 2026 (12 days ago)”</b> — and show it in amber once it exceeds the refresh interval agreed with GAD.",
 why="Monitoring authorities may act on these figures in review meetings. Knowing their vintage is part of reading them correctly.",
 eff="Very low — a derived value beside an existing field.",
 mock="""
 <div class='mockcard amberbg'><div class='mr'><b>LAST UPDATED</b></div>
 <div class='mid'>26 SEP 2026, 05:08 PM</div>
 <div class='warn'>12 days ago — figures may not reflect the current position</div></div>"""),

dict(id=15, tier="C", title="Display implausible legacy values as “Not available”",
 shot="s40.png",
 obs="Allotment year is shown as <b>1900</b> for some officers, which appears to be a placeholder carried in from the source record rather than a true year.",
 sug="Display such values as <b>“Not available”</b> at the point of display, and give GAD a count of affected records so that the source data can be corrected in due course.",
 why="It prevents an evident placeholder from appearing in reports placed before senior officers, while the underlying correction is taken up separately.",
 eff="Low — a display rule, plus a count for GAD.",
 mock="""
 <table class='mock'><tr><th>OFFICER</th><th>DESIGNATION</th><th>ALLOTMENT YEAR</th></tr>
 <tr><td>Digambar Walmik Bhogawade</td><td>Dy Supdt of Land Records</td><td class='mut'>Not available</td></tr>
 <tr><td>Nitin Bhagwat Ganapure</td><td>Dy Supdt of Land Records</td><td>2014</td></tr></table>
 <div class='notebox'><b>For GAD:</b> 1 of 41 records in this region carries a placeholder allotment year.</div>"""),

# --------------------------------------------- D. officer window
dict(id=16, tier="D", title="Make “My Pendency” answer what the officer must do",
 shot="s37.png",
 obs="The officer's dashboard shows <b>My Pendancy: 87</b> as a single figure, alongside tiles for successful and failed eSign and DSC transactions and the IP addresses used. The pendency figure does not indicate how many items await action by the officer and how many are with others.",
 sug="Present two figures — <b>Awaiting my action</b> and <b>Awaiting action by others</b> — each opening the corresponding list. The signature transaction and IP address tiles may be grouped lower on the page under <b>Signature activity</b>.",
 why="It tells the officer what to do today, which is the purpose of the window. The signature details remain available for verification, without occupying the first screen.",
 eff="Low to moderate — re-weighting existing tiles and splitting one count that the system already holds by stage.",
 mock="""
 <div class='twotile'>
  <div class='t amb'><b>12</b><span>Awaiting my action</span><i>3 due within 7 days</i></div>
  <div class='t blu'><b>75</b><span>Awaiting action by others</span><i>with reporting and reviewing authorities</i></div>
 </div>
 <div class='collapsed'>▸ Signature activity &nbsp;<span class='mut'>eSign and DSC transactions, last sign-in details</span></div>"""),

dict(id=17, tier="D", title="Correct the spellings, and place IPR under its own menu",
 shot="s37.png",
 obs="The officer's dashboard carries <b>“My Pendancy”</b>, <b>“Not Submimtted”</b> and <b>“Sumbimtted”</b>. The same screen also carries <b>My IPR Status</b>, which relates to the Immovable Property Return rather than to the APAR.",
 sug="Correct the three spellings to <b>Pendency</b>, <b>Not submitted</b> and <b>Submitted</b>. Place IPR under its own menu item so that the APAR window carries APAR matters only.",
 why="These are the first things noticed in a demonstration before GAD and senior officers, and they cost nothing to put right.",
 eff="Very low — text corrections and one menu placement.",
 mock="""
 <table class='mock'><tr><th>PRESENTLY</th><th>SUGGESTED</th></tr>
 <tr><td class='mut'>My Pendancy</td><td>My Pendency</td></tr>
 <tr><td class='mut'>Not Submimtted</td><td>Not submitted</td></tr>
 <tr><td class='mut'>Sumbimtted</td><td>Submitted</td></tr>
 <tr><td class='mut'>My IPR Status <i>(on the APAR window)</i></td><td>IPR — under its own menu</td></tr></table>"""),

dict(id=18, tier="D", title="Show the roles the user presently holds",
 shot="s38.png",
 obs="The <b>One-Click Switch Role</b> panel lists eleven roles near the top of the window, of which the user holds one. The panel occupies the upper part of the screen, placing the officer's own APAR information further down.",
 sug="Show only the roles held, with the remainder behind the <b>View All Roles</b> control already provided.",
 why="It returns the upper part of the window to the officer's own position, which is what most users come to the screen for.",
 eff="Very low — a filter on an existing list; the control for the full list already exists.",
 mock="""
 <div class='roles'><div class='role on'>✓ USER <span>current</span></div><div class='role on'>PAR CUSTODIAN</div></div>
 <div class='btn ghost'>View all roles (11)</div>
 <div class='cap'>Roles held are shown; the full list remains one click away.</div>"""),

# --------------------------------------------- E. workflow creation
dict(id=19, tier="E", title="Avoid defaulting the same officer to both authorities, and stagger the two target dates",
 shot="s53.png",
 obs="On the Channel of Submission step, the same officer appears selected as both <b>Reporting Authority</b> and <b>Reviewing Authority</b>, and both target dates default to the same date, 31/10/2026. Separately, <b>Form Type</b> on the preceding step is a required field presented without an indication of which form applies to which group of officers.",
 sug="Leave the reviewing authority blank for the custodian to select, and display a confirmation message where the same officer is chosen for both roles. Default the reviewing target date after the reporting target date. Against Form Type, show the applicable form for the officer's group, for example <b>“Form A — Group A and B officers”</b>.",
 why="The two-stage check is the core safeguard in the APAR process. A default that places one officer in both roles may be carried forward unnoticed when workflows are created in bulk.",
 eff="Low — default values, one confirmation message, and a help line against Form Type.",
 mock="""
 <table class='mock'><tr><th>STAGE</th><th>NAME</th><th>TARGET DATE</th></tr>
 <tr><td>Reporting Authority</td><td>Shri Vaseem Anwar Sayyad</td><td>31/07/2026</td></tr>
 <tr><td>Reviewing Authority</td><td class='mut'>Select reviewing authority</td><td>30/09/2026</td></tr></table>
 <div class='notebox warnbox'>The reporting and reviewing authority are the same officer.
 Please confirm this is intended before proceeding.</div>"""),
]

RETAIN = [
 ("Drill-through from the aggregate to named officers",
  "From the regional figure to the list of officers whose workflow has not been created, with Excel and CSV export. This is the step that makes the dashboard actionable, and it already works.", "s40.png"),
 ("The four-step workflow creation wizard",
  "Numbered progress, bulk selection, and Not Started / In Process / Completed filters on the officer list. The structure is sound and should be retained as the pattern for other multi-step screens.", "s55.png"),
 ("The DPC report's method note and hover facility",
  "The report states how the weighted grade is calculated and allows the user to hover to see which preceding years were used. This degree of openness about method is unusual and valuable, particularly for a report placed before a committee.", "s51.png"),
]

TIERS = {
 "A": ("Clarity of information for decision-makers", "#B45309"),
 "B": ("Navigation and ease of use", "#1D4ED8"),
 "C": ("Clarity when data is awaited", "#0F766E"),
 "D": ("The officer's own window", "#7C3AED"),
 "E": ("Workflow creation", "#BE123C"),
}

# ---------------------------------------------------------------- styles
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
@page{size:A4 landscape;margin:0}
body{font-family:'Inter',system-ui,sans-serif;color:#15233D;font-size:11px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:12mm 13mm 10mm;position:relative;page-break-after:always;overflow:hidden;background:#fff}
.page:last-child{page-break-after:auto}
.ph{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #15233D;padding-bottom:5px;margin-bottom:9px}
.ph .t{font-size:9px;letter-spacing:.09em;text-transform:uppercase;color:#64748B}
.ph .n{font-size:9px;color:#64748B}
.pf{position:absolute;left:13mm;right:13mm;bottom:6mm;display:flex;justify-content:space-between;font-size:8px;color:#94A3B8;border-top:1px solid #E2E8F0;padding-top:4px}

/* cover */
.cover{background:#15233D;color:#fff;display:flex;flex-direction:column;justify-content:space-between}
.cover .eyebrow{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#F59E0B;font-weight:600}
.cover h1{font-size:34px;line-height:1.15;font-weight:700;margin:10px 0 12px;max-width:80%}
.cover h2{font-size:14px;font-weight:400;color:#B8C7DE;max-width:68%;line-height:1.6}
.cover .meta{display:flex;gap:38px;border-top:1px solid rgba(255,255,255,.2);padding-top:14px;font-size:10px;color:#B8C7DE}
.cover .meta b{display:block;color:#fff;font-size:12px;margin-bottom:2px}
.cover .draft{display:inline-block;border:1px solid #F59E0B;color:#F59E0B;font-size:9px;letter-spacing:.1em;padding:3px 10px;border-radius:3px;text-transform:uppercase}

h3.sec{font-size:15px;color:#15233D;margin-bottom:5px}
p.lead{font-size:11.5px;color:#334155;max-width:215mm;margin-bottom:9px}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.box{border:1px solid #E2E8F0;border-radius:6px;padding:11px 13px}
.box h4{font-size:11.5px;margin-bottom:4px;color:#15233D}
.box p{font-size:10.5px;color:#475569}
.box.accent{border-left:3px solid #F59E0B}

/* recommendation page */
.rec{display:flex;flex-direction:column}
.recbody{display:grid;grid-template-columns:1fr 1.05fr;gap:14px;align-items:start;margin-top:9px}
.side{display:flex;flex-direction:column;min-height:0}
.shotfull{border:1px solid #CBD5E1;border-radius:4px;background:#F8FAFC;padding:5px;text-align:center}
.shotfull img{max-width:100%;max-height:74mm;width:auto;display:inline-block;border:1px solid #E2E8F0}
.lbl{font-size:8.5px;letter-spacing:.1em;text-transform:uppercase;color:#64748B;font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px}
.lbl::after{content:'';flex:1;height:1px;background:#E2E8F0}
.shotwrap{border:1px solid #CBD5E1;border-radius:4px;overflow:hidden;background:#F8FAFC;margin-bottom:8px}
.shotwrap img{width:100%;display:block}
.obs{font-size:10.5px;color:#334155}
.obs b{color:#15233D}
.sug{font-size:10.5px;color:#334155;margin-bottom:8px}
.why{background:#F1F5F9;border-radius:5px;padding:8px 10px;font-size:10px;color:#334155;margin-top:9px}
.why b{color:#15233D}
.eff{display:flex;gap:7px;align-items:center;font-size:9.5px;color:#475569;margin-top:7px}
.eff .pill{background:#ECFDF3;color:#166534;border-radius:99px;padding:2px 9px;font-weight:600;font-size:9px}
.rectitle{display:flex;gap:9px;align-items:flex-start;margin-bottom:8px}
.rectitle .num{background:#15233D;color:#fff;width:21px;height:21px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex:0 0 auto}
.rectitle h2{font-size:14.5px;line-height:1.3;color:#15233D}
.tierchip{font-size:8.5px;letter-spacing:.07em;text-transform:uppercase;font-weight:700;padding:2px 8px;border-radius:3px;color:#fff}

/* mock components */
.mockbox{border:1px dashed #94A3B8;border-radius:5px;padding:10px;background:#FCFDFF}
table.mock{width:100%;border-collapse:collapse;font-size:9px;background:#fff}
table.mock th{background:#1F5C9E;color:#fff;font-weight:600;padding:4px 6px;text-align:left;font-size:8.5px;border:1px solid #1A4E87}
table.mock th.grp{background:#F59E0B;text-align:center;border-color:#D97706}
table.mock td{padding:4px 6px;border:1px solid #DDE3EF;color:#334155}
table.mock td.g{color:#166534;font-weight:600}
table.mock td.a{color:#B45309;font-weight:600}
table.mock td.r{color:#B91C1C;font-weight:600}
td.mut,.mut{color:#94A3B8}
td.pend span{display:block;font-size:8px;color:#B45309}
.badge{font-size:8px;font-weight:700;padding:2px 7px;border-radius:99px;letter-spacing:.04em}
.badge.green{background:#DCFCE7;color:#166534}
.badge.amber{background:#FEF3C7;color:#92400E}
.badge.red{background:#FEE2E2;color:#991B1B}
.mockcard{border:1px solid #DDE3EF;border-radius:6px;padding:10px 12px;background:#fff}
.mockcard.amberbg{background:#FFFBEB;border-color:#FDE68A}
.mockcard .mr{display:flex;justify-content:space-between;align-items:center;font-size:10px}
.mockcard .big{font-size:26px;font-weight:700;color:#1F3B73;margin:3px 0}
.mockcard .mid{font-size:13px;font-weight:600;color:#92400E;margin:3px 0}
.mockcard .sm{font-size:8.5px;color:#64748B}
.mockcard .warn{font-size:9px;color:#B45309;font-weight:600;margin-top:4px}
.scalebar{display:flex;align-items:center;gap:6px;margin-top:7px;font-size:8.5px;color:#92400E}
.scalebar i{width:38px;height:5px;border-radius:3px;background:#F59E0B;display:block}
.cap{font-size:8.5px;color:#64748B;margin-top:6px;font-style:italic}
.notebox{background:#F1F5F9;border-left:3px solid #1F5C9E;border-radius:0 4px 4px 0;padding:7px 9px;font-size:9px;color:#334155;margin-top:7px}
.notebox.warnbox{background:#FFFBEB;border-left-color:#F59E0B;color:#92400E}
.tabs{display:flex;gap:3px;margin-bottom:7px}
.tab{font-size:9px;padding:5px 11px;background:#E2E8F0;color:#475569;border-radius:4px 4px 0 0}
.tab.on{background:#1F5C9E;color:#fff;font-weight:600}
.tab .dflt{font-size:7.5px;background:rgba(255,255,255,.25);padding:1px 5px;border-radius:99px;margin-left:4px}
.sortrow{font-size:9.5px;color:#334155;margin-bottom:7px}
.minicards{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.mc{border:1px solid #DDE3EF;border-radius:5px;padding:7px 9px;display:flex;justify-content:space-between;align-items:center;font-size:9.5px;background:#fff}
.mc.red{border-left:3px solid #DC2626}.mc.amb{border-left:3px solid #F59E0B}
.mc span{font-weight:700;color:#1F3B73}
.filters{display:flex;gap:9px;align-items:center;flex-wrap:wrap;font-size:9px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:5px;padding:7px 9px;margin-bottom:7px}
.btn{background:#1F5C9E;color:#fff;border-radius:4px;padding:3px 11px;font-size:9px;font-weight:600}
.btn.ghost{background:#EFF5FF;color:#1F5C9E}
.btn.dis{background:#E2E8F0;color:#94A3B8}
.toolbar{display:flex;gap:7px;align-items:center;margin-bottom:7px;font-size:9px}
.srch{border:1px solid #DDE3EF;border-radius:4px;padding:3px 24px 3px 8px;font-size:9px;color:#94A3B8}
.empty{border:1px dashed #CBD5E1;border-radius:5px;padding:12px;text-align:center;background:#F8FAFC;margin-bottom:7px}
.empty b{display:block;font-size:10.5px;color:#15233D;margin-bottom:3px}
.empty span{font-size:9px;color:#64748B}
.empty.alt{background:#FFFBEB;border-color:#FDE68A}
.twotile{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
.twotile .t{border-radius:6px;padding:10px;color:#fff}
.twotile .t.amb{background:#D97706}.twotile .t.blu{background:#1F5C9E}
.twotile .t b{font-size:26px;display:block;line-height:1}
.twotile .t span{font-size:10px;display:block;margin-top:2px}
.twotile .t i{font-size:8.5px;opacity:.85;font-style:normal;display:block;margin-top:3px}
.collapsed{border:1px solid #E2E8F0;border-radius:5px;padding:8px 10px;font-size:9.5px;color:#475569;background:#F8FAFC}
.roles{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:7px}
.role{border:1px solid #DDE3EF;border-radius:5px;padding:6px 9px;font-size:9.5px;background:#fff}
.role.on{border-color:#16A34A;background:#F0FDF4;color:#166534;font-weight:600}
.role span{font-size:8px;color:#64748B;font-weight:400}

/* summary table */
table.sum{width:100%;border-collapse:collapse;font-size:9.5px}
table.sum th{background:#15233D;color:#fff;text-align:left;padding:6px 8px;font-size:8.5px;letter-spacing:.05em;text-transform:uppercase}
table.sum td{padding:5px 8px;border-bottom:1px solid #E2E8F0;vertical-align:top}
table.sum tr:nth-child(even) td{background:#F8FAFC}
table.sum .n{font-weight:700;color:#15233D;width:22px}
.effpill{font-size:8px;font-weight:700;padding:2px 7px;border-radius:99px;white-space:nowrap}
.e1{background:#DCFCE7;color:#166534}.e2{background:#FEF3C7;color:#92400E}
.tiertag{font-size:8px;font-weight:700;color:#fff;padding:1px 6px;border-radius:3px}
.retain{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:10px}
.retain .r img{width:100%;border:1px solid #CBD5E1;border-radius:4px;display:block;margin-bottom:7px}
.retain .r h4{font-size:11px;color:#15233D;margin-bottom:3px}
.retain .r p{font-size:9.5px;color:#475569}
.steps{counter-reset:s}
.steps li{list-style:none;display:flex;gap:9px;margin-bottom:9px;font-size:10.5px;color:#334155}
.steps li::before{counter-increment:s;content:counter(s);background:#15233D;color:#fff;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;flex:0 0 auto}
.steps li b{color:#15233D}
"""

def page(inner, foot_l, foot_r, cls=""):
    return f"<section class='page {cls}'>{inner}<div class='pf'><span>{foot_l}</span><span>{foot_r}</span></div></section>"

def head(t, n):
    return f"<div class='ph'><span class='t'>{t}</span><span class='n'>{n}</span></div>"

FOOT = "MahaPAR · Observations on the SPARROW APAR dashboards · IDinsight with GAD · Draft for discussion"

html = [f"<!DOCTYPE html><html><head><meta charset='utf-8'>",
 "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' rel='stylesheet'>",
 f"<style>{CSS}</style></head><body>"]

# ---- cover
html.append(f"""<section class='page cover'>
<div><span class='eyebrow'>Government of Maharashtra · General Administration Department</span>
<h1>Suggested refinements to the APAR dashboards developed by NIC</h1>
<h2>Nineteen observations from a walkthrough of the SPARROW APAR screens, each framed as a
low-effort refinement that works within the existing design, and each referenced to the screen on which it was observed.</h2></div>
<div><span class='draft'>Draft for discussion</span>
<div class='meta' style='margin-top:14px'>
<div><b>Prepared for</b>General Administration Department,<br>and thereafter for NIC</div>
<div><b>Prepared by</b>IDinsight</div>
<div><b>Basis</b>19 screens recorded from the<br>SPARROW APAR application, October 2026</div>
<div><b>Date</b>October 2026</div>
</div></div></section>""")

# ---- how to read
html.append(page(head("Purpose and approach","Page 2") + """
<h3 class='sec'>What this note is, and what it is not</h3>
<p class='lead'>NIC has built a working APAR dashboard suite covering the officer's own window, service and instance level
monitoring, departmental reports and workflow creation. The structure is sound and a good deal of the detail is well judged.
This note does not propose a redesign. It records nineteen points noticed during a walkthrough of the screens, each of which
can be addressed by changing what is written on the screen, the order in which elements appear, or what is shown when data is
still awaited.</p>
<div class='cols3'>
<div class='box accent'><h4>Within the present design</h4><p>Every suggestion keeps NIC's existing layout, colour scheme and
components. Nothing here calls for a new screen, a new report or a change to the underlying data model. Where a suggestion
needs more than a change of wording or order, this is stated plainly on the page.</p></div>
<div class='box accent'><h4>Referenced to the screen</h4><p>Each page carries the screen on which the point was observed, so
that NIC can locate it directly. The right-hand side shows the suggested form of the same element, drawn in NIC's own
visual style.</p></div>
<div class='box accent'><h4>Effort is our reading, not an estimate</h4><p>The effort noted against each suggestion is
IDinsight's assessment from the screens alone. NIC is best placed to confirm it, and we would welcome correction where our
reading of the effort involved is mistaken.</p></div>
</div>
<h3 class='sec' style='margin-top:14px'>How the suggestions are grouped</h3>
<div class='cols2'>
<div class='box'><h4>A · Clarity of information for decision-makers <span class='tiertag' style='background:#B45309'>5 points</span></h4>
<p>Points where the figures on screen are sound but the labels, headings or notes accompanying them could be read differently
from what is intended.</p></div>
<div class='box'><h4>B · Navigation and ease of use <span class='tiertag' style='background:#1D4ED8'>6 points</span></h4>
<p>Points where information already held by the system takes more steps to reach than it might.</p></div>
<div class='box'><h4>C · Clarity when data is awaited <span class='tiertag' style='background:#0F766E'>4 points</span></h4>
<p>Points where a screen shows a blank value or an empty table without indicating whether the position is pending, not
applicable, or awaiting a selection by the user.</p></div>
<div class='box'><h4>D and E · The officer's window, and workflow creation <span class='tiertag' style='background:#7C3AED'>4 points</span></h4>
<p>Points specific to the window an officer sees for their own APAR, and to the screens on which the custodian creates the
APAR workflow.</p></div>
</div>""", FOOT, "2"))

# ---- summary
rows = []
for r in RECS:
    t, c = TIERS[r["tier"]]
    e1 = "e1" if r["eff"].lower().startswith(("very low","low —","low -")) else "e2"
    eff_short = "Very low" if r["eff"].lower().startswith("very low") else ("Low" if r["eff"].lower().startswith("low") else "Low–moderate")
    rows.append(f"<tr><td class='n'>{r['id']}</td><td><span class='tiertag' style='background:{c}'>{r['tier']}</span></td>"
                f"<td>{r['title']}</td><td><span class='effpill {e1}'>{eff_short}</span></td></tr>")
html.append(page(head("Summary of suggestions","Page 3") + f"""
<h3 class='sec'>The nineteen suggestions at a glance</h3>
<p class='lead'>Ordered by group. The effort rating is IDinsight's reading of the screens and is offered for NIC to confirm or correct.</p>
<table class='sum'><tr><th></th><th>Group</th><th>Suggestion</th><th>Indicative effort</th></tr>{''.join(rows)}</table>
<div class='notebox' style='margin-top:10px'><b>A note on sequencing.</b> Suggestions 17 and 2 — the spelling corrections and the
wording of the performance labels — cost very little and are the points most readily noticed when the system is demonstrated.
They may be worth taking up first. Suggestions 4, 9 and 16 would, in our assessment, make the greatest practical difference to
the monitoring authorities, and would merit discussion with NIC on sequencing.</div>""", FOOT, "3"))

# ---- recommendation pages
pg = 4
for r in RECS:
    tname, tcol = TIERS[r["tier"]]
    html.append(page(
        head(f"Group {r['tier']} · {tname}", f"Suggestion {r['id']} of 19") + f"""
<div class='rec'>
  <div class='rectitle'><span class='num'>{r['id']}</span><div><h2>{r['title']}</h2></div></div>
  <div class='lbl'>As presently displayed in SPARROW</div>
  <div class='shotfull'><img src='{r["shot"]}'></div>
  <div class='recbody'>
    <div class='side'>
      <div class='lbl'>What we observed</div>
      <div class='obs' style='margin-bottom:9px'>{r['obs']}</div>
      <div class='lbl'>Suggested refinement</div>
      <div class='sug'>{r['sug']}</div>
      <div class='eff'><span class='pill'>Effort</span><span>{r['eff']}</span></div>
    </div>
    <div class='side'>
      <div class='lbl'>Indicative form of the suggestion</div>
      <div class='mockbox'>{r['mock']}</div>
      <div class='why'><b>Why it helps.</b> {r['why']}</div>
    </div>
  </div>
</div>""", FOOT, str(pg)))
    pg += 1

# ---- retain page
rcards = "".join(f"<div class='r'><img src='{s}'><h4>{t}</h4><p>{d}</p></div>" for t, d, s in RETAIN)
html.append(page(head("Features we would suggest retaining", f"Page {pg}") + f"""
<h3 class='sec'>Three features that work well and should be carried forward</h3>
<p class='lead'>We note these explicitly so that they are not altered in the course of taking up the suggestions in this note.
Each addresses a need that GAD has raised, and each is already built.</p>
<div class='retain'>{rcards}</div>""", FOOT, str(pg)))
pg += 1

# ---- next steps
html.append(page(head("Suggested next steps", f"Page {pg}") + """
<h3 class='sec'>How we would suggest taking this forward</h3>
<p class='lead'>The suggestions in this note are offered for GAD's consideration in the first instance, and thereafter for
discussion with NIC. We have grouped them so that a decision can be taken on each group rather than on all nineteen at once.</p>
<div class='cols2'>
<div>
<ol class='steps'>
<li><b>GAD's view on the list.</b> Confirm which suggestions GAD wishes to take up, and whether any further points should be
added from the department's own experience of the system.</li>
<li><b>Confirm the two rules that need a departmental decision.</b> Suggestion 3 requires GAD to confirm the DPC eligibility
threshold the report should apply. Suggestion 14 requires the refresh interval beyond which dashboard figures should be
flagged as dated.</li>
<li><b>Discussion with NIC on effort and sequence.</b> NIC to confirm or correct the indicative effort against each
suggestion, and to advise which can be taken up in the current release.</li>
<li><b>A short first set.</b> We would suggest the wording and ordering changes be taken up together as a first set, as they
require no change to data or queries.</li>
<li><b>Review after the first set is deployed.</b> A walkthrough with GAD and NIC once the first set is live, before taking a
view on the remainder.</li>
</ol>
</div>
<div>
<div class='box accent'><h4>Two points for GAD's decision</h4>
<p><b>DPC eligibility threshold.</b> The report's note and its computation presently state different thresholds. The correct
rule is a departmental matter rather than a technical one, and NIC will need it confirmed before the note can be
corrected.</p>
<p style='margin-top:7px'><b>Refresh interval for the dashboards.</b> Suggestion 14 proposes that figures be flagged once they
exceed an agreed age. That interval is for GAD to set, having regard to how the dashboards are used in review meetings.</p>
</div>
<div class='box' style='margin-top:12px'><h4>What this note does not cover</h4>
<p>The observations here are confined to the dashboard and report screens recorded in October 2026. They do not extend to the
APAR forms themselves, to the officer's filing experience, or to the data held in the source systems, each of which is being
taken up separately.</p></div>
<div class='box' style='margin-top:12px'><h4>Acknowledgement</h4>
<p>The screens reviewed represent a substantial body of work covering officer, service, instance and departmental levels,
together with workflow creation and a set of departmental reports. The suggestions in this note are offered in that
context.</p></div>
</div>
</div>""", FOOT, str(pg)))

html.append("</body></html>")
open(OUT, "w").write("\n".join(html))
print("wrote", OUT, "pages:", pg)
