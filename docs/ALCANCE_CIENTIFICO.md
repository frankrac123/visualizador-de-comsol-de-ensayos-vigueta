# Alcance científico

Este proyecto es un prototipo académico de visualización fiel de resultados FEM. COMSOL resolvió los estados; la aplicación reproduce y compara esas soluciones.

| Aspecto | Estado real |
|---|---|
| Mecánica | Tensión plana 2D, extruida en 3D para visualizar |
| Mazars | Daño continuo; 127 estados, calibración al pico documental |
| Fractura | CZM bilineal, 345 estados, trayectoria vertical central prescrita |
| Apertura | Salto de desplazamientos entre caras FEM independientes |
| Volumen CZM | Elástico; no incluye aplastamiento ni plasticidad del concreto |
| Rotura final | Fractura avanzada; queda un ligamento que transmite carga |
| Validación | Sin curva experimental sincronizada de carga–flecha o apertura |
| Cálculo desde la interfaz | Pendiente; el visor utiliza resultados almacenados |

La resistencia a tracción efectiva procede de la calibración de Mazars. E, ν, energía de fractura, rigidez cohesiva y diámetro de rodillos incluyen hipótesis. El valor 14,5 kN es el pico del informe experimental, no una curva experimental completa. El pico CZM de referencia es 13,484 kN y no se ajustó artificialmente para igualarlo.

Se comprobaron contacto unilateral, equilibrio vertical, energía e irreversibilidad. Se calcularon tres mallas y variantes independientes. Los contactos pueden concentrar esfuerzos de compresión superiores a la resistencia documental: el modelo elástico no captura la posible falla local. No usar estas comprobaciones como validación de diseño estructural.

La disipación exacta se integra en COMSOL a partir de la historia nativa y de la ley bilineal isotrópica implementada. Su fórmula requiere propiedades normales/tangenciales iguales, mezcla Power α=1 y ausencia de viscosidad; no es una corrección ajustada ni una fórmula general para cualquier CZM. El acumulador explícito original se conserva como diagnóstico.

Más detalle: [informe](ciencia/INFORME_CIENTIFICO_ETAPA_II.pdf) y [formulación](ciencia/FORMULACION_Y_TRAZABILIDAD.md).
