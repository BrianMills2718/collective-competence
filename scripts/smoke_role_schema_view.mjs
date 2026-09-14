#!/usr/bin/env node
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const PORT=Number(process.env.HYPERGRAPH_ROLE_SCHEMA_PORT||4180);
const VIEWER='/wiki/reference/metamodel/hypergraph-viewer.html';
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.jsonld':'application/ld+json; charset=utf-8'};
function safePath(urlPath){const pathname=decodeURIComponent(new URL(urlPath,`http://127.0.0.1:${PORT}`).pathname),resolved=path.resolve(ROOT,`.${pathname}`);return resolved.startsWith(ROOT+path.sep)||resolved===ROOT?resolved:null;}
async function serve(req,res){const file=safePath(req.url||'/');if(!file||!existsSync(file)){res.writeHead(404);res.end('not found');return;}res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(await readFile(file));}
function assert(ok,msg){if(!ok)throw new Error(msg);}
const server=createServer((req,res)=>void serve(req,res));await new Promise(r=>server.listen(PORT,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1900,height:1200}});const errors=[];page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
try{
  await page.goto(`http://127.0.0.1:${PORT}${VIEWER}`,{waitUntil:'domcontentloaded'});
  await page.selectOption('#fixture','roleSchema');
  await page.waitForFunction(()=>/elements/.test(document.querySelector('#status')?.textContent||''),null,{timeout:15000});
  const counts=await page.evaluate(()=>({nodes:document.querySelectorAll('#viewport .node').length,relations:document.querySelectorAll('#viewport .relation').length}));
  assert(counts.nodes===121,`expected 121 role-schema nodes, found ${counts.nodes}`);
  assert(counts.relations===90,`expected 90 declaresRole relations, found ${counts.relations}`);
  assert(await page.locator('[data-id="sci:EquationRelation"]').count()===1,'Equation RelationType node missing');
  assert(await page.locator('[data-id="sci:eqInput"]').count()===1,'eqInput RoleType node missing');
  assert(await page.locator('[data-id="decl:sci-EquationRelation:sci-eqInput"]').count()===1,'Equation eqInput declaration relation missing');
  assert(await page.locator('[data-id="sci:RelationType"]').count()===1,'RelationType meta-type missing');
  assert(await page.locator('[data-id="sci:RoleType"]').count()===1,'RoleType meta-type missing');
  assert(await page.locator('#viewport .type-trunk').count()>=3,'expected bundled declaresRole + compact instanceOf type trunks');

  const overlap=await page.evaluate(()=>{const xs=[...document.querySelectorAll('#viewport .node-shape,#viewport .relation-shape')].map(e=>({id:e.parentElement?.dataset.id,r:e.getBoundingClientRect()})).filter(x=>x.id);let severe=0,worst=0,pair=null;for(let i=0;i<xs.length;i++)for(let j=i+1;j<xs.length;j++){const a=xs[i].r,b=xs[j].r,ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left)),iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)),area=ix*iy;if(!area)continue;const ratio=area/(Math.min(a.width*a.height,b.width*b.height)||1);if(ratio>.35)severe++;if(ratio>worst){worst=ratio;pair=[xs[i].id,xs[j].id]}}return{severe,worst,pair};});
  assert(overlap.severe===0,`severe metamodel shape collisions: ${JSON.stringify(overlap)}`);

  await page.locator('[data-id="decl:sci-EquationRelation:sci-eqInput"]').click();
  const inspector=await page.locator('#roles').textContent();
  assert(inspector?.includes('declaredRelationType'),'declaration inspector missing declaredRelationType bootstrap role');
  assert(inspector?.includes('sci:declaredRoleType'),'declaration inspector missing declaredRoleType identity');
  assert(inspector?.includes('Equation Relation'),'declaration inspector missing Equation RelationType participant');
  assert(inspector?.includes('input'),'declaration inspector missing eqInput participant');

  await page.locator('#search').fill('Equation');
  assert(await page.locator('#viewport .dim').count()>0,'metamodel search did not dim nonmatches');
  assert(errors.length===0,`browser errors: ${errors.join('\n')}`);
  console.log(`PASS self-hosted role schema viewer: ${counts.nodes} nodes / ${counts.relations} declarations; severe overlap=0; worst=${(overlap.worst*100).toFixed(1)}%`);
}finally{await browser.close();server.close();}
