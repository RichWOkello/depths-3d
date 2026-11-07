# DEPTHS 3D v5.2.0 — Bestiary Pass (development candidate)

**Start here:** `depths_3d_bestiary_pass.ipynb` is the complete Colab notebook. The **first code cell** runs the full game, and the **optional second code cell** opens the turntable viewer. All explanatory sections are Markdown cells. `BESTIARY_VIEWER.html` also runs separately in a desktop WebGL browser, with the six reference crops embedded.

The requested standalone `07_enemies.js` was **not available**; this build integrates with the existing `src/game.js` and retains a named adapter (`DEPTHS_BESTIARY.buildEnemyModel`). Actual WebGL visual likeness and the 60-FPS goal have **not been verified**. Read `BESTIARY_QA_REPORT.md`, `MEASUREMENTS.md`, and `FEATURE_MATCH_REPORT.md` before publishing.

---

# DEPTHS 3D v5.2.0 — Updated Development Candidate

JavaScript/Three.js dark-fantasy FPS by **Richard Okello**. This is a working-code development branch, **not a fully accepted public release**. Existing v5.1.0 must remain recoverable; the `baseline/` archive is included.

## Play and edit

- **Google Colab**: upload `depths_3d_bestiary_pass.ipynb`, connect the runtime and **Run all**. One primary Python code cell contains the complete plain HTML/JavaScript server code, followed by one optional viewer-opening code cell. Requires online loading of Three.js from a CDN with fallback.
- **Local browser**: open `PLAY_DIRECTLY.html` in a modern WebGL browser with internet access for Three.js CDN.
- **Local static server**: run `python -m http.server 8000` in this folder, open `http://localhost:8000` and use `index.html` + `src/game.js`.
- **Edit**: modify `src/game.js` or `src/game.html`, then run `python build.py` to rebuild browser/Colab outputs.
- **GitHub Pages**: publish the root `index.html`, `src/` and supporting files to an existing repo only after local QA. This package does **not** contain or overwrite `.git`.

## Controls

WASD move, mouse look, Space/F fire, R reload, 1–8 weapons, E interact / portal, X rune mechanism, C guard, Esc pause, M expanded map, **N map rotation**, **[ / ] minimap zoom**, **L flashlight**. The game menus include further controls.

## What changed

See `FEATURE_MATRIX.md`, `V5_2_STATUS.md`, `CHANGELOG.md` and `TEST_REPORT.md`. Notable additions: independent weapon viewmodel camera, saber's one-hand stance, procedural emissive lava maps, adaptive quality settings, 47 SVG icons, two-step Soul Forge and improved minimap.

## Important limitations

Live WebGL rendering in a normal browser/Colab, exact grip animations and 60 FPS have **not** been fully verified. The existing gun models are distinctive but remain procedural rather than artist-rigged models, and a complete GPU bloom/refraction compositor is not included. Tests using mock Three.js verify gameplay logic and DOM/UI flow, not graphical fidelity.


### Monster Evolution iteration

See [MONSTER_UPDATE.md](MONSTER_UPDATE.md) for the latest monster model and AI improvements, exact test coverage, and known limitations.

### Six-creature horror roster — v5.2.0 development iteration

The game includes original procedural designs for **Grave Brute, Crypt Crawler, Flesh Ghoul, Dusk Stalker, Ashen Necromancer, and Winged Horror**. The Winged Horror is a new flying/diving enemy, while the others enhance existing archetypes without removing existing bosses.

Open [`CREATURE_GALLERY.html`](CREATURE_GALLERY.html) to inspect and rotate **actual live game meshes**. See [`CREATURE_IMPLEMENTATION.md`](CREATURE_IMPLEMENTATION.md) for the archetype map, animation systems, testing and known visual limitations. After editing the game, run `python build.py` and `python build_creature_gallery.py` to update playable HTML, notebook and gallery.

### Creature Sculpting Refinement — view before publishing

The six enemy families now use **continuous organic core-body geometry** rather than a stack of intersecting sphere shapes. Materials are procedurally painted per family (albedo, bump and roughness), with tapered animated limbs, deeper eye sockets, layered jaws and arched wing surfaces. These are coded Three.js meshes, not static image sprites or downloaded assets.

Open `CREATURE_GALLERY.html` to examine the actual models: click a monster name, drag to rotate, scroll to zoom, or press **1–6** to switch. The gallery requires browser WebGL and access to a Three.js CDN. Code remains readable in `src/game.js`, generated HTML and the eight-cell Colab notebook.

**Realistic expectation:** A procedural mesh system alone will not match the supplied horror reference renders' sculpted skin, high-detail skeletons, facial rigs and cinematic animation. Reaching that standard eventually requires professionally authored or substantially more sophisticated generated 3D assets, a dedicated rig and real GPU visual testing; none of those have been represented as completed here.

## Bestiary Pass files

- `BESTIARY_VIEWER.html`: six-reference comparison turntable, controls, silhouette overlay and optional GLB upload.
- `src/bestiary_pass.js`: procedural six-creature source and adapter.
- `src/game.js`: integrated game script (complete source).
- `MEASUREMENTS.md`: visual estimates and sampled palette values.
- `FEATURE_MATCH_REPORT.md`: ten feature checks per creature, with caveats.
- `BESTIARY_QA_REPORT.md`: executed tests, actual timings and unverified targets.

The previous monster upgrade is retained separately; this zip does not contain a `.git` folder and does not change the published GitHub Pages game.

### Latest v5.2.0 development update — Necromancer rework

The Necromancer now has a recessed skull face and open hood, layered robes, ritual runes,
three trophy skulls, spiked pauldrons, a taller thorn-crowned staff and moving spellcasting
wisps. See `NECROMANCER_REWORK.md` for the reference comparison, test status and limitations.
The updated `BESTIARY_VIEWER.html` starts with the Necromancer selected.


## Five-creature reference fidelity pass — latest development revision

The Flesh Brute, Crypt Crawler, Flesh Imp, Gaunt Hooded Wraith and Winged Gargoyle have received individually modeled anatomy, facial details and procedural skin improvements. The prior approved Necromancer is retained. The turntable now starts with the Brute and has a **Compare faces up close** control. Read `FIVE_CREATURE_FIDELITY_AUDIT.md` and `REFERENCE_CREATURE_QA_REPORT.md` before publishing: real WebGL likeness and 60 FPS remain unverified. No GitHub release has been pushed.
