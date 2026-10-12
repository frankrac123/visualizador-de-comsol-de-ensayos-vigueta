"""Mechanical acceptance checks and reproducible comparisons of independent models."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'05_Resultados';OUT.mkdir(exist_ok=True)
cases=[]
for path in sorted((ROOT/'03_Modelos').glob('*/resultados.json')):
    r=json.loads(path.read_text(encoding='utf-8'));v={k:np.asarray(x,float) for k,x in r['variables'].items()};c=r['configuration'];p=v['load_kN'];peak=int(np.argmax(p));work=np.cumsum(np.r_[0,(p[1:]+p[:-1])*500*np.diff(v['head_mm']/1000)]);energy=v['bulk_energy_J']+v['adhesion_energy_J']+v['contact_energy_J']+v.get('constitutive_dissipation_exact_J',v['fracture_energy_J']);deltaenergy=energy-energy[0];residual=work-deltaenergy;scale=np.maximum.reduce([abs(work),abs(deltaenergy),np.full(len(work),1e-6)])
    checks={'finite':all(np.isfinite(x).all() for x in v.values()),'equilibrium':float(v['equilibrium_relative'].max())<1e-3,'unilateral_contacts':all(v['pressure_min_'+n+'_MPa'].min()>=-1e-8 for n in ['bl','br','tl','tr']),'penetration_under_0p01mm':all(abs(v['gap_min_'+n+'_mm'].min())<.01 for n in ['bl','br','tl','tr']),'cohesive_damage_bounds':float(v['damage_max'].max())<=1.000001 and float(v['damage_max'].min())>=-1e-7,'nonnegative_dissipation':float(v['fracture_energy_J'].min())>=-1e-8,'dissipation_irreversible':float(np.diff(v['fracture_energy_J']).min())>=-1e-7,'final_energy_balance_under_2percent':abs(residual[-1]/max(abs(work[-1]),1e-6))<.02}
    checks={k:bool(value) for k,value in checks.items()}
    checks['all_states_energy_balance_under_2percent']=bool((abs(residual)/scale).max()<.02)
    case={'folder':str(path.parent.relative_to(ROOT)),'configuration':c,'states':len(p),'peak_kN':float(p[peak]),'peak_index':peak,'peak_deflection_mm':float(v['deflection_mm'][peak]),'last_load_kN':float(p[-1]),'capacity_loss_percent':float(100*(1-p[-1]/p[peak])),'last_opening_mm':float(v['cmod_mm'][-1]),'equilibrium_max':float(v['equilibrium_relative'].max()),'energy_residual_final_percent':float(residual[-1]/max(abs(work[-1]),1e-6)*100),'energy_residual_worst_percent':float((abs(residual)/scale).max()*100),'checks':checks,'all_checks_pass':all(checks.values()),'note':'Final energy threshold 2%; worst-state residual separately reported. Bulk compression failure and experimental validation are not checked by these criteria.'}
    case['energy_method']='Native COMSOL closed-form constitutive integral' if 'constitutive_dissipation_exact_J' in v else 'Explicit accumulator; provisional, sensitive to increments'
    case['note']='Energy criteria apply to every stored state. Bulk compression failure and experimental validation are not checked by these criteria.'
    cases.append(case)
    fig,axs=plt.subplots(1,3,figsize=(12,3.7));axs[0].plot(v['deflection_mm'],p);axs[0].set(xlabel='Flecha central (mm)',ylabel='Carga (kN)');axs[1].plot(v['cmod_mm'],p);axs[1].set(xlabel='Apertura inferior (mm)',ylabel='Carga (kN)');axs[2].plot(v['cmod_mm'],work,label='Trabajo externo desde primer estado');axs[2].plot(v['cmod_mm'],deltaenergy,label='Δ energía almacenada + disipada');axs[2].legend(fontsize=7);axs[2].set(xlabel='Apertura inferior (mm)',ylabel='Energía (J)')
    for ax in axs:ax.grid(alpha=.25)
    fig.suptitle(path.parent.name,fontsize=9);fig.tight_layout();fig.savefig(path.parent/'verificacion_global.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.7))
a=json.loads((ROOT.parents[1]/'public/data/manifest.json').read_text(encoding='utf-8'));ax.plot([s['deflection_mm'] for s in a['states']],[s['load_kN'] for s in a['states']],label='A · Mazars (calibrado al pico)')
for case in cases:
    c=case['configuration']
    if c['ft']==.87851483 and c['gf']==220 and c['kn']==1e14 and case['last_opening_mm']>.59:
        v=json.loads((ROOT/case['folder']/'resultados.json').read_text(encoding='utf-8'))['variables'];ax.plot(v['deflection_mm'],v['load_kN'],label=f'B · CZM h={c["mesh"]:g} mm')
ax.axhline(14.5,color='#7b8790',ls=':',label='Pico documental; flecha experimental desconocida');ax.set(xlabel='Flecha central FEM (mm)',ylabel='Carga total (kN)',title='Modelos independientes; sin curva experimental medida');ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'comparacion_Mazars_CZM.png',dpi=180);plt.close(fig)
(OUT/'verificacion_viguetas.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
print(json.dumps(cases,indent=2,ensure_ascii=False))
