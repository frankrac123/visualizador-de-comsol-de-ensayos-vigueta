import {test,expect} from '@playwright/test';
import fs from 'node:fs';
const snapshot=async(page:any)=>page.evaluate(()=>(window as any).__lab);
test('Sincronización, selección por rama y todos los modos',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/');await expect(page.locator('.app-shell')).toBeVisible();
  await page.getByTestId('load-input').fill('5');await page.getByRole('button',{name:'Aplicar carga'}).click();await expect(page.getByRole('status')).toContainText('Solicitada 5');await expect.poll(async()=>(await snapshot(page))?.state.load_kN).toBeGreaterThan(4.5);
  let a=await snapshot(page);expect(a.state.load_kN).toBeLessThan(5.5);expect(a.fieldValues).toBeGreaterThan(60000);
  await page.getByRole('button',{name:'Ver pico'}).click();await expect.poll(async()=>(await snapshot(page))?.state.id).toBe(98);a=await snapshot(page);expect(a.state.load_kN).toBeCloseTo(14.507659947,8);expect(a.state.deflection_mm).toBeCloseTo(.208310185,8);
  for(const label of ['Esfuerzos','Deformaciones','Daño','Deformada amplificada','Comparar deformadas','Material realista'])await page.getByRole('button',{name:label,exact:true}).click();
  await page.getByRole('button',{name:'×25',exact:true}).click();await expect(page.locator('.amplification')).toContainText('amplificados');
  await page.getByRole('button',{name:'↘ Descendente'}).click();await page.getByTestId('load-input').fill('5');await page.getByRole('button',{name:'Aplicar carga'}).click();await expect(page.getByRole('status')).toContainText('fuera');expect((await snapshot(page)).state.id).toBe(98);
  await page.getByTestId('load-input').fill('14');await page.getByRole('button',{name:'Aplicar carga'}).click();await expect.poll(async()=>(await snapshot(page))?.state.branch).toBe('descending');
  for(const value of ['load-extension','damage','local','displacement','reactions','mesh','weight','load-deflection'])await page.getByLabel('Seleccionar gráfica').selectOption(value);
  await page.getByRole('button',{name:'Cambiar tema'}).click();await expect(page.locator('html')).toHaveAttribute('data-theme','dark');await page.getByRole('button',{name:'Cambiar tema'}).click();
  await page.getByRole('button',{name:'Información científica'}).click();await expect(page.getByRole('dialog')).toContainText('extrusión');await page.getByRole('button',{name:'Volver al laboratorio'}).click();
  await page.getByRole('button',{name:'Tabla y procedencia'}).click();await expect(page.locator('tbody tr')).toHaveCount(127);await page.getByRole('button',{name:'×',exact:true}).click();
  await page.getByRole('button',{name:'Ver pico'}).click();await expect.poll(async()=>(await snapshot(page)).state.id).toBe(98);await page.getByRole('button',{name:'Daño',exact:true}).click();await page.evaluate(()=>document.querySelectorAll('.control-panel,.metrics-panel').forEach(el=>{el.scrollTop=0;}));await page.screenshot({path:'validation/etapa_II/laboratorio_pico.png'});
  expect(errors).toEqual([]);
});
test('Reproducción hasta el final y vuelta atrás sin estados inventados',async({page})=>{
  await page.goto('/');await expect(page.locator('.app-shell')).toBeVisible();await page.getByLabel('Velocidad de reproducción').selectOption('24');await page.getByRole('button',{name:'Iniciar ensayo',exact:true}).click();await expect.poll(async()=>(await snapshot(page))?.state.id,{timeout:20000}).toBe(127);await expect.poll(async()=>(await snapshot(page)).playing).toBe(false);let s=await snapshot(page);expect(s.state.load_kN).toBeCloseTo(13.4657736181,7);expect(s.state.deflection_mm).toBeCloseTo(.4233503464,8);
  await page.getByRole('button',{name:'Estado anterior'}).click();await expect.poll(async()=>(await snapshot(page)).state.id).toBe(126);await page.getByLabel('Dirección de reproducción').selectOption('-1');await page.getByRole('button',{name:'Iniciar ensayo',exact:true}).click();await expect.poll(async()=>(await snapshot(page)).state.id,{timeout:20000}).toBe(1);await expect.poll(async()=>(await snapshot(page)).playing).toBe(false);await page.screenshot({path:'validation/etapa_II/laboratorio_inicio.png'});
});
test('Exportación real PNG, SVG, CSV, Excel y PDF',async({page})=>{
  fs.mkdirSync('validation/etapa_II',{recursive:true});await page.goto('/');await expect(page.locator('.app-shell')).toBeVisible();await page.getByRole('button',{name:'Ver pico'}).click();await expect.poll(async()=>(await snapshot(page)).state.id).toBe(98);
  for(const name of ['PNG','SVG','CSV','Excel','Informe PDF']){const pending=page.waitForEvent('download');await page.getByRole('button',{name,exact:true}).click();const download=await pending;await download.saveAs('validation/etapa_II/'+download.suggestedFilename());expect(await download.failure()).toBeNull();}
  expect(fs.readFileSync('validation/etapa_II/CONCRETE_LAB_grafica.svg','utf8')).toContain('<svg');expect(fs.readFileSync('validation/etapa_II/CONCRETE_LAB_mazars_127_estados.csv','utf8').split('\n')).toHaveLength(128);expect(fs.statSync('validation/etapa_II/CONCRETE_LAB_estado_98.pdf').size).toBeGreaterThan(10000);expect(fs.statSync('validation/etapa_II/CONCRETE_LAB_resultados.xlsx').size).toBeGreaterThan(10000);
});
