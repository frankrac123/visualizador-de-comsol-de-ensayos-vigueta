import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'..');
const record=JSON.parse(fs.readFileSync(path.join(root,'comsol/resultados_referencia/integridad_datos.json')));
test('Todos los datos publicados conservan los bytes de la entrega original',()=>{
 for(const [name,expected] of Object.entries(record.files)){
  const raw=fs.readFileSync(path.join(root,name));assert.equal(raw.length,expected.bytes,name);
  assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),expected.sha256,name);
 }
});
test('Extracción independiente CZM conserva el archivo científico de referencia',()=>{
 const raw=fs.readFileSync(path.join(root,'comsol/resultados_referencia/resultados.json'));
 assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),record.reference_results_sha256);
});
