import {test,expect} from '@playwright/test';
import fs from 'node:fs';
const m=JSON.parse(fs.readFileSync('public/data/fracture/manifest.json','utf8'));
const state=async(page:any)=>page.evaluate(()=>(window as any).__lab);
test('CZM carga sus campos y sincroniza apertura, energía, gráficas y tabla',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('/');await expect(page.locator('.app-shell')).toBeVisible();await expect(page.getByTestId('opening-value')).toHaveText('No disponible');
 await page.getByLabel('Modelo físico').selectOption('fracture');await expect.poll(async()=>(await state(page))?.modelId).toBe('fracture');
 await page.getByRole('button',{name:'Ver pico',exact:true}).click();await expect.poll(async()=>(await state(page))?.state.id).toBe(m.peakIndex+1);const s=await state(page);expect(s.state.load_kN).toBeCloseTo(m.states[m.peakIndex].load_kN,10);expect(s.fieldValues).toBe(m.mesh.nodes*5);expect(s.cohesiveValues).toBe(m.cohesive.points*5);
 await page.getByRole('button',{name:'Fractura cohesiva',exact:true}).click();await page.getByRole('button',{name:'×25',exact:true}).click();await page.getByRole('button',{name:'Acercar a la interfaz calculada'}).click();
 await expect(page.getByText('Visualización 3D de resultados FEM 2D.',{exact:true})).toBeVisible();for(const p of ['load-opening','energy','damage','load-deflection'])await page.getByLabel('Seleccionar gráfica').selectOption(p);
 await page.getByTestId('load-input').fill('14.5');await page.getByRole('button',{name:'Aplicar carga'}).click();if(m.states[m.peakIndex].load_kN<14.5)await expect(page.getByRole('status')).toContainText('fuera');
 await page.getByRole('button',{name:'Tabla y procedencia'}).click();await expect(page.locator('tbody tr')).toHaveCount(m.states.length);await expect(page.locator('thead')).toContainText('Apertura');await page.getByRole('button',{name:'×',exact:true}).click();
 await page.getByLabel('Número de estado').fill(String(m.states.length));await expect.poll(async()=>(await state(page))?.state.id).toBe(m.states.length);expect((await state(page)).state.opening_mm).toBeCloseTo(m.states.at(-1).opening_mm,10);expect((await state(page)).state.fractureEnergy_J).toBeCloseTo(m.states.at(-1).fractureEnergy_J,10);
 for(const p of ['load-control','mesh','sensitivity'])await page.getByLabel('Seleccionar gráfica').selectOption(p);await page.getByLabel('Seleccionar gráfica').selectOption('load-deflection');
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'CSV',exact:true}).click();const file=await download;expect(file.suggestedFilename()).toBe(`CONCRETE_LAB_fracture_${m.states.length}_estados.csv`);const csv=fs.readFileSync((await file.path())!,'utf8');expect(csv.trim().split('\n')).toHaveLength(m.states.length+1);expect(csv).toContain(String(m.states.at(-1).fractureEnergy_J));
 await page.evaluate(()=>document.querySelectorAll('.control-panel,.metrics-panel').forEach(p=>p.scrollTop=0));await page.screenshot({path:'validation/etapa_II/fractura_avanzada.png'});expect(errors).toEqual([]);
});
test('Cambios rápidos de modelo no mezclan campos y comparación identifica la escena',async({page})=>{
 await page.goto('/');await expect(page.locator('.app-shell')).toBeVisible();await page.getByLabel('Modelo físico').selectOption('comparison');await expect.poll(async()=>(await state(page))?.modelId).toBe('mazars');await expect(page.getByRole('heading',{name:'Comparación · escena Mazars'})).toBeVisible();await expect(page.getByLabel('Seleccionar gráfica')).toHaveValue('compare-models');
 await page.getByLabel('Modelo físico').selectOption('fracture');await expect.poll(async()=>(await state(page))?.modelId).toBe('fracture');await page.getByRole('button',{name:'Ver pico',exact:true}).click();await page.getByLabel('Modelo físico').selectOption('mazars');await expect.poll(async()=>(await state(page))?.modelId).toBe('mazars');const s=await state(page);expect(s.cohesiveValues).toBe(0);expect(s.fieldValues).toBe(14526*5);await expect(page.getByTestId('opening-value')).toHaveText('No disponible');
});
