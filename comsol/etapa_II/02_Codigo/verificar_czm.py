"""Independent native COMSOL 6.1 cohesive coupon; no original file is modified."""
from pathlib import Path
import argparse, importlib.util, json, sys, time
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
import mph, numpy as np
from jpype.types import JInt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
STAGE=Path(__file__).resolve().parents[1]
import base_comsol as base

def dump(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')

def select(c,tag,dim,bounds,owner=None):
    ids=base.seleccion(c,tag+'box',dim,*bounds)
    if owner:ids=[x for x in ids if x in list(c.selection(owner).entities(dim))]
    if not ids:raise RuntimeError('Empty selection '+tag)
    c.selection().create(tag,'Explicit');c.selection(tag).geom('geom1',dim);c.selection(tag).set(ids)
    return ids

def bulk(j,c,width):
    for key,val in [('Emat','25000[MPa]'),('numat','0.2'),('ftmat','0.87851483[MPa]'),('Gfmat','220[J/m^2]'),('Kcoh','1e14[N/m^3]'),('bmat',f'{width}[mm]')]:j.param().set(key,val)
    c.material().create('mat1','Common');mat=c.material('mat1');mat.selection().all()
    for key,val in [('youngsmodulus','Emat'),('poissonsratio','numat'),('density','2331.488[kg/m^3]')]:mat.propertyGroup('def').set(key,val)
    c.physics().create('solid','SolidMechanics','geom1');s=c.physics('solid')
    s.prop('Type2D').set('Type2D','PlaneStress');s.prop('d').set('d','bmat')
    s.prop('ShapeProperty').set('order_displacement','1')
    return s

def cohesive(c,s,source,dest,tag='cntC'):
    c.pair().create('coh','Contact','geom1');p=c.pair('coh');p.source().named(source);p.destination().named(dest)
    s.create(tag,'SolidContact',1);f=s.feature(tag)
    for key,val in [('pairs',['coh']),('ContactMethodCtrl','Penalty'),('penaltyCtrlPenalty','userDefined'),('pn_penalty','Kcoh'),('zeroInitGap','1'),('E_char','Emat'),('storeContactEnergy','1'),('automaticQuadrature','0'),('integrationOrder','2')]:f.set(key,val)
    f.create('adh1','Adhesion',1);a=f.feature('adh1')
    a.set('ActivationCriterion','Always');a.set('StiffnessInput','FromPenaltyFactor');a.set('ntau','1')
    f.create('dco1','Decohesion',1);d=f.feature('dco1')
    for key,val in [('CohesiveZoneModel','DispDamage'),('TractionSeparationLaw','LinearSeparation'),('sigmat','ftmat'),('sigmas','ftmat'),('Gct','Gfmat'),('Gcs','Gfmat'),('FailureCriterion','Power'),('alpha','1'),('ViscousRegularization','None'),('storeDmgEnergy','1')]:d.set(key,val)
    return f

def evaluation(j,tag,typ,expr,units,selection=None,dataset='dset1'):
    if tag in list(j.result().numerical().tags()):j.result().numerical().remove(tag)
    j.result().numerical().create(tag,typ);f=j.result().numerical(tag)
    if selection:f.selection().named(selection)
    f.set('expr',expr);f.set('unit',units);f.set('innerinput','all');f.set('data',dataset)
    return np.asarray(f.getReal(),float).reshape(len(expr),-1)

def coupon(client,h,kind,increments=103):
    suffix=f'_pasos{increments}' if increments!=103 else ''
    out=STAGE/'04_Verificacion'/f'uniaxial_{kind}_h{h:g}{suffix}'
    out.mkdir(parents=True,exist_ok=True)
    m=client.create('Coupon');j=m.java;j.component().create('comp1',True);c=j.component('comp1')
    c.geom().create('geom1',2);g=c.geom('geom1');g.lengthUnit('mm')
    for name,x in [('L',-5),('R',0)]:
        g.create(name,'Rectangle');f=g.feature(name);f.set('size',['5','10']);f.set('pos',[str(x),'0']);f.set('selresult','on');f.set('selresultshow','all')
    g.feature('fin').set('action','assembly');g.feature('fin').set('createpairs','off');g.run()
    s=bulk(j,c,10)
    for tag,bounds,owner in [('cohL',[-.001,.001,-.001,10.001],'geom1_L_bnd'),('cohR',[-.001,.001,-.001,10.001],'geom1_R_bnd'),('left',[-5.001,-4.999,-.001,10.001],None),('right',[4.999,5.001,-.001,10.001],None),('bottom',[-5.001,5.001,-.001,.001],None)]:select(c,tag,1,bounds,owner)
    cohesive(c,s,'cohL','cohR')
    base.desplazamiento(s,'leftfix','left',1,ux='0');base.desplazamiento(s,'pull','right',1,ux='dload')
    base.desplazamiento(s,'bottomfix','bottom',1,vy='0')
    c.mesh().create('mesh1');mesh=c.mesh('mesh1');f=mesh.feature('size');f.set('custom','on');f.set('hmax',f'{h}[mm]');f.set('hmin',f'{h/4}[mm]');mesh.create('ft','FreeTri');mesh.run()
    if kind=='tension':ds=np.r_[0,np.linspace(.00001,.0005,50),np.linspace(.0006,.51,increments)]
    elif kind=='compression':ds=np.linspace(0,-.01,21)
    elif increments==103:ds=np.r_[np.linspace(0,.26,30),np.linspace(.25,-.002,30),np.linspace(0,.51,55)]
    else:ds=np.r_[0,np.linspace(.00001,.0005,50),np.linspace(.0006,.26,increments//2),np.linspace(.259,-.002,increments//4),np.linspace(0,.51,increments)]
    j.func().create('path','Interpolation');f=j.func('path');f.set('funcname','dpath');f.set('table',[[str(i),str(x)] for i,x in enumerate(ds)]);f.set('argunit','1');f.set('fununit','mm')
    j.param().set('dload','dpath(istep)');j.param().set('istep','0')
    base.estudio(j,'istep',f'range(0,1,{len(ds)-1})')
    j.sol('sol1').feature('s1').set('stol','1e-7')
    t=time.perf_counter();err=None
    try:m.solve()
    except Exception as e:err=str(e);print('SOLVE FAILURE '+err[:500],flush=True)
    m.save(str(out/'modelo.mph'));j.resetHist();m.save(str(out/'modelo.java'))
    result={'mesh_h_mm':h,'kind':kind,'increments':increments,'elapsed_s':time.perf_counter()-t,'solver_error':err,'parameters':{'E_MPa':25000,'nu':.2,'ft_MPa':.87851483,'Gf_J_m2':220,'K_N_m3':1e14},'variables':{},'unavailable':{}}
    expressions={'opening_mm':('solid.cntC.gap','mm'),'damage':('gpeval(2,solid.bdmg)','1'),'history_mm':('gpeval(2,solid.cntC.um_max)','mm'),'stress_MPa':('solid.sx','MPa'),'jump_x_mm':('solid.us','mm'),'traction_x_MPa':('gpeval(2,solid.fsx)','MPa'),'contact_MPa':('solid.cntC.Tn','MPa'),'dissipation_density_J_m2':('gpeval(2,solid.Wbdmg)','J/m^2'),'elastic_density_J_m2':('gpeval(2,solid.Wadhe)','J/m^2')}
    for key,(expr,unit) in expressions.items():
        try:result['variables'][key]=evaluation(j,'ev_'+key,'AvLine',[expr],[unit],'cohR')[0].tolist()
        except Exception as e:result['unavailable'][key]=str(e)[:1200]
    for key,(expr,unit) in {'dload_mm':('dload','mm'),'istep':('istep','1'),'dissipation_J':('solid.Wdmg_tot','J'),'adhesion_energy_J':('solid.Wadhe_tot','J'),'contact_energy_J':('solid.Wcnt_tot','J'),'bulk_energy_J':('solid.Ws_tot','J')}.items():
        try:result['variables'][key]=evaluation(j,'eg_'+key,'EvalGlobal',[expr],[unit])[0].tolist()
        except Exception as e:result['unavailable'][key]=str(e)[:1200]
    dump(out/'resultados.json',result);client.remove(m)
    print(json.dumps({'kind':kind,'mesh':h,'solver_error':err,'computed_variables':list(result['variables']),'unavailable':list(result['unavailable']),'seconds':result['elapsed_s']},ensure_ascii=False),flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mesh',type=float,default=2.5);p.add_argument('--kind',default='tension',choices=['tension','compression','cycle']);p.add_argument('--increments',type=int,default=103);a=p.parse_args()
    mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2);coupon(client,a.mesh,a.kind,a.increments)
