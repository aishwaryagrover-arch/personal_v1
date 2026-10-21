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
 dict(box=(58, 312, 712, 38), side="L", ny=330,
      title="Could the stage that is live today be marked?",
      body="Something like “Self Appraisal · live now · closes 31 May · 14 days left”. "
           "The other four rows could stay exactly as they are. Only one stage is live at "
           "any time, and that is the one piece of information most officials come for."),
 dict(box=(222, 267, 73, 21), side="L", ny=200,
      title="Two small typos",
      body="“conplete” → “complete” in this line, and “goverment” → “government” "
           "in the sign-in card."),
 dict(box=(58, 626, 1162, 32), side="R", ny=620,
      title="Could this band carry the live deadline and the help centre contact?",
      body="The stage that is currently open with its closing date, and the help centre "
           "number and email for anyone who is stuck. At present the band describes the "
           "page rather than carrying anything an official can act on."),
 dict(box=(58, 1062, 1162, 110), side="R", ny=1020,
      title="Can we explore a short FAQ section here?",
      body="The top three only, as drop-downs, matching the three things an official most "
           "often needs to do. For example how to fill the self-appraisal, and how to create "
           "a Parichay SSO ID for those who do not have one. We can decide the three "
           "together. The fuller list can stay behind the FAQs tab above, but that tab is "
           "not easy to spot, so having the top three in the main view would help."),
 dict(box=(655, 1230, 262, 52), side="R", ny=1190,
      title="Could the footer also carry related portals?",
      body="In addition to “Explore MahaPAR”, a second set of links on its right for the "
           "related portals, Maha HRMS and the promotion portal."),
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
<div class='hdr'>MahaPAR landing page: suggestions
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
