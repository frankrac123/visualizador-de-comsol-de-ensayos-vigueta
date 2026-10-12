"""Native 2D cohesive beam, central prescribed path, same four-roller apparatus."""
from pathlib import Path
import argparse,json,sys,time
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
import mph,numpy as np
from jpype.types import JInt
import verificar_czm as z
base=z.base;STAGE=z.STAGE
NAMES=['bl','br','tl','tr']

def build(client,h,ft,gf,kn):
    m=client.create('Vigueta_CZM');j=m.java;j.component().create('comp1',True);c=j.component('comp1');c.sorder('quadratic')
    c.geom().create('geom1',2);g=c.geom('geom1');g.lengthUnit('mm')
    for name,x0,x1,rollers in [('L',-251,0,[-225,-75]),('R',0,251,[225,75])]:
        low=sorted(set([x0,x1]+[x+d for x in rollers[:1] for d in [-3,0,3]]));high=sorted(set([x0,x1]+[x+d for x in rollers[1:] for d in [-3,0,3]]),reverse=True)
        g.create(name,'Polygon');f=g.feature(name);f.set('x',[str(x) for x in low+high]);f.set('y',['0']*len(low)+['151']*len(high));f.set('type','solid');f.set('selresult','on');f.set('selresultshow','all')
    rolls=[('bl',-225,-15,0),('br',225,-15,0),('tl',-75,166,151),('tr',75,166,151)]
    for name,x,y,by in rolls:
        g.create(name,'Circle');f=g.feature(name);f.set('r','15');f.set('pos',[str(x),str(y)]);f.set('selresult','on');f.set('selresultshow','all')
    g.feature('fin').set('action','assembly');g.feature('fin').set('createpairs','off');g.run()
    s=z.bulk(j,c,130.3333333333333);j.param().set('ftmat',f'{ft}[MPa]');j.param().set('Gfmat',f'{gf}[J/m^2]');j.param().set('Kcoh',f'{kn}[N/m^3]');j.param().set('dload','0.003[mm]')
    beamdom=list(c.selection('geom1_L_dom').entities(2))+list(c.selection('geom1_R_dom').entities(2));c.material('mat1').selection().set(beamdom)
    for tag,owner in [('cohL','geom1_L_bnd'),('cohR','geom1_R_bnd')]:z.select(c,tag,1,[-.001,.001,-.001,151.001],owner)
    z.cohesive(c,s,'cohL','cohR')
    for i,(name,x,y,by) in enumerate(rolls,1):
        z.select(c,'dst_'+name,1,[x-3-.001,x+3+.001,by-.001,by+.001])
        c.pair().create('cp_'+name,'Contact','geom1');p=c.pair('cp_'+name);p.source().named('geom1_'+name+'_bnd');p.destination().named('dst_'+name)
        s.create('rd'+str(i),'RigidDomain',2);rd=s.feature('rd'+str(i));rd.selection().named('geom1_'+name+'_dom');rd.set('rho_mat','userdef');rd.set('rho','7850[kg/m^3]')
        rd.create('pdr1','PrescribedDispRot');f=rd.feature('pdr1');f.set('Direction',['1','1','0']);f.set('U0',['0','0' if i<=2 else '-dload','0']);f.set('RotationType','PrescribedRotationGroup');f.set('phi0','0');f.set('WeakConstraints','0');f.set('UnidirectionalConstraints','1')
        s.create('cnt'+str(i),'SolidContact',1);f=s.feature('cnt'+str(i))
        for key,val in [('pairs',['cp_'+name]),('ContactMethodCtrl','Penalty'),('zeroInitGap','0'),('E_char','Emat'),('penaltyCtrlPenalty','ManualTuning'),('fp_penalty','10'),('automaticQuadrature','0'),('integrationOrder','2'),('storeContactEnergy','1')]:f.set(key,val)
    z.select(c,'pin',0,[-225.001,-224.999,-.001,.001],'geom1_L_pnt');base.desplazamiento(s,'pin1','pin',0,ux='0')
    for tag,bounds,owner in [('cL',[-.001,.001,-.001,.001],'geom1_L_pnt'),('cR',[-.001,.001,-.001,.001],'geom1_R_pnt'),('gR',[224.999,225.001,-.001,.001],'geom1_R_pnt')]:
        z.select(c,tag,0,bounds,owner);c.cpl().create('pt'+tag,'Integration','geom1');c.cpl('pt'+tag).selection().named(tag)
    c.cpl().create('ptPin','Integration','geom1');c.cpl('ptPin').selection().named('pin')
    c.mesh().create('mesh1');mesh=c.mesh('mesh1');f=mesh.feature('size');f.set('custom','on');f.set('hmax',f'{h}[mm]');f.set('hmin','.025[mm]');f.set('hgrad','1.4')
    mesh.create('ft','FreeTri');f=mesh.feature('ft');f.selection().geom('geom1',2);f.selection().all()
    for tag,selections,size in [('contact',[f'dst_{n}' for n in NAMES],.04),('roller',[f'geom1_{n}_bnd' for n in NAMES],.75),('fracture',['cohL','cohR'],h/2)]:
        f.create(tag,'Size');sz=f.feature(tag);sz.selection().geom('geom1',1);sz.selection().set(sum([list(c.selection(t).entities(1)) for t in selections],[]))
        for key,val in [('custom','on'),('hmax',f'{size}[mm]'),('hmaxactive','on'),('hmin',f'{size/4}[mm]'),('hminactive','on')]:sz.set(key,val)
    mesh.run();base.estudio(j,'dload','0.0001 0.0005 0.001 0.002 0.003','mm');j.study('std1').feature('stat').set('geometricNonlinearity',True);j.sol('sol1').feature('s1').set('stol','1e-6')
    return m

def control(m,values):
    j=m.java;c=j.component('comp1');s=c.physics('solid');s.feature().remove('rd4');rd=s.feature('rd3');rd.selection().set(list(c.selection('geom1_tl_dom').entities(2))+list(c.selection('geom1_tr_dom').entities(2)))
    rd.feature('pdr1').set('RotationType','FreeGroup');rd.feature('pdr1').set('U0',['0','-qact*1[mm]','0'])
    c.physics().create('ge','GlobalEquations');ge=c.physics('ge').feature('ge1');ge.set('name',['qact']);ge.set('equation',['(ptcR(u)-ptcL(u)-cmod)/1[mm]']);ge.set('initialValueU',['0.003']);ge.set('description',['Head displacement; physical bottom opening controller'])
    j.param().set('cmod',f'{values[0]}[mm]');before=set(str(t) for t in j.sol().tags())
    j.study().create('stdB');std=j.study('stdB');std.create('stat','Stationary');f=std.feature('stat')
    for key,val in [('useparam','on'),('pname',['cmod']),('plistarr',[' '.join(str(x) for x in values)]),('punit',['mm']),('pcontinuationmode','last'),('geometricNonlinearity',True)]:f.set(key,val)
    std.createAutoSequences('all');soltag=(set(str(t) for t in j.sol().tags())-before).pop();sol=j.sol(soltag);v=sol.feature('v1');v.set('initmethod','sol');v.set('initsol','sol1');v.set('solnum','last');sol.feature('s1').set('stol','1e-6')
    for tag in sol.feature('s1').feature().tags():
        f=sol.feature('s1').feature(tag)
        if str(f.getType())=='FullyCoupled':f.set('maxiter',JInt(80));f.set('dtech','auto');f.set('minstep','1e-6')
    j.result().dataset().create('dsetB','Solution');j.result().dataset('dsetB').set('solution',soltag)
    return soltag

def extract(m):
    j=m.java;out={'variables':{},'unavailable':{}}
    def ev(key,typ,expr,unit,selection=None):
        try:
            z.evaluation(j,'b_'+key,typ,[expr],[unit],selection,'dsetB');f=j.result().numerical('b_'+key);f.set('intorder',JInt(2)) if typ=='IntLine' else None
            if typ in ['MaxLine','MinLine']:
                f.set('points','integration');f.set('intorder',JInt(2))
            v=np.asarray(f.getReal(),float).reshape(-1)
            if not np.isfinite(v).all():
                out['unavailable'][key]='Nonfinite native evaluation: '+str(np.flatnonzero(~np.isfinite(v)).tolist());return None
            out['variables'][key]=v.tolist();return v
        except Exception as e:out['unavailable'][key]=str(e)[:900]
    for key,expr,unit in [('cmod_mm','cmod','mm'),('head_mm','qact','1'),('deflection_mm','-(ptcR(v)+ptcL(v))/2','mm'),('gauge_mm','ptgR(u)-ptPin(u)','mm'),('bulk_energy_J','solid.Ws_tot','J'),('fracture_energy_J','solid.Wdmg_tot','J'),('adhesion_energy_J','solid.Wadhe_tot','J'),('contact_energy_J','solid.Wcnt_tot','J')]:ev(key,'EvalGlobal',expr,unit)
    for key,expr,unit in [('damage_max','gpeval(2,solid.bdmg)','1'),('opening_max_mm','solid.cntC.gap','mm')]:ev(key,'MaxLine',expr,unit,'cohR')
    ev('damage_mean','AvLine','gpeval(2,solid.bdmg)','1','cohR')
    forces=[]
    for i,n in enumerate(NAMES,1):
        forces.append(ev('reaction_'+n+'_N','IntLine',f'solid.cnt{i}.gsa_cp_{n}*solid.cnt{i}.Tny_cp_{n}','N','dst_'+n))
        ev('pressure_min_'+n+'_MPa','MinLine',f'solid.cnt{i}.Tn','MPa','dst_'+n);ev('gap_min_'+n+'_mm','MinLine',f'solid.cnt{i}.gap','mm','dst_'+n)
    if all(f is not None for f in forces):
        f=np.array(forces);p=-(f[2]+f[3]);out['variables']['load_kN']=(p/1000).tolist();out['variables']['equilibrium_relative']=(abs(f.sum(axis=0))/np.maximum(abs(p),1)).tolist()
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mesh',type=float,default=8);p.add_argument('--ft',type=float,default=.87851483);p.add_argument('--gf',type=float,default=220);p.add_argument('--kn',type=float,default=1e14);p.add_argument('--max-opening',type=float,default=.1);p.add_argument('--step',type=float,default=.002);a=p.parse_args()
    folder=STAGE/'03_Modelos'/f'CZM_h{a.mesh:g}_ft{a.ft:g}_Gf{a.gf:g}_K{a.kn:g}_o{a.max_opening:g}_ds{a.step:g}';folder.mkdir(parents=True,exist_ok=True)
    mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2)
    client.java.showProgress(str(folder/'progreso_solver.log'))
    t=time.perf_counter();m=build(client,a.mesh,a.ft,a.gf,a.kn)
    print('GEOMETRY AND MESH CREATED; solving initial contacts',flush=True);m.solve();m.save(str(folder/'contactos_iniciales.mph'))
    values=np.unique(np.r_[np.linspace(.0000005,.000015,15),np.linspace(.00002,.001,30),np.arange(.001+a.step,a.max_opening,a.step),a.max_opening])
    tag=control(m,values);err=None
    print('Cohesive continuation '+tag,flush=True)
    try:m.java.sol(tag).runAll()
    except Exception as e:err=str(e);print('CONTINUATION STOP '+err[:800],flush=True)
    m.save(str(folder/'vigueta_fractura.mph'));m.java.resetHist();m.save(str(folder/'vigueta_fractura.java'))
    result=extract(m);result.update(solver_error=err,elapsed_s=time.perf_counter()-t,configuration=vars(a),path_hypothesis='Central vertical predefined cohesive interface, x=0 mm')
    z.dump(folder/'resultados.json',result);print(json.dumps({'folder':str(folder),'variables':list(result['variables']),'unavailable':list(result['unavailable']),'error':err,'seconds':result['elapsed_s']},ensure_ascii=False),flush=True)
