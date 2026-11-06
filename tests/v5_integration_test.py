"""Simulated-renderer integration tests for new v5 mechanics; not a real WebGL benchmark."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'src/game.js').read_text()
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in src
src=src.replace(marker,"""window.__v5={P,WEAPONS,magazines,MASTERY,WEAPON_LEVELS,saveCampaign,continueCampaign,buyUpgrade,drinkPotion,newGame,addEnemy,buildLevel,shoot,makeShot,updateProjectiles,startReload,finishReload,updateHazards,unlockPortalIfReady,createHazard,emitNoise,savedRun,tickBoss,bossWarning,updateBossTelegraphs,flags:()=>({level,floorKeyNeeded,floorKeyCollected,portalOpen,shots:shots.length,hazards:hazards.length,boss:!!currentBoss,seed:campaignSeed}),enemies:()=>enemies,pickups:()=>pickups,setLevel:n=>{level=n},killFloor:()=>{killsThisLevel=totalEnemies;},markKey:()=>{floorKeyCollected=true;P.keys=1;},setState:n=>{state=n},setWeapon};
"""+marker,1)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 page=browser.new_page(viewport={'width':1024,'height':800})
 errors=[];logs=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.on('console',lambda m: logs.append(m.text) if m.type=='error' else None)
 # localStorage replaced by a durable in-page fake to enable isolated persistence testing on about:blank.
 page.set_content('<html><body>'+ (ROOT/'src/game.html').read_text()+'</body></html>')
 page.evaluate("""() => { const data={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{setItem(k,v){data[k]=String(v)},getItem(k){return data[k]??null},removeItem(k){delete data[k]},clear(){for(const k in data)delete data[k]}}}); }""")
 page.add_script_tag(content=(ROOT/'tests/mock_three.js').read_text())
 page.add_script_tag(content=src)
 page.wait_for_selector('[data-a="skipintro"]',timeout=12000)
 tests={}
 tests['magazine_reload']=page.evaluate("""() => {let g=__v5;g.newGame();g.setWeapon(0);const original=g.magazines[0];g.shoot();g.P.cool=0;g.startReload();g.finishReload();return {original,after:g.magazines[0],reserve:g.P.ammo};}""")
 tests['projectile']=page.evaluate("""() => {let g=__v5;g.setWeapon(4);g.P.cool=0;const a=g.P.ammo;g.shoot();let before=g.flags().shots;g.updateProjectiles(.06);let after=g.flags().shots;return {before,after,reserve:g.P.ammo,a,mag:g.magazines[4],exploded:!after};}""")
 tests['ai']=page.evaluate("""() => {let g=__v5,types=['stalker','armored','crawler','necromancer'];for(const t of types)g.addEnemy(t,g.P.x+1,g.P.z+1);g.emitNoise(g.P.x,g.P.z,30);return types.map(t=>{const e=g.enemies().find(e=>e.type===t);return {type:t,alert:e.alert,limbs:e.mesh.userData.legs?.length||0};});}""")
 tests['gated_floor']=page.evaluate("""() => {let g=__v5;g.setLevel(3);g.buildLevel();let key=g.pickups().some(k=>k.type==='key');g.killFloor();g.unlockPortalIfReady();let sealed=!g.flags().portalOpen;g.markKey();g.unlockPortalIfReady();return {key,sealed,opened:g.flags().portalOpen,seed:g.flags().seed};}""")
 tests['shop_save']=page.evaluate("""() => {let g=__v5;g.P.coins=350;g.setWeapon(0);let bought=g.buyUpgrade('weapon');g.buyUpgrade('health');let lv=g.WEAPON_LEVELS[0],maxhp=g.P.maxhp;g.P.potions=2;g.P.hp=10;g.drinkPotion();let afterMed=g.P.hp;let saved=g.saveCampaign();g.P.coins=0;g.WEAPON_LEVELS[0]=0;let restored=g.continueCampaign();return {bought,lv,maxhp,afterMed,saved,restored,weapon:g.WEAPON_LEVELS[0],coins:g.P.coins};}""")
 tests['boss']=page.evaluate("""() => {let g=__v5;g.setLevel(5);g.buildLevel();let b=g.enemies().find(e=>e.type==='boss');if(!b)return {found:false};b.hp=b.maxhp*.2;g.tickBoss(b,.2,5,true);g.bossWarning(b,'blast');g.updateBossTelegraphs(.8);return {found:true,name:b.bossName,phase:b.bossPhase,remaining:b.hp,energy:g.P.energy};}""")
 assert tests['magazine_reload']['after']>=tests['magazine_reload']['original']
 assert tests['projectile']['before']>=1
 assert all(t['alert'] for t in tests['ai'])
 assert tests['gated_floor']['key'] and tests['gated_floor']['sealed'] and tests['gated_floor']['opened']
 assert tests['shop_save']['bought'] and tests['shop_save']['restored'] and tests['shop_save']['weapon']==tests['shop_save']['lv']
 assert tests['boss']['found'] and tests['boss']['phase']==3
 assert not errors,(errors,logs)
 print('PASS v5 integration',tests)
 print('browser errors:',errors,'console:',logs[:5])
 browser.close()
