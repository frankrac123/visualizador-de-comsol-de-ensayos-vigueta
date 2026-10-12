"""Confirm the native integration measure on the existing nonlinear solution."""
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
import mph,numpy as np
from jpype.types import JInt
import verificar_czm as z
mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2)
m=client.load(str(z.STAGE/'03_Modelos/CZM_h8_ft0.878515_Gf220_K1e+14_o0.6_ds0.002/vigueta_fractura.mph'));j=m.java
j.result().numerical().create('measureCheck','IntLine');f=j.result().numerical('measureCheck');f.selection().named('cohR');f.set('data','dsetB');f.set('expr',['1']);f.set('unit',['mm']);f.set('innerinput','all');f.set('intorder',JInt(2));length=np.asarray(f.getReal(),float).reshape(-1)
props={str(p):str(f.getString(str(p))) for p in f.properties() if 'frame' in str(p).lower()}
record={'integration_feature':'IntLine','frame_properties':props,'states':len(length),'length_min_mm':float(length.min()),'length_max_mm':float(length.max()),'undeformed_length_mm':151,'reference_measure_verified':bool(np.max(abs(length-151))<1e-7)}
z.dump(z.STAGE/'05_Resultados/verificacion_medida_integracion.json',record);print(json.dumps(record));client.remove(m)
