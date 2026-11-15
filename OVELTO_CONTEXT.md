# ovelto.labs: project context

This file hands the project over to a new Claude Code session. It covers what has been decided, where the files are, and what's still open.

**How to use it:** start a new session with "Read OVELTO_CONTEXT.md first." To have Claude Code load it automatically, rename it to `CLAUDE.md` at the repo root.

---

## 1. The project

- **Ovelto Labs** (written as `ovelto.labs`) is a new AI-enabled digital agency.
- **Services:** website and app design, vibe-coded prototypes, front-end UI, and AI workflows, agents and tools.
- **Work so far:**
  1. Researched inspiration from other agency websites.
  2. Designed the logo, its animations and the colour palette.
  3. Built a website skeleton to try palettes on.
- **Next step:** build the real website.

## 2. Logo: decided

- **Mark:** two interlocked rings. The first is the **design** ring (blue/teal); the second is the **AI** ring (green). The filled overlap (the "lens") is where design meets AI.
- **Geometry:** each ring is r=34 in a 120×120 box, with centres 32 apart. Stroke 8. The whole mark is **tilted −20°**.
- **Weave:** "true see-through gap". The under-ring gets a real gap cut with an SVG mask, only near each crossing, so nothing is painted in a background colour.
  - At the top crossing, the green ring passes over the blue.
  - At the bottom crossing, the blue ring passes over the green.
- **Small sizes (≤32px):** use stroke 12 and a gap of 5 so the weave stays visible.
- **Wordmark:** `ovelto.labs` in **Space Grotesk**, with "ovelto" at weight 600 and ".labs" at weight 400, letter spacing −3.5%. ".labs" uses the green.
- **No black anywhere.** The darkest colour is Deep Teal `#08303A`.

**Considered and rejected:**
- Other marks: an open loop with a dot (looked like Blender or a power-button icon), agent nodes, and a pixel-to-curve O.
- Filled discs (too close to Mastercard).
- The no-tilt alternatives: big + small rings, planet + moon, open rings, a dotted ring and a vertical link. The user preferred to keep the tilt.
- **Known concern:** two equal tilted rings can hint at the Olympic rings. The user accepted this and kept the tilt.
- **Before going public:** run a trademark search (USPTO design code 26.01, the WIPO Global Brand Database) and a reverse image search.

## 3. Colour: two final options

| Role | Option 1 · Deep Teal + Pistachio (preferred) | Option 2 · Deep Teal + Spring Green |
|---|---|---|
| Base / dark background | `#08303A` | `#08303A` |
| Raised surface | `#0C3B47` | `#0C3B47` |
| Design ring on dark | `#8FD3E0` | `#8FD3E0` |
| AI ring, ".labs", buttons on dark | `#B5E3A1` | `#4ADE80` |
| Overlap on dark | `#E3F5D8` | `#BBF7D0` |
| Light section background | `#F3F7F1` | `#F2F7F4` |
| Design ring on light | `#0F4C5C` | `#0F4C5C` |
| AI ring / ".labs" on light | `#3F7A2A` | `#15803D` |
| Overlap on light | `#B5E3A1` | `#86EFAC` |
| Text on dark / muted | `#F2F7F6` / `#A3C4C8` | same |

**Still open: a brighter blue for the first (design) ring.** These candidates are being compared; each pair is the colour on dark, then the colour on light:
- Sky `#7DD3FC` / `#0369A1`
- Azure `#38BDF8` / `#0284C7`
- Cerulean `#22C3E6` / `#0E7490`
- Cornflower `#6EA8FF` / `#2563EB`
- Electric Blue `#4D8DFF` / `#1D4ED8`

The current colour is Light Teal `#8FD3E0` / `#0F4C5C`.

**Earlier palettes, now superseded:** Navy + Emerald, plus explorations of Forest + Lime, Pine + Mint, Midnight + Lime and others.

## 4. Motion: decided

1. **Site intro**, which plays once on load (about 7 seconds):
   - "ovelto" rises in.
   - The rings draw on, level: design ring first, then the AI ring.
   - The weave snaps shut (the gaps open) and the overlap pops in.
   - The pair swings into the −20° tilt, with the green ring rising and a small overshoot.
   - ".labs" types on letter by letter, with a blinking cursor.
2. **Thinking loader:** the mark spins continuously (2.4s per turn) while the overlap pulses. Use it for loading and "AI is working" states, such as an "Ovelto agent is thinking…" status label or a button's busy state.
3. **Reduced motion:** respect `prefers-reduced-motion` by showing the finished logo.

## 5. Website skeleton (draft)

- **Sections:**
  1. Navigation: logo, Services, Work, Process, About, and a "Start a project" button.
  2. Hero: headline "Where design meets AI-native engineering.", the large mark and the loader.
  3. Four service cards.
  4. "How we work" (light section): Discover, Design, Build, Automate.
  5. Selected work (placeholders).
  6. A contact band.
  7. Footer.
- **Copy:** the wording is a draft. Anything in [brackets] is a placeholder: case studies, email, city, reply time.
- **Fonts:** Space Grotesk for headings, Inter for body text.

## 6. Files in this repo

- `brand/ovelto-logo/`: final logo files in **Option 1 (Pistachio)**: SVG, PNG, `favicon.ico` and an animated SVG of the mark. `README.md` there explains which file to use where.
- `brand/ovelto-logo/alt-spring-green/`: the same set in **Option 2**.
- `brand/tools/build_logo.py`: rebuilds every SVG from the logo's geometry. It converts the wordmark to shapes using Space Grotesk.
  - Usage: `python3 build_logo.py <fonts_dir> <out_dir> [pistachio|spring-green]`.
  - Needs `pip install fonttools pillow`.
  - It expects `SpaceGrotesk-400.ttf` and `SpaceGrotesk-600.ttf` from Google Fonts in the fonts folder.
  - Edit the `PALETTES` dictionary to change colours, such as a new blue.
- `brand/tools/render_png.js`: renders the PNGs and `preview.png` with Playwright. Usage: `node render_png.js <out_dir>`.
- `brand/canvas-source/`: source of every design board, including the logo explorations, the final options, the animations and the website skeleton (`Site.dc.html`).
  - These files use Claude's Design canvas format, with `{{ }}` placeholders and a `support.js` runtime. They won't open as plain web pages, so treat them as a reference when building the real site.
  - `Mark.dc.html` holds the logo geometry, including the maths for the rings, overlap and gaps.
  - `Intro.dc.html` and `FinalOptions.dc.html` hold the CSS keyframes for the intro and loader.

## 7. Next steps

1. Pick Option 1 or 2, and decide whether to brighten the design-ring blue. Then rebuild the logo files with `build_logo.py`.
2. Export the combined intro (mark + typed ".labs") as a website-ready animated SVG, or as an HTML/CSS component.
3. Build the real website from the skeleton, as a plain web page or a framework.
4. Write the real copy and case studies.
5. Run the trademark and reverse image checks.
