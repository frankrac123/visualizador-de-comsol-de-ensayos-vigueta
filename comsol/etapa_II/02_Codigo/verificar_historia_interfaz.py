"""Read-only pointwise verification of native cohesive integration histories."""
from pathlib import Path
import json,sys,hashlib,argparse
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
import mph,numpy as np
from jpype import JArray
from jpype.types import JInt
import verificar_czm as z

if __name__=='__main__':
    mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2)
    parser=argparse.ArgumentParser();parser.add_argument('folder',nargs='*',type=Path);args=parser.parse_args()
    paths=[p.resolve()/'resultados.json' for p in args.folder] or sorted((z.STAGE/'03_Modelos').glob('*/resultados.json'))
    for path in paths:
        if '_o' not in path.parent.name:continue
        r=json.loads(path.read_text(encoding='utf-8'));source=path.parent/'vigueta_fractura.mph';before=hashlib.sha256(source.read_bytes()).hexdigest();m=client.load(str(source));j=m.java
        j.result().numerical().create('historyGP','Eval');f=j.result().numerical('historyGP');f.selection().named('cohR');f.set('data','dsetB');f.set('expr',['X','Y','solid.bdmg','solid.cntC.gap','solid.um_max','solid.Wbdmg','solid.fsx']);f.set('unit',['mm','mm','1','mm','mm','J/m^2','MPa']);f.set('solnum',JArray(JInt)(list(range(1,len(r['variables']['load_kN'])+1))));f.set('pattern','gauss');f.set('gporder',JInt(2));g=np.asarray(f.getData(),float);g=g[:,:,np.argsort(g[1,0])]
        d=g[2];k=g[4];checks={'finite':bool(np.isfinite(g).all()),'damage_bounded':bool(d.min()>=-1e-7 and d.max()<=1.000001),'damage_irreversible':bool(np.diff(d,axis=0).min()>=-1e-7),'history_irreversible':bool(np.diff(k,axis=0).min()>=-1e-8),'source_unchanged':before==hashlib.sha256(source.read_bytes()).hexdigest()}
        onset=np.flatnonzero(d.max(axis=1)>1e-6);closed=np.flatnonzero(d.max(axis=1)>=1-1e-7)
        r['interface_verification']={'method':'Native COMSOL Eval, Gauss pattern order 2, no nodal extrapolation','points':g.shape[-1],'states':g.shape[1],'damage_largest_decrease':float(max(0,-np.diff(d,axis=0).min())),'history_largest_decrease_mm':float(max(0,-np.diff(k,axis=0).min())),'first_damage_state':int(onset[0]+1) if len(onset) else None,'first_fully_decohered_point_state':int(closed[0]+1) if len(closed) else None,'checks':checks,'all_checks_pass':all(checks.values())}
        z.dump(path,r);np.savez_compressed(path.parent/'interfaz_gauss.npz',fields=g,order=['X_mm','Y_mm','damage','gap_mm','history_mm','native_explicit_accumulation_J_m2','traction_x_MPa']);client.remove(m)
        print(path.parent.name,r['interface_verification'],flush=True)
