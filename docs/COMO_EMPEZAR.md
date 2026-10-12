# Empezar sin enredos

## Solo quiero ver el ensayo

Descarga el ZIP de Windows en [Releases](https://github.com/frankrac123/visualizador-de-comsol-de-ensayos-vigueta/releases/tag/v2.0.0), extrae todo y abre `ABRIR_LAB.bat` dentro de `CONCRETE_LAB_3D_ETAPA_II`. No abras el EXE desde la vista comprimida del ZIP.

Para ver esfuerzos: selecciona un modelo físico, elige un estado y, en el panel izquierdo, selecciona **Esfuerzos**. La leyenda muestra unidades y escala. Para la fractura: selecciona **Fractura — CZM**, avanza hacia el estado 345 y usa **Fractura cohesiva** / **Acercar a la interfaz calculada**. Los factores ×10, ×25 y ×50 amplifican únicamente la visualización de desplazamientos.

**Iniciar ensayo** reproduce los estados guardados. La velocidad de reproducción no es tiempo físico. Una carga solo puede seleccionarse dentro del rango de la rama y del modelo activo.

Consulta el [manual completo](ciencia/MANUAL_USO.md).

## Quiero entender la ciencia

Lee [alcance y límites](ALCANCE_CIENTIFICO.md), [formulación](ciencia/FORMULACION_Y_TRAZABILIDAD.md) y el [informe PDF](ciencia/INFORME_CIENTIFICO_ETAPA_II.pdf). El informe conserva la organización de la carpeta científica original; la [procedencia](PROCEDENCIA.md) explica su correspondencia con este repositorio.

## Quiero modificar el programa

Sigue [desarrollo](DESARROLLO.md). No necesitas COMSOL para cambiar la interfaz ni reproducir los datos incluidos.

## Quiero ejecutar COMSOL

Sigue [reproducción científica](../comsol/README.md). Sí necesitas COMSOL instalado y licenciado. Esta versión no tiene un botón que lance nuevos cálculos desde el visor.

## Problemas habituales

| Problema | Solución |
|---|---|
| Descargué código y no encuentro el EXE | Descarga el archivo de **Releases**, no “Source code” |
| El programa no abre después de mover el EXE | Conserva toda la carpeta extraída; el EXE necesita sus archivos vecinos |
| No veo la abertura a escala real | Usa el acercamiento y una escala de desplazamientos indicada |
| Una carga no está disponible | Revisa modelo, rama y pico; Mazars y CZM tienen rangos distintos |
| El mapa tarda en aparecer | Espera a que termine de cargar el estado; requiere WebGL |

Si Windows muestra una advertencia de editor, el ejecutable no tiene firma de código. Comprueba que viene de este repositorio y verifica su SHA-256 con `SHA256SUMS.txt`; no desactives la protección del sistema.
