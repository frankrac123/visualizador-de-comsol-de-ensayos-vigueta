import {useEffect,useRef,useState} from 'react';
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import type {Manifest,State} from './science';
export type ViewMode='material'|'stress'|'strain'|'damage'|'fracture'|'amplified'|'comparison';
export interface MeshData {xy:Float32Array;triangles:Uint32Array;boundary:Uint32Array;cohesiveY?:Float32Array}
export interface SceneHandle {capture:()=>string;reset:()=>void;front:()=>void;fracture:()=>void}
interface Props {manifest:Manifest;mesh:MeshData;state:State;fields:Float32Array;cohesiveFields?:Float32Array;mode:ViewMode;scale:number;dark:boolean;onReady:(h:SceneHandle)=>void}
const palette=(t:number):[number,number,number]=>{
  const stops=[[.08,.16,.36],[.11,.46,.65],[.20,.75,.73],[.97,.81,.36],[.89,.28,.17]];
  const p=Math.min(1,Math.max(0,t))*4,i=Math.min(3,Math.floor(p)),f=p-i;
  return stops[i].map((c,k)=>c+(stops[i+1][k]-c)*f) as [number,number,number];
};
export function fieldScale(m:Manifest,mode:ViewMode):{min:number;max:number;label:string;column:number;multiplier:number}{
  if(mode==='damage'||mode==='fracture')return {min:0,max:1,label:mode==='fracture'?'Daño cohesivo · puntos de integración · 0–1':'Daño escalar · 0–1',column:2,multiplier:1};
  if(mode==='strain'){const v=Math.max(Math.abs(m.ranges.eps[0]),Math.abs(m.ranges.eps[1]))*100;return {min:-v,max:v,label:'Deformación longitudinal · %',column:4,multiplier:100};}
  const v=Math.max(Math.abs(m.ranges.sx[0]),Math.abs(m.ranges.sx[1]));return {min:-v,max:v,label:m.modelId==='fracture'?'Esfuerzo longitudinal del volumen · MPa':'Esfuerzo longitudinal con daño · MPa',column:3,multiplier:1};
}
export function Scene({manifest:m,mesh,state,fields,cohesiveFields,mode,scale,dark,onReady}:Props){
  const fracturePoints=useRef<THREE.Points|null>(null);
  const host=useRef<HTMLDivElement>(null),runtime=useRef<{renderer:THREE.WebGLRenderer;scene:THREE.Scene;camera:THREE.PerspectiveCamera;controls:OrbitControls;beam:THREE.Mesh;ghost:THREE.Mesh;geometry:THREE.BufferGeometry;realMaterial:THREE.MeshStandardMaterial;fieldMaterial:THREE.MeshBasicMaterial;rolls:THREE.Group[];head:THREE.Group;floor:THREE.Mesh;dirty:boolean}> (null);
  const [error,setError]=useState('');
  useEffect(()=>{
    fracturePoints.current=null;
    const el=host.current!;let frame=0;let renderer:THREE.WebGLRenderer;
    try{renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true,alpha:false});}catch{setError('No se pudo inicializar WebGL. Comprueba la aceleración gráfica de Windows.');return;}
    const gl=renderer.getContext(),debug=gl.getExtension('WEBGL_debug_renderer_info'),software=debug?/swiftshader|llvmpipe|software|basic render|warp/i.test(String(gl.getParameter(debug.UNMASKED_RENDERER_WEBGL))):false;
    renderer.setPixelRatio(software?.65:Math.min(window.devicePixelRatio,1.75));renderer.shadowMap.enabled=!software;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.08;renderer.outputColorSpace=THREE.SRGBColorSpace;
    el.appendChild(renderer.domElement);renderer.domElement.setAttribute('aria-label','Modelo tridimensional extruido de COMSOL');
    const scene=new THREE.Scene();scene.background=new THREE.Color('#e9eef3');scene.fog=new THREE.Fog('#e9eef3',1200,2600);
    const camera=new THREE.PerspectiveCamera(35,1,1,4000);camera.position.set(800,500,1030);
    const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,155,0);controls.enableDamping=true;controls.dampingFactor=.09;controls.minDistance=330;controls.maxDistance=1700;controls.maxPolarAngle=Math.PI*.84;
    scene.add(new THREE.HemisphereLight(0xdcefff,0x657080,2.2));
    const key=new THREE.DirectionalLight(0xffffff,3.4);key.position.set(-300,600,400);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-650,right:650,top:650,bottom:-650,near:1,far:1600});key.shadow.bias=-.0002;scene.add(key);
    const fill=new THREE.DirectionalLight(0xc0d9ff,2);fill.position.set(600,260,-400);scene.add(fill);
    const warm=new THREE.DirectionalLight(0xffe2bb,1.3);warm.position.set(-500,200,-300);scene.add(warm);
    const metal=new THREE.MeshStandardMaterial({color:'#8e9ca8',metalness:.88,roughness:.29});
    const body=new THREE.MeshStandardMaterial({color:'#273442',metalness:.65,roughness:.4});
    const black=new THREE.MeshStandardMaterial({color:'#111b24',metalness:.32,roughness:.52});
    const orange=new THREE.MeshStandardMaterial({color:'#ed743c',metalness:.28,roughness:.42});
    const box=(w:number,h:number,d:number,x:number,y:number,z:number,material:THREE.Material=metal,parent:THREE.Object3D=scene)=>{const a=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);a.position.set(x,y,z);a.castShadow=true;a.receiveShadow=true;parent.add(a);return a;};
    const cylinder=(r:number,h:number,x:number,y:number,z:number,material:THREE.Material=metal,parent:THREE.Object3D=scene)=>{const a=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,48),material);a.position.set(x,y,z);a.castShadow=true;a.receiveShadow=true;parent.add(a);return a;};
    const floor=new THREE.Mesh(new THREE.PlaneGeometry(3600,3600),new THREE.MeshStandardMaterial({color:'#dae1e8',roughness:.83}));floor.rotation.x=-Math.PI/2;floor.position.y=-126;floor.receiveShadow=true;scene.add(floor);
    box(780,28,335,0,-96,0,body);box(710,10,270,0,-77,0,metal);
    for(const x of [-335,335]){
      box(52,510,78,x,170,-68,body);box(10,475,8,x+15,170,-24,metal);
      cylinder(11,473,x-40,173,-40);box(95,28,122,x,-85,-48,black);
      for(let y=-36;y<410;y+=19){const ring=new THREE.Mesh(new THREE.TorusGeometry(11,1.1,5,20),metal);ring.rotation.x=Math.PI/2;ring.position.set(x-40,y,-40);scene.add(ring);}
      box(7,340,5,x-19,142,-25,orange);
    }
    box(745,46,128,0,441,-68,body);box(345,18,115,0,464,-68,black);cylinder(40,80,0,395,-68,black);cylinder(17,120,0,297,-68,metal);
    const head=new THREE.Group();head.position.set(0,241,0);scene.add(head);
    box(500,27,130,0,0,-50,body,head);box(225,17,180,0,-13,0,metal,head);box(112,26,104,0,22,-58,black,head);
    for(const x of [-75,75]){box(28,60,140,x,-42,0,metal,head);box(38,7,152,x,-62,0,black,head);}
    for(const x of [-225,225]){box(55,43,190,x,-52,0,metal);box(70,12,218,x,-68,0,black);}
    const rolls=m.states[0].rollers.map(r=>{const g=new THREE.Group();scene.add(g);const a=cylinder(m.geometry.rollerDiameter_mm/2,m.geometry.width_mm+38,0,0,0,metal,g);a.rotation.x=Math.PI/2;for(const z of [-87,87]){const cap=cylinder(18,6,0,0,z,black,g);cap.rotation.x=Math.PI/2;}return g;});
    // Panel de la maquina: detalle industrial decorativo, sin resultados inventados.
    box(99,110,25,400,265,25,body);box(82,66,3,400,284,40,new THREE.MeshStandardMaterial({color:'#101e2b',roughness:.5}));
    box(50,4,3,400,300,43,orange);box(65,3,3,400,285,43,metal);box(32,3,3,384,274,43,metal);
    const n=mesh.xy.length/2,positions=new Float32Array(n*2*3),colors=new Float32Array(n*2*3),uv=new Float32Array(n*2*2);
    for(let layer=0;layer<2;layer++)for(let i=0;i<n;i++){const j=layer*n+i;positions.set([mesh.xy[i*2],mesh.xy[i*2+1],(layer===0?1:-1)*m.geometry.width_mm/2],j*3);uv.set([(mesh.xy[i*2]+251)/70,mesh.xy[i*2+1]/70],j*2);colors.set([1,1,1],j*3);}
    const index:number[]=[];
    for(let i=0;i<mesh.triangles.length;i+=3){const [a,b,c]=mesh.triangles.slice(i,i+3);index.push(a,b,c,c+n,b+n,a+n);}
    for(let i=0;i<mesh.boundary.length;i+=2){const a=mesh.boundary[i],b=mesh.boundary[i+1];index.push(a,b,b+n,a,b+n,a+n);}
    const geometry=new THREE.BufferGeometry();geometry.setIndex(index);geometry.setAttribute('position',new THREE.BufferAttribute(positions,3));geometry.setAttribute('color',new THREE.BufferAttribute(colors,3));geometry.setAttribute('uv',new THREE.BufferAttribute(uv,2));geometry.computeVertexNormals();
    const canvas=document.createElement('canvas');canvas.width=256;canvas.height=256;const ctx=canvas.getContext('2d')!;const image=ctx.createImageData(256,256);let seed=917;
    for(let i=0;i<image.data.length;i+=4){seed=(seed*1664525+1013904223)>>>0;const g=155+((seed>>>24)%60);image.data.set([g,g-1,g-5,255],i);}ctx.putImageData(image,0,0);const texture=new THREE.CanvasTexture(canvas);texture.wrapS=texture.wrapT=THREE.RepeatWrapping;texture.colorSpace=THREE.SRGBColorSpace;
    const realMaterial=new THREE.MeshStandardMaterial({color:'#b9b8b1',map:texture,bumpMap:texture,bumpScale:.14,roughness:.94,metalness:0,side:THREE.DoubleSide});
    const fieldMaterial=new THREE.MeshBasicMaterial({vertexColors:true,side:THREE.DoubleSide,toneMapped:false});
    const beam=new THREE.Mesh(geometry,realMaterial);beam.castShadow=true;beam.receiveShadow=true;scene.add(beam);
    if(mesh.cohesiveY){const fg=new THREE.BufferGeometry(),count=mesh.cohesiveY.length*4;fg.setAttribute('position',new THREE.BufferAttribute(new Float32Array(count*3),3));fg.setAttribute('color',new THREE.BufferAttribute(new Float32Array(count*3),3));const pts=new THREE.Points(fg,new THREE.PointsMaterial({size:3.5,sizeAttenuation:false,vertexColors:true,depthTest:true,toneMapped:false}));pts.visible=false;scene.add(pts);fracturePoints.current=pts;}
    const ghost=new THREE.Mesh(geometry.clone(),new THREE.MeshBasicMaterial({color:'#387cad',wireframe:true,transparent:true,opacity:.14,depthWrite:false}));ghost.visible=false;scene.add(ghost);
    runtime.current={renderer,scene,camera,controls,beam,ghost,geometry,realMaterial,fieldMaterial,rolls,head,floor,dirty:true};
    const resize=()=>{const {width,height}=el.getBoundingClientRect();renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();if(runtime.current)runtime.current.dirty=true;};const observer=new ResizeObserver(resize);observer.observe(el);resize();
    const render=()=>{const moved=controls.update();if(runtime.current&&(runtime.current.dirty||moved)){renderer.render(scene,camera);runtime.current.dirty=false;}frame=requestAnimationFrame(render);};render();
    const reset=()=>{camera.position.set(800,500,1030);controls.target.set(0,155,0);controls.update();};
    onReady({capture:()=>{renderer.render(scene,camera);return renderer.domElement.toDataURL('image/png');},reset,front:()=>{camera.position.set(0,170,1180);controls.target.set(0,155,0);controls.update();},fracture:()=>{controls.minDistance=100;camera.position.set(100,95,250);controls.target.set(0,65,0);controls.update();}});
    return ()=>{cancelAnimationFrame(frame);observer.disconnect();controls.dispose();scene.traverse(obj=>{if(obj instanceof THREE.Mesh||obj instanceof THREE.Points){obj.geometry.dispose();const mats=Array.isArray(obj.material)?obj.material:[obj.material];mats.forEach(mat=>mat.dispose());}});texture.dispose();renderer.dispose();el.removeChild(renderer.domElement);runtime.current=null;fracturePoints.current=null;};
  },[mesh,m]);
  useEffect(()=>{
    const r=runtime.current;if(!r)return;const n=mesh.xy.length/2,pos=r.geometry.getAttribute('position') as THREE.BufferAttribute,col=r.geometry.getAttribute('color') as THREE.BufferAttribute;
    const mapping=fieldScale(m,mode),scientific=['stress','strain','damage'].includes(mode);
    for(let layer=0;layer<2;layer++)for(let i=0;i<n;i++){
      const j=layer*n+i;pos.setXYZ(j,mesh.xy[i*2]+fields[i*5]*scale,mesh.xy[i*2+1]+fields[i*5+1]*scale,(layer===0?1:-1)*m.geometry.width_mm/2);
      if(scientific){const value=fields[i*5+mapping.column]*mapping.multiplier;const color=palette((value-mapping.min)/(mapping.max-mapping.min||1)).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4) as [number,number,number];col.setXYZ(j,...color);}
    }
    pos.needsUpdate=true;col.needsUpdate=true;r.geometry.computeVertexNormals();r.geometry.computeBoundingSphere();r.beam.material=scientific?r.fieldMaterial:r.realMaterial;r.ghost.visible=mode==='comparison';r.dirty=true;r.renderer.shadowMap.needsUpdate=true;
    state.rollers.forEach((roller,i)=>{r.rolls[i].position.set(roller.X_mm+roller.u_mm*scale,roller.Y_mm+roller.v_mm*scale,0);r.rolls[i].rotation.z=roller.rotation_rad*scale;});
    const pts=fracturePoints.current;
    if(pts){pts.visible=mode==='fracture'&&!!cohesiveFields;if(pts.visible&&mesh.cohesiveY&&cohesiveFields){
      const fp=pts.geometry.getAttribute('position') as THREE.BufferAttribute,fc=pts.geometry.getAttribute('color') as THREE.BufferAttribute;
      // Boundary vertices from each connected half remain independent. A linear
      // interpolation maps displayed Gauss markers to the native deformed face.
      const faces:number[][]=[[],[]],half=(m as Manifest&{halfNodeCount?:number}).halfNodeCount??0;
      for(let i=0;i<n;i++)if(Math.abs(mesh.xy[i*2])<1e-5)faces[i<half?0:1].push(i);
      faces.forEach(face=>face.sort((a,b)=>mesh.xy[a*2+1]-mesh.xy[b*2+1]));
      for(let side=0;side<2;side++)for(let layer=0;layer<2;layer++)for(let k=0;k<mesh.cohesiveY.length;k++){
        const y=mesh.cohesiveY[k],face=faces[side];let a=face[0],b=face.at(-1)!;for(let z=1;z<face.length;z++)if(mesh.xy[face[z]*2+1]>=y){a=face[z-1];b=face[z];break;}
        const t=(y-mesh.xy[a*2+1])/(mesh.xy[b*2+1]-mesh.xy[a*2+1]||1),u=fields[a*5]*(1-t)+fields[b*5]*t,v=fields[a*5+1]*(1-t)+fields[b*5+1]*t,j=(side*2+layer)*mesh.cohesiveY.length+k;
        fp.setXYZ(j,u*scale,y+v*scale,(layer===0?1:-1)*(m.geometry.width_mm/2+.15));const rgb=palette(cohesiveFields[k*5]).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);fc.setXYZ(j,rgb[0],rgb[1],rgb[2]);
      }fp.needsUpdate=true;fc.needsUpdate=true;pts.geometry.computeBoundingSphere();
    }}
    r.head.position.y=241-state.head_mm*scale;r.head.rotation.z=state.rollers[2].rotation_rad*scale;
  },[fields,cohesiveFields,state,mode,scale,m,mesh]);
  useEffect(()=>{const r=runtime.current;if(!r)return;const color=dark?'#182331':'#e9eef3';r.scene.background=new THREE.Color(color);r.scene.fog=new THREE.Fog(color,1200,2600);(r.floor.material as THREE.MeshStandardMaterial).color.set(dark?'#222f3d':'#dae1e8');r.dirty=true;},[dark]);
  return <div ref={host} className="scene-host">{error&&<div className="scene-error" role="alert">{error}</div>}</div>;
}
