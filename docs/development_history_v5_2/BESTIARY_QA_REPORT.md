# DEPTHS 3D v5.2.0 — Bestiary Pass: test results

## Executed checks

- `node --check src/game.js`: PASS.
- `python tests/test_module.py`: PASS six species instantiate under mocked Three.js, skin weights sum to 1 across four influences, and named rigs are constructed.
- `python tests/v5_integration_test.py`: PASS simulated weapon, projectile, enemy AI, boss gating, saves, shop, and menu flows.
- `python tests/v52_upgrade_qa.py`: PASS simulated HUD, SVG icons, weapon model presence, Soul Forge navigation.
- `nbformat.validate` and Python compilation of Colab code cells: PASS.
- A comparison viewer includes six reference crops and exposes idle, walk, attack, hit and death simulation controls. **Not visually approved in genuine WebGL.**

## Measured model geometry from the mock runtime

| Creature | High triangles | Mid triangles | Far triangles | Uncached build milliseconds |
|---|---:|---:|---:|---:|
| Flesh Brute | 13,724 | 5,140 | 904 | 294 |
| Crypt Crawler | 13,716 | 4,984 | 868 | 235 |
| Flesh Imp | 12,176 | 4,580 | 844 | 137 |
| Gaunt Hooded Wraith | 11,708 | 4,408 | 612 | 85 |
| Necromancer | 12,540 | 4,664 | 688 | 94 |
| Winged Gargoyle | 11,372 | 4,196 | 840 | 180 |

The measured time is wall-clock in a headless mocked runtime; it is **not** real WebGL draw time. Body meshes are cached for subsequent instances. Three species exceed the 150 ms uncached-generation target. Triangle totals above are body/skinned mesh LOD counts and do **not** include detachable props, eyes, teeth, wings or cloth.

## Limitations and not-verified requirements

- The user-requested `07_enemies.js` was not among currently available uploaded files. This implementation adapts the available `src/game.js` from the prior v5.2.0 game build, retaining its enemy type identifiers; it is **not** an audited edit of `07_enemies.js`.
- The image is a composite reference screenshot, not calibrated orthographic model sheets; ratios are estimates and hex swatches are sampled reference image pixels, including scene lighting. The exact likeness has **not** been achieved or certified.
- Rendering in a genuine GPU WebGL browser/Colab runtime, six-creature visual likeness, foot IK ground contacts, bat membrane quality, shroud opacity, and all animation transitions require manual visual QA.
- 40 animated monsters at 60 FPS on a midrange laptop was **not measured**. On-screen draw calls from separate facial/cloth props may be substantial.
- Audio output and positional balance require a live browser listening test.
- The viewer's GLB upload path is a supported optional replacement workflow; no sculpted GLB models are bundled. The default remains a purely procedural fallback.
- Some requested mechanics are approximations rather than complete physics (IK, spring cloth, wings, shader dissolves, summoning/swarms). See `FEATURE_MATCH_REPORT.md` for creature-specific partial matches.

**Release classification: development candidate, not final visual sign-off.**
