import {useEffect,useRef} from 'react';
import * as echarts from 'echarts';
import type {Manifest} from './science';
export type PlotMode='load-deflection'|'load-extension'|'load-control'|'load-opening'|'energy'|'compare-models'|'damage'|'local'|'displacement'|'reactions'|'mesh'|'sensitivity'|'weight';
export const plotNames:Record<PlotMode,string>={'load-deflection':'Carga · flecha','load-extension':'Carga · extensión entre apoyos','load-control':'Carga · variable controlada','load-opening':'Carga · apertura inferior',energy:'Energía cohesiva disipada','compare-models':'Comparación Mazars · Fractura',damage:'Evolución del daño / fractura',local:'Esfuerzo · deformación local',displacement:'Desplazamiento · estado',reactions:'Reacciones de apoyo',mesh:'Comparación de mallas',sensitivity:'Sensibilidad de parámetros CZM',weight:'Comparación de peso propio'};
export function plotSpec(m:Manifest,mode:PlotMode,index:number,dark:boolean,playing=false){
  const colors=['#de6b3c','#328599','#9257af','#84a44b'];const data=(x:(i:number)=>number,y:(i:number)=>number)=>m.states.map((s,i)=>[x(i),y(i),i]);
  let xlabel='Flecha central (mm)',ylabel='Carga (kN)',points=data(i=>m.states[i].deflection_mm,i=>m.states[i].load_kN),extra:unknown[]=[];
  if(mode==='load-extension'){xlabel='Extensión entre apoyos (mm)';points=data(i=>m.states[i].extension_mm,i=>m.states[i].load_kN);}
  if(mode==='load-control'){xlabel=m.modelId==='fracture'?'Apertura inferior controlada (mm)':'Extensión controlada (mm)';points=data(i=>m.modelId==='fracture'?m.states[i].opening_mm!:m.states[i].extension_mm,i=>m.states[i].load_kN);}
  if(mode==='load-opening'){xlabel='Apertura inferior entre caras (mm)';points=m.states.every(s=>s.opening_mm!==undefined)?data(i=>m.states[i].opening_mm!,i=>m.states[i].load_kN):[];}
  if(mode==='energy'){xlabel='Estado FEM';ylabel='Energía cohesiva disipada (J)';points=m.states.every(s=>s.fractureEnergy_J!==undefined)?data(i=>i+1,i=>m.states[i].fractureEnergy_J!):[];}
  if(mode==='compare-models'){extra=m.cases.filter(c=>c.id==='fracture').map(c=>({name:c.label,data:c.deflection_mm.map((x,i)=>[x,c.load_kN[i],-1])}));}
  if(mode==='damage'){xlabel='Estado aceptado';ylabel='Daño (0–1)';points=data(i=>i+1,i=>m.states[i].damageMax);extra=[{name:'Daño medio',data:data(i=>i+1,i=>m.states[i].damageMean)}];}
  if(mode==='local'){xlabel='Deformación material (%)';ylabel='Esfuerzo longitudinal (MPa)';points=data(i=>m.states[i].strainLocal*100,i=>m.states[i].stressLocal_MPa);extra=m.modelId==='fracture'?[]:[{name:'Centro inferior',data:data(i=>m.states[i].strainCenter*100,i=>m.states[i].stressCenter_MPa)}];}
  if(mode==='displacement'){xlabel='Estado aceptado';ylabel='Desplazamiento (mm)';points=data(i=>i+1,i=>m.states[i].deflection_mm);extra=[{name:'Carrera de cabezal',data:data(i=>i+1,i=>m.states[i].head_mm)}];}
  if(mode==='reactions'){xlabel='Estado aceptado';ylabel='Reacción (kN)';points=data(i=>i+1,i=>m.states[i].reactionLeft_kN);extra=[{name:'Apoyo derecho',data:data(i=>i+1,i=>m.states[i].reactionRight_kN)}];}
  if(mode==='mesh'||mode==='weight'){
    xlabel='Extensión entre apoyos (mm)';points=data(i=>m.states[i].extension_mm,i=>m.states[i].load_kN);
    extra=m.cases.filter(c=>mode==='mesh'?(m.modelId==='fracture'?c.kind==='mesh':c.id!=='peso_propio'&&c.id!=='fracture'):c.id==='peso_propio').map(c=>({name:c.label,data:c.extension_mm.map((x,i)=>[x,c.load_kN[i],-1])}));
  }
  if(mode==='sensitivity'){xlabel='Apertura inferior controlada (mm)';points=m.modelId==='fracture'?data(i=>m.states[i].opening_mm!,i=>m.states[i].load_kN):[];extra=m.cases.filter(c=>c.kind==='sensitivity').map(c=>({name:c.label,data:c.opening_mm!.map((x,i)=>[x,c.load_kN[i],-1])}));}
  if(mode==='mesh'&&m.modelId==='fracture'){xlabel='Apertura inferior controlada (mm)';points=data(i=>m.states[i].opening_mm!,i=>m.states[i].load_kN);extra=m.cases.filter(c=>c.kind==='mesh').map(c=>({name:c.label,data:c.opening_mm!.map((x,i)=>[x,c.load_kN[i],-1])}));}
  if(mode==='weight'&&m.modelId==='fracture')points=[];
  const selected=points[index]??[];const series:any[]=[{name:mode==='compare-models'?'Mazars · escena actual':mode==='local'?'Zona crítica':mode==='damage'?(m.modelId==='fracture'?'Daño cohesivo máximo':'Daño máximo'):mode==='reactions'?'Apoyo izquierdo':'Caso elegido',type:'line',data:points,showSymbol:false,smooth:false,lineStyle:{width:2.5},emphasis:{disabled:true},markPoint:mode.startsWith('load')&&points.length?{symbolSize:34,data:[{type:'max',name:'Máximo'}],label:{formatter:'Pico',fontSize:9},itemStyle:{color:'#e16f3e'}}:undefined,markLine:mode==='compare-models'?{silent:true,data:[{yAxis:m.experimentalPeak_kN,name:'Pico experimental · flecha desconocida'}],label:{formatter:'Pico experimental 14,5 kN · flecha desconocida'}}:undefined},...extra.map((s:any)=>({...s,type:'line',showSymbol:false,smooth:false,lineStyle:{width:1.7,type:'dashed'},emphasis:{disabled:true}})),{name:'Estado seleccionado',type:'scatter',data:selected.length?[selected]:[],symbolSize:11,itemStyle:{color:'#e16f3e',borderColor:dark?'#172333':'white',borderWidth:3},z:12}];
  if(playing){series[0].data=points.slice(0,index+1);if(index<m.peakIndex)series[0].markPoint=undefined;series.push({name:'Trayectoria disponible',type:'line',data:points,showSymbol:false,silent:true,lineStyle:{width:1,color:dark?'#435469':'#d6dde5'},z:0});}
  const option:any={animation:false,color:colors,backgroundColor:'transparent',textStyle:{fontFamily:'Segoe UI, sans-serif',color:dark?'#a4b5c7':'#697581'},grid:{left:76,right:26,top:38,bottom:65},legend:{top:0,type:'scroll',textStyle:{fontSize:10,color:dark?'#a4b5c7':'#697581'}},tooltip:{trigger:'axis',confine:true,formatter:(params:any[])=>params.filter(p=>!['Estado seleccionado','Trayectoria disponible'].includes(p.seriesName)).map(p=>`${p.marker} ${p.seriesName}<br>${p.value[0].toFixed(5)} · ${p.value[1].toFixed(5)}${p.value[2]>=0?` · Estado ${p.value[2]+1}`:''}`).join('<br>')},xAxis:{type:'value',name:xlabel,nameLocation:'middle',nameGap:30,nameTextStyle:{fontSize:10},axisLabel:{fontSize:10},splitLine:{lineStyle:{color:dark?'#2b3847':'#edf0f3'}}},yAxis:{type:'value',name:ylabel,nameLocation:'middle',nameGap:51,nameTextStyle:{fontSize:10},axisLabel:{fontSize:10},splitLine:{lineStyle:{color:dark?'#2b3847':'#edf0f3'}}},dataZoom:[{type:'inside',filterMode:'none'},{type:'slider',height:12,bottom:1,borderColor:'transparent',handleSize:12,textStyle:{fontSize:9},fillerColor:'rgba(221,104,60,.13)'}],series};
  if(!points.length)option.title={text:'No disponible para este modelo',left:'center',top:'middle',textStyle:{fontSize:14}};
  return {option,points,xlabel,ylabel,selected};
}
export interface ChartHandle {png:()=>string;svg:()=>string}
export function Charts({manifest,mode,index,dark,playing,onSelect,onReady}:{manifest:Manifest;mode:PlotMode;index:number;dark:boolean;playing:boolean;onSelect:(i:number)=>void;onReady:(c:ChartHandle)=>void}){
  const host=useRef<HTMLDivElement>(null),chart=useRef<echarts.ECharts|null>(null),selectRef=useRef(onSelect),current=useRef({manifest,mode,index,dark});selectRef.current=onSelect;current.current={manifest,mode,index,dark};
  useEffect(()=>{
    const c=echarts.init(host.current!);chart.current=c;
    const reposition=()=>{if(!(c.getOption() as any)?.xAxis?.length)return;const spec=plotSpec(current.current.manifest,current.current.mode,current.current.index,current.current.dark);if(!spec.selected.length)return;c.setOption({graphic:[{id:'state-handle',position:c.convertToPixel({gridIndex:0},spec.selected.slice(0,2))}]});};
    const observer=new ResizeObserver(()=>{c.resize();reposition();});observer.observe(host.current!);c.on('datazoom',reposition);
    c.on('click',(p:any)=>{if(Array.isArray(p.value)&&p.value[2]>=0)selectRef.current(p.value[2]);});
    const exportChart=(renderer:'svg'|'canvas')=>{const el=document.createElement('div');el.style.cssText='width:1100px;height:480px;position:absolute;left:-9999px';document.body.appendChild(el);const a=echarts.init(el,undefined,{renderer});a.setOption(plotSpec(current.current.manifest,current.current.mode,current.current.index,current.current.dark).option);const result=renderer==='svg'?a.renderToSVGString():a.getDataURL({type:'png',pixelRatio:2,backgroundColor:current.current.dark?'#172333':'#ffffff'});a.dispose();el.remove();return result;};
    onReady({png:()=>exportChart('canvas'),svg:()=>exportChart('svg')});
    return ()=>{observer.disconnect();c.dispose();chart.current=null;};
  },[]);
  useEffect(()=>{
    const c=chart.current;if(!c)return;const spec=plotSpec(manifest,mode,index,dark,playing);const previous=c.getOption() as any;
    if(previous?.dataZoom?.length)spec.option.dataZoom.forEach((z:any,i:number)=>Object.assign(z,{start:previous.dataZoom[i]?.start,end:previous.dataZoom[i]?.end}));
    c.setOption(spec.option,{notMerge:true});
    if(!spec.points.length)return;
    const pixel=c.convertToPixel({gridIndex:0},spec.selected.slice(0,2)) as unknown as number[];
    c.setOption({graphic:[{id:'state-handle',type:'circle',shape:{r:10},position:pixel,invisible:true,draggable:true,z:100,ondrag:function(this:any){
      const pos=c.convertFromPixel({gridIndex:0},this.position) as unknown as number[];
      const xs=spec.points.map(p=>p[0]),ys=spec.points.map(p=>p[1]),dx=Math.max(...xs)-Math.min(...xs)||1,dy=Math.max(...ys)-Math.min(...ys)||1;
      const nearest=spec.points.reduce((best,p,i)=>Math.hypot((p[0]-pos[0])/dx,(p[1]-pos[1])/dy)<Math.hypot((spec.points[best][0]-pos[0])/dx,(spec.points[best][1]-pos[1])/dy)?i:best,0);selectRef.current(nearest);
    }}]});
  },[manifest,mode,index,dark,playing]);
  return <div className="chart-host" ref={host} aria-label={`Gráfica ${plotNames[mode]}`}/>;
}
