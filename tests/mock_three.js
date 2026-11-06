// Lightweight smoke-testing stand-in for Three.js. Validates game startup
// and menu/input wiring without requiring a GPU or external CDN.
(function(){
 class Vec3 {
   constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;}
   set(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;return this;}
   copy(o){this.x=o.x;this.y=o.y;this.z=o.z;return this;}
   clone(){return new Vec3(this.x,this.y,this.z);}
   sub(o){this.x-=o.x;this.y-=o.y;this.z-=o.z;return this;}
   add(o){this.x+=o.x;this.y+=o.y;this.z+=o.z;return this;}
   multiplyScalar(n){this.x*=n;this.y*=n;this.z*=n;return this;}
   length(){return Math.hypot(this.x,this.y,this.z);}
   setScalar(n){return this.set(n,n,n);}
   lerp(o,t){this.x+=(o.x-this.x)*t;this.y+=(o.y-this.y)*t;this.z+=(o.z-this.z)*t;return this;}
   normalize(){return this.multiplyScalar(1/(this.length()||1));}
   project(){return this;}
   distanceTo(o){return Math.hypot(this.x-o.x,this.y-o.y,this.z-o.z);}
 }
 class Color {constructor(v){this.value=v;} set(v){this.value=v;return this;} setHex(v){return this.set(v);} clone(){return new Color(this.value)} setRGB(r,g,b){this.r=r;this.g=g;this.b=b;return this;} }
 class Obj {
   constructor(){this.children=[];this.position=new Vec3;this.rotation={x:0,y:0,z:0,order:'XYZ',set(){}};this.scale=new Vec3(1,1,1);this.quaternion={setFromUnitVectors(){},setFromAxisAngle(){}};this.userData={};this.visible=true;this.color=new Color(0);this.repeat={set(){}};this.instanceMatrix={needsUpdate:false};this.material={color:new Color(0),emissive:new Color(0)};this.geometry={};}
   add(...args){for(const c of args){this.children.push(c);c.parent=this;}return this;}
   remove(c){this.children=this.children.filter(x=>x!==c);if(c&&c.parent===this)c.parent=null;return this;}
   clone(){let o=new Obj();Object.assign(o,this);o.children=[...this.children];return o;}
   setMatrixAt(){} set() {return this;} setAttribute(name,attr){this.attributes=this.attributes||{};this.attributes[name]=attr;return this;} setIndex(idx){this.index=idx;return this;} setFromPoints(){return this;} dispose(){} computeVertexNormals(){}
   setPosition(){} lookAt(){} updateProjectionMatrix(){} rotateX(){}
   getPoint(t){return new Vec3(0,0,t)} getTangent(t){return new Vec3(0,0,1)} getPoints(){return [new Vec3(0,0,0),new Vec3(0,0,1)]}
 }
 class Material extends Obj {
   constructor(o={}){super();Object.assign(this,o);this.color=new Color(o.color);this.emissive=new Color(o.emissive||0);}
   clone(){return new Material({color:this.color.value,emissive:this.emissive.value,opacity:this.opacity});}
 }
 class Shape extends Obj {moveTo(){} lineTo(){}closePath(){}absarc(){} quadraticCurveTo(){} }
 class Renderer extends Obj {
   constructor(){super();this.domElement=document.createElement('canvas')}
   setPixelRatio(){} setSize(){} render(){} dispose(){}
 }
 class Texture extends Obj {constructor(){super();this.repeat={set(){}}} }
 const things={Vector3:Vec3,Color:Color,WebGLRenderer:Renderer,Shape:Shape,BufferAttribute:class{constructor(array,size){this.array=array;this.itemSize=size;this.needsUpdate=false;}},Float32BufferAttribute:class{constructor(array,size){this.array=array;this.itemSize=size;this.needsUpdate=false;}},
   MeshStandardMaterial:Material,MeshPhysicalMaterial:Material,MeshBasicMaterial:Material,LineBasicMaterial:Material,SpriteMaterial:Material,
   CanvasTexture:Texture,InstancedMesh:class extends Obj{constructor(){super()}},
   Mesh:class extends Obj{constructor(geo,mat){super();this.geometry=geo;this.material=mat;this.userData={};this.isMesh=true;}},
   Sprite:class extends Obj{constructor(mat){super();this.material=mat;this.isSprite=true;}},
   SphereGeometry:class extends Obj{constructor(){super();this.attributes={position:{count:1,getX(){return 0},getY(){return 1},getZ(){return 0},setXYZ(){}}};}},
   Fog:class extends Obj{constructor(c){super();this.color=new Color(c)}}};
 window.THREE=new Proxy(things,{get(target,name){if(name in target)return target[name];if(typeof name!=='string')return undefined;if(name.toUpperCase()===name)return 1;return class extends Obj{};}});
})();
