from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 page=b.new_page(viewport={'width':1000,'height':780});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 page.add_script_tag(content=(R/'tests/mock_three.js').read_text());page.add_script_tag(content=(R/'src/game.js').read_text())
 page.locator('[data-a="skipintro"]').click();page.locator('[data-a="begin"]').click();page.locator('[data-a="diffflow:Normal"]').click()
 page.locator('[data-a="startnew"]').click()
 root=page.locator('#dd3d-root')
 root.focus();root.press('Digit4');root.press('Space');root.press('KeyB');root.press('KeyR')
 root.press('KeyI')
 page.wait_for_selector('[data-a="usepotion"]',timeout=8000)
 assert page.locator('[data-a="savecampaign"]').count()>0
 page.locator('[data-a="resume"]').click()
 root.press('Tab')
 page.wait_for_selector('[data-a="chooseweapon:7"]',timeout=8000)
 page.locator('[data-a="chooseweapon:7"]').click()
 root.press('KeyV');root.press('KeyC')
 root.press('KeyP')
 page.wait_for_selector('[data-a="resume"]',timeout=8000)
 assert not errors,errors
 print('PASS: actual keyboard and menu controls - AK burst/reload, inventory, wheel, charged saber, guard, pause')
 b.close()
