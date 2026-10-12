"""Original COMSOL helper functions, extracted without mechanical changes."""
from jpype.types import JBoolean,JInt

def seleccion(c,tag,dim,xmin,xmax,ymin,ymax):
    c.selection().create(tag,'Box')
    f=c.selection(tag)
    f.set('entitydim',JInt(dim))
    f.set('condition','inside')
    for key,value in [('xmin',xmin),('xmax',xmax),('ymin',ymin),('ymax',ymax)]:
        f.set(key,f'{value}[mm]')
    ids=list(f.entities(dim))
    if not ids: raise RuntimeError(f'Seleccion vacia: {tag}')
    return ids

def desplazamiento(s,tag,selection,dim,ux=None,vy=None):
    s.create(tag,f'Displacement{dim}',dim)
    f=s.feature(tag)
    f.selection().named(selection)
    for i,value in enumerate([ux,vy]):
        f.setIndex('Direction',JBoolean(value is not None),JInt(i))
        f.setIndex('U0',value if value is not None else '0',JInt(i))

def estudio(j,parameter,values,unit=''):
    j.study().create('std1')
    j.study('std1').create('stat','Stationary')
    f=j.study('std1').feature('stat')
    f.set('useparam','on')
    f.set('pname',[parameter])
    f.set('plistarr',[values])
    f.set('punit',[unit])
    f.set('pcontinuationmode','last')
    j.study('std1').createAutoSequences('all')
    sol=j.sol('sol1')
    # Ajustes solo en features presentes; dejar explicito que son tolerancias numericas.
    for tag in sol.feature().tags():
        f=sol.feature(tag)
        if str(f.getType())=='Stationary':
            f.set('stol','0.001')
            for subtag in f.feature().tags():
                sub=f.feature(subtag)
                if str(sub.getType())=='FullyCoupled':
                    sub.set('maxiter',JInt(60))
                    sub.set('dtech','auto')
                    sub.set('initstep','0.5')
                    sub.set('minstep','1e-5')
