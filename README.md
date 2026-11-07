# Depths 3D v6.0.0 — The Bestiary Expansion

**Browser-based dark-fantasy 3D dungeon shooter** · JavaScript / Three.js · By Richard Okello · 7 November 2026

[**Play on GitHub Pages**](https://richwokello.github.io/depths-3d/) · [Source repository](https://github.com/RichWOkello/depths-3d)

This release consolidates the development work completed through 7 November 2026 into a **single v6.0.0 version**. The game is procedural and runs with Three.js loaded from a CDN, requiring internet access. GitHub Pages reflects this version **only after the files are pushed and deployed**.

## Gameplay

- First-person dungeon exploration, eight existing weapon slots, ranged and melee combat, relics and equipment.
- Themed dungeon regions, portal vortex and rune objectives, bosses and difficulty modes.
- Soul Forge perk selection and upgrade shop, progress saves, minimap, HUD and audio systems.
- Six horror-style procedural enemies: **Flesh Brute, Crypt Crawler, Flesh Imp, Gaunt Hooded Wraith, Necromancer and Winged Gargoyle**.
- The Necromancer has a detailed recessed skull, layered hood and robes, ornamented staff, casting wisps and magical effects.
- The remaining creatures received a five-species reference-fidelity pass: facial structure, claws, body proportions, skeletal/rib details, wing geometry and textures.

## Run

**Browser**: Open `PLAY_DIRECTLY.html` in Chrome or Edge, or launch a local HTTP server from the project root (`python -m http.server 8000`) and visit `http://localhost:8000`.

**Google Colab**: Open `depths_3d.ipynb`, connect a Python runtime and run the first code cell. It starts the game iframe. The optional viewer cell shows the reference comparison gallery. The notebook embeds readable HTML/JavaScript, not a compressed executable payload.

**Bestiary turntable**: Open `BESTIARY_VIEWER.html`. Drag to rotate; use the character buttons, animation modes and face comparison. The viewer includes embedded reference crops.

**Editing and rebuilding**: Edit `src/game_base.js` (game), `src/bestiary_pass.js` (creatures) or `src/game.html` (markup), then run `python -m pip install pillow nbformat` (first setup) and `python build.py` to regenerate `src/game.js`, `index.html`, `PLAY_DIRECTLY.html` and the notebook. Avoid directly editing generated `src/game.js` unless you also copy those changes back to the source modules.

## Controls

WASD movement, mouse look, Space/F attack, 1–8 weapons, R reload, E interact/portal, X rune switch, C guard, Esc pause, M map, N map orientation, `[ / ]` minimap zoom, L flashlight. See in-game menus for other actions.

## Release status and limitations

**GitHub-ready release candidate**, not certified photorealistic or 60 FPS. The code is assembled, syntax-checked and subject to available automated simulation tests. Full browser/WebGL gameplay, real Colab GPU rendering, visual comparison against artwork and sustained 40-creature performance require actual-device testing. All six creatures remain procedural approximations rather than professionally sculpted/rigged GLB models. A GLB fallback path is exposed for future asset replacement.

The repo-specific Git metadata is intentionally omitted. Copy these files **into your existing `depths-3d` working directory** without deleting its `.git` folder. Follow [UPDATE_LOCAL_REPO.md](UPDATE_LOCAL_REPO.md).

Read [RELEASE_NOTES.md](RELEASE_NOTES.md), [TEST_REPORT.md](TEST_REPORT.md) and [FEATURE_MATCH_REPORT.md](FEATURE_MATCH_REPORT.md) for coverage and known gaps. Original v5.2.0 notes are preserved under `docs/development_history_v5_2/`.
