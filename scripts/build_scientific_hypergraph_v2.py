#!/usr/bin/env python3
"""Build canonical AI-facing scientific-hypergraph-v2 artifacts.

v2 is the explicit machine IR: top-level elements, relations and bindings, graph-native
typing, canonical sci:* relation identities, and import-resolved shared semantics.
v1 remains a migration/import compatibility representation.
"""
from __future__ import annotations
import json
from copy import deepcopy
from pathlib import Path
import argparse
from typing import Any

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import contract_indexes
from probe_semantic_role_schema import transform_role_schema
from probe_semantic_participant_types import FIXTURES, SEMANTIC_TYPE_PROFILE
from materialize_graph_native_v2_probe import materialize

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'wiki/reference/metamodel'
MODEL='scientific-hypergraph-v2'
KERNEL='hypergraph-kernel-v2'
PROFILE='scientific-semantic-types-v2'
ROLE_SCHEMA='scientific-role-schema-v2'


def read(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def write(p:Path,d:dict[str,Any])->None: p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def kernel_doc()->dict[str,Any]:
    elems=[
      ('sci:ModelElement','Model Element'),('sci:instanceOf','instance of'),('sci:specializes','specializes'),('sci:declaresRole','declares role'),
      ('sci:instance','instance'),('sci:type','type'),('sci:subtype','subtype'),('sci:supertype','supertype'),
      ('sci:declaredRelationType','declared relation type'),('sci:declaredRoleType','declared role type'),('sci:roleMinimum','minimum cardinality'),
      ('sci:roleMaximum','maximum cardinality'),('sci:roleQualifiable','qualifiable'),('sci:roleParticipantType','participant type')]
    return {
      'model':MODEL,'authority':'scientific-hypergraph-carrier-v2','imports':[],
      'bootstrap':{'relationTypes':{
        'sci:instanceOf':{'roles':{'sci:instance':{'min':1,'max':1},'sci:type':{'min':1,'max':1}}},
        'sci:specializes':{'roles':{'sci:subtype':{'min':1,'max':1},'sci:supertype':{'min':1,'max':1}}},
        'sci:declaresRole':{'roles':{
          'sci:declaredRelationType':{'min':1,'max':1},'sci:declaredRoleType':{'min':1,'max':1},
          'sci:roleMinimum':{'min':1,'max':1},'sci:roleMaximum':{'min':0,'max':1},
          'sci:roleQualifiable':{'min':1,'max':1},'sci:roleParticipantType':{'min':0,'max':None}}}}},
      'elements':[{'id':i,'label':l,'layer':'metamodel'} for i,l in elems], 'relations':[], 'bindings':[]}


def flatten_normalized(doc:dict[str,Any],imports:list[str],authority:str|None=None)->dict[str,Any]:
    out=materialize(doc)
    out['model']=MODEL; out['imports']=imports
    out['normalization']={'sourceModel':doc.get('model','unknown'),'algorithm':'graph-native-typing-v2'}
    if authority: out['authority']=authority
    return out


def canonicalize(doc:dict[str,Any], imported_ids:set[str], relation_aliases:dict[str,str])->dict[str,Any]:
    out=deepcopy(doc)
    id_alias={k:v for k,v in relation_aliases.items() if k!=v}
    # Canonicalize element identities used only as relation-type aliases.
    for e in out.get('elements',[]):
        if e['id'] in id_alias: e['id']=id_alias[e['id']]
    # canonicalize relation types and all participant references to aliased schema IDs
    for r in out.get('relations',[]): r['relationType']=relation_aliases.get(r['relationType'],r['relationType'])
    for b in out.get('bindings',[]): b['participant']=id_alias.get(b['participant'],b['participant'])

    # Deduplicate elements after alias canonicalization, preferring richer records.
    by_id:dict[str,dict[str,Any]]={}
    for e in out.get('elements',[]):
        old=by_id.get(e['id'])
        if old is None or len(e)>len(old): by_id[e['id']]=e
    # Imported shared definitions are not repeated locally.
    out['elements']=[e for i,e in sorted(by_id.items()) if i not in imported_ids]

    # Drop generated/shared-only typing relations that are already supplied by imports.
    kept=[]
    for r in out.get('relations',[]):
        rel_bind=[b for b in out.get('bindings',[]) if b['relation']==r['id']]
        participants={b['participant'] for b in rel_bind}
        if r['relationType'] in {'sci:instanceOf','sci:specializes'} and participants and participants <= imported_ids:
            continue
        kept.append(r)
    kept_ids={r['id'] for r in kept}
    out['relations']=kept
    out['bindings']=[b for b in out.get('bindings',[]) if b['relation'] in kept_ids]
    return out


def build(output_dir:Path)->None:
    output_dir.mkdir(parents=True,exist_ok=True)
    contracts=load_contracts(DEFAULT_ROLE_SCHEMA); aliases,_=contract_indexes(contracts)
    kernel=kernel_doc(); write(output_dir/f'{KERNEL}.json',kernel); kernel_ids={e['id'] for e in kernel['elements']}

    profile_src=read(Path(SEMANTIC_TYPE_PROFILE)); profile_src['imports']=[]
    for n in profile_src.get('nodes',[]): n.pop('authoringKind',None)
    profile=flatten_normalized(profile_src,[KERNEL],'scientific-semantic-type-profile-v2')
    profile=canonicalize(profile,kernel_ids,aliases); write(output_dir/f'{PROFILE}.json',profile)
    profile_ids=kernel_ids|{e['id'] for e in profile['elements']}|{r['id'] for r in profile['relations']}

    role_src=transform_role_schema(read(DIR/'scientific-role-schema-v1.json')); role_src['imports']=[]
    role=flatten_normalized(role_src,[KERNEL,PROFILE],'scientific-schema-role-declarations-v2')
    role=canonicalize(role,profile_ids,aliases); write(output_dir/f'{ROLE_SCHEMA}.json',role)
    shared_ids=profile_ids|{e['id'] for e in role['elements']}|{r['id'] for r in role['relations']}

    sources=[*FIXTURES,DIR/'role-binding-epistemics-hypergraph-v1.json']
    for src in sources:
        d=read(src); v2=flatten_normalized(d,[KERNEL,PROFILE,ROLE_SCHEMA])
        v2=canonicalize(v2,shared_ids,aliases)
        v2['normalization']['sourceArtifact']=src.name
        target=output_dir/src.name.replace('-v1.json','-v2.json')
        write(target,v2)
        print(f'WROTE {target.name}: {len(v2["elements"])} elements / {len(v2["relations"])} relations / {len(v2["bindings"])} bindings')

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,default=DIR); args=ap.parse_args()
    build(args.output_dir); return 0

if __name__=='__main__': raise SystemExit(main())
