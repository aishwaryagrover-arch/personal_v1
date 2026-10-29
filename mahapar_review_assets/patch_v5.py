#!/usr/bin/env python3
"""
Builds walkthrough v5 from v4: the agreed items from the partner's
engineering-cadre file, folded into our generic Form A walkthrough.

Each replacement is anchored on text unique to v4, so a failed anchor
stops the build rather than writing a half-patched file.
"""
F = "/home/user/personal_v1/MahaPAR_APAR_portal_walkthrough_v5.html"
h = open(F).read()


def swap(old, new, count=1):
    global h
    assert h.count(old) >= 1, "anchor not found: " + old[:80]
    h = h.replace(old, new, count)


# ===========================================================================
# 1. Part 1: leave comes from eHRMS, with a revalidation request
# ===========================================================================
swap("""          <label class="f"><span>Leave or absence of 30 days or more</span>
            <select><option>None this year</option><option>Earned leave — 34 days</option><option>Medical leave</option><option>Other</option></select></label>""",
"""          <div class="ro"><b>Leave or absence of 30 days or more</b>Earned leave, 34 days (10 Nov to 13 Dec 2025)</div>
          <div class="hint" style="margin-top:-6px">Pulled directly from eHRMS. Only leave of 30 days or more is shown; shorter leave adds nothing to grading.</div>
          <div class="btnrow" style="margin-top:8px"><button class="btn ghost sm" onclick="toast('Request sent to the custodian to revalidate the leave record against eHRMS.')">This is not correct, request revalidation</button></div>""")

# ===========================================================================
# 2. Year-round list gains My KPIs
# ===========================================================================
swap("""        <ul class="steplist" id="yearSteps">
          <li onclick="selfStep(6)">""",
"""        <ul class="steplist" id="yearSteps">
          <li onclick="selfStep(8)"><span class="n">&#9679;</span><div>My KPIs<small id="kpiCountSm">Opens for technical cadres</small></div></li>
          <li onclick="selfStep(6)">""")

# ===========================================================================
# 3. The whole of step 3, rebuilt
# ===========================================================================
old3_start = '      <div class="wiz" id="self3">'
old3_end = '      <!-- step 4 · review and sign -->'
i, j = h.index(old3_start), h.index(old3_end)

NEW3 = '''      <div class="wiz" id="self3">

        <!-- technical module first: it decides what 2.1 asks for -->
        <div class="card">
          <div class="part">Part 2.6 · technical cadre</div>
          <div class="hint">Answered first, because it decides what Part 2.1 asks you for.</div>
          <div class="q">Do you belong to a technical cadre?</div>
          <div class="radios">
            <label><input type="radio" name="tech" checked onclick="setTech(0)"><span>No</span></label>
            <label><input type="radio" name="tech" onclick="setTech(1)"><span>Yes &mdash; MahaPAR opens the module for my cadre</span></label>
          </div>
          <div class="hidebox" id="techBox">
            <div class="two">
              <label class="f"><span>Module</span><select id="techMod" onchange="fillDesig()"></select></label>
              <label class="f"><span>Designation held during the reporting period</span><select id="techDesig" onchange="setDesig()"></select></label>
            </div>
            <div class="note info" id="techNote"></div>
          </div>
        </div>

        <div class="card">
          <div class="part">Part 2.1</div>

          <!-- general form: free-text targets -->
          <div id="genBox">
            <div class="q">Key activities, responsibilities and targets for the year</div>
            <div class="hint">Fill only if these were set for your post. Otherwise go to 2.2.</div>
            <div class="note info">&#8505;&#65039; <b>Future direction:</b> role and KRA information pre-filled where available once role mapping for priority departments is complete; targets selected from a drop-down once KPIs are linked to MahaPAR.</div>
            <table>
              <tr><th style="width:50%">Key activity, responsibility or target</th><th>Achievement</th></tr>
              <tr><td><input type="text" value="Disposal of land-records grievances for the section"></td><td><input type="text" value="Average disposal time reduced from 41 to 23 days"></td></tr>
              <tr><td><input type="text" value="Clear 100% of RTI applications within statutory time"></td><td><input type="text" value="214 of 218 cleared within 30 days"></td></tr>
              <tr><td><input type="text" placeholder="3."></td><td><input type="text" placeholder="Achievement"></td></tr>
            </table>
          </div>

          <!-- technical cadre: the KPI table -->
          <div class="hidebox" id="kpiBox">
            <div class="q">Your KPIs for the year</div>
            <div class="hint">Your KPIs, targets and mid-year progress come from <b>My KPIs</b>, which is open all year. Add the year-end status, what you achieved, and the record where it can be checked. Your reporting and reviewing officers see this table when grading.</div>
            <div class="tscroll"><table id="kpiSelf"></table></div>
            <div class="btnrow" style="margin-top:12px"><button class="btn ghost sm" onclick="selfStep(8)">Open My KPIs</button></div>
          </div>
        </div>

        <div class="card">
          <div class="part">Part 2.2</div>
          <div class="q">Your most significant contribution this year</div>
          <div class="hint">One or two pieces of work: what you did, and what changed as a result. No attachments.</div>
          <textarea id="t22" oninput="wc('t22','c22',100)" style="min-height:120px">Redesigned the district land-records grievance workflow on eOffice. Cut average disposal time from 41 days to 23 days across six talukas and cleared a backlog of 1,340 cases.</textarea>
          <div class="counter" id="c22"></div>
          <div class="btnrow" style="margin-top:-4px"><button class="btn ghost sm" onclick="openLog()">Pull from my work log (7 entries)</button></div>
          <div class="rule"></div>
          <div class="part">Part 2.3 · optional</div>
          <div class="q">Systemic factors (factors outside your control) that affected your work</div>
          <div class="hint">For example technical constraints, budget or fund-release constraints, delays in approvals or sanctions, staffing shortages, or dependence on another office, agency or contractor.</div>
          <textarea id="t23" oninput="wc('t23','c23',50)" placeholder="Optional — leave blank if none"></textarea>
          <div class="counter" id="c23"></div>
          <div class="note info" style="margin-top:12px">ℹ️ If a memo was issued to you during the year, answer it in the memo itself rather than here. Your reply is already on record and is shown to the reporting officer.</div>
        </div>

        <div class="card">
          <div class="part">Part 2.4 · learning and development during the year</div>
          <div class="sub">iGOT courses are pulled from your iGOT record; confirm each one. Add anything else below. Total hours are shown to your reporting officer while grading.</div>
          <div class="tscroll"><table id="lndTable"></table></div>
          <div class="btnrow" style="margin-top:12px"><button class="btn ghost sm" onclick="show('lndAdd',1)">+ Add training, a workshop or a qualification</button></div>
          <div class="hidebox" id="lndAdd" style="margin-top:12px;border-top:1px solid var(--border);padding-top:12px">
            <div class="two">
              <label class="f"><span>Type</span>
                <select id="lType" onchange="show('lRoleBox',this.value==='Workshop or conference')">
                  <option value="Other training">Other training (institute, professional body, software, certification)</option>
                  <option value="Workshop or conference">Workshop or conference</option>
                  <option value="Qualification gained">Qualification gained</option>
                </select></label>
              <label class="f"><span>Title</span><input type="text" id="lTitle" placeholder="e.g. Budget preparation workshop"></label>
              <label class="f"><span>Institute or organiser</span><input type="text" id="lBy" placeholder="e.g. YASHADA"></label>
              <label class="f"><span>Dates</span><input type="text" id="lDates" placeholder="e.g. 3 to 4 Mar 2026"></label>
              <label class="f"><span>Hours</span><input type="text" id="lHrs" placeholder="e.g. 12"></label>
              <label class="f hidebox" id="lRoleBox"><span>Your role</span>
                <select id="lRole"><option>Attended</option><option>Presented</option><option>Organised</option></select></label>
            </div>
            <div class="btnrow"><button class="btn sm" onclick="addLnd()">Add row</button><button class="btn sm grey" onclick="show('lndAdd',0)">Cancel</button></div>
          </div>
          <div class="rule"></div>
          <div class="part">Part 2.5 · optional</div>
          <div class="q">Any additional training you need?</div>
          <div class="hint">Choose up to three. Examples for each category are in the annexure.</div>
          <div class="chips" id="trainChips"></div>
          <div class="note info" id="chipNote">ℹ️ 0 of 3 selected.</div>
        </div>

        <div class="btnrow" style="margin-top:-4px;margin-bottom:18px"><button class="btn grey" onclick="selfStep(2)">Back</button><button class="btn" onclick="selfStep(4)">Continue to review and sign</button></div>
      </div>

'''
h = h[:i] + NEW3 + h[j:]

# ===========================================================================
# 4. My KPIs, the year-round screen
# ===========================================================================
swap("""      <!-- year-round · work log -->""",
"""      <!-- year-round · My KPIs -->
      <div class="wiz" id="self8">
        <div class="card">
          <h2>My KPIs · 2025&ndash;26</h2>
          <div class="sub">At the start of the year, pick 3 to 5 KPIs from the menu for your designation, with a target for each. Record mid-year progress by 31 October; a target may be revised then, with a reason. Your reporting officer can see this page. There is no separate mid-year marking.</div>
          <div class="note warn">🔔 MahaPAR sends a reminder in October. This year&rsquo;s reminder went out on 1 Oct 2025; mid-year progress was recorded on 24 Oct 2025.</div>
          <div id="kpiOffNote" class="note info">ℹ️ This page opens once a technical cadre and designation are selected in Part 2.6.</div>
          <div class="tscroll"><table id="myKpiTable"></table></div>
          <div class="btnrow" style="margin-top:12px"><button class="btn ghost sm" onclick="addMyKpi()">+ Add a KPI</button><button class="btn sm" onclick="toast('KPIs and targets saved. Your reporting officer can see them.')">Save</button></div>
        </div>
      </div>

      <!-- year-round · work log -->""")

# ===========================================================================
# 5. Review-and-sign rows follow the new Part 2
# ===========================================================================
swap("""            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.1 Targets</td><td><span class="tag ok">2 entered</span></td></tr>""",
"""            <tr onclick="selfStep(3)" style="cursor:pointer"><td id="chk21lbl">2.1 Targets</td><td><span class="tag ok" id="chk21">2 entered</span></td></tr>""")
swap("""            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.4 Training completed</td><td><span class="tag ok">20 hours</span></td></tr>""",
"""            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.4 Learning and development</td><td><span class="tag ok" id="chkLnd">—</span></td></tr>""")
swap("""            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.6 Technical cadre</td><td><span class="tag ok">No</span></td></tr>""",
"""            <tr onclick="selfStep(3)" style="cursor:pointer"><td>2.6 Technical cadre</td><td><span class="tag ok" id="chkTech">No</span></td></tr>""")

open(F, "w").write(h)
print("part 1 of the patch applied")
