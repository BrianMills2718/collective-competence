// The substrate, in the browser. A line-for-line mirror of
// `goal-discovery/src/lattice/core.py`, `observe.py` and `specimens/`.
//
// A second implementation of a simulator is normally a correctness hazard: the
// two drift, and the one people watch is not the one that produced the results.
// Two things make it safe here. `pyrandom.js` reproduces CPython's random
// stream exactly, so the two can be compared for EQUALITY rather than for
// resemblance. And `tests/test_bench_matches_python.py` runs both over a matrix
// of configurations and requires identical trajectories, so drift is a red
// test rather than a discrepancy nobody notices.
//
// If you change this file, change core.py in the same commit, or the gate will
// tell you. That is the intended workflow.

(function (root) {
  "use strict";

  // --- Faults: per-entity defects, applied at the moment of action -----------

  function makeFaults(spec) {
    spec = spec || {};
    return {
      pFail: spec.pFail || 0,
      unreliable: new Map(Object.entries(spec.unreliable || {}).map(
        ([k, v]) => [Number(k), v])),
      frozen: new Set(spec.frozen || []),
      dead: new Set(spec.dead || []),
    };
  }

  // --- The lattice ----------------------------------------------------------

  class Lattice {
    constructor(occupants, opts) {
      opts = opts || {};
      this.occupants = occupants.slice();
      this.faults = opts.faults || makeFaults();
      this.rng = opts.rng;
      this.radius = opts.radius === undefined ? 1 : opts.radius;
      this.ring = !!opts.ring;
      this.ops = 0;
      this.conserving = opts.conserving === undefined ? true : opts.conserving;
      this.centred = !!opts.centred;
    }

    get size() { return this.occupants.length; }

    windowAt(i) {
      const width = this.centred ? 2 * this.radius + 1 : 2 * this.radius;
      const start = this.centred ? i - this.radius : i;
      const out = [];
      if (this.ring) {
        for (let k = 0; k < width; k++)
          out.push(((start + k) % this.size + this.size) % this.size);
        return out;
      }
      if (start < 0 || start + width > this.size)
        throw new RangeError(`window at ${i} does not fit a line of ${this.size}`);
      for (let k = 0; k < width; k++) out.push(start + k);
      return out;
    }

    sites() {
      if (this.ring) return [...Array(this.size).keys()];
      if (this.centred) {
        const out = [];
        for (let i = this.radius; i < this.size - this.radius; i++) out.push(i);
        return out;
      }
      const width = 2 * this.radius, out = [];
      for (let i = 0; i <= this.size - width; i++) out.push(i);
      return out;
    }

    // Reading costs, because looking is the same primitive acting uses.
    read(i) {
      this.ops += 1;
      return this.windowAt(i).map((k) => this.occupants[k]);
    }

    // Fault order matters and is fixed: dead blocks first, because a dead
    // entity blocks interactions it did not initiate; then the initiator draw;
    // then frozen; then the stochastic failure. Any other order changes results.
    apply(i, rule, initiator, charge) {
      if (charge === undefined) charge = true;
      if (charge) this.ops += 1;
      const sites = this.windowAt(i);
      const before = sites.map((k) => this.occupants[k]);

      for (const o of before) if (o !== null && this.faults.dead.has(o)) return false;
      if (initiator === undefined || initiator === null)
        initiator = this._chooseInitiator(before);
      if (initiator === null) return false;
      if (this.faults.frozen.has(initiator)) return false;
      const q = Math.max(this.faults.pFail, this.faults.unreliable.get(initiator) || 0);
      if (q > 0 && this.rng.random() < q) return false;

      const after = rule(before, initiator);
      if (after.length !== before.length)
        throw new Error(`rule returned ${after.length} sites for a window of ${before.length}`);
      if (this.conserving) {
        const a = before.filter((x) => x !== null).slice().sort((x, y) => x - y);
        const b = after.filter((x) => x !== null).slice().sort((x, y) => x - y);
        if (a.length !== b.length || a.some((x, k) => x !== b[k]))
          throw new Error(
            `rule rearranged [${before}] into [${after}], which is not a permutation ` +
            `of it. This lattice is declared conserving.`);
      }
      let changed = false;
      for (let k = 0; k < sites.length; k++)
        if (this.occupants[sites[k]] !== after[k]) changed = true;
      if (!changed) return false;
      for (let k = 0; k < sites.length; k++) this.occupants[sites[k]] = after[k];
      return true;
    }

    _chooseInitiator(before) {
      const present = before.filter((o) => o !== null);
      if (!present.length) return null;
      if (present.length === 1) return present[0];
      if (present.length === 2)
        return this.rng.random() < 0.5 ? present[0] : present[1];
      return present[this.rng.randrange(present.length)];
    }

    snapshot() {
      return {
        occupants: this.occupants.slice(),
        ops: this.ops,
        rngState: { mt: this.rng.mt.slice(), mti: this.rng.mti },
        faults: {
          pFail: this.faults.pFail,
          unreliable: new Map(this.faults.unreliable),
          frozen: new Set(this.faults.frozen),
          dead: new Set(this.faults.dead),
        },
      };
    }

    restore(snap) {
      this.occupants = snap.occupants.slice();
      this.ops = snap.ops;
      this.rng.mt.set(snap.rngState.mt);
      this.rng.mti = snap.rngState.mti;
      this.faults = {
        pFail: snap.faults.pFail,
        unreliable: new Map(snap.faults.unreliable),
        frozen: new Set(snap.faults.frozen),
        dead: new Set(snap.faults.dead),
      };
    }
  }

  // --- Synchronous update: the classic cellular-automaton schedule ----------

  function stepSynchronous(lat, rule) {
    const before = lat.occupants.slice();
    const updated = before.slice();
    for (const i of lat.sites()) {
      lat.ops += 1;
      const sites = lat.windowAt(i);
      const win = sites.map((k) => before[k]);
      const centre = win[Math.floor(win.length / 2)];
      const out = rule(win, centre === null ? 0 : centre);
      for (let k = 0; k < sites.length; k++)
        if (sites[k] === i || !lat.centred) updated[sites[k]] = out[k];
    }
    const changed = updated.some((v, k) => v !== before[k]);
    lat.occupants = updated;
    return changed;
  }

  // --- Measurement. Functions FROM a lattice; the lattice cannot call them. --

  const observe = {
    values: (lat) => lat.occupants.filter((o) => o !== null),
    inversions(lat) {
      const v = observe.values(lat);
      let n = 0;
      for (let i = 0; i < v.length; i++)
        for (let j = i + 1; j < v.length; j++) if (v[i] > v[j]) n++;
      return n;
    },
    localDisorder(lat) {
      const v = observe.values(lat);
      let n = 0;
      for (let i = 0; i < v.length - 1; i++) if (v[i] > v[i + 1]) n++;
      return n;
    },
    isSorted: (lat) => observe.inversions(lat) === 0,
  };

  // --- Sorting -------------------------------------------------------------

  const RULE_ASCEND = (l, r) => l > r;
  const RULE_DESCEND = (l, r) => l < r;
  const RULE_ALWAYS = () => true;

  function pairwise(preferences) {
    return function (before, initiator) {
      const [left, right] = before;
      if (left === null || right === null) return before;
      return preferences.get(initiator)(left, right) ? [right, left] : before;
    };
  }

  function makeSorting(n, seed, faultSpec, nTypeB) {
    const rng = new root.PyRandom(seed);
    const values = [...Array(n).keys()];
    rng.shuffle(values);
    const typeB = new Set(nTypeB ? rng.sample([...Array(n).keys()], nTypeB) : []);
    const preferences = new Map();
    for (let v = 0; v < n; v++)
      preferences.set(v, typeB.has(v) ? RULE_DESCEND : RULE_ASCEND);
    const lat = new Lattice(values, { faults: makeFaults(faultSpec), rng });
    return { lat, rule: pairwise(preferences), preferences };
  }

  // Controllers as step functions: one call is one interaction, so the bench
  // can drive them from an animation frame and stop between any two steps.
  // `closed` reports that it has halted rather than throwing, because the bench
  // needs to keep drawing after it stops.

  function controller(kind, lat, rule) {
    if (kind === "decentralized")
      return { step() { lat.apply(lat.rng.randrange(lat.size - 1), rule); return true; } };

    let i = 0, foundThisPass = false, halted = false;
    return {
      step() {
        if (halted) return false;
        const before = lat.read(i);
        const [left, right] = before;
        if (left !== null && right !== null && left > right) {
          foundThisPass = true;
          lat.apply(i, rule, null, false);
        }
        i += 1;
        if (i >= lat.size - 1) {
          i = 0;
          if (kind === "closed" && !foundThisPass) halted = true;
          foundThisPass = false;
        }
        // This step HAPPENED, so it is reported as one even if the pass that
        // just ended was the last. Python's generator yields the final site of
        // a halting pass and only raises StopIteration on the following call;
        // returning `!halted` here dropped that last step and put the bench one
        // interaction behind the laboratory on every `closed` run. The
        // conformance gate caught it on its first execution.
        return true;
      },
      get halted() { return halted; },
    };
  }

  // --- Elementary cellular automata ----------------------------------------

  function wolfram(number) {
    if (!(number >= 0 && number <= 255)) throw new RangeError("rule is 0-255");
    return function (before) {
      const [l, c, r] = before;
      const index = (l || 0) * 4 + (c || 0) * 2 + (r || 0);
      return [l, (number >> index) & 1, r];
    };
  }

  function makeCA(number, size, seedCellOnly, seed) {
    let cells;
    if (seedCellOnly) {
      cells = new Array(size).fill(0);
      cells[Math.floor(size / 2)] = 1;
    } else {
      const rng = new root.PyRandom(seed || 0);
      cells = Array.from({ length: size }, () => rng.randrange(2));
    }
    const lat = new Lattice(cells, {
      rng: new root.PyRandom(seed || 0), radius: 1, ring: true,
      conserving: false, centred: true,
    });
    return { lat, rule: wolfram(number) };
  }

  const api = {
    Lattice, makeFaults, stepSynchronous, observe,
    makeSorting, controller, pairwise, wolfram, makeCA,
    RULE_ASCEND, RULE_DESCEND, RULE_ALWAYS,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.Substrate = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
