(() => {
'use strict';
const HV=window.HV;
const baseEnsure=HV.ensureRoleContracts;
const baseMerge=HV.mergeDocuments;
HV.semanticProfileGraph=null;
HV.semanticKindMap=new Map();
HV.importNodeRegistry=new Map();
HV.typeIndex=new Map();
HV.SEMANTIC_PROFILE='scientific-semantic-types-v2-probe.json';

const slugify=s=>String(s).replace(/[^A-Za-z0-9_.-]+/g,'_').replace(/^_+|_+$/g,'')||'x';
const typeList=v=>v==null?[]:(Array.isArray(v)?v:[v]);
HV.semanticTypeForKind=kind=>HV.semanticKindMap.get(kind)||`sci:AuthoringCategory_${slugify(kind)}`;
HV.isTypingEdge=e=>!!e?.normalizationGenerated&&e.type==='sci:instanceOf';
HV.semanticTypesOf=id=>HV.typeIndex.get(id)||new Set();
HV.canonicalRelationType=id=>HV.contractIndex?.relationAliases.get(id)||id;
HV.hasType=(id,type)=>HV.semanticTypesOf(id).has(type);
HV.primarySemanticType=id=>{
  const xs=[...HV.semanticTypesOf(id)].filter(x=>x!=='sci:ModelElement');
  const preferred=xs.find(x=>!['sci:RelationInstance','sci:RoleBinding'].includes(x));
  return preferred||xs[0]||'sci:ModelElement';
};
HV.displayCategory=item=>{
  if(item?.structuralKind==='roleBinding')return 'RoleBinding';
  return HV.labelOf(HV.primarySemanticType(item?.id));
};

HV.ensureRoleContracts=async()=>{
  await baseEnsure();
  if(HV.semanticProfileGraph)return;
  HV.semanticProfileGraph=await HV.fetchJson(HV.SEMANTIC_PROFILE);
  for(const n of HV.semanticProfileGraph.nodes||[]){
    if(n.authoringKind)HV.semanticKindMap.set(n.authoringKind,n.id);
    HV.importNodeRegistry.set(n.id,n);
  }
  for(const n of HV.roleSchemaGraph?.nodes||[])HV.importNodeRegistry.set(n.id,n);
};

const bindingParticipants=(edge,role)=>(edge.bindings||[]).filter(b=>b.role===role).map(b=>b.participant);
const existingPairs=doc=>{
  const out=new Set();
  for(const e of doc.hyperedges||[]){
    if(!['sci:instanceOf','meta:instanceOf'].includes(e.type))continue;
    const bs=e.bindings||[];
    const is=bindingParticipants({bindings:bs},'sci:instance').concat(bindingParticipants({bindings:bs},'instance'));
    const ts=bindingParticipants({bindings:bs},'sci:type').concat(bindingParticipants({bindings:bs},'type'));
    for(const i of is)for(const t of ts)out.add(`${i}\u0000${t}`);
  }
  return out;
};

HV.normalizeDocument=(slug,doc)=>{
  const shared=n=>HV.isSharedNode(n);
  const nm=new Map((doc.nodes||[]).map(n=>[n.id,shared(n)?n.id:`${slug}::${n.id}`]));
  const em=new Map();
  for(const e of doc.hyperedges||[]){
    let sh=['metamodel','schema'].includes(e.layer);
    if(sh){for(const p of HV.fetchParticipants(e)){if(nm.has(p)&&nm.get(p)!==p){sh=false;break;}}}
    em.set(e.id,sh?e.id:`${slug}::${e.id}`);
  }
  const bm=new Map();
  for(const e of doc.hyperedges||[])for(const b of e.bindings||[])if(b?.id)bm.set(b.id,em.get(e.id)===e.id?b.id:`${slug}::${b.id}`);

  const labelMap=new Map();
  for(const n of doc.nodes||[])labelMap.set(n.id,n.label||n.id);
  for(const e of doc.hyperedges||[])labelMap.set(e.id,e.label||e.type||e.id);
  const nodes=[];
  const bindingNodes=[];
  for(const n of doc.nodes||[]){
    const semanticHints=['sci:ModelElement',...typeList(n.type)];
    if(n.kind&&n.kind!=='element')semanticHints.push(HV.semanticTypeForKind(n.kind));
    const x={...n,id:nm.get(n.id),originalId:n.id,source:shared(n)?'shared':slug,displayKind:n.kind||null,semanticTypeHints:[...new Set(semanticHints)]};
    delete x.kind;delete x.type;nodes.push(x);
  }
  const hyperedges=[];
  for(const e of doc.hyperedges||[]){
    const raw=e.bindings||Object.entries(e.roles||{}).map(([key,p])=>HV.resolveV0Binding(e.type,key,p));
    const normalizedId=em.get(e.id),source=['metamodel','schema'].includes(e.layer)&&normalizedId===e.id?'shared':slug;
    const bindings=raw.map(b=>{
      const participant=bm.get(b.participant)||em.get(b.participant)||nm.get(b.participant)||b.participant;
      const id=b.id?(bm.get(b.id)||b.id):undefined;
      const x=id?{...b,id,participant}:{...b,participant};
      if(id){
        const roleText=HV.roleLabel(b.role)+(b.qualifier?`:${b.qualifier}`:'');
        bindingNodes.push({id,originalId:b.id,label:`${roleText} → ${labelMap.get(b.participant)||b.participant}`,layer:e.layer||'study',source,structuralKind:'roleBinding',parentRelation:normalizedId,role:b.role,qualifier:b.qualifier||null,boundParticipant:participant,semanticTypeHints:['sci:ModelElement','sci:RoleBinding']});
      }
      return x;
    });
    hyperedges.push({...e,id:normalizedId,originalId:e.id,type:nm.get(e.type)||e.type,bindings,roles:HV.displayRoles(bindings),source,sourceModel:doc.model||'scientific-hypergraph-v0'});
  }

  const pairs=existingPairs(doc),generatedTypeNodes=[];
  for(const raw of doc.nodes||[]){
    const instance=nm.get(raw.id),sem=[];
    for(const t of typeList(raw.type))sem.push(nm.get(t)||t);
    if(raw.kind&&raw.kind!=='element')sem.push(HV.semanticTypeForKind(raw.kind));
    for(const typeId of [...new Set(sem)]){
      if(pairs.has(`${raw.id}\u0000${typeId}`)||pairs.has(`${raw.id}\u0000${raw.type}`))continue;
      if(!nm.has(typeId)&&!HV.importNodeRegistry.has(typeId)&&!generatedTypeNodes.some(n=>n.id===typeId))generatedTypeNodes.push({id:typeId,label:typeId.split(':').pop(),layer:'schema',source:slug,generatedSemanticType:true,semanticTypeHints:['sci:ModelElement','sci:ElementType']});
      const relSource=shared(raw)?'shared':slug;
      const base=`norm:instanceOf:${slugify(raw.id)}:${slugify(typeId)}`;
      const id=relSource==='shared'?base:`${slug}::${base}`;
      const bindings=[{role:'sci:instance',participant:instance},{role:'sci:type',participant:typeId}];
      hyperedges.push({id,originalId:base,type:'sci:instanceOf',layer:raw.layer||'study',source:relSource,sourceModel:'graph-native-typing-v2',bindings,roles:HV.displayRoles(bindings),normalizationGenerated:true});
    }
  }
  return {nodes:[...nodes,...bindingNodes,...generatedTypeNodes],hyperedges};
};

HV.rebuildTypeIndex=data=>{
  const idx=new Map(),add=(id,t)=>{if(!idx.has(id))idx.set(id,new Set());idx.get(id).add(t);};
  for(const n of data.nodes||[]){add(n.id,'sci:ModelElement');for(const t of n.semanticTypeHints||[])add(n.id,t);if(n.structuralKind==='roleBinding')add(n.id,'sci:RoleBinding');}
  for(const e of data.hyperedges||[]){add(e.id,'sci:ModelElement');add(e.id,'sci:RelationInstance');}
  for(const e of data.hyperedges||[]){if(!['sci:instanceOf','meta:instanceOf'].includes(e.type))continue;const ins=(e.bindings||[]).filter(b=>['sci:instance','instance'].includes(b.role)).map(b=>b.participant),ts=(e.bindings||[]).filter(b=>['sci:type','type'].includes(b.role)).map(b=>b.participant);for(const i of ins)for(const t of ts)add(i,t);}
  HV.typeIndex=idx;return idx;
};

HV.mergeDocuments=entries=>{
  const merged=baseMerge(entries),ids=new Set([...merged.nodes.map(n=>n.id),...merged.hyperedges.map(e=>e.id)]),refs=new Set();
  for(const e of merged.hyperedges){refs.add(e.type);for(const b of e.bindings||[])refs.add(b.participant);}
  for(const id of refs){if(ids.has(id))continue;const raw=HV.importNodeRegistry.get(id);if(!raw)continue;const hints=['sci:ModelElement',...typeList(raw.type)];if(raw.kind&&raw.kind!=='element')hints.push(HV.semanticTypeForKind(raw.kind));merged.nodes.push({...raw,id:raw.id,originalId:raw.id,source:'shared',displayKind:raw.kind||null,semanticTypeHints:[...new Set(hints)],importedForNormalization:true,kind:undefined,type:undefined});ids.add(id);}
  HV.rebuildTypeIndex(merged);return merged;
};

HV.RELATION_PROJECTIONS={
  measurement:new Set(['sci:MeasurementRelation','sci:QuantityValueRelation','sci:AnalysisRelation']),
  probability:new Set(['sci:DistributionRelation']),representation:new Set(['sci:RepresentationRelation']),
  access:new Set(['sci:AccessRelation']),identifiability:new Set(['sci:IdentifiabilityRelation']),
  typing:new Set(['sci:instanceOf','sci:specializes']),
};
})();
