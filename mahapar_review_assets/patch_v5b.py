#!/usr/bin/env python3
"""Second half of the v5 build: the reporting officer section, the reviewing
officer summary, and the script that drives the KPI and learning tables."""
F = "/home/user/personal_v1/MahaPAR_APAR_portal_walkthrough_v5.html"
h = open(F).read()


def swap(old, new):
    global h
    assert old in h, "anchor not found: " + old[:90]
    h = h.replace(old, new, 1)


# ===========================================================================
# A. What the official wrote: show the KPI table when a technical cadre is on
# ===========================================================================
swap("""        <div class="part">Part 2.1 · key activities, responsibilities and targets</div>
        <table>""",
"""        <div class="part">Part 2.1 · key activities, responsibilities and targets</div>
        <div class="hidebox" id="kpiWroteBox"><div class="tscroll"><table id="kpiWrote"></table></div></div>
        <table id="genWrote">""")

swap("""        <div class="part" style="margin-top:14px">Part 2.4 · training completed</div>
        <table>
          <tr><th>Course</th><th>Category</th><th>Hours</th></tr>
          <tr><td>eOffice for Section Officers</td><td>IT and digital tools</td><td>12</td></tr>
          <tr><td>RTI Act: practice and timelines</td><td>General rules and procedures</td><td>8</td></tr>
          <tr><td><b>Total</b></td><td></td><td><b>20</b></td></tr>
        </table>""",
"""        <div class="part" style="margin-top:14px">Part 2.4 · learning and development</div>
        <div class="tscroll"><table id="lndWrote"></table></div>""")

# ===========================================================================
# B. Part 3: renumbered, with KPI marking replacing work output where it applies
# ===========================================================================
swap("""        <div class="part">Part 3.1 · grading</div>
        <div class="q">Grade each dimension from 1 to 10, compared with officials at the same level</div>""",
"""        <div class="part">Part 3.1 · work output · 40%</div>
        <div class="q" id="q31">Grade each dimension from 1 to 10, compared with officials at the same level</div>""")

swap("""        <div class="grp">Work output · 40%</div>
        <div class="dim"><div class="nm">1. Delivery of planned work</div>""",
"""        <!-- technical cadre: KPI marking replaces the two work-output dimensions -->
        <div class="hidebox" id="kpiGradeBox">
          <div class="hint">MahaPAR sets the category from the year-end status the official recorded, so only that band of marks opens: Completed 7 to 10, Partly completed 3 to 6, Not completed 1 to 2. A remark is required for Not completed, or where the target was revised.</div>
          <div id="kpiGrade"></div>
        </div>

        <div id="genGradeBox">
        <div class="dim"><div class="nm">1. Delivery of planned work</div>""")

swap("""        <div class="grp">Functional competence · 30%</div>""",
"""        </div>

        <div class="rule"></div>
        <div class="part">Part 3.2 · functional competence · 30%</div>""")

swap("""        <div class="grp">Personal attributes · 30%</div>""",
"""        <div class="rule"></div>
        <div class="part">Part 3.3 · personal attributes · 30%</div>""")

swap("""        <div class="rule"></div>
        <div class="part">Part 3.2 · integrity</div>""",
"""        <div class="rule"></div>
        <div class="part">Part 3.4 · integrity</div>""")

swap("""        <div class="part">Part 3.5 · training nominations</div>""",
"""        <div class="part">Part 3.8 · training needs</div>""")

swap("""        <div class="part">Part 3.3 · compulsory</div>""",
"""        <div class="part">Part 3.5 · compulsory</div>""")

swap("""        <div class="part">Part 3.4</div>""",
"""        <div class="part">Part 3.7</div>""")

# the below-benchmark memo panel becomes its own numbered part
swap("""        <div class="hidebox" id="lowBox">
          <div class="note danger">""",
"""        <div class="hidebox" id="lowBox">
          <div class="rule"></div>
          <div class="part">Part 3.6 · memos or notices</div>
          <div class="note danger">""")

# 3.8 (b): the recommendations become clickable, as in 2.5
swap("""        <div class="q" style="margin-top:14px">(b) Trainings you recommend (iGOT courses or other), up to three</div>
        <table style="margin-top:8px">
          <tr><th style="width:55%">Training or iGOT course</th><th>Type</th></tr>
          <tr><td><input type="text" placeholder="Course or programme"></td>
            <td class="typecell"><label><input type="checkbox"> Domain</label><label><input type="checkbox"> Functional</label><label><input type="checkbox"> Behavioural</label></td></tr>
          <tr><td><input type="text" placeholder="Course or programme"></td>
            <td class="typecell"><label><input type="checkbox"> Domain</label><label><input type="checkbox"> Functional</label><label><input type="checkbox"> Behavioural</label></td></tr>
          <tr><td><input type="text" placeholder="Course or programme"></td>
            <td class="typecell"><label><input type="checkbox"> Domain</label><label><input type="checkbox"> Functional</label><label><input type="checkbox"> Behavioural</label></td></tr>
        </table>""",
"""        <div class="q" style="margin-top:14px">(b) Training you recommend, up to three</div>
        <div class="hint">Select from the list; each one you select is added below, where you mark its type. Use <b>Other</b> for anything not listed.</div>
        <div class="chips" id="roTrainChips"></div>
        <table style="margin-top:10px" id="roNeedTable"></table>""")

# ===========================================================================
# C. Scoreboard: show where each group average comes from
# ===========================================================================
swap("""          <div class="ln"><span>Work output · 40%</span><b id="wOut">—</b></div>
          <div class="ln"><span>Functional competence · 30%</span><b id="wFun">—</b></div>
          <div class="ln"><span>Personal attributes · 30%</span><b id="wPer">—</b></div>""",
"""          <div class="ln"><span>Work output · 40%<br><small id="wOutSrc">average of dimensions 1 and 2</small></span><b id="wOut">—</b></div>
          <div class="ln"><span>Functional competence · 30%<br><small>average of dimensions 3 and 4</small></span><b id="wFun">—</b></div>
          <div class="ln"><span>Personal attributes · 30%<br><small>average of dimensions 5 and 6</small></span><b id="wPer">—</b></div>""")

# ===========================================================================
# D. Reviewing officer: a group-average summary before the agree question
# ===========================================================================
swap("""      <div class="card">
        <div class="part">Part 4.1</div>""",
"""      <div class="card">
        <h2>As recorded by the reporting officer</h2>
        <div class="sub">Group averages only. The reviewing officer is asked about the overall grade, not the individual items.</div>
        <table id="revSummary"></table>
      </div>

      <div class="card">
        <div class="part">Part 4.1</div>""")

open(F, "w").write(h)
print("part 2 of the patch applied")
