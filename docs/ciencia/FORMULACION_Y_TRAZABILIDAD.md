# Formulación del modelo B

## Hipótesis mecánicas

Tensión plana, espesor 130,333333 mm. El sólido es elástico isotrópico: E=25 GPa, ν=0,2. La interfaz central vertical admite adhesión, daño irreversible y cierre por contacto. Esta elección prescribe la trayectoria X=0 mm; permite propagación sobre esa línea, no búsqueda de una trayectoria arbitraria. Los rodillos y cabezal mantienen la geometría del modelo A. El cabezal puede bascular y la carga se obtiene de sus contactos.

El módulo elástico, Poisson, diámetro de rodillos y condiciones del cabezal son supuestos. ft=0,87851483 MPa fue calibrado para Mazars y solo se transfiere como comparación inicial; no se identifica automáticamente con una resistencia cohesiva medida. Gf=220 J/m² fue adoptado. Kn=10¹⁴ N/m³, kt/kn=1, resistencia tangencial=ft y energía tangencial=Gf son hipótesis explícitas pendientes de sensibilidad. No se incorpora viscosidad ni longitud interna de Mazars a esta interfaz.

## Ecuaciones

En el límite de pequeñas deformaciones: div(σ)=0, σ=C:ε y ε=sym(∇u). El cálculo usa geometría no lineal: F=I+∇_X u, E_G=(FᵀF−I)/2, S=C:E_G, P=FS y Div(P)=0 en referencia. La tensión de Cauchy es σ=FSFᵀ/det(F); la tensión plana elimina la componente normal fuera del plano. La derivada material d(u,X) del visor no es todo el tensor Green-Lagrange.

Para apertura normal δ≥0 en modo I: δ₀=ft/Kn; δf=2Gf/ft. La envolvente es t=Kn δ hasta δ₀, t=ft(δf−δ)/(δf−δ₀) entre δ₀ y δf, y t=0 después de δf.

Historia κ=max de las aperturas alcanzadas. D=0 si κ≤δ₀; D=δf(κ−δ₀)/[κ(δf−δ₀)] si δ₀<κ<δf; D=1 después. Descarga/recarga: t=(1−D)Kn δ. Compresión: el contacto permanece activo, sin recuperar el daño. La ley nativa tiene también respuesta tangencial y criterio mixto Power con α=1; la expresión escalar anterior es su límite de modo I, verificado en una muestra independiente.

δ₀≈8,78515·10⁻⁶ mm; δf≈0,500845 mm. D próximo a uno no significa que la interfaz carezca de tracción: con Kn alto, una interfaz parcialmente dañada puede mantener una fuerza considerable. La apertura y tracción deben mostrarse junto al daño.

Energía superficial total de modo I: ∫t dδ=Gf. Antes de rotura completa, la energía recuperable es ½tδ. La disipación analítica de la envolvente en modo I es Gf·clip[(κ−δ₀)/(δf−δ₀),0,1]. Esta expresión sirve para verificar el acumulador nativo; no sustituye automáticamente el balance de un estado mixto.

Se verificó además su aplicación al modelo nativo implementado con iguales propiedades normales y tangenciales, kt/kn=1, Power α=1 y viscosidad nula. La identidad D(κ) concuerda punto a punto con COMSOL hasta error de redondeo. La expresión se integra en COMSOL sobre el área cohesiva de referencia y el balance global incluye las energías recuperables de volumen, adhesión y contacto. El máximo desbalance de la vigueta de 8 mm es 0,071736 %. Para propiedades mixtas desiguales o regularización viscosa se necesita otra derivación; el script rechaza esas configuraciones.

## Alcance de la compresión

La resistencia documental fc=10,296221 MPa no aparece como criterio de fallo volumétrico del modelo B inicial. La prueba de compresión comprueba el contacto y la elasticidad, no el aplastamiento real del concreto. Tensiones compresivas elevadas alrededor de los rodillos requieren discutir esta limitación y no pueden presentarse como material experimentalmente validado.

## Solución y criterios

Primero se establece el contacto con una pequeña carrera impuesta. Después, un grado de libertad global controla el cabezal para satisfacer uR−uL=CMOD en las dos caras inferiores de la interfaz. Se continúa monótonamente en esa apertura. CMOD aquí designa la apertura inferior entre caras calculadas; no es la extensión de los puntos inferiores separados 450 mm del modelo A.

Se aceptarán exclusivamente estados con campos finitos, contacto sin tracción artificial, equilibrio compatible con la tolerancia de extracción, historia irreversible y balance energético estudiado. El prefijo convergido de un solver detenido no se aceptará sin esas comprobaciones. Una discrepancia de energía o de malla se documentará como pendiente; no se ajustarán ft y Gf simultáneamente para obtener 14,5 kN.

## Evaluación nativa

Los desplazamientos son incógnitas FEM. Las variables internas de contacto se muestrean con `gpeval(2,...)`, correspondiente a la cuadratura explícita de orden 2 para estos elementos lineales. La densidad disipada real de esta versión se llama `solid.Wbdmg`; el manual presenta en una tabla el orden de letras `Wdbmg`, que no existe en el modelo probado. Se conserva evidencia de las consultas y no se completa una variable ausente con cero.

Se mantiene la identidad de los nodos de cada mitad al exportar campos. Cada cara recibe su desplazamiento nativo; nunca se genera una apertura proporcional al daño.

## Fuentes

- COMSOL 6.1 Structural Mechanics, teoría de Decohesion: https://doc.comsol.com/6.1/doc/com.comsol.help.sme/sme_ug_theory.06.086.html
- COMSOL 6.1, guía local, Important Contact Variables, Internal Variables, Gauss Point Evaluation.
- Ejemplo instalado `Structural_Mechanics_Module/Contact_and_Friction/cohesive_zone_debonding.mph`, leído sin modificación, empleado únicamente para conocer la API.
- COMSOL 6.2 Structural Mechanics release: la interfaz nativa Phase Field in Solids se introduce en 6.2; no se atribuye a la instalación 6.1.
