from IPython.display import display, HTML
from google.colab import output
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
GAME_HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DEPTHS 3D v6.0.0 — The Bestiary Expansion</title><style>html,body{margin:0;padding:0;min-height:100%;background:#09080c;color:#ddd;font-family:system-ui,sans-serif}body{display:flex;justify-content:center;align-items:center;min-height:100vh}#dd3d-root{box-shadow:0 0 40px #07070a;width:min(100vw,800px)!important;max-height:min(100vh,700px)}*{box-sizing:border-box}</style></head><body><div id="dd3d-root" tabindex="0" style="position:relative;width:800px;max-width:100%;aspect-ratio:8/7;background:#000;overflow:hidden;outline:none;font-family:Segoe UI,Arial,sans-serif;color:#fff;user-select:none">
<div class="hud" style="position:absolute;left:10px;top:8px;font-size:14px;text-shadow:0 1px 3px #000;line-height:1.5;pointer-events:none"></div>
<canvas class="mm" width="130" height="130" style="position:absolute;right:8px;top:8px;border:1px solid #556;background:rgba(0,0,0,.55);border-radius:6px;pointer-events:none"></canvas>
<div style="position:absolute;left:10px;bottom:12px;width:220px;height:12px;background:#222;border:1px solid #555;border-radius:6px;overflow:hidden;pointer-events:none"><div class="hpb" style="height:100%;width:100%;background:#3ddc84"></div></div>
<div class="dd-crosshair" style="position:absolute;left:50%;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;pointer-events:none"><div style="position:absolute;left:7px;top:0;width:2px;height:16px;background:#e8f7ff;box-shadow:0 0 3px #071323"></div><div style="position:absolute;left:0;top:7px;width:16px;height:2px;background:#e8f7ff;box-shadow:0 0 3px #071323"></div></div>
<div class="flash" style="position:absolute;left:0;top:0;right:0;bottom:0;background:#f00;opacity:0;pointer-events:none"></div>
<div class="toast" style="position:absolute;left:0;right:0;bottom:44px;text-align:center;font-size:15px;text-shadow:0 1px 4px #000;opacity:0;transition:opacity .3s;pointer-events:none"></div>
<div class="ov" style="position:absolute;left:0;top:0;right:0;bottom:0;background:rgba(5,5,12,.72);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;cursor:pointer"></div>
</div>
<script>
(function(){
function start(){
(function(root){
'use strict';
const THREE=root.THREE;
if(!THREE)throw Error('Depths Bestiary requires Three.js r128 or newer');
const TYPES=['brute','crawler','imp','wraith','necromancer','gargoyle'];
const PIXEL_PALETTES={
 brute:['#a49da3','#89828a','#777179','#65585f','#493c41','#2b262b'],
 crawler:['#b3a7a9','#918387','#76676d','#604e54','#493c43','#29252a'],
 imp:['#bd939e','#a57586','#875567','#663d51','#4d2c38','#281e27'],
 wraith:['#a6a3a7','#817b82','#676169','#514b53','#38343b','#211d25'],
 necromancer:['#211a22','#31212b','#422c36','#55313c','#67424b','#81616a'],
 gargoyle:['#b5a7a9','#8c7e80','#73676c','#5d5056','#42383f','#272228']
};
const SPEC={
 brute:{name:'FLESH BRUTE',height:2.7,baseY:1.35,headRatio:.17,armRatio:.59,legRatio:.34,shoulderRatio:.84,posture:16,
   forms:[[0,-.19,.29,.74,.68,.54],[0,.46,.00,.84,.44,.52],[-.66,.60,.02,.36,.35,.42],[.66,.60,.02,.36,.35,.42],[0,.89,.22,.27,.23,.28],[0,-.71,.02,.48,.31,.36]],
   anchors:{pelvis:[0,-.59,0],spine:[0,.05,0],chest:[0,.56,0],neck:[0,.79,.12],head:[0,.99,.25],
     Lshoulder:[-.70,.62,.02],Lelbow:[-.86,-.09,.14],Lwrist:[-.82,-.70,.30],Rshoulder:[.70,.62,.02],Relbow:[.86,-.09,.14],Rwrist:[.82,-.70,.30],
     Lhip:[-.38,-.69,0],Lknee:[-.51,-1.02,.07],Lfoot:[-.52,-1.28,.16],Rhip:[.38,-.69,0],Rknee:[.51,-1.02,.07],Rfoot:[.52,-1.28,.16]},
   limbRadius:{arm:.25,leg:.29},jaw:[0,.82,.43],eye:[.135,1.02,.47,.048],skin:'#736467'},
 crawler:{name:'CRYPT CRAWLER',height:.9,length:2.03,baseY:.45,headRatio:.19,armRatio:.89,legRatio:.82,shoulderRatio:.71,posture:74,
   forms:[[0,-.02,-.21,.37,.23,.78],[0,.10,-.49,.26,.27,.44],[0,-.10,.67,.23,.19,.27],[0,-.045,.31,.25,.21,.36]],
   anchors:{pelvis:[0,-.08,-.58],spine:[0,.06,-.25],chest:[0,.07,.28],neck:[0,-.055,.52],head:[0,-.08,.72],
     Lshoulder:[-.32,.04,.36],Lelbow:[-.70,-.23,.66],Lwrist:[-.91,-.39,.96],Rshoulder:[.32,.04,.36],Relbow:[.70,-.23,.66],Rwrist:[.91,-.39,.96],
     Lhip:[-.27,-.13,-.58],Lknee:[-.66,-.19,-.70],Lfoot:[-.80,-.41,-.85],Rhip:[.27,-.13,-.58],Rknee:[.66,-.19,-.70],Rfoot:[.80,-.41,-.85]},
   limbRadius:{arm:.092,leg:.105},jaw:[0,-.20,.88],eye:[.115,-.012,.92,.035],skin:'#695357'},
 imp:{name:'FLESH IMP',height:1.2,baseY:.60,headRatio:.43,armRatio:.51,legRatio:.36,shoulderRatio:.46,posture:41,
   forms:[[0,-.27,-.11,.35,.36,.32],[0,-.04,.05,.31,.35,.26],[0,.27,.27,.45,.40,.42],[0,.39,.30,.44,.39,.41]],
   anchors:{pelvis:[0,-.35,-.12],spine:[0,-.04,-.06],chest:[0,.11,.10],neck:[0,.23,.19],head:[0,.32,.29],
     Lshoulder:[-.30,.05,.06],Lelbow:[-.37,-.26,.25],Lwrist:[-.41,-.49,.41],Rshoulder:[.30,.05,.06],Relbow:[.37,-.26,.25],Rwrist:[.41,-.49,.41],
     Lhip:[-.22,-.43,-.16],Lknee:[-.33,-.55,.08],Lfoot:[-.36,-.57,.31],Rhip:[.22,-.43,-.16],Rknee:[.33,-.55,.08],Rfoot:[.36,-.57,.31]},
   limbRadius:{arm:.095,leg:.14},jaw:[0,.05,.65],eye:[.237,.39,.623,.141],skin:'#873e55'},
 wraith:{name:'GAUNT HOODED WRAITH',height:2.1,baseY:1.06,headRatio:.13,armRatio:.74,legRatio:.42,shoulderRatio:.34,posture:23,
   forms:[[0,-.16,-.05,.24,.65,.25],[0,.55,-.03,.29,.28,.26],[0,.80,.18,.24,.30,.22],[0,-.61,-.12,.18,.35,.20]],
   anchors:{pelvis:[0,-.58,-.12],spine:[0,-.12,-.06],chest:[0,.45,-.02],neck:[0,.68,.11],head:[0,.86,.20],
     Lshoulder:[-.28,.45,-.01],Lelbow:[-.43,-.21,.13],Lwrist:[-.47,-.81,.30],Rshoulder:[.28,.45,-.01],Relbow:[.43,-.21,.13],Rwrist:[.47,-.81,.30],
     Lhip:[-.15,-.58,-.14],Lknee:[-.18,-.82,-.13],Lfoot:[-.18,-1.02,-.10],Rhip:[.15,-.58,-.14],Rknee:[.18,-.82,-.13],Rfoot:[.18,-1.02,-.10]},
   limbRadius:{arm:.064,leg:.085},jaw:[0,.65,.39],eye:[.096,.91,.406,.048],skin:'#575459'},
 necromancer:{name:'NECROMANCER',height:2.4,baseY:1.2,headRatio:.13,armRatio:.58,legRatio:.47,shoulderRatio:.42,posture:9,
   forms:[[0,-.25,-.03,.30,.70,.32],[0,.43,-.02,.35,.27,.34],[0,.77,.05,.32,.36,.31]],
   anchors:{pelvis:[0,-.68,0],spine:[0,-.05,0],chest:[0,.50,0],neck:[0,.75,.10],head:[0,.93,.16],
     Lshoulder:[-.34,.46,0],Lelbow:[-.47,.03,.19],Lwrist:[-.61,.14,.52],Rshoulder:[.34,.46,0],Relbow:[.50,.10,.10],Rwrist:[.60,-.09,.31],
     Lhip:[-.18,-.68,0],Lknee:[-.19,-.99,0],Lfoot:[-.18,-1.16,.13],Rhip:[.18,-.68,0],Rknee:[.19,-.99,0],Rfoot:[.18,-1.16,.13]},
   limbRadius:{arm:.10,leg:.12},jaw:[0,.73,.38],eye:[.10,.97,.44,.040],skin:'#74686d'},
 gargoyle:{name:'WINGED GARGOYLE',height:1.4,wingspan:4,baseY:1.16,headRatio:.22,armRatio:.61,legRatio:.42,shoulderRatio:.58,posture:43,
   forms:[[0,-.10,-.17,.39,.39,.49],[0,.28,.11,.40,.34,.31],[0,.49,.35,.27,.29,.31]],
   anchors:{pelvis:[0,-.44,-.27],spine:[0,-.05,-.15],chest:[0,.31,.10],neck:[0,.45,.27],head:[0,.55,.39],
     Lshoulder:[-.42,.21,.07],Lelbow:[-.69,-.28,.36],Lwrist:[-.75,-.80,.60],Rshoulder:[.42,.21,.07],Relbow:[.69,-.28,.36],Rwrist:[.75,-.80,.60],
     Lhip:[-.25,-.43,-.27],Lknee:[-.49,-.75,.04],Lfoot:[-.56,-1.06,.40],Rhip:[.25,-.43,-.27],Rknee:[.49,-.75,.04],Rfoot:[.56,-1.06,.40]},
   limbRadius:{arm:.12,leg:.19},jaw:[0,.34,.66],eye:[.134,.57,.66,.049],skin:'#595960'}
};
const BONE_PARENT={pelvis:null,spine:'pelvis',chest:'spine',neck:'chest',head:'neck',
 Lshoulder:'chest',Lelbow:'Lshoulder',Lwrist:'Lelbow',Rshoulder:'chest',Relbow:'Rshoulder',Rwrist:'Relbow',
 Lhip:'pelvis',Lknee:'Lhip',Lfoot:'Lknee',Rhip:'pelvis',Rknee:'Rhip',Rfoot:'Rknee'};
const BONE_NAMES=Object.keys(BONE_PARENT);
const GEOMETRY=new Map(),MATERIALS=new Map(),WING_GEOMETRY=new Map();
function clamp(x,a,b){return Math.max(a,Math.min(b,x));}
function smin(a,b,k){const h=Math.max(k-Math.abs(a-b),0)/k;return Math.min(a,b)-h*h*k*.25;}
function field(plan,x,y,z){let v=99;const f=plan.forms;for(let i=0;i<f.length;i++){
 const p=f[i],dx=(x-p[0])/p[3],dy=(y-p[1])/p[4],dz=(z-p[2])/p[5],d=(Math.hypot(dx,dy,dz)-1)*Math.min(p[3],p[4],p[5]);
 v=i?smin(v,d,plan===SPEC.imp?.18:.22):d;
}const folds=Math.sin(y*18+x*6+Math.sin(z*9)*2)*Math.sin(x*13+z*7)*.009;
const pores=Math.sin(x*44+y*29)*Math.sin(z*37-y*17)*.005;
return v+folds+pores;}
function newBuilder(){return {p:[],i:[],uv:[],idx:[],wg:[]};}
function vertex(b,x,y,z,u,v,weights){const id=b.p.length/3;b.p.push(x,y,z);b.uv.push(u,v);b.wg.push(weights);return id;}
function tri(b,a,c,d){b.idx.push(a,c,d);}
function skinFromPoint(plan,x,y,z){
 let n0=0,n1=0,n2=0,n3=0,w0=-1,w1=-1,w2=-1,w3=-1;
 for(let j=0;j<BONE_NAMES.length;j++){
  const p=plan.anchors[BONE_NAMES[j]],dx=x-p[0],dy=y-p[1],dz=z-p[2];
  const d=dx*dx+dy*dy+dz*dz+.018;
  const w=1/(d*d*(j===4||j===7||j===10||j===13||j===16?1.18:1));
  if(w>w0){w3=w2;n3=n2;w2=w1;n2=n1;w1=w0;n1=n0;w0=w;n0=j;}
  else if(w>w1){w3=w2;n3=n2;w2=w1;n2=n1;w1=w;n1=j;}
  else if(w>w2){w3=w2;n3=n2;w2=w;n2=j;}
  else if(w>w3){w3=w;n3=j;}
 }
 const inv=1/(w0+w1+w2+w3);
 return [[n0,w0*inv],[n1,w1*inv],[n2,w2*inv],[n3,w3*inv]];
}
function addSculpt(plan,b,res){const bounds=[100,100,100,-100,-100,-100];for(const f of plan.forms)for(let j=0;j<3;j++){
 bounds[j]=Math.min(bounds[j],f[j]-f[j+3]-.08);bounds[j+3]=Math.max(bounds[j+3],f[j]+f[j+3]+.08);
}
 const nx=res,ny=Math.floor(res*1.05),nz=Math.floor(res*.90),SX=nx+1,SY=ny+1,SZ=nz+1;
 const sx=(bounds[3]-bounds[0])/nx,sy=(bounds[4]-bounds[1])/ny,sz=(bounds[5]-bounds[2])/nz;
 const id=(x,y,z)=>(z*SY+y)*SX+x;
 const samples=new Float32Array(SX*SY*SZ);
 for(let z=0;z<SZ;z++)for(let y=0;y<SY;y++)for(let x=0;x<SX;x++)samples[id(x,y,z)]=field(plan,bounds[0]+x*sx,bounds[1]+y*sy,bounds[2]+z*sz);
 const vertices=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];
 const tetra=[[0,5,1,6],[0,1,2,6],[0,2,3,6],[0,3,7,6],[0,7,4,6],[0,4,5,6]];
 const e=[[0,1],[1,2],[2,0],[0,3],[1,3],[2,3]];
 const facets=[[],[[0,3,2]],[[0,1,4]],[[1,4,2],[2,4,3]],[[1,2,5]],[[0,3,5],[0,5,1]],[[0,2,5],[0,5,4]],[[3,4,5]],[[3,5,4]],[[0,4,5],[0,5,2]],[[0,1,5],[0,5,3]],[[1,5,2]],[[2,3,4],[1,2,4]],[[0,4,1]],[[0,2,3]],[]];
 for(let z=0;z<nz;z++)for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){
  const vv=[],dd=[];let lo=100,hi=-100;
  for(let j=0;j<8;j++){const a=vertices[j],gx=x+a[0],gy=y+a[1],gz=z+a[2];vv[j]=[bounds[0]+gx*sx,bounds[1]+gy*sy,bounds[2]+gz*sz];dd[j]=samples[id(gx,gy,gz)];lo=Math.min(lo,dd[j]);hi=Math.max(hi,dd[j]);}
  if(lo>0||hi<0)continue;
  for(let t=0;t<6;t++){
   const tt=tetra[t],v=tt.map(i=>vv[i]),d=tt.map(i=>dd[i]);let mask=0;for(let q=0;q<4;q++)if(d[q]<0)mask|=(1<<q);
   if(!mask||mask===15)continue;
   const interp=e.map(([a,c])=>{if((d[a]<0)===(d[c]<0))return null;const f=d[a]/(d[a]-d[c]);return [v[a][0]+(v[c][0]-v[a][0])*f,v[a][1]+(v[c][1]-v[a][1])*f,v[a][2]+(v[c][2]-v[a][2])*f];});
   for(const face of facets[mask]){
    const p=face.map(q=>interp[q]);if(p.some(a=>!a))continue;
    const u=[p[1][0]-p[0][0],p[1][1]-p[0][1],p[1][2]-p[0][2]];
    const v=[p[2][0]-p[0][0],p[2][1]-p[0][1],p[2][2]-p[0][2]];
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
    const cc=[(p[0][0]+p[1][0]+p[2][0])/3,(p[0][1]+p[1][1]+p[2][1])/3,(p[0][2]+p[1][2]+p[2][2])/3];
    const cy=plan===SPEC.crawler?-0.03:0;
    if(n[0]*cc[0]+n[1]*(cc[1]-cy)+n[2]*cc[2]<0){const tmp=p[1];p[1]=p[2];p[2]=tmp;}
    const off=b.p.length/3;
    for(const [px,py,pz] of p)vertex(b,px,py,pz,.5+Math.atan2(pz,px)/(Math.PI*2),(py-bounds[1])/(bounds[4]-bounds[1]),skinFromPoint(plan,px,py,pz));
    tri(b,off,off+1,off+2);
   }
  }
 }
}
function addLoft(b,plan,first,last,r0,r1,res){
 const A=plan.anchors[first],B=plan.anchors[last],length=Math.hypot(B[0]-A[0],B[1]-A[1],B[2]-A[2]);
 const dir=new THREE.Vector3(B[0]-A[0],B[1]-A[1],B[2]-A[2]).normalize();
 const u=new THREE.Vector3(1,0,0);if(Math.abs(dir.dot(u))>.92)u.set(0,0,1);
 u.addScaledVector(dir,-u.dot(dir)).normalize();const v=new THREE.Vector3().crossVectors(dir,u).normalize();
 const idxA=BONE_NAMES.indexOf(first),idxB=BONE_NAMES.indexOf(last),rings=res>20?7:4,sides=res>20?11:7;
 const start=b.p.length/3;
 for(let j=0;j<=rings;j++){
  const t=j/rings;let radius=(r0+(r1-r0)*t)*(1+.19*Math.sin(Math.PI*t));
  for(let k=0;k<=sides;k++){
   const ang=k/sides*Math.PI*2,wrinkle=1+.055*Math.sin(ang*5+t*17),ct=Math.cos(ang),st=Math.sin(ang);
   const x=A[0]+(B[0]-A[0])*t+(u.x*ct+v.x*st)*radius*wrinkle;
   const y=A[1]+(B[1]-A[1])*t+(u.y*ct+v.y*st)*radius*wrinkle;
   const z=A[2]+(B[2]-A[2])*t+(u.z*ct+v.z*st)*radius*wrinkle;
   vertex(b,x,y,z,k/sides,t,[[idxA,1-t],[idxB,t],[0,0],[0,0]]);
  }
 }
 for(let j=0;j<rings;j++)for(let k=0;k<sides;k++){
  const a=start+j*(sides+1)+k,c=a+sides+1;tri(b,a,c,a+1);tri(b,a+1,c,c+1);
 }
}
function createGeometry(plan,res){const b=newBuilder();addSculpt(plan,b,res);
 const a=plan.anchors,s=plan.limbRadius;
 for(const side of ['L','R']){
  addLoft(b,plan,side+'shoulder',side+'elbow',s.arm,s.arm*.74,res);addLoft(b,plan,side+'elbow',side+'wrist',s.arm*.77,s.arm*.49,res);
  if(plan===SPEC.wraith||plan===SPEC.necromancer)continue;
  addLoft(b,plan,side+'hip',side+'knee',s.leg,s.leg*.70,res);addLoft(b,plan,side+'knee',side+'foot',s.leg*.73,s.leg*.46,res);
 }
 const g=new THREE.BufferGeometry(),idx=new Float32Array(b.wg.length*4),weights=new Float32Array(b.wg.length*4);
 for(let j=0;j<b.wg.length;j++)for(let k=0;k<4;k++){idx[j*4+k]=b.wg[j][k][0];weights[j*4+k]=b.wg[j][k][1];}
 g.setAttribute('position',new THREE.Float32BufferAttribute(b.p,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(b.uv,2));
 g.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(idx,4));g.setAttribute('skinWeight',new THREE.Float32BufferAttribute(weights,4));
 g.setIndex(b.idx);g.computeVertexNormals();g.computeBoundingSphere();
 return g;
}
function geometries(type){if(GEOMETRY.has(type))return GEOMETRY.get(type);const plan=SPEC[type];
 const t0=performance.now();const values=[24,15,5].map(n=>createGeometry(plan,n));
 const stats={ms:Math.round(performance.now()-t0),triangles:values.map(g=>g.index.count/3)};
 const entry={geoms:values,stats};GEOMETRY.set(type,entry);return entry;
}
function raster(type){if(MATERIALS.has(type))return MATERIALS.get(type);const palette=PIXEL_PALETTES[type];
 const n=192,c=document.createElement('canvas'),b=document.createElement('canvas'),r=document.createElement('canvas');
 for(const v of [c,b,r]){v.width=n;v.height=n;}
 const C=c.getContext('2d'),B=b.getContext('2d'),R=r.getContext('2d');
 const a=C.createImageData(n,n),bt=B.createImageData(n,n),rt=R.createImageData(n,n);
 const hash=(x,y)=>{let v=Math.imul(x+1337,374761393)^Math.imul(y+2718,668265263)^type.length;v=Math.imul(v^(v>>>13),1274126177);return ((v^(v>>>16))>>>0)/4294967296;};
 const colors=palette.map(p=>[parseInt(p.slice(1,3),16),parseInt(p.slice(3,5),16),parseInt(p.slice(5),16)]);
 if(type==='necromancer'){
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const t=(Math.sin(x*.069+2*Math.sin(y*.036))+1)*.5*.56+hash(x>>2,y>>2)*.44;
  const k=Math.min(4,Math.floor(t*5)),f=t*5-k,shade=colors[k].map((q,z)=>q*(1-f)+colors[k+1][z]*f);
  const vein=Math.pow(Math.max(0,Math.sin(x*.097+Math.sin(y*.12)*3)),18)*12;
  const scar=(Math.abs(Math.sin(y*.12+Math.sin(x*.07)*4))>.985&&hash(x>>4,y>>4)>.6)?22:0;
  const off=(y*n+x)*4;
  for(let z=0;z<3;z++)a.data[off+z]=clamp(shade[z]+(hash(x,y)-.5)*22-(z===0?0:vein)-scar,5,230);
  a.data[off+3]=255;
  const relief=clamp(128+27*(hash(x,y)-.5)+18*Math.sin(x*.17+y*.22)-scar,12,243);
  bt.data[off]=bt.data[off+1]=bt.data[off+2]=relief;bt.data[off+3]=255;
  const gloss=type==='imp'||type==='crawler'?133:190;
  const rv=clamp(gloss+28*(hash(x>>2,y>>2)-.5)-scar,50,240);
  rt.data[off]=rt.data[off+1]=rt.data[off+2]=rv;rt.data[off+3]=255;
 }
 }else{
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const block=hash(x>>2,y>>2),fine=hash(x,y),fiber=Math.sin(x*.13+y*.075+Math.sin(y*.045)*4);
  const macro=Math.sin(x*.037+Math.sin(y*.042)*2.3)*Math.cos(y*.032+Math.sin(x*.053)*1.5);
  const t=clamp(.47+.24*macro+.18*(block-.5)+.16*(fine-.5),0,.999);
  const k=Math.min(4,Math.floor(t*5)),f=t*5-k,shade=colors[k].map((q,z)=>q*(1-f)+colors[k+1][z]*f);
  const crease=Math.sin(y*.091+Math.sin(x*.046)*5.2+x*.018);
  const scar=(Math.abs(crease)<.026&&hash(x>>4,y>>4)>.47)?(type==='brute'?31:15):0;
  const vein=Math.pow(Math.max(0,Math.sin(x*.11+Math.sin(y*.061)*3.2)),24)*(type==='imp'?28:15);
  const bruises=Math.max(0,Math.sin(x*.046+y*.014+Math.sin(y*.022)*2))*Math.max(0,Math.cos(y*.058-x*.019))*12;
  const pores=(fine-.5)*17+(hash(x>>1,y>>1)-.5)*13;
  const off=(y*n+x)*4;
  for(let z=0;z<3;z++){
   let pigment=shade[z]+pores+macro*9-scar+(z===0?bruises*.72:-(bruises*.38+vein));
   if(type==='imp'&&z===0)pigment+=9;
   a.data[off+z]=clamp(pigment,5,224);
  }
  a.data[off+3]=255;
  const relief=clamp(128+27*(fine-.5)+10*fiber+15*macro-scar*.63+vein*.52,12,243);
  bt.data[off]=bt.data[off+1]=bt.data[off+2]=relief;bt.data[off+3]=255;
  const gloss=type==='imp'?105:type==='crawler'?140:type==='brute'?184:type==='wraith'?202:type==='gargoyle'?197:190;
  const rv=clamp(gloss+27*(block-.5)+15*Math.abs(macro)-scar*.8,48,242);
  rt.data[off]=rt.data[off+1]=rt.data[off+2]=rv;rt.data[off+3]=255;
 }
 }
 C.putImageData(a,0,0);B.putImageData(bt,0,0);R.putImageData(rt,0,0);
 const tex=canvas=>{const t=new THREE.CanvasTexture(canvas);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;return t;};
 const mat=new THREE.MeshStandardMaterial({map:tex(c),bumpMap:tex(b),bumpScale:.055,roughnessMap:tex(r),roughness:1,color:0xffffff,metalness:0,vertexColors:false,side:THREE.FrontSide});
 MATERIALS.set(type,mat);return mat;
}
function createSkeleton(plan,group){const bones={},world=plan.anchors;
 for(const name of BONE_NAMES)bones[name]=new THREE.Bone(),bones[name].name=name;
 for(const name of BONE_NAMES){const parent=BONE_PARENT[name],p=world[name];
  if(parent){const q=world[parent];bones[name].position.set(p[0]-q[0],p[1]-q[1],p[2]-q[2]);bones[parent].add(bones[name]);}
  else {bones[name].position.set(...p);group.add(bones[name]);}
 }
 group.updateMatrixWorld(true);const skeleton=new THREE.Skeleton(BONE_NAMES.map(n=>bones[n]));
 skeleton.calculateInverses();return {skeleton,bones};
}
const MAT={};
function std(id,color,metal=0,rough=.74){const key=id+'|'+color;if(!MAT[key])MAT[key]=new THREE.MeshStandardMaterial({color,metalness:metal,roughness:rough,side:THREE.DoubleSide});return MAT[key];}
const DETAILS_GEOMETRY=new Map();
function detailGeometry(key,create){let geo=DETAILS_GEOMETRY.get(key);if(!geo){geo=create();DETAILS_GEOMETRY.set(key,geo);}return geo;}
function bulb(parent,x,y,z,scale,material){const g=detailGeometry('sphere16',()=>new THREE.SphereGeometry(1,16,12));const m=new THREE.Mesh(g,material);m.position.set(x,y,z);m.scale.set(...scale);m.castShadow=true;parent.add(m);return m;}
function path(parent,pts,r,mat){const key='tube:'+r+':'+pts.map(p=>p.join(',')).join('|');const g=detailGeometry(key,()=>new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p))),Math.max(8,pts.length*5),r,7,false));const o=new THREE.Mesh(g,mat);parent.add(o);o.castShadow=true;return o;}
function cusp(parent,x,y,z,r,len,mat,rx=0,rz=0){const g=detailGeometry('cone7',()=>new THREE.ConeGeometry(1,1,7,3));const o=new THREE.Mesh(g,mat);o.scale.set(r,len,r);o.position.set(x,y,z);o.rotation.set(rx,0,rz);parent.add(o);return o;}
function polyPoint(pts,t){const m=pts.length-1;if(m<=0)return pts[0]||[0,0,0];const s=clamp(t,0,.999999)*m,i=Math.floor(s),f=s-i,a=pts[i],b=pts[Math.min(m,i+1)];return[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[2]+(b[2]-a[2])*f];}
function stitchScar(parent,pts,width,scarMat,stitchMat,count=0){const scar=path(parent,pts,width,scarMat);for(let i=0;i<count;i++){const p=polyPoint(pts,(i+.5)/Math.max(1,count));const knot=bulb(parent,p[0],p[1],p[2],[width*2.4,width*1.6,width*2.1],stitchMat);knot.castShadow=true;}return scar;}
function setBaseScale(obj){obj.userData.baseScale=obj.scale.clone();obj.userData.baseY=obj.position.y;return obj;}
function necroOpenHood(head,parts){
 const rows=[[-.19,.30,.36,.00],[-.10,.30,.37,.01],[.10,.27,.35,.025],[.29,.235,.31,.02],[.34,.215,.29,.02]];
 const segments=32,vertices=[],uv=[],ids=[];
 for(let r=0;r<rows.length;r++){
  const [z,rx,ry,cy]=rows[r];
  for(let i=0;i<=segments;i++){
   const a=i/segments*Math.PI*2,c=Math.cos(a),si=Math.sin(a),fold=1+.038*Math.sin(i*.94+r*.8);
   vertices.push(rx*c*fold,cy+ry*si*(1+.04*Math.sin(i*.47)),z+(.02*Math.sin(a*3+r)));
   uv.push(i/segments,r/(rows.length-1));
   if(r<rows.length-1&&i<segments){const k=r*(segments+1)+i;ids.push(k,k+segments+1,k+1,k+1,k+segments+1,k+segments+2);}
  }
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(ids);g.computeVertexNormals();
 const hood=new THREE.Mesh(g,std('necroCowlShell',0x201720,0,.95));hood.castShadow=true;hood.receiveShadow=true;head.add(hood);
 const dark=std('necroHoodInterior',0x09070c,0,.98),border=std('necroHoodStitchedHem',0x6c4351,.10,.68),edge=std('necroHoodGoldThread',0x8b6570,.27,.55);
 bulb(head,0,.03,-.095,[.215,.25,.22],dark);
 const rim=[];for(let i=0;i<=28;i++){const a=i/28*Math.PI*2;rim.push([.235*Math.cos(a),.02+.308*Math.sin(a),.355+.012*Math.cos(a*4)]);}
 const trim=path(head,rim,.018,border);parts.details.push(trim);
 const inner=[];for(let i=0;i<=25;i++){const a=i/25*Math.PI*2;inner.push([.205*Math.cos(a),.02+.285*Math.sin(a),.357+.007*Math.sin(a*2)]);}
 path(head,inner,.006,edge);
 // The upper hood casts a narrow shadow without covering the eyes and teeth.
 path(head,[[-.205,.23,.36],[-.10,.305,.382],[0,.32,.386],[.12,.295,.378],[.212,.21,.36]],.025,std('necroHoodBrow',0x241923));
 for(const s of [-1,1]){
  path(head,[[s*.23,.15,.29],[s*.27,.01,.27],[s*.255,-.14,.28],[s*.18,-.29,.305]],.022,border);
  const shred=clothStrip(head,'necromancer',s*.245,-.18,.44,std('necroHoodTail',0x281b28));
  shred.bone.position.y=-.13;parts.cloth.push(shred);
 }
 parts.hoodShell=hood;
}
function necroRobeShell(bones,parts){
 const root=bones.pelvis,segments=28,rings=12;
 const build=(offset,scale,colour)=>{
  const vertices=[],uv=[],indices=[],colors=[];
  for(let j=0;j<=rings;j++){
   const t=j/rings,y=-.50+t*1.55,rad=(.77*(1-t)+.30*t)*scale;
   for(let k=0;k<=segments;k++){
    const a=k/segments*Math.PI*2,fold=1+.10*Math.cos(a*11+offset)+.035*Math.sin(t*19+a*6+offset);
    const hem=(1-t)*(Math.sin(a*13+offset)*.07+Math.sin(a*7+offset)*.035);
    const x=rad*Math.sin(a)*fold,z=rad*Math.cos(a)*(.75+.12*Math.sin(a*3))+offset*.015;
    vertices.push(x,y+hem,z);uv.push(k/segments,t);
    const crease=(.58+.34*Math.cos(a*11+offset))*(.72+.28*t);
    colors.push(colour[0]*crease,colour[1]*crease,colour[2]*crease);
    if(j<rings&&k<segments){const n=j*(segments+1)+k;indices.push(n,n+1,n+segments+1,n+1,n+segments+2,n+segments+1);}
   }
  }
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));g.setIndex(indices);g.computeVertexNormals();
  const robe=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xffffff,vertexColors:true,roughness:.91,metalness:0,side:THREE.DoubleSide}));robe.castShadow=true;robe.receiveShadow=true;root.add(robe);return robe;
 };
 parts.robeShells.push(build(.6,1,[.39,.22,.27]));
 parts.robeShells.push(build(2.5,.91,[.26,.15,.21]));
 const collar=std('necroCollar',0x2b2029,0,.90);
 for(const s of [-1,1]){
  path(bones.chest,[[s*.24,.26,.04],[s*.47,.15,.0],[s*.49,-.09,.20],[s*.28,-.33,.32]],.057,collar);
  path(bones.chest,[[s*.17,.23,.22],[s*.25,.09,.35],[s*.23,-.22,.40]],.012,std('necroCollarTrim',0x9a6670,.23,.55));
 }
 const runeMat=new THREE.MeshBasicMaterial({color:0xb367ff,transparent:true,opacity:.69,depthWrite:false});
 parts.runeMat=runeMat;
 const rune=pts=>{const r=path(root,pts,.010,runeMat);parts.robeRunes.push(r);};
 // Three asymmetric rune marks and hem stitches float just above the robe surface.
 for(let i=0;i<4;i++){
  const y=.65-i*.22,z=.38+i*.045,x=(i%2?-.11:.12);
  rune([[x-.048,y+.07,z-.01],[x,y-.015,z+.022],[x+.052,y+.07,z-.01]]);
  rune([[x,y+.092,z],[x,y-.084,z+.014]]);
 }
 for(let i=0;i<8;i++){
  const x=(i-3.5)*.12;
  const xx=x*.75;
  rune([[xx,-.40,.60],[xx+.025,-.47,.62]]);
 }
 // Torso has genuine layered cloth panels, not a skin-coloured body painted flat.
}
function necroSkullCharm(parent,x,y,z,scale,parts){
 const g=new THREE.Group();g.position.set(x,y,z);g.scale.setScalar(scale);parent.add(g);
 const bone=std('necroBeltBone',0xa49b96,0,.68),voidMat=std('necroBeltSocket',0x161016,0,.94),aged=std('necroBeltTeeth',0xd2bdb1,0,.57);
 bulb(g,0,.045,0,[.105,.12,.085],bone);bulb(g,0,-.078,.038,[.073,.065,.063],bone);
 for(const s of [-1,1]){bulb(g,s*.052,.055,.081,[.037,.036,.012],voidMat);bulb(g,s*.040,-.032,.088,[.020,.022,.01],voidMat);}
 bulb(g,0,-.007,.101,[.020,.030,.011],voidMat);
 for(let i=0;i<5;i++){const tx=(i-2)*.025;bulb(g,tx,-.101,.098,[.010,.018,.009],aged);}
 parts.trophies.push(g);return g;
}
function necroCastingWisps(root,parts){
 const strand=std('necroWispStrand',0x623a7c,0,.60),flare=new THREE.MeshBasicMaterial({color:0xba6cff,transparent:true,opacity:.79,depthWrite:false});
 parts.wispMat=flare;
 for(let i=0;i<5;i++){
  const group=new THREE.Group();group.position.set(0,.13,.12);root.add(group);
  const a=i*Math.PI*2/5;
  path(group,[[.10*Math.cos(a),0,.07*Math.sin(a)],[.15*Math.cos(a+.45),.13,.11*Math.sin(a+.45)],[.11*Math.cos(a+1),.30,.17*Math.sin(a+1)]],.009,i%2?flare:strand);
  const tip=bulb(group,.11*Math.cos(a+1),.30,.17*Math.sin(a+1),[.025,.025,.025],flare);
  parts.wisps.push({group,tip,phase:i*1.2566});
 }
}
function headDetails(type,bones,parts){
 const plan=SPEC[type],head=bones.head,skull=std('bone',0x918a85,0,.74),dark=std('cavity',0x140d13,0,.92),ivory=std('ivory',0xd4c5b6,0,.48),
  wound=std('woundFace',0x5a272f,0,.70),scar=std('scarFace',0x71545b,0,.88),stitch=std('stitchFace',0x23191c,0,.84),
  tendon=std('tendonFace',0x8e686a,0,.48),bruteFlesh=std('bruteFace',0x6f585d,0,.90),crawlerBone=std('crawlerBone',0x7a6868,0,.86),
  impFlesh=std('impFace',0x8b4c60,0,.78),wraithBone=std('wraithBone',0xa4a0a3,0,.58),necroBone=std('necroBone',0xb8aeaa,0,.52),gargStone=std('gargFace',0x6a5f65,0,.88),
  glowPale=new THREE.MeshBasicMaterial({color:0xd8dee9}),glowPurple=new THREE.MeshBasicMaterial({color:0xa85cff}),glowAmber=new THREE.MeshBasicMaterial({color:0xd8a167});
 const glossEye=color=>new THREE.MeshPhysicalMaterial({color,metalness:.02,roughness:.05,clearcoat:1,clearcoatRoughness:.08});
 const addEye=(x,y,z,scale,mat,pupilScale,pupilMat,socketScale)=>{
  if(socketScale)bulb(head,x,y,z-.02,socketScale,dark);
  const eye=setBaseScale(bulb(head,x,y,z,scale,mat));
  const pupil=setBaseScale(bulb(head,x,y,z+scale[2]*.72,pupilScale,pupilMat));
  parts.eyes.push(eye);parts.pupils.push(pupil);return {eye,pupil};
 };
 let jawOffset=[0,.04,0],jawTop=[.20,.08,.08],jawBottom=[.18,.08,.12],teethTop=8,teethBottom=8,teethWidth=.30,jawTopMat=dark,jawBotMat=std('jaw',0x53464c),skipTeeth=false;
 if(type==='brute'){
  bulb(head,0,.08,.16,[.24,.17,.16],bruteFlesh);bulb(head,0,-.02,.24,[.13,.08,.08],dark);
  for(const s of [-1,1]){bulb(head,s*.18,.11,.18,[.12,.07,.09],bruteFlesh);bulb(head,s*.14,.01,.31,[.07,.05,.03],dark);addEye(s*.11,.02,.36,[.032,.026,.024],glossEye(0x301417),[.012,.012,.010],std('brutePupil',0xa34e43,0,.18),[.08,.05,.04]);}
  stitchScar(head,[[-.16,.16,.18],[-.05,.06,.30],[.03,-.01,.35]],.008,scar,stitch,5);
  stitchScar(head,[[.08,.12,.20],[.16,.03,.33],[.19,-.04,.34]],.007,wound,stitch,4);
  path(head,[[-.05,.00,.40],[0,-.07,.47],[.04,-.14,.43]],.008,tendon);
  jawOffset=[0,-.01,.03];jawTop=[.31,.17,.09];jawBottom=[.30,.12,.16];teethTop=14;teethBottom=12;teethWidth=.50;jawTopMat=dark;jawBotMat=std('bruteJaw',0x6a5556);parts.roarDrool=path(head,[[0,-.02,.41],[.01,-.23,.56],[0,-.43,.47]],.006,std('drool',0xb5989d,0,.12));
 }else if(type==='crawler'){
  bulb(head,0,.03,.16,[.18,.10,.22],crawlerBone);bulb(head,0,-.05,.30,[.10,.07,.10],dark);bulb(head,0,.11,.24,[.15,.06,.12],crawlerBone);
  for(const s of [-1,1]){bulb(head,s*.12,.10,.24,[.07,.04,.06],crawlerBone);addEye(s*.09,.02,.34,[.028,.022,.020],glossEye(0x2a272a),[.010,.010,.009],std('crawlPupil',0xbcb0a5,0,.20),[.06,.04,.03]);}
  stitchScar(head,[[-.05,.16,.16],[0,.10,.29],[.05,.02,.39]],.005,scar,stitch,3);
  path(head,[[-.12,.00,.37],[0,-.02,.48],[.12,.00,.37]],.006,wound);jawOffset=[0,-.08,.05];jawTop=[.16,.08,.07];jawBottom=[.14,.05,.13];teethTop=10;teethBottom=8;teethWidth=.24;jawBotMat=std('crawlJaw',0x605154);
 }else if(type==='imp'){
  bulb(head,0,.12,.18,[.18,.15,.12],impFlesh);bulb(head,0,-.01,.15,[.22,.13,.15],impFlesh);bulb(head,0,.00,.27,[.10,.06,.05],wound);
  for(const s of [-1,1]){const eye=addEye(s*.17,.12,.34,[.12,.11,.09],new THREE.MeshPhysicalMaterial({color:0x40262d,metalness:.02,roughness:.04,clearcoat:1,clearcoatRoughness:.05}),[.044,.044,.030],std('impPupil',0xd8d6cc,0,.15),[.14,.12,.08]);
    const lid=setBaseScale(bulb(head,s*.17,.17,.34,[.13,.038,.07],std('impLid',0x6a3848)));parts.eyelids.push(lid);
    const cheek=bulb(head,s*.18,.02,.24,[.08,.06,.05],impFlesh);parts.details.push(cheek);
    const glint=setBaseScale(bulb(head,s*.14,.15,.40,[.018,.018,.010],new THREE.MeshBasicMaterial({color:0xf7d9d9})));parts.details.push(glint);
  }
  path(head,[[-.05,.02,.31],[0,.01,.36],[.05,.02,.31]],.004,dark);jawOffset=[0,-.02,.12];jawTop=[.12,.045,.05];jawBottom=[.11,.04,.07];teethTop=10;teethBottom=10;teethWidth=.18;jawBotMat=std('impJaw',0x6f4250);
 }else if(type==='wraith'){
  bulb(head,0,.08,.18,[.11,.18,.10],wraithBone);bulb(head,0,-.01,.21,[.07,.06,.04],dark);bulb(head,0,.18,.10,[.14,.09,.10],std('wraithBrow',0x59545c));
  for(const s of [-1,1]){bulb(head,s*.07,.08,.24,[.05,.035,.03],dark);addEye(s*.06,.08,.26,[.014,.014,.010],glowPale,[.009,.009,.007],glowPale,[.045,.032,.025]);}
  jawOffset=[0,-.01,.05];jawTop=[.12,.06,.05];jawBottom=[.08,.05,.09];teethTop=0;teethBottom=0;teethWidth=.16;jawTopMat=std('wraithMaw',0x17141a);jawBotMat=std('wraithJaw',0x5e575b);
 }else if(type==='necromancer'){
  // Face is genuinely inset into an open hood, rather than obscured by a filled oval.
  necroOpenHood(head,parts);
  const cranium=bulb(head,0,.040,.165,[.135,.169,.133],necroBone);parts.faceCranium=cranium;
  bulb(head,0,-.09,.236,[.090,.071,.083],necroBone);
  for(const side of [-1,1]){
   bulb(head,side*.078,.090,.257,[.072,.059,.043],dark);
   path(head,[[side*.14,.10,.235],[side*.12,.035,.305],[side*.10,-.045,.297]],.018,necroBone);
   path(head,[[side*.098,-.035,.30],[side*.064,-.090,.329],[side*.035,-.135,.30]],.010,skull);
   addEye(side*.074,.081,.304,[.018,.014,.009],glowPurple,[.009,.008,.005],glowPurple,[.063,.056,.033]);
  }
  bulb(head,0,-.030,.316,[.024,.037,.014],dark);
  bulb(head,0,.187,.243,[.125,.023,.053],std('necroFrontalBone',0x968b8e,0,.72));
  stitchScar(head,[[-.095,.154,.248],[-.052,.176,.284],[.005,.169,.28]],.004,std('necroForeheadScar',0x55404b),std('necroForeheadStitch',0x2a1c24),3);
  jawOffset=[0,-.045,.040];jawTop=[.095,.048,.033];jawBottom=[.079,.052,.052];teethTop=0;teethBottom=0;teethWidth=.14;jawTopMat=std('necroMaw',0x161117);jawBotMat=std('necroJaw',0xa99d99);
 }else if(type==='gargoyle'){
  bulb(head,0,.10,.14,[.16,.11,.16],gargStone);bulb(head,0,.02,.31,[.11,.07,.11],gargStone);bulb(head,0,-.02,.38,[.07,.05,.05],dark);
  for(const s of [-1,1]){bulb(head,s*.16,.14,.18,[.10,.05,.07],gargStone);bulb(head,s*.10,.08,.31,[.05,.04,.03],dark);addEye(s*.09,.10,.34,[.026,.022,.020],glossEye(0x3b2a24),[.010,.010,.008],glowAmber,[.055,.040,.028]);
    const ear=cusp(head,s*.21,.24,.05,.06,.24,std('gargEar',0x494146),-.55,s*.45);parts.details.push(ear);
  }
  jawOffset=[0,-.03,.11];jawTop=[.18,.09,.07];jawBottom=[.16,.06,.10];teethTop=8;teethBottom=6;teethWidth=.22;jawBotMat=std('gargJaw',0x645156);
 }
 const jawAnchor=plan.jaw, j=new THREE.Group();j.position.set(jawAnchor[0]+jawOffset[0],jawAnchor[1]-plan.anchors.head[1]+jawOffset[1],jawAnchor[2]-plan.anchors.head[2]+jawOffset[2]);head.add(j);parts.jaw=j;
 bulb(j,0,.04,0,jawTop,jawTopMat);bulb(j,0,-.065,.04,jawBottom,jawBotMat);
 if(!skipTeeth){
  for(let i=0;i<teethTop;i++){const x=(i/(Math.max(1,teethTop)-1)-.5)*teethWidth;cusp(j,x,.055,.06,.017,.10,ivory,Math.PI);}
  for(let i=0;i<teethBottom;i++){const x=(i/(Math.max(1,teethBottom)-1)-.5)*teethWidth*.92;cusp(j,x,-.067,.06,.016,.08,ivory,0);}
 }
 if(type==='necromancer'){
  const tooth=std('necroTeeth',0xc7b9b0,0,.61);
  for(let k=0;k<8;k++){const x=(k-3.5)*.023;bulb(j,x,.009,.067,[.010,.023,.013],tooth);bulb(j,x,-.068,.069,[.009,.019,.012],tooth);}
  path(j,[[-.08,-.115,.029],[0,-.131,.061],[.08,-.115,.029]],.009,necroBone);
 }
 if(type==='gargoyle')for(const side of [-1,1]){const horn=cusp(head,side*.18,.25,-.06,.11,.56,std('horn',0x403940),-.45,side*.42);horn.rotation.z=side*.30;const browHorn=cusp(head,side*.09,.22,.22,.035,.18,std('browHorn',0x63545a),-.62,side*.06);parts.details.push(browHorn);}
 if(type==='brute'){for(let i=0;i<7;i++){const x=(i-3)*.14;path(bones.chest,[[x,.25,.22],[x+.026,.06,.32],[x+.05,-.09,.32]],.008,std('scar',0x45252b));}}
}
function clawHand(bone,plan,type,parts,side){const skin=std('clawSkin'+type,type==='imp'?0x9c4555:0x54474d),dark=std('talon',0x201d22,0,.30);
 const s=type==='brute'?1.50:type==='crawler'?1.20:type==='gargoyle'?1.32:1.0;
 const palm=bulb(bone,0,-.025,.016,[.125*s,.055*s,.135*s],skin);parts.details.push(palm);
 for(let k=0;k<4;k++){
  const x=(k-1.5)*.071*s;
  path(bone,[[x,-.04,.06],[x*1.2,-.08,.17*s],[x*1.26,-.16,.24*s]],.021*s,skin);
  const tip=cusp(bone,x*1.3,-.18,.27*s,.022*s,.17*s,dark,Math.PI*.61);parts.details.push(tip);
 }
}
function clothStrip(parent,type,x,z,length,mat){const b=new THREE.Group();b.position.set(x,0,z);parent.add(b);
 const g=new THREE.BufferGeometry(),verts=[],uv=[],ids=[],rings=12;const width=.09+.04*Math.abs(x);
 for(let j=0;j<=rings;j++){
  const t=j/rings,yy=-length*t;const wave=Math.sin(t*10+x*17)*.07*t;
  verts.push(-width*(1-t*.29),yy,wave,width*(1-t*.29),yy,wave);uv.push(0,t,1,t);
  if(j<rings){const a=j*2;ids.push(a,a+2,a+1,a+1,a+2,a+3);}
 }
 g.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(ids);g.computeVertexNormals();
 const mesh=new THREE.Mesh(g,mat);b.add(mesh);return {bone:b,x,z,velocity:0,value:0};
}
function addCloth(type,bones,parts){const cloak=type==='necromancer'?0x241925:type==='wraith'?0x383438:0x544135;
 const fabric=std('fabric'+type,cloak);for(let i=0;i<(type==='necromancer'?12:type==='wraith'?10:9);i++){
  const angle=i*Math.PI*2/(type==='necromancer'?12:type==='wraith'?10:9);
  const radius=type==='brute'?.38:.32,pt=bones.pelvis;
  const c=clothStrip(pt,type,Math.sin(angle)*radius,Math.cos(angle)*radius, type==='brute'?.45:type==='necromancer'?.53:.78,fabric);
  if(type==='necromancer')c.bone.position.y=.11;
  parts.cloth.push(c);
 }
 if(type!=='brute'&&type!=='necromancer'&&type!=='wraith'){
  const hood=bulb(bones.head,0,.11,-.07,[.31,.35,.32],std('hood'+type,cloak));parts.details.push(hood);
  const shadow=bulb(bones.head,0,-.03,.245,[.20,.19,.024],std('hoodshadow',0x0b0811));parts.details.push(shadow);
 }
}
function addStaff(bones,parts){
 const rod=std('necroStaffDarkWood',0x35262e,0,.81),iron=std('necroThorns',0x81717a,.40,.45),bone=std('necroStaffBone',0x98898b,0,.58);
 const root=bones.Lwrist;
 const orbMat=new THREE.MeshBasicMaterial({color:0xb66aff,transparent:true,opacity:.95,depthWrite:false});parts.orbMaterial=orbMat;
 const glowMat=new THREE.MeshBasicMaterial({color:0x9d52ee,transparent:true,opacity:.19,depthWrite:false});
 path(root,[[0,-1.12,.02],[.035,-.71,.03],[-.015,-.27,-.01],[.03,.22,.03],[0,.86,.04],[0,1.25,.04]],.043,rod);
 path(root,[[.01,-.73,.04],[-.038,-.48,.072],[.026,-.31,.05]],.018,bone);
 for(let i=0;i<6;i++){
  const y=-.76+i*.34;
  const band=new THREE.Mesh(new THREE.TorusGeometry(.048,.010,6,18),iron);band.position.set(0,y,.03);band.rotation.x=Math.PI*.5;root.add(band);
 }
 for(let i=0;i<7;i++){
  const a=i*Math.PI*2/7,dx=Math.sin(a),dz=Math.cos(a);
  path(root,[[dx*.025,1.02,dz*.025],[dx*.21,1.33,dz*.17],[dx*.165,1.61,dz*.10],[dx*.047,1.70,dz*.05]],.022,iron);
  cusp(root,dx*.11,1.54,dz*.08,.030,.19,bone,Math.PI*.13,dx*.4);
 }
 const cage=new THREE.Group();cage.position.set(0,1.43,.03);root.add(cage);
 const orb=bulb(cage,0,0,0,[.155,.155,.155],orbMat);parts.orb=orb;
 const halo=bulb(cage,0,0,0,[.24,.24,.24],glowMat);halo.castShadow=false;parts.orbHalo=halo;
 const lamp=new THREE.PointLight(0xaa58ff,.55,3.1,2);lamp.position.set(0,1.43,.03);root.add(lamp);parts.staffLight=lamp;
 parts.staffCrown=cage;
 for(let i=0;i<6;i++){
  const a=i*Math.PI/3,dx=Math.sin(a),dz=Math.cos(a);
  const glyph=bulb(root,dx*.22,1.42,dz*.22,[.027,.027,.027],orbMat);
  parts.runes.push(glyph);
 }
 const casting=bones.Rwrist;
 const spell=bulb(casting,0,.13,.12,[.11,.11,.11],orbMat);parts.spell=spell;
 necroCastingWisps(casting,parts);
}
function addWing(type,bones,parts,sign){
 const anchor=bones.chest,wing=new THREE.Group();wing.position.set(sign*.23,.16,-.16);anchor.add(wing);
 const finger=std('wingfinger',0x51454d);
 const tips=[[sign*.80,.44,-.10],[sign*1.96,.54,-.28],[sign*1.74,.13,-.47],[sign*1.34,-.33,-.52],[sign*.76,-.43,-.35]];
 const rootBone=new THREE.Bone();rootBone.name='WingRoot';wing.add(rootBone);
 const elbow=new THREE.Bone();elbow.name='WingElbow';elbow.position.set(sign*.42,.27,-.03);rootBone.add(elbow);
 const wrist=new THREE.Bone();wrist.name='WingWrist';wrist.position.set(sign*.39,.09,-.12);elbow.add(wrist);
 const fingers=[];
 for(let i=0;i<4;i++){const b=new THREE.Bone();b.name='WingFinger'+i;b.position.set(sign*.20,.08-i*.12,-.06);wrist.add(b);fingers.push(b);}
 const verts=[],uv=[],idx=[],indices=[],weights=[],N=20,M=20;
 for(let i=0;i<=N;i++){
  const seg=Math.min(3.999,i/N*4),k=Math.floor(seg),t=seg-k,A=tips[k],B=tips[k+1];
  const tx=A[0]+(B[0]-A[0])*t,ty=A[1]+(B[1]-A[1])*t,tz=A[2]+(B[2]-A[2])*t;
  for(let j=0;j<=M;j++){
   const r=j/M;
   const torn=(j===M?.94-.17*Math.abs(Math.sin(i*1.31+k*.7)):.98);
   const x=tx*r*torn,y=ty*r*torn+.10*Math.sin(Math.PI*r)*Math.cos(i*.37),z=tz*r*torn+.09*Math.sin(Math.PI*r)*Math.sin(i*.23);
   verts.push(x,y,z);uv.push(i/N,r);
   const tipBone=3+Math.min(k,3),v=clamp(r*1.8,0,1);
   indices.push(0,1,tipBone,0);weights.push((1-v)*.70,(1-v)*.30,v,0);
   if(i<N&&j<M){const a=i*(M+1)+j,b=a+M+1;idx.push(a,b,a+1,a+1,b,b+1);}
  }
 }
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
 geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
 geo.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(indices,4));
 geo.setAttribute('skinWeight',new THREE.Float32BufferAttribute(weights,4));
 geo.setIndex(idx);geo.computeVertexNormals();
 wing.updateMatrixWorld(true);
 const skeleton=new THREE.Skeleton([rootBone,elbow,wrist,...fingers]);skeleton.calculateInverses();
 const sheet=new THREE.SkinnedMesh(geo,wingMaterial());sheet.bind(skeleton);sheet.castShadow=true;sheet.receiveShadow=true;
 sheet.frustumCulled=false;wing.add(sheet);
 for(const e of tips)path(wing,[[0,0,.015],[e[0]*.42,e[1]*.58,.04],[e[0]*.82,e[1]*.87,e[2]*.8],e],.020,finger);
 parts.wings.push({grp:wing,side:sign,elbow,wrist,fingers,membrane:sheet});
}
let WINGMAT=null;
function wingMaterial(){if(WINGMAT)return WINGMAT;
 const size=192,c=document.createElement('canvas');c.width=c.height=size;const ctx=c.getContext('2d');
 ctx.fillStyle='#7a5058';ctx.fillRect(0,0,size,size);
 for(let j=0;j<27;j++){const x=(j*89)%size,y=(j*47)%size,r=2+(j*17)%13;
  ctx.globalCompositeOperation='destination-out';ctx.beginPath();ctx.ellipse(x,y,r,r*.52,j*.3,0,Math.PI*2);ctx.fill();}
 ctx.globalCompositeOperation='source-over';ctx.strokeStyle='rgba(37,17,24,.52)';ctx.lineWidth=2;
 for(let i=0;i<17;i++){ctx.beginPath();ctx.moveTo(7+i*11,0);ctx.lineTo(35+i*8,size);ctx.stroke();}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;
 WINGMAT=new THREE.MeshStandardMaterial({color:0xc2a1a8,map:t,transparent:true,alphaTest:.25,side:THREE.DoubleSide,metalness:0,roughness:.75,depthWrite:true});return WINGMAT;
}
// Species-level anatomical pass. Distinct silhouettes and surface landmarks are
// attached to existing named bones; no changes are required to the enemy AI contract.
const ORGANIC_HEADS=new Map();
function organicCranium(parent,species,profile,material){
 let geom=ORGANIC_HEADS.get(species);
 if(!geom){
  const segments=28,verts=[],uv=[],ids=[],colors=[],rings=profile.length;
  for(let j=0;j<rings;j++){
   const [y,rx,rz,cy,cz]=profile[j];
   for(let i=0;i<=segments;i++){
    const a=i/segments*Math.PI*2,side=Math.cos(a),forward=Math.sin(a);
    const bump=1+.026*Math.sin(a*9+j*1.7)+.015*Math.sin(a*15+j*2.7);
    const ridge=forward>0?Math.pow(forward,4)*(.022*Math.sin(y*15+a*2)):0;
    verts.push(rx*side*bump, y, cy+(rz*forward+ridge)*bump+cz);
    uv.push(i/segments,j/(rings-1));
    const darken=.72+.24*Math.max(0,forward)+.04*Math.sin(a*7+j*1.7);
    colors.push(darken,darken*.92,darken*.90);
    if(j<rings-1&&i<segments){const q=j*(segments+1)+i;ids.push(q,q+segments+1,q+1,q+1,q+segments+1,q+segments+2);}
   }
  }
  geom=new THREE.BufferGeometry();geom.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
  geom.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geom.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geom.setIndex(ids);geom.computeVertexNormals();
  ORGANIC_HEADS.set(species,geom);
 }
 const m=new THREE.Mesh(geom,material);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function organicMat(id,color,rough=.79,metal=0){const key='organic:'+id;let mat=MAT[key];if(!mat){mat=new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal,vertexColors:true,side:THREE.DoubleSide});MAT[key]=mat;}return mat;}
function makeMuscle(parent,pts,r,mat){return path(parent,pts,r,mat);}
function addClawToes(bones,mat,boneMat,parts,count=4){
 for(const side of ['L','R']){const foot=bones[side+'foot'];
  for(let i=0;i<count;i++){const x=(i-(count-1)/2)*.085;
   const digit=path(foot,[[x*.7,-.02,.04],[x,-.055,.15],[x*1.12,-.075,.245]],.020,mat);
   const nail=cusp(foot,x*1.12,-.085,.27,.019,.14,boneMat,Math.PI*.60);
   parts.closeOnly.push(digit,nail);
  }
 }
}
function anatomicDetails(type,b,parts){
 const scar=std('anatomScar',0x4b252d,0,.73),pale=std('anatomTendon',0x877a7b,0,.84),
  ivory=std('anatomIvory',0xb5a5a0,0,.64),dark=std('anatomCrevice',0x281c22,0,.94),
  meat=std('anatomSinew',0x77535a,0,.66),skin=std('anatomDermis',0x6d585e,0,.71);
 if(type==='brute'){
  // Low recessed skull / huge shoulder cap, parted lips, stitched cheeks.
  parts.cranialShell=organicCranium(b.head,'brute',[
   [-.15,.08,.06,0,.07],[-.12,.22,.19,0,.10],[-.03,.25,.23,0,.10],[.08,.20,.18,0,.06],[.19,.14,.12,0,.02],[.29,.03,.04,0,.02]],organicMat('brute',0x89767b));
  for(const side of [-1,1]){
   path(b.head,[[side*.23,.06,.26],[side*.21,-.02,.36],[side*.15,-.10,.39]],.021,meat);
   path(b.head,[[side*.20,-.05,.34],[side*.24,-.13,.29],[side*.21,-.20,.21]],.009,scar);
   for(let k=0;k<4;k++){const x=side*(.08+k*.035),y=.12-k*.065;path(b.head,[[x,y,.29],[x+side*.018,y-.04,.32]],.006,scar);}
  }
  for(const side of ['L','R']){
   const shoulder=b[side+'shoulder'];
   const bulk=bulb(shoulder,0,.01,-.04,[.34,.30,.33],std('bruteDeltoid',0x716369,0,.88));parts.midOnly.push(bulk);
   for(let j=0;j<5;j++){const y=-.20-j*.09;
    const strap=path(b[side+'elbow'],[[-.16,y,.11],[0,y+.025,.19],[.16,y,.10]],.015,std('bruteLeather',0x2f2428,0,.9));parts.midOnly.push(strap);
   }
  }
  for(let i=0;i<7;i++){
   const y=.0-i*.09,x=Math.sin(i*.83)*.21;
   parts.closeOnly.push(stitchScar(b.spine,[[x-.13,y,.49],[x,y-.015,.55],[x+.13,y-.03,.50]],.006,scar,dark,4));
  }
  const left=path(b.chest,[[-.3,.20,.43],[-.25,-.11,.52],[-.12,-.28,.58]],.019,meat);
  const right=path(b.chest,[[.28,.25,.42],[.22,-.15,.52],[.14,-.29,.53]],.016,meat);
  parts.midOnly.push(left,right);parts.anatomy='heavy dermis, stitched wounds, heavy shoulders';
 }else if(type==='crawler'){
  // A long forward skull, exposed collar bones and continuous rib arc anatomy.
  parts.cranialShell=organicCranium(b.head,'crawler',[
   [-.19,.075,.09,0,.01],[-.15,.14,.17,0,.11],[-.06,.19,.19,0,.15],[.03,.18,.16,0,.13],[.13,.15,.11,0,.04],[.18,.035,.04,0,-.04]],organicMat('crawler',0x8e7b7f));
  path(b.head,[[0,.06,.20],[0,-.055,.43],[0,-.14,.48]],.022,std('crawlNoseBone',0x897c7d));
  for(const side of [-1,1]){
   path(b.head,[[side*.08,.085,.28],[side*.15,-.00,.40],[side*.12,-.10,.38]],.024,ivory);
   const fang=cusp(b.head,side*.13,-.13,.46,.035,.22,ivory,Math.PI*.55,side*.2);parts.midOnly.push(fang);
  }
  const ribMat=std('crawlRibSurface',0x8c7779,0,.78);
  for(let i=0;i<9;i++){
   const zz=.24-i*.11,y=.02-i*.013;
   for(const side of [-1,1]){
    const arch=path(b.spine,[[side*.085,y+.16,zz],[side*.22,y+.115,zz+.02],[side*.25,y-.05,zz+.055],[side*.14,y-.12,zz+.06]],.013+(i%3)*.003,ribMat);
    parts.midOnly.push(arch);
   }
  }
  for(const side of ['L','R']){
   const arm=b[side+'elbow'];
   for(let i=0;i<3;i++){
    const vein=path(arm,[[.04*i,-.02,-.03],[.04*i,-.18,.09],[.04*i,-.29,.13]],.008,meat);parts.closeOnly.push(vein);
   }
  }
  for(let i=0;i<6;i++){
   const zz=.30-i*.16;const dorsal=cusp(b.spine,0,.19,zz,.049,.21,ivory,-.36);parts.midOnly.push(dorsal);
  }
  addClawToes(b,skin,dark,parts,4);parts.anatomy='rib arches, exposed vertebrae, hooked teeth';
 }else if(type==='imp'){
  // Distorted infant-like face: forehead domes, irregular eye rims and thick mottled lips.
  parts.cranialShell=organicCranium(b.head,'imp',[
   [-.18,.07,.08,0,.04],[-.12,.29,.22,0,.08],[-.03,.38,.30,0,.10],[.11,.44,.34,0,.08],[.26,.42,.32,0,.06],[.37,.34,.26,0,.00],[.45,.15,.10,0,-.03],[.49,.015,.02,0,-.08]],organicMat('imp',0x934b62,.56));
  const flesh=std('impLips',0x713b4c,0,.47),wrink=std('impWrinkle',0x4c2b39,0,.87),vein=std('impVein',0xa77084,0,.70);
  for(const side of [-1,1]){
   const s=side;
   const ring=[];for(let i=0;i<=20;i++){
    const a=i/20*Math.PI*2;ring.push([s*.17+Math.cos(a)*.133,.12+Math.sin(a)*.113,.343+.02*Math.cos(a*2)]);
   }
   parts.closeOnly.push(path(b.head,ring,.019,flesh));
   parts.eyelids.push(setBaseScale(bulb(b.head,s*.17,.22,.34,[.127,.018,.057],flesh)));
   const tears=path(b.head,[[s*.06,.24,.33],[s*.11,.28,.29],[s*.16,.29,.25]],.009,vein);parts.closeOnly.push(tears);
   for(let j=0;j<3;j++){
    const y=.03-j*.035;
    parts.closeOnly.push(path(b.head,[[s*.08,y,.35],[s*.17,y-.02,.35],[s*.23,y-.03,.30]],.009,wrink));
   }
   const nostril=bulb(b.head,s*.045,-.032,.455,[.024,.018,.007],dark);parts.closeOnly.push(nostril);
  }
  const lip=path(b.head,[[-.105,-.068,.43],[-.05,-.085,.50],[0,-.077,.505],[.060,-.087,.495],[.115,-.050,.42]],.025,flesh);parts.midOnly.push(lip);
  const chin=bulb(b.head,0,-.16,.40,[.15,.06,.09],std('impLowerLip',0x865064,0,.53));parts.midOnly.push(chin);
  for(const side of ['L','R']){const fore=b[side+'elbow'];for(let j=0;j<3;j++){
   parts.closeOnly.push(path(fore,[[j*.022,-.02,.10],[j*.03,-.15,.11],[j*.025,-.26,.10]],.009,vein));
  }}
  addClawToes(b,skin,dark,parts,4);parts.anatomy='grossly oversized head, lip folds, orbital tissue';
 }else if(type==='wraith'){
  // Reference is much less cloaked than the name implies: exposed long bones,
  // hollow eyes, sinewy abdomen and only fragments of a hood.
  parts.cranialShell=organicCranium(b.head,'wraith',[
   [-.20,.065,.055,0,.08],[-.11,.125,.115,0,.12],[.01,.14,.11,0,.11],[.16,.145,.10,0,.06],[.23,.12,.09,0,.03],[.29,.03,.03,0,.03]],organicMat('wraith',0x726b71,.89));
  const sinew=std('wraithSinew',0x7a6971,0,.85),bone=std('wraithBoneRibs',0x8d8488,0,.89),shroud=std('wraithShred',0x38333b,0,.94);
  for(const side of [-1,1]){
   path(b.head,[[side*.11,.15,.18],[side*.14,.04,.24],[side*.07,-.15,.23]],.016,bone);
   const hoodTail=clothStrip(b.head,'wraith',side*.16,-.08,.65,shroud);
   hoodTail.bone.position.y=.24;parts.cloth.push(hoodTail);
  }
  for(let i=0;i<8;i++){
   const y=.24-i*.066,z=.27+i*.012;
   for(const side of [-1,1]){const rib=path(b.spine,[[side*.035,y+.01,z],[side*.15,y-.04,z+.07],[side*.18,y-.10,z-.02]],.014,bone);parts.midOnly.push(rib);}
  }
  for(const side of ['L','R']){
   const arm=b[side+'elbow'];
   for(let k=0;k<3;k++){const x=(k-1)*.045;
    const cord=path(arm,[[x,-.03,.05],[x*.8,-.22,.13],[x*1.5,-.38,.11]],.009,sinew);parts.closeOnly.push(cord);
   }
  }
  for(let k=0;k<6;k++){
   const x=(k%2?-.1:.1),z=(k%3)*.045;
   const r=clothStrip(b.pelvis,'wraith',x,z,.43+(k%3)*.13,shroud);r.bone.position.y=-.17;parts.cloth.push(r);
  }
  parts.anatomy='exposed rib cage, gaunt musculature, fragmented hood';
 }else if(type==='gargoyle'){
  // Beaked skeletal demon face with strong cranial ridges and horn cores.
  parts.cranialShell=organicCranium(b.head,'gargoyle',[
   [-.15,.065,.05,0,.06],[-.10,.17,.12,0,.06],[.00,.22,.19,0,.08],[.10,.22,.18,0,.05],[.20,.18,.15,0,.01],[.27,.08,.07,0,-.05],[.30,.015,.02,0,-.08]],organicMat('gargoyle',0x84777b,.91));
  const shell=std('gargBonyRidge',0x928489,0,.92),scales=std('gargScales',0x645760,0,.89),fangs=std('gargFangs',0xc0b3ab,0,.72);
  for(const side of [-1,1]){
   const s=side;
   path(b.head,[[s*.07,.26,.18],[s*.15,.24,.27],[s*.19,.12,.34],[s*.11,.03,.43]],.034,shell);
   path(b.head,[[s*.13,-.05,.33],[s*.20,-.10,.25],[s*.23,-.13,.16]],.025,scales);
   const horn=path(b.head,[[s*.16,.21,.02],[s*.26,.35,-.03],[s*.34,.42,-.16],[s*.40,.44,-.30]],.046,shell);parts.midOnly.push(horn);
   const tooth=cusp(b.head,s*.13,-.19,.45,.029,.17,fangs,Math.PI*.78);parts.closeOnly.push(tooth);
  }
  const beak=path(b.head,[[0,.01,.31],[0,-.065,.54],[0,-.12,.59]],.035,shell);parts.midOnly.push(beak);
  for(let k=0;k<9;k++){const z=-.18-k*.075,y=.13-(k*.011);const spike=cusp(b.chest,0,y,z,.058,.18,scales,-.65);parts.midOnly.push(spike);}
  for(const side of ['L','R']){
   for(let j=0;j<3;j++){
    const vein=path(b[side+'elbow'],[[j*.04,-.04,.02],[j*.03,-.14,.12],[j*.04,-.30,.10]],.012,shell);parts.closeOnly.push(vein);
   }
  }
  addClawToes(b,scales,fangs,parts,4);
  parts.tailSegments=[];
  for(let i=0;i<6;i++){
   const tail=new THREE.Group();b.pelvis.add(tail);
   if(i===0)tail.position.set(0,-.20,-.36);
   else{tail.position.set(0,-.06,-.21);parts.tailSegments[i-1].add(tail);}
   const piece=path(tail,[[0,0,0],[0,-.04,-.13],[0,-.05,-.26]],Math.max(.022,.081-i*.011),scales);
   parts.tailSegments.push(tail);parts.midOnly.push(piece);
  }
  parts.anatomy='beaked skull, horn ridges, scaly veins, flexible tail';
 }
}
function addDistinct(type,bones,parts){const b=bones,plan=SPEC[type],bone=std('bone',0xc7b9a1,0,.62),wound=std('wound',0x4f222c,0,.65);
 headDetails(type,b,parts);
 if(type!=='necromancer')anatomicDetails(type,b,parts);
 for(const s of ['L','R'])clawHand(b[s+'wrist'],plan,type,parts,s);
 if(type==='brute'){
  addCloth('brute',b,parts);
  for(const s of ['L','R']){
   const strap=new THREE.Mesh(new THREE.TorusGeometry(.22,.025,6,18),std('leather',0x30232a));strap.rotation.x=Math.PI/2;strap.position.y=-.18;b[s+'elbow'].add(strap);
  }
  for(let i=0;i<13;i++){
   const y=.35-i*.085,x=Math.sin(i*9)*.29;
   path(b.chest,[[x,y,.40],[x+.018,y+.02,.455],[x+.045,y+.035,.45]],.006,wound);
  }
 } else if(type==='crawler'){
  for(let i=0;i<9;i++){
   const z=.45-i*.13;const spine=cusp(b.spine,0,.1,z,.07,.19,bone,-.30);parts.details.push(spine);
  }
 } else if(type==='imp'){
  // Eyelids and brow ridges are built against the large eye sockets in the anatomy pass.
 }else if(type==='wraith'){
  addCloth('wraith',b,parts);
  for(let i=0;i<4;i++){
   const a=i*Math.PI*.5;const tail=clothStrip(b.head,'wraith',Math.sin(a)*.10,-.10,.45,std('shroud',0x494249));parts.cloth.push(tail);
  }
 }else if(type==='necromancer'){
  necroRobeShell(b,parts);addCloth('necromancer',b,parts);addStaff(b,parts);
  const armor=std('necroPauldronRim',0x60444d,.30,.52),trim=std('necroPauldronEdge',0x967480,.50,.41);
  for(const side of ['L','R']){
   const shoulder=bulb(b[side+'shoulder'],0,.02,.04,[.22,.13,.26],std('necroPauldron',0x33242d,.24,.51));parts.details.push(shoulder);
   path(b[side+'shoulder'],[[-.18,.045,.24],[0,.14,.26],[.19,.045,.24]],.019,trim);
   for(let i=0;i<4;i++){
    const x=(i-1.5)*.103;
    const spike=cusp(b[side+'shoulder'],x,.17,.005,.045,.28,armor,0,side==='L'?.18:-.18);parts.details.push(spike);
   }
  }
  for(const [x,y,z,size] of [[-.25,.51,.44,.96],[.24,.51,.44,.94],[.02,.29,.50,.63]]){
   necroSkullCharm(b.pelvis,x,y,z,size,parts);
   path(b.pelvis,[[x,.95,.35],[x*1.13,.71,.41],[x,y+.13,z]],.010,std('necroNecklace',0x6b5e65,.31,.49));
  }
  for(let i=0;i<6;i++){
   const x=(i%2?-.36:.36),z=.22+(i%3)*.045;
   const tail=clothStrip(b.chest,'necromancer',x,z,.68+i*.09,std('necroShred',i%2?0x32222a:0x45313a));
   tail.bone.position.y=-.15-i*.06;parts.cloth.push(tail);
  }
 }else if(type==='gargoyle'){
  addWing(type,b,parts,-1);addWing(type,b,parts,1);
  for(let k=0;k<7;k++){
   const s=cusp(b.chest,0,.27-k*.095,-.38,.055,.22,bone,.43);parts.details.push(s);
  }
  // An articulated tapering bony tail is constructed in the anatomy pass below.
 }
}
function build(type,bodyMat){if(!SPEC[type])throw Error('Unknown bestiary type: '+type);const plan=SPEC[type],group=new THREE.Group(),s=createSkeleton(plan,group),entry=geometries(type);
 const base=raster(type),material=bodyMat||base.clone();
 if(bodyMat){material.map=base.map;material.bumpMap=base.bumpMap;material.bumpScale=base.bumpScale;
  material.roughnessMap=base.roughnessMap;material.roughness=1;material.metalness=0;
  material.color.set(0xffffff);material.needsUpdate=true;}
 const lod=new THREE.LOD();group.add(lod);
 for(let i=0;i<3;i++){
  const mesh=new THREE.SkinnedMesh(entry.geoms[i],material);mesh.frustumCulled=false;mesh.castShadow=true;mesh.receiveShadow=true;
  mesh.bind(s.skeleton);lod.addLevel(mesh,[0,10,21][i]);
 }
 const parts={eyes:[],pupils:[],jaw:null,cloth:[],details:[],eyelids:[],wings:[],runes:[],orb:null,spell:null,staffLight:null,hoodShell:null,faceCranium:null,robeShells:[],robeRunes:[],trophies:[],wisps:[],staffCrown:null,orbHalo:null,orbMaterial:null,runeMat:null,wispMat:null,cranialShell:null,closeOnly:[],midOnly:[],tailSegments:[],anatomy:''};
 addDistinct(type,s.bones,parts);
 const run={type,plan,bones:s.bones,parts,mat:material,lod,mesh:group,clock:0,phase:Math.random()*6.28,
  spring:.0,springV:0,breath:0,stagger:0,attack:0,positionPrev:new THREE.Vector3(),
  normCount:entry.stats.triangles,geometryTime:entry.stats.ms,perch:type==='gargoyle',dying:false};
 group.userData.bestiary=run;group.userData.L=[];group.userData.legs=[];group.userData.wings=[];
 group.userData.detailMeshes=parts.details;group.userData.flight=type==='gargoyle';group.userData.type=type;
 return group;
}
function solveCrawlChain(rig,side,start,middle,end,phase,speed){
 const a=rig.plan.anchors[start],b=rig.plan.anchors[middle],c=rig.plan.anchors[end];
 const fx=c[0]+Math.sin(phase)*(speed*.15),fy=c[1]+Math.max(0,Math.sin(phase))*speed*.16,fz=c[2]+Math.cos(phase)*speed*.11;
 const vx=fx-a[0],vy=fy-a[1],vz=fz-a[2],dist=Math.max(.001,Math.hypot(vx,vy,vz));
 const len1=Math.hypot(b[0]-a[0],b[1]-a[1],b[2]-a[2]);
 const len2=Math.hypot(c[0]-b[0],c[1]-b[1],c[2]-b[2]);
 const d=Math.min(dist,len1+len2-.001),along=(len1*len1-len2*len2+d*d)/(2*d),h=Math.sqrt(Math.max(0,len1*len1-along*along));
 const inv=1/dist,ux=vx*inv,uy=vy*inv,uz=vz*inv;
 let px=side==='L'?-1:1,py=0,pz=0;
 const dot=px*ux+py*uy+pz*uz;px-=dot*ux;py-=dot*uy;pz-=dot*uz;
 const perp=Math.max(.0001,Math.hypot(px,py,pz));px/=perp;py/=perp;pz/=perp;
 const kx=a[0]+ux*along+px*h,ky=a[1]+uy*along+py*h,kz=a[2]+uz*along+pz*h;
 rig.bones[middle].position.set(kx-a[0],ky-a[1],kz-a[2]);
 rig.bones[end].position.set(fx-kx,fy-ky,fz-kz);
}
function update(entity,dt,absolute){const g=entity.mesh||entity,rig=g.userData.bestiary;if(!rig)return;
 if(entity.bestiaryDistance!==undefined&&entity.bestiaryDistance>40)return;
 const detailDistance=entity.bestiaryDistance===undefined?0:entity.bestiaryDistance;
 if(rig.type!=='necromancer'){
  const near=detailDistance<13,mid=detailDistance<25;
  for(let i=0;i<rig.parts.closeOnly.length;i++)rig.parts.closeOnly[i].visible=near;
  for(let i=0;i<rig.parts.midOnly.length;i++)rig.parts.midOnly[i].visible=mid;
 }
 dt=clamp(dt||1/60,.001,.08);rig.clock+=dt;const t=absolute===undefined?rig.clock:absolute;
 const plan=rig.plan,b=rig.bones,p=rig.parts;
 const state=entity.state||entity.ai||'idle',speed=clamp(entity.moveMag||entity.speedNow||0,0,1),
 attack=clamp(entity.pose===undefined?(entity.attackAnim||0):entity.pose,0,1),strike=clamp(entity.strike||0,0,1),
 hit=clamp(entity.hitT||entity.hit||0,0,1),dead=clamp(entity.deadT||0,0,1);
 const gait=t*(rig.type==='brute'?4.9:rig.type==='crawler'?11:rig.type==='imp'?12.5:rig.type==='gargoyle'?8:6)+rig.phase;
 const ga=Math.sin(gait),gb=Math.sin(gait+Math.PI),slow=Math.sin(t*1.7+rig.phase);
 b.spine.rotation.set(.025*slow+.08*attack,0,.06*ga*speed);
 b.chest.rotation.x=.015*Math.sin(t*2+rig.phase)+attack*.06;
 b.head.rotation.y=.08*Math.sin(t*.9+rig.phase);b.head.rotation.x=-.09+.06*Math.sin(t*1.2)+attack*.19;
 b.Lshoulder.rotation.x=.10+ga*.46*speed-attack*.63;b.Rshoulder.rotation.x=.10+gb*.46*speed-attack*.63;
 b.Lelbow.rotation.x=.06+.15*attack;b.Relbow.rotation.x=.06+.15*attack;
 b.Lwrist.rotation.z=ga*.09*speed;b.Rwrist.rotation.z=gb*.09*speed;
 b.Lhip.rotation.x=-ga*.26*speed;b.Rhip.rotation.x=-gb*.26*speed;
 b.Lknee.rotation.x=Math.max(0,ga)*.42*speed;b.Rknee.rotation.x=Math.max(0,gb)*.42*speed;
 b.Lfoot.rotation.x=-b.Lknee.rotation.x*.5;b.Rfoot.rotation.x=-b.Rknee.rotation.x*.5;
 const shock=(hit>0?Math.sin(hit*Math.PI)*.23:0);b.chest.rotation.z+=shock;b.head.rotation.x+=shock*.4;
 if(p.jaw)p.jaw.rotation.x=(rig.type==='brute'?.38:.09)+.09*slow+attack*(rig.type==='brute'?.67:.32);
 if(rig.type==='crawler'){
  b.spine.rotation.x=.12*Math.sin(gait*.7)*speed;
  b.chest.rotation.x=.18*Math.sin(gait*.7+1.2)*speed;
  b.Lshoulder.rotation.x=.52*ga*speed-.6*attack;
  b.Rshoulder.rotation.x=-.52*ga*speed-.6*attack;
  b.Lhip.rotation.x=-.42*ga*speed;
  b.Rhip.rotation.x=.42*ga*speed;
  solveCrawlChain(rig,'L','Lshoulder','Lelbow','Lwrist',gait,speed);
  solveCrawlChain(rig,'R','Rshoulder','Relbow','Rwrist',gait+Math.PI,speed);
  solveCrawlChain(rig,'L','Lhip','Lknee','Lfoot',gait+Math.PI,speed);
  solveCrawlChain(rig,'R','Rhip','Rknee','Rfoot',gait,speed);
 }
 if(rig.type==='imp'){
  const hop=Math.max(0,Math.sin(gait))*.10*speed;
  b.spine.scale.y=1-hop*.18;b.head.scale.set(1+hop*.17,1-hop*.1,1+hop*.1);
  const blink=Math.sin(t*.73+rig.phase)> .995?.08:1;
  for(const eye of p.eyes){const base=eye.userData.baseScale; if(base)eye.scale.set(base.x,base.y*blink,base.z);} 
  for(const lid of p.eyelids){const base=lid.userData.baseScale; if(base)lid.position.y=(lid.userData.baseY-(1-blink)*.06);} 
  const dilation=.85+.18*Math.sin(t*1.6);
  for(const pupil of p.pupils){const base=pupil.userData.baseScale; if(base)pupil.scale.set(base.x*dilation,base.y*dilation,base.z);}
 }
 if(rig.type==='wraith'){
  b.spine.rotation.z=.08*Math.sin(t*.76);
  b.Lshoulder.rotation.x=.09*Math.sin(t*1.04)-.25*attack;
  b.Rshoulder.rotation.x=.09*Math.sin(t*1.16)-.25*attack;
  const dissolve=entity.teleportT||entity.tpFade||0;
  if(dissolve>0){rig.mat.transparent=true;rig.mat.opacity=clamp(1-dissolve*.8,.10,1);rig.mat.depthWrite=rig.mat.opacity>.8;}
  else if(rig.mat.transparent){rig.mat.opacity=1;rig.mat.transparent=false;rig.mat.depthWrite=true;}
 }
 if(rig.type==='brute'){
  b.spine.scale.set(1+.016*Math.sin(t*1.30),1+.031*Math.sin(t*1.30),1+.015*Math.sin(t*1.30));
  b.chest.rotation.x+=.10*attack+.025*slow;
  b.Lshoulder.rotation.x=.18+ga*.34*speed-attack*.84;
  b.Rshoulder.rotation.x=.18+gb*.34*speed-attack*.84;
  b.head.rotation.x-=.10+attack*.29;
  if(p.jaw)p.jaw.rotation.x=.33+.32*attack+.10*Math.max(0,slow);
 }
 if(rig.type==='crawler'){
  b.head.rotation.x=-.18+.12*Math.sin(gait*.8)+attack*.34;
  b.head.rotation.z=.07*Math.sin(gait*.7);
  if(p.jaw)p.jaw.rotation.x=.16+.50*attack;
 }
 if(rig.type==='wraith'){
  b.head.rotation.x-=.06;
  b.chest.rotation.x+=.025*Math.sin(t*.85);
  b.Lshoulder.rotation.z=.13*Math.sin(t*.92);
  b.Rshoulder.rotation.z=-.13*Math.sin(t*.87);
 }
 if(rig.type==='gargoyle'){
  b.head.rotation.x=-.10+.24*attack;
  b.Lshoulder.rotation.x+=.29*attack;
  b.Rshoulder.rotation.x+=.29*attack;
  if(p.jaw)p.jaw.rotation.x=.13+.45*attack;
  for(let k=0;k<p.tailSegments.length;k++){
   p.tailSegments[k].rotation.y=.055*Math.sin(t*2+k*.55);
   p.tailSegments[k].rotation.x=.025*Math.sin(t*1.4+k*.70);
  }
 }
 if(rig.type==='necromancer'){
  b.Lshoulder.rotation.x=-.05+.08*Math.sin(t*.6);b.Lelbow.rotation.x=-.11;
  b.Rshoulder.rotation.x=-.28-attack*.95;b.Relbow.rotation.x=-.16-attack*.43;
  b.Rwrist.rotation.z=.10*Math.sin(t*1.5)-attack*.35;
  const pulse=.5+.5*Math.sin(t*3.9+rig.phase),flare=clamp(attack*.7+strike*.5,0,1);
  if(p.orb)p.orb.scale.setScalar(1+.12*pulse+.55*flare);
  if(p.orbHalo)p.orbHalo.scale.setScalar(1+.13*pulse+.32*flare);
  if(p.staffLight)p.staffLight.intensity=.24+.18*pulse+.46*flare;
  if(p.orbMaterial)p.orbMaterial.opacity=.73+.19*pulse+.08*flare;
  if(p.runeMat)p.runeMat.opacity=.38+.28*pulse+.32*flare;
  if(p.wispMat)p.wispMat.opacity=.43+.25*pulse+.27*flare;
  for(let i=0;i<p.runes.length;i++){
   const a=t*.85+i*Math.PI/3;
   p.runes[i].position.x=Math.sin(a)*.22;p.runes[i].position.z=.03+Math.cos(a)*.22;
  }
  if(p.spell)p.spell.scale.setScalar(.48+.36*pulse+.72*flare);
  const distance=entity.bestiaryDistance===undefined?0:entity.bestiaryDistance;
  if(p.staffLight)p.staffLight.visible=distance<16;
  if(p.orbHalo)p.orbHalo.visible=distance<24;
  for(let i=0;i<p.robeRunes.length;i++)p.robeRunes[i].visible=distance<22;
  for(let i=0;i<p.trophies.length;i++){
    const trophy=p.trophies[i];trophy.visible=distance<26;
    trophy.rotation.z=.035*Math.sin(t*1.45+i*1.5);
  }
  for(let i=0;i<p.wisps.length;i++){
   const w=p.wisps[i];w.group.visible=distance<16;
   if(w.group.visible){
    w.group.rotation.y=t*.51+w.phase;
    w.group.rotation.z=.13*Math.sin(t*1.8+w.phase);
    w.group.scale.setScalar(.75+.15*pulse+.29*flare);
   }
  }
 }
 if(rig.type==='gargoyle'){
  const wakes=state!=='idle'&&state!=='perched';
  rig.perch=!entity.alert||!wakes;
  for(const w of p.wings){const fold=rig.perch?.85:.19;
   w.grp.rotation.y=w.side*(fold+Math.sin(t*(wakes?7:1.4))*(wakes?.22:.016));
   w.grp.rotation.z=w.side*(wakes?.16+.18*Math.cos(t*4.8):.07);
   w.elbow.rotation.x=(wakes?.16:0);w.wrist.rotation.y=w.side*(wakes?.14:.03);
   for(let i=0;i<4;i++)w.fingers[i].rotation.y=Math.sin(t*5+i)*.02;
  }
 }
 const delta=slow*.14+attack*.28;rig.springV+=(delta-rig.spring)*dt*48;rig.springV*=Math.exp(-dt*12);rig.spring+=rig.springV*dt;
 for(let i=0;i<p.cloth.length;i++){
  const s=p.cloth[i],dest=rig.spring+.075*Math.sin(t*2.3+i*.72);
  s.velocity+=(dest-s.value)*dt*35;s.velocity*=Math.exp(-dt*7);s.value+=s.velocity*dt;
  s.bone.rotation.z=s.value*.3;s.bone.rotation.x=s.value*.5;
 }
 if(dead>0){b.pelvis.rotation.z=dead*.90;b.spine.rotation.x=dead*.45;}
}
function voice(type,context,violent){const profile={brute:[64,34,.68,'sawtooth'],crawler:[270,70,.16,'triangle'],imp:[710,210,.28,'sawtooth'],wraith:[220,80,.75,'sine'],necromancer:[145,68,.81,'triangle'],gargoyle:[480,115,.40,'sawtooth']}[type];
 if(!context||!profile)return;try{if(context.state==='suspended')context.resume();const t=context.currentTime,
  o=context.createOscillator(),f=context.createBiquadFilter(),v=context.createGain();
  o.type=profile[3];o.frequency.setValueAtTime(profile[0]*(violent?1.18:1),t);o.frequency.exponentialRampToValueAtTime(profile[1],t+profile[2]);
  f.type='lowpass';f.frequency.setValueAtTime(type==='imp'?3500:1100,t);f.frequency.exponentialRampToValueAtTime(200,t+profile[2]);
  v.gain.setValueAtTime(.0001,t);v.gain.exponentialRampToValueAtTime(.08,t+.03);v.gain.exponentialRampToValueAtTime(.0001,t+profile[2]);
  o.connect(f);f.connect(v);v.connect(context.destination);o.start(t);o.stop(t+profile[2]+.02);
 }catch(e){return;}}
function tryGLB(type,url,loader,onModel,onFail){if(!loader||!url){if(onFail)onFail('No GLTFLoader or GLB path; procedural model remains active');return;}
 loader.load(url,gltf=>{if(gltf&&gltf.scene&&onModel)onModel(gltf.scene);},undefined,err=>{if(onFail)onFail(err&&err.message||String(err));});}
function adaptEnemyId(id){return ({chaser:'imp',brute:'brute',crawler:'crawler',teleporter:'wraith',necromancer:'necromancer',winged:'gargoyle',imp:'imp',gargoyle:'gargoyle',wraith:'wraith'})[id]||null;}
function buildEnemyModel(type,bodyMat,glowMat,darkMat){const species=adaptEnemyId(type)||type;if(!SPEC[species])return null;const grp=build(species,bodyMat);return {grp,parts:grp.userData.bestiary.parts};}
root.DEPTHS_BESTIARY={build,buildEnemyModel,update,voice,tryGLB,adaptEnemyId,TYPES,SPEC,PIXEL_PALETTES,geometryStats:()=>Object.fromEntries([...GEOMETRY.entries()].map(([k,v])=>[k,v.stats]))};
})(typeof window!=='undefined'?window:globalThis);


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
const crosshair=wrap.querySelector('.dd-crosshair');
const hm=mk('position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;pointer-events:none;opacity:0','<div style="position:absolute;left:12px;top:-3px;width:2px;height:32px;background:#fff;transform:rotate(45deg)"></div><div style="position:absolute;left:12px;top:-3px;width:2px;height:32px;background:#fff;transform:rotate(-45deg)"></div>');
hud.style.background='linear-gradient(#000b,#0006)'; hud.style.padding='8px 12px'; hud.style.borderRadius='10px'; hud.style.border='1px solid #ffffff22';
mm.style.borderRadius='10px'; mm.style.boxShadow='0 0 14px #000a';mm.style.width='130px';mm.style.height='130px';mm.width=Math.round(130*Math.min(3,window.devicePixelRatio||2));mm.height=mm.width;mctx.setTransform(mm.width/130,0,0,mm.height/130,0,0); toastEl.style.bottom='118px';
const hpWrap=hpb.parentNode; hpWrap.style.width='260px'; hpWrap.style.height='16px'; hpWrap.style.left='14px'; hpWrap.style.bottom='14px'; hpWrap.style.borderRadius='8px';
const VERSION='6.0.0';
const ART_INTRO='data:image/webp;base64,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';
const ART_MENU='data:image/webp;base64,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';
// Shared HUD and menu styling (works in iframe, local HTML and GitHub Pages).
const uiStyle=document.createElement('style');uiStyle.textContent=`
#dd3d-root .forge-tabs{display:flex;gap:5px;flex-wrap:wrap;margin:8px 0 11px}
#dd3d-root .forge-tab{padding:7px 9px;border:1px solid #70694d;border-radius:6px;background:#171c25;color:#f4ddb9;font-size:10px}
#dd3d-root .forge-tab.selected{background:#655038;color:#fff}
#dd3d-root .forge-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;max-height:340px;overflow:hidden}
#dd3d-root .forge-card{border:1px solid #8a7555aa;background:#101b29ee;padding:9px;border-radius:8px;display:flex;flex-direction:column;gap:5px;min-height:118px}
#dd3d-root .forge-card b{font-size:12px;color:#fce4b9}
#dd3d-root .forge-card small{font-size:10px;color:#b6c2ce}
#dd3d-root .forge-cost{margin-top:auto;font-size:10px;color:#e4be77}
#dd3d-root .forge-buy{background:#66533b;border:1px solid #ba9660;color:white;border-radius:5px;padding:5px;font-size:10px}
#dd3d-root .forge-footer{display:flex;justify-content:space-between;align-items:center;margin-top:12px;gap:8px}
#dd3d-root .forge-pager{grid-column:1/-1;display:flex;justify-content:center;align-items:center;gap:14px}
#dd3d-root .hud{max-width:240px!important}
#dd3d-root .cin-hotbar{opacity:.6;transform:scale(.78);transform-origin:bottom center}

#dd3d-root{--gold:#e9bd76;--teal:#83ded4;--red:#ff7270;--ink:#0d111b;font-family:Inter,Segoe UI,Arial,sans-serif!important}
#dd3d-root .hud{background:linear-gradient(120deg,#09111ddf,#17202dc2)!important;border:1px solid #b7c5d533!important;border-radius:10px!important;box-shadow:0 12px 34px #0009!important;padding:10px 15px!important;backdrop-filter:blur(12px)}
#dd3d-root .hud .tiny{font-size:9px;color:#c7d1dd;letter-spacing:2px;font-weight:800}
#dd3d-root .hud .big{font-size:24px;color:#fff1d9;letter-spacing:.5px;font-weight:900}
#dd3d-root .hud .muted{font-size:10px;color:#b8b8c5}
#dd3d-root .mm{border:1px solid #c3b59466!important;border-radius:12px!important;box-shadow:0 8px 22px #000a,0 0 0 3px #0d131c66!important;opacity:.94}
#dd3d-root .cin-hotbar{display:flex;align-items:center;gap:4px;padding:5px 7px;border-radius:11px;background:linear-gradient(#161d2bdd,#0b121de8);box-shadow:0 10px 24px #000a;border:1px solid #d8bd8a55}
#dd3d-root .cin-hotbar .slot{min-width:64px;height:42px;max-width:80px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:1px solid #ffffff1b;border-radius:7px;background:#182231dd;color:#c8d4dd;font-weight:750;font-size:9px;line-height:1.15}
#dd3d-root .cin-hotbar .slot.active{border-color:#f4c67e;background:linear-gradient(145deg,#684829,#3b2d20);color:#fff7e6;box-shadow:inset 0 1px #ffe4ab4a,0 0 15px #c68e3570}
#dd3d-root .cin-hotbar .num{font-size:10px;color:#e9bd76;letter-spacing:1px}
#dd3d-root .cin-ammo{border:1px solid #d8c8a041!important;border-radius:12px!important;background:#0e1622e3!important;padding:10px 15px!important;box-shadow:0 8px 30px #0008;backdrop-filter:blur(8px)}
#dd3d-root .toast{font-weight:800;color:#ffeac2;letter-spacing:.7px;text-shadow:0 2px 4px #000,0 0 24px #000!important}
#dd3d-root .ov{color:#e9edf5;text-align:left!important;padding:0!important;background:#090e17!important;overflow-x:hidden;cursor:default!important}
#dd3d-root .cin-bg{position:absolute;inset:0;background:radial-gradient(ellipse at 12% 15%,#81371f65,transparent 48%),radial-gradient(ellipse at 86% 75%,#1764653e,transparent 45%),linear-gradient(115deg,#0d1019,#070e17);opacity:1;overflow:hidden;pointer-events:none}
#dd3d-root .cin-bg:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 3px,#ffffff08 4px);opacity:.18;mix-blend-mode:screen}
#dd3d-root .cin-bg:after{content:'';position:absolute;width:310px;height:310px;top:7%;right:19%;border:1px solid #cb775d45;border-radius:50%;box-shadow:0 0 90px #b44c2518,inset 0 0 100px #c8663020;animation:cinRotate 25s linear infinite}
@keyframes cinRotate{to{transform:rotate(360deg)}}
@keyframes cinGlow{50%{box-shadow:0 0 22px #c3915e65,inset 0 0 15px #d8a35e22}}
@keyframes cinRise{0%{transform:translateY(0);opacity:.0}15%{opacity:.8}100%{transform:translateY(-380px);opacity:0}}
#dd3d-root .cin-ember{position:absolute;bottom:-15px;width:2px;height:2px;border-radius:100%;background:#ffac69;box-shadow:0 0 9px #ff7f29;animation:cinRise 6s linear infinite}
#dd3d-root .cin-shell{position:relative;z-index:1;width:100%;height:100%;min-height:100%;margin:auto;display:flex;flex-direction:column;box-sizing:border-box;padding:16px 20px 14px;gap:10px}
#dd3d-root .cin-top{display:flex;justify-content:space-between;gap:8px;align-items:center;border-bottom:1px solid #e1c5a72b;padding-bottom:9px;font-size:10px;font-weight:800;letter-spacing:2.1px;color:#c2b5a3}
#dd3d-root .cin-brand{color:#f5c889;font-size:12px}
#dd3d-root .cin-main{display:grid;grid-template-columns:minmax(185px,.75fr) minmax(0,1.65fr);flex:1;gap:16px;min-height:0;align-content:center}
#dd3d-root .cin-left{display:flex;flex-direction:column;justify-content:center;min-width:0;padding:8px 4px 8px 0}
#dd3d-root .cin-tag{font-size:10px;font-weight:800;letter-spacing:2px;color:#8bd0c7;text-transform:uppercase;margin-bottom:12px}
#dd3d-root .cin-title{font-family:Impact,'Arial Narrow',system-ui,sans-serif;font-weight:900;font-size:clamp(31px,5.6vw,64px);line-height:.89;color:#fff0d1;letter-spacing:2px;text-shadow:0 0 32px #e48f4635;margin:0 0 13px}
#dd3d-root .cin-title span{display:block;color:#de8857}
#dd3d-root .cin-desc{font-size:11px;color:#b9bcc8;line-height:1.62;max-width:235px;margin:0 0 20px}
#dd3d-root .cin-metric{display:flex;gap:8px;flex-wrap:wrap}
#dd3d-root .cin-chip{font-size:10px;border:1px solid #ead0a63a;border-radius:5px;padding:6px 8px;color:#e5d2b6;background:#151c2699}
#dd3d-root .cin-panel{border:1px solid #c6a98446;border-radius:13px;background:linear-gradient(150deg,#202938e8,#0e1522ee);box-shadow:0 20px 48px #000b,inset 0 1px #ffffff10;padding:12px;min-width:0;overflow-y:auto;scrollbar-width:thin;scrollbar-color:#8e7059 transparent}
#dd3d-root .cin-tabs{display:flex;gap:6px;margin-bottom:12px}
#dd3d-root button.d3h{appearance:none;border:1px solid #abafbb36;cursor:pointer;color:#dce2ec;background:#1b2634;border-radius:7px;font:700 11px Inter,Segoe UI,Arial,sans-serif;transition:background .15s,transform .15s,border-color .15s;touch-action:manipulation}
#dd3d-root button.d3h:hover{background:#394657;transform:translateY(-1px);border-color:#e0b57a}
#dd3d-root button.d3h:focus-visible{outline:2px solid #83ded4;outline-offset:2px}
#dd3d-root .cin-tab{padding:8px 12px!important;flex:1}
#dd3d-root .cin-tab.selected{color:#121923!important;background:#f1c789!important;border-color:#e4a759!important}
#dd3d-root .cin-label{font-size:9px;font-weight:900;color:#93a9b9;letter-spacing:2px;margin:9px 0 7px}
#dd3d-root .cin-weapons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
#dd3d-root .cin-weapon{display:flex;flex-direction:column;align-items:flex-start;text-align:left;padding:9px 9px!important;min-height:58px}
#dd3d-root .cin-weapon.selected{border-color:#e0af68!important;background:#715139a8!important;box-shadow:inset 0 0 0 1px #e0af6866}
#dd3d-root .cin-gunno{font-size:9px;color:#c9aa82;letter-spacing:1px;margin-bottom:3px}
#dd3d-root .cin-gunname{font-size:11px;font-weight:900;color:#fff1e0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
#dd3d-root .cin-small{font-size:9px;color:#b6bdcb;margin-top:3px}
#dd3d-root .cin-opts{display:flex;flex-wrap:wrap;gap:6px}
#dd3d-root .cin-choice{padding:7px 10px!important}
#dd3d-root .cin-choice.selected{border-color:#e7b67b!important;color:#ffdaa5!important;background:#6c493058!important}
#dd3d-root .cin-play{font-size:13px!important;font-weight:900!important;letter-spacing:2px!important;padding:11px 17px!important;background:linear-gradient(125deg,#f7c782,#c58450)!important;color:#181315!important;border-color:#edc28e!important;flex:1;animation:cinGlow 2.2s ease-in-out infinite}
#dd3d-root .cin-actions{display:flex;gap:7px;margin-top:12px;align-items:center}
#dd3d-root .cin-secondary{padding:11px 14px!important;background:#27333e!important}
#dd3d-root .cin-note{color:#a7b4bf;font-size:10px;line-height:1.4;max-width:100%;margin-top:6px}
#dd3d-root .cin-statgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
#dd3d-root .cin-stat{border:1px solid #ffffff19;border-radius:7px;background:#ffffff08;text-align:center;padding:8px 2px;font-size:10px;color:#b6bec9}
#dd3d-root .cin-stat strong{display:block;color:#ffce8d;font-size:19px}
#dd3d-root .cin-foot{color:#9ca8b1;font-size:10px;border-top:1px solid #d7bd9427;padding-top:8px;display:flex;gap:13px;justify-content:center;flex-wrap:wrap}
#dd3d-root .cin-foot b{color:#f0cf9b;background:#ffffff10;border:1px solid #ffffff38;border-radius:4px;padding:1px 5px}
#dd3d-root .cin-perks{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
#dd3d-root .cin-perk{padding:15px 8px!important;min-height:110px;display:flex;flex-direction:column;align-items:center;text-align:center;justify-content:center;gap:8px}
@media(max-width:620px){#dd3d-root .cin-shell{padding:11px 13px 10px;gap:7px}#dd3d-root .cin-main{grid-template-columns:1fr;gap:8px}#dd3d-root .cin-left{padding:0;display:block}#dd3d-root .cin-title{font-size:27px;margin:2px 0 0}#dd3d-root .cin-title span{display:inline}#dd3d-root .cin-desc,#dd3d-root .cin-tag,#dd3d-root .cin-metric{display:none}#dd3d-root .cin-weapons{grid-template-columns:repeat(2,minmax(0,1fr))}#dd3d-root .cin-weapon{min-height:44px;padding:5px!important}#dd3d-root .cin-panel{padding:7px}#dd3d-root .cin-label{margin:5px 0}#dd3d-root .cin-top{padding-bottom:4px}}


/* Compact, unobtrusive eight-weapon HUD */
#dd3d-root .cin-hotbar{bottom:3px!important;left:50%!important;width:auto!important;max-width:270px!important;gap:2px!important;padding:3px 5px!important;background:#08111ab7!important;border:1px solid #c9b69350!important;opacity:.64;transform:translateX(-50%) scale(.87)!important;pointer-events:none!important}
#dd3d-root .cin-hotbar .slot{min-width:24px!important;max-width:26px!important;width:24px!important;height:25px!important;min-height:0!important;font-size:9px!important;background:transparent!important;gap:0!important;border:0!important;padding:0!important}
#dd3d-root .cin-hotbar .slot.active{min-width:98px!important;width:98px!important;max-width:98px!important;font-size:10px!important;background:#3d3025db!important;border:1px solid #ad865b!important}
#dd3d-root .cin-hotbar .slot:not(.active) .slot-name{display:none!important}
#dd3d-root .cin-hotbar .num{font-size:9px!important}
#dd3d-root .cin-launch{position:relative;z-index:1;height:100%;width:100%;background-position:center;background-size:cover;display:flex;align-items:center;justify-content:center;text-align:center;padding:18px;flex-direction:column;box-sizing:border-box;isolation:isolate;overflow:hidden}
#dd3d-root .cin-launch:before{content:'';position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#07090fb0,#0d08109e),radial-gradient(ellipse at 50% 60%,transparent 0%,#090913d8 90%)}
#dd3d-root .cin-launch::after{content:'';position:absolute;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(ellipse at 50% 100%,#9e3e2550,transparent 60%);animation:launchFog 5s ease-in-out infinite alternate}
#dd3d-root .launch-logo{font-family:Impact,'Arial Black',sans-serif;font-size:clamp(40px,8vw,90px);line-height:1.06;letter-spacing:4px;color:#f9e8cc;text-shadow:0 5px 13px #000,0 0 50px #c63f3280;animation:launchIn .7s ease-out both}
#dd3d-root .launch-logo em{font-style:normal;color:#ed5d3a}
#dd3d-root .launch-kicker{letter-spacing:5px;color:#eecb9d;font-size:11px;font-weight:900;margin:12px 0;text-shadow:0 3px 10px #000}
#dd3d-root .launch-button{font-weight:900!important;letter-spacing:3px!important;margin-top:22px;padding:14px 36px!important;color:#fbe8c9!important;background:#731e20df!important;border:1px solid #fc7856!important;box-shadow:0 0 34px #b83f3185;animation:cinGlow 2s ease-in-out infinite}
#dd3d-root .launch-progress{height:3px;width:min(290px,75%);background:#2b2427;border-radius:4px;overflow:hidden;margin-top:25px}
#dd3d-root .launch-progress>i{display:block;width:100%;height:100%;background:#d6754e;transform-origin:left;animation:launchProgress 4.3s linear forwards}
#dd3d-root .launch-diff{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;width:min(680px,100%);margin:25px auto 8px}
#dd3d-root .launch-diff button{min-height:114px!important;display:flex;align-items:center;justify-content:center;flex-direction:column;padding:14px!important;background:#121923eb!important;border-color:#ad6d5b!important}
#dd3d-root .launch-diff button:hover{background:#593127ee!important}
#dd3d-root .launch-diff span{font-size:24px;margin-bottom:6px}
#dd3d-root .launch-diff small{font-size:9px;color:#bfc3c9;margin-top:6px;line-height:1.4}
@keyframes launchIn{from{opacity:0;transform:scale(1.25);filter:blur(9px)}to{opacity:1;transform:scale(1);filter:blur(0)}}
@keyframes launchProgress{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes launchFog{to{opacity:.4;transform:scale(1.08)}}
@media(max-width:550px){#dd3d-root .launch-diff{grid-template-columns:1fr;gap:6px;margin:12px auto}#dd3d-root .launch-diff button{min-height:54px!important;padding:8px!important}#dd3d-root .launch-diff span{display:none}}
#dd3d-root .cin-weapon{min-height:48px!important;padding:6px 8px!important}
#dd3d-root .cin-label{margin:5px 0 4px!important}
#dd3d-root .cin-tabs{margin-bottom:6px!important}
#dd3d-root .cin-actions{margin-top:7px!important}
#dd3d-root .cin-play{padding:8px 14px!important}
#dd3d-root .cin-panel{padding:10px!important}
#dd3d-root .cin-opts .cin-choice{padding:6px 10px!important}
/* v4.5 slim tactical weapon selector, fixed centerline unobstructed */
#dd3d-root .cin-hotbar{bottom:5px!important;max-width:250px!important;width:250px!important;opacity:.90!important;transform:translateX(-50%) scale(.85)!important;display:flex!important;flex-direction:column!important;gap:3px!important;border:1px solid #b29c6b55!important;border-radius:9px!important;background:linear-gradient(130deg,#101826db,#080e16d8)!important;padding:5px 7px!important;box-shadow:0 5px 22px #000b!important;backdrop-filter:blur(6px)}
#dd3d-root .loadout-selected{display:flex;align-items:center;gap:8px;justify-content:center;min-height:25px}
#dd3d-root .loadout-icon{font-size:22px;filter:drop-shadow(0 0 4px #e9bd7688)}
#dd3d-root .loadout-label{display:flex;flex-direction:column;gap:2px;min-width:0}
#dd3d-root .loadout-kicker{font-size:8px;letter-spacing:1.7px;color:#b8b3a2;font-weight:700}
#dd3d-root .loadout-label strong{font-size:12px;line-height:1.1;color:#f2dfbf;text-overflow:ellipsis;white-space:nowrap;overflow:hidden}
#dd3d-root .loadout-keys{display:flex;justify-content:center;gap:5px}
#dd3d-root .loadout-key{font-size:9px;line-height:16px;text-align:center;width:18px;height:17px;color:#b5c1ca;border-radius:4px;border:1px solid #8295a43c;background:#1c2630bb}
#dd3d-root .loadout-key.current{color:#14151b;background:#efc582;box-shadow:0 0 8px #da974c99;font-weight:900}


`;
uiStyle.textContent += `

/* v5.1 — uncluttered, accessible menu language. One primary task per screen. */
#dd3d-root .ov{background:#070a0e!important;scrollbar-width:thin;}
#dd3d-root .ux-backdrop{position:absolute;inset:0;pointer-events:none;background-size:cover;background-position:50% 52%;filter:saturate(.82) contrast(1.06);}
#dd3d-root .ux-backdrop::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,9,14,.92) 0%,rgba(6,11,18,.67) 55%,rgba(4,8,14,.60) 100%),linear-gradient(0deg,rgba(3,7,12,.75),transparent 40%);}
#dd3d-root .ux-shell{position:relative;z-index:2;display:flex;flex-direction:column;width:100%;height:100%;min-height:0;box-sizing:border-box;padding:17px 25px 14px;gap:14px;color:#eee7dd;}
#dd3d-root .ux-top{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:9px;font-weight:700;color:#b8b7b6;letter-spacing:2px;line-height:1.4;}
#dd3d-root .ux-top .ux-mark{color:#dfbe90;letter-spacing:2.6px;}
#dd3d-root .ux-content{display:flex;flex:1;min-height:0;align-items:center;justify-content:flex-start;}
#dd3d-root .ux-card{box-sizing:border-box;width:min(420px,100%);min-height:0;max-height:100%;padding:7px 19px 7px 0;overflow-y:auto;scrollbar-width:thin;scrollbar-color:#967c5c transparent;}
#dd3d-root .ux-eyebrow{font-size:10px;letter-spacing:2.8px;text-transform:uppercase;font-weight:700;color:#d2aa77;margin:0 0 10px;}
#dd3d-root .ux-heading{font-size:clamp(27px,4.5vw,48px);letter-spacing:.2px;font-weight:650;line-height:1.07;color:#fff6e8;margin:0 0 9px;text-wrap:balance;}
#dd3d-root .ux-sub{font-size:12px;line-height:1.6;color:#c9c7c2;max-width:365px;margin:0 0 19px;}
#dd3d-root .ux-menu{display:flex;flex-direction:column;gap:7px;max-width:342px;}
#dd3d-root button.ux-item{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:left;padding:11px 14px!important;border-radius:9px!important;background:rgba(17,23,29,.82)!important;border:1px solid rgba(222,206,184,.18)!important;color:#f0ebe4!important;font-size:12px!important;font-weight:650!important;letter-spacing:.1px!important;min-height:41px;animation:none!important;box-shadow:none!important;}
#dd3d-root button.ux-item:hover{background:rgba(51,49,47,.94)!important;border-color:#c9ad84a8!important;transform:translateX(2px);}
#dd3d-root button.ux-item.ux-primary{background:linear-gradient(125deg,#e5c18d,#b78c61)!important;color:#211b17!important;border-color:#eacb9f!important;font-weight:850!important;}
#dd3d-root button.ux-item.ux-primary:hover{background:#f5d6a6!important;}
#dd3d-root .ux-arrow{font-size:17px;font-weight:400;line-height:1;opacity:.73;}
#dd3d-root .ux-caption{display:block;letter-spacing:.2px;font-size:10px;color:#aeb6bf;margin-top:5px;line-height:1.5;}
#dd3d-root .ux-metadata{font-size:10px;letter-spacing:.7px;color:#b4b6bc;line-height:1.6;margin-top:14px;}
#dd3d-root .ux-meta-accent{color:#eccb9c;}
#dd3d-root .ux-footer{color:#989da2;font-size:9px;letter-spacing:.3px;display:flex;align-items:center;justify-content:space-between;gap:12px;border-top:1px solid #ffffff25;padding-top:10px;}
#dd3d-root .ux-hint{white-space:nowrap;}
#dd3d-root .ux-section{font-size:10px;font-weight:800;letter-spacing:1.8px;color:#d0ae7e;margin:16px 0 9px;text-transform:uppercase;}
#dd3d-root .ux-gear{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;max-width:480px;}
#dd3d-root button.ux-weapon{padding:8px 10px!important;min-height:52px!important;text-align:left;background:#121920ce!important;border:1px solid #ffffff28!important;border-radius:8px!important;color:#e6e0d9!important;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:4px;}
#dd3d-root button.ux-weapon .ux-weapon-index{font-size:9px;font-weight:750;letter-spacing:1.2px;color:#adacb0;}
#dd3d-root button.ux-weapon .ux-weapon-name{font-size:12px;font-weight:750;}
#dd3d-root button.ux-weapon.selected{background:#51412ebc!important;border-color:#e6bf7e!important;box-shadow:inset 3px 0 #deb77f;}
#dd3d-root .ux-back ~ .ux-heading{font-size:clamp(28px,4.0vw,38px);}
#dd3d-root .ux-setting{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid #ffffff20;padding:10px 0;font-size:12px;}
#dd3d-root .ux-setting-controls{display:flex;align-items:center;gap:8px;flex-shrink:0;}
#dd3d-root button.ux-step{height:29px;width:29px;padding:0!important;border:1px solid #ffffff36!important;border-radius:6px!important;background:#202931!important;color:#fff!important;font-size:16px!important;}
#dd3d-root .ux-value{min-width:53px;text-align:center;color:#ecd3b0;font-variant-numeric:tabular-nums;font-weight:750;}
#dd3d-root .ux-options{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0;}
#dd3d-root button.ux-option{padding:9px 12px!important;background:#19222be8!important;border-radius:8px!important;color:#dfdfdf!important;font-size:11px!important;border:1px solid #ffffff35!important;}
#dd3d-root button.ux-option.selected{background:#7e6442!important;color:#fff!important;border-color:#d8b67f!important;}
#dd3d-root .ux-control-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:7px 0;border-bottom:1px solid #ffffff18;color:#d9dbdc;font-size:11px;}
#dd3d-root .ux-control-row kbd{font-size:10px;letter-spacing:.2px;color:#efcf9d;white-space:nowrap;font-family:inherit;}
#dd3d-root .ux-back{padding:5px 0!important;background:transparent!important;border:none!important;color:#d9bb8e!important;font-size:11px!important;font-weight:700!important;margin-bottom:6px;}
#dd3d-root .ux-back:hover{transform:none!important;color:#ffe6c2!important;text-decoration:underline;}
#dd3d-root .ux-statgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;max-width:355px;}
#dd3d-root .ux-stat{border:1px solid #ffffff22;border-radius:7px;padding:10px 9px;color:#bfc3c7;font-size:10px;background:#10171f9c;}
#dd3d-root .ux-stat strong{display:block;color:#f2d0a0;font-size:19px;margin-bottom:3px;}
#dd3d-root .ux-danger{color:#ffb4a5!important;}
#dd3d-root .ux-scroll{max-height:195px;overflow-y:auto;scrollbar-width:thin;}
/* Cinematic launch has only the title / a single action, difficulty stays readable. */
#dd3d-root .cin-launch{gap:0!important;}
#dd3d-root .cin-launch::before{background:linear-gradient(90deg,#070a10d9,#090c13af),radial-gradient(ellipse at 50% 62%,transparent 0%,#090b10c9 94%);}
#dd3d-root .launch-logo{font-family:Impact,'Arial Narrow',sans-serif;font-weight:750;font-size:clamp(42px,8vw,72px);line-height:1.02;letter-spacing:2px;text-shadow:0 8px 25px #000c;animation:launchIn .7s ease-out both;}
#dd3d-root .launch-logo em{color:#d4a67a;}
#dd3d-root .launch-kicker{font-size:10px;letter-spacing:2.4px;font-weight:750;margin:9px 0;color:#d9cabc;}
#dd3d-root button.launch-button{background:#e4bf8b!important;border:1px solid #ffddab!important;color:#1f1a17!important;padding:12px 30px!important;border-radius:8px!important;box-shadow:none!important;animation:none!important;letter-spacing:1.4px!important;margin-top:25px;}
#dd3d-root .launch-diff{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;width:min(595px,100%);margin:22px auto 6px;}
#dd3d-root .launch-diff button{background:#141c25db!important;border:1px solid #fff4e440!important;min-height:95px!important;padding:14px 12px!important;border-radius:9px!important;font-size:12px!important;line-height:1.4;}
#dd3d-root .launch-diff button:hover{background:#504231ec!important;border-color:#dfbb84!important;}
#dd3d-root .launch-diff span{font-size:11px;margin:0 0 5px;letter-spacing:1.2px;color:#ebc697;}
#dd3d-root .launch-diff small{font-size:10px;line-height:1.4;color:#c3c8ca;}
#dd3d-root .launch-progress{background:#ffffff20;height:2px;}
#dd3d-root .launch-progress>i{background:#cfa473;}
@media(max-width:540px){
 #dd3d-root .ux-shell{padding:12px 15px 10px;gap:8px;}
 #dd3d-root .ux-card{padding:8px 4px 8px 0;}
 #dd3d-root .ux-heading{font-size:29px;}
 #dd3d-root .ux-sub{font-size:11px;margin-bottom:13px;}
 #dd3d-root button.ux-item{min-height:38px;padding:8px 11px!important;}
 #dd3d-root button.ux-weapon{min-height:48px!important;padding:6px 9px!important;}
 #dd3d-root .ux-top{font-size:8px;}
 #dd3d-root .ux-footer{font-size:8px;}
 #dd3d-root .launch-diff{grid-template-columns:1fr;gap:6px;margin:14px auto 8px;max-width:340px;}
 #dd3d-root .launch-diff button{min-height:47px!important;display:grid;grid-template-columns:80px 1fr;text-align:left;padding:8px 12px!important;}
 #dd3d-root .launch-diff span{margin:0;}
 #dd3d-root .launch-diff small{margin:0;}
}
@media(prefers-reduced-motion:reduce){#dd3d-root .cin-launch:after,#dd3d-root .cin-ember,#dd3d-root .launch-logo{animation:none!important;}}
`;
wrap.appendChild(uiStyle);
hotbar.classList.add('cin-hotbar');ammoBox.classList.add('cin-ammo');
// Unified original vector icon library; no emoji fonts or external icon assets.
const iconSprite=document.createElementNS('http://www.w3.org/2000/svg','svg');
iconSprite.setAttribute('aria-hidden','true');
iconSprite.setAttribute('style','position:absolute;width:0;height:0;overflow:hidden;pointer-events:none');
iconSprite.innerHTML=`<symbol id="dd3d-i-pistol" viewBox="0 0 24 24"><path d="M4 12h7l2-3h6v3h-2l-2 6h-4l-1-4H7v5H4z"/></symbol>
<symbol id="dd3d-i-shotgun" viewBox="0 0 24 24"><path d="M2 9h16v3H2z M18 8h4v5h-4 M5 13l-2 7h5l3-7"/></symbol>
<symbol id="dd3d-i-smg" viewBox="0 0 24 24"><path d="M3 9h14l4 2-2 3h-5l-2 6H9l1-6H3z M7 7h8 M15 14l2 7"/></symbol>
<symbol id="dd3d-i-rifle" viewBox="0 0 24 24"><path d="M2 10h20v3H2z M5 8h10 M8 13l-3 7h4l4-7 M17 13l4 4"/></symbol>
<symbol id="dd3d-i-grenade" viewBox="0 0 24 24"><path d="M3 8h14l4 3-4 4H3z M6 6h6 M8 15l-2 5h5l2-5"/></symbol>
<symbol id="dd3d-i-flame" viewBox="0 0 24 24"><path d="M3 11h12l4-2 M7 11l-2 8h5l2-8 M19 5c3 3 3 5 1 6 M19 5c-2 2-2 4 0 6"/></symbol>
<symbol id="dd3d-i-katana" viewBox="0 0 24 24"><path d="M4 21L18 4l2-2-1 4L7 21 M5 16l4 4 M3 18l4 4"/></symbol>
<symbol id="dd3d-i-saber" viewBox="0 0 24 24"><path d="M4 21L18 6 M7 18l4 3 M18 6l3-4 M15 9l2 2 M2 4l3 1 M20 16l2 1"/></symbol>
<symbol id="dd3d-i-health" viewBox="0 0 24 24"><path d="M12 21S3 14.8 3 8.5A5 5 0 0 1 12 6a5 5 0 0 1 9 2.5C21 14.8 12 21 12 21z"/></symbol>
<symbol id="dd3d-i-armor" viewBox="0 0 24 24"><path d="M12 2l8 4v6c0 5-4 8-8 10-4-2-8-5-8-10V6z M9 12l2 2 4-4"/></symbol>
<symbol id="dd3d-i-stamina" viewBox="0 0 24 24"><path d="M13 2L4 13h7l-1 9 10-13h-7z"/></symbol>
<symbol id="dd3d-i-ammo" viewBox="0 0 24 24"><path d="M8 3h8v18H8z M8 8h8 M12 3v5"/></symbol>
<symbol id="dd3d-i-fire" viewBox="0 0 24 24"><path d="M12 22c5 0 8-4 8-9 0-5-4-8-5-10-2 4-4 5-5 7-1-2-1-4-1-5C5 10 4 13 4 16c0 4 3 6 8 6z"/></symbol>
<symbol id="dd3d-i-key" viewBox="0 0 24 24"><path d="M9 14a5 5 0 1 1 5-5l-6 6-2-2-2 2-2-2z"/></symbol>
<symbol id="dd3d-i-coin" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20 M9 9c0-3 6-3 6 0s-6 2-6 5 6 3 6 0 M12 5v14"/></symbol>
<symbol id="dd3d-i-shrine" viewBox="0 0 24 24"><path d="M12 2L3 10h18z M6 10v10 M12 10v10 M18 10v10 M3 22h18"/></symbol>
<symbol id="dd3d-i-portal" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 1 0 0-20 M12 6c-4 3-4 9 0 12 4-3 4-9 0-12 M6 12h12"/></symbol>
<symbol id="dd3d-i-skull" viewBox="0 0 24 24"><path d="M12 2a8 8 0 0 0-8 8v5l4 3v4h8v-4l4-3v-5a8 8 0 0 0-8-8z M8 11h1 M15 11h1 M10 16h4"/></symbol>
<symbol id="dd3d-i-objective" viewBox="0 0 24 24"><path d="M12 2v4 M12 18v4 M2 12h4 M18 12h4 M12 7a5 5 0 1 0 0 10 5 5 0 1 0 0-10"/></symbol>
<symbol id="dd3d-i-boss" viewBox="0 0 24 24"><path d="M4 10L2 2l6 4 4-4 4 4 6-4-2 8v10H4z M8 14h1 M15 14h1"/></symbol>
<symbol id="dd3d-i-xp" viewBox="0 0 24 24"><path d="M12 2l9 10-9 10L3 12z M12 2v20 M3 12h18"/></symbol>
<symbol id="dd3d-i-combo" viewBox="0 0 24 24"><path d="M4 20l4-16 4 8 4-8 4 16z"/></symbol>
<symbol id="dd3d-i-damage" viewBox="0 0 24 24"><path d="M12 2l2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5z"/></symbol>
<symbol id="dd3d-i-firerate" viewBox="0 0 24 24"><path d="M3 12h3 M9 12h3 M15 12h6 M8 3l4 4 4-4 M8 21l4-4 4 4"/></symbol>
<symbol id="dd3d-i-life" viewBox="0 0 24 24"><path d="M20 7c-3-3-6-1-8 1-2-2-5-4-8-1-4 4 0 9 8 14 8-5 12-10 8-14z M12 8v8 M8 12h8"/></symbol>
<symbol id="dd3d-i-pack" viewBox="0 0 24 24"><path d="M5 9V7c0-4 14-4 14 0v2 M4 9h16v12H4z M9 9v12 M15 9v12"/></symbol>
<symbol id="dd3d-i-speed" viewBox="0 0 24 24"><path d="M3 12h4 M3 16h6 M3 8h6 M12 4l8 8-8 8 M20 12H9"/></symbol>
<symbol id="dd3d-i-helmet" viewBox="0 0 24 24"><path d="M4 13a8 8 0 0 1 16 0v5H4z M4 15h4 M16 15h4"/></symbol>
<symbol id="dd3d-i-chest" viewBox="0 0 24 24"><path d="M8 3l4 2 4-2 5 5-3 4v10H6V12L3 8z"/></symbol>
<symbol id="dd3d-i-gauntlet" viewBox="0 0 24 24"><path d="M8 4v7 M11 3v8 M14 4v7 M17 7v5l3-2v5l-5 7H7l-4-9v-2l3 1V6z"/></symbol>
<symbol id="dd3d-i-legs" viewBox="0 0 24 24"><path d="M6 2h12l-2 20h-5l1-12-2 12H5z"/></symbol>
<symbol id="dd3d-i-relic" viewBox="0 0 24 24"><path d="M12 2l8 5v10l-8 5-8-5V7z M12 7l4 5-4 5-4-5z"/></symbol>
<symbol id="dd3d-i-settings" viewBox="0 0 24 24"><path d="M12 3v3 M12 18v3 M3 12h3 M18 12h3 M5.6 5.6l2.2 2.2 M16.2 16.2l2.2 2.2 M18.4 5.6l-2.2 2.2 M7.8 16.2l-2.2 2.2 M12 8a4 4 0 1 0 0 8 4 4 0 1 0 0-8"/></symbol>
<symbol id="dd3d-i-volume" viewBox="0 0 24 24"><path d="M3 9v6h4l6 5V4L7 9z M16 9c2 1 2 5 0 6 M19 6c4 3 4 9 0 12"/></symbol>
<symbol id="dd3d-i-mute" viewBox="0 0 24 24"><path d="M3 9v6h4l6 5V4L7 9z M17 9l5 6 M22 9l-5 6"/></symbol>
<symbol id="dd3d-i-music" viewBox="0 0 24 24"><path d="M10 18V5l10-3v13 M10 18c0 4-8 5-8 1s8-5 8-1 M20 15c0 4-8 5-8 1s8-5 8-1"/></symbol>
<symbol id="dd3d-i-stats" viewBox="0 0 24 24"><path d="M4 20V12h4v8 M10 20V4h4v16 M16 20v-9h4v9"/></symbol>
<symbol id="dd3d-i-trophy" viewBox="0 0 24 24"><path d="M6 3h12v8a6 6 0 0 1-12 0z M6 6H3v3a4 4 0 0 0 4 4 M18 6h3v3a4 4 0 0 1-4 4 M12 17v4 M7 21h10"/></symbol>
<symbol id="dd3d-i-lock" viewBox="0 0 24 24"><path d="M5 10h14v12H5z M8 10V7a4 4 0 0 1 8 0v3 M12 15v3"/></symbol>
<symbol id="dd3d-i-play" viewBox="0 0 24 24"><path d="M6 3l15 9-15 9z"/></symbol>
<symbol id="dd3d-i-pause" viewBox="0 0 24 24"><path d="M6 3h4v18H6z M14 3h4v18h-4z"/></symbol>
<symbol id="dd3d-i-restart" viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 3-7 M3 4v6h6"/></symbol>
<symbol id="dd3d-i-menu" viewBox="0 0 24 24"><path d="M3 6h18 M3 12h18 M3 18h18"/></symbol>
<symbol id="dd3d-i-gamepad" viewBox="0 0 24 24"><path d="M6 7h12l4 10-3 3-4-4H9l-4 4-3-3z M7 12h5 M9.5 9.5v5 M17 11h.1 M19 13h.1"/></symbol>
<symbol id="dd3d-i-keyboard" viewBox="0 0 24 24"><path d="M2 6h20v12H2z M5 9h1 M9 9h1 M13 9h1 M17 9h1 M5 13h1 M9 13h1 M13 13h1 M17 13h1 M6 16h12"/></symbol>
<symbol id="dd3d-i-map" viewBox="0 0 24 24"><path d="M3 5l6-3 6 3 6-3v17l-6 3-6-3-6 3z M9 2v17 M15 5v17"/></symbol>
<symbol id="dd3d-i-arrow" viewBox="0 0 24 24"><path d="M5 12h14 M14 7l5 5-5 5"/></symbol>`;
wrap.appendChild(iconSprite);
function iconMark(id,size=20){return '<svg aria-hidden="true" class="dd-icon" width="'+size+'" height="'+size+'" viewBox="0 0 24 24"><use href="#dd3d-i-'+id+'"/></svg>';}
uiStyle.textContent+='\n#dd3d-root .dd-icon{display:inline-block;vertical-align:middle;fill:none;stroke:currentColor;stroke-width:1.65;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}#dd3d-root .cin-perk .dd-icon{color:#e5be8c}#dd3d-root .forge-card .dd-icon{color:#f1c789;margin-right:5px}';

// Keep the transient hotbar out of the interaction-prompt zone.
uiStyle.textContent+='\n#dd3d-root .cin-hotbar{bottom:4px!important;left:50%!important;width:auto!important;max-width:240px!important;flex-direction:row!important;padding:3px!important;opacity:var(--hotbar-opacity,0)!important;transition:opacity .24s ease!important}#dd3d-root .hud{max-width:240px!important;box-sizing:border-box;font-size:11px!important;line-height:1.35!important}#dd3d-root .toast{bottom:82px!important}#dd3d-root .cin-ammo{right:12px!important;bottom:12px!important;max-width:190px!important}';

const RND=Math.random.bind(Math);
function reseed(a){ Math.random=function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function dailySeed(){ const d=new Date(); return d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate(); }
function save(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
function load(k,d){ try{ return Object.assign(Array.isArray(d)?[]:{},d,JSON.parse(localStorage.getItem(k)||'null')); }catch(e){ return d; } }
const SET=load('d3d_set',{sens:1,fov:72,vol:1,music:0.75,sfx:1,ambient:0.75,quality:1,mute:false});
for(const [k,lo,hi,def] of [['sens',.1,3,1],['fov',60,100,72],['vol',0,1,1],['music',0,1,.75],['sfx',0,1,1],['ambient',0,1,.75],['quality',.5,1.5,1]]){
  SET[k]=Number.isFinite(+SET[k])?Math.max(lo,Math.min(hi,+SET[k])):def;
}
const STATS=load('d3d_stats',{runs:0,kills:0,deaths:0,floors:0,ach:{}});
let BOARD=[]; try{ BOARD=JSON.parse(localStorage.getItem('d3d_board')||'[]'); }catch(e){}
const ACHS={first:'First Blood|Get your first kill',boss:'Demon Slayer|Defeat a boss',f5:'Deep Diver|Reach floor 5',combo:'Combo Master|Reach a x5 combo',rail:'Collateral|Hit 3 enemies with a single shot',barrel:'Boom!|Kill an enemy with an explosive barrel'};
function award(id){ if(STATS.ach[id]) return; STATS.ach[id]=1; save('d3d_stats',STATS); toast('[Achievement] Achievement: '+ACHS[id].split('|')[0],2800); }
const VW=800, VH=700, CELL=4, WALLH=6.8;

// ---------- renderer / scene ----------
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'high-performance'});
renderer.outputEncoding=THREE.sRGBEncoding;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=0.80;
if(renderer.shadowMap)renderer.shadowMap.enabled=SET.quality>=0.9;
if(renderer.shadowMap)renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.setPixelRatio(Math.min(2,(window.devicePixelRatio||1)*SET.quality));
renderer.setSize(VW,VH);
renderer.domElement.style.cssText='display:block;width:100%;height:100%';
wrap.insertBefore(renderer.domElement, wrap.firstChild);
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x050508);
scene.fog=new THREE.Fog(0x050508,2,28);
const camera=new THREE.PerspectiveCamera(SET.fov,VW/VH,0.1,100);
camera.rotation.order='YXZ';
scene.add(camera);
// Independent first-person viewmodel: rendered after the world with cleared depth.
const viewScene=new THREE.Scene();
const viewCamera=new THREE.PerspectiveCamera(58,VW/VH,0.01,10);
viewScene.add(viewCamera);
viewScene.add(new THREE.AmbientLight(0x9da7ba,0.37));
const bossHud=document.createElement('div');bossHud.style.cssText='position:absolute;left:25%;top:8px;width:50%;z-index:8;display:none;pointer-events:none;text-align:center;color:#f7d2c1;font:bold 12px system-ui;text-shadow:0 2px 5px #000';
bossHud.innerHTML='<div id="boss-v5-name"></div><div style="height:9px;background:#1a1022;border:1px solid #d78b6c;border-radius:8px;overflow:hidden"><div id="boss-v5-meter" style="height:100%;background:linear-gradient(90deg,#bd292b,#ef946b);width:100%"></div></div>';
wrap.appendChild(bossHud);

scene.add(new THREE.AmbientLight(0x272136,0.26));
const torch=new THREE.PointLight(0xffb060,0.75,13,2);
scene.add(torch);
// A real, camera-directed cone, distinct from the warm nearby torch illumination.
let flashlightOn=true;
const flashlight=new THREE.SpotLight(0xcadfff,0.62,28,Math.PI/7,.65,2);
flashlight.position.set(0,.02,0);
flashlight.target=flashlight.target||new THREE.Object3D();
flashlight.target.position.set(0,-.08,-8);
flashlight.castShadow=SET.quality>=.9;
if(flashlight.shadow&&flashlight.shadow.mapSize){flashlight.shadow.mapSize.width=512;flashlight.shadow.mapSize.height=512;flashlight.shadow.bias=-.0004;}
camera.add(flashlight);camera.add(flashlight.target);

// Shared dungeon material helper. Barrels and wall torches use this; keep it
// in the startup scope so no spawn path can throw `GM is not defined`.
const GM=(color,emissive=0)=>new THREE.MeshStandardMaterial({
  color:color,emissive:emissive,metalness:0.45,roughness:0.65
});

// ---------- anatomically shaped first-person hand assets ----------
// Original procedural models: textured skin under fingerless tactical gloves,
// five curled fingers with separate joints, asymmetrical palm and an opposable thumb.
const HAND_TEXTURES=(function(){
  function texture(base,seed){
    const c=document.createElement('canvas');c.width=c.height=256;
    const a=c.getContext('2d');a.fillStyle=base;a.fillRect(0,0,256,256);
    let n=seed>>>0;const rand=()=>{n=(Math.imul(n,1664525)+1013904223)>>>0;return n/4294967296;};
    for(let i=0;i<11000;i++){
      const x=rand()*256,y=rand()*256,r=.4+rand()*1.5;
      a.fillStyle=rand()>.54?'rgba(233,222,204,.08)':'rgba(12,17,19,.09)';
      a.fillRect(x,y,r,r);
    }
    // Fine diagonal seams visible under grazing light.
    a.strokeStyle='rgba(0,0,0,.09)';a.lineWidth=.65;
    for(let j=-256;j<512;j+=8){a.beginPath();a.moveTo(j,0);a.lineTo(j+256,256);a.stroke();}
    const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;return t;
  }
  const leather=texture('#45474b',9821),skin=texture('#92735b',13133),cloth=texture('#272e33',4401);
  return {
    leather:new THREE.MeshStandardMaterial({map:leather,bumpMap:leather,bumpScale:.027,color:0xd1d1d1,metalness:.02,roughness:.76}),
    skin:new THREE.MeshStandardMaterial({map:skin,bumpMap:skin,bumpScale:.018,color:0xe4b494,metalness:0,roughness:.81}),
    cloth:new THREE.MeshStandardMaterial({map:cloth,bumpMap:cloth,bumpScale:.021,color:0xb5bbc2,roughness:.96}),
    rubber:new THREE.MeshStandardMaterial({color:0x161a1d,roughness:.9}),
    armor:new THREE.MeshStandardMaterial({color:0x65676b,metalness:.36,roughness:.55}),
    nail:new THREE.MeshStandardMaterial({color:0xb68d78,roughness:.46})
  };
})();
function createRealHand(parent,position,secondary=false,melee=false,opts={}){
  const m=HAND_TEXTURES,root=new THREE.Group();root.position.set(...position);
  const gripCurl=opts.gripCurl!==undefined?opts.gripCurl:(melee?1.06:1.26);
  root.rotation.set(opts.rx!==undefined?opts.rx:(melee?.05:.10), opts.ry!==undefined?opts.ry:(secondary?-.18:.12), opts.rz!==undefined?opts.rz:(secondary?.25:-.12));
  if(opts.scale)root.scale.setScalar(opts.scale);
  parent.add(root);
  const ell=(g,x,y,z,a,b,c,mat)=>{
    const mesh=new THREE.Mesh(new THREE.SphereGeometry(1,20,14),mat);
    mesh.position.set(x,y,z);mesh.scale.set(a,b,c);g.add(mesh);return mesh;
  };
  const section=(g,A,B,radA,radB,mat)=>{
    const p=new THREE.Vector3(...A),q=new THREE.Vector3(...B),v=q.clone().sub(p);
    const bone=new THREE.Mesh(new THREE.CylinderGeometry(radB,radA,v.length(),12),mat);
    bone.position.copy(p).add(q).multiplyScalar(.5);
    bone.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());g.add(bone);return bone;
  };
  // The forearm widens toward the elbow and rolls into a narrow flexible wrist.
  section(root,[secondary?-.16:.13,-.44,.24],[-.025,-.11,.055],.128,.084,m.cloth);
  ell(root,-.018,-.11,.056,.09,.085,.095,m.leather);
  const cuff=new THREE.Mesh(new THREE.TorusGeometry(.093,.012,9,28),m.armor);
  cuff.position.set(-.018,-.115,.055);cuff.rotation.x=Math.PI/2;root.add(cuff);
  const palm=ell(root,-.005,-.023,-.016,.103,.100,.116,m.leather);
  palm.rotation.z=secondary?.08:-.07;palm.rotation.x=.23;
  // Rounded thenar/hypothenar volumes give a hand silhouette, not a box.
  ell(root,secondary?-.077:.076,-.042,.026,.049,.082,.078,m.leather);
  ell(root,secondary?.060:-.065,-.052,.015,.039,.074,.07,m.leather);
  ell(root,0,.052,-.056,.093,.031,.047,m.armor);
  // A real transform hierarchy per finger: every distal phalanx moves with
  // the preceding joint rather than three independent, disconnected sticks.
  const fingers=[];const lengths=[.92,1.10,1.06,.85];
  for(let i=0;i<4;i++){
    const x=(i-1.5)*.047,k=lengths[i],finger=new THREE.Group();
    finger.position.set(x,.058,-.061);
    finger.rotation.x=gripCurl*.32+(opts.fingerBias||0);
    finger.rotation.z=(i-1.5)*.045*(secondary?-1:1);root.add(finger);
    const points=[[0,0,0],[x*.07,-.059*k,.015],[x*.10,-.104*k,.043],[x*.14,-.139*k,.078]];
    let chain=finger;const phalanges=[];
    for(let j=0;j<3;j++){
      const a=points[j],b=points[j+1],seg=[b[0]-a[0],b[1]-a[1],b[2]-a[2]];
      const joint=new THREE.Group();
      if(j>0)joint.position.set(points[j][0]-points[j-1][0],points[j][1]-points[j-1][1],points[j][2]-points[j-1][2]);
      chain.add(joint);
      joint.rotation.x=j===0?0:(j===1?.33:.35)*gripCurl;
      const r0=(.022-j*.0035)*k,r1=(.021-j*.0035)*k;
      section(joint,[0,0,0],seg,r0,r1,j===0?m.leather:m.skin);
      ell(joint,seg[0],seg[1],seg[2],r1*1.05,r1*1.02,r1*1.1,j===0?m.leather:m.skin);
      if(j===1)ell(joint,seg[0],seg[1]+.004,seg[2]+.013,r1*.72,r1*.27,r1*.6,m.rubber);
      if(j===2){const nail=ell(joint,seg[0],seg[1]-.003,seg[2]+.016,.011,.007,.014,m.nail);nail.rotation.x=.35;}
      phalanges.push(joint);chain=joint;
    }
    ell(root,x,.042,-.092,.027,.026,.022,m.armor);
    finger.userData.phalanges=phalanges;
    finger.userData.curl=gripCurl;
    fingers.push(finger);
  }
  // Opposable thumb wraps across the index finger, with separate visible joints.
  const thumb=new THREE.Group();thumb.position.set(secondary?-.086:.087,-.025,.041);
  thumb.rotation.set(.5,0,secondary?.75:-.81);root.add(thumb);
  const sg=secondary?-1:1;
  const pts=[[0,0,0],[sg*.014,-.046,-.027],[sg*.029,-.089,-.087],[sg*.031,-.101,-.123]];
  let thumbChain=thumb;const thumbJoints=[];
  for(let j=0;j<3;j++){
    const a=pts[j],b=pts[j+1];const delta=[b[0]-a[0],b[1]-a[1],b[2]-a[2]];
    const joint=new THREE.Group();
    if(j>0)joint.position.set(pts[j][0]-pts[j-1][0],pts[j][1]-pts[j-1][1],pts[j][2]-pts[j-1][2]);
    joint.rotation.x=j===1?.18*gripCurl:j===2?.22*gripCurl:0;
    thumbChain.add(joint);
    section(joint,[0,0,0],delta,.03-j*.004,.026-j*.004,j===0?m.leather:m.skin);
    ell(joint,delta[0],delta[1],delta[2],.027-j*.003,.023-j*.002,.026-j*.003,j===0?m.leather:m.skin);
    if(j===2)ell(joint,delta[0],delta[1]-.007,delta[2]+.014,.014,.006,.013,m.nail);
    thumbJoints.push(joint);thumbChain=joint;
  }
  thumb.userData.joints=thumbJoints;
  // Kevlar stitching and strap detail sit above the organic silhouette.
  for(const sign of [-1,1]){
    section(root,[sign*.075,-.075,.091],[sign*.062,-.04,.11],.005,.004,m.armor);
  }
  root.userData.fingers=fingers;root.userData.thumb=thumb;
  root.userData.baseCurl=gripCurl;
  root.userData.restRotation={x:root.rotation.x,y:root.rotation.y,z:root.rotation.z};
  root.userData.restPosition=root.position.clone();
  root.userData.melee=melee;
  return root;
}

// ---------- handcrafted real-world-inspired weapon viewmodels ----------
// A compact mesh kit; these are original procedural 3D models, not proprietary game assets.
const gun=new THREE.Group();
gun.position.set(0.37,-0.36,-0.68);
viewScene.add(gun);
const gunModels=Array.from({length:8},function(_,i){
  const group=new THREE.Group(); group.visible=i===0; group.userData={}; gun.add(group); return group;
});
(function buildWeapons(){
  const mat=(c,m=0.5,r=0.48,e=0)=>new THREE.MeshStandardMaterial({color:c,metalness:m,roughness:r,emissive:e});
  const gunmetal=mat(0x25282e,.84,.3), parker=mat(0x393d41,.8,.37), black=mat(0x101317,.58,.53);
  const edge=mat(0x626970,.87,.3), bright=mat(0xc1c5c4,.96,.22), satin=mat(0x777f81,.93,.29);
  const polymer=mat(0x292e31,.12,.8), polymer2=mat(0x44494b,.12,.74), rubber=mat(0x15181a,.02,.9);
  const cherry=mat(0x8a4826,.12,.44), beech=mat(0xa86937,.13,.42), highlight=mat(0xd69353,.12,.45);
  const bakelite=mat(0x59352c,.2,.52), olive=mat(0x515b43,.16,.74), brass=mat(0xb59250,.82,.31);
  const fuel=mat(0x5d6c59,.4,.48), warning=mat(0xd3a43b,.16,.65), glow=mat(0xffac40,.06,.4,0xff6000);
  const glove=mat(0x373b3c,.08,.95), seam=mat(0x1e2426,.08,.92);
  const b=(g,w,h,d,x,y,z,m)=>{const a=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);a.position.set(x,y,z);g.add(a);return a;};
  const sphere=(g,r,x,y,z,m,sx=1,sy=1,sz=1)=>{const a=new THREE.Mesh(new THREE.SphereGeometry(r,16,12),m);a.position.set(x,y,z);a.scale.set(sx,sy,sz);g.add(a);return a;};
  const cyl=(g,r,len,x,y,z,m,axis='z',r2=r)=>{
    const a=new THREE.Mesh(new THREE.CylinderGeometry(r,r2,len,16),m);
    if(axis==='z') a.rotation.x=Math.PI/2;
    if(axis==='x') a.rotation.z=Math.PI/2;
    a.position.set(x,y,z);g.add(a);return a;
  };
  const rod=(g,a,b2,r,m)=>{
    const p=new THREE.Vector3(...a),q=new THREE.Vector3(...b2),v=q.clone().sub(p);
    const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r,r,v.length(),9),m);
    mesh.position.copy(p.add(q).multiplyScalar(.5));
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());g.add(mesh);return mesh;
  };
  const outline=(g,pts,width,m,bevel=.005)=>{
    // The polygon is drawn on the side (y/z) then extruded across the gun's width.
    const s=new THREE.Shape();pts.forEach((p,i)=>{if(!i)s.moveTo(-p[0],p[1]);else s.lineTo(-p[0],p[1]);});s.closePath();
    const geo=new THREE.ExtrudeGeometry(s,{depth:width,steps:1,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel,bevelSegments:2,curveSegments:3});
    const mesh=new THREE.Mesh(geo,m);mesh.rotation.y=Math.PI/2;mesh.position.x=-width/2;g.add(mesh);return mesh;
  };
  const screws=(g,pts,x,m)=>pts.forEach(([y,z])=>{
    cyl(g,.011,.004,x,y,z,m,'x'); b(g,.003,.002,.014,x+Math.sign(x)*.004,y,z,black);
  });
  const gripLines=(g,z0,y0,width,height,x,m,n=8,angle=0)=>{
    for(let k=0;k<n;k++){
      const y=y0+height*(k+.5)/n;
      const o=b(g,.003,.0025,width,x,y,z0+(y-y0)*angle,m);
      o.rotation.x=.15;
    }
  };
  const rail=(g,z1,z2,y,w,m)=>{
    b(g,w,.016,z2-z1,0,y,(z1+z2)/2,m);
    for(let z=z1+.018;z<z2-.005;z+=.045) b(g,w+.018,.012,.017,0,y+.014,z,edge);
  };
  const ring=(g,r,x,y,z,m,t=.012)=>{const a=new THREE.Mesh(new THREE.TorusGeometry(r,t,7,24),m);a.position.set(x,y,z);g.add(a);return a;};
  const guard=(g,pts,m,r=.01)=>{for(let i=0;i<pts.length-1;i++)rod(g,pts[i],pts[i+1],r,m);};
  const wire=(g,pts,m,r=.01)=>guard(g,pts,m,r);
  const label=(g,message,x,y,z,w=.22,h=.027)=>{
    const cv=document.createElement('canvas');cv.width=512;cv.height=64;
    const ctx=cv.getContext('2d');ctx.fillStyle='#ddd6c6';ctx.font='bold 36px Arial';ctx.textAlign='center';ctx.fillText(message,256,44);
    const t=new THREE.CanvasTexture(cv);t.anisotropy=4;
    const a=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:t,transparent:true,depthWrite:false,side:THREE.DoubleSide}));
    a.rotation.y=Math.PI/2;a.position.set(x,y,z);g.add(a);
  };
  const hand=(g,z,y,secondary=false,opts={})=>{
    const rig=createRealHand(g,[secondary?-.115:.115,y,z],secondary,false,opts);
    g.userData.handRigs=g.userData.handRigs||[];
    g.userData.handRigs.push(rig);return rig;
  };
  const poseHand=(rig,pos,rot,curl)=>{
    if(pos)rig.position.set(pos[0],pos[1],pos[2]);
    if(rot)rig.rotation.set(rot[0],rot[1],rot[2]);
    rig.userData.restPosition=rig.position.clone();
    rig.userData.restRotation={x:rig.rotation.x,y:rig.rotation.y,z:rig.rotation.z};
    if(curl!==undefined){rig.userData.baseCurl=curl; for(const f of rig.userData.fingers){f.rotation.x=curl*.32;if(f.userData.phalanges)for(let j=1;j<3;j++)f.userData.phalanges[j].rotation.x=(j===1?.33:.35)*curl;}}
    return rig;
  };
  const use=(i)=>{const g=gunModels[i];g.userData.baseX=0;return g;};

  // 1. Magnum Research Desert Eagle Mk XIX: slab-sided slide, heavy barrel, rail,
  // triangular muzzle and large swept grip distinctive of the original .50 AE pistol.
  {
    const g=use(0),moving=new THREE.Group();g.add(moving);
    outline(g,[[.18,-.035],[.04,-.055],[-.12,-.04],[-.22,-.05],[-.26,-.09],[-.30,-.105],[-.38,-.105],[-.39,-.02],[-.21,.02],[.17,.02]],.105,satin);
    outline(moving,[[.2,.028],[.16,.096],[-.28,.096],[-.43,.06],[-.47,.018],[-.44,-.006],[-.08,-.01],[.12,-.008]],.119,gunmetal);
    b(moving,.12,.02,.35,0,.102,-.20,edge);
    for(let j=0;j<9;j++)b(moving,.124,.008,.008,0,.114,-.41+j*.044,black);
    for(const x of [-.061,.061])for(let j=0;j<9;j++){
      let z=.125-j*.016;
      b(moving,.004,.056,.007,x,.04,z,edge).rotation.x=.34;
    }
    b(moving,.06,.012,.125,0,.098,-.20,black);
    cyl(g,.025,.11,0,.003,-.48,black);ring(g,.034,0,.003,-.535,satin,.009);
    outline(g,[[.13,-.02],[.24,-.06],[.26,-.27],[.22,-.32],[.10,-.3],[.05,-.1]],.092,polymer);
    for(const x of [-.048,.048]){
      outline(g,[[.135,-.075],[.229,-.11],[.225,-.271],[.136,-.245],[.1,-.14]],.007,rubber);
      gripLines(g,.17,-.23,.053,.115,x,polymer2,7,.15);
    }
    b(g,.105,.017,.09,0,-.306,.20,gunmetal);
    guard(g,[[0,-.038,.04],[0,-.105,-.015],[0,-.107,-.12],[0,-.056,-.14]],gunmetal,.011);
    rod(g,[0,-.043,.0],[0,-.089,-.026],.014,black);
    cyl(g,.018,.135,0,-.045,.17,black,'x');
    sphere(g,.014,.064,.013,.10,satin);
    b(g,.06,.015,.017,0,.134,.153,black);
    b(g,.04,.026,.018,0,.126,-.391,black);
    label(moving,'DESERT EAGLE · .50 AE',.068,.053,-.19,.30,.022);
    screws(g,[[.005,.09],[-.244,.189]],.065,bright);
    const h0=hand(g,.17,-.17,false,{rx:.24,ry:.22,rz:-.40,gripCurl:1.34,scale:1.02});
    const h1=hand(g,.24,-.18,true,{rx:.38,ry:-.06,rz:.62,gripCurl:1.42,scale:1.0});
    poseHand(h0,[.118,-.168,.168],[.24,.23,-.42],1.34);
    poseHand(h1,[-.038,-.184,.238],[.34,.04,.71],1.42);
    g.userData.slide=moving;g.userData.slideBaseZ=0;
    g.userData.muzzle={x:0,y:.01,z:-.54};
  }

  // 2. Remington 870: twin barrel/tube, pump with scored walnut, receiver and stock.
  {
    const g=use(1);
    cyl(g,.023,.93,0,.055,-.52,gunmetal);
    cyl(g,.022,.73,0,-.012,-.41,gunmetal);
    ring(g,.029,0,.055,-.985,satin,.006);
    cyl(g,.04,.035,0,.04,-.855,black);
    outline(g,[[.2,-.06],[.19,.085],[-.15,.085],[-.19,.05],[-.18,-.05]],.148,gunmetal);
    b(g,.1,.014,.34,0,.089,-.02,edge);
    for(let k=0;k<5;k++)b(g,.15,.008,.015,0,.075,-.13+k*.042,satin);
    const pump=new THREE.Group();g.add(pump);
    outline(pump,[[.015,.045],[-.10,.045],[-.12,-.076],[-.38,-.076],[-.41,-.015],[-.42,.022],[-.23,.067]],.13,cherry);
    for(let i=0;i<11;i++){
      const z=-.39+i*.027;
      b(pump,.133,.005,.008,0,-.08,z,bakelite);
    }
    b(g,.095,.025,.29,0,-.032,.30,cherry);
    outline(g,[[.24,.03],[.40,.007],[.78,-.028],[.85,-.125],[.79,-.176],[.41,-.12],[.19,-.045]],.103,cherry);
    b(g,.12,.14,.033,0,-.099,.846,rubber);
    guard(g,[[0,-.058,.10],[0,-.13,.112],[0,-.128,.01],[0,-.052,-.06]],black,.01);
    rod(g,[0,-.06,.07],[0,-.107,.042],.011,satin);
    b(g,.026,.025,.02,0,.083,-.95,bright);
    poseHand(hand(g,.28,-.14,false,{rx:.16,ry:.20,rz:-.34,gripCurl:1.28}),[.116,-.145,.278],[.16,.20,-.34],1.28);poseHand(hand(g,-.29,-.11,true,{rx:.32,ry:-.10,rz:.22,gripCurl:1.22}),[-.075,-.108,-.305],[.32,-.10,.22],1.22);
    g.userData.pump=pump;g.userData.pumpBaseZ=0;
    g.userData.muzzle={x:0,y:.055,z:-.99};
  }

  // 3. HK UMP9: chunky reinforced polymer housing, folding skeleton stock,
  // top/side accessory rails, compact straight magazine and rotary selector.
  {
    const g=use(2);
    outline(g,[[.41,.10],[.41,-.01],[.20,-.08],[-.40,-.074],[-.43,.068],[-.23,.095]],.164,polymer);
    outline(g,[[.22,-.06],[.18,.075],[-.35,.075],[-.37,-.055]],.172,polymer2);
    cyl(g,.025,.33,0,.002,-.50,gunmetal);ring(g,.038,0,.002,-.66,black,.009);
    b(g,.175,.041,.23,0,-.049,-.30,polymer);
    for(let k=0;k<3;k++)for(const x of [-.089,.089])b(g,.009,.015,.045,x,-.05,-.36+k*.076,black);
    rail(g,-.38,.18,.116,.12,black);
    b(g,.06,.052,.06,0,.163,-.23,black);
    b(g,.065,.055,.055,0,.158,.13,black);
    outline(g,[[.23,-.056],[.29,-.05],[.35,-.28],[.27,-.34],[.21,-.31]],.1,polymer);
    outline(g,[[.03,-.068],[.14,-.068],[.18,-.33],[.14,-.37],[.055,-.34]],.085,polymer2);
    for(let i=0;i<9;i++)b(g,.09,.006,.018,0,-.16-i*.017,.11-i*.004,black);
    guard(g,[[0,-.064,.195],[0,-.14,.14],[0,-.14,.03],[0,-.06,-.005]],black);
    cyl(g,.015,.175,.09,-.013,.09,satin,'x');
    sphere(g,.016,.093,.014,.12,bright);
    b(g,.014,.06,.2,.107,0,.04,gunmetal);
    const stock=new THREE.Group();g.add(stock);
    wire(stock,[[0,.02,.40],[0,.04,.52],[0,.065,.72],[0,-.085,.78],[0,-.13,.68],[0,-.08,.42]],polymer2,.019);
    b(stock,.13,.16,.032,0,-.032,.79,polymer);
    b(stock,.14,.02,.038,0,.04,.78,rubber);
    label(g,'UMP9 · 9×19',.095,.030,-.06,.14,.029);
    poseHand(hand(g,.27,-.24,false,{rx:.15,ry:.18,rz:-.30,gripCurl:1.30}),[.108,-.235,.266],[.15,.18,-.30],1.30);poseHand(hand(g,-.23,-.15,true,{rx:.29,ry:-.14,rz:.18,gripCurl:1.18}),[-.088,-.148,-.218],[.29,-.14,.18],1.18);
    const bolt=b(g,.03,.025,.085,.094,.032,-.075,edge);
    g.userData.bolt=bolt;g.userData.boltBaseZ=-.075;
    g.userData.muzzle={x:0,y:0,z:-.67};
  }

  // 4. PA md.86 (user's AK-86): stamped receiver, 5.45 curved magazine,
  // wood handguard with the Romanian vertical foregrip, gas tube and wire stock.
  {
    const g=use(3);
    cyl(g,.022,.74,0,.012,-.59,gunmetal);
    cyl(g,.025,.47,0,.082,-.43,gunmetal);
    cyl(g,.032,.08,0,.013,-.95,black);
    for(let j=0;j<3;j++)b(g,.05,.012,.02,0,.028,-.96+j*.025,edge);
    b(g,.065,.075,.047,0,.035,-.75,gunmetal);
    b(g,.04,.09,.05,0,.06,-.92,black);
    outline(g,[[.30,.07],[.30,-.062],[-.19,-.068],[-.2,.085]],.15,gunmetal);
    b(g,.144,.032,.42,0,.091,.055,parker);
    b(g,.155,.028,.1,0,.095,-.16,edge);
    b(g,.156,.01,.13,0,-.047,.135,black);
    for(let i=0;i<3;i++)b(g,.155,.004,.09,0,.073,-.11+i*.09,gunmetal);
    const h1=outline(g,[[-.17,.05],[-.63,.05],[-.63,-.04],[-.18,-.05]],.125,cherry);
    for(let i=0;i<5;i++)b(g,.128,.003,.014,0,.055,-.58+i*.073,highlight);
    outline(g,[[-.15,-.02],[-.53,-.02],[-.53,-.09],[-.18,-.09]],.135,beech);
    outline(g,[[-.40,-.06],[-.50,-.06],[-.47,-.27],[-.39,-.33],[-.36,-.295]],.095,cherry);
    b(g,.09,.015,.07,0,-.32,-.41,bakelite);
    outline(g,[[.12,-.067],[.22,-.057],[.25,-.30],[.20,-.36],[.12,-.31]],.095,cherry);
    outline(g,[[.035,-.07],[-.095,-.065],[-.115,-.28],[-.06,-.41],[.08,-.42],[.11,-.31]],.08,bakelite);
    for(let i=0;i<7;i++){
      const y=-.17-i*.033;
      b(g,.085,.003,.075,0,y,-.01+Math.pow(i/7,1.5)*.025,black);
    }
    guard(g,[[0,-.07,.18],[0,-.14,.14],[0,-.14,.038],[0,-.068,.02]],black);
    rod(g,[0,-.055,.09],[0,-.112,.054],.013,edge);
    // The real PA md.86 has a skeletonized side-folding wire stock.
    wire(g,[[-.058,.024,.30],[-.062,.076,.58],[-.062,-.105,.74],[-.062,-.17,.65],[-.061,-.066,.31]],edge,.012);
    wire(g,[[.058,.024,.30],[.062,.076,.58],[.062,-.105,.74],[.062,-.17,.65],[.061,-.066,.31]],edge,.012);
    b(g,.136,.14,.031,0,-.092,.75,polymer);
    b(g,.14,.013,.036,0,-.023,.75,rubber);
    b(g,.04,.055,.04,0,.134,.22,black);
    b(g,.038,.052,.04,0,.108,-.79,black);
    b(g,.02,.012,.12,.084,.018,.075,edge);
    label(g,'MD · 86',.078,.025,.15,.12,.026);
    const bolt=b(g,.022,.027,.085,.088,.04,.075,satin);
    screws(g,[[.023,.26],[-.02,.0]],.081,satin);
    poseHand(hand(g,.23,-.20,false,{rx:.12,ry:.22,rz:-.26,gripCurl:1.31}),[.105,-.202,.232],[.12,.22,-.26],1.31);poseHand(hand(g,-.45,-.19,true,{rx:.33,ry:-.16,rz:.14,gripCurl:1.15}),[-.082,-.188,-.428],[.33,-.16,.14],1.15);
    g.userData.bolt=bolt;g.userData.boltBaseZ=.075;
    g.userData.muzzle={x:0,y:.015,z:-.98};
  }

  // 5. M79: hinged single-shot 40mm grenade launcher, wood furniture and
  // notched barrel sights, with the recognizable oversized barrel.
  {
    const g=use(4);
    cyl(g,.073,.63,0,.025,-.31,gunmetal);
    cyl(g,.058,.59,0,.025,-.31,black);
    ring(g,.075,0,.025,-.632,satin,.010);
    ring(g,.061,0,.025,-.639,black,.013);
    b(g,.159,.07,.07,0,.022,-.01,gunmetal);
    b(g,.152,.09,.20,0,-.003,.09,parker);
    b(g,.024,.032,.05,0,.125,-.31,black);
    b(g,.026,.05,.045,0,.138,-.50,edge);
    b(g,.085,.023,.25,0,.128,-.33,edge);
    for(let k=0;k<5;k++)b(g,.092,.011,.014,0,.141,-.45+k*.047,black);
    outline(g,[[.18,.03],[.28,-.06],[.32,-.21],[.26,-.25],[.17,-.14]],.12,cherry);
    outline(g,[[.2,.01],[.4,-.04],[.72,-.07],[.78,-.125],[.72,-.19],[.38,-.16],[.2,-.055]],.13,cherry);
    for(let i=0;i<8;i++)b(g,.135,.004,.018,0,-.145,.32+i*.045,highlight);
    b(g,.138,.14,.025,0,-.127,.785,rubber);
    guard(g,[[0,-.085,.17],[0,-.145,.13],[0,-.15,.025],[0,-.085,-.005]],black);
    rod(g,[0,-.092,.083],[0,-.13,.064],.012,edge);
    cyl(g,.03,.17,.082,.065,-.02,black,'x');
    sphere(g,.022,.088,.103,-.05,bright);
    poseHand(hand(g,.20,-.21,false,{rx:.14,ry:.20,rz:-.28,gripCurl:1.27}),[.106,-.208,.205],[.14,.20,-.28],1.27);poseHand(hand(g,-.37,-.18,true,{rx:.34,ry:-.15,rz:.16,gripCurl:1.16}),[-.084,-.175,-.352],[.34,-.15,.16],1.16);
    g.userData.muzzle={x:0,y:.025,z:-.64};
  }

  // 6. M2-type man-portable flamethrower: fuel packs, shoulder harness,
  // rubber hose, trigger nozzle, grip and metallic flame regulator.
  {
    const g=use(5);
    b(g,.33,.36,.10,0,-.06,.38,olive);
    for(const x of [-.125,.125]){
      cyl(g,.09,.57,x,-.075,.34,fuel,'y');
      cyl(g,.091,.045,x,.22,.34,gunmetal,'y');
      cyl(g,.079,.02,x,-.365,.34,black,'y');
      cyl(g,.017,.054,x,.27,.34,brass,'y');
    }
    for(const x of [-.115,.115]){
      b(g,.09,.035,.03,x,.055,.425,black);
      b(g,.05,.32,.04,x,-.08,.433,polymer);
    }
    cyl(g,.048,.63,0,.04,-.37,parker);
    cyl(g,.06,.11,0,.04,-.73,gunmetal);
    ring(g,.064,0,.04,-.79,bright,.01);
    cyl(g,.04,.027,0,.04,-.81,black);
    cyl(g,.023,.05,0,.04,-.84,glow);
    b(g,.14,.078,.27,0,-.01,-.12,parker);
    b(g,.052,.09,.07,0,-.13,-.05,black);
    outline(g,[[.08,-.04],[.17,-.04],[.20,-.265],[.13,-.28],[.06,-.21]],.095,polymer);
    guard(g,[[0,-.06,-.04],[0,-.12,-.11],[0,-.14,-.21],[0,-.06,-.23]],black);
    for(let i=0;i<6;i++)ring(g,.045,0,.04,-.59-i*.028,edge,.006);
    cyl(g,.038,.16,0,.16,-.35,brass,'x');
    cyl(g,.044,.033,.10,.16,-.35,black,'x');
    sphere(g,.026,.12,.16,-.35,warning);
    const curve=new THREE.CatmullRomCurve3([
      new THREE.Vector3(-.14,-.24,.36),new THREE.Vector3(-.20,-.27,.20),
      new THREE.Vector3(-.21,-.23,-.03),new THREE.Vector3(-.115,-.11,-.27),
      new THREE.Vector3(-.05,-.02,-.41)
    ]);
    const hose=new THREE.Mesh(new THREE.TubeGeometry(curve,42,.025,12,false),rubber);g.add(hose);
    for(let i=0;i<8;i++){
      const p=curve.getPoint(i/9+.07),t=curve.getTangent(i/9+.07).normalize();
      const clamp=new THREE.Mesh(new THREE.TorusGeometry(.029,.004,6,12),edge);
      clamp.position.copy(p);clamp.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),t);g.add(clamp);
    }
    b(g,.07,.025,.13,0,.11,-.11,black);
    b(g,.025,.075,.035,0,.152,-.07,edge);
    label(g,'M2  |  FUEL',.175,.06,.36,.12,.02);
    poseHand(hand(g,.14,-.19,false,{rx:.12,ry:.21,rz:-.30,gripCurl:1.29}),[.107,-.192,.145],[.12,.21,-.30],1.29);poseHand(hand(g,-.36,-.15,true,{rx:.36,ry:-.15,rz:.20,gripCurl:1.17}),[-.090,-.154,-.345],[.36,-.15,.20],1.17);
    g.userData.muzzle={x:0,y:.04,z:-.85};
  }
})();

const modelKeyLight=new THREE.PointLight(0xfff0d8,1.55,3.5);
modelKeyLight.position.set(.7,.78,-.65);viewScene.add(modelKeyLight);
const modelRimLight=new THREE.PointLight(0x89baff,.8,2.8);
modelRimLight.position.set(-.6,.15,-.48);viewScene.add(modelRimLight);

// ---------- first-person katana: anatomical, handle-locked grip ----------
function createKatanaGrip(parent,kind='katana'){
  const root=new THREE.Group();parent.add(root);
  const m=HAND_TEXTURES, cx=0,cy=-.03;
  const ell=(x,y,z,a,b,c,mat)=>{
    const mesh=new THREE.Mesh(new THREE.SphereGeometry(1,20,14),mat);
    mesh.position.set(x,y,z);mesh.scale.set(a,b,c);root.add(mesh);return mesh;
  };
  const segment=(a,b,r0,r1,mat,into=root)=>{
    const A=new THREE.Vector3(...a),B=new THREE.Vector3(...b),d=B.clone().sub(A);
    const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r1,r0,d.length(),12),mat);
    mesh.position.copy(A).add(B).multiplyScalar(.5);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());into.add(mesh);return mesh;
  };
  // Flesh is visible near the knuckles, with a dark fitted forearm sleeve.
  // Keep the forearm away from the near-plane to avoid the enormous 'mitt' look.
  segment([.29,-.23,.48],[.13,-.085,.25],.10,.073,m.cloth);
  ell(.13,-.085,.265,.075,.08,.073,m.leather);
  const cuff=new THREE.Mesh(new THREE.TorusGeometry(.082,.011,8,28),m.rubber);
  cuff.position.set(.15,-.11,.28);cuff.rotation.x=Math.PI/2;root.add(cuff);
  const palm=ell(.090,-.045,.164,.061,.066,.111,m.skin);
  palm.rotation.y=-.08;palm.rotation.z=-.17;
  ell(.068,-.058,.225,.052,.048,.067,m.skin); // thenar muscle
  ell(.104,-.010,.080,.038,.039,.043,m.skin); // index knuckle cushion
  const fingers=[];
  const zAnchors=[.045,.103,.165,.227], thick=[.019,.018,.017,.0155];
  // Each finger crosses from the right side over the top and around the far
  // side of the 4.2 cm-radius hilt. The inner surface grazes but does not
  // penetrate the grip. Successive fingers are offset along the handle.
  for(let j=0;j<4;j++){
    const finger=new THREE.Group();root.add(finger);fingers.push(finger);
    const z=zAnchors[j],r=.066+(.003*(j===1?1:0));
    const angles=[-.52,.24,1.03,1.93,2.55];
    let prev=null;
    for(let k=0;k<angles.length;k++){
      const theta=angles[k];
      const curr=[cx+r*Math.cos(theta),cy+r*Math.sin(theta),z-.005*k];
      if(prev){
        const t=thick[j]*(1-.11*(k-1));
        segment(prev,curr,t*1.04,t,k<=2?m.skin:m.skin,finger);
        const knuckle=new THREE.Mesh(new THREE.SphereGeometry(t,10,8),m.skin);
        knuckle.position.set(...curr);finger.add(knuckle);
      }
      prev=curr;
    }
    const tip=prev;
    const nail=new THREE.Mesh(new THREE.SphereGeometry(.012,10,8),m.nail);
    nail.position.set(tip[0]-.002,tip[1]+.009,tip[2]-.003);
    nail.scale.set(.8,.37,1.08);finger.add(nail);
  }
  // Opposable thumb sweeps around the lower half, away from the four digits.
  const thumb=new THREE.Group();root.add(thumb);
  const thumbAngles=[-.44,-1.12,-1.91,-2.50];
  let prev=null;
  for(let k=0;k<thumbAngles.length;k++){
    const theta=thumbAngles[k],r=.069;
    const q=[r*Math.cos(theta),cy+r*Math.sin(theta),.252-.012*k];
    if(prev){
      const t=.024-.002*k;segment(prev,q,t,t*.92,m.skin,thumb);
      const joint=new THREE.Mesh(new THREE.SphereGeometry(t,10,8),m.skin);
      joint.position.set(...q);thumb.add(joint);
    }
    prev=q;
  }
  // Motion comes from the weapon group: fingers never slide away from the hilt.
  root.userData.fingers=fingers;root.userData.thumb=thumb;root.userData.melee=true;
  root.userData.katanaGrip=kind==='katana';root.userData.saberGrip=kind==='saber';root.userData.handleLocked=true;
  root.userData.restPosition=root.position.clone();
  root.userData.restRotation={x:0,y:0,z:0};
  root.userData.baseCurl=1.45;
  return root;
}

// Real melee viewmodels are separate from the six firearms, but use the same camera rig.
(function buildBlades(){
  const hilt=new THREE.MeshStandardMaterial({color:0x171e26,metalness:.66,roughness:.36});
  const silk=new THREE.MeshStandardMaterial({color:0x342123,metalness:.1,roughness:.85});
  const steel=new THREE.MeshStandardMaterial({color:0xe1e8eb,metalness:1,roughness:.19,side:THREE.DoubleSide});
  const copper=new THREE.MeshStandardMaterial({color:0xb99158,metalness:.9,roughness:.25});
  const blue=new THREE.MeshBasicMaterial({color:0x8eeaff});
  const glow=new THREE.MeshBasicMaterial({color:0x2ab8ff,transparent:true,opacity:.18,depthWrite:false,blending:THREE.AdditiveBlending});
  function cyl(g,r1,r2,len,x,y,z,mat){const m=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,len,14),mat);m.rotation.x=Math.PI/2;m.position.set(x,y,z);g.add(m);return m;}
  for(const i of [6,7]){
    const g=gunModels[i];
    g.position.set(i===6?.06:.14,i===6?-.02:-.07,i===6?0:.06);
    g.rotation.set(i===6?.10:.18,i===6?.35:0,i===6?-.10:0);
    if(i!==6){
      cyl(g,.046,.048,.37,0,-.03,.13,hilt);
      cyl(g,.052,.051,.04,0,-.03,.33,copper);
      for(let j=0;j<9;j++){
        const m=new THREE.Mesh(new THREE.TorusGeometry(.047,.005,5,20),blue);
        m.rotation.y=(j%2)*.25;m.position.set(0,-.03,.27-j*.041);g.add(m);
      }
      cyl(g,.078,.077,.025,0,-.03,-.08,hilt);
    }
    if(i===6){
      // Katana proportions: 0.79 blade / 0.31 handle, with a curved shinogi
      // ridge, individually tapered cross-sections, sharp kissaki and edge.
      // All dimensions are local viewmodel units; no geometry intersects the fist.
      const handleBase=new THREE.Mesh(new THREE.CylinderGeometry(.042,.044,.305,18),silk);
      handleBase.rotation.x=Math.PI/2;handleBase.position.set(0,-.03,.158);g.add(handleBase);
      const wrap=new THREE.MeshStandardMaterial({color:0x908879,metalness:.18,roughness:.83});
      for(let n=0;n<9;n++)for(const sg of [-1,1]){
        const pts=[];
        for(let j=0;j<=9;j++){
          const t=j/9,ang=sg*(.15+Math.PI*1.50*t)+(sg<0?Math.PI:0);
          pts.push(new THREE.Vector3(.0455*Math.cos(ang),-.03+.0455*Math.sin(ang),.026+n*.030+t*.027));
        }
        const band=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),12,.0028,5,false),wrap);
        g.add(band);
      }
      const kashira=new THREE.Mesh(new THREE.CylinderGeometry(.047,.049,.028,20),copper);
      kashira.rotation.x=Math.PI/2;kashira.position.set(0,-.03,.316);g.add(kashira);
      const fuchi=new THREE.Mesh(new THREE.CylinderGeometry(.049,.047,.027,20),copper);
      fuchi.rotation.x=Math.PI/2;fuchi.position.set(0,-.03,-.010);g.add(fuchi);
      const guardMat=new THREE.MeshStandardMaterial({color:0x403b35,metalness:.8,roughness:.33});
      const tsuba=new THREE.Mesh(new THREE.SphereGeometry(1,24,16),guardMat);
      tsuba.scale.set(.081,.068,.011);tsuba.position.set(0,-.03,-.052);g.add(tsuba);
      const tsubaRim=new THREE.Mesh(new THREE.TorusGeometry(.066,.004,8,32),copper);
      tsubaRim.position.set(0,-.03,-.065);tsubaRim.scale.y=.85;g.add(tsubaRim);
      const habaki=new THREE.Mesh(new THREE.CylinderGeometry(.042,.036,.05,18),copper);
      habaki.rotation.x=Math.PI/2;habaki.position.set(0,-.03,-.091);g.add(habaki);
      const bladeVerts=[],bladeIndices=[],sliceCount=24;
      const brightEdge=new THREE.MeshStandardMaterial({color:0xf4f7f5,metalness:.68,roughness:.17,side:THREE.DoubleSide});
      const edgePts=[],ridgePts=[];
      for(let i=0;i<=sliceCount;i++){
        const t=i/sliceCount,point=Math.max(0,(t-.83)/.17),
          taper=(1-.25*t)*(1-Math.pow(point,1.26)*.99);
        const w=Math.max(.00035,.045*taper),center=-.03+.046*t*t,
          z=-.105-.795*t,th=.0095*(1-.65*t);
        const ring=[[-w,-.004],[-w*.62,th],[w*.50,th*.78],
          [w,.0002],[w*.53,-th],[-w*.62,-th]];
        for(const [x,dy] of ring)bladeVerts.push(x,center+dy,z);
        edgePts.push(new THREE.Vector3(w,center+.0002,z));
        ridgePts.push(new THREE.Vector3(-w*.30,center+th*.95,z));
        if(i>0)for(let k=0;k<6;k++){
          const a=(i-1)*6+k,b=(i-1)*6+(k+1)%6,
            c=i*6+k,d=i*6+(k+1)%6;
          bladeIndices.push(a,b,c,b,d,c);
        }
      }
      for(let k=1;k<5;k++){
        bladeIndices.push(0,k+1,k);
        const base=sliceCount*6;bladeIndices.push(base,base+k,base+k+1);
      }
      const geo=new THREE.BufferGeometry();
      geo.setAttribute('position',new THREE.Float32BufferAttribute(bladeVerts,3));
      geo.setIndex(bladeIndices);geo.computeVertexNormals();
      const blade=new THREE.Mesh(geo,steel);g.add(blade);
      const cuttingEdge=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(edgePts),25,.0026,5,false),brightEdge);
      g.add(cuttingEdge);
      const ridge=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(ridgePts.slice(0,18)),18,.0021,5,false),brightEdge);
      g.add(ridge);
      g.userData.blade=blade;g.userData.bladeTip=new THREE.Vector3(0,-.03+.046,-.90);
      g.userData.muzzle={x:0,y:-.03,z:-.90};
    } else {
      // Energy saber: compact camera-scale hilt, subdued hardware and a slender
      // blade that progressively emerges from the emitter. Matching the katana
      // grip axis means there is no second, floating glove underneath the prop.
      // Hilt spans z=-.03..+.30, blade extends toward negative z.
      const brushed=new THREE.MeshStandardMaterial({color:0x53616b,metalness:.91,roughness:.28});
      const trim=new THREE.MeshStandardMaterial({color:0xb1c0c6,metalness:.94,roughness:.19});
      const darkGrip=new THREE.MeshStandardMaterial({color:0x171d24,metalness:.25,roughness:.80});
      const energized=new THREE.MeshStandardMaterial({color:0x72dcff,emissive:0x1e8dbd,emissiveIntensity:.9,metalness:.38,roughness:.20});
      const body=cyl(g,.040,.043,.295,0,-.03,.143,hilt);
      body.userData.part='hilt';
      for(let n=0;n<7;n++){
        const z=.053+n*.029;
        // Thin grip ridges remain below the wrapping fingers.
        cyl(g,.044,.044,.007,0,-.03,z,n%2?darkGrip:brushed);
      }
      cyl(g,.047,.046,.025,0,-.03,.293,trim); // pommel
      cyl(g,.034,.032,.010,0,-.03,.310,darkGrip);
      cyl(g,.049,.047,.028,0,-.03,-.018,brushed); // emitter collar
      cyl(g,.053,.048,.025,0,-.03,-.048,trim);
      cyl(g,.033,.031,.018,0,-.03,-.072,darkGrip);
      cyl(g,.027,.027,.010,0,-.03,-.085,energized);
      const activation=new THREE.Mesh(new THREE.BoxGeometry(.009,.014,.032),energized);
      activation.position.set(.044,-.028,.025);g.add(activation);
      const switchGuard=new THREE.Mesh(new THREE.BoxGeometry(.011,.025,.050),brushed);
      switchGuard.position.set(.044,-.029,.025);switchGuard.position.x=.045;g.add(switchGuard);
      activation.position.x=.052;
      for(let n=0;n<4;n++){
        const vent=new THREE.Mesh(new THREE.BoxGeometry(.004,.009,.012),darkGrip);
        vent.position.set(-.045,-.029,-.012+n*.016);g.add(vent);
      }
      // Cylinders are rotated around X to point along world Z. Their LENGTH is
      // still local-Y, so scale.y (not scale.z) drives a genuine blade extension.
      const auraMat=new THREE.MeshBasicMaterial({color:0x22baff,transparent:true,opacity:.23,
        depthWrite:false,blending:THREE.AdditiveBlending});
      const coreMat=new THREE.MeshBasicMaterial({color:0x6be1ff,transparent:true,opacity:.95,depthWrite:false});
      const whiteMat=new THREE.MeshBasicMaterial({color:0xf4ffff,transparent:true,opacity:.96,depthWrite:false});
      const aura=cyl(g,.029,.030,1.00,0,-.03,-.595,auraMat);
      const core=cyl(g,.016,.016,.984,0,-.03,-.585,coreMat);
      const white=cyl(g,.008,.008,.973,0,-.03,-.579,whiteMat);
      const light=new THREE.PointLight(0x39bfff,0,3.5);light.position.set(0,-.03,-.26);g.add(light);
      g.userData.bladeAura=aura;g.userData.bladeCore=core;g.userData.bladeWhite=white;
      g.userData.bladeLight=light;g.userData.bladeProgress=0;
      g.userData.bladeLengths=[1.00,.984,.973];
      g.userData.bladeBaseZ=-.094;
      g.userData.muzzle={x:0,y:-.03,z:-1.075};
      aura.scale.y=core.scale.y=white.scale.y=.001;
      g.userData.hilt=body;
    }
    // Dual weapon-locked procedural hands: the primary grip is near the guard,
    // while the mirrored support grip is lower on the hilt. Both stay parented
    // to the animated weapon, preventing detached palms during swings.
    const primary=createKatanaGrip(g,i===6?'katana':'saber');
    primary.position.z=-.062;
    primary.userData.restPosition.copy(primary.position);
    const support=createKatanaGrip(g,i===6?'katana':'saber');
    support.scale.x=-1;support.position.z=.070;
    support.userData.restPosition.copy(support.position);
    if(i===7){support.position.x-=.32;support.position.y-=.19;support.position.z+=.22;support.userData.restPosition.copy(support.position);support.visible=false;}
    g.userData.handRigs=[primary,support];
  }
})();

// Animated broad saber/steel swipe, visible across the viewport during contact.
// The 3D ribbon is curved and vertex-faded rather than a constant-width torus.
const slashFX=new THREE.Group();viewScene.add(slashFX);slashFX.visible=false;slashFX.renderOrder=999;
const slashGeo=new THREE.BufferGeometry(),slashPositions=new Float32Array(31*2*3),slashColors=new Float32Array(31*2*3);
slashGeo.setAttribute('position',new THREE.BufferAttribute(slashPositions,3));
slashGeo.setAttribute('color',new THREE.BufferAttribute(slashColors,3));
const slashIndex=[];for(let i=0;i<30;i++){const v=i*2;slashIndex.push(v,v+1,v+2,v+1,v+3,v+2);}
slashGeo.setIndex(slashIndex);
const slashMat=new THREE.MeshBasicMaterial({color:0xffffff,vertexColors:true,transparent:true,opacity:.85,depthWrite:false,depthTest:false,side:THREE.DoubleSide,blending:THREE.AdditiveBlending});
const slashRibbon=new THREE.Mesh(slashGeo,slashMat);slashRibbon.renderOrder=999;slashFX.add(slashRibbon);
const slashLineGeo=new THREE.BufferGeometry();slashLineGeo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(31*3),3));
const slashLine=new THREE.Line(slashLineGeo,new THREE.LineBasicMaterial({color:0xfff8ed,transparent:true,opacity:.85,depthTest:false,depthWrite:false,blending:THREE.AdditiveBlending}));
slashLine.renderOrder=1000;slashFX.add(slashLine);
function slashPath(v,side,weapon,style='horizontal'){
  const sx=side<0?-1:1;
  if(weapon===6){
    if(style==='heavy')return [sx*(.22-.36*v),.92-1.32*v,-1.42+.10*Math.sin(v*Math.PI)];
    if(style==='thrust')return [sx*(.22-.17*v),-.04+.13*v,-1.21-.44*v];
    if(style==='diagonal')return [sx*(1.03-2.04*v),.85-1.18*v+.14*Math.sin(v*Math.PI),-1.35+.1*Math.sin(v*Math.PI)];
    return [sx*(1.08-2.18*v),.22-.28*v+.14*Math.sin(v*Math.PI),-1.37+.07*Math.sin(v*Math.PI)];
  }
  if(style==='heavy')return [sx*(.22-.38*v),.88-1.25*v,-1.34+.08*Math.sin(v*Math.PI)];
  if(style==='thrust')return [sx*(.19-.17*v),-.025+.12*v,-1.16-.38*v];
  if(style==='diagonal')return [sx*(1.00-2.03*v),.79-1.13*v+.14*Math.sin(v*Math.PI),-1.30+.10*Math.sin(v*Math.PI)];
  return [sx*(1.06-2.10*v),.20-.30*v+.14*Math.sin(v*Math.PI),-1.31+.09*Math.sin(v*Math.PI)];
}
function animateSlash(progress,weapon,side=1,style='horizontal'){
  const t=weapon>=6?(progress-.245)/.50:(progress-.14)/.58;
  if(weapon<6||t<=0||t>=1.1){slashFX.visible=false;return;}
  slashFX.visible=true;
  const tip=Math.min(1,t),tail=Math.max(0,tip-(weapon===7?.57:.42));
  const col=weapon===7?[.20,.80,1]:[.84,.92,1];
  for(let i=0;i<=30;i++){
    const u=i/30,p=tail+(tip-tail)*u,[x,y,z]=slashPath(p,side,weapon,style),width=(weapon===7?.17:.15)*Math.sin(Math.PI*u)+.03;
    const normal=Math.max(.06,Math.sin(u*Math.PI)),fade=normal*(1-Math.max(0,t-1)*9);
    for(let q=0;q<2;q++){
      const ii=(i*2+q)*3,off=(q?1:-1)*width;
      slashPositions[ii]=x+off*.36;slashPositions[ii+1]=y+off;slashPositions[ii+2]=z;
      const fade2=fade*(q?.48:1);slashColors[ii]=col[0]*fade2;slashColors[ii+1]=col[1]*fade2;slashColors[ii+2]=col[2]*fade2;
    }
    const li=i*3;slashLineGeo.attributes.position.array[li]=x;slashLineGeo.attributes.position.array[li+1]=y;slashLineGeo.attributes.position.array[li+2]=z;
  }
  slashGeo.attributes.position.needsUpdate=true;slashGeo.attributes.color.needsUpdate=true;
  slashLineGeo.attributes.position.needsUpdate=true;
  slashMat.opacity=weapon===7?.95:.78;
  slashLine.material.color.setHex(weapon===7?0xb7faff:0xffffff);
  slashLine.material.opacity=Math.max(0,.95-(Math.max(0,t-.82)*3));
  slashFX.rotation.z=side<0?.08:-.08;
}

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
const floorMat=new THREE.MeshStandardMaterial({map:floorTex,bumpMap:floorTex,bumpScale:0.17,metalness:0.06,roughness:0.94});
const ceilMat=new THREE.MeshStandardMaterial({map:ceilTex,bumpMap:ceilTex,bumpScale:0.1,roughness:1});
const glowTex=(function(){const c=document.createElement('canvas'); c.width=c.height=64; const x=c.getContext('2d');
  const g=x.createRadialGradient(32,32,2,32,32,32); g.addColorStop(0,'rgba(255,210,110,1)'); g.addColorStop(0.4,'rgba(255,120,30,.4)'); g.addColorStop(1,'rgba(255,80,0,0)');
  x.fillStyle=g; x.fillRect(0,0,64,64); return new THREE.CanvasTexture(c);})();
const glowMat=new THREE.SpriteMaterial({map:glowTex,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
const KICK=[0.16,0.28,0.085,0.135,0.3,0.045,0.38,0.32];
const mflash=new THREE.Sprite(glowMat); mflash.scale.set(0.5,0.5,1); mflash.position.set(0,0,-0.8); mflash.visible=false; gun.add(mflash);
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
    g.gain.value=(v||0.05)*(SET.mute?0:SET.vol)*SET.sfx;
    g.gain.exponentialRampToValueAtTime(0.0001,actx.currentTime+d);
    o.connect(g); g.connect(actx.destination);
    o.start(); o.stop(actx.currentTime+d);
  }catch(e){}
}

// ---------- realistic audio ----------
let nbuf=null, stepT=0.3, stepL=false, hb=0, flameSoundAt=0;
function noise(dur,f0,f1,vol,type,pan){
  if(!actx) return;
  try{
    if(!nbuf){ nbuf=actx.createBuffer(1,actx.sampleRate,actx.sampleRate); const d=nbuf.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; }
    const s=actx.createBufferSource(), fl=actx.createBiquadFilter(), g=actx.createGain(), t=actx.currentTime;
    s.buffer=nbuf; s.loop=true; fl.type=type||'lowpass';
    fl.frequency.setValueAtTime(f0,t); fl.frequency.exponentialRampToValueAtTime(Math.max(20,f1),t+dur);
    g.gain.setValueAtTime(Math.max(0.0002,vol*(SET.mute?0:SET.vol)*SET.sfx),t); g.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    s.connect(fl); fl.connect(g);
    if(pan&&actx.createStereoPanner){ const p=actx.createStereoPanner(); p.pan.value=Math.max(-1,Math.min(1,pan)); g.connect(p); p.connect(actx.destination); } else g.connect(actx.destination);
    s.start(t); s.stop(t+dur);
  }catch(e){}
}
// Original synthesized ambient score and UI cues; never autoplay before user interaction.
let musicNodes=null, musicInterval=null, flameLoop=null, flameGain=null, saberGain=null;
function ensureGameAudio(){
  if(!actx){try{actx=new (window.AudioContext||window.webkitAudioContext)();}catch(e){return;}}
  if(actx.state==='suspended')actx.resume().catch(()=>{});
  if(musicNodes)return;
  const master=actx.createGain();master.gain.value=.065;master.connect(actx.destination);
  const menuBus=actx.createGain(), gameBus=actx.createGain();
  menuBus.gain.value=1;gameBus.gain.value=0;menuBus.connect(master);gameBus.connect(master);
  const low=actx.createBiquadFilter();low.type='lowpass';low.frequency.value=500;low.connect(menuBus);
  const combatG=actx.createGain(),bossG=actx.createGain();combatG.gain.value=0;bossG.gain.value=0;
  const combatOsc=actx.createOscillator(),bossOsc=actx.createOscillator();
  combatOsc.type='triangle';combatOsc.frequency.value=82.41;
  bossOsc.type='sawtooth';bossOsc.frequency.value=55;
  combatOsc.connect(combatG);bossOsc.connect(bossG);combatG.connect(gameBus);bossG.connect(gameBus);
  combatOsc.start();bossOsc.start();
  const os=[];
  [[55,'sine',.48],[82.41,'triangle',.16],[110,'sine',.12],[164.81,'sine',.06]].forEach(([hz,type,vol])=>{
    const o=actx.createOscillator(),g=actx.createGain();o.type=type;o.frequency.value=hz;g.gain.value=vol;o.connect(g);g.connect(low);o.start();os.push(o);
  });
  musicNodes={master,low,os,menuBus,gameBus,combatG,bossG,combatOsc,bossOsc};
  let count=0;
  musicInterval=setInterval(()=>{
    if(!actx||actx.state!=='running'||SET.vol<=0)return;
    // Slow, eerie original notes over a low persistent drone.
    const seq=[164.8,146.8,130.8,110,164.8,196,146.8,123.5],hz=seq[count++%seq.length];
    const o=actx.createOscillator(),g=actx.createGain(),t=actx.currentTime;
    o.type='sine';o.frequency.value=hz;
    g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(.10,t+.11);g.gain.exponentialRampToValueAtTime(.0001,t+1.3);
    o.connect(g);g.connect(state==='playing'?gameBus:menuBus);o.start(t);o.stop(t+1.35);
  },1600);
  // Flamethrower: continuous, filtered turbulent-noise loop with low combustion rumble.
  const b=actx.createBuffer(1,actx.sampleRate*2,actx.sampleRate),data=b.getChannelData(0);
  for(let i=0;i<data.length;i++)data[i]=Math.random()*2-1;
  const src=actx.createBufferSource(),filter=actx.createBiquadFilter();
  filter.type='lowpass';filter.frequency.value=1350;
  flameGain=actx.createGain();flameGain.gain.value=0;src.buffer=b;src.loop=true;
  src.connect(filter);filter.connect(flameGain);flameGain.connect(actx.destination);src.start();flameLoop={src,filter};
  const saberOsc=actx.createOscillator();saberOsc.type='sawtooth';saberOsc.frequency.value=91;
  const saberFilter=actx.createBiquadFilter();saberFilter.type='lowpass';saberFilter.frequency.value=310;
  saberGain=actx.createGain();saberGain.gain.value=0;
  saberOsc.connect(saberFilter);saberFilter.connect(saberGain);saberGain.connect(actx.destination);saberOsc.start();
}
function menuClickSound(kind){
  if(!actx||SET.vol<=0||SET.mute)return;
  if(kind==='equip'){beep(380,.09,'triangle',.028,250);noise(.08,1700,240,.11,'lowpass');}
  else if(kind==='confirm'){beep(480,.11,'sine',.052,200);beep(660,.18,'triangle',.029,-100);}
  else {beep(480,.075,'triangle',.035,-160);}
}
function updateGameAudio(){
  if(!actx||!musicNodes)return;
  const t=actx.currentTime;
  const playing=state==='playing'&&!paused;
  const volume=SET.mute?0:SET.vol*SET.music;
  // Adaptive mixing: quiet pause menus and short ducking during explosions.
  musicNodes.master.gain.setTargetAtTime(.14*volume*(paused?.42:1)*(boomT>.1?.62:1),t,.24);
  musicNodes.menuBus.gain.setTargetAtTime(playing?0:1,t,.47);
  musicNodes.gameBus.gain.setTargetAtTime(playing?1:0,t,.47);
  musicNodes.low.frequency.setTargetAtTime(playing?650:350,t,.6);
  const fighting=playing&&enemies.some(e=>e.hp>0&&e.alert&&Math.hypot(e.x-P.x,e.z-P.z)<16);
  const boss=playing&&currentBoss&&currentBoss.hp>0;
  const root=[55,65.4,49,58.3,51.9,55,61.7,49,58.3][(level-1)%9];
  musicNodes.combatOsc.frequency.setTargetAtTime(root*1.5,t,.35);
  musicNodes.bossOsc.frequency.setTargetAtTime(root,t,.35);
  musicNodes.combatG.gain.setTargetAtTime(fighting?.15*(.6+.4*Math.sin(t*6)**2):0,t,.55);
  musicNodes.bossG.gain.setTargetAtTime(boss?.085*(.65+.35*Math.sin(t*9)**2):0,t,.45);
  if(flameGain)flameGain.gain.setTargetAtTime(state==='playing'&&!paused&&P.wi===5&&(keys.mouse||keys.Space||keys.KeyF)&&P.ammo>0?.35*SET.vol:0,t,.075);
  if(saberGain){const sp=(gunModels[7]&&gunModels[7].userData.bladeProgress)||0;saberGain.gain.setTargetAtTime(state==='playing'&&!paused&&P.wi===7?.005*SET.vol+.024*sp*SET.vol:0,t,.08);}
}
function bladeSound(i){
  // Katana gets a steel-air whoosh; the energy saber gets a brighter charged sweep.
  if(i===6){noise(.36,6200,420,.52,'bandpass');noise(.15,11000,1800,.17,'highpass');beep(910,.12,'triangle',.06,-520);beep(520,.18,'sine',.05,-150);}
  else{beep(210,.34,'sawtooth',.14,1450);beep(610,.18,'triangle',.08,-420);noise(.34,7600,360,.44,'bandpass');noise(.11,11500,2100,.18,'highpass');}
}
function bladeImpactSound(i,x,z){
  const pan=pan3(x,z);
  if(i===6){noise(.28,7000,720,.46,'bandpass',pan);noise(.085,11800,1800,.33,'highpass',pan);beep(1320,.10,'triangle',.15,-860);beep(210,.12,'sine',.07,-40);}
  else{noise(.24,9200,420,.52,'bandpass',pan);noise(.11,12500,1700,.24,'highpass',pan);beep(640,.24,'sawtooth',.18,-420);beep(190,.27,'sine',.13,-120);}
}
function gunSound(i){
  if(i>=6){bladeSound(i);return;}

  if(i===0){ noise(0.18,5200,300,0.55,'lowpass'); noise(0.05,9000,2500,0.3,'highpass'); beep(170,0.1,'sine',0.2,-100); }
  else if(i===1){ noise(0.55,3200,70,0.95,'lowpass'); beep(65,0.4,'sine',0.4,-30); noise(0.09,8000,1500,0.4,'highpass'); }
  else if(i===2){ noise(0.09,6500,500,0.4,'lowpass'); beep(240,0.05,'square',0.08,-130); }
  else if(i===3){ noise(0.19,4500,280,0.62,'lowpass'); noise(0.035,7000,1400,0.19,'highpass'); beep(112,0.16,'sine',0.21,-65); }
  else if(i===4){ beep(120,0.22,'square',0.22,-70); noise(0.14,1300,180,0.5,'lowpass'); }
  else { if(actx&&actx.currentTime-flameSoundAt>.14){ flameSoundAt=actx.currentTime;noise(.23,3400,280,.52,'lowpass');noise(.10,7800,900,.23,'highpass');} }
}
function vol3(x,z,max){ return Math.max(0,1-Math.hypot(x-P.x,z-P.z)/max); }
function pan3(x,z){ const d=Math.hypot(x-P.x,z-P.z)||1; return ((x-P.x)*Math.cos(P.yaw)-(z-P.z)*Math.sin(P.yaw))/d; }
function footstep(sprint){ stepL=!stepL; noise(0.09,sprint?750:520,110,0.3,'lowpass',stepL?-0.25:0.25); beep(65+Math.random()*25,0.07,'sine',0.12,-30); }
function creatureSound(type,x,z,attack=false){
  if(!actx||SET.vol<=0)return;
  const bestiaryType=window.DEPTHS_BESTIARY&&window.DEPTHS_BESTIARY.adaptEnemyId(type);
  if(bestiaryType){window.DEPTHS_BESTIARY.voice(bestiaryType,actx,attack);return;}
  const d=Math.hypot(x-P.x,z-P.z),v=Math.max(0,1-d/27);
  if(v<.035)return;
  const pan=pan3(x,z), t=actx.currentTime;
  const panner=actx.createStereoPanner?actx.createStereoPanner():null;
  if(panner){panner.pan.value=Math.max(-.85,Math.min(.85,pan));panner.connect(actx.destination);}
  const dst=panner||actx.destination;
  const profiles={
    chaser:[110,47,.4,'sawtooth',.16],shooter:[350,95,.68,'sine',.11],
    brute:[67,31,1.02,'sawtooth',.25],teleporter:[470,115,.55,'triangle',.14],
    splitter:[170,66,.63,'square',.09],mini:[300,120,.25,'triangle',.07],
    boss:[54,24,1.45,'sawtooth',.35],
    stalker:[147,36,.55,'triangle',.13],crawler:[280,62,.32,'sawtooth',.12],
    necromancer:[258,115,.88,'sine',.12],winged:[620,185,.69,'sawtooth',.18]
  };
  const [start,end,length,wave,gain]=profiles[type]||profiles.chaser;
  try{
    const osc=actx.createOscillator(),filter=actx.createBiquadFilter(),amp=actx.createGain();
    osc.type=wave;osc.frequency.setValueAtTime(start*(attack?1.32:1),t);
    osc.frequency.exponentialRampToValueAtTime(end,t+length);
    filter.type='lowpass';filter.frequency.setValueAtTime(type==='shooter'?2400:1000,t);
    filter.frequency.exponentialRampToValueAtTime(180,t+length);
    amp.gain.setValueAtTime(.0001,t);
    amp.gain.exponentialRampToValueAtTime(gain*v*SET.vol+.0001,t+.06);
    amp.gain.exponentialRampToValueAtTime(.0001,t+length);
    osc.connect(filter);filter.connect(amp);amp.connect(dst);osc.start(t);osc.stop(t+length+.03);
  }catch(e){}
  if(type==='boss'||type==='brute')noise(.32,500,55,.22*v,'lowpass',pan);
  else if(type==='splitter')noise(.16,2400,150,.13*v,'bandpass',pan);
  else if(type==='shooter')noise(.22,3100,270,.14*v,'bandpass',pan);
  else if(type==='winged')noise(.29,6500,1450,.16*v,'highpass',pan);
  else if(type==='crawler')noise(.16,2500,360,.13*v,'bandpass',pan);
  else if(type==='necromancer')noise(.28,1200,80,.10*v,'lowpass',pan);
}
function growl(e,big){creatureSound(e.type,e.x,e.z,false);}
let dungeonAmbienceClock=7;
function dungeonAmbience(dt){
  dungeonAmbienceClock-=dt;
  if(dungeonAmbienceClock>0||!actx||SET.vol===0||state!=='playing')return;
  dungeonAmbienceClock=6+Math.random()*8;
  const type=(level-1)%DUNGEON_THEMES.length;
  if(type===3){beep(520,.18,'sine',.025,-380);noise(.27,1800,200,.10,'bandpass');}
  else if(type===1||type===4){noise(.24,1700,100,.15,'highpass');beep(130,.43,'triangle',.046,-90);}
  else if(type===2||type===5){noise(.52,700,60,.16,'lowpass');beep(65,.43,'sine',.057,-25);}
  else{noise(.32,880,95,.11,'bandpass');beep(93,.3,'triangle',.023,-48);}
}

// ---------- state ----------
let state='ready', paused=false;
let level=1, grid=null, GW=0, GH=0, explored=null;
let levelGroup=null, portal=null, portalOpen=false, exitCell=[1,1];
let lastMapDraw=-1,mapExpanded=false,mapZoom=1,mapRotate=false;
let enemies=[], pickups=[], orbs=[], fx=[], shots=[], hazards=[], secretWalls=[], runicSwitches=[], totalEnemies=0, killsThisLevel=0;
const P={x:0,z:0,yaw:0,pitch:0,hp:100,maxhp:100,armor:25,ammo:80,score:0,cool:0,kills:0,r:0.4,wi:0,inv:0,combo:0,ct:0,shake:0,dmgm:1,rate:1,leech:0,scav:0,spd:1,entry:null,coins:0,keys:0,potions:2,stamina:100,maxStamina:100,energy:100,reloadT:0,reloadWi:-1};
const MAG_CAP=[7,6,30,30,1,85];
const magazines=MAG_CAP.slice();
const MASTERY=Array(8).fill(0);
const WEAPON_LEVELS=Array(8).fill(0);
const GUN_TECH={capacity:Array(6).fill(0),reload:Array(6).fill(0),accuracy:Array(6).fill(0),recoil:Array(6).fill(0),velocity:Array(6).fill(0)};
const BASE_CAP=MAG_CAP.slice();

let rifleMode='AUTO',burstQueue=0,triggerHeld=false,pendingSaberCharge=0,parryWindow=0;
let campaignSeed=1234567,activeObjective='Eliminate the guardians',floorKeyNeeded=false,floorKeyCollected=false,floorSwitchNeeded=false,floorSwitchOn=false;
let inventoryOpen=false,applyingSave=false,gameSession=0;
let recentNoise=null;
let bossTelegraphs=[];
let currentBoss=null;
function emitNoise(x,z,range){
 recentNoise={x,z,range,at:time};
 for(const e of enemies){const d=Math.hypot(e.x-x,e.z-z);
  if(d<range*(e.type==='stalker'?1.4:1)){e.alert=true;e.heard={x,z};e.huntTimer=6.5;if(!e.gr)e.gr=0.35;}
 }
}


let decals=[], checkpoints=[], lastCP=null, flames=[], barrels=[], gpHeld=false;
let bladeSwing=0, bladeHitT=0, lastWeaponSelect=0, bladeElapsed=0, bladeDuration=.5, pendingMelee=null, saberDraw=0;
let muzzle=0, recoil=0, walkT=0, flashA=0, time=0, bobAmt=0, lastWalkT=0, heat=0, boomT=0, hitT=0, hbLast='', amLast='';
const keys={};
// v5.1 gameplay systems: frame-independent dodge motion and directional guard.
const DEFENSE={dodgeTime:0,dodgeCooldown:0,dodgeX:0,dodgeZ:0,guard:'high',exhausted:0};
const EQUIPMENT={helmet:0,chest:0,gauntlets:0,legs:0};
const RELICS={vigor:false,duelist:false,bulwark:false};
const RELIC_DATA={vigor:{price:100,name:'Relic of Vigor',desc:'Stamina regenerates 25% faster'},duelist:{price:125,name:'Duelist Sigil',desc:'Melee damage +12%, maximum armour -10'},bulwark:{price:140,name:'Stone Heart',desc:'Incoming damage -12%, sprint speed -7%'}};
const ARMOUR_DATA={helmet:{price:65,name:'Helmet',reduction:.035},chest:{price:120,name:'Chest armour',reduction:.075},gauntlets:{price:65,name:'Gauntlets',reduction:.035},legs:{price:85,name:'Leg armour',reduction:.045}};
function armourReduction(){return Math.min(.45,Object.keys(EQUIPMENT).reduce((v,k)=>v+EQUIPMENT[k]*ARMOUR_DATA[k].reduction,0)+(RELICS.bulwark?.12:0));}
function masteryTier(i){return Math.min(5,Math.floor(Math.sqrt(Math.max(0,MASTERY[i])/250)));}
function weaponDamageBonus(i){return 1+masteryTier(i)*.025+(i>=6&&RELICS.duelist?.12:0);}
function beginDodge(){
 if(state!=='playing'||paused||DEFENSE.dodgeCooldown>0||DEFENSE.dodgeTime>0||P.stamina<24||DEFENSE.exhausted>0)return false;
 const forward=(keys.KeyW?1:0)-(keys.KeyS?1:0),right=(keys.KeyD?1:0)-(keys.KeyA?1:0);
 const f=forward||(!right?1:0),r=right,n=Math.hypot(f,r)||1;
 DEFENSE.dodgeX=(-Math.sin(P.yaw)*f+Math.cos(P.yaw)*r)/n;
 DEFENSE.dodgeZ=(-Math.cos(P.yaw)*f-Math.sin(P.yaw)*r)/n;
 DEFENSE.dodgeTime=.23;DEFENSE.dodgeCooldown=.8;P.stamina-=24;
 P.inv=Math.max(P.inv,.13);beep(330,.07,'triangle',.025,-130);return true;
}
function activeGuardDirection(){if(keys.KeyA)return 'left';if(keys.KeyD)return 'right';if(keys.KeyS)return 'low';return 'high';}

const WEAPONS=[
 {n:'Desert Eagle',cd:.34,cost:1,dmg:2.8,pel:1,spr:.008,pierce:false,col:0xb8bcc5,len:1.05,d:'Heavy semi-auto pistol with serious stopping power'},
 {n:'Remington 870',cd:.82,cost:3,dmg:1.35,pel:8,spr:.13,pierce:false,col:0xa0663a,len:.95,d:'Pump-action shotgun. Devastating up close'},
 {n:'UMP9',cd:.085,cost:1,dmg:1.05,pel:1,spr:.04,pierce:false,col:0x5d748a,len:1.02,d:'Controlled automatic fire for close to mid range'},
 {n:'AK-86',cd:.12,cost:1,dmg:2.1,pel:1,spr:.028,pierce:false,col:0xb56b2a,len:1.15,d:'AK-pattern assault rifle with hard-hitting rifle rounds'},
 {n:'M79 Grenade',cd:1,cost:5,dmg:6.5,pel:1,spr:.008,pierce:false,blast:4.5,col:0x7acb4a,len:1,d:'Single-shot grenade launcher with a heavy blast'},
 {n:'M2 Flamethrower',cd:.06,cost:1,dmg:.8,pel:3,spr:.18,pierce:true,rng:8,burn:4,col:0xff6a2a,len:1,d:'Backpack flamethrower that ignites enemies'},
 {n:'Katana',short:'Katana',cd:.52,cost:0,dmg:7,pel:1,spr:0,pierce:true,rng:2.45,melee:true,col:0xe7e8e1,len:1.2,d:'Fast steel slash. No ammunition needed'},
 {n:'Light Saber',short:'Light Saber',cd:.41,cost:0,dmg:9,pel:1,spr:0,pierce:true,rng:3.5,melee:true,col:0x54d7ff,len:1.4,d:'High-energy blade. No ammunition needed'}];
WEAPONS.forEach(function(w,i){ w.ico=iconMark(['pistol','shotgun','smg','rifle','grenade','flame','katana','saber'][i],21); w.short=w.short||['Desert Eagle','Remington 870','UMP9','AK-86','M79','M2 Flame'][i]; });
const PERKS=[
 {n:'Hollow Points',i:'Target',d:'+25% weapon damage',f:function(){P.dmgm*=1.25;}},
 {n:'Quick Hands',i:'Stamina',d:'Fire 20% faster',f:function(){P.rate*=0.8;}},
 {n:'Iron Skin',i:'Armor',d:'+25 max HP and full heal',f:function(){P.maxhp+=25;P.hp=P.maxhp;}},
 {n:'Vampiric',i:'Blood',d:'Heal 2 HP on every kill',f:function(){P.leech+=2;}},
 {n:'Scavenger',i:'Pack',d:'+40 ammo now, ammo pickups +50%',f:function(){P.ammo+=40;P.scav+=0.5;}},
 {n:'Light Boots',i:'Speed',d:'+15% movement speed',f:function(){P.spd*=1.15;}}];
const DIFF={Easy:{d:.7,c:.8},Normal:{d:1,c:1},Hard:{d:1.4,c:1.3}};
const BASE_GUN_RELOAD=[1.55,2.6,1.9,2.15,2.7,2.1],BASE_GUN_VELOCITY=[125,95,145,175,25,18];
const BASE_GUN_SPREAD=WEAPONS.slice(0,6).map(w=>w.spr),BASE_GUN_RECOIL=KICK.slice(0,6);
WEAPONS.forEach((w,i)=>{if(i<6){w.mag=MAG_CAP[i];w.reload=BASE_GUN_RELOAD[i];w.velocity=BASE_GUN_VELOCITY[i];w.gravity=[1.4,2.0,1.0,1.0,16,0][i];}});
function applyGunTech(){
 for(let i=0;i<6;i++){
  MAG_CAP[i]=BASE_CAP[i]+GUN_TECH.capacity[i]*(i===5?12:i===2||i===3?5:1);
  WEAPONS[i].mag=MAG_CAP[i];WEAPONS[i].reload=BASE_GUN_RELOAD[i]*Math.pow(.90,GUN_TECH.reload[i]);
  WEAPONS[i].spr=BASE_GUN_SPREAD[i]*Math.pow(.87,GUN_TECH.accuracy[i]);
  WEAPONS[i].velocity=BASE_GUN_VELOCITY[i]*(1+GUN_TECH.velocity[i]*.08);
  KICK[i]=BASE_GUN_RECOIL[i]*Math.pow(.88,GUN_TECH.recoil[i]);
  magazines[i]=Math.min(magazines[i],MAG_CAP[i]);
 }
}

let startW=0, difficulty='Normal', menuKind='main', menuTab='play', mode='Normal', perkChoices=[];
function setWeapon(i){ if(!WEAPONS[i])return; bladeSwing=0;pendingMelee=null;slashFX.visible=false; P.wi=i;burstQueue=0; gunModels.forEach(function(g,k){g.visible=(k===i);}); if(i!==7&&gunModels[7]&&gunModels[7].userData.bladeProgress!==undefined)gunModels[7].userData.bladeProgress=0; if(i===7){const U=gunModels[7].userData;U.bladeProgress=0;for(const blade of [U.bladeAura,U.bladeCore,U.bladeWhite])if(blade)blade.scale.y=.001; ensureGameAudio(); if(actx&&SET.vol>0){beep(118,.20,'sawtooth',.06,820);beep(182,.23,'triangle',.04,540);noise(.18,7200,420,.16,'bandpass');}} lastWeaponSelect=performance.now();hbLast='';toast(WEAPONS[i].n,750);menuClickSound('equip'); }
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
  const rooms=3+Math.floor(n/6);
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

// ---------- cathedral architecture and floor-specific art direction ----------
// Six themes each have distinct masonry, floor slabs, fog, accent materials,
// pillars and room dressing. Canvas textures keep the game self-contained.
function makeRuinTexture(base,mortar,kind,seed){
  const c=document.createElement('canvas');c.width=c.height=768;
  const ctx=c.getContext('2d');let a=(seed*1664525+1013904223)|0;
  const rng=()=>{a=(Math.imul(a,1664525)+1013904223)|0;return (a>>>0)/4294967296;};
  ctx.fillStyle=mortar;ctx.fillRect(0,0,768,768);
  const slab=kind==='floor';
  if(slab){
    const cols=5,rows=5,w=768/cols,h=768/rows;
    for(let row=0;row<rows;row++)for(let col=0;col<cols+1;col++){
      const off=(row%2)*w*.5,x=col*w-off+2,y=row*h+2;
      ctx.fillStyle=base;ctx.fillRect(x,y,w-5,h-5);
      ctx.fillStyle='rgba(255,245,220,.06)';ctx.fillRect(x+5,y+5,w-18,4);
      ctx.fillStyle='rgba(0,0,0,.22)';ctx.fillRect(x+w-15,y+4,6,h-12);
      for(let k=0;k<34;k++){const xx=x+8+rng()*(w-16),yy=y+8+rng()*(h-16),s=.6+rng()*5;ctx.fillStyle=rng()>.62?'rgba(0,0,0,.13)':'rgba(240,224,195,.05)';ctx.fillRect(xx,yy,s,s);}
      if(rng()>.35){ctx.strokeStyle='rgba(15,13,14,.37)';ctx.lineWidth=1+rng()*1.6;ctx.beginPath();let xx=x+rng()*w,yy=y+rng()*h;ctx.moveTo(xx,yy);for(let j=0;j<7;j++){xx+=(rng()-.5)*34;yy+=10+rng()*16;ctx.lineTo(xx,yy);}ctx.stroke();}
    }
  }else{
    const cols=4,w=768/cols;
    for(let col=0;col<cols;col++){
      const x=col*w;
      ctx.fillStyle=base;ctx.fillRect(x+4,0,w-8,768);
      ctx.fillStyle='rgba(255,246,220,.05)';ctx.fillRect(x+8,0,6,768);
      ctx.fillStyle='rgba(0,0,0,.18)';ctx.fillRect(x+w-13,0,7,768);
      for(let y=0;y<768;y+=96){ctx.fillStyle='rgba(0,0,0,.16)';ctx.fillRect(x+4,y,w-8,5);}
      if(col<cols-1){ctx.fillStyle=mortar;ctx.fillRect(x+w-4,0,8,768);}
      const archX=x+w*.5;
      ctx.strokeStyle='rgba(14,12,16,.28)';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(archX-62,236);ctx.lineTo(archX-62,115);ctx.quadraticCurveTo(archX,32,archX+62,115);ctx.lineTo(archX+62,236);ctx.stroke();
      ctx.strokeStyle='rgba(232,214,180,.035)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(archX-44,220);ctx.lineTo(archX-44,122);ctx.quadraticCurveTo(archX,62,archX+44,122);ctx.lineTo(archX+44,220);ctx.stroke();
      for(let i=0;i<7;i++){const yy=45+rng()*690;ctx.fillStyle='rgba(0,0,0,'+(.04+rng()*.05)+')';ctx.fillRect(x+30+rng()*(w-60),yy,4+rng()*6,30+rng()*90);}
      for(let i=0;i<90;i++){const xx=x+12+rng()*(w-24),yy=18+rng()*732,s=.6+rng()*5;ctx.fillStyle=rng()>.58?'rgba(0,0,0,.12)':'rgba(242,227,202,.05)';ctx.fillRect(xx,yy,s,s);}
    }
    for(let row=0;row<8;row++){const y=row*96+2;ctx.fillStyle='rgba(0,0,0,.16)';ctx.fillRect(0,y,768,6);}
  }
  const vign=ctx.createRadialGradient(384,384,160,384,384,470);vign.addColorStop(0,'rgba(0,0,0,0)');vign.addColorStop(1,'rgba(0,0,0,.22)');ctx.fillStyle=vign;ctx.fillRect(0,0,768,768);
  for(let i=0;i<7200;i++){const x=rng()*768,y=rng()*768;ctx.fillStyle=rng()>.5?'rgba(0,0,0,.10)':'rgba(220,209,186,.06)';ctx.fillRect(x,y,1+rng()*2,1+rng()*2);}
  const tex=new THREE.CanvasTexture(c);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;
  tex.anisotropy=6;tex.needsUpdate=true;return tex;
}

// Cached 256px procedural micro-roughness maps; generated once per theme, not per frame.
function makeRoughnessTexture(seed){
 const c=document.createElement('canvas');c.width=c.height=256;
 const ctx=c.getContext('2d');const pixels=ctx.createImageData(256,256);let n=seed>>>0;
 for(let i=0;i<256*256;i++){
  n=(Math.imul(n,1664525)+1013904223)>>>0;
  const value=155+((n>>>20)%68);
  pixels.data[4*i]=pixels.data[4*i+1]=pixels.data[4*i+2]=value;pixels.data[4*i+3]=255;
 }
 ctx.putImageData(pixels,0,0);
 const tex=new THREE.CanvasTexture(c);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.needsUpdate=true;return tex;
}
// Black emissive mask with narrow orange branching lava veins for the Infernal Sanctum.
function makeLavaVeinTexture(seed){
 const c=document.createElement('canvas');c.width=c.height=512;
 const ctx=c.getContext('2d');ctx.fillStyle='#000';ctx.fillRect(0,0,512,512);
 let n=seed>>>0;const random=()=>{n=(Math.imul(n,1664525)+1013904223)>>>0;return n/4294967296;};
 for(let i=0;i<23;i++){
  let x=random()*512,y=random()*512;
  const pts=[[x,y]];
  for(let j=0;j<9;j++){x+=(random()-.5)*65;y+=16+random()*28;pts.push([x,y]);}
  for(const [width,color] of [[7,'rgba(183,28,3,.21)'],[2.4,'rgba(255,67,4,.65)'],[.75,'rgba(255,166,31,.92)']]){
   ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineJoin='round';ctx.beginPath();
   pts.forEach(([a,b],j)=>j?ctx.lineTo(a,b):ctx.moveTo(a,b));ctx.stroke();
  }
 }
 const tex=new THREE.CanvasTexture(c);tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.needsUpdate=true;return tex;
}
const DUNGEON_THEMES=[
  {name:'The Ashen Cloister',wall:'#55545c',mortar:'#21222c',floor:'#3c373b',joint:'#14151b',fog:0x070911,accent:0xb89879,torch:0xff8a41,trim:0x645e60,mood:'basalt and ash'},
  {name:'The Ossuary',wall:'#716756',mortar:'#312821',floor:'#534839',joint:'#2b211a',fog:0x100d09,accent:0xcdbca3,torch:0xe7b875,trim:0x9d8161,mood:'ancient bone chambers'},
  {name:'The Blood Basilica',wall:'#644649',mortar:'#291a20',floor:'#422b2f',joint:'#200d14',fog:0x160609,accent:0xaa5254,torch:0xff5740,trim:0x76373d,mood:'ruined red chapels'},
  {name:'The Drowned Nave',wall:'#455e62',mortar:'#203339',floor:'#32484b',joint:'#19282f',fog:0x03191d,accent:0x5cabad,torch:0x79ced4,trim:0x587c7d,mood:'submerged cathedral'},
  {name:'The Royal Catacombs',wall:'#5e546b',mortar:'#242032',floor:'#40394d',joint:'#1b172a',fog:0x0e0a1d,accent:0xa68bc0,torch:0xdab4f6,trim:0x6f6183,mood:'violet tombs'},
  {name:'The Infernal Sanctum',wall:'#242023',mortar:'#09090b',floor:'#211919',joint:'#08090b',fog:0x0c0504,accent:0xe64c18,torch:0xff5c18,trim:0x3b2a25,mood:'charred basalt and magma fissures'},
  {name:'The Haunted Scriptorium',wall:'#48534b',mortar:'#18231d',floor:'#353c32',joint:'#131b15',fog:0x080f0b,accent:0xa0c596,torch:0xa5cc76,trim:0x616d52,mood:'haunted library'},
  {name:'The Sunken Temple',wall:'#5b5948',mortar:'#29291f',floor:'#484b39',joint:'#1d241e',fog:0x0c1510,accent:0xacae6e,torch:0x80ad8a,trim:0x62694b,mood:'ancient temple'},
  {name:'The Ember Fortress',wall:'#66534e',mortar:'#2a2022',floor:'#3b302f',joint:'#1c1416',fog:0x1e1010,accent:0xe6a05d,torch:0xf08848,trim:0x88605a,mood:'abandoned fortress'}
 ].map((theme,i)=>({...theme,wallMap:makeRuinTexture(theme.wall,theme.mortar,'wall',i+11),floorMap:makeRuinTexture(theme.floor,theme.joint,'floor',i+31),roughnessMap:makeRoughnessTexture(i+310),lavaMap:i===5?makeLavaVeinTexture(712):null}));
let currentTheme=DUNGEON_THEMES[0];

// A single gateway factory serves all floor themes; no frame-time geometry allocations.
const PORTAL_SKINS=[
  [0x7daec9,0x343444,0x9dc5f4], [0xc0a078,0x494035,0xf5d2a0],
  [0xbf4660,0x352730,0xf07799], [0x40b3b0,0x263a3e,0x71ffdf],
  [0x7864e8,0x535164,0xc1b7ff], [0xff5722,0x17191c,0xffac35],
  [0x69d47d,0x34453a,0xbdff88], [0xd4bf68,0x6a5e43,0xfff1bb],
  [0xe87732,0x262023,0xffad66]
];
const PORTAL_VERTEX=`varying vec2 vUv; varying vec3 vEye; void main(){vUv=uv;vec4 mv=modelViewMatrix*vec4(position,1.);vEye=-mv.xyz;gl_Position=projectionMatrix*mv;}`;
const PORTAL_FRAGMENT=`precision highp float;
varying vec2 vUv;varying vec3 vEye;
uniform float uTime;uniform float uOpen;uniform float uNear;
uniform vec3 uColor;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453123);}
float noise2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}
float fbm(vec2 p){float a=.5,n=0.;for(int i=0;i<4;i++){n+=a*noise2(p);p=p*2.03+vec2(14.7,5.1);a*=.5;}return n;}
void main(){vec2 p=vUv*2.-1.;float r=length(p);if(r>1.)discard;
float a=atan(p.y,p.x);float t=uTime*(.27+uNear*.35);
float tw=a+3.5/(r+.3)+t*.95+fbm(p*3.+t*.12)*2.2;
vec2 q=vec2(cos(tw),sin(tw))*max(r,.015);
float n=fbm(q*5.5+vec2(t*.1,-t*.17));
float bands=sin(23.*r-7.*tw-t*4.+n*5.);
float tunnel=pow(1.-r,1.2);float bright=pow(max(0.,1.-r),3.5)*2.0;
float rays=.3+.7*pow(max(0.,sin(8.*tw+22.*r+t*2.)),6.);
float rim=pow(max(0.,r),8.);
vec3 c=mix(uColor*.075,uColor*(.5+n*.75),(1.-smoothstep(.18,.95,r)));
c+=uColor*(.1+.2*bands)*tunnel + vec3(.72,.85,1.)*bright*.9;
c+=uColor*rim*(.35+rays*.65);
float opacity=mix(.18,1.,uOpen)*(1.-smoothstep(.98,1.,r));
gl_FragColor=vec4(c,opacity);
}`;
function createAbyssalGateway(t,boss){
 const pal=PORTAL_SKINS[t%PORTAL_SKINS.length],g=new THREE.Group(),scale=boss?1.22:1;
 g.scale.setScalar(scale);
 const metal=new THREE.MeshStandardMaterial({color:0x25252b,roughness:.48,metalness:.72});
 const stone=new THREE.MeshStandardMaterial({color:pal[1],roughness:.96,metalness:.05,flatShading:true});
 const sigil=new THREE.MeshStandardMaterial({color:0x461b24,emissive:0x5a0a1a,emissiveIntensity:.24,roughness:.4});
 const make=(geo,mat,x,y,z)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;g.add(m);return m;};
 const ring=make(new THREE.TorusGeometry(1.23,.22,12,48),stone,0,2.0,0);
 make(new THREE.TorusGeometry(1.47,.07,8,64),metal,0,2.0,0);
 const rotor=make(new THREE.TorusGeometry(1.38,.055,7,56),sigil,0,2.0,.09);
 const disc=new THREE.Mesh(new THREE.CircleGeometry(1.10,64),new THREE.ShaderMaterial({vertexShader:PORTAL_VERTEX,fragmentShader:PORTAL_FRAGMENT,uniforms:{uTime:{value:0},uOpen:{value:0},uNear:{value:0},uColor:{value:new THREE.Color(pal[0])}},transparent:true,depthWrite:false,side:THREE.DoubleSide}));
 disc.position.set(0,2,.08);g.add(disc);
 const runes=[];for(let i=0;i<20;i++){
  const a=Math.PI*2*i/20;
  const m=make(new THREE.BoxGeometry(.105,.18,.035),sigil,Math.sin(a)*1.24,2+Math.cos(a)*1.24,.19);
  m.rotation.z=-a; runes.push(m);
 }
 for(const x of [-1.53,1.53]){
  const c=make(new THREE.CylinderGeometry(.24,.30,3.65,8),stone,x,1.82,.03);
  make(new THREE.BoxGeometry(.66,.30,.68),metal,x,.23,.03);
  make(new THREE.BoxGeometry(.66,.29,.68),stone,x,3.62,.03);
 }
 const seal=make(new THREE.IcosahedronGeometry(.29,1),sigil,0,2,.22);
 const shards=[];for(let i=0;i<14;i++){
  const m=make(new THREE.TetrahedronGeometry(.085+(i%3)*.025),stone,0,0,0);
  shards.push(m);
 }
 const ground=make(new THREE.RingGeometry(.45,1.54,50),new THREE.MeshBasicMaterial({color:pal[2],transparent:true,opacity:.12,side:THREE.DoubleSide,depthWrite:false}),0,.035,0);ground.rotation.x=-Math.PI/2;
 const light=new THREE.PointLight(pal[0],0.2,15,2);light.position.y=2.1;g.add(light);
 const rays=[];for(let i=0;i<5;i++){
  const m=make(new THREE.PlaneGeometry(.14,3.1),new THREE.MeshBasicMaterial({color:pal[0],transparent:true,opacity:.04,side:THREE.DoubleSide,depthWrite:false}),0,2,0);
  m.rotation.z=i*Math.PI/5; rays.push(m);
 }
 g.userData={ring,disc,light,rotor,runes,seal,shards,ground,rays,pal,phase:0,boss};
 return g;
}
function updateAbyssalGateway(g,dt,clock,open,px,pz){
 if(!g)return;const d=g.userData;
 const distance=Math.hypot(px-g.position.x,pz-g.position.z);
 if(open&&d.phase<1)d.phase=Math.min(1,d.phase+dt/2.4);
 const power=open?d.phase:0;
 d.disc.material.uniforms.uTime.value=clock;
 d.disc.material.uniforms.uOpen.value=power;
 d.disc.material.uniforms.uNear.value=Math.max(0,1-distance/7);
 d.rotor.rotation.z+=dt*(open?.27:.04);
 d.ring.rotation.z+=dt*.025;
 d.seal.visible=!open;d.seal.rotation.y+=dt;
 d.seal.scale.setScalar(1+Math.sin(clock*7)*.12);
 d.light.intensity=.18+power*(1.3+.27*Math.sin(clock*4));
 d.ground.material.opacity=.035+power*.17;
 for(let i=0;i<d.runes.length;i++){
  const lit=open&&i<Math.floor(power*d.runes.length);
  d.runes[i].material.emissive.setHex(open?d.pal[0]:0x681620);
  // A shared material is deliberate: sequential ignition uses per-object visibility.
  d.runes[i].scale.setScalar(lit?1+.23*Math.sin(clock*5+i):.7);
 }
 for(let i=0;i<d.shards.length;i++){
  const a=clock*(.18+i*.012)+i*6.28318/d.shards.length;
  const r=1.55+.13*Math.sin(clock+i);
  d.shards[i].position.set(Math.cos(a)*r,2+Math.sin(a)*r,Math.sin(clock*.6+i)*.19);
  d.shards[i].rotation.x+=dt*.27;d.shards[i].rotation.y+=dt*.33;
 }
 for(let i=0;i<d.rays.length;i++)d.rays[i].material.opacity=power*.037;
}

const ANCIENT_GEO={skull:new THREE.SphereGeometry(1,18,14),jaw:new THREE.SphereGeometry(1,12,9),pillar:new THREE.CylinderGeometry(.27,.31,3.35,10),bone:new THREE.CylinderGeometry(.054,.075,.9,9)};
const ancientBone=new THREE.MeshStandardMaterial({color:0xbcb19a,roughness:.88,metalness:.04});
const ancientDark=new THREE.MeshStandardMaterial({color:0x151112,roughness:1});
const ancientIron=new THREE.MeshStandardMaterial({color:0x454b50,metalness:.72,roughness:.63});
const ancientBlood=new THREE.MeshStandardMaterial({color:0x46070d,metalness:.28,roughness:.23,transparent:true,opacity:.94,depthWrite:false,side:THREE.DoubleSide});
const bloodBorder=new THREE.MeshBasicMaterial({color:0x210709,transparent:true,opacity:.9,depthWrite:false,side:THREE.DoubleSide});
function dungeonPart(parent,geo,mat,x,y,z,sx=1,sy=1,sz=1){
  const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.scale.set(sx,sy,sz);parent.add(m);return m;
}
function dungeonBone(parent,from,to,r=.055,mat=ancientBone){
  const a=new THREE.Vector3(...from),b=new THREE.Vector3(...to),d=b.clone().sub(a);
  const m=new THREE.Mesh(new THREE.CylinderGeometry(r*.86,r,d.length(),9),mat);
  m.position.copy(a).add(b).multiplyScalar(.5);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());parent.add(m);return m;
}
function dungeonSkull(parent,x,y,z,scale=1){
  const head=new THREE.Group();head.position.set(x,y,z);head.scale.setScalar(scale);parent.add(head);
  dungeonPart(head,ANCIENT_GEO.skull,ancientBone,0,.10,0,.205,.23,.185);
  dungeonPart(head,ANCIENT_GEO.jaw,ancientBone,0,-.09,.068,.15,.09,.135);
  for(const sign of [-1,1]){
    dungeonPart(head,ANCIENT_GEO.skull,ancientDark,sign*.09,.088,.155,.060,.069,.038);
    dungeonPart(head,ANCIENT_GEO.skull,ancientBone,sign*.155,-.01,.09,.045,.05,.035);
  }
  dungeonPart(head,ANCIENT_GEO.skull,ancientDark,0,-.004,.183,.031,.05,.028);
  for(let i=0;i<6;i++)dungeonPart(head,new THREE.BoxGeometry(.03,.045,.026),ancientBone,(i-2.5)*.043,-.144,.16);
  return head;
}
function dungeonChain(parent,a,b,count=10){
  const p=new THREE.Vector3(...a),q=new THREE.Vector3(...b);
  for(let k=0;k<count;k++){
    const t=(k+.5)/count,at=p.clone().lerp(q,t);at.y-=.14*Math.sin(Math.PI*t);
    const link=new THREE.Mesh(new THREE.TorusGeometry(.055,.012,6,12),ancientIron);
    link.position.copy(at);link.rotation.y=k%2?Math.PI/2:0;parent.add(link);
  }
}
function dungeonPuddle(x,z,size=1){
  const puddle=new THREE.Group();puddle.position.set(x,0,z);
  const shape=new THREE.Shape(),rings=25;
  for(let j=0;j<=rings;j++){
    const a=j/rings*Math.PI*2,r=1+.19*Math.sin(a*3+x*1.2)+.12*Math.cos(a*7+z);
    const px=Math.cos(a)*size*r,pz=Math.sin(a)*size*.67*r;
    if(j===0)shape.moveTo(px,pz);else shape.lineTo(px,pz);
  }
  const geo=new THREE.ShapeGeometry(shape);
  const rim=dungeonPart(puddle,geo,bloodBorder,0,.010,0,1.08,1.08,1.08);rim.rotation.x=-Math.PI/2;
  const fill=dungeonPart(puddle,geo,ancientBlood,0,.017,0);fill.rotation.x=-Math.PI/2;
  for(let k=0;k<4;k++){
    const c=new THREE.Mesh(new THREE.CircleGeometry(.13+k*.04,15),new THREE.MeshBasicMaterial({color:0x992a2c,transparent:true,opacity:.14,depthWrite:false}));
    c.rotation.x=-Math.PI/2;c.position.set(Math.sin(k*1.4)*size*.4,.022,Math.cos(k*2)*size*.23);puddle.add(c);
  }
  levelGroup.add(puddle);
}
function dungeonSkeleton(x,z,wallX,wallZ){
  const root=new THREE.Group();root.position.set(x+wallX*1.54,0,z+wallZ*1.54);
  root.rotation.y=Math.atan2(-wallX,-wallZ);levelGroup.add(root);
  dungeonPart(root,ANCIENT_GEO.skull,ancientBone,0,1.55,.05,.16,.30,.11);
  dungeonSkull(root,0,2.66,.03,.86);
  dungeonBone(root,[0,2.42,0],[0,1.18,0],.075);
  dungeonPart(root,ANCIENT_GEO.skull,ancientBone,0,1.22,.10,.25,.10,.14);
  for(let j=0;j<5;j++){
    const y=2.18-j*.18,w=.31-j*.024;
    for(const side of [-1,1]){
      dungeonBone(root,[0,y,0],[side*w*.7,y-.085,.17],.028);
      dungeonBone(root,[side*w*.7,y-.085,.17],[side*w,y-.02,.04],.025);
    }
  }
  for(const sign of [-1,1]){
    dungeonBone(root,[sign*.28,2.3,0],[sign*.64,1.99,.14],.054);
    dungeonBone(root,[sign*.64,1.99,.14],[sign*.92,2.42,.13],.038);
    dungeonBone(root,[sign*.14,1.15,0],[sign*.25,.72,.16],.065);
    dungeonBone(root,[sign*.25,.72,.16],[sign*.32,.18,.05],.044);
    dungeonChain(root,[sign*.92,2.42,.13],[sign*1.26,3.32,-.12],9);
    dungeonPart(root,new THREE.SphereGeometry(.065,9,7),ancientIron,sign*1.26,3.32,-.12);
  }
  dungeonChain(root,[0,1.0,-.10],[.2,3.45,-.18],13);
}
function dungeonSkullPile(x,z,count){
  const pile=new THREE.Group();pile.position.set(x,0,z);levelGroup.add(pile);
  for(let k=0;k<count;k++){
    const a=k*2.399,dist=.1+.19*Math.sqrt(k);
    const skull=dungeonSkull(pile,Math.sin(a)*dist,.24+Math.floor(k/3)*.21,Math.cos(a)*dist,.60+Math.random()*.24);
    skull.rotation.set((Math.random()-.5)*.38,Math.random()*Math.PI*2,(Math.random()-.5)*.32);
  }
  for(let k=0;k<5;k++){
    const a=Math.random()*Math.PI*2;
    dungeonBone(pile,[Math.cos(a)*.22,.17,Math.sin(a)*.3],[Math.cos(a+1.3)*.42,.09,Math.sin(a+1.3)*.4],.045);
  }
}
function dungeonArch(x,z,axis){
  const root=new THREE.Group();root.position.set(x,0,z);root.rotation.y=axis?Math.PI/2:0;levelGroup.add(root);
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.wallMap,color:0xd0d0d0,roughness:.9,bumpMap:currentTheme.wallMap,bumpScale:.13});
  for(const side of [-1,1]){
    dungeonPart(root,ANCIENT_GEO.pillar,stone,side*1.46,1.68,0);
    dungeonPart(root,new THREE.BoxGeometry(.62,.2,.62),stone,side*1.46,3.34,0);
    dungeonPart(root,new THREE.BoxGeometry(.69,.26,.69),stone,side*1.46,.15,0);
  }
  const half=new THREE.Mesh(new THREE.TorusGeometry(1.46,.20,8,28,Math.PI),stone);
  half.position.set(0,3.31,0);root.add(half);
  const ornament=dungeonPart(root,new THREE.OctahedronGeometry(.22,0),stone,0,4.60,0);
  ornament.rotation.z=Math.PI/4;
}
function dungeonAltar(x,z){
  const g=new THREE.Group();g.position.set(x,0,z);levelGroup.add(g);
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.wallMap,roughness:.87});
  dungeonPart(g,new THREE.BoxGeometry(1.35,.45,.63),stone,0,.44,0);
  dungeonPart(g,new THREE.BoxGeometry(1.48,.12,.8),stone,0,.72,0);
  dungeonPart(g,new THREE.BoxGeometry(.9,.31,.55),stone,0,.16,0);
  dungeonSkull(g,0,.92,-.06,.83);
  for(const sign of [-1,1]){
    dungeonPart(g,new THREE.CylinderGeometry(.026,.036,.24,8),ancientBone,sign*.48,.91,-.07);
    const ember=new THREE.Mesh(new THREE.SphereGeometry(.055,9,7),new THREE.MeshBasicMaterial({color:currentTheme.torch}));
    ember.position.set(sign*.48,1.06,-.07);g.add(ember);
  }
}
// Wall-set stained glass, worn mosaics, small flood pools and glowing fissures.
function dungeonWallWindow(x,z,dx,dz,style){
  const root=new THREE.Group();root.position.set(x+dx*1.79,0,z+dz*1.79);
  root.rotation.y=Math.atan2(-dx,-dz);levelGroup.add(root);
  const shade=style===4?0x7f51c5:style===2?0xa93d44:0x4eafb1;
  const glass=new THREE.MeshBasicMaterial({color:shade,transparent:true,opacity:.83,side:THREE.DoubleSide});
  const frame=new THREE.MeshStandardMaterial({color:currentTheme.trim,metalness:.23,roughness:.72});
  const pane=new THREE.Shape();pane.moveTo(-.48,1.55);pane.lineTo(-.48,3.2);
  pane.quadraticCurveTo(-.48,3.63,0,3.91);pane.quadraticCurveTo(.48,3.63,.48,3.2);
  pane.lineTo(.48,1.55);pane.closePath();
  dungeonPart(root,new THREE.ShapeGeometry(pane),glass,0,0,.08);
  dungeonBone(root,[-.52,1.55,.10],[-.52,3.20,.10],.048,frame);
  dungeonBone(root,[.52,1.55,.10],[.52,3.20,.10],.048,frame);
  dungeonBone(root,[0,1.55,.11],[0,3.90,.11],.034,frame);
  dungeonBone(root,[-.52,2.60,.12],[.52,2.60,.12],.028,frame);
  const upper=new THREE.Mesh(new THREE.TorusGeometry(.51,.047,8,18,Math.PI),frame);
  upper.position.set(0,3.23,.11);root.add(upper);
  for(let i=0;i<4;i++){
    const gem=new THREE.Mesh(new THREE.OctahedronGeometry(.09,0),new THREE.MeshBasicMaterial({color:i%2?0xffb667:shade,transparent:true,opacity:.95}));
    gem.position.set((i-1.5)*.19,2.82+(i%2)*.3,.14);root.add(gem);
  }
}
function dungeonWater(x,z,r){
  const g=new THREE.Group();g.position.set(x,.018,z);levelGroup.add(g);
  const sh=new THREE.Shape();for(let k=0;k<=25;k++){
    const a=k/25*Math.PI*2,rr=r*(1+.14*Math.sin(a*4+x));
    const xx=Math.cos(a)*rr,yy=Math.sin(a)*rr*.72;
    if(!k)sh.moveTo(xx,yy);else sh.lineTo(xx,yy);
  }
  const mat=new THREE.MeshStandardMaterial({color:0x173c46,metalness:.72,roughness:.14,transparent:true,opacity:.8,side:THREE.DoubleSide});
  const surface=new THREE.Mesh(new THREE.ShapeGeometry(sh),mat);surface.rotation.x=-Math.PI/2;g.add(surface);
  const edge=new THREE.Mesh(new THREE.RingGeometry(r*.38,r*.42,24),new THREE.MeshBasicMaterial({color:0x6babb7,transparent:true,opacity:.13,depthWrite:false,side:THREE.DoubleSide}));
  edge.rotation.x=-Math.PI/2;edge.position.y=.007;g.add(edge);
}
function dungeonRubble(x,z){
  const group=new THREE.Group();group.position.set(x,0,z);levelGroup.add(group);
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.wallMap,roughness:.97});
  for(let i=0;i<7;i++){
    const a=i*2.4,dist=.22+.13*i;
    const block=new THREE.Mesh(new THREE.DodecahedronGeometry(.14+Math.random()*.22,0),stone);
    block.position.set(Math.sin(a)*dist,.10,Math.cos(a)*dist);block.rotation.set(Math.random()*3,Math.random()*3,Math.random()*3);group.add(block);
  }
}
function dungeonFissure(x,z){
  const points=[],a=Math.random()*6.28,dx=Math.cos(a),dz=Math.sin(a);
  for(let i=0;i<8;i++){
    const t=i/7-.5,side=Math.sin(i*2.7+x)*.22;
    points.push(new THREE.Vector3(x+dx*t*2.8-dz*side,.024,z+dz*t*2.8+dx*side));
  }
  const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:0xff6127,transparent:true,opacity:.75}));
  levelGroup.add(line);
  for(let k=0;k<2;k++){
    const light=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,color:0xff4b16,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}));
    light.position.set(x+(k-.5)*.9,.13,z);light.scale.set(.8,.8,1);levelGroup.add(light);
  }
}
function decorateDungeon(m,n){
  const locations=[],walls=[];
  for(let y=2;y<n-2;y++)for(let x=2;x<n-2;x++){
    if(grid[y][x]!==0||m.dist[y][x]<4||(x===exitCell[0]&&y===exitCell[1]))continue;
    const dirs=[[0,1],[0,-1],[1,0],[-1,0]].filter(([dx,dz])=>grid[y+dz][x+dx]===1);
    const item={x:(x+.5)*CELL,z:(y+.5)*CELL,gx:x,gz:y,dirs};
    locations.push(item);if(dirs.length)walls.push(item);
  }
  const take=(pool)=>pool.length?pool.splice(Math.floor(Math.random()*pool.length),1)[0]:null;
  for(let k=0;k<Math.min(3+Math.floor(level/3),8);k++){
    const c=take(locations);if(c)dungeonPuddle(c.x+(Math.random()-.5)*.35,c.z+(Math.random()-.5)*.35,.65+Math.random()*.65);
  }
  for(let k=0;k<Math.min(4+Math.floor(level/2),11);k++){
    const c=take(locations);if(c)dungeonSkullPile(c.x+(Math.random()-.5),c.z+(Math.random()-.5),2+Math.floor(Math.random()*3));
  }
  for(let k=0;k<Math.min(2+Math.floor(level/3),5);k++){
    const c=take(walls);if(c){const d=c.dirs[0];dungeonSkeleton(c.x,c.z,d[0],d[1]);}
  }
  for(let k=0;k<Math.min(2+Math.floor(level/2),6);k++){
    const c=take(locations);if(c)dungeonArch(c.x,c.z,grid[c.gz][c.gx-1]===0&&grid[c.gz][c.gx+1]===0);
  }
  const altar=take(locations);if(altar)dungeonAltar(altar.x,altar.z);
  const style=(level-1)%DUNGEON_THEMES.length;
  if(style===0||style===1){
    for(let k=0;k<4;k++){const c=take(locations);if(c)dungeonRubble(c.x,c.z);}
    if(style===1)for(let k=0;k<3;k++){const c=take(locations);if(c)dungeonSkullPile(c.x,c.z,4);}
  }
  if(style===2||style===4||style===3){
    for(let k=0;k<Math.min(3+Math.floor(level/4),6);k++){
      const c=take(walls);if(c){const d=c.dirs[0];dungeonWallWindow(c.x,c.z,d[0],d[1],style);}
    }
  }
  if(style===2){for(let k=0;k<3;k++){const c=take(locations);if(c)dungeonPuddle(c.x,c.z,1.1);}}
  if(style===3){for(let k=0;k<6;k++){const c=take(locations);if(c)dungeonWater(c.x,c.z,.55+Math.random()*.64);}}
  if(style===5){for(let k=0;k<5;k++){const c=take(locations);if(c)dungeonFissure(c.x,c.z);}}
}

// ---------- gothic architectural kit ----------
// Visible 3D masonry, rib vaults and stained-glass recesses (not just a wall texture).
// The ornaments sit within roughly 0.4m of solid walls or above head height,
// preserving pathfinding and player collision in narrow passages.
const GOTHIC_GEOM={
  column:new THREE.CylinderGeometry(.16,.21,3.85,14),
  capital:new THREE.CylinderGeometry(.32,.21,.29,10),
  foot:new THREE.CylinderGeometry(.31,.29,.24,12),
  ring:new THREE.TorusGeometry(.51,.045,8,32),
  orb:new THREE.IcosahedronGeometry(.19,1),
  slab:new THREE.BoxGeometry(.34,.52,.36),
  keystone:new THREE.OctahedronGeometry(.22,0)
};
const ARCH_BONEMAT=new THREE.MeshStandardMaterial({color:0xb8a88f,metalness:.1,roughness:.74});
const ARCH_IRON=new THREE.MeshStandardMaterial({color:0x252b2d,metalness:.76,roughness:.48});
function catPart(parent,geo,material,x,y,z,sx=1,sy=1,sz=1){
  const m=new THREE.Mesh(geo,material);m.position.set(x,y,z);m.scale.set(sx,sy,sz);parent.add(m);return m;
}
function catCurve(parent,pts,r,mat){
  const curve=new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p)));
  const mesh=new THREE.Mesh(new THREE.TubeGeometry(curve,28,r,8,false),mat);
  parent.add(mesh);return mesh;
}
function catLocalRoot(x,z,dx,dz){
  const g=new THREE.Group();g.position.set(x+dx*(CELL/2-.22),0,z+dz*(CELL/2-.22));
  g.rotation.y=Math.atan2(-dx,-dz);levelGroup.add(g);return g;
}
function cathedralWallBay(x,z,dx,dz,variant=0){
  const root=catLocalRoot(x,z,dx,dz);
  const stone=new THREE.MeshStandardMaterial({color:0xd3cdc3,map:currentTheme.wallMap,
    bumpMap:currentTheme.wallMap,bumpScale:.24,roughness:.93,metalness:.015});
  const shadow=new THREE.MeshBasicMaterial({color:0x090c12,side:THREE.DoubleSide});
  const gild=new THREE.MeshStandardMaterial({color:currentTheme.trim,metalness:.33,roughness:.57});
  // Deep recessed pointed window shape painted into the wall face.
  const lancet=new THREE.Shape();lancet.moveTo(-.67,1.18);lancet.lineTo(-.67,4.36);
  lancet.quadraticCurveTo(-.6,5.20,0,5.68);
  lancet.quadraticCurveTo(.6,5.20,.67,4.36);
  lancet.lineTo(.67,1.18);lancet.closePath();
  const inset=new THREE.Mesh(new THREE.ShapeGeometry(lancet,16),shadow);inset.position.z=.105;root.add(inset);
  const glassColor=[0x5a7f89,0xc5a772,0xa7243e,0x337782,0x7154ae,0xb84e2f][(level-1)%6];
  const glass=new THREE.MeshStandardMaterial({color:glassColor,emissive:glassColor,
    emissiveIntensity:variant===1?.55:.26,transparent:true,opacity:.84,
    side:THREE.DoubleSide,roughness:.32,metalness:.22});
  const face=new THREE.Mesh(new THREE.ShapeGeometry(lancet,16),glass);face.position.z=.126;root.add(face);
  // Every bay has clustered columns and pointed arch ribs with sculpted capitals.
  for(const sign of [-1,1]){
    catPart(root,GOTHIC_GEOM.column,stone,sign*.88,3.1,.14,1,1.33,1);
    catPart(root,GOTHIC_GEOM.foot,stone,sign*.88,.21,.14);
    catPart(root,GOTHIC_GEOM.capital,gild,sign*.88,5.73,.14);
    catPart(root,GOTHIC_GEOM.slab,stone,sign*1.10,3.55,.17,.74,4.1,.85);
    catCurve(root,[[sign*.80,5.65,.18],[sign*.58,6.06,.18],[sign*.25,6.42,.18],[0,6.58,.18]],.085,stone);
    catCurve(root,[[sign*.67,4.35,.18],[sign*.56,5.00,.18],[sign*.27,5.45,.18],[0,5.66,.18]],.037,gild);
    for(let k=0;k<4;k++){
      const y=1.60+k*.88;
      catPart(root,new THREE.BoxGeometry(.065,.58,.095),gild,sign*.87,y,.37);
    }
  }
  // Metallic window mullions divide the stained glass into lancet panels.
  catCurve(root,[[0,1.25,.165],[0,2.45,.165],[0,3.75,.165],[0,5.62,.165]],.035,ARCH_IRON);
  for(let k=0;k<3;k++){
    const y=1.8+k*.94;
    catCurve(root,[[-.64,y,.165],[-.20,y+.09,.165],[.20,y+.09,.165],[.64,y,.165]],.028,ARCH_IRON);
  }
  const rose=new THREE.Mesh(GOTHIC_GEOM.ring,gild);rose.position.set(0,4.65,.19);root.add(rose);
  for(let k=0;k<8;k++){
    const a=k*Math.PI/4;
    catCurve(root,[[0,4.65,.2],[Math.cos(a)*.39,4.65+Math.sin(a)*.39,.2]],.022,gild);
  }
  const rosette=catPart(root,GOTHIC_GEOM.orb,glass,0,4.65,.23,.90,.90,.44);rosette.rotation.z=.3;
  const key=catPart(root,GOTHIC_GEOM.keystone,stone,0,6.55,.23);key.rotation.z=Math.PI/4;
  // A faint localized color wash makes stained glass readable in darker floors.
  if(variant===1){const l=new THREE.PointLight(glassColor,.43,7,2);l.position.set(0,3.4,.75);root.add(l);}
  return root;
}
function cathedralVault(x,z){
  const g=new THREE.Group();g.position.set(x,0,z);levelGroup.add(g);
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.wallMap,
    bumpMap:currentTheme.wallMap,bumpScale:.18,color:0xc9c4b9,roughness:.88});
  const apex=[0,WALLH-.22,0];
  const corners=[[-1.56,-1.56],[-1.56,1.56],[1.56,-1.56],[1.56,1.56]];
  for(const [cx,cz] of corners){
    catCurve(g,[[cx,4.88,cz],[cx*.85,5.43,cz*.85],[cx*.55,6.12,cz*.55],apex],.092,stone);
  }
  for(let k=0;k<4;k++){
    const a=k*Math.PI*.5;
    catCurve(g,[[Math.cos(a)*1.68,5.02,Math.sin(a)*1.68],
      [Math.cos(a)*.8,6.13,Math.sin(a)*.8],apex],.07,stone);
  }
  catPart(g,GOTHIC_GEOM.keystone,stone,0,WALLH-.19,0,1.25,.6,1.25);
}
function cathedralChandelier(x,z){
  const g=new THREE.Group();g.position.set(x,0,z);levelGroup.add(g);
  const iron=ARCH_IRON;
  const stem=new THREE.Mesh(new THREE.CylinderGeometry(.025,.035,2.20,12),iron);
  stem.position.y=5.45;g.add(stem);
  for(let i=0;i<6;i++){
    const a=i*Math.PI/3,x0=Math.cos(a),z0=Math.sin(a);
    catCurve(g,[[0,4.32,0],[x0*.40,4.15,z0*.40],[x0*.9,4.30,z0*.9]],.025,iron);
    catPart(g,new THREE.CylinderGeometry(.12,.16,.12,12),iron,x0*.91,4.31,z0*.91);
    catPart(g,new THREE.CylinderGeometry(.035,.04,.21,8),ARCH_BONEMAT,x0*.91,4.48,z0*.91);
    const flame=catPart(g,new THREE.ConeGeometry(.056,.20,9),new THREE.MeshBasicMaterial({color:0xffa75a}),
      x0*.91,4.66,z0*.91);flame.rotation.z=Math.sin(i)*.09;
  }
  catPart(g,new THREE.TorusGeometry(.62,.055,9,30),iron,0,4.18,0).rotation.x=Math.PI/2;
  const light=new THREE.PointLight(currentTheme.torch,1.25,10,1.8);light.position.y=4.50;g.add(light);
  const crown=catPart(g,GOTHIC_GEOM.keystone,iron,0,4.12,0);
  return g;
}
function cathedralTomb(x,z,style){
  const root=new THREE.Group();root.position.set(x,0,z);levelGroup.add(root);
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.floorMap,color:0xd7cebd,
    bumpMap:currentTheme.floorMap,bumpScale:.09,roughness:.92});
  catPart(root,new THREE.BoxGeometry(1.55,.55,.93),stone,0,.29,0);
  catPart(root,new THREE.BoxGeometry(1.72,.16,1.10),stone,0,.66,0);
  const lid=catPart(root,new THREE.BoxGeometry(1.48,.16,.85),stone,0,.79,0);
  lid.rotation.z=style===1?.13:0;
  dungeonSkull(root,0,1.08,0,.55);
  for(const side of [-1,1]){
    catPart(root,GOTHIC_GEOM.keystone,ARCH_IRON,side*.57,.72,.36,.45,.48,.45);
  }
}
function cathedralGargoyle(x,z,dx,dz){
  const g=catLocalRoot(x,z,dx,dz);const mat=new THREE.MeshStandardMaterial({
    color:0x777078,map:currentTheme.wallMap,bumpMap:currentTheme.wallMap,
    bumpScale:.18,roughness:.86});
  catPart(g,new THREE.BoxGeometry(.78,.19,.43),mat,0,3.70,.4);
  catPart(g,new THREE.SphereGeometry(.32,14,11),mat,0,4.10,.41,1,.74,1.30);
  catPart(g,new THREE.SphereGeometry(.18,12,9),mat,0,4.34,.65,1,.9,1.2);
  for(const sign of [-1,1]){
    const horn=catPart(g,new THREE.ConeGeometry(.09,.38,10),mat,sign*.17,4.62,.55);
    horn.rotation.z=sign*.23;
    catCurve(g,[[sign*.25,4.02,.49],[sign*.44,3.93,.64],[sign*.56,3.73,.78]],.065,mat);
    catPart(g,GOTHIC_GEOM.orb,ARCH_IRON,sign*.09,4.37,.79,.32,.29,.42);
  }
}
function decorateCathedral(m,n){
  const walls=[],cells=[];
  for(let y=2;y<n-2;y++)for(let x=2;x<n-2;x++){
    if(grid[y][x]!==0||m.dist[y][x]<5)continue;
    const px=(x+.5)*CELL,pz=(y+.5)*CELL;
    const wallDirs=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dx,dz])=>grid[y+dz][x+dx]===1);
    cells.push([px,pz]);
    if(wallDirs.length)walls.push({x:px,z:pz,dir:wallDirs[Math.floor(Math.random()*wallDirs.length)]});
  }
  const take=a=>a.length?a.splice(Math.floor(Math.random()*a.length),1)[0]:null;
  const windowCount=Math.min(7,Math.max(3,Math.floor(n/4)));
  for(let i=0;i<windowCount;i++){
    const c=take(walls);if(c)cathedralWallBay(c.x,c.z,c.dir[0],c.dir[1],i<2?1:0);
  }
  for(let i=0;i<Math.min(9,Math.floor(n/2));i++){
    const c=take(cells);if(c)cathedralVault(c[0],c[1]);
  }
  for(let i=0;i<Math.min(3,1+Math.floor(level/4));i++){
    const c=take(cells);if(c)cathedralChandelier(c[0],c[1]);
  }
  for(let i=0;i<Math.min(3,1+Math.floor(level/5));i++){
    const c=take(walls);if(c)cathedralGargoyle(c.x,c.z,c.dir[0],c.dir[1]);
  }
  if(level%6===2||level%6===5||level%6===0){
    for(let i=0;i<2;i++){const c=take(cells);if(c)cathedralTomb(c[0],c[1],i);}
  }
}

// Repeated carved Gothic wall bays. All pieces are instanced: richer geometry
// without multiplying the draw calls on large, procedurally generated floors.
const FACADE_GEOMETRY={
  square:new THREE.BoxGeometry(1,1,1),
  pillar:new THREE.CylinderGeometry(.14,.17,1,10),
  arch:(()=>{const pts=[[-1.12,1.50],[-1.12,3.45],[-1.02,4.22],[-.70,4.94],[0,5.48],[.70,4.94],[1.02,4.22],[1.12,3.45],[1.12,1.50]];
    return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(p[0],p[1],.16))),32,.095,7,false);})(),
  recess:(()=>{const p=new THREE.Shape();p.moveTo(-1.02,1.46);p.lineTo(-1.02,3.45);
    p.quadraticCurveTo(-.92,4.53,0,5.26);p.quadraticCurveTo(.92,4.53,1.02,3.45);
    p.lineTo(1.02,1.46);p.closePath();return new THREE.ShapeGeometry(p,12);})(),
  relief:new THREE.TorusGeometry(.30,.045,7,20)
};
function buildGothicWallFacades(){
  const bays=[];
  for(let y=1;y<GH-1;y++)for(let x=1;x<GW-1;x++){
    if(grid[y][x]!==1||secretWalls.some(w=>w.gx===x&&w.gz===y))continue;
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
      if(grid[y+dz][x+dx]!==0)continue;
      if(((x*19+y*31+dx*7+dz*11+level*13)>>>0)%5===0)continue;
      const wx=(x+.5)*CELL+dx*CELL*.5,wz=(y+.5)*CELL+dz*CELL*.5;
      bays.push({x:wx,z:wz,yaw:Math.atan2(dx,dz)});
    }
  }
  if(!bays.length)return;
  const stone=new THREE.MeshStandardMaterial({map:currentTheme.wallMap,color:0xc2bdb4,roughness:.89,bumpMap:currentTheme.wallMap,bumpScale:.17});
  const mold=new THREE.MeshStandardMaterial({color:currentTheme.trim,roughness:.81,metalness:.05});
  const shadow=new THREE.MeshStandardMaterial({color:0x191718,roughness:1,side:THREE.DoubleSide});
  const parts=[
    {geo:FACADE_GEOMETRY.square,mat:stone,places:[[-1.68,3.05,.13,.25,5.95,.32],[1.68,3.05,.13,.25,5.95,.32]]},
    {geo:FACADE_GEOMETRY.pillar,mat:mold,places:[[-1.49,2.87,.25,1,5.4,1],[1.49,2.87,.25,1,5.4,1]]},
    {geo:FACADE_GEOMETRY.square,mat:stone,places:[[0,.33,.12,3.67,.32,.30],[0,5.96,.13,3.65,.21,.29]]},
    {geo:FACADE_GEOMETRY.recess,mat:shadow,places:[[0,0,.10,1,1,1]]},
    {geo:FACADE_GEOMETRY.arch,mat:mold,places:[[0,0,.19,1,1,1]]},
    {geo:FACADE_GEOMETRY.relief,mat:mold,places:[[0,3.20,.23,1,1,1]]}
  ];
  const matrix=new THREE.Matrix4();
  for(const part of parts){
    const inst=new THREE.InstancedMesh(part.geo,part.mat,bays.length*part.places.length);
    let idx=0;
    for(const bay of bays){const c=Math.cos(bay.yaw),sn=Math.sin(bay.yaw);
      for(const [lx,ly,lz,sx,sy,sz] of part.places){
        const wx=bay.x+lx*c+lz*sn,wz=bay.z-lx*sn+lz*c;
        // 4x4 affine matrix: local +Z is the outward face of the wall.
        matrix.set(c*sx,0,sn*sz,wx,0,sy,0,ly,-sn*sx,0,c*sz,wz,0,0,0,1);
        inst.setMatrixAt(idx++,matrix);
      }
    }
    inst.instanceMatrix.needsUpdate=true;inst.frustumCulled=false;inst.userData.cathedralFacade=true;levelGroup.add(inst);
  }
}


// ---------- ABYSSAL V5: safe procedural room landmarks, hazards and objectives ----------
function roomLandmark(x,z,kind){
  const g=new THREE.Group();g.position.set(x,0,z);levelGroup.add(g);
  const stone=new THREE.MeshStandardMaterial({color:currentTheme.trim,roughness:.91,bumpMap:currentTheme.wallMap,bumpScale:.10});
  const wood=new THREE.MeshStandardMaterial({color:0x433020,roughness:.91});
  if(kind==='library'){
    // Short bookcases sit near the perimeter, preserving a 2 m walking lane.
    for(const side of [-1,1]){
      const shelf=new THREE.Mesh(new THREE.BoxGeometry(.48,1.9,2.2),wood);
      shelf.position.set(side*1.25,.95,0);g.add(shelf);
      for(let j=0;j<4;j++){
        const lip=new THREE.Mesh(new THREE.BoxGeometry(.56,.06,2.2),stone);lip.position.set(side*1.25,.4+j*.42,0);g.add(lip);
        for(let k=0;k<8;k++){
          const book=new THREE.Mesh(new THREE.BoxGeometry(.21,.26,.10),new THREE.MeshStandardMaterial({color:[0x5d3437,0x48614d,0x544466][(j+k)%3],roughness:.9}));
          book.position.set(side*1.18,.50+j*.42,(k-3.5)*.25);g.add(book);
        }
      }
    }
  }else if(kind==='ritual'){
    const altar=new THREE.Mesh(new THREE.CylinderGeometry(.85,.96,.30,8),stone);altar.position.y=.18;g.add(altar);
    const sigil=new THREE.Mesh(new THREE.RingGeometry(.40,.47,24),new THREE.MeshBasicMaterial({color:currentTheme.torch,side:THREE.DoubleSide,transparent:true,opacity:.74}));
    sigil.rotation.x=-Math.PI/2;sigil.position.y=.335;g.add(sigil);
    for(let k=0;k<5;k++){const a=k/5*Math.PI*2,sk=dungeonSkull(g,Math.cos(a)*.61,.44,Math.sin(a)*.61,.4);sk.rotation.y=a;}
  }else if(kind==='armory'){
    for(const side of [-1,1]){
      const rack=new THREE.Mesh(new THREE.BoxGeometry(.25,1.5,1.7),wood);rack.position.set(side*1.25,.75,0);g.add(rack);
      for(let j=0;j<4;j++){const bar=new THREE.Mesh(new THREE.CylinderGeometry(.023,.03,1.4,8),ancientIron);
        bar.position.set(side*1.25,.72,(j-1.5)*.36);bar.rotation.x=Math.PI/2;g.add(bar);}
    }
  }else if(kind==='chapel'){
    for(const side of [-1,1]){
      const seat=new THREE.Mesh(new THREE.BoxGeometry(.43,.40,1.55),wood);seat.position.set(side*1.32,.3,0);g.add(seat);
      const back=new THREE.Mesh(new THREE.BoxGeometry(.12,.75,1.55),wood);back.position.set(side*1.48,.66,0);g.add(back);
    }
    dungeonSkull(g,0,.62,0,.9);
  }else{
    const plinth=new THREE.Mesh(new THREE.BoxGeometry(.88,.6,.88),stone);plinth.position.y=.30;g.add(plinth);
    const statue=new THREE.Mesh(new THREE.DodecahedronGeometry(.39,1),ancientBone);statue.position.y=1.06;g.add(statue);
    for(const side of [-1,1]){
      const horn=new THREE.Mesh(new THREE.ConeGeometry(.08,.48,9),ancientBone);horn.position.set(side*.22,1.43,0);horn.rotation.z=side*.38;g.add(horn);
    }
  }
}
function createHazard(kind,x,z,r=.82){
  const colors={lava:0xc9401c,poison:0x5da94c,spikes:0x777f84,fire:0xe65c1c};
  const mesh=new THREE.Mesh(new THREE.CircleGeometry(r,28),new THREE.MeshBasicMaterial({color:colors[kind],transparent:true,opacity:kind==='spikes'?.62:.72,depthWrite:false,side:THREE.DoubleSide}));
  mesh.rotation.x=-Math.PI/2;mesh.position.set(x,.035,z);levelGroup.add(mesh);
  const obj={kind,x,z,r,mesh,t:Math.random()*5,damageClock:0,ttl:kind==='fire'?2.8:Infinity};hazards.push(obj);
  if(kind==='spikes')for(let j=0;j<7;j++){
    const a=j/7*Math.PI*2,spike=new THREE.Mesh(new THREE.ConeGeometry(.09,.36,7),ancientIron);
    spike.position.set(x+Math.cos(a)*r*.63,.19,z+Math.sin(a)*r*.63);levelGroup.add(spike);
    obj.spikes=obj.spikes||[];obj.spikes.push(spike);
  }
}
function updateHazards(dt){
  for(const h of hazards.slice()){
    h.t+=dt;h.ttl-=dt;
    if(h.ttl<=0){levelGroup.remove(h.mesh);hazards.splice(hazards.indexOf(h),1);if(h.mesh.geometry?.dispose)h.mesh.geometry.dispose();if(h.mesh.material?.dispose)h.mesh.material.dispose();continue;}
    h.damageClock=Math.max(0,h.damageClock-dt);
    h.mesh.material.opacity=.52+.15*Math.sin(h.t*2.4);
    if(Math.hypot(P.x-h.x,P.z-h.z)<h.r+.12&&h.damageClock<=0){
      h.damageClock=.75;hurt(h.kind==='lava'?9:h.kind==='poison'?5:h.kind==='fire'?3:7);
      if(h.kind==='lava')vfx('fire',P.x,.2,P.z,.75,.4,.1,1,.1,.6);
      if(h.kind==='poison')toast('TOXIN EXPOSURE',650);
    }
    if(h.kind==='fire')for(const e of enemies){
      if(Math.hypot(e.x-h.x,e.z-h.z)<h.r+e.r){e.burn=Math.max(e.burn||0,.55);}
    }
  }
}
// An explicit entry state prevents repeated floor increments during the transition.
let portalTransitToken=0;
const portalPrompt=document.createElement('div');
portalPrompt.style.cssText='position:absolute;left:50%;top:53%;transform:translate(-50%,-50%);z-index:7;color:#edecff;background:#0a0c17cc;border:1px solid #ae91f155;padding:8px 13px;border-radius:8px;font:bold 12px Segoe UI,sans-serif;text-align:center;pointer-events:none;display:none;white-space:nowrap';
wrap.appendChild(portalPrompt);
const portalTransit=document.createElement('div');
portalTransit.style.cssText='position:absolute;inset:0;z-index:15;pointer-events:none;display:none;align-items:center;justify-content:center;flex-direction:column;background:radial-gradient(circle,#a3e8ff 0%,#211d35 50%,#02040a 100%);color:#fff;transition:opacity .65s;font-weight:900;letter-spacing:3px;text-shadow:0 3px 24px #000;text-align:center';
wrap.appendChild(portalTransit);
function beginPortalDescent(){
 if(state!=='playing')return;
 const token=++portalTransitToken;
 state='portalEntering';
 const nextName=DUNGEON_THEMES[level%DUNGEON_THEMES.length].name;
 portalTransit.innerHTML='<div style="font-size:14px;opacity:.8">DESCENDING INTO</div><div style="font-size:24px;margin-top:15px">'+nextName.toUpperCase()+'</div>';
 portalTransit.style.display='flex';portalTransit.style.opacity='0';
 requestAnimationFrame(()=>{if(token===portalTransitToken)portalTransit.style.opacity='1';});
 camera.fov=Math.min(104,SET.fov+22);camera.updateProjectionMatrix();
 P.shake=.33;beep(120,.65,'sawtooth',.13,620);noise(.4,1500,250,.2,'lowpass');
 setTimeout(()=>{
  if(token!==portalTransitToken||state!=='portalEntering')return;
  camera.fov=SET.fov;camera.updateProjectionMatrix();
  if(level>=20&&mode!=='Survival'&&mode!=='New Game+'){
   state='victory';STATS.floors++;recordRun();saveBest();saveCampaign();showMenu('victory');
  }else{
   level++;P.score+=200+level*20;saveBest();P.hp=Math.min(P.maxhp,P.hp+25);P.ammo+=15;
   buildLevel();saveCampaign();toast('Level '+level+' — the dungeon grows...',2400);
   STATS.floors++;if(level>=5)award('f5');recordRun();
   perkChoices=PERKS.slice().sort(()=>Math.random()-.5).slice(0,3);
   forgeStage=0;forgeChosen=false;state='perk';showMenu('perk');
  }
  portalTransit.style.opacity='0';setTimeout(()=>{if(token===portalTransitToken)portalTransit.style.display='none';},660);
 },1200);
}
function unlockPortalIfReady(){
  const enough=killsThisLevel>=Math.ceil(totalEnemies*.5);
  if(portalOpen||!enough||(floorKeyNeeded&&!floorKeyCollected)||(floorSwitchNeeded&&!floorSwitchOn)||(currentBoss&&currentBoss.hp>0))return;
  portalOpen=true;
  portal.userData.phase=0;P.shake=Math.max(P.shake,.22);
  toast('THE PORTAL IS OPEN · FIND THE EXIT',2350);beep(540,.4,'sine',.07,270);
}


// Release level-specific GPU resources before generating another floor.
// Theme atlases, shared hand/monster materials and reused primitives remain cached.
function releaseDungeon(group){
 if(!group)return;
 const seen=new Set(),geos=new Set(),mats=new Set();
 const preserveMats=new Set([wallMat,floorMat,ceilMat,ancientBone,ancientDark,ancientIron,ancientBlood,bloodBorder,...CREATURE_MATERIAL_CACHE.values()]);
 const reusableTex=new Set([...DUNGEON_THEMES.map(t=>t.wallMap),...DUNGEON_THEMES.map(t=>t.floorMap),...DUNGEON_THEMES.map(t=>t.roughnessMap),...DUNGEON_THEMES.filter(t=>t.lavaMap).map(t=>t.lavaMap),skinTex,CREATURE_ALBEDO,VFX_TEXTURES.fire,VFX_TEXTURES.smoke,VFX_TEXTURES.glow,glowTex]);
 const walk=o=>{
  if(!o||seen.has(o))return;seen.add(o);
  if(o.geometry&&o.geometry!==wallGeo)geos.add(o.geometry);
  if(o.material){const list=Array.isArray(o.material)?o.material:[o.material];for(const m of list)if(m&&!preserveMats.has(m))mats.add(m);}
  if(o.children)for(const c of o.children)walk(c);
 };
 walk(group);
 for(const m of mats){if(m.map&&!reusableTex.has(m.map)&&m.map.dispose)m.map.dispose();if(m.dispose)m.dispose();}
 for(const geo of geos)if(!ORGAN_GEOMETRY.includes(geo)&&geo.dispose)geo.dispose();
}


// ---------- ABYSSAL V5: breakable walls, runic mechanisms and hidden treasure ----------
function createSecretWall(gx,gz){
 const x=(gx+.5)*CELL,z=(gz+.5)*CELL;
 const mat=new THREE.MeshStandardMaterial({color:currentTheme.trim,roughness:.94,bumpMap:currentTheme.wallMap,bumpScale:.16});
 const mesh=new THREE.Mesh(new THREE.BoxGeometry(CELL-.05,WALLH,CELL-.05),mat);
 mesh.position.set(x,WALLH/2,z);levelGroup.add(mesh);
 const glyph=new THREE.Mesh(new THREE.OctahedronGeometry(.23,0),new THREE.MeshBasicMaterial({color:currentTheme.torch}));
 glyph.position.set(0,.35,CELL/2+.045);mesh.add(glyph);
 secretWalls.push({gx,gz,x,z,mesh,hp:6});
}
function damageSecretWall(x,z,amount){
 const cx=Math.floor(x/CELL),cz=Math.floor(z/CELL);
 const wall=secretWalls.find(w=>w.gx===cx&&w.gz===cz);if(!wall)return false;
 wall.hp-=amount;
 if(wall.hp>0){burst(wall.x,.75,wall.z,0xa89b7f,5,2);return true;}
 levelGroup.remove(wall.mesh);secretWalls.splice(secretWalls.indexOf(wall),1);
 grid[wall.gz][wall.gx]=0;resetMonsterNavigation();
 burst(wall.x,1.1,wall.z,0xb4a28d,20,4);noise(.4,980,90,.25,'lowpass');
 addPickup('gem',wall.x,wall.z);P.coins+=35;
 toast('SECRET PASSAGE REVEALED · +35 SOUL COINS',1800);return true;
}
function createRunicSwitch(x,z){
 const group=new THREE.Group();group.position.set(x,0,z);levelGroup.add(group);
 const stone=new THREE.Mesh(new THREE.CylinderGeometry(.31,.4,1.05,9),new THREE.MeshStandardMaterial({color:currentTheme.trim,roughness:.88}));
 stone.position.y=.55;group.add(stone);
 const rune=new THREE.Mesh(new THREE.OctahedronGeometry(.19,1),new THREE.MeshStandardMaterial({color:0x5ec5dc,emissive:0x1d96b2,emissiveIntensity:1.5}));
 rune.position.y=1.27;group.add(rune);runicSwitches.push({x,z,group,rune,on:false});
}
function interactRune(){
 if(state!=='playing'||paused)return;
 const r=runicSwitches.find(o=>!o.on&&Math.hypot(P.x-o.x,P.z-o.z)<1.65);
 if(!r){toast('NO MECHANISM IN REACH',600);return;}
 r.on=true;r.rune.material.color.set(0x91ffac);r.rune.material.emissive.set(0x48d07c);
 floorSwitchOn=true;P.coins+=25;beep(670,.3,'sine',.06,300);
  toast('RUNES ACTIVATED · +25 COINS',1200);unlockPortalIfReady();saveCampaign();
}


// Environment-specific enemy distribution, with early-floor safety constraints.
// Internal IDs are preserved for migration, damage rules and boss waves.
// Public-facing names are the six original horror creature designs.
const CREATURE_NAMES=Object.freeze({
 chaser:'FLESH IMP',brute:'FLESH BRUTE',crawler:'CRYPT CRAWLER',
 stalker:'DUSK STALKER',teleporter:'GAUNT HOODED WRAITH',necromancer:'NECROMANCER',
 winged:'WINGED GARGOYLE',armored:'CHAINED FLESH BRUTE'
});
const ENEMY_POOLS=[
 [['imp',5],['shooter',2],['stalker',2],['brute',1]],
 [['crawler',4],['splitter',2],['stalker',2],['necromancer',1]],
 [['imp',3],['stalker',3],['brute',2],['gargoyle',2]],
 [['shooter',3],['teleporter',2],['crawler',2],['necromancer',2],['gargoyle',1]],
 [['brute',3],['armored',2],['gargoyle',3],['necromancer',2]],
 [['imp',3],['brute',2],['armored',2],['gargoyle',2]],
 [['necromancer',3],['stalker',3],['crawler',2],['gargoyle',2]],
 [['teleporter',2],['necromancer',3],['crawler',2],['gargoyle',3]],
 [['armored',3],['shooter',2],['brute',2],['gargoyle',3]]
];
function chooseThemeEnemy(){
 const pool=ENEMY_POOLS[(level-1)%ENEMY_POOLS.length];
 const valid=pool.filter(([type])=>level>=({brute:3,armored:5,necromancer:4,stalker:2,crawler:2,teleporter:2,splitter:2,gargoyle:3,imp:1}[type]||1));
 const total=valid.reduce((a,v)=>a+v[1],0);let r=Math.random()*total;
 for(const [type,weight] of valid){r-=weight;if(r<=0)return type;}return 'chaser';
}

// ---------- level building ----------
const shardGeo=new THREE.SphereGeometry(0.07,5,5);
function cellCenter(c){return [(c[0]+0.5)*CELL,(c[1]+0.5)*CELL];}

function buildLevel(){
  reseed((mode==='Daily'?dailySeed():campaignSeed)+level*7919);
  if(levelGroup){scene.remove(levelGroup);releaseDungeon(levelGroup);}
  levelGroup=new THREE.Group(); scene.add(levelGroup);
  enemies=[];fallenMonsters=[]; pickups=[]; orbs=[]; fx=[]; shots=[]; bossTelegraphs=[];currentBoss=null; killsThisLevel=0; portalOpen=false; flames=[]; checkpoints=[]; barrels=[]; decals=[];hazards=[];secretWalls=[];runicSwitches=[];
  resetMonsterNavigation();
  const n=Math.min(27,9+2*level);
  const m=genMaze(n); grid=m.g; GW=GH=n; exitCell=m.far;
  let bossArenaCell=null;
  if(level%(mode==='Survival'?3:5)===0){
    const choices=[];
    for(let y=3;y<n-3;y++)for(let x=3;x<n-3;x++){
      const d=m.dist[y][x];if(grid[y][x]===0&&d>=8&&d<m.dist[exitCell[1]][exitCell[0]]-2)choices.push([x,y]);
    }
    if(choices.length){bossArenaCell=choices[Math.floor(Math.random()*choices.length)];
      const [bx,by]=bossArenaCell;
      for(let yy=by-2;yy<=by+2;yy++)for(let xx=bx-2;xx<=bx+2;xx++)grid[yy][xx]=0;
    }
  }
  floorKeyNeeded=level%3===0;floorKeyCollected=false;P.keys=0;
  floorSwitchNeeded=level%4===0;floorSwitchOn=false;
  activeObjective=floorKeyNeeded?'Recover the crypt key + defeat guardians':floorSwitchNeeded?'Activate the rune switch + defeat guardians':'Defeat guardians + reach the portal';

  currentTheme=DUNGEON_THEMES[(level-1)%DUNGEON_THEMES.length];
  wallMat.map=currentTheme.wallMap;wallMat.bumpMap=currentTheme.wallMap;wallMat.bumpScale=.17;wallMat.roughnessMap=currentTheme.roughnessMap;wallMat.emissiveMap=currentTheme.lavaMap;wallMat.emissive.set(currentTheme.lavaMap?0xff5424:0x000000);wallMat.emissiveIntensity=currentTheme.lavaMap?.68:0;wallMat.color.set(0xc8c9c7);wallMat.needsUpdate=true;
  floorMat.map=currentTheme.floorMap;floorMat.bumpMap=currentTheme.floorMap;floorMat.roughnessMap=currentTheme.roughnessMap;floorMat.bumpScale=.11;floorMat.emissiveMap=currentTheme.lavaMap;floorMat.emissive.set(currentTheme.lavaMap?0x9b2a08:0x000000);floorMat.emissiveIntensity=currentTheme.lavaMap?.20:0;floorMat.color.set(0xc7c7c7);floorMat.needsUpdate=true;
  ceilMat.map=currentTheme.wallMap;ceilMat.bumpMap=currentTheme.wallMap;ceilMat.roughnessMap=currentTheme.roughnessMap;ceilMat.color.set(0x777778);ceilMat.needsUpdate=true;
  scene.fog.color.set(currentTheme.fog);scene.background.set(currentTheme.fog);
  torch.color.set(currentTheme.torch);
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
  const hidden=[];
  for(const [cx,cz] of cells){
    if(m.dist[cz]&&m.dist[cz][cx]>=0)continue;
    const LR=grid[cz]&&grid[cz][cx-1]===0&&grid[cz][cx+1]===0;
    const UD=grid[cz-1]&&grid[cz+1]&&grid[cz-1][cx]===0&&grid[cz+1][cx]===0;
    if((LR||UD)&&Math.abs(cx-1)+Math.abs(cz-1)>5)hidden.push([cx,cz]);
  }
  hidden.sort(()=>Math.random()-.5);const selected=hidden.slice(0,Math.min(2,Math.ceil(level/5)+1));
  const hiddenSet=new Set(selected.map(c=>c[1]*n+c[0]));
  const normalCells=cells.filter(c=>!hiddenSet.has(c[1]*n+c[0]));
  const inst=new THREE.InstancedMesh(wallGeo,wallMat,normalCells.length);
  const mat4=new THREE.Matrix4();
  normalCells.forEach((c,i)=>{ mat4.setPosition((c[0]+0.5)*CELL,WALLH/2,(c[1]+0.5)*CELL); inst.setMatrixAt(i,mat4); });
  inst.instanceMatrix.needsUpdate=true;
  inst.frustumCulled=false; // fixes walls vanishing when the origin block leaves the view
  levelGroup.add(inst);
  selected.forEach(c=>createSecretWall(c[0],c[1]));
  buildGothicWallFacades();

  currentTheme.floorMap.repeat.set(n/3,n/3);currentTheme.wallMap.repeat.set(n/4,n/4);
  const fl=new THREE.Mesh(new THREE.PlaneGeometry(n*CELL,n*CELL),floorMat);
  fl.rotation.x=-Math.PI/2; fl.position.set(n*CELL/2,0,n*CELL/2); levelGroup.add(fl);
  const ce=new THREE.Mesh(new THREE.PlaneGeometry(n*CELL,n*CELL),ceilMat);
  ce.rotation.x=Math.PI/2; ce.position.set(n*CELL/2,WALLH,n*CELL/2); levelGroup.add(ce);

  const sc=cellCenter([1,1]); P.x=sc[0]; P.z=sc[1]; P.yaw=0;
  // face an open direction
  if(grid[1][2]===0) P.yaw=-Math.PI/2; else P.yaw=Math.PI;

  // v5.2 cinematic portal: shader vortex plus carved frame and pooled ornaments.
  const pc=cellCenter(exitCell);
  portal=createAbyssalGateway((level-1)%DUNGEON_THEMES.length,level%5===0);
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
  decorateDungeon(m,n);
  decorateCathedral(m,n);
  const clearCells=[];
  for(let cy=2;cy<n-2;cy++)for(let cx=2;cx<n-2;cx++){
    if(grid[cy][cx]!==0||m.dist[cy][cx]<7||m.dist[cy][cx]>m.dist[exitCell[1]][exitCell[0]]-3)continue;
    if([[1,0],[-1,0],[0,1],[0,-1]].some(v=>grid[cy+v[1]][cx+v[0]]!==0))continue;
    clearCells.push([cx,cy]);
  }
  const rooms=['library','ritual','armory','chapel','statue'];
  for(let j=0;j<Math.min(5,clearCells.length);j++){
    const ix=Math.floor(Math.random()*clearCells.length),c=clearCells.splice(ix,1)[0];
    if(!c)break;const point=cellCenter(c);
    roomLandmark(point[0],point[1],rooms[(j+level)%rooms.length]);
  }

  const normal=Math.min(38,Math.round((4+level*2)*DIFF[difficulty].c*(mode==='Survival'?1.3:mode==='New Game+'?1.25:1)));
  if((level%(mode==='Survival'?3:5)===0)&&(bossArenaCell||far.length)){
    const bc=bossArenaCell||pick(far),bp=cellCenter(bc);
    addEnemy('boss',bp[0],bp[1]);
    // A readable confrontation arena, with signature columns beyond the central combat area.
    for(const [ox,oz] of [[-6,-6],[6,-6],[-6,6],[6,6]]){
      const pillar=new THREE.Mesh(new THREE.CylinderGeometry(.3,.38,4.4,9),new THREE.MeshStandardMaterial({color:currentTheme.trim,roughness:.9}));
      pillar.position.set(bp[0]+ox,2.2,bp[1]+oz);
      if(!solid(bp[0]+ox,bp[1]+oz))levelGroup.add(pillar);
    }
    bossWarningAmbient(bp[0],bp[1]);
  }
  for(let i=0;i<normal&&far.length;i++){
    const c=pick(far),p=cellCenter(c);
    const kind=chooseThemeEnemy();addEnemy(kind,p[0],p[1]);
    if(kind==='imp'&&level>=3&&Math.random()<.19&&enemies.length<36){
      for(let j=0;j<3;j++){const xx=p[0]+Math.cos(j*2.09)*.84,zz=p[1]+Math.sin(j*2.09)*.84;
        if(!blocked(xx,zz,.3))addEnemy('imp',xx,zz);}
    }
  }
  totalEnemies=enemies.length;
  if(level%5===0) setTimeout(()=>toast('Warning BOSS FLOOR — something huge is hunting you',3200),400);
  const nh=3+Math.floor(level/2), na=4+level, ng=5+level;
  for(let i=0;i<nh&&all.length;i++){const p=cellCenter(pick(all)); addPickup('hp',p[0],p[1]);}
  for(let i=0;i<na&&all.length;i++){const p=cellCenter(pick(all)); addPickup('ammo',p[0],p[1]);}
  for(let i=0;i<ng&&all.length;i++){const p=cellCenter(pick(all)); addPickup('gem',p[0],p[1]);}
  for(let i=0;i<2+Math.floor(level/2)&&all.length;i++){const p=cellCenter(pick(all)); addBarrel(p[0],p[1]);}
  if(floorKeyNeeded&&(far.length||all.length)){
    const p=cellCenter(pick(far.length?far:all));addPickup('key',p[0],p[1]);
  }
  if(floorSwitchNeeded&&(far.length||all.length)){
    const p=cellCenter(pick(far.length?far:all));createRunicSwitch(p[0],p[1]);
  }
  const kinds=['poison','spikes','lava'];
  for(let i=0;i<Math.min(3+Math.floor(level/3),7)&&all.length;i++){
    const c=pick(all);if(!c)break;const p=cellCenter(c);
    const kind=kinds[(i+Math.floor(level/2))%3];createHazard(kind,p[0],p[1],.62+Math.random()*.24);
  }
  Math.random=RND;
}

const skinTex=(function(){
 const cv=document.createElement('canvas');cv.width=cv.height=256;const ctx=cv.getContext('2d');
 ctx.fillStyle='#808080';ctx.fillRect(0,0,256,256);
 for(let i=0;i<9500;i++){const k=Math.floor(75+Math.random()*105);
 ctx.fillStyle='rgba('+k+','+k+','+k+','+(0.13+Math.random()*.4)+')';
 const x=Math.random()*256,y=Math.random()*256,r=.35+Math.random()*3;
 ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();}
 const t=new THREE.CanvasTexture(cv);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t;
})();
// Irregular smooth sculpted base shapes reused by all enemies to control GPU memory.
const ORGAN_GEOMETRY=Array.from({length:8},(_,seed)=>{
 const g=new THREE.SphereGeometry(1,20,14),p=g.attributes.position;
 for(let i=0;i<p.count;i++){
   const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
   const n=1+.018*Math.sin(x*13+seed)*Math.cos(y*11-seed)+.013*Math.sin(z*19+x*8);
   p.setXYZ(i,x*n,y*n,z*n);
 }
 g.computeVertexNormals();return g;
});
// Procedural shared flesh relief: high-frequency pores and low-frequency scars.
// All detail assets are generated locally, without image files or network requests.
const CREATURE_ALBEDO=(function(){
 const c=document.createElement('canvas');c.width=c.height=256;
 const x=c.getContext('2d');x.fillStyle='#eee9e4';x.fillRect(0,0,256,256);
 let seed=78013;const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;};
 for(let i=0;i<7000;i++){
   const v=100+Math.floor(rand()*130),a=.014+rand()*.14;
   x.fillStyle='rgba('+v+','+Math.max(0,v-10)+','+Math.max(0,v-17)+','+a+')';
   x.beginPath();x.ellipse(rand()*256,rand()*256,.3+rand()*4,.3+rand()*2,rand()*6.28,0,6.29);x.fill();
 }
 for(let i=0;i<26;i++){
   let px=rand()*256,py=rand()*256;
   x.strokeStyle='rgba(77,24,28,'+(.08+rand()*.17)+')';x.lineWidth=.5+rand()*1.6;
   x.beginPath();x.moveTo(px,py);
   x.bezierCurveTo(px+rand()*40-20,py+rand()*40-20,px+rand()*60-30,py+rand()*60-30,px+rand()*90-45,py+rand()*90-45);
   x.stroke();
 }
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;return t;
})();
const CREATURE_MATERIAL_CACHE=new Map();
function creatureMaterial(hex,roughness=.82,metalness=.015){
 const key=hex+'|'+roughness+'|'+metalness;
 if(!CREATURE_MATERIAL_CACHE.has(key)) CREATURE_MATERIAL_CACHE.set(key,new THREE.MeshStandardMaterial({
   color:hex,roughness,metalness,map:CREATURE_ALBEDO,bumpMap:skinTex,bumpScale:.058,
   roughnessMap:skinTex
 }));
 return CREATURE_MATERIAL_CACHE.get(key);
}

// PROCEDURAL_SCULPT_V2 — distinctive watertight organic torso sculptures.
// All vertices, albedo, bump and roughness textures are generated in JavaScript.
// No downloadable creature assets are required; one indexed-independent geometry
// per species is cached and shared between every enemy of that species.
const SCULPTED_CREATURES=new Set(['chaser','brute','crawler','stalker','necromancer','winged']);
const SCULPT_BODY_CACHE=new Map(), SCULPT_SKIN_CACHE=new Map();
const SCULPT_PLANS={
  brute:{blob:[
    [0,-.18,-.03,.86,.81,.59],[0,-.36,.35,.76,.57,.48],
    [-.58,.47,-.01,.42,.45,.41],[.60,.46,.01,.44,.43,.40],
    [0,.52,.01,.55,.43,.43],[0,.92,.28,.40,.40,.36],
    [0,.91,.51,.32,.24,.23]],smooth:.25,grain:.030,fold:.022},
  crawler:{blob:[
    [0,-.22,-.10,.43,.28,.70],[0,-.13,.31,.35,.27,.38],
    [0,-.065,.61,.28,.28,.28],[0,-.21,-.48,.27,.20,.32]],smooth:.17,grain:.020,fold:.014},
  chaser:{blob:[
    [0,-.38,-.12,.47,.39,.49],[0,-.12,.11,.37,.31,.41],
    [0,.15,.34,.49,.44,.43],[0,.06,.55,.28,.24,.23]],smooth:.20,grain:.025,fold:.028},
  stalker:{blob:[
    [0,-.22,-.10,.22,.56,.22],[0,.35,-.06,.30,.28,.24],
    [0,.66,.09,.18,.30,.19],[0,-.56,-.08,.15,.18,.15],
    [-.23,.35,-.05,.14,.14,.15],[.22,.34,-.05,.14,.14,.15]],smooth:.11,grain:.014,fold:.012},
  necromancer:{blob:[
    [0,-.15,-.04,.31,.69,.31],[0,.43,-.03,.33,.28,.30],
    [0,.69,.04,.33,.38,.33],[0,.62,.30,.23,.25,.15]],smooth:.18,grain:.018,fold:.010},
  winged:{blob:[
    [0,-.15,-.03,.39,.53,.35],[0,.36,.09,.39,.36,.34],
    [0,.69,.25,.29,.29,.31],[-.34,.35,0,.25,.29,.28],
    [.34,.35,0,.25,.29,.28]],smooth:.17,grain:.024,fold:.012}
};
function sculptField(plan,x,y,z){
  // Rounded ellipsoid SDF union, then deterministic wrinkles/noise.
  let d=99;
  for(let i=0;i<plan.blob.length;i++){
    const b=plan.blob[i];
    const px=(x-b[0])/b[3],py=(y-b[1])/b[4],pz=(z-b[2])/b[5];
    const v=(Math.hypot(px,py,pz)-1)*Math.min(b[3],b[4],b[5]);
    if(i===0)d=v;else{
      const k=plan.smooth;
      const h=Math.max(k-Math.abs(d-v),0)/k;
      d=Math.min(d,v)-h*h*k*.25;
    }
  }
  const micro=Math.sin(x*21.9+z*15.7)*Math.sin(y*16.1-x*12.8)*.36+
    Math.sin(x*8.1+y*13.8+z*10.7)*.44+Math.sin(z*24.7-y*18.9)*.20;
  // Curved skin creases cluster around the abdomen, not like repetitive stripes.
  const wrinkles=(Math.sin(y*22+Math.sin(x*7+z*6)*2.3)*Math.sin(x*9.1+z*4.2))*.5;
  return d+(plan.grain*micro+plan.fold*wrinkles)*Math.min(1,.35+Math.abs(y)*.4);
}
function sculptBodyGeometry(type){
  if(SCULPT_BODY_CACHE.has(type))return SCULPT_BODY_CACHE.get(type);
  const plan=SCULPT_PLANS[type];if(!plan)return null;
  const bnds=[99,99,99,-99,-99,-99];
  for(const b of plan.blob)for(let j=0;j<3;j++){
    bnds[j]=Math.min(bnds[j],b[j]-b[j+3]-.15);
    bnds[j+3]=Math.max(bnds[j+3],b[j]+b[j+3]+.15);
  }
  const nX=24,nY=30,nZ=24;
  const cell=[(bnds[3]-bnds[0])/nX,(bnds[4]-bnds[1])/nY,(bnds[5]-bnds[2])/nZ];
  const NX=nX+1,NY=nY+1,NZ=nZ+1;
  const idx=(x,y,z)=>(z*NY+y)*NX+x;
  const field=new Float32Array(NX*NY*NZ);
  for(let z=0;z<NZ;z++)for(let y=0;y<NY;y++)for(let x=0;x<NX;x++)
    field[idx(x,y,z)]=sculptField(plan,bnds[0]+x*cell[0],bnds[1]+y*cell[1],bnds[2]+z*cell[2]);
  const corners=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];
  const tetra=[[0,5,1,6],[0,1,2,6],[0,2,3,6],[0,3,7,6],[0,7,4,6],[0,4,5,6]];
  const edges=[[0,1],[1,2],[2,0],[0,3],[1,3],[2,3]];
  const tri=[[],[[0,3,2]],[[0,1,4]],[[1,4,2],[2,4,3]],[[1,2,5]],[[0,3,5],[0,5,1]],[[0,2,5],[0,5,4]],[[3,4,5]],[[3,5,4]],[[0,4,5],[0,5,2]],[[0,1,5],[0,5,3]],[[1,5,2]],[[2,3,4],[1,2,4]],[[0,4,1]],[[0,2,3]],[]];
  // Precompute scalar-grid gradients once, instead of evaluating expensive
  // skin noise six times per triangle vertex. Startup stays responsive.
  const fieldNormals=new Float32Array(field.length*3);
  for(let z=0;z<NZ;z++)for(let y=0;y<NY;y++)for(let x=0;x<NX;x++){
    const i=idx(x,y,z),g=i*3;
    let gx=(field[idx(Math.min(nX,x+1),y,z)]-field[idx(Math.max(0,x-1),y,z)])/cell[0];
    let gy=(field[idx(x,Math.min(nY,y+1),z)]-field[idx(x,Math.max(0,y-1),z)])/cell[1];
    let gz=(field[idx(x,y,Math.min(nZ,z+1))]-field[idx(x,y,Math.max(0,z-1))])/cell[2];
    const len=Math.hypot(gx,gy,gz)||1;
    fieldNormals[g]=gx/len;fieldNormals[g+1]=gy/len;fieldNormals[g+2]=gz/len;
  }
  const positions=[],normals=[],uvs=[];
  const gradient=(v)=>{
    let nx=v[3],ny=v[4],nz=v[5],len=Math.hypot(nx,ny,nz)||1;
    return [nx/len,ny/len,nz/len];
  };
  const emit=(v,n)=>{
    positions.push(v[0],v[1],v[2]);normals.push(n[0],n[1],n[2]);
    uvs.push(.5+Math.atan2(v[2],v[0])/(Math.PI*2), (v[1]-bnds[1])/(bnds[4]-bnds[1]));
  };
  for(let z=0;z<nZ;z++)for(let y=0;y<nY;y++)for(let x=0;x<nX;x++){
    const vv=[],ff=[];
    for(let c=0;c<8;c++){
      const d=corners[c],xx=x+d[0],yy=y+d[1],zz=z+d[2],i=idx(xx,yy,zz),n=i*3;
      vv[c]=[bnds[0]+xx*cell[0],bnds[1]+yy*cell[1],bnds[2]+zz*cell[2],
        fieldNormals[n],fieldNormals[n+1],fieldNormals[n+2]];
      ff[c]=field[i];
    }
    let min=99,max=-99;for(const q of ff){min=Math.min(min,q);max=Math.max(max,q);}
    if(min>0||max<0)continue;
    for(const t of tetra){
      const ds=t.map(q=>ff[q]);let mask=0;
      for(let j=0;j<4;j++)if(ds[j]<0)mask|=(1<<j);
      if(mask===0||mask===15)continue;
      const interpolated=edges.map(([a,b])=>{
        const dA=ds[a],dB=ds[b];if((dA<0)===(dB<0))return null;
        const u=dA/(dA-dB),A=vv[t[a]],B=vv[t[b]];
        return [A[0]+(B[0]-A[0])*u,A[1]+(B[1]-A[1])*u,A[2]+(B[2]-A[2])*u,
          A[3]+(B[3]-A[3])*u,A[4]+(B[4]-A[4])*u,A[5]+(B[5]-A[5])*u];
      });
      for(const face of tri[mask]){
        let a=interpolated[face[0]],b=interpolated[face[1]],c=interpolated[face[2]];
        if(!a||!b||!c)continue;
        const na=gradient(a);let nb=gradient(b),nc=gradient(c);
        const ax=b[0]-a[0],ay=b[1]-a[1],az=b[2]-a[2],bx=c[0]-a[0],by=c[1]-a[1],bz=c[2]-a[2];
        const cross=(ay*bz-az*by)*(na[0]+nb[0]+nc[0])+(az*bx-ax*bz)*(na[1]+nb[1]+nc[1])+(ax*by-ay*bx)*(na[2]+nb[2]+nc[2]);
        if(cross<0){const tmp=b;b=c;c=tmp;const nt=nb;nb=nc;nc=nt;}
        emit(a,na);emit(b,nb);emit(c,nc);
      }
    }
  }
  const geom=new THREE.BufferGeometry();
  geom.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
  geom.setAttribute('normal',new THREE.Float32BufferAttribute(normals,3));
  geom.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));
  if(geom.computeBoundingSphere)geom.computeBoundingSphere();
  SCULPT_BODY_CACHE.set(type,geom);
  return geom;
}
function sculptSkinMaterial(type){
  if(SCULPT_SKIN_CACHE.has(type))return SCULPT_SKIN_CACHE.get(type);
  const palettes={brute:[118,98,96],crawler:[117,83,82],chaser:[134,74,87],
    stalker:[64,69,77],necromancer:[93,87,94],winged:[89,88,94]};
  const rgb=palettes[type]||[112,101,100];
  const N=256,makeCanvas=()=>{const c=document.createElement('canvas');c.width=c.height=N;return c;};
  const albedo=makeCanvas(),bump=makeCanvas(),rough=makeCanvas(),ac=albedo.getContext('2d'),bc=bump.getContext('2d'),rc=rough.getContext('2d');
  const a=ac.createImageData(N,N),b=bc.createImageData(N,N),r=rc.createImageData(N,N);
  let seed=type.split('').reduce((v,c)=>((v*33)^(c.charCodeAt(0)))>>>0,19638);
  const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
  const hash=(x,y)=>{let n=Math.imul(x,374761393)+Math.imul(y,668265263)+seed;
    n=Math.imul(n^(n>>>13),1274126177);return ((n^(n>>>16))>>>0)/4294967296;};
  const smooth=(v)=>v*v*(3-2*v),noise=(x,y)=>{
    const ix=Math.floor(x),iy=Math.floor(y),fx=smooth(x-ix),fy=smooth(y-iy);
    const a=hash(ix,iy),b=hash(ix+1,iy),c=hash(ix,iy+1),d=hash(ix+1,iy+1);
    return ((a+(b-a)*fx)*(1-fy)+(c+(d-c)*fx)*fy);
  };
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    const uvx=x/N,uvy=y/N;
    const n0=noise(uvx*4.3,uvy*4.3)-.5;
    const n1=noise(uvx*21,uvy*21)-.5;
    const n2=noise(uvx*87,uvy*87)-.5;
    const injury=Math.max(0,Math.sin(uvx*32+Math.sin(uvy*29)*3)*Math.cos(uvy*39+Math.sin(uvx*41)*2)-.72)*3;
    const vein=Math.pow(Math.max(0,1-Math.abs(Math.sin(uvx*25+Math.sin(uvy*22)*1.5))),15)*(.18+Math.max(0,n0));
    const shade=n0*60+n1*29+n2*11-injury*41-vein*28;
    const off=(y*N+x)*4;
    const blood=type==='chaser'?6:type==='brute'?4:0;
    a.data[off]=Math.min(244,Math.max(14,rgb[0]+shade+blood));
    a.data[off+1]=Math.min(225,Math.max(9,rgb[1]+shade*.8-injury*13));
    a.data[off+2]=Math.min(225,Math.max(10,rgb[2]+shade*.8-injury*14));a.data[off+3]=255;
    const relief=Math.max(15,Math.min(230,125+n1*60+n2*45-injury*46+vein*38));
    b.data[off]=b.data[off+1]=b.data[off+2]=relief;b.data[off+3]=255;
    const wetness=type==='chaser'||type==='crawler'?38:12;
    const rv=Math.max(60,Math.min(237,195-wetness+n0*44+n1*48-injury*36));
    r.data[off]=r.data[off+1]=r.data[off+2]=rv;r.data[off+3]=255;
  }
  ac.putImageData(a,0,0);bc.putImageData(b,0,0);rc.putImageData(r,0,0);
  // Non-repeating broad scars and capillaries, painted on the skin texture.
  for(let j=0;j<18;j++){
    let x=rnd()*N,y=rnd()*N;const len=15+rnd()*75;
    ac.beginPath();ac.moveTo(x,y);ac.bezierCurveTo(x+len*.18,y+len*.17,x-len*.22,y+len*.56,x+len*.35,y+len);
    ac.strokeStyle=j%3===0?'rgba(41,18,25,.53)':'rgba(83,28,35,.33)';ac.lineWidth=.6+rnd()*2.4;ac.stroke();
    bc.beginPath();bc.moveTo(x,y);bc.bezierCurveTo(x+len*.18,y+len*.17,x-len*.22,y+len*.56,x+len*.35,y+len);
    bc.strokeStyle='rgba(235,235,235,.38)';bc.lineWidth=1+rnd()*2;bc.stroke();
  }
  const tex=(c)=>{const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;
    t.anisotropy=4;return t;};
  const m=new THREE.MeshStandardMaterial({color:0xffffff,map:tex(albedo),bumpMap:tex(bump),bumpScale:.065,
    roughnessMap:tex(rough),roughness:1,metalness:0,emissive:0x160809,emissiveIntensity:.015});
  SCULPT_SKIN_CACHE.set(type,m);return m;
}

// ---------- organic procedural creature models ----------
// Meshes are built from smooth, irregular ellipsoids, curved tendons and membranes.
// No external model CDN is needed, so the same monsters work offline after Three.js loads.
function buildMonster(type,mat){
  const g=new THREE.Group(), U={L:[],legs:[],wings:[],extras:[],detailMeshes:[]};g.userData=U;
  const flesh=mat;
  // Replace disconnected ellipsoid torsos with shared continuous sculptures.
  const sculpt=(parent,type,skip)=>{
    if(!SCULPTED_CREATURES.has(type))return null;
    const mesh=new THREE.Mesh(sculptBodyGeometry(type),flesh);
    parent.add(mesh);mesh.castShadow=true;mesh.receiveShadow=true;
    U.sculpt=mesh;U.torso=mesh;
    mesh.userData.restScale=mesh.scale.clone();
    return mesh;
  };
  const skin=(c,r=.87)=>creatureMaterial(c,r);
  const bone=skin(0xc8bca3,.61), scar=skin(0x32171b,.9), wet=skin(0x4b131c,.35);
  const tendon=skin(0x4f2427), midnight=skin(0x15131b,.68);
  const iris=creatureMaterial(0x272126,.30,.02); // dark glassy sclera, colored pupils
  const glow=(c)=>{
    const key='glow|'+c;
    if(!CREATURE_MATERIAL_CACHE.has(key))CREATURE_MATERIAL_CACHE.set(key,
      new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:1.0,roughness:.26}));
    return CREATURE_MATERIAL_CACHE.get(key);
  };
  const child=(parent,mesh,x,y,z)=>{mesh.position.set(x,y,z);parent.add(mesh);return mesh;};
  const organ=(parent,x,y,z,rx,ry,rz,m,seed=0)=>{
    const geo=ORGAN_GEOMETRY[Math.abs(seed)%ORGAN_GEOMETRY.length];
    const o=child(parent,new THREE.Mesh(geo,m),x,y,z);o.scale.set(rx,ry,rz);return o;
  };
  const tube=(parent,pts,r,m,radSeg=9)=>{
    const curve=new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p)));
    const mesh=new THREE.Mesh(new THREE.TubeGeometry(curve,Math.max(9,pts.length*6),r,radSeg,false),m);
    parent.add(mesh);return mesh;
  };
  const spike=(parent,x,y,z,r,len,m,dx=0,dz=0)=>{
    const a=child(parent,new THREE.Mesh(new THREE.ConeGeometry(r,len,11),m),x,y,z);
    a.rotation.z=dx;a.rotation.x=dz;return a;
  };
  const eyes=(parent,y,z,sep,rad,color)=>{
    for(const sign of [-1,1]){
      // Recessed charcoal socket, moist eyeball, tiny emissive pupil and eyelid folds.
      organ(parent,sign*sep,y,z-.012,rad*1.40,rad*1.20,rad*.42,midnight,3);
      organ(parent,sign*sep,y,z+rad*.34,rad*.80,rad*.74,rad*.70,iris,6);
      organ(parent,sign*sep,y,z+rad*.94,rad*.36,rad*.41,rad*.24,glow(color));
      tube(parent,[[sign*sep-rad*1.05,y+rad*.13,z+rad*.28],
        [sign*sep,y+rad*.88,z+rad*.5],[sign*sep+rad*1.05,y+rad*.13,z+rad*.28]],rad*.095,scar,6);
    }
  };
  // One smoothly tapered muscular arm rather than three disconnected spheres.
  // It retains the same animated shoulder pivot, wrist and attack timing.
  const limb=(parent,x,y,z,len,w,m,phase,amp,back=false)=>{
    const joint=new THREE.Group();joint.position.set(x,y,z);parent.add(joint);
    const rings=13,sides=12,vertices=[],normals=[],uvs=[],indices=[];
    for(let i=0;i<=rings;i++){
      const t=i/rings,bulge=Math.sin(Math.PI*t),r=w*(1.14-.49*t+.23*bulge*bulge);
      const centerZ=.13*t+.028*Math.sin(Math.PI*t),centerX=.018*Math.sin(2*Math.PI*t);
      for(let k=0;k<=sides;k++){
        const a=k/sides*Math.PI*2,c=Math.cos(a),v=Math.sin(a);
        const rib=1+.045*Math.sin(a*3+t*21)*Math.sin(t*6);
        vertices.push(centerX+r*c*rib,-len*t,centerZ+r*v*.90*rib);
        normals.push(c,0,v);uvs.push(k/sides,t);
      }
    }
    for(let i=0;i<rings;i++)for(let k=0;k<sides;k++){
      let a=i*(sides+1)+k,b=a+sides+1;indices.push(a,a+1,b,a+1,b+1,b);
    }
    const geom=new THREE.BufferGeometry();geom.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));
    geom.setAttribute('uv',new THREE.Float32BufferAttribute(uvs,2));geom.setIndex(indices);geom.computeVertexNormals();
    const arm=new THREE.Mesh(geom,m);joint.add(arm);arm.castShadow=true;arm.receiveShadow=true;
    organ(joint,0,-len,.13,w*.78,w*.55,w*.9,m);
    for(let k=-1;k<=1;k++)tube(joint,[[k*w*.40,-len*.18,.045],[k*w*.44,-len*.51,.11],[k*w*.40,-len*.88,.14]],w*.067,tendon,7);
    U.L.push({p:joint,ph:phase,amp:amp,base:back?-.55:.08,ax:'x'});return joint;
  };
  // Articulated, two-bone leg rig. The gait solver positions the knee and ankle
  // from each foot's planted world-space location; neither bone is a rigid pendulum.
  const jointedLeg=(parent,side,hipX,hipY,hipZ,footX,footZ,upper,lower,width,m,phase=0)=>{
    const upperMesh=new THREE.Mesh(new THREE.CylinderGeometry(.74,1.16,2,12,7),m);
    const lowerMesh=new THREE.Mesh(new THREE.CylinderGeometry(.63,.98,2,12,7),m);
    const kneeMesh=new THREE.Mesh(new THREE.SphereGeometry(1,13,9),m);
    const ankleMesh=new THREE.Mesh(new THREE.SphereGeometry(1,12,9),m);
    parent.add(upperMesh,lowerMesh,kneeMesh,ankleMesh);
    const foot=new THREE.Group();parent.add(foot);
    organ(foot,0,.032,.14,width*1.02,width*.37,width*1.55,m,2);
    for(let k=-1;k<=1;k++){
      const toeX=k*width*.56;
      const toe=organ(foot,toeX,.018,.30,width*.28,width*.26,width*.7,m,k+3);
      toe.rotation.y=k*.15;
      spike(foot,toeX,.018,.47,width*.13,width*.48,bone,0,Math.PI/2);
    }
    const leg={side,hipX,hipY,hipZ,restX:footX,restZ:footZ,upper,lower,width,
      phase,upperMesh,lowerMesh,kneeMesh,ankleMesh,foot,pin:null,swingFrom:null,
      swingTo:null,inSwing:false,phasePrev:0,contactCount:0,lastFoot:null};
    U.legs.push(leg);return leg;
  };
  const jaw=(parent,y,z,width,m)=>{
    const cavity=organ(parent,0,y+.075,z+.075,width*1.06,width*.38,.09,midnight,4);
    cavity.scale.z*=1.25;
    const j=new THREE.Group();j.position.set(0,y,z);parent.add(j);
    organ(j,0,-.105,.12,width,.115,.19,m);
    organ(j,0,-.064,.20,width*.76,.046,.045,wet,4);
    for(let k=-4;k<=4;k++){
      const x=k*width*.21;
      spike(j,x,-.004,.265,.024*(1-Math.abs(k)*.08),.13+((k+5)%3)*.055,bone,Math.PI);
      const upper=spike(parent,x,y+.16,z+.19,.022,.13+((k+4)%3)*.042,bone,Math.PI);
      U.detailMeshes.push(upper);
    }
    U.jaw=j;return j;
  };
  const rib=(parent,y,half,z,m)=>{
    tube(parent,[[-half,y+.08,z],[-half*.55,y-.05,z+.12],[0,y-.13,z+.19],[half*.55,y-.05,z+.12],[half,y+.08,z]],.028,m);
  };
  // Wing membrane: scalloped edges, several finger-like bones and independent flap roots.
  const wing=(parent,sgn,yy,size,m)=>{
    const wingG=new THREE.Group();wingG.position.set(sgn*.42,yy,-.33);parent.add(wingG);
    // Tapered membranous fan, not a set of cuboids.
    const shape=new THREE.Shape();shape.moveTo(0,0);
    shape.lineTo(sgn*size*.38,size*.56);shape.lineTo(sgn*size*1.15,size*.79);
    shape.quadraticCurveTo(sgn*size*.92,size*.33,sgn*size*1.13,size*.06);
    shape.quadraticCurveTo(sgn*size*.90,size*.17,sgn*size*.86,-size*.25);
    shape.quadraticCurveTo(sgn*size*.71,-size*.05,sgn*size*.56,-size*.31);
    shape.quadraticCurveTo(sgn*size*.28,-size*.09,0,-size*.12);shape.closePath();
    // Arched membrane with folded bat-wing knuckles and three-dimensional veins.
    const geo=new THREE.ShapeGeometry(shape,18),pos=geo.attributes&&geo.attributes.position;
    if(pos){for(let i=0;i<pos.count;i++){
      const x=pos.getX(i),y=pos.getY(i);
      pos.setZ(i,-.065*Math.sin((x/size)*Math.PI*1.4)+.13*Math.sin((y/size)*Math.PI));
    }
    pos.needsUpdate=true;geo.computeVertexNormals();}
    const membrane=new THREE.MeshStandardMaterial({color:m,side:THREE.DoubleSide,
      transparent:true,opacity:.95,roughness:.74,metalness:0,bumpMap:skinTex,bumpScale:.085});
    const a=new THREE.Mesh(geo,membrane);wingG.add(a);a.castShadow=true;
    const bones=[[sgn*size*.38,size*.56],[sgn*size*1.15,size*.79],
      [sgn*size*1.13,size*.06],[sgn*size*.86,-size*.25],[sgn*size*.56,-size*.31]];
    for(const v of bones)
      tube(wingG,[[0,0,.06],[v[0]*.44,v[1]*.52,.12],[v[0],v[1],.035]],.018,bone,7);
    for(let k=0;k<10;k++){
      const f=(k+1)/11,x=sgn*size*(.23+.66*f),y=-size*(.03+.18*Math.abs(Math.sin(k*2.4)));
      tube(wingG,[[sgn*size*.25,size*.15,.036],[x*.69,y*.35,.02],[x,y,-.016]],.007,tendon,5);
    }
    U.wings.push({p:wingG,sgn:sgn});return wingG;
  };
  const talons=(parent,x,y,z,spread=.16,len=.28,count=4)=>{
    const hand=organ(parent,x,y,z,spread*.92,.075,.15,flesh,4);
    for(let k=0;k<count;k++){
      const px=x+(k-(count-1)*.5)*spread*.47;
      U.detailMeshes.push(tube(parent,[[px,y-.025,z+.06],[px*1.10,y-.08,z+.16],[px*1.22,y-.13,z+len*.55]],.019,wet,6));
      const tip=child(parent,new THREE.Mesh(new THREE.ConeGeometry(.023,.16,6),bone),
        px*1.24,y-.16,z+len*.64);
      tip.rotation.x=Math.PI*.59;U.detailMeshes.push(tip);
    }
    return hand;
  };
  const scarLine=(parent,points,width=.018)=>{const m=tube(parent,points,width,scar,6);U.detailMeshes.push(m);return m;};
  const fangs=(parent,y,z,span,count=7)=>{
    for(let k=0;k<count;k++){
      const x=(k/(count-1)-.5)*span;
      const tooth=child(parent,new THREE.Mesh(new THREE.ConeGeometry(.027,.13+(k%3)*.025,6),bone),x,y,z);
      tooth.rotation.x=Math.PI;U.detailMeshes.push(tooth);
    }
  };
  // v5.2 Monster Evolution: the three specialist archetypes have their own
  // silhouettes and locomotion instead of borrowing another creature model.
  if(type==='stalker'){
    // Dusk Stalker: nearly skeletal biped, lantern eyes, elongated claws, ripped tendons.
    sculpt(g,'stalker');
    // Shadowed exposed facial plane; integrated torso and neck use one surface.
    organ(g,0,.64,.255,.155,.19,.10,scar);
    jaw(g,.40,.32,.15,scar);fangs(g,.45,.41,.24,6);
    eyes(g,.74,.315,.105,.048,0xc99b51);
    for(let h=0;h<5;h++)rib(g,.28-h*.14,.23+Math.sin(h)*.025,.22,bone);
    for(const side of [-1,1]){
      const a=limb(g,side*.29,.35,-.045,1.07,.077,flesh,side*Math.PI,.94);
      talons(a,0,-1.05,.09,.16,.45,4);
      jointedLeg(g,side,side*.13,-.47,0,side*.20,.30,.69,.57,.095,flesh,side>0?.5:0);
      spike(g,side*.145,.94,-.04,.055,.30,bone,side*.33);
      scarLine(g,[[side*.23,.47,.05],[side*.12,.24,.20],[side*.15,-.09,.19]],.014);
    }
    tube(g,[[0,-.35,-.21],[0,-.58,-.47],[.12,-.56,-.75]],.042,flesh);
    for(let i=0;i<4;i++)spike(g,0,-.03+i*.20,-.24,.023,.16,scar,.67);
  }else if(type==='crawler'){
    // Crypt Crawler: exposed vertebrae and asymmetrical spider-long forelegs.
    const body=new THREE.Group();g.add(body);U.pulse=body;
    sculpt(body,'crawler');
    organ(body,0,-.09,.83,.225,.13,.12,midnight,4);
    eyes(body,.04,.84,.20,.063,0xccb7a2);
    jaw(body,-.36,.78,.27,scar);fangs(body,-.28,.96,.41,9);
    for(let i=0;i<6;i++){
      const side=i<3?-1:1,lane=i%3,z=[.46,-.12,-.60][lane];
      organ(body,side*.43,-.21,z,.20,.14,.24,flesh,i);
      jointedLeg(g,side,side*.44,-.30,z,side*(lane===0?1.08:.86),z*.88,
        lane===0?.82:.67,lane===0?.79:.69,lane===0?.088:.115,flesh,(lane+(side>0?1:0))%2*.5);
      if(lane===0)talons(body,side*.53,-.47,.76,.21,.45,4);
    }
    for(let i=0;i<7;i++){
      const z=-.71+i*.19;
      spike(body,0,.05+(i%2)*.035,z,.055,.22+(i%3)*.04,bone,.25);
      scarLine(body,[[-.20,-.04,z],[0,-.17,z+.025],[.22,-.04,z]],.014);
    }
    U.torso=body.children[0];
  }else if(type==='necromancer'){
    // Ashen Necromancer: tapered shroud, hollow hood, skeletal face, rune focus.
    sculpt(g,'necromancer');
    const cloak=new THREE.Mesh(new THREE.CylinderGeometry(.32,.70,1.82,11,3,true),
      new THREE.MeshStandardMaterial({color:0x221a24,side:THREE.DoubleSide,roughness:.97,bumpMap:skinTex,bumpScale:.045}));
    cloak.position.y=-.36;cloak.position.z=-.06;g.add(cloak);
    for(let k=0;k<9;k++){
      const a=k*Math.PI*2/9;
      const rag=new THREE.Mesh(new THREE.ConeGeometry(.12,.42,5),midnight);
      rag.position.set(Math.cos(a)*.59,-1.38,Math.sin(a)*.48);
      rag.rotation.z=Math.sin(a)*.25;g.add(rag);
    }
    organ(g,0,.67,.045,.37,.39,.34,midnight,6);
    organ(g,0,.63,.34,.24,.27,.15,bone,2);
    organ(g,0,.53,.455,.18,.10,.03,scar,2);
    eyes(g,.75,.46,.125,.057,0xb879f7);
    jaw(g,.38,.40,.14,bone);fangs(g,.39,.52,.20,6);
    for(const side of [-1,1]){
      const arm=limb(g,side*.46,.37,-.04,.87,.105,flesh,side*2.2,.50);
      talons(arm,0,-.83,.09,.13,.35,4);
      jointedLeg(g,side,side*.24,-.53,.0,side*.27,.16,.57,.51,.13,flesh,side>0?.5:0);
      tube(g,[[side*.28,.38,-.32],[side*.41,-.03,-.42],[side*.52,-.58,-.26]],.065,midnight);
      spike(g,side*.39,.90,-.04,.09,.23,bone,side*.33);
    }
    const staff=new THREE.Group();staff.position.set(.70,-.15,.26);g.add(staff);
    const shaft=new THREE.Mesh(new THREE.CylinderGeometry(.033,.055,1.9,9),bone);
    shaft.position.y=.41;staff.add(shaft);
    const crystal=new THREE.Mesh(new THREE.OctahedronGeometry(.175,1),glow(0x713db3));
    crystal.position.y=1.36;staff.add(crystal);
    const sigil=new THREE.Mesh(new THREE.TorusGeometry(.26,.022,7,18),glow(0x5b347f));
    sigil.position.y=1.35;staff.add(sigil);U.staff=staff;U.crystal=crystal;U.sigil=sigil;
    for(let i=0;i<6;i++){
      const a=i*Math.PI/3;
      spike(g,Math.cos(a)*.24,.98,Math.sin(a)*.23,.03,.22,bone,.12);
    }
  }else if(type==='chaser'){
    // Flesh Ghoul: low, swollen body, infant-like malformed head, wet skin, huge eyes.
    sculpt(g,'chaser');
    organ(g,0,.17,.67,.25,.14,.11,scar);
    organ(g,0,.045,.74,.35,.14,.17,wet);
    jaw(g,-.14,.77,.31,wet);fangs(g,-.17,.94,.43,8);
    eyes(g,.25,.66,.27,.14,0xb7a59d);
    for(const sign of [-1,1]){
      const a=limb(g,sign*.44,-.10,.20,.66,.15,flesh,sign*Math.PI,.75);
      talons(a,0,-.62,.17,.23,.34,4);
      jointedLeg(g,sign,sign*.23,-.53,-.14,sign*.36,.20,.41,.38,.15,flesh,sign>0?.5:0);
      organ(g,sign*.34,-.16,.06,.22,.17,.27,flesh,5);
      scarLine(g,[[sign*.28,.19,.57],[sign*.34,-.05,.50],[sign*.32,-.31,.36]],.014);
    }
    for(let j=-2;j<=2;j++){
      organ(g,j*.16,-.43,.36,.07,.055,.05,wet,j+4);
    }
    tube(g,[[0,-.48,-.43],[0,-.51,-.75],[.18,-.57,-.96]],.072,flesh);
  }else if(type==='winged'){
    // Winged Horror: independent patagium wings, long claws, hooked jaw and talons.
    U.flight=true;
    sculpt(g,'winged');
    organ(g,0,.53,.52,.27,.17,.23,scar);
    jaw(g,.34,.59,.23,wet);fangs(g,.41,.72,.36,9);
    eyes(g,.78,.52,.18,.070,0xf4a451);
    for(let i=0;i<5;i++)spike(g,(i-2)*.12,1.06+(i%2)*.08,.1,.06,.36,bone,(i-2)*.23);
    for(const sign of [-1,1]){
      const arm=limb(g,sign*.43,.25,.02,.91,.115,flesh,sign*2.2,.62);
      talons(arm,0,-.86,.14,.18,.36,4);
      const leg=limb(g,sign*.22,-.48,-.06,.72,.125,flesh,sign*2.6,.36);
      talons(leg,0,-.69,.19,.18,.40,3);
      wing(g,sign,.48,1.64,0x553039);
      tube(g,[[sign*.26,.29,-.25],[sign*.51,.11,-.42],[sign*.69,-.27,-.30]],.046,tendon);
    }
    for(let i=0;i<5;i++)rib(g,.27-i*.17,.38-i*.014,.38,bone);
    tube(g,[[0,-.46,-.30],[0,-.63,-.65],[.09,-.76,-.94]],.06,flesh);
  }else if(type==='shooter'){
    organ(g,0,0,0,.66,.64,.53,flesh,4);
    organ(g,0,.1,.49,.47,.46,.20,bone);
    organ(g,0,.09,.655,.27,.29,.14,glow(0x9b3644));
    organ(g,0,.09,.778,.13,.16,.08,midnight);
    for(let i=0;i<8;i++){
      const a=i*Math.PI/4,px=Math.cos(a)*.44,pz=Math.sin(a)*.4;
      const tip=[Math.cos(a)*(.64+.12*(i%2)),-.92,Math.sin(a)*.65];
      const group=new THREE.Group();g.add(group);
      tube(group,[[px,-.25,pz],[px*1.35,-.47,pz*1.3],tip],.066,flesh);
      U.L.push({p:group,ph:a,amp:.13,base:0,ax:'z'});
    }
    for(let j=-2;j<=2;j++)spike(g,j*.16,-.30,.40,.045,.22,bone,Math.PI,.2);
    eyes(g,.52,.21,.27,.075,0xd9a6ff);
  }else if(type==='brute'){
    // Grave Brute: scar-ridden sagging belly, enormous shoulders, cleft head, fists.
    sculpt(g,'brute');
    organ(g,0,.91,.61,.33,.25,.23,scar,7);
    jaw(g,.59,.67,.38,wet);fangs(g,.71,.81,.61,10);
    eyes(g,1.13,.60,.23,.076,0xbca26d);
    for(const sign of [-1,1]){
      organ(g,sign*.79,.48,.02,.39,.41,.39,flesh,2);
      const arm=limb(g,sign*.84,.42,.06,1.23,.29,flesh,sign*2.8,.56);
      organ(arm,0,-1.18,.11,.32,.24,.31,flesh,5);
      talons(arm,0,-1.21,.24,.31,.32,4);
      jointedLeg(g,sign,sign*.40,-.64,.01,sign*.43,.28,.71,.61,.27,flesh,sign>0?.5:0);
      spike(g,sign*.58,.91,-.02,.095,.36,bone,sign*.7);
      scarLine(g,[[sign*.56,.43,.49],[sign*.45,.23,.64],[sign*.30,-.23,.59]],.024);
      for(let a=0;a<3;a++){
        organ(g,sign*(.15+a*.14),-.49,.40,.095,.07,.09,wet,a);
      }
    }
    for(let i=0;i<5;i++)rib(g,.42-i*.23,.55-i*.02,.57,scar);
    scarLine(g,[[-.37,-.38,.62],[-.19,-.49,.75],[.27,-.42,.64]],.025);
  }else if(type==='teleporter'){
    organ(g,0,.12,0,.46,.87,.42,flesh,3);
    organ(g,0,.65,.22,.36,.32,.29,midnight);
    eyes(g,.67,.49,.19,.09,0x5ff7ff);
    const hood=new THREE.Group();g.add(hood);U.spin=hood;
    for(let i=0;i<7;i++){
      const a=i*Math.PI*2/7;
      tube(g,[[Math.cos(a)*.24,-.2,Math.sin(a)*.24],[Math.cos(a)*.43,-.63,Math.sin(a)*.43],[Math.cos(a+1)*.55,-1.06,Math.sin(a+1)*.55]],.057,flesh);
    }
    for(let i=0;i<6;i++){
      const a=i*Math.PI/3;
      organ(hood,Math.cos(a)*.72,.15+Math.sin(a*2)*.3,Math.sin(a)*.72,.08,.07,.1,glow(0x73d8e5));
    }
  }else if(type==='splitter'||type==='mini'){
    const body=new THREE.Group();g.add(body);U.pulse=body;
    organ(body,0,0,0,.62,.48,.57,flesh,2);
    for(let i=0;i<6;i++){
      const side=i<3?-1:1, lane=i%3, front=[.55,.05,-.55][lane];
      organ(body,side*.32,-.12,front,.18,.20,.20,flesh,i);
      jointedLeg(g,side,side*.31,-.19,front,side*.76,front*.94,
        .80,.78,.13,flesh,((lane+(side>0?1:0))%2)*.5);
    }
    eyes(body,.12,.49,.19,.085,0xbdff85);
    jaw(body,-.16,.43,.23,scar);
    if(type==='mini')g.scale.set(.65,.65,.65);
  }else{ // demon lord, articulated wings, crown and armored musculature
    organ(g,0,0,0,1.0,1.26,.74,flesh,1);
    organ(g,0,.39,.56,.72,.55,.28,scar,1);
    organ(g,0,1.21,.16,.55,.57,.48,flesh);
    organ(g,0,1.02,.56,.46,.27,.35,wet);jaw(g,.75,.56,.48,scar);
    eyes(g,1.36,.58,.26,.11,0xffbc43);
    for(let k=-2;k<=2;k++)spike(g,k*.20,1.78+(.2-Math.abs(k)*.07),.07,.13,.76-Math.abs(k)*.1,bone,k*.25);
    for(let k=-2;k<=2;k++)rib(g,.62-k*.19,.67,.72,bone);
    for(const sign of [-1,1]){
      limb(g,sign*1.08,.75,.02,1.42,.27,flesh,sign*2.9,.6);
      jointedLeg(g,sign,sign*.43,-.94,0,sign*.52,.28,.84,.72,.32,flesh,sign>0?.5:0);
      spike(g,sign*.99,1.02,.10,.19,.65,bone,sign*.7);
      wing(g,sign,1.01,1.9,0x72263b);
    }
    organ(g,0,.18,.72,.32,.34,.12,glow(0xff6d25));
  }
  // Skeletal anatomy, raised tendons, asymmetrical scars and teeth are layered
  // onto each species so silhouettes remain expressive rather than geometric toys.
  const anatomyFlesh=skin(0x54282b,.92), cartilage=skin(0xc6b69d,.72);
  if(type==='chaser'||type==='brute'||type==='boss'||type==='winged'){
    const back=[.32,.46,.68].map((v,i)=>v+(type==='boss'?.22:0));
    for(let i=0;i<back.length;i++){
      const y=back[i],s=type==='boss'?1.35:type==='brute'?1.05:.62;
      spike(g,0,y,-.35*s,.045*s,.23*s,cartilage,Math.PI*.70);
      for(const k of [-1,1]){
        tube(g,[[k*.16*s,y-.13,.28*s],[k*.22*s,y,.41*s],[k*.17*s,y+.12,.31*s]],.019*s,anatomyFlesh);
      }
    }
    if(U.jaw)for(let j=-2;j<=2;j++)spike(U.jaw,j*.07,-.07,.21,.021,.12,cartilage,Math.PI);
  }
  if(type==='shooter'){
    for(let i=0;i<7;i++){
      const a=i*2.40;
      organ(g,Math.sin(a)*.40,Math.cos(a)*.32,.19,.07,.13,.06,anatomyFlesh,i);
    }
  }
  if(type==='teleporter'){
    for(let i=0;i<5;i++)spike(g,Math.sin(i*2.2)*.22,.98,Math.cos(i*2.2)*.2,.045,.28,cartilage,.4);
  }
  if(type==='splitter'||type==='mini'){
    for(let i=0;i<7;i++){
      const a=i*Math.PI*2/7;
      organ(g,Math.cos(a)*.32,.23,Math.sin(a)*.3,.10,.13,.10,anatomyFlesh,i);
    }
  }
  if(!U.sculpt)U.torso=g.children.find(c=>c.isMesh&&ORGAN_GEOMETRY.includes(c.geometry))||null;
  if(U.torso)U.torso.userData.restScale=U.torso.scale.clone();
  return g;
}
// Move the tapered limb mesh between joint endpoints without rebuilding geometry.
const IK_UP=new THREE.Vector3(0,1,0);
function placeLimbSegment(mesh,a,b,r){
  const delta=b.clone().sub(a),len=delta.length();
  mesh.position.copy(a).add(b).multiplyScalar(.5);
  mesh.quaternion.setFromUnitVectors(IK_UP,delta.multiplyScalar(1/Math.max(0.00001,len)));
  mesh.scale.set(r,len*.57,r*.88);
}
function solveMonsterLeg(leg,e,target){
  const hip=new THREE.Vector3(leg.hipX,leg.hipY,leg.hipZ);
  const ankle=target.clone();
  const diff=ankle.clone().sub(hip);
  // Geometric two-bone IK with a forward-pointing knee and anatomical reach limits.
  const rawD=diff.length();
  const d=Math.min(leg.upper+leg.lower-.002,Math.max(.075,rawD));
  const axis=diff.normalize();
  const along=(leg.upper*leg.upper-leg.lower*leg.lower+d*d)/(2*d);
  const height=Math.sqrt(Math.max(0,leg.upper*leg.upper-along*along));
  // Knee bends toward the monster's forward axis rather than folding sideways.
  const forward=new THREE.Vector3(0,0,1);
  const side=forward.clone().sub(axis.clone().multiplyScalar(forward.x*axis.x+forward.y*axis.y+forward.z*axis.z));
  if(side.length()<.0001)side.set(0,1,0);
  side.normalize();
  const knee=hip.clone().add(axis.clone().multiplyScalar(along)).add(side.multiplyScalar(height));
  placeLimbSegment(leg.upperMesh,hip,knee,leg.width*1.08);
  placeLimbSegment(leg.lowerMesh,knee,ankle,leg.width*.78);
  leg.kneeMesh.position.copy(knee);leg.kneeMesh.scale.setScalar(leg.width*.92);
  leg.ankleMesh.position.copy(ankle);leg.ankleMesh.scale.setScalar(leg.width*.70);
  leg.foot.position.copy(ankle);
  leg.foot.rotation.x=leg.inSwing?Math.sin(Math.PI*leg.swingPhase)*.14:0;
}
function animateGroundedLegs(e,dt){
  const U=e.mesh.userData, legs=U.legs;
  if(!legs||!legs.length)return;
  const groundedSpeed=Math.hypot(e.actualVX||0,e.actualVZ||0);
  const moving=groundedSpeed>.06;
  const scale=e.mesh.scale.x||1;
  const cy=Math.cos(e.yaw||0),sy=Math.sin(e.yaw||0);
  // Convert between creature-local and world floor locations.
  const worldFoot=(leg,lead=0)=>({
    x:e.x+(leg.restX*cy+leg.restZ*sy)*scale+(e.actualVX||0)*lead,
    z:e.z+(-leg.restX*sy+leg.restZ*cy)*scale+(e.actualVZ||0)*lead
  });
  const footLocal=(p,lift)=>new THREE.Vector3(
    ((p.x-e.x)*cy-(p.z-e.z)*sy)/scale,
    (.065+lift-e.baseY-(e.bodyLift||0))/scale,
    ((p.x-e.x)*sy+(p.z-e.z)*cy)/scale
  );
  for(const leg of legs){
    const phase=(((e.gait/(Math.PI*2)+leg.phase)%1)+1)%1;
    const inSwing=moving&&phase>=.61;
    if(!leg.pin){leg.pin=worldFoot(leg);leg.phasePrev=phase;}
    if(inSwing&&!leg.inSwing){
      leg.swingFrom={...leg.pin};
      leg.swingTo=worldFoot(leg,.13);
      leg.inSwing=true;
    }
    let target=leg.pin,lift=0;
    if(inSwing){
      const q=Math.min(1,Math.max(0,(phase-.61)/.39));
      const ease=q*q*(3-2*q);
      leg.swingPhase=q;
      target={x:leg.swingFrom.x+(leg.swingTo.x-leg.swingFrom.x)*ease,
        z:leg.swingFrom.z+(leg.swingTo.z-leg.swingFrom.z)*ease};
      lift=(e.type==='brute'||e.type==='boss'?.30:.23)*Math.sin(Math.PI*q)*e.moveMag;
    }else{
      if(leg.inSwing){
        leg.pin={...leg.swingTo};leg.contactCount++;leg.inSwing=false;
        const v=vol3(e.x,e.z,20);
        if(v>.12&&e.moveMag>.3){
          noise(e.type==='boss'?.25:.11,e.type==='boss'?220:480,70,
            (e.type==='boss'?.5:e.type==='brute'?.32:.11)*v,'lowpass',pan3(e.x,e.z));
          if((e.type==='brute'||e.type==='boss')&&v>.55)P.shake=Math.max(P.shake,.07*v);
        }
      }
      target=leg.pin;
      // Prevent indefinitely anchored feet after a teleport, push, or strong turn.
      const natural=worldFoot(leg);
      const span=Math.hypot(natural.x-target.x,natural.z-target.z);
      if(span>1.4*scale){leg.pin={...natural};target=leg.pin;}
      if(!moving){leg.pin.x+=(natural.x-leg.pin.x)*Math.min(1,dt*1.5);
        leg.pin.z+=(natural.z-leg.pin.z)*Math.min(1,dt*1.5);target=leg.pin;}
    }
    solveMonsterLeg(leg,e,footLocal(target,lift));
    leg.phasePrev=phase;
    leg.lastFoot={x:target.x,z:target.z,y:.065+lift};
  }
}
function animMonster(e,dt){
  const U=e.mesh.userData;
  if(U.bestiary){
    window.DEPTHS_BESTIARY.update(e,dt,time);
    e.bodyLift=U.bestiary.type==='wraith'?.07*Math.sin(time*1.9+e.ph):
      U.bestiary.type==='gargoyle'?.07+Math.sin(time*2.8+e.ph)*.11-Math.sin(Math.PI*Math.min(1,(e.diveTime||0)/1.05))*.28:0;
    return;
  }
  if(!U.L)return;
  const mv=e.moveMag||0,stride=e.gait||e.ph,breathT=time*.9+e.ph;
  const amp=(e.alert?.35:.10)+mv*.66;
  // Upper body counterbalances the stance leg, while the arms oppose the hips.
  for(const l of U.L){const swing=Math.sin(stride+l.ph)*l.amp*amp;
    if(l.ax==='z')l.p.rotation.z=l.base+swing;
    else if(l.ax==='y')l.p.rotation.y=swing;
    else l.p.rotation.x=l.base+swing;
  }
  if(U.torso){const b=U.torso.userData.restScale,breath=1+Math.sin(breathT)*(.01+.012*mv);
    U.torso.scale.set(b.x*breath,b.y*(2-breath),b.z*(1+.5*(breath-1)));}
  // Ground creatures use two grounded stance feet; hovering creatures float separately.
  e.bodyLift=U.flight
    ? .07+Math.sin(time*2.8+e.ph)*.16-Math.sin(Math.PI*Math.min(1,(e.diveTime||0)/1.05))*.62
    : U.legs.length?(Math.sin(stride*2)*.019*mv):Math.sin(time*1.8+e.ph)*.11;
  if(U.jaw)U.jaw.rotation.x=.05+Math.max(0,Math.sin(time*3.4+e.ph))*(e.alert?.36:.06)+(mv*.05);
  if(U.wings)for(const w of U.wings){
    const flapping=U.flight?(1.4+(e.diveTime>0?2.6:0)):(1.4+mv);
    w.p.rotation.y=w.sgn*(.12+(e.wingFold||0)+Math.sin(time*flapping+e.ph)*(.28+.24*amp));
    w.p.rotation.z=w.sgn*(.10+.11*Math.cos(time*flapping+e.ph));
    w.p.rotation.x=Math.sin(time*flapping*.5+e.ph)*.12;
  }
  // Telegraph and follow-through are linked to the actual attack window.
  const wind=Math.max(0,Math.min(1,e.attackAnim||0));
  if(wind>0){
    const attackCurve=Math.sin(Math.PI*wind);
    if(U.jaw)U.jaw.rotation.x+=attackCurve*.50;
    for(let j=0;j<Math.min(2,U.L.length);j++) U.L[j].p.rotation.x+=attackCurve*.35;
    if(U.staff)U.staff.rotation.x=-attackCurve*.45;
  }
  if(U.crystal)U.crystal.scale.setScalar(1+.12*Math.sin(time*6+e.ph));
  if(U.sigil)U.sigil.rotation.z+=dt*.54;
  if(U.flight)for(const arm of U.L){arm.p.rotation.x+=(e.diveTime>0?-.42:.12);}
  if(U.spin)U.spin.rotation.y+=dt*(1.1+mv*.9);
  if(U.pulse){const k=1+Math.sin(time*4+e.ph)*(.022+.020*mv);U.pulse.scale.set(k,1/k,k);}
  if(U.legs.length)animateGroundedLegs(e,dt);
}
function addBarrel(x,z){
  const m=new THREE.Mesh(new THREE.CylinderGeometry(0.4,0.4,0.9,10),GM(0xaa2222,0x330000)); m.position.set(x,0.45,z); levelGroup.add(m);
  const band=new THREE.Mesh(new THREE.CylinderGeometry(0.41,0.41,0.15,10),GM(0xffcc22,0x332200)); band.position.y=0.1; m.add(band);
  barrels.push({x:x,z:z,mesh:m});
}
function explode(x,z,r,dmg,bar){
  if(bar){ levelGroup.remove(bar.mesh); barrels.splice(barrels.indexOf(bar),1); }
  boomFx(x,z,r); noise(.8,1600,45,.85,'lowpass'); noise(.18,9000,500,.50,'highpass'); beep(50,.52,'sine',.38,-22);
  for(const e of enemies.slice()){
    const d=Math.hypot(e.x-x,e.z-z);
    if(d<r){ e.hp-=dmg*(1-d/r*0.5); e.hit=0.12; e.alert=true; if(d>0.01) moveEnt(e,(e.x-x)/d*(1-d/r)*1.8,(e.z-z)/d*(1-d/r)*1.8,e.r); if(e.hp<=0){ killEnemy(e); if(bar) award('barrel'); } }
  }
  for(const wall of secretWalls.slice())if(Math.hypot(wall.x-x,wall.z-z)<r)damageSecretWall(wall.x,wall.z,20);
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
  type=({imp:'chaser',gargoyle:'winged',wraith:'teleporter'})[type]||type;
  const s=1+0.1*(level-1);
  let col,geo,hp,speed,r,dmg,y;
  if(type==='chaser'){col=0x824550;hp=5;speed=3.6;r=.51;dmg=10;y=1.10;}
  else if(type==='shooter'){col=0x6d537c;geo=new THREE.IcosahedronGeometry(0.6);hp=5;speed=2.4;r=0.5;dmg=0;y=1.4;}
  else if(type==='boss'){col=0x60283e;geo=new THREE.IcosahedronGeometry(1.4);hp=45;speed=2.1;r=1.0;dmg=26;y=1.9;}
  else if(type==='teleporter'){col=0x526b73;hp=6;speed=2.6;r=0.5;dmg=10;y=1.4;}
  else if(type==='splitter'){col=0x567447;hp=10;speed=2.6;r=0.7;dmg=10;y=1.2;}
  else if(type==='mini'){col=0x6d944e;hp=3;speed=4.2;r=0.35;dmg=8;y=0.9;}
  else if(type==='stalker'){col=0x3a3b41;hp=8;speed=3.82;r=.49;dmg=14;y=1.28;}
  else if(type==='armored'){col=0x606870;hp=28;speed=1.75;r=.9;dmg=23;y=1.45;}
  else if(type==='crawler'){col=0x69535a;hp=8;speed=4.25;r=.65;dmg=9;y=1.10;}
  else if(type==='necromancer'){col=0x564c62;hp=14;speed=2.05;r=.65;dmg=0;y=1.40;}
  else if(type==='winged'){col=0x64616a;hp=11;speed=3.35;r=.68;dmg=16;y=2.22;}
  else {col=0x978265;geo=new THREE.DodecahedronGeometry(1.0);hp=14;speed=2.2;r=0.85;dmg=22;y=1.4;}
  const skinType=type==='armored'?'brute':type;
  const mat=SCULPTED_CREATURES.has(skinType)?sculptSkinMaterial(skinType).clone():new THREE.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:.07,roughness:.81,metalness:.015,map:CREATURE_ALBEDO,bumpMap:skinTex,bumpScale:.055,roughnessMap:skinTex});
  const visual={armored:'brute'}[type]||type;
  const bestiaryId=window.DEPTHS_BESTIARY.adaptEnemyId(type);
  const mesh=bestiaryId?window.DEPTHS_BESTIARY.build(bestiaryId,mat):buildMonster(visual,mat);
  if(bestiaryId)y=window.DEPTHS_BESTIARY.SPEC[bestiaryId].baseY;
  if(bestiaryId==='imp')mesh.scale.setScalar(.94+Math.random()*.16);
  if(type==='armored'){
    for(let side of [-1,1]){
      const armor=new THREE.Mesh(new THREE.DodecahedronGeometry(.42,0),new THREE.MeshStandardMaterial({color:0x3b454b,metalness:.68,roughness:.55}));
      armor.scale.set(1,.65,.65);armor.position.set(side*.65,.52,.15);mesh.add(armor);
    }
    const core=new THREE.Mesh(new THREE.OctahedronGeometry(.18,1),new THREE.MeshBasicMaterial({color:0xff8b3c}));
    core.position.set(0,.45,.64);mesh.add(core);
  }
  if(type==='stalker'){
    for(let side of [-1,1]){
      const horn=new THREE.Mesh(new THREE.ConeGeometry(.10,.49,8),new THREE.MeshStandardMaterial({color:0x1d2327,roughness:.85}));
      horn.position.set(side*.27,.95,.02);horn.rotation.z=side*.45;mesh.add(horn);
    }
  }
  if(type==='necromancer'&&!mesh.userData.bestiary){
    const orb=new THREE.Mesh(new THREE.IcosahedronGeometry(.19,1),new THREE.MeshBasicMaterial({color:0x7debd4}));
    orb.position.set(0,.85,.35);mesh.add(orb);
  }
  mesh.position.set(x,y,z); levelGroup.add(mesh);
  if(bestiaryId&&window.DEPTHS_BESTIARY_GLBS&&window.THREE.GLTFLoader){
    const url=window.DEPTHS_BESTIARY_GLBS[bestiaryId];
    if(url){const loader=new THREE.GLTFLoader();
      window.DEPTHS_BESTIARY.tryGLB(bestiaryId,url,loader,(sculpt)=>{
        if(!mesh.parent)return;
        mesh.children.forEach(o=>o.visible=false);
        mesh.add(sculpt);sculpt.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
      },err=>console.warn('Bestiary GLB fallback:',err));}
  }
  const e={type:type,x:x,z:z,hp:Math.ceil(hp*s),maxhp:Math.ceil(hp*s),speed:speed,r:r,dmg:dmg*s,
    mesh:mesh,mat:mat,baseCol:col,baseY:y,name:CREATURE_NAMES[type]||type.toUpperCase(),diveCooldown:2.7,diveTime:0,diveHit:false,alert:false,ai:'idle',attackAnim:0,attackPhase:0,alertAge:0,ambushCooldown:0,chargeCooldown:2.2,huntTimer:0,healT:5,summonT:6,attackCharge:0,meleeCool:.4+Math.random(),bossPhase:1,vulnerable:0,cool:1+Math.random(),ph:Math.random()*6,hit:0,yaw:0,moveMag:0,gait:Math.random()*6.28,bodyLift:0,vx:0,vz:0,actualVX:0,actualVZ:0,px:x,pz:z,hr:({boss:1.5,brute:1.0,mini:0.5,splitter:0.8})[type]||0.7};
  if(type==='boss'){
    const names=['THE ABOMINATION','THE BONE KING','THE HOLLOW SERAPH','THE ABYSSAL WARDEN'];
    e.bossKind=Math.max(0,(Math.ceil(level/(mode==='Survival'?3:5))-1)%4);
    e.bossName=names[e.bossKind];e.vulnerable=2;e.shieldT=0;
    const bossPalette=[0x76311e,0x88999a,0x9e84b6,0x633c32];
    e.mat.color.setHex(bossPalette[e.bossKind]);e.baseCol=bossPalette[e.bossKind];
    const regalia=new THREE.Group();e.mesh.add(regalia);e.regalia=regalia;
    const metal=new THREE.MeshStandardMaterial({color:e.bossKind===1?0x717e80:0x241e29,roughness:.51,metalness:.62});
    for(const side of [-1,1]){
      const plate=new THREE.Mesh(new THREE.DodecahedronGeometry(.37,1),metal);
      plate.position.set(side*.94,.88,-.02);plate.scale.set(1,.44,.92);regalia.add(plate);
    }
    const crest=new THREE.Mesh(new THREE.TorusGeometry(.39,.057,7,28),new THREE.MeshStandardMaterial({color:bossPalette[e.bossKind],emissive:bossPalette[e.bossKind],emissiveIntensity:.42,roughness:.42}));
    crest.position.set(0,1.45,-.23);regalia.add(crest);
    if(e.bossKind===1)for(let i=0;i<5;i++){
      const crown=new THREE.Mesh(new THREE.ConeGeometry(.075,.46,7),metal);
      crown.position.set((i-2)*.20,2.11-.08*Math.abs(i-2),.03);regalia.add(crown);
    }
    if(e.bossKind===2){crest.rotation.y=Math.PI/2;crest.scale.set(1.7,1.7,1);}

    if(e.bossKind===2){e.baseY=2.35;e.mesh.position.y=2.35;}
    if(e.bossKind===1){
      const ward=new THREE.Mesh(new THREE.SphereGeometry(1.5,18,12),new THREE.MeshBasicMaterial({color:0x6be4d9,transparent:true,opacity:.13,wireframe:true,depthWrite:false}));
      ward.position.y=.23;e.mesh.add(ward);e.ward=ward;ward.visible=false;
    }
    currentBoss=e;
  }
  enemies.push(e);
}


const flameGeo=new THREE.SphereGeometry(0.12,8,8);
const glowHp=new THREE.SpriteMaterial({map:glowTex,color:0x66ff99,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
const glowAm=new THREE.SpriteMaterial({map:glowTex,color:0xffdd55,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
function PM(c,e,m){ return new THREE.MeshStandardMaterial({color:c,emissive:e||0,metalness:m||0,roughness:0.5}); }
function pkHealth(){
  // Compact red field-medical case with cross, clasp, handle, stitching and zipper.
  const g=new THREE.Group();
  const canvas=new THREE.MeshStandardMaterial({color:0x8e232a,roughness:.92}),zip=new THREE.MeshStandardMaterial({color:0xd4c5a5,metalness:.66,roughness:.3});
  const kit=new THREE.Mesh(new THREE.BoxGeometry(.52,.34,.23),canvas);g.add(kit);
  const seam=new THREE.Mesh(new THREE.BoxGeometry(.54,.018,.24),zip);seam.position.y=.13;g.add(seam);
  for(const side of [-1,1]){
    const face=new THREE.Mesh(new THREE.BoxGeometry(.24,.07,.012),PM(0xe7e1d0));face.position.set(0,.016,side*.12);g.add(face);
    const cross=new THREE.Mesh(new THREE.BoxGeometry(.07,.24,.014),PM(0xe7e1d0));cross.position.set(0,.016,side*.13);g.add(cross);
  }
  const strap=new THREE.Mesh(new THREE.TorusGeometry(.09,.025,8,24,Math.PI),PM(0x20252b));strap.position.y=.18;strap.rotation.z=Math.PI;g.add(strap);
  for(const x of [-.17,.17]){const clasp=new THREE.Mesh(new THREE.BoxGeometry(.045,.045,.03),zip);clasp.position.set(x,-.09,.125);g.add(clasp);}
  const s=new THREE.Sprite(glowHp);s.scale.set(1.1,1.1,1);g.add(s);g.scale.set(1.45,1.45,1.45);return g;
}
function pkAmmo(){
  // Ammunition case with cartridges and visible brass projectile profiles.
  const g=new THREE.Group(), dark=PM(0x313a31),brass=PM(0xc3a15c,0,0.85),tip=PM(0x82472d,0,0.55);
  const base=new THREE.Mesh(new THREE.BoxGeometry(.60,.20,.30),dark);base.position.y=-.17;g.add(base);
  const ridge=new THREE.Mesh(new THREE.BoxGeometry(.59,.045,.29),PM(0x737d66,0,0.55));ridge.position.y=-.045;g.add(ridge);
  for(let i=0;i<5;i++){
    const x=(i-2)*.115;
    const bullet=new THREE.Mesh(new THREE.CylinderGeometry(.035,.035,.24,12),brass);bullet.position.set(x,.105,0);g.add(bullet);
    const head=new THREE.Mesh(new THREE.ConeGeometry(.035,.105,12),tip);head.position.set(x,.276,0);g.add(head);
    const rim=new THREE.Mesh(new THREE.CylinderGeometry(.044,.044,.025,12),brass);rim.position.set(x,-.02,0);g.add(rim);
  }
  const s=new THREE.Sprite(glowAm);s.scale.set(1.2,1.2,1);g.add(s);g.scale.set(1.35,1.35,1.35);return g;
}
const glowGem=new THREE.SpriteMaterial({map:glowTex,color:0x55ddff,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false});
function pkGem(){
  // An occult faceted soul fragment: deliberately supernatural, not a health/ammo item.
  const g=new THREE.Group();
  const shard=new THREE.Mesh(new THREE.IcosahedronGeometry(.28,1),new THREE.MeshPhysicalMaterial({color:0x6adbe0,emissive:0x17749c,emissiveIntensity:1,metalness:.2,roughness:.1,transparent:true,opacity:.89}));
  shard.scale.y=1.42;g.add(shard);
  const core=new THREE.Mesh(new THREE.OctahedronGeometry(.14),new THREE.MeshBasicMaterial({color:0xedfffe}));core.scale.y=1.4;g.add(core);
  const ring=new THREE.Mesh(new THREE.TorusGeometry(.43,.018,9,32),PM(0xb9edea,0x207b88,.66));ring.rotation.x=1.2;g.add(ring);
  for(let k=0;k<3;k++){const stud=new THREE.Mesh(new THREE.OctahedronGeometry(.045),PM(0xeafdfa));const a=k*Math.PI*2/3;stud.position.set(Math.cos(a)*.43,Math.sin(a)*.43,0);ring.add(stud);}
  const s=new THREE.Sprite(glowGem);s.scale.set(1.2,1.2,1);g.add(s);return g;
}
function pickupLabel(type){
 const text=type==='hp'?'MEDICAL SUPPLIES':type==='ammo'?'AMMUNITION':type==='key'?'CRYPT KEY':'SOUL RELIC';
 const col=type==='hp'?'#fb9c96':type==='ammo'||type==='key'?'#eed39c':'#9cf9f2';
 const c=document.createElement('canvas');c.width=512;c.height=84;const a=c.getContext('2d');
 a.fillStyle='rgba(9,16,25,.8)';a.fillRect(1,7,510,70);a.strokeStyle=col;a.strokeRect(1,7,510,70);
 a.fillStyle=col;a.font='bold 32px Arial';a.textAlign='center';a.fillText(text,256,54);
 const tex=new THREE.CanvasTexture(c),sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true,depthWrite:false}));
 sprite.position.set(0,.64,0);sprite.scale.set(1.45,.25,1);sprite.visible=false;return sprite;
}
// Irregular, thin wet material decals: pooled geometries and mesh objects, no flat red disk.
const bloodMat=new THREE.MeshPhysicalMaterial({color:0x6b0c0c,roughness:.22,metalness:.11,clearcoat:.58,clearcoatRoughness:.2,transparent:true,opacity:.73,depthWrite:false,side:THREE.DoubleSide});
const BLOOD_POOL=[];
const BLOOD_SHAPES=Array.from({length:8},(_,variant)=>{
  const sh=new THREE.Shape(),n=19;
  for(let i=0;i<n;i++){
    const a=i*Math.PI*2/n,r=.38*(.66+.23*Math.sin(i*9.1+variant*2.6)+.1*Math.cos(i*3.8+variant*4.7));
    const x=Math.cos(a)*r,y=Math.sin(a)*r;
    i?sh.lineTo(x,y):sh.moveTo(x,y);
  }
  sh.closePath();return new THREE.ShapeGeometry(sh);
});
function blood(x,y,z,n){
  burst(x,y,z,0x8a0f0f,n,5);
  if(decals.length>60){const old=decals.shift();levelGroup.remove(old);if(old.material===bloodMat&&BLOOD_POOL.length<64)BLOOD_POOL.push(old);}
  const d=BLOOD_POOL.pop()||new THREE.Mesh(BLOOD_SHAPES[0],bloodMat);
  d.geometry=BLOOD_SHAPES[Math.floor(Math.random()*BLOOD_SHAPES.length)];d.scale.setScalar(.7+Math.random()*.95);
  d.rotation.set(-Math.PI/2,0,Math.random()*6.28);
  d.position.set(x+(Math.random()-.5)*.8,.025,z+(Math.random()-.5)*.8);
  levelGroup.add(d);decals.push(d);
}
const shellGeo=new THREE.CylinderGeometry(0.018,0.018,0.06,6), shellBrass=new THREE.MeshStandardMaterial({color:0xd8a62a,metalness:0.9,roughness:0.3}), shellRed=new THREE.MeshStandardMaterial({color:0xcc2222,roughness:0.6});
// Layered GPU-facing effects: hand-generated smoke/fire textures (no external images).
const VFX_TEXTURES=(function(){
 function tex(kind){
   const c=document.createElement('canvas');c.width=c.height=128;const a=c.getContext('2d');
   const center=64;
   if(kind==='fire'){
     let g=a.createRadialGradient(64,65,1,64,65,60);
     g.addColorStop(0,'rgba(255,255,240,1)');g.addColorStop(.19,'rgba(255,244,140,.97)');
     g.addColorStop(.48,'rgba(255,135,21,.83)');g.addColorStop(.75,'rgba(220,37,9,.44)');
     g.addColorStop(1,'rgba(90,8,5,0)');a.fillStyle=g;a.fillRect(0,0,128,128);
     a.globalCompositeOperation='destination-out';
     for(let k=0;k<22;k++){
       const x=64+(Math.random()-.5)*95,y=64+(Math.random()-.5)*95,r=3+Math.random()*13;
       a.fillStyle='rgba(0,0,0,'+(.09+Math.random()*.2)+')';a.beginPath();a.arc(x,y,r,0,Math.PI*2);a.fill();
     }
   }else if(kind==='smoke'){
     for(let k=0;k<130;k++){
       const x=64+(Math.random()-.5)*100,y=64+(Math.random()-.5)*104,r=6+Math.random()*21;
       const g=a.createRadialGradient(x,y,1,x,y,r);
       g.addColorStop(0,'rgba(255,255,255,.09)');g.addColorStop(1,'rgba(255,255,255,0)');
       a.fillStyle=g;a.beginPath();a.arc(x,y,r,0,Math.PI*2);a.fill();
     }
   }else{
     const g=a.createRadialGradient(64,64,0,64,64,62);
     g.addColorStop(0,'rgba(255,255,255,.95)');g.addColorStop(.28,'rgba(255,255,255,.6)');
     g.addColorStop(1,'rgba(255,255,255,0)');a.fillStyle=g;a.fillRect(0,0,128,128);
   }
   const t=new THREE.CanvasTexture(c);t.magFilter=THREE.LinearFilter;t.minFilter=THREE.LinearFilter;return t;
 }
 return {fire:tex('fire'),smoke:tex('smoke'),glow:tex('glow')};
})();
const VFX_MATS={
 fire:new THREE.SpriteMaterial({map:VFX_TEXTURES.fire,color:0xffffff,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending}),
 smoke:new THREE.SpriteMaterial({map:VFX_TEXTURES.smoke,color:0x6f747d,transparent:true,depthWrite:false,opacity:.6}),
 spark:new THREE.SpriteMaterial({map:VFX_TEXTURES.glow,color:0xffb852,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending})
};
// White-hot jet visible at the nozzle while holding the flamethrower trigger.
const flameNozzle=new THREE.Sprite(VFX_MATS.fire.clone());
flameNozzle.position.set(0,.05,-.86);flameNozzle.visible=false;gun.add(flameNozzle);
const VFX_POOL={fire:[],smoke:[],spark:[],glow:[]};
function vfx(kind,x,y,z,scale,life,vx,vy,vz,brightness=1){
 if(fx.length>(SET.quality<.75?120:SET.quality<1.25?260:420))return null;
 const pool=VFX_POOL[kind]||(VFX_POOL[kind]=[]);
 const obj=pool.pop()||new THREE.Sprite(VFX_MATS[kind].clone());
 obj.material.color.set(0xffffff);obj.material.opacity=brightness;obj.position.set(x,y,z);obj.scale.set(scale,scale,1);
 obj.material.rotation=Math.random()*6.28;levelGroup.add(obj);
 fx.push({vfx:true,kind:kind,mesh:obj,t:0,dur:life,scale:scale,
  vx:vx||0,vy:vy||0,vz:vz||0,phase:Math.random()*6.283,alpha:brightness});
 return obj;
}
const boomGeo=new THREE.SphereGeometry(1,16,12), ringGeo=new THREE.RingGeometry(0.88,1,40), scorchMat=new THREE.MeshBasicMaterial({color:0x120805,transparent:true,opacity:0.8,depthWrite:false});
function boomFx(x,z,r){
  // White-hot ignition, orange rolling fire, black turbulent smoke and radial sparks.
  vfx('fire',x,1.0,z,1.8,.25,0,1.2,0,1);
  for(let i=0;i<(SET.quality<.75?7:SET.quality<1.25?14:22);i++){
    const a=Math.random()*Math.PI*2,u=.4+Math.random()*4.7;
    vfx('fire',x+Math.cos(a)*Math.random()*.28,.5+Math.random()*1.1,z+Math.sin(a)*Math.random()*.28,
      .52+Math.random()*1.35,.30+Math.random()*.48,Math.cos(a)*u,1.4+Math.random()*3.1,Math.sin(a)*u,.6+Math.random()*.35);
  }
  for(let i=0;i<(SET.quality<.75?7:SET.quality<1.25?15:23);i++){
    const a=Math.random()*Math.PI*2,u=.9+Math.random()*4.2;
    vfx('smoke',x+Math.cos(a)*Math.random()*.6,.55+Math.random()*1.5,z+Math.sin(a)*Math.random()*.6,
      .75+Math.random()*1.35,1.0+Math.random()*1.25,Math.cos(a)*u,1.3+Math.random()*2,Math.sin(a)*u,.52);
  }
  for(let i=0;i<(SET.quality<.75?8:SET.quality<1.25?15:22);i++){
    const a=Math.random()*Math.PI*2,u=3+Math.random()*10;
    vfx('spark',x,1.0,z,.07+Math.random()*.12,.27+Math.random()*.66,
      Math.cos(a)*u,2+Math.random()*7,Math.sin(a)*u,.75);
  }
  const rg=new THREE.Mesh(ringGeo,new THREE.MeshBasicMaterial({color:0xffd192,transparent:true,opacity:.68,side:THREE.DoubleSide,depthWrite:false}));
  rg.rotation.x=-Math.PI/2;rg.position.set(x,.06,z);levelGroup.add(rg);
  fx.push({pr:true,kind:'ring',mesh:rg,t:0,dur:.53,r:r,x0:x,y0:.06,z0:z,x1:x,y1:.06,z1:z});
  const light=new THREE.PointLight(0xff9b46,9,r*5,2);light.position.set(x,1.2,z);levelGroup.add(light);
  fx.push({vfxLight:true,mesh:light,t:0,dur:.31});
  if(decals.length>60)levelGroup.remove(decals.shift());
  const sc=new THREE.Mesh(new THREE.CircleGeometry(r*.65,24),scorchMat);
  sc.rotation.x=-Math.PI/2;sc.position.set(x,.025,z);levelGroup.add(sc);decals.push(sc);
  boomT=1;P.shake=Math.max(P.shake,.62);
}
function eject(wi){
  if(wi>3) return;
  const rx=Math.cos(P.yaw), rz=-Math.sin(P.yaw), fx2=-Math.sin(P.yaw), fz2=-Math.cos(P.yaw);
  const m=new THREE.Mesh(shellGeo,wi===1?shellRed:shellBrass); if(wi===1) m.scale.set(1.5,1.6,1.5);
  m.position.set(P.x+rx*0.3+fx2*0.3,1.25,P.z+rz*0.3+fz2*0.3); m.rotation.set(Math.random()*3,Math.random()*3,Math.random()*3); levelGroup.add(m);
  fx.push({mesh:m,vx:rx*(2+Math.random()*1.5),vy:2+Math.random()*1.5,vz:rz*(2+Math.random()*1.5),life:1.3,line:false});
}
function addPickup(type,x,z){
  const mesh=type==='hp'?pkHealth():(type==='ammo'?pkAmmo():pkGem());
  mesh.position.set(x,0.9,z);mesh.add(pickupLabel(type));levelGroup.add(mesh);
  pickups.push({type:type,x:x,z:z,mesh:mesh,ph:Math.random()*6});
}

// weapon projectiles: [kind, colour, length, speed]
const PJ=[['bolt',0xffe08a,0.6,110],['bolt',0xffa040,0.28,75],['bolt',0x8ac8ff,0.42,115],['bolt',0xffd27a,0.58,120],['gren',0x7acb4a,0,26],['flame',0xff7a22,0,14]];
function spawnProj(wi,x0,y0,z0,x1,y1,z1,done){
  const p=PJ[wi], kind=p[0], dist=Math.hypot(x1-x0,y1-y0,z1-z0); let m, dur=0.3;
  if(kind==='bolt'){ m=new THREE.Mesh(new THREE.BoxGeometry(0.035,0.035,p[2]),new THREE.MeshBasicMaterial({color:p[1]})); dur=dist/p[3]; m.position.set(x0,y0,z0); m.lookAt(x1,y1,z1); }
  else if(kind==='gren'){ m=new THREE.Mesh(new THREE.SphereGeometry(0.13,10,10),PM(0x7acb4a,0x2a5010)); dur=Math.max(0.12,dist/p[3]); m.position.set(x0,y0,z0); }
  else { const material=VFX_MATS.fire.clone(); material.opacity=.94;
    m=new THREE.Sprite(material);m.scale.set(.45,.45,1);m.position.set(x0,y0,z0);
    dur=Math.max(.08,dist/p[3]);
  }
  levelGroup.add(m);
  fx.push({pr:true,kind:kind,mesh:m,t:0,dur:dur,x0:x0,y0:y0,z0:z0,x1:x1,y1:y1,z1:z1,done:done});
}

// ---------- fx ----------
function burst(x,y,z,col,n,spd){
  n=Math.ceil(n*(SET.quality<.75?.36:SET.quality<1.25?.65:1));
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
  a*=1-armourReduction();

  if(keys.KeyC&&P.wi>=6&&P.stamina>0&&DEFENSE.exhausted<=0){
    const perfect=parryWindow>0;
    const guardDirection=activeGuardDirection();DEFENSE.guard=guardDirection;
    const cost=perfect?5:Math.max(7,a*.75);
    if(P.stamina<cost){P.stamina=0;DEFENSE.exhausted=1.15;a*=.9;toast('GUARD BROKEN · EXHAUSTED',750);}
    else {P.stamina-=cost;a*=perfect?.06:(guardDirection==='high'?.42:.58);}

    if(perfect){beep(1130,.14,'triangle',.08,-320);vfx('spark',P.x,1.25,P.z,.6,.24,0,.7,0,.8);}
  }
  if(P.armor>0){const absorbed=Math.min(P.armor,a*.5);P.armor-=absorbed;a-=absorbed;}
  P.hp-=a; flashA=Math.min(0.55,flashA+0.12+a*0.01); P.shake=Math.max(P.shake,Math.min(0.6,0.15+a*0.03));
  if(P.hp<=0){
    P.hp=0; state='dead'; saveBest(); STATS.deaths++; recordRun(); beep(160,0.6,'sawtooth',0.08,-100);
    showMenu('dead');
  }
}
// Dead monsters retain a brief physical fall instead of instantly popping away.
// Corpses do not participate in enemy AI or collision and are capped to eight meshes.
let fallenMonsters=[];
function killEnemy(e){
  if(!e||enemies.indexOf(e)<0)return;
  fallenMonsters.push({mesh:e.mesh,t:0,lean:(e.x%2<1?-1:1),originY:e.mesh.position.y});
  if(fallenMonsters.length>8){const oldest=fallenMonsters.shift();levelGroup.remove(oldest.mesh);}
  enemies.splice(enemies.indexOf(e),1);
  P.kills++; if(e.type!=='mini') killsThisLevel++; STATS.kills++; award('first');
  if(e.type==='boss'){award('boss');currentBoss=null;P.coins+=150;toast('BOSS DEFEATED · +150 SOUL COINS',1600);} 
  if(P.leech) P.hp=Math.min(P.maxhp,P.hp+P.leech);
  if(e.type==='splitter'){ for(let i=0;i<2;i++){ addEnemy('mini',e.x,e.z); enemies[enemies.length-1].alert=true; } }
  P.combo=P.ct>0?Math.min(10,P.combo+1):1; P.ct=3;
  P.score+=Math.round((e.type==='boss'?1000:(e.type==='brute'?250:(e.type==='shooter'?120:100)))*(1+(P.combo-1)*0.1));
  if(P.combo>=3) toast('Combo x'+P.combo+'!',900); if(P.combo>=5) award('combo');
  burst(e.x,e.baseY,e.z,e.baseCol,e.type==='boss'?40:16,6); blood(e.x,e.baseY,e.z,e.type==='boss'?30:14);
  noise(0.35,700,60,0.4,'lowpass',pan3(e.x,e.z)); beep(140,0.3,'sawtooth',0.1,-90);
  if(Math.random()<0.28) addPickup(Math.random()<0.5?'hp':'ammo',e.x,e.z);
  unlockPortalIfReady();
}
// Frame-sampled sweeping melee contact: enemies must actually intersect the
// sword arc during its active window. Each target can only be hit once per swing.
let meleeSwingNumber=0,meleeCombo=0,meleeComboUntil=0;
function meleeAttack(w,requested='light'){
  if(state!=='playing'||paused||P.cool>0||keys.KeyC)return;
  if(P.wi===7&&gunModels[7].userData.bladeProgress<.84){
    P.cool=.13;return; // saber is still extending: no phantom early hit
  }
  let style='horizontal',side=(meleeSwingNumber++%2?1:-1);
  if(P.wi===6||P.wi===7){
    const mode=requested==='heavy'?'heavy':requested==='thrust'?'thrust':'light';
    if(mode==='heavy'||mode==='thrust'){
      if(P.wi===7&&mode==='heavy'){
        if(P.energy<18){toast('NOT ENOUGH ENERGY',800);return;}
        P.energy-=18;
      }else{
        const cost=mode==='heavy'?15:8;
        if(P.stamina<cost){toast('NOT ENOUGH STAMINA',800);return;}
        P.stamina-=cost;
      }
      style=mode;
    }else{
      style=meleeCombo%2===1?'diagonal':'horizontal';
    }
  }
  meleeCombo=time<meleeComboUntil?Math.min(3,meleeCombo+1):1;
  meleeComboUntil=time+1.2;
  const duration=w.cd*P.rate*(style==='heavy'?(P.wi===7?1.44:1.54):
    style==='thrust'?(P.wi===7?1.14:1.18):1-(meleeCombo-1)*.035);
  if(style==='light'){
    const cost=P.wi===7?3:6;
    if(P.stamina<cost){toast('NOT ENOUGH STAMINA',800);return;}
    P.stamina-=cost;
  }
  P.cool=duration;recoil=.015;bladeSwing=1;bladeElapsed=0;bladeDuration=duration;
  pendingMelee={weapon:P.wi,hits:new Set(),lastPhase:0,side,style,total:0};
  gunSound(P.wi);
  if(P.wi===6&&style==='heavy'){beep(115,.23,'triangle',.06,-52);noise(.19,2100,350,.17,'bandpass');}
  if(P.wi===7&&style==='heavy'){beep(270,.25,'sawtooth',.09,660);noise(.24,5100,420,.24,'bandpass');}
  if(P.wi===6&&style==='thrust')noise(.16,4600,620,.25,'bandpass');
  if(P.wi===7&&style==='thrust'){beep(510,.20,'sawtooth',.09,-240);noise(.16,5900,720,.23,'bandpass');}
  emitNoise(P.x,P.z,8);P.shake=Math.max(P.shake,.06);
}
function meleeWound(e,weapon){
  if(!e.mesh||!e.mesh.userData)return;
  const U=e.mesh.userData;U.wounds=U.wounds||[];
  if(U.wounds.length>=3)return;
  const size=e.type==='boss'?1.5:e.type==='brute'?1.15:.75;
  const mat=new THREE.MeshStandardMaterial({color:weapon===7?0x142b36:0x4b131b,
    emissive:weapon===7?0x1b8ba9:0x32050a,emissiveIntensity:weapon===7?.65:.18,
    roughness:.62,transparent:true,opacity:.96,depthWrite:false});
  const curve=new THREE.CatmullRomCurve3([
    new THREE.Vector3(-.38*size,.45*size,.41*size),
    new THREE.Vector3(-.09*size,.13*size,.46*size),
    new THREE.Vector3(.32*size,-.19*size,.41*size)]);
  const mark=new THREE.Mesh(new THREE.TubeGeometry(curve,12,.013*size,6,false),mat);
  mark.rotation.z=(U.wounds.length-1)*.18;e.mesh.add(mark);U.wounds.push(mark);
}
function severMonsterPart(e,weapon){
  if(!e.mesh||!e.mesh.userData||!e.mesh.userData.L)return;
  const limbs=e.mesh.userData.L.filter(l=>l.p&&l.p.parent);
  if(!limbs.length)return;
  const count=e.type==='boss'?2:1;
  for(let k=0;k<Math.min(count,limbs.length);k++){
    const entry=limbs[k===0?0:limbs.length-1];if(!entry.p.parent)continue;
    const part=entry.p,local=part.position.clone();part.parent.remove(part);
    // The monster is already facing the player; rotate the local anchor into world space.
    const a=e.mesh.rotation.y,wx=local.x*Math.cos(a)+local.z*Math.sin(a),
       wz=-local.x*Math.sin(a)+local.z*Math.cos(a);
    part.position.set(e.x+wx,e.baseY+local.y+(e.bodyLift||0),e.z+wz);
    part.rotation.y+=a;part.scale.multiplyScalar(.96);levelGroup.add(part);
    const dir=(k===0?1:-1),force=weapon===7?4.2:3.3;
    fx.push({severed:true,mesh:part,life:1.7+Math.random()*.6,
      vx:dir*(1.2+Math.random()*1.2)+(e.knockX||0)*.5,
      vy:3+Math.random()*2.0,vz:(Math.random()-.5)*force+(e.knockZ||0)*.5,
      spinX:(Math.random()-.5)*5,spinY:(Math.random()-.5)*6,bounced:false});
    for(let j=0;j<8;j++)vfx(weapon===7?'spark':'fire',part.position.x,part.position.y,part.position.z,
      .12+Math.random()*.1,.25,(Math.random()-.5)*2,1+Math.random()*2,(Math.random()-.5)*2,.76);
  }
}
function resolveMelee(previousPhase,currentPhase){
  const swing=pendingMelee;if(!swing)return;
  if(!swing.wallHit&&currentPhase>.35){
    const dx=-Math.sin(P.yaw),dz=-Math.cos(P.yaw);
    for(let dist=.8;dist<Math.min(2.8,WEAPONS[swing.weapon].rng);dist+=.3){
      if(damageSecretWall(P.x+dx*dist,P.z+dz*dist,WEAPONS[swing.weapon].dmg)){swing.wallHit=true;break;}
    }
  }
  const weapon=swing.weapon,w=WEAPONS[weapon];
  const first=Math.max(previousPhase,.27),last=Math.min(currentPhase,.74);
  if(last<first)return;
  const samples=Math.max(1,Math.ceil((last-first)/.036));
  for(let i=0;i<=samples;i++){
    const phase=first+(last-first)*i/samples;
    const mid=(phase-.27)/.47;
    const arc=swing.style==='thrust'?0:
      swing.style==='heavy'?(.5-mid)*.60*swing.side:
      swing.style==='diagonal'?(.5-mid)*(weapon===7?2.30:2.40)*swing.side:
      (.5-mid)*(weapon===7?2.32:2.65)*swing.side;
    const fx=-Math.sin(P.yaw),fz=-Math.cos(P.yaw),rx=Math.cos(P.yaw),rz=-Math.sin(P.yaw);
    for(const e of enemies.slice()){
      if(swing.hits.has(e))continue;
      const vx=e.x-P.x,vz=e.z-P.z,d=Math.hypot(vx,vz);
      if(d<.28||d>w.rng+e.hr)continue;
      const right=(vx*rx+vz*rz)/d,front=(vx*fx+vz*fz)/d;
      const angular=Math.atan2(right,front);
      const angularError=Math.atan2(Math.sin(angular-arc),Math.cos(angular-arc));
      const tolerance=swing.style==='thrust'?.13:
        swing.style==='heavy'?.22:.18;
      if(Math.abs(angularError)>(tolerance+Math.atan2(e.hr*.76,d)))continue;
      if(swing.style==='thrust'&&d>w.rng*.86+e.hr)continue;
      if(!los(P.x,P.z,e.x,e.z))continue;
      swing.hits.add(e);swing.total++;
      const leverage=Math.max(.68,Math.min(1.22,1.18-d/(w.rng*4)));
      const damage=w.dmg*P.dmgm*(swing.style==='heavy'?(weapon===7?1.48:1.65):swing.style==='thrust'?(weapon===7?1.12:1.17):1)*(1+WEAPON_LEVELS[weapon]*.09)*weaponDamageBonus(weapon)*leverage*(e.type==='armored'?.55:1)*(e.type==='boss'&&e.vulnerable>0?1.55:1)*(1+(meleeCombo-1)*.12);
      e.hp-=damage;e.hit=.22;e.alert=true;e.stagger=.30+(weapon===7?.08:0);e.staggerSide=swing.side;
      const force=weapon===7?(swing.style==='heavy'?6.0:5.6):swing.style==='heavy'?5.4:3.8;
      e.knockX=(e.knockX||0)+((vx/d)*.80+rx*swing.side*.24)*force;
      e.knockZ=(e.knockZ||0)+((vz/d)*.80+rz*swing.side*.24)*force;
      P.shake=Math.max(P.shake,weapon===7?.23:.18);hitT=1;
      dmgNum(e.x,e.baseY+.7,e.z,Math.max(1,Math.round(damage)),weapon===7?'#8ae8ff':'#ffe0c1');
      meleeWound(e,weapon);
      blood(e.x,e.baseY,e.z,weapon===7?8:11);
      for(let k=0;k<9;k++)vfx(weapon===7?'spark':'fire',e.x+(Math.random()-.5)*.4,
        e.baseY+.5+(Math.random()-.5)*.8,e.z+(Math.random()-.5)*.4,
        .12+Math.random()*.12,.25+Math.random()*.2,(Math.random()-.5)*3,
        .5+Math.random()*2,(Math.random()-.5)*3,.78);
      bladeImpactSound(weapon,e.x,e.z);
      if(e.hp<=0){severMonsterPart(e,weapon);killEnemy(e);}
    }
  }
  if(swing.total>=3)award('rail');
}

// ---------- ABYSSAL V5: continuous collision projectiles and magazine system ----------
function startReload(){
  const wi=P.wi;if(wi>=6||P.reloadT>0||magazines[wi]>=MAG_CAP[wi]||P.ammo<=0)return false;
  P.reloadT=WEAPONS[wi].reload;P.reloadWi=wi;
  menuClickSound('equip');toast('RELOADING · '+WEAPONS[wi].n,750);return true;
}
function finishReload(){
  const wi=P.reloadWi;if(wi<0)return;
  const need=MAG_CAP[wi]-magazines[wi],taken=Math.min(need,Math.floor(P.ammo/Math.max(1,WEAPONS[wi].cost)));
  magazines[wi]+=taken;P.ammo-=taken*Math.max(1,WEAPONS[wi].cost);
  P.reloadWi=-1;P.reloadT=0;if(taken)beep(570,.09,'triangle',.035,150);
}
function makeShot(wi,angle,tilt,pellet=0){
  const w=WEAPONS[wi],speed=w.velocity;
  const cp=Math.cos(tilt);
  const dx=-Math.sin(angle)*cp, dz=-Math.cos(angle)*cp, dy=Math.sin(tilt);
  // All projectiles are integrated in update(); damage is never decided at firing time.
  const mesh=new THREE.Mesh(new THREE.SphereGeometry(wi===4?.11:.025,6,6),
    new THREE.MeshBasicMaterial({color:wi===4?0x929b66:wi===5?0xff963e:0xffdba2}));
  mesh.position.set(P.x+dx*.36,1.42+dy*.14,P.z+dz*.36);levelGroup.add(mesh);
  shots.push({mesh,wi,x:mesh.position.x,y:mesh.position.y,z:mesh.position.z,
    vx:dx*speed,vy:dy*speed+(wi===4?4:0),vz:dz*speed,life:wi===4?3.0:1.15,
    pierces:wi===0?1:0,hit:new Set(),pellet,travel:0});
}
function finishShot(shot,impact=false){
  const index=shots.indexOf(shot);if(index>=0)shots.splice(index,1);
  if(shot.mesh.parent)shot.mesh.parent.remove(shot.mesh);
  if(shot.mesh.geometry)shot.mesh.geometry.dispose();
  if(shot.mesh.material)shot.mesh.material.dispose();
  if(impact&&shot.wi===4)explode(shot.x,shot.z,WEAPONS[4].blast,WEAPONS[4].dmg*P.dmgm,null);
}
function projectileHitEnemy(shot,e){
  const w=WEAPONS[shot.wi],headshot=shot.y>e.baseY+.47*(e.type==='boss'?1.7:1) &&shot.y<e.baseY+1.5;
  const weak=(e.type==='armored'&&headshot)||(e.type==='boss'&&e.vulnerable>0);
  let damage=w.dmg*P.dmgm*(1+WEAPON_LEVELS[shot.wi]*.09)*weaponDamageBonus(shot.wi)*(headshot?1.85:1)*(weak?1.5:1);
  if(shot.wi===1)damage*=Math.max(.32,1-shot.travel/24);
  if(e.type==='armored'&&!weak)damage*=.40;
  if(e.type==='boss'&&e.bossKind===1&&e.shieldT>0)damage*=.35;
  if(e.type==='winged'&&!e.alert)damage*=.40;
  e.hp-=damage;e.hit=.16;e.alert=true;
  e.knockX=(e.knockX||0)+shot.vx/Math.max(1,w.velocity)*(shot.wi===1?1.7:.42);
  e.knockZ=(e.knockZ||0)+shot.vz/Math.max(1,w.velocity)*(shot.wi===1?1.7:.42);
  e.stagger=Math.max(e.stagger||0,shot.wi===1?.32:.12);
  e.lastHit=shot.wi;
  if(shot.wi===5)e.burn=4;
  dmgNum(e.x,e.baseY+.78,e.z,Math.round(damage)+(headshot?' ✦':''),headshot?'#ffcc77':'#fff');
  if(shot.wi!==5)blood(e.x,e.baseY,e.z,headshot?9:4);
  MASTERY[shot.wi]+=damage;
  if(e.hp<=0)killEnemy(e);
}
function updateProjectiles(dt){
  for(let i=shots.length-1;i>=0;i--){
    const s=shots[i];if(!s)continue;
    const speed=Math.hypot(s.vx,s.vy,s.vz),steps=Math.min(32,Math.max(1,Math.ceil(speed*dt/.35)));
    const h=dt/steps;let ended=false;
    for(let k=0;k<steps;k++){
      s.vy-=WEAPONS[s.wi].gravity*h;
      s.x+=s.vx*h;s.y+=s.vy*h;s.z+=s.vz*h;s.travel+=speed*h;
      if(s.y<.12||s.y>WALLH-.05||solid(s.x,s.z)){
        if(solid(s.x,s.z))damageSecretWall(s.x,s.z,s.wi===4?12:WEAPONS[s.wi].dmg);
        if(s.wi!==4&&Math.random()<.3)burst(s.x,Math.max(.1,s.y),s.z,0xe3af75,2,1);
        finishShot(s,true);ended=true;break;
      }
      const bar=barrels.find(b=>Math.hypot(b.x-s.x,b.z-s.z)<.52&&s.y<1.3);
      if(bar){finishShot(s,false);explode(bar.x,bar.z,4,8,bar);ended=true;break;}
      let hitSomething=false;
      for(const e of enemies.slice()){
        if(s.hit.has(e)||Math.hypot(e.x-s.x,e.z-s.z)>e.hr+.08)continue;
        if(Math.abs(s.y-e.baseY)>(e.type==='boss'?2.1:1.5))continue;
        if(s.wi===4){finishShot(s,true);ended=true;hitSomething=true;break;}
        s.hit.add(e);projectileHitEnemy(s,e);hitSomething=true;
        if(!s.pierces){finishShot(s,false);ended=true;break;}
        s.pierces--;
      }
      if(ended)break;
      if(hitSomething&&s.wi===0){vfx('spark',s.x,s.y,s.z,.12,.18,.2,.2,.2,.7);}
    }
    if(!ended){s.mesh.position.set(s.x,s.y,s.z);s.life-=dt;if(s.life<=0)finishShot(s,s.wi===4);}
  }
}

function shoot(){
  if(state!=='playing'||P.cool>0||P.reloadT>0)return;
  const wi=P.wi,w=WEAPONS[wi];
  if(w.melee){meleeAttack(w);return;}
  if(magazines[wi]<=0){if(!startReload()){P.cool=.18;beep(100,.08,'square',.05);}return;}
  magazines[wi]--;P.cool=w.cd*P.rate*Math.max(.90,1-masteryTier(wi)*.02);
  muzzle=.065;P.shake=Math.max(P.shake,wi===1||wi===4?.27:.06);recoil=KICK[wi];
  gunSound(wi);if(wi<5)eject(wi);if(w.burn)heat=Math.min(1,heat+.18);
  // Sound is a first-class AI input; gunshots are investigated even without line of sight.
  emitNoise(P.x,P.z,wi===4?30:wi===5?14:wi===1?24:20);
  // Burst queue is primed by an initial press, never by continuation shots.
  const pelletCount=w.pel;
  for(let p=0;p<pelletCount;p++){
    const spread=(Math.random()-.5)*2*w.spr*(1+(P.shake*.05));
    const tilt=P.pitch+(Math.random()-.5)*w.spr*.65;
    if(wi===5){
      // Flame remains a short-range continuous cone with persistent fire VFX.
      const dx=-Math.sin(P.yaw+spread),dz=-Math.cos(P.yaw+spread);
      let r=1;
      while(r<w.rng&&!solid(P.x+dx*r,P.z+dz*r)){
        const e=enemies.find(e=>Math.hypot(e.x-(P.x+dx*r),e.z-(P.z+dz*r))<e.hr+.16);
        if(e){const damage=w.dmg*P.dmgm;e.hp-=damage;e.burn=4;e.alert=true;MASTERY[wi]+=damage;
          if(e.hp<=0)killEnemy(e);break;}
        r+=.43;
      }
      const fx=P.x+dx*Math.min(r,6),fz=P.z+dz*Math.min(r,6);
      spawnProj(wi,P.x+dx*.48,1.3,P.z+dz*.48,fx,1.3+Math.sin(P.pitch)*r*.6,fz,null);
      if(hazards.filter(h=>h.kind==='fire').length<12&&Math.random()<.04&&!solid(fx,fz))createHazard('fire',fx,fz,.42);
    }else makeShot(wi,P.yaw+spread,tilt,p);
  }
  if(magazines[wi]===0&&wi!==5)toast('MAGAZINE EMPTY · PRESS R',700);
}
// Shared grid flow field gives every monster a route around solid dungeon walls.
// Rebuild only after the player enters a new maze cell or the dungeon changes.
let monsterNav=null,monsterNavX=-1,monsterNavZ=-1;
function resetMonsterNavigation(){monsterNav=null;monsterNavX=-1;monsterNavZ=-1;}
function getMonsterNavigation(){
  const px=Math.floor(P.x/CELL),pz=Math.floor(P.z/CELL);
  if(monsterNav&&px===monsterNavX&&pz===monsterNavZ)return monsterNav;
  monsterNavX=px;monsterNavZ=pz;
  const dist=new Int16Array(GW*GH);dist.fill(-1);monsterNav=dist;
  if(px<0||pz<0||px>=GW||pz>=GH||grid[pz][px]!==0)return dist;
  const queue=[pz*GW+px];dist[queue[0]]=0;
  for(let head=0;head<queue.length;head++){
    const idx=queue[head],x=idx%GW,z=Math.floor(idx/GW),next=dist[idx]+1;
    for(const [sx,sz] of [[1,0],[-1,0],[0,1],[0,-1]]){
      const nx=x+sx,nz=z+sz;
      if(nx<0||nz<0||nx>=GW||nz>=GH||grid[nz][nx]!==0)continue;
      const nidx=nz*GW+nx;if(dist[nidx]!==-1)continue;
      dist[nidx]=next;queue.push(nidx);
    }
  }
  return dist;
}
function monsterWaypoint(e,hasDirectPath){
  if(hasDirectPath)return {x:P.x,z:P.z};
  const dist=getMonsterNavigation(),gx=Math.floor(e.x/CELL),gz=Math.floor(e.z/CELL);
  if(gx<0||gz<0||gx>=GW||gz>=GH)return {x:P.x,z:P.z};
  const here=dist[gz*GW+gx];
  if(here<=0)return {x:P.x,z:P.z};
  let best=null,bestDist=here;
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
    const nx=gx+dx,nz=gz+dz;
    if(nx<0||nz<0||nx>=GW||nz>=GH)continue;
    const nd=dist[nz*GW+nx];
    if(nd>=0&&nd<bestDist){bestDist=nd;best={x:(nx+.5)*CELL,z:(nz+.5)*CELL};}
  }
  return best||{x:(gx+.5)*CELL,z:(gz+.5)*CELL};
}


// ---------- ABYSSAL V5: telegraphed multi-phase boss encounters ----------
function bossWarningAmbient(x,z){
  const ring=new THREE.Mesh(new THREE.RingGeometry(2.4,2.6,40),new THREE.MeshBasicMaterial({color:currentTheme.torch,side:THREE.DoubleSide,transparent:true,opacity:.25,depthWrite:false}));
  ring.rotation.x=-Math.PI/2;ring.position.set(x,.04,z);levelGroup.add(ring);
}

function bossWarning(e,kind){
  if(bossTelegraphs.length>=8)return;
  const radius=kind==='pulse'?3.8:kind==='blast'?2.8:kind==='line'?1.75:2.5;
  const x=kind==='pulse'?e.x:P.x,z=kind==='pulse'?e.z:P.z;
  const ring=new THREE.Mesh(new THREE.RingGeometry(radius-.08,radius,36),
    new THREE.MeshBasicMaterial({color:kind==='blast'?0xff4b23:0xef6aab,transparent:true,opacity:.68,depthWrite:false,side:THREE.DoubleSide}));
  ring.rotation.x=-Math.PI/2;ring.position.set(x,.07,z);levelGroup.add(ring);
  bossTelegraphs.push({mesh:ring,x,z,radius,remaining:1.12,kind,owner:e});
  if(kind==='line'){
    const vx=P.x-e.x,vz=P.z-e.z,len=Math.hypot(vx,vz)||1;
    for(let i=1;i<=2;i++){
      const tx=e.x+vx/len*Math.min(len,i*2.6),tz=e.z+vz/len*Math.min(len,i*2.6);
      const m=ring.clone();m.position.set(tx,.075,tz);levelGroup.add(m);
      bossTelegraphs.push({mesh:m,x:tx,z:tz,radius:1.5,remaining:1.12,kind:'strike',owner:e});
    }
  }
  noise(.32,1100,130,.26,'lowpass',pan3(x,z));
}
function updateBossTelegraphs(dt){
  for(let i=bossTelegraphs.length-1;i>=0;i--){const a=bossTelegraphs[i];
    a.remaining-=dt;a.mesh.material.opacity=.25+Math.abs(Math.sin(time*19))*.45;
    if(a.remaining>0)continue;
    levelGroup.remove(a.mesh);a.mesh.geometry.dispose();a.mesh.material.dispose();bossTelegraphs.splice(i,1);
    boomFx(a.x,a.z,a.radius);
    if(Math.hypot(P.x-a.x,P.z-a.z)<a.radius)hurt(a.kind==='pulse'?19:15);
    for(const e of enemies){if(e!==a.owner&&Math.hypot(e.x-a.x,e.z-a.z)<a.radius){e.hit=.15;}}
  }
}
function tickBoss(e,dt,d,visible){
  const next=e.hp>e.maxhp*.66?1:e.hp>e.maxhp*.33?2:3;
  if(e.bossPhase!==next){
    e.bossPhase=next;e.vulnerable=2.0;
    toast(e.bossName+' · PHASE '+next,1600);creatureSound('boss',e.x,e.z,true);
    for(let j=0;j<18;j++)vfx('spark',e.x,e.baseY+.3,e.z,.24,.4,(Math.random()-.5)*4,2,(Math.random()-.5)*4,.9);
  }
  if(!e.alert)return;
  e.bossTimer=(e.bossTimer||3.8)-dt;
  e.shieldT=Math.max(0,(e.shieldT||0)-dt);
  if(e.ward){e.ward.visible=e.shieldT>0;e.ward.rotation.y+=dt*.8;}
  if(e.bossKind===2){e.bodyLift=(e.bodyLift||0)+Math.sin(time*2.1)*.14;}
  if(e.bossKind===3&&e.bossPhase>=2&&Math.random()<dt*.2){
    const a=Math.random()*6.28,x=e.x+Math.cos(a)*2.3,z=e.z+Math.sin(a)*2.3;
    if(!solid(x,z))createHazard('fire',x,z,.65);
  }
  if(e.bossTimer<=0&&visible){
    e.bossTimer=Math.max(1.7,4.7-e.bossPhase*.6);
    const kind=e.bossKind===0?'pulse':e.bossKind===1?'blast':e.bossKind===2?'line':e.bossPhase===3?'pulse':'blast';
    if(e.bossKind===1&&e.bossPhase>=2){e.shieldT=1.9;e.vulnerable=0;}
    if(e.bossKind===3&&e.bossPhase>=2){
      for(let k=0;k<3;k++){const a=k/3*Math.PI*2+time;
        const xx=e.x+Math.cos(a)*3,zz=e.z+Math.sin(a)*3;
        if(!solid(xx,zz))createHazard('fire',xx,zz,.70);
      }
    }
    bossWarning(e,kind);
    if(e.bossKind===1&&enemies.length<40&&e.bossPhase>=2){
      for(let k=0;k<2;k++){const x=e.x+Math.cos(k*Math.PI)*2,z=e.z+Math.sin(k*Math.PI)*2;
        if(!blocked(x,z,.34)){addEnemy('mini',x,z);enemies[enemies.length-1].alert=true;}}
    }
    if(e.bossKind===2&&e.bossPhase>=2)e.tp=.1;
  }
}


// ---------- ABYSSAL V5: defensive melee, timed counter and charged energy sweep ----------
function chargeSaber(){
 if(state!=='playing'||paused||P.wi!==7||P.cool>0||pendingSaberCharge>0||P.energy<30)return false;
 P.energy-=30;P.cool=1.15;pendingSaberCharge=.52;
 beep(160,.48,'sawtooth',.10,740);noise(.38,5600,400,.23,'bandpass');
 toast('CHARGING ENERGY WAVE',450);return true;
}
function unleashSaberWave(){
 const dx=-Math.sin(P.yaw),dz=-Math.cos(P.yaw);
 for(const e of enemies.slice()){
  const x=e.x-P.x,z=e.z-P.z,dist=Math.hypot(x,z);
  if(dist>4.8||dist<.1||(x*dx+z*dz)/dist<.28||!los(P.x,P.z,e.x,e.z))continue;
  const damage=14*P.dmgm*(1+WEAPON_LEVELS[7]*.09);
  e.hp-=damage;e.hit=.36;e.stagger=.45;
  e.knockX=(e.knockX||0)+x/dist*3.4;e.knockZ=(e.knockZ||0)+z/dist*3.4;
  dmgNum(e.x,e.baseY+.6,e.z,Math.round(damage),'#a2f8ff');
  for(let j=0;j<4;j++)vfx('spark',e.x,e.baseY+.6,e.z,.24,.38,(Math.random()-.5)*2,2,(Math.random()-.5)*2,.85);
  if(e.hp<=0)killEnemy(e);
 }
 for(let j=0;j<22;j++){
   const a=P.yaw+(j/21-.5)*2.1,x=P.x-Math.sin(a)*3.2,z=P.z-Math.cos(a)*3.2;
   if(!solid(x,z))vfx('spark',x,.6+Math.random()*.6,z,.24,.32,0,.9,0,.85);
 }
 P.shake=Math.max(P.shake,.24);beep(850,.24,'sawtooth',.16,-570);
}

// ---------- update ----------
function update(dt){
  if(bladeSwing>0){
    const before=bladeElapsed/Math.max(.1,bladeDuration);
    bladeElapsed+=dt;
    if(pendingMelee)resolveMelee(before,bladeElapsed/Math.max(.1,bladeDuration));
    if(bladeElapsed>=bladeDuration){bladeSwing=0;pendingMelee=null;}
  }
  if(pendingSaberCharge>0){pendingSaberCharge-=dt;if(pendingSaberCharge<=0){pendingSaberCharge=0;unleashSaberWave();}}
  parryWindow=Math.max(0,parryWindow-dt);
  DEFENSE.dodgeCooldown=Math.max(0,DEFENSE.dodgeCooldown-dt);
  DEFENSE.exhausted=Math.max(0,DEFENSE.exhausted-dt);
  if(DEFENSE.dodgeTime>0){
    const slice=Math.min(dt,DEFENSE.dodgeTime);DEFENSE.dodgeTime-=slice;
    // moveEnt uses the same collision handling as ordinary locomotion.
    moveEnt(P,DEFENSE.dodgeX*18*slice,DEFENSE.dodgeZ*18*slice,P.r);
  }

  P.energy=Math.min(100,P.energy+dt*3.1);
  if(keys.KeyC&&P.wi>=6&&P.stamina>0)P.stamina=Math.max(0,P.stamina-dt*10);
  dungeonAmbience(dt);
  updateProjectiles(dt);
  updateBossTelegraphs(dt);
  updateHazards(dt);
  time+=dt; P.inv=Math.max(0,P.inv-dt); P.ct-=dt; if(P.ct<=0) P.combo=0;
  const saber=gunModels[7]&&gunModels[7].userData;
  if(saber&&saber.bladeCore){
    const target=(state==='playing'&&!paused&&P.wi===7)?1:0;
    saber.bladeProgress+=(target-saber.bladeProgress)*(1-Math.exp(-dt*(target?3.0:6.0)));
    const k=Math.max(.001,Math.min(1,saber.bladeProgress));
    // Local Y is the cylinder axis even when the mesh points along world Z.
    // Keep the near end fixed at the emitter, stretching the tip forward.
    for(const [j,mesh] of [saber.bladeAura,saber.bladeCore,saber.bladeWhite].entries()){
      const len=saber.bladeLengths[j];
      mesh.scale.y=k;
      mesh.position.z=saber.bladeBaseZ-len*k*.5;
    }
    saber.bladeAura.material.opacity=.04+.23*k;
    saber.bladeCore.material.opacity=.05+.90*k;
    saber.bladeWhite.material.opacity=.05+.94*k;
    saber.bladeLight.position.z=saber.bladeBaseZ-.35*k;
    saber.bladeLight.intensity=1.5*k;
  }
  if(P.hp<30){ hb-=dt; if(hb<=0){ hb=0.9; beep(58,0.14,'sine',0.35,-18); setTimeout(function(){ beep(52,0.12,'sine',0.25,-15); },170); } }
  for(const c of checkpoints){
    if(!c.on&&Math.hypot(c.x-P.x,c.z-P.z)<1.5){
      c.on=true; c.mat.color.set(0x33ff99); c.mat.emissive.set(0x11cc66); lastCP={x:c.x,z:c.z};
      P.hp=Math.min(P.maxhp,P.hp+40); P.ammo+=10;saveCampaign();toast('CHECKPOINT SAVED  (+40 HP, +10 ammo)',2400); beep(660,0.25,'sine',0.07,400);
    }
  }
  P.cool=Math.max(0,P.cool-dt);
  if(P.reloadT>0){P.reloadT=Math.max(0,P.reloadT-dt);if(P.reloadT===0)finishReload();}
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
  const sprint=(k.ShiftLeft||k.ShiftRight)&&P.stamina>2;
  const sp=(sprint?9:6)*dt*P.spd*(RELICS.bulwark&&sprint?.93:1);
  const spendingSprint=sprint&&(Math.abs(f)+Math.abs(s)>0);
  const regen=17*(RELICS.vigor?1.25:1);
  P.stamina=Math.max(0,Math.min(P.maxStamina,P.stamina+dt*(spendingSprint?-26:(DEFENSE.exhausted>0?0:regen))));
  let mx=-Math.sin(P.yaw)*f+Math.cos(P.yaw)*s, mz=-Math.cos(P.yaw)*f-Math.sin(P.yaw)*s;
  const ml=Math.hypot(mx,mz);
  if(ml>0){
    mx=mx/ml*sp; mz=mz/ml*sp; moveEnt(P,mx,mz,P.r); walkT+=dt;
    const spr=!!(k.ShiftLeft||k.ShiftRight); stepT+=dt*(spr?1.5:1); if(stepT>0.4){ stepT=0; footstep(spr); }
  } else stepT=0.3;
  const fireHeld=!!(k.Space||k.KeyF||k.mouse||gpFire);
  if(P.wi===3&&rifleMode==='BURST'){
    if(fireHeld&&!triggerHeld&&burstQueue===0){burstQueue=2;shoot();}
    else if(burstQueue>0&&P.cool<=0&&P.reloadT===0){burstQueue--;shoot();}
  }else if(fireHeld)shoot();
  triggerHeld=fireHeld;

  // enemies
  const dead=[];
  for(const e of enemies){
    const dx=P.x-e.x, dz=P.z-e.z, d=Math.hypot(dx,dz)||0.001;
    const visible=d<(e.type==='stalker'?13:22)&&los(e.x,e.z,P.x,P.z);
    e.bestiaryDistance=d;e.tpFade=Math.max(0,(e.tpFade||0)-dt*2.1);
    e.vulnerable=Math.max(0,(e.vulnerable||0)-dt);
    e.attackAnim=Math.max(0,(e.attackAnim||0)-dt*2.5);
    e.ambushCooldown=Math.max(0,(e.ambushCooldown||0)-dt);
    e.chargeCooldown=Math.max(0,(e.chargeCooldown||0)-dt);
    e.diveCooldown=Math.max(0,(e.diveCooldown||0)-dt);
    e.diveTime=Math.max(0,(e.diveTime||0)-dt);
    e.alertAge=e.alert?(e.alertAge||0)+dt:0;
    // Distance/quality LOD for small teeth, fine scars and individual nails.
    // Heavy body meshes remain visible at every quality level.
    e.lodTimer=(e.lodTimer||0)-dt;
    if(e.lodTimer<=0){
      e.lodTimer=.25+(Math.abs(e.x+e.z)%4)*.045;
      const near=SET.quality>=1.25||d<(SET.quality<.75?8.5:15);
      const lod=e.mesh.userData;
      if(lod.detailMeshes&&lod.detailVisible!==near){
        lod.detailVisible=near;
        for(const part of lod.detailMeshes)part.visible=near;
      }
    }
    // Narrow crypt corridors force flying creatures to fold their wing membranes.
    if(e.type==='winged'){
      e.wingFold=(blocked(e.x+1.45,e.z,.10)||blocked(e.x-1.45,e.z,.10)||
        blocked(e.x,e.z+1.45,.10)||blocked(e.x,e.z-1.45,.10))?.62:.06;
    }
    // Explicit state is useful for animation, sound, debugging and later AI extensions.
    e.ai=(e.stagger||0)>0?'stagger':e.attackCharge>0?'attack':e.retreat>0?'retreat':!e.alert?'patrol':visible?'pursue':e.huntTimer>0?'investigate':'search';
    if(e.huntTimer>0)e.huntTimer-=dt;
    if(e.type==='boss')tickBoss(e,dt,d,visible);

    if(!e.alert&&visible&&d<20){e.alert=true;e.ai='pursue';growl(e,e.type==='brute'||e.type==='boss');
      if(e.type==='winged')burst(e.x,e.baseY-.6,e.z,0xa49e99,15,2);}
    if(e.type==='stalker'&&visible&&d<8&&e.hp<e.maxhp*.4)e.retreat=2.4;
    if(e.retreat>0)e.retreat=Math.max(0,e.retreat-dt);
    if(e.type==='necromancer'&&e.alert){
      e.healT-=dt;e.summonT-=dt;
      if(e.healT<=0){e.healT=6.2;
        for(const ally of enemies){if(ally!==e&&Math.hypot(ally.x-e.x,ally.z-e.z)<7){ally.hp=Math.min(ally.maxhp,ally.hp+3);vfx('spark',ally.x,ally.baseY+.6,ally.z,.45,.4,0,.9,0,.55);}}
      }
      if(e.summonT<=0&&enemies.length<43){e.summonT=7.4;
        for(let count=0;count<2;count++){const xx=e.x+Math.cos(count*3.0)*1.4,zz=e.z+Math.sin(count*3.0)*1.4;
          if(!blocked(xx,zz,.36)){addEnemy('mini',xx,zz);enemies[enemies.length-1].alert=true;}}
        creatureSound('shooter',e.x,e.z,true);
      }
    }
    if(e.burn>0){
      e.burn-=dt; e.hp-=1.6*dt*P.dmgm; if(e.hp<=0) dead.push(e);
      if(!e.fireS){ e.fireS=new THREE.Sprite(VFX_MATS.fire.clone()); e.fireS.position.y=0.3; e.mesh.add(e.fireS); }
      e.fireS.visible=true; const fk=2+Math.sin(time*18+e.ph)*0.3; e.fireS.scale.set(fk,fk*1.3,1);
      e.bp=(e.bp||0)-dt; if(e.bp<=0){ e.bp=.14; vfx('fire',e.x+(Math.random()-.5)*.6,e.baseY+.35,e.z+(Math.random()-.5)*.6,.65,.40,(Math.random()-.5),1.2,(Math.random()-.5),.7);if(Math.random()<.38)vfx('smoke',e.x,e.baseY+.8,e.z,.7,1.0,.2,1.5,.2,.3); }
      e.sp=(e.sp||0)-dt; if(e.sp<=0){ e.sp=0.5; for(const o of enemies){ if(o!==e&&!(o.burn>0)&&Math.hypot(o.x-e.x,o.z-e.z)<1.5) o.burn=2.5; } }
    } else if(e.fireS) e.fireS.visible=false;
    if(e.hit>0){ e.hit-=dt; e.mat.emissive.set(0x9a2b24); e.mat.emissiveIntensity=0.42; }
    else { e.mat.emissive.set(0x161016); e.mat.emissiveIntensity=e.alert?0.075:0.015; }
    if(e.burn>0){ e.mat.emissive.set(0xff5a10); e.mat.emissiveIntensity=0.8+Math.sin(time*20)*0.3; }
    if(!e.alert){
      e.patrolT=(e.patrolT||0)-dt;
      if(e.patrolT<=0){e.patrolT=3+Math.random()*2.8;
        const cx=Math.floor(e.x/CELL),cz=Math.floor(e.z/CELL);
        const opts=[[1,0],[-1,0],[0,1],[0,-1]].filter(q=>grid[cz+q[1]]&&grid[cz+q[1]][cx+q[0]]===0);
        if(opts.length){const v=opts[Math.floor(Math.random()*opts.length)];e.patrolX=(cx+v[0]+.5)*CELL;e.patrolZ=(cz+v[1]+.5)*CELL;}
      }
      if(e.patrolX!==undefined){const px=e.patrolX-e.x,pz=e.patrolZ-e.z,d2=Math.hypot(px,pz);
        if(d2>.4){const step=Math.min(d2,e.speed*.22*dt);moveEnt(e,px/d2*step,pz/d2*step,e.r);
          e.moveMag=.22;e.gait+=dt*3.4;e.yaw+=(((Math.atan2(px,pz)-e.yaw+Math.PI*3)%(Math.PI*2))-Math.PI)*Math.min(1,dt*3);
        }else e.moveMag=0;
      }
      animMonster(e,dt);e.mesh.position.set(e.x,e.baseY+(e.bodyLift||0),e.z);e.mesh.rotation.y=e.yaw;continue;
    }
    e.gr=(e.gr===undefined?Math.random()*4:e.gr)-dt;
    if(e.gr<=0){ e.gr=4+Math.random()*5; growl(e,e.type==='brute'||e.type==='boss'); }
    if(e.type==='teleporter'){
      e.tp=(e.tp||2)-dt;
      if(e.tp<=0){ e.tp=3+Math.random()*2; const a=Math.random()*6.28, rr=5+Math.random()*4, nx=P.x+Math.cos(a)*rr, nz=P.z+Math.sin(a)*rr;
        if(!blocked(nx,nz,0.6)){ e.tpFade=.8;burst(e.x,1.4,e.z,0x33ddff,10,4); e.x=nx; e.z=nz; e.px=nx;e.pz=nz;e.vx=0;e.vz=0; for(const l of (e.mesh.userData.legs||[]))l.pin=null; burst(nx,1.4,nz,0x33ddff,10,4); } }
    }
    let want=1;
    const ranged=(e.type==='shooter'||e.type==='boss'||e.type==='necromancer'||e.type==='teleporter');
    if(e.retreat>0)want=-1.05;
    if(ranged){ if(d<6) want=-.8; else if(d<10) want=0; }
    if(e.type==='stalker'&&d<3.2&&e.hp<e.maxhp*.35)want=-1.2;
    if(e.type==='necromancer'&&visible&&d<8)want=-1.15;
    if(e.type==='crawler'&&visible&&d>2.1&&d<8)want=.92;
    if(e.type==='winged'&&e.diveTime>0)want=1.58;
    // Impact inertia is integrated separately from pursuit, with drag and wall collision.
    if(e.knockX||e.knockZ){
      moveEnt(e,(e.knockX||0)*dt,(e.knockZ||0)*dt,e.r);
      const friction=Math.exp(-10.5*dt);
      e.knockX=(e.knockX||0)*friction;e.knockZ=(e.knockZ||0)*friction;
      if(Math.abs(e.knockX)<.015)e.knockX=0;
      if(Math.abs(e.knockZ)<.015)e.knockZ=0;
    }
    e.stagger=Math.max(0,(e.stagger||0)-dt);
    const waypoint=monsterWaypoint(e,visible);
    if(e.type==='crawler'&&visible&&d>2.3&&d<12){
      const lateral=Math.sin(e.ph+Math.floor(time/2.4)*2)>0?1:-1;
      const sideDist=2.6;
      const tx=P.x+Math.cos(P.yaw)*sideDist*lateral;
      const tz=P.z-Math.sin(P.yaw)*sideDist*lateral;
      if(!blocked(tx,tz,e.r)){waypoint.x=tx;waypoint.z=tz;e.ai='flank';}
    }
    if(e.type==='stalker'&&visible&&d>5){
      const sign=Math.sin(e.ph)>0?1:-1;waypoint.x=P.x+Math.cos(P.yaw)*sign*3.8;waypoint.z=P.z-Math.sin(P.yaw)*sign*3.8;
      if(blocked(waypoint.x,waypoint.z,e.r)){waypoint.x=P.x;waypoint.z=P.z;}
    }
    if(e.heard&&!visible&&e.huntTimer>0){waypoint.x=e.heard.x;waypoint.z=e.heard.z;}
    const wx=waypoint.x-e.x,wz=waypoint.z-e.z,wd=Math.hypot(wx,wz)||.001;
    const desiredSpeed=(want>0&&d<e.r+1.0)?0:e.speed*want*(e.stagger>0?.16:1);
    // Brutes commit to a short charge only on a visible, unobstructed lane.
    let chargeBonus=1;
    if((e.type==='brute'||e.type==='armored')&&visible&&d>3.5&&d<9&&e.chargeCooldown<=0&&e.stagger<=0){
      e.chargeTime=.72;e.chargeCooldown=5.2;e.ai='charge';
      e.attackAnim=1;creatureSound('brute',e.x,e.z,true);
    }
    if(e.chargeTime>0){e.chargeTime=Math.max(0,e.chargeTime-dt);chargeBonus=1.65;e.ai='charge';}
    const chaseX=wx/wd*desiredSpeed*chargeBonus,chaseZ=wz/wd*desiredSpeed*chargeBonus;
    // Winged Horrors circle, telegraph a diving strike, then retreat to hover height.
    if(e.type==='winged'&&visible&&d>3.2&&d<9&&e.diveCooldown<=0&&e.stagger<=0){
      e.diveTime=1.05;e.diveCooldown=4.1;e.diveHit=false;e.attackAnim=1;
      e.ai='dive';creatureSound('winged',e.x,e.z,true);
    }
    if(e.type==='winged'&&e.diveTime>0){
      chargeBonus=1.82;e.ai='dive';
      if(!e.diveHit&&d<2.15&&visible){
        e.diveHit=true;e.meleeCool=Math.max(e.meleeCool||0,1.1);hurt(e.dmg*.57);
        P.shake=Math.max(P.shake,.11);
        vfx('spark',e.x,e.baseY-.26,e.z,.36,.36,0,.5,0,.57);
      }
    }
    const steer=1-Math.exp(-dt*(e.type==='brute'||e.type==='boss'?3.0:5.2));
    e.vx+=(chaseX-e.vx)*steer; e.vz+=(chaseZ-e.vz)*steer;
    // Velocity-based acceleration makes feet accelerate and decelerate with the body.
    moveEnt(e,e.vx*dt,e.vz*dt,e.r);
    for(const o of enemies){
      if(o===e) continue;
      const ox=e.x-o.x, oz=e.z-o.z, od=Math.hypot(ox,oz);
      if(od<1.1&&od>0.001) moveEnt(e,ox/od*dt*2,oz/od*dt*2,e.r);
    }
    const mvx=(e.x-e.px)/Math.max(dt,.001), mvz=(e.z-e.pz)/Math.max(dt,.001);
    e.px=e.x;e.pz=e.z;e.actualVX=mvx;e.actualVZ=mvz;
    e.moveMag=Math.min(1,Math.hypot(mvx,mvz)/Math.max(.01,e.speed));
    if(e.moveMag>.025)e.gait+=dt*(e.type==='brute'||e.type==='boss'?9.4:11.0+e.speed*.75)*e.moveMag;
    const targetYaw=(!ranged&&d>2.6&&Math.hypot(e.vx,e.vz)>.18)?Math.atan2(e.vx,e.vz):Math.atan2(P.x-e.x,P.z-e.z);
    if(e.yaw===undefined)e.yaw=targetYaw;
    const yawDiff=((targetYaw-e.yaw+Math.PI*3)%(Math.PI*2))-Math.PI;
    e.yaw+=yawDiff*Math.min(1,dt*(e.type==='brute'||e.type==='boss'?2.6:5.8));
    animMonster(e,dt);
    e.mesh.position.set(e.x,e.baseY+(e.bodyLift||0),e.z);
    e.mesh.rotation.y=e.yaw;
    e.mesh.rotation.z=(e.stagger||0)/.4*(e.staggerSide||1)*.18+Math.sin(e.gait)*.024*e.moveMag;
    e.mesh.rotation.x=e.moveMag>.1?.023*Math.sin(e.gait*.5):0;
    if(ranged){
      e.cool-=dt;
      if(e.cool<=0&&visible){
        e.cool=e.type==='boss'?Math.max(.7,1.8-e.bossPhase*.24):e.type==='necromancer'?2.4:e.type==='teleporter'?3.1:1.5+Math.random()*.8;
        const spread=e.type==='boss'?(e.bossPhase>=3?[-.48,-.24,0,.24,.48]:[-.28,0,.28]):[0];
        for(const a of spread){
          const ca=Math.cos(a), sa=Math.sin(a);
          const ux=dx/d, uz=dz/d;
          const m=new THREE.Mesh(new THREE.SphereGeometry(0.22,10,10),
            new THREE.MeshBasicMaterial({color:e.type==='boss'?0xff4aa0:0xd070ff}));
          m.position.set(e.x,1.4,e.z); levelGroup.add(m);
          orbs.push({mesh:m,x:e.x,z:e.z,vx:(ux*ca-uz*sa)*9,vz:(ux*sa+uz*ca)*9,life:4,wraith:e.type==='teleporter'});
        }
        beep(420,0.12,'sine',0.04,-200);
      }
    }
    if(e.dmg>0){
      e.meleeCool=Math.max(0,(e.meleeCool||0)-dt);
      if(e.attackCharge>0){
        e.attackCharge-=dt;
        if(e.attackCharge<=0&&Math.hypot(P.x-e.x,P.z-e.z)<e.r+1.2&&visible){
          hurt(e.dmg*(e.type==='boss'?.55:.36));
          P.shake=Math.max(P.shake,.14);beep(95,.14,'sawtooth',.06,-35);
        }
      }else if(e.meleeCool===0&&d<e.r+(e.type==='winged'?1.60:1.25)&&visible){
        e.meleeCool=e.type==='boss'?2.25:e.type==='brute'||e.type==='armored'?1.9:1.20;
        e.attackCharge=e.type==='boss'?.72:e.type==='brute'||e.type==='armored'?.65:e.type==='stalker'||e.type==='winged'?.39:.27;
        e.attackAnim=1;e.ai='attack';
        creatureSound(e.type==='armored'?'brute':e.type,e.x,e.z,true);
        vfx('spark',e.x,e.baseY+.6,e.z,.22,.32,0,.25,0,.48);
      }
    }
  }
  dead.forEach(function(e){ if(enemies.indexOf(e)>=0) killEnemy(e); });
  // orbs
  for(let i=orbs.length-1;i>=0;i--){
    const o=orbs[i];
    if(o.wraith){const dx=P.x-o.x,dz=P.z-o.z,len=Math.max(.001,Math.hypot(dx,dz));
      o.vx+=((dx/len)*6-o.vx)*Math.min(1,dt*1.2);o.vz+=((dz/len)*6-o.vz)*Math.min(1,dt*1.2);}
    o.x+=o.vx*dt; o.z+=o.vz*dt; o.life-=dt;
    o.mesh.position.set(o.x,1.4,o.z);
    let dead=o.life<=0||solid(o.x,o.z);
    if(!dead&&Math.hypot(o.x-P.x,o.z-P.z)<0.7){
      if(P.wi>=6&&keys.KeyC&&P.stamina>0){
        P.stamina=Math.max(0,P.stamina-4);
        const near=enemies.filter(e=>Math.hypot(e.x-P.x,e.z-P.z)<9).sort((a,b)=>Math.hypot(a.x-P.x,a.z-P.z)-Math.hypot(b.x-P.x,b.z-P.z))[0];
        if(near){near.hp-=parryWindow>0?12:5;near.hit=.3;if(near.hp<=0)killEnemy(near);}
        burst(o.x,1.4,o.z,0x8deaff,8,2);beep(1000,.14,'sawtooth',.12,-420);
      }else hurt(9+level);
      dead=true;
    }
    if(dead){ burst(o.x,1.4,o.z,0xd070ff,5,3); levelGroup.remove(o.mesh); orbs.splice(i,1); }
  }
  // Low-cost death pose (no geometry, materials or arrays allocated per frame).
  for(let i=fallenMonsters.length-1;i>=0;i--){
    const corpse=fallenMonsters[i];corpse.t+=dt;
    const k=Math.min(1,corpse.t/1.55);
    corpse.mesh.rotation.z=corpse.lean*Math.min(1,k*1.75)*1.21;
    corpse.mesh.rotation.x=Math.min(1,k*1.5)*.23;
    corpse.mesh.position.y=corpse.originY-k*.45;
    if(k>=1){levelGroup.remove(corpse.mesh);fallenMonsters.splice(i,1);}
  }
  // pickups
  for(let i=pickups.length-1;i>=0;i--){
    const p=pickups[i];
    p.mesh.rotation.y+=dt*1.25;p.mesh.position.y=.87+Math.sin(time*2.2+p.ph)*.11;
    const label=p.mesh.children[p.mesh.children.length-1];if(label&&label.isSprite)label.visible=Math.hypot(p.x-P.x,p.z-P.z)<5.5;
    if(p.type==='gem') p.mesh.children[2].rotation.z+=dt*3;
    if(Math.hypot(p.x-P.x,p.z-P.z)<1.1){
      if(p.type==='hp'){ if(P.hp>=P.maxhp) continue; P.hp=Math.min(P.maxhp,P.hp+30); toast('+30 HP',900); }
      else if(p.type==='ammo'){ const am=Math.round(25*(1+P.scav)); P.ammo+=am; toast('+'+am+' ammo',900); }
      else if(p.type==='key'){P.keys++;floorKeyCollected=true;toast('CRYPT KEY ACQUIRED · EXIT UNLOCKED WHEN GUARDIANS FALL',1800);unlockPortalIfReady();saveCampaign();}
      else { P.score+=50;P.coins+=12;toast('+12 SOUL COINS',700); }
      beep(900,0.1,'sine',0.05,300);
      levelGroup.remove(p.mesh); pickups.splice(i,1);
    }
  }
  // fx
  for(let i=fx.length-1;i>=0;i--){
    const f2=fx[i];
    if(f2.vfxLight){
      f2.t+=dt;f2.mesh.intensity=9*Math.pow(Math.max(0,1-f2.t/f2.dur),2);
      if(f2.t>=f2.dur){levelGroup.remove(f2.mesh);fx.splice(i,1);}continue;
    }
    if(f2.vfx){
      f2.t+=dt;const k=Math.min(1,f2.t/f2.dur),o=f2.mesh;
      o.position.x+=f2.vx*dt;o.position.y+=f2.vy*dt;o.position.z+=f2.vz*dt;
      o.position.x+=Math.sin(f2.phase+time*9)*dt*.11;
      const sc=f2.scale*(f2.kind==='smoke'?1+2.4*k:f2.kind==='fire'?1+.65*k:.65+.55*k);
      o.scale.set(sc,sc,1);
      o.material.rotation+=dt*(f2.kind==='smoke'?.2:1.1);
      o.material.opacity=f2.alpha*Math.pow(1-k,f2.kind==='smoke'?.88:1.65);
      if(f2.kind==='smoke')o.material.color.setRGB(.3-.12*k,.31-.13*k,.36-.15*k);
      if(k>=1){levelGroup.remove(o);const pool=VFX_POOL[f2.kind]||(VFX_POOL[f2.kind]=[]);if(pool.length<160)pool.push(o);else o.material.dispose();fx.splice(i,1);}continue;
    }
    if(f2.pr){
      f2.t+=dt; const k=Math.min(1,f2.t/f2.dur), mm=f2.mesh;
      if(f2.kind==='beam'){ mm.material.opacity=0.8*(1-k); }
      else if(f2.kind==='boom'){ const s=f2.r*Math.sqrt(k)+0.05; mm.scale.set(s,s*0.8,s); mm.material.opacity=0.9*(1-k); }
      else if(f2.kind==='ring'){ const s=f2.r*1.15*k+0.1; mm.scale.set(s,s,s); mm.material.opacity=0.9*(1-k); }
      else{
        mm.position.set(f2.x0+(f2.x1-f2.x0)*k,f2.y0+(f2.y1-f2.y0)*k+(f2.kind==='gren'?Math.sin(k*3.1416)*1.2:0),f2.z0+(f2.z1-f2.z0)*k);
        if(f2.kind==='flame'){
          const sc=.38+1.45*Math.sin(Math.PI*(k*.8+.1));mm.scale.set(sc,sc*1.17,1);
          mm.material.opacity=.93*Math.pow(1-k,1.35);
          mm.material.rotation+=dt*5.2;
          if(Math.random()<.12)vfx('smoke',mm.position.x,mm.position.y,mm.position.z,.25,.43,.12,.62,.12,.2);
        }
      }
      if(k>=1){ levelGroup.remove(mm); if(f2.kind==='flame')mm.material.dispose(); fx.splice(i,1); if(f2.done) f2.done(); }
      continue;
    }
    if(f2.severed){
      f2.life-=dt;
      f2.mesh.position.x+=f2.vx*dt;
      f2.mesh.position.z+=f2.vz*dt;
      f2.mesh.position.y+=f2.vy*dt;
      f2.vy-=12.8*dt;
      f2.mesh.rotation.x+=f2.spinX*dt;
      f2.mesh.rotation.y+=f2.spinY*dt;
      if(f2.mesh.position.y<.14){
        f2.mesh.position.y=.14;
        if(!f2.bounced){
          f2.vy=Math.abs(f2.vy)*.18;
          f2.vx*=.37;f2.vz*=.37;f2.bounced=true;
          burst(f2.mesh.position.x,.14,f2.mesh.position.z,0x682022,4,1.2);
        }else{f2.vy=0;f2.vx*=.82;f2.vz*=.82;}
      }
      if(f2.life<=0){levelGroup.remove(f2.mesh);fx.splice(i,1);}
      continue;
    }
    f2.life-=dt;
    if(!f2.line){ f2.mesh.position.x+=f2.vx*dt; f2.mesh.position.y+=f2.vy*dt; f2.mesh.position.z+=f2.vz*dt; f2.vy-=9*dt;
      if(f2.mesh.position.y<0.05){f2.mesh.position.y=0.05;f2.vy=0;f2.vx*=0.8;f2.vz*=0.8;} }
    if(f2.life<=0){ levelGroup.remove(f2.mesh); fx.splice(i,1); }
  }
  // portal
  updateAbyssalGateway(portal,dt,time,portalOpen,P.x,P.z);
  const pp=cellCenter(exitCell);
  if(portalOpen&&Math.hypot(pp[0]-P.x,pp[1]-P.z)<1.5){
    // Intentional interaction: E activates the transition, not an auto-trigger.
  } else if(!portalOpen&&Math.hypot(pp[0]-P.x,pp[1]-P.z)<1.8){
    toast(floorKeyNeeded&&!floorKeyCollected?'Find the crypt key':floorSwitchNeeded&&!floorSwitchOn?'Activate the rune switch (X)':currentBoss?'Defeat '+currentBoss.bossName:'Defeat '+Math.max(0,Math.ceil(totalEnemies*.5)-killsThisLevel)+' guardians',1200);
  }
  // explore
  const pcx=Math.floor(P.x/CELL), pcz=Math.floor(P.z/CELL);
  for(let y=pcz-3;y<=pcz+3;y++) for(let x=pcx-3;x<=pcx+3;x++)
    if(x>=0&&y>=0&&x<GW&&y<GH&&(x-pcx)*(x-pcx)+(y-pcz)*(y-pcz)<=10) explored[y*GW+x]=1;
}

function render(){
  const sh=P.shake; camera.position.set(P.x+(Math.random()-0.5)*sh*0.4,1.6+Math.sin(walkT*10)*0.045+(Math.random()-0.5)*sh*0.4,P.z+(Math.random()-0.5)*sh*0.4); P.shake*=0.9;
  camera.rotation.y=P.yaw;
  camera.rotation.x=P.pitch;
  flashlight.intensity=flashlightOn?.62:0;
  torch.position.set(P.x,2.0,P.z);
  torch.intensity=.95+Math.sin(time*13)*.08+Math.random()*.05+(muzzle>0?2:0)+boomT*3+heat*2.5;
  const mvg=walkT!==lastWalkT?1:0; lastWalkT=walkT; bobAmt+=(mvg-bobAmt)*0.15;
  const melee=P.wi>=6,progress=bladeSwing?Math.min(1,bladeElapsed/Math.max(.1,bladeDuration)):0;
  if(P.wi===6){
    const swing=pendingMelee, side=swing?swing.side:1, style=swing?swing.style:'horizontal';
    const smooth=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t);};
    const p=progress;
    const wind=smooth(p/.25),cut=smooth((p-.25)/.46),recover=smooth((p-.71)/.29);
    // Small procedural offsets are applied to one shared pivot. The anatomically
    // modeled fist is a fixed child of that pivot and cannot slide off the hilt.
    const configs={
      horizontal:{wind:[.12,.065,.06,.15,side*.58,-side*.45],end:[-.15,-.04,-.18,-.23,-side*.85,side*.49]},
      diagonal:{wind:[.10,.13,.065,.23,side*.52,-side*.62],end:[-.14,-.10,-.17,-.57,-side*.74,side*.66]},
      heavy:{wind:[.02,.18,.09,.52,side*.13,-side*.17],end:[-.025,-.12,-.20,-.65,-side*.19,side*.12]},
      thrust:{wind:[.03,-.025,.10,-.07,side*.12,-side*.08],end:[-.12,.012,-.30,-.08,-side*.13,side*.07]}
    };
    const cfg=configs[style]||configs.horizontal;
    const pose=cfg.wind.map((v,i)=>{
      const end=cfg.end[i];
      const active=wind*(1-cut)*v+cut*(1-recover)*end;
      return active;
    });
    const sprint=(keys.ShiftLeft||keys.ShiftRight)?1.3:1;
    const sway=Math.sin(walkT*4.2)*.009*bobAmt*sprint;
    const bob=Math.abs(Math.sin(walkT*8.4))*.012*bobAmt*sprint;
    // Lower-right idle stance: slender blade reaches toward the screen center.
    gun.position.set(.35+sway+pose[0]*.56,-.36+bob+Math.sin(time*1.25)*.003+pose[1]*.62,-.91+pose[2]*.48);
    gun.rotation.set(.05+pose[3]*.26,.015+pose[4]*.26,-.035+pose[5]*.24);
    const model=gunModels[6];
    model.position.set(.065+pose[0]*.48,-.012+pose[1]*.55,.015+pose[2]*.62);
    model.rotation.set(.11+pose[3]*.85,.37+pose[4]*.92,-.10+pose[5]*.92);
    const fist=model.userData.handRigs[0];
    if(fist){fist.position.copy(fist.userData.restPosition);fist.rotation.set(0,0,0);}
    // The energy saber is primarily one-handed; off-hand grips only for heavy attacks/guard.
    const offHand=model.userData.handRigs[1];
    if(offHand){const supportActive=!!(keys.KeyC||(pendingMelee&&pendingMelee.style==='heavy'&&bladeSwing>0));offHand.visible=supportActive;
      if(supportActive){offHand.position.set(offHand.userData.restPosition.x+.32,offHand.userData.restPosition.y+.19,offHand.userData.restPosition.z-.22);}
      else offHand.position.copy(offHand.userData.restPosition);}
    if(keys.KeyC&&!bladeSwing&&P.stamina>0){
      model.position.x-=.11;model.position.y+=.14;model.position.z-=.05;
      model.rotation.set(.63,-.15,.45);
      gun.position.x-=.05;gun.position.y+=.045;
    }
  }else if(P.wi===7){
    // Light Saber has a dedicated lower-right ready stance, not the old melee
    // pivot that threw the blade across the entire screen. The single hand is
    // attached directly to the saber's handle and never slides relative to it.
    const swing=pendingMelee,side=swing?swing.side:1,style=swing?swing.style:'horizontal';
    const smooth=v=>{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v);};
    const wind=smooth(progress/.24),cut=smooth((progress-.24)/.48),recovery=smooth((progress-.72)/.28);
    const arcs={
      horizontal:{wind:[.08,.06,.04,.12,side*.49,-side*.32],end:[-.11,-.04,-.14,-.18,-side*.72,side*.42]},
      diagonal:{wind:[.08,.09,.05,.20,side*.47,-side*.40],end:[-.12,-.08,-.16,-.44,-side*.75,side*.53]},
      heavy:{wind:[.02,.14,.09,.36,side*.10,-side*.13],end:[-.02,-.11,-.18,-.61,-side*.19,side*.12]},
      thrust:{wind:[.02,-.02,.08,-.05,side*.08,-side*.05],end:[-.09,.01,-.29,-.10,-side*.10,side*.05]}
    };
    const cfg=arcs[style]||arcs.horizontal;
    const pose=cfg.wind.map((v,i)=>wind*(1-cut)*v+cut*(1-recovery)*cfg.end[i]);
    const sprint=(keys.ShiftLeft||keys.ShiftRight)?1.3:1;
    const sway=Math.sin(walkT*4.2)*.009*bobAmt*sprint;
    const bob=Math.abs(Math.sin(walkT*8.4))*.010*bobAmt*sprint;
    gun.position.set(.35+sway+pose[0]*.52,-.36+bob+Math.sin(time*1.2)*.003+pose[1]*.55,-.91+pose[2]*.51);
    gun.rotation.set(.045+pose[3]*.22,.015+pose[4]*.23,-.03+pose[5]*.22);
    const model=gunModels[7];
    model.position.set(.07+pose[0]*.43,-.01+pose[1]*.48,.02+pose[2]*.55);
    model.rotation.set(.13+pose[3]*.82,.28+pose[4]*.91,-.10+pose[5]*.89);
    const fist=model.userData.handRigs[0];
    if(fist){fist.position.copy(fist.userData.restPosition);fist.rotation.set(0,0,0);}
    if(keys.KeyC&&!bladeSwing&&P.stamina>0){
      model.position.x-=.10;model.position.y+=.12;model.position.z-=.04;
      model.rotation.set(.57,-.14,.38);
      gun.position.x-=.045;gun.position.y+=.045;
    }
  }else if(melee){
    // Defensive fallback, should not execute for the eight normal slots.
    gun.position.set(.35,-.36,-.91);
    gun.rotation.set(0,0,0);
  }else{
    gun.position.set(.37+Math.sin(walkT*5)*.022*bobAmt,-.37+Math.abs(Math.sin(walkT*10))*.018*bobAmt+Math.sin(time*1.6)*.004,-.66+recoil+(P.reloadT>0&&P.reloadWi===P.wi?.13*Math.sin(Math.PI*P.reloadT/WEAPONS[P.wi].reload):0));
    gun.rotation.set(recoil*.65,-.12+Math.sin(walkT*5)*.014*bobAmt,-recoil*.28);
    const model=gunModels[P.wi];
    const longGun=P.wi>0&&P.wi!==6&&P.wi!==7;
    for(const [hi,h] of (model.userData.handRigs||[]).entries()){
      const rest=h.userData.restRotation,restP=h.userData.restPosition,curl=h.userData.baseCurl||1.26;
      const sway=Math.sin(walkT*8+hi*.55)*.013*bobAmt;
      h.rotation.x=rest.x+sway+recoil*(hi===0?-.42:(longGun?-.10:-.22));
      h.rotation.y=rest.y+Math.cos(walkT*4+hi)*.006*bobAmt+recoil*(hi===0?.02:-.01);
      h.rotation.z=rest.z+recoil*(hi===0?.08:(longGun?-.02:-.05));
      h.position.set(restP.x,restP.y+Math.abs(Math.sin(walkT*8+hi))*.004*bobAmt,restP.z+recoil*(hi===0?.012:.004));
      for(const finger of h.userData.fingers){
        const effectiveCurl=curl+recoil*(hi===0?.30:.10);
        finger.rotation.x+=(effectiveCurl*.32-finger.rotation.x)*.18;
        const joints=finger.userData.phalanges;
        if(joints)for(let j=1;j<joints.length;j++)joints[j].rotation.x+=((j===1?.33:.35)*effectiveCurl-joints[j].rotation.x)*.18;
      }
    }
  }
  animateSlash(progress,P.wi,(pendingMelee&&pendingMelee.side)||1,(pendingMelee&&pendingMelee.style)||'horizontal');
  updateGameAudio();
  const kk=Math.min(1,recoil/KICK[P.wi]), Ud=gunModels[P.wi].userData;
  if(Ud.slide) Ud.slide.position.z=(Ud.slideBaseZ||0)+kk*0.085;
  if(Ud.pump) Ud.pump.position.z=(Ud.pumpBaseZ||0)+Math.sin(kk*Math.PI)*0.18;
  if(Ud.bolt) Ud.bolt.position.z=(Ud.boltBaseZ||0)+kk*0.11;
  mflash.visible=muzzle>0 && P.wi<5;
  flameNozzle.visible=(P.wi===5&&muzzle>0);
  if(flameNozzle.visible){const z=.76+Math.random()*.35;flameNozzle.scale.set(z,z*1.8,1);flameNozzle.material.rotation=Math.sin(time*16)*.17;}
  const mp=Ud.muzzle||{x:0,y:0,z:-.8};mflash.position.set(mp.x,mp.y,mp.z);
  const fs=0.33+Math.random()*0.2; mflash.scale.set(fs,fs,1);
  flashA=Math.max(0,flashA-0.02);
  flash.style.opacity=flashA;
  for(const s of flames){ const k=2.2+Math.sin(time*9+s.position.x*3)*0.25; s.scale.set(k,k,1); }
  renderer.autoClear=true;
  renderer.render(scene,camera);
  renderer.autoClear=false;
  if(renderer.clearDepth)renderer.clearDepth();
  renderer.render(viewScene,viewCamera);
  renderer.autoClear=true;
  bossHud.style.display=currentBoss&&state==='playing'&&currentBoss.hp>0?'block':'none';
  if(currentBoss&&currentBoss.hp>0){bossHud.querySelector('#boss-v5-name').textContent=currentBoss.bossName+' · PHASE '+currentBoss.bossPhase;
    bossHud.querySelector('#boss-v5-meter').style.width=Math.max(0,100*currentBoss.hp/currentBoss.maxhp).toFixed(1)+'%';}
  if(state==='playing'&&!paused&&portal){
    const dx=P.x-portal.position.x,dz=P.z-portal.position.z,near=Math.hypot(dx,dz)<2.5;
    portalPrompt.style.display=near?'block':'none';
    if(near){
      if(portalOpen)portalPrompt.textContent=portal.userData.phase<.99?'PORTAL ACTIVATING':'E  ENTER THE PORTAL';
      else {
       const remaining=Math.max(0,Math.ceil(totalEnemies*.5)-killsThisLevel);
       portalPrompt.textContent='SEALED · '+remaining+' GUARDIANS REMAIN'+(floorKeyNeeded&&!floorKeyCollected?' · KEY REQUIRED':'')+(floorSwitchNeeded&&!floorSwitchOn?' · RUNE REQUIRED':'');
      }
    }
  }else portalPrompt.style.display='none';
  // HUD
  const cpOn=checkpoints.filter(function(c){ return c.on; }).length;
  hud.innerHTML='<div class="tiny" style="color:#e7c497">'+currentTheme.name.toUpperCase()+'</div><div class="tiny" style="margin-top:2px">'+(level%5===0?'Warning BOSS ENCOUNTER':'SECTOR · DEEP '+String(level).padStart(2,'0'))+'</div>'+
    '<div class="big">'+P.score+' <span class="muted">/ BEST '+Math.max(best,P.score)+'</span></div>'+
    '<div class="muted" style="margin-top:4px">Kills '+killsThisLevel+' / '+totalEnemies+' ELIMINATED ·  '+cpOn+' / '+checkpoints.length+' SHRINES</div>'+
    '<div class="tiny" style="margin-top:5px;color:'+(portalOpen?'#8ff9d2':'#ffad91')+'">'+(portalOpen?'◇ EXIT PORTAL ACTIVE':'◇ PORTAL SEALED')+'</div>'+
    '<div class="tiny" style="margin-top:4px;color:#c3d9d5">OBJECTIVE · '+activeObjective+'</div>'+ 
    '<div class="tiny" style="margin-top:3px;color:#ffe8b0">Coins '+P.coins+' · Armor '+Math.ceil(P.armor)+' · Stamina '+Math.ceil(P.stamina)+' · Key '+P.keys+'</div>'+ 
    (P.combo>=2?'<div class="tiny" style="color:#ffd593">COMBO × '+P.combo+'</div>':'');
  hpLbl.textContent='+ VITALS  '+Math.ceil(P.hp)+' / '+P.maxhp;
  const hbHtml='<div class="loadout-keys compact">'+WEAPONS.map(function(w,i){return '<span title="'+w.n+'" class="loadout-key'+(i===P.wi?' current':'')+'">'+(i+1)+'</span>';}).join('')+'</div>';
  if(hbHtml!==hbLast){hotbar.innerHTML=hbHtml;hbLast=hbHtml;}
  hotbar.style.setProperty('--hotbar-opacity',performance.now()-lastWeaponSelect<2200?'0.9':'0');
  const w0=WEAPONS[P.wi], amHtml='<div style="font-size:10px;opacity:.7;letter-spacing:1px">'+w0.ico+' '+w0.n.toUpperCase()+'</div><div style="font-size:25px;font-weight:800;color:'+(P.wi<6&&magazines[P.wi]<3?'#ff8a83':'#ffd990')+'">'+(w0.melee?'UNLIM':magazines[P.wi]+' <span style="font-size:12px;color:#a9a9a9">/ '+P.ammo+'</span>')+'</div><div style="font-size:10px;opacity:.7">'+(P.wi===6?'G HEAVY · T THRUST · C GUARD':w0.melee?'MELEE · NO AMMO':P.reloadT>0?'RELOADING… (R)':P.wi===3?'B · '+rifleMode:'R · RELOAD')+'</div>';
  if(amHtml!==amLast){ ammoBox.innerHTML=amHtml; amLast=amHtml; }
  // Crosshair expands for recoil / movement and confirms actual hits.
  crosshair.style.transform='scale('+(1+Math.min(.8,recoil*3.1)+Math.min(.26,bobAmt*.08)).toFixed(2)+')';
  crosshair.style.opacity=state==='playing'?'1':'0';
  hm.style.opacity=hitT; hitT*=0.82; ht.style.opacity=heat; heat*=0.93; boomT*=0.9;
  hpb.style.width=(100*P.hp/P.maxhp)+'%';
  hpb.style.background=P.hp<30?'#e0455a':'#3ddc84';
  // minimap: pixel-doubled canvas, throttled to ~30 fps.
  if(time-lastMapDraw>=1/30){lastMapDraw=time;
  const s=130/GW*mapZoom;
  mctx.clearRect(0,0,130,130);mctx.save();
  const mapPX=P.x/CELL*s,mapPZ=P.z/CELL*s;
  mctx.translate(65,65);if(mapRotate)mctx.rotate(P.yaw);mctx.translate(-mapPX,-mapPZ);
  for(let y=0;y<GH;y++) for(let x=0;x<GW;x++){
    if(!explored[y*GW+x]) continue;
    mctx.fillStyle=grid[y][x]===1?'#6a6f8c':'#2b2f44';
    mctx.fillRect(x*s-.1,y*s-.1,s+.2,s+.2);
  }
  if(explored[exitCell[1]*GW+exitCell[0]]){
    mctx.fillStyle=portalOpen?'#33e0ff':'#ff5566';
    mctx.beginPath();mctx.arc((exitCell[0]+.5)*s,(exitCell[1]+.5)*s,2.7+Math.sin(time*5)*.65,0,Math.PI*2);mctx.fill();
  }
  for(const c of checkpoints){ if(explored[Math.floor(c.z/CELL)*GW+Math.floor(c.x/CELL)]){ mctx.fillStyle=c.on?'#33ff99':'#8899aa'; mctx.fillRect(c.x/CELL*s-2,c.z/CELL*s-2,4,4); } }
  for(const a of runicSwitches){const gx=Math.floor(a.x/CELL),gz=Math.floor(a.z/CELL);if(explored[gz*GW+gx]){mctx.fillStyle=a.on?'#72eca0':'#e7bd59';mctx.fillRect(a.x/CELL*s-2,a.z/CELL*s-2,4,4);}}
  for(const p of pickups){if(p.type==='key'){const gx=Math.floor(p.x/CELL),gz=Math.floor(p.z/CELL);if(explored[gz*GW+gx]){mctx.fillStyle='#f5d462';mctx.fillRect(p.x/CELL*s-2,p.z/CELL*s-2,4,4);}}}
  mctx.fillStyle='#ff4040';
  for(const e of enemies){
    if(Math.hypot(e.x-P.x,e.z-P.z)<16){ mctx.fillRect(e.x/CELL*s-1.5,e.z/CELL*s-1.5,3,3); }
  }
  const px=P.x/CELL*s, pz=P.z/CELL*s;
  mctx.fillStyle='#ffe066'; mctx.beginPath(); mctx.arc(px,pz,2.6,0,6.3); mctx.fill();
  // Facing arrow and FOV wedge make navigation legible at compact size.
  mctx.fillStyle='rgba(249,220,112,.09)';mctx.beginPath();mctx.moveTo(px,pz);
  mctx.arc(px,pz,20,-Math.PI/2-P.yaw-.36,-Math.PI/2-P.yaw+.36);mctx.closePath();mctx.fill();
  mctx.fillStyle='#ffe066';mctx.beginPath();mctx.moveTo(px-Math.sin(P.yaw)*8,pz-Math.cos(P.yaw)*8);
  mctx.lineTo(px+Math.cos(P.yaw)*4,pz-Math.sin(P.yaw)*4);
  mctx.lineTo(px-Math.cos(P.yaw)*4,pz+Math.sin(P.yaw)*4);mctx.closePath();mctx.fill();
  mctx.restore();
  mctx.fillStyle='rgba(7,11,18,.85)';mctx.fillRect(0,117,130,13);
  mctx.fillStyle='#d5dce7';mctx.font='8px sans-serif';mctx.fillText((mapRotate?'ROTATING':'NORTH UP')+' · '+mapZoom.toFixed(1)+'x',5,126);
  }
}


// ---------- ABYSSAL V5: inventory, in-run shop and validated campaign persistence ----------
const CAMPAIGN_KEY='depths3d_v5_save';
function clampNum(v,a,b,def){return typeof v==='number'&&Number.isFinite(v)?Math.max(a,Math.min(b,v)):def;}
function savedRun(){
 try{
   const obj=JSON.parse(localStorage.getItem(CAMPAIGN_KEY)||'null');
   if(!obj||obj.schema!==5||!obj.player||!Array.isArray(obj.mags)||!Array.isArray(obj.levels)||!Number.isInteger(obj.level)||obj.level<1||obj.level>30)return null;
   return obj;
 }catch(e){return null;}
}
function saveCampaign(){
  try{
    const player={};for(const k of ['hp','maxhp','armor','ammo','score','kills','dmgm','rate','leech','scav','spd','coins','keys','potions','stamina','maxStamina','energy','x','z','yaw','pitch','wi'])player[k]=Number.isFinite(P[k])?P[k]:0;
    const obj={schema:5,equipment:{...EQUIPMENT},relics:{...RELICS},level,seed:campaignSeed,mode,difficulty,player,mags:magazines.slice(),levels:WEAPON_LEVELS.slice(),tech:Object.fromEntries(Object.entries(GUN_TECH).map(([k,v])=>[k,v.slice()])),mastery:MASTERY.slice(),floorKeyCollected,floorSwitchOn,checkpoint:lastCP,at:Date.now()};
    localStorage.setItem(CAMPAIGN_KEY,JSON.stringify(obj));
    toast('CAMPAIGN SAVED',1000);return true;
  }catch(e){toast('SAVE UNAVAILABLE IN THIS BROWSER',1400);return false;}
}
function continueCampaign(){
  const data=savedRun();if(!data){toast('NO VALID CAMPAIGN SAVE',1700);return false;}
  applyingSave=true;
  try{
    level=data.level;
    campaignSeed=clampNum(data.seed,1,2147483647,77711);
    mode=['Normal','Hardcore','Daily','Survival','New Game+'].includes(data.mode)?data.mode:'Normal';
    difficulty=['Easy','Normal','Hard'].includes(data.difficulty)?data.difficulty:'Normal';
    buildLevel();
    for(const key of ['hp','maxhp','armor','ammo','score','kills','coins','keys','potions','stamina','maxStamina','energy']){
      P[key]=clampNum(data.player[key],0,key==='score'||key==='kills'?99999999:999999, P[key]);
    }
    for(const key of ['dmgm','rate','leech','scav','spd'])P[key]=clampNum(data.player[key],0,20,P[key]);
    P.hp=Math.min(P.maxhp,P.hp);
    P.x=clampNum(data.player.x,0,GW*CELL,P.x);P.z=clampNum(data.player.z,0,GH*CELL,P.z);
    if(blocked(P.x,P.z,P.r)){const c=cellCenter([1,1]);P.x=c[0];P.z=c[1];}
    P.yaw=clampNum(data.player.yaw,-100,100,P.yaw);P.pitch=clampNum(data.player.pitch,-.88,.88,0);
    P.inv=1.8;P.cool=0;P.reloadT=0;P.reloadWi=-1;
    for(const k of Object.keys(GUN_TECH))for(let i=0;i<6;i++)GUN_TECH[k][i]=Math.round(clampNum(data.tech&&data.tech[k]&&data.tech[k][i],0,5,0));
    applyGunTech();
    for(let i=0;i<6;i++)magazines[i]=Math.round(clampNum(data.mags[i],0,MAG_CAP[i],MAG_CAP[i]));
    for(let i=0;i<8;i++){WEAPON_LEVELS[i]=Math.round(clampNum(data.levels[i],0,5,0));MASTERY[i]=clampNum((data.mastery||[])[i],0,1000000,0);}
    // Schema 5 remains backward-compatible with v5.0.0 saves: missing new fields use defaults.
    for(const k of Object.keys(EQUIPMENT))EQUIPMENT[k]=Math.round(clampNum(data.equipment&&data.equipment[k],0,3,0));
    for(const k of Object.keys(RELICS))RELICS[k]=data.relics&&data.relics[k]===true;

    floorKeyCollected=!!data.floorKeyCollected;floorSwitchOn=!!data.floorSwitchOn;if(floorSwitchOn){runicSwitches.forEach(r=>{r.on=true;r.rune.material.color.set(0x91ffac);});}if(floorKeyCollected){P.keys=Math.max(1,P.keys);for(const item of pickups.slice())if(item.type==='key'){
      levelGroup.remove(item.mesh);pickups.splice(pickups.indexOf(item),1);
    }}
    if(data.checkpoint&&Number.isFinite(data.checkpoint.x)&&Number.isFinite(data.checkpoint.z)&&!blocked(data.checkpoint.x,data.checkpoint.z,P.r))lastCP={x:data.checkpoint.x,z:data.checkpoint.z};
    unlockPortalIfReady();
    setWeapon(Math.round(clampNum(data.player.wi,0,7,0)));
    state='playing';paused=false;hideOverlay();wrap.focus();toast('CAMPAIGN RESTORED · FLOOR '+level,1800);return true;
  }catch(e){toast('SAVE CORRUPTED · START NEW GAME',2300);return false;}
  finally{applyingSave=false;}
}
function deleteCampaign(){
 try{localStorage.removeItem(CAMPAIGN_KEY);toast('SAVED CAMPAIGN CLEARED',1200);}catch(e){toast('STORAGE UNAVAILABLE',1200);}
}
function buyUpgrade(item){
  const prices={medkit:35,armor:60,health:90,stamina:80,weapon:65+45*WEAPON_LEVELS[P.wi]};
  for(const k of Object.keys(ARMOUR_DATA))prices['equip_'+k]=ARMOUR_DATA[k].price*(1+EQUIPMENT[k]);
  for(const k of Object.keys(RELIC_DATA))prices['relic_'+k]=RELIC_DATA[k].price;
  for(const k of Object.keys(GUN_TECH))prices[k]=50+25*GUN_TECH[k][Math.min(P.wi,5)];
  const price=prices[item];if(price===undefined)return false;
  if(P.coins<price){toast('NOT ENOUGH SOUL COINS · '+price+' REQUIRED',1400);return false;}
  if(item.startsWith('equip_')&&EQUIPMENT[item.slice(6)]>=3){toast('ARMOUR AT MAXIMUM LEVEL',950);return false;}
  if(item.startsWith('relic_')&&RELICS[item.slice(6)]){toast('RELIC ALREADY EQUIPPED',950);return false;}
  if(item==='weapon'&&WEAPON_LEVELS[P.wi]>=5){toast('WEAPON AT MAXIMUM LEVEL',900);return false;}
  if(GUN_TECH[item]&&(P.wi>=6||GUN_TECH[item][P.wi]>=5)){toast('GUN TECH UNAVAILABLE OR MAXED',900);return false;}
  P.coins-=price;
  if(item==='medkit')P.potions++;
  else if(item==='armor')P.armor=Math.min(150,P.armor+35);
  else if(item==='health'){P.maxhp+=20;P.hp=Math.min(P.maxhp,P.hp+20);}
  else if(item==='stamina'){P.maxStamina+=20;P.stamina=P.maxStamina;}
  else if(item==='weapon')WEAPON_LEVELS[P.wi]++;
  else if(item.startsWith('equip_'))EQUIPMENT[item.slice(6)]++;
  else if(item.startsWith('relic_'))RELICS[item.slice(6)]=true;
  else if(GUN_TECH[item]){
    const previous=MAG_CAP[P.wi];GUN_TECH[item][P.wi]++;applyGunTech();
    if(item==='capacity')magazines[P.wi]+=MAG_CAP[P.wi]-previous;
  }
  beep(710,.13,'triangle',.04,130);saveCampaign();return true;
}
function drinkPotion(){
  if(P.potions<=0){toast('NO MEDKITS',900);return false;}
  if(P.hp>=P.maxhp){toast('HEALTH ALREADY FULL',900);return false;}
  P.potions--;P.hp=Math.min(P.maxhp,P.hp+45);beep(920,.2,'sine',.05,-320);
  toast('MEDKIT · +45 HEALTH',900);return true;
}
function inventoryPanel(){
  let markup='<div class="cin-label">FIELD INVENTORY / FLOOR '+level+'</div><h2>EXPEDITION SUPPLIES</h2>';
  markup+='<div class="cin-note">Coins Soul coins '+P.coins+' · Key Crypt keys '+P.keys+' · Medkit Medkits '+P.potions+'</div>';
  markup+='<div class="cin-note">+ Health '+Math.ceil(P.hp)+'/'+P.maxhp+' · Armor Armor '+Math.ceil(P.armor)+' · Stamina Stamina '+Math.ceil(P.stamina)+'/'+P.maxStamina+'</div>';
  markup+='<div class="cin-label">ARMOUR · '+Math.round(armourReduction()*100)+'% DAMAGE REDUCTION</div>';
  markup+='<div class="cin-note">'+Object.keys(EQUIPMENT).map(k=>ARMOUR_DATA[k].name+' '+EQUIPMENT[k]+'/3').join(' · ')+'</div>';
  markup+='<div class="cin-label">RELICS</div><div class="cin-note">'+(Object.keys(RELICS).filter(k=>RELICS[k]).map(k=>RELIC_DATA[k].name).join(' · ')||'None equipped')+'</div>';
  markup+='<div class="cin-label">EQUIPMENT & MASTERY</div><div style="font-size:11px;line-height:1.75;max-height:120px;overflow:auto">';
  WEAPONS.forEach((w,i)=>markup+='<div style="border-bottom:1px solid #ffffff20">'+(i===P.wi?'◇ ':'· ')+w.n+' · LV '+WEAPON_LEVELS[i]+' · MASTERY '+masteryTier(i)+'/5 · XP '+Math.floor(MASTERY[i])+(i<6?' · '+magazines[i]+'/'+MAG_CAP[i]:'')+'</div>');
  markup+='</div><div class="cin-label">GUN TECH · '+(P.wi<6?Object.keys(GUN_TECH).map(k=>k.toUpperCase()+' '+GUN_TECH[k][P.wi]).join(' · '):'MELEE')+'</div><div class="cin-actions">'+action('usepotion','+ USE MEDKIT (H)','cin-secondary')+action('savecampaign','SAVE CAMPAIGN','cin-secondary')+'</div>';
  markup+='<div class="cin-actions">'+action('resume','PLAY BACK TO DUNGEON','cin-play')+'</div>';return markup;
}
function shopPanel(){
  const buttons=[['medkit','MEDKIT · 35 COINS'],['armor','ARMOR +35 · 60 COINS'],['health','MAX HP +20 · 90 COINS'],['stamina','MAX STAMINA +20 · 80 COINS'],['weapon','WEAPON DAMAGE +9% · '+(65+45*WEAPON_LEVELS[P.wi])+' COINS']];
  for(const k of Object.keys(ARMOUR_DATA)){
    const a=ARMOUR_DATA[k],tier=EQUIPMENT[k];buttons.push(['equip_'+k,a.name.toUpperCase()+' '+(tier>=3?'MAX':'LV '+tier+' · '+a.price*(tier+1)+' COINS')]);
  }
  for(const k of Object.keys(RELIC_DATA)){
    const r=RELIC_DATA[k];buttons.push(['relic_'+k,r.name.toUpperCase()+' · '+(RELICS[k]?'EQUIPPED':r.price+' COINS')]);
  }
  if(P.wi<6){
    for(const [k,t] of [['capacity','MAG CAPACITY'],['reload','RELOAD SPEED'],['accuracy','ACCURACY'],['recoil','RECOIL CONTROL'],['velocity','BULLET VELOCITY']]){
      const lvl=GUN_TECH[k][P.wi];buttons.push([k,t+' '+(lvl>=5?'MAX':'LV '+lvl+' · '+(50+25*lvl)+' COINS')]);
    }
  }
  return '<div class="cin-label">SOUL FORGE · '+P.coins+' COINS</div><div class="cin-opts" style="display:flex;flex-wrap:wrap;gap:5px">'+buttons.map(([k,t])=>action('buy:'+k,t,'cin-choice')).join('')+'</div>';
}

function shopPanelV52(category,page){
 const all=[];
 const add=(type,title,cost,desc)=>all.push({type,title,cost,desc});
 if(category==='Survival'){
  add('medkit','Medical supplies',35,'Restore health');add('health','Vitality',90,'Max health +20');add('stamina','Endurance',80,'Max stamina +20');
 }else if(category==='Offense'){
  add('weapon','Weapon damage',65+45*WEAPON_LEVELS[P.wi],'Damage +9%');add('armor','Armour restoration',60,'Restore 35 armour');
 }else if(category==='Armor'){
  for(const k of Object.keys(ARMOUR_DATA)){const a=ARMOUR_DATA[k],tier=EQUIPMENT[k];add('equip_'+k,a.name,tier>=3?-1:a.price*(tier+1),'Tier '+tier+' / 3');}
 }else if(category==='Weapon Tuning'){
  if(P.wi<6)for(const [k,t] of [['capacity','Magazine'],['reload','Reload speed'],['accuracy','Precision'],['recoil','Recoil control'],['velocity','Projectile velocity']]){
   const lvl=GUN_TECH[k][P.wi];add(k,t,lvl>=5?-1:50+25*lvl,'Tier '+lvl+' / 5');
  } else add('weapon','Melee sharpening',65+45*WEAPON_LEVELS[P.wi],'Improve current melee weapon');
 }else{
  for(const k of Object.keys(RELIC_DATA)){const r=RELIC_DATA[k];add('relic_'+k,r.name,RELICS[k]?-1:r.price,RELICS[k]?'Equipped':'Unique relic bonus');}
 }
 const start=page*6,arr=all.slice(start,start+6);
 const cards=arr.map(i=>'<div class="forge-card"><b>'+i.title+'</b><small>'+i.desc+'</small><div class="forge-cost">'+(i.cost<0?'MAXED':i.cost+' COINS')+'</div>'+action('buy:'+i.type,i.cost<0?'Owned / Maxed':i.cost>P.coins?'Not enough coins':'Purchase','forge-buy')+'</div>').join('');
 return cards+(all.length>6?'<div class="forge-pager">'+action('forgepage:-1','Previous')+' Page '+(page+1)+' / '+Math.ceil(all.length/6)+' '+action('forgepage:1','Next')+'</div>':'');
}
// ---------- v5.1 Minimal menu system / one task per page ----------
function hideOverlay(){ov.style.display='none';if(launchTimeout){clearTimeout(launchTimeout);launchTimeout=null;}}
function action(a,label,cls='cin-choice',sel=false){
 return '<button type="button" class="d3h '+cls+(sel?' selected':'')+'" data-a="'+a+'">'+label+'</button>';
}
function item(a,label,primary=false,detail=''){
 return action(a,'<span>'+label+(detail?'<small class="ux-caption">'+detail+'</small>':'')+'</span><span class="ux-arrow" aria-hidden="true">›</span>','ux-item'+(primary?' ux-primary':''));
}
function back(a,label='Back'){return action(a,'‹ &nbsp;'+label,'ux-back');}
function rowSetting(label,key,value){
 return '<div class="ux-setting"><span>'+label+'</span><span class="ux-setting-controls">'+action('set:'+key+':-1','−','ux-step')+
 '<b class="ux-value">'+value+'</b>'+action('set:'+key+':1','+','ux-step')+'</span></div>';
}
let launchTimeout=null,settingsReturn='main',forgeStage=0,forgeCategory='Survival',forgePage=0,forgeChosen=false;
function showLaunchStage(kind){
 menuKind=kind;
 if(launchTimeout){clearTimeout(launchTimeout);launchTimeout=null;}
 ov.style.display='flex';ov.style.justifyContent='center';ov.style.overflow='hidden';ov.style.overflowY='hidden';
 const pic=kind==='intro'?ART_INTRO:ART_MENU;
 let inner='';
 if(kind==='intro'){
   inner='<div class="launch-kicker">A DARK-FANTASY DESCENT</div><div class="launch-logo">DEPTHS <em>3D</em></div>'+
     '<div class="launch-kicker">THE ABYSS IS CALLING</div><div class="launch-progress"><i></i></div>'+
     '<div style="margin-top:23px">'+action('skipintro','SKIP INTRO','ux-option')+'</div>';
 }else if(kind==='title'){
   inner='<div class="launch-kicker">THE BESTIARY EXPANSION</div><div class="launch-logo">DEPTHS <em>3D</em></div>'+
     '<div class="launch-kicker" style="font-weight:450;letter-spacing:1.2px;margin-top:12px">Every descent is different.</div>'+
     action('begin','CLICK TO START','launch-button')+
     (savedRun()?'<div style="margin-top:15px">'+action('continue','Continue saved expedition','ux-back')+'</div>':'')+
     '<div style="margin-top:7px">'+action('view:settings','Settings','ux-back')+'</div>';
 }else{
   inner='<div class="launch-kicker">BEFORE THE DESCENT</div><div class="launch-logo" style="font-size:clamp(32px,5.4vw,52px)">CHOOSE <em>DIFFICULTY</em></div>'+
     '<div class="launch-diff">'+
       action('diffflow:Easy','<span>EXPLORER</span><small>A gentler descent</small>','ux-option')+
       action('diffflow:Normal','<span>VETERAN</span><small>Balanced survival</small>','ux-option')+
       action('diffflow:Hard','<span>NIGHTMARE</span><small>Unforgiving encounters</small>','ux-option')+'</div>'+
     '<div style="margin-top:10px">'+action('back:title','‹ Back','ux-back')+'</div>';
 }
 ov.innerHTML='<div class="cin-launch" style="background-image:url('+pic+')">'+inner+'</div>';
 if(kind==='intro')launchTimeout=setTimeout(()=>{if(menuKind==='intro')showMenu('title');},4300);
}
function settingsOptions(){
 return '<div class="ux-menu">'+
   item('settingspage:audio','Audio')+
   item('settingspage:visual','Display')+
   item('settingspage:controls','Controls')+
   item('settingspage:game','Gameplay')+
   item('settingspage:save','Saved data')+'</div>';
}
function panelHeader(label,title,subtitle='',backAction='back:main'){
 return back(backAction)+'<div class="ux-eyebrow">'+label+'</div><h1 class="ux-heading">'+title+'</h1>'+
   (subtitle?'<p class="ux-sub">'+subtitle+'</p>':'');
}
function showMenu(kind){
 if(kind==='intro'||kind==='title'||kind==='difficulty'){showLaunchStage(kind);return;}
 menuKind=kind;
 try{if(document.exitPointerLock&&document.pointerLockElement)document.exitPointerLock();}catch(e){}
 ov.style.background='#080e18';ov.style.justifyContent='center';ov.style.overflow='hidden';ov.style.overflowY='hidden';
 let page='';
 const settingsBack='back:settings';
 if(kind==='main'){
   page='<div class="ux-eyebrow">The Bestiary Expansion</div><h1 class="ux-heading">DEPTHS 3D</h1>'+
     '<p class="ux-sub">Enter the darkness. Make every shot count.</p><div class="ux-menu">'+
     item('startnew','New expedition',true)+(savedRun()?item('continue','Continue expedition'):'')+
     item('view:loadout','Loadout',false,WEAPONS[startW].n)+
     item('view:settings','Settings')+item('view:records','Records')+'</div>'+
     '<div class="ux-metadata"><span class="ux-meta-accent">'+difficulty.toUpperCase()+'</span> &nbsp;·&nbsp; '+mode.toUpperCase()+'</div>';
 }else if(kind==='loadout'){
   page=panelHeader('Expedition setup','Choose a weapon','A starting preference. Switch weapons in-game with keys 1–8.')+
     '<div class="ux-gear">';
   WEAPONS.forEach((w,i)=>{page+=action('wpn:'+i,'<span class="ux-weapon-index">'+String(i+1).padStart(2,'0')+' '+(startW===i?' · EQUIPPED':'')+'</span><span class="ux-weapon-name">'+w.n+'</span>','ux-weapon',startW===i);});
   page+='</div>';
 }else if(kind==='settings'){
   page=panelHeader('Preferences','Settings','Tune the experience. Each category has its own page.','back:'+settingsReturn)+settingsOptions();
 }else if(kind==='settings-audio'){
   page=panelHeader('Settings / Audio','Sound','Control each audio channel independently.',settingsBack)+
     rowSetting('Master volume','vol',Math.round(SET.vol*100)+'%')+
     rowSetting('Music','music',Math.round(SET.music*100)+'%')+
     rowSetting('Sound effects','sfx',Math.round(SET.sfx*100)+'%')+
     rowSetting('Ambience','ambient',Math.round(SET.ambient*100)+'%')+
     action('togglemute',SET.mute?'Unmute audio':'Mute all','ux-option')+
     '<div class="ux-metadata">Audio starts when you interact with the game.</div>';
 }else if(kind==='settings-visual'){
   page=panelHeader('Settings / Display','Visuals','Adjust clarity and comfort without changing gameplay.',settingsBack)+
     rowSetting('Field of view','fov',SET.fov+'°')+
     rowSetting('Resolution scale','quality',Math.round(SET.quality*100)+'%')+
     '<div class="ux-options">'+['Low','Medium','High'].map((v,i)=>action('qualitypreset:'+i,v,'ux-option',i===(SET.quality<.75?0:SET.quality>=1.25?2:1))).join('')+'</div>'+ 
     '<div class="ux-metadata">Higher resolution uses more GPU resources.</div>';
 }else if(kind==='settings-controls'){
   page=panelHeader('Settings / Controls','Controls','All keyboard and mouse controls in one place.',settingsBack);
   for(const [label,keys] of [['Move','W A S D'],['Turn / look','Mouse or Q / E'],['Fire / attack','Click, Space, F'],['Switch weapon','1–8 or mouse wheel'],['Reload / change rifle mode','R / B'],['Inventory / quick wheel','I / Tab'],['Blade heavy / thrust','G / T'],['Guard / parry / saber wave','Hold C / tap C / V'],['Use medkit / interact','H / X'],['Pause','P or Esc']]){
     page+='<div class="ux-control-row"><span>'+label+'</span><kbd>'+keys+'</kbd></div>';
   }
   page+='<div class="ux-section">Mouse sensitivity</div>'+rowSetting('Look speed','sens',SET.sens.toFixed(1)+'×');
 }else if(kind==='settings-game'){
   page=panelHeader('Settings / Gameplay','Gameplay','Select the next expedition style.',settingsBack)+
     '<div class="ux-section">Difficulty</div><div class="ux-options">';
   for(const d of ['Easy','Normal','Hard'])page+=action('diff:'+d,d==='Easy'?'Explorer':d==='Normal'?'Veteran':'Nightmare','ux-option',difficulty===d);
   page+='</div><div class="ux-section">Expedition mode</div><div class="ux-options">';
   for(const d of ['Normal','Hardcore','Daily','Survival'])page+=action('mode:'+d,d,'ux-option',mode===d);
   page+='</div><div class="ux-metadata">These selections will be used for the next expedition.</div>';
 }else if(kind==='settings-save'){
   const data=savedRun();
   page=panelHeader('Settings / Saved data','Saved data','Browser-local campaign progress.',settingsBack)+
     '<p class="ux-sub">'+(data?'Save found · Floor '+data.level+'.':'No saved campaign on this browser.')+'</p><div class="ux-menu">'+
     (data?item('continue','Continue saved expedition'): '')+
     (state==='playing'?item('savecampaign','Save current expedition'):'')+
     (data?item('deleteprompt','Delete saved expedition',false,'Requires confirmation'):'')+'</div>';
 }else if(kind==='records'){
   page=panelHeader('Archive','Records','Your journey so far.')+'<div class="ux-statgrid">';
   for(const [label,val] of [['RUNS',STATS.runs],['KILLS',STATS.kills],['DEATHS',STATS.deaths],['FLOORS',STATS.floors],['BEST',best]])page+='<div class="ux-stat"><strong>'+val+'</strong>'+label+'</div>';
   page+='</div><div class="ux-section">Recent expeditions</div><div class="ux-scroll">';
   if(!BOARD.length)page+='<div class="ux-sub">No completed expeditions yet.</div>';
   BOARD.slice(0,6).forEach((r,i)=>page+='<div class="ux-control-row"><span>'+String(i+1).padStart(2,'0')+' · '+r.w+'</span><kbd>FLOOR '+r.l+' · '+r.s+'</kbd></div>');
   page+='</div><div class="ux-section">Achievements</div><div class="ux-metadata">';
   Object.keys(ACHS).forEach(k=>page+=(STATS.ach[k]?'◇ ':'◇ ')+ACHS[k].split('|')[0]+' &nbsp; ');
   page+='</div>';
 }else if(kind==='pause'){
   page='<div class="ux-eyebrow">Expedition suspended</div><h1 class="ux-heading">Paused</h1><p class="ux-sub">Floor '+level+' · '+WEAPONS[P.wi].n+' · Score '+P.score+'</p><div class="ux-menu">'+
     item('resume','Resume',true)+item('inventory','Inventory')+item('view:settings','Settings')+item('savecampaign','Save expedition')+item('menu','Return to title')+'</div>';
 }else if(kind==='dead'){
   page='<div class="ux-eyebrow ux-danger">Expedition ended</div><h1 class="ux-heading">You Died</h1><p class="ux-sub">Floor '+level+' · '+P.kills+' kills · '+P.score+' points</p><div class="ux-menu">'+
     (mode!=='Hardcore'?item('respawn','Respawn',true,'Return to your checkpoint'):'')+item('startnew','New expedition')+item('menu','Return to title')+'</div>';
 }else if(kind==='inventory'){
   page='<div class="ux-eyebrow">In-game</div><div class="ux-scroll">'+inventoryPanel()+'</div>';
 }else if(kind==='wheel'){
   page='<div class="ux-eyebrow">Quick switch</div><h1 class="ux-heading">Weapons</h1><div class="ux-gear">';
   WEAPONS.forEach((w,i)=>page+=action('chooseweapon:'+i,'<span class="ux-weapon-index">'+(i+1)+'</span><span class="ux-weapon-name">'+w.n+'</span>','ux-weapon',P.wi===i));
   page+='</div><div style="margin-top:10px" class="ux-menu">'+item('resume','Back to the dungeon')+'</div>';
 }else if(kind==='confirmnew'){
   page='<div class="ux-eyebrow">Confirmation</div><h1 class="ux-heading">Start over?</h1><p class="ux-sub">Starting a new expedition replaces your saved campaign.</p>'+
     '<div class="ux-menu">'+item('play','Start new expedition',true)+item('back:main','Keep current save')+'</div>';
 }else if(kind==='confirmdelete'){
   page='<div class="ux-eyebrow">Confirmation</div><h1 class="ux-heading">Delete save?</h1><p class="ux-sub">This permanently clears the saved campaign on this browser.</p>'+
     '<div class="ux-menu">'+item('deletesave','Delete saved expedition',true)+item('back:settings-save','Cancel')+'</div>';
 }else if(kind==='victory'){
   page='<div class="ux-eyebrow">The abyss is silent</div><h1 class="ux-heading">Victory</h1><p class="ux-sub">The Abyssal Warden has fallen.</p><div class="ux-menu">'+
     item('newgameplus','Begin New Game+',true)+item('menu','Return to title')+'</div>';
 }else if(kind==='perk'){
   const categories=['Survival','Offense','Armor','Weapon Tuning','Relics'];
   page='<div class="ux-eyebrow">Floor '+(level-1)+' cleared · STEP '+(forgeStage+1)+' OF 2</div>'+
     '<h1 class="ux-heading">'+(forgeStage===0?'Choose a perk':'The Soul Forge')+'</h1>'+
     '<p class="ux-sub">'+(forgeStage===0?'Select one permanent reward to continue.':'Spend coins and prepare for the next descent. · '+P.coins+' coins')+'</p>';
   if(forgeStage===0){
     if(forgeChosen){page+='<p class="ux-sub">Your perk is locked in for this floor. Review the reward below or return to the shop.</p>';forgeStage=0;}
     page+='<div class="cin-perks" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px">';
     perkChoices.forEach((perk,i)=>page+=action('perk:'+i,iconMark(['damage','firerate','armor','life','pack','speed'][Math.max(0,PERKS.indexOf(perk))],27)+'<b>'+perk.n+'</b><span class="cin-note">'+perk.d+'</span>','cin-perk'));
     page+='</div>';
     if(forgeChosen)page+='<div class="forge-footer">'+action('forgeshop','Return to Soul Forge','cin-play')+'</div>'; 
   }else{
     page+='<div class="forge-tabs">'+categories.map(c=>action('forgecat:'+c,c,'forge-tab',forgeCategory===c)).join('')+'</div>';
     page+='<div class="forge-cards">'+shopPanelV52(forgeCategory,forgePage)+'</div>';
     page+='<div class="forge-footer">'+action('forgeback','Back to perks','ux-back')+action('forgenext','Continue descent','cin-play')+'</div>';
   }

 }
 const bg='<div class="ux-backdrop" style="background-image:url('+ART_MENU+')"></div>';
 ov.scrollTop=0;
 ov.innerHTML=bg+'<div class="ux-shell"><div class="ux-top"><span class="ux-mark">◇ DEPTHS 3D</span><span>THE BESTIARY EXPANSION · v'+VERSION+'</span></div>'+
   '<div class="ux-content"><div class="ux-card">'+page+'</div></div>'+
   '<div class="ux-footer"><span>AN EXPEDITION INTO DARKNESS</span><span class="ux-hint">WASD · SPACE · ESC &nbsp; / &nbsp; ALL CONTROLS IN SETTINGS</span></div></div>';
 ov.style.display='flex';
}

function newGame(){
  level=1;campaignSeed=1+Math.floor(RND()*2000000000);
  P.hp=P.maxhp=100;P.armor=25;P.ammo=80;P.coins=0;P.keys=0;P.potions=2;P.stamina=P.maxStamina=100;P.energy=100;
  P.pitch=0;P.score=0;P.kills=0;P.cool=0;P.reloadT=0;P.reloadWi=-1;
  burstQueue=0;triggerHeld=false;flashA=0;P.inv=0;P.combo=0;P.ct=0;P.dmgm=1;P.rate=1;P.leech=0;P.scav=0;P.spd=1;P.entry=null;
  for(const k of Object.keys(GUN_TECH))GUN_TECH[k].fill(0);
  applyGunTech();for(let i=0;i<6;i++)magazines[i]=MAG_CAP[i];
  for(let i=0;i<8;i++){WEAPON_LEVELS[i]=0;MASTERY[i]=0;}
  for(const k of Object.keys(EQUIPMENT))EQUIPMENT[k]=0;
  for(const k of Object.keys(RELICS))RELICS[k]=false;
  DEFENSE.dodgeTime=DEFENSE.dodgeCooldown=DEFENSE.exhausted=0;
  STATS.runs++;
  buildLevel(); setWeapon(startW); state='playing'; paused=false; hideOverlay();
  toast('Find the portal. Complete the floor objective to escape.',3000);saveCampaign();
}

function newGamePlus(){
 const retainedEquipment={...EQUIPMENT},retainedRelics={...RELICS},retainedCoins=P.coins,retainLevels=WEAPON_LEVELS.slice(),retainMastery=MASTERY.slice(),retainTech=Object.fromEntries(Object.entries(GUN_TECH).map(([k,v])=>[k,v.slice()]));
 mode='New Game+';difficulty='Hard';newGame();P.coins=retainedCoins;
 for(let i=0;i<8;i++){WEAPON_LEVELS[i]=retainLevels[i];MASTERY[i]=retainMastery[i];}
 for(const k of Object.keys(EQUIPMENT))EQUIPMENT[k]=retainedEquipment[k];
 for(const k of Object.keys(RELICS))RELICS[k]=retainedRelics[k];
 for(const k of Object.keys(GUN_TECH))GUN_TECH[k].splice(0,6,...retainTech[k]);applyGunTech();
 P.maxhp+=15;P.hp=P.maxhp;P.armor=45;saveCampaign();toast('NEW GAME+ · GREATER DANGERS AWAIT',1800);
}

function activate(){ if(state==='dead'){ if(mode!=='Hardcore'){ respawn(); wrap.focus(); } } else if(state==='ready'){ newGame(); wrap.focus(); } }
ov.addEventListener('mousedown',function(ev){ ev.stopPropagation(); });
ov.addEventListener('click',function(ev){
  const t=ev.target.closest('[data-a]'); if(!t) return;
  const a=t.getAttribute('data-a').split(':');
  ensureGameAudio();menuClickSound(a[0]==='play'||a[0]==='diffflow'?'confirm':'tap');
  if(a[0]==='skipintro'){showMenu('title');}
  else if(a[0]==='begin'){showMenu('difficulty');}
  else if(a[0]==='diffflow'){difficulty=a[1];showMenu('main');}
  else if(a[0]==='view'){
    if(a[1]==='settings')settingsReturn=(menuKind==='pause'||menuKind==='title')?menuKind:'main';
    showMenu(a[1]);
  }
  else if(a[0]==='settingspage'){showMenu('settings-'+a[1]);}
  else if(a[0]==='back'){showMenu(a[1]);}
  else if(a[0]==='startnew'){if(savedRun())showMenu('confirmnew');else{newGame();wrap.focus();}}
  else if(a[0]==='deleteprompt'){showMenu('confirmdelete');}
  else if(a[0]==='mode'){mode=a[1];showMenu(menuKind);}
  else if(a[0]==='perk'){const pk=perkChoices[+a[1]];if(!pk||forgeChosen)return;pk.f();forgeChosen=true;toast(pk.n+' acquired',1800);forgeStage=1;saveCampaign();showMenu('perk');}
  else if(a[0]==='forgecat'){forgeCategory=a[1];forgePage=0;showMenu('perk');}
  else if(a[0]==='forgepage'){forgePage=Math.max(0,forgePage+(+a[1]));showMenu('perk');}
  else if(a[0]==='forgeback'){forgeStage=0;showMenu('perk');}
  else if(a[0]==='forgeshop'){forgeStage=1;showMenu('perk');}
  else if(a[0]==='forgenext'){if(P.coins>0&&!window.confirm('Continue with '+P.coins+' unspent coins?'))return;state='playing';paused=false;saveCampaign();hideOverlay();wrap.focus();}
  else if(a[0]==='buy'){buyUpgrade(a[1]);showMenu(menuKind);}
  else if(a[0]==='inventory'){paused=true;showMenu('inventory');}
  else if(a[0]==='chooseweapon'){setWeapon(+a[1]);paused=false;hideOverlay();wrap.focus();}
  else if(a[0]==='newgameplus'){newGamePlus();wrap.focus();}
  else if(a[0]==='continue'){continueCampaign();}
  else if(a[0]==='savecampaign'){saveCampaign();showMenu(menuKind);}
  else if(a[0]==='deletesave'){deleteCampaign();showMenu('settings-save');}
  else if(a[0]==='usepotion'){drinkPotion();showMenu(menuKind);}
  else if(a[0]==='togglemute'){SET.mute=!SET.mute;save('d3d_set',SET);showMenu(menuKind);}
  else if(a[0]==='qualitypreset'){SET.quality=[.65,1,1.35][Math.max(0,Math.min(2,+a[1]||0))];if(renderer.shadowMap)renderer.shadowMap.enabled=SET.quality>=.9;flashlight.castShadow=SET.quality>=.9;renderer.setPixelRatio(Math.min(2,(window.devicePixelRatio||1)*SET.quality));save('d3d_set',SET);showMenu(menuKind);}
  else if(a[0]==='set'){
    const st={sens:[.1,.3,3],fov:[5,60,100],vol:[.1,0,1],music:[.1,0,1],sfx:[.1,0,1],ambient:[.1,0,1],quality:[.1,.5,1.5]}[a[1]];
    if(!st)return;
    SET[a[1]]=Math.round(Math.min(st[2],Math.max(st[1],SET[a[1]]+st[0]*(+a[2])))*100)/100;
    camera.fov=SET.fov;camera.updateProjectionMatrix();if(renderer.shadowMap)renderer.shadowMap.enabled=SET.quality>=.9;flashlight.castShadow=SET.quality>=.9;renderer.setPixelRatio(Math.min(2,(window.devicePixelRatio||1)*SET.quality));
    save('d3d_set',SET);showMenu(menuKind);
  }
  else if(a[0]==='wpn'){startW=+a[1];showMenu('loadout');}
  else if(a[0]==='diff'){difficulty=a[1];showMenu(menuKind);}
  else if(a[0]==='respawn'){respawn();wrap.focus();}
  else if(a[0]==='play'){newGame();wrap.focus();}
  else if(a[0]==='resume'){paused=false;hideOverlay();wrap.focus();}
  else if(a[0]==='menu'){state='ready';paused=false;showMenu('title');}
});
showMenu('intro');
wrap.addEventListener('mousedown',function(ev){
  if(ev.button===2){ keys.look=true; ev.preventDefault(); return; }
  if(state!=='playing'||paused) return;
  keys.mouse=true; wrap.focus();
  try{
    if(window.self===window.top && document.pointerLockElement!==renderer.domElement && renderer.domElement.requestPointerLock){
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
  if((keys.look||document.pointerLockElement===renderer.domElement)&&state==='playing'&&!paused) {P.yaw-=ev.movementX*0.0045*SET.sens;P.pitch=Math.max(-.88,Math.min(.88,P.pitch-ev.movementY*.0036*SET.sens));}
});
wrap.addEventListener('keydown',function(ev){
  if(ev.code==='KeyE'&&state==='playing'&&!paused&&portalOpen&&portal&&portal.userData.phase>=.98&&Math.hypot(P.x-portal.position.x,P.z-portal.position.z)<2.2){ev.preventDefault();beginPortalDescent();return;}

  if(ev.code==='KeyL'&&!ev.repeat){flashlightOn=!flashlightOn;toast(flashlightOn?'FLASHLIGHT ON':'FLASHLIGHT OFF',650);ev.preventDefault();}
  if(ev.code==='KeyM'&&!ev.repeat){mapExpanded=!mapExpanded;mm.style.width=mapExpanded?'260px':'130px';mm.style.height=mapExpanded?'260px':'130px';mm.style.zIndex=mapExpanded?'14':'2';ev.preventDefault();}
  if(ev.code==='KeyN'&&!ev.repeat){mapRotate=!mapRotate;lastMapDraw=-1;ev.preventDefault();}
  if((ev.code==='BracketLeft'||ev.code==='BracketRight')&&!ev.repeat){mapZoom=Math.max(1,Math.min(3,mapZoom+(ev.code==='BracketRight'?.5:-.5)));lastMapDraw=-1;ev.preventDefault();}
  if(ev.code==='KeyC'&&state==='playing'&&!paused&&P.wi>=6&&!keys.KeyC){parryWindow=.26;}
  if(ev.code==='AltLeft'&&!ev.repeat){ev.preventDefault();beginDodge();}

  if(ev.code==='KeyV'&&state==='playing'&&!paused)chargeSaber();
  if(!ev.repeat&&state==='playing'&&!paused&&P.wi>=6&&P.cool<=0){
    if(ev.code==='KeyG')meleeAttack(WEAPONS[P.wi],'heavy');
    if(ev.code==='KeyT')meleeAttack(WEAPONS[P.wi],'thrust');
  }
  if(ev.code==='Tab'&&state==='playing'){
    ev.preventDefault();
    if(paused){paused=false;hideOverlay();wrap.focus();}
    else{paused=true;showMenu('wheel');}
  }
  keys[ev.code]=true;
  if(/^Digit[1-8]$/.test(ev.code)&&state==='playing'&&!paused) setWeapon(+ev.code[5]-1);
  if(['Space','AltLeft','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].indexOf(ev.code)>=0) ev.preventDefault();
  if(ev.code==='KeyR'&&(state==='dead'||state==='ready')) activate();
  else if(ev.code==='KeyR'&&state==='playing'&&!paused)startReload();
  if(ev.code==='KeyB'&&state==='playing'&&!paused){rifleMode=rifleMode==='AUTO'?'BURST':'AUTO';burstQueue=0;toast('AK-86 · '+rifleMode,900);}
  if(ev.code==='KeyH'&&state==='playing'&&!paused)drinkPotion();
  if(ev.code==='KeyX'&&state==='playing'&&!paused)interactRune();
  if(ev.code==='KeyI'&&state==='playing'){
    if(paused){paused=false;hideOverlay();wrap.focus();}
    else{paused=true;showMenu('inventory');}
  }
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

// Initial dungeon renders behind overlays, which also own their illustrated art.
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

// Load the pinned Three.js build on all hosts (Colab proxy, local file, GitHub Pages).
// Failed CDN requests and WebGL startup errors are shown rather than leaving a black screen.
function fail(reason){
  const wrap=document.getElementById('dd3d-root');
  if(!wrap) return;
  wrap.innerHTML='';
  const msg=document.createElement('div');
  msg.style.cssText='padding:30px 24px;color:#ffc4b9;font:15px/1.7 Segoe UI,Arial,sans-serif;text-align:left;background:#17131d;min-height:100%;box-sizing:border-box';
  const title=document.createElement('strong');
  title.style.cssText='font-size:19px;color:#ffd5a6';
  title.textContent='Depths 3D could not start';
  msg.appendChild(title);
  const details=document.createElement('p');
  details.textContent=reason||'Three.js did not load. Check the internet connection, then reload the page.';
  msg.appendChild(details);
  const info=document.createElement('small');
  info.textContent='A browser with WebGL enabled is required. In Colab, run the notebook cell again if the proxy iframe was disconnected.';
  msg.appendChild(info);wrap.appendChild(msg);
}
function boot(){
  try{
    if(!window.THREE) throw new Error('Three.js has not loaded');
    start();
  }catch(err){
    console.error('Depths 3D startup failed:',err);
    fail('Startup error: '+(err&&err.message?err.message:String(err)));
  }
}
function loadScript(urls){
  if(!urls.length){fail('Could not download Three.js from any of the three CDNs. Please check the internet connection and any browser extensions blocking scripts.');return;}
  const s=document.createElement('script');
  let settled=false;
  const timer=setTimeout(next,10000);
  function next(){
    if(settled) return; settled=true;clearTimeout(timer);
    s.onload=null;s.onerror=null;s.remove();
    if(window.THREE) boot(); else loadScript(urls.slice(1));
  }
  s.src=urls[0];s.async=true;
  s.onload=next;s.onerror=next;
  document.head.appendChild(s);
}
if(window.THREE) boot();
else loadScript([
  'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js',
  'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js',
  'https://unpkg.com/three@0.128.0/build/three.min.js'
]);
})();

</script></body></html>"""
BESTIARY_VIEWER_HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Depths 3D — Bestiary Viewer</title><style>
*{box-sizing:border-box}body{margin:0;background:#09090f;color:#e9e4dc;font:14px system-ui,Segoe UI,sans-serif}header{padding:12px 18px;background:#18151e;border-bottom:1px solid #493d4b;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}h1{font:600 20px Georgia,serif;margin:0}small{color:#aca4b2}main{max-width:1250px;margin:12px auto;padding:0 12px}.switch,.actions,.tools{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}button{border:1px solid #625064;background:#251c2c;color:#eee;border-radius:6px;padding:9px 12px;cursor:pointer;font:inherit}button.active,button:hover{border-color:#e7ae81;background:#53364c}.screens{display:grid;grid-template-columns:1fr 1fr;gap:12px}.panel{position:relative;background:linear-gradient(#1c1820,#0c0b11);border:1px solid #554750;border-radius:8px;min-width:0;overflow:hidden}.panel h2{font-size:14px;margin:0;padding:9px 12px;border-bottom:1px solid #4a3948}#reference{transition:transform .3s ease;width:100%;height:470px;object-fit:contain;object-position:center;background:#0c0b0e}#stage{width:100%;height:470px;position:relative;touch-action:none;background:radial-gradient(ellipse at 40% 40%,#302a32,#09090d)}#stage canvas{display:block;width:100%;height:100%}#over{position:absolute;inset:0;object-fit:contain;width:100%;height:100%;opacity:0;pointer-events:none;filter:grayscale(1) contrast(7) brightness(2);mix-blend-mode:screen}label{display:flex;align-items:center;gap:8px}input{accent-color:#cc8ca4}#status{padding:12px;background:#18141a;border-radius:6px;margin-top:9px;line-height:1.6}#error{color:#ffb3a3}footer{margin:10px auto;max-width:1000px;color:#aa9da9;font-size:12px} @media(max-width:760px){.screens{grid-template-columns:1fr}#stage,#reference{height:320px}}</style></head><body><header><div><h1>DEPTHS 3D v6.0.0 — BESTIARY EXPANSION</h1><small>Original photo references and actual procedural Three.js creatures · v6.0.0</small></div><span id="error">Loading Three.js...</span></header><main><div class="switch" id="species"></div><div class="screens"><section class="panel"><h2>Reference photograph / concept crop</h2><img id="reference" alt="Reference crop"></section><section class="panel"><h2>Interactive procedural 3D model · drag to turn · scroll to zoom</h2><div id="stage"><img id="over" alt="Approximate silhouette alignment"></div></section></div><div class="actions" id="actions"></div><div class="tools"><label><input id="spin" type="checkbox" checked>Auto-turntable</label><label><input id="overlay" type="checkbox">Reference silhouette overlay (approximate)</label><label>Overlay opacity <input id="opacity" type="range" min="0" max="65" value="23"></label><button id="sound">Play synthesized monster voice</button><button id="reset">Reset view</button><button id="faceview">Compare faces up close</button><label>Load GLB replacement <input id="glb" type="file" accept=".glb"></label></div><div id="status"></div></main><footer>Reference artwork is provided only for visual comparison. The shader-based procedural model is an approximation, not a copy or a photogrammetry reconstruction; no GLB models are included. Browser must support WebGL and reach one of the Three.js CDNs.</footer>
<script>
const REF_DATA={"brute":"data:image/webp;base64,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","crawler":"data:image/webp;base64,UklGRuJOAABXRUJQVlA4INZOAACwRwGdASrWAVEBPm0ylUgkIqIlprWqgLANiWdukctguM6vHEoytXSaZXFRu7gG+r0O3vt248xNVt30/f3jeWc6xp1foidNlag+pHhr+R/Yf67+/fu//i/dg0H9n//N6G/zr8n/2PQnwV+bOod7l/4n9/7mzyb+H/4noL+BPAP1d8gL+lf3f047678n/6fYK/rH+w9Wf/V8pH2H7Bn7I79Cxl7DMrdonkDPppXB2iIgvjoBkKRXAl9CD0oLQiJCjtdgPQS6EZd/r9/gDL3yu1cSYTKmgBgsmIGtJ13bHwPRYBywLkdptsZbpETcaG+NwtkH+M+9DyVKvYx7MFb+LSKOKv7X725nHbA4K0l/0JIq/oc0nvhur05NSofxUQ+HhH6N+8zyGpiYmVW7kzK5RiTRNV8ye55Xpnk5c5mD8T59SBvhhMETD3tMhhRMUIffm8BPF0YuJtMmg5PcTaVY5HIJgsRuDk+rNvnjPBjlCzeostrHaymQMD7XiXl88loXsj/U/tLSwhFd+0nGPQ8fxTmKCjzo1u4SRRipsIvSWuhtJ0PRjZjvJdVkhtm+j0VYSWHBO8S4usSdRcTqgw3kwCIKaI88IkbYpMzjxOrh74PJiaWx2YDSCOovS1CNkpLXJ2GyfsqUb2xvY7KoYLB3rZHtpmI/ANQItI/X3HyTip2OKd5w+5wR8acagmgO9+pk5fJFFw3HQwclTHnrNyeHKEJUkJ/+nUXEqQvH9D56kc5TJeVLZnFROU4MMX0r0Brpz0sXw5jXQz5FtPMI3/Oo32+u7ULcACPPeh5Bsdw6IQqnwbgfD2JgjY4rc/UFZiAvlNZ3h7UAQ8Y1DS3xux9vMKyxFILkQcxus9flJ5JSyKiDF3NxhG/IwBzsSlUy3r9AkNHO1Oz5c5K3e707k/xW9iG6V7YOkcg4y1q4whtSxb6SetCEdpWXojk8JfnfeJFbTbIQMP9gY67/LL2OyQWSZsA9k6gHkLbTno1zKFSHm1utRYXas/MT4vb0P4daS0vCasihdfiuHuaWg7cVXdDNK5EMkrStzYdu6Ns3pE0ERVNtyWGhoJg8iz/sa8d5LlflNgQIDtk0jmBfuz5TgpM2B/D30JgG0SWDmIBsaMJYm2QuQCA1CLjV0DxTCb6U2oWXJmFgBfNMztSD3r2QToEdZI5dfePHNWNljEqPRNqVs2FWiyLEm4OSFz4zrVBkZyfpCZ507fYDZNLe24K1kqAEVKpQfEoGuXtP91EftvO7wjAtwe8/a0F9k4rOgechF0bJzdk9PiYGum2Ei6zmQ4WrRByf+hU+jAu3qlty/6/vQ+kLfDtKm0YGSjdoPPnKrYngbmU1+luT22tFD2o4Crx9w44YcfahK8NE7sH0XH43daTRZx9kzNlmrLAke4xED48tLLzGGSwJxPqGMaEzw+DKev7ydiHO+p44rz28xcuV2NMkBCR5IbBil1/sUjdK+uFg2X0AkflWx5jyDMrPo+U4OIXvBUiKTcN8iHz9rPmukvn1FDHCTYDfjgpmcu5hBQhjUXWKtEHDlFuvksG5K5hc+BUtsb760CfznPk6nOjaX0bNi4xhcd2JXiTdZkiK60rtAUUTSXWpsDE8qlOQt31cdmM7lmVvpuN5mvi4rIcW1LSzITX6ODBB4GB+Bz2obYkN9KkM51IOrRpPIIip6iUEmV6fVX99JJP9ASGdZh5dCTPxnzJ0LYOk1h9lrEWsjl+EeQmZ3qxjirD8whlY+FSvqH8ffXA0d98mK6/IdH37FHCbnI1yvpzKqpzTEbBkE5bFzPAkAKOBPd9kWPbsr8DP9g5yalLUd5O2eEWPRlp2YM9ez0iWyqm6RbndHmt1zVOqbp6L93Del9lNtr8C5rCDFcme1wf8h0rfqpplCOwknvVr4i3HG2lxvrfVXdCZQTLRIk1E3C9MklwdP9wxIcN1CchwUZNycbcBE+cFklVHNXMx/b5wY50LANJSK6wdOAWxvbC0C/198wpaLwtze27phi3jvNN99iXJR/kHc9S/5d5m9psC78EblrzuqLtNDELLsD/6lMvrmsaJOgBzPKo6KcLEME7p952rmBQkAfnCESFXMVMlUoi3qdd7w5FYi57vQbYHEjig82PyOmXzktDhAMoziqmgqJeIL4Fmdgt9tDSB0BX09FdjnlPP8HMxwWN9z7BM5r3KPh6VX+vnof0GYVWFOT1RiL+jVA9A3Ga8OF8N/zSbmQ4DSNvfod/sP2QrxlI3lXm05aS6qY0ZgvvJUgmWJ3R8LDrRpg675NP6UKTm1GziuG/JbQWjnauucHJBYDwl5tCdb9jaYjT9KHYzn8sPcSgK/qKMkW1Hc96KYxz5/AKi33E5AGmQJNPczbpn26iCpWHDrrH68LENWHVoDWHj+2xGYyt/bmRD4Gi6n+Ry1ANXqPgQ9WVQz7VgU1W0l5whafGOEeOQuTkHEq4u8ZGep55Xh1qSH8V8cSTraPmA3NghjSKxGx8gbAjJR77lFbe72lzN65iuYTmTHGdx0bCmh3Swkks+HGw+Nd2L+SOnj1Xf9imCNNJ75MZppn8lcQefkgXE04g2okvd9uxpQlCVBvCTw9lCl/P+illzDWXX0NrtngnRxE0NUBj5Q5aQ58JnEmxPOZqAsJMV8rNQqVVVLOTENDN9yDS/Ct2duptNA2t+ssLk1lYv9AdvR1BnjFuEfp9IFRtGgcNBuFO0BaIr4T0PVxLqegcwxDamk5Xjp5rwmZGjf0CqFNBdoWr/m1P6xPyYimeKF0vfHPwj7lrO/Qkx9gCC6+dV72KxTMufPWuB9DZ6O3sLPyj1PDubFLLf9y9uuRG1QMVhzPjSbn0mkNRDAPZfoRF561kadS8C4gmyRBVIV1SiV0/LmAAfG/NhI4wz/EsLMXXfk7O8CBio0+Gr7QFCsrnaS50FdBtbahwl9Bxi6GnmjZDINcKGI82lWl4bn4VLB6AXF65vVOCMztMOPy32bTFhrHtPj2pE4aX+x0VNC9QCSg6N3W0hD0lSNF4KP5uhf9fbd8xIcjR2ZMDPDb4baX57r7U/wXIMxq8858pTPm7LfyqwJk6e8flsfmgTOmQWAdTPJhotmGDeS0MpUP9fy8pX/7EXV3J+J8Am+OqwLYUaTh2QT+Mh6nnM17A+kPPeQAHX+05MkJ15hbmP8P5A7IluEou42KYeJjHyAASFj5DhRvmT6LmoGnkdV2XB25trzEz0vRHhfgSSIVOP/90MlaEkU/zdzGV2+O20+XyfOLVbvXmpoA7GqGpHbJxe5j8/Njnr+NHqeplRp7BXokisnqsWSrlqpOTuzN1WbC+KDYvKcVo2p+vrFo4BmqI0qYtSWvO7hE7wtPzkj4ab3J+t33BOQGxf8eV2cs7pkFPn49uSvU70Xi0xbBvw4WwQt4y+7kuyVU9jmivQP13OAAchjxMeWc3AS0Uj0o2sdlMyi6l5tA1VWlSBFqAaUL8JostfAN7+Nx+ZgIrqwWGWyqhI4F3HxazQ8aZoPu5AB/RTwAD+9iKra3NZ9r+dlouWjwz07X8yF3+RZdiRA2lEL3FaNO6OWBwmIne/QCMPtr6BDlGcGKi+ABNSYD2t3r1OxGUhZaTCc8nmxHxrJvCJINpWgQVZ9J2sOu+uzu0U5vmbqFUdlNtY48Ha0Q5KODXT/C703AYVF0LIu9gu5oZdzKzLZLGha7fnQ7g3m/tdqu0mwZm30iNs4RD5X4yBKwRzofP/IlDlxGcmCLelrWVANINFuIXIenleagHiQRg6PgRSN7FPMd+vdiR1yywINTxLBevY7q4DI974XCOp/LyXhXz1nsXtRoAG2R7dk6AMbfV3i76mh149BiJP46V5wIM8iGY2rx7mNfqiJDxD5Dna9ST96gxP+wTqioHRzLGw7DywVBfs2zK9oQ3p5iTvVhIkDpN9WFGTDFX9gOykwDGdim301F7Bu1WFbjxZP+ovKA31ngACmuSTdh3qcukwVepZbAUwoynU3FGhe8YCAlI6BnTTFaSmzGHnhHa9KuQFSLXsAohGmOjTXOKWy3phLJtDP7fUQ8jPjGhZJQAsiEQz69jzEWm/L3nv1+8rUekfd7bA0CC/qKxlFeZWxeOAk91vmgbrjCDNJAXYitEKsugnnHnj2Y9/BfQaZt41fn+3f6e6E4lo62Ll/CSopd5y/zx56r0fALQPmtzsqauoE+yEpY/fIAOAXxvh06HwttWX1HKuWdQ6LFclLbo91ouVFMHKuRhlE66IJUdOr3fr8FwpbvNGof/tGW1zvKK060TTUiTGZVFQSkLeqWLP5FqZmsax9B+NUMxL6ED+69A45s6sEy5EjbqVdVOIKi9wBjql7oN1MC9k55nj7e5eMB8qczsuTmKfuRJW07YfENUVGqMAg1LtSjm4UXPH6KgGkxZ6Jy3NRGRYG3Jlk8/VSLGfqiKb8Og0K/L/bL9BWbSYcmAt+ieqAhVvXIUqsNs5u49o/VIsXdfA0H3G3uxIm1EBLehjHvM1iU3+fXUGljdVwALB4cRETOS4JbfzVxxBo0L0BVltsMfReQq3NzGToAT5nZWskb6vfejpBS/Uf8PBMSlyGb1yGEpziWRzgq1znUD0Cond6bOgVnzpsrC/GHuklkBeiKRfKZDkrrphiwwby0MmBhtIi8eY9vJY6iP2PgCyzMAxcFPBGTe6gYUJjFh0xmDdSNpatoYfSOZRSXlqLXf3nqieQCk570tpIIUECf71U7DoEeaExypxmguGIazDFMVdQpU24z6FJa6XQrFQRUnDZaP00zQcn9p8AEvWYYmEmM/aDOntnVMtKrOeFBt3JQgXmA9hPCvaJvouJ0xBrwepGy0INh921H0o9Ac5kqxtH1LAd2KleqmXKxBpqlWWaY2y+u4iuwwI+5mgNaoukXQAdnhPkjBhMop3YoWLVJuy2wNqa2/UR9vOANGCd9+fiClZcQASAylb6AwJlQ3AdjmyVQe7hrOklXUobS8XiL7IJmSsOTdCUhNxpOwiHJ4Ge29dg4MK7HoSNMdboa7VxFbzgXdnUSpGNhtQkz5bROcjtzNLyRW3yIz41pGymXk2B9h58lY0WD/jP39s18nhQfPb0yjFNROqwORsYPOL3Rd1S2HDb8PZqBzQTDwOxZSdQjAE81iKRiQFPkA8FzfAfAtagVXTr1Ujj9tCxTLNIcRfGz3TpjdNW1dBOxSYqwu6RTaBXkAewhinTvo/lmLI23zrZb5pTg/yqwNgQPdFeYbj51lWMYboBfHJzoJ2scqNiZD24ST50bEbUgYPEWBPdvnEphVCGRcFUJX9yqwejTx2y7ZUGkLuEUkVnVI7wI7Oq2dQCcAniKKeUxx4Rymp7wMndJ5POXu7gabm+S1Mg3DmcWYWr2L53Jpz52eews/cXtTz55dOSitLp+fvQ785Ri4+Bd7ei+01b+9/8X44rJ29/Q8FC7WZ/jwvObVrusgXvV/6US7SFX3pPlviDuoQZuUezQ11r/MxdcJrh2TRmzmUMS2yOxxZJIPnZoV6T3pZxgGXf3lfZBokv7Jj3wvQhn+4exVMOHAapCkH6QsXbUSq22KFjmTH2ZCq8ZDkiIhdEejvEdDbx+daYH5fZ+PASFB6B0feokrb8M5YVVNUkTJw7tNLhiruf5btUE2ZGx4cR2vah/dtEO77b/5u0MGxcUotYXGiwlrBSWZ16sqIm25/79927tDSeurD9gFk87OCj1u02o/bHcy7nn2h6o0ngCrxXv7VIFe2fSvKHLhAZWi+MsmrI7wmCnm+rgscr05TbU67puR5vBD+HKsNPXt59VMCwt1eJwcAqYpkhvstwhmr6JG8Vn3PqnLF4OFFfLHeznsptEaq4sqI+DKrQEqZLgJarJ5r3oCejINPsQHq9aG6Tw0tMQC43RDvQvCvf5XMDLkEc1I5RJlo8mXDmB+dpzE+9ZmFKcpp5NSTp9tYth69COWntcSM9XxbOX1q0pwUxIGSUQiw3sg6PVB1AvDM2Xa2/wOlFcLbJokcKz2qD+NK6FSDas0qDI2hEtG6cHv3ILHZ1qvMBejF8VOOZ4xKHVPp22Mv5U8AIuvroKmg9DLS/TipeqBUNnIAcJ9lQkP1FNBMuY/Wsi5uWMxrBo32tYk13LxqGSiBMoiBwcST4HNkK4WY8dNA7SD7ajY1hq6epA1eXwV+0qDJOtZ4Eb0f54M68AZG8iRqPtIiubd4DvjQI3byZ4PDQyTYR2YZacdfYJypGnRSFTYCzPPxpZHjTAQdRVYsjXTJ99Yy4VJwzcRUAX45NochkcpF4Eik3x/VsVQObDjl27UMefpj0B+qD3OAOQ4O0xHoIA08RLmwxzhFB0Vdv4xL32+N5l1yY3xTodjGKgpbm2t/HR4UuogBvZiF023b7iaGEFDquQJyZmCGNNFSwpGD7OuQe8TFVLL9R3uP+dYCer8dmOmZ44md5JuWnqSuwghH6u1+SInp73+ChYspSM+oP5PsuvXNRcafb2/3udKRRCz/F3rGg4QvbT4wPhPKQg2YeCGEMG6Gb4/t6TRFvckr9/aOFVL9Ao9rg9+PC5xAlpkNbT6p2f9Vkzv+pQIR+Qrm0cdguWzQpFujTBRBKsM3kvIgBL6lpMrulon6/lZbryipAegmlCO9LXGs6EnuDsF4cW/EYQ7X0Q1Uh7gJfVoEcoZo71okXi9ei2Bg/b4jVrJc90jEVseAJWa+eZcw+NMvdZ+8TCO5LQVRoWOG3+JCKrGLDQXeAmqvMEakMauMbEE4O13+fKJhX4IVTJm4I8IsScfM6kMtsI6smn5GNJmV7ojiXtQRB12jOBtQBoASkCzNfXje5VnqYWQEJkpCCxzVNDPwIIZLuSPOSFvfcOnN6X/yjIJyCo/hDRbtfG1D3qUepFa3txH57VIyhFscSrjO0ptRRyiaT0F9hx0ji0pCDlL9Vli9CD84WBYITh816Lp8moG94e8csCFQoyhdKUiGUp99KezYkS7YS8bLMqwRfcg2A5eV1l20xkVVAHVmJJRhDj0luraKNc+xU/vE1egReBiUlIjMAihBEIXrQ9cV21Sx+1F+ULZjnIKVLWVGie6WbJaawqN6NXYAvbl/qx3JVu3X1m2vZuyx71ful5+6gOUiCFT7I9JZl4m0dDW5sXJ9OZhJ6eq97WYxK9hz7Mh+WU+T42mLGjbJYagRzMbME0dfTqszOntSF0zAmJ8C0YUeqirFUMPoKszscYwnUW06bX7iR6SMZvAvmZPKyklkDMDplck8Egkoo7YGUSBKBA/Zv0sOSZRyVH4/H7i9yCL74EkNJkf0Tt+hcFL4ZVvdYMJn1bWqo8AUx4ii+SYazNxpAP7/KnZ5q4qF9B5CahOVQNh+tokCX2jZLjH+giZ/b8Qt9+JCYknjhuWZg7tVJC3aGg4BChEjEDbj9coWMO/l0iVqbcMnsNTrtvHptjhKV4cF3QMDVRHxqLvlPIMXnV3E5AY4lUqorFrnonZU8+pUD2COCHXsQNH+mk7/P/0qiWXX0d+rvQogDVeeQNrPJx15KUgKTuDq1WhdexPPCvThi6781urZ9CH1zBRA7rwEMb2ZUvMqOcw7nphxQxhjThTKHsgJRD4rJXhybMuOq7IGt159UwR6O1f8CWz89PFtFSh61DYR+AjY83Umq5lAaZszHyW98bFFLKrxq6C10FbBEMjs7GPd8v/YavVy3go29/udULAhoKt8AQ5BYA3FnXIOsa7hMAUcFcjMQBkBNE9ukX2LyWBl0/jjcCofPWLq70x0kxCedq9LldzSfZu205haE04Z3QkvekXX0Y+Z5+5tpqoXLIuc+L3r8ZZ/VEIRF0cCn8HNwJ47BngUhh6W1cRtsJFEgBAGSpdlke77LxYuVCVSAx0ie3euuTrYE3jMzXHKvsUTdyQQGWN2SFHUEYKFF22JOdT9BTTgJCPjzRM6DX5ibMZ5GXsxi2x9cm8hUejTOgnvnf4SMKBTfEWHszA9ck0zbpc/dZ9Z+ewannVPbJpvPAKyB5Pbw4+q1YYQ2xDAhseJV2+ERAaJrXudNGKKywz8mqsqPsE0zQbDF27v1KPJJesVfaP3Y2iymayhYqhh5HJBqFmZtGE5uhMxEQa/4FMzTWg2vswm17pAjD31+z6alaUj69c/z6IdJTlryFoq//UDu1RFdRdLYuN/trNtJllYP/1dYtC7Y4mxII1554P3IksQg494eqVu7qjYtRzx2wbSc7g2wkLSiw1cpgu8DWGfKzpyi6Y8yUBi8/gz0o6DgWSk6E3V8JVHnQFO8wPR4zZ5JyBBLv+y4g8yyh+Qn1B2UwgpQkCErJS+uJxgCFVtDhQMqA4ni0TLRncwmfQb23USpppJ2UkSu3wzpKAXNedN3+8K+lLMI9aVA/fhqsKKfTUX/Yc6g3WuGgbYGnFvqYrevHaeRaxB/iRF8HlPVbuinywooieEFwogKi8lE9zWH/BOFPk+iCqo/8J8hPWDp7/olGg857HK8cbSUCzKf/We3NnOdN6XDwRuW7BWqFN3pg1QCOyLPpuNUtBw4eQqpYwElpKJ8OgDnEuByeExMJu+YMzoDe5U+U1f3EPbUDSNlYRraBtyJb/Ur0FSqK1Fa/AkenhkD+5rwd/kRMsra/rJ2BockKUzevMF4puW/kCWSLUksO3IQNfna/YWzpKAdPWPscT/0rTRkGejXiuCoaw2N5nrDfQ6zEDauBUClkAubqfZNg2HxZenX7sKYFDvtEcCrXb5YM/g3K0RTugcMxtWQk7YjUuIWIo7sQkzCnQ8ZgJH0P7Yg6/zajKD6cXnLsKyIOfm24rKw4pn1bn/NsPl/BufTJ1ZhczrTlU8JxIro5oPWpnvHr6lUiabGeft0+seGjDT2PXk+sP2m1Y8NZzRh8Hk3FYynSLk74mB6OoEmUjSWfPEshj/IWoeKlP76kT/a7hsTMOmxfgqf4g/9S63t9/uP9K8tcXvyIldiFlVLaZDQoSUydDyb9wAcK6RMnSRbY0ipH8zn7lXTTcjgOYM+VHFX+FbrAADgE3HT6g7rZ2+tNk2Mb7CStkFliJHcxE2XXJuMiz1HDgs708KHBJz1E0NctLDh4CWj1/yHC9CEsj+4Y01MxImz4sfflfV6w0Jaaezyg/KfPSwMEJpdhkIvPTRk5Rdan6fT2YZf9XM8R5UXUORCRPXFG7eOImatJUeLhe8aRQv7U3SqsQqPnBtc+iSQ8/L/1gp4olZ69xdPzXWbn5q79Y8klQfgOMwfkvrrTdlAGorLYF4mXkVPJayxghI6N1NKOjRZljM5P0jibUBbaQxhlXc7RrhVkRsKvfgEGhv+cKHRFk+KJXwZBeLyLqKIwq29ZMT8663fEMV95FXlZoTiqst7A+WWLez73HVk+LN4hvqhiCSiwDVitVomd4a0gjtPtUC/xYgr31nDLt0rnIJmcdb+31D/o4xNRVQZIPqHXwcNFQ5r6EWa0zGxWQ2ZrqlUsn0O3B65p6ljTat37PZ8DmW7Hl+07qr/7HLMwMwIFuvOVBO3/IrPLFNcHDqgc7/5HG23X4R6xXQs3YHwRoNneFTpNP/hpslUKYAhOUBHztJ7kYWtMps/HB8g//fo/Dlbn2JJC34+qqsZjVtaxZsnrtV2vufvI7H9F+MEYjtQKMBD8lGSnEX9Uxl6Dn8LzJ8JmXHKmWTU90ltNuI3tUC1lwSW3h4Jg9TGyHDnwCesmaPF525VAoyocwtaWhfbWHMo1P+9xkFtYOFQ36MocBNupdlGDyhGfcAEw1++9/Hv82ikzew0F6Bqpc4sFGoeQOU3uwL21BohssdroTwNTOM6dKgbZ1MgB8tKhaLeOaEABq2tWbgA4tcAEXekfgqh05TDiCr+oPe0H/0ZUiRKzethmEghBTm4caPO+qZVDLrZV6a/NhLQNQ4Lq6BGvVXHgzL1M8s26rpH+FwOWUJAyD2+JLCahGfmvUpQiEwzuNqDqsAjHkpC+Nul96tJJLlLrh6m5T4xf0vmx/KLFpptQvnV01Z2ZNBU2jfS1MS+uHBYQADpDqP4zMMhdZV2C1Kx7XHDSi8nQRliNDpkiR9XZSv8qkgNuKs1im2D0MdADju+on54PpgRXgtMS2F89xYoFW+6diSNz1pGUSPNhmB0VI5RXQ5HdszmQop3vqexIYKByhIXNHLeSJ+jWJ2mPcEh/u1Mzr49Gm6oSrGOB94dqz+BUd3DQd9+mZEVAiJQWEAPI2L+uMEmHoyFAklEpwXWFeqeVgmuA2V67RMMfaTw2uhCyStGss5pF7V6Pk01L5+FFYRGulhqW0gNQdSu+kvQdFfo8OhanaaES90UoQfaEUBroSBzL5stw6/E6mt3251KIN+ZGIcovnuMIXHY0fATE3XoH6H6QDR89ORTGEmeQHXbGreqh2uhjNgsq7b9tIzghrYQ0U6es1ylJ1Ez0uNEXalLHtJx7C0BFzPUppH94+GogNU7PxnCAByEnnlVf4k0Ef20nqtablUW+I/xo1Fcm/0R2LOvr3Z3eE4I7cwD12VhlX0gMSnGK91vWOrcHtzHB5QHufUE7FSMrTGP7tKYENOP6dUCKOG7V4cKWkeY5+EpVziWc/X0lJVNG5mcbqwlUZSmsG/W2Ojf0Z5lwkDsDGO0Vk0lRTpY9MPmFY3tbgDxSznHiXmrlz3KymDOV0ZAl2nSAQ95Y6nLO0Zb8plsXt6Oi8QeJutUzh83ujw9rMQRFbVC7PejeuYXJUPP8gsdeZcE2hWlJWaEueX/aYexEh8JFfa5hG0ApIemzi/fUXhap8VO8mcnqe240gHUG/0SOKm7P3L0Sd+gBUUH5THn73n3f0fm3wv9c+eIYopK90xgOsWVIKmsk/E6EkLq2IEOIpPF28r7G+LtDEaNUckqDsmmqtGiZo/7jJLCeEkKd8yzdbbP+kXIVtMIePSjOLijiK2UfGbC/lhh6qt8Jxd4XW+SIWQjFjQ9pYibtsViIB1oH/ZSIbrqcNjLygnXQkIalmRZdbUKbuA/4X32bzUvkxfcfyC8d/8Hbe/KCc6QPck7+Yn+hHHFgBT9VWqmREK6q/jQtCJSt//2ZI/dweGq3L/lDtUfrMpxmJNBJN6ALSL4icL4ocqLcKLf8rz7M6EtN3RbpNBo5CT9wc4Qo0ZFy/CCgVZVaZcn/d/JeRPNH8RhI9YFRVeZElUiVa2MLQwuElXIfw5QQSnF4fx/XZMI+WyZyBWeS0z6eUiKf6WrCg8uUxHSoEB+3WDUSjHDhiqJSj5nq8Qdr8XSRRcGBjU3nxXANQCeHKo4lcJX7obtSOFEsL5o9syuZ4vTpzruRabGMdPlvnY0UHXFbBEhcvz5JSCaj+MGHVtV7fAFWGo2b6pYk54ncjtVAC5ghSLn7ffTvUxvbbsGh7PGBCjb1OJkLd0dyB7NZjOMfl/kQ2i3mYojmpnV72RoJjSnqglnM6HTXuL9WIPY8OKJpZnrrkGPM7SkinKMtmt8t7/zLYWJCJrTOYA1ybKeinthw3F4UhRiXUlVNniK28Z3Lv2WZPIM3D9IsMDzhT7xyqiKrZ9+VC4R6h8P3kMLj80KqI9ULj14aKeWjWbfUXyyOGm9adhgV+hid0JNXBRz3Xo5QR9knBsTzMkVEch2kWCKl5tz7kIRDGF+NTgv5OL4h7ESEWNliSXiCen9IH0JlVasvvihs7gO2mHTJcJkttp7304D0Dp3r7AXyERiTFclV/YvAbgbZEM4g1GiIvbrgPKah97lcvp0CDwRnRWL0TTmljchkGseAtruyU7cOiJbS9eC9neZJX/926+tlnoTpWnoOB8VkfwixJOjU3E3kK8I4IzE+qVg0k/lPuN/aO+sgh97Ec2IV50g0NjUIkp2A0b83+cAvRLanfZiLth4QO7xTHOXWllsO5XclvvcqL4AeQXeydhdfqL42/IVw5zOauxQNSox9l19qs47nILdb7Yp2mRUEJOTQ1UPXk1ZxQ2GTWXepOdb0SE7ltnmhxoOQYqwJsEs0aY6++ke4QTUZpSQ1T/Ay2wZM+k8dJ/uM16vAFAuzlqrDiT+TPqeMvm21PEIsshEv6shnTZySwctCuj4eMRW4ORq6u3ED7lmuBm0nnPQqISwOvzGkd6Okak4sxf6BP2A3+KTUAclxL5+e5zMJL90a0UOl6M19ykgk5/P3kityt7Phl7IwOurdzHJZkPrVcT4feDDnpG8JRjs3asFma2VVgQNSSXWeGu55ZokMGDwLRkX04d3ukYl/BKcZxSobrDIhCCtoT0A6LELF2KWNEWfMcy09/I2lABoqcDKcuFwHJLVC4471qRmb4tvgdS72BR+k/XpqckoWyJAV/rf/Tvx11dAY0R2mxCPqt47GzNfpcOqx5XUIAg64yNgsk3LucqkEdB42un2VQi+P8rYBlw+Rd5lZpVQqGeuKWyu4IEm2q+R5+9fRoBiihlBD60YQIgB2bww7sqxEs3QXH55CNBOSADzl57bEXniWs83pS0hEK4jInsjQ/+rQo12MYRd3MwJdIo65s/4Lb1K1/A1L+5wDV+sxa1iMc4qMNWVyXxutL26w8X9UGscVEtdu0E8V+MRtce6k04ZGlgFHbk+2pMHrB7boBJf/S9iVAxYT1Abu9mXr/OEcv5gEyjHuYS/njOIZobErdYFgEn/TQFmJeUACaBpycq1gRKoV8O9Gxlq3dznuCSTJyC40t89m62FfLknRdQYc9HZyCa+WI8M9YCFNgDnDyqgsWbaEGNQYVDUvBbBWppxuyK2z8C9jhJoMETQ2efmoczZLMPo66ejlAmVativqacr2qmvQAdI8uDwVCEiFEx8ZORVCw5PcqahQm43Q/3FQm8u5XrcOMYlIOVyJMHgJ/A4G+u+MomhSmNyx7favcJKNMXxx+2RTvHpLdRJdvUb8RyyhZYWjmtEkLi+cZH9AHJAzcCSPId4/9fUEb1T4Jjm/IrSxGZe0VR07Bpg76adYs7C9U0exPpSO06i0jNbVW1UlWKLtHKM7MtO4d1rcbUT1DujRJq4muoETGYkThKDuXMvP4adHoFiFJYB2Lc2TuOPo9QIIEwyxUghqW0/RYsKbukFUzGiaqBERdFj5ZYaCBDpkYoXVIbEuVDQAF/5qqCoHPLuLe0DQFcNb+5XcFpr6uvl5I2Ex13dmrqfcmEN6w8t6Rel89b8yALmHoGd/+S+KPpMsi/Iz003mJtQv2BGPLyGJtEzwbQkujeyOpL7//gxGUMEfRqQgnm3I4eIIjp3wsh/zKSG9HXB3dXncUiZ5pZklRj5xMNE4G1Ve797e2KzWM9fqbg6f2tv5+0WTKwHp4bi13RY8aSci7D4zN9tUWTcPZ7e432/DfwvpKdRRmeXN/X2389mKkfDW2gSylpxn/MoC6+4N9CRQJOptXQeGmvuWOjJo96BeFVFe3h1Libs533I8B477M6SavQDA4dq53yTGXWuyArBBdlH6ZywGP1Cb1HVCBTY5NXahm68/zbdgc1BKCyVco7kXG41kymjOL1jbun+Ykev9qDInlZL5duz4LZrhOBrHiwBYri3UCD+INfu3bndvS3lstNlafGZqAH4M+U8XlmqWD0EGMaK5L4OV7dqyOB1mNj17KBiKrq91HWdayluxuv1qT/Rxh6LL5w8KfTDFhwvIUPQpuSkNnGW/eCom0TFrDaNODssxK+Y27KYFXFklKo1TgYvgYDmUaBIhaCHJEKdzLLi0HTzeBeUcHrcKm1APUWYUK0HjRa1MxkQlgny+96sQugZ8Kd43rB4FHXgXllzhJTD0c8/tqP+pvyT3iYKCFRtYLxGSNLDzGLwBJV40F00kCY8vpdciwuSGHFx8aZDbei1UMgDSg7E/64RKyB91Y0eWeIvV+2XSetQbxxw5e0gz4uar+7JNDZMT/7whG2+EN5ySCSqPcF2Q5nj3gIMMqV8MpRJJIfjaHl4+5zTV/HjdxMuELi4OkyT9Qd0OBetE9GUzUox2mNnNYErFVYV2WlLuhH8u8cStKy3cHVO4kIu+1llPph19n75qVQMPqf1wObkqs/O0cVxN7mHxdpJhBvYHb3Qaqs6CoORlyLBtEt64JxH9g2MJ3jaK0epEJPEu+85vY3RUF2/Tm/CCepqOaraBYvPzpFqZE4qCpFw8RtnLxp45k689qmtNSWiPwau1Oqigu7cY38eLvFy/BfB3KQZXFv2I6vbx2ngVzcYkLilbfwkOiPbyGN7l21/ohqczs9Dk+z7hKEoPAQisLVHHjShtJJl9VP1fT6CX5VWU/rU5r4myvuyBbCI1M3Yyp4vscpeOobXIQlBEuPo1fZmRtiYq8iTXs4kYbJXi+4EGGZtxktg12rgFANj5wpYSboDeRaLiK4PWftT6J+eBqstLC5MJuPK5x5ju0pR/AI6Jjbc3JJJ0ilfnOBfoa9qhC+7RYR6Q0Oi+o6JIIMsZZEVmCdTjgsNPEUxRA5HQqIDOjoWKSSPTYlxw/dA7s6Ykn0sEdcZXOoPX2LwKsel3SRVH+lXvvnRBqKhvVPA+Uk9LGlzFEewk7TvryrMSlUJQy7v1FPMur+xmFM8qMYyNh5tofIfvubVIlGHGDPB/edGRJEWQuRbP7MebNaZznw5Y6hdc058Qv8zpog5YB3fVh5g2qqs+upO6CC4j/JJZ82hFqb6Z7zaV+TIOIPCiAbrrqfTlEcDZYhLtPHHPGSmdYwXzGotGxjrPn4CaoWh3J3+3UW09E3ZMOZJrPE26yQtunIx+CNvQytpbgepI+MpJFGO7DAy1PbmKy65qiJw2v96EVosGxvQCeFhRE5VcnX5H+p9/YImh0rWLO2DEjtHtqhUJM06CilUUAoe6tTaFPdDzYkJtVTa3s6ZoaPp8jvGWRNzACMTrYIAQcIex7IYuVrsrS4Nmpv5mlsmKDijrkvdcjBgJeNptCzRB6KeyMxHqxm7MF5CCoZqvJ8DgBCSDZEdo0p8P37/ErY1CH5VG5VkA0N/vwmYZAtdpkC+BadN/i5Q2F9bTGLvk66piIWHf2FoaD7X39nfCBswdkmdp6CgeQUDWvdZ33iQ1ihjQMNSDhOAgmvcMUPcJ6vVRUW2S++e4BooEpYdR5BQHpMwbTsUnoXDCMil7EP6wNdqzUOZf7WpiMO92B1yyUVSmgGtEttSg+1RuVCLrK0eig+73gcdJbPZrWuXH4LsAcEzAu5GLH7DSh5FI92gW08OPkkmWE/4SP91pvsvf3pyST1zYZQV2OUGhagBnNfWDvSHpXXWopPAY/dlrnu0ooqVtEvXx9I3HSgYpFimaG0a3FeXHyowykPG+1Pg5AUrmU86qsP4sCb0Vs+yrH6G6qDTNthOg7cbhTU/Y6R4dvanDXAJU5D2CddL7XJNyeCAgZrZc5quuEmE1OpX0xIZsv8OOH0hxTIvof+1Ab066HrfQg6m4rdGgvS7obm0r4+cLQTCM5SShhgLDp5xt7UPENohRdv3nlOJhX96yQsjtLdWGqvH1jCE3V4oH5+2Q0TSKR9TqBRcOIyazlXNxnPOS1P85uro8lnj063bHVTqcD9Lh1Hlfm2X+zCQsEiFwqdLt+a5UqHLEGGyuVo5EWTYZSJMQ/dg9JNBEym2v91ax1EdgunToKa0mpS50VaAUuz0jfjqhem1S+FuaslluFMPt/tYQ0b5B21b2hZUsHYPbT9v6w0TqZzriS/33lKdvNWhWlsgyB140FV22mAjpivjR2pHJnUq7aXCzO6BVV+h/LJuD81aDYjfASkUXBaO56AsIFFOkQahTShxEj98Wz830ewli30AJqx8CPMwETAHuFiwiBTnzBqH40Cq2F+yJHOJOPmvcli6k649XNzD9ppFYrgO7Iay7+OFhY2AeBVJpcrmm6+95GTG/9sECn5yVFT5rXfCkef0zDWGF/ogPI9NatsN+kxoujQnLFclFyXQkP84o5MQjtmysqJ8bx7V8ClI5FfmG3xObUqyLriEvPoGmx3GUMvRAJSY54BaDeTS0/Wb2mwslJ20aA+P/H2CPuRR9oWaa3NZ0HmK2yRQiUwv1VC2FlHe2KBfzO4X0MUJEsRK3V5Jgaf5lFMIMvPxxtaSR0Ka0+KsOgkAlNlgVYvGrtvPAUy3AnVuUb1Orx1iaWIKhxGXuH6kK06xUSEMufMbCrmLUi4INyTvgBrtF9WlavoEIaAXV3GpViUwh+qD5ye1o8VY+9+6Q/vwikbnVagIsLoImrNBmToC3w6VRrJJBSiiU7Cj/sBujQ0DMT0bqiWiGAZDtz2SW4ZhKQyXS5vk9k6HB7gksia5oKlma8ad1bfhnHIRinLAmhbvPGa0tn6bNZ3KoEZoqh82yp/Or3AcuvTnomHxgFdYbvDS/cbtiqkoqAmSyfobZFRL0yskW4faOg/MrXi+99fxbWN19QF87l7TLIaa79yeaeZ+PwHEbyBuU6QujB6tzv9GjeY53sZHDTVkzI6F4UuJU3yhTSXKAH7hzEXEd++x/gf2ZJNis/RJmWd3wKwp/LMPQ9KMu2R2AhZkm5fo12rB3uLNHdoUswszmRM2cux9DHmpH0G8QThutOq0eXEP0mOajDLROSF3LAKOIDARFnhs9oyyBYCwjdj+SUV2qtYSEq3y08KSTWI4HpfZZsWN+D/lfxVDQtvg4QPHJdMW27Vj34eyWcnhd3KHf1+7JK6ZIsco2TKcCvaanGyNugNTQOULwYNzcgTBsKxzGgFv8YU+TpdS11/k3LC8CkrwS7jWcLVqb7CtQhtxdXFoABMWBcvkqIsetr9QBWFT/7VcGYCYvKWHkkAkZIpPiCbFDUedbpkCM0CayzhXZicFOjP6BV91HQqazCLzgkHuAQVyLMh8Y5lXDt8wF9x0Huqqy75RebE7dTE/DXrirI06eQR+O8IHhWvMLVHmQ/u0wEkX9/L2EXBbOYVA7hcJR5z3cjLEjPKbVG71PKlVJislOV47P7+XJrH30HjHj0hVCmOBDUZz3CtsxD5ULaGxRFEFX9pqCO6T3B/InvkVZDWZ1qtg9Aqii5z4xs7tXy6Zd1j7nSvqIWGhdcBy6URwZkEuhSZmKk2M9SeHYB9/iHo4WsePb+jxRqFVXHC7HAgvm9Ru7olB0EJWo0Rf62bGb0RQFr1EvPXSYw/dUjhbmAoMb/goKXJS6QW5EG6HJeqaKtqGc6qOJ7gpBKu1Qp3fIZIrA/BP1Tgkr/SUK269x4Q+Qcj5jXJEA4jpiU8T9rqITJTGUZBT51ybiLCWEBHPzCe+kz7ZrKgXEJ7/iGumt90j8/ti4bUPKY2tw+d6bKv9Gkzbvy5auoBc8m/JTN1AlB06kV3UmZZDORUcxOrvsmr6A300TnnG4Pn3RrJ8A2HdrpWHb5WHGLpmyRgg51wSwsZmXXP91zFkupL+13Uu84vsO6GgIgJmCh48KzCheK+tvp2E8BcA1R0/dk/Ury5GDRUrHeqqW2tNR/NGX6EQluIQMzJLYYtyJyrGF/vJc3ycoRBoxDq/OGjQpUhwxhNytJ7HUYXuD7iU3HmYLImhgYjGnQJXy9NAlNwk/4EL9bzjCC19IwvOASFc8a+8mYuCHEZOBAxjm2hqvIAQcMFSCzSMTQ2wou2zzlmPLxVVmsYgIfjiMzNqzlX9lf67Y/herR3tVs6xy3KSRuRVazhWLKtXG007rFRPj2XqeU9d7zO6AK5/rDtsGV044qfGEMS7WtmoqIRqy2sLiUb6C+KrNQxE0xGE0YsGegjl2Inm5fwDaZwX1MKo6lAaUvTFkPEdFGc9W/X+e0EGLEYkZIRl3ZbM8+eIZY3JeuryPuf91oS639EabpJDv6LvjvRhNLaTlhHR/7+pS2An3S/51D3UNGt6L/O5/h7GSxJhc4BWkdDeX+iafwRYjbMBHHrhTQAq4QLF1TcLb5ucW+XpdisVDLzvuimKQNItC5B43/2BQB4BvfkTh0YajxUBg4BwnCi9fEeLdCO/Bl3DwW1Y6PBSw1uAxgvQZaaozw3l+R0boJ5Q2D1gT92fHkYavMYkXsO4Xi1aZqTAPXbRwPoc3ypoPQJ8SxCZnB/cfgx+LkLqPVnysx+ItKQM+tgBfIQcLGFSDj12HdFwauQMt+fXvdtXVThaMAQCbRcCV4d5mB3+I76AVydoZDS24ZM4JRSmi5zUoXHJcqnw7ZUE73f+VziDl4dnaSRnLtvTSssvZKrPEX/601l9OKYe4asAQ/u9+l6oI+Y1D4hRnxueNHHtwVq8HUMLq6EDsMYK9TUMzcVJmWxF0DdkDAMJf0vxBN+RbzJDo8AE0iBRgCx9uOg5rehwn2GmYXun+LSShHLGDaP+j8yDC2Yon1cWtGMqngTrT14ia6E7fqqZ23es/OSQOCdXRDoiHIms7sTP5ckNuby5KUmNooh1sOmsJZo98zDrKbLM0wq8Uzs5RWH19dZ2tgizgRcNZbKuTJFn+jL6KfWHzTRZMBEMHmTuRfBJ6WTfZ5C++wY+Aa7M4WrHZgvpZ/fmGm7FYkmV2WAKwn8tvIH5LVCwvv50KZ6vO5k9yoMCAzSvO51UA14MCYpHtehxVz2AdvcdJAKo82AvqkluXiD/GP9IkxIQmnbP8Y/HV+PZ5suNqU2OsgKEACN8unZxXn9QKOwN/kcTLy1ZZt8/5oDCO5QiTmoBOxSoQ3O2xQs3x5cBHpLnYJMHEtGKLNTlFG9IH2zH/UQFii+GXcB1ENICzAXDcQAAeR1Vyw9ZfJkDRw7g313p1xwOBWxftcIaeJHta3JhCwsT2DtDZLNuk4fX7EEGL5N77shJVMW23JQGfg54sgT2wYfcSsb90rFgwrfprGeRzvilXmelw8ENtlhYpR90OSt7/74SD743ZBPhjt4ZGTlFXJpPEMFXUBEgltD8IVxDDSswy/fHV+pQb1WUcioml98Y5Xtq2yBThHQlVLPxSV/kb6BYvmLFWdz4pj/7Nd/bhWzqZW4IbazML6Ue7kYeGU4JGHG98DEBR0rHXDOQepyZgybKKsc9IfAEB3oIbBxD5UfOMXOBOHwwjGCHJ4hiRTwBnO3zYZnYjkpvEoS9Pxzi1x9wDhTTgwLLy5U2LerruUlJDYdwhTxKrkuOtsWQ0V3lu2mgq6GjJZVnIMxddy/BE2tmHBhuxcBZoNpVsUNPrVhhI7ufKerZ8cldn559w0jfebt4WSONs/gB6CcjFA8ltCSbpx409aK80g3NHV+YfzDrtQ1VQHsp/uGJUvS7YXN4Q+xvAHHzQVRsRq1aul1rO49Fvt3/R8f6ZAxgsZmRuN6kgwjlZ5Qym7y3+vu5VRtSCrsezxhqWwfYGM6qPXI6xqVAIAaInlD1lnMNthG+/u/eFiiqt9HLR8MtSVnr22VfQyjJ4E+ysBzaPXhpHy0fNVKg2XoTOaC4jr1RVrMRH7XVNvlIGIDK0KHDmSlgqt+sz/NZ5e4KinUCybyHiIv2cWu2nwxEb69mOaOOUEjUwgV16pxXDb/B7Xt25AKdHo8eY6sojJYnzv6BwZW2uq8kiy+Tgp6cxvE/oNtNpO8quOLrRNK++WxuHRQF7klSuXWg1mhvObzhGUNUGNzvSIi42QUiwrsOnoXzSOZaSo6umVNzeLrdw2PV/peDXjjo1wy3a1z4Hbd4WjeRb/GrUjemtvWwR+0UX8ZiEOpKhie8ym7kZ/shbUMuVmsLA3cQlYZq88xQ0L3I91237oEZQeNhYy8FelJlhpBG6zLfPRgiS36G0SjrdqVRAVhd355QA/4+4LKclvF7f+MdtwzMZBER9afLBuz8oodO9YfNoUTHSTaGArC1Jc7jOzxoKoZSS39UFIfnTdwDuWX23nMmVsw/NAG4JoEr2vFRwBtNWIYBp0G17K1dZ4dt4nqZvlGHDsJED1qKt+O2uaojDJN64U4KfUQlfabVMXdWlJmq2AaPsiQ9M2lCsheYY3otL2JVJ2xh9j3QupvuzTbdgD/MCS7fq66Sj6Zb5VqGwJ71Fjq/lwDAX+UcdQ8tNDwRnkU6G2mssRWQuP5U9Kty7AAfCbLp/dA4/axdjokymemIjep1Z/cLThAxkR0NwHyzbFlOWYbGhnZQDhmFYslR9RAebpH7W6GhL3G+nmc5YdvdO9geIQUuOB0NvSFtgiHa6VTPXyRnE3Vk12iZzb62I7qiXHumYfs5g1y1K7e2YRPQhclS8YyeFcJOeAD30VtX6brfuxHPO7f+ZiThy15x6hhPP/H/KZW+in129AKyQHMc/X0e96d0u6ztIpVZDSVcOAkBd3jeWY12MEmBWXV76auPnp4QJFx4LLGnyJKnpYYzurB9J311p0RepRC3q1d8xnxVK66ZN676ePRYsiOlPrg5dmwbcAcyGcODb+wAtawbJ+MFpKLpcf5eT9YaIyCn06P2/ePE8XUyPGYdMmprx/JlAFQtDiqDaXirRiZ5DvK5lo1VHAGdwZ6x3nmknaZfvKz/SzU/daDDuRqUbxHMKFrzIhMWQ/cCS+cfZrTxPRm02CT0JQUsi8tRXNXk/jGrDem2HGGq03qbFdyOWZBjfFDETdRBaBWj5VlT5VxBBAUyjtgjyU192DaojEirXtHuXNCp+fHv51pDxJ4/kbJ/P+FCjHA4aJ5/CMWCZ+8kwvYvvQHazPptfZsx1tV3fqbJE1iEUBJptupRJWaIdvKW9dllAgN5u/rsnFMdW7Pz/kHMZntr8PcyLwfqq3KNHF6g/NoUimObLxRZ8LZ9dNzX/KRXzZ3pYZhP6iyLTLcmxspatgx8/5/NQECtVcd9y59BtyyUL3CqEtbSI2WGWuxcizdYSfgNaXtIIk7ib3YHkfhyn+b61Way4t/e8kXtfTEqIUhXcxaFqOO8IDs9UNwg35fVP6ail+iV3M5idc+nUHh3qf2t2FdgZ95b3xJqw+XSYNiY2qnWljVUrGvBsaGzkpQGOEoiQ4gVwNTBhWA4UtSkVrx3b4ZG0zHVbeOY0VBPhrN2ZhZ7OyrE+aRf6mCb9izMO4deLWZlQgCRUeXOcPqRfaCv03iNxSGtsxWdTB7AhTHykbLGjU1jRIZoLHoafjfwgsj/oJpBMW8HpQR72MOPijqiJann1tn76yt/vTwTgQqF+/xT9mwixJOb0B/8uYtpPgMqwW1PaoY0iN22FMi/EezBpt/y+XnWTrrwwyQwa/q0mh+KDajXUNmm9HOVo3qoajMn9eCsTN34t/R9L9bhMW2hjo0fOBez/DVOY2MkLRhFYQ7GiNH5HQotpDTEolYtuZ16GSAtWJzpskT4WgRufMnqsZv9rzYzbWUhLI5Ge/TxODD/iZDkFVVzzX1dpF85kjg7opWaEx06xOhudc0tpJKjv5T7kuNyQgqqeXxly8Eozz0MN+wEjiT6l3Ivir0aTZlhEd4sxQhXjBEIJ7xLvmsZiYkVMJX7HnVM3EdAn/TjN7IkCVO1f+mXfH8Q239LwsbNOL0yfGgWkSnJ4Q+rEO2qlsTkZJpkIUmr+6So80cev0opTnhmZQs+CFwFa6Iv12O40ISoxIrLFZ/eoG4nnjapaz7bA6zatxVMy/y6K5u7SS8s+LLE6RW2uPQYDvJFLU7zq+BfHDibsyWbnEIZrKR5JxtzFTykG74TnkHMx2q4h8ESWfkqCdOepHcSwxEGXHux7+yqCdbZ2bxCeBrUopkgimtV9xGmlSXVNmxUD9RPJ4SlfOdhAoJTSrpecNgDzoGAsMAxuxN5wVhbEejZPz/zAw0ptbGrcRX/ELqxr4Xob9ek8VgBbmiKbyrtGK2so5Ar52WdvC+Gpya8O57lt3g2FKV4rAVUqX6vpr+4XLpzMBxvUF4USBoaSJiH6UKzLiTmsuO5uOwPj9HrOeXl6l7WJakqkL/wgmhrhYsDh075UJEkW49nK6+e8/8FkkWhYnVBR06WHUkmM1yZypKw73pNtu0S34obWp5Dtq9xQss18fPYHs7E7e/HPqLx7FtTlm51f0+Lm7+YZaMc80IoZtxPD0Qi9DsAvJaPTOB+YzHs181Aa7/RDOCCJ8r2abAO4rEVuSX0xKkKx9+uPjGWmHect73lN07GZUb5FpgKqBfVHO29E0ZVFM7nDirqUU1UPwQXxVqB2vJJ04///tIov0uTK9lt0e31zc0Tk6b//BjGWAJCZCh9FmapfBVupquEvACvU6zR82pIenicb7E4+/TKQrVj7lePmdyUDCpfL+6Drm66GR1uRlUBylrVCHIlVRX8Dn9FWp9sWTYl1tOLWPSmpfkBF+oge4MPbhy1b+rGlZg3zk/DcbeTrjBMWl7AMtxLilGcU+ANYP8lQgrZmKuVhz7pHKFek8pHhYgntE9RttWxYTYh6z2vVmFgBQ1OxchHh9eS+7Ym2p+Twr4mva3R+SIlO70S+3UJLl5TxGBJVrOEZHubEMOH7guauNlvX13gOwtE+ce157t9V/IrJVPlT8mTJ62wd9uVw89zilBPDEpU1JuQd1LoebHHuAI/S25iqjy+a/6Znb7WoJXPoLJ41B8X85jtzW/4ZC19jwM6UM+DZ4GUKD9w6P8CvX49jjn5ZQ4IGmWzAaN3/q0K8TmRWsD1xaSPdXAnn6FjRKfV47yGPFkoHxyzH6PRNxRLr+tDMLHm6NT69iJ2K/IJkPPOGSoCTMWhrtZLWd+xU5HGxsjFoiaOkxV7F1yud8E1ZWStsxgxakdu1Kv9W1+hE06K23hlkTeOsOnihDU+jZTPjWOxbnM1Zh2c/fROnCTWiO7flCrv/N+JvJlBpx7zY8a+8PtEs6M3Ot/KmfA6ldutRD2Pfbv4shLKSl+nvm3vZDu0oxKfzRd7qwynMDVo6D1UxfgSfLfVaij+RrF2pL/WizXH+PLilR0pllK50mr4QURc/kD+DENxho67tfRJYSKXmzAzjVNWOAaP1nKhtoGYMHOgGhMar4RG4RIDQrR3okpCbXWcvJ5+9jJ/Q+q1afIoyGY8EhykQAZDYY+dTQI0GliqN8xM/qodCBc7/XVWBnWgqqZnNPD6EcsUL0IRtYPg0lu4EW6nW/iRx5GWWpGdU+myWca8bZaW9K4vfxz4ch75i1mkFjtcJRmv3DTmTLaq2RYrNuKguzZb4CNW1Ds2Ed6lLc76l77BXi2vYAUsbj8M57rRYWHo8gptD5ZRBBPiEf7jByqMZvTOpCy62O2r7JMiShTOsrc93573Elq4hDCI0v9VW1EL388o/UG/2tO7S9Y8VYlfPjmX6bbGMF4QyqM4R4ugEAp3YZFIfUHq3O4xO5lX64x8EVjFh+kyNUb0qDYyBoJUG3K+tGu/Cz7hxv/GjM3sLkTzCVeflaLCcvw89/SEzJ7cXYoCS55cBOO1zfnUWAgv0utHIn+eqZ/fUFjFsdCaQ+hFcB7YCH8klWNvTN557IFWsmb1t/Ilc1Vb1pMn2tFv2b8AvFuoxci1xcFL8E1y0PmTE352CU5qEXsOUxclvCMuNAZmHnu01r6xEJBypm1JIMhlhgKciytlCg1xZVv4Hj0yk9/syiq/SSjURU6nBI8WlqD7ahcqamLGiIvmZEh+hiY4nuDtr1x7RtvH/Hr1j4aLcvUllfiItzd6fNDRuTKfGjCW2P1X4C9lRYwcNSIp8s85N9+cLR5Jk3vkxgGi9K1i6Bqj3VzujWsLGWSu8fhErqy0uvOfJNFgwV3qhLwENwYP+jwmk1fAxVI/3PZQfEYUcC53U723CaCZgGkgAt4rwJ8Fq5lDeJTzWydpZPQud/f4utvtEveLYvfJTucA5ZgVjNzdQnu7+f+/6csH+C/la+Qz1Ie9wDzTpazzvpYXMeHG4a55DZ5fqE1jnPo8xE8mDkKcWc/6tB66R/uUWRxjDgon1rYjnjgTGZt3GwI2jws8idpBcv1koQAcX6klV5XmnxSZBWnDqxn11roGJfkOtI6IAeewEHqMo8XNc6Gt6f4n2DuvwJdp3qU8hyJPuM6stA1e7M+UujiVPv5DfFcV+A6ktjA+fMLm/ADqBNSl30AXUHegfLy+9TeJ2YkhzW+ECGUpikRKn4tdpyyvGmb1fEBKA3fr2vZiIJQWl9RMx34Fjb3GuyStp27xolIazO3e+wcvPLzWsKx418Qt+S5Et2467nwuYycV6tSZUJM4Gnvu+OcZ85ilSO6ldFGKISaREgptrXekG7+nM9f//did8tbr69Co+M8PDupZmBjH6dCWc5JxSM62PZe/34m52dkAcFvUtU54NcdX3XxjwoP0lb4ZmtXEjA9D7s/jKB7mF4ubPy+AOygTy1FlJTYSPtYn6XoaeTNhM9jayFGY1zdnXESEbAkfTxCwEqGnQYomjwAoftOwk6S8M0e0fTtSEpwXlgu/GIjgNoVM9lt1e9yQ2X0UYc4GsBjAUmKrZMf45O+jvILFLooxQR+jCwGqydXF7Fa4e3MtX/jCl0UPg/udseOugh09d/Douk/H64YRz56PDPhhRuWvCm/JwACvCBQhBtf0qrU00dE8rIlxTefXMx9bbDu6b0QWvxppO/JoOAfCR3Wju7rcyLZqhfvfwFcm1jSiGI2Wr4fhlb1ofHwQFyKzQ75rjy9+cusvPKwLRsD8Gf8OTxA5En4GUjeMf5N1NKhoSDjP4jSal5LhjaS81SHkSOPS+EXzFPa4SpHakJgE6K6sB2gnFitJDSstLzQQZwIaRcwpx7NqjI/G3vuCWERZu7/wqfw6OvfEkfSdgX+0zaOsXCm7S6GrRrISgDWrzE5D4hVs7F4g4wtSHMph7+Dv64A+bjbIR495QoqocF8O/YCFike5zvbTHgISRzLMHoQrvbfGEHc7v3/mwvRMkGuHoUwnTi87Z2dhh0UKcgEiMnOaJsi3TmSmnwGJHze0zNi16n9XiM5bQG+hOzDwef62x+2eSAsdAQ/m9EChPAr69vSultVGvhW0VFFWMNJhGDy1JVhRKj75d2z4+bs0kYZ0NBacmFg8F4nuj0XtwXz5YwyjYw2GY5Q+5BKjNOE7pV6OhblSL6x/ud4L0cqfZjwsOoRsIq0YwoZaeIrtLgl9ad1hraqAGhGMnInVeWXGQLquvivC4mjfZreBfcWHbR40mKr7D9FO8vV2DGNnbbilyxlz/+UJuHy6HvedMIj8NzOuhc/s/EVAcQfuzIE1g26S2rXPquhELRooMl22MbvKEYcYVRGxL7qEtuHJDEvomDfIFtgcLDb2QP5gN8k8/cdl680JRa9OcdaoScrlYIHGNL99mgZL+w5zASWMUOByarRNHIxH2yab876/1mDne+uYibqcV9k7Jk+XpfwGMaFdmhQY+SNJXw7YHLdb38K8CekroOYDpPxUEoyDZ1bW/pWxpmLIqxWfL1x2gle4ofRJg6yOM/CEr7S1qRlCak0mYe+63IQlxI0N9eAFPXzQhzWoAn3rKGts0OJ/b9XmAkko4mho7z3cxt8rCxpi08Liq4+md9rNyttL/odD/v6T2JnQU4uhC5gb44WKUbdYsYb3rsuUpr/PXp6KjK1r//qVWHePLfksH6XygsoPiHC8zQ9p/O55F3+iH4IlJ6zaZEBJJ+WDEGeCHe2sQRkkDegqS5a2sdrCzsVf8y5X4/jZKIY9dvdRcY4JzN/bAEXfHmb50cqghmp2ZxrsR4xvsoYEZmFY2GP9h+KFVN33q5f6zdU5y1zzFvnUFWQezHlB7ypohxR9MghYJrnmv31jwpPO21iGALWsbXmMeXUWBYtwBLpv1P5EtePJ0TW07gb+kjZHbc+ecFg4I4grQ/1bxmvcT4Gb0WXcgUR1S63x1ZiZ6HJ1Lmvm+94Dks0s858HhLBu6tFawzP129mxAcxzoRBxgMfnl9nc8dBoj62zaCCGuJTQYDnttFO2gii1ibLp+no+WR56acCzX8RlQXBX42LsX1HUmsKA/RY4Iu2oykDT6kEr8fryBTHEkydVGGVwjWGY5d7t6/P4evP+jVARXrDKjPoFwZayR4Od3/D4hvHH/7KJql+9KNdzsss294gcjTg2GjEzqVNQOi7T9rn9FR2qwS0mCBGlD6/eGZtLc7tnSfqItcELZcQ0L5vDqztx8ciaIKAyZhUgr8rc75mqNrDRRdpld39OBscXCkjUBAwp78ldVPKbVVlhEOrnjsZbZLF2BjCU/FoL0VLhkAUVQTlrIIj97QHsmMN1ylvOeymf78FcDnmFBs8fPZ9i3k27JId85QcGqAmKtZ7j5mxp/VsyT1lJYHtapN4AlOb2WZVZdh5sMcfc971mpVZcL2jfnmc9DT71cWWo9qDNQvaqdAuFQjmnC7pYQqQjMJXOCpofeBjNY+iWqDVKhyclHxcMxlyS5tM36Rkco4N25PuyhD18rJ/8jWdP/XGxMTigWF8A8fpJSW0lVLC73qZxhb9TVkhazu6DZPG81LCTdcdTVXVXSEXTwqQW5U4omTtji4O3rjAX/IMGGd19AICEEC8EzotxhErqRoccsD+vGoMhGtQ4irzR/ioRoKUma2ygbGTgQlB0nmepHcB2C3cTSH+FpOdkCdajt7hLGdCEtKTJeZ3NOhoXyf0ndiSc4JP1Z1IRa96w2k8BuMwBP6agKAecBaVkeMoOmSAMlT5uhJyYdeHjaagBzhJkUKBE3ZHjH/ZIsll1s6S9YFCFTdUaV9mzddUA7FkShvDlcTki7NGR24Igw7MaEQo5vqQZWIeiL5ftACb7PPecCE7kLlIXfl3ClGdMrziext9HTINNFhGKovTdnj7lmUdjsgUaIDo+a5y+V9kg5OdYpdfqUUKGIGH7P2LlgM6TK+0mprHDKCun+opJNlQSTZ8nZI9JUFSgw6UlI6w64AuJc1he55YsSSL7As8i7+CFbPlLSFJ//zpzXFn8TayDd+H8bsoK/dDoALvcRz8zBe4AzeuaGYKwQERbjoU+500BEcZbTZMO6Dxn44QZD3KC300KFfFEoYHO2rx0Ko3/S1O5kCGPQjuezIWYXhoJ2Mf1ZiLt8TNG28e7Sb6T5+de3+VjSb04P/Azj7M73Tfm72DQfwCNOSG4fewr+8mHgcJus3Ik3pa/cBNy+AD19JJEsngpEd10KMkAd95rLQK/cgA","imp":"data:image/webp;base64,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","wraith":"data:image/webp;base64,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","necromancer":"data:image/webp;base64,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","gargoyle":"data:image/webp;base64,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"};
const MODEL_LABELS={brute:'Flesh Brute',crawler:'Crypt Crawler',imp:'Flesh Imp',wraith:'Gaunt Hooded Wraith',necromancer:'Necromancer',gargoyle:'Winged Gargoyle'};
function threeLoader(urls,done){if(window.THREE){done();return;}if(!urls.length){document.getElementById('error').textContent='Could not load Three.js from CDNs';return;}let script=document.createElement('script');script.src=urls[0];script.onload=()=>threeLoader(urls.slice(1),done);script.onerror=()=>threeLoader(urls.slice(1),done);document.head.appendChild(script);}
const installBestiary=function(){
(function(root){
'use strict';
const THREE=root.THREE;
if(!THREE)throw Error('Depths Bestiary requires Three.js r128 or newer');
const TYPES=['brute','crawler','imp','wraith','necromancer','gargoyle'];
const PIXEL_PALETTES={
 brute:['#a49da3','#89828a','#777179','#65585f','#493c41','#2b262b'],
 crawler:['#b3a7a9','#918387','#76676d','#604e54','#493c43','#29252a'],
 imp:['#bd939e','#a57586','#875567','#663d51','#4d2c38','#281e27'],
 wraith:['#a6a3a7','#817b82','#676169','#514b53','#38343b','#211d25'],
 necromancer:['#211a22','#31212b','#422c36','#55313c','#67424b','#81616a'],
 gargoyle:['#b5a7a9','#8c7e80','#73676c','#5d5056','#42383f','#272228']
};
const SPEC={
 brute:{name:'FLESH BRUTE',height:2.7,baseY:1.35,headRatio:.17,armRatio:.59,legRatio:.34,shoulderRatio:.84,posture:16,
   forms:[[0,-.19,.29,.74,.68,.54],[0,.46,.00,.84,.44,.52],[-.66,.60,.02,.36,.35,.42],[.66,.60,.02,.36,.35,.42],[0,.89,.22,.27,.23,.28],[0,-.71,.02,.48,.31,.36]],
   anchors:{pelvis:[0,-.59,0],spine:[0,.05,0],chest:[0,.56,0],neck:[0,.79,.12],head:[0,.99,.25],
     Lshoulder:[-.70,.62,.02],Lelbow:[-.86,-.09,.14],Lwrist:[-.82,-.70,.30],Rshoulder:[.70,.62,.02],Relbow:[.86,-.09,.14],Rwrist:[.82,-.70,.30],
     Lhip:[-.38,-.69,0],Lknee:[-.51,-1.02,.07],Lfoot:[-.52,-1.28,.16],Rhip:[.38,-.69,0],Rknee:[.51,-1.02,.07],Rfoot:[.52,-1.28,.16]},
   limbRadius:{arm:.25,leg:.29},jaw:[0,.82,.43],eye:[.135,1.02,.47,.048],skin:'#736467'},
 crawler:{name:'CRYPT CRAWLER',height:.9,length:2.03,baseY:.45,headRatio:.19,armRatio:.89,legRatio:.82,shoulderRatio:.71,posture:74,
   forms:[[0,-.02,-.21,.37,.23,.78],[0,.10,-.49,.26,.27,.44],[0,-.10,.67,.23,.19,.27],[0,-.045,.31,.25,.21,.36]],
   anchors:{pelvis:[0,-.08,-.58],spine:[0,.06,-.25],chest:[0,.07,.28],neck:[0,-.055,.52],head:[0,-.08,.72],
     Lshoulder:[-.32,.04,.36],Lelbow:[-.70,-.23,.66],Lwrist:[-.91,-.39,.96],Rshoulder:[.32,.04,.36],Relbow:[.70,-.23,.66],Rwrist:[.91,-.39,.96],
     Lhip:[-.27,-.13,-.58],Lknee:[-.66,-.19,-.70],Lfoot:[-.80,-.41,-.85],Rhip:[.27,-.13,-.58],Rknee:[.66,-.19,-.70],Rfoot:[.80,-.41,-.85]},
   limbRadius:{arm:.092,leg:.105},jaw:[0,-.20,.88],eye:[.115,-.012,.92,.035],skin:'#695357'},
 imp:{name:'FLESH IMP',height:1.2,baseY:.60,headRatio:.43,armRatio:.51,legRatio:.36,shoulderRatio:.46,posture:41,
   forms:[[0,-.27,-.11,.35,.36,.32],[0,-.04,.05,.31,.35,.26],[0,.27,.27,.45,.40,.42],[0,.39,.30,.44,.39,.41]],
   anchors:{pelvis:[0,-.35,-.12],spine:[0,-.04,-.06],chest:[0,.11,.10],neck:[0,.23,.19],head:[0,.32,.29],
     Lshoulder:[-.30,.05,.06],Lelbow:[-.37,-.26,.25],Lwrist:[-.41,-.49,.41],Rshoulder:[.30,.05,.06],Relbow:[.37,-.26,.25],Rwrist:[.41,-.49,.41],
     Lhip:[-.22,-.43,-.16],Lknee:[-.33,-.55,.08],Lfoot:[-.36,-.57,.31],Rhip:[.22,-.43,-.16],Rknee:[.33,-.55,.08],Rfoot:[.36,-.57,.31]},
   limbRadius:{arm:.095,leg:.14},jaw:[0,.05,.65],eye:[.237,.39,.623,.141],skin:'#873e55'},
 wraith:{name:'GAUNT HOODED WRAITH',height:2.1,baseY:1.06,headRatio:.13,armRatio:.74,legRatio:.42,shoulderRatio:.34,posture:23,
   forms:[[0,-.16,-.05,.24,.65,.25],[0,.55,-.03,.29,.28,.26],[0,.80,.18,.24,.30,.22],[0,-.61,-.12,.18,.35,.20]],
   anchors:{pelvis:[0,-.58,-.12],spine:[0,-.12,-.06],chest:[0,.45,-.02],neck:[0,.68,.11],head:[0,.86,.20],
     Lshoulder:[-.28,.45,-.01],Lelbow:[-.43,-.21,.13],Lwrist:[-.47,-.81,.30],Rshoulder:[.28,.45,-.01],Relbow:[.43,-.21,.13],Rwrist:[.47,-.81,.30],
     Lhip:[-.15,-.58,-.14],Lknee:[-.18,-.82,-.13],Lfoot:[-.18,-1.02,-.10],Rhip:[.15,-.58,-.14],Rknee:[.18,-.82,-.13],Rfoot:[.18,-1.02,-.10]},
   limbRadius:{arm:.064,leg:.085},jaw:[0,.65,.39],eye:[.096,.91,.406,.048],skin:'#575459'},
 necromancer:{name:'NECROMANCER',height:2.4,baseY:1.2,headRatio:.13,armRatio:.58,legRatio:.47,shoulderRatio:.42,posture:9,
   forms:[[0,-.25,-.03,.30,.70,.32],[0,.43,-.02,.35,.27,.34],[0,.77,.05,.32,.36,.31]],
   anchors:{pelvis:[0,-.68,0],spine:[0,-.05,0],chest:[0,.50,0],neck:[0,.75,.10],head:[0,.93,.16],
     Lshoulder:[-.34,.46,0],Lelbow:[-.47,.03,.19],Lwrist:[-.61,.14,.52],Rshoulder:[.34,.46,0],Relbow:[.50,.10,.10],Rwrist:[.60,-.09,.31],
     Lhip:[-.18,-.68,0],Lknee:[-.19,-.99,0],Lfoot:[-.18,-1.16,.13],Rhip:[.18,-.68,0],Rknee:[.19,-.99,0],Rfoot:[.18,-1.16,.13]},
   limbRadius:{arm:.10,leg:.12},jaw:[0,.73,.38],eye:[.10,.97,.44,.040],skin:'#74686d'},
 gargoyle:{name:'WINGED GARGOYLE',height:1.4,wingspan:4,baseY:1.16,headRatio:.22,armRatio:.61,legRatio:.42,shoulderRatio:.58,posture:43,
   forms:[[0,-.10,-.17,.39,.39,.49],[0,.28,.11,.40,.34,.31],[0,.49,.35,.27,.29,.31]],
   anchors:{pelvis:[0,-.44,-.27],spine:[0,-.05,-.15],chest:[0,.31,.10],neck:[0,.45,.27],head:[0,.55,.39],
     Lshoulder:[-.42,.21,.07],Lelbow:[-.69,-.28,.36],Lwrist:[-.75,-.80,.60],Rshoulder:[.42,.21,.07],Relbow:[.69,-.28,.36],Rwrist:[.75,-.80,.60],
     Lhip:[-.25,-.43,-.27],Lknee:[-.49,-.75,.04],Lfoot:[-.56,-1.06,.40],Rhip:[.25,-.43,-.27],Rknee:[.49,-.75,.04],Rfoot:[.56,-1.06,.40]},
   limbRadius:{arm:.12,leg:.19},jaw:[0,.34,.66],eye:[.134,.57,.66,.049],skin:'#595960'}
};
const BONE_PARENT={pelvis:null,spine:'pelvis',chest:'spine',neck:'chest',head:'neck',
 Lshoulder:'chest',Lelbow:'Lshoulder',Lwrist:'Lelbow',Rshoulder:'chest',Relbow:'Rshoulder',Rwrist:'Relbow',
 Lhip:'pelvis',Lknee:'Lhip',Lfoot:'Lknee',Rhip:'pelvis',Rknee:'Rhip',Rfoot:'Rknee'};
const BONE_NAMES=Object.keys(BONE_PARENT);
const GEOMETRY=new Map(),MATERIALS=new Map(),WING_GEOMETRY=new Map();
function clamp(x,a,b){return Math.max(a,Math.min(b,x));}
function smin(a,b,k){const h=Math.max(k-Math.abs(a-b),0)/k;return Math.min(a,b)-h*h*k*.25;}
function field(plan,x,y,z){let v=99;const f=plan.forms;for(let i=0;i<f.length;i++){
 const p=f[i],dx=(x-p[0])/p[3],dy=(y-p[1])/p[4],dz=(z-p[2])/p[5],d=(Math.hypot(dx,dy,dz)-1)*Math.min(p[3],p[4],p[5]);
 v=i?smin(v,d,plan===SPEC.imp?.18:.22):d;
}const folds=Math.sin(y*18+x*6+Math.sin(z*9)*2)*Math.sin(x*13+z*7)*.009;
const pores=Math.sin(x*44+y*29)*Math.sin(z*37-y*17)*.005;
return v+folds+pores;}
function newBuilder(){return {p:[],i:[],uv:[],idx:[],wg:[]};}
function vertex(b,x,y,z,u,v,weights){const id=b.p.length/3;b.p.push(x,y,z);b.uv.push(u,v);b.wg.push(weights);return id;}
function tri(b,a,c,d){b.idx.push(a,c,d);}
function skinFromPoint(plan,x,y,z){
 let n0=0,n1=0,n2=0,n3=0,w0=-1,w1=-1,w2=-1,w3=-1;
 for(let j=0;j<BONE_NAMES.length;j++){
  const p=plan.anchors[BONE_NAMES[j]],dx=x-p[0],dy=y-p[1],dz=z-p[2];
  const d=dx*dx+dy*dy+dz*dz+.018;
  const w=1/(d*d*(j===4||j===7||j===10||j===13||j===16?1.18:1));
  if(w>w0){w3=w2;n3=n2;w2=w1;n2=n1;w1=w0;n1=n0;w0=w;n0=j;}
  else if(w>w1){w3=w2;n3=n2;w2=w1;n2=n1;w1=w;n1=j;}
  else if(w>w2){w3=w2;n3=n2;w2=w;n2=j;}
  else if(w>w3){w3=w;n3=j;}
 }
 const inv=1/(w0+w1+w2+w3);
 return [[n0,w0*inv],[n1,w1*inv],[n2,w2*inv],[n3,w3*inv]];
}
function addSculpt(plan,b,res){const bounds=[100,100,100,-100,-100,-100];for(const f of plan.forms)for(let j=0;j<3;j++){
 bounds[j]=Math.min(bounds[j],f[j]-f[j+3]-.08);bounds[j+3]=Math.max(bounds[j+3],f[j]+f[j+3]+.08);
}
 const nx=res,ny=Math.floor(res*1.05),nz=Math.floor(res*.90),SX=nx+1,SY=ny+1,SZ=nz+1;
 const sx=(bounds[3]-bounds[0])/nx,sy=(bounds[4]-bounds[1])/ny,sz=(bounds[5]-bounds[2])/nz;
 const id=(x,y,z)=>(z*SY+y)*SX+x;
 const samples=new Float32Array(SX*SY*SZ);
 for(let z=0;z<SZ;z++)for(let y=0;y<SY;y++)for(let x=0;x<SX;x++)samples[id(x,y,z)]=field(plan,bounds[0]+x*sx,bounds[1]+y*sy,bounds[2]+z*sz);
 const vertices=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]];
 const tetra=[[0,5,1,6],[0,1,2,6],[0,2,3,6],[0,3,7,6],[0,7,4,6],[0,4,5,6]];
 const e=[[0,1],[1,2],[2,0],[0,3],[1,3],[2,3]];
 const facets=[[],[[0,3,2]],[[0,1,4]],[[1,4,2],[2,4,3]],[[1,2,5]],[[0,3,5],[0,5,1]],[[0,2,5],[0,5,4]],[[3,4,5]],[[3,5,4]],[[0,4,5],[0,5,2]],[[0,1,5],[0,5,3]],[[1,5,2]],[[2,3,4],[1,2,4]],[[0,4,1]],[[0,2,3]],[]];
 for(let z=0;z<nz;z++)for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){
  const vv=[],dd=[];let lo=100,hi=-100;
  for(let j=0;j<8;j++){const a=vertices[j],gx=x+a[0],gy=y+a[1],gz=z+a[2];vv[j]=[bounds[0]+gx*sx,bounds[1]+gy*sy,bounds[2]+gz*sz];dd[j]=samples[id(gx,gy,gz)];lo=Math.min(lo,dd[j]);hi=Math.max(hi,dd[j]);}
  if(lo>0||hi<0)continue;
  for(let t=0;t<6;t++){
   const tt=tetra[t],v=tt.map(i=>vv[i]),d=tt.map(i=>dd[i]);let mask=0;for(let q=0;q<4;q++)if(d[q]<0)mask|=(1<<q);
   if(!mask||mask===15)continue;
   const interp=e.map(([a,c])=>{if((d[a]<0)===(d[c]<0))return null;const f=d[a]/(d[a]-d[c]);return [v[a][0]+(v[c][0]-v[a][0])*f,v[a][1]+(v[c][1]-v[a][1])*f,v[a][2]+(v[c][2]-v[a][2])*f];});
   for(const face of facets[mask]){
    const p=face.map(q=>interp[q]);if(p.some(a=>!a))continue;
    const u=[p[1][0]-p[0][0],p[1][1]-p[0][1],p[1][2]-p[0][2]];
    const v=[p[2][0]-p[0][0],p[2][1]-p[0][1],p[2][2]-p[0][2]];
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
    const cc=[(p[0][0]+p[1][0]+p[2][0])/3,(p[0][1]+p[1][1]+p[2][1])/3,(p[0][2]+p[1][2]+p[2][2])/3];
    const cy=plan===SPEC.crawler?-0.03:0;
    if(n[0]*cc[0]+n[1]*(cc[1]-cy)+n[2]*cc[2]<0){const tmp=p[1];p[1]=p[2];p[2]=tmp;}
    const off=b.p.length/3;
    for(const [px,py,pz] of p)vertex(b,px,py,pz,.5+Math.atan2(pz,px)/(Math.PI*2),(py-bounds[1])/(bounds[4]-bounds[1]),skinFromPoint(plan,px,py,pz));
    tri(b,off,off+1,off+2);
   }
  }
 }
}
function addLoft(b,plan,first,last,r0,r1,res){
 const A=plan.anchors[first],B=plan.anchors[last],length=Math.hypot(B[0]-A[0],B[1]-A[1],B[2]-A[2]);
 const dir=new THREE.Vector3(B[0]-A[0],B[1]-A[1],B[2]-A[2]).normalize();
 const u=new THREE.Vector3(1,0,0);if(Math.abs(dir.dot(u))>.92)u.set(0,0,1);
 u.addScaledVector(dir,-u.dot(dir)).normalize();const v=new THREE.Vector3().crossVectors(dir,u).normalize();
 const idxA=BONE_NAMES.indexOf(first),idxB=BONE_NAMES.indexOf(last),rings=res>20?7:4,sides=res>20?11:7;
 const start=b.p.length/3;
 for(let j=0;j<=rings;j++){
  const t=j/rings;let radius=(r0+(r1-r0)*t)*(1+.19*Math.sin(Math.PI*t));
  for(let k=0;k<=sides;k++){
   const ang=k/sides*Math.PI*2,wrinkle=1+.055*Math.sin(ang*5+t*17),ct=Math.cos(ang),st=Math.sin(ang);
   const x=A[0]+(B[0]-A[0])*t+(u.x*ct+v.x*st)*radius*wrinkle;
   const y=A[1]+(B[1]-A[1])*t+(u.y*ct+v.y*st)*radius*wrinkle;
   const z=A[2]+(B[2]-A[2])*t+(u.z*ct+v.z*st)*radius*wrinkle;
   vertex(b,x,y,z,k/sides,t,[[idxA,1-t],[idxB,t],[0,0],[0,0]]);
  }
 }
 for(let j=0;j<rings;j++)for(let k=0;k<sides;k++){
  const a=start+j*(sides+1)+k,c=a+sides+1;tri(b,a,c,a+1);tri(b,a+1,c,c+1);
 }
}
function createGeometry(plan,res){const b=newBuilder();addSculpt(plan,b,res);
 const a=plan.anchors,s=plan.limbRadius;
 for(const side of ['L','R']){
  addLoft(b,plan,side+'shoulder',side+'elbow',s.arm,s.arm*.74,res);addLoft(b,plan,side+'elbow',side+'wrist',s.arm*.77,s.arm*.49,res);
  if(plan===SPEC.wraith||plan===SPEC.necromancer)continue;
  addLoft(b,plan,side+'hip',side+'knee',s.leg,s.leg*.70,res);addLoft(b,plan,side+'knee',side+'foot',s.leg*.73,s.leg*.46,res);
 }
 const g=new THREE.BufferGeometry(),idx=new Float32Array(b.wg.length*4),weights=new Float32Array(b.wg.length*4);
 for(let j=0;j<b.wg.length;j++)for(let k=0;k<4;k++){idx[j*4+k]=b.wg[j][k][0];weights[j*4+k]=b.wg[j][k][1];}
 g.setAttribute('position',new THREE.Float32BufferAttribute(b.p,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(b.uv,2));
 g.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(idx,4));g.setAttribute('skinWeight',new THREE.Float32BufferAttribute(weights,4));
 g.setIndex(b.idx);g.computeVertexNormals();g.computeBoundingSphere();
 return g;
}
function geometries(type){if(GEOMETRY.has(type))return GEOMETRY.get(type);const plan=SPEC[type];
 const t0=performance.now();const values=[24,15,5].map(n=>createGeometry(plan,n));
 const stats={ms:Math.round(performance.now()-t0),triangles:values.map(g=>g.index.count/3)};
 const entry={geoms:values,stats};GEOMETRY.set(type,entry);return entry;
}
function raster(type){if(MATERIALS.has(type))return MATERIALS.get(type);const palette=PIXEL_PALETTES[type];
 const n=192,c=document.createElement('canvas'),b=document.createElement('canvas'),r=document.createElement('canvas');
 for(const v of [c,b,r]){v.width=n;v.height=n;}
 const C=c.getContext('2d'),B=b.getContext('2d'),R=r.getContext('2d');
 const a=C.createImageData(n,n),bt=B.createImageData(n,n),rt=R.createImageData(n,n);
 const hash=(x,y)=>{let v=Math.imul(x+1337,374761393)^Math.imul(y+2718,668265263)^type.length;v=Math.imul(v^(v>>>13),1274126177);return ((v^(v>>>16))>>>0)/4294967296;};
 const colors=palette.map(p=>[parseInt(p.slice(1,3),16),parseInt(p.slice(3,5),16),parseInt(p.slice(5),16)]);
 if(type==='necromancer'){
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const t=(Math.sin(x*.069+2*Math.sin(y*.036))+1)*.5*.56+hash(x>>2,y>>2)*.44;
  const k=Math.min(4,Math.floor(t*5)),f=t*5-k,shade=colors[k].map((q,z)=>q*(1-f)+colors[k+1][z]*f);
  const vein=Math.pow(Math.max(0,Math.sin(x*.097+Math.sin(y*.12)*3)),18)*12;
  const scar=(Math.abs(Math.sin(y*.12+Math.sin(x*.07)*4))>.985&&hash(x>>4,y>>4)>.6)?22:0;
  const off=(y*n+x)*4;
  for(let z=0;z<3;z++)a.data[off+z]=clamp(shade[z]+(hash(x,y)-.5)*22-(z===0?0:vein)-scar,5,230);
  a.data[off+3]=255;
  const relief=clamp(128+27*(hash(x,y)-.5)+18*Math.sin(x*.17+y*.22)-scar,12,243);
  bt.data[off]=bt.data[off+1]=bt.data[off+2]=relief;bt.data[off+3]=255;
  const gloss=type==='imp'||type==='crawler'?133:190;
  const rv=clamp(gloss+28*(hash(x>>2,y>>2)-.5)-scar,50,240);
  rt.data[off]=rt.data[off+1]=rt.data[off+2]=rv;rt.data[off+3]=255;
 }
 }else{
 for(let y=0;y<n;y++)for(let x=0;x<n;x++){
  const block=hash(x>>2,y>>2),fine=hash(x,y),fiber=Math.sin(x*.13+y*.075+Math.sin(y*.045)*4);
  const macro=Math.sin(x*.037+Math.sin(y*.042)*2.3)*Math.cos(y*.032+Math.sin(x*.053)*1.5);
  const t=clamp(.47+.24*macro+.18*(block-.5)+.16*(fine-.5),0,.999);
  const k=Math.min(4,Math.floor(t*5)),f=t*5-k,shade=colors[k].map((q,z)=>q*(1-f)+colors[k+1][z]*f);
  const crease=Math.sin(y*.091+Math.sin(x*.046)*5.2+x*.018);
  const scar=(Math.abs(crease)<.026&&hash(x>>4,y>>4)>.47)?(type==='brute'?31:15):0;
  const vein=Math.pow(Math.max(0,Math.sin(x*.11+Math.sin(y*.061)*3.2)),24)*(type==='imp'?28:15);
  const bruises=Math.max(0,Math.sin(x*.046+y*.014+Math.sin(y*.022)*2))*Math.max(0,Math.cos(y*.058-x*.019))*12;
  const pores=(fine-.5)*17+(hash(x>>1,y>>1)-.5)*13;
  const off=(y*n+x)*4;
  for(let z=0;z<3;z++){
   let pigment=shade[z]+pores+macro*9-scar+(z===0?bruises*.72:-(bruises*.38+vein));
   if(type==='imp'&&z===0)pigment+=9;
   a.data[off+z]=clamp(pigment,5,224);
  }
  a.data[off+3]=255;
  const relief=clamp(128+27*(fine-.5)+10*fiber+15*macro-scar*.63+vein*.52,12,243);
  bt.data[off]=bt.data[off+1]=bt.data[off+2]=relief;bt.data[off+3]=255;
  const gloss=type==='imp'?105:type==='crawler'?140:type==='brute'?184:type==='wraith'?202:type==='gargoyle'?197:190;
  const rv=clamp(gloss+27*(block-.5)+15*Math.abs(macro)-scar*.8,48,242);
  rt.data[off]=rt.data[off+1]=rt.data[off+2]=rv;rt.data[off+3]=255;
 }
 }
 C.putImageData(a,0,0);B.putImageData(bt,0,0);R.putImageData(rt,0,0);
 const tex=canvas=>{const t=new THREE.CanvasTexture(canvas);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;return t;};
 const mat=new THREE.MeshStandardMaterial({map:tex(c),bumpMap:tex(b),bumpScale:.055,roughnessMap:tex(r),roughness:1,color:0xffffff,metalness:0,vertexColors:false,side:THREE.FrontSide});
 MATERIALS.set(type,mat);return mat;
}
function createSkeleton(plan,group){const bones={},world=plan.anchors;
 for(const name of BONE_NAMES)bones[name]=new THREE.Bone(),bones[name].name=name;
 for(const name of BONE_NAMES){const parent=BONE_PARENT[name],p=world[name];
  if(parent){const q=world[parent];bones[name].position.set(p[0]-q[0],p[1]-q[1],p[2]-q[2]);bones[parent].add(bones[name]);}
  else {bones[name].position.set(...p);group.add(bones[name]);}
 }
 group.updateMatrixWorld(true);const skeleton=new THREE.Skeleton(BONE_NAMES.map(n=>bones[n]));
 skeleton.calculateInverses();return {skeleton,bones};
}
const MAT={};
function std(id,color,metal=0,rough=.74){const key=id+'|'+color;if(!MAT[key])MAT[key]=new THREE.MeshStandardMaterial({color,metalness:metal,roughness:rough,side:THREE.DoubleSide});return MAT[key];}
const DETAILS_GEOMETRY=new Map();
function detailGeometry(key,create){let geo=DETAILS_GEOMETRY.get(key);if(!geo){geo=create();DETAILS_GEOMETRY.set(key,geo);}return geo;}
function bulb(parent,x,y,z,scale,material){const g=detailGeometry('sphere16',()=>new THREE.SphereGeometry(1,16,12));const m=new THREE.Mesh(g,material);m.position.set(x,y,z);m.scale.set(...scale);m.castShadow=true;parent.add(m);return m;}
function path(parent,pts,r,mat){const key='tube:'+r+':'+pts.map(p=>p.join(',')).join('|');const g=detailGeometry(key,()=>new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(...p))),Math.max(8,pts.length*5),r,7,false));const o=new THREE.Mesh(g,mat);parent.add(o);o.castShadow=true;return o;}
function cusp(parent,x,y,z,r,len,mat,rx=0,rz=0){const g=detailGeometry('cone7',()=>new THREE.ConeGeometry(1,1,7,3));const o=new THREE.Mesh(g,mat);o.scale.set(r,len,r);o.position.set(x,y,z);o.rotation.set(rx,0,rz);parent.add(o);return o;}
function polyPoint(pts,t){const m=pts.length-1;if(m<=0)return pts[0]||[0,0,0];const s=clamp(t,0,.999999)*m,i=Math.floor(s),f=s-i,a=pts[i],b=pts[Math.min(m,i+1)];return[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[2]+(b[2]-a[2])*f];}
function stitchScar(parent,pts,width,scarMat,stitchMat,count=0){const scar=path(parent,pts,width,scarMat);for(let i=0;i<count;i++){const p=polyPoint(pts,(i+.5)/Math.max(1,count));const knot=bulb(parent,p[0],p[1],p[2],[width*2.4,width*1.6,width*2.1],stitchMat);knot.castShadow=true;}return scar;}
function setBaseScale(obj){obj.userData.baseScale=obj.scale.clone();obj.userData.baseY=obj.position.y;return obj;}
function necroOpenHood(head,parts){
 const rows=[[-.19,.30,.36,.00],[-.10,.30,.37,.01],[.10,.27,.35,.025],[.29,.235,.31,.02],[.34,.215,.29,.02]];
 const segments=32,vertices=[],uv=[],ids=[];
 for(let r=0;r<rows.length;r++){
  const [z,rx,ry,cy]=rows[r];
  for(let i=0;i<=segments;i++){
   const a=i/segments*Math.PI*2,c=Math.cos(a),si=Math.sin(a),fold=1+.038*Math.sin(i*.94+r*.8);
   vertices.push(rx*c*fold,cy+ry*si*(1+.04*Math.sin(i*.47)),z+(.02*Math.sin(a*3+r)));
   uv.push(i/segments,r/(rows.length-1));
   if(r<rows.length-1&&i<segments){const k=r*(segments+1)+i;ids.push(k,k+segments+1,k+1,k+1,k+segments+1,k+segments+2);}
  }
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(ids);g.computeVertexNormals();
 const hood=new THREE.Mesh(g,std('necroCowlShell',0x201720,0,.95));hood.castShadow=true;hood.receiveShadow=true;head.add(hood);
 const dark=std('necroHoodInterior',0x09070c,0,.98),border=std('necroHoodStitchedHem',0x6c4351,.10,.68),edge=std('necroHoodGoldThread',0x8b6570,.27,.55);
 bulb(head,0,.03,-.095,[.215,.25,.22],dark);
 const rim=[];for(let i=0;i<=28;i++){const a=i/28*Math.PI*2;rim.push([.235*Math.cos(a),.02+.308*Math.sin(a),.355+.012*Math.cos(a*4)]);}
 const trim=path(head,rim,.018,border);parts.details.push(trim);
 const inner=[];for(let i=0;i<=25;i++){const a=i/25*Math.PI*2;inner.push([.205*Math.cos(a),.02+.285*Math.sin(a),.357+.007*Math.sin(a*2)]);}
 path(head,inner,.006,edge);
 // The upper hood casts a narrow shadow without covering the eyes and teeth.
 path(head,[[-.205,.23,.36],[-.10,.305,.382],[0,.32,.386],[.12,.295,.378],[.212,.21,.36]],.025,std('necroHoodBrow',0x241923));
 for(const s of [-1,1]){
  path(head,[[s*.23,.15,.29],[s*.27,.01,.27],[s*.255,-.14,.28],[s*.18,-.29,.305]],.022,border);
  const shred=clothStrip(head,'necromancer',s*.245,-.18,.44,std('necroHoodTail',0x281b28));
  shred.bone.position.y=-.13;parts.cloth.push(shred);
 }
 parts.hoodShell=hood;
}
function necroRobeShell(bones,parts){
 const root=bones.pelvis,segments=28,rings=12;
 const build=(offset,scale,colour)=>{
  const vertices=[],uv=[],indices=[],colors=[];
  for(let j=0;j<=rings;j++){
   const t=j/rings,y=-.50+t*1.55,rad=(.77*(1-t)+.30*t)*scale;
   for(let k=0;k<=segments;k++){
    const a=k/segments*Math.PI*2,fold=1+.10*Math.cos(a*11+offset)+.035*Math.sin(t*19+a*6+offset);
    const hem=(1-t)*(Math.sin(a*13+offset)*.07+Math.sin(a*7+offset)*.035);
    const x=rad*Math.sin(a)*fold,z=rad*Math.cos(a)*(.75+.12*Math.sin(a*3))+offset*.015;
    vertices.push(x,y+hem,z);uv.push(k/segments,t);
    const crease=(.58+.34*Math.cos(a*11+offset))*(.72+.28*t);
    colors.push(colour[0]*crease,colour[1]*crease,colour[2]*crease);
    if(j<rings&&k<segments){const n=j*(segments+1)+k;indices.push(n,n+1,n+segments+1,n+1,n+segments+2,n+segments+1);}
   }
  }
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));g.setIndex(indices);g.computeVertexNormals();
  const robe=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xffffff,vertexColors:true,roughness:.91,metalness:0,side:THREE.DoubleSide}));robe.castShadow=true;robe.receiveShadow=true;root.add(robe);return robe;
 };
 parts.robeShells.push(build(.6,1,[.39,.22,.27]));
 parts.robeShells.push(build(2.5,.91,[.26,.15,.21]));
 const collar=std('necroCollar',0x2b2029,0,.90);
 for(const s of [-1,1]){
  path(bones.chest,[[s*.24,.26,.04],[s*.47,.15,.0],[s*.49,-.09,.20],[s*.28,-.33,.32]],.057,collar);
  path(bones.chest,[[s*.17,.23,.22],[s*.25,.09,.35],[s*.23,-.22,.40]],.012,std('necroCollarTrim',0x9a6670,.23,.55));
 }
 const runeMat=new THREE.MeshBasicMaterial({color:0xb367ff,transparent:true,opacity:.69,depthWrite:false});
 parts.runeMat=runeMat;
 const rune=pts=>{const r=path(root,pts,.010,runeMat);parts.robeRunes.push(r);};
 // Three asymmetric rune marks and hem stitches float just above the robe surface.
 for(let i=0;i<4;i++){
  const y=.65-i*.22,z=.38+i*.045,x=(i%2?-.11:.12);
  rune([[x-.048,y+.07,z-.01],[x,y-.015,z+.022],[x+.052,y+.07,z-.01]]);
  rune([[x,y+.092,z],[x,y-.084,z+.014]]);
 }
 for(let i=0;i<8;i++){
  const x=(i-3.5)*.12;
  const xx=x*.75;
  rune([[xx,-.40,.60],[xx+.025,-.47,.62]]);
 }
 // Torso has genuine layered cloth panels, not a skin-coloured body painted flat.
}
function necroSkullCharm(parent,x,y,z,scale,parts){
 const g=new THREE.Group();g.position.set(x,y,z);g.scale.setScalar(scale);parent.add(g);
 const bone=std('necroBeltBone',0xa49b96,0,.68),voidMat=std('necroBeltSocket',0x161016,0,.94),aged=std('necroBeltTeeth',0xd2bdb1,0,.57);
 bulb(g,0,.045,0,[.105,.12,.085],bone);bulb(g,0,-.078,.038,[.073,.065,.063],bone);
 for(const s of [-1,1]){bulb(g,s*.052,.055,.081,[.037,.036,.012],voidMat);bulb(g,s*.040,-.032,.088,[.020,.022,.01],voidMat);}
 bulb(g,0,-.007,.101,[.020,.030,.011],voidMat);
 for(let i=0;i<5;i++){const tx=(i-2)*.025;bulb(g,tx,-.101,.098,[.010,.018,.009],aged);}
 parts.trophies.push(g);return g;
}
function necroCastingWisps(root,parts){
 const strand=std('necroWispStrand',0x623a7c,0,.60),flare=new THREE.MeshBasicMaterial({color:0xba6cff,transparent:true,opacity:.79,depthWrite:false});
 parts.wispMat=flare;
 for(let i=0;i<5;i++){
  const group=new THREE.Group();group.position.set(0,.13,.12);root.add(group);
  const a=i*Math.PI*2/5;
  path(group,[[.10*Math.cos(a),0,.07*Math.sin(a)],[.15*Math.cos(a+.45),.13,.11*Math.sin(a+.45)],[.11*Math.cos(a+1),.30,.17*Math.sin(a+1)]],.009,i%2?flare:strand);
  const tip=bulb(group,.11*Math.cos(a+1),.30,.17*Math.sin(a+1),[.025,.025,.025],flare);
  parts.wisps.push({group,tip,phase:i*1.2566});
 }
}
function headDetails(type,bones,parts){
 const plan=SPEC[type],head=bones.head,skull=std('bone',0x918a85,0,.74),dark=std('cavity',0x140d13,0,.92),ivory=std('ivory',0xd4c5b6,0,.48),
  wound=std('woundFace',0x5a272f,0,.70),scar=std('scarFace',0x71545b,0,.88),stitch=std('stitchFace',0x23191c,0,.84),
  tendon=std('tendonFace',0x8e686a,0,.48),bruteFlesh=std('bruteFace',0x6f585d,0,.90),crawlerBone=std('crawlerBone',0x7a6868,0,.86),
  impFlesh=std('impFace',0x8b4c60,0,.78),wraithBone=std('wraithBone',0xa4a0a3,0,.58),necroBone=std('necroBone',0xb8aeaa,0,.52),gargStone=std('gargFace',0x6a5f65,0,.88),
  glowPale=new THREE.MeshBasicMaterial({color:0xd8dee9}),glowPurple=new THREE.MeshBasicMaterial({color:0xa85cff}),glowAmber=new THREE.MeshBasicMaterial({color:0xd8a167});
 const glossEye=color=>new THREE.MeshPhysicalMaterial({color,metalness:.02,roughness:.05,clearcoat:1,clearcoatRoughness:.08});
 const addEye=(x,y,z,scale,mat,pupilScale,pupilMat,socketScale)=>{
  if(socketScale)bulb(head,x,y,z-.02,socketScale,dark);
  const eye=setBaseScale(bulb(head,x,y,z,scale,mat));
  const pupil=setBaseScale(bulb(head,x,y,z+scale[2]*.72,pupilScale,pupilMat));
  parts.eyes.push(eye);parts.pupils.push(pupil);return {eye,pupil};
 };
 let jawOffset=[0,.04,0],jawTop=[.20,.08,.08],jawBottom=[.18,.08,.12],teethTop=8,teethBottom=8,teethWidth=.30,jawTopMat=dark,jawBotMat=std('jaw',0x53464c),skipTeeth=false;
 if(type==='brute'){
  bulb(head,0,.08,.16,[.24,.17,.16],bruteFlesh);bulb(head,0,-.02,.24,[.13,.08,.08],dark);
  for(const s of [-1,1]){bulb(head,s*.18,.11,.18,[.12,.07,.09],bruteFlesh);bulb(head,s*.14,.01,.31,[.07,.05,.03],dark);addEye(s*.11,.02,.36,[.032,.026,.024],glossEye(0x301417),[.012,.012,.010],std('brutePupil',0xa34e43,0,.18),[.08,.05,.04]);}
  stitchScar(head,[[-.16,.16,.18],[-.05,.06,.30],[.03,-.01,.35]],.008,scar,stitch,5);
  stitchScar(head,[[.08,.12,.20],[.16,.03,.33],[.19,-.04,.34]],.007,wound,stitch,4);
  path(head,[[-.05,.00,.40],[0,-.07,.47],[.04,-.14,.43]],.008,tendon);
  jawOffset=[0,-.01,.03];jawTop=[.31,.17,.09];jawBottom=[.30,.12,.16];teethTop=14;teethBottom=12;teethWidth=.50;jawTopMat=dark;jawBotMat=std('bruteJaw',0x6a5556);parts.roarDrool=path(head,[[0,-.02,.41],[.01,-.23,.56],[0,-.43,.47]],.006,std('drool',0xb5989d,0,.12));
 }else if(type==='crawler'){
  bulb(head,0,.03,.16,[.18,.10,.22],crawlerBone);bulb(head,0,-.05,.30,[.10,.07,.10],dark);bulb(head,0,.11,.24,[.15,.06,.12],crawlerBone);
  for(const s of [-1,1]){bulb(head,s*.12,.10,.24,[.07,.04,.06],crawlerBone);addEye(s*.09,.02,.34,[.028,.022,.020],glossEye(0x2a272a),[.010,.010,.009],std('crawlPupil',0xbcb0a5,0,.20),[.06,.04,.03]);}
  stitchScar(head,[[-.05,.16,.16],[0,.10,.29],[.05,.02,.39]],.005,scar,stitch,3);
  path(head,[[-.12,.00,.37],[0,-.02,.48],[.12,.00,.37]],.006,wound);jawOffset=[0,-.08,.05];jawTop=[.16,.08,.07];jawBottom=[.14,.05,.13];teethTop=10;teethBottom=8;teethWidth=.24;jawBotMat=std('crawlJaw',0x605154);
 }else if(type==='imp'){
  bulb(head,0,.12,.18,[.18,.15,.12],impFlesh);bulb(head,0,-.01,.15,[.22,.13,.15],impFlesh);bulb(head,0,.00,.27,[.10,.06,.05],wound);
  for(const s of [-1,1]){const eye=addEye(s*.17,.12,.34,[.12,.11,.09],new THREE.MeshPhysicalMaterial({color:0x40262d,metalness:.02,roughness:.04,clearcoat:1,clearcoatRoughness:.05}),[.044,.044,.030],std('impPupil',0xd8d6cc,0,.15),[.14,.12,.08]);
    const lid=setBaseScale(bulb(head,s*.17,.17,.34,[.13,.038,.07],std('impLid',0x6a3848)));parts.eyelids.push(lid);
    const cheek=bulb(head,s*.18,.02,.24,[.08,.06,.05],impFlesh);parts.details.push(cheek);
    const glint=setBaseScale(bulb(head,s*.14,.15,.40,[.018,.018,.010],new THREE.MeshBasicMaterial({color:0xf7d9d9})));parts.details.push(glint);
  }
  path(head,[[-.05,.02,.31],[0,.01,.36],[.05,.02,.31]],.004,dark);jawOffset=[0,-.02,.12];jawTop=[.12,.045,.05];jawBottom=[.11,.04,.07];teethTop=10;teethBottom=10;teethWidth=.18;jawBotMat=std('impJaw',0x6f4250);
 }else if(type==='wraith'){
  bulb(head,0,.08,.18,[.11,.18,.10],wraithBone);bulb(head,0,-.01,.21,[.07,.06,.04],dark);bulb(head,0,.18,.10,[.14,.09,.10],std('wraithBrow',0x59545c));
  for(const s of [-1,1]){bulb(head,s*.07,.08,.24,[.05,.035,.03],dark);addEye(s*.06,.08,.26,[.014,.014,.010],glowPale,[.009,.009,.007],glowPale,[.045,.032,.025]);}
  jawOffset=[0,-.01,.05];jawTop=[.12,.06,.05];jawBottom=[.08,.05,.09];teethTop=0;teethBottom=0;teethWidth=.16;jawTopMat=std('wraithMaw',0x17141a);jawBotMat=std('wraithJaw',0x5e575b);
 }else if(type==='necromancer'){
  // Face is genuinely inset into an open hood, rather than obscured by a filled oval.
  necroOpenHood(head,parts);
  const cranium=bulb(head,0,.040,.165,[.135,.169,.133],necroBone);parts.faceCranium=cranium;
  bulb(head,0,-.09,.236,[.090,.071,.083],necroBone);
  for(const side of [-1,1]){
   bulb(head,side*.078,.090,.257,[.072,.059,.043],dark);
   path(head,[[side*.14,.10,.235],[side*.12,.035,.305],[side*.10,-.045,.297]],.018,necroBone);
   path(head,[[side*.098,-.035,.30],[side*.064,-.090,.329],[side*.035,-.135,.30]],.010,skull);
   addEye(side*.074,.081,.304,[.018,.014,.009],glowPurple,[.009,.008,.005],glowPurple,[.063,.056,.033]);
  }
  bulb(head,0,-.030,.316,[.024,.037,.014],dark);
  bulb(head,0,.187,.243,[.125,.023,.053],std('necroFrontalBone',0x968b8e,0,.72));
  stitchScar(head,[[-.095,.154,.248],[-.052,.176,.284],[.005,.169,.28]],.004,std('necroForeheadScar',0x55404b),std('necroForeheadStitch',0x2a1c24),3);
  jawOffset=[0,-.045,.040];jawTop=[.095,.048,.033];jawBottom=[.079,.052,.052];teethTop=0;teethBottom=0;teethWidth=.14;jawTopMat=std('necroMaw',0x161117);jawBotMat=std('necroJaw',0xa99d99);
 }else if(type==='gargoyle'){
  bulb(head,0,.10,.14,[.16,.11,.16],gargStone);bulb(head,0,.02,.31,[.11,.07,.11],gargStone);bulb(head,0,-.02,.38,[.07,.05,.05],dark);
  for(const s of [-1,1]){bulb(head,s*.16,.14,.18,[.10,.05,.07],gargStone);bulb(head,s*.10,.08,.31,[.05,.04,.03],dark);addEye(s*.09,.10,.34,[.026,.022,.020],glossEye(0x3b2a24),[.010,.010,.008],glowAmber,[.055,.040,.028]);
    const ear=cusp(head,s*.21,.24,.05,.06,.24,std('gargEar',0x494146),-.55,s*.45);parts.details.push(ear);
  }
  jawOffset=[0,-.03,.11];jawTop=[.18,.09,.07];jawBottom=[.16,.06,.10];teethTop=8;teethBottom=6;teethWidth=.22;jawBotMat=std('gargJaw',0x645156);
 }
 const jawAnchor=plan.jaw, j=new THREE.Group();j.position.set(jawAnchor[0]+jawOffset[0],jawAnchor[1]-plan.anchors.head[1]+jawOffset[1],jawAnchor[2]-plan.anchors.head[2]+jawOffset[2]);head.add(j);parts.jaw=j;
 bulb(j,0,.04,0,jawTop,jawTopMat);bulb(j,0,-.065,.04,jawBottom,jawBotMat);
 if(!skipTeeth){
  for(let i=0;i<teethTop;i++){const x=(i/(Math.max(1,teethTop)-1)-.5)*teethWidth;cusp(j,x,.055,.06,.017,.10,ivory,Math.PI);}
  for(let i=0;i<teethBottom;i++){const x=(i/(Math.max(1,teethBottom)-1)-.5)*teethWidth*.92;cusp(j,x,-.067,.06,.016,.08,ivory,0);}
 }
 if(type==='necromancer'){
  const tooth=std('necroTeeth',0xc7b9b0,0,.61);
  for(let k=0;k<8;k++){const x=(k-3.5)*.023;bulb(j,x,.009,.067,[.010,.023,.013],tooth);bulb(j,x,-.068,.069,[.009,.019,.012],tooth);}
  path(j,[[-.08,-.115,.029],[0,-.131,.061],[.08,-.115,.029]],.009,necroBone);
 }
 if(type==='gargoyle')for(const side of [-1,1]){const horn=cusp(head,side*.18,.25,-.06,.11,.56,std('horn',0x403940),-.45,side*.42);horn.rotation.z=side*.30;const browHorn=cusp(head,side*.09,.22,.22,.035,.18,std('browHorn',0x63545a),-.62,side*.06);parts.details.push(browHorn);}
 if(type==='brute'){for(let i=0;i<7;i++){const x=(i-3)*.14;path(bones.chest,[[x,.25,.22],[x+.026,.06,.32],[x+.05,-.09,.32]],.008,std('scar',0x45252b));}}
}
function clawHand(bone,plan,type,parts,side){const skin=std('clawSkin'+type,type==='imp'?0x9c4555:0x54474d),dark=std('talon',0x201d22,0,.30);
 const s=type==='brute'?1.50:type==='crawler'?1.20:type==='gargoyle'?1.32:1.0;
 const palm=bulb(bone,0,-.025,.016,[.125*s,.055*s,.135*s],skin);parts.details.push(palm);
 for(let k=0;k<4;k++){
  const x=(k-1.5)*.071*s;
  path(bone,[[x,-.04,.06],[x*1.2,-.08,.17*s],[x*1.26,-.16,.24*s]],.021*s,skin);
  const tip=cusp(bone,x*1.3,-.18,.27*s,.022*s,.17*s,dark,Math.PI*.61);parts.details.push(tip);
 }
}
function clothStrip(parent,type,x,z,length,mat){const b=new THREE.Group();b.position.set(x,0,z);parent.add(b);
 const g=new THREE.BufferGeometry(),verts=[],uv=[],ids=[],rings=12;const width=.09+.04*Math.abs(x);
 for(let j=0;j<=rings;j++){
  const t=j/rings,yy=-length*t;const wave=Math.sin(t*10+x*17)*.07*t;
  verts.push(-width*(1-t*.29),yy,wave,width*(1-t*.29),yy,wave);uv.push(0,t,1,t);
  if(j<rings){const a=j*2;ids.push(a,a+2,a+1,a+1,a+2,a+3);}
 }
 g.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(ids);g.computeVertexNormals();
 const mesh=new THREE.Mesh(g,mat);b.add(mesh);return {bone:b,x,z,velocity:0,value:0};
}
function addCloth(type,bones,parts){const cloak=type==='necromancer'?0x241925:type==='wraith'?0x383438:0x544135;
 const fabric=std('fabric'+type,cloak);for(let i=0;i<(type==='necromancer'?12:type==='wraith'?10:9);i++){
  const angle=i*Math.PI*2/(type==='necromancer'?12:type==='wraith'?10:9);
  const radius=type==='brute'?.38:.32,pt=bones.pelvis;
  const c=clothStrip(pt,type,Math.sin(angle)*radius,Math.cos(angle)*radius, type==='brute'?.45:type==='necromancer'?.53:.78,fabric);
  if(type==='necromancer')c.bone.position.y=.11;
  parts.cloth.push(c);
 }
 if(type!=='brute'&&type!=='necromancer'&&type!=='wraith'){
  const hood=bulb(bones.head,0,.11,-.07,[.31,.35,.32],std('hood'+type,cloak));parts.details.push(hood);
  const shadow=bulb(bones.head,0,-.03,.245,[.20,.19,.024],std('hoodshadow',0x0b0811));parts.details.push(shadow);
 }
}
function addStaff(bones,parts){
 const rod=std('necroStaffDarkWood',0x35262e,0,.81),iron=std('necroThorns',0x81717a,.40,.45),bone=std('necroStaffBone',0x98898b,0,.58);
 const root=bones.Lwrist;
 const orbMat=new THREE.MeshBasicMaterial({color:0xb66aff,transparent:true,opacity:.95,depthWrite:false});parts.orbMaterial=orbMat;
 const glowMat=new THREE.MeshBasicMaterial({color:0x9d52ee,transparent:true,opacity:.19,depthWrite:false});
 path(root,[[0,-1.12,.02],[.035,-.71,.03],[-.015,-.27,-.01],[.03,.22,.03],[0,.86,.04],[0,1.25,.04]],.043,rod);
 path(root,[[.01,-.73,.04],[-.038,-.48,.072],[.026,-.31,.05]],.018,bone);
 for(let i=0;i<6;i++){
  const y=-.76+i*.34;
  const band=new THREE.Mesh(new THREE.TorusGeometry(.048,.010,6,18),iron);band.position.set(0,y,.03);band.rotation.x=Math.PI*.5;root.add(band);
 }
 for(let i=0;i<7;i++){
  const a=i*Math.PI*2/7,dx=Math.sin(a),dz=Math.cos(a);
  path(root,[[dx*.025,1.02,dz*.025],[dx*.21,1.33,dz*.17],[dx*.165,1.61,dz*.10],[dx*.047,1.70,dz*.05]],.022,iron);
  cusp(root,dx*.11,1.54,dz*.08,.030,.19,bone,Math.PI*.13,dx*.4);
 }
 const cage=new THREE.Group();cage.position.set(0,1.43,.03);root.add(cage);
 const orb=bulb(cage,0,0,0,[.155,.155,.155],orbMat);parts.orb=orb;
 const halo=bulb(cage,0,0,0,[.24,.24,.24],glowMat);halo.castShadow=false;parts.orbHalo=halo;
 const lamp=new THREE.PointLight(0xaa58ff,.55,3.1,2);lamp.position.set(0,1.43,.03);root.add(lamp);parts.staffLight=lamp;
 parts.staffCrown=cage;
 for(let i=0;i<6;i++){
  const a=i*Math.PI/3,dx=Math.sin(a),dz=Math.cos(a);
  const glyph=bulb(root,dx*.22,1.42,dz*.22,[.027,.027,.027],orbMat);
  parts.runes.push(glyph);
 }
 const casting=bones.Rwrist;
 const spell=bulb(casting,0,.13,.12,[.11,.11,.11],orbMat);parts.spell=spell;
 necroCastingWisps(casting,parts);
}
function addWing(type,bones,parts,sign){
 const anchor=bones.chest,wing=new THREE.Group();wing.position.set(sign*.23,.16,-.16);anchor.add(wing);
 const finger=std('wingfinger',0x51454d);
 const tips=[[sign*.80,.44,-.10],[sign*1.96,.54,-.28],[sign*1.74,.13,-.47],[sign*1.34,-.33,-.52],[sign*.76,-.43,-.35]];
 const rootBone=new THREE.Bone();rootBone.name='WingRoot';wing.add(rootBone);
 const elbow=new THREE.Bone();elbow.name='WingElbow';elbow.position.set(sign*.42,.27,-.03);rootBone.add(elbow);
 const wrist=new THREE.Bone();wrist.name='WingWrist';wrist.position.set(sign*.39,.09,-.12);elbow.add(wrist);
 const fingers=[];
 for(let i=0;i<4;i++){const b=new THREE.Bone();b.name='WingFinger'+i;b.position.set(sign*.20,.08-i*.12,-.06);wrist.add(b);fingers.push(b);}
 const verts=[],uv=[],idx=[],indices=[],weights=[],N=20,M=20;
 for(let i=0;i<=N;i++){
  const seg=Math.min(3.999,i/N*4),k=Math.floor(seg),t=seg-k,A=tips[k],B=tips[k+1];
  const tx=A[0]+(B[0]-A[0])*t,ty=A[1]+(B[1]-A[1])*t,tz=A[2]+(B[2]-A[2])*t;
  for(let j=0;j<=M;j++){
   const r=j/M;
   const torn=(j===M?.94-.17*Math.abs(Math.sin(i*1.31+k*.7)):.98);
   const x=tx*r*torn,y=ty*r*torn+.10*Math.sin(Math.PI*r)*Math.cos(i*.37),z=tz*r*torn+.09*Math.sin(Math.PI*r)*Math.sin(i*.23);
   verts.push(x,y,z);uv.push(i/N,r);
   const tipBone=3+Math.min(k,3),v=clamp(r*1.8,0,1);
   indices.push(0,1,tipBone,0);weights.push((1-v)*.70,(1-v)*.30,v,0);
   if(i<N&&j<M){const a=i*(M+1)+j,b=a+M+1;idx.push(a,b,a+1,a+1,b,b+1);}
  }
 }
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
 geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
 geo.setAttribute('skinIndex',new THREE.Uint16BufferAttribute(indices,4));
 geo.setAttribute('skinWeight',new THREE.Float32BufferAttribute(weights,4));
 geo.setIndex(idx);geo.computeVertexNormals();
 wing.updateMatrixWorld(true);
 const skeleton=new THREE.Skeleton([rootBone,elbow,wrist,...fingers]);skeleton.calculateInverses();
 const sheet=new THREE.SkinnedMesh(geo,wingMaterial());sheet.bind(skeleton);sheet.castShadow=true;sheet.receiveShadow=true;
 sheet.frustumCulled=false;wing.add(sheet);
 for(const e of tips)path(wing,[[0,0,.015],[e[0]*.42,e[1]*.58,.04],[e[0]*.82,e[1]*.87,e[2]*.8],e],.020,finger);
 parts.wings.push({grp:wing,side:sign,elbow,wrist,fingers,membrane:sheet});
}
let WINGMAT=null;
function wingMaterial(){if(WINGMAT)return WINGMAT;
 const size=192,c=document.createElement('canvas');c.width=c.height=size;const ctx=c.getContext('2d');
 ctx.fillStyle='#7a5058';ctx.fillRect(0,0,size,size);
 for(let j=0;j<27;j++){const x=(j*89)%size,y=(j*47)%size,r=2+(j*17)%13;
  ctx.globalCompositeOperation='destination-out';ctx.beginPath();ctx.ellipse(x,y,r,r*.52,j*.3,0,Math.PI*2);ctx.fill();}
 ctx.globalCompositeOperation='source-over';ctx.strokeStyle='rgba(37,17,24,.52)';ctx.lineWidth=2;
 for(let i=0;i<17;i++){ctx.beginPath();ctx.moveTo(7+i*11,0);ctx.lineTo(35+i*8,size);ctx.stroke();}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;
 WINGMAT=new THREE.MeshStandardMaterial({color:0xc2a1a8,map:t,transparent:true,alphaTest:.25,side:THREE.DoubleSide,metalness:0,roughness:.75,depthWrite:true});return WINGMAT;
}
// Species-level anatomical pass. Distinct silhouettes and surface landmarks are
// attached to existing named bones; no changes are required to the enemy AI contract.
const ORGANIC_HEADS=new Map();
function organicCranium(parent,species,profile,material){
 let geom=ORGANIC_HEADS.get(species);
 if(!geom){
  const segments=28,verts=[],uv=[],ids=[],colors=[],rings=profile.length;
  for(let j=0;j<rings;j++){
   const [y,rx,rz,cy,cz]=profile[j];
   for(let i=0;i<=segments;i++){
    const a=i/segments*Math.PI*2,side=Math.cos(a),forward=Math.sin(a);
    const bump=1+.026*Math.sin(a*9+j*1.7)+.015*Math.sin(a*15+j*2.7);
    const ridge=forward>0?Math.pow(forward,4)*(.022*Math.sin(y*15+a*2)):0;
    verts.push(rx*side*bump, y, cy+(rz*forward+ridge)*bump+cz);
    uv.push(i/segments,j/(rings-1));
    const darken=.72+.24*Math.max(0,forward)+.04*Math.sin(a*7+j*1.7);
    colors.push(darken,darken*.92,darken*.90);
    if(j<rings-1&&i<segments){const q=j*(segments+1)+i;ids.push(q,q+segments+1,q+1,q+1,q+segments+1,q+segments+2);}
   }
  }
  geom=new THREE.BufferGeometry();geom.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
  geom.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geom.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geom.setIndex(ids);geom.computeVertexNormals();
  ORGANIC_HEADS.set(species,geom);
 }
 const m=new THREE.Mesh(geom,material);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function organicMat(id,color,rough=.79,metal=0){const key='organic:'+id;let mat=MAT[key];if(!mat){mat=new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal,vertexColors:true,side:THREE.DoubleSide});MAT[key]=mat;}return mat;}
function makeMuscle(parent,pts,r,mat){return path(parent,pts,r,mat);}
function addClawToes(bones,mat,boneMat,parts,count=4){
 for(const side of ['L','R']){const foot=bones[side+'foot'];
  for(let i=0;i<count;i++){const x=(i-(count-1)/2)*.085;
   const digit=path(foot,[[x*.7,-.02,.04],[x,-.055,.15],[x*1.12,-.075,.245]],.020,mat);
   const nail=cusp(foot,x*1.12,-.085,.27,.019,.14,boneMat,Math.PI*.60);
   parts.closeOnly.push(digit,nail);
  }
 }
}
function anatomicDetails(type,b,parts){
 const scar=std('anatomScar',0x4b252d,0,.73),pale=std('anatomTendon',0x877a7b,0,.84),
  ivory=std('anatomIvory',0xb5a5a0,0,.64),dark=std('anatomCrevice',0x281c22,0,.94),
  meat=std('anatomSinew',0x77535a,0,.66),skin=std('anatomDermis',0x6d585e,0,.71);
 if(type==='brute'){
  // Low recessed skull / huge shoulder cap, parted lips, stitched cheeks.
  parts.cranialShell=organicCranium(b.head,'brute',[
   [-.15,.08,.06,0,.07],[-.12,.22,.19,0,.10],[-.03,.25,.23,0,.10],[.08,.20,.18,0,.06],[.19,.14,.12,0,.02],[.29,.03,.04,0,.02]],organicMat('brute',0x89767b));
  for(const side of [-1,1]){
   path(b.head,[[side*.23,.06,.26],[side*.21,-.02,.36],[side*.15,-.10,.39]],.021,meat);
   path(b.head,[[side*.20,-.05,.34],[side*.24,-.13,.29],[side*.21,-.20,.21]],.009,scar);
   for(let k=0;k<4;k++){const x=side*(.08+k*.035),y=.12-k*.065;path(b.head,[[x,y,.29],[x+side*.018,y-.04,.32]],.006,scar);}
  }
  for(const side of ['L','R']){
   const shoulder=b[side+'shoulder'];
   const bulk=bulb(shoulder,0,.01,-.04,[.34,.30,.33],std('bruteDeltoid',0x716369,0,.88));parts.midOnly.push(bulk);
   for(let j=0;j<5;j++){const y=-.20-j*.09;
    const strap=path(b[side+'elbow'],[[-.16,y,.11],[0,y+.025,.19],[.16,y,.10]],.015,std('bruteLeather',0x2f2428,0,.9));parts.midOnly.push(strap);
   }
  }
  for(let i=0;i<7;i++){
   const y=.0-i*.09,x=Math.sin(i*.83)*.21;
   parts.closeOnly.push(stitchScar(b.spine,[[x-.13,y,.49],[x,y-.015,.55],[x+.13,y-.03,.50]],.006,scar,dark,4));
  }
  const left=path(b.chest,[[-.3,.20,.43],[-.25,-.11,.52],[-.12,-.28,.58]],.019,meat);
  const right=path(b.chest,[[.28,.25,.42],[.22,-.15,.52],[.14,-.29,.53]],.016,meat);
  parts.midOnly.push(left,right);parts.anatomy='heavy dermis, stitched wounds, heavy shoulders';
 }else if(type==='crawler'){
  // A long forward skull, exposed collar bones and continuous rib arc anatomy.
  parts.cranialShell=organicCranium(b.head,'crawler',[
   [-.19,.075,.09,0,.01],[-.15,.14,.17,0,.11],[-.06,.19,.19,0,.15],[.03,.18,.16,0,.13],[.13,.15,.11,0,.04],[.18,.035,.04,0,-.04]],organicMat('crawler',0x8e7b7f));
  path(b.head,[[0,.06,.20],[0,-.055,.43],[0,-.14,.48]],.022,std('crawlNoseBone',0x897c7d));
  for(const side of [-1,1]){
   path(b.head,[[side*.08,.085,.28],[side*.15,-.00,.40],[side*.12,-.10,.38]],.024,ivory);
   const fang=cusp(b.head,side*.13,-.13,.46,.035,.22,ivory,Math.PI*.55,side*.2);parts.midOnly.push(fang);
  }
  const ribMat=std('crawlRibSurface',0x8c7779,0,.78);
  for(let i=0;i<9;i++){
   const zz=.24-i*.11,y=.02-i*.013;
   for(const side of [-1,1]){
    const arch=path(b.spine,[[side*.085,y+.16,zz],[side*.22,y+.115,zz+.02],[side*.25,y-.05,zz+.055],[side*.14,y-.12,zz+.06]],.013+(i%3)*.003,ribMat);
    parts.midOnly.push(arch);
   }
  }
  for(const side of ['L','R']){
   const arm=b[side+'elbow'];
   for(let i=0;i<3;i++){
    const vein=path(arm,[[.04*i,-.02,-.03],[.04*i,-.18,.09],[.04*i,-.29,.13]],.008,meat);parts.closeOnly.push(vein);
   }
  }
  for(let i=0;i<6;i++){
   const zz=.30-i*.16;const dorsal=cusp(b.spine,0,.19,zz,.049,.21,ivory,-.36);parts.midOnly.push(dorsal);
  }
  addClawToes(b,skin,dark,parts,4);parts.anatomy='rib arches, exposed vertebrae, hooked teeth';
 }else if(type==='imp'){
  // Distorted infant-like face: forehead domes, irregular eye rims and thick mottled lips.
  parts.cranialShell=organicCranium(b.head,'imp',[
   [-.18,.07,.08,0,.04],[-.12,.29,.22,0,.08],[-.03,.38,.30,0,.10],[.11,.44,.34,0,.08],[.26,.42,.32,0,.06],[.37,.34,.26,0,.00],[.45,.15,.10,0,-.03],[.49,.015,.02,0,-.08]],organicMat('imp',0x934b62,.56));
  const flesh=std('impLips',0x713b4c,0,.47),wrink=std('impWrinkle',0x4c2b39,0,.87),vein=std('impVein',0xa77084,0,.70);
  for(const side of [-1,1]){
   const s=side;
   const ring=[];for(let i=0;i<=20;i++){
    const a=i/20*Math.PI*2;ring.push([s*.17+Math.cos(a)*.133,.12+Math.sin(a)*.113,.343+.02*Math.cos(a*2)]);
   }
   parts.closeOnly.push(path(b.head,ring,.019,flesh));
   parts.eyelids.push(setBaseScale(bulb(b.head,s*.17,.22,.34,[.127,.018,.057],flesh)));
   const tears=path(b.head,[[s*.06,.24,.33],[s*.11,.28,.29],[s*.16,.29,.25]],.009,vein);parts.closeOnly.push(tears);
   for(let j=0;j<3;j++){
    const y=.03-j*.035;
    parts.closeOnly.push(path(b.head,[[s*.08,y,.35],[s*.17,y-.02,.35],[s*.23,y-.03,.30]],.009,wrink));
   }
   const nostril=bulb(b.head,s*.045,-.032,.455,[.024,.018,.007],dark);parts.closeOnly.push(nostril);
  }
  const lip=path(b.head,[[-.105,-.068,.43],[-.05,-.085,.50],[0,-.077,.505],[.060,-.087,.495],[.115,-.050,.42]],.025,flesh);parts.midOnly.push(lip);
  const chin=bulb(b.head,0,-.16,.40,[.15,.06,.09],std('impLowerLip',0x865064,0,.53));parts.midOnly.push(chin);
  for(const side of ['L','R']){const fore=b[side+'elbow'];for(let j=0;j<3;j++){
   parts.closeOnly.push(path(fore,[[j*.022,-.02,.10],[j*.03,-.15,.11],[j*.025,-.26,.10]],.009,vein));
  }}
  addClawToes(b,skin,dark,parts,4);parts.anatomy='grossly oversized head, lip folds, orbital tissue';
 }else if(type==='wraith'){
  // Reference is much less cloaked than the name implies: exposed long bones,
  // hollow eyes, sinewy abdomen and only fragments of a hood.
  parts.cranialShell=organicCranium(b.head,'wraith',[
   [-.20,.065,.055,0,.08],[-.11,.125,.115,0,.12],[.01,.14,.11,0,.11],[.16,.145,.10,0,.06],[.23,.12,.09,0,.03],[.29,.03,.03,0,.03]],organicMat('wraith',0x726b71,.89));
  const sinew=std('wraithSinew',0x7a6971,0,.85),bone=std('wraithBoneRibs',0x8d8488,0,.89),shroud=std('wraithShred',0x38333b,0,.94);
  for(const side of [-1,1]){
   path(b.head,[[side*.11,.15,.18],[side*.14,.04,.24],[side*.07,-.15,.23]],.016,bone);
   const hoodTail=clothStrip(b.head,'wraith',side*.16,-.08,.65,shroud);
   hoodTail.bone.position.y=.24;parts.cloth.push(hoodTail);
  }
  for(let i=0;i<8;i++){
   const y=.24-i*.066,z=.27+i*.012;
   for(const side of [-1,1]){const rib=path(b.spine,[[side*.035,y+.01,z],[side*.15,y-.04,z+.07],[side*.18,y-.10,z-.02]],.014,bone);parts.midOnly.push(rib);}
  }
  for(const side of ['L','R']){
   const arm=b[side+'elbow'];
   for(let k=0;k<3;k++){const x=(k-1)*.045;
    const cord=path(arm,[[x,-.03,.05],[x*.8,-.22,.13],[x*1.5,-.38,.11]],.009,sinew);parts.closeOnly.push(cord);
   }
  }
  for(let k=0;k<6;k++){
   const x=(k%2?-.1:.1),z=(k%3)*.045;
   const r=clothStrip(b.pelvis,'wraith',x,z,.43+(k%3)*.13,shroud);r.bone.position.y=-.17;parts.cloth.push(r);
  }
  parts.anatomy='exposed rib cage, gaunt musculature, fragmented hood';
 }else if(type==='gargoyle'){
  // Beaked skeletal demon face with strong cranial ridges and horn cores.
  parts.cranialShell=organicCranium(b.head,'gargoyle',[
   [-.15,.065,.05,0,.06],[-.10,.17,.12,0,.06],[.00,.22,.19,0,.08],[.10,.22,.18,0,.05],[.20,.18,.15,0,.01],[.27,.08,.07,0,-.05],[.30,.015,.02,0,-.08]],organicMat('gargoyle',0x84777b,.91));
  const shell=std('gargBonyRidge',0x928489,0,.92),scales=std('gargScales',0x645760,0,.89),fangs=std('gargFangs',0xc0b3ab,0,.72);
  for(const side of [-1,1]){
   const s=side;
   path(b.head,[[s*.07,.26,.18],[s*.15,.24,.27],[s*.19,.12,.34],[s*.11,.03,.43]],.034,shell);
   path(b.head,[[s*.13,-.05,.33],[s*.20,-.10,.25],[s*.23,-.13,.16]],.025,scales);
   const horn=path(b.head,[[s*.16,.21,.02],[s*.26,.35,-.03],[s*.34,.42,-.16],[s*.40,.44,-.30]],.046,shell);parts.midOnly.push(horn);
   const tooth=cusp(b.head,s*.13,-.19,.45,.029,.17,fangs,Math.PI*.78);parts.closeOnly.push(tooth);
  }
  const beak=path(b.head,[[0,.01,.31],[0,-.065,.54],[0,-.12,.59]],.035,shell);parts.midOnly.push(beak);
  for(let k=0;k<9;k++){const z=-.18-k*.075,y=.13-(k*.011);const spike=cusp(b.chest,0,y,z,.058,.18,scales,-.65);parts.midOnly.push(spike);}
  for(const side of ['L','R']){
   for(let j=0;j<3;j++){
    const vein=path(b[side+'elbow'],[[j*.04,-.04,.02],[j*.03,-.14,.12],[j*.04,-.30,.10]],.012,shell);parts.closeOnly.push(vein);
   }
  }
  addClawToes(b,scales,fangs,parts,4);
  parts.tailSegments=[];
  for(let i=0;i<6;i++){
   const tail=new THREE.Group();b.pelvis.add(tail);
   if(i===0)tail.position.set(0,-.20,-.36);
   else{tail.position.set(0,-.06,-.21);parts.tailSegments[i-1].add(tail);}
   const piece=path(tail,[[0,0,0],[0,-.04,-.13],[0,-.05,-.26]],Math.max(.022,.081-i*.011),scales);
   parts.tailSegments.push(tail);parts.midOnly.push(piece);
  }
  parts.anatomy='beaked skull, horn ridges, scaly veins, flexible tail';
 }
}
function addDistinct(type,bones,parts){const b=bones,plan=SPEC[type],bone=std('bone',0xc7b9a1,0,.62),wound=std('wound',0x4f222c,0,.65);
 headDetails(type,b,parts);
 if(type!=='necromancer')anatomicDetails(type,b,parts);
 for(const s of ['L','R'])clawHand(b[s+'wrist'],plan,type,parts,s);
 if(type==='brute'){
  addCloth('brute',b,parts);
  for(const s of ['L','R']){
   const strap=new THREE.Mesh(new THREE.TorusGeometry(.22,.025,6,18),std('leather',0x30232a));strap.rotation.x=Math.PI/2;strap.position.y=-.18;b[s+'elbow'].add(strap);
  }
  for(let i=0;i<13;i++){
   const y=.35-i*.085,x=Math.sin(i*9)*.29;
   path(b.chest,[[x,y,.40],[x+.018,y+.02,.455],[x+.045,y+.035,.45]],.006,wound);
  }
 } else if(type==='crawler'){
  for(let i=0;i<9;i++){
   const z=.45-i*.13;const spine=cusp(b.spine,0,.1,z,.07,.19,bone,-.30);parts.details.push(spine);
  }
 } else if(type==='imp'){
  // Eyelids and brow ridges are built against the large eye sockets in the anatomy pass.
 }else if(type==='wraith'){
  addCloth('wraith',b,parts);
  for(let i=0;i<4;i++){
   const a=i*Math.PI*.5;const tail=clothStrip(b.head,'wraith',Math.sin(a)*.10,-.10,.45,std('shroud',0x494249));parts.cloth.push(tail);
  }
 }else if(type==='necromancer'){
  necroRobeShell(b,parts);addCloth('necromancer',b,parts);addStaff(b,parts);
  const armor=std('necroPauldronRim',0x60444d,.30,.52),trim=std('necroPauldronEdge',0x967480,.50,.41);
  for(const side of ['L','R']){
   const shoulder=bulb(b[side+'shoulder'],0,.02,.04,[.22,.13,.26],std('necroPauldron',0x33242d,.24,.51));parts.details.push(shoulder);
   path(b[side+'shoulder'],[[-.18,.045,.24],[0,.14,.26],[.19,.045,.24]],.019,trim);
   for(let i=0;i<4;i++){
    const x=(i-1.5)*.103;
    const spike=cusp(b[side+'shoulder'],x,.17,.005,.045,.28,armor,0,side==='L'?.18:-.18);parts.details.push(spike);
   }
  }
  for(const [x,y,z,size] of [[-.25,.51,.44,.96],[.24,.51,.44,.94],[.02,.29,.50,.63]]){
   necroSkullCharm(b.pelvis,x,y,z,size,parts);
   path(b.pelvis,[[x,.95,.35],[x*1.13,.71,.41],[x,y+.13,z]],.010,std('necroNecklace',0x6b5e65,.31,.49));
  }
  for(let i=0;i<6;i++){
   const x=(i%2?-.36:.36),z=.22+(i%3)*.045;
   const tail=clothStrip(b.chest,'necromancer',x,z,.68+i*.09,std('necroShred',i%2?0x32222a:0x45313a));
   tail.bone.position.y=-.15-i*.06;parts.cloth.push(tail);
  }
 }else if(type==='gargoyle'){
  addWing(type,b,parts,-1);addWing(type,b,parts,1);
  for(let k=0;k<7;k++){
   const s=cusp(b.chest,0,.27-k*.095,-.38,.055,.22,bone,.43);parts.details.push(s);
  }
  // An articulated tapering bony tail is constructed in the anatomy pass below.
 }
}
function build(type,bodyMat){if(!SPEC[type])throw Error('Unknown bestiary type: '+type);const plan=SPEC[type],group=new THREE.Group(),s=createSkeleton(plan,group),entry=geometries(type);
 const base=raster(type),material=bodyMat||base.clone();
 if(bodyMat){material.map=base.map;material.bumpMap=base.bumpMap;material.bumpScale=base.bumpScale;
  material.roughnessMap=base.roughnessMap;material.roughness=1;material.metalness=0;
  material.color.set(0xffffff);material.needsUpdate=true;}
 const lod=new THREE.LOD();group.add(lod);
 for(let i=0;i<3;i++){
  const mesh=new THREE.SkinnedMesh(entry.geoms[i],material);mesh.frustumCulled=false;mesh.castShadow=true;mesh.receiveShadow=true;
  mesh.bind(s.skeleton);lod.addLevel(mesh,[0,10,21][i]);
 }
 const parts={eyes:[],pupils:[],jaw:null,cloth:[],details:[],eyelids:[],wings:[],runes:[],orb:null,spell:null,staffLight:null,hoodShell:null,faceCranium:null,robeShells:[],robeRunes:[],trophies:[],wisps:[],staffCrown:null,orbHalo:null,orbMaterial:null,runeMat:null,wispMat:null,cranialShell:null,closeOnly:[],midOnly:[],tailSegments:[],anatomy:''};
 addDistinct(type,s.bones,parts);
 const run={type,plan,bones:s.bones,parts,mat:material,lod,mesh:group,clock:0,phase:Math.random()*6.28,
  spring:.0,springV:0,breath:0,stagger:0,attack:0,positionPrev:new THREE.Vector3(),
  normCount:entry.stats.triangles,geometryTime:entry.stats.ms,perch:type==='gargoyle',dying:false};
 group.userData.bestiary=run;group.userData.L=[];group.userData.legs=[];group.userData.wings=[];
 group.userData.detailMeshes=parts.details;group.userData.flight=type==='gargoyle';group.userData.type=type;
 return group;
}
function solveCrawlChain(rig,side,start,middle,end,phase,speed){
 const a=rig.plan.anchors[start],b=rig.plan.anchors[middle],c=rig.plan.anchors[end];
 const fx=c[0]+Math.sin(phase)*(speed*.15),fy=c[1]+Math.max(0,Math.sin(phase))*speed*.16,fz=c[2]+Math.cos(phase)*speed*.11;
 const vx=fx-a[0],vy=fy-a[1],vz=fz-a[2],dist=Math.max(.001,Math.hypot(vx,vy,vz));
 const len1=Math.hypot(b[0]-a[0],b[1]-a[1],b[2]-a[2]);
 const len2=Math.hypot(c[0]-b[0],c[1]-b[1],c[2]-b[2]);
 const d=Math.min(dist,len1+len2-.001),along=(len1*len1-len2*len2+d*d)/(2*d),h=Math.sqrt(Math.max(0,len1*len1-along*along));
 const inv=1/dist,ux=vx*inv,uy=vy*inv,uz=vz*inv;
 let px=side==='L'?-1:1,py=0,pz=0;
 const dot=px*ux+py*uy+pz*uz;px-=dot*ux;py-=dot*uy;pz-=dot*uz;
 const perp=Math.max(.0001,Math.hypot(px,py,pz));px/=perp;py/=perp;pz/=perp;
 const kx=a[0]+ux*along+px*h,ky=a[1]+uy*along+py*h,kz=a[2]+uz*along+pz*h;
 rig.bones[middle].position.set(kx-a[0],ky-a[1],kz-a[2]);
 rig.bones[end].position.set(fx-kx,fy-ky,fz-kz);
}
function update(entity,dt,absolute){const g=entity.mesh||entity,rig=g.userData.bestiary;if(!rig)return;
 if(entity.bestiaryDistance!==undefined&&entity.bestiaryDistance>40)return;
 const detailDistance=entity.bestiaryDistance===undefined?0:entity.bestiaryDistance;
 if(rig.type!=='necromancer'){
  const near=detailDistance<13,mid=detailDistance<25;
  for(let i=0;i<rig.parts.closeOnly.length;i++)rig.parts.closeOnly[i].visible=near;
  for(let i=0;i<rig.parts.midOnly.length;i++)rig.parts.midOnly[i].visible=mid;
 }
 dt=clamp(dt||1/60,.001,.08);rig.clock+=dt;const t=absolute===undefined?rig.clock:absolute;
 const plan=rig.plan,b=rig.bones,p=rig.parts;
 const state=entity.state||entity.ai||'idle',speed=clamp(entity.moveMag||entity.speedNow||0,0,1),
 attack=clamp(entity.pose===undefined?(entity.attackAnim||0):entity.pose,0,1),strike=clamp(entity.strike||0,0,1),
 hit=clamp(entity.hitT||entity.hit||0,0,1),dead=clamp(entity.deadT||0,0,1);
 const gait=t*(rig.type==='brute'?4.9:rig.type==='crawler'?11:rig.type==='imp'?12.5:rig.type==='gargoyle'?8:6)+rig.phase;
 const ga=Math.sin(gait),gb=Math.sin(gait+Math.PI),slow=Math.sin(t*1.7+rig.phase);
 b.spine.rotation.set(.025*slow+.08*attack,0,.06*ga*speed);
 b.chest.rotation.x=.015*Math.sin(t*2+rig.phase)+attack*.06;
 b.head.rotation.y=.08*Math.sin(t*.9+rig.phase);b.head.rotation.x=-.09+.06*Math.sin(t*1.2)+attack*.19;
 b.Lshoulder.rotation.x=.10+ga*.46*speed-attack*.63;b.Rshoulder.rotation.x=.10+gb*.46*speed-attack*.63;
 b.Lelbow.rotation.x=.06+.15*attack;b.Relbow.rotation.x=.06+.15*attack;
 b.Lwrist.rotation.z=ga*.09*speed;b.Rwrist.rotation.z=gb*.09*speed;
 b.Lhip.rotation.x=-ga*.26*speed;b.Rhip.rotation.x=-gb*.26*speed;
 b.Lknee.rotation.x=Math.max(0,ga)*.42*speed;b.Rknee.rotation.x=Math.max(0,gb)*.42*speed;
 b.Lfoot.rotation.x=-b.Lknee.rotation.x*.5;b.Rfoot.rotation.x=-b.Rknee.rotation.x*.5;
 const shock=(hit>0?Math.sin(hit*Math.PI)*.23:0);b.chest.rotation.z+=shock;b.head.rotation.x+=shock*.4;
 if(p.jaw)p.jaw.rotation.x=(rig.type==='brute'?.38:.09)+.09*slow+attack*(rig.type==='brute'?.67:.32);
 if(rig.type==='crawler'){
  b.spine.rotation.x=.12*Math.sin(gait*.7)*speed;
  b.chest.rotation.x=.18*Math.sin(gait*.7+1.2)*speed;
  b.Lshoulder.rotation.x=.52*ga*speed-.6*attack;
  b.Rshoulder.rotation.x=-.52*ga*speed-.6*attack;
  b.Lhip.rotation.x=-.42*ga*speed;
  b.Rhip.rotation.x=.42*ga*speed;
  solveCrawlChain(rig,'L','Lshoulder','Lelbow','Lwrist',gait,speed);
  solveCrawlChain(rig,'R','Rshoulder','Relbow','Rwrist',gait+Math.PI,speed);
  solveCrawlChain(rig,'L','Lhip','Lknee','Lfoot',gait+Math.PI,speed);
  solveCrawlChain(rig,'R','Rhip','Rknee','Rfoot',gait,speed);
 }
 if(rig.type==='imp'){
  const hop=Math.max(0,Math.sin(gait))*.10*speed;
  b.spine.scale.y=1-hop*.18;b.head.scale.set(1+hop*.17,1-hop*.1,1+hop*.1);
  const blink=Math.sin(t*.73+rig.phase)> .995?.08:1;
  for(const eye of p.eyes){const base=eye.userData.baseScale; if(base)eye.scale.set(base.x,base.y*blink,base.z);} 
  for(const lid of p.eyelids){const base=lid.userData.baseScale; if(base)lid.position.y=(lid.userData.baseY-(1-blink)*.06);} 
  const dilation=.85+.18*Math.sin(t*1.6);
  for(const pupil of p.pupils){const base=pupil.userData.baseScale; if(base)pupil.scale.set(base.x*dilation,base.y*dilation,base.z);}
 }
 if(rig.type==='wraith'){
  b.spine.rotation.z=.08*Math.sin(t*.76);
  b.Lshoulder.rotation.x=.09*Math.sin(t*1.04)-.25*attack;
  b.Rshoulder.rotation.x=.09*Math.sin(t*1.16)-.25*attack;
  const dissolve=entity.teleportT||entity.tpFade||0;
  if(dissolve>0){rig.mat.transparent=true;rig.mat.opacity=clamp(1-dissolve*.8,.10,1);rig.mat.depthWrite=rig.mat.opacity>.8;}
  else if(rig.mat.transparent){rig.mat.opacity=1;rig.mat.transparent=false;rig.mat.depthWrite=true;}
 }
 if(rig.type==='brute'){
  b.spine.scale.set(1+.016*Math.sin(t*1.30),1+.031*Math.sin(t*1.30),1+.015*Math.sin(t*1.30));
  b.chest.rotation.x+=.10*attack+.025*slow;
  b.Lshoulder.rotation.x=.18+ga*.34*speed-attack*.84;
  b.Rshoulder.rotation.x=.18+gb*.34*speed-attack*.84;
  b.head.rotation.x-=.10+attack*.29;
  if(p.jaw)p.jaw.rotation.x=.33+.32*attack+.10*Math.max(0,slow);
 }
 if(rig.type==='crawler'){
  b.head.rotation.x=-.18+.12*Math.sin(gait*.8)+attack*.34;
  b.head.rotation.z=.07*Math.sin(gait*.7);
  if(p.jaw)p.jaw.rotation.x=.16+.50*attack;
 }
 if(rig.type==='wraith'){
  b.head.rotation.x-=.06;
  b.chest.rotation.x+=.025*Math.sin(t*.85);
  b.Lshoulder.rotation.z=.13*Math.sin(t*.92);
  b.Rshoulder.rotation.z=-.13*Math.sin(t*.87);
 }
 if(rig.type==='gargoyle'){
  b.head.rotation.x=-.10+.24*attack;
  b.Lshoulder.rotation.x+=.29*attack;
  b.Rshoulder.rotation.x+=.29*attack;
  if(p.jaw)p.jaw.rotation.x=.13+.45*attack;
  for(let k=0;k<p.tailSegments.length;k++){
   p.tailSegments[k].rotation.y=.055*Math.sin(t*2+k*.55);
   p.tailSegments[k].rotation.x=.025*Math.sin(t*1.4+k*.70);
  }
 }
 if(rig.type==='necromancer'){
  b.Lshoulder.rotation.x=-.05+.08*Math.sin(t*.6);b.Lelbow.rotation.x=-.11;
  b.Rshoulder.rotation.x=-.28-attack*.95;b.Relbow.rotation.x=-.16-attack*.43;
  b.Rwrist.rotation.z=.10*Math.sin(t*1.5)-attack*.35;
  const pulse=.5+.5*Math.sin(t*3.9+rig.phase),flare=clamp(attack*.7+strike*.5,0,1);
  if(p.orb)p.orb.scale.setScalar(1+.12*pulse+.55*flare);
  if(p.orbHalo)p.orbHalo.scale.setScalar(1+.13*pulse+.32*flare);
  if(p.staffLight)p.staffLight.intensity=.24+.18*pulse+.46*flare;
  if(p.orbMaterial)p.orbMaterial.opacity=.73+.19*pulse+.08*flare;
  if(p.runeMat)p.runeMat.opacity=.38+.28*pulse+.32*flare;
  if(p.wispMat)p.wispMat.opacity=.43+.25*pulse+.27*flare;
  for(let i=0;i<p.runes.length;i++){
   const a=t*.85+i*Math.PI/3;
   p.runes[i].position.x=Math.sin(a)*.22;p.runes[i].position.z=.03+Math.cos(a)*.22;
  }
  if(p.spell)p.spell.scale.setScalar(.48+.36*pulse+.72*flare);
  const distance=entity.bestiaryDistance===undefined?0:entity.bestiaryDistance;
  if(p.staffLight)p.staffLight.visible=distance<16;
  if(p.orbHalo)p.orbHalo.visible=distance<24;
  for(let i=0;i<p.robeRunes.length;i++)p.robeRunes[i].visible=distance<22;
  for(let i=0;i<p.trophies.length;i++){
    const trophy=p.trophies[i];trophy.visible=distance<26;
    trophy.rotation.z=.035*Math.sin(t*1.45+i*1.5);
  }
  for(let i=0;i<p.wisps.length;i++){
   const w=p.wisps[i];w.group.visible=distance<16;
   if(w.group.visible){
    w.group.rotation.y=t*.51+w.phase;
    w.group.rotation.z=.13*Math.sin(t*1.8+w.phase);
    w.group.scale.setScalar(.75+.15*pulse+.29*flare);
   }
  }
 }
 if(rig.type==='gargoyle'){
  const wakes=state!=='idle'&&state!=='perched';
  rig.perch=!entity.alert||!wakes;
  for(const w of p.wings){const fold=rig.perch?.85:.19;
   w.grp.rotation.y=w.side*(fold+Math.sin(t*(wakes?7:1.4))*(wakes?.22:.016));
   w.grp.rotation.z=w.side*(wakes?.16+.18*Math.cos(t*4.8):.07);
   w.elbow.rotation.x=(wakes?.16:0);w.wrist.rotation.y=w.side*(wakes?.14:.03);
   for(let i=0;i<4;i++)w.fingers[i].rotation.y=Math.sin(t*5+i)*.02;
  }
 }
 const delta=slow*.14+attack*.28;rig.springV+=(delta-rig.spring)*dt*48;rig.springV*=Math.exp(-dt*12);rig.spring+=rig.springV*dt;
 for(let i=0;i<p.cloth.length;i++){
  const s=p.cloth[i],dest=rig.spring+.075*Math.sin(t*2.3+i*.72);
  s.velocity+=(dest-s.value)*dt*35;s.velocity*=Math.exp(-dt*7);s.value+=s.velocity*dt;
  s.bone.rotation.z=s.value*.3;s.bone.rotation.x=s.value*.5;
 }
 if(dead>0){b.pelvis.rotation.z=dead*.90;b.spine.rotation.x=dead*.45;}
}
function voice(type,context,violent){const profile={brute:[64,34,.68,'sawtooth'],crawler:[270,70,.16,'triangle'],imp:[710,210,.28,'sawtooth'],wraith:[220,80,.75,'sine'],necromancer:[145,68,.81,'triangle'],gargoyle:[480,115,.40,'sawtooth']}[type];
 if(!context||!profile)return;try{if(context.state==='suspended')context.resume();const t=context.currentTime,
  o=context.createOscillator(),f=context.createBiquadFilter(),v=context.createGain();
  o.type=profile[3];o.frequency.setValueAtTime(profile[0]*(violent?1.18:1),t);o.frequency.exponentialRampToValueAtTime(profile[1],t+profile[2]);
  f.type='lowpass';f.frequency.setValueAtTime(type==='imp'?3500:1100,t);f.frequency.exponentialRampToValueAtTime(200,t+profile[2]);
  v.gain.setValueAtTime(.0001,t);v.gain.exponentialRampToValueAtTime(.08,t+.03);v.gain.exponentialRampToValueAtTime(.0001,t+profile[2]);
  o.connect(f);f.connect(v);v.connect(context.destination);o.start(t);o.stop(t+profile[2]+.02);
 }catch(e){return;}}
function tryGLB(type,url,loader,onModel,onFail){if(!loader||!url){if(onFail)onFail('No GLTFLoader or GLB path; procedural model remains active');return;}
 loader.load(url,gltf=>{if(gltf&&gltf.scene&&onModel)onModel(gltf.scene);},undefined,err=>{if(onFail)onFail(err&&err.message||String(err));});}
function adaptEnemyId(id){return ({chaser:'imp',brute:'brute',crawler:'crawler',teleporter:'wraith',necromancer:'necromancer',winged:'gargoyle',imp:'imp',gargoyle:'gargoyle',wraith:'wraith'})[id]||null;}
function buildEnemyModel(type,bodyMat,glowMat,darkMat){const species=adaptEnemyId(type)||type;if(!SPEC[species])return null;const grp=build(species,bodyMat);return {grp,parts:grp.userData.bestiary.parts};}
root.DEPTHS_BESTIARY={build,buildEnemyModel,update,voice,tryGLB,adaptEnemyId,TYPES,SPEC,PIXEL_PALETTES,geometryStats:()=>Object.fromEntries([...GEOMETRY.entries()].map(([k,v])=>[k,v.stats]))};
})(typeof window!=='undefined'?window:globalThis);

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
</script></body></html>"""
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
