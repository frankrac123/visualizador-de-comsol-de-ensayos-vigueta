"""Native COMSOL evaluation of closed-form dissipation for this isotropic CZM.

Valid ONLY for the implemented equal stiffness/strength/energy of modes I/II,
Power mixing with alpha=1, bilinear displacement damage and no viscosity.
It is not an energy calibration.
The native explicit accumulator remains separately available as a diagnostic.
"""
from pathlib import Path
import argparse,json,sys
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
import mph,numpy as np
import verificar_czm as z
from jpype.types import JInt
STAGE=z.STAGE
EXPR='Gfmat*max(0,min(1,(solid.um_max-ftmat/Kcoh)/(2*Gfmat/ftmat-ftmat/Kcoh)))'
DAMAGE='if(solid.um_max<=ftmat/Kcoh,0,min(1,(2*Gfmat/ftmat)*(solid.um_max-ftmat/Kcoh)/(max(solid.um_max,1e-30[m])*(2*Gfmat/ftmat-ftmat/Kcoh))))'

def native(client,folder,coupon=False):
    folder=folder.resolve()
    filename='modelo.mph' if coupon else 'vigueta_fractura.mph';resultpath=folder/'resultados.json';r=json.loads(resultpath.read_text(encoding='utf-8'));m=client.load(str(folder/filename));j=m.java
    # Guard mathematical applicability using actual model parameters/features.
    d=j.component('comp1').physics('solid').feature('cntC').feature('dco1');a=j.component('comp1').physics('solid').feature('cntC').feature('adh1')
    if str(d.getString('FailureCriterion'))!='Power' or float(str(d.getString('alpha')))!=1:
        raise RuntimeError('Exact-energy formula requires Power mixing with alpha=1')
    if str(d.getString('ViscousRegularization'))!='None' or str(d.getString('CohesiveZoneModel'))!='DispDamage' or str(d.getString('TractionSeparationLaw'))!='LinearSeparation' or str(d.getString('sigmat'))!=str(d.getString('sigmas')) or str(d.getString('Gct'))!=str(d.getString('Gcs')) or float(str(a.getString('ntau')))!=1:raise RuntimeError('Exact-energy formula assumptions are not satisfied')
    dataset='dset1' if coupon else 'dsetB'
    ftag='exactEnergy';j.result().numerical().create(ftag,'IntLine');f=j.result().numerical(ftag);f.selection().named('cohR');f.set('data',dataset);f.set('expr',[f'bmat*gpeval(2,{EXPR})']);f.set('unit',['J']);f.set('innerinput','all');f.set('intorder',JInt(2));energy=np.asarray(f.getReal(),float).reshape(-1)
    j.result().numerical().create('exactLaw','MaxLine');f=j.result().numerical('exactLaw');f.selection().named('cohR');f.set('data',dataset);f.set('expr',[f'abs(gpeval(2,solid.bdmg-({DAMAGE})))']);f.set('unit',['1']);f.set('innerinput','all');f.set('points','integration');f.set('intorder',JInt(2));error=np.asarray(f.getReal(),float).reshape(-1)
    if not np.isfinite(energy).all() or error.max()>1e-7:raise RuntimeError('Native energy/law evaluation failed verification')
    r['variables']['constitutive_dissipation_exact_J']=energy.tolist();r['exact_energy_method']={'expression':EXPR,'native_evaluation':'COMSOL IntLine, bmat*gpeval(2,expression), quadrature 2','native_damage_law_max_error':float(error.max()),'scope':'Equal normal/tangential stiffness, strength and energy; bilinear displacement damage; no viscosity; reference cohesive area.','original_accumulator_preserved':True}
    z.dump(resultpath,r)
    if not coupon:
        v=r['variables'];p=np.array(v['load_kN']);work=np.cumsum(np.r_[0,(p[1:]+p[:-1])*500*np.diff(np.array(v['head_mm'])/1000)]);et=np.array(v['bulk_energy_J'])+v['adhesion_energy_J']+np.array(v['contact_energy_J'])+energy;res=work-et+et[0];scale=np.maximum.reduce([abs(work),abs(et-et[0]),np.full(len(work),1e-6)])
        r['exact_energy_verification']={'max_relative_residual_percent':float((abs(res)/scale).max()*100),'final_relative_residual_percent':float(res[-1]/max(abs(work[-1]),1e-6)*100),'max_absolute_residual_J':float(abs(res).max())};z.dump(resultpath,r)
        # Update already exported per-state values without altering any mesh or displacement.
        for out in [STAGE/'05_Resultados/visor_fractura_avanzada',STAGE.parents[1]/'public/data/fracture']:
            path=out/'manifest.json'
            if path.exists():
                manifest=json.loads(path.read_text(encoding='utf-8'))
                if manifest['sources'][0]['path']==(folder/filename).relative_to(STAGE.parent).as_posix():
                    for k,s in enumerate(manifest['states']):s['fractureEnergy_J']=float(energy[k]);s['nativeAccumulatorEnergy_J']=v['fracture_energy_J'][k];s['energyResidual_J']=float(res[k]);s['convergence']='equilibrium_and_irreversibility_checked_energy_exact_law'
                    manifest['energyMethod']=r['exact_energy_method'];manifest['energyVerification']=r['exact_energy_verification'];manifest['cohesive']['fieldsOrder'][3]='native_explicit_accumulation_J_m2';z.dump(path,manifest)
    client.remove(m);print(folder.name,'exact dissipation J',energy[-1],'damage-law error',error.max(),r.get('exact_energy_verification',''),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',nargs='*',type=Path);p.add_argument('--coupons',action='store_true');args=p.parse_args();mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2)
    folders=args.folder or [x.parent for x in (STAGE/('04_Verificacion' if args.coupons else '03_Modelos')).glob('*/resultados.json')]
    for folder in folders:native(client,folder,args.coupons)
