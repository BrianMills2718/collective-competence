#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_GAUGE_PORT||4182);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','gauge');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});

  assert(await page.locator('[data-id="gauge::gauge:GaugeEquivalenceRelation"]').count()===1,'local GaugeEquivalenceRelation type is not rendered');
  assert(await page.locator('[data-id="gauge::gauge:equivalence"]').count()===1,'gauge equivalence occurrence is not rendered');
  assert(await page.locator('[data-id="gauge::gauge:transform"]').count()===1,'gauge transformation equation is not rendered');

  const centralHasLocal = await page.evaluate(() => !!HV.roleContracts?.relationTypes?.['gauge:GaugeEquivalenceRelation']);
  assert(!centralHasLocal,'GaugeEquivalenceRelation incorrectly appears in shared role schema');

  await page.locator('[data-id="gauge::gauge:equivalence"]').click();
  const text=await page.locator('#roles').textContent();
  assert(text?.includes('gauge:representation'),'gauge inspector missing local representation RoleType');
  assert(text?.includes('original')&&text?.includes('transformed'),'gauge representation qualifiers missing');
  assert(text?.includes('gauge:transformation'),'gauge inspector missing transformation role');
  assert(text?.includes('gauge:invariant'),'gauge inspector missing invariant role');
  assert(text?.includes('magnetic field B(x)'),'gauge inspector does not expose B as invariant');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS gauge equivalence: local schema renders, higher-order transform is inspectable, and B is exposed as invariant');
} finally {await browser.close();server.close();}
