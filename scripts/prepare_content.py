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
 ('referencia', 'Conoce el comportamiento', 'Ejecuta la demo antes de cambiar Java.', ['Guarda las tres pruebas iniciales.', 'Comprueba los contadores del JSON.']),
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
        sections=java_sections(guide) if ident=='java' else ui_sections(guide)
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
            sections=sections,resources=resources,images=images,files=files,download='downloads/'+zipname,
            sourceUrl='https://github.com/JoseManuelVasquez/bobathon_bcn_2026/tree/main/laboratorios/'+name))
    data=dict(title='Bobathon BCN',year='2026',repository='https://github.com/JoseManuelVasquez/bobathon_bcn_2026',courses=courses)
    (pub/'content/courses.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
    (pub/'.nojekyll').touch()
    print('Contenido preparado:',', '.join(f'{c["project"]}: {len(c["sections"])} etapas' for c in courses))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path)
    args=parser.parse_args()
    if args.source_root:import_labs(args.source_root.resolve())
    build()
