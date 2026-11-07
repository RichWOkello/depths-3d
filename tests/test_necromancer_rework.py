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
        const g=B.build('necromancer');
        const r=g.userData.bestiary,p=r.parts;
        const baseline={robeLayers:p.robeShells.length,hood:p.hoodShell!==null,face:p.faceCranium!==null,
            staff:p.staffCrown!==null,staffLight:p.staffLight!==null,runeGroups:p.robeRunes.length,
            beltSkulls:p.trophies.length,wanderingWisps:p.wisps.length,orbHalo:p.orbHalo!==null,
            boneCount:Object.keys(r.bones).length,mainSkinIndex:r.lod.levels[0].object.geometry.attributes.skinIndex.count,
            baselineRuneOpacity:p.runeMat.opacity,baselineStaffLight:p.staffLight.intensity};
        const casting={mesh:g,moveMag:0,ai:'attack',state:'attack',alert:true,pose:1,strike:1,hitT:0,deadT:0};
        B.update(casting,1/60,1.2);
        const after={runeOpacity:p.runeMat.opacity,staffLight:p.staffLight.intensity,rightArmPitch:r.bones.Rshoulder.rotation.x,
            leftArmPitch:r.bones.Lshoulder.rotation.x,spellScale:p.spell.scale.x,orbiters:p.runes.length};
        const idle={mesh:g,moveMag:0,ai:'idle',state:'idle',alert:false,pose:0,strike:0,hitT:0,deadT:0};
        B.update(idle,1/60,1.4);
        const afterIdle={runeOpacity:p.runeMat.opacity,staffLight:p.staffLight.intensity,rightArmPitch:r.bones.Rshoulder.rotation.x};
        const stats=B.geometryStats();
        const range={};
        for(const type of B.TYPES){const x=B.build(type),pr=x.userData.bestiary;range[type]={built:!!pr,triangles:pr.normCount};}
        return {baseline,after,afterIdle,range};
    }''')
    browser.close()
    assert result['baseline']['robeLayers']==2
    assert result['baseline']['hood'] and result['baseline']['face']
    assert result['baseline']['staff'] and result['baseline']['staffLight']
    assert result['baseline']['runeGroups']>=10
    assert result['baseline']['beltSkulls']==3
    assert result['baseline']['wanderingWisps']==5
    assert result['baseline']['orbHalo']
    assert result['baseline']['boneCount']==17
    assert result['after']['runeOpacity']>result['afterIdle']['runeOpacity']
    assert result['after']['staffLight']>result['afterIdle']['staffLight']
    assert result['after']['rightArmPitch']<result['afterIdle']['rightArmPitch']
    assert all(v['built'] for v in result['range'].values())
    (ROOT/'tests/necromancer_test.json').write_text(json.dumps(result,indent=2))
    print('PASS necromancer model, hood, skull, garments, belt ornaments, spell and casting animations')
    print(json.dumps(result,indent=2))
