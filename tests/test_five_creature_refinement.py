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
      const B=window.DEPTHS_BESTIARY, result={};
      for (const type of ['brute','crawler','imp','wraith','gargoyle']) {
        const mesh=B.build(type), r=mesh.userData.bestiary,p=r.parts;
        const g=r.lod.levels[0].object.geometry;
        const second=B.build(type);
        const e={mesh,ai:'attack',state:'attack',pose:.9,strike:.8,moveMag:.8,hitT:.2,deadT:0,bestiaryDistance:4,alert:true};
        B.update(e,.016,2.4);
        const nearCount=p.closeOnly.filter(x=>x.visible).length;
        e.bestiaryDistance=30;B.update(e,.016,2.5);
        const farHidden=p.closeOnly.length && p.closeOnly.every(x=>x.visible===false)&&p.midOnly.every(x=>x.visible===false);
        e.bestiaryDistance=3;B.update(e,.016,2.6);
        let finite=true;
        for(const value of g.attributes.position.array)if(!Number.isFinite(value)){finite=false;break;}
        result[type]={
          anatomy:p.anatomy, shell:!!p.cranialShell,
          nearDetails:p.closeOnly.length,midDetails:p.midOnly.length,
          nearCount,farHidden,
          sharedGeometry:r.lod.levels[0].object.geometry===second.userData.bestiary.lod.levels[0].object.geometry,
          finite,triangles:r.normCount.slice(),wings:p.wings.length,tail:p.tailSegments.length,
          hasJaw:!!p.jaw,eyeCount:p.eyes.length,
          disconnected:!mesh.children.includes(r.lod),
          optimizedGeometryCache:B.geometryStats()[type].ms
        };
      }
      const n=B.build('necromancer'), np=n.userData.bestiary.parts;
      result.necromancer={hood:!!np.hoodShell,robeLayers:np.robeShells.length,skulls:np.trophies.length,wisps:np.wisps.length,staff:!!np.staffCrown};
      return result;
    }''')
    browser.close()
    for species in ['brute','crawler','imp','wraith','gargoyle']:
        r=result[species]
        assert r['shell'] and r['finite'] and r['farHidden'] and r['sharedGeometry'],(species,r)
        assert r['nearDetails']>0 and r['midDetails']>0 and r['hasJaw'] and not r['disconnected'],(species,r)
        assert len(r['triangles'])==3 and r['triangles'][2]<1000
    assert result['gargoyle']['wings']==2 and result['gargoyle']['tail']==6
    assert result['necromancer']==dict(hood=True,robeLayers=2,skulls=3,wisps=5,staff=True)
    (ROOT/'tests/five_creatures_test.json').write_text(json.dumps(result,indent=2))
    print('PASS five-creature anatomy and LOD/caching, plus unchanged Necromancer features')
    print(json.dumps(result,indent=2))
