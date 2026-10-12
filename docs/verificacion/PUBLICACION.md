# Verificación de la publicación GitHub — 12 de octubre de 2026

- Compilación TypeScript/Vite: correcta.
- Pruebas portables: 17 registradas; 15 aprobadas y dos hashes MPH omitidos explícitamente sin fuentes nativas.
- Pruebas científicas con los MPH originales: 15/15 aprobadas, sin omisiones.
- Prueba de interfaz de la copia pública: CZM carga, apertura, energía, gráficas, tabla y CSV; aprobada en Edge.
- Datos del visor: 827 archivos copiados con SHA-256 idéntico; Git conserva sus bytes sin normalizar saltos de línea.
- Extracción JSON CZM independiente: SHA-256 idéntico al archivo científico original.
- Código Python: sintaxis válida; las cinco funciones auxiliares extraídas conservan el mismo AST que las originales.
- Modelo Java: solo se retiró la ruta personal de `modelPath`; no se modificó la física.
- PDF: informe original de ocho páginas, sin ruta personal del equipo.
- ZIP público: CRC correcto; sus 73 archivos del runtime permanecen byte por byte iguales al paquete previamente probado. Se retiraron rutas personales del log de pruebas incluido; esta copia tiene un SHA-256 de ZIP distinto, documentado en la descarga.

No se repitieron las simulaciones FEM completas por reorganizar carpetas. Los resultados corresponden a la entrega original, cuyas cinco pruebas UI y prueba del ejecutable se documentan en el informe. La ejecución automática de CI en GitHub comprobará de forma independiente la instalación, los datos portables y la compilación.
