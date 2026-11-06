# Changelog

## [5.0.0] — 2026-11-06 · The Abyssal Expansion

Major update from v4.0.0, combining the improvements developed through the v4.x and v5.0 development passes under one public **v5.0.0** release.

### Combat and weapon models
- Expanded to eight weapon slots, including a katana and Light Saber alongside six real-world-inspired firearms and launchers.
- Added simulated projectile movement, ballistic grenades, collision-based impacts, weapon recoil, reloads, weak points, burns, guard/parry, and distinct melee attacks.
- Corrected the first-person katana and energy-saber models, one-hand hilt grips, camera stances, attack arcs, and gradual saber ignition.
- Added layered explosions, flames, hit reactions, sound effects and attack trails.

### Enemies and dungeons
- Added varied monster archetypes, maze navigation, procedural grounded gait, detection/retreat/flanking behavior, and named multi-phase bosses.
- Expanded the Gothic environments with stone architecture, stained glass, ossuaries, chained skeletons, pools, hazards, room set pieces, hidden passages and mechanisms.
- Added keys, ritual switches and other exploration objectives in the campaign.

### Player systems and user interface
- Added progression, equipment upgrades, inventory, Soul Forge, campaign saving, Survival mode and New Game+.
- Reorganized the cinematic introduction, New Expedition / Continue navigation, Loadout, Records, Settings and pause interfaces into minimal dedicated screens.
- Retained quick weapons, minimap, checkpoints and difficulty selection.

### Cross-platform release
- One canonical source in `src/game.js`, rebuilt into GitHub Pages `index.html`, standalone `PLAY_DIRECTLY.html`, and the self-contained Colab notebook.
- Added professional README, release notes, update guide and build verification workflow for the existing GitHub repository.

### Validation
- See `TEST_REPORT.md` and `FEATURE_MATRIX.md`. Automated tests validate source behavior with simulated rendering; real hardware WebGL and Colab acceptance require manual testing.

## Previous public releases

Development before the v5.0.0 release included v4.0.0 and earlier versions. The detailed internal intermediate notes are archived in [docs/DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md). Those intermediate build labels are not separate v5.x GitHub releases.
