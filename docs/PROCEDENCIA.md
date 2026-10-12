# Procedencia y organización pública

La publicación reorganiza copias de la entrega científica Etapa II. Los archivos originales permanecen en el proyecto local; no se alteraron los modelos al preparar GitHub.

Los 827 archivos de `public/data/` se copiaron byte por byte. `comsol/resultados_referencia/integridad_datos.json` conserva tamaño y SHA-256. Los manifiestos mantienen los identificadores y hashes de los MPH de origen, aunque esos MPH no se distribuyen en Git. Las rutas históricas son referencias al proyecto científico original, no rutas que el visor necesite abrir.

El JSON CZM independiente y el CSV global conservan los valores originales. El modelo Java solo cambia `modelPath` a `.` para retirar una ruta personal. Los scripts publicados extraen tres funciones auxiliares COMSOL y dos auxiliares de malla sin cambiar sus algoritmos; se adaptan únicamente importaciones y rutas al árbol público.

El PDF es el informe original revisado de ocho páginas. Sus rutas se refieren a carpetas originales: `06_Documentacion` corresponde aquí a `docs/ciencia`, `05_Resultados` a las figuras y referencias documentadas, y `02_Codigo` a `comsol/etapa_II/02_Codigo`.

Las capturas y `docs/verificacion/ui-results-original.json` son evidencia de la entrega original. La validación específica de la copia pública se registra por separado en `docs/verificacion/PUBLICACION.md`.

Durante la validación original se sustituyó un log generado de pruebas UI cuya versión anterior no se recuperó; el informe de ejemplo anterior sí se recuperó. Esta incidencia no cambió las fuentes MPH ni los datos físicos y no debe describirse como preservación absoluta de todos los archivos auxiliares históricos.

No se publican seriales/licencias COMSOL, PDFs de terceros, entornos instalados ni temporales. El paquete Windows publicado contiene resultados y runtime de visualización, no el software COMSOL ni sus modelos binarios.
