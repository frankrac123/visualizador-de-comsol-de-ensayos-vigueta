# Cálculo científico con COMSOL

Aquí están los scripts de referencia Python/API Java del modelo CZM, un modelo Java exportado y resultados independientes. No se requiere esta carpeta para abrir el programa Windows. Resolver exige **COMSOL 6.1 y los módulos/licencias que habiliten Solid Mechanics, Contact, Adhesion y Decohesion**; no se distribuye una licencia.

## Entorno y carpetas

Python 3.11 fue el entorno de cálculo original. Crea un entorno virtual e instala `python -m pip install -r comsol/requirements.txt`. La versión del wrapper mph debe ser compatible con tu instalación COMSOL; las demás dependencias no constituyen un entorno congelado bit por bit. Comprueba `python -c "import mph; print(mph.start(version='6.1', cores=2))"`.

Trabaja desde `comsol/etapa_II/02_Codigo`. Los scripts crean MPH, Java, JSON y campos en `../03_Modelos`, muestras en `../04_Verificacion` y verificaciones en `../05_Resultados`; estas salidas grandes están excluidas de Git.

## Verificar primero una muestra

```sh
python verificar_czm.py --mesh 2.5 --kind tension
python verificar_czm.py --mesh 1.25 --kind tension --increments 1001
python verificar_czm.py --mesh 1.25 --kind cycle --increments 1001
python energia_constitutiva_exacta.py --coupons
python analizar_verificacion.py
```

La muestra de compresión comprueba contacto y elasticidad; no aplastamiento. `serie_uniaxial.py` ejecuta las muestras iniciales. Se conservan las discrepancias del acumulador explícito en pasos gruesos; no confundirlas con la disipación constitutiva exacta.

## Resolver la vigueta de referencia

```sh
python vigueta_czm.py --mesh 8 --max-opening 0.6 --step 0.002
python vigueta_czm.py --mesh 6 --max-opening 0.6 --step 0.002
python vigueta_czm.py --mesh 4 --max-opening 0.6 --step 0.002
```

La geometría de referencia está definida en el script: 502 × 130,333 × 151 mm, luz 450 mm, cuatro rodillos de diámetro supuesto 30 mm. No es un importador genérico de vigas. La trayectoria central está prescrita. El volumen es elástico, sin falla por compresión. Un cálculo completo tardó entre 20 y 42 minutos en el equipo original, antes de todo el posprocesado.

`--ft`, `--gf` y `--kn` permiten variantes; no calibran automáticamente contra una curva experimental.

## Extraer, verificar e integrar

Para el modelo de 8 mm, desde la carpeta del código:

```sh
python extraer_campos_czm.py ../03_Modelos/CZM_h8_ft0.878515_Gf220_K1e+14_o0.6_ds0.002 --out ../05_Resultados/visor_fractura_avanzada
python energia_constitutiva_exacta.py
python verificar_historia_interfaz.py
python comprobar_marco_integracion.py
python analizar_viguetas.py
```

La extracción inicial marca energía provisional. No sustituir los datos del visor antes de completar energía exacta, historia y aceptación. `energia_constitutiva_exacta.py` actualiza el manifiesto extraído que corresponde al modelo fuente. Si repites extracción, repite el posprocesado.

`preparar_entrega_cientifica.py` está destinado a reproducir **el conjunto completo** de tres mallas y cinco series cortas de sensibilidad; exige esa configuración, perfiles nativos, manifiesto de 345 estados y todos los casos aceptados. No es un importador para cualquier ensayo. Modifica el catálogo y la comparación de `public/data/fracture/`; ejecutarlo solo tras preparar y verificar ese conjunto y respaldar los datos.

Series cortas: referencia `--mesh 8 --max-opening 0.3 --step 0.003`, y cuatro variantes independientes añadiendo `--gf 110`, `--gf 440`, `--ft 1.054217796` o `--kn 5e13`, una por ejecución. Todas utilizan el mismo protocolo. La comparación no necesita interpolación entre controles nativos.

## Qué está verificado y qué no

Los algoritmos y parámetros de la entrega original se ejecutaron en COMSOL. La copia para GitHub adapta importaciones/rutas; se verifica su sintaxis y la equivalencia de las funciones auxiliares, sin repetir todos los cálculos FEM únicamente por reorganizar carpetas. Los resultados públicos pertenecen a la entrega original. La conexión automática desde el botón del visor a un cálculo nuevo todavía está pendiente.

`modelos_java/vigueta_fractura.java` reproduce la configuración exportada de COMSOL. Requiere sus herramientas Java; no se ejecuta con el JDK estándar aislado. Se retiró únicamente la ruta personal `modelPath`. Los MPH originales se conservan fuera del repositorio.
