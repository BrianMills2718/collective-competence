(() => {
'use strict';
const HV = window.HV = window.HV || {};
HV.FIXTURES = {
  roleSchema:'scientific-role-schema-v1.json',
  cc:'c2-q1-hypergraph-v0.json',
  mechanics:'classical-mechanics-hypergraph-v1.json',
  oscillator:'harmonic-oscillator-hypergraph.json',
  reaction:'first-order-reaction-hypergraph.json',
  stochastic:'ornstein-uhlenbeck-hypergraph.json',
  heat:'heat-equation-hypergraph.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph.json',
  calibration:'calibration-covariance-hypergraph.json',
};
HV.AGGREGATE_FIXTURES = ['cc','mechanics','oscillator','reaction','stochastic','heat','multiscale','calibration'];
HV.SOURCE_LABEL = {
  roleSchema:'Scientific relation / role metamodel',
  cc:'Collective Competence', mechanics:'Classical mechanics (typed-role v1)', oscillator:'Harmonic oscillator', reaction:'Reaction kinetics',
  stochastic:'Ornstein-Uhlenbeck stochastic process', heat:'Heat-equation PDE',
  multiscale:'Random walk -> diffusion multiscale', calibration:'Correlated calibration uncertainty'
};
HV.COLORS = {metamodel:'#58a6ff',schema:'#c297ff',theory:'#66d48f',study:'#f1a65a',evidence:'#ff7b72',edge:'#758395'};
HV.DOMAIN_COLORS = ['#64d58f','#54c7ec','#f1a65a','#f778ba','#a78bfa','#2dd4bf','#fb7185','#facc15','#60a5fa','#34d399'];
HV.NS = 'http://www.w3.org/2000/svg';
HV.RELATION_PROJECTIONS = {
  measurement:new Set(['schema:Measurement','schema:QuantityValue','schema:Analysis']),
  probability:new Set(['schema:Distribution']),
  representation:new Set(['schema:Representation']),
  access:new Set(['schema:StudyView']),
  identifiability:new Set(['schema:Identifiability']),
};
HV.q = id => document.getElementById(id);
HV.els = Object.fromEntries(['fixture','projection','layer','relationType','search','relayout','fit','focus','status','graph','stage','loading','selTitle','selMeta','selDesc','roles'].map(id=>[id,HV.q(id)]));
HV.state = {data:{nodes:[],hyperedges:[]},view:null,layout:null,selected:null,focus:null,transform:{x:0,y:0,k:1},pan:null,names:new Map([['shared','Shared kernel / schema']]),preset:'all'};
HV.roleContracts = null;
HV.roleSchemaGraph = null;
HV.contractIndex = null;
HV.isSharedNode = n => ['metamodel','schema'].includes(n.layer);
HV.nodeWidth = n => Math.max(104,Math.min(210,64+String(n.label||n.id).length*5));
HV.nodeHeight = 52; HV.relationHeight = 48;
HV.index = () => {const m=new Map();HV.state.data.nodes.forEach(x=>m.set(x.id,x));HV.state.data.hyperedges.forEach(x=>m.set(x.id,x));return m;};
HV.labelOf = id => {const x=HV.index().get(id);return x?.label||x?.type||id;};
HV.relationWidth = e => Math.max(92,Math.min(152,60+String(HV.labelOf(e.type)).length*4.5));
HV.escapeHtml = s => String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
HV.truncate = (s,n=26) => {s=String(s??'');return s.length>n?`${s.slice(0,n-1)}…`:s;};
HV.colorForSource = source => {const ks=[...HV.state.names.keys()].filter(x=>x!=='shared').sort();const i=Math.max(0,ks.indexOf(source));return HV.DOMAIN_COLORS[i%HV.DOMAIN_COLORS.length];};
HV.fetchJson = async path => {const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(`${path}: HTTP ${r.status}`);return r.json();};
HV.bindingParticipants = (edge,role) => (edge.bindings||[]).filter(b=>b.role===role).map(b=>b.participant);
HV.contractsFromRoleSchemaGraph = graph => {
  const nodeMap=new Map((graph.nodes||[]).map(n=>[n.id,n]));
  const declarations=new Map();
  const one=(e,role,required=true)=>{const xs=HV.bindingParticipants(e,role);if(!xs.length&&!required)return null;if(xs.length!==1)throw new Error(`${e.id}: ${role} requires one participant`);return xs[0];};
  for(const e of graph.hyperedges||[]){
    if(e.type!=='sci:declaresRole')continue;
    const relationId=one(e,'sci:declaredRelationType'),roleId=one(e,'sci:declaredRoleType');
    if(relationId==='sci:declaresRole')continue;
    const minId=one(e,'sci:roleMinimum'),maxId=one(e,'sci:roleMaximum',false),qualId=one(e,'sci:roleQualifiable');
    if(!declarations.has(relationId))declarations.set(relationId,{aliases:nodeMap.get(relationId)?.aliases||[],roles:{}});
    const roleNode=nodeMap.get(roleId),spec={
      label:roleNode?.label||roleId,
      aliases:roleNode?.aliases||[],
      min:nodeMap.get(minId)?.value,
      max:maxId===null?null:nodeMap.get(maxId)?.value,
      qualifiable:!!nodeMap.get(qualId)?.value,
    };
    const kinds=HV.bindingParticipants(e,'sci:roleParticipantKind').map(id=>nodeMap.get(id)?.value??nodeMap.get(id)?.label??id);
    if(kinds.length)spec.participantKinds=kinds;
    declarations.get(relationId).roles[roleId]=spec;
  }
  return {version:1,description:'Generated from scientific-role-schema-v1.json',relationTypes:Object.fromEntries([...declarations].sort(([a],[b])=>a.localeCompare(b)))};
};
HV.ensureRoleContracts = async () => {
  if(HV.roleContracts) return;
  HV.roleSchemaGraph = await HV.fetchJson('scientific-role-schema-v1.json');
  HV.roleContracts = HV.contractsFromRoleSchemaGraph(HV.roleSchemaGraph);
  const relationAliases=new Map(),roleAliases=new Map(),roleSpecs=new Map();
  for(const [canonical,spec] of Object.entries(HV.roleContracts.relationTypes||{})){
    relationAliases.set(canonical,canonical);for(const a of spec.aliases||[])relationAliases.set(a,canonical);
    const rm=new Map();for(const [roleId,rs] of Object.entries(spec.roles||{})){roleSpecs.set(roleId,rs);rm.set(roleId,roleId);for(const a of rs.aliases||[])rm.set(a,roleId);}roleAliases.set(canonical,rm);
  }
  HV.contractIndex={relationAliases,roleAliases,roleSpecs};
};
HV.roleLabel = roleId => HV.contractIndex?.roleSpecs.get(roleId)?.label || roleId.replace(/^sci:/,'');
HV.splitRoleKey = key => {const i=key.indexOf(':');return i<0?[key,null]:[key.slice(0,i),key.slice(i+1)||null];};
HV.resolveV0Binding = (relationType,key,participant) => {
  const canonical=HV.contractIndex.relationAliases.get(relationType);if(!canonical)throw new Error(`No role contract for ${relationType}`);
  const [base,qualifier]=HV.splitRoleKey(key),role=HV.contractIndex.roleAliases.get(canonical)?.get(base)||HV.contractIndex.roleAliases.get(canonical)?.get(key);
  if(!role)throw new Error(`Role ${key} is not declared for ${relationType}`);
  return qualifier?{role,qualifier,participant}:{role,participant};
};
HV.displayRoles = bindings => {const roles={},counts=new Map();for(const b of bindings){const base=HV.roleLabel(b.role)+(b.qualifier?`:${b.qualifier}`:'');const n=(counts.get(base)||0)+1;counts.set(base,n);roles[n===1?base:`${base}#${n}`]=b.participant;}return roles;};
HV.fetchParticipants = edge => edge.bindings?edge.bindings.map(b=>b.participant):Object.values(edge.roles||{});
HV.normalizeDocument = (slug,doc) => {
  const nm=new Map((doc.nodes||[]).map(n=>[n.id,HV.isSharedNode(n)?n.id:`${slug}::${n.id}`]));
  const em=new Map();
  for(const e of doc.hyperedges||[]){let shared=['metamodel','schema'].includes(e.layer);if(shared){for(const p of HV.fetchParticipants(e)){if(nm.has(p)&&nm.get(p)!==p){shared=false;break;}}}em.set(e.id,shared?e.id:`${slug}::${e.id}`);}
  const nodes=(doc.nodes||[]).map(n=>({...n,id:nm.get(n.id),originalId:n.id,source:HV.isSharedNode(n)?'shared':slug}));
  const hyperedges=(doc.hyperedges||[]).map(e=>{
    const rawBindings=e.bindings||Object.entries(e.roles||{}).map(([key,p])=>HV.resolveV0Binding(e.type,key,p));
    const bindings=rawBindings.map(b=>({...b,participant:em.get(b.participant)||nm.get(b.participant)||b.participant}));
    return {...e,id:em.get(e.id),originalId:e.id,type:nm.get(e.type)||e.type,bindings,roles:HV.displayRoles(bindings),source:['metamodel','schema'].includes(e.layer)&&em.get(e.id)===e.id?'shared':slug,sourceModel:doc.model||'scientific-hypergraph-v0'};
  });
  return {nodes,hyperedges};
};
HV.sharedEdgeKey = e => `${e.type}|${JSON.stringify((e.bindings||[]).map(b=>({role:b.role,qualifier:b.qualifier||null,participant:b.participant})).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b))))}`;
HV.mergeDocuments = entries => {
  const nm=new Map(),pending=[],canon=new Map(),alias=new Map();
  for(const {slug,doc} of entries){HV.state.names.set(slug,HV.SOURCE_LABEL[slug]||slug);const d=HV.normalizeDocument(slug,doc);for(const n of d.nodes)if(!nm.has(n.id))nm.set(n.id,n);for(const e of d.hyperedges){if(e.source==='shared'){const k=HV.sharedEdgeKey(e);if(canon.has(k)){alias.set(e.id,canon.get(k).id);continue;}canon.set(k,e);}pending.push(e);}}
  const edges=new Map();for(const e of pending){const bindings=(e.bindings||[]).map(b=>({...b,participant:alias.get(b.participant)||b.participant}));const x={...e,id:alias.get(e.id)||e.id,bindings,roles:HV.displayRoles(bindings)};if(!edges.has(x.id))edges.set(x.id,x);}
  return {nodes:[...nm.values()],hyperedges:[...edges.values()]};
};
HV.populateRelationTypes = () => {const old=HV.els.relationType.value,types=[...new Set(HV.state.data.hyperedges.map(e=>e.type))].sort((a,b)=>HV.labelOf(a).localeCompare(HV.labelOf(b)));HV.els.relationType.innerHTML='<option value="all">All relation types</option>'+types.map(t=>`<option value="${HV.escapeHtml(t)}">${HV.escapeHtml(HV.labelOf(t))}</option>`).join('');if(types.includes(old))HV.els.relationType.value=old;};
HV.showLoading = (on,text='Laying out graph…') => {HV.els.loading.textContent=text;HV.els.loading.style.display=on?'block':'none';};
HV.loadPreset = async key => {HV.showLoading(true,'Loading fixtures…');try{await HV.ensureRoleContracts();HV.state.names=new Map([['shared','Shared kernel / schema']]);HV.state.preset=key;const keys=key==='all'?HV.AGGREGATE_FIXTURES:[key];const entries=await Promise.all(keys.map(async slug=>({slug,doc:slug==='roleSchema'?HV.roleSchemaGraph:await HV.fetchJson(HV.FIXTURES[slug])})));HV.state.data=HV.mergeDocuments(entries);HV.state.selected=null;HV.state.focus=null;HV.populateRelationTypes();await HV.relayout(true);}catch(error){console.error(error);HV.els.status.textContent=`Load failed: ${error.message}`;HV.showLoading(false);}};
})();
