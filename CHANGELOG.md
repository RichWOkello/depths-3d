# Changelog

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
