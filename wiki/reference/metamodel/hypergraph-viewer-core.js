(() => {
'use strict';
const HV = window.HV = window.HV || {};
HV.FIXTURES = {
  cc:'c2-q1-hypergraph-v0.json',
  mechanics:'classical-mechanics-hypergraph.json',
  oscillator:'harmonic-oscillator-hypergraph.json',
  reaction:'first-order-reaction-hypergraph.json',
  stochastic:'ornstein-uhlenbeck-hypergraph.json',
  heat:'heat-equation-hypergraph.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph.json',
  calibration:'calibration-covariance-hypergraph.json',
};
HV.SOURCE_LABEL = {
  cc:'Collective Competence', mechanics:'Classical mechanics', oscillator:'Harmonic oscillator', reaction:'Reaction kinetics',
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
HV.state = {data:{nodes:[],hyperedges:[]},view:null,layout:null,selected:null,focus:null,transform:{x:0,y:0,k:1},pan:null,names:new Map([['shared','Shared kernel / schema']])};
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
HV.normalizeDocument = (slug,doc) => {
  const nm=new Map((doc.nodes||[]).map(n=>[n.id,HV.isSharedNode(n)?n.id:`${slug}::${n.id}`]));
  const em=new Map();
  for(const e of doc.hyperedges||[]){let shared=['metamodel','schema'].includes(e.layer);if(shared){for(const p of Object.values(e.roles||{})){if(nm.has(p)&&nm.get(p)!==p){shared=false;break;}}}em.set(e.id,shared?e.id:`${slug}::${e.id}`);}
  return {
    nodes:(doc.nodes||[]).map(n=>({...n,id:nm.get(n.id),originalId:n.id,source:HV.isSharedNode(n)?'shared':slug})),
    hyperedges:(doc.hyperedges||[]).map(e=>({...e,id:em.get(e.id),originalId:e.id,type:nm.get(e.type)||e.type,roles:Object.fromEntries(Object.entries(e.roles||{}).map(([r,p])=>[r,em.get(p)||nm.get(p)||p])),source:['metamodel','schema'].includes(e.layer)&&em.get(e.id)===e.id?'shared':slug})),
  };
};
HV.sharedEdgeKey = e => `${e.type}|${JSON.stringify(Object.entries(e.roles||{}).sort(([a],[b])=>a.localeCompare(b)))}`;
HV.mergeDocuments = entries => {
  const nm=new Map(),pending=[],canon=new Map(),alias=new Map();
  for(const {slug,doc} of entries){HV.state.names.set(slug,HV.SOURCE_LABEL[slug]||slug);const d=HV.normalizeDocument(slug,doc);for(const n of d.nodes)if(!nm.has(n.id))nm.set(n.id,n);for(const e of d.hyperedges){if(e.source==='shared'){const k=HV.sharedEdgeKey(e);if(canon.has(k)){alias.set(e.id,canon.get(k).id);continue;}canon.set(k,e);}pending.push(e);}}
  const edges=new Map();for(const e of pending){const x={...e,id:alias.get(e.id)||e.id,roles:Object.fromEntries(Object.entries(e.roles||{}).map(([r,p])=>[r,alias.get(p)||p]))};if(!edges.has(x.id))edges.set(x.id,x);}
  return {nodes:[...nm.values()],hyperedges:[...edges.values()]};
};
HV.populateRelationTypes = () => {const old=HV.els.relationType.value,types=[...new Set(HV.state.data.hyperedges.map(e=>e.type))].sort((a,b)=>HV.labelOf(a).localeCompare(HV.labelOf(b)));HV.els.relationType.innerHTML='<option value="all">All relation types</option>'+types.map(t=>`<option value="${HV.escapeHtml(t)}">${HV.escapeHtml(HV.labelOf(t))}</option>`).join('');if(types.includes(old))HV.els.relationType.value=old;};
HV.showLoading = (on,text='Laying out graph…') => {HV.els.loading.textContent=text;HV.els.loading.style.display=on?'block':'none';};
HV.loadPreset = async key => {HV.showLoading(true,'Loading fixtures…');try{HV.state.names=new Map([['shared','Shared kernel / schema']]);const keys=key==='all'?Object.keys(HV.FIXTURES):[key];const entries=await Promise.all(keys.map(async slug=>({slug,doc:await HV.fetchJson(HV.FIXTURES[slug])})));HV.state.data=HV.mergeDocuments(entries);HV.state.selected=null;HV.state.focus=null;HV.populateRelationTypes();await HV.relayout(true);}catch(error){console.error(error);HV.els.status.textContent=`Load failed: ${error.message}`;HV.showLoading(false);}};
})();
