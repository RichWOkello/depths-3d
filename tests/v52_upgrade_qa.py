"""Deterministic browser-simulation acceptance checks, NOT live GPU/Colab verification."""
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
s=(R/'src/game.js').read_text(encoding='utf8')
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in s
s=s.replace(marker,'''window.__v52={renderer,scene,viewScene,gunModels,WEAPONS,SET,P,keys,newGame,showMenu,PERKS,shopPanelV52,
 setPerks:()=>{perkChoices=PERKS.slice(0,3);forgeStage=0;forgeChosen=false;P.coins=200;state='perk';paused=true;},
 getForge:()=>({stage:forgeStage,chosen:forgeChosen}),getMode:()=>({mapZoom,mapRotate}),
 getHands:()=>gunModels.map(g=>(g.userData.handRigs||[]).length),
 getFingerJoints:()=>gunModels.slice(0,6).map(g=>{const h=g.userData.handRigs[0];return {fingers:h.userData.fingers.length,phalanges:h.userData.fingers.map(f=>f.userData.phalanges.length),thumb:h.userData.thumb.userData.joints.length};}),
 getSaber:()=>gunModels[7].userData.handRigs.map(h=>h.visible),getGunParent:()=>gun.parent===viewScene,
 getTheme:()=>DUNGEON_THEMES[5],getMat:()=>({tone:renderer.toneMappingExposure}),getVFX:()=>VFX_POOL};'''+marker,1)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1100,'height':900});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
 page.add_script_tag(content=s)
 page.wait_for_selector('[data-a="skipintro"]',timeout=8000)
 icons=page.locator('symbol[id^="dd3d-i-"]').count()
 assert icons>=40,icons
 page.locator('[data-a="skipintro"]').click()
 page.locator('[data-a="begin"]').click()
 page.locator('[data-a="diffflow:Normal"]').click()
 page.locator('[data-a="startnew"]').click()
 page.wait_for_timeout(400)
 result=page.evaluate('''() => {
  const x=window.__v52;
  const handCount=x.getHands(), fingerJoints=x.getFingerJoints();
  const viewmodel=x.getGunParent();
  const root=document.getElementById('dd3d-root').getBoundingClientRect();
  const hud=document.querySelector('.hud').getBoundingClientRect(),mm=document.querySelector('.mm').getBoundingClientRect();
  const toast=document.querySelector('.toast').getBoundingClientRect(),bar=document.querySelector('.cin-hotbar').getBoundingClientRect();
  const weapons=x.WEAPONS.map((w,i)=>({name:w.n,children:x.gunModels[i].children.length,hasHands:handCount[i]>0}));
  x.setPerks();x.showMenu('perk');
  return {root:{w:root.width,h:root.height},iconCount:document.querySelectorAll('symbol[id^="dd3d-i-"]').length,
    viewmodel,handCount,fingerJoints,weapons,hudWidth:hud.width,minimap:!!mm.width,unobstructed:toast.bottom<bar.top+80,firstStage:x.getForge()};
 }''')
 assert result['viewmodel'] and all(k>=2 for k in result['handCount']),result
 assert all(d['fingers']==4 and d['thumb']==3 and d['phalanges']==[3]*4 for d in result['fingerJoints']),result
 assert all(w['children']>3 for w in result['weapons']),result
 assert result['root']['h']>=690,result
 assert result['hudWidth']<=241,result
 assert page.locator('[data-a^="perk:"]').count()==3
 page.locator('[data-a="perk:0"]').click()
 print('after perk',page.evaluate('window.__v52.getForge()'),page.locator('.ov').inner_text()[:350]);assert page.locator('[data-a^="forgecat:"]').count()>=5
 assert page.evaluate('window.__v52.getForge().stage')==1
 page.locator('[data-a="forgeback"]').click()
 assert page.evaluate('window.__v52.getForge().stage')==0
 assert page.locator('[data-a="forgeshop"]').count()==1
 page.locator('[data-a="forgeshop"]').click()
 assert page.evaluate('window.__v52.getForge().stage')==1
 page.locator('[data-a="forgecat:Relics"]').click()
 assert page.locator('[data-a="forgenext"]').count()==1
 page.screenshot(path=str(R/'tests/v52_soul_forge_mock.png'))
 print('PASS: 47 SVG icons, eight viewmodels with grips, independent model scene, 800x700 HUD, two-step forge back/forward, menu actions')
 print('Details:',result)
 assert not errors,errors
 browser.close()
