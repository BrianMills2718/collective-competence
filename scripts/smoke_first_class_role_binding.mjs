#!/usr/bin/env node
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_BINDING_PORT||4184);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}

const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1500,height:1000}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','binding');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});

  const binding='binding::binding:analysis-model';
  const claim='binding::h:model-assignment-claim';
  assert(await page.locator(`[data-id="${binding}"]`).count()===1,'addressable RoleBinding node did not render');
  assert(await page.locator(`[data-id="${claim}"]`).count()===1,'binding-scoped claim did not render');

  await page.locator(`[data-id="${claim}"]`).click();
  let text=await page.locator('#roles').textContent();
  assert(text?.includes('claimScope')||text?.includes('scope'),'claim inspector missing scope RoleType');
  assert(text?.includes('analysis model')||text?.includes('analysis-model'),'claim scope does not resolve to the addressable binding');

  await page.locator(`[data-id="${binding}"]`).click();
  text=await page.locator('#roles').textContent();
  assert((await page.locator('#selMeta').textContent())?.includes('roleBinding'),'binding inspector does not identify RoleBinding kind');
  assert(text?.includes('analysis model')||text?.includes('analysisModel'),'binding inspector missing canonical RoleType');
  assert(text?.includes('candidate model A'),'binding inspector missing bound participant');
  assert(text?.includes('h:analysis')||text?.includes('Analysis'),'binding inspector missing parent relation');
  assert(text?.includes('Claim')||text?.includes('claim'),'binding inspector missing inbound claim targeting the assignment');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS first-class RoleBinding viewer: claim targets one addressable assignment and binding inspector exposes parent/role/participant/inbound claim');
} finally {await browser.close();server.close();}
