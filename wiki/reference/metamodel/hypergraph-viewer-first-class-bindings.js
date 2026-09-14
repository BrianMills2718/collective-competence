(() => {
'use strict';
const HV=window.HV;

// Override v1 normalization so ID-bearing RoleBindings are addressable graph
// elements. Anonymous bindings remain ordinary incidence records and do not add
// visual nodes. This keeps the common view compact while allowing evidence or
// provenance relations to target one specific role assignment.
HV.normalizeDocument=(slug,doc)=>{
  const nm=new Map((doc.nodes||[]).map(n=>[n.id,HV.isSharedNode(n)?n.id:`${slug}::${n.id}`]));
  const em=new Map();
  for(const e of doc.hyperedges||[]){
    let shared=['metamodel','schema'].includes(e.layer);
    if(shared){
      for(const p of HV.fetchParticipants(e)){
        if(nm.has(p)&&nm.get(p)!==p){shared=false;break;}
      }
    }
    em.set(e.id,shared?e.id:`${slug}::${e.id}`);
  }

  // A binding inherits the fixture/shared identity scope of its parent relation.
  const bm=new Map();
  for(const e of doc.hyperedges||[]){
    for(const b of e.bindings||[]){
      if(!b?.id)continue;
      bm.set(b.id,em.get(e.id)===e.id?b.id:`${slug}::${b.id}`);
    }
  }

  const labelMap=new Map();
  for(const n of doc.nodes||[])labelMap.set(n.id,n.label||n.id);
  for(const e of doc.hyperedges||[])labelMap.set(e.id,e.label||e.type||e.id);

  const nodes=(doc.nodes||[]).map(n=>({...n,id:nm.get(n.id),originalId:n.id,source:HV.isSharedNode(n)?'shared':slug}));
  const bindingNodes=[];
  const hyperedges=(doc.hyperedges||[]).map(e=>{
    const rawBindings=e.bindings||Object.entries(e.roles||{}).map(([key,p])=>HV.resolveV0Binding(e.type,key,p));
    const normalizedId=em.get(e.id);
    const source=['metamodel','schema'].includes(e.layer)&&normalizedId===e.id?'shared':slug;
    const bindings=rawBindings.map(b=>{
      const participant=bm.get(b.participant)||em.get(b.participant)||nm.get(b.participant)||b.participant;
      const id=b.id?(bm.get(b.id)||b.id):undefined;
      const normalized=id?{...b,id,participant}:{...b,participant};
      if(id){
        const roleText=HV.roleLabel(b.role)+(b.qualifier?`:${b.qualifier}`:'');
        bindingNodes.push({
          id,
          originalId:b.id,
          label:`${roleText} → ${labelMap.get(b.participant)||b.participant}`,
          layer:e.layer||'study',
          kind:'roleBinding',
          type:'sci:RoleBinding',
          source,
          parentRelation:normalizedId,
          role:b.role,
          qualifier:b.qualifier||null,
          boundParticipant:participant,
        });
      }
      return normalized;
    });
    return {...e,id:normalizedId,originalId:e.id,type:nm.get(e.type)||e.type,bindings,roles:HV.displayRoles(bindings),source,sourceModel:doc.model||'scientific-hypergraph-v0'};
  });
  return {nodes:[...nodes,...bindingNodes],hyperedges};
};
})();
