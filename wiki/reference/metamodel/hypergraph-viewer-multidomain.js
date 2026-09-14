(() => {
'use strict';
const HV=window.HV;
const baseHubLayout=HV.hubLayout;
function slotFor(index){
  const band=Math.floor(index/4)+1;
  const quadrant=index%4;
  const side=quadrant%2===0?-1:1;
  const verticalSign=quadrant<2?-1:1;
  return [side,verticalSign*(2*band-1)];
}
HV.hubLayout=view=>{
  const layout=baseHubLayout(view);
  const all=[...view.nodes,...view.hyperedges];
  const domains=[...new Set(all.map(x=>x.source).filter(x=>x&&x!=='shared'))].sort();
  const counts=new Map(domains.map(d=>[d,all.filter(x=>x.source===d).length]));
  const ordered=[...domains].sort((a,b)=>counts.get(b)-counts.get(a)||a.localeCompare(b));
  const desired=new Map(ordered.map((d,i)=>[d,slotFor(i)]));
  for(const d of ordered){
    const old=layout.slotMap.get(d)||desired.get(d);
    const next=desired.get(d);
    if(old[0]===next[0]&&old[1]===next[1])continue;
    for(const item of all){
      if(item.source!==d)continue;
      const p=layout.positions.get(item.id);
      if(!p)continue;
      if(old[0]!==next[0])p.x=-p.x;
      p.y+=(next[1]-old[1])*760;
    }
    layout.slotMap.set(d,next);
  }
  let minx=Infinity,miny=Infinity,maxx=-Infinity,maxy=-Infinity;
  for(const z of layout.positions.values()){
    minx=Math.min(minx,z.x-z.w/2);maxx=Math.max(maxx,z.x+z.w/2);
    miny=Math.min(miny,z.y-z.h/2);maxy=Math.max(maxy,z.y+z.h/2);
  }
  layout.width=maxx-minx+180;layout.height=maxy-miny+180;
  layout.offsetX=-minx+90;layout.offsetY=-miny+90;
  return layout;
};
})();
