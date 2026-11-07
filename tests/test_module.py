from playwright.sync_api import sync_playwright
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page()
 page.goto('about:blank')
 page.add_script_tag(path=str(ROOT/'tests/three_bestiary_mock.js'))
 page.add_script_tag(path=str(ROOT/'bestiary_pass.js'))
 results=[]
 for t in ['brute','crawler','imp','wraith','necromancer','gargoyle']:
  try:
   r=page.evaluate('''type => {const B=window.DEPTHS_BESTIARY,tm=performance.now(),g=B.build(type);
    const e={mesh:g,moveMag:.5,ai:'attack',alert:true,hitT:.2,pose:.5};
    for(let i=0;i<60;i++)B.update(e,1/60,i/60);
    const rig=g.userData.bestiary,geo=rig.lod.levels[0].object.geometry;
    const si=geo.attributes.skinIndex,sw=geo.attributes.skinWeight;
    let valid=true;
    for(let j=0;j<sw.count;j++){let w=0;for(let k=0;k<4;k++)w+=sw.array[j*4+k];if(Math.abs(w-1)>.0001)valid=false;}
    return {type,ms:Math.round(performance.now()-tm),buildMs:rig.geometryTime,
      triangles:rig.normCount,vertices:geo.attributes.position.count,bones:Object.keys(rig.bones).length,
      maxInfluences:4,weightsValid:valid,numberOfWings:rig.parts.wings.length};
  }''',t)
   results.append(r)
  except Exception as ex:
   results.append({'type':t,'error':str(ex)})
 print(json.dumps(results,indent=2))
 (ROOT/'tests/model_test.json').write_text(json.dumps(results,indent=2))
 b.close()
 assert all('error' not in r and r['weightsValid'] for r in results),results
