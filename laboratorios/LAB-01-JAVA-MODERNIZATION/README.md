# LAB 01 · AssetDesk: Java 8 → Java 21 con el wizard de Bob

**Caso ficticio y agnóstico:** una organización presta recursos compartidos a sus equipos: portátiles, proyectores, kits de pruebas y equipos de videoconferencia. AssetDesk consulta el catálogo, asigna un recurso y lo devuelve.

Primero ejecuta la demo original de AssetDesk. Después pulsa **Start** en **Java Upgrade** dentro de IBM Bob Premium Package for Java. El punto de partida es Java 8, Maven, salida JSON y cinco pruebas JUnit 4. No necesita base de datos ni servidor.

## Empieza aquí

1. Abre esta carpeta en IBM Bob y copia el [prompt de arranque](LAB.md#1-arrancar-assetdesk-legacy) al chat. Bob prepara `work/` y ejecuta la demo.
2. Abre **`work/`**, la carpeta con el `pom.xml`, en IBM Bob.
3. Sigue [LAB.md](LAB.md) para analizar el proyecto, abrir el wizard de Java Upgrade y verificar la demo después del cambio.

## Material incluido

| Archivo o carpeta | Uso |
| --- | --- |
| [LAB.md](LAB.md) | Qué pulsar, elegir y comprobar en cada fase |
| [referencia/ANALISIS-INICIAL.md](referencia/ANALISIS-INICIAL.md) | Resumen detallado del proyecto de partida |
| [referencia/ARQUITECTURA.md](referencia/ARQUITECTURA.md) | Diagramas Mermaid de estructura y asignación |
| [plantillas/INFORME-FINAL.md](plantillas/INFORME-FINAL.md) | Hoja de resultados del participante |
| [referencia/VALIDACION-PREPARACION.md](referencia/VALIDACION-PREPARACION.md) | Comprobaciones del material inicial |
| `legacy/` | Código inicial de AssetDesk |
| `scripts/preparar.sh` | Crea la copia de trabajo sin sobrescribir una existente |
| `scripts/comprobar-demo.py` | Comprobación opcional del JSON de la demo |


Continúa con [RoomFlow, LAB 02](../LAB-02-UI-MODERNIZATION/README.md) para modernización de UI. Ambos escenarios se pueden presentar a cualquier empresa.
