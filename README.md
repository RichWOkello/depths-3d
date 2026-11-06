# 🏰 Depths 3D

A first-person 3D dungeon shooter built with **Three.js**. Play it in your browser, or run it inside **Google Colab**. Nothing to install.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RichWOkello/depths-3d/blob/main/depths_3d.ipynb)
![version](https://img.shields.io/badge/version-3.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)

## Play

| Option | How |
|---|---|
| **Easiest: on your computer** | Download or clone this repo and **double-click `index.html`**. No server needed. |
| **In Colab** | Click the **Open In Colab** badge, run the cell, then click the game |
| **On the web** | Enable GitHub Pages (steps below), then open **https://richwokello.github.io/depths-3d/** |
| **Local server (optional)** | In this folder run `py -m http.server 8000` (Windows) or `python3 -m http.server 8000` (Mac/Linux), then open http://localhost:8000 |

> The game loads Three.js from a CDN, so it needs an internet connection.

## Controls

| Key | Action |
|---|---|
| W A S D | Move (hold **Shift** to sprint) |
| ← → or Q E | Turn |
| Space / F / left-click | Fire |
| 1 2 3 4 or mouse wheel | Switch weapon (Pistol, Shotgun, SMG, Railgun) |
| Right-click + drag | Mouse look (in the standalone page, left-click also captures the mouse) |
| P / Esc | Pause |
| R | Restart after death |

## Gameplay

- Every floor is a freshly generated maze that gets bigger and deadlier.
- Kill **half the enemies** to open the cyan portal, then reach it to descend.
- 3D monsters: 👹 **Imps** rush you, 👁 **Eye-demons** float back and spit orbs, **Ogres** (floor 3+) are slow and tough.
- Four guns: Pistol, Shotgun, SMG and a piercing Railgun. Pick your starting gun and difficulty in the main menu.
- 👹 **Every 5th floor is a boss floor**, with a huge enemy that fires triple spreads.
- **Checkpoints:** two shrines per floor save your spot. After death you respawn at the last one (15% score penalty, 3 seconds of protection).
- Kill streaks build a **combo multiplier**. Each floor has its own colour theme and wall-mounted torches.
- **Perks:** clear a floor and pick 1 of 3 upgrades (damage, fire rate, max HP, life steal, ammo, speed).
- **6 guns** (adds Grenade Launcher and Flamethrower), explosive barrels, **teleporter** and **splitter** monsters.
- **Modes:** Normal, Hardcore (no respawns) and Daily (same dungeons for everyone). Includes a top-10 board, stats and achievements.
- Pick up health, ammo and gems. The minimap fills in as you explore.
- Your **best score** is saved in your browser.

## What's new

See [CHANGELOG.md](CHANGELOG.md). v1.1 highlights: boss floors, saved high score, pause key, mouse capture, and a standalone web version you can host on GitHub Pages.

## How it works

- Maze generation with a recursive backtracker, extra loops and carved rooms
- Grid collision, line-of-sight checks, BFS-style distance logic and hitscan shooting
- Instanced wall meshes, procedural canvas textures, a flickering torch light
- Web Audio sound effects (no audio files)

## Project structure

```
depths-3d/
├── src/
│   ├── game.js        # the whole game (Three.js)
│   └── game.html      # HUD / overlay markup
├── index.html         # standalone web page (generated)
├── depths_3d.ipynb    # Colab notebook (generated)
├── build.py           # regenerates index.html and the notebook from src/
├── CHANGELOG.md
└── LICENSE
```

Edit files in `src/`, then run `python build.py` to rebuild `index.html` and `depths_3d.ipynb`.

## Enable GitHub Pages

1. Open the repo on GitHub → **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch **main** and folder **/ (root)**, then **Save**.
4. After a minute the game is live at `https://richwokello.github.io/depths-3d/`.

## Author

Created by **Richard Okello** ([@RichWOkello](https://github.com/RichWOkello)).

## License

[MIT](LICENSE) © 2026 Richard Okello
