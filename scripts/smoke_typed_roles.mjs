#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_TYPED_ROLE_PORT||4179);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','mechanics');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});
  const relation=page.locator('[data-id="mechanics::h:ke-equation"]');
  assert(await relation.count()===1,'typed v2 kinetic-energy equation relation not rendered');
  await relation.click();
  const meta=await page.locator('#selMeta').textContent();
  assert(meta?.includes('scientific-hypergraph-v2'),`inspector did not identify v2 source model: ${meta}`);
  const text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:eqInput'),'inspector missing sci:eqInput RoleType identity');
  assert(text?.includes('input:mass'),'inspector missing mass qualifier');
  assert(text?.includes('input:velocity'),'inspector missing velocity qualifier');
  assert(text?.includes('sci:eqOutput'),'inspector missing sci:eqOutput RoleType identity');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS typed-role viewer: v2 mechanics exposes canonical RoleType identities and qualifiers');
} finally {await browser.close();server.close();}
