"""Build the Colab notebook and the standalone web page from src/.

Usage:  python build.py
Writes: depths_3d.ipynb  and  index.html
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
js = (ROOT / "src" / "game.js").read_text(encoding="utf-8")
frag = (ROOT / "src" / "game.html").read_text(encoding="utf-8")
VERSION = next(l.split("'")[1] for l in js.splitlines() if l.startswith("const VERSION="))

assert '"""' not in js and '"""' not in frag, "triple quotes would break the Colab cell"


def lines(text):
    parts = text.rstrip("\n").split("\n")
    return [p + "\n" for p in parts[:-1]] + [parts[-1]]


# ---------- Colab notebook ----------
code = f'''#@title 🏰 Depths 3D v{VERSION} — first-person dungeon shooter (needs internet for three.js)
import uuid
from IPython.display import HTML, display

_uid = uuid.uuid4().hex[:8]

_html = r"""{frag.rstrip()}
<script>
{js}
</script>"""

display(HTML(_html.replace("dd3d-root", "g" + _uid)))
'''

md = f"""# 🏰 Depths 3D  ·  v{VERSION}
A first-person 3D dungeon shooter (Three.js) running inside Colab. Run the cell below, then **click the game** to start.

| Key | Action |
|---|---|
| **W A S D** | Move (hold **Shift** to sprint) |
| **← →** or **Q E** | Turn |
| **Space / F / left-click** | Fire |
| **Right-click + drag** | Mouse look |
| **P** | Pause |
| **R** | Restart after death |

**Goal:** kill half the enemies to open the cyan portal, reach it, and descend. Every 5th floor is a boss floor.

*Created by Richard Okello. MIT licensed.*"""

nb = {
    "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": lines(md)},
        {"cell_type": "code", "metadata": {"cellView": "form"}, "execution_count": None, "outputs": [], "source": lines(code)},
    ],
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}
(ROOT / "depths_3d.ipynb").write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")

# ---------- standalone web page (GitHub Pages) ----------
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Depths 3D — a first-person dungeon shooter</title>
<style>
  body {{ margin:0; min-height:100vh; background:#0b0b12; color:#dcdce8; font-family:Segoe UI,Arial,sans-serif;
         display:flex; flex-direction:column; align-items:center; justify-content:center; padding:16px; box-sizing:border-box; }}
  h1 {{ margin:0 0 4px; font-size:22px; }}
  .sub {{ opacity:.65; font-size:13px; margin-bottom:12px; }}
  .game {{ box-shadow:0 8px 40px #000a; border-radius:8px; overflow:hidden; }}
  footer {{ margin-top:14px; font-size:12px; opacity:.55; text-align:center; line-height:1.6; }}
  a {{ color:#8ab4ff; }}
</style>
</head>
<body>
<h1>🏰 Depths 3D <span style="font-size:13px;opacity:.6">v{VERSION}</span></h1>
<div class="sub">W A S D move · ← → turn · Space/F/click fire · right-drag look · P pause</div>
<div class="game">
{frag.rstrip()}
</div>
<footer>Created by Richard Okello · <a href="https://github.com/RichWOkello/depths-3d">GitHub</a> · MIT License</footer>
<script src="src/game.js"></script>
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"Built v{VERSION}: depths_3d.ipynb, index.html")
