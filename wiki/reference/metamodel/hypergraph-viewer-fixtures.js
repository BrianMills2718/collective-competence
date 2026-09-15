(() => {
'use strict';
const HV = window.HV = window.HV || {};
HV.FIXTURES = {
  roleSchema:'scientific-role-schema-v1.json',
  cc:'c2-q1-hypergraph-v2.json',
  mechanics:'classical-mechanics-hypergraph-v2.json',
  oscillator:'harmonic-oscillator-hypergraph-v2.json',
  reaction:'first-order-reaction-hypergraph-v2.json',
  stochastic:'ornstein-uhlenbeck-hypergraph-v2.json',
  heat:'heat-equation-hypergraph-v2.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph-v2.json',
  calibration:'calibration-covariance-hypergraph-v2.json',
  causal:'causal-markov-equivalence-hypergraph-v2.json',
  topology:'dynamic-topology-hypergraph-v2.json',
  gauge:'gauge-equivalence-hypergraph-v2.json',
  spde:'stochastic-heat-equation-hypergraph-v2.json',
  lineage:'uncertain-lineage-hypergraph-v2.json',
  binding:'role-binding-epistemics-hypergraph-v2.json',
};
HV.AGGREGATE_FIXTURES = ['cc','mechanics','oscillator','reaction','stochastic','heat','multiscale','calibration','causal','topology','gauge','spde','lineage'];
HV.SOURCE_LABEL = {
  roleSchema:'Scientific relation / role metamodel',
  cc:'Collective Competence C2/Q1 (v2)',
  mechanics:'Classical mechanics (v2)',
  oscillator:'Harmonic oscillator (v2)',
  reaction:'Reaction kinetics (v2)',
  stochastic:'Ornstein-Uhlenbeck stochastic process (v2)',
  heat:'Heat-equation PDE (v2)',
  multiscale:'Random walk → diffusion multiscale (v2)',
  calibration:'Correlated calibration uncertainty (v2)',
  causal:'Causal Markov equivalence + intervention (v2)',
  topology:'Dynamic topology + entity creation (local schema v2)',
  gauge:'Gauge-equivalent representations (local schema v2)',
  spde:'Stochastic heat equation + random field (v2)',
  lineage:'Uncertain lineage + model-dependent identity (local schema v2)',
  binding:'First-class RoleBinding epistemics (structural v2)',
};
})();
