from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
src=(R/'src/game.js').read_text()
needle='// Initial dungeon renders behind overlays, which also own their illustrated art.'
src=src.replace(needle,"""window.__w={buildLevel,setLevel:x=>{level=x},getGrid:()=>grid,getExit:()=>exitCell,getStart:()=>[1,1],getTheme:()=>currentTheme.name,getSecrets:()=>secretWalls.length,getSwitches:()=>runicSwitches.length,getKey:()=>pickups.some(p=>p.type==='key'),getHazards:()=>hazards.length,boss:()=>currentBoss?.bossName||null};\n"""+needle,1)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 pg=browser.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
 pg.set_content('<html><body>'+(R/'src/game.html').read_text()+'</body></html>')
 pg.add_script_tag(content=(R/'tests/mock_three.js').read_text());pg.add_script_tag(content=src)
 pg.wait_for_selector('[data-a="skipintro"]')
 result=pg.evaluate("""()=>{
 const result=[];
 for(let level=1;level<=20;level++){
  __w.setLevel(level);__w.buildLevel();
  const grid=__w.getGrid(),exit=__w.getExit(),n=grid.length,queue=[[1,1]],seen=new Set(['1,1']);
  for(let i=0;i<queue.length;i++){
    const [x,y]=queue[i];for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){
      let xx=x+dx,yy=y+dy,k=xx+','+yy;
      if(xx>=0&&yy>=0&&xx<n&&yy<n&&grid[yy][xx]===0&&!seen.has(k)){seen.add(k);queue.push([xx,yy]);}
    }
  }
  result.push({level,theme:__w.getTheme(),exitReachable:seen.has(exit[0]+','+exit[1]),key:__w.getKey(),switches:__w.getSwitches(),hazards:__w.getHazards(),secret:__w.getSecrets(),boss:__w.boss()});
 }
 return result;
 }""")
 assert len(result)==20 and all(x['exitReachable'] for x in result), result
 assert all(x['key'] for x in result if x['level']%3==0),result
 assert all(x['switches'] for x in result if x['level']%4==0),result
 assert len(set(x['theme'] for x in result))>=9,result
 assert len(set(x['boss'] for x in result if x['boss']))>=4,result
 assert not errors,errors
 print('PASS: 20 connected floors, nine environment themes, all key/altar gates reachable, four boss identities')
 print('FLOOR SAMPLE:',result[0],result[2],result[3],result[4],result[8],result[19])
 browser.close()
