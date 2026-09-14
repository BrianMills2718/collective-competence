(() => {
'use strict';
const HV=window.HV;
HV.selectItem=id=>{
  const S=HV.state,E=HV.els;S.selected=id;
  const item=HV.index().get(id),relation=S.data.hyperedges.find(e=>e.id===id);if(!item)return;
  E.selTitle.textContent=item.label||(relation?HV.labelOf(relation.type):id);
  E.selMeta.textContent=`${relation?'n-ary relation':item.kind||'element'} · ${item.layer||''} · ${item.source||''}${relation?` · ${relation.sourceModel}`:''}`;
  if(relation){
    E.selDesc.textContent='First-class n-ary relation with typed incidence bindings. Each binding resolves to a RoleType; ID-bearing bindings are themselves addressable ModelElements.';
    const header=`<div class="role"><div class="roleName">relation type</div><div>${HV.escapeHtml(HV.labelOf(relation.type))}<br><span class="small">${HV.escapeHtml(relation.type)}</span></div></div>`;
    const rows=(relation.bindings||[]).map(b=>{
      const label=HV.roleLabel(b.role)+(b.qualifier?`:${b.qualifier}`:'');
      const bindingId=b.id?`<br><span class="small">binding ${HV.escapeHtml(b.id)}</span>`:'';
      return `<div class="role"><div class="roleName">${HV.escapeHtml(label)}<br><span class="small">${HV.escapeHtml(b.role)}</span>${bindingId}</div><div>${HV.escapeHtml(HV.labelOf(b.participant))}</div></div>`;
    }).join('');
    E.roles.innerHTML=header+rows;
  }else if(item.kind==='roleBinding'){
    const inbound=S.data.hyperedges.filter(e=>(e.bindings||[]).some(b=>b.participant===id));
    E.selDesc.textContent='Addressable RoleBinding: one specific participant-to-role assignment in a parent relation. Scientific claims, evidence, provenance, or uncertainty may target this binding without reidentifying the whole relation.';
    const rows=[
      ['parent relation',HV.labelOf(item.parentRelation),item.parentRelation],
      ['role type',HV.roleLabel(item.role),item.role],
      ...(item.qualifier?[['qualifier',item.qualifier,null]]:[]),
      ['participant',HV.labelOf(item.boundParticipant),item.boundParticipant],
      ...inbound.map(e=>['targeted by',HV.labelOf(e.type),e.originalId||e.id]),
    ];
    E.roles.innerHTML=rows.map(([name,label,sub])=>`<div class="role"><div class="roleName">${HV.escapeHtml(name)}</div><div>${HV.escapeHtml(label)}${sub?`<br><span class="small">${HV.escapeHtml(sub)}</span>`:''}</div></div>`).join('');
  }else{
    const incident=S.data.hyperedges.filter(e=>e.type===id||(e.bindings||[]).some(b=>b.participant===id));
    E.selDesc.textContent=`Model element participating in ${incident.length} semantic relation${incident.length===1?'':'s'}.`;
    E.roles.innerHTML=incident.map(e=>`<div class="role"><div class="roleName">${HV.escapeHtml(e.type===id?'type of':HV.labelOf(e.type))}</div><div>${HV.escapeHtml(e.originalId||e.id)}</div></div>`).join('');
  }
  HV.render();
};
})();
