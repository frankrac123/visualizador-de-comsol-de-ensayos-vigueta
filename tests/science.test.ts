import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {strainPercent,newtonsToKilonewtons,selectLoad,selectDeflection,interpolateCompatible,validateManifest,branchIndices,type Manifest} from '../src/science.ts';
const root=path.resolve(import.meta.dirname,'..');
const nativeRoot=process.env.COMSOL_PROJECT_DIR;

const m=JSON.parse(fs.readFileSync(path.join(root,'public/data/manifest.json'),'utf8')) as Manifest;
test('Serie completa coincide con la entrega COMSOL',()=>{validateManifest(m);assert.equal(m.states.length,127);assert.ok(Math.abs(m.states[m.peakIndex].load_kN-14.507659947165633)<1e-10);assert.ok(Math.abs(m.states[m.peakIndex].deflection_mm-.20831018528165818)<1e-12);assert.ok(Math.abs(m.states.at(-1)!.load_kN-13.4657736181)<1e-8);assert.ok(Math.abs(m.states.at(-1)!.deflection_mm-.4233503464)<1e-9);});
test('Conversiones de unidades',()=>{assert.equal(newtonsToKilonewtons(14500),14.5);assert.equal(strainPercent(.001),.1);assert.equal(strainPercent(-.002),-.2);});
test('Carga repetida selecciona ramas distintas',()=>{const a=selectLoad(m,14.0,'ascending'),b=selectLoad(m,14.0,'descending');assert.equal(a.error,undefined);assert.equal(b.error,undefined);assert.ok(a.index<m.peakIndex);assert.ok(b.index>m.peakIndex);assert.notEqual(a.index,b.index);});
test('El pico está disponible en ambas ramas',()=>{const p=m.states[m.peakIndex].load_kN;assert.equal(selectLoad(m,p,'ascending').index,m.peakIndex);assert.equal(selectLoad(m,p,'descending').index,m.peakIndex);});
test('Cargas y flechas fuera del rango se rechazan',()=>{assert.equal(selectLoad(m,5,'descending').index,-1);assert.equal(selectLoad(m,15,'ascending').index,-1);assert.equal(selectLoad(m,NaN,'ascending').index,-1);assert.equal(selectDeflection(m,-1),-1);assert.equal(selectDeflection(m,1),-1);});
test('Selección manual retorna un estado almacenado',()=>{for(const p of [5,10,14.5]){const result=selectLoad(m,p,'ascending');assert.ok(result.index>=0);assert.ok(m.states.includes(m.states[result.index]));assert.equal(m.states[result.index].id,result.index+1);}assert.equal(selectDeflection(m,m.states[97].deflection_mm),97);});
test('Interpolación limitada, declarada estimación y sin cruce de rama',()=>{const a=m.states[20],b=m.states[21],r=interpolateCompatible(a,b,.5);assert.equal(r.estimated,true);assert.equal(r.load_kN,(a.load_kN+b.load_kN)/2);assert.throws(()=>interpolateCompatible(a,b,1.01));assert.throws(()=>interpolateCompatible(a,m.states[23],.5));assert.throws(()=>interpolateCompatible(m.states[m.peakIndex],m.states[m.peakIndex+1],.5));});
test('Campos y malla exportados completos y finitos',()=>{const nodes=m.mesh.nodes;assert.equal(fs.statSync(path.join(root,'public/data',m.mesh.coordinates)).size,nodes*2*4);const bytes=fs.readFileSync(path.join(root,'public/data',m.mesh.connectivity));const triangles=new Uint32Array(bytes.buffer,bytes.byteOffset,bytes.length/4);assert.equal(triangles.length,m.mesh.triangles*3);assert.ok(triangles.every(v=>v<nodes));for(const s of m.states){const data=fs.readFileSync(path.join(root,'public/data',s.fields));assert.equal(data.length,nodes*5*4);const fields=new Float32Array(data.buffer,data.byteOffset,data.length/4);assert.ok(fields.every(Number.isFinite));for(let i=0;i<nodes;i++)assert.ok(fields[i*5+2]>=-1e-7&&fields[i*5+2]<=1.000001);assert.ok(Math.abs(s.reactionLeft_kN+s.reactionRight_kN-s.load_kN)<.001*s.load_kN);}assert.ok(triangles.length>0);});
test('Fuentes conservan sus SHA-256',{skip:!nativeRoot},async()=>{const crypto=await import('node:crypto');for(const source of m.sources){const p=path.resolve(nativeRoot!,source.path);const hash=crypto.createHash('sha256');for await(const chunk of fs.createReadStream(p))hash.update(chunk);assert.equal(hash.digest('hex'),source.sha256);}});
test('Rama posterior termina en el último estado aceptado',()=>{const indices=branchIndices(m,'descending');assert.equal(indices.at(-1),126);assert.ok(indices.every(i=>i>=m.peakIndex));assert.equal(m.states[126].branch,'descending');});
test('Fractura conserva caras distintas y campos independientes de Mazars',()=>{
 const dir=path.join(root,'public/data/fracture'),b=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8')) as Manifest;validateManifest(b);assert.equal(b.modelId,'fracture');assert.ok(b.halfNodeCount!>0&&b.halfNodeCount!<b.mesh.nodes);assert.notEqual(b.sources[0].sha256,m.sources[0].sha256);
 const bytes=fs.readFileSync(path.join(dir,b.mesh.connectivity)),tri=new Uint32Array(bytes.buffer,bytes.byteOffset,bytes.length/4),half=b.halfNodeCount!;
 for(let i=0;i<tri.length;i+=3)assert.ok([tri[i],tri[i+1],tri[i+2]].every(n=>n<half)||[tri[i],tri[i+1],tri[i+2]].every(n=>n>=half),'Una cara se fusionó con la otra');
 for(const s of b.states){const raw=fs.readFileSync(path.join(dir,s.fields)),f=new Float32Array(raw.buffer,raw.byteOffset,raw.length/4);assert.equal(f.length,b.mesh.nodes*5);assert.ok(f.every(Number.isFinite));const cb=fs.readFileSync(path.join(dir,s.cohesiveFields!)),c=new Float32Array(cb.buffer,cb.byteOffset,cb.length/4);assert.equal(c.length,b.cohesive!.points*5);assert.ok(c.every(Number.isFinite));for(let k=0;k<c.length;k+=5)assert.ok(c[k]>=0&&c[k]<=1);assert.ok(Math.abs(Math.max(...Array.from(c).filter((_,i)=>i%5===0))-s.damageMax)<1e-7);assert.ok(s.opening_mm!>=0);assert.ok(s.fractureEnergy_J!>=0);}
 assert.equal(m.states[0].opening_mm,undefined);assert.equal(m.states[0].fractureEnergy_J,undefined);
});
test('Selección de carga usa la serie propia del CZM y rechaza extrapolar 14,5 kN',()=>{
 const b=JSON.parse(fs.readFileSync(path.join(root,'public/data/fracture/manifest.json'),'utf8')) as Manifest;const r=selectLoad(b,5,'ascending');assert.ok(r.index>=0);assert.equal(b.states[r.index].source,b.sources[0].path);assert.ok(Math.abs(b.states[r.index].load_kN-5)<1);if(b.states[b.peakIndex].load_kN<14.5)assert.equal(selectLoad(b,14.5,'ascending').index,-1);
});
test('Apertura CZM coincide con el salto FEM de las dos caras inferiores',()=>{
 const dir=path.join(root,'public/data/fracture'),b=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8')) as Manifest;
 const raw=fs.readFileSync(path.join(dir,b.mesh.coordinates)),xy=new Float32Array(raw.buffer,raw.byteOffset,raw.length/4);const lower:number[]=[];
 for(let i=0;i<b.mesh.nodes;i++)if(Math.abs(xy[2*i])<1e-7&&Math.abs(xy[2*i+1])<1e-7)lower.push(i);assert.equal(lower.length,2);assert.ok(lower[0]<b.halfNodeCount!&&lower[1]>=b.halfNodeCount!);
 for(const s of b.states){const data=fs.readFileSync(path.join(dir,s.fields)),f=new Float32Array(data.buffer,data.byteOffset,data.length/4);assert.ok(Math.abs(f[5*lower[1]]-f[5*lower[0]]-s.opening_mm!)<2e-7);for(let i=0;i<b.mesh.nodes;i++)assert.equal(f[5*i+2],0,'El volumen elastico no debe llevar daño fabricado');}
});
test('Serie CZM y energía del visor coinciden con la extracción COMSOL independiente',()=>{
 const b=JSON.parse(fs.readFileSync(path.join(root,'public/data/fracture/manifest.json'),'utf8')) as Manifest;const r=JSON.parse(fs.readFileSync(path.join(root,'comsol/resultados_referencia/resultados.json'),'utf8'));const v=r.variables;
 assert.ok(r.exact_energy_verification.max_relative_residual_percent<2);
 for(const [i,s] of b.states.entries()){assert.equal(s.load_kN,v.load_kN[i]);assert.equal(s.deflection_mm,v.deflection_mm[i]);assert.equal(s.opening_mm,v.cmod_mm[i]);assert.equal(s.fractureEnergy_J,v.constitutive_dissipation_exact_J[i]);assert.equal(s.reactionLeft_kN,v.reaction_bl_N[i]/1000);}
});
test('Modelo CZM fuente conserva su SHA-256 después del posprocesado',{skip:!nativeRoot},async()=>{
 const crypto=await import('node:crypto');const b=JSON.parse(fs.readFileSync(path.join(root,'public/data/fracture/manifest.json'),'utf8')) as Manifest;
 for(const source of b.sources){const hash=crypto.createHash('sha256');for await(const chunk of fs.createReadStream(path.resolve(nativeRoot!,source.path)))hash.update(chunk);assert.equal(hash.digest('hex'),source.sha256);}
});
