#!/usr/bin/env python3
"""Build the workshop content and downloads from the student Markdown sources."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
LABS = [('java', 'LAB-01-JAVA-MODERNIZATION'), ('ui', 'LAB-02-UI-MODERNIZATION')]
EXCLUDE = {'work', 'target', 'node_modules', '.git', '.idea', '.bob', '.vscode', '__pycache__', 'INSTRUCTOR.md', '.DS_Store'}

def participant_text(text):
    text = re.sub(r'(?m)^(#{1,6} .+?)\s*·\s*\d+(?:[–-]\d+)?\s*(?:min|minutos)\.?\s*$', r'\1', text)
    text = re.sub(r'(?m)^\*\*Duración orientativa:.*\n?', '', text)
    text = re.sub(r'(?m)^\| \[INSTRUCTOR\.md\].*\n?', '', text)
    text = text.replace('El instructor prepara JDK 8 y 21, Maven y la licencia del paquete. Para usar Git Flow debe haber un repositorio con commit inicial; la preparación está en [INSTRUCTOR.md](INSTRUCTOR.md).', 'Comprueba que tienes JDK 8 y 21, Maven y el paquete Premium de Bob disponibles. Si eliges Git Flow, prepara un repositorio con commit inicial.')
    return text

def import_labs(source_root):
    for _, name in LABS:
        src = source_root / name
        dest = ROOT / 'laboratorios' / name
        if not (src / 'LAB.md').is_file():
            raise SystemExit(f'Falta la guía del laboratorio: {name}')
        dest.mkdir(parents=True, exist_ok=True)
        for p in src.rglob('*'):
            rel = p.relative_to(src)
            if any(part in EXCLUDE for part in rel.parts) or not p.is_file():
                continue
            if any(word in p.name.lower() for word in ('token', 'credential', 'secret')):
                raise SystemExit('No se permite importar credenciales en el contenido.')
            if rel.parts[0] not in {'LAB.md', 'README.md', '.gitignore', 'legacy', 'legacy-jsf', 'legacy-struts', 'scripts', 'plantillas', 'referencia'}:
                continue
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix == '.md':
                out.write_text(participant_text(p.read_text()), encoding='utf-8')
            else:
                shutil.copy2(p, out)

JAVA_META = [
 ('contexto', 'El punto de partida', 'Entiende AssetDesk y el cambio que vas a validar.', ['Identifica la aplicación de consola y sus reglas.', 'Distingue una actualización de Java de un rediseño.']),
 ('preparar', 'Prepara tu proyecto', 'Abre una copia de trabajo en Bob.', ['Localiza pom.xml y las fuentes.', 'Comprueba el entorno Java y Maven.']),
 ('referencia', 'Conoce el comportamiento', 'Ejecuta la demo antes de cambiar Java.', ['Guarda las cinco pruebas iniciales.', 'Comprueba los contadores del JSON.']),
 ('analizar', 'Analiza con Bob', 'Contrasta el análisis con el código real.', ['Revisa dependencias y responsabilidades.', 'Anota recomendaciones y límites.']),
 ('destino', 'Elige Java 21', 'Configura el destino en el wizard.', ['Selecciona Java Upgrade.', 'Registra Java 21 como objetivo.']),
 ('modernizar', 'Ejecuta la modernización', 'Revisa los cambios y el ciclo de compilación.', ['Confirma que el plan trabaja sobre AssetDesk.', 'Revisa el diff y las correcciones.']),
 ('pruebas', 'Amplía las pruebas', 'Usa Java Unit Testing con ResourceService.', ['Distingue pruebas nuevas y de referencia.', 'Revisa casos de error y cobertura real.']),
 ('validar', 'Valida y concluye', 'Demuestra el mismo comportamiento con Java 21.', ['Ejecuta verify y la demo con el JDK destino.', 'Guarda tu informe, evidencias y pendientes.']),
]
UI_META = [
 ('contexto', 'Entiende RoomFlow', 'Conoce las reservas y las reglas que vas a conservar.', ['Identifica las variantes JSF y Struts.', 'Comprende aforo, estados y conflictos.']),
 ('preparacion', 'Prepara el entorno', 'Comprueba herramientas y puertos.', ['Revisa el Java utilizado por Maven.', 'Elige una sola variante de entrada.']),
 ('preparar', 'Abre tu copia en Bob', 'Prepara un espacio de trabajo seguro.', ['Comprueba que work/ contiene el proyecto correcto.', 'Localiza tu informe de entrega.']),
 ('antes', 'Explora la UI original', 'Recorre las reservas antes de modernizar.', ['Guarda una captura con el estado inicial.', 'Prueba confirmar y cancelar.']),
 ('analizar', 'Analiza la aplicación', 'Revisa las responsabilidades del código.', ['Contrasta el análisis con las reglas.', 'Identifica qué asumirá React.']),
 ('wizard', 'Elige el flujo UI', 'Configura el destino y revisa las aprobaciones.', ['Selecciona UI Modernization y React.', 'Anota backend, diseño y alcance elegidos.']),
 ('backend', 'Genera la API Java', 'Conserva las reglas y revisa sus pruebas.', ['Abre Swagger y consulta los endpoints.', 'Comprueba el arranque antes de confirmar el checkpoint.']),
 ('frontend', 'Construye la nueva UI', 'Sigue Setup, componentes e integración.', ['Continúa hasta tener pantallas funcionales.', 'Comprueba tema y peticiones reales a la API.']),
 ('comparacion', 'Compara el antes y después', 'Revisa diseño, navegación y funciones.', ['Compara pantallas con el mismo estado de datos.', 'Revisa móvil, formularios y estados.']),
 ('validacion', 'Pon a prueba las reglas', 'Comprueba acciones, errores y recuperación.', ['Demuestra aforo y conflicto de sala.', 'Valida recarga, API apagada y recuperación.']),
 ('conclusiones', 'Contrasta el resultado', 'Aprende de las evidencias de la sesión de referencia.', ['Distingue lo ejecutado de lo no comprobado.', 'Explica cambios, conservación y límites.']),
 ('entrega', 'Prepara tu entrega', 'Documenta tus decisiones y conclusiones.', ['Adjunta capturas, Mermaid y resultados.', 'Demuestra una confirmación y un rechazo real.']),
 ('referencia-tecnica', 'Consulta técnica', 'Arquitectura, endpoints y resolución de problemas.', ['Consulta los diagramas cuando los necesites.', 'Usa las rutas que haya generado tu ejecución.']),
]

def ui_sections(text):
    def pos(s):
        n = text.find(s)
        if n < 0: raise SystemExit(f'No se encuentra una sección del lab UI: {s}')
        return n
    points = [pos('<a id="contexto">'), pos('<a id="preparacion">')]
    points += [re.search(rf'(?m)^### {i}\. ', text).start() for i in range(1, 7)]
    points += [pos(f'<a id="{s}">') for s in ('comparacion','validacion','conclusiones','entrega','referencia-tecnica')]
    result=[]
    for i, meta in enumerate(UI_META):
        md=text[points[i]:points[i+1] if i+1<len(points) else len(text)].strip()
        md=re.sub(r'<a id="pasos"></a>\s*\n\s*## Pasos del laboratorio\s*', '', md)
        md=re.sub(r'<!-- ROOMFLOW_INFORME_(?:INICIO|FIN) -->', '', md)
        result.append(dict(id=meta[0],title=meta[1],subtitle=meta[2],checks=meta[3],markdown=md,source='LAB.md'))
    return result

def java_sections(text):
    points=[re.search(r'(?m)^## Objetivo',text).start()]
    points += [re.search(rf'(?m)^## {i}\. ',text).start() for i in range(1,8)]
    return [dict(id=m[0],title=m[1],subtitle=m[2],checks=m[3],markdown=text[points[i]:points[i+1] if i+1<len(points) else len(text)].strip(),source='LAB.md') for i,m in enumerate(JAVA_META)]

# The full student guides remain the source of optional commands and reference
# material. The website follows five decisions/checkpoints, rather than every
# individual wizard task. sourceIds also keep old bookmarks and notes usable.
GUIDED_JAVA = [
 dict(id='explorar', title='Explora el antes', subtitle='Conoce AssetDesk antes de actualizar Java.',
      action='Abre la carpeta del laboratorio en Bob y pega el prompt de abajo en su chat. Bob preparará AssetDesk y ejecutará la demo con Java 8.',
      bob='Detecta tu entorno, prepara la copia y ejecuta la compilación, las pruebas y la demo.',
      participant='Explora la aplicación y guarda su comportamiento de partida.',
      expected='La demo parte de 3 recursos disponibles y 1 asignado, pasa a 2 y 2, y termina de nuevo en 3 y 1. Las cinco pruebas iniciales pasan.',
      path=['File → Open Folder', 'Carpeta del laboratorio', 'Chat de Bob · prompt'],
      sourceIds=['contexto','preparar','referencia'],
      intro='AssetDesk gestiona el préstamo de recursos compartidos. Vas a actualizar Java y a remediar una dependencia del laboratorio.',
      introIds=['preparar'],
      details=[('Resultados y comandos de referencia', ['referencia'])]),
 dict(id='analizar', title='Analiza con Bob', subtitle='Revisa el análisis y remedia una dependencia antes de actualizar Java.',
      action='Pulsa Ask en Analyze and suggest modernization. Después, escribe Java Vulnerability Remediation en el chat de Bob para escanear y corregir la dependencia de la práctica.',
      bob='Identifica oportunidades de modernización y propone una actualización para el hallazgo de seguridad.',
      participant='Guarda el hallazgo, revisa el cambio propuesto y repite las pruebas y el escaneo.',
      expected='Puedes explicar una recomendación de Bob. Has comprobado el cambio de versión, las pruebas pasan y el aviso de la práctica desaparece del segundo escaneo.',
      path=['IBM Bob Premium Package for Java', 'Analyze and suggest modernization', 'Java Vulnerability Remediation'],
      sourceIds=['analizar'],
      intro='Abre en el editor uno de los archivos citados por Bob. Si una explicación no está clara, utiliza el chat con ese archivo como contexto para entenderla.',
      details=[('Revisar el análisis y remediar la dependencia', ['analizar'])]),
 dict(id='modernizar', title='IBM Bob Premium Package for Java', subtitle='Deja que Bob ejecute la actualización que has elegido.',
      action='Inicia Java Modernization desde Start Workflow, selecciona Java Upgrade y el destino Java 21. Revisa el plan y sigue las preguntas del wizard.',
      bob='Modifica Maven y el código, compila y propone correcciones durante el workflow.',
      participant='Elige el destino, revisa el plan y lee las operaciones que vas a aprobar.',
      expected='El workflow ha aplicado la actualización y su compilación termina correctamente, o has identificado y documentado un bloqueo concreto.',
      path=['Start Workflow', 'Java Modernization', 'Java Upgrade → Java 21'],
      sourceIds=['destino','modernizar'],
      intro='Mantén el foco en Bob y vuelve a esta guía al alcanzar el checkpoint. Revisa las ediciones del pom.xml en Source Control después de que Bob las aplique.',
      details=[('Opciones del wizard y revisión de los cambios', ['destino','modernizar'])]),
 dict(id='comprobar', title='Comprueba el después', subtitle='Verifica el resultado con el Java de destino.',
      action='Utiliza Java Unit Testing para ampliar las pruebas de ResourceService y vuelve a ejecutar con Java 21 el recorrido de asignación y devolución.',
      bob='Genera y ejecuta pruebas, y te ayuda a diagnosticar los fallos que aparezcan.',
      participant='Revisa las salidas y compara los contadores con los que guardaste al principio.',
      expected='Maven utiliza JDK 21, las pruebas ejecutadas pasan y la demo conserva los contadores 3/1 → 2/2 → 3/1. Distingues los casos ejecutados de los pendientes.',
      path=['Java Unit Testing', 'ResourceService', 'Terminal · pruebas y demo'],
      sourceIds=['pruebas','validar'],
      intro='Comprueba al menos un caso de error, como intentar asignar un recurso ocupado. Contrasta la prueba generada y su resultado; una tarea marcada como terminada necesita una evidencia de ejecución.',
      details=[('Generar pruebas con el asistente', ['pruebas']), ('Comandos y comprobación de la demo final', ['validar'])]),
 dict(id='concluir', title='Explica el resultado', subtitle='Cierra el reto con evidencias que puedas mostrar.',
      action='Revisa con Bob un cambio significativo, contrasta el Mermaid con el código final y guarda tres conclusiones de tu modernización.',
      bob='Puede ayudarte a resumir los cambios y explicar el diagrama.',
      participant='Revisa el resumen y presenta qué cambió, qué se conservó y qué queda pendiente.',
      expected='Puedes mostrar el cambio de Java, la remediación, las pruebas, la demo y un Mermaid revisado. Tus conclusiones distinguen resultados comprobados y pendientes.',
      path=['Source Control · diff', 'Mermaid · revisión', 'Exportar mi recorrido'],
      sourceIds=['validar'],
      intro='Guarda tres conclusiones breves en Tus notas y exporta tu recorrido. Puedes pedir a Bob que te ayude a completar el informe; revisa sus afirmaciones con las salidas de tu ejecución.',
      markdown='''<details>
<summary>Resumen detallado, Mermaid e informe ampliado</summary>

Consulta [el análisis de referencia](referencia/ANALISIS-INICIAL.md) y [los diagramas Mermaid de arquitectura](referencia/ARQUITECTURA.md). Contrasta versiones, dependencias y responsabilidades con tu resultado. El diagrama de tareas del workflow y el de arquitectura explican aspectos distintos.

Para conservar un informe ampliado, utiliza `work/docs/INFORME-FINAL.md`. Incluye el análisis, decisiones, cambios, pruebas, Mermaid y pendientes. Anota la versión de Bob y el JDK realmente utilizado.

</details>''', details=[]),
]

GUIDED_UI = [
 dict(id='explorar', title='Explora el antes', subtitle='Prueba RoomFlow y guarda tu referencia visual.',
      action='Abre la carpeta del laboratorio en Bob y pega el prompt de abajo en su chat. Elige JSF o Struts y guarda una captura del listado cuando Bob te dé la URL.',
      bob='Detecta tu entorno, prepara la variante y comprueba que la aplicación arranca.',
      participant='Explora búsqueda, detalle y estados de una reserva en la aplicación original.',
      expected='Has elegido JSF o Struts, conoces el recorrido de Ana y tienes una captura de las cuatro reservas iniciales.',
      path=['File → Open Folder', 'Chat de Bob · prompt JSF o Struts', 'Navegador · listado'],
      sourceIds=['contexto','preparacion','preparar','antes'],
      intro='RoomFlow reserva salas y conserva aforos, estados y conflictos en Java. Vas a utilizar UI Modernization para generar una interfaz React conectada a una API Java.',
      screenshot='referencia/sesion-bob/antes-listado.png', caption='Referencia del antes: listado Struts. Explora tu variante con sus datos iniciales.',
      introIds=['preparar'],
      details=[('Validar el entorno y recorrer la aplicación', ['preparacion','antes']), ('Contexto, datos iniciales y reglas de negocio', ['contexto'])]),
 dict(id='analizar', title='Analiza con Bob', subtitle='Identifica qué conservará Java y qué asumirá React.',
      action='Pulsa Ask en Analyze and suggest modernization y revisa cómo Bob interpreta las pantallas y las reglas de RoomFlow.',
      bob='Analiza el framework, las dependencias y las responsabilidades del código.',
      participant='Abre una referencia del análisis y comprueba dónde se aplica una regla de reservas.',
      expected='Puedes localizar una pantalla y una regla de negocio en el código, y explicar su responsabilidad en el resultado esperado.',
      path=['IBM Bob Premium Package for Java', 'Analyze and suggest modernization', 'Ask'],
      sourceIds=['analizar'],
      intro='Elige una regla concreta, como el aforo o el conflicto de sala. Si necesitas entenderla, consulta a Bob con el servicio o la pantalla correspondiente como contexto.',
      details=[('Revisar el análisis de la aplicación', ['analizar'])]),
 dict(id='modernizar', title='IBM Bob Premium Package for Java', subtitle='Acompaña la generación de la API y del frontend.',
      action='En IBM Bob Premium Package for Java, inicia Java Modernization, elige UI Modernization y React, y completa backend, frontend e integración.',
      bob='Genera la API, los componentes React y su integración; compila y corrige los errores del workflow.',
      participant='Revisa el alcance y las decisiones, aprueba las operaciones y comprueba los checkpoints de arranque.',
      expected='La API y el frontend arrancan con los comandos de tu ejecución, y la UI consulta datos reales de tu API.',
      path=['Start Workflow', 'Java Modernization → UI Modernization', 'React → backend y frontend'],
      sourceIds=['wizard','backend','frontend'],
      intro='Continúa en Bob entre sus subtareas. Cuando el wizard te pida confirmar que un servicio arrancó, abre su URL y compruébalo antes de responder. Usa las carpetas, puertos y comandos que genere tu ejecución.',
      screenshot='referencia/sesion-bob/07-componentes-home-page.png', caption='Captura del ensayo: Bob avanza por las tareas del frontend. Los nombres y el orden pueden variar según la versión.',
      details=[('Elegir opciones y revisar aprobaciones', ['wizard']), ('Ayuda para arrancar la API cuando el wizard lo solicite', ['backend']), ('Ayuda para arrancar React y continuar la integración', ['frontend'])]),
 dict(id='comprobar', title='Comprueba el después', subtitle='Repite el recorrido y demuestra una regla de negocio.',
      action='En la UI React, recorre una reserva de principio a fin y provoca un rechazo por aforo o conflicto. Compara el antes y el después con los mismos datos.',
      bob='Ejecuta sus validaciones y puede ayudarte a diagnosticar el caso que falle.',
      participant='Prueba la aplicación, revisa las peticiones a la API y guarda evidencias del resultado.',
      expected='Puedes buscar, abrir, crear, confirmar y cancelar una reserva con recarga, y demostrar un rechazo real. Has comparado capturas con el mismo estado de datos.',
      path=['React · listado y formulario', 'API · respuesta real', 'Antes y después'],
      sourceIds=['comparacion','validacion'], comparison=True,
      intro='Empieza con las cuatro reservas iniciales. Registra cada caso como ejecutado correctamente, fallido o no ejecutado. Utiliza Listado en el comparador para ver las mismas cuatro reservas; las vistas de Inicio son referencias de pantallas distintas.',
      details=[('Casos de prueba y resultados esperados', ['validacion']), ('Más capturas y criterios de comparación', ['comparacion'])]),
 dict(id='concluir', title='Explica el resultado', subtitle='Presenta tus decisiones y las evidencias de tu ejecución.',
      action='Revisa con Bob el diff y el Mermaid del resultado, y guarda tres conclusiones sobre la modernización de RoomFlow.',
      bob='Puede ayudarte a resumir la transformación y explicar las responsabilidades de cada capa.',
      participant='Contrasta las afirmaciones con el código y las pruebas, y presenta tus conclusiones.',
      expected='Puedes mostrar una mejora de UI, una regla preservada y un límite pendiente, junto con tus capturas, pruebas y Mermaid revisado.',
      path=['Source Control · diff', 'Workflow · Mermaid y resumen', 'Exportar mi recorrido'],
      sourceIds=['conclusiones','entrega'], noteIds=['referencia-tecnica'],
      intro='Utiliza Tus notas para recoger qué cambió, qué se conservó y qué queda pendiente. Exporta tu recorrido al terminar. El ensayo de referencia sirve para comparar; registra las versiones y resultados de tu propia ejecución.',
      screenshot='referencia/sesion-bob/09-workflow-completado.png', caption='Referencia del cierre: resumen de tareas de Bob. Contrasta el Mermaid con tu propia ejecución.',
      details=[('Informe ampliado y plantilla de entrega', ['entrega']), ('Resultados del ensayo de referencia', ['conclusiones']), ('Consulta técnica y resolución de problemas', ['referencia-tecnica'])]),
]

SUPPORT = '''<details>
<summary>Si te bloqueas: utiliza el chat de Bob</summary>

Mantén abierto el archivo relevante y aporta el error o la salida de la terminal al chat de Bob. Consulta qué ocurre, revisa la corrección que proponga y deja que la aplique dentro de la tarea. Después vuelve a ejecutar la comprobación que falló.

Si el wizard espera que arranques un servicio en otro terminal, usa el comando y la carpeta que te indique y comprueba la URL. Puedes consultar cómo hacerlo desde el propio IDE.

Si no aparece el flujo, revisa la raíz del proyecto y el paquete instalado. Consulta [cómo iniciar el workflow](https://bob.ibm.com/docs/ide/premium-packages/java-modernization/getting-started) y [los requisitos](https://bob.ibm.com/docs/ide/premium-packages/java-modernization/prerequisites).

</details>'''

def guided_sections(ident, original):
    by_id = {s['id']: s for s in original}
    configs = GUIDED_JAVA if ident == 'java' else GUIDED_UI
    result = []
    for config in configs:
        section = {k:v for k,v in config.items() if k not in {'details','intro','introIds','markdown'}}
        parts = [config['intro']]
        parts.extend(by_id[key]['markdown'] for key in config.get('introIds', []))
        for summary, ids in config['details']:
            blocks = [by_id[key]['markdown'] for key in ids]
            parts.append('<details>\n<summary>'+summary+'</summary>\n\n'+'\n\n'.join(blocks)+'\n\n</details>')
        if config.get('markdown'):parts.append(config['markdown'])
        parts.append(SUPPORT)
        section.update(markdown='\n\n'.join(parts), source='LAB.md',
                       checks=[config['expected']],
                       legacyTitles={key:by_id[key]['title'] for key in config['sourceIds']+config.get('noteIds',[])})
        result.append(section)
    return result

def build():
    pub=ROOT/'public'
    for folder in ['content','media','downloads','resources']:
        p=pub/folder
        if p.exists():shutil.rmtree(p)
        p.mkdir(parents=True)
    courses=[]
    for ident,name in LABS:
        src=ROOT/'laboratorios'/name
        guide=(src/'LAB.md').read_text()
        original=java_sections(guide) if ident=='java' else ui_sections(guide)
        sections=guided_sections(ident,original)
        aliases={key:s['id'] for s in sections for key in s['sourceIds']+s.get('noteIds',[])}
        # The original last Java step included both validation and closure.
        if ident=='java':aliases['validar']='comprobar'
        aliases['pasos']='modernizar'
        resources=[];files={};images={}
        for p in sorted(src.rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(src).as_posix()
            if p.suffix=='.md':
                if rel not in {'LAB.md','README.md'}:
                    md=p.read_text();heading=re.search(r'^# (.+)',md,re.M)
                    resources.append(dict(path=rel,title=heading.group(1) if heading else p.stem,markdown=md))
            elif p.suffix.lower() in {'.png','.jpg','.jpeg','.svg','.webp'}:
                out=pub/'media'/ident/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
                images[rel]=out.relative_to(pub).as_posix()
            elif p.suffix in {'.json','.txt','.mmd'}:
                out=pub/'resources'/ident/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
                files[rel]=out.relative_to(pub).as_posix()
        zipname='lab-01-java.zip' if ident=='java' else 'lab-02-ui.zip'
        with zipfile.ZipFile(pub/'downloads'/zipname,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(src.rglob('*')):
                if p.is_file():z.write(p,Path(name)/p.relative_to(src))
        courses.append(dict(id=ident,folder=name,number='01' if ident=='java' else '02',
            title='Modernización Java' if ident=='java' else 'Modernización de UI',
            project='AssetDesk' if ident=='java' else 'RoomFlow',
            stack='Java 8 → Java 21' if ident=='java' else 'JSF / Struts → React',
            description='Lleva una aplicación Java a su siguiente versión y demuestra que el comportamiento se conserva.' if ident=='java' else 'Transforma una interfaz legacy en una experiencia React conectada a una API Java.',
            sections=sections,aliases=aliases,resources=resources,images=images,files=files,download='downloads/'+zipname,
            sourceUrl='https://github.com/JoseManuelVasquez/bobathon_bcn_2026/tree/main/laboratorios/'+name))
    data=dict(title='Bobathon BCN',year='2026',repository='https://github.com/JoseManuelVasquez/bobathon_bcn_2026',courses=courses)
    (pub/'content/courses.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
    (pub/'.nojekyll').touch()
    print('Contenido preparado:',', '.join(f'{c["project"]}: {len(c["sections"])} pasos' for c in courses))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path)
    args=parser.parse_args()
    if args.source_root:import_labs(args.source_root.resolve())
    build()
