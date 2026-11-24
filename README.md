# Bobathon BCN 2026

Workshop interactivo de modernización con IBM Bob Premium Package for Java.

**Web:** https://JoseManuelVasquez.github.io/bobathon_bcn_2026/

Dos recorridos para participantes: **AssetDesk, Java 8 → Java 21**, y **RoomFlow, JSF/Struts → React y API Java**. Incluye etapas guiadas, progreso y notas en el navegador, búsqueda, diagramas ampliables, comparador visual y descargas de los laboratorios.

La vista general contiene únicamente los dos retos. La presentación sigue el estilo de la documentación de Bob y permite elegir **Light, Dark o System**; la elección se conserva en el navegador. La comparación visual está en la etapa correspondiente del reto de UI.

## Preparar y ejecutar la web

Necesitas Node compatible con Vite y Python 3. La versión inicial se compiló con Node 24.

```bash
npm ci
npm run content
npm run dev
```

## Mantener el contenido

Los Markdown de `laboratorios/` son la fuente del contenido del workshop. Edita las guías y regenera la web:

```bash
npm run build
```

`prepare_content.py` organiza las etapas, prepara las imágenes y crea los ZIP de los laboratorios. Los ZIP excluyen copias de trabajo, builds y configuración local. Para importar una nueva copia de los dos laboratorios desde otro directorio:

```bash
python3 scripts/prepare_content.py --source-root /ruta/al/material
npm run build
```

Los nombres de archivo y marcadores de las guías identifican las etapas y la plantilla del informe; consérvalos al editar el contenido.

## Publicar en GitHub Pages

El resultado de producción está en **`docs/`**. Pages publica la rama **`main`**, carpeta **`/docs`**, con `.nojekyll`. Tras cambiar el código o las guías, compila y sube tanto las fuentes como `docs/`.

La web aloja la guía y las interacciones del navegador. Los proyectos Java y sus APIs se ejecutan en el equipo del participante, siguiendo cada laboratorio. Progreso y notas se guardan en el navegador; se pueden exportar a Markdown.

Las aplicaciones y datos del workshop son ficticios. Las evidencias de la sesión de referencia se distinguen de los resultados que cada participante debe comprobar. Las fuentes IBM Plex Sans e IBM Plex Mono se distribuyen con sus licencias en `docs/licenses/`. El icono de Bob procede de la [documentación oficial](https://bob.ibm.com/icon.svg?v=1).
