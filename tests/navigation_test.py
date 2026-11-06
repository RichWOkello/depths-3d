"""The flow field must lead walking enemies around a wall to a nearby player."""
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
src=(R/'src/game.js').read_text()
needle='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert needle in src
src=src.replace(needle,r'''
window.__navigationTest=()=>{
  level=5;buildLevel();
  state='playing';paused=false;
  P.x=6;P.z=6;P.hp=10000;
  const nav=getMonsterNavigation(),reachable=[];
  for(let y=1;y<GH-1;y++)for(let x=1;x<GW-1;x++){
    const i=y*GW+x,d=nav[i];if(d>7&&!los(P.x,P.z,(x+.5)*CELL,(y+.5)*CELL))reachable.push({x,y,d});
  }
  reachable.sort((a,b)=>b.d-a.d);
  if(!reachable.length)throw Error('No remote maze cells found');
  const chosen=reachable[0];
  enemies=[];addEnemy('chaser',(chosen.x+.5)*CELL,(chosen.y+.5)*CELL);
  const e=enemies[0];e.alert=true;e.speed=3.8;
  const point=monsterWaypoint(e,false),before=nav[chosen.y*GW+chosen.x];
  const pCell=[Math.floor(point.x/CELL),Math.floor(point.z/CELL)];
  const next=nav[pCell[1]*GW+pCell[0]];
  for(let i=0;i<300;i++)update(.025);
  const after=nav[Math.floor(e.z/CELL)*GW+Math.floor(e.x/CELL)];
  return {before,next,after,progress:before-after,remainingHP:P.hp,legContacts:e.mesh.userData.legs.map(l=>l.contactCount)};
};
''' + needle,1)
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1024,'height':760})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
  page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
  page.add_script_tag(content=src)
  page.wait_for_selector('[data-a="skipintro"]')
  r=page.evaluate('window.__navigationTest()')
  assert r['next']<r['before'],r
  assert r['progress']>=2,r
  assert sum(r['legContacts'])>=2,r
  assert not errors,errors
  print('PASS: maze-aware enemy path, physical footfall contacts:',r)
  b.close()
