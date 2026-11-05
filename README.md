# 🏰 Depths 3D

A first-person 3D dungeon shooter built with **Three.js**. Play it in your browser, or run it inside **Google Colab**. Nothing to install.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RichWOkello/depths-3d/blob/main/depths_3d.ipynb)
![version](https://img.shields.io/badge/version-1.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)

## Play

| Option | How |
|---|---|
| **In the browser** | Open **https://richwokello.github.io/depths-3d/** (see *Enable GitHub Pages* below) |
| **In Colab** | Click the **Open In Colab** badge, run the cell, then click the game |
| **Locally** | Run `python -m http.server` in this folder and open http://localhost:8000 |

> The game loads Three.js from a CDN, so it needs an internet connection.

## Controls

| Key | Action |
|---|---|
| W A S D | Move (hold **Shift** to sprint) |
| ← → or Q E | Turn |
| Space / F / left-click | Fire |
| Right-click + drag | Mouse look (in the standalone page, left-click also captures the mouse) |
| P / Esc | Pause |
| R | Restart after death |

## Gameplay

- Every floor is a freshly generated maze that gets bigger and deadlier.
- Kill **half the enemies** to open the cyan portal, then reach it to descend.
- 🔴 **Chasers** rush you, 🟣 **Shooters** keep their distance and fire orbs, 🟠 **Brutes** (floor 3+) are slow and tough.
- 👹 **Every 5th floor is a boss floor**, with a huge enemy that fires triple spreads.
- Pick up health, ammo and gems. The minimap fills in as you explore.
- Your **best score** is saved in your browser.

## What's new in v1.1.0

See [CHANGELOG.md](CHANGELOG.md). Highlights: boss floors, saved high score, pause key, mouse capture, and a standalone web version you can host on GitHub Pages.

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
