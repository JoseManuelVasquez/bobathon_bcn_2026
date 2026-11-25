# Validación del material inicial · AssetDesk

Comprobaciones realizadas durante esta revisión del laboratorio:

| Elemento | Verificación | Resultado |
| --- | --- | --- |
| Java 8 / Maven | `mvn clean verify` en Docker, imagen maven:3.9-eclipse-temurin-8 | Compilación, cinco pruebas y empaquetado correctos |
| Demo Java 8 | JAR ejecutado y JSON comprobado con comprobar-demo.py | Catálogo, asignación, devolución y contadores correctos |
| Ejecución Java 21 | El mismo JAR Java 8 ejecutado en JDK 21 | Demo correcta |
| Ejercicio de remediación | Consulta de OSV para Commons Lang 3.17.0 y 3.18.0 | El aviso se identifica en 3.17.0 y desaparece en 3.18.0. El JAR de AssetDesk no incluye Commons Lang. |

Ejecutar bytecode Java 8 en JDK 21 no equivale a haber realizado Java Upgrade con Bob. Esa actualización, sus cambios y sus pruebas se ejecutan durante la sesión del participante.

El informe del participante registra las evidencias reales del wizard. No se ha simulado una sesión de Bob ni se atribuyen a su workflow estos resultados de preparación.

Comprobaciones adicionales del material: enlaces locales y bloques Markdown, XML, sintaxis de scripts, preparación sin sobrescritura y los cuatro diagramas Mermaid de este laboratorio validados correctamente.
