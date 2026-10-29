#!/usr/bin/env python3
"""
Turns the annexure HTML into a version Google Docs converts cleanly.

Docs drops class-based CSS on import, so the table rules, header fill and
cell padding have to ride on each element as inline attributes.
"""
import re

SRC = "/home/user/personal_v1/MahaPAR_APAR_roles_and_responsibilities.html"
OUT = "/tmp/claude-0/-home-user-personal-v1/9b715f77-b654-5d38-be81-49173dc191a2/scratchpad/roles_gdoc.html"

NAVY, FILL = "#1B3A6B", "#CBD9EC"
TD = 'style="vertical-align:top"'
TH = f'bgcolor="{FILL}" style="background-color:{FILL};color:{NAVY};text-align:left"' 

h = open(SRC).read()
h = re.sub(r"<style>.*?</style>", "", h, flags=re.S)          # class CSS is dropped on import anyway
h = h.replace('<div class="pb"></div>', "")                    # page breaks come from the Docs layout

h = h.replace("<table>", '<table border="1" cellspacing="0" cellpadding="5" '
                         'style="border-collapse:collapse;width:100%">')
h = re.sub(r'<table style="[^"]*">',
           '<table border="1" cellspacing="0" cellpadding="5" '
           'style="border-collapse:collapse;width:100%">', h)

h = re.sub(r"<(th|td)\b([^>]*)>", lambda m: f"<{m.group(1)} {TH if m.group(1) == 'th' else TD}>", h)

h = h.replace('<h1>', f'<h1 style="color:{NAVY};text-align:center">')
h = re.sub(r"<h2([^>]*)>", lambda m: f'<h2{m.group(1)} style="color:{NAVY}">', h)
h = re.sub(r"<h3([^>]*)>", lambda m: f'<h3{m.group(1)} style="color:{NAVY}">', h)
h = h.replace('<p class="sub">', '<p style="text-align:center">')
h = re.sub(r'<p class="scope">(.*?)</p>', r'<p><i>\1</i></p>', h, flags=re.S)
h = re.sub(r'<p class="count">(.*?)</p>', r'<p><b>\1</b></p>', h, flags=re.S)
h = h.replace('<div class="lead">', f'<div style="border:1px solid {NAVY};padding:10px">')

open(OUT, "w").write(h)
print(OUT, len(h), "bytes")
