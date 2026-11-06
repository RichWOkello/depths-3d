from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 page=b.new_page(viewport={'width':1024,'height':800})
 errors=[];logs=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:logs.append(m.text) if m.type=='error' else None)
 page.set_content('<html><head></head><body>'+ (R/'src/game.html').read_text() + '</body></html>')
 page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
 page.add_script_tag(content=(R/'src/game.js').read_text())
 page.wait_for_selector('[data-a="skipintro"]',timeout=15000)
 page.screenshot(path=str(R/'tests/intro.png'))
 page.locator('[data-a="skipintro"]').click()
 page.wait_for_selector('[data-a="begin"]')
 page.screenshot(path=str(R/'tests/title.png'))
 page.locator('[data-a="begin"]').click()
 page.wait_for_selector('[data-a="diffflow:Normal"]')
 page.screenshot(path=str(R/'tests/difficulty.png'))
 page.locator('[data-a="diffflow:Normal"]').click()
 page.locator('[data-a="view:loadout"]').click()
 page.wait_for_selector('[data-a="wpn:7"]')
 page.screenshot(path=str(R/'tests/menu.png'))
 assert page.locator('[data-a="wpn:7"]').count()==1
 page.locator('[data-a="wpn:7"]').click()
 page.locator('[data-a="back:main"]').click()
 page.locator('[data-a="startnew"]').click()
 page.wait_for_timeout(350)
 assert page.locator('.ov').evaluate('e=>e.style.display')=='none'
 game=page.locator('#dd3d-root')
 game.press('Digit7')
 game.press('Space')
 page.wait_for_timeout(700)
 game.press('Digit8')
 game.press('Space')
 page.wait_for_timeout(700)
 page.screenshot(path=str(R/'tests/gameplay_mock.png'))
 game.press('KeyP')
 page.wait_for_selector('[data-a="resume"]')
 assert not errors,errors
 print('PASS: intro -> title -> difficulty -> menu -> weapon 7 and 8 -> combat -> pause')
 print('console errors:',logs[:8])
 b.close()
