(() => {
'use strict';
const HV=window.HV;
HV.projectionSeed = mode => {
  const nodes=new Set(),edges=new Set(),allN=HV.state.data.nodes,allE=HV.state.data.hyperedges,eids=new Set(allE.map(e=>e.id));
  if(mode==='all'){
    const layer=HV.els.layer.value,type=HV.els.relationType.value;
    if(layer==='all'&&type==='all'){allN.forEach(n=>nodes.add(n.id));allE.forEach(e=>edges.add(e.id));return{nodes,edges};}
    if(type==='all')allN.filter(n=>layer==='all'||n.layer===layer).forEach(n=>nodes.add(n.id));
    allE.filter(e=>(layer==='all'||e.layer===layer)&&(type==='all'||e.type===type)).forEach(e=>edges.add(e.id));
    return{nodes,edges};
  }
  if(mode==='theory'){
    const theory=new Set(allN.filter(n=>n.layer==='theory').map(n=>n.id));theory.forEach(id=>nodes.add(id));
    for(const e of allE)if(e.type==='schema:Equation'||e.layer==='theory'||Object.values(e.roles||{}).some(p=>theory.has(p)))edges.add(e.id);
  }else if(mode==='evidence'){
    const evidence=new Set(allN.filter(n=>n.layer==='evidence').map(n=>n.id));evidence.forEach(id=>nodes.add(id));
    for(const e of allE)if(e.layer==='evidence'||Object.values(e.roles||{}).some(p=>evidence.has(p)))edges.add(e.id);
  }else{
    const types=HV.RELATION_PROJECTIONS[mode]||new Set();allE.filter(e=>types.has(e.type)).forEach(e=>edges.add(e.id));
  }
  let changed=true;while(changed){changed=false;for(const id of [...edges]){const e=allE.find(x=>x.id===id);if(!e)continue;if(!nodes.has(e.type)){nodes.add(e.type);changed=true;}for(const p of Object.values(e.roles||{})){if(eids.has(p)){if(!edges.has(p)){edges.add(p);changed=true;}}else if(!nodes.has(p)){nodes.add(p);changed=true;}}}}
  return{nodes,edges};
};
HV.project = () => {const mode=HV.els.projection?.value||'all';let {nodes,edges}=HV.projectionSeed(mode);if(HV.state.focus){nodes=new Set([...nodes].filter(x=>HV.state.focus.has(x)));edges=new Set([...edges].filter(x=>HV.state.focus.has(x)));}return{nodes:HV.state.data.nodes.filter(n=>nodes.has(n.id)),hyperedges:HV.state.data.hyperedges.filter(e=>edges.has(e.id))};};
HV.incidence = view => {const all=new Map(),graph=new Map();view.nodes.forEach(n=>all.set(n.id,n));view.hyperedges.forEach(e=>all.set(e.id,e));for(const id of all.keys())graph.set(id,new Set());for(const e of view.hyperedges){if(graph.has(e.type)){graph.get(e.id).add(e.type);graph.get(e.type).add(e.id);}for(const p of Object.values(e.roles||{}))if(graph.has(p)){graph.get(e.id).add(p);graph.get(p).add(e.id);}}return{all,graph};};
HV.column = (x,r) => x.layer==='theory'?(r?0:1):x.layer==='study'?(r?2:3):x.layer==='evidence'?(r?4:5):(r?2:3);
HV.barycentricOrder = (cols,all,graph,rels) => {const order=new Map([...cols].map(([c,ids])=>[c,[...ids].sort((a,b)=>HV.labelOf(a).localeCompare(HV.labelOf(b)))])),colOf=id=>HV.column(all.get(id),rels.has(id));for(let sweep=0;sweep<10;sweep++){let row=new Map();for(const ids of order.values())ids.forEach((id,i)=>row.set(id,i));const cs=[...order.keys()].sort((a,b)=>sweep%2?a-b:b-a);for(const c of cs){order.get(c).sort((a,b)=>{const score=id=>{const ys=[...(graph.get(id)||[])].filter(n=>Math.abs(colOf(n)-c)<=1&&row.has(n)).map(n=>row.get(n));return ys.length?ys.reduce((s,x)=>s+x,0)/ys.length:(row.get(id)||0);};return score(a)-score(b)||a.localeCompare(b);});row=new Map();for(const ids of order.values())ids.forEach((id,i)=>row.set(id,i));}}return order;};
HV.pack = (ids,cy,rels,gap=30) => {const hs=ids.map(id=>rels.has(id)?HV.relationHeight:HV.nodeHeight),total=hs.reduce((a,b)=>a+b,0)+gap*Math.max(0,ids.length-1);let y=cy-total/2,m=new Map();ids.forEach((id,i)=>{m.set(id,y+hs[i]/2);y+=hs[i]+gap;});return m;};
HV.hubLayout = view => {
  const {all,graph}=HV.incidence(view),rels=new Set(view.hyperedges.map(e=>e.id)),positions=new Map(),shared=view.nodes.filter(n=>n.source==='shared'),meta=shared.filter(n=>n.layer==='metamodel').sort((a,b)=>a.id.localeCompare(b.id)),schema=shared.filter(n=>n.layer==='schema'),sharedR=view.hyperedges.filter(e=>e.source==='shared').sort((a,b)=>a.id.localeCompare(b.id));
  const cols=Math.max(1,Math.ceil(Math.sqrt(meta.length))),rows=Math.ceil(meta.length/cols);meta.forEach((n,i)=>positions.set(n.id,{x:(i%cols-(cols-1)/2)*190,y:(Math.floor(i/cols)-(rows-1)/2)*115,w:HV.nodeWidth(n),h:HV.nodeHeight}));
  const ring=(items,r,isRel,phase)=>items.sort((a,b)=>a.id.localeCompare(b.id)).forEach((item,i)=>{const t=phase+2*Math.PI*i/Math.max(1,items.length);positions.set(item.id,{x:r*Math.cos(t),y:r*Math.sin(t),w:isRel?HV.relationWidth(item):HV.nodeWidth(item),h:isRel?HV.relationHeight:HV.nodeHeight});});
  ring(sharedR,315,true,-Math.PI/2);ring(schema.filter(n=>n.kind==='relationType'),470,false,-Math.PI/2);ring(schema.filter(n=>n.kind!=='relationType'),650,false,-Math.PI/2+.12);
  const domains=[...new Set([...all.values()].map(x=>x.source).filter(x=>x&&x!=='shared'))].sort(),counts=new Map(domains.map(d=>[d,[...all.values()].filter(x=>x.source===d).length])),ordered=[...domains].sort((a,b)=>counts.get(b)-counts.get(a)||a.localeCompare(b)),slots=[[-1,-1],[1,-1],[-1,1],[1,1]],slotMap=new Map(ordered.map((d,i)=>[d,slots[i]||[i%2?-1:1,Math.floor(i/2)%2?-1:1]]));
  for(const d of domains){const [side,row]=slotMap.get(d),items=[...all.values()].filter(x=>x.source===d),columns=new Map();for(const x of items){const c=HV.column(x,rels.has(x.id));if(!columns.has(c))columns.set(c,[]);columns.get(c).push(x.id);}const orderedCols=HV.barycentricOrder(columns,all,graph,rels),cy=row*760;for(const [c,ids] of orderedCols){const ys=HV.pack(ids,cy,rels);for(const id of ids){const x=all.get(id);positions.set(id,{x:side*(720+c*215),y:ys.get(id),w:rels.has(id)?HV.relationWidth(x):HV.nodeWidth(x),h:rels.has(id)?HV.relationHeight:HV.nodeHeight});}}}
  let minx=Infinity,miny=Infinity,maxx=-Infinity,maxy=-Infinity;for(const z of positions.values()){minx=Math.min(minx,z.x-z.w/2);maxx=Math.max(maxx,z.x+z.w/2);miny=Math.min(miny,z.y-z.h/2);maxy=Math.max(maxy,z.y+z.h/2);}return{positions,slotMap,width:maxx-minx+180,height:maxy-miny+180,offsetX:-minx+90,offsetY:-miny+90};
};
HV.relayout = async (fit=true) => {HV.showLoading(true,'Computing hub-and-lobes layout…');try{HV.state.view=HV.project();HV.state.layout=HV.hubLayout(HV.state.view);HV.render();if(fit)HV.fitGraph();const mode=HV.els.projection?.value||'all';HV.els.status.textContent=`${HV.state.view.nodes.length} elements · ${HV.state.view.hyperedges.length} hyperrelations · ${mode==='all'?'overview':mode}`;}catch(error){console.error(error);HV.els.status.textContent=`Layout failed: ${error.message}`;}finally{HV.showLoading(false);}};
})();
