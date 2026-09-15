#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_SPDE_PORT||4183);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}const body=await readFile(file);res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(body);}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE}:{})});const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','spde');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});

  assert(await page.locator('[data-id="spde::h:noise-distribution"]').count()===1,'random-field DistributionRelation is not rendered');
  assert(await page.locator('[data-id="spde::h:spde"]').count()===1,'stochastic PDE EquationRelation is not rendered');
  assert(await page.locator('[data-id="spde::h:infer-kappa"]').count()===1,'SPDE parameter inference relation is not rendered');
  assert(await page.locator('[data-id="spde::h:kappa-fit"]').count()===1,'fitted diffusivity QuantityValueRelation is not rendered');

  await page.locator('[data-id="spde::h:spde"]').click();
  let text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:eqDriver')||text?.includes('driver'),'SPDE inspector missing stochastic driver RoleType');
  assert(text?.includes('noise-distribution')||text?.includes('Distribution'),'SPDE inspector does not expose the random-field distribution as driver');
  assert(text?.includes('boundary condition')||text?.includes('Boundary'),'SPDE inspector missing boundary conditions');
  assert(text?.includes('operator'),'SPDE inspector missing differential operator');

  await page.locator('[data-id="spde::h:infer-kappa"]').click();
  text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:analysisInput')||text?.includes('input'),'inference inspector missing analysis-input RoleType');
  assert(text?.includes('observed field samples'),'inference inspector missing measured field input');
  assert(text?.includes('sci:analysisOutput')||text?.includes('output'),'inference inspector missing analysis-output RoleType');
  assert(text?.includes('sci:QuantityValueRelation')||text?.includes('QuantityValue Relation')||text?.includes('Quantity Value'),'inference inspector does not expose a canonical QuantityValue relation as output');
  assert(text?.includes('sci:analysisUncertainty')||text?.includes('uncertainty'),'inference inspector missing uncertainty RoleType');

  await page.locator('[data-id="spde::h:kappa-fit"]').click();
  text=await page.locator('#roles').textContent();
  assert(text?.includes('sci:numericalValue')||text?.includes('numerical value'),'fitted diffusivity relation missing numerical-value RoleType');
  assert(text?.includes('0.207'),'fitted diffusivity relation missing value 0.207');
  assert(text?.includes('±0.012'),'fitted diffusivity relation missing uncertainty value');

  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log('PASS stochastic PDE: random-field driver, PDE structure, measurement and diffusivity inference render compositionally');
} finally {await browser.close();server.close();}
