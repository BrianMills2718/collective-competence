(() => {
  'use strict';

  const FIXTURES = {
    cc: 'c2-q1-hypergraph-v0.json',
    mechanics: 'classical-mechanics-hypergraph.json',
    oscillator: 'harmonic-oscillator-hypergraph.json',
    reaction: 'first-order-reaction-hypergraph.json',
  };
  const SOURCE_LABEL = {
    cc: 'Collective Competence', mechanics: 'Classical mechanics', oscillator: 'Harmonic oscillator', reaction: 'Reaction kinetics'
  };
  const LAYER_RANK = { metamodel: 0, schema: 1, theory: 2, study: 3, evidence: 4 };
  const COLORS = { metamodel: '#58a6ff', schema: '#c297ff', theory: '#66d48f', study: '#f1a65a', evidence: '#ff7b72' };
  const DOMAIN_COLORS = ['#64d58f','#54c7ec','#f1a65a','#f778ba','#a78bfa','#2dd4bf','#facc15','#fb7185'];
  const NS = 'http://www.w3.org/2000/svg';
  const elk = typeof ELK !== 'undefined' ? new ELK() : null;

  const ids = ['fixture','layer','relationType','layoutMode','search','relayout','fit','focus','file','status','graph','stage','loading','selTitle','selMeta','selDesc','roles'];
  const els = Object.fromEntries(ids.map(id => [id, document.getElementById(id)]));

  const state = {
    data: { nodes: [], hyperedges: [] },
    visible: null,
    layout: null,
    selected: null,
    focusSet: null,
    transform: { x: 0, y: 0, k: 1 },
    panning: null,
    sourceLabel: 'all stress tests',
    sourceNames: new Map(),
  };

  function rank(x) { return LAYER_RANK[x?.layer] ?? 3; }
  function safe(v) { return String(v ?? ''); }
  function escapeHtml(s) { return safe(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function truncate(s,n=28){ s=safe(s); return s.length>n ? s.slice(0,n-1)+'…' : s; }
  function isSharedNode(n){ return ['metamodel','schema'].includes(n.layer); }
  function index(){ const m=new Map(); state.data.nodes.forEach(x=>m.set(x.id,x)); state.data.hyperedges.forEach(x=>m.set(x.id,x)); return m; }
  function labelOf(id){ const x=index().get(id); return x?.label || x?.type || id; }
  function sourceColor(source){ if(source==='shared') return COLORS.schema; const keys=[...state.sourceNames.keys()].filter(x=>x!=='shared').sort(); const i=Math.max(0,keys.indexOf(source)); return DOMAIN_COLORS[i%DOMAIN_COLORS.length]; }

  async function fetchJson(path){ const r=await fetch(path,{cache:'no-store'}); if(!r.ok) throw new Error(`${path}: HTTP ${r.status}`); return r.json(); }

  function normalizedDocument(slug,doc){
    const nodeIdMap=new Map();
    for(const n of doc.nodes||[]) nodeIdMap.set(n.id, isSharedNode(n) ? n.id : `${slug}::${n.id}`);
    const edgeIdMap=new Map();
    for(const e of doc.hyperedges||[]){
      let shared=['metamodel','schema'].includes(e.layer);
      if(shared){
        for(const p of Object.values(e.roles||{})){
          if(nodeIdMap.has(p) && nodeIdMap.get(p)!==p){ shared=false; break; }
        }
      }
      edgeIdMap.set(e.id, shared ? e.id : `${slug}::${e.id}`);
    }
    const nodes=(doc.nodes||[]).map(n=>({ ...n, id:nodeIdMap.get(n.id), originalId:n.id, source:isSharedNode(n)?'shared':slug, sources:[isSharedNode(n)?'shared':slug] }));
    const hyperedges=(doc.hyperedges||[]).map(e=>{
      const roles={}; for(const [role,p] of Object.entries(e.roles||{})) roles[role]=edgeIdMap.get(p) || nodeIdMap.get(p) || p;
      return { ...e, id:edgeIdMap.get(e.id), originalId:e.id, type:nodeIdMap.get(e.type)||e.type, roles, source:['metamodel','schema'].includes(e.layer)&&edgeIdMap.get(e.id)===e.id?'shared':slug, sources:[slug] };
    });
    return {nodes,hyperedges};
  }

  function mergeDocuments(entries){
    const nodeMap=new Map(), edgeMap=new Map();
    for(const {slug,doc} of entries){
      state.sourceNames.set(slug,SOURCE_LABEL[slug]||slug);
      const norm=normalizedDocument(slug,doc);
      for(const n of norm.nodes){
        if(!nodeMap.has(n.id)) nodeMap.set(n.id,n);
        else {
          const ex=nodeMap.get(n.id);
          if(ex.label!==n.label || ex.kind!==n.kind || ex.layer!==n.layer) console.warn('Shared node mismatch',n.id,ex,n);
          ex.sources=[...new Set([...(ex.sources||[]),...(n.sources||[])])];
        }
      }
      for(const e of norm.hyperedges){
        if(e.source==='shared' && edgeMap.has(e.id)){
          const ex=edgeMap.get(e.id);
          if(ex.type!==e.type || JSON.stringify(ex.roles)!==JSON.stringify(e.roles)) console.warn('Shared relation mismatch',e.id,ex,e);
          ex.sources=[...new Set([...(ex.sources||[]),slug])];
        } else {
          if(edgeMap.has(e.id)) throw new Error(`Merged hyperedge ID collision: ${e.id}`);
          edgeMap.set(e.id,e);
        }
      }
    }
    return {model:'scientific-hypergraph-merged',nodes:[...nodeMap.values()],hyperedges:[...edgeMap.values()]};
  }

  async function loadPreset(value){
    showLoading(true,'Loading fixture…');
    try{
      state.sourceNames=new Map([['shared','Shared kernel/schema']]);
      const keys=value==='all'?Object.keys(FIXTURES):[value];
      const docs=await Promise.all(keys.map(async slug=>({slug,doc:await fetchJson(FIXTURES[slug])})));
      state.data=mergeDocuments(docs); state.sourceLabel=value==='all'?'all stress tests':value; state.selected=null; state.focusSet=null;
      populateRelationTypes(); await relayout(true);
    }catch(err){ console.error(err); els.status.textContent=`Load failed: ${err.message}`; showLoading(false); }
  }

  async function loadFiles(files){
    const entries=[]; state.sourceNames=new Map([['shared','Shared kernel/schema']]);
    for(const file of files){ const slug=file.name.replace(/\.(jsonld|json)$/i,'').replace(/[^a-z0-9_-]+/gi,'-'); entries.push({slug,doc:JSON.parse(await file.text())}); }
    state.data=mergeDocuments(entries); state.sourceLabel=entries.map(x=>x.slug).join(', '); state.selected=null; state.focusSet=null; populateRelationTypes(); await relayout(true);
  }

  function populateRelationTypes(){
    const current=els.relationType.value; const ids=[...new Set(state.data.hyperedges.map(e=>e.type))].sort((a,b)=>labelOf(a).localeCompare(labelOf(b)));
    els.relationType.innerHTML='<option value="all">All relation types</option>'+ids.map(id=>`<option value="${escapeHtml(id)}">${escapeHtml(labelOf(id))}</option>`).join(''); if(ids.includes(current)) els.relationType.value=current;
  }

  function projection(){
    const idx=index(); let baseNodes=new Set(),baseEdges=new Set(); const layer=els.layer.value, relationType=els.relationType.value;
    if(layer==='all'&&relationType==='all'){ state.data.nodes.forEach(n=>baseNodes.add(n.id)); state.data.hyperedges.forEach(e=>baseEdges.add(e.id)); }
    else{
      for(const n of state.data.nodes) if(layer==='all'||n.layer===layer) baseNodes.add(n.id);
      for(const e of state.data.hyperedges){ if((layer==='all'||e.layer===layer)&&(relationType==='all'||e.type===relationType)) baseEdges.add(e.id); }
      if(relationType!=='all') baseNodes.clear();
    }
    let changed=true; while(changed){ changed=false; for(const id of [...baseEdges]){ const e=idx.get(id); if(!e) continue; if(!baseNodes.has(e.type)){baseNodes.add(e.type);changed=true;} for(const p of Object.values(e.roles||{})){ if(state.data.hyperedges.some(x=>x.id===p)){ if(!baseEdges.has(p)){baseEdges.add(p);changed=true;} } else if(!baseNodes.has(p)){baseNodes.add(p);changed=true;} } } }
    if(layer!=='all'&&relationType==='all'){
      for(const e of state.data.hyperedges){ if(Object.values(e.roles||{}).some(p=>baseNodes.has(p))){ baseEdges.add(e.id);baseNodes.add(e.type);Object.values(e.roles||{}).forEach(p=>state.data.hyperedges.some(x=>x.id===p)?baseEdges.add(p):baseNodes.add(p)); } }
    }
    if(state.focusSet){ baseNodes=new Set([...baseNodes].filter(x=>state.focusSet.has(x))); baseEdges=new Set([...baseEdges].filter(x=>state.focusSet.has(x))); }
    return {nodes:state.data.nodes.filter(n=>baseNodes.has(n.id)),hyperedges:state.data.hyperedges.filter(e=>baseEdges.has(e.id))};
  }

  function incidence(view){
    const all=new Map();view.nodes.forEach(n=>all.set(n.id,n));view.hyperedges.forEach(e=>all.set(e.id,e));
    const inc=new Map([...all.keys()].map(id=>[id,new Set()]));
    for(const e of view.hyperedges){ if(inc.has(e.type)){inc.get(e.id)?.add(e.type);inc.get(e.type)?.add(e.id);} for(const p of Object.values(e.roles||{})){ if(inc.has(p)){inc.get(e.id)?.add(p);inc.get(p)?.add(e.id);} } }
    return {all,inc};
  }

  function circularMean(angles,fallback=0){ if(!angles.length) return fallback; const x=angles.reduce((s,a)=>s+Math.cos(a),0),y=angles.reduce((s,a)=>s+Math.sin(a),0); return Math.atan2(y,x); }
  function spreadAngles(items,desired,lo,hi,minGap){
    if(!items.length)return new Map(); const ordered=[...items].sort((a,b)=>(desired.get(a)??0)-(desired.get(b)??0)||a.localeCompare(b));
    if(ordered.length===1)return new Map([[ordered[0],Math.max(lo,Math.min(hi,desired.get(ordered[0])??(lo+hi)/2))]]);
    const span=hi-lo, gap=Math.min(minGap,span/(ordered.length-1)); const vals=[];
    for(let i=0;i<ordered.length;i++){ const want=Math.max(lo,Math.min(hi,desired.get(ordered[i])??(lo+hi)/2)); vals[i]=i===0?want:Math.max(want,vals[i-1]+gap); }
    if(vals.at(-1)>hi){ const shift=vals.at(-1)-hi; for(let i=0;i<vals.length;i++)vals[i]-=shift; }
    for(let i=vals.length-2;i>=0;i--) vals[i]=Math.min(vals[i],vals[i+1]-gap);
    if(vals[0]<lo){ const shift=lo-vals[0];for(let i=0;i<vals.length;i++)vals[i]+=shift; }
    return new Map(ordered.map((id,i)=>[id,vals[i]]));
  }

  function placePolarTracks(arr,desired,lo,hi,baseR,trackStep=78,maxTracks=4){
    const sorted=[...arr].sort((a,b)=>(desired.get(a.id)??0)-(desired.get(b.id)??0)||a.id.localeCompare(b.id));
    const tracks=Array.from({length:maxTracks},(_,i)=>({r:baseR+i*trackStep,items:[]}));
    const result=new Map();
    for(const n of sorted){
      let best=null;
      for(let ti=0;ti<tracks.length;ti++){
        const tr=tracks[ti], half=(nodeWidth(n)/2+14)/tr.r, last=tr.items.at(-1);
        const want=Math.max(lo+half,Math.min(hi-half,desired.get(n.id)??(lo+hi)/2));
        const cand=last?Math.max(want,last.angle+last.half+half):want;
        if(cand<=hi-half){ const score=Math.abs(cand-want)+ti*.025; if(!best||score<best.score)best={ti,cand,half,score}; }
      }
      if(!best){
        let ti=tracks.length-1;
        for(let i=0;i<tracks.length;i++)if(tracks[i].items.length<tracks[ti].items.length)ti=i;
        const tr=tracks[ti],half=(nodeWidth(n)/2+14)/tr.r,last=tr.items.at(-1),want=Math.max(lo+half,Math.min(hi-half,desired.get(n.id)??(lo+hi)/2));
        best={ti,cand:last?last.angle+last.half+half:want,half,score:99};
      }
      tracks[best.ti].items.push({id:n.id,angle:best.cand,half:best.half});
    }
    for(const tr of tracks){
      if(!tr.items.length)continue;
      const last=tr.items.at(-1);
      if(last.angle+last.half>hi){
        const total=tr.items.reduce((sum,x)=>sum+2*x.half,0),free=Math.max(0,(hi-lo)-total),gap=tr.items.length>1?free/(tr.items.length-1):0;
        let cursor=lo; for(const x of tr.items){cursor+=x.half;x.angle=cursor;cursor+=x.half+gap;}
      }
      for(const x of tr.items)result.set(x.id,{angle:x.angle,r:tr.r});
    }
    return result;
  }

  function semanticRadialLayout(view){
    const {all,inc}=incidence(view); const pos=new Map(); const domains=[...new Set([...all.values()].map(x=>x.source).filter(s=>s&&s!=='shared'))].sort();
    const domainCount=Math.max(1,domains.length),maxR=domainCount<=2?700:domainCount<=4?830:920;
    const metas=view.nodes.filter(n=>n.layer==='metamodel').sort((a,b)=>a.id.localeCompare(b.id)),metaR=105;
    metas.forEach((n,i)=>{const a=-Math.PI/2+2*Math.PI*i/Math.max(1,metas.length);pos.set(n.id,{x:metaR*Math.cos(a),y:metaR*Math.sin(a),w:nodeWidth(n),h:54,kind:'node'});});
    const sector=new Map(); domains.forEach((d,i)=>sector.set(d,-Math.PI/2+(i+.5)*2*Math.PI/domainCount)); const half=Math.min(Math.PI*.38,Math.PI/domainCount*.72);
    const schemas=view.nodes.filter(n=>n.layer==='schema').sort((a,b)=>a.id.localeCompare(b.id)),schemaR=225;
    schemas.forEach((n,i)=>{ const a=-Math.PI+2*Math.PI*i/Math.max(1,schemas.length); pos.set(n.id,{x:schemaR*Math.cos(a),y:schemaR*Math.sin(a),w:nodeWidth(n),h:48,kind:'node'}); });
    for(const d of domains){
      const c=sector.get(d),lo=c-half,hi=c+half,domainRelations=view.hyperedges.filter(e=>e.source===d).sort((a,b)=>a.id.localeCompare(b.id)),byLayer=new Map();
      for(const e of domainRelations){ const k=e.layer||'study'; if(!byLayer.has(k))byLayer.set(k,[]); byLayer.get(k).push(e); }
      const relRadius={theory:330,study:430,evidence:540,metamodel:280,schema:300},relAngle=new Map();
      for(const [layer,arr] of byLayer){ const desired=new Map(); arr.forEach((e,i)=>desired.set(e.id,lo+(i+1)*(hi-lo)/(arr.length+1))); const spread=spreadAngles(arr.map(e=>e.id),desired,lo,hi,0.11); for(const e of arr){ const a=spread.get(e.id),r=relRadius[layer]||430;relAngle.set(e.id,a);pos.set(e.id,{x:r*Math.cos(a),y:r*Math.sin(a),w:relationWidth(e),h:48,kind:'relation'}); } }
      const domainNodes=view.nodes.filter(n=>n.source===d),nodesByLayer=new Map();for(const n of domainNodes){const k=n.layer||'study';if(!nodesByLayer.has(k))nodesByLayer.set(k,[]);nodesByLayer.get(k).push(n);}
      const nodeRadius={theory:365,study:535,evidence:690,metamodel:300,schema:320};
      for(const [layer,arr] of nodesByLayer){ const desired=new Map(); for(const n of arr){const a=[];for(const nb of inc.get(n.id)||[])if(relAngle.has(nb))a.push(relAngle.get(nb));desired.set(n.id,a.length?circularMean(a,c):c);} const placements=placePolarTracks(arr,desired,lo,hi,nodeRadius[layer]||535,76,layer==='study'?4:3); for(const n of arr){const q=placements.get(n.id),a=q?.angle??c,r=q?.r??(nodeRadius[layer]||535);pos.set(n.id,{x:r*Math.cos(a),y:r*Math.sin(a),w:nodeWidth(n),h:50,kind:'node'});} }
    }
    let f=0;for(const item of all.values()){if(pos.has(item.id))continue;const a=2*Math.PI*f++/Math.max(1,all.size);pos.set(item.id,{x:300*Math.cos(a),y:300*Math.sin(a),w:item.roles?relationWidth(item):nodeWidth(item),h:50,kind:item.roles?'relation':'node'});}
    const bounds=layoutBounds(pos,90);return{mode:'radial',positions:pos,width:bounds.width,height:bounds.height,offsetX:bounds.offsetX,offsetY:bounds.offsetY,domains,sector,maxR};
  }

  function nodeWidth(n){ const label=n?.label||n?.id||''; return Math.max(100,Math.min(210,62+label.length*5.1)); }
  function relationWidth(e){ const label=labelOf(e?.type); return Math.max(84,Math.min(145,56+label.length*4.5)); }
  function layoutBounds(pos,pad=50){ let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity; for(const p of pos.values()){ minX=Math.min(minX,p.x-p.w/2);maxX=Math.max(maxX,p.x+p.w/2);minY=Math.min(minY,p.y-p.h/2);maxY=Math.max(maxY,p.y+p.h/2); } return {width:maxX-minX+2*pad,height:maxY-minY+2*pad,offsetX:-minX+pad,offsetY:-minY+pad}; }

  function internalId(kind,id){return `${kind}|${id}`;}
  function buildElkGraph(view){
    const all=new Map();view.nodes.forEach(n=>all.set(n.id,n));view.hyperedges.forEach(e=>all.set(e.id,e));const children=[];
    for(const n of view.nodes) children.push({id:internalId('n',n.id),width:nodeWidth(n),height:58,layoutOptions:{'elk.partitioning.partition':rank(n)}});
    for(const e of view.hyperedges) children.push({id:internalId('r',e.id),width:relationWidth(e),height:52,layoutOptions:{'elk.partitioning.partition':rank(e)}});
    const present=new Set(children.map(x=>x.id)),edges=[];let no=0;const edgeMeta=new Map();
    function add(a,b,meta){if(!present.has(a)||!present.has(b)||a===b)return;const id=`elk-edge-${no++}`;edges.push({id,sources:[a],targets:[b]});edgeMeta.set(id,meta);}
    for(const e of view.hyperedges){const rid=internalId('r',e.id);add(internalId('n',e.type),rid,{kind:'type',label:'type',relation:e.id,participant:e.type});for(const [role,p] of Object.entries(e.roles||{})){const part=all.get(p);if(!part)continue;const pid=internalId(view.hyperedges.some(x=>x.id===p)?'r':'n',p);const pr=rank(part),rr=rank(e),forward=pr<rr||(pr===rr&&p.localeCompare(e.id)<0);add(forward?pid:rid,forward?rid:pid,{kind:'role',label:role,relation:e.id,participant:p});}}
    return {graph:{id:'root',layoutOptions:{'elk.algorithm':'layered','elk.direction':'RIGHT','elk.edgeRouting':'ORTHOGONAL','elk.partitioning.activate':true,'elk.spacing.nodeNode':46,'elk.spacing.edgeNode':26,'elk.spacing.edgeEdge':16,'elk.layered.spacing.nodeNodeBetweenLayers':120,'elk.layered.crossingMinimization.strategy':'LAYER_SWEEP','elk.layered.crossingMinimization.greedySwitch.type':'TWO_SIDED','elk.layered.nodePlacement.strategy':'BRANDES_KOEPF','elk.layered.nodePlacement.favorStraightEdges':true,'elk.padding':'[top=42,left=42,bottom=42,right=42]'},children,edges},edgeMeta};
  }

  async function elkLayout(view){ if(!elk) throw new Error('ELK unavailable'); const built=buildElkGraph(view),g=await elk.layout(built.graph);const pos=new Map();for(const ch of g.children||[]){const isRel=ch.id.startsWith('r|'),id=ch.id.slice(2);pos.set(id,{x:(ch.x||0)+(ch.width||100)/2,y:(ch.y||0)+(ch.height||50)/2,w:ch.width||100,h:ch.height||50,kind:isRel?'relation':'node'});}return {mode:'elk',positions:pos,width:g.width||1,height:g.height||1,offsetX:0,offsetY:0,elkGraph:g,edgeMeta:built.edgeMeta}; }

  async function relayout(fitAfter=false){ if(!state.data.nodes.length)return;showLoading(true,'Computing layout…');const started=performance.now();try{const view=projection();state.visible=view;state.layout=els.layoutMode.value==='elk'?await elkLayout(view):semanticRadialLayout(view);render();if(fitAfter)fitGraph();els.status.textContent=`${view.nodes.length} elements · ${view.hyperedges.length} hyperrelations · ${state.layout.mode} ${Math.round(performance.now()-started)} ms`;}catch(err){console.error(err);els.status.textContent=`Layout failed: ${err.message}`;}finally{showLoading(false);} }

  function render(){ const svg=els.graph;svg.innerHTML='';const root=document.createElementNS(NS,'g');root.id='viewport';root.setAttribute('transform',transformString());svg.appendChild(root);if(!state.layout)return;const edgeGroup=document.createElementNS(NS,'g'),labelGroup=document.createElementNS(NS,'g'),nodeGroup=document.createElementNS(NS,'g');root.append(edgeGroup,labelGroup,nodeGroup);if(state.layout.mode==='elk')renderElkEdges(edgeGroup,labelGroup);else renderRadialEdges(edgeGroup,labelGroup);renderNodes(nodeGroup);if(state.layout.mode==='radial')renderDomainLabels(root);applySearch();updateRoleLabelVisibility(); }
  function toCanvas(p){return{x:p.x+state.layout.offsetX,y:p.y+state.layout.offsetY};}
  function renderRadialEdges(edgeGroup,labelGroup){const pos=state.layout.positions;for(const e of state.visible.hyperedges){const rp=pos.get(e.id);if(!rp)continue;const a=toCanvas(rp),tp=pos.get(e.type);if(tp){const b=toCanvas(tp);drawCurve(edgeGroup,a,b,'type-edge',sourceColor(e.source),.28);}for(const [role,pid] of Object.entries(e.roles||{})){const pp=pos.get(pid);if(!pp)continue;const b=toCanvas(pp);drawCurve(edgeGroup,a,b,'edge','#758395',.62);drawRoleLabel(labelGroup,a,b,role,e.id,pid);}}}
  function drawCurve(group,a,b,cls,color,opacity){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy)||1,mx=(a.x+b.x)/2,my=(a.y+b.y)/2,sign=hash01(`${a.x},${a.y},${b.x},${b.y}`)>.5?1:-1,curv=Math.min(42,L*.08)*sign,cx=mx-dy/L*curv,cy=my+dx/L*curv;const path=document.createElementNS(NS,'path');path.setAttribute('d',`M ${a.x} ${a.y} Q ${cx} ${cy} ${b.x} ${b.y}`);path.setAttribute('class',`edge ${cls}`);path.style.stroke=color;path.style.opacity=opacity;group.appendChild(path);}
  function drawRoleLabel(group,a,b,role,relation,participant){const t=document.createElementNS(NS,'text');t.setAttribute('x',(a.x+b.x)/2);t.setAttribute('y',(a.y+b.y)/2-4);t.setAttribute('text-anchor','middle');t.setAttribute('class','role-label');t.dataset.relation=relation;t.dataset.search=`${role} ${relation} ${participant}`.toLowerCase();t.textContent=role;group.appendChild(t);}
  function hash01(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return((h>>>0)%1000)/1000;}
  function renderElkEdges(edgeGroup,labelGroup){const g=state.layout.elkGraph;for(const edge of g.edges||[]){const meta=state.layout.edgeMeta.get(edge.id)||{kind:'role',label:''};for(const section of edge.sections||[]){const pts=[section.startPoint,...(section.bendPoints||[]),section.endPoint].filter(Boolean);if(pts.length<2)continue;const path=document.createElementNS(NS,'path');path.setAttribute('d',`M ${pts.map(p=>`${p.x} ${p.y}`).join(' L ')}`);path.setAttribute('class',`edge ${meta.kind==='type'?'type-edge':''}`);edgeGroup.appendChild(path);const mid=polylineMidpoint(pts),t=document.createElementNS(NS,'text');t.setAttribute('x',mid.x);t.setAttribute('y',mid.y-4);t.setAttribute('text-anchor','middle');t.setAttribute('class','role-label');t.dataset.relation=meta.relation;t.dataset.search=`${meta.label} ${meta.relation} ${meta.participant}`.toLowerCase();t.textContent=meta.label;labelGroup.appendChild(t);}}}
  function renderNodes(group){const pos=state.layout.positions,visibleIndex=new Map();state.visible.nodes.forEach(n=>visibleIndex.set(n.id,n));state.visible.hyperedges.forEach(e=>visibleIndex.set(e.id,e));for(const [id,p0] of pos){const item=visibleIndex.get(id);if(!item)continue;const p=toCanvas(p0),isRelation=!!item.roles,g=document.createElementNS(NS,'g');g.setAttribute('class',`${isRelation?'relation':'node'} ${state.selected===id?'selected':''}`);g.setAttribute('transform',`translate(${p.x-p0.w/2} ${p.y-p0.h/2})`);g.dataset.id=id;g.dataset.search=searchable(item).toLowerCase();g.style.cursor='pointer';g.addEventListener('click',ev=>{ev.stopPropagation();selectItem(id);});const color=COLORS[item.layer]||sourceColor(item.source);if(isRelation){const poly=document.createElementNS(NS,'polygon');poly.setAttribute('points',`${p0.w/2},0 ${p0.w},${p0.h/2} ${p0.w/2},${p0.h} 0,${p0.h/2}`);poly.setAttribute('fill',color);poly.setAttribute('fill-opacity','.14');poly.setAttribute('stroke',color);poly.setAttribute('class','relation-shape');g.appendChild(poly);}else{const rect=document.createElementNS(NS,'rect');rect.setAttribute('width',p0.w);rect.setAttribute('height',p0.h);rect.setAttribute('rx',item.kind==='type'||item.kind==='relationType'?22:9);rect.setAttribute('fill',color);rect.setAttribute('fill-opacity','.14');rect.setAttribute('stroke',color);rect.setAttribute('class','node-shape');g.appendChild(rect);}const title=document.createElementNS(NS,'text');title.setAttribute('x',p0.w/2);title.setAttribute('y',p0.h/2-1);title.setAttribute('text-anchor','middle');title.setAttribute('class','node-label');title.textContent=truncate(isRelation?labelOf(item.type):(item.label||item.id),28);g.appendChild(title);const sub=document.createElementNS(NS,'text');sub.setAttribute('x',p0.w/2);sub.setAttribute('y',p0.h/2+13);sub.setAttribute('text-anchor','middle');sub.setAttribute('class','node-sub');sub.textContent=isRelation?truncate(item.originalId||item.id,24):truncate(item.kind||item.layer||'',22);g.appendChild(sub);group.appendChild(g);}}
  function renderDomainLabels(root){const layout=state.layout;if(!layout.domains?.length)return;const r=layout.maxR+70;for(const d of layout.domains){const a=layout.sector.get(d),p=toCanvas({x:r*Math.cos(a),y:r*Math.sin(a)}),t=document.createElementNS(NS,'text');t.setAttribute('x',p.x);t.setAttribute('y',p.y);t.setAttribute('text-anchor','middle');t.setAttribute('class','domain-label');t.style.fill=sourceColor(d);t.textContent=(state.sourceNames.get(d)||d).toUpperCase();root.appendChild(t);}}
  function searchable(item){return[item.id,item.originalId,item.label,item.kind,item.layer,item.source,item.type,...Object.keys(item.roles||{}),...Object.values(item.roles||{})].filter(Boolean).join(' ');}
  function polylineMidpoint(points){let total=0,lengths=[];for(let i=1;i<points.length;i++){const d=Math.hypot(points[i].x-points[i-1].x,points[i].y-points[i-1].y);lengths.push(d);total+=d;}let target=total/2;for(let i=0;i<lengths.length;i++){if(target<=lengths[i]){const a=points[i],b=points[i+1],t=lengths[i]?target/lengths[i]:0;return{x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t};}target-=lengths[i];}return points[Math.floor(points.length/2)];}
  function selectItem(id){state.selected=id;const item=index().get(id);if(!item)return;const relation=state.data.hyperedges.find(x=>x.id===id);els.selTitle.textContent=item.label||(relation?labelOf(relation.type):id);els.selMeta.textContent=`${relation?'n-ary relation':item.kind||'element'} · ${item.layer||'unlayered'} · ${item.source||''}`;if(relation){els.selDesc.textContent='First-class hyperrelation. Relation type and every role binding are explicit; this relation may itself participate in another relation.';els.roles.innerHTML=`<div class="role"><div class="roleName">relation type</div><div>${escapeHtml(labelOf(relation.type))}</div></div>`+Object.entries(relation.roles||{}).map(([r,p])=>`<div class="role"><div class="roleName">${escapeHtml(r)}</div><div>${escapeHtml(labelOf(p))}</div></div>`).join('');}else{const inc=state.data.hyperedges.filter(e=>e.type===id||Object.values(e.roles||{}).includes(id));els.selDesc.textContent=`Model element participating in ${inc.length} semantic relation${inc.length===1?'':'s'}.`;els.roles.innerHTML=inc.map(e=>`<div class="role"><div class="roleName">${escapeHtml(e.type===id?'type of':labelOf(e.type))}</div><div>${escapeHtml(e.originalId||e.id)}</div></div>`).join('');}render();}
  function neighborhood(id){const out=new Set([id]);for(const e of state.data.hyperedges){if(e.id===id||e.type===id||Object.values(e.roles||{}).includes(id)){out.add(e.id);out.add(e.type);Object.values(e.roles||{}).forEach(p=>out.add(p));}}const item=index().get(id);if(item?.roles){out.add(item.type);Object.values(item.roles).forEach(p=>out.add(p));}return out;}
  function applySearch(){const q=els.search.value.trim().toLowerCase(),viewport=document.getElementById('viewport');if(!viewport)return;viewport.querySelectorAll('.node,.relation,.role-label').forEach(el=>el.classList.toggle('dim',!!q&&!(el.dataset.search||'').includes(q)));}
  function updateRoleLabelVisibility(){const viewport=document.getElementById('viewport');if(!viewport)return;viewport.querySelectorAll('.role-label').forEach(el=>{const selected=state.selected&&el.dataset.relation===state.selected;el.style.display=(state.transform.k>=.78||selected)?'':'none';});}
  function transformString(){const t=state.transform;return`translate(${t.x} ${t.y}) scale(${t.k})`;}
  function updateTransform(){const v=document.getElementById('viewport');if(v){v.setAttribute('transform',transformString());updateRoleLabelVisibility();}}
  function fitGraph(){if(!state.layout)return;const w=els.stage.clientWidth,h=els.stage.clientHeight,gw=Math.max(1,state.layout.width||1),gh=Math.max(1,state.layout.height||1),k=Math.max(.08,Math.min(1.45,Math.min((w-50)/gw,(h-50)/gh)));state.transform={x:(w-gw*k)/2,y:(h-gh*k)/2,k};updateTransform();}
  function showLoading(on,text='Laying out graph…'){els.loading.textContent=text;els.loading.style.display=on?'block':'none';}

  els.fixture.addEventListener('change',()=>loadPreset(els.fixture.value));els.layer.addEventListener('change',()=>relayout(true));els.relationType.addEventListener('change',()=>relayout(true));els.layoutMode.addEventListener('change',()=>relayout(true));els.search.addEventListener('input',applySearch);els.relayout.addEventListener('click',()=>relayout(true));els.fit.addEventListener('click',fitGraph);els.focus.addEventListener('click',async()=>{if(state.focusSet){state.focusSet=null;els.focus.textContent='Focus neighborhood';await relayout(true);return;}if(!state.selected){els.status.textContent='Select a node or relation first';return;}state.focusSet=neighborhood(state.selected);els.focus.textContent='Clear focus';await relayout(true);});els.file.addEventListener('change',async()=>{if(els.file.files?.length)await loadFiles([...els.file.files]);});
  els.graph.addEventListener('click',()=>{state.selected=null;render();});els.graph.addEventListener('wheel',ev=>{ev.preventDefault();const rect=els.graph.getBoundingClientRect(),mx=ev.clientX-rect.left,my=ev.clientY-rect.top,old=state.transform.k,next=Math.max(.08,Math.min(4,old*(ev.deltaY<0?1.12:.89))),gx=(mx-state.transform.x)/old,gy=(my-state.transform.y)/old;state.transform.x=mx-gx*next;state.transform.y=my-gy*next;state.transform.k=next;updateTransform();},{passive:false});els.graph.addEventListener('pointerdown',ev=>{if(ev.target.closest('.node,.relation'))return;state.panning={x:ev.clientX,y:ev.clientY,tx:state.transform.x,ty:state.transform.y};els.graph.setPointerCapture(ev.pointerId);});els.graph.addEventListener('pointermove',ev=>{if(!state.panning)return;state.transform.x=state.panning.tx+ev.clientX-state.panning.x;state.transform.y=state.panning.ty+ev.clientY-state.panning.y;updateTransform();});els.graph.addEventListener('pointerup',()=>state.panning=null);window.addEventListener('resize',fitGraph);

  loadPreset('all');
})();