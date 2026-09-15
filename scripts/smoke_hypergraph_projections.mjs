#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const PORT = Number(process.env.HYPERGRAPH_PROJECTION_SMOKE_PORT || 4178);
const VIEWER = '/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>{void serve(req,res);});await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});const page=await browser.newPage({viewport:{width:1800,height:1200}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:20000});
  const options=await page.locator('#projection option').count();assert(options===9,`expected 9 projection options, found ${options}`);
  const overviewCount=await page.locator('#viewport .node,#viewport .relation').count();assert(overviewCount>250,`unexpectedly small eight-fixture overview: ${overviewCount}`);
  const bundles=await page.locator('#viewport .bundle-junction').count();assert(bundles>0,'type-edge bundling inactive in overview');

  for(const mode of ['theory','measurement','probability','representation','access','evidence','identifiability','typing']){
    await page.selectOption('#projection',mode);
    await page.waitForFunction(m=>(document.querySelector('#status')?.textContent||'').includes(m),mode,{timeout:12000});
    const count=await page.locator('#viewport .node,#viewport .relation').count();
    assert(count>0,`${mode} projection is empty`);
    if(mode!=='typing') assert(count<overviewCount,`${mode} projection did not reduce the graph: ${count} >= ${overviewCount}`);
    else assert(count>overviewCount,`typing projection should expose normalized typing infrastructure: ${count} <= ${overviewCount}`);
    const disabled=await page.evaluate(()=>({layer:document.querySelector('#layer')?.disabled,type:document.querySelector('#relationType')?.disabled}));
    assert(disabled.layer&&disabled.type,`${mode} projection should disable manual layer/type filters`);
    const hasId=async (...ids)=>{for(const id of ids)if(await page.locator(`[data-id="${id}"]`).count())return true;return false;};
    if(mode==='measurement') assert(await hasId('sci:MeasurementRelation','schema:Measurement'),'measurement projection missing Measurement relation type');
    if(mode==='probability') assert(await hasId('sci:DistributionRelation','schema:Distribution'),'probability projection missing Distribution relation type');
    if(mode==='representation') assert(await hasId('sci:RepresentationRelation','schema:Representation'),'representation projection missing Representation relation type');
    if(mode==='access') assert(await hasId('sci:AccessRelation','schema:StudyView'),'access projection missing Access relation type');
    if(mode==='identifiability') assert(await hasId('sci:IdentifiabilityRelation','schema:Identifiability'),'identifiability projection missing Identifiability relation type');
    if(mode==='typing'){const typed=await page.evaluate(()=>window.HV.state.view.hyperedges.filter(e=>window.HV.canonicalRelationType(e.type)==='sci:instanceOf').length);assert(typed>0,'typing projection missing canonical instanceOf relations');}
    console.log(`PASS projection ${mode}: ${count} rendered items`);
  }

  await page.selectOption('#projection','all');
  await page.waitForFunction(()=>/overview/.test(document.querySelector('#status')?.textContent||''),null,{timeout:12000});
  const enabled=await page.evaluate(()=>({layer:!document.querySelector('#layer')?.disabled,type:!document.querySelector('#relationType')?.disabled}));
  assert(enabled.layer&&enabled.type,'overview should re-enable manual layer/type filters');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log(`PASS named projections and type bundling: overview=${overviewCount}, bundle junctions=${bundles}`);
} finally {await browser.close();server.close();}
