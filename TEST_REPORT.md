# Depths 3D v5.0.0 — Katana and Light Saber correction QA

**Targeted scope:** Existing v5.0.0 build with corrected katana and Light Saber only; the six firearm meshes, enemy classes, menus, save format and platform delivery are unchanged.

**Verified with headless Chromium and a mocked Three.js renderer:**

- Katana has exactly one visible rig, four curved finger assemblies, one thumb, and a dedicated slim 150-vertex blade geometry.
- Weapon stance changes during walking and guarding; gripping hand is rigidly attached to katana's hilt during idle, attack, and recovery (no relative pose drift in tests).
- Horizontal, diagonal, heavy vertical, and thrust attacks run, use cooldowns/stamina where appropriate, and do not apply damage at key press.
- Contact-phase melee damage, hit reactions, stagger, knockback and finishing effects remain operational.
- Actual G and T keyboard events trigger heavy and thrust attack styles; C guard blocks new attacks.
- All eight weapon slots and the light saber remain selectable.
- Full menu flow, 20-floor generation, world integration, monster AI/navigation, control, and persistence regression tests passed.
- `tests/saber_correction_qa.py` confirms exactly one handle-locked saber hand, a four-finger circumferential grip, layered blade geometry and correct axial ignition from the emitter.
- Saber idle, walking, sprinting and guarding positions are distinct while the hand stays at a fixed offset from the hilt.
- Horizontal, diagonal, heavy and thrust attacks cause contact-window damage (not instant damage), preserve one-hit-per-target per swing, and use energy/stamina where appropriate.
- Guard prevents simultaneous attacks; actual G/T key events trigger the new saber styles without uncaught JavaScript errors.
- Existing `katana_correction_qa.py`, general melee/physics, menu, AI/navigation, save and 20-floor world tests passed.
- The real Colab page server and static `index.html`/`src/game.js` returned HTTP 200; notebook compiles and JavaScript syntax validates.

**Not yet verified:** Real hardware WebGL appearance, physical finger-versus-grip mesh intersections at every angle, nearby-wall clipping, sustained frame-rate in Colab, and subjective fidelity of animations and audio. Mock-based tests cannot establish photorealism or professional motion capture.

---

## Earlier development QA history

# Previous consolidated interface QA

## v5.1 UI-specific test results

- `tests/minimal_menu_qa.py`: intro skip, title, difficulty, uncluttered main screen, eight-weapon Loadout, Audio, Display, Controls, Gameplay, Saved Data routing, setting changes, gameplay launch, attack and pause. No uncaught JS exceptions using a Three.js simulated renderer.
- `tests/minimal_save_qa.py`: used an in-page localStorage shim to check new-run confirmation, cancellation, saved-campaign Continue visibility, delete-save confirmation and actual removal of the save key. This is an in-page storage test, **not** proof of persistence across real browser reloads.
- Narrow-viewport navigation tested at 420px width; Settings and Saved Data remained reachable.
- Readability checked through screenshots generated in Chromium with the game's real menu artwork and a simulated 3D renderer.
- All 12 test scripts passed, with the 20-floor generation test run separately after the combined command reached its time limit. All results use simulated rendering except real local HTTP delivery checks.

## Test environment

The automated GUI tests use a lightweight Three.js substitute in Chromium. This validates JavaScript execution, event wiring, game-state updates and deterministic gameplay algorithms, but **not actual WebGL fidelity or GPU speed**. The Colab loader was exercised with a simulated `google.colab.output` facade and a real local Python HTTP server in the test process; the test browser could not navigate to local URLs due to environment policy.

## Verified by running code

1. **Syntax and outputs** — `node --check src/game.js` and `python build.py` passed; the static `index.html` references `src/game.js` and the Colab notebook is syntactically valid Python.
2. **Colab HTTP launcher** — local server returned HTTP 200 with embedded game HTML from the notebook payload. A static server also returned HTTP 200 for `index.html` and `src/game.js`.
3. **Primary launch** — simulated Chromium test went from intro to title to difficulty to weapon armory to PLAY, katana/saber combat and pause without JavaScript exceptions.
4. **Combat physics** — a 2.8-damage Desert Eagle round actually traveled to a 4-HP creature, leaving approximately 1.2 HP. The M79 started with an upward velocity, fell under gravity and exploded, clearing its projectile object.
5. **New AI types** — stalker, armored, crawler and necromancer initialized with appropriate model rigs and responded to sound events. The retained leg IK foot-planting and BFS obstacle navigation tests passed.
6. **World generation** — 20 independently generated floors all retained a connected start-to-exit path. All scheduled crypt keys and rune switches spawned, nine environment themes appeared and four named boss identities occurred at their expected floors.
7. **Mechanisms** — a secret masonry section could take damage, open a traversable passage and reward currency. A floor requiring a key remained sealed until the key condition was fulfilled.
8. **Boss phases** — a floor-five boss switched from phase one to phase three after taking enough damage; its warning-ring logic executed without a JavaScript exception.
9. **Inventory and shop** — a purchased damage upgrade incremented a weapon level; a health upgrade increased max health; a medkit restored 45 HP. A v5 save snapshot was written and restored in a mocked localStorage environment.
10. **Input paths** — actual key events exercised AK burst selection, reload, inventory, weapon quick selection, saber charge, guard and pause.
11. **Regression** — original pre-v5 tests for weapon hands, progressive ignition, melee stagger/sever feedback, grounded legs, wall facades and maze navigation passed in the mock environment.

## Not yet established by those tests

- Full rendered WebGL visual/audio results in an actual user Colab iframe.
- Stable frame rate with heavy effects on different integrated/discrete GPUs.
- Persistent localStorage data surviving a real browser-origin reload: the game save round-trip was tested against an in-memory localStorage shim because localhost navigation was administratively blocked.
- Complete human playthrough of all 20 floors, enemy AI tuning and full-game balancing.
- Every requested advanced mechanic in the original development brief; see `FEATURE_MATRIX.md`.

The game can be played in supported modern browsers, but final visual review, long-session performance and full campaign acceptance must happen in a real browser environment.
