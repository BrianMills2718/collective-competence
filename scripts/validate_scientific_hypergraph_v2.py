#!/usr/bin/env python3
"""Validate canonical AI-facing scientific-hypergraph-v2 import closures."""
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict,deque
from pathlib import Path
from typing import Any

from generate_role_contracts_from_schema_graph import contracts_from_graph

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'wiki/reference/metamodel'
MODEL='scientific-hypergraph-v2'


def read(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))

def v2_to_nested(doc:dict[str,Any])->dict[str,Any]:
    by=defaultdict(list)
    for b in doc.get('bindings',[]):
        x={k:v for k,v in b.items() if k!='relation'}; by[b['relation']].append(x)
    return {'model':'scientific-hypergraph-v1','imports':doc.get('imports',[]),
            'nodes':[dict(e) for e in doc.get('elements',[])],
            'hyperedges':[{**{k:v for k,v in r.items() if k!='relationType'},'type':r['relationType'],'bindings':by[r['id']]} for r in doc.get('relations',[])]}

def resolve(root:Path)->list[tuple[Path,dict[str,Any]]]:
    docs=[]; seen=set()
    def visit(p:Path):
        key=p.resolve()
        if key in seen:return
        seen.add(key); d=read(p)
        if d.get('model')!=MODEL: raise ValueError(f'{p}: expected {MODEL}')
        for imp in d.get('imports',[]):
            q=DIR/f'{imp}.json'
            if not q.exists(): raise ValueError(f'{p}: missing import {imp!r} -> {q}')
            visit(q)
        docs.append((p,d))
    visit(root); return docs

def bootstrap_contracts(docs):
    out={}
    for _,d in docs:
        for rid,spec in d.get('bootstrap',{}).get('relationTypes',{}).items():
            old=out.get(rid)
            if old is not None and old!=spec: raise ValueError(f'conflicting bootstrap contract {rid}')
            out[rid]=spec
    return out

def merged_contracts(docs):
    result=bootstrap_contracts(docs)
    # Contract declarations may point to semantic type/value nodes supplied by imports,
    # so derive declarations from the resolved closure rather than file-local graphs.
    nodes=[]; hyperedges=[]; seen_nodes=set(); seen_edges=set()
    for _,d in docs:
        nested=v2_to_nested(d)
        for n in nested['nodes']:
            if n['id'] not in seen_nodes:
                seen_nodes.add(n['id']); nodes.append(n)
        for e in nested['hyperedges']:
            if e['id'] not in seen_edges:
                seen_edges.add(e['id']); hyperedges.append(e)
    closure={'model':'scientific-hypergraph-v1','imports':[],'nodes':nodes,'hyperedges':hyperedges}
    if any(e.get('type')=='sci:declaresRole' for e in hyperedges):
        c=contracts_from_graph(closure)
        for rid,spec in c.get('relationTypes',{}).items():
            old=result.get(rid)
            if old is not None:
                # Bootstrap contracts carry only the irreducible min/max needed to read
                # the self-hosted graph. Once the graph is readable, its richer
                # labels/aliases/qualifier metadata may replace that bootstrap view.
                for role,bs in old.get('roles',{}).items():
                    gs=spec.get('roles',{}).get(role)
                    if gs is None or gs.get('min',0)!=bs.get('min',0) or gs.get('max')!=bs.get('max'):
                        raise ValueError(f'graph declaration for {rid}/{role} conflicts with bootstrap cardinality')
            result[rid]=spec
    return result

def validate(path:Path)->tuple[int,int,int,int]:
    docs=resolve(path); contracts=merged_contracts(docs)
    elements={}; relations={}; addr_bindings={}; bindings=[]
    for p,d in docs:
        for e in d.get('elements',[]):
            if e['id'] in elements: raise ValueError(f'duplicate element id across closure: {e["id"]}')
            elements[e['id']]=(p,e)
        for r in d.get('relations',[]):
            if r['id'] in relations: raise ValueError(f'duplicate relation id across closure: {r["id"]}')
            relations[r['id']]=(p,r)
        for b in d.get('bindings',[]):
            bindings.append((p,b))
            if b.get('id'):
                if b['id'] in addr_bindings: raise ValueError(f'duplicate binding id across closure: {b["id"]}')
                addr_bindings[b['id']]=(p,b)
    all_ids=set(elements)|set(relations)|set(addr_bindings)
    if len(all_ids)!=len(elements)+len(relations)+len(addr_bindings): raise ValueError('global element/relation/binding ID collision')

    # Semantic type index with transitive specialization.
    direct=defaultdict(set); supers=defaultdict(set)
    for _,r in relations.values():
        if r['relationType'] not in {'sci:instanceOf','sci:specializes'}: continue
        rb=[b for _,b in bindings if b['relation']==r['id']]
        def ps(role): return [b['participant'] for b in rb if b['role']==role]
        if r['relationType']=='sci:instanceOf':
            for i in ps('sci:instance'):
                for t in ps('sci:type'): direct[i].add(t)
        else:
            for sub in ps('sci:subtype'):
                for sup in ps('sci:supertype'): supers[sub].add(sup)
    for x in all_ids: direct[x].add('sci:ModelElement')
    for x in relations: direct[x].add('sci:RelationInstance')
    for x in addr_bindings: direct[x].add('sci:RoleBinding')
    changed=True
    while changed:
        changed=False
        for x,ts in list(direct.items()):
            add=set()
            for t in list(ts): add|=supers.get(t,set())
            if not add<=ts: ts|=add; changed=True
        for sub,ss in list(supers.items()):
            add=set()
            for s in list(ss): add|=supers.get(s,set())
            if not add<=ss: ss|=add; changed=True

    counts=defaultdict(Counter); adjacency=defaultdict(set)
    for p,r in relations.values():
        rid=r['id']; rt=r.get('relationType')
        if rt not in elements: raise ValueError(f'{p}:{rid}: relationType {rt!r} does not resolve in import closure')
        if rt not in contracts: raise ValueError(f'{p}:{rid}: no role contract for relationType {rt!r}')
        adjacency[rid].add(rt); adjacency[rt].add(rid)
    for p,b in bindings:
        rid=b.get('relation'); role=b.get('role'); part=b.get('participant')
        if rid not in relations: raise ValueError(f'{p}: binding relation {rid!r} missing')
        if role not in elements: raise ValueError(f'{p}:{rid}: role identity {role!r} missing from closure')
        if part not in all_ids: raise ValueError(f'{p}:{rid}: participant {part!r} missing from closure')
        rt=relations[rid][1]['relationType']; spec=contracts[rt].get('roles',{}).get(role)
        if spec is None: raise ValueError(f'{p}:{rid}: role {role!r} not declared by {rt}')
        if b.get('qualifier') is not None and not spec.get('qualifiable',False): raise ValueError(f'{p}:{rid}: role {role} is not qualifiable')
        allowed=spec.get('participantTypes')
        if allowed and not (direct[part] & set(allowed)):
            raise ValueError(f'{p}:{rid}: participant {part!r} types {sorted(direct[part])} violate {role!r} allowed {allowed}')
        counts[rid][role]+=1
        bid=b.get('id')
        if bid:
            adjacency[rid].add(bid);adjacency[bid].add(rid);adjacency[bid].add(part);adjacency[part].add(bid);adjacency[bid].add(role);adjacency[role].add(bid)
        else:
            adjacency[rid].add(part);adjacency[part].add(rid);adjacency[rid].add(role);adjacency[role].add(rid)
    for rid,(_,r) in relations.items():
        for role,spec in contracts[r['relationType']].get('roles',{}).items():
            n=counts[rid][role]; mn=int(spec.get('min',0)); mx=spec.get('max')
            if n<mn: raise ValueError(f'{rid}: role {role} count {n} below {mn}')
            if mx is not None and n>int(mx): raise ValueError(f'{rid}: role {role} count {n} above {mx}')
    # The root model must be one connected semantic component through the resolved
    # import graph. Imported libraries may contain unused vocabulary that is not part
    # of this model's active component.
    _,root_doc=docs[-1]
    root_ids={e['id'] for e in root_doc.get('elements',[])}|{r['id'] for r in root_doc.get('relations',[])}|{b['id'] for b in root_doc.get('bindings',[]) if b.get('id')}
    if not root_ids: raise ValueError('root v2 artifact declares no addressable IDs')
    start=next(iter(root_ids)); seen={start}; q=deque([start])
    while q:
        x=q.popleft()
        for y in adjacency[x]:
            if y not in seen: seen.add(y); q.append(y)
    missing=root_ids-seen
    if missing: raise ValueError(f'root semantic graph disconnected across import closure: {len(missing)} IDs; sample {sorted(missing)[:12]}')
    return len(elements),len(relations),len(bindings),len(docs)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path); args=ap.parse_args()
    a,b,c,d=validate(args.fixture); print(f'valid scientific-hypergraph-v2 closure: {a} elements / {b} relations / {c} bindings across {d} imported documents; one component')
if __name__=='__main__':main()
