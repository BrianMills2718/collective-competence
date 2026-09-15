#!/usr/bin/env python3
from pathlib import Path
from query_scientific_hypergraph_v2 import closure
from validate_scientific_hypergraph_v2 import DIR

def assert_(x,m):
    if not x: raise AssertionError(m)

def main():
    _,els,rels,bs,by,addr,types=closure(DIR/'classical-mechanics-hypergraph-v2.json')
    assert_('sci:Expression' in types['study:KExpression'],'KExpression semantic type missing')
    measurements=[r for r in rels.values() if r['relationType']=='sci:MeasurementRelation']
    assert_(len(measurements)==2,f'expected 2 mechanics measurements, got {len(measurements)}')
    assert_(all(r['relationType'].startswith('sci:') for r in measurements),'noncanonical relation type in v2')

    _,_,causal,_,_,_,_=closure(DIR/'causal-markov-equivalence-hypergraph-v2.json')
    assert_(sum(r['relationType']=='sci:IdentifiabilityRelation' for r in causal.values())==2,'causal identifiability relations missing')
    assert_(sum(r['relationType']=='sci:AccessRelation' for r in causal.values())==2,'causal access relations missing')

    _,_,_,_,_,addr,types=closure(DIR/'role-binding-epistemics-hypergraph-v2.json')
    assert_('binding:analysis-model' in addr,'addressable RoleBinding missing')
    assert_('sci:RoleBinding' in types['binding:analysis-model'],'RoleBinding semantic type missing')
    print('PASS v2 AI query acceptance: semantic typing, canonical relation IDs, causal identifiability/access, first-class RoleBinding')
if __name__=='__main__':main()
