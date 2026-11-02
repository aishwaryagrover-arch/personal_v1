#!/usr/bin/env python3
"""
Stakeholder timeline strips, in the style of the GAD set, rebuilt for
legibility: larger headings, the gap between the heading and the rail closed
up, and rendered at 3x so the text stays sharp when the strip is scaled down
into the document.
"""
import subprocess, os

OUT = "/home/user/personal_v1/mahapar_timelines"
PDF = "/home/user/personal_v1/MahaPAR_stakeholder_timelines.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1600, 300
SCALE = 3                                   # render factor; keeps small text sharp

INK = "#0F1F45"
RAIL = "#1D7AF3"

# tone: circle fill, icon stroke, pill fill, pill text
TONES = [("#E3EFFD", "#1D7AF3", "#E3EFFD"),
         ("#E0F3E9", "#0E9F6E", "#E0F3E9"),
         ("#FBF0D8", "#C98A10", "#FBF0D8"),
         ("#EFE9FA", "#7C5BD9", "#EFE9FA")]

I = {
 "people": "<circle cx='9' cy='9' r='2.6'/><circle cx='17.5' cy='9.5' r='2'/><path d='M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5'/><path d='M16 14.5c2.4 0 4.5 1.7 4.5 4.5'/>",
 "chart": "<path d='M4 20V11'/><path d='M10 20V5'/><path d='M16 20v-6'/><path d='M21 20H3'/>",
 "search": "<circle cx='11' cy='11' r='6.5'/><path d='M16 16l4.5 4.5'/>",
 "alert": "<path d='M12 3.5 22 20H2z'/><path d='M12 10v4.5'/><circle cx='12' cy='17.3' r='.9' fill='currentColor' stroke='none'/>",
 "doc": "<rect x='5' y='3' width='14' height='18' rx='2'/><path d='M8.5 8h7M8.5 12h7M8.5 16h4'/>",
 "pen": "<path d='M5 3h9l5 5v13H5z'/><path d='M8.5 12h5M8.5 16h3'/><path d='M17 11.5 20.5 15 16 19.5l-3.5-3.5z' fill='none'/>",
 "check": "<circle cx='12' cy='12' r='8.5'/><path d='m8 12 2.8 2.8L16.2 9.4'/>",
 "flag": "<path d='M6 21V4'/><path d='M6 5h11l-2 3.5L17 12H6z'/>",
 "calendar": "<rect x='3.5' y='5' width='17' height='15' rx='2'/><path d='M3.5 10h17M8 3.5v3M16 3.5v3'/>",
 "tree": "<rect x='9' y='3' width='6' height='4.5' rx='1'/><rect x='3' y='16' width='6' height='4.5' rx='1'/><rect x='15' y='16' width='6' height='4.5' rx='1'/><path d='M12 7.5v4M6 16v-4.5h12V16'/>",
 "clock": "<circle cx='12' cy='12' r='8.5'/><path d='M12 7v5.2l3.2 2'/>",
 "send": "<path d='M4 12 20.5 4.5 15 20.5l-3-7z'/><path d='m12 13.5 8.5-9'/>",
}

# name, title, [(icon, heading, timing)]
ROLES = [
 ("1_user", "User / Official reported upon", [
   ("doc",      "Record work through the year",            "Throughout the year"),
   ("send",     "Respond to memos received",               "By the memo date"),
   ("check",    "Check PAR details and mapped authorities", "From 1 April"),
   ("pen",      "Complete and submit the self-appraisal",  "By 30 May"),
   ("search",   "Track the PAR through each stage",        "Throughout the cycle"),
   ("flag",     "Read the disclosed PAR and represent",    "By 31 August"),
  ]),

 ("2_reporting", "Reporting Authority", [
   ("doc",   "Issue memos where performance or conduct needs improvement", "Throughout the year"),
   ("pen",   "Review self-appraisals and assess performance",              "By 30 June"),
   ("flag",  "Flag planned leave or transfer",                             "Before 30 June"),
  ]),

 ("3_reviewing", "Reviewing Authority", [
   ("doc",   "Review assigned PARs",                                  "By 31 July"),
   ("check", "Confirm the overall grade, record any disagreement",    "By 31 July"),
   ("flag",  "Flag planned leave or transfer",                        "Before 31 July"),
  ]),

 ("4_custodian", "Custodian", [
   ("people",   "Onboard officers and generate PARs",        "By 31 March"),
   ("check",    "Verify Part 1 and correction requests",     "From 1 April"),
   ("clock",    "Send reminders and follow up on pendency",  "Throughout the cycle"),
   ("tree",     "Update mapping when postings change",       "As changes arise"),
   ("send",     "Disclose completed PARs",                   "1 to 31 August"),
   ("alert",    "Close all PARs and report unresolved cases", "By 30 September"),
  ]),

 ("5_cma", "Cadre Monitoring Authority (CMA)", [
   ("people",  "Ensure all cadre officers are onboarded",         "By 31 March"),
   ("chart",   "Monitor PAR progress across the cadre",           "Throughout the cycle"),
   ("search",  "Identify pendency and follow up with Custodians", "Throughout the cycle"),
   ("alert",   "Escalate unresolved issues",                      "As required"),
  ]),

 ("6_sdma", "Sub Department Monitoring Authority (SDMA)", [
   ("people", "Ensure all sub-department officers are onboarded",  "By 31 March"),
   ("chart",  "Monitor PAR progress across the sub-department",    "Throughout the cycle"),
   ("search", "Identify pendency and follow up with CMAs",         "Throughout the cycle"),
   ("alert",  "Escalate persistent issues to GAD",                 "As required"),
  ]),

 ("7_gad", "Super Admin / GAD", [
   ("calendar", "Notify departments of APAR timelines",        "By 31 March"),
   ("chart",    "Monitor statewide PAR progress",              "Throughout the cycle"),
   ("tree",     "Direct action on pendency through the SDMAs", "As required"),
   ("alert",    "Resolve escalated issues",                    "As required"),
  ]),
]


def icon(name, colour):
    return (f"<svg viewBox='0 0 24 24' width='34' height='34' fill='none' stroke='{colour}' "
            f"stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round' "
            f"style='color:{colour}'>{I[name]}</svg>")


CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{overflow:hidden}}
.wrap{{display:flow-root}}
body{{width:{W}px;height:{H}px;background:#fff;color:{INK};padding:14px 30px 0;
 font-family:'Segoe UI Semibold','Segoe UI',system-ui,-apple-system,sans-serif;
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
.track{{display:flex;align-items:flex-start}}
.step{{flex:1;padding:0 10px;text-align:center;position:relative}}
.ico{{width:62px;height:62px;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center}}
.lab{{font-size:19px;font-weight:700;line-height:1.24;margin-top:9px;letter-spacing:-.1px;min-height:48px}}
.rail{{position:relative;height:26px;margin-top:10px}}
.rail .line{{position:absolute;top:11px;left:0;right:0;height:4px;background:{RAIL};border-radius:2px}}
.rail .tip{{position:absolute;top:4px;right:-13px;width:0;height:0;
 border-left:15px solid {RAIL};border-top:9px solid transparent;border-bottom:9px solid transparent}}
.dot{{position:absolute;top:5px;width:16px;height:16px;border-radius:50%;background:#fff;
 border:4px solid {RAIL};transform:translateX(-50%)}}
.pills{{display:flex;margin-top:9px}}
.pill{{flex:1;padding:0 10px;text-align:center}}
.pill span{{display:inline-block;border-radius:999px;padding:9px 20px;font-size:17px;font-weight:700;color:{INK};white-space:nowrap}}
"""


def strip(steps):
    n = len(steps)
    cells, dots, pills = "", "", ""
    for i, (ic, lab, when) in enumerate(steps):
        c, s, p = TONES[i % len(TONES)]
        cells += (f"<div class='step'><div class='ico' style='background:{c}'>{icon(ic, s)}</div>"
                  f"<div class='lab'>{lab}</div></div>")
        pos = (i + 0.5) * 100 / n
        dots += f"<div class='dot' style='left:{pos:.3f}%'></div>"
        pills += f"<div class='pill'><span style='background:{p}'>{when}</span></div>"
    return (f"<div class='track'>{cells}</div>"
            f"<div class='rail'><div class='line'></div>{dots}<div class='tip'></div></div>"
            f"<div class='pills'>{pills}</div>")


def page(body):
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


os.makedirs(OUT, exist_ok=True)
for name, title, steps in ROLES:
    src, png = f"{OUT}/_{name}.html", f"{OUT}/timeline_{name}.png"
    open(src, "w").write(page(strip(steps)))
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    f"--window-size={W},{H}", f"--force-device-scale-factor={SCALE}",
                    "--virtual-time-budget=4000", f"--screenshot={png}", src],
                   check=True, capture_output=True)
    os.remove(src)
    print("wrote", png)

sheet = "".join(f"<div class='card'><h2>{t}</h2>{strip(s)}</div>" for _, t, s in ROLES)
html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>
@page{{size:A4 landscape;margin:11mm}}
{CSS}
html,body{{overflow:visible}}
body{{width:auto;height:auto;padding:0}}
h1{{font-size:26px;margin-bottom:14px}}
h2{{font-size:20px;margin-bottom:10px}}
.card{{border:1px solid #DCE4F0;border-radius:12px;padding:16px 20px 20px;margin-bottom:14px;break-inside:avoid}}
</style></head><body><h1>MahaPAR: stakeholder timelines</h1>{sheet}</body></html>"""
sp = f"{OUT}/_sheet.html"
open(sp, "w").write(html)
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--virtual-time-budget=6000", "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}", sp], check=True, capture_output=True)
os.remove(sp)
print("wrote", PDF)
