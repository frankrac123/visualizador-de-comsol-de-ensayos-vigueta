"""Prepare native-series comparisons, figures, CSV and independent viewer catalog."""
from pathlib import Path
import csv,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':12,'axes.labelsize':13,'axes.titlesize':13,'xtick.labelsize':11,'ytick.labelsize':11})
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'05_Resultados';APP=ROOT.parents[1]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
cases=json.loads((OUT/'verificacion_viguetas.json').read_text(encoding='utf-8'))
accepted=[c for c in cases if '_o' in c['folder']]
for c in accepted:
    r=json.loads((ROOT/c['folder']/'resultados.json').read_text(encoding='utf-8'))
    assert c['all_checks_pass'] and r['interface_verification']['all_checks_pass'],c['folder']
    c['interface_verification']=r['interface_verification'];c['energy_method_verification']=r['exact_energy_method']
mesh=sorted([c for c in accepted if c['last_opening_mm']>.59],key=lambda x:x['configuration']['mesh'],reverse=True)
assert len(mesh)==3
series=[json.loads((ROOT/c['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'] for c in mesh]
for s in series[1:]:assert np.allclose(series[0]['cmod_mm'],s['cmod_mm'],rtol=0,atol=1e-12)
ref=np.array(series[-1]['load_kN']);peaks=np.array([c['peak_kN'] for c in mesh]);mstats={'meshes_mm':[c['configuration']['mesh'] for c in mesh],'identical_native_opening_grid':True,'peak_spread_percent_of_fine':float((peaks.max()-peaks.min())/peaks[-1]*100),'max_curve_difference_percent_of_fine_peak':[float(np.max(abs(np.array(s['load_kN'])-ref))/peaks[-1]*100) for s in series],'rms_curve_difference_kN':[float(np.sqrt(np.mean((np.array(s['load_kN'])-ref)**2))) for s in series],'interpretation':'Three-level trend for this prescribed crack, local contact sizes unchanged. Not a universal convergence order or experimental validation.'}
base=mesh[0];basev=series[0];bmanifestpath=APP/'public/data/fracture/manifest.json';b=json.loads(bmanifestpath.read_text(encoding='utf-8'));assert len(b['states'])==345
matched=[c for c in accepted if c['last_opening_mm']==.3 and c['configuration']['ft']==.87851483 and c['configuration']['gf']==220 and c['configuration']['kn']==1e14]
matchedv=json.loads((ROOT/matched[0]['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'] if matched else None
protocol=None
if matchedv:
    fine_lookup={round(x,12):i for i,x in enumerate(basev['cmod_mm'])};pairs=[(i,fine_lookup[round(x,12)]) for i,x in enumerate(matchedv['cmod_mm']) if round(x,12) in fine_lookup]
    protocol={'steps_mm':[.002,.003],'common_native_control_states':len(pairs),'no_interpolation':True,'max_load_difference_kN_at_common_native_controls':max(abs(matchedv['load_kN'][i]-basev['load_kN'][k]) for i,k in pairs),'peak_difference_percent':100*(matched[0]['peak_kN']/base['peak_kN']-1)}
comparisons=[]
for c in accepted:
    if c is base:continue
    cfg=c['configuration'];v=json.loads((ROOT/c['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'];is_mesh=c in mesh
    label=f'CZM h={cfg["mesh"]:g} mm' if is_mesh else ('Referencia · paso 0,003 mm' if c in matched else f'Gf={cfg["gf"]:g} J/m²' if cfg['gf']!=220 else f'ft={cfg["ft"]:.4f} MPa' if cfg['ft']!=.87851483 else f'Kn={cfg["kn"]:.1e} N/m³')
    source=(ROOT/c['folder']/'vigueta_fractura.mph');comparisons.append({'id':source.parent.name,'label':label,'kind':'mesh' if is_mesh else 'sensitivity','load_kN':v['load_kN'],'deflection_mm':v['deflection_mm'],'extension_mm':v['gauge_mm'],'opening_mm':v['cmod_mm'],'source':source.relative_to(ROOT.parent).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'note':f'Native COMSOL states; CMOD last {c["last_opening_mm"]:g} mm. One parameter changed per sensitivity; comparisons require a common control range.'})
for state in b['states']:state['uid']=f'fracture:{b["sources"][0]["sha256"]}:{state["solution"]}'
b['cases']=comparisons;b['numericalVerification']={'status':'Equilibrio · energía · irreversibilidad','meshes':mstats,'experimentalValidation':False};b['cohesive']['fieldsOrder'][3]='native_explicit_accumulation_J_m2'
dump(bmanifestpath,b);dump(OUT/'visor_fractura_avanzada/manifest.json',b)
dump(APP/'public/data/model_catalog.json',{'mazars':{'available':True,'manifest':'manifest.json','states':127,'status':'original_preserved'},'fracture':{'available':True,'manifest':'fracture/manifest.json','states':345,'status':'native_CZM_verified_prescribed_path_elastic_bulk_not_experimentally_validated'}})
for c in accepted:
    v=json.loads((ROOT/c['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'];path=ROOT/c['folder']/'serie_global.csv';keys=list(v)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['native_state',*keys]);w.writerows([[i+1,*[v[k][i] for k in keys]] for i in range(c['states'])])
fig,axs=plt.subplots(1,3,figsize=(10.5,3.8))
for c,v in zip(mesh,series):
    name=f'h={c["configuration"]["mesh"]:g} mm';axs[0].plot(v['cmod_mm'],v['load_kN'],label=name);axs[1].plot(v['cmod_mm'],v['deflection_mm'],label=name);axs[2].plot(v['cmod_mm'],v['constitutive_dissipation_exact_J'],label=name)
for ax,y in zip(axs,['Carga total (kN)','Flecha central (mm)','Disipación cohesiva (J)']):ax.set(xlabel='Apertura inferior FEM (mm)',ylabel=y);ax.grid(alpha=.25);ax.legend(fontsize=10)
fig.suptitle('Tres mallas: mismo control, parámetros y trayectoria prescrita');fig.tight_layout();fig.savefig(OUT/'mallas_CZM.png',dpi=180);fig.savefig(OUT/'mallas_CZM.svg');plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(10.5,3.8))
for ax,param,title in zip(axs,['gf','ft','kn'],['Energía de fractura','Resistencia a tracción','Rigidez cohesiva']):
    rv=matchedv or basev;mask=np.array(rv['cmod_mm'])<=.3+1e-10;ax.plot(np.array(rv['cmod_mm'])[mask],np.array(rv['load_kN'])[mask],label='Referencia con mismo paso',lw=2)
    for c in accepted:
        if c['configuration'][param]!=base['configuration'][param]:
            v=json.loads((ROOT/c['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'];ax.plot(v['cmod_mm'],v['load_kN'],label=f'{param}={c["configuration"][param]:g}')
    ax.set(xlabel='Apertura inferior FEM (mm)',ylabel='Carga total (kN)',title=title);ax.grid(alpha=.25);ax.legend(fontsize=10)
fig.suptitle('Sensibilidad: un parámetro por variante; solo rango común hasta 0,3 mm');fig.tight_layout();fig.savefig(OUT/'sensibilidad_CZM.png',dpi=180);plt.close(fig)
g=np.load(ROOT/base['folder']/'interfaz_gauss.npz')['fields'];fig,axs=plt.subplots(1,3,figsize=(10.5,4.5))
for i,label in [(9,'Inicio del daño'),(base['peak_index'],'Pico'),(344,'Estado avanzado')]:
    for ax,e in zip(axs,[3,2,6]):ax.plot(g[e,i],g[1,i],label=label)
for ax,title in zip(axs,['Apertura normal nativa (mm)','Daño cohesivo D (0–1)','Tracción x, signo de cara (MPa)']):ax.set(xlabel=title,ylabel='Altura material Y (mm)');ax.grid(alpha=.25);ax.legend(fontsize=10)
fig.suptitle('Perfil en puntos de integración: apertura y tracción acompañan al daño');fig.tight_layout();fig.savefig(OUT/'perfil_fractura_CZM.png',dpi=180);plt.close(fig)
dump(OUT/'resumen_entrega.json',{'cases':accepted,'mesh_comparison':mstats,'protocol_comparison':protocol,'viewer_model':base,'statesA':127,'statesB':345,'bulk_damage_in_B':False,'experimental_validation':False,'native_fields_only':True})
print(json.dumps(mstats,ensure_ascii=False,indent=2));print('Accepted cases',len(accepted),'independent comparison series',len(comparisons))
