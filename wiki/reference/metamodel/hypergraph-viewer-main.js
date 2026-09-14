(() => {
'use strict';
const HV=window.HV,E=HV.els,S=HV.state;
HV.syncProjectionControls = () => {const named=(E.projection?.value||'all')!=='all';E.layer.disabled=named;E.relationType.disabled=named;if(named){E.layer.value='all';E.relationType.value='all';}};
E.fixture.addEventListener('change',()=>HV.loadPreset(E.fixture.value));
E.projection?.addEventListener('change',async()=>{S.focus=null;HV.syncProjectionControls();await HV.relayout(true);});
E.layer.addEventListener('change',()=>HV.relayout(true));E.relationType.addEventListener('change',()=>HV.relayout(true));E.search.addEventListener('input',HV.applySearch);E.relayout.addEventListener('click',()=>HV.relayout(true));E.fit.addEventListener('click',HV.fitGraph);
E.focus.addEventListener('click',async()=>{if(S.focus){S.focus=null;E.focus.textContent='Focus neighborhood';await HV.relayout(true);return;}if(!S.selected){E.status.textContent='Select a node or relation first';return;}S.focus=HV.neighborhood(S.selected);E.focus.textContent='Clear focus';await HV.relayout(true);});
E.graph.addEventListener('click',()=>{S.selected=null;HV.render();});
E.graph.addEventListener('wheel',ev=>{ev.preventDefault();const rect=E.graph.getBoundingClientRect(),mx=ev.clientX-rect.left,my=ev.clientY-rect.top,old=S.transform.k,next=Math.max(.08,Math.min(4,old*(ev.deltaY<0?1.12:.89))),gx=(mx-S.transform.x)/old,gy=(my-S.transform.y)/old;S.transform.x=mx-gx*next;S.transform.y=my-gy*next;S.transform.k=next;HV.updateTransform();},{passive:false});
E.graph.addEventListener('pointerdown',ev=>{if(ev.target.closest('.node,.relation'))return;S.pan={x:ev.clientX,y:ev.clientY,tx:S.transform.x,ty:S.transform.y};E.graph.setPointerCapture(ev.pointerId);});E.graph.addEventListener('pointermove',ev=>{if(!S.pan)return;S.transform.x=S.pan.tx+ev.clientX-S.pan.x;S.transform.y=S.pan.ty+ev.clientY-S.pan.y;HV.updateTransform();});E.graph.addEventListener('pointerup',()=>{S.pan=null;});window.addEventListener('resize',HV.fitGraph);
HV.syncProjectionControls();HV.loadPreset('all');
})();
