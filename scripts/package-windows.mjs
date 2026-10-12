import {packager} from '@electron/packager';
import path from 'node:path';
import fs from 'node:fs';
const root=fs.realpathSync('.'),out=path.join(root,'release'),tmpdir=path.join(root,'.packaging-temp');
for(const p of [out,tmpdir])if(fs.existsSync(p)&&!fs.realpathSync(p).startsWith(root+path.sep))throw new Error('El destino de empaquetado sale del repositorio');
console.log(await packager({dir:root,name:'ConcreteLab3D_CZM',platform:'win32',arch:'x64',out,tmpdir,overwrite:true,asar:true,prune:false,appVersion:'2.0.0',ignore:[/^\/(node_modules|public|src|tests|scripts|docs|comsol|release[^/]*|validation|test-results|playwright-report|\.github|\.git)($|\/)/]}));
