(() => {
'use strict';
const HV=window.HV;
// Canonical v2 is the primary machine/viewer format. The loader still understands
// v0/v1 for migration compatibility, but built-in scientific fixtures use v2.
Object.assign(HV.FIXTURES, {
  cc:'c2-q1-hypergraph-v2.json',
  mechanics:'classical-mechanics-hypergraph-v2.json',
  oscillator:'harmonic-oscillator-hypergraph-v2.json',
  reaction:'first-order-reaction-hypergraph-v2.json',
  stochastic:'ornstein-uhlenbeck-hypergraph-v2.json',
  heat:'heat-equation-hypergraph-v2.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph-v2.json',
  calibration:'calibration-covariance-hypergraph-v2.json',
});
const original=HV.relayout;
HV.relayout=async (...args) => {
  await original(...args);
  const text=HV.els.status.textContent||'';
  if(!/Layout failed|Load failed/.test(text) && !/semantic hub/.test(text)) HV.els.status.textContent=`${text} · semantic hub`;
};
})();
