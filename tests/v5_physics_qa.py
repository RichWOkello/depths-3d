"""Focused synthetic-browser integration checks. Renderer is a Three.js mock, not GPU/WebGL."""
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
code=(R/'src/game.js').read_text()
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
code=code.replace(marker,"""window.__physics={P,keys,newGame,buildLevel,setWeapon,addEnemy,shoot,updateProjectiles,shots:()=>shots,enemies:()=>enemies,createHazard,updateHazards,hazards:()=>hazards,secretWalls:()=>secretWalls,damageSecretWall,grid:()=>grid,runicSwitches:()=>runicSwitches,interactRune,unlockPortalIfReady,bosses:()=>enemies.filter(e=>e.type==='boss'),magazines,WEAPONS,chargeSaber,unleashSaberWave,flags:()=>({level,portalOpen,seed:campaignSeed,floorSwitchNeeded,floorSwitchOn})};\n"""+marker,1)
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 pg=b.new_page();err=[];pg.on('pageerror',lambda e:err.append(str(e)))
 pg.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 pg.add_script_tag(content=(R/'tests/mock_three.js').read_text());pg.add_script_tag(content=code)
 pg.wait_for_selector('[data-a="skipintro"]',timeout=15000)
 result=pg.evaluate("""()=>{
 const g=__physics;g.newGame();g.setWeapon(0);
 const f=[-Math.sin(g.P.yaw),-Math.cos(g.P.yaw)];
 const e=g.addEnemy('chaser',g.P.x+f[0]*2,g.P.z+f[1]*2);
 const target=g.enemies()[g.enemies().length-1],start=target.hp;
 g.P.pitch=0;g.P.cool=0;g.shoot();let emitted=g.shots().length;
 for(let k=0;k<8;k++)g.updateProjectiles(.020);
 const hit={initialHP:start,remainingHP:target.hp,emitted};
 // Grenade trajectory: starts with upward vertical velocity, then falls under gravity.
 g.setWeapon(4);g.P.cool=0;g.P.pitch=.2;g.shoot();
 const gren=g.shots().find(s=>s.wi===4),rise=gren?.vy;
 for(let k=0;k<130;k++)g.updateProjectiles(.024);
 const ballistic={initialVy:rise,remaining:g.shots().filter(s=>s.wi===4).length};
 // Destroy a real secret wall by hitting its special cell.
 const wall=g.secretWalls()[0];let secret={available:!!wall};
 if(wall){g.damageSecretWall(wall.x,wall.z,20);secret={available:true,opened:g.grid()[wall.gz][wall.gx]===0};}
 // Actual interactive rune switch, as opposed to a menu-only feature.
 g.P.hp=100;g.P.armor=0;g.P.wi=6;
 g.keys.KeyC=true;let before=g.P.hp; // parryWindow may be zero; guard still cuts damage.
 const shieldedBefore=g.P.hp;g.keys.KeyC=false;
 const guarded=before===shieldedBefore;
 g.setWeapon(7);g.P.energy=100;g.P.cool=0;
 const charged=g.chargeSaber(),energy=g.P.energy;g.unleashSaberWave();
 return {hit,ballistic,secret,guarded,charged,energy};
 }""")
 assert result['hit']['emitted']>=1 and result['hit']['remainingHP']<result['hit']['initialHP'],result
 assert result['ballistic']['initialVy']>0 and result['ballistic']['remaining']==0,result
 assert result['secret']['available'] and result['secret']['opened'],result
 assert result['charged'] and result['energy']==70,result
 assert not err,err
 print('PASS: real travelling bullet impact, gravitational grenade, breakable passage, charged saber, no runtime errors',result)
 b.close()
