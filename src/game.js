(function(){
function start(){
const wrap=document.getElementById('dd3d-root');
const hud=wrap.querySelector('.hud'), mm=wrap.querySelector('.mm'), mctx=mm.getContext('2d');
const hpb=wrap.querySelector('.hpb'), flash=wrap.querySelector('.flash');
const ov=wrap.querySelector('.ov'), toastEl=wrap.querySelector('.toast');
const vg=document.createElement('div');
vg.style.cssText='position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 50%,rgba(0,0,0,.7) 100%)';
wrap.insertBefore(vg,hud);
const VERSION='3.1.0';
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
  const steel=GM(0x8a8fa0), dark=GM(0x22242c), wood=GM(0x6a4220), blue=GM(0x4a90e2), cy=GM(0x33e0ff,0x33e0ff), orange=GM(0xff9a2a,0xff6a00);
  let g=gunModels[0];
  gb(g,.08,.09,.42,0,0,-.1,steel); gc(g,.025,.2,0,.01,-.4,dark); gb(g,.07,.2,.09,0,-.14,.08,wood); gb(g,.02,.03,.03,0,.07,-.28,orange);
  g=gunModels[1];
  gc(g,.032,.75,-.04,.02,-.42,dark); gc(g,.032,.75,.04,.02,-.42,dark); gb(g,.13,.11,.4,0,-.02,.05,wood); gb(g,.15,.09,.22,0,-.06,-.32,wood); gb(g,.09,.1,.3,0,-.1,.35,wood);
  g=gunModels[2];
  gb(g,.09,.12,.5,0,0,-.05,blue); gc(g,.022,.3,0,.02,-.42,dark); gb(g,.06,.28,.08,0,-.2,-.02,dark); gb(g,.06,.16,.08,0,-.1,.22,dark); gb(g,.03,.04,.1,0,.09,-.1,orange);
  g=gunModels[3];
  gb(g,.1,.12,.55,0,-.02,.05,dark); gc(g,.03,.95,0,.02,-.55,steel); gc(g,.012,.7,0,.02,-.5,cy);
  for(let i=0;i<4;i++){ const r=new THREE.Mesh(new THREE.TorusGeometry(.055,.012,6,14),cy); r.position.set(0,.02,-.25-i*.2); g.add(r); }
  g=gunModels[4]; const grn=GM(0x7acb4a);
  gc(g,.075,.6,0,0,-.2,grn); gc(g,.1,.16,0,-.02,.08,dark); gb(g,.07,.2,.09,0,-.15,.15,wood); gc(g,.04,.12,0,0,-.55,dark);
  g=gunModels[5]; const red=GM(0xaa3322);
  gc(g,.04,.55,0,.02,-.38,dark); gc(g,.05,.1,0,.02,-.68,orange); gc(g,.075,.45,0,.12,0,red); gb(g,.08,.2,.1,0,-.14,.12,wood);
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

// ---------- state ----------
let state='ready', paused=false;
let level=1, grid=null, GW=0, GH=0, explored=null;
let levelGroup=null, portal=null, portalOpen=false, exitCell=[1,1];
let enemies=[], pickups=[], orbs=[], fx=[], totalEnemies=0, killsThisLevel=0;
const P={x:0,z:0,yaw:0,hp:100,maxhp:100,ammo:60,score:0,cool:0,kills:0,r:0.4,wi:0,inv:0,combo:0,ct:0,shake:0,dmgm:1,rate:1,leech:0,scav:0,spd:1,entry:null};
let checkpoints=[], lastCP=null, flames=[], barrels=[], gpHeld=false;
let muzzle=0, recoil=0, walkT=0, flashA=0, time=0;
const keys={};
const WEAPONS=[
 {n:'Pistol',cd:.28,cost:1,dmg:2,pel:1,spr:.01,pierce:false,col:0x8a8fa0,len:1,d:'Accurate and cheap'},
 {n:'Shotgun',cd:.8,cost:3,dmg:1.3,pel:8,spr:.14,pierce:false,col:0xa0663a,len:.9,d:'8 pellets. Deadly up close'},
 {n:'SMG',cd:.07,cost:1,dmg:1,pel:1,spr:.05,pierce:false,col:0x4a90e2,len:1.1,d:'Rapid fire'},
 {n:'Railgun',cd:1.1,cost:6,dmg:9,pel:1,spr:0,pierce:true,col:0x33e0ff,len:1.4,d:'Pierces every enemy in line'},
 {n:'Grenade',cd:1,cost:5,dmg:6,pel:1,spr:.01,pierce:false,blast:3.5,col:0x7acb4a,len:1,d:'Explosive splash damage'},
 {n:'Flamer',cd:.06,cost:1,dmg:.8,pel:3,spr:.18,pierce:true,rng:8,col:0xff6a2a,len:1,d:'Short range, burns crowds'}];
const PERKS=[
 {n:'Hollow Points',d:'+25% weapon damage',f:function(){P.dmgm*=1.25;}},
 {n:'Quick Hands',d:'Fire 20% faster',f:function(){P.rate*=0.8;}},
 {n:'Iron Skin',d:'+25 max HP and full heal',f:function(){P.maxhp+=25;P.hp=P.maxhp;}},
 {n:'Vampiric',d:'Heal 2 HP on every kill',f:function(){P.leech+=2;}},
 {n:'Scavenger',d:'+40 ammo now, ammo pickups +50%',f:function(){P.ammo+=40;P.scav+=0.5;}},
 {n:'Light Boots',d:'+15% movement speed',f:function(){P.spd*=1.15;}}];
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
  enemies=[]; pickups=[]; orbs=[]; fx=[]; killsThisLevel=0; portalOpen=false; flames=[]; checkpoints=[]; barrels=[];
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

function buildMonster(type,mat){
  const g=new THREE.Group();
  const S=function(r){return new THREE.SphereGeometry(r,10,10);};
  const X=function(geo,col,em){return new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:col,emissive:em||0,flatShading:true}));};
  const add=function(m,x,y,z,rx,rz){m.position.set(x,y,z); if(rx) m.rotation.x=rx; if(rz) m.rotation.z=rz; g.add(m); return m;};
  const eyes=function(y,z,s,c){[-1,1].forEach(function(k){add(X(S(s),c,c),k*s*1.9,y,z);});};
  const horns=function(y,sp,h,col){[-1,1].forEach(function(k){add(X(new THREE.ConeGeometry(h*0.25,h,6),col),k*sp,y,0.05,0,-k*0.35);});};
  if(type==='chaser'){ // imp
    const b=add(new THREE.Mesh(S(0.5),mat),0,0,0); b.scale.y=1.2;
    add(new THREE.Mesh(S(0.3),mat),0,0.8,0.1); horns(1.15,0.18,0.35,0x2a0a0a); eyes(0.85,0.36,0.06,0xffee33);
    [-1,1].forEach(function(k){ add(X(new THREE.CylinderGeometry(0.07,0.07,0.7,6),0xaa2222),k*0.55,0.05,0.25,-1.1);
      add(X(new THREE.ConeGeometry(0.06,0.22,5),0xffe9a0),k*0.55,-0.12,0.6,1.57); });
  } else if(type==='shooter'){ // floating eye-demon
    add(new THREE.Mesh(S(0.7),mat),0,0,0);
    add(X(S(0.4),0xf4f4f4,0x555555),0,0.1,0.5); add(X(S(0.19),0x110011),0,0.1,0.86); add(X(S(0.07),0xff2222,0xff2222),0.05,0.14,1.03);
    horns(0.7,0.3,0.4,0x3a1060);
    for(let i=0;i<5;i++){ const a=i*1.256; add(X(new THREE.CylinderGeometry(0.08,0.03,0.9,6),0x7a30b0),Math.cos(a)*0.38,-0.85,Math.sin(a)*0.38); }
  } else if(type==='brute'){ // ogre
    add(new THREE.Mesh(new THREE.BoxGeometry(1.1,1.2,0.8),mat),0,0,0);
    add(X(new THREE.BoxGeometry(0.55,0.45,0.5),0x7a4a22),0,0.95,0.1); eyes(1.0,0.37,0.07,0xff3030);
    [-1,1].forEach(function(k){ add(X(new THREE.BoxGeometry(0.36,1.1,0.36),0x8a5a2a),k*0.78,-0.1,0.1);
      add(X(new THREE.BoxGeometry(0.4,0.8,0.4),0x5a3a1a),k*0.3,-1.0,0); add(X(new THREE.ConeGeometry(0.06,0.25,5),0xfff2cc),k*0.15,0.78,0.42,1.4); });
  } else if(type==='teleporter'){
    add(new THREE.Mesh(new THREE.OctahedronGeometry(0.65),mat),0,0,0);
    add(X(new THREE.TorusGeometry(0.9,0.04,6,24),0x99f0ff,0x33ddff),0,0,0,1.2); eyes(0.1,0.45,0.07,0xffffff);
  } else if(type==='splitter'||type==='mini'){
    add(new THREE.Mesh(S(0.6),mat),0,0,0); add(new THREE.Mesh(S(0.35),mat),0.45,0.3,0.1); add(new THREE.Mesh(S(0.3),mat),-0.4,-0.2,0.2); eyes(0.15,0.52,0.08,0xffffff);
    if(type==='mini') g.scale.set(0.55,0.55,0.55);
  } else { // boss demon lord
    const b=add(new THREE.Mesh(S(1.1),mat),0,0,0); b.scale.y=1.25;
    add(new THREE.Mesh(S(0.55),mat),0,1.5,0.15); horns(2.05,0.4,0.95,0x220000); eyes(1.58,0.62,0.1,0xffff33);
    [-1,1].forEach(function(k){ add(X(new THREE.BoxGeometry(1.9,0.07,1.2),0x5a0a1a,0x300008),k*1.6,0.7,-0.5,0,k*0.45);
      add(X(new THREE.CylinderGeometry(0.2,0.2,1.3,7),0xaa1144),k*1.2,-0.2,0.4,-0.9); });
  }
  return g;
}

function addBarrel(x,z){
  const m=new THREE.Mesh(new THREE.CylinderGeometry(0.4,0.4,0.9,10),GM(0xaa2222,0x330000)); m.position.set(x,0.45,z); levelGroup.add(m);
  const band=new THREE.Mesh(new THREE.CylinderGeometry(0.41,0.41,0.15,10),GM(0xffcc22,0x332200)); band.position.y=0.1; m.add(band);
  barrels.push({x:x,z:z,mesh:m});
}
function explode(x,z,r,dmg,bar){
  if(bar){ levelGroup.remove(bar.mesh); barrels.splice(barrels.indexOf(bar),1); }
  burst(x,1,z,0xff9a2a,30,8); burst(x,1,z,0xffee88,12,6); P.shake=Math.max(P.shake,0.6); beep(90,0.4,'sawtooth',0.1,-60);
  for(const e of enemies.slice()){
    const d=Math.hypot(e.x-x,e.z-z);
    if(d<r){ e.hp-=dmg*(1-d/r*0.5); e.hit=0.12; e.alert=true; if(e.hp<=0){ killEnemy(e); if(bar) award('barrel'); } }
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
function addPickup(type,x,z){
  const mesh=type==='hp'?pkHealth():(type==='ammo'?pkAmmo():new THREE.Mesh(new THREE.OctahedronGeometry(0.3),new THREE.MeshStandardMaterial({color:0x44e0ff,emissive:0x1fa8d0,emissiveIntensity:1})));
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
  burst(e.x,e.baseY,e.z,e.baseCol,e.type==='boss'?40:16,6);
  beep(300,0.18,'sawtooth',0.06,-200);
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
  P.ammo-=w.cost; P.cool=w.cd*P.rate; muzzle=0.06; P.shake=Math.max(P.shake,(w.pel>1||w.blast)?0.25:0.05); recoil=w.pierce?0.25:(w.pel>1?0.2:0.1);
  beep(w.pierce?200:(w.pel>1?140:780),0.1,w.pierce?'sawtooth':'square',0.05,-100);
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
      const cr=Math.random()<0.1, dv=w.dmg*P.dmgm*(cr?2:1); e.hp-=dv; e.hit=0.1; e.alert=true;
      if(w.pel<2||Math.random()<0.3) dmgNum(e.x,e.baseY+0.9,e.z,(cr?'💥':'')+Math.max(1,Math.round(dv)),cr?'#ffd23a':'#fff');
      burst(e.x,e.baseY,e.z,0xffffff,4,3);
      if(e.hp<=0) killEnemy(e); else beep(220,0.05,'triangle',0.05);
    }
  }
}

// ---------- update ----------
function update(dt){
  time+=dt; P.inv=Math.max(0,P.inv-dt); P.ct-=dt; if(P.ct<=0) P.combo=0;
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
  if(ml>0){ mx=mx/ml*sp; mz=mz/ml*sp; moveEnt(P,mx,mz,P.r); walkT+=dt; }
  if(k.Space||k.KeyF||k.mouse||gpFire) shoot();

  // enemies
  for(const e of enemies){
    const dx=P.x-e.x, dz=P.z-e.z, d=Math.hypot(dx,dz)||0.001;
    const visible=d<22&&los(e.x,e.z,P.x,P.z);
    if(!e.alert&&visible&&d<20) e.alert=true;
    e.mesh.position.set(e.x,e.baseY+Math.sin(time*3+e.ph)*0.15,e.z);
    e.mesh.rotation.y=Math.atan2(dx,dz);
    if(e.hit>0){ e.hit-=dt; e.mat.emissive.set(0xffffff); e.mat.emissiveIntensity=1.2; }
    else { e.mat.emissive.set(e.baseCol); e.mat.emissiveIntensity=e.alert?0.9:0.35; }
    if(!e.alert) continue;
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
  torch.intensity=1.35+Math.sin(time*13)*0.08+Math.random()*0.06+(muzzle>0?2.2:0);
  gun.position.z=-0.6+recoil; gun.rotation.x=recoil*0.8;
  flashA=Math.max(0,flashA-0.02);
  flash.style.opacity=flashA;
  for(const s of flames){ const k=2.2+Math.sin(time*9+s.position.x*3)*0.25; s.scale.set(k,k,1); }
  renderer.render(scene,camera);
  // HUD
  hud.innerHTML='<b>Level '+level+'</b> &nbsp; Score '+P.score+' &nbsp; <span style="opacity:.7">Best '+Math.max(best,P.score)+'</span><br>Kills '+killsThisLevel+'/'+totalEnemies+
    ' &nbsp; Ammo <b style="color:'+(P.ammo<8?'#ff6b6b':'#ffd23a')+'">'+P.ammo+'</b><br>Portal: '+
    (portalOpen?'<span style="color:#33e0ff">OPEN</span>':'<span style="color:#ff5566">sealed</span>')+'<br>'+wbar();
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
function btn(a,label,bg){ return '<span data-a="'+a+'" style="'+BTN+'background:'+bg+'">'+label+'</span>'; }
function pill(a,label,on){ return '<span data-a="'+a+'" style="display:inline-block;padding:6px 14px;margin:3px;border-radius:20px;cursor:pointer;font-size:12px;font-weight:600;border:1px solid '+(on?'#ffd23a':'#ffffff30')+';background:'+(on?'#ffd23a22':'#ffffff0d')+';color:'+(on?'#ffd23a':'#ddd')+'">'+label+'</span>'; }
function srow(label,key,txt){ return '<div style="margin:10px 0;font-size:13px"><span style="display:inline-block;width:150px;text-align:right;opacity:.8">'+label+'</span> '+pill('set:'+key+':-1','−',false)+'<b style="display:inline-block;min-width:56px">'+txt+'</b>'+pill('set:'+key+':1','+',false)+'</div>'; }
function showMenu(kind){
  menuKind=kind;
  try{ if(document.exitPointerLock) document.exitPointerLock(); }catch(e){}
  ov.style.background='radial-gradient(ellipse at 50% 15%,rgba(80,24,8,.9),rgba(4,4,12,.95))'; ov.style.justifyContent='flex-start'; ov.style.overflowY='auto';
  let h='<div style="margin:auto 0;width:100%"><div style="font-size:42px;font-weight:900;letter-spacing:7px;background:linear-gradient(#fff2a8,#ff7a1a);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 14px #ff6a2a88)">DEPTHS 3D</div>'+
    '<div style="font-size:11px;opacity:.55;margin-bottom:10px;letter-spacing:1px">v'+VERSION+' · BY RICHARD OKELLO · BEST '+best+'</div>';
  if(kind==='perk'){
    h+='<div style="font-size:18px;margin:8px 0 10px;color:#ffd23a">FLOOR CLEARED — CHOOSE A PERK</div><div style="display:flex;justify-content:center">';
    perkChoices.forEach(function(p,i){ h+='<div data-a="perk:'+i+'" style="width:190px;padding:16px;margin:6px;border-radius:12px;cursor:pointer;background:linear-gradient(#ffffff18,#ffffff08);border:1px solid #ffd23a66"><div style="font-size:15px;font-weight:bold;color:#ffd23a">'+p.n+'</div><div style="font-size:12px;opacity:.8;margin-top:6px">'+p.d+'</div></div>'; });
    h+='</div>';
  } else if(kind==='dead'){
    h+='<div style="font-size:22px;color:#ff6b7f;font-weight:bold">YOU DIED</div><div style="font-size:14px;margin:2px 0 10px">Floor '+level+' · Score '+P.score+' · Kills '+P.kills+'<br><span style="opacity:.7">'+(mode==='Hardcore'?'Hardcore: no respawns':'Respawning costs 15% of your score')+'</span></div>'+(mode==='Hardcore'?'':btn('respawn','✚ Respawn at checkpoint','#2f8f5b'))+btn('play','↻ New run','#444')+btn('menu','☰ Menu','#444');
  } else if(kind==='pause'){
    h+='<div style="font-size:22px;margin:8px 0 12px">PAUSED</div>'+btn('resume','▶ Resume','#2f8f5b')+btn('play','↻ Restart','#444')+btn('menu','☰ Main menu','#444');
  } else {
    h+=pill('tab:play','▶ Play',menuTab==='play')+pill('tab:stats','🏆 Stats',menuTab==='stats')+pill('tab:set','⚙ Settings',menuTab==='set')+'<div style="margin-top:6px">';
    if(menuTab==='play'){
      h+='<div style="font-size:11px;opacity:.6;margin-top:4px;letter-spacing:2px">STARTING WEAPON</div><div style="display:flex;justify-content:center;flex-wrap:wrap">';
      WEAPONS.forEach(function(w,i){
        const c='#'+w.col.toString(16).padStart(6,'0');
        h+='<div data-a="wpn:'+i+'" style="width:112px;padding:7px;margin:3px;border-radius:10px;cursor:pointer;text-align:left;font-size:10px;line-height:1.35;background:#ffffff10;border:2px solid '+(i===startW?'#ffd23a':'#ffffff25')+'"><b style="font-size:13px;color:'+c+'">'+(i+1)+' · '+w.n+'</b><br>'+w.d+'<br><span style="opacity:.65">DMG '+w.dmg+(w.pel>1?'×'+w.pel:'')+' · AMMO '+w.cost+'</span></div>';
      });
      h+='</div><div style="font-size:11px;opacity:.6;margin-top:6px;letter-spacing:2px">DIFFICULTY</div>';
      Object.keys(DIFF).forEach(function(k){ h+=pill('diff:'+k,k,k===difficulty); });
      h+='<div style="font-size:11px;opacity:.6;margin-top:4px;letter-spacing:2px">MODE</div>';
      ['Normal','Hardcore','Daily'].forEach(function(k){ h+=pill('mode:'+k,k,k===mode); });
      h+='<div style="font-size:11px;opacity:.7;margin:2px 0 8px">'+({Normal:'Respawn at checkpoints. Pick a perk after every floor.',Hardcore:'One life. No respawns.',Daily:'Same dungeon layouts for everyone today.'})[mode]+'</div>'+btn('play','▶ PLAY','#2f8f5b');
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
  h+='<div style="font-size:10px;opacity:.5;margin-top:10px;line-height:1.5">W A S D move · ← → / Q E turn · Space / F / click fire · 1–6 or wheel switch gun · P pause · gamepad supported</div></div>';
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
