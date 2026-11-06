"""Targeted Light Saber v5.0.0 first-person rig, ignition and combat tests.
Uses a simulated Three.js renderer; not a photorealism/WebGL image test.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'src/game.js').read_text(encoding='utf-8')
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in js
js=js.replace(marker,r'''
window.__saberQA={
 model:()=>{
   const U=gunModels[7].userData,hand=U.handRigs[0];
   return {slots:gunModels.length,hands:gunModels.map(g=>g.userData.handRigs.length),
     singleHand:U.handRigs.length===1,grip:hand.userData.saberGrip,
     locked:hand.userData.handleLocked,fingers:hand.userData.fingers.length,
     thumb:!!hand.userData.thumb,hilt:!!U.hilt,
     lengths:U.bladeLengths,base:U.bladeBaseZ,blades:[!!U.bladeAura,!!U.bladeCore,!!U.bladeWhite]};
 },
 ignition:()=>{
   state='playing';paused=false;setWeapon(7);P.cool=0;P.inv=99;
   const U=gunModels[7].userData;
   const initial={p:U.bladeProgress,axial:U.bladeCore.scale.y,radial:U.bladeCore.scale.z};
   update(.10);const middle={p:U.bladeProgress,axial:U.bladeCore.scale.y,
     center:U.bladeCore.position.z,radial:U.bladeCore.scale.z};
   update(.40);const later={p:U.bladeProgress,axial:U.bladeCore.scale.y,
     center:U.bladeCore.position.z,radial:U.bladeCore.scale.z};
   update(.65);const full=U.bladeProgress;
   setWeapon(0);const off=U.bladeProgress;
   return {initial,middle,later,full,off};
 },
 stance:()=>{
   state='playing';paused=false;P.cool=0;P.inv=99;setWeapon(7);
   render();const model=gunModels[7],hand=model.userData.handRigs[0];
   const idle=[gun.position.x,gun.position.y,gun.position.z,model.position.x,model.position.y,model.position.z];
   walkT+=.5;bobAmt=1;keys.KeyW=true;render();
   const walk=[gun.position.x,gun.position.y,gun.position.z];keys.KeyW=false;
   keys.ShiftLeft=true;walkT+=.4;render();
   const run=[gun.position.x,gun.position.y,gun.position.z];keys.ShiftLeft=false;
   keys.KeyC=true;render();const guard=[model.position.x,model.position.y,model.position.z];
   keys.KeyC=false;render();
   return {idle,walk,run,guard,held:hand.position.distanceTo(hand.userData.restPosition)<1e-6};
 },
 attack:(style)=>{
   state='playing';paused=false;P.inv=99;P.cool=0;P.energy=100;P.stamina=100;keys.KeyC=false;
   setWeapon(7);update(.95);P.cool=0;
   enemies.length=0;
   addEnemy('brute',P.x-Math.sin(P.yaw)*1.85,P.z-Math.cos(P.yaw)*1.85);
   const e=enemies[0],before=e.hp,initialEnergy=P.energy,initialStamina=P.stamina;
   meleeAttack(WEAPONS[7],style);
   const actual=pendingMelee?.style,immediate=e.hp,spentStamina=P.stamina,spentEnergy=P.energy;
   render();const first=[gun.position.x,gun.position.y,gun.position.z];
   update(bladeDuration*.48);render();const middle=[gun.position.x,gun.position.y,gun.position.z];
   const during=e.hp;
   update(bladeDuration*.53);render();
   const hand=gunModels[7].userData.handRigs[0];
   return {style,actual,before,immediate,during,after:e.hp,
     held:hand.position.distanceTo(hand.userData.restPosition)<1e-6,
     first,middle,energyBefore:initialEnergy,energyAfter:P.energy,
     staminaBefore:initialStamina,staminaSpent:spentStamina,staminaAfter:P.stamina,energySpent:spentEnergy};
 },
 guard:()=>{
   state='playing';paused=false;setWeapon(7);P.cool=0;P.stamina=100;
   keys.KeyC=true;meleeAttack(WEAPONS[7]);
   const prevented=!pendingMelee;keys.KeyC=false;return prevented;
 },
 reset:()=>{state='playing';paused=false;setWeapon(7);P.cool=0;P.energy=100;P.stamina=100;
   gunModels[7].userData.bladeProgress=1;pendingMelee=null;bladeSwing=0;},
 style:()=>pendingMelee?.style||null
};
''' + marker,1)
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  page=browser.new_page(viewport={'width':1024,'height':800})
  errors=[];console=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:console.append(m.text) if m.type=='error' else None)
  page.set_content('<html><body>'+ (ROOT/'src/game.html').read_text(encoding='utf-8')+'</body></html>')
  page.add_script_tag(content=(ROOT/'tests/mock_three.js').read_text(encoding='utf-8'))
  page.add_script_tag(content=js)
  page.wait_for_selector('[data-a="skipintro"]',timeout=15000)
  model=page.evaluate('window.__saberQA.model()')
  assert model['slots']==8 and model['singleHand'] and model['grip'] and model['locked'],model
  assert model['fingers']==4 and model['thumb'] and model['hilt'] and all(model['blades']),model
  assert model['hands']==[2,2,2,2,2,2,1,1],model
  assert model['lengths']==[1,.984,.973],model
  print('PASS saber grip, proportions, and all eight weapon slots:',model)
  ignition=page.evaluate('window.__saberQA.ignition()')
  assert 0==ignition['initial']['p']<ignition['middle']['p']<ignition['later']['p']<ignition['full']<1.001,ignition
  assert ignition['initial']['axial']<ignition['middle']['axial']<ignition['later']['axial'],ignition
  assert abs(ignition['middle']['radial']-1)<1e-6 and abs(ignition['later']['radial']-1)<1e-6,ignition
  assert ignition['later']['center']<ignition['middle']['center'] and ignition['off']==0,ignition
  print('PASS physically axial progressive saber ignition:',ignition)
  stance=page.evaluate('window.__saberQA.stance()')
  assert stance['held'] and stance['idle'][:3]!=stance['walk'] and stance['walk']!=stance['run'],stance
  assert stance['guard']!=stance['idle'][3:],stance
  print('PASS idle, walk, sprint, guard with attached hand:',stance)
  for style in ('horizontal','diagonal','heavy','thrust'):
    result=page.evaluate(f'window.__saberQA.attack("{style}")')
    assert result['actual']==style and result['immediate']==result['before'],result
    assert result['held'] and result['first']!=result['middle'],result
    assert result['during']<result['before'] and result['after']<=result['during'],result
    if style=='heavy':assert result['energySpent']<result['energyBefore'],result
    if style=='thrust':assert result['staminaSpent']<result['staminaBefore'],result
    print('PASS Light Saber attack:',style,'damage=',round(result['before']-result['after'],2),'attached=',result['held'])
  assert page.evaluate('window.__saberQA.guard()')
  page.evaluate('window.__saberQA.reset()')
  game=page.locator('#dd3d-root')
  game.press('KeyG');assert page.evaluate('window.__saberQA.style()')=='heavy'
  page.evaluate('window.__saberQA.reset()')
  game.press('KeyT');assert page.evaluate('window.__saberQA.style()')=='thrust'
  assert not errors,errors
  print('PASS guard prevents attacks, G/T controls, no JavaScript page errors')
  print('console errors:',console[:3])
  browser.close()
