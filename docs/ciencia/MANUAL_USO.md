# Usar CONCRETE LAB 3D — Etapa II

1. Abre el programa de la Etapa II y espera a que cargue el primer estado.
2. En **Modelo físico**, selecciona Mazars, Fractura — CZM o Comparación científica.
3. Introduce una carga dentro del rango calculado y elige la rama ascendente o descendente. El programa selecciona un estado almacenado, sin fabricar estados intermedios. El pico CZM difiere del pico Mazars: una carga disponible en un modelo puede no existir en el otro.
4. Usa **Ver pico**, la barra de estados o **Iniciar ensayo**. La velocidad indica estados por segundo en pantalla, no tiempo físico del ensayo.
5. En CZM, usa **Fractura cohesiva** y **Acercar a la interfaz calculada**. Los puntos coloreados corresponden al daño en puntos de integración de COMSOL. Las dos caras se desplazan según sus campos FEM independientes.
6. Una apertura real submilimétrica puede resultar difícil de distinguir a escala ×1. Los botones ×10, ×25 y ×50 amplifican los desplazamientos y muestran el factor. Restablece la cámara con el botón de casa.
7. Selecciona esfuerzos, deformaciones o las gráficas de apertura y energía. En Mazars esas últimas magnitudes se indican como no disponibles; daño continuo no equivale a apertura.
8. En Comparación científica, la escena identifica que está mostrando Mazars y la gráfica añade la curva CZM. Cambia a Fractura para inspeccionar sus campos. La línea de 14,5 kN es únicamente el pico documental; no se dispone de flecha experimental sincronizada.
9. Consulta **Tabla y procedencia** para ver el identificador, modelo y solución nativa. Las exportaciones CSV/Excel incluyen apertura y energía cuando existen. PNG/SVG exportan la gráfica y PDF exporta el estado actual con su alcance.

La etiqueta **Visualización 3D de resultados FEM 2D.** es permanente. La máquina tiene geometría ilustrativa; el análisis mecánico sigue siendo bidimensional con extrusión uniforme al ancho de la vigueta.

El CZM prescribe una trayectoria central y el sólido inicial es elástico sin aplastamiento volumétrico. Esto permite estudiar una interfaz que se abre y pierde tracción, pero no representa una predicción experimental validada de todas las formas de fallo del concreto. Lee el informe científico antes de utilizar valores para una conclusión académica.
