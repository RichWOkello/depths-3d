(function(){
function start(){
const wrap=document.getElementById('dd3d-root');
const hud=wrap.querySelector('.hud'), mm=wrap.querySelector('.mm'), mctx=mm.getContext('2d');
const hpb=wrap.querySelector('.hpb'), flash=wrap.querySelector('.flash');
const ov=wrap.querySelector('.ov'), toastEl=wrap.querySelector('.toast');
const VERSION='1.1.0';
const VW=800, VH=500, CELL=4, WALLH=3.2;

// ---------- renderer / scene ----------
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(VW,VH);
renderer.domElement.style.cssText='display:block;width:800px;height:500px';
wrap.insertBefore(renderer.domElement, wrap.firstChild);
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x050508);
scene.fog=new THREE.Fog(0x050508,2,28);
const camera=new THREE.PerspectiveCamera(72,VW/VH,0.1,100);
camera.rotation.order='YXZ';
scene.add(camera);
scene.add(new THREE.AmbientLight(0x4a4a70,0.7));
const torch=new THREE.PointLight(0xffb060,1.4,26,1.6);
scene.add(torch);

// gun viewmodel
const gun=new THREE.Mesh(new THREE.BoxGeometry(0.09,0.11,0.55),
  new THREE.MeshStandardMaterial({color:0x666a7a,metalness:0.6,roughness:0.4}));
gun.position.set(0.3,-0.26,-0.6);
const barrel=new THREE.Mesh(new THREE.BoxGeometry(0.04,0.04,0.25),
  new THREE.MeshStandardMaterial({color:0x22242c}));
barrel.position.set(0,0.02,-0.35); gun.add(barrel);
camera.add(gun);

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
const floorMat=new THREE.MeshStandardMaterial({map:floorTex,roughness:1});
const ceilMat=new THREE.MeshStandardMaterial({map:ceilTex,roughness:1});
const wallGeo=new THREE.BoxGeometry(CELL,WALLH,CELL);

// ---------- audio ----------
let actx=null;
function beep(f,d,type,v,slide){
  if(!actx) return;
  try{
    const o=actx.createOscillator(), g=actx.createGain();
    o.type=type||'square'; o.frequency.value=f;
    if(slide) o.frequency.exponentialRampToValueAtTime(Math.max(30,f+slide),actx.currentTime+d);
    g.gain.value=v||0.05;
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
const P={x:0,z:0,yaw:0,hp:100,maxhp:100,ammo:60,score:0,cool:0,kills:0,r:0.4};
let muzzle=0, recoil=0, walkT=0, flashA=0, time=0;
const keys={};
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
  if(levelGroup) scene.remove(levelGroup);
  levelGroup=new THREE.Group(); scene.add(levelGroup);
  enemies=[]; pickups=[]; orbs=[]; fx=[]; killsThisLevel=0; portalOpen=false;
  const n=Math.min(27,9+2*level);
  const m=genMaze(n); grid=m.g; GW=GH=n; exitCell=m.far;
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

  const normal=Math.min(26,4+level*2);
  if(level%5===0&&far.length){ const bc=pick(far), bp=cellCenter(bc); addEnemy('boss',bp[0],bp[1]); }
  for(let i=0;i<normal&&far.length;i++){
    const c=pick(far), p=cellCenter(c), r=Math.random();
    let type='chaser';
    if(level>=3&&r<0.18) type='brute'; else if(r<0.5) type='shooter';
    addEnemy(type,p[0],p[1]);
  }
  totalEnemies=enemies.length;
  if(level%5===0) setTimeout(()=>toast('⚠ BOSS FLOOR — something huge is hunting you',3200),400);
  const nh=3+Math.floor(level/2), na=4+level, ng=5+level;
  for(let i=0;i<nh&&all.length;i++){const p=cellCenter(pick(all)); addPickup('hp',p[0],p[1]);}
  for(let i=0;i<na&&all.length;i++){const p=cellCenter(pick(all)); addPickup('ammo',p[0],p[1]);}
  for(let i=0;i<ng&&all.length;i++){const p=cellCenter(pick(all)); addPickup('gem',p[0],p[1]);}
}

function addEnemy(type,x,z){
  const s=1+0.1*(level-1);
  let col,geo,hp,speed,r,dmg,y;
  if(type==='chaser'){col=0xff3a3a;geo=new THREE.OctahedronGeometry(0.6);hp=4;speed=3.4;r=0.5;dmg=12;y=1.2;}
  else if(type==='shooter'){col=0xb04cff;geo=new THREE.IcosahedronGeometry(0.6);hp=5;speed=2.4;r=0.5;dmg=0;y=1.4;}
  else if(type==='boss'){col=0xff2288;geo=new THREE.IcosahedronGeometry(1.4);hp=45;speed=2.1;r=1.0;dmg=26;y=1.9;}
  else {col=0xff9a2a;geo=new THREE.DodecahedronGeometry(1.0);hp=14;speed=2.2;r=0.85;dmg=22;y=1.4;}
  const mat=new THREE.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:0.6,flatShading:true});
  const mesh=new THREE.Mesh(geo,mat);
  mesh.position.set(x,y,z); levelGroup.add(mesh);
  const e={type:type,x:x,z:z,hp:Math.ceil(hp*s),maxhp:Math.ceil(hp*s),speed:speed,r:r,dmg:dmg*s,
    mesh:mesh,mat:mat,baseCol:col,baseY:y,alert:false,cool:1+Math.random(),ph:Math.random()*6,hit:0,hr:type==='boss'?1.5:(type==='brute'?1.0:0.7)};
  enemies.push(e);
}

function addPickup(type,x,z){
  let mesh;
  if(type==='hp') mesh=new THREE.Mesh(new THREE.SphereGeometry(0.35,14,12),new THREE.MeshStandardMaterial({color:0x33ff77,emissive:0x22cc55,emissiveIntensity:0.9}));
  else if(type==='ammo') mesh=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.35,0.35),new THREE.MeshStandardMaterial({color:0xffd23a,emissive:0xcc9a10,emissiveIntensity:0.8}));
  else mesh=new THREE.Mesh(new THREE.OctahedronGeometry(0.3),new THREE.MeshStandardMaterial({color:0x44e0ff,emissive:0x1fa8d0,emissiveIntensity:1}));
  mesh.position.set(x,0.9,z); levelGroup.add(mesh);
  pickups.push({type:type,x:x,z:z,mesh:mesh,ph:Math.random()*6});
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
  if(state!=='playing') return;
  P.hp-=a; flashA=Math.min(0.55,flashA+0.12+a*0.01);
  if(P.hp<=0){
    P.hp=0; state='dead'; saveBest(); beep(160,0.6,'sawtooth',0.08,-100);
    showOverlay('YOU DIED','Reached level '+level+' &nbsp;·&nbsp; Score '+P.score+' &nbsp;·&nbsp; Kills '+P.kills+'<br>Best score: <b>'+best+'</b><br><br>Press <b>R</b> or click to try again');
  }
}
function killEnemy(e){
  levelGroup.remove(e.mesh);
  enemies.splice(enemies.indexOf(e),1);
  P.kills++; killsThisLevel++;
  P.score+= e.type==='boss'?1000:(e.type==='brute'?250:(e.type==='shooter'?120:100));
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
  if(P.ammo<=0){ beep(90,0.08,'square',0.04); P.cool=0.25; return; }
  P.ammo--; P.cool=0.17; muzzle=0.06; recoil=0.12;
  beep(780,0.09,'square',0.05,-500);
  const dx=-Math.sin(P.yaw), dz=-Math.cos(P.yaw);
  let hitE=null, end=40;
  for(let t=0.4;t<40;t+=0.25){
    const x=P.x+dx*t, z=P.z+dz*t;
    if(solid(x,z)){ end=t; break; }
    for(const e of enemies){
      if(Math.hypot(e.x-x,e.z-z)<e.hr){ hitE=e; end=t; break; }
    }
    if(hitE) break;
  }
  const rx=Math.cos(P.yaw), rz=-Math.sin(P.yaw);
  tracer(P.x+rx*0.3+dx*0.6,1.4,P.z+rz*0.3+dz*0.6, P.x+dx*end,1.5,P.z+dz*end);
  if(hitE){
    const crit=Math.random()<0.1, dmg=crit?4:2;
    hitE.hp-=dmg; hitE.hit=0.1; hitE.alert=true;
    burst(P.x+dx*end,1.4,P.z+dz*end,0xffffff,5,3);
    if(hitE.hp<=0) killEnemy(hitE); else beep(220,0.05,'triangle',0.05);
  } else {
    burst(P.x+dx*end,1.4,P.z+dz*end,0xffcc66,4,2);
  }
}

// ---------- update ----------
function update(dt){
  time+=dt;
  P.cool=Math.max(0,P.cool-dt);
  muzzle=Math.max(0,muzzle-dt); recoil=Math.max(0,recoil-dt*0.9);
  // input
  const k=keys;
  const f=((k.KeyW||k.ArrowUp)?1:0)-((k.KeyS||k.ArrowDown)?1:0);
  const s=(k.KeyD?1:0)-(k.KeyA?1:0);
  const turn=((k.ArrowLeft||k.KeyQ)?1:0)-((k.ArrowRight||k.KeyE)?1:0);
  P.yaw+=turn*2.4*dt;
  const sp=(k.ShiftLeft||k.ShiftRight?9:6)*dt;
  let mx=-Math.sin(P.yaw)*f+Math.cos(P.yaw)*s, mz=-Math.cos(P.yaw)*f-Math.sin(P.yaw)*s;
  const ml=Math.hypot(mx,mz);
  if(ml>0){ mx=mx/ml*sp; mz=mz/ml*sp; moveEnt(P,mx,mz,P.r); walkT+=dt; }
  if(k.Space||k.KeyF||k.mouse) shoot();

  // enemies
  for(const e of enemies){
    const dx=P.x-e.x, dz=P.z-e.z, d=Math.hypot(dx,dz)||0.001;
    const visible=d<22&&los(e.x,e.z,P.x,P.z);
    if(!e.alert&&visible&&d<20) e.alert=true;
    e.mesh.position.set(e.x,e.baseY+Math.sin(time*3+e.ph)*0.15,e.z);
    e.mesh.rotation.y+=dt*1.6; e.mesh.rotation.x+=dt*0.7;
    if(e.hit>0){ e.hit-=dt; e.mat.emissive.set(0xffffff); e.mat.emissiveIntensity=1.2; }
    else { e.mat.emissive.set(e.baseCol); e.mat.emissiveIntensity=e.alert?0.9:0.35; }
    if(!e.alert) continue;
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
      else if(p.type==='ammo'){ P.ammo+=25; toast('+25 ammo',900); }
      else { P.score+=50; toast('+50',700); }
      beep(900,0.1,'sine',0.05,300);
      levelGroup.remove(p.mesh); pickups.splice(i,1);
    }
  }
  // fx
  for(let i=fx.length-1;i>=0;i--){
    const f2=fx[i]; f2.life-=dt;
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
  } else if(!portalOpen&&Math.hypot(pp[0]-P.x,pp[1]-P.z)<1.8){
    toast('Sealed. Kill '+(Math.ceil(totalEnemies*0.5)-killsThisLevel)+' more enemies.',1200);
  }
  // explore
  const pcx=Math.floor(P.x/CELL), pcz=Math.floor(P.z/CELL);
  for(let y=pcz-3;y<=pcz+3;y++) for(let x=pcx-3;x<=pcx+3;x++)
    if(x>=0&&y>=0&&x<GW&&y<GH&&(x-pcx)*(x-pcx)+(y-pcz)*(y-pcz)<=10) explored[y*GW+x]=1;
}

function render(){
  camera.position.set(P.x,1.6+Math.sin(walkT*10)*0.045,P.z);
  camera.rotation.y=P.yaw;
  torch.position.set(P.x,2.0,P.z);
  torch.intensity=1.35+Math.sin(time*13)*0.08+Math.random()*0.06+(muzzle>0?2.2:0);
  gun.position.z=-0.6+recoil; gun.rotation.x=recoil*0.8;
  flashA=Math.max(0,flashA-0.02);
  flash.style.opacity=flashA;
  renderer.render(scene,camera);
  // HUD
  hud.innerHTML='<b>Level '+level+'</b> &nbsp; Score '+P.score+' &nbsp; <span style="opacity:.7">Best '+Math.max(best,P.score)+'</span><br>Kills '+killsThisLevel+'/'+totalEnemies+
    ' &nbsp; Ammo <b style="color:'+(P.ammo<8?'#ff6b6b':'#ffd23a')+'">'+P.ammo+'</b><br>Portal: '+
    (portalOpen?'<span style="color:#33e0ff">OPEN</span>':'<span style="color:#ff5566">sealed</span>');
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
function showOverlay(title,html){
  ov.innerHTML='<div style="font-size:30px;font-weight:bold;margin-bottom:8px">'+title+'</div><div style="font-size:14px;line-height:1.6">'+html+'</div>';
  ov.style.display='flex';
}
function hideOverlay(){ ov.style.display='none'; }
function newGame(){
  level=1; P.hp=P.maxhp=100; P.ammo=60; P.score=0; P.kills=0; P.cool=0; flashA=0;
  buildLevel(); state='playing'; paused=false; hideOverlay();
  toast('Find the portal. Kill half the dungeon to open it.',3000);
}
const HELP='<b>W A S D</b> move &nbsp; <b>← →</b> or <b>Q E</b> turn &nbsp; <b>Shift</b> sprint<br><b>Space</b> / <b>F</b> / left-click fire &nbsp; <b>hold right-click + drag</b> to look &nbsp; <b>P</b> pause<br>Kill half the enemies to open the cyan portal, then reach it.<br><br><b>Click to play</b>';
showOverlay('🏰 DEPTHS 3D <span style="font-size:13px;opacity:.6">v'+VERSION+'</span>',HELP+'<br><span style="opacity:.6">Best score: '+best+'</span>');

function activate(){
  wrap.focus();
  if(!actx){ try{ actx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} }
  if(state==='ready'||state==='dead') newGame();
  else if(paused){ paused=false; hideOverlay(); }
}
wrap.addEventListener('mousedown',function(ev){
  if(ev.button===2){ keys.look=true; ev.preventDefault(); return; }
  if(state==='playing'&&!paused) keys.mouse=true; else activate();
  if(state==='playing'&&!paused){
    wrap.focus();
    try{
      if(document.pointerLockElement!==renderer.domElement&&renderer.domElement.requestPointerLock){
        const pr=renderer.domElement.requestPointerLock();
        if(pr&&pr.catch) pr.catch(function(){});
      }
    }catch(e){}
  }
});
window.addEventListener('mouseup',function(ev){ if(ev.button===2) keys.look=false; else keys.mouse=false; });
wrap.addEventListener('contextmenu',function(ev){ev.preventDefault();});
wrap.addEventListener('mousemove',function(ev){
  if((keys.look||document.pointerLockElement===renderer.domElement)&&state==='playing'&&!paused) P.yaw-=ev.movementX*0.0045;
});
wrap.addEventListener('keydown',function(ev){
  keys[ev.code]=true;
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(ev.code)>=0) ev.preventDefault();
  if(ev.code==='KeyR'&&(state==='dead'||state==='ready')) activate();
  if((ev.code==='KeyP'||ev.code==='Escape')&&state==='playing'){
    if(paused){ paused=false; hideOverlay(); }
    else { paused=true; showOverlay('PAUSED','Press <b>P</b> or click to resume'); }
  }
});
wrap.addEventListener('keyup',function(ev){ keys[ev.code]=false; });
wrap.addEventListener('blur',function(){
  for(const c in keys) keys[c]=false;
  if(state==='playing'&&!paused){ paused=true; showOverlay('PAUSED','Click to resume'); }
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

if(window.THREE){ start(); }
else {
  const s=document.createElement('script');
  s.src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
  s.onload=start;
  s.onerror=function(){ document.getElementById('dd3d-root').innerHTML='<div style="padding:20px;color:#f88">Could not load three.js from the CDN. Check your internet connection and re-run this cell.</div>'; };
  document.head.appendChild(s);
}
})();
