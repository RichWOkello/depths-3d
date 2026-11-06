"""Build web/Colab/paste-cell versions of Depths 3D from src/game.*.

Run: python build.py
Creates: index.html, PLAY_DIRECTLY.html, depths_3d.ipynb, colab_one_cell.py
All outputs carry the same game code (no GitHub dependency or uploads).
"""
import base64
import json
import lzma
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
js = (ROOT / 'src' / 'game.js').read_text(encoding='utf-8')
fragment = (ROOT / 'src' / 'game.html').read_text(encoding='utf-8').strip()
version = next(line.split("'")[1] for line in js.splitlines() if line.startswith('const VERSION='))

# One shared document shell. index.html loads the JS as a separate source file,
# whereas Colab embeds the same JS inline into an HTTP-served document.
def shell(script):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="description" content="Depths 3D is a first-person gothic dungeon shooter playable on the web and in Google Colab.">
<title>Depths 3D v{version} — The Abyssal Expansion</title>
<style>
  * {{ box-sizing:border-box; }}
  html,body {{ margin:0; min-height:100%; background:#0b0d16; color:#dce2f0; font-family:system-ui,Segoe UI,Arial,sans-serif; }}
  main {{ max-width:860px; margin:0 auto; padding:13px; }}
  header {{ text-align:center; padding:2px 0 8px; }}
  h1 {{ margin:0; font-size:22px; color:#ffe1ac; letter-spacing:1px; }}
  .sub {{ font-size:12px; opacity:.75; margin:5px 0; }}
  .game {{ width:100%; max-width:800px; margin:auto; border:1px solid #474250; box-shadow:0 10px 35px #0009; border-radius:9px; overflow:hidden; }}
  #dd3d-root {{ width:100% !important; max-width:none !important; }}
  .help {{ text-align:center; font-size:12px; line-height:1.65; margin:8px auto; color:#b4bdce; }}
  .help b {{ color:#e4edfd; }}
  footer {{ opacity:.7; text-align:center; font-size:11px; padding:4px; }}
</style>
</head>
<body>
<main>
<header><h1>🏰 DEPTHS 3D <small style="font-size:12px;opacity:.6">v{version}</small></h1>
<div class="sub">The Abyssal Expansion · A cinematic dungeon shooter</div></header>
<div class="game">{fragment}</div>
<div class="help"><b>Begin from the title screen; adjust your loadout and preferences in the menu.</b> WASD move · Space/F fire · 1–8 weapons · Esc pause · Complete controls under Settings</div>
<footer>Created by Richard Okello · MIT License</footer>
</main>
{script}
</body>
</html>
'''

web_page = shell('<script src="src/game.js"></script>')
(ROOT / 'index.html').write_text(web_page, encoding='utf-8')
(ROOT / 'PLAY_DIRECTLY.html').write_text(shell('<script>\n' + js.replace('</script', '<\\/script') + '\n</script>'), encoding='utf-8')
# Colab requires a real HTML document served over HTTP, not display(HTML(...))
# with a script tag. That old approach can render a static/broken game output.
colab_page = shell('<script>\n' + js.replace('</script', '<\\/script') + '\n</script>')
payload = base64.b85encode(lzma.compress(colab_page.encode('utf-8'), preset=6)).decode('ascii')
chunks = textwrap.wrap(payload, 118)
blob = '\n'.join('    ' + repr(c) for c in chunks)

colab_code = f'''# DEPTHS 3D v{version} — SINGLE-CELL GOOGLE COLAB GAME
# No ZIP upload, GitHub, git clone, or external Python packages needed.
# Internet is required for Three.js, and WebGL must be enabled in the browser.
import base64, lzma, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from google.colab import output

# Complete, locally embedded game payload: same source as index.html.
GAME_DATA = (\n{blob}\n)
GAME_HTML = lzma.decompress(base64.b85decode(''.join(GAME_DATA))).decode('utf-8')

class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split('?', 1)[0]
        if route not in ('/', '/index.html'):
            self.send_error(404)
            return
        body = GAME_HTML.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('x-colab-notebook-cache-control', 'no-cache')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass

# Stop a previous server if this notebook cell is rerun in the same runtime.
if '_depths_existing_server' in globals():
    try:
        _depths_existing_server.shutdown()
        _depths_existing_server.server_close()
    except Exception:
        pass
# 0 selects an available port without assuming a fixed Colab port.
server = ThreadingHTTPServer(('0.0.0.0', 0), GameHandler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
_depths_existing_server = server
print('Depths 3D v{version} ready. Watch or skip the intro, choose difficulty, then select New expedition.')
print('If it looks blank, enable hardware acceleration/WebGL in your browser.')
output.serve_kernel_port_as_iframe(server.server_port, width='100%', height='700')
'''
(ROOT / 'colab_one_cell.py').write_text(colab_code, encoding='utf-8')

def nb_lines(s):
    xs = s.splitlines(keepends=True)
    return xs if xs else ['']

intro = f'''# 🏰 Depths 3D v{version} — The Abyssal Expansion Edition

Play the same game in **Google Colab**, through **PLAY_DIRECTLY.html**, or with **index.html** on GitHub Pages.

The v5 expansion adds simulated ballistic projectiles, magazine reloads, advanced enemy behaviors, nine environmental themes, rune and crypt-key objectives, breakable secret walls, interactive hazards, four named phased bosses, weapon upgrades, inventory, and browser campaign saving.

1. Connect a Colab Python runtime and **Run the code cell** below.
2. Watch the short intro (or skip it), choose **CLICK TO START**, select the difficulty, then choose **New expedition** from the minimal main menu. Loadout and settings are separate screens.
3. Click inside the game to focus. **WASD** moves; **Q/E** or **←/→** turns; mouse drag looks around; **Space/F** fires; **R** reloads; **1–8** selects weapons; **Tab** opens the armory; **I** opens inventory; **X** activates runes; **H** uses a medkit; **C** parries with blades; **V** releases a charged saber wave.

The notebook hosts the real page in an iframe with `google.colab.output.serve_kernel_port_as_iframe`. The previous approach of embedding a JavaScript `<script>` with `display(HTML(...))` is no longer used.

No files need to be uploaded to Colab. Three.js is loaded from a CDN and WebGL support is required.

*Created by Richard Okello · MIT License.*
'''
notebook = {
    'cells': [
        {'cell_type':'markdown', 'id':'depths-3d-guide', 'metadata': {}, 'source':nb_lines(intro)},
        {'cell_type':'code', 'id':'depths-3d-game', 'metadata': {}, 'execution_count':None, 'outputs':[], 'source':nb_lines(colab_code)}
    ],
    'metadata': {'colab':{'provenance': []},'kernelspec':{'display_name':'Python 3','name':'python3'},'language_info':{'name':'python'}},
    'nbformat':4,'nbformat_minor':5
}
(ROOT / 'depths_3d.ipynb').write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'Built v{version}: index.html, PLAY_DIRECTLY.html, depths_3d.ipynb, colab_one_cell.py')
print(f'  JavaScript: {len(js):,} chars | Colab cell: {len(colab_code):,} chars')
