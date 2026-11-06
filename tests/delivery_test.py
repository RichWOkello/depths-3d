from pathlib import Path
import json,sys,types,urllib.request,threading,functools,http.server,socketserver,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'src/game.js').read_text()
nb=json.loads((ROOT/'depths_3d.ipynb').read_text())
assert nb['nbformat']==4
code=''.join(c['source'][0] if isinstance(c['source'],list) and len(c['source'])==1 else ''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in nb['cells'] if c['cell_type']=='code')
compile(code,'<colab>','exec')
compile((ROOT/'colab_one_cell.py').read_text(),'<one-cell>','exec')
assert "script src=\"src/game.js\"" in (ROOT/'index.html').read_text()
assert 'Light Saber' in js and 'click to start' in js.lower()
print('PASS: notebook schema, Colab Python cell compilation, single shared JavaScript source')
# Fake the Colab iframe handoff and verify the actual embedded HTML is served.
google=types.ModuleType('google');colab=types.ModuleType('google.colab');output=types.ModuleType('google.colab.output')
ports=[]
output.serve_kernel_port_as_iframe=lambda port,**kw:ports.append(port)
colab.output=output;google.colab=colab
sys.modules['google']=google;sys.modules['google.colab']=colab;sys.modules['google.colab.output']=output
ns={}
exec(compile(code,'<colab>','exec'),ns)
assert ports
served=urllib.request.urlopen(f'http://127.0.0.1:{ports[0]}/',timeout=8)
html=served.read().decode('utf8')
assert served.status==200 and '<script>' in html and 'const VERSION=\'5.0.0\'' in html
assert 'const ART_MENU=' in html and 'Light Saber' in html
ns['server'].shutdown();ns['server'].server_close()
print('PASS: Colab cell starts HTTP server and serves complete game HTML with artwork')
# Confirm GitHub Pages entry point serves the same source files from a static HTTP server.
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet)
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
for resource in ('index.html','src/game.js'):
 with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/{resource}',timeout=8) as r:
  assert r.status==200 and r.read()
server.shutdown();server.server_close()
print('PASS: static HTTP entrypoint and shared JavaScript both return HTTP 200')
print('NOTE: browser navigation to file:// and localhost is blocked by sandbox policy; JS UI was tested by set_content() separately')
