# ovelto.labs: logo files

Two interlocked rings: **design** (teal) and **AI-native tools** (green). They link through each other, tilted 20°, and the overlap is where the two meet.

There are two final palette options:

- **Option 1: Deep Teal + Pistachio.** This is the default, and it's what this folder contains.
- **Option 2: Deep Teal + Spring Green.** The same set of files is in `alt-spring-green/`.

## Files

| Use | File |
|---|---|
| Website header, documents (light background) | `svg/ovelto-lockup-light.svg` |
| Deep teal / dark backgrounds | `svg/ovelto-lockup-dark.svg` |
| Square spaces (social profile, footer) | `svg/ovelto-lockup-stacked-light.svg` / `-dark.svg` |
| Symbol only | `svg/ovelto-mark-light.svg` / `-dark.svg` |
| One-colour printing, stamps, embossing | `svg/ovelto-*-mono-teal.svg` / `-mono-white.svg` |
| App / social avatar | `svg/ovelto-app-icon.svg`, `png/ovelto-app-icon-1024.png` |
| Browser tab icon | `favicon.ico`, `png/favicon-*.png`, `png/apple-touch-icon-180.png` |
| Website intro animation (symbol only) | `svg/ovelto-mark-animated.svg` (plays once on load; change `1` to `infinite` in its `<style>` to loop) |

Use the SVGs wherever you can, because they stay sharp at any size. The PNGs have transparent backgrounds.

The wordmark is converted to shapes, so you don't need the font installed to display the files.

`preview.png` shows every file on the background it's meant for.

## Colours (no black)

| Name | Option 1 · Pistachio | Option 2 · Spring Green | Role |
|---|---|---|---|
| Deep Teal | `#08303A` | `#08303A` | Main background, text on light |
| Light Teal | `#8FD3E0` | `#8FD3E0` | Design ring on dark |
| Green | `#B5E3A1` | `#4ADE80` | AI ring, ".labs", buttons on dark |
| Pale green | `#E3F5D8` | `#BBF7D0` | Overlap on dark |
| Teal (on light) | `#0F4C5C` | `#0F4C5C` | Design ring on light |
| Green (on light) | `#3F7A2A` | `#15803D` | AI ring and ".labs" on light |
| Overlap (on light) | `#B5E3A1` | `#86EFAC` | Overlap on light |
| Light background | `#F3F7F1` | `#F2F7F4` | Light sections |

Bright greens are hard to read on white. On light backgrounds, ".labs" and the AI ring switch to the darker "on light" green.

## Type

- Wordmark: **Space Grotesk**. "ovelto" is set in weight 600 and ".labs" in weight 400, with letter spacing at −3.5%.
- Space Grotesk is a free Google Font, so the website can use the same family for headings.

## Motion

- **Site intro:** the rings draw on, the weave snaps shut, the mark swings into its 20° tilt (the green ring rises), then ".labs" types on.
- **Thinking loader:** the mark spins while the overlap pulses. Use it for loading and "AI is working" states.

## Rules

- Don't fill the rings or add red, orange or yellow. That keeps it clearly apart from Mastercard.
- Keep the 20° tilt and the over-under weave. They're what make the mark ours.
- Below 32px, use `ovelto-mark-small.svg`. It has heavier strokes so the weave stays readable.
- Leave clear space around the logo of at least half the mark's height.
