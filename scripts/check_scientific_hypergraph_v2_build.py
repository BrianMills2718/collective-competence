#!/usr/bin/env python3
"""Require committed AI-facing v2 artifacts to equal deterministic rebuild output."""
from pathlib import Path
from tempfile import TemporaryDirectory
import filecmp
from build_scientific_hypergraph_v2 import build,DIR

NAMES=['hypergraph-kernel-v2.json','scientific-semantic-types-v2.json','scientific-role-schema-v2.json']
NAMES += [p.name.replace('-v1.json','-v2.json') for p in [
 DIR/'c2-q1-hypergraph-v1.json',DIR/'classical-mechanics-hypergraph-v1.json',DIR/'harmonic-oscillator-hypergraph-v1.json',
 DIR/'first-order-reaction-hypergraph-v1.json',DIR/'ornstein-uhlenbeck-hypergraph-v1.json',DIR/'heat-equation-hypergraph-v1.json',
 DIR/'random-walk-diffusion-multiscale-hypergraph-v1.json',DIR/'calibration-covariance-hypergraph-v1.json',
 DIR/'causal-markov-equivalence-hypergraph-v1.json',DIR/'dynamic-topology-hypergraph-v1.json',DIR/'gauge-equivalence-hypergraph-v1.json',
 DIR/'stochastic-heat-equation-hypergraph-v1.json',DIR/'uncertain-lineage-hypergraph-v1.json',DIR/'role-binding-epistemics-hypergraph-v1.json']]

def main():
    with TemporaryDirectory() as td:
        out=Path(td); build(out)
        stale=[]
        for name in NAMES:
            if not (DIR/name).exists() or not filecmp.cmp(DIR/name,out/name,shallow=False): stale.append(name)
        if stale: raise SystemExit('stale/non-deterministic v2 artifacts: '+', '.join(stale))
    print(f'PASS canonical v2 rebuild is byte-identical for {len(NAMES)} artifacts')
if __name__=='__main__': main()
