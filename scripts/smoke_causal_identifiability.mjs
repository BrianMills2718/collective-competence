#!/usr/bin/env node
import {createServer} from 'node:http';import {readFile} from 'node:fs/promises';import {existsSync} from 'node:fs';import path from 'node:path';import {chromium} from 'playwright';
const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..'),PORT=Number(process.env.HYPERGRAPH_CAUSAL_PORT||4180),VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
const safe=u=>{const p=decodeURIComponent(new URL(u,`http://127.0.0.1:${PORT}`).pathname),r=path.resolve(ROOT,`.${p}`);return r.startsWith(ROOT+path.sep)||r===ROOT?r:null};
async function serve(req,res){const f=safe(req.url||'/');if(!f||!existsSync(f)){res.writeHead(404);return res.end('not found')}res.writeHead(200,{'content-type':MIME[path.extname(f)]||'application/octet-stream','cache-control':'no-store'});res.end(await readFile(f));}
function assert(ok,msg){if(!ok)throw new Error(msg)}
const server=createServer((a,b)=>void serve(a,b));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1700,height:1100}}),errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','causal');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});
  assert(await page.locator('[data-id="causal::claim:CI"]').count()===1,'conditional-independence proposition missing');
  const obs=page.locator('[data-id="causal::h:obs-identifiability"]');assert(await obs.count()===1,'observational identifiability relation missing');await obs.click();
  let text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:idEquivalenceClass'),'observational relation missing equivalence-class RoleType');
  assert(text?.includes('observational Markov-equivalence class'),'observational equivalence class missing');
  assert(text?.includes('observationally underdetermined'),'observational status is not underdetermined');
  const inter=page.locator('[data-id="causal::h:int-identifiability"]');assert(await inter.count()===1,'interventional identifiability relation missing');await inter.click();
  text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:idInterventionFamily'),'interventional relation missing intervention-family RoleType');
  assert(text?.includes('do(X=x) intervention'),'do(X=x) intervention missing');
  assert(text?.includes('identified by intervention'),'interventional status is not identified');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS causal identifiability: observational equivalence is underdetermined and do(X=x) distinguishes the candidates');
}finally{await browser.close();server.close();}
