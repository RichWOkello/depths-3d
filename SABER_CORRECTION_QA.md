# Light Saber — first-person correction QA (Depths 3D v5.0.0)

**Source of truth:** `src/game.js`. All three entry points (`index.html`, `PLAY_DIRECTLY.html`, and the self-contained Colab notebook) are regenerated with `python build.py`.

## Applied corrections

- One anatomical, hilt-locked gripping hand. The circumference of the grip matches the hand’s curled finger geometry, with the thumb on the opposite side. No second overlapping melee hand.
- New reduced-size saber hilt with machined emitter, pommel, grip details and illuminated switch.
- Slender 1.0-unit energy blade with core, white center and translucent blue aura. The blade extends along its cylinder’s local **Y** axis and is repositioned so the emitter-end never drifts.
- Dedicated lower-right stance with limited lateral swing, restrained walking/sprinting sway, blocking pose and controlled recovery.
- Horizontal and diagonal light strikes, **G** heavy vertical slash (18 energy), **T** thrust (8 stamina), **hold C** guard/parry and retained **V** charged wave.
- Style-specific combat contact sweeps preserve one hit per enemy per strike and existing visual/sound hit effects.

## Tests actually run

- `node --check src/game.js` — passed.
- `tests/saber_correction_qa.py` — passed all grip/ignition/stance/swing/guard/keyboard checks in headless Chromium with a Three.js mock.
- `tests/katana_correction_qa.py` — passed, confirming katana remains intact.
- `tests/physics_regression.py` — passed, including both one-hand melee rigs.
- `tests/delivery_test.py`, `tests/flow_test.py`, `tests/v5_controls_qa.py`, `tests/v5_integration_test.py`, `tests/v5_physics_qa.py`, `tests/minimal_menu_qa.py`, `tests/minimal_save_qa.py`, `tests/grounded_gait_test.py`, `tests/navigation_test.py`, `tests/theme_melee_test.py`, `tests/v5_world_qa.py` — passed.

## Limitations

The tests check game logic and geometry transformations using simulated Three.js, not live hardware WebGL. Physical hand/handle mesh interpenetration, nearby-wall clipping, on-screen occlusion, GPU frame rate, subjective sound/animation quality and live Colab iframe operation require testing in a WebGL-capable browser. The hand is procedural geometry rather than a rigged production-grade character mesh.

**No GitHub publication was performed.**
