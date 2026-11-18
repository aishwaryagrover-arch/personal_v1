#!/usr/bin/env python3
"""
Build walkthrough v6 from v5, applying ACS (GAD) feedback.

Every change is marked in place with one of two flags:
  .note.add   "Added in this version"      — what changed
  .note.disc  "Needs discussion"           — one or two lines, no more

Changes: self-authority mapping, memo reframed as feedback for growth,
upward feedback (2.6), departmental enquiry record, broadened NRC rule,
departmental KRAs shown while grading.
"""
import os
import sys

SRC = "/home/user/personal_v1/MahaPAR_APAR_portal_walkthrough_v5.html"
DST = "/home/user/personal_v1/MahaPAR_APAR_portal_walkthrough_v6.html"

s = open(SRC, encoding="utf-8").read()
n = 0


def rep(old, new, count=1):
    """Exact replacement; fails loudly if the anchor moved."""
    global s, n
    found = s.count(old)
    if found != count:
        sys.exit("ANCHOR x%d (expected %d): %r" % (found, count, old[:110]))
    s = s.replace(old, new)
    n += 1


# ══════════════════════════════════════════════ 0 · flag styles
rep("buildScales();renderChips();renderRoChips();renderMemos();renderCycle();renderLog();fillModules();setTech(0);renderLnd();",
    "buildScales();renderChips();renderRoChips();renderMemos();renderCycle();renderLog();fillModules();setTech(0);renderLnd();renderUp();")

rep(".note b{font-weight:700}",
    """.note b{font-weight:700}
.note.add{background:#ECFDF5;color:#065F46;border-left:4px solid #10B981}
.note.disc{background:#F5F3FF;color:#5B21B6;border-left:4px solid #8B5CF6}
.ftag.add{background:#D1FAE5;color:#065F46}
.ftag.disc{background:#EDE9FE;color:#5B21B6}
.upm{display:inline-block;min-width:30px;text-align:center;padding:5px 8px;margin-right:5px;
     border:1px solid var(--border);border-radius:6px;font-size:12.5px;cursor:pointer;
     background:#fff;color:var(--muted);user-select:none}
.upm:hover{border-color:var(--navy);color:var(--navy)}
.upm.on{background:var(--navy);border-color:var(--navy);color:#fff;font-weight:700}
.upm.na{min-width:40px;font-size:11.5px}""")

ADD = '<div class="note add">&#10133; <b>Newly added / changed:</b> '
DISC = '<div class="note disc">&#128310; <b>Needs discussion:</b> '

# ══════════════════════════════════════════════ 1 · four stat tiles on one row
rep(".g-3{grid-template-columns:repeat(3,minmax(0,1fr))}",
    ".g-3{grid-template-columns:repeat(3,minmax(0,1fr))}\n"
    ".g-4{grid-template-columns:repeat(4,minmax(0,1fr))}")
rep('@media(max-width:1080px){.g-2-1,.g-1-2,.g-3{grid-template-columns:1fr}}',
    '@media(max-width:1080px){.g-2-1,.g-1-2,.g-3,.g-4{grid-template-columns:1fr}}')
rep('<div class="grid g-3" style="margin-bottom:18px">',
    '<div class="grid g-4" style="margin-bottom:18px">')

# ══════════════════════════════════════════════ 2 · self pane intro + step list
rep("Four sections. Part 1 is already filled in and your reporting chain is mapped by the custodian. "
    "Check them, then complete Part 2 and sign.",
    "Four sections. Part 1 is already filled in. You map your own reporting and reviewing authority "
    "for the year and the custodian validates it, then you complete Part 2 and sign.")

rep('<li onclick="selfStep(2)"><span class="n">2</span><div>Your reporting chain<small>Mapped by the custodian</small></div></li>',
    '<li onclick="selfStep(2)"><span class="n">2</span><div>Create your PAR workflow<small>Map your authorities &middot; custodian validates</small></div></li>')

rep('<li onclick="selfStep(7)"><span class="n">&#9679;</span><div>Memos received<small>2 &middot; 1 awaiting your reply</small></div></li>'
    .replace("&middot;", "·"),
    '<li onclick="selfStep(7)"><span class="n">&#9679;</span><div>Memos received<small>2 · 1 awaiting your reply</small></div></li>')

# ══════════════════════════════════════════════ 3 · step 2 → create your PAR workflow
OLD_STEP2_START = '          <div class="part">Part 1.1 · your reporting chain</div>\n'
OLD_STEP2_END = '          <div class="btnrow" style="margin-top:12px"><button class="btn grey" onclick="selfStep(1)">Back</button><button class="btn" onclick="selfStep(3)">Continue</button></div>\n'
i0 = s.index(OLD_STEP2_START)
i1 = s.index(OLD_STEP2_END) + len(OLD_STEP2_END)

OFFICERS = ('<option>Select officer</option>'
            '<option>Shri C. D. Joshi — Deputy Secretary</option>'
            '<option>Shri R. S. Gokhale — Deputy Secretary</option>'
            '<option>Shri E. F. Rane — Joint Secretary</option>'
            '<option>Smt. S. V. Deshmukh — Joint Secretary</option>'
            '<option>No authority was in position for this period</option>')

NEW_STEP2 = f'''          <div class="part">Part 1.1 · create your PAR workflow <span class="ftag add">Newly added / changed</span></div>
          {ADD}you now record your own reporting and reviewing authority for the year. It goes to the custodian, who validates it or issues a correction. <b>This process is yet to be finalised.</b></div>
          <div class="sub">Assessment year 2025&ndash;26 · 01 Apr 2025 to 31 Mar 2026 · 365 days · Shri A. B. Sawant, Section Officer</div>

          <div class="q" style="margin-top:14px">1 · Who was your reporting authority?</div>
          <div class="hint">Pick each officer and the dates they served. Add as many as you had during the year. APAR and NRC periods are worked out from the tenures you record.</div>
          <table id="mapRepTable">
            <tr><th style="width:52%">Officer</th><th>From</th><th>To</th><th></th></tr>
            <tr><td><select>{OFFICERS}</select></td>
                <td><input type="date" value="2025-04-01"></td>
                <td><input type="date" value="2026-03-31"></td>
                <td><button class="btn sm ghost" onclick="toast('Dates set to the full assessment year.')">Full year</button></td></tr>
          </table>
          <div class="btnrow" style="margin-top:8px"><button class="btn ghost sm" onclick="addTenure('mapRepTable')">+ Add another officer / tenure</button></div>

          <div class="q" style="margin-top:16px">2 · Who was your reviewing authority?</div>
          <div class="hint">The same, for the officer who reviewed the assessment made on you.</div>
          <table id="mapRevTable">
            <tr><th style="width:52%">Officer</th><th>From</th><th>To</th><th></th></tr>
            <tr><td><select>{OFFICERS}</select></td>
                <td><input type="date" value="2025-04-01"></td>
                <td><input type="date" value="2026-03-31"></td>
                <td><button class="btn sm ghost" onclick="toast('Dates set to the full assessment year.')">Full year</button></td></tr>
          </table>
          <div class="btnrow" style="margin-top:8px"><button class="btn ghost sm" onclick="addTenure('mapRevTable')">+ Add another officer / tenure</button></div>

          <div class="note info" style="margin-top:14px">ℹ️ <b>Where an authority was not in position,</b> select that in the drop-down rather than leaving the row out. MahaPAR issues a <b>No Report Certificate</b> for a period where you served under the reporting officer for <b>3 months or less</b>, or where <b>neither a reporting nor a reviewing authority</b> was in position. Where a reviewing authority alone is missing, an <b>accepting authority</b> is assigned instead and no NRC arises.</div>
          <div class="btnrow"><button class="btn" onclick="submitMapping()">Submit for the custodian to validate</button><button class="btn ghost" onclick="toast('Draft saved. Nothing has gone to the custodian.')">Save draft</button></div>

          <div class="hidebox" id="mapDone" style="margin-top:16px">
            <div class="rule"></div>
            <div class="part">Your PAR workflow <span class="tag warn" id="mapStatus">Submitted · awaiting custodian validation</span></div>
            <div class="hint">You cannot change it while it is with the custodian. If the custodian corrects it, you are notified and the corrected record is shown here.</div>
            <table>
              <tr><th>Role</th><th>Name and post</th><th>From</th><th>To</th></tr>
              <tr><td>Reporting authority</td><td>Shri C. D. Joshi — Deputy Secretary</td><td>01/04/2025</td><td>31/03/2026</td></tr>
              <tr><td>Reviewing authority</td><td>Shri E. F. Rane — Joint Secretary</td><td>01/04/2025</td><td>31/03/2026</td></tr>
              <tr><td>Accepting authority</td><td>Not applicable</td><td colspan="2" style="color:var(--muted);font-size:12px">Assigned only where no reviewing authority was in position</td></tr>
            </table>
            <div class="btnrow"><button class="btn ghost" onclick="show('reqBox',1)">Raise a request for a change</button></div>
            <div class="hidebox" id="reqBox" style="margin-top:12px">
              <div class="rule"></div>
              <div class="q">What needs correcting?</div>
              <div class="hint">Your request goes to the custodian, Shri G. H. Mane.</div>
              <label class="f"><span>What is not correct</span>
                <select><option>Reporting authority is not correct</option><option>Reviewing authority is not correct</option><option>The dates are not correct</option><option>A period is missing</option><option>Other</option></select></label>
              <textarea id="tReq" oninput="wc('tReq','cReq',100)" placeholder="State what the record should say. Maximum 100 words."></textarea>
              <div class="counter" id="cReq">0 / 100 words</div>
              <div class="btnrow"><button class="btn" onclick="toast('Request sent to the custodian. You will be notified when it is acted on.');show('reqBox',0)">Send request</button><button class="btn grey" onclick="show('reqBox',0)">Cancel</button></div>
            </div>
          </div>
          <div class="btnrow" style="margin-top:12px"><button class="btn grey" onclick="selfStep(1)">Back</button><button class="btn" onclick="selfStep(3)">Continue</button></div>
'''
s = s[:i0] + NEW_STEP2 + s[i1:]
n += 1

# ══════════════════════════════════════════════ 4 · 2.1 · departmental KRA direction
rep('<div class="note info">&#8505;&#65039; <b>Future direction:</b> role and KRA information pre-filled '
    'where available once role mapping for priority departments is complete; targets selected from a '
    'drop-down once KPIs are linked to MahaPAR.</div>',
    '<div class="note info">&#8505;&#65039; <b>Future direction:</b> role and KRA information pre-filled '
    'where available once role mapping for priority departments is complete; targets selected from a '
    'drop-down once KPIs are linked to MahaPAR.</div>\n            '
    + DISC + 'how far departments have completed the KRA-defining exercise, and how those departmental '
    'KRAs flow into this table.</div>')

# ══════════════════════════════════════════════ 5 · Part 2.6 · feedback for the reporting officer
rep('        <div class="btnrow" style="margin-top:-4px;margin-bottom:18px">'
    '<button class="btn grey" onclick="selfStep(2)">Back</button>'
    '<button class="btn" onclick="selfStep(4)">Continue to review and sign</button></div>',
    f'''        <div class="card">
          <div class="part">Part 2.7 · optional · confidential <span class="ftag add">Newly added / changed</span></div>
          {ADD}feedback on your reporting officer across five areas, with an optional note. No part of it is graded. <b>Work in progress:</b> this question is not final &mdash; the areas, the rating scale and the wording are to be revised based on the state study and insights from other states.</div>
          <div class="q">Feedback for your reporting officer</div>
          <div class="hint" style="margin-bottom:8px">Is there any feedback for your reporting officer that would help you in your work next year?</div>
          <div class="hint">Rate each area from 1 to 5, where <b>1 is needs attention</b> and <b>5 is consistently strong</b>. Mark <b>N/A</b> where you have no basis to judge.</div>
          <table id="upTable"></table>
          <div class="q" style="margin-top:16px">Anything you would like to add?</div>
          <div class="hint">Keep it about your reporting officer and about the work. Maximum 50 words.</div>
          <textarea id="t26" oninput="wc('t26','c26',50)" placeholder="Optional. Maximum 50 words." style="min-height:90px"></textarea>
          <div class="counter" id="c26"></div>
          <div class="note info">&#8505;&#65039; Responses to a reporting officer are <b>pooled across everyone who reports to them and shared anonymously</b>. They are not graded, are not seen by the reviewing officer, and form no part of the APAR record.</div>
          {DISC}what safeguards, beyond pooling and anonymity, will ensure that sharing feedback carries no consequence for the official &mdash; and at what point the pooled feedback should reach the reporting officer. One option is to release it only after that officer has submitted every assessment for the cycle.</div>
        </div>

        <div class="btnrow" style="margin-top:-4px;margin-bottom:18px"><button class="btn grey" onclick="selfStep(2)">Back</button><button class="btn" onclick="selfStep(4)">Continue to review and sign</button></div>''')

rep('<tr onclick="selfStep(3)" style="cursor:pointer"><td>2.5 Training needed</td><td><span class="tag grey">Optional</span></td></tr>',
    '<tr onclick="selfStep(3)" style="cursor:pointer"><td>2.5 Training needed</td><td><span class="tag grey">Optional</span></td></tr>\n'
    '            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.7 Feedback for your reporting officer</td><td><span class="tag grey" id="chk26">Optional</span></td></tr>')

rep('<tr onclick="selfStep(2)" style="cursor:pointer"><td>Part 1.1–1.2 · reporting chain and NRC</td><td><span class="tag ok">Complete</span></td></tr>',
    '<tr onclick="selfStep(2)" style="cursor:pointer"><td>Part 1.1–1.2 · PAR workflow and NRC</td><td><span class="tag ok">Submitted for validation</span></td></tr>')

rep('<tr><td>Memos issued to you this year</td><td><span class="tag warn" id="chkMemo">2 · 1 unanswered</span></td></tr>',
    '<tr><td>Memos issued to you this year</td><td><span class="tag warn" id="chkMemo">2 · 1 unanswered</span></td></tr>')

# ══════════════════════════════════════════════ 6 · memo → feedback for growth (official's window)
rep('<h2>Memos received this year</h2>\n'
    '          <div class="sub">Issued in eHRMS by your reporting officer during the assessment period. '
    'These are visible on the grading screen.</div>',
    '<h2>Memos received this year</h2>\n'
    f'          <div class="sub">Memos issued in eHRMS by your reporting officer during the year. '
    'Each one records where your work needed to improve and what was expected, so that nothing in the '
    'assessment comes as a surprise.</div>\n'
    f'          {ADD}the same record, framed as development rather than as a disciplinary note.</div>')

rep('<tr><td>Memos issued to you during the year</td><td><span id="dMemo">2 · 1 unanswered</span></td></tr>',
    '<tr><td>Memos issued to you during the year</td><td><span id="dMemo">2 · 1 unanswered</span></td></tr>')

rep('<div class="note info">ℹ️ The memos issued to you and your replies are attached to your representation automatically.</div>',
    '<div class="note info">ℹ️ The memos issued to you and your replies are attached to your representation automatically.</div>')

rep('<div class="note info" style="margin-top:12px">ℹ️ If a memo was issued to you during the year, answer it in the memo itself rather than here. Your reply is already on record and is shown to the reporting officer.</div>',
    '<div class="note info" style="margin-top:12px">ℹ️ If a memo was issued to you during the year, answer it against the memo itself rather than here. Your reply is already on record and is shown to the reporting officer.</div>')

# ══════════════════════════════════════════════ 7 · reporting officer · memo card and composer
rep('<h2 style="cursor:pointer" onclick="toggleMemoCard()">Memo record for <span id="memoWho">Shri A. B. Sawant</span> for this assessment year',
    '<h2 style="cursor:pointer" onclick="toggleMemoCard()">Memo record for <span id="memoWho">Shri A. B. Sawant</span> for this assessment year')

rep('<div class="sub">Issued by you to this official during 2025–26. Shown here automatically.</div>',
    '<div class="sub">Memos you issued to this official during 2025–26, shown here automatically.</div>\n'
    f'        {ADD}framed as a development record. A memo notes where work needed to improve and what support '
    'was offered &mdash; it is not a penalty, and an official who received it during the year is not taken by '
    'surprise by the assessment.</div>')

rep('<div class="btnrow"><button class="btn amber" onclick="show(\'memoComposer\',1)">Issue a memo</button></div>',
    '<div class="btnrow"><button class="btn amber" onclick="show(\'memoComposer\',1)">Issue a memo</button></div>')

rep('<div class="part">eHRMS · issue a memo</div>\n'
    '          <div class="hint">Memos are raised in eHRMS, where your reporting chain is maintained, and can be issued any day of the year. MahaPAR reads them at grading.</div>',
    '<div class="part">eHRMS · issue a memo</div>\n'
    '          <div class="hint">Memos are raised in eHRMS, where your reporting chain is maintained, and can be issued any day of the year. MahaPAR reads them at grading.</div>')

rep('<label class="f"><span>Concern relates to</span>', '<label class="f"><span>Area for development</span>')

rep('<label class="f"><span>Subject</span><input type="text" id="mSub" placeholder="e.g. Delay in filing quarterly returns"></label>\n'
    '          <label class="f"><span>What the concern is, and what you expect to change</span>\n'
    '            <textarea id="mBody" placeholder="State the specific instance, date and what improvement is expected. Maximum 150 words."></textarea>',
    '<label class="f"><span>Subject</span><input type="text" id="mSub" placeholder="e.g. Timeliness of quarterly returns"></label>\n'
    '          <label class="f"><span>What you observed, and what good would look like</span>\n'
    '            <textarea id="mBody" placeholder="The specific instance and date, the guidance or support offered, and what improvement would look like by the next review. Maximum 150 words."></textarea>')

rep('<span>Notify the official that their response, or failure to respond, may be considered during the APAR assessment.</span>',
    '<span>Notify the official that this feedback is on record, that they may respond to it, and that both the feedback and their response are available at the time of assessment.</span>')

rep('<div class="btnrow"><button class="btn" onclick="sendMemo()">Sign and send memo</button>',
    '<div class="btnrow"><button class="btn" onclick="sendMemo()">Sign and send memo</button>')

rep('<div class="note info" style="margin-top:12px">ℹ️ Memos are issued in eHRMS, not here. One issued today is dated today and attaches to the <b>current</b> cycle, not to the year being assessed — so a concern should be recorded when it arises.</div>',
    '<div class="note info" style="margin-top:12px">ℹ️ Memos are issued in eHRMS, not here. One issued today is dated today and attaches to the <b>current</b> cycle, not to the year being assessed — so a memo should be issued when the concern arises, while there is still time to act on it.</div>')

# pending-with-me table header
rep('<th>Self-appraisal</th><th>Memos issued this year</th>',
    '<th>Self-appraisal</th><th>Memos issued this year</th>')
rep("This official has no memo record, so a below-benchmark grade would carry no documentation.",
    "This official has no memo record, so a below-benchmark grade would carry no documentation.")

# ══════════════════════════════════════════════ 8 · Part 3.1 · departmental KRAs for reference
rep('<div class="part" style="cursor:pointer;margin-top:14px" onclick="toggleCard(\'sysBody\',\'sysCaret\')">System data for your reference',
    f'''<div class="part" style="cursor:pointer;margin-top:14px" onclick="toggleCard('kraBody','kraCaret')">Departmental KRAs for this post <span class="ftag add">Newly added / changed</span> <span id="kraCaret" style="float:right;font-size:22px;line-height:1;color:var(--navy)">&#9662;</span></div>
        <div class="hidebox on" id="kraBody">
          <div class="hint">The KRAs the post carries, with what the official recorded against each in Part 2.1. Use them to anchor <b>dimension 1, delivery of planned work</b> and <b>dimension 2, quality of work</b>, so that delivery is judged against what this post is actually responsible for.</div>
          <table>
            <tr><th style="width:34%">Departmental KRA</th><th>Target for the year</th><th>What the official recorded</th></tr>
            <tr><td>Land-records grievance redressal</td><td>Disposal of land-records grievances for the section</td><td>Average disposal time reduced from 41 to 23 days</td></tr>
            <tr><td>Statutory compliance &middot; RTI</td><td>Clear 100% of RTI applications within statutory time</td><td>214 of 218 cleared within 30 days</td></tr>
            <tr><td>Returns and reporting</td><td>File all quarterly returns by the due date</td><td>3 of 4 on time; Q1 filed 23 days late</td></tr>
          </table>
          {ADD}departmental KRAs are shown here so that delivery and quality of work are read against the post&rsquo;s own responsibilities rather than in the abstract.</div>
          <div class="note info">&#8505;&#65039; <b>Future direction:</b> KRAs are typed into Part 2.1 today. They will be pre-filled from the department&rsquo;s KRA set once role mapping is complete.</div>
        </div>

        <div class="part" style="cursor:pointer;margin-top:14px" onclick="toggleCard('sysBody','sysCaret')">System data for your reference''')

# ══════════════════════════════════════════════ 9 · departmental enquiry record
rep('''        <div class="rule"></div>
        <div class="part">Part 3.4 · integrity</div>''',
    f'''        <div class="rule"></div>
        <div class="part">Departmental enquiry record <span class="ftag add">Newly added / changed</span></div>
        <div class="hint">Read-only, from the departmental enquiry portal. Shown for your reference while recording integrity below.</div>
        <table>
          <tr><th style="width:30%">Field</th><th>Value</th></tr>
          <tr><td>Status</td><td><b>Enquiry ongoing</b></td></tr>
          <tr><td>What the enquiry is about</td><td>Irregularity alleged in the sanction of three land-conversion cases in 2024&ndash;25</td></tr>
          <tr><td>Case reference</td><td>DE/RFD/2025/114</td></tr>
          <tr><td>Date initiated</td><td>09 Sep 2025</td></tr>
          <tr><td>Current stage</td><td>Enquiry officer appointed; statement of defence received</td></tr>
          <tr><td>Last updated</td><td>22 Feb 2026</td></tr>
        </table>
        {ADD}the reporting officer can now see whether a departmental enquiry is open against the official, and what it concerns.</div>
        <div class="note warn">&#9888;&#65039; <b>An enquiry that has not concluded is not a finding.</b> A pending enquiry is not by itself a ground for an adverse grade or for recording integrity as doubtful.</div>
        {DISC}which particulars of a departmental enquiry a reporting officer should see here &mdash; the fields above are a first proposal.</div>
        <div class="note info">&#8505;&#65039; <b>Future direction:</b> filled automatically once the departmental enquiry portal is linked to MahaPAR. Until then the custodian records the status.</div>

        <div class="rule"></div>
        <div class="part">Part 3.4 · integrity</div>''')

# ══════════════════════════════════════════════ 10 · Part 3.6 and the citation button
rep('<div class="part">Part 3.6 · memos or notices</div>\n'
    '          <div class="note danger">⚠️ <b>This overall grade is below the benchmark of 6.</b> You may attach memos or notices issued during the year as proof that the official was advised and given opportunities to improve.</div>\n'
    '          <div class="checks"><label><input type="checkbox" id="attachMemo" checked onchange="renderAttach()"><span>Attach the memo record for this year as evidence</span></label></div>',
    '<div class="part">Part 3.6 · memos issued during the year</div>\n'
    '          <div class="note danger">⚠️ <b>This overall grade is below the benchmark of 6.</b> Attach the memos issued during the year to show that the official was told where improvement was needed and was given the opportunity to act on it.</div>\n'
    '          <div class="checks"><label><input type="checkbox" id="attachMemo" checked onchange="renderAttach()"><span>Attach this year&rsquo;s memo record as evidence</span></label></div>')

rep('<button class="btn ghost sm" onclick="insertMemoRef()">Cite the memo record</button>',
    '<button class="btn ghost sm" onclick="insertMemoRef()">Cite the memo record</button>')

rep('<li style="margin-bottom:6px">Grade several dimensions <b>4 or 5</b> — the overall grade falls below 6 and the memo evidence panel opens, pre-filled from this year\'s memo record.</li>\n'
    '          <li>Press <b>Cite the memo record</b> to pull the memo dates and response status into 3.5.</li>',
    '<li style="margin-bottom:6px">Grade several dimensions <b>4 or 5</b> — the overall grade falls below 6 and the evidence panel opens, pre-filled from this year\'s memo record.</li>\n'
    '          <li>Press <b>Cite the memo record</b> to pull the memo dates and response status into 3.5.</li>')

rep("the year's memo record all sit on one screen with the grades. Extreme grades and a below-benchmark overall grade open the justification the form requires; the memo record is what makes a low grade defensible.",
    "the year's memo record all sit on one screen with the grades. Extreme grades and a below-benchmark overall grade open the justification the form requires; the memo record is what makes a low grade defensible.")

# ══════════════════════════════════════════════ 11 · custodian · tiles and step list
rep('<div class="ctile pink" onclick="custStep(2)" style="cursor:pointer"><span>APARs past their deadline at some stage</span><b>47</b><i>See what is pending, and with whom &rsaquo;</i></div>',
    '<div class="ctile pink" onclick="custStep(2)" style="cursor:pointer"><span>APARs past their deadline at some stage</span><b>47</b><i>See what is pending, and with whom &rsaquo;</i></div>\n'
    '    <div class="ctile amber" onclick="custStep(1)" style="cursor:pointer"><span>PAR workflows submitted by officials</span><b>1,042</b><i>242 not yet submitted &rsaquo;</i></div>')

rep('<li class="on" onclick="custStep(1)"><span class="n">1</span><div>Authority mapping<small>Map who reports on whom · validate NRCs</small></div></li>',
    '<li class="on" onclick="custStep(1)"><span class="n">1</span><div>Validate authority mapping<small>Check what officials mapped · validate NRCs</small></div></li>')

rep('<li onclick="custStep(4)"><span class="n">4</span><div>Memo tracking<small>Unanswered memos · remind</small></div></li>',
    '<li onclick="custStep(4)"><span class="n">4</span><div>Memo tracking<small>Unanswered memos · remind</small></div></li>')

rep('<p>As custodian you are responsible for four things in this cycle: recording who reports on whom and issuing No Report Certificates;',
    '<p>As custodian you are responsible for four things in this cycle: validating the reporting chain each official maps for themselves and issuing No Report Certificates;')

# ══════════════════════════════════════════════ 12 · custodian · mapping becomes validation
rep('<h2>Authority mapping</h2>\n'
    '          <div class="sub">Map every official to a reporting and reviewing officer, with the period each served under them. MahaPAR works out the duration and decides whether an APAR workflow is created or an NRC is auto-generated.</div>',
    '<h2>Validate authority mapping <span class="ftag add">Newly added / changed</span></h2>\n'
    '          <div class="sub">Officials now map their own reporting and reviewing authority. You check what they recorded and either validate it or issue a correction. MahaPAR works out the duration and decides whether an APAR workflow is created or an NRC is auto-generated.</div>\n'
    f'          {ADD}the mapping is submitted by the official; the custodian validates or corrects it, and pendency on unsubmitted mappings is tracked like any other stage. <b>This process is yet to be finalised.</b></div>\n'
    '')

rep('<tr><th>Official</th><th>Reporting officer<br>Reviewing officer</th><th>From<br>To</th><th>Duration</th><th>MahaPAR action</th></tr>',
    '<tr><th>Official</th><th>Mapped by the official<br>(reporting / reviewing)</th><th>From<br>To</th><th>Duration</th><th>Status</th><th>MahaPAR action</th></tr>')

# three existing rows need the extra status cell
rep('<td>12 months</td><td><span class="tag ok">APAR workflow created</span></td></tr>\n'
    '            <tr><td style="min-width:120px"><b>Shri L. M. Pawar</b>',
    '<td>12 months</td><td><span class="tag ok">Validated</span></td><td><span class="tag ok">APAR workflow created</span></td></tr>\n'
    '            <tr><td style="min-width:120px"><b>Shri L. M. Pawar</b>')

rep('<td>12 months</td><td><span class="tag ok">APAR workflow created</span></td></tr>\n'
    '            <tr><td style="min-width:120px"><b>Smt. J. K. More</b>',
    '<td>12 months</td><td><span class="tag warn">Submitted · to validate</span></td><td><span class="tag ok">APAR workflow created</span></td></tr>\n'
    '            <tr><td style="min-width:120px"><b>Smt. J. K. More</b>')

rep('<td>2 months<br>10 days</td><td><span class="tag warn">Under 3 months — NRC auto-generated</span></td></tr>',
    '<td>2 months<br>10 days</td><td><span class="tag warn">Submitted · to validate</span></td><td><span class="tag warn">Tenure 3 months or less — NRC auto-generated</span></td></tr>')

rep('<td>—</td><td><span class="tag red">Not mapped · no workflow</span></td></tr>',
    '<td>—</td><td><span class="tag red">Not submitted</span></td><td><span class="tag red">Not mapped · no workflow</span></td></tr>\n'
    '            <tr><td style="min-width:120px"><b>Smt. P. R. Shelke</b><br><span style="color:var(--muted)">Senior Clerk · Form B</span></td>\n'
    '              <td><span style="color:var(--muted)">No reporting authority in position</span><br><span style="color:var(--muted)">No reviewing authority in position</span></td>\n'
    '              <td>01/04/2025<br>31/03/2026</td>\n'
    '              <td>12 months</td><td><span class="tag warn">Submitted · to validate</span></td><td><span class="tag warn">No authority in position — NRC auto-generated</span></td></tr>')

rep('<div class="btnrow" style="margin-top:12px"><button class="btn ghost sm" onclick="toast(\'A further period is added where the reporting officer changed during the year.\')">+ Add a period</button><button class="btn sm" onclick="toast(\'Mapping saved. MahaPAR has created 2 APAR workflows and generated 1 No Report Certificate for your validation.\')">Save mapping</button></div>\n'
    '          <div class="note warn" style="margin-top:12px">⚠️ <b>1 official is not yet mapped.</b> No APAR workflow is created until a reporting officer and a period are recorded.</div>\n'
    '          <div class="note info">ℹ️ Officials can see this mapping in their own window but cannot change it. They may raise a request for a change, which comes to you.</div>',
    '<div class="btnrow" style="margin-top:12px"><button class="btn sm" onclick="toast(\'Mapping validated. MahaPAR has created the APAR workflows and generated 2 No Report Certificates for your validation.\')">Validate selected</button><button class="btn sm ghost" onclick="toast(\'A correction notifies the official and records the reason. The corrected mapping replaces what they submitted.\')">Issue a correction</button><button class="btn sm ghost" onclick="toast(\'Reminder sent to the 242 officials who have not submitted their PAR workflow.\')">Remind those who have not submitted</button></div>\n'
    '          <div class="note warn" style="margin-top:12px">⚠️ <b>242 officials have not yet submitted their PAR workflow,</b> and 1 is not mapped at all. No APAR workflow is created until a reporting authority and a period are on record, or an NRC is issued.</div>\n'
    '          <div class="note info">ℹ️ Officials map their own authorities and can see the validated record in their own window. A correction you issue replaces what they submitted and notifies them.</div>')

rep('<div class="note info">ℹ️ <b>Future direction:</b> once e-office orders are fully digitised, this mapping will be pre-filled from eHRMS and the custodian will only validate or correct it, rather than enter it.</div>',
    '<div class="note info">ℹ️ <b>Future direction:</b> once e-office orders are fully digitised, the mapping will be pre-filled from eHRMS, and both the official and the custodian will confirm it rather than enter it.</div>')

# ══════════════════════════════════════════════ 13 · NRC queue with explicit reasons
rep('<h3>NRC auto-generated by the MahaPAR system</h3>\n'
    '          <div class="sub">Auto-generated where the mapped period is under 3 months. Your validation issues the certificate.</div>\n'
    '          <div class="memo"><div class="top"><b>Smt. J. K. More</b><span class="tag warn">Awaiting your validation</span></div>\n'
    '            <div class="meta">Under Shri R. S. Gokhale · 20/01/2026 – 31/03/2026 · 2 months 10 days</div>',
    '<h3>NRC auto-generated by the MahaPAR system <span class="ftag add">Newly added / changed</span></h3>\n'
    '          <div class="sub">Auto-generated where the mapped tenure is 3 months or less, <b>or</b> where neither a reporting nor a reviewing authority was in position for the period. Each certificate records which of the two reasons applies. Your validation issues it.</div>\n'
    f'          {ADD}the second ground &mdash; no reporting and no reviewing authority in position &mdash; and the reason is now stated on each certificate.</div>\n'
    '          <div class="memo"><div class="top"><b>Smt. J. K. More</b><span class="tag warn">Awaiting your validation</span></div>\n'
    '            <div class="meta">Under Shri R. S. Gokhale · 20/01/2026 – 31/03/2026 · 2 months 10 days</div>\n'
    '            <div class="meta"><b>Reason:</b> tenure under the reporting authority was 3 months or less.</div>')

rep('<div class="memo answered"><div class="top"><b>Change requests from officials</b><span class="tag grey">0</span></div>',
    '<div class="memo"><div class="top"><b>Smt. P. R. Shelke</b><span class="tag warn">Awaiting your validation</span></div>\n'
    '            <div class="meta">01/04/2025 – 31/03/2026 · 12 months</div>\n'
    '            <div class="meta"><b>Reason:</b> no reporting authority and no reviewing authority was in position for the period.</div>\n'
    '            <div class="btnrow"><button class="btn sm" onclick="openNRC()">Validate and issue</button><button class="btn sm grey" onclick="toast(\'Rejecting needs a recorded reason, and sends the period back to mapping.\')">Reject</button></div>\n'
    '          </div>\n'
    '          <div class="note info">ℹ️ Where a <b>reviewing</b> authority alone was not in position, no NRC arises: an accepting authority is assigned under Part 5 instead.</div>\n'
    '          <div class="memo answered"><div class="top"><b>Change requests from officials</b><span class="tag grey">0</span></div>')

# ══════════════════════════════════════════════ 14 · custodian · pendency and stage-by-stage
rep('<tr><th>Official</th><th>Post</th><th>Waiting at</th><th>Waiting with</th><th>Overdue by</th><th></th></tr>',
    '<tr><th>Official</th><th>Post</th><th>Waiting at</th><th>Waiting with</th><th>Overdue by</th><th></th></tr>\n'
    '            <tr><td><b>Smt. P. R. Shelke</b></td><td>Senior Clerk</td><td>PAR workflow mapping <span class="ftag add">Newly added / changed</span></td><td>The official</td><td><span class="tag red">17 days</span></td><td><button class="btn sm ghost" onclick="toast(\'Reminder sent to Smt. P. R. Shelke to submit her PAR workflow.\')">Remind</button></td></tr>')

rep('<tr><th>Stage</th><th>Completed</th><th>On time</th><th>Late</th><th>Still pending</th></tr>\n'
    '            <tr><td>Self-appraisal</td>',
    '<tr><th>Stage</th><th>Completed</th><th>On time</th><th>Late</th><th>Still pending</th></tr>\n'
    '            <tr><td>PAR workflow mapping by the official <span class="ftag add">Newly added / changed</span></td><td>1,042</td><td>967</td><td>75</td><td><b>242</b></td></tr>\n'
    '            <tr><td>Self-appraisal</td>')

# ══════════════════════════════════════════════ 15 · custodian · memo tracking reframed
rep('<h2>Memos awaiting a reply from the official</h2>\n'
    '          <div class="sub">A memo was issued during the year and the official has not replied by the due date. You can remind them.</div>',
    '<h2>Memos awaiting a reply from the official</h2>\n'
    '          <div class="sub">A memo was issued during the year and the official has not replied by the due date. You can remind them.</div>')

rep('<tr><th>Official</th><th>Memo issued by</th><th>Issued on</th><th>Reply was due</th><th>Overdue by</th><th></th></tr>',
    '<tr><th>Official</th><th>Memo issued by</th><th>Issued on</th><th>Reply was due</th><th>Overdue by</th><th></th></tr>')

rep('<h2>Memos issued, by reporting officer</h2>',
    '<h2>Memos issued, by reporting officer</h2>')

rep('<tr><th>Reporting officer</th><th>Subordinates</th><th>Memos issued this year</th><th>Awaiting a reply</th><th>Officials with zero memos</th></tr>',
    '<tr><th>Reporting officer</th><th>Subordinates</th><th>Memos issued this year</th><th>Awaiting a reply</th><th>Officials who received no memo <span class="ftag add">Newly added / changed</span></th></tr>')

rep('<div class="sub">Counts only, for GAD&rsquo;s review. There is no action for the custodian here.</div>'.replace("&rsquo;", "'"),
    '<div class="sub">Counts only, for GAD\'s review. There is no action for the custodian here. A high figure in the last column is a supervision gap, not a clean record: it means a low grade later would arrive without warning.</div>')

rep('<div class="note info" style="margin-top:14px">ℹ️ A reply left unrecorded can count against the official when the APAR is graded. Reminding them keeps that fair.</div>',
    '<div class="note info" style="margin-top:14px">ℹ️ A reply left unrecorded can count against the official when the APAR is graded. Reminding them keeps that fair.</div>\n'
    f'          {ADD}the last column is now read as a supervision gap rather than a clean record. The memo record and its use at grading are unchanged.</div>')

# ══════════════════════════════════════════════ 16 · JS helpers
rep("function toggleMemoCard(",
    """var UPTHEMES = [
  "Respectful and fair behaviour with juniors",
  "Quality of support and guidance on the work",
  "Clarity of communication and instructions",
  "Mentorship and building your capability",
  "Timely decisions when the work needs one"
];
var upMarks = {};
function renderUp(){
  var t = document.getElementById('upTable');
  if (!t) return;
  var h = '<tr><th style="width:52%">Area</th><th>Your rating</th></tr>';
  UPTHEMES.forEach(function(name, i){
    var cells = '';
    for (var n = 1; n <= 5; n++){
      cells += '<span class="upm' + (upMarks[i] === n ? ' on' : '') +
               '" onclick="setUp(' + i + ',' + n + ')">' + n + '</span>';
    }
    cells += '<span class="upm na' + (upMarks[i] === 0 ? ' on' : '') +
             '" onclick="setUp(' + i + ',0)">N/A</span>';
    h += '<tr><td>' + name + '</td><td>' + cells + '</td></tr>';
  });
  t.innerHTML = h;
}
function setUp(i, n){ upMarks[i] = n; renderUp(); }
function addTenure(id){
  var t=document.getElementById(id), r=t.rows[1].cloneNode(true);
  r.querySelectorAll('input').forEach(function(i){i.value='';});
  t.appendChild(r);
}
function submitMapping(){
  show('mapDone',1);
  toast('PAR workflow submitted to the custodian, Shri G. H. Mane, for validation.');
}
function toggleMemoCard(""")

# ══════════════════════════════════════════════ 17 · 2.6 is not shown to the reporting officer
rep('<div class="note info">&#8505;&#65039; You respond to the training request in <b>Part 3.8</b> below.</div>',
    '<div class="note info">&#8505;&#65039; You respond to the training request in <b>Part 3.8</b> below.</div>\n'
    '        <div class="note info">&#8505;&#65039; <b>Part 2.6 is deliberately not shown here.</b> Feedback an official shares with their reporting officer is pooled across everyone who reports to them and shared anonymously, separately from any APAR.</div>')

rep('seeing that memos are being issued during the year;',
    'seeing that memos are being issued during the year;')


# ══════════════════════════════════════════════ 18 · banners and provenance
rep('<span><b>DRAFT FOR DISCUSSION</b> · IDinsight with GAD · October 2026 · demo data · all names and figures are illustrative</span>',
    '<span><b>DRAFT FOR DISCUSSION WITH GAD</b> · Template created by IDinsight · '
    'November 2026 · demo data · all names and figures are illustrative</span>')

rep('<footer>MahaPAR · draft user windows for discussion with GAD · IDinsight, October 2026 · demo data, no real official records</footer>',
    '<footer><b>Template created by IDinsight</b> · MahaPAR draft user windows for '
    'discussion with GAD · November 2026 · demo data, no real official records<br>'
    '<span style="opacity:.8">Prepared by IDinsight for the General Administration '
    'Department, Government of Maharashtra. Not for circulation or reuse without '
    'permission.</span></footer>')

# the feedback item is not settled: say so on the question itself
rep(DISC + 'what safeguards, beyond pooling and anonymity, will ensure that sharing '
         'feedback carries no consequence for the official &mdash; and at what point the '
         'pooled feedback should reach the reporting officer. One option is to release it '
         'only after that officer has submitted every assessment for the cycle.</div>',
    DISC + 'what safeguards, beyond pooling and anonymity, will ensure that '
    'sharing feedback carries no consequence for the official &mdash; and at what point the '
    'pooled feedback should reach the reporting officer.</div>')


open(DST, "w", encoding="utf-8").write(s)
print("wrote", DST, "·", n, "edits ·", round(os.path.getsize(DST) / 1024), "KB")
