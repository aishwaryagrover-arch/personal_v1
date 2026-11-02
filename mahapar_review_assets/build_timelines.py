#!/usr/bin/env python3
"""
Rebuilds the stakeholder timeline strips for the roles and responsibilities
document.

The originals clipped at the right edge because the nodes were laid out on a
fixed rail that ran past the page. Here each step owns an equal column and the
rail is drawn between the first and last node, so nothing can overflow however
many steps a role has. Headings are cut to two or three words, taken from the
action each step stands for.
"""
import subprocess, os

OUT = "/home/user/personal_v1/mahapar_timelines"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1760, 352                      # one strip, rendered at 2x

NAVY, INK, MUTED = "#1B3A6B", "#101828", "#5A6B85"
RAIL, PILL, PILLINK = "#C7D4E6", "#EDF2F9", "#1B3A6B"

# (file name, role title, [(step heading, timing)], footnote)
ROLES = [
 ("1_user", "User / Official reported upon", [
   ("Keep a work log", "Through the year"),
   ("Reply to memos", "By the memo date"),
   ("Check PAR details", "From 1 April"),
   ("Submit self-appraisal", "By 30 May"),
   ("Track your PAR", "Through the cycle"),
   ("Read disclosed PAR", "By 31 August"),
  ], "A representation, if any, within 15 days of disclosure. Closed PARs stay available after closure."),

 ("2_reporting", "Reporting Authority", [
   ("Issue memos", "Through the year"),
   ("Open pending PARs", "From 1 June"),
   ("Read the self-appraisal", "During June"),
   ("Record the assessment", "By 30 June"),
   ("Clear all pendency", "By 30 June"),
  ], "Inform the Custodian of leave, transfer or unavailability well before 30 June."),

 ("3_reviewing", "Reviewing Authority", [
   ("Open pending reviews", "From 1 July"),
   ("Examine the assessment", "During July"),
   ("Record the review", "By 31 July"),
   ("Clear all pendency", "By 31 July"),
  ], "Inform the Custodian of leave, transfer or unavailability well before 31 July."),

 ("4_custodian", "Custodian", [
   ("Onboard and generate PARs", "By 31 March"),
   ("Verify Part 1", "From 1 April"),
   ("Remind and follow up", "Through the cycle"),
   ("Update mapping", "As changes arise"),
   ("Disclose PARs", "1 to 31 August"),
   ("Close and report", "By 30 September"),
  ], "Track unanswered memos through the cycle. Provide closed PARs to the DPC on requisition."),

 ("5_cma", "Cadre Monitoring Authority", [
   ("Check cadre readiness", "By 31 March"),
   ("Track cadre progress", "Through the cycle"),
   ("Spot stuck offices", "Through the cycle"),
   ("Follow up with Custodians", "As required"),
   ("Escalate unresolved", "By 30 September"),
  ], "Open an individual officer's record only where a case needs to be examined."),

 ("6_sdma", "Sub Department Monitoring Authority", [
   ("Confirm readiness", "By 31 March"),
   ("Monitor offices and cadres", "Through the cycle"),
   ("Compare and prioritise", "Through the cycle"),
   ("Follow up through the CMA", "Through the cycle"),
   ("Report to GAD", "Monthly, by 30 Sept"),
  ], "Final position on the sub-department to the Super Admin by 30 September."),

 ("7_gad", "Super Admin / GAD", [
   ("Set the strength baseline", "January to March"),
   ("Check state readiness", "By 31 March"),
   ("Monitor statewide", "Through the cycle"),
   ("Direct priority action", "As required"),
   ("Decide on escalations", "After 30 September"),
  ], "Each level follows up with the level immediately below it before escalating."),
]

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{overflow:hidden}}
body{{width:{W}px;height:{H}px;background:#fff;font-family:'Segoe UI',system-ui,sans-serif;
  color:{INK};padding:26px 34px}}
h2{{font-size:22px;color:{NAVY};margin-bottom:2px}}
.sub{{font-size:14px;color:{MUTED};margin-bottom:26px}}
.track{{display:flex;align-items:flex-start;position:relative}}
.step{{flex:1;text-align:center;position:relative;padding:0 6px}}
/* the rail is drawn by each step, so it can never run past the last node */
.step::before{{content:'';position:absolute;top:19px;left:0;right:50%;height:3px;background:{RAIL}}}
.step::after{{content:'';position:absolute;top:19px;left:50%;right:0;height:3px;background:{RAIL}}}
.step:first-child::before,.step:last-child::after{{display:none}}
.num{{position:relative;z-index:2;width:40px;height:40px;border-radius:50%;background:{NAVY};color:#fff;
  font-size:18px;font-weight:700;line-height:40px;margin:0 auto}}
.lab{{font-size:16px;font-weight:700;line-height:1.25;margin-top:12px;min-height:40px}}
.pill{{display:inline-block;background:{PILL};color:{PILLINK};border-radius:999px;
  padding:5px 13px;font-size:13.5px;font-weight:600;margin-top:8px;white-space:nowrap}}
.note{{margin-top:22px;font-size:13.5px;color:{MUTED};text-align:center}}
"""


def strip(title, steps, note):
    cells = "".join(
        f"<div class='step'><div class='num'>{i}</div>"
        f"<div class='lab'>{lab}</div><div class='pill'>{when}</div></div>"
        for i, (lab, when) in enumerate(steps, 1))
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<h2>{title}</h2><div class='sub'>Main actions in sequence</div>
<div class='track'>{cells}</div>
<div class='note'>{note}</div></body></html>"""


os.makedirs(OUT, exist_ok=True)
for name, title, steps, note in ROLES:
    src = f"{OUT}/_{name}.html"
    png = f"{OUT}/timeline_{name}.png"
    open(src, "w").write(strip(title, steps, note))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    f"--window-size={W},{H}", "--force-device-scale-factor=2",
                    "--virtual-time-budget=4000", f"--screenshot={png}", src],
                   check=True, capture_output=True)
    os.remove(src)
    print("wrote", png)

# one sheet with all seven, for review and for printing
sheet = "".join(
    f"<div class='card'>{strip(t, s, n).split('<body>')[1].split('</body>')[0]}</div>"
    for _, t, s, n in ROLES)
html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>
@page{{size:A4 landscape;margin:12mm}}
{CSS}
html,body{{overflow:visible}}
body{{width:auto;height:auto;padding:0}}
.card{{border:1px solid #D9E1EC;border-radius:10px;padding:20px 24px;margin-bottom:16px;break-inside:avoid}}
h1{{font-size:24px;color:{NAVY};margin-bottom:16px}}
</style></head><body><h1>MahaPAR: stakeholder timelines</h1>{sheet}</body></html>"""
sp = f"{OUT}/_sheet.html"
open(sp, "w").write(html)
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--virtual-time-budget=6000", "--no-pdf-header-footer",
                f"--print-to-pdf=/home/user/personal_v1/MahaPAR_stakeholder_timelines.pdf", sp],
               check=True, capture_output=True)
os.remove(sp)
print("wrote /home/user/personal_v1/MahaPAR_stakeholder_timelines.pdf")
