(function(){
class V{constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;}set(x,y,z){this.x=x;this.y=y;this.z=z;return this;}copy(v){return this.set(v.x,v.y,v.z);}clone(){return new V(this.x,this.y,this.z);}dot(v){return this.x*v.x+this.y*v.y+this.z*v.z;}addScaledVector(v,s){this.x+=v.x*s;this.y+=v.y*s;this.z+=v.z*s;return this;}normalize(){let n=Math.hypot(this.x,this.y,this.z)||1;this.x/=n;this.y/=n;this.z/=n;return this;}crossVectors(a,b){return this.set(a.y*b.z-a.z*b.y,a.z*b.x-a.x*b.z,a.x*b.y-a.y*b.x);}setScalar(n){return this.set(n,n,n);} }
class O{constructor(){this.children=[];this.position=new V;this.rotation={x:0,y:0,z:0,set(x,y,z){this.x=x;this.y=y;this.z=z;}};this.scale=new V(1,1,1);this.userData={};this.visible=true;}add(...args){for(const a of args){this.children.push(a);a.parent=this;}return this;}updateMatrixWorld(){} }
class G extends O{constructor(){super();this.attributes={};this.index={count:0};this.boundingSphere={radius:1};}setAttribute(n,v){this.attributes[n]=v;return this;}setIndex(v){this.index={array:v,count:v.length};return this;}computeVertexNormals(){this.attributes.normal={count:this.attributes.position.array.length/3};}computeBoundingSphere(){} }
class A{constructor(array,size){this.array=array;this.itemSize=size;this.count=array.length/size;}}
class M{constructor(props={}){Object.assign(this,props);this.color={set(){}};}clone(){return new M(this);} }
class Mesh extends O{constructor(geo,mat){super();this.geometry=geo;this.material=mat;this.isMesh=true;}bind(s){this.skeleton=s;}}
class LOD extends O{constructor(){super();this.levels=[];}addLevel(o,d){this.add(o);this.levels.push({object:o,distance:d});}}
class Skin extends O{constructor(bones){super();this.bones=bones;}calculateInverses(){}}
class T extends O{constructor(){super();this.repeat={set(){}};}}
class Curve{constructor(pts){this.pts=pts;}}
const three={Vector3:V,Group:O,Bone:class extends O{},Mesh,SkinnedMesh:Mesh,LOD,Skeleton:Skin,BufferGeometry:G,Float32BufferAttribute:A,Uint16BufferAttribute:A,CanvasTexture:T,MeshStandardMaterial:M,MeshPhysicalMaterial:M,MeshBasicMaterial:M,SphereGeometry:G,ConeGeometry:G,TorusGeometry:G,TubeGeometry:G,CatmullRomCurve3:Curve,PointLight:class extends O{},DoubleSide:2,FrontSide:0,RepeatWrapping:1000};
window.THREE=three;
})();
