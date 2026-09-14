#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..'),PORT=4181;
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safe(u){const p=decodeURIComponent(new URL(u,`http://127.0.0.1:${PORT}`).pathname),r=path.resolve(ROOT,`.${p}`);return r.startsWith(ROOT+path.sep)||r===ROOT?r:null;}
async function serve(req,res){const f=safe(req.url||'/');if(!f||!existsSync(f)){res.writeHead(404);res.end('not found');return;}res.writeHead(200,{'content-type':MIME[path.extname(f)]||'application/octet-stream','cache-control':'no-store'});res.end(await readFile(f));}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1600,height:1000}}),errors=[];
page.on('console',m=>{if(m.type()==='error')errors.push(`console: ${m.text()}`)});page.on('pageerror',e=>errors.push(`pageerror: ${e.stack||e}`));
try{
  await page.goto(`http://127.0.0.1:${PORT}/wiki/reference/metamodel/hypergraph-viewer.html`,{waitUntil:'domcontentloaded'});
  await page.waitForTimeout(2500);
  const info=await page.evaluate(()=>({
    status:document.querySelector('#status')?.textContent||'',
    fixture:document.querySelector('#fixture')?.value||'',
    renderedNodes:document.querySelectorAll('#viewport .node').length,
    renderedRelations:document.querySelectorAll('#viewport .relation').length,
    dataNodes:window.HV?.state?.data?.nodes?.length||0,
    dataRelations:window.HV?.state?.data?.hyperedges?.length||0,
    sourceModels:[...new Set((window.HV?.state?.data?.hyperedges||[]).map(e=>e.sourceModel).filter(Boolean))],
    v0Relations:(window.HV?.state?.data?.hyperedges||[]).filter(e=>e.sourceModel==='scientific-hypergraph-v0').length,
    v1Relations:(window.HV?.state?.data?.hyperedges||[]).filter(e=>e.sourceModel==='scientific-hypergraph-v1').length,
    fixturePaths:window.HV?.FIXTURES||{},
  }));
  console.log(JSON.stringify(info,null,2));
  if(errors.length)console.error(errors.join('\n'));
  if(/Load failed|Layout failed/.test(info.status)||errors.length||!info.renderedNodes||!info.renderedRelations)process.exitCode=1;
  if(info.v0Relations!==0){console.error(`Expected v1-only built-ins but found ${info.v0Relations} normalized v0 relations`);process.exitCode=1;}
} finally {await browser.close();server.close();}
