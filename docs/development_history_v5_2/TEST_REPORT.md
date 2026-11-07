
## Targeted v5.2.0 Necromancer Rework verification

- PASS: `node --check src/game.js` and `node --check src/bestiary_pass.js`.
- PASS: `python tests/test_module.py` — six species construct, skeleton influences valid.
- PASS: `python tests/test_necromancer_rework.py` — open hood, face geometry, two robe layers, staff crown and light, sixteen robe runes, three belt skulls, five magic wisps; casting raises the free hand and intensifies the orb/light/runes.
- PASS: `python tests/v52_upgrade_qa.py` — HUD, viewmodels, perk/shop flow in a simulated browser.
- PASS: `python tests/v5_integration_test.py` — simulated weapons, save/load, AI, portal, boss and Soul Forge.
- PASS: viewer inline-script syntax; notebook schema and Python-code compilation.
- UNVERIFIED: real Three.js WebGL appearance, actual head likeness versus reference, audio listening, performance on laptop, 40-creature 60 FPS, Colab browser GUI run.
- The visible skeletal mask, robe and staff are procedural approximations, not scanned or Blender-authored character assets.
