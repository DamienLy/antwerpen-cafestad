const {chromium,devices}=require('playwright');
const URL="file://"+require("path").resolve(__dirname,"../docs/index.html");
(async()=>{const b=await chromium.launch();const log=[];
async function run(label,ctxOpts,tap){
  const ctx=await b.newContext(ctxOpts);const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto(URL);await p.waitForTimeout(900);
  const click=async(x,y)=>tap?p.touchscreen.tap(x,y):p.mouse.click(x,y);
  const clickSel=async s=>{try{await p.locator(s).first().scrollIntoViewIfNeeded({timeout:1500})}catch(_){};const bb=await p.locator(s).first().boundingBox();if(!bb)return 'GEEN '+s;await click(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(250);return null};
  const scr=n=>p.evaluate(n=>{const x=st[n],[cx,cy]=pos(x),m=svg.getScreenCTM(),r=svg.getBoundingClientRect(),X=m.a*cx+m.e,Y=m.d*cy+m.f;const top=document.elementFromPoint(X,Y);const ok=X>r.left+4&&X<r.right-4&&Y>r.top+4&&Y<r.bottom-4&&top&&svg.contains(top);return ok?[X,Y]:[-1,-1]},n);
  const state=()=>p.evaluate(()=>({hidden:card.hidden,sel,h2:card.querySelector('h2')&&card.querySelector('h2').textContent}));
  const under=(x,y)=>p.evaluate(([x,y])=>{const e=document.elementFromPoint(x,y);return e?(e.tagName+'.'+(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)+'#'+e.id):'none'},[x,y]);
  const test=async(mode)=>{
    for(const n of ['Dam 12','Kid\'s','Café Ernst','Bar Leon','Café Clodette','Pamela','Den Engel','Cabron','ABC','Café Jozef','Bosbar','Ons Huis']){await p.evaluate(()=>{if(morphT===null)fit();else morphCam(true)});await p.waitForTimeout(150);
      const [x,y]=await scr(n);const W=await p.evaluate(()=>[innerWidth,innerHeight]);
      if(x<0||y<0||x>W[0]||y>W[1]){log.push(`${label} ${mode} ${n}: buiten beeld`);continue}
      const u=await under(x,y);await click(x,y);await p.waitForTimeout(300);let s=await state();
      const ok=!s.hidden&&s.sel===n;log.push(`${label} ${mode} tik ${n}: ${ok?'OK':'FOUT → '+JSON.stringify(s)+' onder: '+u}`);
      if(!ok)continue;
      // arrow
      const ar=await p.locator('#card .arr:not([disabled])').first();if(await ar.count()){await ar.scrollIntoViewIfNeeded();const bb=await ar.boundingBox();const u2=await under(bb.x+bb.width/2,bb.y+bb.height/2);await click(bb.x+bb.width/2,bb.y+bb.height/2);await p.waitForTimeout(300);s=await state();log.push(`   pijltje: ${s.sel!==n&&!s.hidden?'OK → '+s.sel:'FOUT '+JSON.stringify(s)+' onder: '+u2}`)}
      await p.locator('#card .x').scrollIntoViewIfNeeded();const xb=await p.locator('#card .x').boundingBox();const u3=await under(xb.x+xb.width/2,xb.y+xb.height/2);await click(xb.x+xb.width/2,xb.y+xb.height/2);await p.waitForTimeout(300);s=await state();
      log.push(`   kruisje: ${s.hidden?'OK':'FOUT '+JSON.stringify(s)+' onder: '+u3}`);
    }};
  await test('kaart');
  await clickSel('[data-tab="morph"]');await p.waitForTimeout(400);
  await test('poster');
  // slider half
  await p.evaluate(()=>{const m=document.getElementById('mt');m.value=500;m.dispatchEvent(new Event('input'))});await p.waitForTimeout(300);
  await test('halfweg');
  await clickSel('[data-tab="map"]');
  // other buttons
  for(const [s,chk] of [['#rnd','!card.hidden'],['#tourBtn','!card.hidden'],['#setBtn','!card.hidden']]){
    const e=await clickSel(s);const v=await p.evaluate(chk);log.push(`${label} knop ${s}: ${e||(v?'OK':'FOUT')}`);
    const xb=await p.locator('#card .x').boundingBox();if(xb){await click(xb.x+xb.width/2,xb.y+xb.height/2);await p.waitForTimeout(250);log.push(`   kruisje: ${await p.evaluate('card.hidden')?'OK':'FOUT'}`)}}
  // line chip & ride
  await clickSel('#chips button');log.push(`${label} lijnchip: focus=${await p.evaluate('focusLine')}`);await clickSel('#chips button');
  await p.evaluate(()=>showLine(D.lines[0].id));const r=await clickSel('[data-ride]');await p.waitForTimeout(1500);log.push(`${label} rijd mee: ${r||'sel='+await p.evaluate('sel')}`);
  const xb=await p.locator('#card .x').boundingBox();if(xb){await click(xb.x+xb.width/2,xb.y+xb.height/2);await p.waitForTimeout(250);log.push(`   kruisje na rit: ${await p.evaluate('card.hidden')?'OK':'FOUT'}`)}
  // zoom buttons
  const w0=await p.evaluate('view.w');await clickSel('#zi');const w1=await p.evaluate('view.w');log.push(`${label} zoom +: ${w1<w0?'OK':'FOUT'}`);
  // search
  await p.fill('#q','Kulminator');await p.waitForTimeout(300);await clickSel('#results [data-n]');log.push(`${label} zoeken: ${await p.evaluate('sel')}`);
  if(errs.length)log.push(`${label} JS-FOUTEN: ${errs.join(' | ')}`);
  await ctx.close()}
await run('laptop',{viewport:{width:1300,height:860}},false);
await run('iphone',{...devices['iPhone 13']},true);
console.log(log.join('\n'));await b.close()})();
