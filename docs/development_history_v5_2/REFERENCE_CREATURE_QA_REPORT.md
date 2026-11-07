# Depths 3D v5.2.0 — Reference Creature Pass QA

## Scope
Five creature designs were refined: Flesh Brute, Crypt Crawler, Flesh Imp, Gaunt Hooded Wraith, Winged Gargoyle. The Necromancer is carried over from the approved prior build.

## Checks performed
- PASS: JavaScript syntax validation of addon and integrated game.
- PASS: Full game, browser HTML and notebook rebuild from the same source.
- PASS: Structural smoke test of five new cranium lofts and face/limb features.
- PASS: Three LOD meshes for each species; 4 normalized skinning weights, no non-finite vertices in tested geometry.
- PASS: Geometry cache is shared across instances.
- PASS: Near/mid detailed meshes are switched off at distances exceeding 13 m and 25 m.
- PASS: Gargoyle has two animated wing assemblies and six new tail joints.
- PASS: Approved Necromancer hood, robes, three trophy skulls, staff and five wisps preserved.
- PASS: Existing v5 combat, portal, boss, save, Soul Forge and menu simulation checks.

## Measured performance (simulated JavaScript browser with mocked Three.js renderer)
- 40 model builds: **1347 ms** (includes uncached first builds).
- 4,800 animation updates: **20 ms**, or **0.0043 ms per model update** in the mock.
- 40 character scene graphs contain about **5,276 mesh objects**, most being small details; only nearer details are visible.
- First-time geometry generation is above the 150 ms target for some species (including Brute and Crawler in measured runs).
- **These figures are not GPU frame rates. 60 FPS with 40 monsters is NOT verified.**

## Not verified
- Actual WebGL rendering, facial resemblance to the reference, animation clipping, hard 60 FPS GPU target, browser audio, or a real Colab session.
- The available browser had no working connection to the Three.js CDN. Headless structural tests used a mock library.
- Sculpted photoreal skin, muscle deformation, physically accurate jaw joints and professional motion capture are not present.

## Files
- `depths_3d_bestiary_pass.ipynb` — single primary game code cell and separate viewer cell.
- `PLAY_DIRECTLY.html` — standalone game that loads Three.js from a CDN.
- `BESTIARY_VIEWER.html` — reference-versus-procedural turntable with face close-up.
- `src/game.js` — complete browser game source.
- `src/bestiary_pass.js` — editable five-species improvements plus approved Necromancer.
- `FIVE_CREATURE_FIDELITY_AUDIT.md` — visual feature-by-feature checklist.
