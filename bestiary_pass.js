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
