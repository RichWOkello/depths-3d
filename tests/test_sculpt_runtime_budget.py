from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page()
 page.goto('about:blank')
 page.add_script_tag(path=str(ROOT/'tests/three_bestiary_mock.js'))
 page.add_script_tag(path=str(ROOT/'src/bestiary_pass.js'))
 result=page.evaluate('''() => {
  const B=window.DEPTHS_BESTIARY;
  const types=['brute','crawler','imp','wraith','necromancer','gargoyle'];
  const entities=[];
  const a=performance.now();
  for(let i=0;i<40;i++){
    const type=types[i%types.length],mesh=B.build(type);
    entities.push({mesh,ai:'pursue',state:'walk',alert:true,moveMag:.65,pose:0,strike:0,hitT:0,deadT:0,bestiaryDistance:8+(i%12)*2});
  }
  const buildTime=performance.now()-a;
  const b=performance.now();
  for(let f=0;f<120;f++)for(const e of entities)B.update(e,1/60,f/60);
  const updateTime=performance.now()-b;
  function count(o){let n=o.isMesh?1:0;for(const c of o.children||[])n+=count(c);return n;}
  return {build40Ms:Math.round(buildTime),updates4800Ms:Math.round(updateTime),mockUpdateMsPerEntity: +(updateTime/4800).toFixed(4),
    meshObjects40:entities.reduce((n,e)=>n+count(e.mesh),0),firstLOD:Object.fromEntries(types.map(t=>[t,B.geometryStats()[t]]))};
 }''')
 browser.close()
 (ROOT/'tests/sculpt_runtime_budget.json').write_text(json.dumps(result,indent=2))
 print('SIMULATED 40-enemy benchmark (NO GPU):')
 print(json.dumps(result,indent=2))
