from pathlib import Path
from PIL import Image,ImageFilter
import base64,io,json,html,zipfile,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parent
addon=(ROOT/'src/bestiary_pass.js').read_text()
base=(ROOT/'src/game_base.js').read_text()
assert base.count('function start(){')==1
GAME=base.replace('function start(){','function start(){\n'+addon+'\n',1)
(ROOT/'src/game.js').write_text(GAME)
fragment=(ROOT/'src/game.html').read_text()
style='''<style>html,body{margin:0;padding:0;min-height:100%;background:#09080c;color:#ddd;font-family:system-ui,sans-serif}body{display:flex;justify-content:center;align-items:center;min-height:100vh}#dd3d-root{box-shadow:0 0 40px #07070a;width:min(100vw,800px)!important;max-height:min(100vh,700px)}*{box-sizing:border-box}</style>'''
prefix='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DEPTHS 3D v6.0.0 — The Bestiary Expansion</title>'+style+'</head><body>'
(ROOT/'index.html').write_text(prefix+fragment+'<script src="src/game.js"></script></body></html>')
GAME_HTML=prefix+fragment+'<script>\n'+GAME+'\n</script></body></html>'
(ROOT/'PLAY_DIRECTLY.html').write_text(GAME_HTML)
subprocess.run(['node','--check',str(ROOT/'src/game.js')],check=True)
# self-contained viewer thumbnails and approximation masks
IMAGES={}
for typ in ['brute','crawler','imp','wraith','necromancer','gargoyle']:
 im=Image.open(ROOT/'refs'/f'{typ}.png').convert('RGB')
 im.thumbnail((500,450))
 b=io.BytesIO();im.save(b,format='WEBP',quality=80,method=5)
 IMAGES[typ]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
# extra JS data mapping only, reference imagery is for the viewer, not inserted in the game
image_map=json.dumps(IMAGES,separators=(',',':'))
viewer_head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Depths 3D — Bestiary Viewer</title><style>
*{box-sizing:border-box}body{margin:0;background:#09090f;color:#e9e4dc;font:14px system-ui,Segoe UI,sans-serif}header{padding:12px 18px;background:#18151e;border-bottom:1px solid #493d4b;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}h1{font:600 20px Georgia,serif;margin:0}small{color:#aca4b2}main{max-width:1250px;margin:12px auto;padding:0 12px}.switch,.actions,.tools{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}button{border:1px solid #625064;background:#251c2c;color:#eee;border-radius:6px;padding:9px 12px;cursor:pointer;font:inherit}button.active,button:hover{border-color:#e7ae81;background:#53364c}.screens{display:grid;grid-template-columns:1fr 1fr;gap:12px}.panel{position:relative;background:linear-gradient(#1c1820,#0c0b11);border:1px solid #554750;border-radius:8px;min-width:0;overflow:hidden}.panel h2{font-size:14px;margin:0;padding:9px 12px;border-bottom:1px solid #4a3948}#reference{transition:transform .3s ease;width:100%;height:470px;object-fit:contain;object-position:center;background:#0c0b0e}#stage{width:100%;height:470px;position:relative;touch-action:none;background:radial-gradient(ellipse at 40% 40%,#302a32,#09090d)}#stage canvas{display:block;width:100%;height:100%}#over{position:absolute;inset:0;object-fit:contain;width:100%;height:100%;opacity:0;pointer-events:none;filter:grayscale(1) contrast(7) brightness(2);mix-blend-mode:screen}label{display:flex;align-items:center;gap:8px}input{accent-color:#cc8ca4}#status{padding:12px;background:#18141a;border-radius:6px;margin-top:9px;line-height:1.6}#error{color:#ffb3a3}footer{margin:10px auto;max-width:1000px;color:#aa9da9;font-size:12px} @media(max-width:760px){.screens{grid-template-columns:1fr}#stage,#reference{height:320px}}</style></head><body><header><div><h1>DEPTHS 3D v6.0.0 — BESTIARY EXPANSION</h1><small>Original photo references and actual procedural Three.js creatures · v6.0.0</small></div><span id="error">Loading Three.js...</span></header><main><div class="switch" id="species"></div><div class="screens"><section class="panel"><h2>Reference photograph / concept crop</h2><img id="reference" alt="Reference crop"></section><section class="panel"><h2>Interactive procedural 3D model · drag to turn · scroll to zoom</h2><div id="stage"><img id="over" alt="Approximate silhouette alignment"></div></section></div><div class="actions" id="actions"></div><div class="tools"><label><input id="spin" type="checkbox" checked>Auto-turntable</label><label><input id="overlay" type="checkbox">Reference silhouette overlay (approximate)</label><label>Overlay opacity <input id="opacity" type="range" min="0" max="65" value="23"></label><button id="sound">Play synthesized monster voice</button><button id="reset">Reset view</button><button id="faceview">Compare faces up close</button><label>Load GLB replacement <input id="glb" type="file" accept=".glb"></label></div><div id="status"></div></main><footer>Reference artwork is provided only for visual comparison. The shader-based procedural model is an approximation, not a copy or a photogrammetry reconstruction; no GLB models are included. Browser must support WebGL and reach one of the Three.js CDNs.</footer>
<script>
const REF_DATA=__REF_DATA__;
const MODEL_LABELS={brute:'Flesh Brute',crawler:'Crypt Crawler',imp:'Flesh Imp',wraith:'Gaunt Hooded Wraith',necromancer:'Necromancer',gargoyle:'Winged Gargoyle'};
function threeLoader(urls,done){if(window.THREE){done();return;}if(!urls.length){document.getElementById('error').textContent='Could not load Three.js from CDNs';return;}let script=document.createElement('script');script.src=urls[0];script.onload=()=>threeLoader(urls.slice(1),done);script.onerror=()=>threeLoader(urls.slice(1),done);document.head.appendChild(script);}
const installBestiary=function(){
__MODULE__
};
function startViewer(){
 try{
 installBestiary();
 const B=window.DEPTHS_BESTIARY,types=B.TYPES;
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'high-performance'});
 renderer.setPixelRatio(Math.min(1.5,window.devicePixelRatio||1));renderer.outputEncoding=THREE.sRGBEncoding;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.83;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 const el=document.getElementById('stage');el.insertBefore(renderer.domElement,el.firstChild);
 const scene=new THREE.Scene();scene.background=new THREE.Color(0x141118);
 const camera=new THREE.PerspectiveCamera(49,1,.08,65);let camDist=5.4,angle=.22,focusY=1.25,faceView=false;camera.position.set(0,1.5,camDist);
 const hemi=new THREE.HemisphereLight(0x8d9cab,0x18101a,.7);scene.add(hemi);
 const key=new THREE.DirectionalLight(0xffc6a6,2.5);key.position.set(3,5,4);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.near=.5;key.shadow.camera.far=14;scene.add(key);
 const fill=new THREE.PointLight(0x7264ad,.7,11);fill.position.set(-2,1,-3);scene.add(fill);
 const platform=new THREE.Mesh(new THREE.CylinderGeometry(2.05,2.05,.22,60),new THREE.MeshStandardMaterial({color:0x221b22,metalness:.35,roughness:.75}));platform.position.y=-.18;platform.receiveShadow=true;scene.add(platform);
 let mesh=null,entity=null,mode='idle',selected='brute',active=true,actorTurn=0,audio=null;
 function resize(){const w=el.clientWidth||500,h=el.clientHeight||400;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
 function select(type){selected=type;if(mesh){scene.remove(mesh);}
  document.getElementById('reference').src=REF_DATA[type];document.getElementById('over').src=REF_DATA[type];
  mesh=B.build(type);mesh.position.y=B.SPEC[type].baseY;scene.add(mesh);
  entity={mesh:mesh,ai:mode,state:mode,moveMag:0,pose:0,strike:0,hitT:0,deadT:0,alert:mode!=='idle'};
  document.querySelectorAll('#species button').forEach(b=>b.classList.toggle('active',b.dataset.id===type));setMode('idle');
  faceView=false;focusY=Math.max(.60,Math.min(1.55,B.SPEC[type].baseY+.12));camDist=type==='crawler'||type==='imp'?4.1:5.4;document.getElementById('reference').style.transform='none';
  showStats();}
 function showStats(){const g=mesh.userData.bestiary,st=B.geometryStats()[selected];document.getElementById('status').textContent=
  `${MODEL_LABELS[selected]} · height: ${B.SPEC[selected].height}m · named body bones: ${Object.keys(g.bones).length} · LOD triangles: ${st.triangles.join(' / ')} · first-build mesh generation: ${st.ms.toFixed(1)} ms · Stage: ${mode}. Selected comparison crop is illustrated in 2D; proportions are artistic estimates.`;}
 function setMode(m){mode=m;if(!entity)return;entity.state=m;entity.ai=m;entity.alert=m!=='idle';entity.moveMag=m==='walk'?1:0;entity.pose=m==='attack'?1:0;entity.strike=m==='attack'?1:0;entity.hitT=m==='hit'?.85:0;entity.deadT=m==='death'?1:0;
  document.querySelectorAll('#actions button').forEach(b=>b.classList.toggle('active',b.dataset.mode===m));}
 for(const type of types){let b=document.createElement('button');b.textContent=MODEL_LABELS[type];b.dataset.id=type;b.onclick=()=>select(type);document.getElementById('species').appendChild(b);}
 for(const v of ['idle','walk','attack','hit','death']){let b=document.createElement('button');b.textContent=v[0].toUpperCase()+v.slice(1);b.dataset.mode=v;b.onclick=()=>setMode(v);document.getElementById('actions').appendChild(b);}
 document.getElementById('spin').onchange=ev=>{active=ev.target.checked;};
 const overlay=document.getElementById('over');document.getElementById('overlay').onchange=ev=>{overlay.style.opacity=ev.target.checked?(Number(document.getElementById('opacity').value)/100):0;};
 document.getElementById('opacity').oninput=ev=>{if(document.getElementById('overlay').checked)overlay.style.opacity=Number(ev.target.value)/100;};
 document.getElementById('reset').onclick=()=>{faceView=false;camDist=selected==='crawler'||selected==='imp'?4.1:5.4;focusY=Math.max(.6,Math.min(1.55,B.SPEC[selected].baseY+.12));angle=.22;document.getElementById('reference').style.transform='none';};
 document.getElementById('faceview').onclick=()=>{
  faceView=!faceView;
  if(faceView){const spec=B.SPEC[selected];focusY=spec.baseY+spec.anchors.head[1];camDist=selected==='brute'?1.75:selected==='gargoyle'?1.45:1.20;
   const origins={brute:'47% 24%',crawler:'28% 30%',imp:'53% 32%',wraith:'37% 19%',necromancer:'50% 21%',gargoyle:'47% 33%'};
   document.getElementById('reference').style.transformOrigin=origins[selected];
   document.getElementById('reference').style.transform='scale(1.55)';
  } else{camDist=selected==='crawler'||selected==='imp'?4.1:5.4;focusY=Math.max(.6,Math.min(1.55,B.SPEC[selected].baseY+.12));document.getElementById('reference').style.transform='none';}
  document.getElementById('faceview').textContent=faceView?'Show full bodies':'Compare faces up close';
 };
 document.getElementById('sound').onclick=()=>{audio=audio||new(window.AudioContext||window.webkitAudioContext)();B.voice(selected,audio,true);};
 document.getElementById('glb').onchange=ev=>{const file=ev.target.files[0];if(!file)return;const url=URL.createObjectURL(file);const old=document.getElementById('error');old.textContent='Loading GLB viewer support...';let s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js';s.onload=()=>{
   if(!THREE.GLTFLoader){old.textContent='GLTFLoader unavailable';return;}
   B.tryGLB(selected,url,new THREE.GLTFLoader(),scene3=>{if(mesh){scene.remove(mesh);}mesh=scene3;mesh.position.y=0;scene.add(mesh);entity=null;old.textContent='Custom GLB loaded';URL.revokeObjectURL(url);},reason=>{old.textContent=reason;URL.revokeObjectURL(url);});
  };s.onerror=()=>{old.textContent='GLTFLoader CDN unavailable';URL.revokeObjectURL(url);};document.head.appendChild(s);};
 let dragging=false,prev=0;el.addEventListener('pointerdown',e=>{dragging=true;prev=e.clientX;el.setPointerCapture(e.pointerId);});el.addEventListener('pointermove',e=>{if(!dragging)return;angle+=(e.clientX-prev)*.006;prev=e.clientX;});el.addEventListener('pointerup',()=>dragging=false);el.addEventListener('wheel',e=>{e.preventDefault();camDist=Math.max(2.7,Math.min(10,camDist+e.deltaY*.004));},{passive:false});
 select('brute');resize();window.addEventListener('resize',resize);document.getElementById('error').textContent='Three.js ready';
 let last=performance.now(),clock=0;
 function frame(now){requestAnimationFrame(frame);let dt=Math.min(.05,(now-last)/1000);last=now;clock+=dt;
  if(active)angle+=dt*.25;
  if(mesh){mesh.rotation.y=angle;if(entity){if(mode==='attack')entity.pose=.5+.5*Math.sin(clock*5);if(mode==='hit')entity.hitT=.5+.5*Math.sin(clock*4);if(mode==='death')entity.deadT=Math.min(1,entity.deadT+dt*.2);B.update(entity,dt,clock);}}
  camera.position.set(Math.sin(.08)*.2,focusY+.15,camDist);camera.lookAt(0,focusY,0);renderer.render(scene,camera);
 }
 requestAnimationFrame(frame);
 }catch(err){document.getElementById('error').textContent='Viewer error: '+err.message;console.error(err);}
}
threeLoader(['https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js','https://unpkg.com/three@0.128.0/build/three.min.js'],startViewer);
</script></body></html>'''
viewer=viewer_head.replace('__REF_DATA__',image_map).replace('__MODULE__',addon)
(ROOT/'BESTIARY_VIEWER.html').write_text(viewer)
# Measurements, features, and notebook
SPEC={
 'brute':['Flesh Brute',2.70,.17,.59,.34,.84,16],
 'crawler':['Crypt Crawler',.90,.19,.89,.82,.71,74],
 'imp':['Flesh Imp',1.20,.43,.51,.36,.46,41],
 'wraith':['Gaunt Hooded Wraith',2.10,.13,.74,.42,.34,23],
 'necromancer':['Necromancer',2.40,.13,.58,.47,.42,9],
 'gargoyle':['Winged Gargoyle',1.40,.22,.61,.42,.58,43],
}
palette={'brute': ['#a49da3', '#89828a', '#777179', '#65585f', '#493c41', '#2b262b'], 'crawler': ['#b3a7a9', '#918387', '#76676d', '#604e54', '#493c43', '#29252a'], 'imp': ['#bd939e', '#a57586', '#875567', '#663d51', '#4d2c38', '#281e27'], 'wraith': ['#a6a3a7', '#817b82', '#676169', '#514b53', '#38343b', '#211d25'], 'necromancer': ['#211a22', '#31212b', '#422c36', '#55313c', '#67424b', '#81616a'], 'gargoyle': ['#b5a7a9', '#8c7e80', '#73676c', '#5d5056', '#42383f', '#272228']}
lines=['# Six-creature reference measurements','',
'Ratios and posture are **visual estimates** derived from a single image, not actual measurable 3D anatomy. Heights come from the user specification. Palette hex values were sampled from pixels in the reference crop; lighting, background, and compression affect them.','',
'| Creature | Height (m) | Head:body | Arm:height | Leg:height | Shoulder:height | Posture from vertical | Six reference-pixel colors |',
'|---|---:|---:|---:|---:|---:|---:|---|']
for typ,a in SPEC.items():lines.append('| '+a[0]+' | '+str(a[1])+' | '+str(a[2])+' | '+str(a[3])+' | '+str(a[4])+' | '+str(a[5])+' | '+str(a[6])+'° | '+', '.join('`'+q+'`' for q in palette[typ])+' |')
(ROOT/'MEASUREMENTS.md').write_text('\n'.join(lines)+'\n')
features={
'brute':[('Huge hunched torso','Structural match'),('Tiny recessed head','Partial'),('Large open roar mouth','Partial'),('Visible pot belly','Structural match'),('Grey-pink mottling','Partial'),('Scars/stitches','Partial'),('Arms reach to knees','Structural match'),('Leather forearm bindings','Partial'),('Ragged loincloth','Partial'),('Weighted knuckle walk','Partial')],
'crawler':[('Crouched quadrupedal stance','Structural match'),('Long forelimbs','Structural match'),('Arched back','Structural match'),('Spinal ridge','Partial'),('Visible rib relief','Partial'),('Sunken skull-like head','Partial'),('Four planted claws','Partial'),('Leathery brown-grey skin','Partial'),('Crawling spine wave','Structural match'),('Fully grounded diagonal gait','Not verified')],
'imp':[('Oversized bulbous head','Structural match'),('Giant glossy eyes','Partial'),('Pupil dilation','Structural match'),('Blinking eyelids','Partial'),('Raw pink-red skin','Partial'),('Tiny needle-tooth mouth','Partial'),('Squat hunch','Structural match'),('Clawed short limbs','Partial'),('Scamper and squash','Partial'),('Four-to-six imp group spawning','Partial')],
'wraith':[('Very tall narrow frame','Structural match'),('Gaunt angled pose','Structural match'),('Deep hood','Partial'),('Hollow skull face','Partial'),('Extremely long hands','Partial'),('Ragged hem','Partial'),('Grey-brown fabric','Partial'),('Floating movement','Structural match'),('Teleport dissolve','Partial'),('Homing spectral orbs','Structural match')],
'necromancer':[('Towering robed silhouette','Structural match'),('Deep hood','Partial'),('Skull-like face','Partial'),('Maroon-black robe','Partial'),('Purple ornaments','Partial'),('Spiked shoulder pieces','Partial'),('Bone trophies','Partial'),('Ornate arcane staff','Partial'),('Pulsing glowing staff orb','Structural match'),('Rune-casting free hand','Partial')],
'gargoyle':[('Crouched compact posture','Structural match'),('Large membranous wings','Structural match'),('Wing finger bones','Structural match'),('Horned head','Partial'),('Lean muscular physique','Structural match'),('Ragged holes in membrane','Partial'),('Clawed gripping feet','Partial'),('Long tail','Partial'),('Perched wake and swoop AI','Structural match'),('Correct game collision/flying height','Not verified')]}
feature_lines=['# Six-monster feature audit','',
'**Status key:** Structural match = element exists in geometry or game logic, NOT a verified visual match; Partial = rough procedural approximation; Not verified = cannot certify without playing WebGL game. Nothing here asserts exact reference likeness.','']
for typ,vals in features.items():
 feature_lines.extend(['## '+SPEC[typ][0],'','| Reference requirement | Status |','|---|---|'])
 for a,b in vals:feature_lines.append('| '+a+' | '+b+' |')
 feature_lines.append('')
(ROOT/'FEATURE_MATCH_REPORT.md').write_text('\n'.join(feature_lines))
# Notebook: ONE game code cell contains full plain HTML and builds a transient HTTP server; second optional code cell only opens viewer
import nbformat
nb=nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_markdown_cell('# DEPTHS 3D v6.0.0 — The Bestiary Expansion\n\nThe game is loaded by **one primary code cell** below; after running it the game appears in a Colab iframe. An optional second cell shows the six-creature comparison gallery. These monsters are procedural visual approximations, not photogrammetry copies.'))
nb.cells.append(nbformat.v4.new_markdown_cell('\n'.join(lines)))
nb.cells.append(nbformat.v4.new_markdown_cell('## Technique plan\n\nThe existing game has been preserved, including its controls, eight weapons, dungeons, bosses, save and Soul Forge. The bestiary extension builds cached signed-distance surfaces for body masses; articulated skinned lofts for limbs; 17 named body bones; 4 bone influences per vertex; low-, medium- and high-detail meshes; procedural skin textures; attached eyes, claws, teeth, cloth, staff, and bat wings. Animations read gameplay states. The game uses **Three.js r128 via a CDN with two CDN fallbacks**, so running it requires internet and browser WebGL. No external model/image/audio file is required to play.'))
server='''from IPython.display import display, HTML
from google.colab import output
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
GAME_HTML = r"""__GAME__"""
BESTIARY_VIEWER_HTML = r"""__VIEWER__"""
class DepthsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        text = BESTIARY_VIEWER_HTML if self.path.split('?')[0] in ('/bestiary','/gallery') else GAME_HTML
        payload = text.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
    def log_message(self, format, *args):
        return
old_server = globals().get('_depths_bestiary_server')
if old_server is not None:
    try:
        old_server.shutdown()
        old_server.server_close()
    except Exception:
        pass
_depths_bestiary_server = ThreadingHTTPServer(('0.0.0.0', 0), DepthsHandler)
_depths_bestiary_thread = Thread(target=_depths_bestiary_server.serve_forever, daemon=True)
_depths_bestiary_thread.start()
print('Depths 3D v6.0.0 Bestiary Pass loaded on port', _depths_bestiary_server.server_port)
output.serve_kernel_port_as_iframe(_depths_bestiary_server.server_port, width='100%', height=700)
'''
assert '"""' not in GAME_HTML and '"""' not in viewer
server=server.replace('__GAME__',GAME_HTML).replace('__VIEWER__',viewer)
compile(server,'<Colab launcher>','exec')
nb.cells.append(nbformat.v4.new_markdown_cell('## Run the complete game\n\nRun the following cell once. It includes all readable HTML and JavaScript in plain strings and starts a local notebook server. To restart it, run the same cell again; an older server is closed automatically.'))
nb.cells.append(nbformat.v4.new_code_cell(server))
nb.cells.append(nbformat.v4.new_markdown_cell('## Bestiary Viewer\n\nRun the **optional** next cell to open the turntable with the six reference crops, idle/walk/attack/hit/death controls, reference overlay and a local GLB import path. The game cell above must run first.'))
nb.cells.append(nbformat.v4.new_code_cell("print('Depths 3D Bestiary Viewer ready')\noutput.serve_kernel_port_as_iframe(_depths_bestiary_server.server_port, path='/bestiary', width='100%', height=900)"))
nb.cells.append(nbformat.v4.new_markdown_cell('## Test results and limitations\n\nThe JavaScript source, build and procedural model construction can be checked automatically. Actual GPU/WebGL rendering, animation likeness, 40-creature frame rate and average-laptop 60 FPS **have not been verified** here. The strict sub-150 ms uncached mesh generation target is not achieved by every creature. The named `07_enemies.js` was not attached, so this integrates with the actual latest available `src/game.js`, and exposes a `buildEnemyModel(...)` compatibility adapter; integration with an unseen enemy file remains unverified. See `TEST_REPORT.md` and `FEATURE_MATCH_REPORT.md`.'))
nb.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}}
nbformat.validate(nb)
nbformat.write(nb,str(ROOT/'depths_3d.ipynb'))
(ROOT/'colab_one_cell.py').write_text(server)
(ROOT/'BESTIARY_CROPS.json').write_text(json.dumps({k:str((ROOT/'refs'/f'{k}.png').relative_to(ROOT)) for k in SPEC},indent=2))
print('Built:',len(GAME),'game JS chars;',len(GAME_HTML),'game HTML chars;',len(viewer),'viewer HTML chars;', (ROOT/'depths_3d.ipynb').stat().st_size,'notebook bytes')
