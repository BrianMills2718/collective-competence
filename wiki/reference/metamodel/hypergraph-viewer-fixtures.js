(() => {
'use strict';
const HV = window.HV = window.HV || {};
HV.FIXTURES = {
  roleSchema:'scientific-role-schema-v1.json',
  cc:'c2-q1-hypergraph-v1.json',
  mechanics:'classical-mechanics-hypergraph-v1.json',
  oscillator:'harmonic-oscillator-hypergraph-v1.json',
  reaction:'first-order-reaction-hypergraph-v1.json',
  stochastic:'ornstein-uhlenbeck-hypergraph-v1.json',
  heat:'heat-equation-hypergraph-v1.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph-v1.json',
  calibration:'calibration-covariance-hypergraph-v1.json',
  causal:'causal-markov-equivalence-hypergraph-v1.json',
  topology:'dynamic-topology-hypergraph-v1.json',
  gauge:'gauge-equivalence-hypergraph-v1.json',
};
HV.AGGREGATE_FIXTURES = ['cc','mechanics','oscillator','reaction','stochastic','heat','multiscale','calibration','causal','topology','gauge'];
HV.SOURCE_LABEL = {
  roleSchema:'Scientific relation / role metamodel',
  cc:'Collective Competence C2/Q1 (v1)',
  mechanics:'Classical mechanics (v1)',
  oscillator:'Harmonic oscillator (v1)',
  reaction:'Reaction kinetics (v1)',
  stochastic:'Ornstein-Uhlenbeck stochastic process (v1)',
  heat:'Heat-equation PDE (v1)',
  multiscale:'Random walk → diffusion multiscale (v1)',
  calibration:'Correlated calibration uncertainty (v1)',
  causal:'Causal Markov equivalence + intervention (v1)',
  topology:'Dynamic topology + entity creation (local schema v1)',
  gauge:'Gauge-equivalent representations (local schema v1)',
};
})();
