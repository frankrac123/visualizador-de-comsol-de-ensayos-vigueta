const { app, BrowserWindow, protocol, net } = require('electron');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
protocol.registerSchemesAsPrivileged([{scheme:'concrete',privileges:{standard:true,secure:true,supportFetchAPI:true}}]);
app.whenReady().then(() => {
  const root=path.join(app.getAppPath(),'dist');
  protocol.handle('concrete', request => {
    const url=new URL(request.url);const target=path.resolve(root,'.'+decodeURIComponent(url.pathname));
    if (url.hostname!=='app' || !target.startsWith(root+path.sep)) return new Response('Ruta no permitida',{status:403});
    return net.fetch(pathToFileURL(target).toString());
  });
  const win=new BrowserWindow({width:1560,height:980,minWidth:1100,minHeight:740,title:'CONCRETE LAB 3D',backgroundColor:'#edf1f5',autoHideMenuBar:true,webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true}});
  win.webContents.setWindowOpenHandler(()=>({action:'deny'}));
  win.webContents.on('will-navigate',(event,url)=>{if (!url.startsWith('concrete://app/'))event.preventDefault();});
  win.loadURL('concrete://app/index.html');
  win.webContents.session.on('will-download',(_event,item)=>{
    item.once('done',(_e,state)=>{if(state==='completed')console.log('Exportado',item.getSavePath());});
  });
});
app.on('window-all-closed',()=>app.quit());
