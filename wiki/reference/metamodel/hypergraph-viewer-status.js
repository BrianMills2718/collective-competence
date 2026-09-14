(() => {
'use strict';
const HV=window.HV;
const original=HV.relayout;
HV.relayout=async (...args) => {
  await original(...args);
  const text=HV.els.status.textContent||'';
  if(!/Layout failed|Load failed/.test(text) && !/semantic hub/.test(text)) HV.els.status.textContent=`${text} · semantic hub`;
};
})();
