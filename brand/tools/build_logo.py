"""Build the final Ovelto Labs logo files (SVG) from geometry + Space Grotesk outlines.

Logo spec (agreed with the user):
  - Two interlocked rings (r=34, centres 32 apart) in a 120x120 box, tilted -20 degrees.
  - Weave = "true see-through gap": the UNDER ring gets a gap cut with a mask, only near
    each crossing. Nothing is painted in a background colour, so files work on any ground.
  - Wordmark "ovelto" (Space Grotesk 600) + ".labs" (Space Grotesk 400), -3.5% tracking,
    converted to vector outlines so no font is needed to display the files.

Usage: python3 -I build_logo.py <fonts_dir> <out_dir>
"""
import os
import sys

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS_DIR, OUT = sys.argv[1], sys.argv[2]
PALETTE = sys.argv[3] if len(sys.argv) > 3 else "pistachio"
os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)

# ---- Brand palettes (no black: darkest tone is Deep Teal) ----
# Each: ring colours + overlap ("lens") for light grounds and for the deep-teal ground.
PALETTES = {
    # Chosen palette: Deep Teal + Pistachio
    "pistachio": dict(
        deep="#08303A", mist="#F3F7F1",
        lightA="#0F4C5C", lightB="#3F7A2A", lightLens="#B5E3A1",      # on light grounds
        darkA="#8FD3E0", darkB="#B5E3A1", darkLens="#E3F5D8",         # on deep teal
        monoLens="#C7DBD6", monoWhiteLens="#2A5A63"),
    # Runner-up: Deep Teal + Spring Green
    "spring-green": dict(
        deep="#08303A", mist="#F2F7F4",
        lightA="#0F4C5C", lightB="#15803D", lightLens="#86EFAC",
        darkA="#8FD3E0", darkB="#4ADE80", darkLens="#BBF7D0",
        monoLens="#C7DBD6", monoWhiteLens="#2A5A63"),
}
C = PALETTES[PALETTE]
DEEP, MIST = C["deep"], C["mist"]

# Colour sets: ringA, ringB, lens, word ("ovelto"), dot-labs (".labs")
THEMES = {
    "light":      dict(a=C["lightA"], b=C["lightB"], lens=C["lightLens"], w1=DEEP, w2=C["lightB"]),
    "dark":       dict(a=C["darkA"], b=C["darkB"], lens=C["darkLens"], w1=MIST, w2=C["darkB"]),
    "mono-teal":  dict(a=DEEP, b=DEEP, lens=C["monoLens"], w1=DEEP, w2=DEEP),
    "mono-white": dict(a="#FFFFFF", b="#FFFFFF", lens=C["monoWhiteLens"], w1="#FFFFFF", w2="#FFFFFF"),
}


def load_font(weight):
    """Load Space Grotesk; if it is a variable font, pin it to the requested weight."""
    path = os.path.join(FONTS_DIR, f"SpaceGrotesk-{weight}.ttf")
    font = TTFont(path)
    if "fvar" in font:
        from fontTools.varLib import instancer
        font = instancer.instantiateVariableFont(font, {"wght": weight})
    return font


def mark_svg_group(uid, t, stroke=8, gap=3, x=0, y=0, scale=1.0):
    """Return (defs, body) for the mark placed at (x,y) with a 120*scale box.

    The masks cut the under ring only inside a small circle (r=13) around each crossing:
    top crossing (60,30): ring B passes over ring A -> A is cut by B's stroke.
    bottom crossing (60,90): ring A passes over ring B -> B is cut by A's stroke.
    """
    cut = stroke + 2 * gap
    defs = f"""
    <clipPath id="{uid}-ct"><circle cx="60" cy="30" r="13"/></clipPath>
    <clipPath id="{uid}-cb"><circle cx="60" cy="90" r="13"/></clipPath>
    <mask id="{uid}-ma" maskUnits="userSpaceOnUse" x="-40" y="-40" width="200" height="200">
      <rect x="-40" y="-40" width="200" height="200" fill="#fff"/>
      <circle cx="76" cy="60" r="34" fill="none" stroke="#000" stroke-width="{cut}" clip-path="url(#{uid}-ct)"/>
    </mask>
    <mask id="{uid}-mb" maskUnits="userSpaceOnUse" x="-40" y="-40" width="200" height="200">
      <rect x="-40" y="-40" width="200" height="200" fill="#fff"/>
      <circle cx="44" cy="60" r="34" fill="none" stroke="#000" stroke-width="{cut}" clip-path="url(#{uid}-cb)"/>
    </mask>"""
    body = f"""
  <g transform="translate({x:g} {y:g}) scale({scale:g})">
    <g transform="rotate(-20 60 60)">
      <path d="M60 30 A34 34 0 0 1 60 90 A34 34 0 0 1 60 30 Z" fill="{t['lens']}"/>
      <circle cx="44" cy="60" r="34" fill="none" stroke="{t['a']}" stroke-width="{stroke}" mask="url(#{uid}-ma)"/>
      <circle cx="76" cy="60" r="34" fill="none" stroke="{t['b']}" stroke-width="{stroke}" mask="url(#{uid}-mb)"/>
    </g>
  </g>"""
    return defs, body


def text_paths(runs, size, x0, baseline):
    """Lay out text runs [(font, text, colour)] as SVG <path>s. Returns (svg, advance_px)."""
    out, x = [], x0
    track = -0.035 * size  # letter-spacing -0.035em
    for font, text, colour in runs:
        upm = font["head"].unitsPerEm
        s = size / upm
        cmap, gs, hmtx = font.getBestCmap(), font.getGlyphSet(), font["hmtx"]
        ds = []
        for ch in text:
            gname = cmap[ord(ch)]
            pen = SVGPathPen(gs)
            # font units are y-up; flip into SVG y-down at the baseline
            gs[gname].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
            ds.append(pen.getCommands())
            x += hmtx[gname][0] * s + track
        out.append(f'<path fill="{colour}" d="{" ".join(ds)}"/>')
    return "\n  ".join(out), x - x0 - track  # no trailing tracking after last glyph


def ink_metrics(font, size):
    """x-height-ish metrics in px: (ascender of 'l', descender 0) for vertical centring."""
    gs = font.getGlyphSet()
    bp = BoundsPen(gs)
    gs[font.getBestCmap()[ord("l")]].draw(bp)
    s = size / font["head"].unitsPerEm
    return bp.bounds[3] * s  # top of 'l' above baseline


def write(name, svg):
    with open(os.path.join(OUT, "svg", name), "w") as f:
        f.write(svg)


F600, F400 = load_font(600), load_font(400)
HDR = '<?xml version="1.0" encoding="UTF-8"?>\n'

# ---- 1. Mark only (120x120 viewBox, transparent background) ----
for key, t in THEMES.items():
    d, b = mark_svg_group("m", t)
    write(f"ovelto-mark-{key}.svg",
          f'{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512" role="img" aria-label="Ovelto Labs">\n  <defs>{d}\n  </defs>{b}\n</svg>\n')

# Small-size mark (favicons, <= 32px): heavier strokes + wider gap so the weave survives
d, b = mark_svg_group("m", THEMES["light"], stroke=12, gap=5)
write("ovelto-mark-small.svg",
      f'{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="32" height="32" role="img" aria-label="Ovelto Labs">\n  <defs>{d}\n  </defs>{b}\n</svg>\n')

# ---- 2. App icon (navy rounded square) ----
d, b = mark_svg_group("m", THEMES["dark"], stroke=9, x=14, y=14, scale=92 / 120)
write("ovelto-app-icon.svg",
      f'{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512" role="img" aria-label="Ovelto Labs">\n  <defs>{d}\n  </defs>\n  <rect width="120" height="120" rx="27" fill="{DEEP}"/>{b}\n</svg>\n')

# ---- 3. Horizontal lockup: mark + "ovelto.labs" ----
SIZE = 84          # wordmark font size (px) relative to a 132px mark, as on the canvas
MARK = 132
GAP = 22
PAD = 8
cap = ink_metrics(F600, SIZE)                 # height of 'l' above baseline
baseline = PAD + MARK / 2 + cap / 2 - 4       # optically centre the text on the mark
for key, t in THEMES.items():
    d, b = mark_svg_group("m", t, x=PAD, y=PAD, scale=MARK / 120)
    txt, adv = text_paths([(F600, "ovelto", t["w1"]), (F400, ".labs", t["w2"])], SIZE, PAD + MARK + GAP, baseline)
    W, H = PAD + MARK + GAP + adv + PAD, MARK + 2 * PAD
    write(f"ovelto-lockup-{key}.svg",
          f'{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="ovelto.labs">\n  <defs>{d}\n  </defs>{b}\n  {txt}\n</svg>\n')

# ---- 4. Stacked lockup (mark above wordmark) ----
SSIZE, SMARK = 44, 128
for key in ("light", "dark"):
    t = THEMES[key]
    _, adv = text_paths([(F600, "ovelto", t["w1"]), (F400, ".labs", t["w2"])], SSIZE, 0, 0)
    W = max(adv, SMARK) + 2 * PAD
    d, b = mark_svg_group("m", t, x=(W - SMARK) / 2, y=PAD, scale=SMARK / 120)
    base = PAD + SMARK + 14 + ink_metrics(F600, SSIZE)
    txt, _ = text_paths([(F600, "ovelto", t["w1"]), (F400, ".labs", t["w2"])], SSIZE, (W - adv) / 2, base)
    H = base + 12 + PAD
    write(f"ovelto-lockup-stacked-{key}.svg",
          f'{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="ovelto.labs">\n  <defs>{d}\n  </defs>{b}\n  {txt}\n</svg>\n')

# ---- 5. Animated mark ("Full intro": draw -> weave snaps -> swing into tilt), self-contained CSS ----
t = THEMES["light"]
anim = f'''{HDR}<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512" role="img" aria-label="Ovelto Labs">
  <style>
    /* Plays once on load (forwards). Change "1" to "infinite" to loop. */
    .a{{animation:3.6s cubic-bezier(.22,1,.36,1) 1 both}}
    .vb{{transform-box:view-box;transform-origin:60px 60px}}
    .tb{{transform-box:fill-box;transform-origin:center}}
    .ra{{animation-name:ra}} .rb{{animation-name:rb}} .cut{{animation-name:cut}}
    .lens{{animation-name:lens}} .swing{{animation-name:swing}}
    @keyframes ra{{0%{{stroke-dashoffset:214px}}40%,100%{{stroke-dashoffset:0px}}}}
    @keyframes rb{{0%,12%{{stroke-dashoffset:-214px}}52%,100%{{stroke-dashoffset:0px}}}}
    @keyframes cut{{0%,56%{{stroke-width:0px}}64%{{stroke-width:19px}}72%,100%{{stroke-width:14px}}}}
    @keyframes lens{{0%,58%{{transform:scale(0);opacity:0}}72%{{transform:scale(1.15);opacity:1}}82%,100%{{transform:scale(1);opacity:1}}}}
    @keyframes swing{{0%,66%{{transform:rotate(20deg)}}80%{{transform:rotate(-7deg)}}92%,100%{{transform:rotate(0deg)}}}}
    @media (prefers-reduced-motion: reduce){{.a{{animation:none}}}}
  </style>
  <defs>
    <clipPath id="ct"><circle cx="60" cy="30" r="13"/></clipPath>
    <clipPath id="cb"><circle cx="60" cy="90" r="13"/></clipPath>
    <mask id="ma" maskUnits="userSpaceOnUse" x="-40" y="-40" width="200" height="200">
      <rect x="-40" y="-40" width="200" height="200" fill="#fff"/>
      <circle class="a cut" cx="76" cy="60" r="34" fill="none" stroke="#000" stroke-width="14" clip-path="url(#ct)"/>
    </mask>
    <mask id="mb" maskUnits="userSpaceOnUse" x="-40" y="-40" width="200" height="200">
      <rect x="-40" y="-40" width="200" height="200" fill="#fff"/>
      <circle class="a cut" cx="44" cy="60" r="34" fill="none" stroke="#000" stroke-width="14" clip-path="url(#cb)"/>
    </mask>
  </defs>
  <g class="a vb swing">
    <g transform="rotate(-20 60 60)">
      <path class="a tb lens" d="M60 30 A34 34 0 0 1 60 90 A34 34 0 0 1 60 30 Z" fill="{t['lens']}"/>
      <circle class="a ra" cx="44" cy="60" r="34" fill="none" stroke="{t['a']}" stroke-width="8" stroke-dasharray="214" mask="url(#ma)"/>
      <circle class="a rb" cx="76" cy="60" r="34" fill="none" stroke="{t['b']}" stroke-width="8" stroke-dasharray="214" mask="url(#mb)"/>
    </g>
  </g>
</svg>
'''
write("ovelto-mark-animated.svg", anim)
print("SVGs written:", sorted(os.listdir(os.path.join(OUT, "svg"))))
