/* deterministic timeline engine: window.seek(T) */
const EASE = {
  lin: p=>p,
  out: p=>1-Math.pow(1-p,3),
  expo: p=>p>=1?1:1-Math.pow(2,-9*p),
  back: p=>{const c=1.70158,c3=c+1;return 1+c3*Math.pow(p-1,3)+c*Math.pow(p-1,2);},
  inout: p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,
};
const PRESET = {
  fade : {d:.55, e:'out',  o:[0,1]},
  up   : {d:.70, e:'out',  o:[0,1], y:[52,0]},
  down : {d:.70, e:'out',  o:[0,1], y:[-38,0]},
  left : {d:.70, e:'out',  o:[0,1], x:[-44,0]},
  pop  : {d:.60, e:'back', o:[0,1], s:[.82,1]},
  wipe : {d:.55, e:'expo', sx:[0,1]},
  img  : {d:.95, e:'out',  o:[0,1], s:[1.10,1]},
  dim  : {d:.55, e:'out',  o:[1,.26]},
  rise : {d:1.6, e:'out',  o:[0,1], y:[26,0]},
};
let SCENES=[], TRACKS=[], TOTAL=0;

function build(total){
  TOTAL=total;
  const nodes=[...document.querySelectorAll('.scene')];
  SCENES=nodes.map((el,i)=>({el,start:parseFloat(el.dataset.s)}));
  SCENES.forEach((s,i)=>{ s.end = (i+1<SCENES.length)? SCENES[i+1].start : TOTAL+0.5; s.el.style.zIndex=10+i; });
  document.querySelectorAll('[data-a],[data-a2]').forEach(el=>{
    ['a','a2'].forEach(k=>{
      const v=el.dataset[k]; if(!v) return;
      const p=v.split(',').map(x=>x.trim());
      const t0=parseFloat(p[0]);
      const type=p[2]||'up';
      const base=PRESET[type]||PRESET.up;
      const d=p[1]?parseFloat(p[1]):base.d;
      TRACKS.push({el,t0,d,e:base.e,o:base.o,y:base.y,x:base.x,s:base.s,sx:base.sx});
    });
  });
  TRACKS.forEach(t=>{ if(!t.el._st) t.el._st={o:null,y:0,x:0,s:1,sx:null}; });
}

function seek(T){
  SCENES.forEach(sc=>{
    const vis = T>=sc.start-0.02 && T<sc.end;
    sc.el.style.display = vis?'block':'none';
    if(!vis) return;
    const fs=sc.end-0.30;
    sc.el.style.opacity = T>fs ? String(Math.max(0,1-(T-fs)/0.26)) : '1';
    const dr=(T-sc.start);
    sc.el.style.transform=`translateY(${(-dr*1.6).toFixed(2)}px)`;
  });
  TRACKS.forEach(t=>{
    const raw=(T-t.t0)/t.d;
    const p=EASE[t.e](Math.max(0,Math.min(1,raw)));
    const st=t.el._st;
    if(t.o)  st.o = t.o[0]+(t.o[1]-t.o[0])*p;
    if(t.y)  st.y = t.y[0]+(t.y[1]-t.y[0])*p;
    if(t.x)  st.x = t.x[0]+(t.x[1]-t.x[0])*p;
    if(t.s)  st.s = t.s[0]+(t.s[1]-t.s[0])*p;
    if(t.sx) st.sx= t.sx[0]+(t.sx[1]-t.sx[0])*p;
  });
  TRACKS.forEach(t=>{
    const st=t.el._st;
    if(st.o!==null) t.el.style.opacity=st.o.toFixed(3);
    const tr=[];
    if(st.y) tr.push(`translateY(${st.y.toFixed(2)}px)`);
    if(st.x) tr.push(`translateX(${st.x.toFixed(2)}px)`);
    if(st.s!==1) tr.push(`scale(${st.s.toFixed(4)})`);
    if(st.sx!==null) tr.push(`scaleX(${st.sx.toFixed(4)})`);
    t.el.style.transform=tr.join(' ');
  });
  const bar=document.getElementById('prog');
  if(bar) bar.style.transform=`scaleX(${Math.min(1,T/TOTAL).toFixed(4)})`;
  const g=document.getElementById('glow');
  if(g) g.style.transform=`translate(${(Math.sin(T*0.42)*70).toFixed(1)}px,${(Math.cos(T*0.31)*90).toFixed(1)}px)`;
}
window.seek=seek; window.buildTimeline=build;
