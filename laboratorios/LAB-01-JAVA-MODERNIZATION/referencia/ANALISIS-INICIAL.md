# AssetDesk · Resumen detallado del proyecto inicial

## Funcionalidad

AssetDesk administra recursos compartidos entre equipos de una organización. El catálogo contiene un portátil de formación, un proyector, un kit de pruebas y un equipo de videoconferencia. No hay información de empresas reales.

La aplicación acepta dos comandos: `list` muestra el catálogo y `demo` ejecuta una asignación y devolución. Cada ejecución crea un servicio nuevo y recupera el mismo catálogo; no existe persistencia entre procesos.

## Estructura y responsabilidades

| Elemento | Responsabilidad |
| --- | --- |
| `AssetDeskApplication` | Comandos, recorrido de demostración y salida JSON mediante Gson |
| `SharedResource` | ID, nombre, categoría, fecha de registro, estado y equipo asignado |
| `ResourceService` | Catálogo en memoria, consulta, asignación, devolución y contadores |
| `ResourceServiceTest` | Tres pruebas JUnit 4 de referencia |
| `pom.xml` | Java 8, dependencias, compilación, pruebas y JAR ejecutable |

Los métodos de consulta devuelven copias. Las operaciones del servicio están sincronizadas sobre la misma instancia; esa protección no se extiende a otros procesos.

## Reglas

- Solo se asigna un recurso AVAILABLE.
- El equipo es obligatorio y admite hasta 120 caracteres tras recortar espacios.
- Solo se devuelve un recurso ASSIGNED.
- Un ID desconocido produce un error.
- Al devolverlo, el recurso queda AVAILABLE y se elimina el equipo asignado.

## Inventario inicial

El proyecto usa Java 8, Maven, Gson 2.8.9 y los plugins Compiler 3.8.1, Surefire 2.22.2 y Shade 3.2.4. Las pruebas usan JUnit 4.13.2 y Commons Lang 3.17.0. El modelo utiliza `java.util.Date` y cadenas para los estados.

No hay Spring, Java EE, interfaces web ni datasource. El alcance principal es el JDK, la cadena de build, sus dependencias y la conservación del comportamiento.

## Evidencias de comportamiento

Inicialmente: cuatro recursos, tres disponibles, uno asignado. Asignar el recurso 1 deja dos disponibles y dos asignados. Devolverlo restaura tres disponibles y uno asignado.

Las cinco pruebas iniciales cubren los contadores, la asignación y devolución, el rechazo de un recurso ocupado, el inventario JSON y el mensaje de uso del CLI. En Java Unit Testing puedes ampliar la cobertura con equipo vacío, ID desconocido y devolución inválida.

## Revisión de modernización

El asistente debe detectar el nivel Java inicial y proponer la ruta al destino elegido. Los cambios reales de bibliotecas y plugins se revisan en el diff. Una actualización de JDK no significa automáticamente que se hayan rediseñado modelos o solucionado todas las vulnerabilidades.

Los resultados de escaneo, cobertura, tiempos y compilación se registran con su evidencia. Esta referencia describe el código; no sustituye la ejecución del workflow.
