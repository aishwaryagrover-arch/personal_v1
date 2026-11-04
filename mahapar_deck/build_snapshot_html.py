#!/usr/bin/env python3
"""
Single-file HTML showcase of the five ways to present the before/after forms.

HTML is the better medium for this than slides: a snapshot that is too dense to
read on a slide can be clicked and zoomed here, and the stage views can hold the
whole page instead of a crop. Images are embedded as base64 JPEGs so the file
travels as one attachment with nothing to link to.
"""
import base64
import io
import os

from PIL import Image

SCR = ("/tmp/claude-0/-home-user-personal-v1/"
       "9b715f77-b654-5d38-be81-49173dc191a2/scratchpad")
OUT = "/home/user/personal_v1/MahaPAR_form_snapshots.html"


def b64(path, maxw=1400, q=80, grey=False):
    """Embed an image as a base64 JPEG, downscaled to maxw to keep the file small."""
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if grey:
        im = im.convert("L").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ── images ────────────────────────────────────────────────────────────────────
SIL_OLD = [b64(f"{SCR}/crops/sil_old_{i+1}.png", maxw=320, q=72) for i in range(11)]
SIL_NEW = [b64(f"{SCR}/crops/sil_new_{i+1}.png", maxw=320, q=72) for i in range(2)]

# Full-resolution-ish stage snapshots: these are the ones people will zoom into.
STAGES = [
    dict(key="self", name="Self-appraisal",
         olab="Current · Form 1, Section 2", nlab="Form A · Part 2",
         note="The officer wrote free prose under open headings and repeated details "
              "the department already holds. Form A asks for targets against "
              "achievement, one significant contribution, and systemic factors — in "
              "set fields, with the officer's own details pre-filled."),
    dict(key="rep", name="Reporting officer",
         olab="Current · Form 1, Section 3 · 17 rated items",
         nlab="Form A · Part 3.1 · 7 dimensions",
         note="Three tables of 17 rows, each graded by hand and averaged by hand, "
              "become one table of seven dimensions with written descriptors, and "
              "MahaPAR calculates the weighted overall grade."),
    dict(key="rev", name="Reviewing officer",
         olab="Current · Form 1, Section 4B", nlab="Form A · Part 4",
         note="The reviewing officer re-graded every dimension a second time. In "
              "Form A they record agreement or disagreement with the reporting "
              "officer's overall grade and their own overall grade, with reasons "
              "required only where they differ."),
]
for st in STAGES:
    st["old"] = b64(f"{SCR}/crops/old_{st['key']}.png", maxw=1131, q=82)
    st["new"] = b64(f"{SCR}/crops/new_{st['key']}.png", maxw=1186, q=82)

PAGE6 = b64(f"{SCR}/crops/page_old06.png", maxw=1100, q=82)

# Structural stack: (label, pages in the current form, class, what happened)
OLD_PARTS = [("Part 1 · officer details, chain, leave", 2, "kept", "Kept, now pre-filled"),
             ("Part 2 · self-appraisal", 2, "simp", "Cut to about half a page"),
             ("Part 3 · reporting officer", 4, "simp", "Cut to about one page"),
             ("Part 4A · Collector / Div. Commissioner", 1, "gone",
              "Removed, subject to GAD"),
             ("Part 4B · reviewing officer", 2, "gone", "Cut to three lines")]
NEW_PARTS = [("Part 1", 0.30, "kept"), ("Part 2", 0.50, "simp"),
             ("Part 3", 0.70, "simp"), ("Part 4", 0.12, "new"),
             ("Part 5", 0.10, "new"), ("Part 6", 0.28, "new")]
UNIT = 34          # px per page of the current form


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── fragments ─────────────────────────────────────────────────────────────────
sil_old = "".join(f'<img src="{s}" alt="current form page {i+1}">'
                  for i, s in enumerate(SIL_OLD))
sil_new = "".join(f'<img src="{s}" alt="Form A page {i+1}">'
                  for i, s in enumerate(SIL_NEW))

rows2 = "".join(f"""
  <div class="row2">
    <div class="rowlab">{esc(st['name'])}</div>
    <img class="z" src="{st['old']}" alt="{esc(st['olab'])}">
    <div class="arr">&rarr;</div>
    <img class="z" src="{st['new']}" alt="{esc(st['nlab'])}">
  </div>""" for st in STAGES)

tabs = "".join(f'<button class="tab{" on" if i == 0 else ""}" data-t="{st["key"]}">'
               f'{esc(st["name"])}</button>' for i, st in enumerate(STAGES))

panes = "".join(f"""
  <section class="pane{' on' if i == 0 else ''}" id="p-{st['key']}">
    <div class="pair">
      <div class="side">
        <div class="tag old">{esc(st['olab'])}</div>
        <img class="z" src="{st['old']}" alt="{esc(st['olab'])}">
      </div>
      <div class="arr big">&rarr;</div>
      <div class="side">
        <div class="tag new">{esc(st['nlab'])}</div>
        <img class="z" src="{st['new']}" alt="{esc(st['nlab'])}">
      </div>
    </div>
    <div class="note"><b>What the audience sees</b><p>{esc(st['note'])}</p></div>
  </section>""" for i, st in enumerate(STAGES))

old_stack = "".join(f"""
  <div class="strow">
    <div class="blk {c}" style="height:{p * UNIT}px">
      <span>{esc(n)}</span><em>{p} page{'' if p == 1 else 's'}</em>
    </div>
    <div class="fate" style="height:{p * UNIT}px">{esc(f)}</div>
  </div>""" for n, p, c, f in OLD_PARTS)

new_stack = "".join(f"""
  <div class="strow">
    <div class="blk {c} thin" style="height:{max(p * UNIT, 7)}px">
      {'<span>' + esc(n) + '</span>' if p * UNIT > 20 else ''}
    </div>
    <div class="fate small" style="height:{max(p * UNIT, 7)}px">
      {'' if p * UNIT > 20 else esc(n)}</div>
  </div>""" for n, p, c in NEW_PARTS)

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MahaPAR form snapshots</title>
<style>
:root {{
  --navy:#1c3c6e; --blue:#2563eb; --red:#dc2626; --redlt:#fee2e2;
  --green:#16a34a; --greenlt:#dcfce7; --amber:#d97706; --amberlt:#fef3c7;
  --ink:#1e293b; --dim:#64748b; --line:#e2e8f0; --grey:#f8f9fb; --slate:#475569;
}}
* {{ box-sizing:border-box }}
body {{ margin:0; font:15px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--ink); background:#fff }}
header {{ background:var(--navy); color:#fff; padding:22px 40px }}
header h1 {{ margin:0; font-size:21px; letter-spacing:.2px }}
header p {{ margin:6px 0 0; color:#a9b7ce; font-size:13.5px; max-width:880px }}
nav {{ position:sticky; top:0; z-index:20; background:#fff; border-bottom:1px solid var(--line);
      padding:0 40px; display:flex; gap:26px; overflow-x:auto }}
nav a {{ padding:13px 0; color:var(--dim); text-decoration:none; font-size:13.5px;
        white-space:nowrap; border-bottom:2px solid transparent }}
nav a:hover {{ color:var(--navy); border-bottom-color:var(--navy) }}
main {{ padding:0 40px 80px }}
.opt {{ padding:34px 0; border-bottom:1px solid var(--line) }}
.opt h2 {{ margin:0 0 4px; font-size:18px; color:var(--navy) }}
.opt .sub {{ margin:0 0 20px; color:var(--dim); font-size:13.5px; max-width:920px }}
.verdict {{ margin-top:18px; font-size:13px; color:var(--dim);
           border-left:3px solid var(--line); padding-left:12px }}
.verdict b {{ color:var(--navy) }}
.tag {{ display:inline-block; padding:5px 12px; border-radius:4px; font-size:11.5px;
       font-weight:700; letter-spacing:.4px; text-transform:uppercase; margin-bottom:8px }}
.tag.old {{ background:var(--redlt); color:var(--red) }}
.tag.new {{ background:var(--greenlt); color:var(--green) }}

/* 1 silhouettes */
.sil {{ display:flex; gap:46px; align-items:flex-start; flex-wrap:wrap }}
.sil .grid {{ display:grid; grid-template-columns:repeat(4,88px); gap:8px }}
.sil.two .grid {{ grid-template-columns:repeat(2,88px) }}
.sil img {{ width:88px; border:1px solid var(--line); filter:grayscale(1) contrast(.55)
           brightness(1.12) }}
.sil .col {{ max-width:360px }}

/* 2 rows */
.row2 {{ display:grid; grid-template-columns:120px 1fr 40px 1fr; align-items:center;
        gap:12px; background:var(--grey); border:1px solid var(--line); border-radius:6px;
        padding:10px 14px; margin-bottom:10px }}
.rowlab {{ font-weight:700; color:var(--navy); font-size:13.5px }}
.row2 img {{ width:100%; max-height:120px; object-fit:contain; object-position:top;
            background:#fff; border:1px solid var(--line) }}
.arr {{ text-align:center; color:var(--blue); font-size:22px }}
.arr.big {{ font-size:30px; padding-top:60px }}

/* 3 stage panes */
.tabs {{ display:flex; gap:8px; margin-bottom:16px }}
.tab {{ border:1px solid var(--line); background:#fff; color:var(--dim); padding:8px 16px;
       border-radius:5px; font-size:13.5px; cursor:pointer }}
.tab.on {{ background:var(--navy); border-color:var(--navy); color:#fff; font-weight:600 }}
.pane {{ display:none }} .pane.on {{ display:block }}
.pair {{ display:grid; grid-template-columns:1fr 50px 1fr; gap:14px; align-items:flex-start }}
.pair img {{ width:100%; border:1px solid var(--line); background:#fff; cursor:zoom-in }}
.note {{ margin-top:16px; background:var(--grey); border:1px solid var(--line);
        border-radius:6px; padding:14px 16px }}
.note b {{ color:var(--navy); font-size:14px }}
.note p {{ margin:5px 0 0; color:var(--dim); font-size:13.5px }}

/* 4 callouts */
.cal {{ display:grid; grid-template-columns:330px 1fr; gap:26px; align-items:flex-start }}
.shot {{ position:relative }}
.shot img {{ width:100%; border:1px solid var(--line); cursor:zoom-in }}
.box {{ position:absolute; border:2px solid var(--red); border-radius:2px; pointer-events:none }}
.card {{ background:var(--grey); border:1px solid var(--line); border-radius:6px;
        padding:14px 16px; margin-bottom:12px }}
.card b {{ color:var(--navy); font-size:14px }}
.card p {{ margin:5px 0 0; color:var(--dim); font-size:13.5px }}
.catch {{ background:var(--amberlt); border:1px solid #ebc882; border-radius:6px;
         padding:13px 16px; font-size:13.5px }}
.catch b {{ color:var(--amber) }}

/* 5 structural stack */
.stacks {{ display:flex; gap:70px; flex-wrap:wrap }}
.strow {{ display:grid; grid-template-columns:270px 210px; gap:14px }}
.blk {{ border-radius:3px; margin-bottom:3px; color:#fff; padding:6px 11px;
       display:flex; flex-direction:column; justify-content:center; overflow:hidden }}
.blk span {{ font-weight:700; font-size:12.5px; line-height:1.25 }}
.blk em {{ font-style:normal; font-size:11.5px; color:#dde4ee }}
.blk.thin {{ padding:0 11px }}
.blk.kept {{ background:var(--slate) }} .blk.simp {{ background:var(--amber) }}
.blk.gone {{ background:var(--red) }}  .blk.new  {{ background:var(--green) }}
.fate {{ display:flex; align-items:center; font-size:12.5px; color:var(--dim);
        margin-bottom:3px }}
.fate.small {{ font-size:11.5px }}
.legend {{ margin-top:20px; background:var(--grey); border:1px solid var(--line);
          border-radius:6px; padding:11px 16px; font-size:12.5px; color:var(--dim) }}
.legend b {{ margin-right:14px }}
.rule {{ border-top:1px solid var(--line); margin:8px 0 6px; width:270px }}
.below {{ font-size:11.5px; color:var(--dim); font-style:italic; max-width:270px }}

/* lightbox */
#lb {{ position:fixed; inset:0; background:rgba(15,23,42,.92); display:none;
      z-index:50; overflow:auto; cursor:zoom-out; padding:28px }}
#lb.on {{ display:block }}
#lb img {{ display:block; margin:0 auto; max-width:none; width:1200px;
          background:#fff; box-shadow:0 10px 40px rgba(0,0,0,.4) }}
#lb .hint {{ position:fixed; top:12px; right:20px; color:#cbd5e1; font-size:12.5px }}
@media (max-width:900px) {{
  main, header, nav {{ padding-left:18px; padding-right:18px }}
  .pair, .cal {{ grid-template-columns:1fr }} .arr.big {{ padding:0 }}
}}
</style></head><body>

<header>
  <h1>MahaPAR · showing the form before and after</h1>
  <p>Five ways to put the current APAR form next to Form A draft v5. Click any
  snapshot to open it full size — that is the one thing a slide cannot do, and the
  reason this version exists alongside the deck.</p>
</header>

<nav>
  <a href="#o1">1 · Page silhouettes</a>
  <a href="#o2">2 · Three stages, one view</a>
  <a href="#o3">3 · One stage at a time</a>
  <a href="#o4">4 · Page with callouts</a>
  <a href="#o5">5 · Structural stack</a>
</nav>

<main>

<section class="opt" id="o1">
  <h2>Option 1 · Page silhouettes</h2>
  <p class="sub">Every page of the current form against Form A, at the same scale.
  Deliberately unreadable: the eye reads area, not text.</p>
  <div class="sil">
    <div><div class="tag old">Current · Form 1 · 11 pages</div>
      <div class="grid">{sil_old}</div></div>
    <div><div class="tag new">Form A · 2 pages</div>
      <div class="sil two"><div class="grid">{sil_new}</div></div></div>
    <div class="col">
      <div class="card"><b>What this does well</b>
        <p>The scale of the cut is unmistakable in one look, and nothing pretends to
        be legible. Works for the whole form, for either group.</p></div>
      <div class="card"><b>What it cannot do</b>
        <p>It says nothing about what changed inside the form.</p></div>
    </div>
  </div>
  <p class="verdict"><b>Verdict:</b> best for the whole-form view; pairs with a slide
  that explains the content.</p>
</section>

<section class="opt" id="o2">
  <h2>Option 2 · All three stages in one view</h2>
  <p class="sub">On a slide this fails — nothing is readable. In HTML it works as a
  contact sheet: click any snapshot to open it full size.</p>
  {rows2}
  <p class="verdict"><b>Verdict:</b> unusable on a slide, useful here as an index into
  the full snapshots.</p>
</section>

<section class="opt" id="o3">
  <h2>Option 3 · One stage at a time, whole snapshot</h2>
  <p class="sub">The complete before and after for each stage, not a crop. This is the
  version that became three separate slides in the deck.</p>
  <div class="tabs">{tabs}</div>
  {panes}
  <p class="verdict"><b>Verdict:</b> the only option where the audience can actually read
  the change.</p>
</section>

<section class="opt" id="o4">
  <h2>Option 4 · Full page with callout zooms</h2>
  <p class="sub">One page of the current form, with the two blocks that changed most
  marked and explained beside it.</p>
  <div class="cal">
    <div>
      <div class="shot">
        <img src="{PAGE6}" alt="Current Form 1, page 6">
        <div class="box" style="left:7%; top:13%; width:86%; height:22%"></div>
        <div class="box" style="left:7%; top:48%; width:86%; height:34%"></div>
      </div>
      <div class="tag old" style="margin-top:8px">Current · Form 1, page 6 of the form</div>
    </div>
    <div>
      <div class="card"><b>Work completion · 3 items, graded and averaged by hand</b>
        <p>In Form A this becomes dimensions 1 and 2, and MahaPAR does the arithmetic.
        Two of the three items collapse into &lsquo;delivery of planned work&rsquo;.</p></div>
      <div class="card"><b>Personal attributes · 8 items</b>
        <p>Overall bearing, emotional stability, moral courage and leadership are judged
        separately today. Form A folds them into two dimensions with written descriptors
        behind each.</p></div>
      <div class="catch"><b>The catch:</b> the callouts carry the message, not the page.
      The page behind them is decoration, and a bilingual form needs each callout
      translated to be useful.</div>
    </div>
  </div>
  <p class="verdict"><b>Verdict:</b> familiar consulting device, but the page itself does
  no work.</p>
</section>

<section class="opt" id="o5">
  <h2>Option 5 · Structural stack, no screenshot at all</h2>
  <p class="sub">Block height is proportional to the real length of each part, so the
  volume claim is made without asking anyone to read a form.</p>
  <div class="stacks">
    <div><div class="tag old">Current · Form 1 · 11 pages</div>{old_stack}</div>
    <div><div class="tag new">Form A · 2 pages</div>{new_stack}
      <div class="rule"></div>
      <div class="below">Everything below this line is new ground the old form never
      covered.</div></div>
  </div>
  <div class="legend"><b style="color:var(--slate)">Kept</b>
    <b style="color:var(--amber)">Simplified</b>
    <b style="color:var(--red)">Removed</b>
    <b style="color:var(--green)">New in Form A</b>
    Block height is proportional to the real length of each part.</div>
  <p class="verdict"><b>Verdict:</b> readable, shows volume and shows what happened to
  each part.</p>
</section>

</main>

<div id="lb"><div class="hint">click anywhere to close</div><img alt=""></div>

<script>
// stage tabs
document.querySelectorAll('.tab').forEach(function (b) {{
  b.onclick = function () {{
    document.querySelectorAll('.tab').forEach(function (x) {{ x.classList.remove('on'); }});
    document.querySelectorAll('.pane').forEach(function (x) {{ x.classList.remove('on'); }});
    b.classList.add('on');
    document.getElementById('p-' + b.dataset.t).classList.add('on');
  }};
}});

// click any snapshot to open it full size
var lb = document.getElementById('lb'), lbi = lb.querySelector('img');
document.querySelectorAll('.z, .shot img').forEach(function (im) {{
  im.onclick = function () {{ lbi.src = im.src; lb.classList.add('on'); }};
}});
lb.onclick = function () {{ lb.classList.remove('on'); lbi.src = ''; }};
document.addEventListener('keydown', function (e) {{
  if (e.key === 'Escape') {{ lb.classList.remove('on'); lbi.src = ''; }}
}});
</script>
</body></html>
"""

with open(OUT, "w") as f:
    f.write(HTML)
print("wrote", OUT, "·", round(os.path.getsize(OUT) / 1e6, 2), "MB")
