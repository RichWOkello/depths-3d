"""Targeted v5.0.0 katana correction test, using mocked Three.js.
Verifies model structure, one-hand grip, attack timing, keyboard inputs,
blocking and untouched weapon slots. No claim of photorealistic WebGL verification.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'src/game.js').read_text(encoding='utf-8')
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in js
js=js.replace(marker,r'''
window.__katanaQA={
 describe:()=>{
  const model=gunModels[6],hand=model.userData.handRigs[0];
  return {slots:gunModels.length,hands:gunModels.map(g=>g.userData.handRigs?.length||0),
    grip:!!hand.userData.katanaGrip, fingers:hand.userData.fingers.length,
    thumb:!!hand.userData.thumb,blade:!!model.userData.blade,
    vertices:model.userData.blade.geometry.attributes.position.array.length/3,
    tip:model.userData.bladeTip.z,restGrip:[hand.position.x,hand.position.y,hand.position.z]};
 },
 stance:()=>{
  state='playing';paused=false;setWeapon(6);P.cool=0;
  render();const model=gunModels[6],hand=model.userData.handRigs[0];
  const idle=[gun.position.x,gun.position.y,gun.position.z,model.position.x,model.position.y,model.position.z];
  keys.KeyW=true;walkT+=.55;bobAmt=1;render();const walking=[gun.position.x,gun.position.y,gun.position.z];keys.KeyW=false;
  keys.KeyC=true;render();const guard=[model.position.x,model.position.y,model.position.z];keys.KeyC=false;
  render();return {idle,walking,guard,handFixed:hand.position.distanceTo(hand.userData.restPosition)<1e-6};
 },
 attack:(style)=>{
  state='playing';paused=false;setWeapon(6);P.cool=0;P.stamina=100;
  keys.KeyC=false;enemies.length=0;
  addEnemy('brute',P.x-Math.sin(P.yaw)*1.90,P.z-Math.cos(P.yaw)*1.90);
  const e=enemies[0],before=e.hp;
  meleeAttack(WEAPONS[6],style);
  const actual=pendingMelee?.style,immediate=e.hp;
  render();const start=[gun.position.x,gun.position.y,gun.position.z];
  update(bladeDuration*.47);render();const middle=[gun.position.x,gun.position.y,gun.position.z];
  const changed=e.hp;
  update(bladeDuration*.55);render();const end=[gun.position.x,gun.position.y,gun.position.z];
  const hand=gunModels[6].userData.handRigs[0];
  return {actual,before,immediate,changed,after:e.hp,held:hand.position.distanceTo(hand.userData.restPosition)<1e-5,
    start,middle,end,remaining:enemies.length};
 },
 style:()=>pendingMelee?.style||null,
 resetCooldown:()=>{P.cool=0;P.stamina=100;pendingMelee=null;bladeSwing=0;},
 block:()=>{
  state='playing';paused=false;setWeapon(6);P.cool=0;P.stamina=100;keys.KeyC=true;
  meleeAttack(WEAPONS[6],'light');
  const prevented=!pendingMelee;
  keys.KeyC=false;return {prevented};
 }
};
'''+marker,1)
with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
  page=browser.new_page(viewport={'width':1024,'height':800})
  errors=[];logs=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:logs.append(m.text) if m.type=='error' else None)
  page.set_content('<html><body>'+ (ROOT/'src/game.html').read_text(encoding='utf-8')+'</body></html>')
  page.add_script_tag(content=(ROOT/'tests/mock_three.js').read_text(encoding='utf-8'))
  page.add_script_tag(content=js)
  page.wait_for_selector('[data-a="skipintro"]',timeout=15000)
  model=page.evaluate('window.__katanaQA.describe()')
  assert model['slots']==8 and model['hands'][6]==1 and model['hands'][7]==1,model
  assert model['grip'] and model['fingers']==4 and model['thumb'],model
  assert model['vertices']>=140 and model['blade'] and -.95<model['tip']<-.80,model
  stance=page.evaluate('window.__katanaQA.stance()')
  assert stance['handFixed'] and stance['idle'][:3]!=stance['walking'],stance
  assert stance['guard']!=stance['idle'][3:],stance
  print('PASS model geometry, eight weapons, single wrapped-grip hand:',model)
  print('PASS idle/walk/guard transitions:',stance)
  for style in ('horizontal','diagonal','heavy','thrust'):
    result=page.evaluate(f'window.__katanaQA.attack("{style}")')
    assert result['actual']==style and result['immediate']==result['before'],(style,result)
    assert result['held'] and result['start']!=result['middle'],(style,result)
    assert result['changed']<result['before'],(style,result)
    assert result['remaining']>=0,(style,result)
    print('PASS katana attack:',style, {k:v for k,v in result.items() if k not in ('start','middle','end')})
  block=page.evaluate('window.__katanaQA.block()')
  assert block['prevented'],block
  game=page.locator('#dd3d-root')
  page.evaluate('window.__katanaQA.resetCooldown()')
  game.press('KeyG')
  assert page.evaluate('window.__katanaQA.style()')=='heavy','G heavy attack key did not trigger'
  page.evaluate('window.__katanaQA.resetCooldown()')
  game.press('KeyT')
  assert page.evaluate('window.__katanaQA.style()')=='thrust','T thrust key did not trigger'
  assert not errors, errors
  print('PASS guard blocks new attacks; G and T keyboard bindings; no JS page errors')
  print('CONSOLE:',logs[:3])
  browser.close()
