#!/usr/bin/env python3
"""
Builds the APAR roles and responsibilities annexure (content only, no GR
header, signature block or distribution list).

Content follows Form A v4.1 and Form B v3 wherever the older stakeholder
draft differs; the differences are listed on the last page for GAD.
"""
import subprocess, os

OUT = "/home/user/personal_v1/MahaPAR_APAR_roles_and_responsibilities.pdf"
HTMLOUT = "/home/user/personal_v1/MahaPAR_APAR_roles_and_responsibilities.html"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# role: (title, one-line scope, [(responsibility, form ref, by when, how in MahaPAR)])
CHAIN = [
 ("Official reported upon",
  "Every Group A and Group B official for whom an APAR is generated.",
  [("<b>Keep a work log through the year.</b> Record noteworthy tasks and activities as they happen.",
    "2.2", "Through the year",
    "The work log is open all year in MahaPAR and the eHRMS app. Entries can be pulled into the self-appraisal (2.2) when the cycle opens, so the official is not writing the year from memory in May."),
   ("<b>Respond to any memo issued to you by the reporting officer.</b>", "", "Within the date given in the memo",
    "Memos are issued and answered in eHRMS through the year. The reply is recorded against the memo itself and is shown to the reporting officer at grading, along with whether the memo was answered."),
   ("<b>Check Part 1 and the reporting chain mapped for you</b>, and ask for a correction where it is wrong.", "Part 1, 1.1, 1.2", "15 April",
    "Details come from Sevaarth and the service record. The chain is shown as a row for each period and is mapped by the custodian. <b>Request a correction</b> sends an error to the custodian. Where eHRMS is not yet live, leave or absence of 30 days or more is entered by the official. Any No Report Certificate raised for a period of less than three months is shown here for checking."),
   ("<b>Fill and submit the self-appraisal.</b>", "Part 2", "15 May",
    "The whole of Part 2 on one page: key activities and targets with achievements (2.1), the most significant contribution (2.2), any systemic factors (2.3), trainings completed (2.4), up to three training areas needed (2.5), and the technical cadre module where applicable (2.6). Signed with DSC or eSign."),
   ("<b>Read the disclosed APAR and submit a representation if any.</b>", "Part 6", "Within 15 days of disclosure",
    "The outcome opens in MahaPAR with one representation box. The memos issued during the year and the replies are attached automatically.")]),

 ("Reporting officer",
  "The officer under whom the official served for three months or more in the year.",
  [("<b>Issue a memo during the year where an official mapped to you needs to improve.</b>", "", "Through the year, as the concern arises",
    "Memos are raised in eHRMS, where the reporting chain is maintained, and can be issued on any day of the year. A memo cannot be back-dated, so a concern recorded only at grading time attaches to the next cycle, not to the year being assessed. MahaPAR reads the memos at grading."),
   ("<b>Complete the assessment of each official mapped to you.</b> This covers: grading the six dimensions, and the technical module where the official is in a technical cadre; justifying any grade of 1 to 2 or 9 to 10; attaching memos where the overall grade is below the benchmark; recording integrity; writing the overall assessment; stating agreement with the self-appraisal; and confirming or changing the training nominations.",
    "Part 3", "15 June",
    "The whole of Part 2 opens above the grading table, so the self-appraisal, the targets and the training requested are read before grading. Annexure 3 explains what each dimension looks like in a desk post and in a field post. System data on iGOT hours, eOffice use and attendance is shown for reference and is not weighted. The justification box opens automatically for a grade of 1 to 2 or 9 to 10, and the stage cannot be signed until it is filled; memos issued during the year are shown against the dimension they relate to, with whether the official answered them, and can be cited there. Where the overall grade is below 6, the memo record for the year and the replies can be attached with one click. Doubtful integrity requires reasons in a separate confidential note. Under training nominations the officer agrees with or changes what the official asked for in 2.5 and may recommend up to three trainings, each marked domain, functional or behavioural.")]),

 ("Reviewing officer",
  "The officer immediately senior to the reporting officer in the mapped chain.",
  [("<b>Complete the review of each APAR that comes to you.</b> Agree with the reporting officer&rsquo;s overall grade, or record your own overall grade with the reason.",
    "Part 4", "15 July",
    "Agreeing takes two clicks. Dimension-wise grades are not revised. Where you differ, your grade replaces the reporting officer&rsquo;s overall grade, and a grade of 1 to 2 or 9 to 10 needs the specific accomplishment or failure behind it.")]),

 ("Accepting authority (only if GAD adds this stage)",
  "Maharashtra's current forms have no accepting stage. If GAD adds one, it acts only where a stage was never completed; it is not an appellate stage and does not revise grades.",
  [("<b>Record which stage is missing and the action taken</b>, so that the APAR is not left incomplete.", "Part 5", "31 July",
    "The stage opens only where MahaPAR auto-forwarded a stage that was never recorded.")]),
]

ADMIN = [
 ("Custodian (establishment officer)",
  "Responsible for APAR data of one office (organisation unit).",
  [("Open the cycle for the year and notify the dates set by GAD.", "", "1 April",
    "<b>Initiate cycle and complete authority mapping</b>. Past cycles can be viewed and exported from the same place."),
   ("Map each official's tenures and reporting and reviewing officers for the year, and verify Part 1.", "Part 1, 1.1", "30 April",
    "Selected from drop-down lists. Once office orders are digitised and linked to eHRMS this will be pre-filled and the custodian will only validate or correct it."),
   ("Verify and issue No Report Certificates.", "1.2", "30 April",
    "MahaPAR raises the NRC from the mapped period; the custodian verifies the period and signs."),
   ("Act on correction requests raised by officials on Part 1 and the chain.", "Part 1, 1.1", "30 April",
    "Requests appear in the mapping screen against the official who raised them."),
   ("Track what is pending across the cycle and follow it up.", "", "Throughout the cycle",
    "<b>Track what is pending across APAR cycle</b> shows the count at each stage. <b>Facilitate APAR cycle</b> carries two actions: send bulk reminders to all pendencies, or open an individual pendency and follow it up."),
   ("Track memos issued in the office and remind officials who have not answered one.", "", "Throughout the cycle",
    "The memo tracking section lists officials with unanswered memos and sends them a reminder. The custodian does not read the memo content."),
   ("Disclose the completed APAR to the official and record any representation.", "Part 6", "After the reviewing stage",
    "Disclosure is a custodian action in MahaPAR. The 15-day representation window runs from the date of disclosure."),
   ("Supply APARs to the Departmental Promotion Committee.", "", "On requisition",
    "Closed APARs are exported from the register for the cadre and period asked for."),
   ("Close the cycle on the date notified by GAD.", "", "31 December",
    "No entries are accepted after the cycle closes. Closed cycles stay available for viewing and export.")]),

 ("Cadre Monitoring Authority, point of contact",
  "One cadre across all offices, for example Assistant Police Inspector.",
  [("Watch how the cadre is progressing through the cycle and see which APARs are generated, closed or pending.", "", "Throughout the cycle",
    "<b>View Cadre Report</b>, with the count at each stage for the whole cadre."),
   ("Open an individual official's details and past APARs where a case needs to be examined.", "", "As required",
    "From the cadre report, an official's record and closed APARs can be opened directly."),
   ("Take up offices in the cadre where pendency is not moving, with the custodians concerned.", "", "After the custodian's own follow-up",
    "Reminders to officials are sent by the custodian. The Cadre Monitoring Authority follows up with the custodian, not with the official.")]),

 ("Sub Department Monitoring Authority, point of contact",
  "One whole sub department, for example MH-POLICE.",
  [("Watch how each office and each cadre of the sub department is doing.", "", "Throughout the cycle",
    "<b>Overall Service</b> for the sub department as a whole, <b>OU Wise</b> for each office and <b>Individual Officers</b> for a single record."),
   ("Follow up on pending APARs in the sub department, office by office.", "", "Throughout the cycle",
    "OU Wise ranks offices by pendency, so the offices needing attention first are visible without a search."),
   ("Report to GAD on offices where pendency continues after follow-up.", "", "Monthly during the cycle",
    "The sub department register can be exported for reporting.")]),

 ("General Administration Department (state administrator)",
  "The state-level view of every department, service, cadre and office.",
  [("Notify the cycle dates each year.", "", "Before 1 April", "Set centrally for all departments."),
   ("Configure pre-filling, automatic forwarding, grade calculation and the timeliness marks.", "Part 6", "Before 1 April",
    "Part 6 is generated by MahaPAR; no officer enters it."),
   ("Monitor pendency across the state and identify where action is needed first.", "", "Throughout the cycle",
    "Department, service, cadre and office wise reports, with stage deadlines tracked in one place."),
   ]),
]

ESCALATION = [
 ("Official does not confirm Part 1 by 15 April", "The custodian completes the mapping from the service record."),
 ("Official does not submit the self-appraisal by 15 May", "The reporting officer assesses on the available record."),
 ("Reporting officer does not complete the stage by 15 June", "MahaPAR forwards the APAR and the reviewing officer completes the assessment."),
 ("Reviewing officer does not complete the stage by 15 July", "The reporting officer's assessment becomes final."),
 ("A stage is never completed at all", "Where GAD adds an accepting stage, the accepting authority records the missing stage and the action taken (Part 5)."),
 ("Pendency in an office is not moving", "Custodian sends reminders, then the Cadre Monitoring Authority takes it up with the custodian, then the Sub Department Monitoring Authority, then GAD."),
]

TIMELINE = [("31 March", "Reporting year ends"), ("1 April", "Cycle opens"),
            ("15 April", "Official confirms Part 1"), ("30 April", "Custodian verifies Part 1 and the mapping"),
            ("15 May", "Self-appraisal"), ("15 June", "Reporting officer"),
            ("15 July", "Reviewing officer"), ("31 July", "Accepting authority, if GAD adds this stage and a stage is missing"),
            ("31 December", "Cycle closes")]

OPEN = [
 ("The reporting chain is now mapped by the custodian",
  "The earlier draft had the official enter the reporting and reviewing officers for the custodian to verify. Form A v4.1 places the mapping with the custodian and leaves the official a correction request. The responsibility has moved between two roles, so the resolution should say so plainly."),
 ("The reviewing officer works on the overall grade only",
  "The earlier draft allowed the reviewing officer to revise individual dimensions, with MahaPAR recalculating. Form A v4.1 asks only about the overall grade and states that dimension-wise grades are not revised."),
 ("The accepting authority is not an appellate stage",
  "The accepting stage is optional and Maharashtra's current forms have none. If GAD adds it, the earlier draft let it record a revised overall grade, while Form A v4.1 opens Part 5 only where the reporting or reviewing stage is missing and asks only which stage is missing and what action was taken. The second is followed here."),
 ("Form references have shifted",
  "In Form A v4.1 grading is 3.1, integrity 3.2, the overall assessment 3.3, agreement with the self-appraisal 3.4 and training nominations 3.5. The technical cadre question is 2.6, with four modules, T1 to T4."),
 ("Deadlines",
  "The dates above are the ones proposed in the stakeholder draft, modelled on Gujarat's cycle, which gives each stage about 30 days. The digital walkthrough currently shows 31 May for the reporting stage. One of the two needs to be corrected once GAD confirms the dates."),
 ("New roles need to be nominated",
  "The Cadre Monitoring Authority and Sub Department Monitoring Authority points of contact do not exist today. The resolution should require each department to nominate them and intimate GAD within a stated period."),
]


def rows(items):
    out = []
    for n, (r, ref, when, how) in enumerate(items, 1):
        out.append(f"<tr><td>{r}</td><td class='c'>{ref or '&ndash;'}</td>"
                   f"<td class='c'>{when or '&ndash;'}</td><td>{how or '&ndash;'}</td></tr>")
    return "".join(out)


def block(title, scope, items):
    n = len(items)
    return f"""<div class="role">
  <h3>{title}</h3><p class="scope">{scope}</p>
  <p class="count">{n} action{"s" if n != 1 else ""}</p>
  <table><tr><th style="width:28%">Responsibility</th><th style="width:8%">Form</th>
  <th style="width:14%">By when</th><th>How it is done in MahaPAR</th></tr>{rows(items)}</table></div>"""


HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>APAR roles and responsibilities</title>
<style>
@page{{size:A4 portrait;margin:16mm 12mm}}
*{{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:'Times New Roman',Georgia,serif;color:#000;font-size:13px;margin:0;line-height:1.5}}
h1{{font-size:21px;margin:0 0 6px;text-align:center}}
.sub{{font-size:12px;margin:0 0 16px;text-align:center}}
h2{{font-size:16px;margin:26px 0 10px;border-bottom:1.5px solid #000;padding-bottom:4px}}
h3{{font-size:14px;margin:0 0 2px}}
.scope{{font-size:12.5px;margin:0 0 3px;font-style:italic}}
.count{{font-size:12.5px;margin:0 0 8px;font-weight:700}}
.role{{margin-bottom:20px}}
table{{width:100%;border-collapse:collapse;margin-bottom:4px}}
th{{background:#E8E8E8;color:#000;text-align:left;font-weight:700;font-size:12.5px;padding:6px 8px;border:1px solid #000}}
td{{border:1px solid #000;padding:6px 8px;vertical-align:top;font-size:12.5px}}
td.c{{white-space:nowrap}}
.lead{{border:1px solid #000;padding:10px 12px;margin-bottom:18px}}
.lead p{{margin:0 0 7px}} .lead p:last-child{{margin:0}}
ol{{margin:6px 0 0 20px;padding:0}} li{{margin-bottom:10px}}
.note{{font-size:12.5px;margin:6px 0 0}}
.pb{{break-before:page}}
</style></head><body>

<h1>APAR under MahaPAR: who does what, by when, and how</h1>
<p class="sub">Draft for discussion with GAD | IDinsight | Based on Form A, for Group A and Group B officials, current draft</p>

<div class="lead">
  <p>The APAR covers the financial year just ended, 1 April to 31 March, and the cycle opens on the following 1 April. The APAR for 2025-26 opens on 1 April 2026.</p>
  <p>Every part is filed in MahaPAR and signed with a digital signature or eSign. Paper forms are not accepted.</p>
  <p>If a stage is not completed by its date, MahaPAR forwards the APAR to the next stage, records the delay, and deducts timeliness marks from the APAR of the official who held it. These marks are 5 per cent of the final score, that is &minus;0.5 to +0.5 on the 10-point scale, and they sit in Part 6, which MahaPAR generates on its own. Timeliness is counted for every role an official holds in the cycle: their own self-appraisal, their assessments as a reporting officer, and their reviews as a reviewing officer.</p>
</div>

<h2>A. The cycle at a glance</h2>
<table>{''.join(f"<tr><td class='c' style='width:22%'><b>{d}</b></td><td>{e}</td></tr>" for d, e in TIMELINE)}</table>
<p class="note"><b>Note on the dates.</b> The dates shown are the ones proposed in the stakeholder draft, modelled on Gujarat&rsquo;s cycle, which gives each stage about 30 days. They will be finalised in consultation with GAD.</p>
<p class="note">After the reviewing stage the completed APAR is disclosed to the official by the custodian. The official may submit one representation within 15 days of disclosure. No entries are accepted after the cycle closes.</p>

<div class="pb"></div>
<h2>B. Officers in the APAR chain</h2>
{''.join(block(*r) for r in CHAIN)}

<div class="pb"></div>
<h2>C. Administrative and monitoring roles</h2>
{''.join(block(*r) for r in ADMIN)}

<div class="pb"></div>
<h2>D. What happens if a stage is not completed</h2>
<table><tr><th style="width:40%">Situation</th><th>What happens next</th></tr>
{''.join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in ESCALATION)}</table>
<p class="note">Follow-up runs upward: official, custodian, Cadre Monitoring Authority, Sub Department Monitoring Authority, GAD. Reminders to an official are sent by the custodian. Each level above follows up with the level below it, not with the official.</p>

</body></html>"""

open(HTMLOUT, "w").write(HTML)
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--virtual-time-budget=6000", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT}", HTMLOUT], check=True, capture_output=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
