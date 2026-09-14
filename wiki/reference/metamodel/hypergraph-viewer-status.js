(() => {
'use strict';
const HV=window.HV;
// Typed-role v1 is now the primary acceptance/viewer format. The core loader still
// understands v0 for migration compatibility, but built-in scientific fixtures use v1.
Object.assign(HV.FIXTURES, {
  cc:'c2-q1-hypergraph-v1.json',
  mechanics:'classical-mechanics-hypergraph-v1.json',
  oscillator:'harmonic-oscillator-hypergraph-v1.json',
  reaction:'first-order-reaction-hypergraph-v1.json',
  stochastic:'ornstein-uhlenbeck-hypergraph-v1.json',
  heat:'heat-equation-hypergraph-v1.json',
  multiscale:'random-walk-diffusion-multiscale-hypergraph-v1.json',
  calibration:'calibration-covariance-hypergraph-v1.json',
});
const original=HV.relayout;
HV.relayout=async (...args) => {
  await original(...args);
  const text=HV.els.status.textContent||'';
  if(!/Layout failed|Load failed/.test(text) && !/semantic hub/.test(text)) HV.els.status.textContent=`${text} · semantic hub`;
};
})();
