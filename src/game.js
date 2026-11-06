(function(){
function start(){
const wrap=document.getElementById('dd3d-root');
const hud=wrap.querySelector('.hud'), mm=wrap.querySelector('.mm'), mctx=mm.getContext('2d');
const hpb=wrap.querySelector('.hpb'), flash=wrap.querySelector('.flash');
const ov=wrap.querySelector('.ov'), toastEl=wrap.querySelector('.toast');
const vg=document.createElement('div');
vg.style.cssText='position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 50%,rgba(0,0,0,.7) 100%)';
wrap.insertBefore(vg,hud);
const mk=function(css,html){ const d=document.createElement('div'); d.style.cssText=css; if(html) d.innerHTML=html; wrap.insertBefore(d,ov); return d; };
const ht=mk('position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;opacity:0;mix-blend-mode:screen;background:radial-gradient(ellipse at center,rgba(255,120,0,0) 30%,rgba(255,80,0,.6) 100%)');
const hotbar=mk('position:absolute;left:50%;transform:translateX(-50%);bottom:12px;display:flex;pointer-events:none');
const ammoBox=mk('position:absolute;right:14px;bottom:12px;text-align:right;pointer-events:none;text-shadow:0 1px 4px #000;background:#0007;padding:6px 12px;border-radius:10px;border:1px solid #ffffff22');
const hpLbl=mk('position:absolute;left:14px;bottom:36px;font-size:12px;font-weight:bold;pointer-events:none;text-shadow:0 1px 3px #000');
const hm=mk('position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;pointer-events:none;opacity:0','<div style="position:absolute;left:12px;top:-3px;width:2px;height:32px;background:#fff;transform:rotate(45deg)"></div><div style="position:absolute;left:12px;top:-3px;width:2px;height:32px;background:#fff;transform:rotate(-45deg)"></div>');
hud.style.background='linear-gradient(#000b,#0006)'; hud.style.padding='8px 12px'; hud.style.borderRadius='10px'; hud.style.border='1px solid #ffffff22';
mm.style.borderRadius='10px'; mm.style.boxShadow='0 0 14px #000a'; toastEl.style.bottom='70px';
const hpWrap=hpb.parentNode; hpWrap.style.width='260px'; hpWrap.style.height='16px'; hpWrap.style.left='14px'; hpWrap.style.bottom='14px'; hpWrap.style.borderRadius='8px';
const VERSION='4.0.0';
const RND=Math.random.bind(Math);
function reseed(a){ Math.random=function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function dailySeed(){ const d=new Date(); return d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate(); }
function save(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
function load(k,d){ try{ return Object.assign(Array.isArray(d)?[]:{},d,JSON.parse(localStorage.getItem(k)||'null')); }catch(e){ return d; } }
const SET=load('d3d_set',{sens:1,fov:72,vol:1});
const STATS=load('d3d_stats',{runs:0,kills:0,deaths:0,floors:0,ach:{}});
let BOARD=[]; try{ BOARD=JSON.parse(localStorage.getItem('d3d_board')||'[]'); }catch(e){}
const ACHS={first:'First Blood|Get your first kill',boss:'Demon Slayer|Defeat a boss',f5:'Deep Diver|Reach floor 5',combo:'Combo Master|Reach a x5 combo',rail:'Skewered|Hit 3 enemies with one railgun shot',barrel:'Boom!|Kill an enemy with an explosive barrel'};
function award(id){ if(STATS.ach[id]) return; STATS.ach[id]=1; save('d3d_stats',STATS); toast('🏆 Achievement: '+ACHS[id].split('|')[0],2800); }
const VW=800, VH=500, CELL=4, WALLH=3.2;

// ---------- renderer / scene ----------
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(2,window.devicePixelRatio||1));
renderer.setSize(VW,VH);
renderer.domElement.style.cssText='display:block;width:800px;height:500px';
wrap.insertBefore(renderer.domElement, wrap.firstChild);
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x050508);
scene.fog=new THREE.Fog(0x050508,2,28);
const camera=new THREE.PerspectiveCamera(SET.fov,VW/VH,0.1,100);
camera.rotation.order='YXZ';
scene.add(camera);
scene.add(new THREE.AmbientLight(0x4a4a70,0.7));
const torch=new THREE.PointLight(0xffb060,1.4,26,1.6);
scene.add(torch);

// gun viewmodels (one per weapon)
const gun=new THREE.Group(); gun.position.set(0.3,-0.26,-0.6); camera.add(gun);
const GM=function(c,e){return new THREE.MeshStandardMaterial({color:c,metalness:.6,roughness:.4,emissive:e||0});};
const gb=function(g,w,h,d,x,y,z,m){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m); o.position.set(x,y,z); g.add(o); return o;};
const gc=function(g,r,l,x,y,z,m){const o=new THREE.Mesh(new THREE.CylinderGeometry(r,r,l,10),m); o.rotation.x=Math.PI/2; o.position.set(x,y,z); g.add(o); return o;};
const gunModels=[0,1,2,3,4,5].map(function(i){const g=new THREE.Group(); g.visible=i===0; gun.add(g); return g;});
(function(){
  const M=function(c,m,r,e){return new THREE.MeshStandardMaterial({color:c,metalness:m,roughness:r,emissive:e||0});};
  const steel=M(0x8b909c,0.9,0.28), blue=M(0x1c1f26,0.85,0.32), poly=M(0x25272c,0.15,0.75), wood=M(0x5e3b1d,0,0.8);
  const cy=M(0x33e0ff,0.3,0.2,0x33e0ff), orange=M(0xff9a2a,0,0.5,0xff6a00), red=M(0xaa3322,0.3,0.5), dot=M(0xff2020,0,0.2,0xff2020), blk=M(0x000000,0,1);
  const U=function(i){ return gunModels[i].userData; };
  let g=gunModels[0]; // pistol
  U(0).slide=gb(g,.07,.075,.4,0,.02,-.12,blue); gb(g,.068,.05,.34,0,-.035,-.09,steel); gc(g,.022,.1,0,.02,-.36,steel);
  gb(g,.062,.2,.085,0,-.14,.1,poly).rotation.x=.18; [-1,1].forEach(function(k){ gb(g,.012,.17,.075,k*.037,-.14,.1,wood).rotation.x=.18; });
  gb(g,.05,.015,.1,0,-.075,-.02,steel); gb(g,.012,.05,.012,0,-.05,0,steel); gb(g,.012,.02,.02,0,.07,.07,steel); gb(g,.01,.02,.01,0,.07,-.31,steel);
  g=gunModels[1]; // pump shotgun
  gc(g,.026,.85,0,.03,-.45,steel); gc(g,.024,.6,0,-.02,-.35,steel); gb(g,.075,.1,.3,0,0,0,blue);
  U(1).pump=gb(g,.085,.07,.2,0,-.05,-.3,wood); gb(g,.06,.12,.45,0,-.05,.4,wood).rotation.x=-.12; gb(g,.012,.04,.12,0,-.07,.08,steel); gb(g,.01,.015,.01,0,.058,-.85,orange);
  g=gunModels[2]; // SMG
  gb(g,.08,.1,.5,0,0,-.05,poly); gc(g,.03,.34,0,.01,-.46,blue); for(let i=0;i<4;i++) gc(g,.036,.012,0,.01,-.36-i*.05,steel);
  gb(g,.055,.3,.075,0,-.2,-.02,blue).rotation.x=.12; gb(g,.06,.15,.075,0,-.1,.2,poly).rotation.x=.25;
  gb(g,.05,.02,.2,0,.065,-.08,steel); gb(g,.03,.035,.05,0,.095,-.05,poly); gb(g,.012,.012,.012,0,.1,-.075,dot);
  gb(g,.02,.02,.3,-.03,0,.38,steel); gb(g,.02,.02,.3,.03,0,.38,steel); gb(g,.07,.1,.02,0,0,.54,poly); U(2).bolt=gb(g,.02,.02,.04,.045,.03,-.05,steel);
  g=gunModels[3]; // railgun
  gb(g,.1,.12,.55,0,-.02,.08,blue); gb(g,.03,.05,.9,-.045,.02,-.5,steel); gb(g,.03,.05,.9,.045,.02,-.5,steel); gc(g,.018,.8,0,.02,-.5,cy);
  for(let i=0;i<5;i++){ const r=new THREE.Mesh(new THREE.TorusGeometry(.06,.014,8,16),cy); r.position.set(0,.02,-.2-i*.16); g.add(r); }
  for(let i=0;i<4;i++) gb(g,.12,.02,.04,0,.075,.05+i*.07,steel);
  gb(g,.07,.2,.09,0,-.15,.15,poly).rotation.x=.2; gb(g,.06,.1,.18,0,-.08,-.18,poly); U(3).mat=cy;
  g=gunModels[4]; // grenade launcher
  gc(g,.08,.5,0,0,-.3,blue); gc(g,.1,.2,0,-.02,0,steel); for(let i=0;i<6;i++){ const a2=i*1.047; gc(g,.018,.205,Math.cos(a2)*.07,-.02+Math.sin(a2)*.07,0,blk); }
  gb(g,.07,.2,.09,0,-.16,.15,wood).rotation.x=.25; gb(g,.06,.12,.4,0,-.04,.35,wood); gb(g,.02,.08,.03,0,.08,-.1,steel); gc(g,.09,.03,0,0,-.55,orange);
  g=gunModels[5]; // flamethrower
  gc(g,.035,.6,0,.02,-.4,steel); gc(g,.05,.1,0,.02,-.72,blue); gb(g,.03,.03,.03,0,.02,-.78,orange);
  gc(g,.075,.5,-.08,.13,.1,red); gc(g,.075,.5,.08,.13,.1,red); gb(g,.07,.16,.09,0,-.13,.12,poly).rotation.x=.2; gc(g,.012,.45,0,.04,-.15,blue); gc(g,.03,.04,0,.2,0,steel);
})();

// ---------- textures ----------
function mkTex(base,line,dots){
  const c=document.createElement('canvas'); c.width=c.height=128;
  const x=c.getContext('2d');
  x.fillStyle=base; x.fillRect(0,0,128,128);
  for(let i=0;i<1400;i++){
    x.fillStyle='rgba(0,0,0,'+(Math.random()*0.28)+')';
    x.fillRect(Math.random()*128,Math.random()*128,2,2);
  }
  if(line){
    x.strokeStyle=line; x.lineWidth=2;
    for(let r=0;r<4;r++){
      const y=r*32; x.beginPath(); x.moveTo(0,y); x.lineTo(128,y); x.stroke();
      const off=(r%2)*32;
      for(let b=off;b<128;b+=64){ x.beginPath(); x.moveTo(b,y); x.lineTo(b,y+32); x.stroke(); }
    }
  }
  const t=new THREE.CanvasTexture(c);
  t.wrapS=t.wrapT=THREE.RepeatWrapping;
  return t;
}
const wallTex=mkTex('#6b6275','#2a2530',true);
const floorTex=mkTex('#3a3640','#1c1a20',true);
const ceilTex=mkTex('#2a2832',null,false);
const wallMat=new THREE.MeshStandardMaterial({map:wallTex,roughness:0.95});
wallMat.bumpMap=wallTex; wallMat.bumpScale=0.8;
const floorMat=new THREE.MeshStandardMaterial({map:floorTex,roughness:1});
const ceilMat=new THREE.MeshStandardMaterial({map:ceilTex,roughness:1});
const glowTex=(function(){const c=document.createElement('canvas'); c.width=c.height=64; const x=c.getContext('2d');
  const g=x.createRadialGradient(32,32,2,32,32,32); g.addColorStop(0,'rgba(255,210,110,1)'); g.addColorStop(0.4,'rgba(255,120,30,.4)'); g.addColorStop(1,'rgba(255,80,0,0)');
  x.fillStyle=g; x.fillRect(0,0,64,64); return new THREE.CanvasTexture(c);})();
const glowMat=new THREE.SpriteMaterial({map:glowTex,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
const MZ=[0.62,0.85,0.7,1.0,0.62,0.78], KICK=[0.12,0.28,0.07,0.25,0.3,0.03];
const mflash=new THREE.Sprite(glowMat); mflash.scale.set(0.5,0.5,1); mflash.position.set(0,0.02,-0.8); mflash.visible=false; gun.add(mflash);
const PALS=[[0xffffff,0x050508],[0xb8ffd0,0x03100a],[0xffe0b0,0x120a04],[0xd8c0ff,0x0a0614],[0xff9a9a,0x140404]];
const wallGeo=new THREE.BoxGeometry(CELL,WALLH,CELL);

// ---------- audio ----------
let actx=null;
function beep(f,d,type,v,slide){
  if(!actx) return;
  try{
    const o=actx.createOscillator(), g=actx.createGain();
    o.type=type||'square'; o.frequency.value=f;
    if(slide) o.frequency.exponentialRampToValueAtTime(Math.max(30,f+slide),actx.currentTime+d);
    g.gain.value=(v||0.05)*SET.vol;
    g.gain.exponentialRampToValueAtTime(0.0001,actx.currentTime+d);
    o.connect(g); g.connect(actx.destination);
    o.start(); o.stop(actx.currentTime+d);
  }catch(e){}
}

// ---------- realistic audio ----------
let nbuf=null, stepT=0.3, stepL=false, hb=0;
function noise(dur,f0,f1,vol,type,pan){
  if(!actx) return;
  try{
    if(!nbuf){ nbuf=actx.createBuffer(1,actx.sampleRate,actx.sampleRate); const d=nbuf.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; }
    const s=actx.createBufferSource(), fl=actx.createBiquadFilter(), g=actx.createGain(), t=actx.currentTime;
    s.buffer=nbuf; s.loop=true; fl.type=type||'lowpass';
    fl.frequency.setValueAtTime(f0,t); fl.frequency.exponentialRampToValueAtTime(Math.max(20,f1),t+dur);
    g.gain.setValueAtTime(Math.max(0.0002,vol*SET.vol),t); g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    s.connect(fl); fl.connect(g);
    if(pan&&actx.createStereoPanner){ const p=actx.createStereoPanner(); p.pan.value=Math.max(-1,Math.min(1,pan)); g.connect(p); p.connect(actx.destination); } else g.connect(actx.destination);
    s.start(t); s.stop(t+dur);
  }catch(e){}
}
function gunSound(i){
  if(i===0){ noise(0.18,5200,300,0.55,'lowpass'); noise(0.05,9000,2500,0.3,'highpass'); beep(170,0.1,'sine',0.2,-100); }
  else if(i===1){ noise(0.55,3200,70,0.95,'lowpass'); beep(65,0.4,'sine',0.4,-30); noise(0.09,8000,1500,0.4,'highpass'); }
  else if(i===2){ noise(0.09,6500,500,0.4,'lowpass'); beep(240,0.05,'square',0.08,-130); }
  else if(i===3){ beep(1500,0.4,'sawtooth',0.12,-1300); beep(90,0.45,'sine',0.3,-40); noise(0.3,9000,800,0.3,'bandpass'); }
  else if(i===4){ beep(120,0.22,'square',0.22,-70); noise(0.14,1300,180,0.5,'lowpass'); }
  else { noise(0.15,2600,700,0.35,'bandpass'); }
}
function vol3(x,z,max){ return Math.max(0,1-Math.hypot(x-P.x,z-P.z)/max); }
function pan3(x,z){ const d=Math.hypot(x-P.x,z-P.z)||1; return ((x-P.x)*Math.cos(P.yaw)-(z-P.z)*Math.sin(P.yaw))/d; }
function footstep(sprint){ stepL=!stepL; noise(0.09,sprint?750:520,110,0.3,'lowpass',stepL?-0.25:0.25); beep(65+Math.random()*25,0.07,'sine',0.12,-30); }
function growl(e,big){
  const v=vol3(e.x,e.z,22); if(v<0.05) return;
  noise(big?0.9:0.5,big?260:430,big?65:110,0.55*v,'lowpass',pan3(e.x,e.z)); beep(big?52:88,big?0.8:0.45,'sawtooth',0.18*v,big?-14:-30);
}

// ---------- state ----------
let state='ready', paused=false;
let level=1, grid=null, GW=0, GH=0, explored=null;
let levelGroup=null, portal=null, portalOpen=false, exitCell=[1,1];
let enemies=[], pickups=[], orbs=[], fx=[], totalEnemies=0, killsThisLevel=0;
const P={x:0,z:0,yaw:0,hp:100,maxhp:100,ammo:60,score:0,cool:0,kills:0,r:0.4,wi:0,inv:0,combo:0,ct:0,shake:0,dmgm:1,rate:1,leech:0,scav:0,spd:1,entry:null};
let decals=[], checkpoints=[], lastCP=null, flames=[], barrels=[], gpHeld=false;
let muzzle=0, recoil=0, walkT=0, flashA=0, time=0, bobAmt=0, lastWalkT=0, heat=0, boomT=0, hitT=0, hbLast='', amLast='';
const keys={};
const WEAPONS=[
 {n:'Pistol',cd:.28,cost:1,dmg:2,pel:1,spr:.01,pierce:false,col:0x8a8fa0,len:1,d:'Accurate and cheap'},
 {n:'Shotgun',cd:.8,cost:3,dmg:1.3,pel:8,spr:.14,pierce:false,col:0xa0663a,len:.9,d:'8 pellets. Deadly up close'},
 {n:'SMG',cd:.07,cost:1,dmg:1,pel:1,spr:.05,pierce:false,col:0x4a90e2,len:1.1,d:'Rapid fire'},
 {n:'Railgun',cd:1.1,cost:6,dmg:9,pel:1,spr:0,pierce:true,col:0x33e0ff,len:1.4,d:'Pierces every enemy in line'},
 {n:'Grenade',cd:1,cost:5,dmg:6,pel:1,spr:.01,pierce:false,blast:4.5,col:0x7acb4a,len:1,d:'Big area blast + knockback'},
 {n:'Flamer',cd:.06,cost:1,dmg:.8,pel:3,spr:.18,pierce:true,rng:8,burn:4,col:0xff6a2a,len:1,d:'Sets enemies on fire'}];
WEAPONS.forEach(function(w,i){ w.ico=['🔫','💥','🔸','⚡','💣','🔥'][i]; });
const PERKS=[
 {n:'Hollow Points',i:'🎯',d:'+25% weapon damage',f:function(){P.dmgm*=1.25;}},
 {n:'Quick Hands',i:'⚡',d:'Fire 20% faster',f:function(){P.rate*=0.8;}},
 {n:'Iron Skin',i:'🛡️',d:'+25 max HP and full heal',f:function(){P.maxhp+=25;P.hp=P.maxhp;}},
 {n:'Vampiric',i:'🩸',d:'Heal 2 HP on every kill',f:function(){P.leech+=2;}},
 {n:'Scavenger',i:'🎒',d:'+40 ammo now, ammo pickups +50%',f:function(){P.ammo+=40;P.scav+=0.5;}},
 {n:'Light Boots',i:'👟',d:'+15% movement speed',f:function(){P.spd*=1.15;}}];
const DIFF={Easy:{d:.7,c:.8},Normal:{d:1,c:1},Hard:{d:1.4,c:1.3}};
let startW=0, difficulty='Normal', menuKind='main', menuTab='play', mode='Normal', perkChoices=[];
function setWeapon(i){ P.wi=i; gunModels.forEach(function(g,k){ g.visible=(k===i); }); toast(WEAPONS[i].n,700); }
function wbar(){ return WEAPONS.map(function(w,i){ return '<span style="padding:1px 6px;border-radius:4px;margin-right:3px;background:'+(i===P.wi?'#ffd23a;color:#000':'#0008')+'">'+(i+1)+' '+w.n+'</span>'; }).join(''); }
let best=0;
try{ best=parseInt(localStorage.getItem('depths3d_best'),10)||0; }catch(e){}
function saveBest(){
  if(P.score>best){ best=P.score; try{ localStorage.setItem('depths3d_best',String(best)); }catch(e){} }
}

function toast(t,ms){
  toastEl.textContent=t; toastEl.style.opacity=1;
  clearTimeout(toast.h); toast.h=setTimeout(()=>{toastEl.style.opacity=0;},ms||1800);
}
function solid(x,z){
  const gx=Math.floor(x/CELL), gz=Math.floor(z/CELL);
  if(gx<0||gz<0||gx>=GW||gz>=GH) return true;
  return grid[gz][gx]===1;
}
function blocked(x,z,r){return solid(x-r,z-r)||solid(x+r,z-r)||solid(x-r,z+r)||solid(x+r,z+r);}
function moveEnt(o,dx,dz,r){
  if(!blocked(o.x+dx,o.z,r)) o.x+=dx;
  if(!blocked(o.x,o.z+dz,r)) o.z+=dz;
}
function los(x0,z0,x1,z1){
  const d=Math.hypot(x1-x0,z1-z0), n=Math.ceil(d/0.8);
  for(let i=1;i<n;i++){
    const t=i/n;
    if(solid(x0+(x1-x0)*t,z0+(z1-z0)*t)) return false;
  }
  return true;
}

// ---------- maze generation ----------
function genMaze(n){
  const g=[];
  for(let y=0;y<n;y++) g.push(new Array(n).fill(1));
  const st=[[1,1]]; g[1][1]=0;
  while(st.length){
    const c=st[st.length-1], x=c[0], y=c[1];
    const dirs=[[2,0],[-2,0],[0,2],[0,-2]].sort(()=>Math.random()-0.5);
    let moved=false;
    for(const d of dirs){
      const nx=x+d[0], ny=y+d[1];
      if(nx>0&&ny>0&&nx<n-1&&ny<n-1&&g[ny][nx]===1){
        g[y+d[1]/2][x+d[0]/2]=0; g[ny][nx]=0; st.push([nx,ny]); moved=true; break;
      }
    }
    if(!moved) st.pop();
  }
  for(let y=1;y<n-1;y++) for(let x=1;x<n-1;x++){
    if(g[y][x]===1 && Math.random()<0.08){
      if((g[y][x-1]===0&&g[y][x+1]===0)||(g[y-1][x]===0&&g[y+1][x]===0)) g[y][x]=0;
    }
  }
  const rooms=2+Math.floor(n/8);
  for(let r=0;r<rooms;r++){
    const cx=2+Math.floor(Math.random()*(n-4)), cy=2+Math.floor(Math.random()*(n-4));
    for(let y=cy-1;y<=cy+1;y++) for(let x=cx-1;x<=cx+1;x++) g[y][x]=0;
  }
  // BFS from start
  const dist=[]; for(let y=0;y<n;y++) dist.push(new Array(n).fill(-1));
  const q=[[1,1]]; dist[1][1]=0; let far=[1,1];
  while(q.length){
    const c=q.shift();
    for(const d of [[1,0],[-1,0],[0,1],[0,-1]]){
      const nx=c[0]+d[0], ny=c[1]+d[1];
      if(nx>=0&&ny>=0&&nx<n&&ny<n&&g[ny][nx]===0&&dist[ny][nx]<0){
        dist[ny][nx]=dist[c[1]][c[0]]+1; q.push([nx,ny]);
        if(dist[ny][nx]>dist[far[1]][far[0]]) far=[nx,ny];
      }
    }
  }
  return {g:g,dist:dist,far:far};
}

// ---------- level building ----------
const shardGeo=new THREE.SphereGeometry(0.07,5,5);
function cellCenter(c){return [(c[0]+0.5)*CELL,(c[1]+0.5)*CELL];}

function buildLevel(){
  if(mode==='Daily') reseed(dailySeed()+level*7919);
  if(levelGroup) scene.remove(levelGroup);
  levelGroup=new THREE.Group(); scene.add(levelGroup);
  enemies=[]; pickups=[]; orbs=[]; fx=[]; killsThisLevel=0; portalOpen=false; flames=[]; checkpoints=[]; barrels=[]; decals=[];
  const n=Math.min(27,9+2*level);
  const m=genMaze(n); grid=m.g; GW=GH=n; exitCell=m.far;
  const pal=PALS[(level-1)%5]; wallMat.color.set(pal[0]); floorMat.color.set(pal[0]); scene.fog.color.set(pal[1]); scene.background.set(pal[1]);
  explored=new Uint8Array(n*n);

  const cells=[];
  for(let y=0;y<n;y++) for(let x=0;x<n;x++){
    if(grid[y][x]!==1) continue;
    let near=false;
    for(let dy=-1;dy<=1&&!near;dy++) for(let dx=-1;dx<=1;dx++){
      const xx=x+dx, yy=y+dy;
      if(xx>=0&&yy>=0&&xx<n&&yy<n&&grid[yy][xx]===0){near=true;break;}
    }
    if(near) cells.push([x,y]);
  }
  const inst=new THREE.InstancedMesh(wallGeo,wallMat,cells.length);
  const mat4=new THREE.Matrix4();
  cells.forEach((c,i)=>{ mat4.setPosition((c[0]+0.5)*CELL,WALLH/2,(c[1]+0.5)*CELL); inst.setMatrixAt(i,mat4); });
  inst.instanceMatrix.needsUpdate=true;
  inst.frustumCulled=false; // fixes walls vanishing when the origin block leaves the view
  levelGroup.add(inst);

  floorTex.repeat.set(n,n); ceilTex.repeat.set(n/2,n/2);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(n*CELL,n*CELL),floorMat);
  fl.rotation.x=-Math.PI/2; fl.position.set(n*CELL/2,0,n*CELL/2); levelGroup.add(fl);
  const ce=new THREE.Mesh(new THREE.PlaneGeometry(n*CELL,n*CELL),ceilMat);
  ce.rotation.x=Math.PI/2; ce.position.set(n*CELL/2,WALLH,n*CELL/2); levelGroup.add(ce);

  const sc=cellCenter([1,1]); P.x=sc[0]; P.z=sc[1]; P.yaw=0;
  // face an open direction
  if(grid[1][2]===0) P.yaw=-Math.PI/2; else P.yaw=Math.PI;

  // portal
  const pc=cellCenter(exitCell);
  portal=new THREE.Group();
  const ring=new THREE.Mesh(new THREE.TorusGeometry(1.1,0.13,12,36),
    new THREE.MeshStandardMaterial({color:0xff3344,emissive:0xff3344,emissiveIntensity:1}));
  ring.position.y=1.4;
  const disc=new THREE.Mesh(new THREE.CircleGeometry(1.05,28),
    new THREE.MeshBasicMaterial({color:0xff3344,transparent:true,opacity:0.25,side:THREE.DoubleSide}));
  disc.position.y=1.4;
  const plight=new THREE.PointLight(0xff3344,1.2,12,1.5); plight.position.y=1.6;
  portal.add(ring); portal.add(disc); portal.add(plight);
  portal.userData={ring:ring,disc:disc,light:plight};
  portal.position.set(pc[0],0,pc[1]);
  levelGroup.add(portal);

  // candidate cells
  const far=[], all=[];
  for(let y=0;y<n;y++) for(let x=0;x<n;x++){
    if(grid[y][x]===0 && !(x===exitCell[0]&&y===exitCell[1])){
      if(m.dist[y][x]>=9) far.push([x,y]);
      if(m.dist[y][x]>=3) all.push([x,y]);
    }
  }
  const pick=a=>a.splice(Math.floor(Math.random()*a.length),1)[0];

  const maxd=m.dist[exitCell[1]][exitCell[0]];
  [0.33,0.66].forEach(function(f){
    let bi=-1, bd=1e9;
    all.forEach(function(c,i){ const dd=Math.abs(m.dist[c[1]][c[0]]-maxd*f); if(dd<bd){ bd=dd; bi=i; } });
    if(bi>=0){ const c=all.splice(bi,1)[0], p=cellCenter(c); addCheckpoint(p[0],p[1]); }
  });
  lastCP={x:P.x,z:P.z};
  for(let y=1;y<n-1;y++) for(let x=1;x<n-1;x++){
    if(grid[y][x]!==0||Math.random()>0.06) continue;
    const ds=[[1,0],[-1,0],[0,1],[0,-1]];
    for(const d of ds){ if(grid[y+d[1]][x+d[0]]===1){ const p=cellCenter([x,y]); addTorch(p[0],p[1],d[0],d[1]); break; } }
  }
  const normal=Math.min(30,Math.round((4+level*2)*DIFF[difficulty].c));
  if(level%5===0&&far.length){ const bc=pick(far), bp=cellCenter(bc); addEnemy('boss',bp[0],bp[1]); }
  for(let i=0;i<normal&&far.length;i++){
    const c=pick(far), p=cellCenter(c), r=Math.random();
    let type='chaser';
    if(level>=3&&r<0.18) type='brute'; else if(r<0.5) type='shooter'; else if(level>=2&&r>0.88) type='teleporter'; else if(level>=2&&r>0.76) type='splitter';
    addEnemy(type,p[0],p[1]);
  }
  totalEnemies=enemies.length;
  if(level%5===0) setTimeout(()=>toast('⚠ BOSS FLOOR — something huge is hunting you',3200),400);
  const nh=3+Math.floor(level/2), na=4+level, ng=5+level;
  for(let i=0;i<nh&&all.length;i++){const p=cellCenter(pick(all)); addPickup('hp',p[0],p[1]);}
  for(let i=0;i<na&&all.length;i++){const p=cellCenter(pick(all)); addPickup('ammo',p[0],p[1]);}
  for(let i=0;i<ng&&all.length;i++){const p=cellCenter(pick(all)); addPickup('gem',p[0],p[1]);}
  for(let i=0;i<2+Math.floor(level/2)&&all.length;i++){const p=cellCenter(pick(all)); addBarrel(p[0],p[1]);}
  Math.random=RND;
}

const skinTex=mkTex('#8c7d72',null,false);
function buildMonster(type,mat){
  const g=new THREE.Group(), L=[], U={L:L}; g.userData=U;
  mat.map=skinTex; mat.bumpMap=skinTex; mat.bumpScale=1.5; mat.roughness=0.8;
  const S=function(r){return new THREE.SphereGeometry(r,14,12);};
  const M=function(c,e,r){return new THREE.MeshStandardMaterial({color:c,emissive:e||0,roughness:r===undefined?0.7:r});};
  const add=function(m,x,y,z,rx,rz,par){ m.position.set(x,y,z); if(rx) m.rotation.x=rx; if(rz) m.rotation.z=rz; (par||g).add(m); return m; };
  const limb=function(x,y,z,len,r,m,ph,amp,base,end,par,ax){
    const p=new THREE.Group(); p.position.set(x,y,z); (par||g).add(p);
    add(new THREE.Mesh(new THREE.CylinderGeometry(r,r*0.7,len,10),m),0,-len/2,0,0,0,p);
    if(end) add(end,0,-len,0,0,0,p);
    if(base&&ax!=='z') p.rotation.x=base;
    L.push({p:p,ph:ph,amp:amp,base:base||0,ax:ax||'x'}); return p;
  };
  const eyes=function(y,z,s,c){ [-1,1].forEach(function(k){ add(new THREE.Mesh(S(s),M(c,c,0.2)),k*s*2.2,y,z); }); };
  const claws=function(par,y,n){ for(let i=0;i<n;i++) add(new THREE.Mesh(new THREE.ConeGeometry(0.035,0.2,6),M(0xe8e0c8,0,0.4)),(i-(n-1)/2)*0.07,y-0.1,0.05,0.4,0,par); };
  const fangs=function(par,y,z,w,n,up){ for(let i=0;i<n;i++) add(new THREE.Mesh(new THREE.ConeGeometry(0.02,0.08,5),M(0xf2ecd8,0,0.4)),(i-(n-1)/2)*w/n,y,z,up?0:3.14,0,par); };
  const jawOf=function(y,z,w,col){ const j=new THREE.Group(); j.position.set(0,y,z); g.add(j);
    add(new THREE.Mesh(new THREE.BoxGeometry(w,0.05,w*1.1),M(col,0x200000)),0,-0.02,w*0.4,0,0,j); fangs(j,0.04,w*0.9,w,6,true); U.jaw=j; return j; };
  if(type==='chaser'){ // imp
    add(new THREE.Mesh(S(0.45),mat),0,0.05,0).scale.set(1,1.25,0.9);
    for(let i=0;i<3;i++) add(new THREE.Mesh(new THREE.ConeGeometry(0.06,0.22,6),M(0x2a0a0a)),0,0.45-i*0.22,-0.38,-0.6);
    add(new THREE.Mesh(S(0.28),mat),0,0.8,0.15); jawOf(0.66,0.2,0.22,0x701010); fangs(g,0.72,0.4,0.2,5,false); eyes(0.86,0.37,0.05,0xffee33);
    [-1,1].forEach(function(k){
      add(new THREE.Mesh(new THREE.ConeGeometry(0.06,0.32,6),M(0x2a0a0a)),k*0.16,1.08,0.1,0,-k*0.35);
      const arm=limb(k*0.5,0.4,0.1,0.75,0.09,M(0xa02820),k>0?0:Math.PI,0.7,-0.9,new THREE.Mesh(S(0.1),M(0x701818))); claws(arm,-0.75,3);
      limb(k*0.2,-0.4,0,0.65,0.13,M(0x701818),k>0?Math.PI:0,0.8,0,new THREE.Mesh(new THREE.BoxGeometry(0.16,0.06,0.28),M(0x2a0a0a)));
    });
    limb(0,-0.2,-0.4,0.9,0.07,M(0x701818),0,0.5,0,null,null,'z');
  } else if(type==='shooter'){ // eye-demon
    add(new THREE.Mesh(S(0.7),mat),0,0,0); add(new THREE.Mesh(S(0.4),M(0xf2f2e8,0x331111,0.3)),0,0.1,0.5);
    add(new THREE.Mesh(S(0.22),M(0xb01818,0x601010,0.2)),0,0.1,0.78); add(new THREE.Mesh(S(0.1),M(0x050005,0,0.1)),0,0.1,0.95);
    for(let i=0;i<6;i++){ const a=i*1.047; add(new THREE.Mesh(new THREE.BoxGeometry(0.012,0.28,0.012),M(0xaa2020)),Math.cos(a)*0.3,0.1+Math.sin(a)*0.3,0.62,0,a-1.57); }
    jawOf(-0.35,0.35,0.5,0x401040); fangs(g,-0.3,0.62,0.5,6,false);
    [-1,1].forEach(function(k){ add(new THREE.Mesh(new THREE.ConeGeometry(0.08,0.4,6),M(0x3a1060)),k*0.3,0.7,0.1,0,-k*0.4); });
    for(let i=0;i<6;i++){ const a=i*1.047; limb(Math.cos(a)*0.4,-0.5,Math.sin(a)*0.4,0.95,0.08,M(0x7a3098),a*2,0.35,0,null,null,'z'); }
  } else if(type==='brute'){ // ogre
    add(new THREE.Mesh(S(0.72),mat),0,0.05,0).scale.set(1.1,1.15,0.85); add(new THREE.Mesh(S(0.55),M(0x8a6a50)),0,-0.25,0.2).scale.set(1,0.8,0.9);
    add(new THREE.Mesh(S(0.3),mat),0,1.05,0.15); add(new THREE.Mesh(new THREE.BoxGeometry(0.5,0.08,0.12),M(0x2a1a10)),0,1.15,0.38);
    jawOf(0.9,0.28,0.3,0x4a2a18); [-1,1].forEach(function(k){ add(new THREE.Mesh(new THREE.ConeGeometry(0.04,0.18,6),M(0xfff2cc,0,0.4)),k*0.13,1.02,0.42); }); eyes(1.1,0.4,0.05,0xff3030);
    add(new THREE.Mesh(new THREE.BoxGeometry(0.9,0.5,0.5),M(0x4a3a2a)),0,-0.55,0.05);
    [-1,1].forEach(function(k){
      const arm=limb(k*0.9,0.5,0,0.95,0.17,M(0x8a5a3a),k>0?0:Math.PI,0.6,-0.3,new THREE.Mesh(S(0.22),M(0x7a4a2a)));
      if(k>0){ add(new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.1,1.0,8),M(0x4a3018)),0,-1.0,0.45,-1.3,0,arm); add(new THREE.Mesh(S(0.2),M(0x3a2410)),0,-1.0,0.95,0,0,arm); }
      limb(k*0.35,-0.55,0,0.8,0.19,M(0x6a4a30),k>0?Math.PI:0,0.5,0,new THREE.Mesh(new THREE.BoxGeometry(0.3,0.1,0.45),M(0x2a1a10)));
    });
  } else if(type==='teleporter'){
    add(new THREE.Mesh(new THREE.OctahedronGeometry(0.6),mat),0,0,0).scale.y=1.4;
    const sp=new THREE.Group(); g.add(sp); U.spin=sp;
    for(let i=0;i<5;i++){ const a=i*1.256; add(new THREE.Mesh(new THREE.OctahedronGeometry(0.16),M(0x99f0ff,0x33ddff,0.1)),Math.cos(a)*0.9,Math.sin(i*2)*0.3,Math.sin(a)*0.9,0,0,sp); }
    eyes(0.15,0.4,0.06,0xffffff);
  } else if(type==='splitter'||type==='mini'){
    const body=new THREE.Group(); g.add(body); U.pulse=body; add(new THREE.Mesh(S(0.6),mat),0,0,0,0,0,body);
    for(let i=0;i<5;i++) add(new THREE.Mesh(S(0.12+(i%3)*0.05),mat),Math.cos(i*1.3)*0.5,Math.sin(i*2.1)*0.4,Math.sin(i*1.3)*0.45,0,0,body);
    eyes(0.15,0.5,0.08,0xffffff); jawOf(-0.2,0.4,0.3,0x224422);
    if(type==='mini') g.scale.set(0.55,0.55,0.55);
  } else { // boss demon lord
    add(new THREE.Mesh(S(1.1),mat),0,0,0).scale.set(1.1,1.3,0.9); add(new THREE.Mesh(S(0.3),new THREE.MeshBasicMaterial({color:0xff7a22})),0,0.2,0.85);
    for(let i=0;i<3;i++) add(new THREE.Mesh(new THREE.BoxGeometry(0.9,0.05,0.1),M(0x2a0808)),0,0.05+i*0.2,0.92);
    add(new THREE.Mesh(S(0.55),mat),0,1.55,0.2); jawOf(1.35,0.45,0.5,0x500000); fangs(g,1.42,0.8,0.5,6,false); eyes(1.62,0.55,0.1,0xffff33);
    [-1,1].forEach(function(k){
      add(new THREE.Mesh(new THREE.ConeGeometry(0.12,1.0,7),M(0x1a0000)),k*0.4,2.15,0.1,0,-k*0.5);
      const arm=limb(k*1.25,0.7,0.1,1.2,0.2,M(0x7a1030),k>0?0:Math.PI,0.5,-0.4,new THREE.Mesh(S(0.28),M(0x501020))); claws(arm,-1.2,4);
      limb(k*0.5,-0.9,0,1.1,0.25,M(0x501020),k>0?Math.PI:0,0.4,0,new THREE.Mesh(new THREE.BoxGeometry(0.4,0.12,0.6),M(0x1a0808)));
      const w=new THREE.Group(); w.position.set(k*0.7,1.0,-0.5); g.add(w); w.rotation.z=k*0.5;
      add(new THREE.Mesh(new THREE.BoxGeometry(2.0,0.06,1.4),M(0x4a0a1a,0x150004)),k*1.1,0,0,0,0,w);
      add(new THREE.Mesh(new THREE.BoxGeometry(2.1,0.07,0.07),M(0x1a0808)),k*1.1,0,0.5,0,0,w); add(new THREE.Mesh(new THREE.BoxGeometry(2.1,0.07,0.07),M(0x1a0808)),k*1.1,0,-0.4,0,0,w);
      L.push({p:w,ph:0,amp:k*0.35,base:k*0.5,ax:'z'});
    });
  }
  return g;
}
function animMonster(e,dt){
  const U=e.mesh.userData; if(!U.L) return;
  const t=time*(1.5+e.speed*1.4)+e.ph, amt=e.alert?1:0.15;
  for(const l of U.L){ const v=Math.sin(t+l.ph)*l.amp*amt; if(l.ax==='z') l.p.rotation.z=l.base+v; else if(l.ax==='y') l.p.rotation.y=v; else l.p.rotation.x=l.base+v; }
  if(U.jaw) U.jaw.rotation.x=0.05+Math.max(0,Math.sin(time*2.5+e.ph))*(e.alert?0.55:0.12);
  if(U.spin) U.spin.rotation.y+=dt*2.5;
  if(U.pulse){ const s=1+Math.sin(time*5+e.ph)*0.08; U.pulse.scale.set(s,1/s,s); }
}
function addBarrel(x,z){
  const m=new THREE.Mesh(new THREE.CylinderGeometry(0.4,0.4,0.9,10),GM(0xaa2222,0x330000)); m.position.set(x,0.45,z); levelGroup.add(m);
  const band=new THREE.Mesh(new THREE.CylinderGeometry(0.41,0.41,0.15,10),GM(0xffcc22,0x332200)); band.position.y=0.1; m.add(band);
  barrels.push({x:x,z:z,mesh:m});
}
function explode(x,z,r,dmg,bar){
  if(bar){ levelGroup.remove(bar.mesh); barrels.splice(barrels.indexOf(bar),1); }
  burst(x,1,z,0xff9a2a,30,8); burst(x,1,z,0xffee88,12,6); burst(x,0.5,z,0x444444,14,5); boomFx(x,z,r); P.shake=Math.max(P.shake,0.6); noise(0.9,1400,50,0.9,'lowpass'); beep(55,0.6,'sine',0.4,-25);
  for(const e of enemies.slice()){
    const d=Math.hypot(e.x-x,e.z-z);
    if(d<r){ e.hp-=dmg*(1-d/r*0.5); e.hit=0.12; e.alert=true; if(d>0.01) moveEnt(e,(e.x-x)/d*(1-d/r)*1.8,(e.z-z)/d*(1-d/r)*1.8,e.r); if(e.hp<=0){ killEnemy(e); if(bar) award('barrel'); } }
  }
  if(Math.hypot(P.x-x,P.z-z)<r*0.7) hurt(8);
  for(const b of barrels.slice()){ if(Math.hypot(b.x-x,b.z-z)<r) explode(b.x,b.z,r,dmg,b); }
}
function dmgNum(x,y,z,txt,col){
  const v=new THREE.Vector3(x,y,z).project(camera); if(v.z>1) return;
  const el=document.createElement('div'); el.textContent=txt;
  el.style.cssText='position:absolute;pointer-events:none;font-weight:bold;font-size:14px;text-shadow:0 1px 2px #000;color:'+col+';left:'+((v.x+1)/2*VW)+'px;top:'+((1-v.y)/2*VH)+'px;transition:all .7s ease-out;opacity:1';
  wrap.appendChild(el);
  requestAnimationFrame(function(){ el.style.top=(parseFloat(el.style.top)-40)+'px'; el.style.opacity='0'; });
  setTimeout(function(){ el.remove(); },750);
}
function recordRun(){
  if(!P.entry){ P.entry={s:0,l:1,w:'',m:'',d:new Date().toLocaleDateString()}; BOARD.push(P.entry); }
  P.entry.s=Math.max(P.entry.s,P.score); P.entry.l=Math.max(P.entry.l,level); P.entry.w=WEAPONS[startW].n; P.entry.m=mode;
  BOARD.sort(function(a,b){return b.s-a.s;}); BOARD=BOARD.slice(0,10);
  save('d3d_board',BOARD); save('d3d_stats',STATS);
}
function addTorch(x,z,dx,dz){
  const px=x+dx*(CELL/2-0.25), pz=z+dz*(CELL/2-0.25);
  const s=new THREE.Sprite(glowMat); s.scale.set(2.2,2.2,1); s.position.set(px,2.1,pz); levelGroup.add(s); flames.push(s);
  const b=new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.05,0.5,6),GM(0x3a2a1a)); b.position.set(px,1.8,pz); levelGroup.add(b);
  const f=new THREE.Mesh(new THREE.SphereGeometry(0.1,6,6),new THREE.MeshBasicMaterial({color:0xffb030})); f.position.set(px,2.1,pz); levelGroup.add(f);
}
function addCheckpoint(x,z){
  const g=new THREE.Group(); g.position.set(x,0,z);
  const mat=new THREE.MeshStandardMaterial({color:0x667788,emissive:0x112233,emissiveIntensity:1});
  const base=new THREE.Mesh(new THREE.CylinderGeometry(0.7,0.8,0.25,12),mat); base.position.y=0.12;
  const pil=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.14,1.8,8),mat); pil.position.y=1.1;
  const orb=new THREE.Mesh(new THREE.SphereGeometry(0.25,12,12),mat); orb.position.y=2.1;
  g.add(base); g.add(pil); g.add(orb); levelGroup.add(g);
  checkpoints.push({x:x,z:z,on:false,mat:mat});
}
function respawn(){
  P.x=lastCP.x; P.z=lastCP.z; P.hp=Math.round(P.maxhp*0.6); P.ammo=Math.max(P.ammo,30);
  P.score=Math.floor(P.score*0.85); P.inv=3;
  orbs.forEach(function(o){ levelGroup.remove(o.mesh); }); orbs=[];
  state='playing'; paused=false; hideOverlay(); toast('Respawned at your last checkpoint',2200);
}

function addEnemy(type,x,z){
  const s=1+0.1*(level-1);
  let col,geo,hp,speed,r,dmg,y;
  if(type==='chaser'){col=0xff3a3a;geo=new THREE.OctahedronGeometry(0.6);hp=4;speed=3.4;r=0.5;dmg=12;y=1.2;}
  else if(type==='shooter'){col=0xb04cff;geo=new THREE.IcosahedronGeometry(0.6);hp=5;speed=2.4;r=0.5;dmg=0;y=1.4;}
  else if(type==='boss'){col=0xff2288;geo=new THREE.IcosahedronGeometry(1.4);hp=45;speed=2.1;r=1.0;dmg=26;y=1.9;}
  else if(type==='teleporter'){col=0x33ddff;hp=6;speed=2.6;r=0.5;dmg=10;y=1.4;}
  else if(type==='splitter'){col=0x66dd44;hp=10;speed=2.6;r=0.7;dmg=10;y=1.2;}
  else if(type==='mini'){col=0x99ee66;hp=3;speed=4.2;r=0.35;dmg=8;y=0.9;}
  else {col=0xff9a2a;geo=new THREE.DodecahedronGeometry(1.0);hp=14;speed=2.2;r=0.85;dmg=22;y=1.4;}
  const mat=new THREE.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:0.6,flatShading:true});
  const mesh=buildMonster(type,mat);
  mesh.position.set(x,y,z); levelGroup.add(mesh);
  const e={type:type,x:x,z:z,hp:Math.ceil(hp*s),maxhp:Math.ceil(hp*s),speed:speed,r:r,dmg:dmg*s,
    mesh:mesh,mat:mat,baseCol:col,baseY:y,alert:false,cool:1+Math.random(),ph:Math.random()*6,hit:0,hr:({boss:1.5,brute:1.0,mini:0.5,splitter:0.8})[type]||0.7};
  enemies.push(e);
}

const flameGeo=new THREE.SphereGeometry(0.12,8,8);
const glowHp=new THREE.SpriteMaterial({map:glowTex,color:0x66ff99,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
const glowAm=new THREE.SpriteMaterial({map:glowTex,color:0xffdd55,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
function PM(c,e,m){ return new THREE.MeshStandardMaterial({color:c,emissive:e||0,metalness:m||0,roughness:0.5}); }
function pkHealth(){ // first-aid bag + bandage roll
  const g=new THREE.Group(), add=function(m,x,y,z,rz){ m.position.set(x,y,z); if(rz) m.rotation.z=rz; g.add(m); return m; };
  const red=PM(0xe02020,0x660000);
  add(new THREE.Mesh(new THREE.BoxGeometry(0.5,0.38,0.2),PM(0xf4f4f4,0x222222)),-0.1,0,0);
  [0.106,-0.106].forEach(function(z){ add(new THREE.Mesh(new THREE.BoxGeometry(0.28,0.08,0.012),red),-0.1,0,z); add(new THREE.Mesh(new THREE.BoxGeometry(0.08,0.28,0.012),red),-0.1,0,z); });
  add(new THREE.Mesh(new THREE.TorusGeometry(0.09,0.02,6,12,Math.PI),PM(0x888888,0,0.5)),-0.1,0.19,0);
  add(new THREE.Mesh(new THREE.CylinderGeometry(0.11,0.11,0.2,14),PM(0xf0dcae)),0.33,-0.1,0.04,Math.PI/2);
  add(new THREE.Mesh(new THREE.CylinderGeometry(0.113,0.113,0.04,14),red),0.33,-0.1,0.04,Math.PI/2);
  add(new THREE.Mesh(new THREE.BoxGeometry(0.2,0.012,0.12),PM(0xf0dcae)),0.33,-0.205,0.1);
  const s=new THREE.Sprite(glowHp); s.scale.set(1.6,1.6,1); g.add(s); g.scale.set(1.25,1.25,1.25);
  return g;
}
function pkAmmo(){ // three brass bullets
  const g=new THREE.Group(), brass=PM(0xd8a62a,0x332200,0.8), rim=PM(0xa87a18,0,0.8), tip=PM(0xb5651d,0x1a0a00,0.7);
  [[-0.14,0],[0.14,0],[0,0.13]].forEach(function(p){
    const c=new THREE.Mesh(new THREE.CylinderGeometry(0.07,0.07,0.3,12),brass); c.position.set(p[0],0.15-0.25,p[1]); g.add(c);
    const r=new THREE.Mesh(new THREE.CylinderGeometry(0.082,0.082,0.035,12),rim); r.position.set(p[0],0.02-0.25,p[1]); g.add(r);
    const t=new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.07,0.17,12),tip); t.position.set(p[0],0.385-0.25,p[1]); g.add(t);
  });
  const s=new THREE.Sprite(glowAm); s.scale.set(1.5,1.5,1); g.add(s); g.scale.set(1.3,1.3,1.3);
  return g;
}
const glowGem=new THREE.SpriteMaterial({map:glowTex,color:0x55ddff,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
function pkGem(){ // faceted XP crystal with orbiting ring
  const g=new THREE.Group();
  const o=new THREE.Mesh(new THREE.OctahedronGeometry(0.26),new THREE.MeshStandardMaterial({color:0x7af2ff,emissive:0x1fb8e0,emissiveIntensity:0.9,metalness:0.2,roughness:0.08,flatShading:true,transparent:true,opacity:0.92})); o.scale.y=1.5; g.add(o);
  const core=new THREE.Mesh(new THREE.OctahedronGeometry(0.12),new THREE.MeshBasicMaterial({color:0xffffff})); core.scale.y=1.5; g.add(core);
  const ring=new THREE.Mesh(new THREE.TorusGeometry(0.4,0.015,6,28),new THREE.MeshBasicMaterial({color:0x9ff6ff})); ring.rotation.x=1.2; g.add(ring);
  for(let i=0;i<4;i++){ const sp=new THREE.Mesh(new THREE.OctahedronGeometry(0.04),new THREE.MeshBasicMaterial({color:0xffffff})); sp.position.set(Math.cos(i*1.57)*0.4,Math.sin(i*1.57)*0.4,0); ring.add(sp); }
  const s=new THREE.Sprite(glowGem); s.scale.set(1.4,1.4,1); g.add(s); return g;
}
const bloodMat=new THREE.MeshBasicMaterial({color:0x5a0a0a,transparent:true,opacity:0.7,depthWrite:false});
function blood(x,y,z,n){
  burst(x,y,z,0x8a0f0f,n,5);
  if(decals.length>60) levelGroup.remove(decals.shift());
  const d=new THREE.Mesh(new THREE.CircleGeometry(0.25+Math.random()*0.35,10),bloodMat); d.rotation.x=-Math.PI/2;
  d.position.set(x+(Math.random()-0.5)*0.8,0.02,z+(Math.random()-0.5)*0.8); levelGroup.add(d); decals.push(d);
}
const shellGeo=new THREE.CylinderGeometry(0.018,0.018,0.06,6), shellBrass=new THREE.MeshStandardMaterial({color:0xd8a62a,metalness:0.9,roughness:0.3}), shellRed=new THREE.MeshStandardMaterial({color:0xcc2222,roughness:0.6});
const boomGeo=new THREE.SphereGeometry(1,16,12), ringGeo=new THREE.RingGeometry(0.88,1,40), scorchMat=new THREE.MeshBasicMaterial({color:0x120805,transparent:true,opacity:0.8,depthWrite:false});
function boomFx(x,z,r){
  const put=function(m,k,dur,rr){ levelGroup.add(m); fx.push({pr:true,kind:k,mesh:m,t:0,dur:dur,r:rr,x0:x,y0:m.position.y,z0:z,x1:x,y1:m.position.y,z1:z}); };
  const ball=function(c,o){ return new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:o,blending:THREE.AdditiveBlending,depthWrite:false}); };
  const f=new THREE.Mesh(boomGeo,ball(0xff8a2a,0.85)); f.position.set(x,0.9,z); put(f,'boom',0.45,r);
  const c=new THREE.Mesh(boomGeo,ball(0xfff0b0,0.95)); c.position.set(x,0.9,z); put(c,'boom',0.25,r*0.55);
  const rg=new THREE.Mesh(ringGeo,new THREE.MeshBasicMaterial({color:0xffc060,transparent:true,opacity:0.9,side:THREE.DoubleSide,depthWrite:false})); rg.rotation.x=-Math.PI/2; rg.position.set(x,0.06,z); put(rg,'ring',0.5,r);
  if(decals.length>60) levelGroup.remove(decals.shift());
  const sc=new THREE.Mesh(new THREE.CircleGeometry(r*0.55,16),scorchMat); sc.rotation.x=-Math.PI/2; sc.position.set(x,0.025,z); levelGroup.add(sc); decals.push(sc);
  boomT=1; P.shake=Math.max(P.shake,0.7);
}
function eject(wi){
  if(wi>2) return;
  const rx=Math.cos(P.yaw), rz=-Math.sin(P.yaw), fx2=-Math.sin(P.yaw), fz2=-Math.cos(P.yaw);
  const m=new THREE.Mesh(shellGeo,wi===1?shellRed:shellBrass); if(wi===1) m.scale.set(1.5,1.6,1.5);
  m.position.set(P.x+rx*0.3+fx2*0.3,1.25,P.z+rz*0.3+fz2*0.3); m.rotation.set(Math.random()*3,Math.random()*3,Math.random()*3); levelGroup.add(m);
  fx.push({mesh:m,vx:rx*(2+Math.random()*1.5),vy:2+Math.random()*1.5,vz:rz*(2+Math.random()*1.5),life:1.3,line:false});
}
function addPickup(type,x,z){
  const mesh=type==='hp'?pkHealth():(type==='ammo'?pkAmmo():pkGem());
  mesh.position.set(x,0.9,z); levelGroup.add(mesh);
  pickups.push({type:type,x:x,z:z,mesh:mesh,ph:Math.random()*6});
}

// weapon projectiles: [kind, colour, length, speed]
const PJ=[['bolt',0xffe08a,0.5,100],['bolt',0xffa040,0.25,70],['bolt',0x8ac8ff,0.45,110],['beam',0x33e0ff,0,0],['gren',0x7acb4a,0,26],['flame',0xff7a22,0,14]];
function spawnProj(wi,x0,y0,z0,x1,y1,z1,done){
  const p=PJ[wi], kind=p[0], dist=Math.hypot(x1-x0,y1-y0,z1-z0); let m, dur=0.3;
  if(kind==='bolt'){ m=new THREE.Mesh(new THREE.BoxGeometry(0.035,0.035,p[2]),new THREE.MeshBasicMaterial({color:p[1]})); dur=dist/p[3]; m.position.set(x0,y0,z0); m.lookAt(x1,y1,z1); }
  else if(kind==='beam'){
    m=new THREE.Mesh(new THREE.BoxGeometry(0.12,0.12,dist),new THREE.MeshBasicMaterial({color:p[1],transparent:true,opacity:0.8}));
    m.add(new THREE.Mesh(new THREE.BoxGeometry(0.04,0.04,dist),new THREE.MeshBasicMaterial({color:0xffffff})));
    m.position.set((x0+x1)/2,(y0+y1)/2,(z0+z1)/2); m.lookAt(x1,y1,z1);
  }
  else if(kind==='gren'){ m=new THREE.Mesh(new THREE.SphereGeometry(0.13,10,10),PM(0x7acb4a,0x2a5010)); dur=Math.max(0.12,dist/p[3]); m.position.set(x0,y0,z0); }
  else { m=new THREE.Mesh(flameGeo,new THREE.MeshBasicMaterial({color:Math.random()<0.5?0xff7a22:0xffd23a,transparent:true,opacity:0.8})); dur=Math.max(0.08,dist/p[3]); m.position.set(x0,y0,z0); }
  levelGroup.add(m);
  fx.push({pr:true,kind:kind,mesh:m,t:0,dur:dur,x0:x0,y0:y0,z0:z0,x1:x1,y1:y1,z1:z1,done:done});
}

// ---------- fx ----------
function burst(x,y,z,col,n,spd){
  for(let i=0;i<n;i++){
    const m=new THREE.Mesh(shardGeo,new THREE.MeshBasicMaterial({color:col}));
    m.position.set(x,y,z); levelGroup.add(m);
    fx.push({mesh:m,vx:(Math.random()-0.5)*spd,vy:Math.random()*spd*0.8,vz:(Math.random()-0.5)*spd,life:0.5+Math.random()*0.3,line:false});
  }
}
function tracer(x0,y0,z0,x1,y1,z1){
  const g=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x0,y0,z0),new THREE.Vector3(x1,y1,z1)]);
  const l=new THREE.Line(g,new THREE.LineBasicMaterial({color:0xffe08a}));
  levelGroup.add(l); fx.push({mesh:l,life:0.07,line:true,vx:0,vy:0,vz:0});
}

// ---------- combat ----------
function hurt(a){
  if(state!=='playing'||P.inv>0) return;
  a*=DIFF[difficulty].d;
  P.hp-=a; flashA=Math.min(0.55,flashA+0.12+a*0.01); P.shake=Math.max(P.shake,Math.min(0.6,0.15+a*0.03));
  if(P.hp<=0){
    P.hp=0; state='dead'; saveBest(); STATS.deaths++; recordRun(); beep(160,0.6,'sawtooth',0.08,-100);
    showMenu('dead');
  }
}
function killEnemy(e){
  levelGroup.remove(e.mesh);
  enemies.splice(enemies.indexOf(e),1);
  P.kills++; if(e.type!=='mini') killsThisLevel++; STATS.kills++; award('first');
  if(e.type==='boss') award('boss');
  if(P.leech) P.hp=Math.min(P.maxhp,P.hp+P.leech);
  if(e.type==='splitter'){ for(let i=0;i<2;i++){ addEnemy('mini',e.x,e.z); enemies[enemies.length-1].alert=true; } }
  P.combo=P.ct>0?Math.min(10,P.combo+1):1; P.ct=3;
  P.score+=Math.round((e.type==='boss'?1000:(e.type==='brute'?250:(e.type==='shooter'?120:100)))*(1+(P.combo-1)*0.1));
  if(P.combo>=3) toast('Combo x'+P.combo+'!',900); if(P.combo>=5) award('combo');
  burst(e.x,e.baseY,e.z,e.baseCol,e.type==='boss'?40:16,6); blood(e.x,e.baseY,e.z,e.type==='boss'?30:14);
  noise(0.35,700,60,0.4,'lowpass',pan3(e.x,e.z)); beep(140,0.3,'sawtooth',0.1,-90);
  if(Math.random()<0.28) addPickup(Math.random()<0.5?'hp':'ammo',e.x,e.z);
  if(!portalOpen && killsThisLevel>=Math.ceil(totalEnemies*0.5)){
    portalOpen=true;
    portal.userData.ring.material.color.set(0x33e0ff);
    portal.userData.ring.material.emissive.set(0x33e0ff);
    portal.userData.disc.material.color.set(0x33e0ff);
    portal.userData.disc.material.opacity=0.45;
    portal.userData.light.color.set(0x33e0ff);
    toast('The portal is open! Find it on the minimap.',2600);
    beep(520,0.3,'sine',0.07,300);
  }
}
function shoot(){
  if(state!=='playing'||P.cool>0) return;
  const w=WEAPONS[P.wi];
  if(P.ammo<w.cost){ beep(90,0.08,'square',0.04); P.cool=0.25; toast('Not enough ammo for the '+w.n,900); return; }
  P.ammo-=w.cost; P.cool=w.cd*P.rate; muzzle=0.06; P.shake=Math.max(P.shake,(w.pel>1||w.blast)?0.25:0.05); recoil=KICK[P.wi];
  gunSound(P.wi); eject(P.wi); if(w.burn) heat=Math.min(1,heat+0.2);
  const rx=Math.cos(P.yaw), rz=-Math.sin(P.yaw);
  for(let p=0;p<w.pel;p++){
    const a=P.yaw+(Math.random()-0.5)*2*w.spr, dx=-Math.sin(a), dz=-Math.cos(a), hits=[];
    let end=w.rng||40, hitB=null;
    for(let t=0.4;t<(w.rng||40);t+=0.25){
      const x=P.x+dx*t, z=P.z+dz*t;
      if(solid(x,z)){ end=t; break; }
      let stop=false;
      for(const b of barrels){ if(Math.hypot(b.x-x,b.z-z)<0.6){ hitB=b; end=t; stop=true; break; } }
      if(stop) break;
      for(const e of enemies){
        if(hits.indexOf(e)<0&&Math.hypot(e.x-x,e.z-z)<e.hr){ hits.push(e); if(!w.pierce){ end=t; stop=true; break; } }
      }
      if(stop) break;
    }
    const ex=P.x+dx*end, ez=P.z+dz*end;
    spawnProj(P.wi,P.x+rx*0.3+dx*0.6,1.3,P.z+rz*0.3+dz*0.6,ex,1.45,ez,w.blast?function(){ explode(ex,ez,w.blast,w.dmg*P.dmgm,null); }:null);
    if(!hits.length) burst(P.x+dx*end,1.4,P.z+dz*end,0xffcc66,3,2);
    if(hitB) explode(hitB.x,hitB.z,4,8,hitB);
    if(w.pierce&&w.dmg>5&&hits.length>=3) award('rail');
    for(const e of (w.blast?[]:hits)){
      const cr=Math.random()<0.1, dv=w.dmg*P.dmgm*(cr?2:1); e.hp-=dv; e.hit=0.1; e.alert=true; hitT=1; if(w.burn) e.burn=w.burn;
      if(w.pel<2||Math.random()<0.3) dmgNum(e.x,e.baseY+0.9,e.z,(cr?'💥':'')+Math.max(1,Math.round(dv)),cr?'#ffd23a':'#fff');
      blood(e.x,e.baseY,e.z,5);
      if(e.hp<=0) killEnemy(e); else noise(0.06,1500,300,0.25,'lowpass',pan3(e.x,e.z));
    }
  }
}

// ---------- update ----------
function update(dt){
  time+=dt; P.inv=Math.max(0,P.inv-dt); P.ct-=dt; if(P.ct<=0) P.combo=0;
  if(P.hp<30){ hb-=dt; if(hb<=0){ hb=0.9; beep(58,0.14,'sine',0.35,-18); setTimeout(function(){ beep(52,0.12,'sine',0.25,-15); },170); } }
  for(const c of checkpoints){
    if(!c.on&&Math.hypot(c.x-P.x,c.z-P.z)<1.5){
      c.on=true; c.mat.color.set(0x33ff99); c.mat.emissive.set(0x11cc66); lastCP={x:c.x,z:c.z};
      P.hp=Math.min(P.maxhp,P.hp+40); P.ammo+=10; toast('✔ Checkpoint saved  (+40 HP, +10 ammo)',2400); beep(660,0.25,'sine',0.07,400);
    }
  }
  P.cool=Math.max(0,P.cool-dt);
  muzzle=Math.max(0,muzzle-dt); recoil=Math.max(0,recoil-dt*0.9);
  // input
  const k=keys;
  let f=((k.KeyW||k.ArrowUp)?1:0)-((k.KeyS||k.ArrowDown)?1:0);
  let s=(k.KeyD?1:0)-(k.KeyA?1:0), gpFire=false;
  const gp=navigator.getGamepads?navigator.getGamepads()[0]:null;
  if(gp){
    const dz=function(v){ return Math.abs(v)<0.15?0:v; };
    f-=dz(gp.axes[1]); s+=dz(gp.axes[0]); P.yaw-=dz(gp.axes[2])*2.8*dt*SET.sens;
    gpFire=!!((gp.buttons[7]&&gp.buttons[7].pressed)||(gp.buttons[0]&&gp.buttons[0].pressed));
    const sw=!!(gp.buttons[5]&&gp.buttons[5].pressed);
    if(sw&&!gpHeld) setWeapon((P.wi+1)%WEAPONS.length); gpHeld=sw;
  }
  const turn=((k.ArrowLeft||k.KeyQ)?1:0)-((k.ArrowRight||k.KeyE)?1:0);
  P.yaw+=turn*2.4*dt;
  const sp=(k.ShiftLeft||k.ShiftRight?9:6)*dt*P.spd;
  let mx=-Math.sin(P.yaw)*f+Math.cos(P.yaw)*s, mz=-Math.cos(P.yaw)*f-Math.sin(P.yaw)*s;
  const ml=Math.hypot(mx,mz);
  if(ml>0){
    mx=mx/ml*sp; mz=mz/ml*sp; moveEnt(P,mx,mz,P.r); walkT+=dt;
    const spr=!!(k.ShiftLeft||k.ShiftRight); stepT+=dt*(spr?1.5:1); if(stepT>0.4){ stepT=0; footstep(spr); }
  } else stepT=0.3;
  if(k.Space||k.KeyF||k.mouse||gpFire) shoot();

  // enemies
  const dead=[];
  for(const e of enemies){
    const dx=P.x-e.x, dz=P.z-e.z, d=Math.hypot(dx,dz)||0.001;
    const visible=d<22&&los(e.x,e.z,P.x,P.z);
    if(!e.alert&&visible&&d<20){ e.alert=true; growl(e,e.type==='brute'||e.type==='boss'); }
    e.mesh.position.set(e.x,e.baseY+Math.sin(time*3+e.ph)*0.15,e.z);
    e.mesh.rotation.y=Math.atan2(dx,dz); animMonster(e,dt);
    if(e.burn>0){
      e.burn-=dt; e.hp-=1.6*dt*P.dmgm; if(e.hp<=0) dead.push(e);
      if(!e.fireS){ e.fireS=new THREE.Sprite(glowMat); e.fireS.position.y=0.3; e.mesh.add(e.fireS); }
      e.fireS.visible=true; const fk=2+Math.sin(time*18+e.ph)*0.3; e.fireS.scale.set(fk,fk*1.3,1);
      e.bp=(e.bp||0)-dt; if(e.bp<=0){ e.bp=0.1; burst(e.x+(Math.random()-0.5)*0.6,e.baseY+0.4,e.z+(Math.random()-0.5)*0.6,0xffa030,2,1.6); }
      e.sp=(e.sp||0)-dt; if(e.sp<=0){ e.sp=0.5; for(const o of enemies){ if(o!==e&&!(o.burn>0)&&Math.hypot(o.x-e.x,o.z-e.z)<1.5) o.burn=2.5; } }
    } else if(e.fireS) e.fireS.visible=false;
    if(e.hit>0){ e.hit-=dt; e.mat.emissive.set(0xffffff); e.mat.emissiveIntensity=1.2; }
    else { e.mat.emissive.set(e.baseCol); e.mat.emissiveIntensity=e.alert?0.9:0.35; }
    if(e.burn>0){ e.mat.emissive.set(0xff5a10); e.mat.emissiveIntensity=0.8+Math.sin(time*20)*0.3; }
    if(!e.alert) continue;
    e.gr=(e.gr===undefined?Math.random()*4:e.gr)-dt;
    if(e.gr<=0){ e.gr=4+Math.random()*5; growl(e,e.type==='brute'||e.type==='boss'); }
    if(e.type==='brute'||e.type==='boss'){
      e.sd=(e.sd||0)+dt;
      if(e.sd>0.7){ e.sd=0; const v=vol3(e.x,e.z,18); if(v>0){ noise(0.22,220,50,0.6*v,'lowpass',pan3(e.x,e.z)); if(v>0.5) P.shake=Math.max(P.shake,0.12*v); } }
    }
    if(e.type==='teleporter'){
      e.tp=(e.tp||2)-dt;
      if(e.tp<=0){ e.tp=3+Math.random()*2; const a=Math.random()*6.28, rr=5+Math.random()*4, nx=P.x+Math.cos(a)*rr, nz=P.z+Math.sin(a)*rr;
        if(!blocked(nx,nz,0.6)){ burst(e.x,1.4,e.z,0x33ddff,10,4); e.x=nx; e.z=nz; burst(nx,1.4,nz,0x33ddff,10,4); } }
    }
    let want=1;
    const ranged=(e.type==='shooter'||e.type==='boss');
    if(ranged){ if(d<7) want=-0.8; else if(d<11) want=0; }
    if(want!==0&&!(want>0&&d<1.0)){
      const st=e.speed*want*dt;
      moveEnt(e,dx/d*st,dz/d*st,e.r);
    }
    for(const o of enemies){
      if(o===e) continue;
      const ox=e.x-o.x, oz=e.z-o.z, od=Math.hypot(ox,oz);
      if(od<1.1&&od>0.001) moveEnt(e,ox/od*dt*2,oz/od*dt*2,e.r);
    }
    if(ranged){
      e.cool-=dt;
      if(e.cool<=0&&visible){
        e.cool=e.type==='boss'?1.6:1.5+Math.random()*0.8;
        const spread=e.type==='boss'?[-0.3,0,0.3]:[0];
        for(const a of spread){
          const ca=Math.cos(a), sa=Math.sin(a);
          const ux=dx/d, uz=dz/d;
          const m=new THREE.Mesh(new THREE.SphereGeometry(0.22,10,10),
            new THREE.MeshBasicMaterial({color:e.type==='boss'?0xff4aa0:0xd070ff}));
          m.position.set(e.x,1.4,e.z); levelGroup.add(m);
          orbs.push({mesh:m,x:e.x,z:e.z,vx:(ux*ca-uz*sa)*9,vz:(ux*sa+uz*ca)*9,life:4});
        }
        beep(420,0.12,'sine',0.04,-200);
      }
    }
    if(e.dmg>0&&d<e.r+0.9) hurt(e.dmg*dt);
  }
  dead.forEach(function(e){ if(enemies.indexOf(e)>=0) killEnemy(e); });
  // orbs
  for(let i=orbs.length-1;i>=0;i--){
    const o=orbs[i];
    o.x+=o.vx*dt; o.z+=o.vz*dt; o.life-=dt;
    o.mesh.position.set(o.x,1.4,o.z);
    let dead=o.life<=0||solid(o.x,o.z);
    if(!dead&&Math.hypot(o.x-P.x,o.z-P.z)<0.7){ hurt(9+level); dead=true; beep(140,0.15,'sawtooth',0.06); }
    if(dead){ burst(o.x,1.4,o.z,0xd070ff,5,3); levelGroup.remove(o.mesh); orbs.splice(i,1); }
  }
  // pickups
  for(let i=pickups.length-1;i>=0;i--){
    const p=pickups[i];
    p.mesh.rotation.y+=dt*2; p.mesh.position.y=0.9+Math.sin(time*2.5+p.ph)*0.12;
    if(p.type==='gem') p.mesh.children[2].rotation.z+=dt*3;
    if(Math.hypot(p.x-P.x,p.z-P.z)<1.1){
      if(p.type==='hp'){ if(P.hp>=P.maxhp) continue; P.hp=Math.min(P.maxhp,P.hp+30); toast('+30 HP',900); }
      else if(p.type==='ammo'){ const am=Math.round(25*(1+P.scav)); P.ammo+=am; toast('+'+am+' ammo',900); }
      else { P.score+=50; toast('+50',700); }
      beep(900,0.1,'sine',0.05,300);
      levelGroup.remove(p.mesh); pickups.splice(i,1);
    }
  }
  // fx
  for(let i=fx.length-1;i>=0;i--){
    const f2=fx[i];
    if(f2.pr){
      f2.t+=dt; const k=Math.min(1,f2.t/f2.dur), mm=f2.mesh;
      if(f2.kind==='beam'){ mm.material.opacity=0.8*(1-k); }
      else if(f2.kind==='boom'){ const s=f2.r*Math.sqrt(k)+0.05; mm.scale.set(s,s*0.8,s); mm.material.opacity=0.9*(1-k); }
      else if(f2.kind==='ring'){ const s=f2.r*1.15*k+0.1; mm.scale.set(s,s,s); mm.material.opacity=0.9*(1-k); }
      else{
        mm.position.set(f2.x0+(f2.x1-f2.x0)*k,f2.y0+(f2.y1-f2.y0)*k+(f2.kind==='gren'?Math.sin(k*3.1416)*1.2:0),f2.z0+(f2.z1-f2.z0)*k);
        if(f2.kind==='flame'){ const sc=1+k*2.5; mm.scale.set(sc,sc,sc); mm.material.opacity=0.8*(1-k); }
      }
      if(k>=1){ levelGroup.remove(mm); fx.splice(i,1); if(f2.done) f2.done(); }
      continue;
    }
    f2.life-=dt;
    if(!f2.line){ f2.mesh.position.x+=f2.vx*dt; f2.mesh.position.y+=f2.vy*dt; f2.mesh.position.z+=f2.vz*dt; f2.vy-=9*dt;
      if(f2.mesh.position.y<0.05){f2.mesh.position.y=0.05;f2.vy=0;f2.vx*=0.8;f2.vz*=0.8;} }
    if(f2.life<=0){ levelGroup.remove(f2.mesh); fx.splice(i,1); }
  }
  // portal
  portal.userData.ring.rotation.z+=dt*(portalOpen?2.5:0.6);
  portal.userData.disc.rotation.z-=dt;
  const pp=cellCenter(exitCell);
  if(portalOpen&&Math.hypot(pp[0]-P.x,pp[1]-P.z)<1.5){
    level++; P.score+=200+level*20; saveBest(); P.hp=Math.min(P.maxhp,P.hp+25); P.ammo+=15;
    buildLevel(); toast('Level '+level+' — the dungeon grows...',2400); beep(300,0.4,'sine',0.07,500);
    STATS.floors++; if(level>=5) award('f5'); recordRun();
    perkChoices=PERKS.slice().sort(function(){ return Math.random()-0.5; }).slice(0,3); state='perk'; showMenu('perk');
  } else if(!portalOpen&&Math.hypot(pp[0]-P.x,pp[1]-P.z)<1.8){
    toast('Sealed. Kill '+(Math.ceil(totalEnemies*0.5)-killsThisLevel)+' more enemies.',1200);
  }
  // explore
  const pcx=Math.floor(P.x/CELL), pcz=Math.floor(P.z/CELL);
  for(let y=pcz-3;y<=pcz+3;y++) for(let x=pcx-3;x<=pcx+3;x++)
    if(x>=0&&y>=0&&x<GW&&y<GH&&(x-pcx)*(x-pcx)+(y-pcz)*(y-pcz)<=10) explored[y*GW+x]=1;
}

function render(){
  const sh=P.shake; camera.position.set(P.x+(Math.random()-0.5)*sh*0.4,1.6+Math.sin(walkT*10)*0.045+(Math.random()-0.5)*sh*0.4,P.z+(Math.random()-0.5)*sh*0.4); P.shake*=0.9;
  camera.rotation.y=P.yaw;
  torch.position.set(P.x,2.0,P.z);
  torch.intensity=1.35+Math.sin(time*13)*0.08+Math.random()*0.06+(muzzle>0?2.2:0)+boomT*3+heat*1.5;
  const mvg=walkT!==lastWalkT?1:0; lastWalkT=walkT; bobAmt+=(mvg-bobAmt)*0.15;
  gun.position.set(0.3+Math.sin(walkT*5)*0.014*bobAmt,-0.26+Math.abs(Math.sin(walkT*10))*0.014*bobAmt+Math.sin(time*1.6)*0.003,-0.6+recoil);
  gun.rotation.x=recoil*0.8;
  const kk=Math.min(1,recoil/KICK[P.wi]), Ud=gunModels[P.wi].userData;
  if(Ud.slide) Ud.slide.position.z=-0.12+kk*0.07;
  if(Ud.pump) Ud.pump.position.z=-0.3+Math.sin(kk*3.14)*0.14;
  if(Ud.bolt) Ud.bolt.position.z=-0.05+kk*0.1;
  if(Ud.mat) Ud.mat.emissiveIntensity=0.8+kk*3;
  mflash.visible=muzzle>0; mflash.position.z=-MZ[P.wi]; const fs=0.35+Math.random()*0.3; mflash.scale.set(fs,fs,1);
  flashA=Math.max(0,flashA-0.02);
  flash.style.opacity=flashA;
  for(const s of flames){ const k=2.2+Math.sin(time*9+s.position.x*3)*0.25; s.scale.set(k,k,1); }
  renderer.render(scene,camera);
  // HUD
  const cpOn=checkpoints.filter(function(c){ return c.on; }).length;
  hud.innerHTML='<div style="font-size:10px;opacity:.6;letter-spacing:2px">FLOOR '+level+(level%5===0?' · BOSS':'')+'</div><div style="font-size:22px;font-weight:800;line-height:1.1">'+P.score+' <span style="font-size:10px;opacity:.55;font-weight:400">BEST '+Math.max(best,P.score)+'</span></div>'+
    '<div style="font-size:12px;margin-top:2px">☠ '+killsThisLevel+'/'+totalEnemies+' &nbsp; ⚑ '+cpOn+'/'+checkpoints.length+'</div>'+
    '<div style="font-size:11px;margin-top:2px">PORTAL '+(portalOpen?'<b style="color:#33e0ff">OPEN</b>':'<b style="color:#ff5566">SEALED</b>')+'</div>'+(P.combo>=2?'<div style="font-size:12px;color:#ffd23a;font-weight:bold">COMBO ×'+P.combo+'</div>':'');
  hpLbl.textContent='❤ '+Math.ceil(P.hp)+' / '+P.maxhp;
  const hbHtml=WEAPONS.map(function(w,i){ const on=i===P.wi; return '<div style="width:56px;height:44px;margin:0 2px;border-radius:8px;text-align:center;padding-top:3px;box-sizing:border-box;background:'+(on?'linear-gradient(#ffd23a,#e0a010)':'#000a')+';color:'+(on?'#000':'#ddd')+';border:1px solid '+(on?'#fff':'#ffffff33')+'"><div style="font-size:16px;line-height:18px">'+w.ico+'</div><div style="font-size:9px;font-weight:bold">'+(i+1)+' '+w.n+'</div></div>'; }).join('');
  if(hbHtml!==hbLast){ hotbar.innerHTML=hbHtml; hbLast=hbHtml; }
  const w0=WEAPONS[P.wi], amHtml='<div style="font-size:10px;opacity:.6;letter-spacing:2px">'+w0.n.toUpperCase()+'</div><div style="font-size:30px;font-weight:800;line-height:1;color:'+(P.ammo<w0.cost*3?'#ff6b6b':'#ffd23a')+'">'+P.ammo+'</div><div style="font-size:10px;opacity:.6">'+w0.cost+' per shot</div>';
  if(amHtml!==amLast){ ammoBox.innerHTML=amHtml; amLast=amHtml; }
  hm.style.opacity=hitT; hitT*=0.82; ht.style.opacity=heat; heat*=0.93; boomT*=0.9;
  hpb.style.width=(100*P.hp/P.maxhp)+'%';
  hpb.style.background=P.hp<30?'#e0455a':'#3ddc84';
  // minimap
  const s=130/GW;
  mctx.clearRect(0,0,130,130);
  for(let y=0;y<GH;y++) for(let x=0;x<GW;x++){
    if(!explored[y*GW+x]) continue;
    mctx.fillStyle=grid[y][x]===1?'#6a6f8c':'#2b2f44';
    mctx.fillRect(x*s,y*s,s+0.5,s+0.5);
  }
  if(explored[exitCell[1]*GW+exitCell[0]]){
    mctx.fillStyle=portalOpen?'#33e0ff':'#ff5566';
    mctx.fillRect(exitCell[0]*s,exitCell[1]*s,s,s);
  }
  for(const c of checkpoints){ if(explored[Math.floor(c.z/CELL)*GW+Math.floor(c.x/CELL)]){ mctx.fillStyle=c.on?'#33ff99':'#8899aa'; mctx.fillRect(c.x/CELL*s-2,c.z/CELL*s-2,4,4); } }
  mctx.fillStyle='#ff4040';
  for(const e of enemies){
    if(Math.hypot(e.x-P.x,e.z-P.z)<16){ mctx.fillRect(e.x/CELL*s-1.5,e.z/CELL*s-1.5,3,3); }
  }
  const px=P.x/CELL*s, pz=P.z/CELL*s;
  mctx.fillStyle='#ffe066'; mctx.beginPath(); mctx.arc(px,pz,2.6,0,6.3); mctx.fill();
  mctx.strokeStyle='#ffe066'; mctx.beginPath(); mctx.moveTo(px,pz);
  mctx.lineTo(px-Math.sin(P.yaw)*8,pz-Math.cos(P.yaw)*8); mctx.stroke();
}

// ---------- overlay / flow ----------
function hideOverlay(){ ov.style.display='none'; }
const BTN='display:inline-block;padding:10px 26px;border-radius:8px;font-weight:bold;cursor:pointer;margin:4px;border:1px solid #ffffff40;';
function btn(a,label,bg){ return '<span class="d3h" data-a="'+a+'" style="'+BTN+'background:'+bg+'">'+label+'</span>'; }
const MENU_ART='<style>@keyframes d3glow{0%,100%{filter:drop-shadow(0 0 10px #ff6a2a88)}50%{filter:drop-shadow(0 0 26px #ffa040)}}@keyframes d3pulse{0%,100%{box-shadow:0 0 0 0 #3fcf7e77}50%{box-shadow:0 0 0 12px #3fcf7e00}}@keyframes d3float{0%{transform:translateY(0);opacity:0}10%{opacity:1}100%{transform:translateY(-520px);opacity:0}}.d3h{transition:transform .12s,filter .12s}.d3h:hover{transform:translateY(-2px);filter:brightness(1.3)}</style><svg viewBox="0 0 800 500" preserveAspectRatio="xMidYMid slice" style="position:absolute;left:0;top:0;width:100%;height:100%"><defs><radialGradient id="mgBg" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#5a1a0e"/><stop offset=".45" stop-color="#1c0a18"/><stop offset="1" stop-color="#05050b"/></radialGradient><radialGradient id="mgPortal"><stop offset="0" stop-color="#9ff6ff"/><stop offset=".4" stop-color="#33b8e0" stop-opacity=".6"/><stop offset="1" stop-color="#33b8e0" stop-opacity="0"/></radialGradient><radialGradient id="mgFire"><stop offset="0" stop-color="#ffe9a0"/><stop offset=".5" stop-color="#ff8a2a"/><stop offset="1" stop-color="#ff4a00" stop-opacity="0"/></radialGradient><radialGradient id="mgVig" cx="50%" cy="50%" r="70%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient><filter id="mgBlur"><feGaussianBlur stdDeviation="6"/></filter></defs><rect width="800" height="500" fill="url(#mgBg)"/><g stroke="#4a3350" stroke-width="1.2" fill="none" opacity=".7"><path d="M0 0L330 170M0 500L330 330M800 0L470 170M800 500L470 330"/><path d="M330 170H470V330H330Z"/><path d="M280 140H520V360H280Z" opacity=".6"/><path d="M200 95H600V405H200Z" opacity=".4"/></g><circle cx="400" cy="250" r="90" fill="url(#mgPortal)"><animate attributeName="r" values="80;102;80" dur="4s" repeatCount="indefinite"/></circle><circle cx="400" cy="250" r="46" fill="none" stroke="#9ff6ff" stroke-width="3" opacity=".8"/><g fill="#07040a"><path d="M400 300C340 300 310 230 330 170C350 120 450 120 470 170C490 230 460 300 400 300Z"/><path d="M345 160L300 70L370 130ZM455 160L500 70L430 130Z"/><path d="M330 220L120 120L170 260L110 330L250 300L300 330Z"/><path d="M470 220L680 120L630 260L690 330L550 300L500 330Z"/></g><g filter="url(#mgBlur)"><circle cx="378" cy="190" r="10" fill="#ffee33"/><circle cx="422" cy="190" r="10" fill="#ffee33"/></g><circle cx="378" cy="190" r="4.5" fill="#fff8c0"><animate attributeName="opacity" values="1;.5;1" dur="2.4s" repeatCount="indefinite"/></circle><circle cx="422" cy="190" r="4.5" fill="#fff8c0"><animate attributeName="opacity" values="1;.5;1" dur="2.4s" repeatCount="indefinite"/></circle><g fill="#0a0a10" stroke="#ffffff30"><g transform="translate(30 440) rotate(-28)"><rect width="170" height="13" rx="3"/><rect x="-22" y="2" width="44" height="10"/><rect x="95" y="13" width="12" height="38"/><rect x="40" y="13" width="22" height="28"/></g><g transform="translate(770 440) rotate(208) scale(1 -1)"><rect width="170" height="13" rx="3"/><rect x="-22" y="2" width="44" height="10"/><rect x="95" y="13" width="12" height="38"/><rect x="40" y="13" width="22" height="28"/></g></g><g><rect x="64" y="300" width="12" height="130" fill="#1a1016"/><circle cx="70" cy="290" r="62" fill="url(#mgFire)" opacity=".55" filter="url(#mgBlur)"/><ellipse cx="70" cy="286" rx="14" ry="30" fill="url(#mgFire)"><animate attributeName="ry" values="26;35;28;33;26" dur=".8s" repeatCount="indefinite"/></ellipse><rect x="724" y="300" width="12" height="130" fill="#1a1016"/><circle cx="730" cy="290" r="62" fill="url(#mgFire)" opacity=".55" filter="url(#mgBlur)"/><ellipse cx="730" cy="286" rx="14" ry="30" fill="url(#mgFire)"><animate attributeName="ry" values="28;33;26;35;28" dur=".9s" repeatCount="indefinite"/></ellipse></g><ellipse cx="200" cy="475" rx="260" ry="46" fill="#c8c0e0" opacity=".13" filter="url(#mgBlur)"><animate attributeName="cx" values="200;280;200" dur="14s" repeatCount="indefinite"/></ellipse><ellipse cx="600" cy="480" rx="240" ry="40" fill="#c8c0e0" opacity=".11" filter="url(#mgBlur)"><animate attributeName="cx" values="600;520;600" dur="17s" repeatCount="indefinite"/></ellipse><rect width="800" height="500" fill="url(#mgVig)"/></svg>';
const EMBERS=(function(){ let s=''; for(let i=0;i<16;i++){ s+='<i style="position:absolute;left:'+(Math.random()*100)+'%;bottom:-10px;width:'+(2+Math.random()*3)+'px;height:'+(2+Math.random()*3)+'px;border-radius:50%;background:#ffa040;box-shadow:0 0 6px #ff7a20;opacity:0;animation:d3float '+(5+Math.random()*6)+'s linear '+(Math.random()*6)+'s infinite"></i>'; } return s; })();
function menuArt(op){ return '<div style="position:absolute;left:0;top:0;right:0;bottom:0;overflow:hidden;pointer-events:none;opacity:'+op+'">'+MENU_ART+EMBERS+'</div>'; }
function pill(a,label,on){ return '<span class="d3h" data-a="'+a+'" style="display:inline-block;padding:6px 14px;margin:3px;border-radius:20px;cursor:pointer;font-size:12px;font-weight:600;border:1px solid '+(on?'#ffd23a':'#ffffff30')+';background:'+(on?'#ffd23a22':'#ffffff0d')+';color:'+(on?'#ffd23a':'#ddd')+'">'+label+'</span>'; }
function srow(label,key,txt){ return '<div style="margin:10px 0;font-size:13px"><span style="display:inline-block;width:150px;text-align:right;opacity:.8">'+label+'</span> '+pill('set:'+key+':-1','−',false)+'<b style="display:inline-block;min-width:56px">'+txt+'</b>'+pill('set:'+key+':1','+',false)+'</div>'; }
function showMenu(kind){
  menuKind=kind;
  try{ if(document.exitPointerLock) document.exitPointerLock(); }catch(e){}
  ov.style.background='#05050b'; ov.style.justifyContent='flex-start'; ov.style.overflowY='auto';
  let h=menuArt(kind==='main'?1:0.5)+'<div style="margin:auto 0;width:100%;position:relative;z-index:1"><div style="font-size:42px;font-weight:900;letter-spacing:7px;background:linear-gradient(#fff2a8,#ff7a1a);-webkit-background-clip:text;background-clip:text;color:transparent;animation:d3glow 3s ease-in-out infinite">DEPTHS 3D</div>'+
    '<div style="font-size:11px;color:#ffb070;letter-spacing:4px;margin-top:-2px">DESCEND · SURVIVE · SLAY THE DEMON LORD</div>'+
    '<div style="font-size:11px;opacity:.55;margin-bottom:10px;letter-spacing:1px">v'+VERSION+' · BY RICHARD OKELLO · BEST '+best+'</div>';
  if(kind==='perk'){
    h+='<div style="font-size:18px;margin:8px 0 10px;color:#ffd23a">FLOOR CLEARED — CHOOSE A PERK</div><div style="display:flex;justify-content:center">';
    perkChoices.forEach(function(p,i){ h+='<div class="d3h" data-a="perk:'+i+'" style="width:190px;padding:16px;margin:6px;border-radius:12px;cursor:pointer;background:linear-gradient(#ffffff18,#ffffff08);border:1px solid #ffd23a66"><div style="font-size:30px">'+p.i+'</div><div style="font-size:15px;font-weight:bold;color:#ffd23a">'+p.n+'</div><div style="font-size:12px;opacity:.8;margin-top:6px">'+p.d+'</div></div>'; });
    h+='</div>';
  } else if(kind==='dead'){
    h+='<div style="font-size:22px;color:#ff6b7f;font-weight:bold">YOU DIED</div><div style="font-size:14px;margin:2px 0 10px">Floor '+level+' · Score '+P.score+' · Kills '+P.kills+'<br><span style="opacity:.7">'+(mode==='Hardcore'?'Hardcore: no respawns':'Respawning costs 15% of your score')+'</span></div>'+(mode==='Hardcore'?'':btn('respawn','✚ Respawn at checkpoint','#2f8f5b'))+btn('play','↻ New run','#444')+btn('menu','☰ Menu','#444');
  } else if(kind==='pause'){
    h+='<div style="font-size:22px;margin:8px 0 12px">PAUSED</div>'+btn('resume','▶ Resume','#2f8f5b')+btn('play','↻ Restart','#444')+btn('menu','☰ Main menu','#444');
  } else {
    h+=pill('tab:play','▶ Play',menuTab==='play')+pill('tab:stats','🏆 Stats',menuTab==='stats')+pill('tab:set','⚙ Settings',menuTab==='set')+'<div style="margin:8px auto 0;max-width:740px;padding:10px 12px;border-radius:14px;background:rgba(8,6,14,.62);border:1px solid #ffffff1f;box-shadow:0 8px 30px #000a;backdrop-filter:blur(4px)">';
    if(menuTab==='play'){
      h+='<div style="font-size:11px;opacity:.6;margin-top:4px;letter-spacing:2px">STARTING WEAPON</div><div style="display:flex;justify-content:center;flex-wrap:wrap">';
      WEAPONS.forEach(function(w,i){
        const c='#'+w.col.toString(16).padStart(6,'0');
        h+='<div class="d3h" data-a="wpn:'+i+'" style="width:112px;padding:7px;margin:3px;border-radius:10px;cursor:pointer;text-align:left;font-size:10px;line-height:1.35;background:linear-gradient(#ffffff18,#ffffff06);border:2px solid '+(i===startW?'#ffd23a':'#ffffff25')+'"><b style="font-size:13px;color:'+c+'">'+w.ico+' '+(i+1)+' · '+w.n+'</b><br>'+w.d+'<br><span style="opacity:.65">DMG '+w.dmg+(w.pel>1?'×'+w.pel:'')+' · AMMO '+w.cost+'</span></div>';
      });
      h+='</div><div style="font-size:11px;opacity:.6;margin-top:6px;letter-spacing:2px">DIFFICULTY</div>';
      Object.keys(DIFF).forEach(function(k){ h+=pill('diff:'+k,k,k===difficulty); });
      h+='<div style="font-size:11px;opacity:.6;margin-top:4px;letter-spacing:2px">MODE</div>';
      ['Normal','Hardcore','Daily'].forEach(function(k){ h+=pill('mode:'+k,k,k===mode); });
      h+='<div style="font-size:11px;opacity:.7;margin:2px 0 8px">'+({Normal:'Respawn at checkpoints. Pick a perk after every floor.',Hardcore:'One life. No respawns.',Daily:'Same dungeon layouts for everyone today.'})[mode]+'</div>'+'<div style="margin-top:6px">'+btn('play','▶ PLAY','linear-gradient(#3fcf7e,#1f8a52);animation:d3pulse 1.8s infinite;font-size:18px;padding:12px 60px;letter-spacing:3px')+'</div>';
    } else if(menuTab==='stats'){
      h+='<div style="display:flex;justify-content:center;flex-wrap:wrap">';
      [['Runs',STATS.runs],['Kills',STATS.kills],['Deaths',STATS.deaths],['Floors',STATS.floors],['Best',best]].forEach(function(s){ h+='<div style="width:90px;padding:8px;margin:3px;border-radius:10px;background:#ffffff10"><div style="font-size:18px;font-weight:bold;color:#ffd23a">'+s[1]+'</div><div style="font-size:10px;opacity:.6">'+s[0].toUpperCase()+'</div></div>'; });
      h+='</div><div style="font-size:11px;opacity:.6;margin-top:8px;letter-spacing:2px">TOP 10 RUNS</div><div style="font-size:12px;line-height:1.55">';
      if(!BOARD.length) h+='<span style="opacity:.5">No runs yet. Go set a score!</span>';
      BOARD.forEach(function(r,i){ h+='#'+(i+1)+' <b>'+r.s+'</b> · Floor '+r.l+' · '+r.w+' · '+r.m+'<br>'; });
      h+='</div><div style="font-size:11px;opacity:.6;margin-top:8px;letter-spacing:2px">ACHIEVEMENTS</div><div style="font-size:12px;line-height:1.55">';
      Object.keys(ACHS).forEach(function(k){ const p=ACHS[k].split('|'); h+=(STATS.ach[k]?'✅ <b>':'🔒 <span style="opacity:.6">')+p[0]+(STATS.ach[k]?'</b>':'')+' — '+p[1]+(STATS.ach[k]?'':'</span>')+'<br>'; });
      h+='</div>';
    } else {
      h+='<div style="margin-top:10px">'+srow('Mouse sensitivity','sens',SET.sens.toFixed(1)+'x')+srow('Field of view','fov',SET.fov+'°')+srow('Volume','vol',Math.round(SET.vol*100)+'%')+'</div><div style="font-size:11px;opacity:.55;margin-top:8px">Settings are saved in your browser.</div>';
    }
    h+='</div>';
  }
  h+='<div style="margin-top:10px;font-size:10px;opacity:.9">'+[['WASD','Move'],['← →','Turn'],['Space','Fire'],['1–6','Guns'],['P','Pause']].map(function(k){ return '<span style="display:inline-block;margin:2px 7px"><span style="border:1px solid #ffffff55;border-bottom-width:3px;border-radius:5px;padding:1px 6px;background:#ffffff14;font-weight:bold">'+k[0]+'</span> '+k[1]+'</span>'; }).join('')+'</div></div>';
  ov.innerHTML=h; ov.style.display='flex';
}
function newGame(){
  level=1; P.hp=P.maxhp=100; P.ammo=70; P.score=0; P.kills=0; P.cool=0; flashA=0; P.inv=0; P.combo=0; P.ct=0; P.dmgm=1; P.rate=1; P.leech=0; P.scav=0; P.spd=1; P.entry=null; STATS.runs++;
  buildLevel(); setWeapon(startW); state='playing'; paused=false; hideOverlay();
  toast('Find the portal. Kill half the dungeon to open it.',3000);
}
function activate(){ if(state==='dead'){ if(mode!=='Hardcore'){ respawn(); wrap.focus(); } } else if(state==='ready'){ newGame(); wrap.focus(); } }
ov.addEventListener('mousedown',function(ev){ ev.stopPropagation(); });
ov.addEventListener('click',function(ev){
  const t=ev.target.closest('[data-a]'); if(!t) return;
  const a=t.getAttribute('data-a').split(':');
  if(!actx){ try{ actx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} }
  if(a[0]==='tab'){ menuTab=a[1]; showMenu('main'); }
  else if(a[0]==='mode'){ mode=a[1]; showMenu(menuKind); }
  else if(a[0]==='perk'){ const pk=perkChoices[+a[1]]; pk.f(); toast(pk.n+' acquired',1800); state='playing'; hideOverlay(); wrap.focus(); }
  else if(a[0]==='set'){ const st={sens:[0.1,0.3,3],fov:[5,60,100],vol:[0.1,0,1]}[a[1]]; SET[a[1]]=Math.round(Math.min(st[2],Math.max(st[1],SET[a[1]]+st[0]*(+a[2])))*100)/100; camera.fov=SET.fov; camera.updateProjectionMatrix(); save('d3d_set',SET); showMenu(menuKind); }
  else if(a[0]==='wpn'){ startW=+a[1]; showMenu(menuKind); }
  else if(a[0]==='diff'){ difficulty=a[1]; showMenu(menuKind); }
  else if(a[0]==='respawn'){ respawn(); wrap.focus(); }
  else if(a[0]==='play'){ newGame(); wrap.focus(); }
  else if(a[0]==='resume'){ paused=false; hideOverlay(); wrap.focus(); }
  else if(a[0]==='menu'){ state='ready'; paused=false; showMenu('main'); }
});
showMenu('main');
wrap.addEventListener('mousedown',function(ev){
  if(ev.button===2){ keys.look=true; ev.preventDefault(); return; }
  if(state!=='playing'||paused) return;
  keys.mouse=true; wrap.focus();
  try{
    if(document.pointerLockElement!==renderer.domElement&&renderer.domElement.requestPointerLock){
      const pr=renderer.domElement.requestPointerLock(); if(pr&&pr.catch) pr.catch(function(){});
    }
  }catch(e){}
});
wrap.addEventListener('wheel',function(ev){
  if(state==='playing'&&!paused){ setWeapon((P.wi+(ev.deltaY>0?1:WEAPONS.length-1))%WEAPONS.length); ev.preventDefault(); }
},{passive:false});
document.addEventListener('pointerlockchange',function(){
  if(!document.pointerLockElement&&state==='playing'&&!paused){ paused=true; showMenu('pause'); }
});
window.addEventListener('mouseup',function(ev){ if(ev.button===2) keys.look=false; else keys.mouse=false; });
wrap.addEventListener('contextmenu',function(ev){ev.preventDefault();});
wrap.addEventListener('mousemove',function(ev){
  if((keys.look||document.pointerLockElement===renderer.domElement)&&state==='playing'&&!paused) P.yaw-=ev.movementX*0.0045*SET.sens;
});
wrap.addEventListener('keydown',function(ev){
  keys[ev.code]=true;
  if(/^Digit[1-6]$/.test(ev.code)&&state==='playing'&&!paused) setWeapon(+ev.code[5]-1);
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(ev.code)>=0) ev.preventDefault();
  if(ev.code==='KeyR'&&(state==='dead'||state==='ready')) activate();
  if((ev.code==='KeyP'||ev.code==='Escape')&&state==='playing'){
    if(paused){ paused=false; hideOverlay(); }
    else { paused=true; showMenu('pause'); }
  }
});
wrap.addEventListener('keyup',function(ev){ keys[ev.code]=false; });
wrap.addEventListener('blur',function(){
  for(const c in keys) keys[c]=false;
  if(state==='playing'&&!paused){ paused=true; showMenu('pause'); }
});

// initial dummy level so the scene renders behind the title
buildLevel();
let last=performance.now();
function loop(now){
  requestAnimationFrame(loop);
  const dt=Math.min(0.05,(now-last)/1000); last=now;
  if(state==='playing'&&!paused) update(dt);
  else if(state==='ready'){ time+=dt; walkT=0; P.yaw+=dt*0.15; }
  render();
}
requestAnimationFrame(loop);
}

function fail(){
  document.getElementById('dd3d-root').innerHTML='<div style="padding:20px;color:#f88;line-height:1.6">Could not load three.js from the CDN.<br>Check your internet connection, then reload the page (or re-run the Colab cell).</div>';
}
function loadScript(urls){
  if(!urls.length){ fail(); return; }
  const s=document.createElement('script');
  s.src=urls[0];
  s.onload=function(){ if(window.THREE) start(); else loadScript(urls.slice(1)); };
  s.onerror=function(){ loadScript(urls.slice(1)); };
  document.head.appendChild(s);
}
if(window.THREE){ start(); }
else {
  loadScript([
    'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',
    'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js'
  ]);
}
})();
