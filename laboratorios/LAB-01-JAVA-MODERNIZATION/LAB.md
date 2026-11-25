# LAB 01 · AssetDesk: recorrido por el wizard Java

## Objetivo

Actualizar **Java 8 → Java 21** con IBM Bob Premium Package for Java, corregir una dependencia con un aviso de seguridad y demostrar que asignar y devolver recursos sigue funcionando.

AssetDesk contiene **cuatro recursos: tres disponibles y uno asignado**. La demo asigna el recurso 1 y lo devuelve. Cada ejecución parte del mismo estado en memoria.

## 1. Preparar y abrir

Abre en IBM Bob la carpeta descomprimida del laboratorio, la que contiene `legacy/`. Copia este prompt y pégalo en el chat de Bob.

```prompt
Prepara y ejecuta la demo de AssetDesk en esta carpeta. Identifica mi sistema operativo y mi terminal. Usa los comandos adecuados para Windows, macOS o Linux.

Si work/ no existe, prepara una copia de legacy/ siguiendo scripts/preparar.sh y crea el informe desde la plantilla. Si work/ ya existe, verifica que contiene el pom.xml de AssetDesk y conserva mi trabajo.

Comprueba que Maven utiliza un JDK 8. Si falta Java o Maven, dime qué falta y espera. En work/, ejecuta mvn clean verify y después java -jar target/assetdesk.jar demo. Muéstrame las pruebas y los contadores de la demo. Conserva el código y las versiones de partida.
```

Cuando termine la demo, abre `work/` en Bob con **File → Open Folder** para que el asistente trabaje sobre el `pom.xml` de AssetDesk.

Comprueba que tienes JDK 8 y 21, Maven y el paquete Premium de Bob disponibles. Si eliges Git Flow, prepara un repositorio con commit inicial.

## 2. Observar la referencia
Estos son los comandos de referencia que ejecuta Bob desde `work/` con JDK 8.

```bash
mvn clean verify
java -jar target/assetdesk.jar demo
```

Guarda el resultado de las cinco pruebas iniciales y comprueba el JSON:

| Momento | Disponibles | Asignados |
| --- | --- | --- |
| `initialSummary` | 3 | 1 |
| `afterAssignment` | 2 | 2 |
| `afterRelease` | 3 | 1 |

**Comprobación:** el proyecto compila y el recorrido funciona antes del cambio.

## 3. Lanzar el análisis incluido en Bob
1. Abre **IBM Bob Premium Package for Java**, la página de tarjetas que aparece en la captura.
2. Localiza **Analyze and suggest modernization** y pulsa **Ask**.
3. Si Bob pregunta por el proyecto, selecciona la raíz **`work/`**.
4. Sigue sus preguntas y espera el resultado.
5. Revisa las referencias a archivos y las recomendaciones.

Compara con [ANALISIS-INICIAL.md](referencia/ANALISIS-INICIAL.md) y anota las recomendaciones y lo que haya quedado sin comprobar.

**Comprobación:** el análisis corresponde al código abierto. AssetDesk no tiene UI, base de datos ni servidor de aplicaciones.

### Remediar una dependencia con Bob

1. En el chat de Bob, escribe **Java Vulnerability Remediation** para abrir el flujo del paquete Premium sobre `work/`.
2. Guarda el hallazgo de **Apache Commons Lang**, que se usa en una prueba del CLI. La versión inicial `3.17.0` está afectada por [CVE-2025-48924](https://osv.dev/vulnerability/GHSA-j288-q9x7-2f5v).
3. Pide a Bob que remediе este hallazgo. Revisa en el diff que actualiza la dependencia a `3.18.0` o posterior compatible con Java 8, y que mantiene `scope` en `test`.
4. Ejecuta `mvn clean verify` y vuelve a lanzar el escaneo. Conserva la versión anterior y la nueva, el resultado de las pruebas y la evidencia de que el aviso concreto ya no aparece.

El ejercicio consiste en corregir la versión declarada en Maven y comprobar el resultado con las pruebas del proyecto. [Flujo de remediación de IBM](https://github.com/IBM/ibm-bob-java#java-vulnerability-remediation).

## 4. Elegir el flujo y el destino
Pulsa **Start** en la tarjeta **Java Upgrade**, o inicia **Java Modernization** desde el selector de workflows. [Acceso oficial de IBM](https://bob.ibm.com/es/docs/ide/premium-packages/java-modernization/getting-started).

En **Flow Selection / Modernization Type**, como en la captura:

| Control | Selección |
| --- | --- |
| Proyecto, si se pregunta | AssetDesk, raíz `work/` |
| `Modernization Type` | **Java Upgrade** |
| `Enable Git Flow` | Activado si el repositorio está preparado |
| `Name of the branch to create` | `workshop/assetdesk-java21` |
| `Continue` | Avanzar |

Cuando el asistente solicite el destino, elige **Java 21**. No hay APIs Java EE que migrar en este proyecto.

**Comprobación:** UI Modernization y Liberty pueden aparecer deshabilitados; es coherente con esta aplicación de consola. No necesitas esas opciones para este lab.

## 5. Revisar y ejecutar
1. Revisa el entorno, el JDK detectado y el build que muestre Bob.
2. Confirma que el plan trabaja sobre AssetDesk y el destino es Java 21.
3. Continúa cuando el asistente presente el plan y sus cambios.
4. Sigue las subtareas de transformación, compilación y corrección de errores.
5. Si una fase falla, revisa la causa y las opciones que ofrezca Bob.
6. Abre **Source Control** para comparar Maven y las clases modificadas.

Las pantallas siguientes a Flow Selection dependen de la versión y los hallazgos. Sigue los controles reales del asistente; no se presupone que emita un archivo con un nombre determinado.

**Comprobación:** el workflow termina su compilación o identifica un bloqueo concreto. Editar la versión de Java por sí solo no demuestra el resultado.

## 6. Generar pruebas con el asistente
1. Pulsa **Start** en **Unit Test Generation**, o selecciona **Java Unit Testing** en el wizard.
2. Selecciona AssetDesk y, cuando permita elegir alcance, **`ResourceService`**.
3. Revisa la estrategia de pruebas que ofrezca Bob.
4. Continúa con la generación y ejecución.
5. Revisa resultados y cobertura, si el workflow la produce.

Busca casos de asignación, devolución, recurso ocupado, equipo vacío e ID desconocido. Distingue las cinco pruebas iniciales de las nuevas. Anota como pendiente cualquier caso que no se haya ejecutado.

## 7. Validar y cerrar
Con JDK 21 seleccionado:

```bash
java -version
mvn -version
mvn clean verify
java -jar target/assetdesk.jar demo
```

Repite la tabla del paso 2. Opcionalmente:

```bash
java -jar target/assetdesk.jar demo | python3 ../scripts/comprobar-demo.py
```

Abre [ARQUITECTURA.md](referencia/ARQUITECTURA.md) en la vista previa Markdown y contrasta sus diagramas con el resultado. Si Bob ofrece un Mermaid de progreso, consérvalo: representa las tareas del workflow, no necesariamente la arquitectura.

Completa **`work/docs/INFORME-FINAL.md`** con el análisis, decisiones, cambios, pruebas y pendientes. Es una hoja de revisión del participante. Muestra al grupo un diff y la demo final.

## Criterios de finalización

- [ ] Análisis integrado revisado.
- [ ] Dependencia de pruebas actualizada y aviso comprobado con un segundo escaneo.
- [ ] Java Upgrade ejecutado con destino 21.
- [ ] Pruebas revisadas y ejecutadas con el JDK destino.
- [ ] Demo de asignación y devolución correcta.
- [ ] Resumen detallado y Mermaid contrastados con el código.

**Si el wizard no reconoce el proyecto:** revisa la raíz `work/`, el build inicial, JDK/Maven y la instalación/licencia del paquete. Los [requisitos oficiales](https://bob.ibm.com/docs/ide/premium-packages/java-modernization/prerequisites) ayudan a preparar el entorno.
