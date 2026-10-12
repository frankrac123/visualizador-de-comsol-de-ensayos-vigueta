# Desarrollo, pruebas y empaquetado

## Preparar

Usa Node.js 24 LTS. Ejecuta `npm ci` en la raíz. `npm run dev` sirve el visor en localhost:5178. `npm run build` genera `dist/`, y `npm run desktop` abre esa compilación con Electron.

El código JavaScript de escritorio sirve archivos locales mediante un protocolo restringido; el navegador no tiene acceso directo a Node.js. Los datos se cargan desde `public/data/` y no se requieren servicios externos para visualizar.

## Pruebas portables

`npm test` comprueba datos, unidades, selección de ramas, conectividad de caras, apertura nodal, energía contra la extracción JSON y SHA-256 de todos los archivos científicos incluidos. Dos pruebas de hashes MPH aparecen como **skipped** sin fuentes nativas. No se consideran verificadas por esta omisión.

Para ejecutarlas también en PowerShell:

```powershell
$env:COMSOL_PROJECT_DIR = 'D:\Proyecto_COMSOL_Vigueta'
npm run test:native
```

La carpeta debe contener las rutas originales documentadas en los manifiestos. El comando falla si se pide la verificación nativa y falta la variable o un archivo.

## Pruebas de interfaz

```sh
npm run build
npx playwright install chromium
npm run test:ui
```

En Windows también puede usarse Edge: `$env:PLAYWRIGHT_CHANNEL='msedge'`. Son cinco pruebas que incluyen reproducción, cambio de modelos y descargas PNG/SVG/CSV/Excel/PDF. Las salidas van a `validation/etapa_II/`, excluida de Git.

## Paquete Windows

```sh
npm run package:windows
```

Genera `release/ConcreteLab3D_CZM-win32-x64/`. El empaquetador puede necesitar descargar el runtime Electron y requiere conexión en ese paso. Copia o comprime la carpeta completa; no distribuyas el EXE aislado. Este comando crea una aplicación nueva del código del repositorio, no reemplaza el ZIP científico original de Releases.

## Datos y modelos nuevos

`public/data/manifest.json` describe Mazars y `public/data/fracture/manifest.json` CZM. Cada estado referencia sus campos binarios. Un cambio de modelo carga malla, datos y campos compatibles antes de cambiar la escena. El catálogo está en `public/data/model_catalog.json`.

No sustituyas curvas manteniendo campos de otro cálculo. La integración de un cálculo nuevo requiere validar unidades, malla, orden de campos, identificadores y energía; el procedimiento científico de referencia está en `comsol/README.md`. No hay conexión de cálculo en vivo en esta versión.
