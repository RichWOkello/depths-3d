from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent.parent
source=(R/'src/game.js').read_text(encoding='utf8')
needle='// Initial dungeon renders behind overlays, which also own their illustrated art.'
assert needle in source
source=source.replace(needle,"""
window.__depthsTest={
 theme:function(n){level=n;buildLevel();return {name:currentTheme.name,props:levelGroup.children.length,monsters:enemies.length};},
 attack:function(wi){state='playing';paused=false;P.wi=wi;gunModels.forEach((g,i)=>g.visible=i===wi);
   const enemy=enemies[0];enemies.length=0;
   addEnemy('chaser',P.x-Math.sin(P.yaw)*2.2,P.z-Math.cos(P.yaw)*2.2);
   const target=enemies[0];let hp=target.hp;
   shoot();return {hpBefore:hp,hpAtKey:target.hp,now:bladeElapsed,weapon:P.wi};
 },
 after:function(dt){update(dt);return {bladeElapsed:bladeElapsed,phase:bladeSwing,enemies:enemies.length};},
};
""" + needle,1)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 page=b.new_page(viewport={'width':1024,'height':800})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
 page.add_script_tag(content=source)
 page.wait_for_selector('[data-a="skipintro"]')
 themes=page.evaluate('''() => Array.from({length:6},(_,i)=>window.__depthsTest.theme(i+1))''')
 assert len({x['name'] for x in themes})==6,themes
 assert all(x['props']>30 and x['monsters']>0 for x in themes),themes
 print('THEMES:',themes)
 start=page.evaluate('''() => window.__depthsTest.attack(6)''')
 assert start['hpAtKey']==start['hpBefore'], 'Melee damage must not apply immediately at key press'
 end=page.evaluate('''() => window.__depthsTest.after(.23)''')
 assert end['bladeElapsed']>.20,end
 assert end['enemies']==0, f'Melee contact should eliminate nearby weak test enemy: {end}'
 page.wait_for_timeout(80)
 assert not errors, errors
 print('MELEE: delayed collision phase OK, all 6 dungeon types OK, no JS exceptions')
 b.close()
