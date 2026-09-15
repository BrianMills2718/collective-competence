#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_TOPOLOGY_PORT||4181);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','topology');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});

  assert(await page.locator('[data-id="topology::topo:DivisionRelation"]').count()===1,'local DivisionRelation type is not rendered');
  assert(await page.locator('[data-id="topology::topo:BondChangeRelation"]').count()===1,'local BondChangeRelation type is not rendered');
  assert(await page.locator('[data-id="topology::topo:division-1"]').count()===1,'division occurrence is not rendered');
  assert(await page.locator('[data-id="topology::topo:bond-1"]').count()===1,'bond-change occurrence is not rendered');

  const centralHasLocal = await page.evaluate(() => !!HV.roleContracts?.relationTypes?.['topo:DivisionRelation']);
  assert(!centralHasLocal,'DivisionRelation incorrectly appears in the shared scientific role schema');

  await page.locator('[data-id="topology::topo:division-1"]').click();
  let text=await page.locator('#roles').textContent();
  assert(text?.includes('topo:divisionParent'),'division inspector missing local parent RoleType identity');
  assert(text?.includes('topo:divisionChild'),'division inspector missing local child RoleType identity');
  assert(text?.includes('topo:topologyBefore')&&text?.includes('topo:topologyAfter'),'division inspector missing topology transition roles');

  await page.locator('[data-id="topology::topo:bond-1"]').click();
  text=await page.locator('#roles').textContent();
  assert(text?.includes('topo:bondEndpoint'),'bond inspector missing local endpoint RoleType');
  assert(text?.includes('left')&&text?.includes('right'),'bond endpoint qualifiers are not visible');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS dynamic topology: local RelationTypes/RoleTypes render and remain outside the shared schema');
} finally {await browser.close();server.close();}
