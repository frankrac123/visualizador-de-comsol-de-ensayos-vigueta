"""Original native mesh and digest helpers, extracted without algorithm changes."""
import hashlib
import numpy as np

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024**2),b''):h.update(b)
 return h.hexdigest()

def mesh(raw,f):
 xy=raw[:2,0].T
 coords,inv=np.unique(np.round(xy,9),axis=0,return_inverse=True)
 elements=np.asarray(f.getElements(),dtype=np.int64)
 if elements.shape[0]!=3:raise RuntimeError(f'Conectividad inesperada {elements.shape}')
 if elements.min()<0 or elements.max()>=len(xy):raise RuntimeError('Indices nativos fuera del rango')
 triangles=inv[elements.T]
 side1=coords[triangles[:,1]]-coords[triangles[:,0]];side2=coords[triangles[:,2]]-coords[triangles[:,0]]
 area=side1[:,0]*side2[:,1]-side1[:,1]*side2[:,0]
 triangles=triangles[abs(area)>1e-12];area=area[abs(area)>1e-12]
 triangles[area<0]=triangles[area<0][:,[0,2,1]]
 triangles=np.unique(triangles,axis=0)
 # Se mantiene la orientacion positiva y se identifican los bordes de extrusión.
 edges=np.vstack([triangles[:,[0,1]],triangles[:,[1,2]],triangles[:,[2,0]]])
 unique,counts=np.unique(np.sort(edges,axis=1),axis=0,return_counts=True)
 boundary=unique[counts==1]
 assert len(boundary)>0 and counts.max()<=2,'La malla no es una superficie manifold'
 return coords,inv,triangles,boundary
