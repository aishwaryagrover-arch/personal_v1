#!/usr/bin/env python3
"""
IDinsight HTML-fidelity PPTX component library.

A reusable set of python-pptx recipes that reproduce the dense, well-structured
"HTML deck" look inside the branded IDinsight template — fully editable output.

Design principles
------------------
1. Tokens mirror the template THEME (which already encodes the IDinsight brand):
   accent1=#1C2F62, accent2=#A8CCEB, accent3=#0F4D42, accent4=#D49E00, lt2=#F2F2F5.
2. The HTML "slide" is 960x540 px; the PPTX slide is 10" x 5.62".
   960 px == 10 in, so 1 px == 9525 EMU exactly  ->  port HTML geometry 1:1.
3. Build content on a white canvas + hand-placed components (full design control),
   and draw the IDinsight chrome (header band + wordmark + slide number) ourselves
   so it matches the template's native content layouts.
4. Font is Inter everywhere (theme font; embedded in template; a Google Font, so it
   survives the Google Slides round-trip). Kill inherited shadows on every shape.
5. Editable structure: when a coloured shape carries text, the text lives in that
   shape's OWN text frame (see `shape_text`) — never a separate textbox stacked on
   top. This means one click selects the whole block in PowerPoint. `canvas()`
   uses a real slide background (`p:bg`), not a full-slide rectangle, so nothing
   traps clicks over the deck. See "Editable structure" section of SKILL.md.

Every function returns the shape(s) it created so callers can fine-tune.
"""
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

# ── DESIGN TOKENS (== template theme / branding skill) ──────────────
DB   = RGBColor(0x1C, 0x2F, 0x62)   # dark blue (hero / accent1)
DB2  = RGBColor(0x26, 0x4D, 0x96)   # blue 2
DB3  = RGBColor(0x54, 0x80, 0xD6)   # mid blue (accents)
S2C  = RGBColor(0x74, 0x8E, 0xBE)   # muted mid-blue
LB   = RGBColor(0xA8, 0xCC, 0xEB)   # light blue (rules / accent2)
PB   = RGBColor(0xDE, 0xE5, 0xF7)   # pale blue (callout bg)
E8   = RGBColor(0xE8, 0xEC, 0xF4)   # bluish tint
DG   = RGBColor(0x21, 0x2E, 0x38)   # body text (dk1)
MG   = RGBColor(0x6B, 0x72, 0x80)   # subtitle / caption grey
LG   = RGBColor(0xF2, 0xF2, 0xF5)   # light grey zone bg (lt2)
BORDER = RGBColor(0xE0, 0xE5, 0xEF) # hairline card border
WH   = RGBColor(0xFF, 0xFF, 0xFF)
GR   = RGBColor(0x0F, 0x4D, 0x42)   # green (checks / accent3)
LGR  = RGBColor(0xAB, 0xE5, 0xBF)   # light green
AM   = RGBColor(0xD4, 0x9E, 0x00)   # amber (warnings / accent4)
AML  = RGBColor(0xFF, 0xF0, 0xC2)   # amber light (warn bg)
FONT = "Inter"

# Type scale (pt) — denser than PPTX defaults, floored for legibility
T_TITLE_HERO = 30; T_TITLE = 16; T_SUB = 8.5; T_BANDHEAD = 8
T_CARDTITLE = 10; T_BODY = 8; T_QUOTE = 7.5; T_LABEL = 7; T_STAT = 30; T_NUM = 8

# Layout grid (px)
MARGIN = 32; CONTENT_W = 896; GAP = 12
def col_w(n): return (CONTENT_W - (n - 1) * GAP) / n
def col_x(i, n): return MARGIN + i * (col_w(n) + GAP)

PXE = 9525
def X(px): return Emu(int(round(px * PXE)))

# ── PRIMITIVES ──────────────────────────────────────────────────────
def _radius(sp, frac):
    try: sp.adjustments[0] = frac
    except Exception: pass

def rect(slide, x, y, w, h, fill=None, line=None, line_w=0.75,
         shape=MSO_SHAPE.RECTANGLE, radius=None):
    sp = slide.shapes.add_shape(shape, X(x), X(y), X(w), X(h))
    if radius is not None: _radius(sp, radius)
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    return sp

def text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=2, line_spacing=None, wrap=True):
    """paras: list of paragraphs; each = list of (txt, size, color, bold, italic)."""
    tb = slide.shapes.add_textbox(X(x), X(y), X(w), X(h))
    tf = tb.text_frame; tf.word_wrap = wrap; tf.vertical_anchor = anchor
    for m in ("left", "right", "top", "bottom"): setattr(tf, f"margin_{m}", 0)
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_before = Pt(0); p.space_after = Pt(space_after)
        if line_spacing: p.line_spacing = line_spacing
        for run in para:
            t, sz, col, bold, ital = run
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.name = FONT
            r.font.color.rgb = col; r.font.bold = bold; r.font.italic = ital
    return tb

def _r(t, sz, col, bold=False, ital=False): return (t, sz, col, bold, ital)

def shape_text(shape, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE,
               space_after=2, line_spacing=None, wrap=True,
               m_left=6, m_right=6, m_top=2, m_bottom=2):
    """Write text into a SHAPE's OWN text frame — the correct pattern for text
    that lives inside a coloured card/box/band. Result: one click in PowerPoint
    selects the whole block; dragging moves shape + text together.

    `paras` is the same list-of-paragraphs format as `text()`. Anchor defaults
    to MIDDLE so text sits centred vertically inside the shape.
    Margins are in px (converted to EMU) — small defaults keep text off the
    shape edge without eating into a tight card.
    """
    tf = shape.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = X(m_left); tf.margin_right = X(m_right)
    tf.margin_top = X(m_top); tf.margin_bottom = X(m_bottom)
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        # clear any inherited run on the first paragraph
        if i == 0:
            for r in list(p.runs): r._r.getparent().remove(r._r)
        p.alignment = align; p.space_before = Pt(0); p.space_after = Pt(space_after)
        if line_spacing: p.line_spacing = line_spacing
        for run in para:
            t, sz, col, bold, ital = run
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.name = FONT
            r.font.color.rgb = col; r.font.bold = bold; r.font.italic = ital
    return shape

# ── CHROME ──────────────────────────────────────────────────────────
_A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
_P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"

def canvas(slide, color=WH):
    """Set a REAL slide background (p:bg). This does NOT paint a full-slide
    rectangle on top of the slide — a rectangle would trap every click and
    prevent selecting anything beneath it in PowerPoint. A real background
    sits below all shapes and never intercepts selection.

    Use for any slide built on the Blank layout (which is dark navy by
    default) or when you need a specific slide background colour.
    """
    hex_ = f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"
    cSld = slide._element.find(qn('p:cSld'))
    old = cSld.find(qn('p:bg'))
    if old is not None: cSld.remove(old)
    cSld.insert(0, parse_xml(
        f'<p:bg xmlns:p="{_P_NS}" xmlns:a="{_A_NS}"><p:bgPr>'
        f'<a:solidFill><a:srgbClr val="{hex_}"/></a:solidFill>'
        f'<a:effectLst/></p:bgPr></p:bg>'))

def header_band(slide, wordmark="IDinsight"):
    band = rect(slide, 0, 0, 960, 52, fill=DB)
    shape_text(band, [[_r(wordmark, 11, WH, True)]],
               align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
               m_right=28, m_left=0)

def title_block(slide, title, subtitle="", sub_color=MG):
    text(slide, MARGIN, 64, CONTENT_W, 30, [[_r(title, T_TITLE, DB, True)]])
    if subtitle:
        text(slide, MARGIN, 92, CONTENT_W, 16, [[_r(subtitle, T_SUB, sub_color, ital=True)]])
    rect(slide, MARGIN, 112, CONTENT_W, 3, fill=LB, radius=0.5)

def slide_number(slide, n):
    text(slide, 0, 516, 944, 14, [[_r(str(n), T_NUM, MG)]], align=PP_ALIGN.RIGHT)

def content_slide(prs, blank_layout, title, subtitle="", n=None, sub_color=MG):
    s = prs.slides.add_slide(blank_layout)
    canvas(s); header_band(s); title_block(s, title, subtitle, sub_color)
    if n is not None: slide_number(s, n)
    return s

# ── COMPONENTS ──────────────────────────────────────────────────────
def zone_column(slide, x, y, w, h, head, head_bg, head_fg, body_bg, body_radius=0.06):
    """Two-tone colored zone: dark header band + light tinted body. Returns body box."""
    rect(slide, x, y, w, h, fill=body_bg, radius=body_radius)
    hh = 30
    band = rect(slide, x, y, w, hh, fill=head_bg,
                shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, radius=0.18)
    shape_text(band, [[_r(head, T_BANDHEAD, head_fg, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=12, m_right=12)
    return (x, y+hh, w, h-hh)   # inner content region

def quote_card(slide, x, y, w, h, quote, accent=DB):
    card = rect(slide, x, y, w, h, fill=WH, radius=0.08)
    rect(slide, x, y, 3, h, fill=accent)               # left accent bar (own shape)
    shape_text(card, [[_r(quote, T_QUOTE, DG, ital=True)]],
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.18,
               m_left=10, m_right=8, m_top=5, m_bottom=5)

def info_card(slide, x, y, w, h, header, title, header_bg=DB, header_fg=WH):
    """Bordered white card with a colored top band + bold title. Returns inner-body top y."""
    rect(slide, x, y, w, h, fill=WH, line=BORDER, line_w=0.75, radius=0.05)
    band = rect(slide, x, y, w, 26, fill=header_bg,
                shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, radius=0.2)
    shape_text(band, [[_r(header, 8.5, header_fg, True)]],
               anchor=MSO_ANCHOR.MIDDLE, m_left=12, m_right=12)
    # title sits at an offset below the band — legitimate separate textbox
    text(slide, x+12, y+34, w-24, 18, [[_r(title, T_CARDTITLE, DB, True)]])
    return y + 56

def checklist(slide, x, y, w, items, mark="✓", mark_col=GR, gap=25, size=T_BODY):
    cy = y
    for it in items:
        text(slide, x, cy, w, 24, [[_r(mark+"  ", 9, mark_col, True), _r(it, size, DG)]], line_spacing=1.1)
        cy += gap
    return cy

def example_box(slide, x, y, w, h, label, body):
    box = rect(slide, x, y, w, h, fill=LG, radius=0.06)
    shape_text(box,
               [[_r(label, T_LABEL, MG, True)],
                [_r(body, T_QUOTE, DG, ital=True)]],
               anchor=MSO_ANCHOR.TOP, line_spacing=1.18, space_after=3,
               m_left=8, m_right=8, m_top=7, m_bottom=5)

def step_box(slide, x, y, w, h, header, title, question, formula_lines, color):
    rect(slide, x, y, w, h, fill=LG, radius=0.05)
    rect(slide, x, y, w, 24, fill=color, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, radius=0.2)
    text(slide, x+12, y, w-24, 24, [[_r(header, 9, WH, True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(slide, x+12, y+30, w-24, 16, [[_r(title, 9.5, color, True)]])
    text(slide, x+12, y+48, w-24, 42, [[_r(question, T_BODY, MG, ital=True)]], line_spacing=1.2)
    rect(slide, x+12, y+94, w-24, 2, fill=LB)
    fy = y+104
    rect(slide, x, fy, w, (y+h)-fy, fill=color)
    text(slide, x+10, fy, w-20, (y+h)-fy, [[_r(l, 8.5, WH, True)] for l in formula_lines],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.25, space_after=3)

def stat_callout(slide, x, y, w, h, stat, label, accent=DB, fill=LG):
    box = rect(slide, x, y, w, h, fill=fill, radius=0.06)
    rect(slide, x, y, w, 4, fill=accent, radius=0.0)            # top accent strip
    shape_text(box,
               [[_r(stat, T_STAT, accent, True)],
                [_r(label, T_BODY, DG)]],
               anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15, space_after=6,
               m_left=10, m_right=10, m_top=14, m_bottom=10)

def ladder_rung(slide, x, y, w, h, badge, title, desc, color):
    rect(slide, x, y, w, h, fill=WH, line=BORDER, line_w=0.75, radius=0.08)
    rect(slide, x, y, 64, h, fill=color, shape=MSO_SHAPE.ROUND_1_RECTANGLE, radius=0.1)
    text(slide, x, y, 64, h, [[_r(badge, 12, WH, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(slide, x+76, y+8, w-86, 16, [[_r(title, 10, DB, True)]])
    text(slide, x+76, y+26, w-86, h-30, [[_r(desc, T_QUOTE, DG)]], line_spacing=1.18)

def badge_block(slide, x, y, w, h, num, name, sub, question, delta_title, delta_desc, color):
    rect(slide, x, y, w, h, fill=LG, radius=0.06)
    rect(slide, x+12, y+12, 22, 22, fill=color, shape=MSO_SHAPE.OVAL)
    text(slide, x+12, y+12, 22, 22, [[_r(num, 11, WH, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(slide, x+40, y+13, w-50, 20, [[_r(name, 11, DB, True)]])
    text(slide, x+12, y+40, w-24, 14, [[_r(sub, T_LABEL, MG, True)]])
    rect(slide, x+12, y+56, w-24, 2, fill=LB)
    text(slide, x+12, y+64, w-24, h-130, [[_r(question, T_QUOTE, DG)]], line_spacing=1.2)
    df = y + h - 56
    rect(slide, x, df, w, 56, fill=color)
    text(slide, x+10, df+8, w-20, 40,
         [[_r(delta_title, T_LABEL, WH, True)], [_r(delta_desc, 7, WH)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)

def comparison_table(slide, x, y, w, h, col_headers, rows, label_w=150,
                     head_colors=(LG, DB, S2C), head_fgs=(MG, WH, WH)):
    """rows: list of (label, [cell_para_or_str, ...]). Cells may be a string or a
    list-of-paragraphs (for rich content). col_headers[0] is the empty corner."""
    ncol = len(col_headers)
    data_w = w - label_w
    cw = data_w / (ncol - 1)
    rh_head = 26
    # header row
    rect(slide, x, y, label_w, rh_head, fill=head_colors[0])
    for j in range(1, ncol):
        cx = x + label_w + (j-1)*cw
        rect(slide, cx, y, cw, rh_head, fill=head_colors[j])
        text(slide, cx+10, y, cw-20, rh_head, [[_r(col_headers[j], 11, head_fgs[j], True)]], anchor=MSO_ANCHOR.MIDDLE)
    ry = y + rh_head
    body_h = h - rh_head
    rh = body_h / len(rows)
    for i, (lab, cells) in enumerate(rows):
        lbg = LG if i % 2 else RGBColor(0xFA,0xFA,0xFB)
        rect(slide, x, ry, label_w, rh, fill=lbg, line=BORDER, line_w=0.5)
        text(slide, x+10, ry+8, label_w-20, rh-12, [[_r(lab, 9, DB, True)]], line_spacing=1.1)
        for j, cell in enumerate(cells):
            cx = x + label_w + j*cw
            cbg = (E8 if (j==1) else RGBColor(0xFB,0xFC,0xFE)) if i % 2 else (PB if (j==1) else WH)
            rect(slide, cx, ry, cw, rh, fill=cbg, line=BORDER, line_w=0.5)
            if isinstance(cell, str):
                text(slide, cx+10, ry+8, cw-20, rh-12, [[_r(cell, 8, DG)]], line_spacing=1.25)
            else:
                text(slide, cx+10, ry+8, cw-20, rh-12, cell, line_spacing=1.2, space_after=2)
        ry += rh

def accent_bar_list(slide, x, y, w, items, bar=DB, gap=4, item_h=46):
    """items: list of (title, desc). White rows with a thick left accent bar."""
    cy = y
    for title, desc in items:
        row = rect(slide, x, cy, w, item_h, fill=LG, radius=0.05)
        rect(slide, x, cy, 5, item_h, fill=bar)                     # accent stripe
        shape_text(row,
                   [[_r(title, 9.5, DB, True)],
                    [_r(desc, T_BODY, DG)]],
                   anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15, space_after=2,
                   m_left=16, m_right=10, m_top=7, m_bottom=5)
        cy += item_h + gap
    return cy

def callout_bar(slide, x, y, w, h, lead, body, kind="info"):
    if kind == "warn":
        bar = rect(slide, x, y, w, h, fill=AML, radius=0.1)
        rect(slide, x, y, 4, h, fill=AM)                            # accent stripe
        runs = [[_r(lead, 8, DG, True), _r(body, 8, DG, ital=True)]]
    else:
        bar = rect(slide, x, y, w, h, fill=PB, radius=0.12)
        runs = [[_r(lead, 8, DB, True), _r(body, 8, DG)]]
    shape_text(bar, runs, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1,
               m_left=14, m_right=12)

def flow_node(slide, x, y, w, h, lines, fill, fg=WH, sizes=None):
    node = rect(slide, x, y, w, h, fill=fill, radius=0.1)
    if sizes is None: sizes = [11]*len(lines)
    shape_text(node,
               [[_r(l, sizes[i], fg, i==0)] for i, l in enumerate(lines)],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
               line_spacing=1.15, m_left=6, m_right=6)

def arrow(slide, x, y, w, h, color=MG):
    text(slide, x, y, w, h, [[_r("→", 16, color, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ── REAL TABLES ─────────────────────────────────────────────────────
def real_table(slide, x, y, w, h, header, rows, col_widths=None,
               header_fill=DB, header_fg=WH, body_fg=DG,
               zebra=None, hdr_pt=9, body_pt=8):
    """Build a REAL PowerPoint table (one graphicFrame holding an a:tbl) — use
    when the content is genuine tabular data (connected rows and columns of
    related data with a header). The user can then insert/delete rows, resize
    columns, and restyle the header in one action; cells stay aligned.

    Do NOT use for layouts that only LOOK table-ish — KPI tile rows, comparison
    cards, box-and-arrow flows. Build those with shapes + shape_text (see
    `comparison_table` for a rich-content grid alternative).

    header:  list[str] — one label per column.
    rows:    list[list[str]] — one string per cell, matching header length.
    col_widths: optional list[int px]. Defaults to equal split.
    zebra:   optional RGBColor for alternate body rows.
    """
    ncols = len(header); nrows = len(rows) + 1
    gf = slide.shapes.add_table(nrows, ncols, X(x), X(y), X(w), X(h))
    tbl = gf.table
    tbl.first_row = False           # kill default banded style so our fills show
    tbl.horz_banding = False
    if col_widths:
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = X(cw)

    def _cell(cell, txt, fg, bold, align, fill=None, size=body_pt):
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = X(6); cell.margin_right = X(6)
        cell.margin_top = X(3); cell.margin_bottom = X(3)
        if fill is not None:
            cell.fill.solid(); cell.fill.fore_color.rgb = fill
        p = cell.text_frame.paragraphs[0]; p.alignment = align
        # clear inherited runs
        for r in list(p.runs): r._r.getparent().remove(r._r)
        r = p.add_run(); r.text = txt
        r.font.name = FONT; r.font.size = Pt(size)
        r.font.bold = bold; r.font.color.rgb = fg

    for c, htext in enumerate(header):
        _cell(tbl.cell(0, c), htext, header_fg, True,
              PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER,
              fill=header_fill, size=hdr_pt)
    for ri, row in enumerate(rows, start=1):
        fill = None
        if zebra is not None and ri % 2 == 0: fill = zebra
        else: fill = WH
        for c, val in enumerate(row):
            _cell(tbl.cell(ri, c), val, body_fg, False,
                  PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER, fill=fill)
    return gf
