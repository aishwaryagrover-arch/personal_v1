#!/usr/bin/env python3
"""
Annotates the MahaPAR landing-page wireframe with our suggestions, in the
same style GAD has been using: red boxes on the element, red note in the
margin, arrow between the two.

Coordinates are in the wireframe's own pixel space (1278 x 1370); the
script offsets them onto the canvas.
"""
import base64, subprocess, os

D   = "/home/user/personal_v1/mahapar_review_assets"
SHOT = f"{D}/wf_clean.png"
OUT  = "/home/user/personal_v1/MahaPAR_landing_page_suggestions.png"

SW, SH = 1278, 1370          # wireframe size
LG, RG = 430, 560            # left and right margins for notes
PAD_T, PAD_B = 70, 40
SX, SY = LG, PAD_T           # where the wireframe sits on the canvas
CW = LG + SW + RG
CH = PAD_T + SH + PAD_B

RED = "#D92D20"

# (box on the wireframe), (note text), side, note y on canvas
NOTES = [
 dict(box=(58, 312, 712, 38), side="L", ny=300,
      title="Show the stage that is open today",
      body="“Self Appraisal · open now · closes 31 May · 14 days left”. "
           "The other four rows stay as they are — only one stage is ever live."),
 dict(box=(222, 267, 73, 21), side="L", ny=200,
      title="Typo", body="“conplete” → “complete”"),
 dict(box=(58, 428, 712, 38), side="L", ny=470,
      title="Add the right to represent",
      body="One line on this row: “The appraisal is shared with you. You may "
           "submit a representation within 15 days.” No sixth step needed."),
 dict(box=(58, 1228, 520, 64), side="L", ny=1180,
      title="Footer",
      body="“Content managed by the General Administration Department. Designed "
           "and developed by NIC Maharashtra.” Add the last-updated date, and the "
           "helpline number and support email as plain text, not only a button."),
 dict(box=(1036, 54, 64, 22), side="R", ny=120,
      title="Drop this nav item",
      body="All five deadlines are already on screen in the hero."),
 dict(box=(968, 446, 242, 70), side="R", ny=400,
      title="Don’t dead-end the people most likely to be stuck",
      body="The portal does not issue email IDs. Replace the button with one line: "
           "“No government email ID? Contact your establishment officer, or register "
           "on Parichay (SACCESS).”  Also: “goverment” → “government”."),
 dict(box=(58, 626, 1162, 32), side="R", ny=690,
      title="This describes the page; it does not carry a notice",
      body="Put the latest GR or circular here with its date — or remove the band. "
           "It is prime space below the hero."),
 dict(box=(646, 818, 584, 236), side="R", ny=870,
      title="Same card twice",
      body="“Understanding the APAR workflow” is repeated. Three cards is enough."),
 dict(box=(58, 1062, 1162, 110), side="R", ny=1060,
      title="Add three FAQs here, as drop-downs",
      body="Just three — the questions the helpdesk is actually asked, answered in a "
           "line or two each, below “A little guidance”. The full list can stay behind "
           "the FAQs tab above."),
]

b64 = base64.b64encode(open(SHOT, "rb").read()).decode()

boxes, notes, arrows = [], [], []
for i, n in enumerate(NOTES, 1):
    x, y, w, h = n["box"]
    bx, by = SX + x, SY + y
    boxes.append(f"<div class='hl' style='left:{bx}px;top:{by}px;width:{w}px;height:{h}px'></div>")
    num = f"{i} · "
    if n["side"] == "L":
        nx, nw = 24, LG - 70
        notes.append(f"<div class='note L' style='left:{nx}px;top:{n['ny']}px;width:{nw}px'>"
                     f"<b>{num}{n['title']}</b><span>{n['body']}</span></div>")
        ax1, ay1 = nx + nw, n["ny"] + 26          # from note's right edge
        ax2, ay2 = bx - 6, by + h / 2             # to box's left edge
    else:
        nx, nw = SX + SW + 34, RG - 70
        notes.append(f"<div class='note R' style='left:{nx}px;top:{n['ny']}px;width:{nw}px'>"
                     f"<b>{num}{n['title']}</b><span>{n['body']}</span></div>")
        ax1, ay1 = nx - 8, n["ny"] + 26
        ax2, ay2 = bx + w + 6, by + h / 2
    mx = (ax1 + ax2) / 2
    arrows.append(f"<path d='M {ax1} {ay1} C {mx} {ay1}, {mx} {ay2}, {ax2} {ay2}' "
                  f"fill='none' stroke='{RED}' stroke-width='2.4' marker-end='url(#a)'/>")

HTML = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{CW}px;height:{CH}px;background:#fff;position:relative;
  font-family:system-ui,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased}}
.shot{{position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;
  box-shadow:0 2px 14px rgba(0,0,0,.14)}}
.hl{{position:absolute;border:2.6px solid {RED};border-radius:7px;z-index:3}}
svg{{position:absolute;inset:0;width:{CW}px;height:{CH}px;z-index:4;pointer-events:none}}
.note{{position:absolute;z-index:5;color:{RED};line-height:1.42}}
.note.L{{text-align:right}}
.note b{{display:block;font-size:17px;font-weight:700;margin-bottom:3px}}
.note span{{display:block;font-size:14.5px;color:#B42318}}
.num{{display:inline-block;width:25px;height:25px;line-height:25px;text-align:center;
  border-radius:50%;background:{RED};color:#fff;font-size:15px;font-weight:800;margin-right:8px;
  vertical-align:middle;position:relative;top:-1px}}
.hdr{{position:absolute;left:24px;top:16px;color:#101828;font-size:19px;font-weight:700}}
.hdr span{{font-weight:400;color:#667085;font-size:14.5px;margin-left:10px}}
</style></head><body>
<div class='hdr'>MahaPAR landing page — suggestions
  <span>IDinsight · on the wireframe shared by the GAD UI team</span></div>
<img class='shot' src='data:image/png;base64,{b64}'>
{''.join(boxes)}
{''.join(notes)}
<svg><defs><marker id='a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7'
  orient='auto-start-reverse'><path d='M 0 0 L 10 5 L 0 10 z' fill='{RED}'/></marker></defs>
{''.join(arrows)}</svg>
</body></html>"""

import time
stamp=int(time.time())
html_path=f"{D}/wf_annotated_{stamp}.html"
open(html_path,"w").write(HTML)
subprocess.run([
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--disable-gpu",
    "--no-sandbox", f"--window-size={CW},{CH}", "--force-device-scale-factor=2",
    "--virtual-time-budget=6000", f"--screenshot={OUT}", html_path],
    check=True, capture_output=True)
os.remove(html_path)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
