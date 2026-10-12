"""Export true independent half meshes, native cohesive Gauss data and rigid poses."""
from pathlib import Path
import argparse,json,hashlib,sys,importlib.util
sys.stdout.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
import mph,numpy as np
from jpype import JArray
from jpype.types import JInt
import verificar_czm as z
STAGE=z.STAGE;APP=STAGE.parents[1]
import export_utils as old

def feature(j,tag,selection,expr,units,numbers,gauss=False):
    if tag in list(j.result().numerical().tags()):j.result().numerical().remove(tag)
    j.result().numerical().create(tag,'Eval');f=j.result().numerical(tag);f.selection().named(selection);f.set('data','dsetB');f.set('expr',expr);f.set('unit',units);f.set('solnum',JArray(JInt)(numbers))
    if gauss:f.set('pattern','gauss');f.set('gporder',JInt(2))
    return f

def export(folder,out):
    out.mkdir(parents=True,exist_ok=True);result=json.loads((folder/'resultados.json').read_text(encoding='utf-8'));v=result['variables'];source=folder/'vigueta_fractura.mph';before=old.digest(source)
    mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2);m=client.load(str(source));j=m.java
    count=len(v['load_kN']);numbers=list(range(1,count+1));coords=[];tri=[];bound=[];fields=[];maxerr=0.;all_gp=None
    # Each material half has its own coordinate grouping, preserving coincident faces.
    offset=0
    for side in ['L','R']:
        f=feature(j,'mesh'+side,'geom1_'+side+'_dom',['X','Y','u','v','0','solid.sx','d(u,X)'],['mm','mm','mm','mm','1','MPa','1'],numbers)
        raw=np.asarray(f.getData(),float);xy,inv,tt,bb=old.mesh(raw,f);counts=np.bincount(inv);part=np.stack([np.stack([np.bincount(inv,weights=raw[e,k])/counts for e in range(2,7)],axis=1) for k in range(count)])
        if not np.isfinite(part).all():raise RuntimeError('Nonfinite bulk field')
        coords.append(xy);tri.append(tt+offset);bound.append(bb+offset);fields.append(part);offset+=len(xy)
        print('Native half',side,'nodes',len(xy),flush=True)
    xy=np.vstack(coords);tri=np.vstack(tri);bound=np.vstack(bound);field=np.concatenate(fields,axis=1)
    xy.astype('<f4').tofile(out/'coordinates.bin');tri.astype('<u4').tofile(out/'triangles.bin');bound.astype('<u4').tofile(out/'boundary.bin')
    f=feature(j,'interfaceGP','cohR',['X','Y','solid.bdmg','solid.cntC.gap','solid.um_max','solid.Wbdmg','solid.fsx'],['mm','mm','1','mm','mm','J/m^2','MPa'],numbers,True)
    gp=np.asarray(f.getData(),float);order=np.argsort(gp[1,0]);gp=gp[:,:,order]
    if not np.isfinite(gp).all():raise RuntimeError('Nonfinite native cohesive Gauss sample')
    if gp[2].min()<-1e-7 or gp[2].max()>1.000001:raise RuntimeError('Native Gauss damage outside [0,1]')
    if np.diff(gp[2],axis=0).min()<-1e-7:raise RuntimeError('Cohesive damage not irreversible at native integration points')
    np.savez_compressed(folder/'interfaz_gauss.npz',fields=gp,order=['X_mm','Y_mm','damage','gap_mm','history_mm','dissipation_J_m2','traction_x_MPa'])
    gp[1,0].astype('<f4').tofile(out/'cohesive_y.bin')
    poses=[]
    for name,x,y in [('bl',-225,-15),('br',225,-15),('tl',-75,166),('tr',75,166)]:
        f=feature(j,'rigid'+name,'geom1_'+name+'_dom',['X','Y','u','v'],['mm']*4,numbers);raw=np.asarray(f.getData());design=np.column_stack([np.ones(raw.shape[-1]),raw[0,0]-x,raw[1,0]-y]);pose=[]
        for k in range(count):
            fit=np.linalg.lstsq(design,raw[2:,k].T,rcond=None)[0];err=float(np.max(abs(design@fit-raw[2:,k].T)))
            if err>1e-5:raise RuntimeError('Nonrigid roller export')
            pose.append(dict(name=name,X_mm=x,Y_mm=y,u_mm=float(fit[0,0]),v_mm=float(fit[0,1]),rotation_rad=float(np.arctan2(fit[1,1],1+fit[1,0])),fit_error_mm=err))
        poses.append(pose)
    # Local bulk stress/strain at the right lower face, not cohesive traction divided by opening.
    right_bottom=len(coords[0])+int(np.argmin(np.sum(coords[1]**2,axis=1)))
    if not np.allclose(xy[right_bottom],[0,0],atol=1e-7):raise RuntimeError('Right lower material vertex missing')
    local=np.stack([field[:,right_bottom,3],field[:,right_bottom,4]])
    peak=int(np.argmax(v['load_kN']));states=[]
    p=np.asarray(v['load_kN'])*1000;q=np.asarray(v['head_mm'])/1000;work=np.cumsum(np.r_[0,(p[1:]+p[:-1])*.5*np.diff(q)])
    energy=np.array(v['bulk_energy_J'])+v['adhesion_energy_J']+np.array(v['contact_energy_J'])+np.array(v['fracture_energy_J']);energy_residual=work-(energy-energy[0])
    for k in range(count):
        f32=field[k].astype('<f4');maxerr=max(maxerr,float(abs(field[k]-f32).max()));f32.tofile(out/f'state_{k+1:03d}.bin')
        # The auxiliary fracture file stores native Gauss samples, never bulk damage.
        np.stack([gp[e,k] for e in [2,3,4,5,6]],axis=1).astype('<f4').tofile(out/f'cohesive_{k+1:03d}.bin')
        states.append(dict(id=k+1,branch='ascending' if k<=peak else 'descending',load_kN=v['load_kN'][k],deflection_mm=v['deflection_mm'][k],extension_mm=v['gauge_mm'][k],head_mm=v['head_mm'][k],damageMax=float(gp[2,k].max()),damageMean=v['damage_mean'][k],reactionLeft_kN=v['reaction_bl_N'][k]/1000,reactionRight_kN=v['reaction_br_N'][k]/1000,stressLocal_MPa=float(local[0,k]),strainLocal=float(local[1,k]),damageLocal=0,stressCenter_MPa=float(local[0,k]),strainCenter=float(local[1,k]),rollers=[poses[r][k] for r in range(4)],fields=f'state_{k+1:03d}.bin',source=source.relative_to(STAGE.parent).as_posix(),solution=k+1,equilibriumError=v['equilibrium_relative'][k],cohesiveFields=f'cohesive_{k+1:03d}.bin',opening_mm=v['cmod_mm'][k],openingMaxGauss_mm=float(max(0,gp[3,k].max())),fractureEnergy_J=v['fracture_energy_J'][k],externalWorkFromFirst_J=float(work[k]),energyResidual_J=float(energy_residual[k]),convergence='equilibrium_checked_energy_provisional'))
    reference=json.loads((APP/'public/data/manifest.json').read_text(encoding='utf-8'));manifest={**reference,'modelId':'fracture','modelName':'CZM — trayectoria central prescrita','peakIndex':peak,'criticalPoint_mm':[0,0],'states':states,'cases':[],'material':{**reference['material'],'model':'Elastic bulk + bilinear cohesive interface','internalLength_mm':0},'mesh':dict(nodes=len(xy),triangles=len(tri),boundaryEdges=len(bound),coordinates='coordinates.bin',connectivity='triangles.bin',boundary='boundary.bin',method='Native FEM connectivity; grouping within each material half only; coincident fracture faces remain independent'),'ranges':{key:[float(field[:,:,i].min()),float(field[:,:,i].max())] for i,key in enumerate(['u','v','damage','sx','eps'])},'sources':[dict(path=source.relative_to(STAGE.parent).as_posix(),sha256=before,states=count)],'quantization':dict(format='float32',maxAbsoluteError=maxerr),'cohesive':dict(points=gp.shape[2],coordinates='cohesive_y.bin',fieldsOrder=['damage','gap_mm','history_mm','dissipation_J_m2','traction_x_MPa'],quadratureOrder=2),'limitations':['Visualización 3D de resultados FEM 2D.','CZM en una trayectoria central vertical prescrita; no predice una trayectoria arbitraria.','Apertura inferior entre caras calculadas; no es extensión entre apoyos.','El daño cohesivo corresponde a la interfaz; el volumen es elástico.','No se modela aplastamiento o plastificación volumétrica bajo los rodillos.','ft procede de la calibración Mazars; Gf, E, nu, rigidez cohesiva y diámetro son hipótesis.','Balance energético y sensibilidad deben consultarse en el informe de verificación; una trayectoria convergida no equivale a validación experimental.','No existe curva experimental sincronizada ni apertura medida por estado.']}
    manifest['halfNodeCount']=len(coords[0])
    manifest['fieldsOrder']=['u_mm','v_mm','elastic_bulk_marker_not_damage','sx_bulk_MPa','eps_material']
    z.dump(out/'manifest.json',manifest);z.dump(folder/'exportacion_verificada.json',dict(states=count,nodes=len(xy),faces_independent=True,cohesive_gauss_points=gp.shape[2],damage_irreversible=True,energyResidualFinal_percent=float(energy_residual[-1]/max(abs(work[-1]),1e-12)*100),sourceUnchanged=before==old.digest(source)))
    if before!=old.digest(source):raise RuntimeError('Source model modified')
    print('EXPORT COMPLETE',count,len(xy),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--out',type=Path,default=STAGE/'05_Resultados/visor_fractura');a=p.parse_args();export(a.folder,a.out)
