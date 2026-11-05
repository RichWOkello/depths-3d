# Changelog

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
