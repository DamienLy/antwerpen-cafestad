const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];
const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1,colorScheme:'light'});p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/antwerpen-cafestad/docs/index.html');await p.waitForTimeout(1200);
await p.evaluate(()=>{
  document.querySelector('header').style.display='none';
  document.querySelectorAll('.levels,.zoom,.key,#card,#lmode,#morph,#toast,.cartouche').forEach(e=>e&&(e.style.display='none'));
  const r=D.stations.map(x=>P(x.lat,x.lon)),xs=r.map(q=>q[0]),ys=r.map(q=>q[1]);
  const x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys);
  const h=(y1-y0)*1.08,w=h*1200/630;view={x:x1-w+(x1-x0)*.06,y:y0-(y1-y0)*.04,w,h};render();
  const o=document.createElement('div');o.innerHTML=`<div style="font:800 64px/1.02 var(--display);letter-spacing:-.01em"><span style="color:#e8901e">Cafékaart</span><br><span style="color:#c0272d">Antwerpen</span></div>
  <div style="font:600 20px var(--body);color:#3a3a3a;margin-top:14px;white-space:nowrap">De caféstad-poster op de echte kaart</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;max-width:330px">${D.lines.map(l=>`<span style="width:26px;height:26px;border-radius:50%;background:${l.c};box-shadow:0 0 0 2px #fff"></span>`).join('')}</div>
  <div style="font:500 18px var(--body);color:#555;margin-top:14px">12 lijnen · 138 cafés</div>`;
  Object.assign(o.style,{position:'fixed',left:'0',top:'0',bottom:'0',width:'420px',padding:'64px 0 0 52px',boxSizing:'border-box',
    background:'linear-gradient(90deg,rgba(250,248,243,1) 0%,rgba(250,248,243,.97) 70%,rgba(250,248,243,0) 100%)',zIndex:50});
  document.body.appendChild(o)});
await p.waitForTimeout(600);await p.screenshot({path:'/home/claude/antwerpen-cafestad/docs/preview.png'});await p.screenshot({path:'/home/claude/antwerpen-cafestad/docs/preview.jpg',type:'jpeg',quality:84});
console.log(JSON.stringify(errs));await b.close()})();
