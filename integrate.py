from pathlib import Path
from shutil import copytree,copy2
ROOT=Path('/mnt/data/Depths3D_Bestiary_v5.2.0_Build')
SOURCE=Path('/mnt/data/Depths3D_v5.2.0_Sculpted_Creatures_Upgrade')
for name in ['src/game.html','README.md','LICENSE','CHANGELOG.md','.nojekyll','.gitignore']:
 target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);copy2(SOURCE/name,target)
(ROOT/'src/bestiary_pass.js').write_text((ROOT/'bestiary_pass.js').read_text())
s=(SOURCE/'src/game.js').read_text()
s=s.replace("chaser:'FLESH GHOUL',brute:'GRAVE BRUTE',crawler:'CRYPT CRAWLER',", "chaser:'FLESH IMP',brute:'FLESH BRUTE',crawler:'CRYPT CRAWLER',")
s=s.replace("stalker:'DUSK STALKER',necromancer:'ASHEN NECROMANCER',", "stalker:'DUSK STALKER',teleporter:'GAUNT HOODED WRAITH',necromancer:'NECROMANCER',")
s=s.replace("winged:'WINGED HORROR',armored:'CHAINED GRAVE BRUTE'", "winged:'WINGED GARGOYLE',armored:'CHAINED FLESH BRUTE'")
# preserve actual internal game identifiers, use bestiary aliases only for theme pools
start=s.index('const ENEMY_POOLS=[');end=s.index('function chooseThemeEnemy()',start)
segment=s[start:end].replace("['chaser'", "['imp'").replace("['winged'", "['gargoyle'")
s=s[:start]+segment+s[end:]
s=s.replace("const valid=pool.filter(([type])=>level>=({brute:3,armored:5,necromancer:4,stalker:2,crawler:2,teleporter:2,splitter:2,winged:3}[type]||1));", "const valid=pool.filter(([type])=>level>=({brute:3,armored:5,necromancer:4,stalker:2,crawler:2,teleporter:2,splitter:2,gargoyle:3,imp:1}[type]||1));")
s=s.replace("    addEnemy(chooseThemeEnemy(),p[0],p[1]);", "    const kind=chooseThemeEnemy();addEnemy(kind,p[0],p[1]);\n    if(kind==='imp'&&level>=3&&Math.random()<.19&&enemies.length<36){\n      for(let j=0;j<3;j++){const xx=p[0]+Math.cos(j*2.09)*.84,zz=p[1]+Math.sin(j*2.09)*.84;\n        if(!blocked(xx,zz,.3))addEnemy('imp',xx,zz);}\n    }")
s=s.replace("function addEnemy(type,x,z){\n  const s=", "function addEnemy(type,x,z){\n  type=({imp:'chaser',gargoyle:'winged',wraith:'teleporter'})[type]||type;\n  const s=")
old="""  const visual={armored:'brute'}[type]||type;
  const mesh=buildMonster(visual,mat);"""
new="""  const visual={armored:'brute'}[type]||type;
  const bestiaryId=window.DEPTHS_BESTIARY.adaptEnemyId(type);
  const mesh=bestiaryId?window.DEPTHS_BESTIARY.build(bestiaryId,mat):buildMonster(visual,mat);
  if(bestiaryId)y=window.DEPTHS_BESTIARY.SPEC[bestiaryId].baseY;
  if(bestiaryId==='imp')mesh.scale.setScalar(.94+Math.random()*.16);"""
assert old in s;s=s.replace(old,new,1)
old="""  if(type==='necromancer'){
    const orb=new THREE.Mesh(new THREE.IcosahedronGeometry(.19,1),new THREE.MeshBasicMaterial({color:0x7debd4}));"""
new="""  if(type==='necromancer'&&!mesh.userData.bestiary){
    const orb=new THREE.Mesh(new THREE.IcosahedronGeometry(.19,1),new THREE.MeshBasicMaterial({color:0x7debd4}));"""
assert old in s;s=s.replace(old,new,1)
# Normal combat still happens under original internal types, with new art created by the adapter
old="""function animMonster(e,dt){
  const U=e.mesh.userData;if(!U.L)return;"""
new="""function animMonster(e,dt){
  const U=e.mesh.userData;
  if(U.bestiary){
    window.DEPTHS_BESTIARY.update(e,dt,time);
    e.bodyLift=U.bestiary.type==='wraith'?.07*Math.sin(time*1.9+e.ph):
      U.bestiary.type==='gargoyle'?.07+Math.sin(time*2.8+e.ph)*.11-Math.sin(Math.PI*Math.min(1,(e.diveTime||0)/1.05))*.28:0;
    return;
  }
  if(!U.L)return;"""
assert old in s;s=s.replace(old,new,1)
s=s.replace("    const visible=d<(e.type==='stalker'?13:22)&&los(e.x,e.z,P.x,P.z);", "    const visible=d<(e.type==='stalker'?13:22)&&los(e.x,e.z,P.x,P.z);\n    e.bestiaryDistance=d;e.tpFade=Math.max(0,(e.tpFade||0)-dt*2.1);")
s=s.replace("if(!e.alert&&visible&&d<20){e.alert=true;e.ai='pursue';growl(e,e.type==='brute'||e.type==='boss');}", "if(!e.alert&&visible&&d<20){e.alert=true;e.ai='pursue';growl(e,e.type==='brute'||e.type==='boss');\n      if(e.type==='winged')burst(e.x,e.baseY-.6,e.z,0xa49e99,15,2);}")
s=s.replace("if(!blocked(nx,nz,0.6)){ burst(e.x,1.4,e.z,0x33ddff,10,4);", "if(!blocked(nx,nz,0.6)){ e.tpFade=.8;burst(e.x,1.4,e.z,0x33ddff,10,4);")
# night wraith ranged orb (existing projectile update already exists)
s=s.replace("const ranged=(e.type==='shooter'||e.type==='boss'||e.type==='necromancer');", "const ranged=(e.type==='shooter'||e.type==='boss'||e.type==='necromancer'||e.type==='teleporter');")
s=s.replace("e.type==='necromancer'?2.4:1.5+Math.random()*.8", "e.type==='necromancer'?2.4:e.type==='teleporter'?3.1:1.5+Math.random()*.8")
s=s.replace("orbs.push({mesh:m,x:e.x,z:e.z,vx:(ux*ca-uz*sa)*9,vz:(ux*sa+uz*ca)*9,life:4});", "orbs.push({mesh:m,x:e.x,z:e.z,vx:(ux*ca-uz*sa)*9,vz:(ux*sa+uz*ca)*9,life:4,wraith:e.type==='teleporter'});")
s=s.replace("    o.x+=o.vx*dt; o.z+=o.vz*dt; o.life-=dt;", "    if(o.wraith){const dx=P.x-o.x,dz=P.z-o.z,len=Math.max(.001,Math.hypot(dx,dz));\n      o.vx+=((dx/len)*6-o.vx)*Math.min(1,dt*1.2);o.vz+=((dz/len)*6-o.vz)*Math.min(1,dt*1.2);}\n    o.x+=o.vx*dt; o.z+=o.vz*dt; o.life-=dt;")
# gargoyle bullet damage reduction while perched
old="""  if(e.type==='boss'&&e.bossKind===1&&e.shieldT>0)damage*=.35;
  e.hp-=damage;"""
new="""  if(e.type==='boss'&&e.bossKind===1&&e.shieldT>0)damage*=.35;
  if(e.type==='winged'&&!e.alert)damage*=.40;
  e.hp-=damage;"""
assert old in s;s=s.replace(old,new,1)
# Add synthesis compatible with original Web Audio user gesture gate
s=s.replace("function creatureSound(type,x,z,attack=false){\n  if(!actx||SET.vol<=0)return;", "function creatureSound(type,x,z,attack=false){\n  if(!actx||SET.vol<=0)return;\n  const bestiaryType=window.DEPTHS_BESTIARY&&window.DEPTHS_BESTIARY.adaptEnemyId(type);\n  if(bestiaryType){window.DEPTHS_BESTIARY.voice(bestiaryType,actx,attack);return;}")
# one full parented prefab fallback path for optional GLB loaded via GLTFLoader
s=s.replace("  mesh.position.set(x,y,z); levelGroup.add(mesh);", """  mesh.position.set(x,y,z); levelGroup.add(mesh);
  if(bestiaryId&&window.DEPTHS_BESTIARY_GLBS&&window.THREE.GLTFLoader){
    const url=window.DEPTHS_BESTIARY_GLBS[bestiaryId];
    if(url){const loader=new THREE.GLTFLoader();
      window.DEPTHS_BESTIARY.tryGLB(bestiaryId,url,loader,(sculpt)=>{
        if(!mesh.parent)return;
        mesh.children.forEach(o=>o.visible=false);
        mesh.add(sculpt);sculpt.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
      },err=>console.warn('Bestiary GLB fallback:',err));}
  }""",1)
# keep prior game source separate from addon to maintain a single source of truth
(ROOT/'src/game_base.js').write_text(s)
print('Created integrated source',len(s),'characters', 'source sections',s.count('DEPTHS_BESTIARY'))
