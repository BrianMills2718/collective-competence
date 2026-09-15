(() => {
'use strict';
const HV=window.HV;
const baseLayout=HV.hubLayout;
const baseTypeEdges=HV.renderBundledTypeEdges;

function binding(edge,role){return (edge.bindings||[]).find(b=>b.role===role)?.participant||null;}

function roleSchemaLayout(view){
  const nodeMap=new Map(view.nodes.map(n=>[n.id,n]));
  const groups=new Map();
  for(const edge of view.hyperedges){
    if(edge.type!=='sci:declaresRole')continue;
    const relation=binding(edge,'sci:declaredRelationType'),role=binding(edge,'sci:declaredRoleType');
    if(!relation||!role)continue;
    if(!groups.has(relation))groups.set(relation,[]);
    groups.get(relation).push({edge,role});
  }
  const positions=new Map();
  const relationIds=[...groups.keys()].sort((a,b)=>(nodeMap.get(a)?.label||a).localeCompare(nodeMap.get(b)?.label||b));
  let y=0;
  const rowGap=72,groupGap=70;
  for(const relationId of relationIds){
    const rows=groups.get(relationId).sort((a,b)=>(nodeMap.get(a.role)?.label||a.role).localeCompare(nodeMap.get(b.role)?.label||b.role));
    const start=y;
    for(const {edge,role} of rows){
      positions.set(edge.id,{x:370,y,w:HV.relationWidth(edge),h:HV.relationHeight});
      const rn=nodeMap.get(role);positions.set(role,{x:690,y,w:HV.nodeWidth(rn),h:HV.nodeHeight});
      y+=rowGap;
    }
    const middle=(start+(y-rowGap))/2;
    const relationNode=nodeMap.get(relationId);positions.set(relationId,{x:40,y:middle,w:HV.nodeWidth(relationNode),h:HV.nodeHeight});
    y+=groupGap;
  }

  const metadata=view.nodes.filter(n=>!positions.has(n.id));
  const classNodes=metadata.filter(n=>n.id==='sci:RelationType'||n.id==='sci:RoleType');
  const values=metadata.filter(n=>HV.hasType?.(n.id,'sci:Value')&&n.id!=='sci:RelationType'&&n.id!=='sci:RoleType').sort((a,b)=>String(a.label).localeCompare(String(b.label)));
  const other=metadata.filter(n=>!classNodes.includes(n)&&!values.includes(n)).sort((a,b)=>a.id.localeCompare(b.id));
  classNodes.forEach((n,i)=>positions.set(n.id,{x:-270,y:-80+i*130,w:HV.nodeWidth(n),h:HV.nodeHeight}));
  values.forEach((n,i)=>positions.set(n.id,{x:1020,y:-150+i*66,w:HV.nodeWidth(n),h:HV.nodeHeight}));
  other.forEach((n,i)=>positions.set(n.id,{x:1270,y:-150+i*66,w:HV.nodeWidth(n),h:HV.nodeHeight}));

  let minx=Infinity,miny=Infinity,maxx=-Infinity,maxy=-Infinity;
  for(const z of positions.values()){minx=Math.min(minx,z.x-z.w/2);maxx=Math.max(maxx,z.x+z.w/2);miny=Math.min(miny,z.y-z.h/2);maxy=Math.max(maxy,z.y+z.h/2);}
  return {positions,slotMap:new Map(),width:maxx-minx+180,height:maxy-miny+180,offsetX:-minx+90,offsetY:-miny+90,roleSchema:true};
}

HV.hubLayout=view=>HV.state.preset==='roleSchema'?roleSchemaLayout(view):baseLayout(view);

HV.renderBundledTypeEdges=edgeGroup=>{
  if(HV.state.preset!=='roleSchema')return baseTypeEdges(edgeGroup);
  const layout=HV.state.layout,declType=layout.positions.get('sci:declaresRole');
  if(declType){
    const a=HV.canvasPoint(declType),junction={x:a.x+190,y:a.y};
    HV.curve(edgeGroup,a,junction,'type-edge type-trunk',.34);
    for(const e of HV.state.view.hyperedges){const rp=layout.positions.get(e.id);if(rp)HV.curve(edgeGroup,junction,HV.canvasPoint(rp),'type-edge type-branch',.13);}
  }
  // Compact node `type` fields are serialization sugar for instanceOf. Render them
  // as two bundled meta-typing trunks so RoleType/RelationType membership is visible.
  for(const target of ['sci:RelationType','sci:RoleType']){
    const targetPos=layout.positions.get(target);if(!targetPos)continue;
    const members=HV.state.view.nodes.filter(n=>HV.hasType?.(n.id,target)&&layout.positions.has(n.id));
    if(!members.length)continue;
    const a=HV.canvasPoint(targetPos),junction={x:a.x+150,y:a.y};
    HV.curve(edgeGroup,a,junction,'type-edge type-trunk',.28);
    for(const n of members)HV.curve(edgeGroup,junction,HV.canvasPoint(layout.positions.get(n.id)),'type-edge type-branch',.12);
  }
};
})();
