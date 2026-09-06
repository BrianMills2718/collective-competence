// CPython's `random.Random`, reproduced exactly, so the browser substrate draws
// the SAME numbers as the Python one.
//
// This file is the reason a second implementation of the substrate is safe here.
// Without it the browser could only approximate a Python run, every comparison
// between them would be statistical, and a real divergence would hide inside the
// noise. With it, `tests/test_bench_matches_python.py` can require the two
// implementations to agree step for step -- the same gate the Python substrate
// passes against `selfsort.py`.
//
// Verified against CPython 3.11 for random(), randrange(), shuffle() and
// sample(). `getrandbits` is implemented for k <= 32 only, which is all that
// `_randbelow` needs at any lattice size this laboratory uses; it throws rather
// than silently returning a wrong number outside that range.

class PyRandom {
  constructor(seed) { this.mt = new Uint32Array(624); this.mti = 625; this.seedInt(seed); }
  initGenrand(s) {
    const mt = this.mt; mt[0] = s >>> 0;
    for (let i = 1; i < 624; i++) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      // 1812433253 * prev, in 32-bit, done in 16-bit halves to avoid FP loss
      const lo = (prev & 0xffff) * 1812433253;
      const hi = ((prev >>> 16) * 1812433253) & 0xffff;
      mt[i] = (((hi << 16) >>> 0) + lo + i) >>> 0;
    }
    this.mti = 624;
  }
  initByArray(key) {
    this.initGenrand(19650218);
    const mt = this.mt;
    let i = 1, j = 0, k = Math.max(624, key.length);
    for (; k; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      const lo = (prev & 0xffff) * 1664525;
      const hi = ((prev >>> 16) * 1664525) & 0xffff;
      mt[i] = ((((mt[i] ^ (((hi << 16) >>> 0) + lo)) >>> 0) + key[j] + j) >>> 0);
      i++; j++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (k = 623; k; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      const lo = (prev & 0xffff) * 1566083941;
      const hi = ((prev >>> 16) * 1566083941) & 0xffff;
      mt[i] = ((((mt[i] ^ (((hi << 16) >>> 0) + lo)) >>> 0) - i) >>> 0);
      i++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
    }
    mt[0] = 0x80000000;
  }
  seedInt(seed) {
    let n = BigInt(seed); if (n < 0n) n = -n;
    const key = [];
    if (n === 0n) key.push(0);
    while (n > 0n) { key.push(Number(n & 0xffffffffn)); n >>= 32n; }
    this.initByArray(key);
  }
  genrand() {
    const mt = this.mt;
    if (this.mti >= 624) {
      for (let i = 0; i < 624; i++) {
        const y = ((mt[i] & 0x80000000) | (mt[(i + 1) % 624] & 0x7fffffff)) >>> 0;
        let next = (mt[(i + 397) % 624] ^ (y >>> 1)) >>> 0;
        if (y & 1) next = (next ^ 0x9908b0df) >>> 0;
        mt[i] = next;
      }
      this.mti = 0;
    }
    let y = mt[this.mti++];
    y = (y ^ (y >>> 11)) >>> 0;
    y = (y ^ ((y << 7) & 0x9d2c5680)) >>> 0;
    y = (y ^ ((y << 15) & 0xefc60000)) >>> 0;
    y = (y ^ (y >>> 18)) >>> 0;
    return y >>> 0;
  }
  random() {
    const a = this.genrand() >>> 5, b = this.genrand() >>> 6;
    return (a * 67108864 + b) * (1.0 / 9007199254740992.0);
  }
  getrandbits(k) {
    if (k === 0) return 0;
    if (k > 32) throw new RangeError(
      `getrandbits(${k}) is not implemented; this port covers k <= 32, which ` +
      `covers every lattice size the bench offers. A larger draw would return ` +
      `a number CPython would not, so it refuses rather than diverging quietly.`);
    return this.genrand() >>> (32 - k);
  }
  randbelow(n) {
    if (n <= 0) return 0;
    const k = 32 - Math.clz32(n);          // n.bit_length()
    let r = this.getrandbits(k);
    while (r >= n) r = this.getrandbits(k);
    return r;
  }
  randrange(n) { return this.randbelow(n); }
  shuffle(x) {
    for (let i = x.length - 1; i > 0; i--) {
      const j = this.randbelow(i + 1);
      const t = x[i]; x[i] = x[j]; x[j] = t;
    }
  }
  sample(population, k) {       // CPython's pool branch (n <= setsize)
    const n = population.length, pool = population.slice(), result = [];
    for (let i = 0; i < k; i++) {
      const j = this.randbelow(n - i);
      result.push(pool[j]);
      pool[j] = pool[n - i - 1];
    }
    return result;
  }
}
// Usable from both Node (conformance test) and a browser <script> (the bench).
if (typeof module !== "undefined" && module.exports) module.exports = { PyRandom };
if (typeof globalThis !== "undefined") globalThis.PyRandom = PyRandom;
