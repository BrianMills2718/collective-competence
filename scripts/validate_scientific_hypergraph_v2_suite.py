#!/usr/bin/env python3
from pathlib import Path
from validate_scientific_hypergraph_v2 import validate,DIR

FILES=[DIR/'scientific-semantic-types-v2.json',DIR/'scientific-role-schema-v2.json']+sorted(DIR.glob('*-hypergraph-v2.json'))

def main():
    total=[0,0,0]
    for p in FILES:
        e,r,b,d=validate(p); total[0]+=e;total[1]+=r;total[2]+=b
        print(f'PASS {p.name}: closure {e} elements / {r} relations / {b} bindings / {d} documents')
    print(f'PASS all {len(FILES)} v2 roots; aggregate resolved counts (with repeated imports per root) {total[0]} elements / {total[1]} relations / {total[2]} bindings')
if __name__=='__main__':main()
