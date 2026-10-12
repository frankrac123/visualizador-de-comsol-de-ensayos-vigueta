"""Compare native coupon solutions with analytic limits and check energy/history."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];summaries=[]
for path in sorted((ROOT/'04_Verificacion').glob('uniaxial_*/resultados.json')):
    r=json.loads(path.read_text(encoding='utf-8'));v={k:np.asarray(x,float) for k,x in r['variables'].items()};p=r['parameters'];ft=p['ft_MPa'];K=p['K_N_m3']/1e9;df=2*p['Gf_J_m2']/(ft*1e6)*1000;d0=ft/K
    x=v['opening_mm'];stress=v['stress_MPa'];damage=v['damage'];hist=v['history_mm'];diss=v['dissipation_J'];s={'file':str(path.relative_to(ROOT)),'kind':r['kind'],'mesh_h_mm':r['mesh_h_mm'],'steps':len(x),'solver_success':r['solver_error'] is None,'damage_min':float(damage.min()),'damage_max':float(damage.max()),'damage_largest_decrease':float(max(0,-np.diff(damage).min())),'history_largest_decrease_mm':float(max(0,-np.diff(hist).min())),'dissipation_largest_decrease_J':float(max(0,-np.diff(diss).min())),'dissipation_final_J':float(diss[-1])}
    if r['kind']=='tension':
        exact=np.where(x<=d0,K*x,np.maximum(0,ft*(df-x)/(df-d0)));s['traction_max_absolute_error_MPa']=float(abs(stress-exact).max());s['energy_from_native_traction_J_m2']=float(np.trapezoid(stress*1e6,x/1000));s['native_dissipation_final_error_percent']=float((diss[-1]/(.0001*p['Gf_J_m2'])-1)*100)
        s['law_verified']=s['traction_max_absolute_error_MPa']<1e-3
        s['energy_accumulator_within_1percent']=abs(s['native_dissipation_final_error_percent'])<1
    elif r['kind']=='compression':
        expected=v['dload_mm']/(10/p['E_MPa']+1/K);s['elastic_contact_max_error_MPa']=float(abs(stress-expected).max());s['note']='Verifies elastic compression and interface contact only. No bulk compression damage law is implemented; exceeding fc is outside material validity.'
    else:
        s['irreversibility_verified']=s['damage_largest_decrease']<1e-7 and s['history_largest_decrease_mm']<1e-8
        s['native_dissipation_final_error_percent']=float((diss[-1]/(.0001*p['Gf_J_m2'])-1)*100)
        s['energy_accumulator_within_1percent']=abs(s['native_dissipation_final_error_percent'])<1
    if 'constitutive_dissipation_exact_J' in v:
        s['exact_constitutive_dissipation_final_J']=float(v['constitutive_dissipation_exact_J'][-1]);s['native_damage_law_max_error']=r['exact_energy_method']['native_damage_law_max_error']
        expected=0 if r['kind']=='compression' else .0001*p['Gf_J_m2'];s['exact_constitutive_energy_verified']=bool(abs(s['exact_constitutive_dissipation_final_J']-expected)<1e-9)
    summaries.append(s)
    fig,axs=plt.subplots(1,3,figsize=(12,3.5));axs[0].plot(x,stress,label='FEM COMSOL');axs[0].set(xlabel='Apertura / penetración (mm)',ylabel='Tensión longitudinal (MPa)');axs[1].plot(v['dload_mm'],damage);axs[1].set(xlabel='Carrera impuesta (mm)',ylabel='Daño cohesivo (0–1)');axs[2].plot(v['dload_mm'],diss);axs[2].set(xlabel='Carrera impuesta (mm)',ylabel='Disipación nativa (J)');
    for ax in axs:ax.grid(alpha=.25)
    fig.suptitle(f'Muestra {r["kind"]}, h={r["mesh_h_mm"]} mm, {len(x)} estados');fig.tight_layout();fig.savefig(path.parent/'verificacion.png',dpi=160);plt.close(fig)
(ROOT/'04_Verificacion/resumen_verificacion.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
print(json.dumps(summaries,indent=2,ensure_ascii=False))
