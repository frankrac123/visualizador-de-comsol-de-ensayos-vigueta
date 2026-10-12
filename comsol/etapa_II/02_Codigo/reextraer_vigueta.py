import json,sys,time
import mph
import vigueta_czm as b
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
folder=Path(sys.argv[1]);mph.option('session','stand-alone');client=mph.start(version='6.1',cores=2);m=client.load(str(folder/'vigueta_fractura.mph'))
r=b.extract(m);r.update(configuration={'mesh':8,'ft':.87851483,'gf':220,'kn':1e14},solver_error=None,reextracted=True)
b.z.dump(folder/'resultados.json',r)
for key,v in r['variables'].items():print(key,len(v),min(v),max(v),v[-1],flush=True)
print('Unavailable:',r['unavailable'],flush=True)
