"""UI save/continue/destructive-action behavior, with a same-page persistent storage stub."""
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':900,'height':650});errors=[]
 page.on('pageerror',lambda e: errors.append(str(e)))
 page.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 page.evaluate("""()=>{const d={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return d[k]??null},setItem(k,v){d[k]=String(v)},removeItem(k){delete d[k]},clear(){for(const k in d)delete d[k]}}});}""")
 page.add_script_tag(content=(R/'tests/mock_three.js').read_text())
 page.add_script_tag(content=(R/'src/game.js').read_text())
 page.locator('[data-a="skipintro"]').click()
 page.locator('[data-a="view:settings"]').click()
 page.locator('[data-a="back:title"]').click()
 page.locator('[data-a="begin"]').click()
 page.locator('[data-a="diffflow:Normal"]').click()
 page.locator('[data-a="startnew"]').click()
 assert page.evaluate("localStorage.getItem('depths3d_v5_save')!==null")
 root=page.locator('#dd3d-root');root.focus();root.press('KeyP')
 page.locator('[data-a="menu"]').click()
 assert page.locator('[data-a="continue"]').count()==1
 page.locator('[data-a="begin"]').click();page.locator('[data-a="diffflow:Normal"]').click()
 page.locator('[data-a="startnew"]').click()
 assert page.locator('[data-a="play"]').count()==1
 page.locator('[data-a="back:main"]').click()
 assert page.locator('[data-a="continue"]').count()==1
 page.locator('[data-a="view:settings"]').click()
 page.locator('[data-a="settingspage:save"]').click()
 page.locator('[data-a="deleteprompt"]').click()
 assert page.locator('[data-a="deletesave"]').count()==1
 page.locator('[data-a="deletesave"]').click()
 assert page.evaluate("localStorage.getItem('depths3d_v5_save')===null")
 assert page.locator('[data-a="deleteprompt"]').count()==0
 assert not errors, errors
 print('PASS: title settings back, saved expedition, new-run confirmation, cancellation, delete confirmation and actual save removal')
 b.close()
