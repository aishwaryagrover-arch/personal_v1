#!/usr/bin/env python3
"""
Web version of the dashboard refinement note.

Reuses the same content as build.py (the PDF), rendered as a single
scrolling page with group filters, anchor navigation, and a click-to-
enlarge view of each screenshot. Output sits beside the cropped
screenshots so that relative image paths resolve.
"""
import importlib.util, sys, io, contextlib

spec = importlib.util.spec_from_file_location(
    "note", "/home/user/personal_v1/mahapar_review_assets/build.py")
note = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):      # build.py writes the PDF html on import
    spec.loader.exec_module(note)

RECS, RETAIN, TIERS = note.RECS, note.RETAIN, note.TIERS
OUT = "/home/user/personal_v1/mahapar_review_assets/dashboard_refinements.html"

CSS = note.CSS + """
/* ---------- web overrides: the print page box is not used here ---------- */
body{background:#EEF1F6;font-size:13px;padding:0}
.page{display:none}
.web{max-width:1280px;margin:0 auto;padding:0 22px 70px}

.masthead{background:#15233D;color:#fff;padding:30px 0 26px;margin-bottom:0}
.masthead .in{max-width:1280px;margin:0 auto;padding:0 22px}
.masthead .eyebrow{font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#F59E0B;font-weight:600}
.masthead h1{font-size:27px;line-height:1.2;font-weight:700;margin:9px 0 9px;max-width:860px}
.masthead p{font-size:13.5px;color:#B8C7DE;max-width:780px;line-height:1.6}
.masthead .meta{display:flex;gap:34px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.18);margin-top:18px;padding-top:14px;font-size:11.5px;color:#B8C7DE}
.masthead .meta b{display:block;color:#fff;font-size:12.5px;margin-bottom:2px}
.draftchip{display:inline-block;border:1px solid #F59E0B;color:#F59E0B;font-size:9.5px;letter-spacing:.1em;padding:3px 10px;border-radius:3px;text-transform:uppercase;margin-bottom:4px}

.bar{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #DDE3EF;box-shadow:0 1px 3px rgba(16,24,40,.05)}
.bar .in{max-width:1280px;margin:0 auto;padding:9px 22px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.bar .lab{font-size:11.5px;color:#64748B;margin-right:2px}
.fchip{border:1px solid #DDE3EF;background:#fff;border-radius:99px;padding:6px 14px;font-size:12px;color:#475569;cursor:pointer}
.fchip:hover{border-color:#94A3B8}
.fchip.on{background:#15233D;border-color:#15233D;color:#fff;font-weight:600}
.fchip .c{opacity:.7;margin-left:4px;font-size:11px}
.bar .right{margin-left:auto;display:flex;gap:8px;align-items:center}
.tog{border:1px solid #DDE3EF;background:#fff;border-radius:7px;padding:6px 12px;font-size:12px;color:#475569;cursor:pointer}
.tog.on{background:#EFF5FF;border-color:#2563EB;color:#1D4ED8;font-weight:600}

.intro{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:22px 0 10px}
.intro .box{background:#fff}
.sumwrap{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:18px 20px;margin-bottom:26px}
.sumwrap h3{font-size:15px;color:#15233D;margin-bottom:4px}
.sumwrap p.lead{font-size:12.5px}
table.sum a{color:#1D4ED8;text-decoration:none}
table.sum a:hover{text-decoration:underline}
table.sum tr{cursor:pointer}
table.sum tr:hover td{background:#EFF5FF}

.card{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:20px 22px;margin-bottom:20px;scroll-margin-top:66px}
.card .top{display:flex;gap:11px;align-items:flex-start;margin-bottom:4px}
.card .num{background:#15233D;color:#fff;width:25px;height:25px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;flex:0 0 auto}
.card h2{font-size:17px;line-height:1.3;color:#15233D;flex:1}
.card .grouptag{font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;font-weight:700;padding:3px 9px;border-radius:4px;color:#fff;white-space:nowrap}
.shotbox{border:1px solid #CBD5E1;border-radius:6px;background:#F8FAFC;padding:7px;text-align:center;margin:12px 0 4px;cursor:zoom-in;position:relative}
.shotbox img{max-width:100%;max-height:430px;width:auto;display:inline-block;border:1px solid #E2E8F0;background:#fff}
.shotbox .zoomhint{position:absolute;right:10px;top:10px;background:rgba(21,35,61,.78);color:#fff;font-size:10px;padding:3px 9px;border-radius:99px}
.body2{display:grid;grid-template-columns:1fr 1.05fr;gap:20px;align-items:start;margin-top:14px}
.obs,.sug{font-size:12.5px}
.why{font-size:12px}
.eff{font-size:11.5px}
.lbl{font-size:9.5px}
.mockbox{background:#FCFDFF}
table.mock{font-size:10.5px}
table.mock th{font-size:10px;padding:5px 7px}
table.mock td{padding:5px 7px}

.retainweb{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.retainweb .r{background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:14px}
.retainweb .r img{width:100%;border:1px solid #CBD5E1;border-radius:5px;display:block;margin-bottom:10px;cursor:zoom-in}
.retainweb .r h4{font-size:13px;color:#15233D;margin-bottom:4px}
.retainweb .r p{font-size:12px;color:#475569}
.secthead{margin:34px 0 14px;border-left:4px solid #F59E0B;padding-left:12px}
.secthead h3{font-size:18px;color:#15233D}
.secthead p{font-size:12.5px;color:#64748B;margin-top:2px}
.steps li{font-size:12.5px}
.nextgrid{display:grid;grid-template-columns:1.1fr 1fr;gap:18px;background:#fff;border:1px solid #DDE3EF;border-radius:10px;padding:20px 22px}

/* lightbox */
.lb{position:fixed;inset:0;background:rgba(13,25,48,.92);display:none;align-items:center;justify-content:center;z-index:100;padding:26px;cursor:zoom-out}
.lb.on{display:flex}
.lb img{max-width:100%;max-height:100%;border:1px solid rgba(255,255,255,.2);border-radius:4px}
.lb .close{position:absolute;top:16px;right:22px;color:#fff;font-size:13px;background:rgba(255,255,255,.14);border-radius:7px;padding:7px 14px}
.webfoot{text-align:center;font-size:11.5px;color:#94A3B8;padding:26px 0 0;border-top:1px solid #DDE3EF;margin-top:34px}
.hidden{display:none !important}
@media(max-width:980px){.body2,.intro,.retainweb,.nextgrid{grid-template-columns:1fr}}
"""

def effort_short(e):
    el = e.lower()
    return "Very low" if el.startswith("very low") else ("Low" if el.startswith("low —") or el.startswith("low -") else "Low–moderate")

rows = []
for r in RECS:
    t, c = TIERS[r["tier"]]
    es = effort_short(r["eff"])
    cls = "e1" if es == "Very low" else ("e1" if es == "Low" else "e2")
    rows.append(
        f"<tr onclick=\"jump('r{r['id']}')\"><td class='n'>{r['id']}</td>"
        f"<td><span class='tiertag' style='background:{c}'>{r['tier']}</span></td>"
        f"<td><a href='#r{r['id']}'>{r['title']}</a></td>"
        f"<td><span class='effpill {cls}'>{es}</span></td></tr>")

cards = []
for r in RECS:
    tname, tcol = TIERS[r["tier"]]
    cards.append(f"""
<article class='card' id='r{r['id']}' data-tier='{r['tier']}'>
  <div class='top'><span class='num'>{r['id']}</span><h2>{r['title']}</h2>
    <span class='grouptag' style='background:{tcol}'>Group {r['tier']}</span></div>
  <div class='shot-part'>
    <div class='lbl'>As presently displayed in SPARROW</div>
    <div class='shotbox' onclick="zoom('{r['shot']}')"><span class='zoomhint'>Click to enlarge</span>
      <img src='{r['shot']}' loading='lazy'></div>
  </div>
  <div class='body2'>
    <div>
      <div class='lbl'>What we observed</div>
      <div class='obs' style='margin-bottom:12px'>{r['obs']}</div>
      <div class='lbl'>Suggested refinement</div>
      <div class='sug'>{r['sug']}</div>
      <div class='eff'><span class='pill'>Effort</span><span>{r['eff']}</span></div>
    </div>
    <div>
      <div class='lbl'>Indicative form of the suggestion</div>
      <div class='mockbox'>{r['mock']}</div>
      <div class='why'><b>Why it helps.</b> {r['why']}</div>
    </div>
  </div>
</article>""")

counts = {k: sum(1 for r in RECS if r["tier"] == k) for k in TIERS}
chips = "".join(
    f"<button class='fchip' data-f='{k}' onclick=\"filt('{k}')\">{v[0]}<span class='c'>{counts[k]}</span></button>"
    for k, v in TIERS.items())

retain = "".join(
    f"<div class='r'><img src='{s}' onclick=\"zoom('{s}')\" loading='lazy'><h4>{t}</h4><p>{d}</p></div>"
    for t, d, s in RETAIN)

HTML = f"""<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>APAR Dashboard Refinements</title>
<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' rel='stylesheet'>
<style>{CSS}</style></head><body>

<header class='masthead'><div class='in'>
  <span class='eyebrow'>Government of Maharashtra · General Administration Department</span>
  <h1>Suggested refinements to the APAR dashboards developed by NIC</h1>
  <p>Nineteen observations from a walkthrough of the SPARROW APAR screens, each framed as a low-effort refinement that works
  within the existing design, and each referenced to the screen on which it was observed.</p>
  <div class='meta'>
    <div><b>Prepared for</b>General Administration Department,<br>and thereafter for NIC</div>
    <div><b>Prepared by</b>IDinsight</div>
    <div><b>Basis</b>19 screens recorded from the<br>SPARROW APAR application, October 2026</div>
    <div><b>Status</b><span class='draftchip'>Draft for discussion</span></div>
  </div>
</div></header>

<nav class='bar'><div class='in'>
  <span class='lab'>Show</span>
  <button class='fchip on' data-f='all' onclick="filt('all')">All nineteen<span class='c'>19</span></button>
  {chips}
  <span class='right'>
    <button class='tog' id='tgShots' onclick='toggleShots()'>Hide screenshots</button>
    <button class='tog' onclick="window.print()">Print</button>
  </span>
</div></nav>

<div class='web'>

<div class='intro'>
  <div class='box accent'><h4>Within the present design</h4><p>Every suggestion keeps NIC's existing layout, colour scheme and
  components. Nothing here calls for a new screen, a new report or a change to the underlying data model. Where a suggestion
  needs more than a change of wording or order, this is stated plainly.</p></div>
  <div class='box accent'><h4>Referenced to the screen</h4><p>Each item carries the screen on which the point was observed, so
  that NIC can locate it directly. Click any screenshot to enlarge it. Beside it is the suggested form of the same element,
  drawn in NIC's own visual style.</p></div>
  <div class='box accent'><h4>Effort is our reading, not an estimate</h4><p>The effort noted against each suggestion is
  IDinsight's assessment from the screens alone. NIC is best placed to confirm it, and we would welcome correction where our
  reading of the effort involved is mistaken.</p></div>
</div>

<div class='sumwrap'>
  <h3>The nineteen suggestions at a glance</h3>
  <p class='lead'>Grouped by theme. Select any row to go to the detail. The effort rating is IDinsight's reading of the
  screens and is offered for NIC to confirm or correct.</p>
  <table class='sum'><tr><th></th><th>Group</th><th>Suggestion</th><th>Indicative effort</th></tr>{''.join(rows)}</table>
  <div class='notebox' style='margin-top:12px'><b>A note on sequencing.</b> Suggestions 17 and 2 — the spelling corrections
  and the wording of the performance labels — cost very little and are the points most readily noticed when the system is
  demonstrated. They may be worth taking up first. Suggestions 4, 9 and 16 would, in our assessment, make the greatest
  practical difference to the monitoring authorities, and would merit discussion with NIC on sequencing.</div>
</div>

<div class='secthead'><h3>The suggestions in detail</h3>
<p>One entry per observation, in group order.</p></div>

{''.join(cards)}

<div class='secthead'><h3>Features we would suggest retaining</h3>
<p>Noted explicitly so that they are not altered in the course of taking up the suggestions above.</p></div>
<div class='retainweb'>{retain}</div>

<div class='secthead'><h3>Suggested next steps</h3>
<p>Offered for GAD's consideration in the first instance, and thereafter for discussion with NIC.</p></div>
<div class='nextgrid'>
  <div><ol class='steps'>
    <li><b>GAD's view on the list.</b> Confirm which suggestions GAD wishes to take up, and whether any further points should
    be added from the department's own experience of the system.</li>
    <li><b>Confirm the two rules that need a departmental decision.</b> Suggestion 3 requires GAD to confirm the DPC
    eligibility threshold the report should apply. Suggestion 14 requires the refresh interval beyond which dashboard figures
    should be flagged as dated.</li>
    <li><b>Discussion with NIC on effort and sequence.</b> NIC to confirm or correct the indicative effort against each
    suggestion, and to advise which can be taken up in the current release.</li>
    <li><b>A short first set.</b> We would suggest the wording and ordering changes be taken up together as a first set, as
    they require no change to data or queries.</li>
    <li><b>Review after the first set is deployed.</b> A walkthrough with GAD and NIC once the first set is live, before
    taking a view on the remainder.</li>
  </ol></div>
  <div>
    <div class='box accent'><h4>Two points for GAD's decision</h4>
      <p><b>DPC eligibility threshold.</b> The report's note and its computation presently state different thresholds. The
      correct rule is a departmental matter rather than a technical one, and NIC will need it confirmed before the note can be
      corrected.</p>
      <p style='margin-top:8px'><b>Refresh interval for the dashboards.</b> Suggestion 14 proposes that figures be flagged
      once they exceed an agreed age. That interval is for GAD to set, having regard to how the dashboards are used in review
      meetings.</p></div>
    <div class='box' style='margin-top:14px'><h4>What this note does not cover</h4>
      <p>The observations here are confined to the dashboard and report screens recorded in October 2026. They do not extend
      to the APAR forms themselves, to the officer's filing experience, or to the data held in the source systems, each of
      which is being taken up separately.</p></div>
    <div class='box' style='margin-top:14px'><h4>Acknowledgement</h4>
      <p>The screens reviewed represent a substantial body of work covering officer, service, instance and departmental
      levels, together with workflow creation and a set of departmental reports. The suggestions here are offered in that
      context.</p></div>
  </div>
</div>

<div class='webfoot'>MahaPAR · Observations on the SPARROW APAR dashboards · IDinsight with GAD · Draft for discussion ·
October 2026</div>
</div>

<div class='lb' id='lb' onclick='closeZoom()'><span class='close'>Close ✕</span><img id='lbimg'></div>

<script>
function filt(f){{
  document.querySelectorAll('.fchip').forEach(b=>b.classList.toggle('on',b.dataset.f===f));
  document.querySelectorAll('.card').forEach(c=>c.classList.toggle('hidden', f!=='all' && c.dataset.tier!==f));
}}
function jump(id){{
  filt('all');
  const el=document.getElementById(id);
  el.scrollIntoView({{behavior:'smooth',block:'start'}});
  el.style.boxShadow='0 0 0 3px #BFD4F6'; setTimeout(()=>el.style.boxShadow='',1400);
}}
let shots=true;
function toggleShots(){{
  shots=!shots;
  document.querySelectorAll('.shot-part').forEach(s=>s.classList.toggle('hidden',!shots));
  const b=document.getElementById('tgShots');
  b.textContent=shots?'Hide screenshots':'Show screenshots'; b.classList.toggle('on',!shots);
}}
function zoom(src){{
  document.getElementById('lbimg').src=src;
  document.getElementById('lb').classList.add('on');
}}
function closeZoom(){{document.getElementById('lb').classList.remove('on');}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeZoom();}});
</script>
</body></html>"""

open(OUT, "w").write(HTML)
print("wrote", OUT, "·", len(RECS), "suggestions")
