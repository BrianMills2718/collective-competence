#!/usr/bin/env node

import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const PORT = Number(process.env.HYPERGRAPH_SMOKE_PORT || 4177);
const VIEWER = '/wiki/reference/metamodel/hypergraph-viewer.html';
const ARTIFACT_DIR = path.join(ROOT, 'artifacts');
const SCREENSHOT = path.join(ARTIFACT_DIR, 'scientific-hypergraph-viewer.png');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.jsonld': 'application/ld+json; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml',
};

function safePath(urlPath) {
  const pathname = decodeURIComponent(new URL(urlPath, `http://127.0.0.1:${PORT}`).pathname);
  const resolved = path.resolve(ROOT, `.${pathname}`);
  if (!resolved.startsWith(ROOT + path.sep) && resolved !== ROOT) return null;
  return resolved;
}

async function serve(req, res) {
  const file = safePath(req.url || '/');
  if (!file || !existsSync(file)) {
    res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
    res.end('not found');
    return;
  }
  try {
    const body = await readFile(file);
    res.writeHead(200, {
      'content-type': MIME[path.extname(file)] || 'application/octet-stream',
      'cache-control': 'no-store',
    });
    res.end(body);
  } catch (error) {
    res.writeHead(500, { 'content-type': 'text/plain; charset=utf-8' });
    res.end(String(error));
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const server = createServer((req, res) => { void serve(req, res); });
await new Promise(resolve => server.listen(PORT, '127.0.0.1', resolve));

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1800, height: 1200 } });
const consoleErrors = [];
page.on('console', msg => {
  if (msg.type() === 'error') consoleErrors.push(msg.text());
});
page.on('pageerror', error => consoleErrors.push(error.stack || String(error)));

try {
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => /elements/.test(document.querySelector('#status')?.textContent || ''), null, { timeout: 20000 });
  await page.waitForTimeout(250);

  const initial = await page.evaluate(() => {
    const ids = [...document.querySelectorAll('#viewport .node,#viewport .relation')]
      .map(x => x.dataset.id)
      .filter(Boolean);
    return {
      status: document.querySelector('#status')?.textContent || '',
      ids,
      nodes: document.querySelectorAll('#viewport .node').length,
      relations: document.querySelectorAll('#viewport .relation').length,
      domains: document.querySelectorAll('#viewport .domain-label').length,
      layout: document.querySelector('#layoutMode')?.value || '',
    };
  });

  assert(initial.nodes > 0, 'no model-element nodes rendered');
  assert(initial.relations > 0, 'no relation-instance nodes rendered');
  assert(initial.domains >= 4, `expected >=4 domain labels, found ${initial.domains}`);
  assert(new Set(initial.ids).size === initial.ids.length, 'rendered IDs are not globally unique');
  assert(initial.ids.includes('mechanics::study:LabFrame'), 'mechanics study:LabFrame lost during merge');
  assert(initial.ids.includes('oscillator::study:LabFrame'), 'oscillator study:LabFrame lost during merge');
  assert(initial.layout === 'radial', `expected radial default, found ${initial.layout}`);

  const overlap = await page.evaluate(() => {
    const items = [...document.querySelectorAll('#viewport .node,#viewport .relation')]
      .map(el => ({ id: el.dataset.id, rect: el.getBoundingClientRect() }));
    let significant = 0;
    let severe = 0;
    let worst = 0;
    let worstPair = null;
    for (let i = 0; i < items.length; i++) {
      for (let j = i + 1; j < items.length; j++) {
        const a = items[i].rect, b = items[j].rect;
        const ix = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const iy = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        const area = ix * iy;
        if (!area) continue;
        const denom = Math.min(a.width * a.height, b.width * b.height) || 1;
        const ratio = area / denom;
        if (ratio > 0.08) significant++;
        if (ratio > 0.35) severe++;
        if (ratio > worst) { worst = ratio; worstPair = [items[i].id, items[j].id]; }
      }
    }
    return { significant, severe, worst, worstPair, count: items.length };
  });

  // The smoke test treats substantial node-on-node collisions as a regression.
  assert(overlap.severe === 0, `severe layout collision(s): ${JSON.stringify(overlap)}`);

  await page.locator('#viewport .relation').first().click();
  const inspectorRows = await page.locator('#roles .role').count();
  assert(inspectorRows >= 2, `relation inspector has only ${inspectorRows} rows`);

  const beforeFocus = await page.locator('#viewport .node,#viewport .relation').count();
  await page.locator('#focus').click();
  await page.waitForFunction(() => /elements/.test(document.querySelector('#status')?.textContent || ''), null, { timeout: 12000 });
  await page.waitForTimeout(120);
  const afterFocus = await page.locator('#viewport .node,#viewport .relation').count();
  assert(afterFocus > 0 && afterFocus < beforeFocus, `focus did not reduce graph: ${beforeFocus} -> ${afterFocus}`);

  await page.locator('#focus').click();
  await page.waitForFunction(() => /elements/.test(document.querySelector('#status')?.textContent || ''), null, { timeout: 12000 });

  await page.locator('#search').fill('velocity');
  const dimmed = await page.locator('#viewport .dim').count();
  assert(dimmed > 0, 'search did not dim non-matches');
  await page.locator('#search').fill('');

  const hasElk = await page.locator('#layoutMode option[value="elk"]').count();
  assert(hasElk === 1, 'ELK layered alternate layout missing');
  await page.selectOption('#layoutMode', 'elk');
  await page.waitForFunction(() => /elk/i.test(document.querySelector('#status')?.textContent || ''), null, { timeout: 20000 });
  await page.selectOption('#layoutMode', 'radial');
  await page.waitForFunction(() => /radial/i.test(document.querySelector('#status')?.textContent || ''), null, { timeout: 12000 });

  assert(consoleErrors.length === 0, `browser console/page errors: ${consoleErrors.join('\n')}`);

  await mkdir(ARTIFACT_DIR, { recursive: true });
  await page.screenshot({ path: SCREENSHOT, fullPage: true });

  console.log(`PASS exact viewer smoke: ${initial.status}`);
  console.log(`PASS rendered ${initial.nodes} elements + ${initial.relations} hyperrelations across ${initial.domains} domain sectors`);
  console.log(`PASS fixture-local identity isolation: mechanics::study:LabFrame and oscillator::study:LabFrame both present`);
  console.log(`PASS radial layout overlap: significant=${overlap.significant}, severe=${overlap.severe}, worst=${(overlap.worst * 100).toFixed(1)}%`);
  console.log(`PASS relation inspector rows=${inspectorRows}; focus ${beforeFocus} -> ${afterFocus}; search dimmed=${dimmed}`);
  console.log(`PASS radial + ELK deterministic layout modes executed without console errors`);
  console.log(`SCREENSHOT ${path.relative(ROOT, SCREENSHOT)}`);
} finally {
  await browser.close();
  server.close();
}
