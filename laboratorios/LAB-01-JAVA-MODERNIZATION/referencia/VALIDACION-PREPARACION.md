# Validación del material inicial · AssetDesk

Comprobaciones realizadas durante esta revisión del laboratorio:

| Elemento | Verificación | Resultado |
| --- | --- | --- |
| Java 8 / Maven | `mvn clean verify` en Docker, imagen maven:3.9-eclipse-temurin-8 | Compilación, tres pruebas y empaquetado correctos |
| Demo Java 8 | JAR ejecutado y JSON comprobado con comprobar-demo.py | Catálogo, asignación, devolución y contadores correctos |
| Ejecución Java 21 | El mismo JAR Java 8 ejecutado en JDK 21 | Demo correcta |

Ejecutar bytecode Java 8 en JDK 21 no equivale a haber realizado Java Upgrade con Bob. Esa actualización, sus cambios y sus pruebas se ejecutan durante la sesión del participante.

El informe del participante registra las evidencias reales del wizard. No se ha simulado una sesión de Bob ni se atribuyen a su workflow estos resultados de preparación.

Comprobaciones adicionales del material: enlaces locales y bloques Markdown, XML, sintaxis de scripts, preparación sin sobrescritura y los cuatro diagramas Mermaid de este laboratorio validados correctamente.
