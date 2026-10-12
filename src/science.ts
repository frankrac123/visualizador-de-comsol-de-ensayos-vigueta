export type Branch='ascending'|'descending';
export interface Manifest {modelId?:'mazars'|'fracture';modelName?:string;dataPath?:string;halfNodeCount?:number;cohesive?:{points:number;coordinates:string;fieldsOrder:string[];quadratureOrder:number};energyVerification?:{max_relative_residual_percent:number};energyMethod?:{scope:string};numericalVerification?:{status:string}}
export interface State {cohesiveFields?:string;opening_mm?:number;openingMaxGauss_mm?:number;fractureEnergy_J?:number;externalWorkFromFirst_J?:number;energyResidual_J?:number;convergence?:string}
export interface Roller {name:string;X_mm:number;Y_mm:number;u_mm:number;v_mm:number;rotation_rad:number;fit_error_mm:number}
export interface State {id:number;branch:Branch;load_kN:number;deflection_mm:number;extension_mm:number;head_mm:number;damageMax:number;damageMean:number;reactionLeft_kN:number;reactionRight_kN:number;stressLocal_MPa:number;strainLocal:number;damageLocal:number;stressCenter_MPa:number;strainCenter:number;rollers:Roller[];fields:string;source:string;solution:number;equilibriumError:number}
export interface Comparison {id:string;label:string;load_kN:number[];deflection_mm:number[];extension_mm:number[];source:string;note:string;kind?:'mesh'|'sensitivity';opening_mm?:number[]}
export interface Manifest {schemaVersion:number;project:string;comsolVersion:string;modelDimension:number;visualDimension:number;geometry:{length_mm:number;width_mm:number;height_mm:number;span_mm:number;loadX_mm:number[];rollerDiameter_mm:number};material:{model:string;E_GPa:number;nu:number;fc_MPa:number;ft_MPa:number;Gft_J_m2:number;internalLength_mm:number};peakIndex:number;experimentalPeak_kN:number;criticalPoint_mm:number[];states:State[];cases:Comparison[];mesh:{nodes:number;triangles:number;boundaryEdges:number;coordinates:string;connectivity:string;boundary:string;method:string};fieldsOrder:string[];ranges:Record<string,[number,number]>;sources:{path:string;sha256:string;states:number}[];quantization:{format:string;maxAbsoluteError:number};limitations:string[]}
export const strainPercent=(fraction:number)=>fraction*100;
export const newtonsToKilonewtons=(value:number)=>value/1000;
export function stateUid(m:Manifest,s:State):string{return `${m.modelId??'mazars'}:${m.sources.find(src=>src.path===s.source)?.sha256??'source-unknown'}:${s.solution}`;}
export function branchIndices(m:Manifest,branch:Branch):number[]{return m.states.map((_,i)=>i).filter(i=>branch==='ascending'?i<=m.peakIndex:i>=m.peakIndex);}
export function selectLoad(m:Manifest,target:number,branch:Branch):{index:number;requested:number;exact:boolean;error?:string}{
  const indices=branchIndices(m,branch), loads=indices.map(i=>m.states[i].load_kN);const low=Math.min(...loads),high=Math.max(...loads);
  if(!Number.isFinite(target)||target<low-1e-9||target>high+1e-9)return {index:-1,requested:target,exact:false,error:`Carga fuera de la rama disponible (${low.toFixed(3)}–${high.toFixed(3)} kN).`};
  const index=indices.reduce((best,i)=>Math.abs(m.states[i].load_kN-target)<Math.abs(m.states[best].load_kN-target)?i:best,indices[0]);
  return {index,requested:target,exact:Math.abs(m.states[index].load_kN-target)<1e-8};
}
export function selectDeflection(m:Manifest,target:number):number {
  if(!Number.isFinite(target)||target<Math.min(...m.states.map(s=>s.deflection_mm))||target>Math.max(...m.states.map(s=>s.deflection_mm)))return -1;
  return m.states.reduce((best,s,i)=>Math.abs(s.deflection_mm-target)<Math.abs(m.states[best].deflection_mm-target)?i:best,0);
}
export function interpolateCompatible(a:State,b:State,t:number):{load_kN:number;deflection_mm:number;estimated:true}{
  if(t<0||t>1||!Number.isFinite(t)||b.id!==a.id+1||a.branch!==b.branch)throw new Error('Solo estados adyacentes de la misma rama; sin extrapolación.');
  return {load_kN:a.load_kN+(b.load_kN-a.load_kN)*t,deflection_mm:a.deflection_mm+(b.deflection_mm-a.deflection_mm)*t,estimated:true};
}
export function validateManifest(m:Manifest):void{
  if(m.schemaVersion!==1||m.states.length<2||m.mesh.nodes<3)throw new Error('Esquema de datos incompleto');
  for(const [i,s] of m.states.entries()){
    if(s.id!==i+1||!Object.values(s).filter(v=>typeof v==='number').every(Number.isFinite))throw new Error('Estado inválido');
    if(s.damageMax<0||s.damageMax>1.000001||s.damageMean<0||s.damageMean>1.000001)throw new Error('Daño fuera de rango');
    if(Math.abs(s.reactionLeft_kN+s.reactionRight_kN-s.load_kN)>.001*Math.max(s.load_kN,.001))throw new Error('Reacciones inconsistentes');
  }
  if(m.states[m.peakIndex].load_kN!==Math.max(...m.states.map(s=>s.load_kN)))throw new Error('Pico incoherente');
}
