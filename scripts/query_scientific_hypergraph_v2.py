#!/usr/bin/env python3
"""Machine query CLI for canonical scientific-hypergraph-v2 import closures.

Outputs JSON only. Intended for AI agents and automation, not human presentation.
"""
from __future__ import annotations
import argparse,json
from collections import defaultdict,deque,Counter
from pathlib import Path
from typing import Any
from validate_scientific_hypergraph_v2 import resolve


def closure(path:Path):
    docs=resolve(path); elements={};relations={};bindings=[];by_relation=defaultdict(list)
    for p,d in docs:
        for e in d.get('elements',[]): elements[e['id']]={**e,'_document':p.name}
        for r in d.get('relations',[]): relations[r['id']]={**r,'_document':p.name}
        for b in d.get('bindings',[]):
            x={**b,'_document':p.name};bindings.append(x);by_relation[x['relation']].append(x)
    addr={b['id']:b for b in bindings if b.get('id')}
    all_ids=set(elements)|set(relations)|set(addr)
    types=defaultdict(set); supers=defaultdict(set)
    for i in all_ids: types[i].add('sci:ModelElement')
    for i in relations: types[i].add('sci:RelationInstance')
    for i in addr: types[i].add('sci:RoleBinding')
    for rid,r in relations.items():
        bs=by_relation[rid]
        if r['relationType']=='sci:instanceOf':
            ins=[b['participant'] for b in bs if b['role']=='sci:instance']; ts=[b['participant'] for b in bs if b['role']=='sci:type']
            for i in ins:
                for t in ts: types[i].add(t)
        elif r['relationType']=='sci:specializes':
            subs=[b['participant'] for b in bs if b['role']=='sci:subtype']; sups=[b['participant'] for b in bs if b['role']=='sci:supertype']
            for a in subs:
                for z in sups: supers[a].add(z)
    changed=True
    while changed:
        changed=False
        for x,ts in list(types.items()):
            add=set().union(*(supers.get(t,set()) for t in list(ts))) if ts else set()
            if not add<=ts: ts|=add;changed=True
        for x,ss in list(supers.items()):
            add=set().union(*(supers.get(t,set()) for t in list(ss))) if ss else set()
            if not add<=ss:ss|=add;changed=True
    return docs,elements,relations,bindings,by_relation,addr,types

def item_record(cid,elements,relations,addr,types,by_relation,bindings):
    if cid in elements: base={'kind':'element',**elements[cid]}
    elif cid in relations: base={'kind':'relation',**relations[cid],'bindings':by_relation[cid]}
    elif cid in addr: base={'kind':'binding',**addr[cid]}
    else: raise KeyError(cid)
    base['semanticTypes']=sorted(types.get(cid,set()))
    inc=[]
    for b in bindings:
        if b['participant']==cid: inc.append({'relation':b['relation'],'role':b['role'],'binding':b.get('id'),'qualifier':b.get('qualifier')})
    base['inboundBindings']=inc
    return base

def adjacency(elements,relations,bindings):
    g=defaultdict(set)
    for rid,r in relations.items():
        g[rid].add(r['relationType']);g[r['relationType']].add(rid)
    for b in bindings:
        r,p,role=b['relation'],b['participant'],b['role'];bid=b.get('id')
        if bid:
            for a,z in [(r,bid),(bid,p),(bid,role)]:g[a].add(z);g[z].add(a)
        else:
            for a,z in [(r,p),(r,role)]:g[a].add(z);g[z].add(a)
    return g

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('fixture',type=Path)
    sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('summary')
    p=sub.add_parser('show');p.add_argument('id')
    p=sub.add_parser('types');p.add_argument('id')
    p=sub.add_parser('relations');p.add_argument('--type',required=True,dest='rtype')
    p=sub.add_parser('subgraph');p.add_argument('id');p.add_argument('--depth',type=int,default=1)
    args=ap.parse_args(); docs,elements,relations,bindings,by_relation,addr,types=closure(args.fixture)
    if args.cmd=='summary':
        root=docs[-1][1]; out={'model':root.get('model'),'root':args.fixture.name,'imports':[p.name for p,_ in docs[:-1]],
          'closure':{'elements':len(elements),'relations':len(relations),'bindings':len(bindings),'documents':len(docs)},
          'relationTypeCounts':dict(sorted(Counter(r['relationType'] for r in relations.values()).items()))}
    elif args.cmd=='show': out=item_record(args.id,elements,relations,addr,types,by_relation,bindings)
    elif args.cmd=='types': out={'id':args.id,'semanticTypes':sorted(types.get(args.id,set()))}
    elif args.cmd=='relations':
        ids=[rid for rid,r in relations.items() if r['relationType']==args.rtype]
        out={'relationType':args.rtype,'count':len(ids),'relations':[item_record(i,elements,relations,addr,types,by_relation,bindings) for i in ids]}
    else:
        g=adjacency(elements,relations,bindings);seen={args.id};q=deque([(args.id,0)])
        while q:
            x,d=q.popleft()
            if d>=args.depth:continue
            for y in g[x]:
                if y not in seen:seen.add(y);q.append((y,d+1))
        out={'seed':args.id,'depth':args.depth,'ids':sorted(seen),
             'elements':[elements[i] for i in sorted(seen&set(elements))],
             'relations':[item_record(i,elements,relations,addr,types,by_relation,bindings) for i in sorted(seen&set(relations))],
             'bindings':[addr[i] for i in sorted(seen&set(addr))]}
    print(json.dumps(out,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
