"""Regression: real two-joint leg rigs, pinned stance, swing clearance and six-themed wall reliefs."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'src/game.js').read_text('utf-8')
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in src
src=src.replace(marker,r'''
window.__gaitTest={
 shapes:()=>{
   const out={};for(const type of ['chaser','brute','boss','splitter','mini','shooter','teleporter']){
     const mon=buildMonster(type,new THREE.MeshStandardMaterial({color:0x999999}));
     out[type]={legs:mon.userData.legs.length,arms:mon.userData.L.length,
       segmented:mon.userData.legs.every(l=>l.upperMesh&&l.lowerMesh&&l.kneeMesh&&l.foot)};
   }return out;
 },
 anchored:()=>{
   level=1;buildLevel();enemies=[];state='playing';paused=false;
   addEnemy('chaser',8,8);const e=enemies[0];e.alert=true;e.yaw=.4;e.gait=0;
   e.moveMag=.65;e.actualVX=1.8;e.actualVZ=0;
   animMonster(e,.016);
   const left=e.mesh.userData.legs[0],initial=left.lastFoot;
   const pin={...left.pin},k0=left.kneeMesh.position.clone();
   e.x+=.25;e.gait=.20;animMonster(e,.016);
   const after=left.lastFoot;
   const anchorError=Math.hypot(pin.x-after.x,pin.z-after.z);
   const kneeTravel=k0.distanceTo(left.kneeMesh.position);
   e.gait=Math.PI*2*.75;animMonster(e,.016);
   const air=left.lastFoot.y;
   e.gait=Math.PI*2*1.04;animMonster(e,.016);
   return {anchorError,kneeTravel,air,ground:initial.y,landings:left.contactCount,
      legBones:left.upperMesh.geometry&&left.lowerMesh.geometry?2:0};
 },
 facades:()=>{
   const data=[];for(let i=1;i<=6;i++){
     level=i;buildLevel();data.push({theme:currentTheme.name,
       facadeBatches:levelGroup.children.filter(o=>o.userData.cathedralFacade).length,
       objects:levelGroup.children.length});
   }return data;
 }
};
''' + marker,1)
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1000,'height':760})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content('<html><body>'+(ROOT/'src/game.html').read_text('utf-8')+'</body></html>')
  page.add_script_tag(content=(ROOT/'tests/mock_three.js').read_text('utf-8'))
  page.add_script_tag(content=src)
  page.wait_for_selector('[data-a="skipintro"]')
  species=page.evaluate('window.__gaitTest.shapes()')
  assert species['chaser']['legs']==2 and species['brute']['legs']==2 and species['boss']['legs']==2,species
  assert species['splitter']['legs']==6 and species['mini']['legs']==6,species
  assert species['shooter']['legs']==0 and species['teleporter']['legs']==0,species
  assert all(x['segmented'] for x in species.values()),species
  anchored=page.evaluate('window.__gaitTest.anchored()')
  assert anchored['anchorError']<.00001,anchored
  assert anchored['kneeTravel']>.01,anchored
  assert anchored['air']>.065 and abs(anchored['ground']-.065)<1e-6,anchored
  assert anchored['landings']>=1,anchored
  walls=page.evaluate('window.__gaitTest.facades()')
  assert len({w['theme'] for w in walls})==6,walls
  assert all(w['facadeBatches']==6 for w in walls),walls
  assert not errors,errors
  print('PASS: anatomical and multi-legged rigs:',species)
  print('PASS: foot planting/swing/knee and contacts:',anchored)
  print('PASS: six Gothic environments with instanced wall-relief batches:',walls)
  print('PASS: no JavaScript exceptions')
  browser.close()
