# Changelog

## [3.0.0] - 2026-11-06
### Added
- **Redesigned menu:** gradient title, Play / Stats / Settings tabs, weapon, difficulty and mode pickers.
- **Perks:** pick 1 of 3 upgrades after every floor.
- **Two new guns:** Grenade Launcher (splash damage) and Flamethrower (short range, piercing), each with its own model. Six guns total.
- **New monsters:** teleporters that blink around you, and splitters that burst into minis.
- **Explosive barrels** that chain-explode and hurt enemies (and you).
- **Settings:** mouse sensitivity, field of view and volume (saved).
- **Game modes:** Normal, Hardcore (no respawns) and Daily (seeded dungeon layouts).
- **Progress:** local top-10 leaderboard, lifetime stats and 6 achievements.
- **Game feel:** screen shake and floating damage numbers.
- **Gamepad support** (sticks to move/look, trigger or A to fire, right bumper to switch gun).
- Includes all v2.1.0 changes (checkpoints, gun models, graphics, combo multiplier).

## [2.1.0] - 2026-11-06
### Added
- **Checkpoints:** two glowing shrines per floor. Touch one to save your spot (+40 HP, +10 ammo). Dying lets you respawn at the last checkpoint (or the floor start) instead of restarting the whole run.
- **Unique gun models:** pistol, double-barrel shotgun, SMG with magazine, and a glowing-ring railgun.
- **Graphics:** per-floor colour themes, bump-mapped walls, wall-mounted flickering torches, vignette, and sharper rendering on high-DPI screens.
- **Combo multiplier** for kill streaks, and 3 seconds of protection after respawning.
- Minimap shows checkpoints.

## [2.0.0] - 2026-11-05
### Added
- **New menu interface:** main menu, pause menu and game-over menu with weapon cards, difficulty (Easy / Normal / Hard) and clickable buttons.
- **Weapon selection:** Pistol, Shotgun, SMG and Railgun (pierces every enemy in line). Switch in-game with `1`-`4` or the mouse wheel.
- **Monster models:** imps, eye-demons, ogres and a winged demon-lord boss, built from 3D shapes with horns, eyes, claws and tentacles, and turning to face you.
- Includes all v1.1.1 fixes (CDN fallback, clearer README).

### Changed
- Clicking the game no longer starts it; use the menu buttons (or `R`).

## [1.1.1] - 2026-11-05
### Fixed
- Standalone page: if the primary CDN is blocked or slow, the game now falls back to a second CDN (jsDelivr) before giving up.
- Clearer load-failure message that also covers reloading the standalone page.

### Changed
- README: the easiest way to play locally is now to double-click `index.html`. Added Windows-friendly server command (`py -m http.server`) and clarified that GitHub Pages must be enabled first.

## [1.1.0] - 2026-11-05
### Added
- **Boss floors:** every 5th level has a boss with a triple-spread attack and contact damage (1000 points).
- **Saved high score** (browser localStorage) shown in the HUD, title screen and game-over screen.
- **Pause** with `P` or `Esc`.
- **Mouse capture:** left-click captures the mouse for smooth mouse look where the browser allows it. Right-drag still works everywhere.
- **Standalone web version** (`index.html`) that can be hosted on GitHub Pages.
- `src/` folder and `build.py` to generate the notebook and web page from one source.
- MIT license, changelog and expanded README.

### Changed
- Enemy AI refactored so shooters and bosses share ranged logic; contact damage applies to any enemy with a melee value.
- Title screen shows the game version.

## [1.0.0] - 2026-11-03
### Added
- First release: procedural 3D mazes, fog and torchlight, chasers/shooters/brutes, pickups, minimap, portal progression, sound effects.
- Google Colab notebook.
