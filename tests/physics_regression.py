from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'src/game.js').read_text('utf-8')
marker='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert marker in js
js=js.replace(marker,r'''
window.__physicsTest={
  hands:()=>gunModels.map(g=>({count:(g.userData.handRigs||[]).length,
    fingers:(g.userData.handRigs||[]).map(h=>h.userData.fingers.length),
    thumbs:(g.userData.handRigs||[]).every(h=>!!h.userData.thumb)})),
  floors:()=>Array.from({length:6},(_,i)=>{level=i+1;buildLevel();return {name:currentTheme.name,objects:levelGroup.children.length};}),
  saber:()=>{setWeapon(7);state='playing';paused=false;update(.06);
    const before=gunModels[7].userData.bladeProgress;
    update(.21);return {before,after:gunModels[7].userData.bladeProgress};},
  hit:()=>{
    level=1;buildLevel();state='playing';paused=false;P.cool=0;
    enemies.length=0;setWeapon(6);P.cool=0;
    addEnemy('chaser',P.x-Math.sin(P.yaw)*2.0,P.z-Math.cos(P.yaw)*2.0);
    const target=enemies[0],before=target.hp;
    shoot();const immediate=target.hp;
    update(.22);update(.12);
    return {before,immediate,remaining:enemies.length,severed:fx.filter(x=>x.severed).length,
      wound:target.mesh.userData.wounds?.length||0};
  },
  knockback:()=>{
    level=2;buildLevel();state='playing';paused=false;P.cool=0;
    enemies.length=0;setWeapon(6);P.cool=0;
    addEnemy('brute',P.x-Math.sin(P.yaw)*2.05,P.z-Math.cos(P.yaw)*2.05);
    const target=enemies[0],initial=target.hp;
    shoot();update(.19);update(.12);
    return {initial,after:target.hp,stagger:target.stagger||0,
      impulse:Math.hypot(target.knockX||0,target.knockZ||0)};
  }
};
''' + marker,1)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    page=browser.new_page(viewport={'width':1000,'height':760})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content('<html><body>'+(ROOT/'src/game.html').read_text('utf-8')+'</body></html>')
    page.add_script_tag(content=(ROOT/'tests/mock_three.js').read_text('utf-8'))
    page.add_script_tag(content=js)
    page.wait_for_selector('[data-a="skipintro"]')
    hands=page.evaluate('window.__physicsTest.hands()')
    assert all(h['count']>=1 and h['thumbs'] and len(h['fingers'])==h['count'] and all(f==4 for f in h['fingers']) for h in hands),hands
    assert hands[6]['count']==1 and hands[7]['count']==1,hands
    floors=page.evaluate('window.__physicsTest.floors()')
    assert len(set(f['name'] for f in floors))==6,floors
    assert min(f['objects'] for f in floors)>=60,floors
    saber=page.evaluate('window.__physicsTest.saber()')
    assert 0<saber['before']<saber['after']<1.01,saber
    hit=page.evaluate('window.__physicsTest.hit()')
    assert hit['before']==hit['immediate'] and hit['remaining']==0,hit
    assert hit['severed']>=1,hit
    knock=page.evaluate('window.__physicsTest.knockback()')
    assert knock['after']<knock['initial'] and knock['impulse']>=0,knock
    assert not errors,errors
    print('PASS hands:',hands)
    print('PASS cathedral floors:',floors)
    print('PASS saber ignition:',saber)
    print('PASS melee finishing strike:',hit)
    print('PASS stagger/knockback:',knock)
    print('PASS JavaScript errors:',errors)
    browser.close()
