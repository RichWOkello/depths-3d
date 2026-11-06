from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    page=browser.new_page(viewport={'width':900,'height':650})
    errors=[];logs=[]
    page.on('pageerror',lambda exc:errors.append(str(exc)))
    page.on('console',lambda msg:logs.append(msg.text) if msg.type=='error' else None)
    page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
    page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
    page.add_script_tag(content=(R/'src/game.js').read_text())
    page.wait_for_selector('[data-a="skipintro"]',timeout=15000)
    page.locator('[data-a="skipintro"]').click()
    page.wait_for_selector('[data-a="begin"]')
    page.wait_for_timeout(850)
    page.screenshot(path=str(R/'tests/v51_title.png'))
    assert page.locator('.launch-logo').count()==1
    page.locator('[data-a="begin"]').click()
    page.wait_for_selector('[data-a="diffflow:Normal"]')
    page.wait_for_timeout(850)
    page.screenshot(path=str(R/'tests/v51_difficulty.png'))
    page.locator('[data-a="diffflow:Normal"]').click()
    page.wait_for_selector('[data-a="startnew"]')
    page.screenshot(path=str(R/'tests/v51_main.png'))
    assert page.locator('[data-a="wpn:7"]').count()==0  # no eight-weapon wall on main menu
    assert page.locator('[data-a="view:settings"]').count()==1
    page.locator('[data-a="view:loadout"]').click()
    page.wait_for_selector('[data-a="wpn:7"]')
    page.screenshot(path=str(R/'tests/v51_loadout.png'))
    page.locator('[data-a="wpn:7"]').click()
    page.locator('[data-a="back:main"]').click()
    page.locator('[data-a="view:settings"]').click()
    page.wait_for_selector('[data-a="settingspage:audio"]')
    page.screenshot(path=str(R/'tests/v51_settings.png'))
    page.locator('[data-a="settingspage:audio"]').click()
    page.wait_for_selector('[data-a="set:music:-1"]')
    page.locator('[data-a="set:music:-1"]').click()
    page.locator('[data-a="back:settings"]').click()
    page.locator('[data-a="settingspage:visual"]').click()
    page.locator('[data-a="set:quality:1"]').click()
    page.locator('[data-a="back:settings"]').click()
    page.locator('[data-a="settingspage:controls"]').click()
    assert page.locator('.ux-control-row').count()>=8
    page.locator('[data-a="back:settings"]').click()
    page.locator('[data-a="settingspage:game"]').click()
    page.locator('[data-a="mode:Daily"]').click()
    assert page.locator('[data-a="mode:Daily"]').get_attribute('class').find('selected')>=0
    page.locator('[data-a="back:settings"]').click()
    page.locator('[data-a="back:main"]').click()
    page.wait_for_selector('[data-a="startnew"]')
    page.locator('[data-a="startnew"]').click()
    # Existing saved games get a confirmation before replacing.
    if page.locator('[data-a="play"]').count():page.locator('[data-a="play"]').click()
    page.wait_for_function("document.querySelector('.ov').style.display==='none'")
    root=page.locator('#dd3d-root')
    root.focus();root.press('Digit7');root.press('Space');root.press('Digit8');root.press('Space')
    root.press('KeyP');page.wait_for_selector('[data-a="resume"]')
    page.locator('[data-a="view:settings"]').click()
    page.locator('[data-a="settingspage:save"]').click()
    if page.locator('[data-a="deleteprompt"]').count():
        page.locator('[data-a="deleteprompt"]').click()
        assert page.locator('[data-a="deletesave"]').count()==1
        page.locator('[data-a="back:settings-save"]').click()
    else:
        assert 'No saved campaign' in page.locator('.ux-card').inner_text()
    page.locator('[data-a="back:settings"]').click()
    page.locator('[data-a="back:pause"]').click()
    page.locator('[data-a="resume"]').click()
    assert not errors,(errors,logs[:10])
    print('PASS: title, difficulty, clean main, loadout, audio, visual, controls, game settings, save confirmation, combat and pause')
    print('console errors',logs[:8])
    browser.close()
