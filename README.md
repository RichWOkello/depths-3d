# 🏰 Depths 3D

A first-person 3D dungeon shooter that runs inside Google Colab. It is built with Three.js and Python, and needs no installs.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RichWOkello/depths-3d/blob/main/depths_3d.ipynb)

## Play
1. Click the **Open in Colab** badge above.
2. Run the code cell (▶).
3. Click the game area to start.

> The game needs an internet connection because it loads Three.js from a CDN.

## Controls
| Key | Action |
|---|---|
| W A S D | Move (hold Shift to sprint) |
| ← → or Q E | Turn |
| Space / F / left-click | Fire |
| Right-click + drag | Mouse look |
| R | Restart after death |

## Gameplay
- Every level is a new procedurally generated maze.
- Kill half the enemies to open the cyan portal, then reach it to descend.
- Enemies: 🔴 chasers, 🟣 shooters, 🟠 brutes (from level 3).
- Pick up health, ammo and gems. The minimap fills in as you explore.

## How it works
- Maze generation with a recursive backtracker, plus extra loops and carved rooms
- Grid-based collision, line-of-sight checks and hitscan shooting
- Instanced wall meshes, procedural canvas textures and a flickering torch light
- Web Audio sound effects
