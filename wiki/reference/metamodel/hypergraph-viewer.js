(() => {
  'use strict';

  const FIXTURES = {
    cc: 'c2-q1-hypergraph-v0.json',
    mechanics: 'classical-mechanics-hypergraph.json',
    oscillator: 'harmonic-oscillator-hypergraph.json',
    reaction: 'first-order-reaction-hypergraph.json',
  };
  const LAYER_RANK = { metamodel: 0, schema: 1, theory: 2, study: 3, evidence: 4 };
  const COLORS = { metamodel: '#58a6ff', schema: '#c297ff', theory: '#66d48f', study: '#f1a65a', evidence: '#ff7b72' };
  const NS = 'http://www.w3.org/2000/svg';
  const elk = new ELK();

  const els = Object.fromEntries([
    'fixture','layer','relationType','search','relayout','fit','focus','file','status','graph','stage','loading',
    'selTitle','selMeta','selDesc','roles'
  ].map(id => [id, document.getElementById(id)]));

  const state = {
    data: { nodes: [], hyperedges: [] },
    visible: null,
    layout: null,
    selected: null,
    focusSet: null,
    transform: { x: 0, y: 0, k: 1 },
    panning: null,
    sourceLabel: 'all stress tests',
  };

  function rank(item) { return LAYER_RANK[item?.layer] ?? 3; }
  function safeText(v) { return String(v ?? ''); }
  function labelOf(id) {
    const x = index().get(id);
    return x?.label || x?.type || id;
  }
  function index() {
    const m = new Map();
    state.data.nodes.forEach(x => m.set(x.id, x));
    state.data.hyperedges.forEach(x => m.set(x.id, x));
    return m;
  }

  async function fetchJson(path) {
    const r = await fetch(path, { cache: 'no-store' });
    if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`);
    return r.json();
  }

  function mergeDocuments(entries) {
    const nodeMap = new Map();
    const hyperedges = [];
    for (const { slug, doc } of entries) {
      const edges = doc.hyperedges || [];
      const edgeMap = new Map(edges.map(e => [e.id, `${slug}::${e.id}`]));
      for (const n of doc.nodes || []) {
        const existing = nodeMap.get(n.id);
        const source = ['metamodel','schema'].includes(n.layer) ? 'shared' : slug;
        if (existing) {
          existing.sources = Array.from(new Set([...(existing.sources || []), source]));
        } else {
          nodeMap.set(n.id, { ...n, source, sources: [source] });
        }
      }
      for (const e of edges) {
        const roles = {};
        for (const [role, participant] of Object.entries(e.roles || {})) {
          roles[role] = edgeMap.get(participant) || participant;
        }
        hyperedges.push({ ...e, id: edgeMap.get(e.id), originalId: e.id, roles, source: slug });
      }
    }
    return { model: 'scientific-hypergraph-merged', nodes: [...nodeMap.values()], hyperedges };
  }

  async function loadPreset(value) {
    showLoading(true, 'Loading fixture…');
    try {
      const keys = value === 'all' ? Object.keys(FIXTURES) : [value];
      const docs = await Promise.all(keys.map(async slug => ({ slug, doc: await fetchJson(FIXTURES[slug]) })));
      state.data = mergeDocuments(docs);
      state.sourceLabel = value === 'all' ? 'all stress tests' : value;
      state.selected = null;
      state.focusSet = null;
      populateRelationTypes();
      await relayout(true);
    } catch (err) {
      console.error(err);
      els.status.textContent = 'Load failed — use Open JSON or serve this folder over HTTP';
      showLoading(false);
    }
  }

  async function loadFiles(files) {
    const entries = [];
    for (const file of files) {
      const text = await file.text();
      const slug = file.name.replace(/\.(jsonld|json)$/i, '').replace(/[^a-z0-9_-]+/gi, '-');
      entries.push({ slug, doc: JSON.parse(text) });
    }
    state.data = mergeDocuments(entries);
    state.sourceLabel = entries.map(x => x.slug).join(', ');
    state.selected = null;
    state.focusSet = null;
    populateRelationTypes();
    await relayout(true);
  }

  function populateRelationTypes() {
    const current = els.relationType.value;
    const ids = [...new Set(state.data.hyperedges.map(e => e.type))].sort((a,b) => labelOf(a).localeCompare(labelOf(b)));
    els.relationType.innerHTML = '<option value="all">All relation types</option>' + ids.map(id => `<option value="${escapeHtml(id)}">${escapeHtml(labelOf(id))}</option>`).join('');
    if (ids.includes(current)) els.relationType.value = current;
  }

  function projection() {
    const idx = index();
    let baseNodes = new Set();
    let baseEdges = new Set();
    const layer = els.layer.value;
    const relationType = els.relationType.value;

    if (layer === 'all' && relationType === 'all') {
      baseNodes = new Set(state.data.nodes.map(n => n.id));
      baseEdges = new Set(state.data.hyperedges.map(e => e.id));
    } else {
      for (const n of state.data.nodes) if (layer === 'all' || n.layer === layer) baseNodes.add(n.id);
      for (const e of state.data.hyperedges) {
        const layerOk = layer === 'all' || e.layer === layer;
        const typeOk = relationType === 'all' || e.type === relationType;
        if (layerOk && typeOk) baseEdges.add(e.id);
      }
      if (relationType !== 'all') baseNodes.clear();
    }

    // A view is a projection, not a severed layer: retain the context needed to read each visible relation.
    for (const id of [...baseEdges]) {
      const e = idx.get(id);
      if (!e) continue;
      baseNodes.add(e.type);
      Object.values(e.roles || {}).forEach(p => {
        if (state.data.hyperedges.some(x => x.id === p)) baseEdges.add(p);
        else baseNodes.add(p);
      });
    }

    // If a layer-selected node participates in a relation, retain that relation and its immediate context.
    if (layer !== 'all' && relationType === 'all') {
      for (const e of state.data.hyperedges) {
        if (Object.values(e.roles || {}).some(p => baseNodes.has(p))) {
          baseEdges.add(e.id);
          baseNodes.add(e.type);
          Object.values(e.roles || {}).forEach(p => state.data.hyperedges.some(x => x.id === p) ? baseEdges.add(p) : baseNodes.add(p));
        }
      }
    }

    if (state.focusSet) {
      baseNodes = new Set([...baseNodes].filter(id => state.focusSet.has(id)));
      baseEdges = new Set([...baseEdges].filter(id => state.focusSet.has(id)));
    }

    return {
      nodes: state.data.nodes.filter(n => baseNodes.has(n.id)),
      hyperedges: state.data.hyperedges.filter(e => baseEdges.has(e.id)),
    };
  }

  function internalId(kind, id) { return `${kind}|${id}`; }
  function itemDimensions(item, relation = false) {
    const label = relation ? labelOf(item.type) : (item.label || item.id);
    return relation
      ? { width: Math.max(92, Math.min(150, 64 + label.length * 4.3)), height: 52 }
      : { width: Math.max(128, Math.min(230, 88 + label.length * 5.1)), height: 58 };
  }

  function buildElkGraph(view) {
    const all = new Map();
    view.nodes.forEach(n => all.set(n.id, n));
    view.hyperedges.forEach(e => all.set(e.id, e));
    const children = [];

    for (const n of view.nodes) {
      const d = itemDimensions(n, false);
      children.push({ id: internalId('n', n.id), width: d.width, height: d.height, layoutOptions: { 'elk.partitioning.partition': rank(n) } });
    }
    for (const e of view.hyperedges) {
      const d = itemDimensions(e, true);
      children.push({ id: internalId('r', e.id), width: d.width, height: d.height, layoutOptions: { 'elk.partitioning.partition': rank(e) } });
    }

    const present = new Set(children.map(x => x.id));
    const edges = [];
    let edgeNo = 0;
    const edgeMeta = new Map();

    function addEdge(a, b, meta) {
      if (!present.has(a) || !present.has(b) || a === b) return;
      const id = `elk-edge-${edgeNo++}`;
      edges.push({ id, sources: [a], targets: [b] });
      edgeMeta.set(id, meta);
    }

    for (const e of view.hyperedges) {
      const rid = internalId('r', e.id);
      addEdge(internalId('n', e.type), rid, { kind: 'type', label: 'type', relation: e.id, participant: e.type });
      for (const [role, p] of Object.entries(e.roles || {})) {
        const participant = all.get(p);
        if (!participant) continue;
        const pid = internalId(view.hyperedges.some(x => x.id === p) ? 'r' : 'n', p);
        // ELK direction is a layout hint only; role labels carry scientific semantics.
        const pr = rank(participant), rr = rank(e);
        const forward = pr < rr || (pr === rr && p.localeCompare(e.id) < 0);
        addEdge(forward ? pid : rid, forward ? rid : pid, { kind: 'role', label: role, relation: e.id, participant: p });
      }
    }

    return {
      graph: {
        id: 'root',
        layoutOptions: {
          'elk.algorithm': 'layered',
          'elk.direction': 'RIGHT',
          'elk.edgeRouting': 'ORTHOGONAL',
          'elk.partitioning.activate': true,
          'elk.spacing.nodeNode': 42,
          'elk.spacing.edgeNode': 22,
          'elk.spacing.edgeEdge': 12,
          'elk.layered.spacing.nodeNodeBetweenLayers': 105,
          'elk.layered.spacing.edgeNodeBetweenLayers': 28,
          'elk.layered.crossingMinimization.strategy': 'LAYER_SWEEP',
          'elk.layered.crossingMinimization.greedySwitch.type': 'TWO_SIDED',
          'elk.layered.nodePlacement.strategy': 'BRANDES_KOEPF',
          'elk.layered.nodePlacement.favorStraightEdges': true,
          'elk.padding': '[top=42,left=42,bottom=42,right=42]',
        },
        children,
        edges,
      },
      edgeMeta,
    };
  }

  async function relayout(fitAfter = false) {
    if (!state.data.nodes.length) return;
    showLoading(true, 'ELK: layering / crossing minimization / routing…');
    const started = performance.now();
    try {
      const view = projection();
      state.visible = view;
      const built = buildElkGraph(view);
      const laidOut = await elk.layout(built.graph);
      state.layout = { graph: laidOut, edgeMeta: built.edgeMeta };
      render();
      if (fitAfter) fitGraph();
      const elapsed = Math.round(performance.now() - started);
      els.status.textContent = `${view.nodes.length} elements · ${view.hyperedges.length} hyperrelations · ELK ${elapsed} ms`;
    } catch (err) {
      console.error(err);
      els.status.textContent = `Layout failed: ${err.message}`;
    } finally {
      showLoading(false);
    }
  }

  function render() {
    const svg = els.graph;
    svg.innerHTML = '';
    const root = document.createElementNS(NS, 'g');
    root.id = 'viewport';
    root.setAttribute('transform', transformString());
    svg.appendChild(root);
    if (!state.layout) return;

    const layoutNode = new Map((state.layout.graph.children || []).map(x => [x.id, x]));
    const visibleIndex = new Map();
    state.visible.nodes.forEach(n => visibleIndex.set(internalId('n', n.id), n));
    state.visible.hyperedges.forEach(e => visibleIndex.set(internalId('r', e.id), e));

    const edgeGroup = document.createElementNS(NS, 'g');
    const labelGroup = document.createElementNS(NS, 'g');
    const nodeGroup = document.createElementNS(NS, 'g');
    root.append(edgeGroup, labelGroup, nodeGroup);

    for (const edge of state.layout.graph.edges || []) {
      const meta = state.layout.edgeMeta.get(edge.id) || { kind: 'role', label: '' };
      const sections = edge.sections || [];
      if (!sections.length) continue;
      for (const section of sections) {
        const pts = [section.startPoint, ...(section.bendPoints || []), section.endPoint].filter(Boolean);
        if (pts.length < 2) continue;
        const path = document.createElementNS(NS, 'path');
        path.setAttribute('d', `M ${pts.map(p => `${p.x} ${p.y}`).join(' L ')}`);
        path.setAttribute('class', `edge ${meta.kind === 'type' ? 'type-edge' : ''}`);
        edgeGroup.appendChild(path);
        const mid = polylineMidpoint(pts);
        const t = document.createElementNS(NS, 'text');
        t.setAttribute('x', mid.x); t.setAttribute('y', mid.y - 4);
        t.setAttribute('text-anchor', 'middle'); t.setAttribute('class', 'role-label');
        t.dataset.search = `${meta.label} ${meta.relation} ${meta.participant}`.toLowerCase();
        t.textContent = meta.label;
        labelGroup.appendChild(t);
      }
    }

    for (const ln of state.layout.graph.children || []) {
      const item = visibleIndex.get(ln.id);
      if (!item) continue;
      const isRelation = ln.id.startsWith('r|');
      const g = document.createElementNS(NS, 'g');
      g.setAttribute('class', `${isRelation ? 'relation' : 'node'} ${state.selected === item.id ? 'selected' : ''}`);
      g.setAttribute('transform', `translate(${ln.x || 0} ${ln.y || 0})`);
      g.style.cursor = 'pointer';
      g.dataset.id = item.id;
      g.dataset.search = searchable(item).toLowerCase();
      g.addEventListener('click', ev => { ev.stopPropagation(); selectItem(item.id); });

      const color = COLORS[item.layer] || '#aab4bf';
      if (isRelation) {
        const poly = document.createElementNS(NS, 'polygon');
        const w = ln.width || 100, h = ln.height || 50;
        poly.setAttribute('points', `${w/2},0 ${w},${h/2} ${w/2},${h} 0,${h/2}`);
        poly.setAttribute('fill', color); poly.setAttribute('fill-opacity', '.14'); poly.setAttribute('stroke', color); poly.setAttribute('class', 'relation-shape');
        g.appendChild(poly);
      } else {
        const rect = document.createElementNS(NS, 'rect');
        rect.setAttribute('x', 0); rect.setAttribute('y', 0); rect.setAttribute('width', ln.width); rect.setAttribute('height', ln.height);
        rect.setAttribute('rx', item.kind === 'type' || item.kind === 'relationType' ? 24 : 9);
        rect.setAttribute('fill', color); rect.setAttribute('fill-opacity', '.14'); rect.setAttribute('stroke', color); rect.setAttribute('class', 'node-shape');
        g.appendChild(rect);
      }

      const title = document.createElementNS(NS, 'text');
      title.setAttribute('x', (ln.width || 100)/2); title.setAttribute('y', (ln.height || 50)/2 - 1); title.setAttribute('text-anchor', 'middle'); title.setAttribute('class', 'node-label');
      title.textContent = truncate(isRelation ? labelOf(item.type) : (item.label || item.id), 29);
      g.appendChild(title);
      const sub = document.createElementNS(NS, 'text');
      sub.setAttribute('x', (ln.width || 100)/2); sub.setAttribute('y', (ln.height || 50)/2 + 14); sub.setAttribute('text-anchor', 'middle'); sub.setAttribute('class', 'node-sub');
      sub.textContent = isRelation ? truncate(item.originalId || item.id, 30) : truncate(item.kind || item.layer || '', 28);
      g.appendChild(sub);
      nodeGroup.appendChild(g);
    }

    applySearch();
  }

  function searchable(item) {
    return [item.id, item.originalId, item.label, item.kind, item.layer, item.type, ...Object.keys(item.roles || {}), ...Object.values(item.roles || {})].filter(Boolean).join(' ');
  }
  function truncate(s, n) { s = safeText(s); return s.length > n ? `${s.slice(0, n-1)}…` : s; }
  function escapeHtml(s) { return safeText(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

  function polylineMidpoint(points) {
    let total = 0; const lengths = [];
    for (let i=1;i<points.length;i++) { const d = Math.hypot(points[i].x-points[i-1].x, points[i].y-points[i-1].y); lengths.push(d); total += d; }
    let target = total/2;
    for (let i=0;i<lengths.length;i++) {
      if (target <= lengths[i]) { const a=points[i], b=points[i+1], t=lengths[i] ? target/lengths[i] : 0; return {x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t}; }
      target -= lengths[i];
    }
    return points[Math.floor(points.length/2)];
  }

  function selectItem(id) {
    state.selected = id;
    const item = index().get(id);
    if (!item) return;
    const relation = state.data.hyperedges.find(x => x.id === id);
    els.selTitle.textContent = item.label || (relation ? labelOf(relation.type) : id);
    els.selMeta.textContent = `${relation ? 'n-ary relation' : item.kind || 'element'} · ${item.layer || 'unlayered'} · ${id}`;
    if (relation) {
      els.selDesc.textContent = 'First-class hyperrelation. The relation type and every role binding are explicit; this relation may itself participate in another relation.';
      els.roles.innerHTML = `<div class="role"><div class="roleName">relation type</div><div>${escapeHtml(labelOf(relation.type))}</div></div>` + Object.entries(relation.roles || {}).map(([role,p]) => `<div class="role"><div class="roleName">${escapeHtml(role)}</div><div>${escapeHtml(labelOf(p))}</div></div>`).join('');
    } else {
      const incident = state.data.hyperedges.filter(e => e.type === id || Object.values(e.roles || {}).includes(id));
      els.selDesc.textContent = `Model element participating in ${incident.length} semantic relation${incident.length===1?'':'s'}.`;
      els.roles.innerHTML = incident.map(e => `<div class="role"><div class="roleName">${escapeHtml(e.type===id?'type of':labelOf(e.type))}</div><div>${escapeHtml(e.originalId || e.id)}</div></div>`).join('');
    }
    render();
  }

  function neighborhood(id) {
    const result = new Set([id]);
    const idx = index();
    for (const e of state.data.hyperedges) {
      const involved = e.id === id || e.type === id || Object.values(e.roles || {}).includes(id);
      if (!involved) continue;
      result.add(e.id); result.add(e.type);
      Object.values(e.roles || {}).forEach(p => result.add(p));
    }
    const item = idx.get(id);
    if (item?.roles) { result.add(item.type); Object.values(item.roles).forEach(p => result.add(p)); }
    return result;
  }

  function applySearch() {
    const q = els.search.value.trim().toLowerCase();
    const viewport = document.getElementById('viewport');
    if (!viewport) return;
    viewport.querySelectorAll('.node,.relation,.role-label').forEach(el => {
      const hit = !q || (el.dataset.search || '').includes(q);
      el.classList.toggle('dim', !hit);
    });
  }

  function transformString() { const t=state.transform; return `translate(${t.x} ${t.y}) scale(${t.k})`; }
  function updateTransform() { const v=document.getElementById('viewport'); if (v) { v.setAttribute('transform', transformString()); v.querySelectorAll('.role-label').forEach(x => x.style.display = state.transform.k < .52 ? 'none' : ''); } }
  function fitGraph() {
    if (!state.layout) return;
    const w = els.stage.clientWidth, h = els.stage.clientHeight;
    const gw = Math.max(1, state.layout.graph.width || 1), gh = Math.max(1, state.layout.graph.height || 1);
    const k = Math.max(.08, Math.min(1.35, Math.min((w-40)/gw, (h-40)/gh)));
    state.transform = { x:(w-gw*k)/2, y:(h-gh*k)/2, k };
    updateTransform();
  }
  function showLoading(on, text='Laying out graph…') { els.loading.textContent=text; els.loading.style.display=on?'block':'none'; }

  els.fixture.addEventListener('change', () => loadPreset(els.fixture.value));
  els.layer.addEventListener('change', () => relayout(true));
  els.relationType.addEventListener('change', () => relayout(true));
  els.search.addEventListener('input', applySearch);
  els.relayout.addEventListener('click', () => relayout(true));
  els.fit.addEventListener('click', fitGraph);
  els.focus.addEventListener('click', async () => {
    if (state.focusSet) { state.focusSet=null; els.focus.textContent='Focus neighborhood'; await relayout(true); return; }
    if (!state.selected) { els.status.textContent='Select a node or relation first'; return; }
    state.focusSet = neighborhood(state.selected); els.focus.textContent='Clear focus'; await relayout(true);
  });
  els.file.addEventListener('change', async () => { if (els.file.files?.length) await loadFiles([...els.file.files]); });

  els.graph.addEventListener('click', () => { state.selected=null; render(); });
  els.graph.addEventListener('wheel', ev => {
    ev.preventDefault();
    const rect = els.graph.getBoundingClientRect();
    const mx=ev.clientX-rect.left, my=ev.clientY-rect.top, old=state.transform.k;
    const next=Math.max(.08,Math.min(4,old*(ev.deltaY<0?1.12:.89)));
    const gx=(mx-state.transform.x)/old, gy=(my-state.transform.y)/old;
    state.transform.x=mx-gx*next; state.transform.y=my-gy*next; state.transform.k=next; updateTransform();
  }, { passive:false });
  els.graph.addEventListener('pointerdown', ev => {
    if (ev.target.closest('.node,.relation')) return;
    state.panning={x:ev.clientX,y:ev.clientY,tx:state.transform.x,ty:state.transform.y}; els.graph.setPointerCapture(ev.pointerId);
  });
  els.graph.addEventListener('pointermove', ev => { if (!state.panning) return; state.transform.x=state.panning.tx+ev.clientX-state.panning.x; state.transform.y=state.panning.ty+ev.clientY-state.panning.y; updateTransform(); });
  els.graph.addEventListener('pointerup', () => state.panning=null);
  window.addEventListener('resize', () => fitGraph());

  loadPreset('all');
})();
