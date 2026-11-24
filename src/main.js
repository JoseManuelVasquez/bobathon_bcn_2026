import '@fontsource/ibm-plex-sans/latin-400.css';
import '@fontsource/ibm-plex-sans/latin-500.css';
import '@fontsource/ibm-plex-sans/latin-600.css';
import '@fontsource/ibm-plex-mono/latin-400.css';
import bobIcon from './bob-icon.svg?raw';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { icon } from './icons.js';
import { migrateProgress } from './progress.js';
import './style.css';

const STORAGE = 'bobathon-bcn-2026:workshop:v1';
const app = document.querySelector('#app');
const esc = (s='') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let saved = { completed: {}, notes: {}, theme: 'system' };
try { saved = { ...saved, ...JSON.parse(localStorage.getItem(STORAGE) || '{}') }; } catch { /* Start with a fresh local record. */ }
saved.completed = typeof saved.completed === 'object' && saved.completed ? saved.completed : {};
saved.notes = typeof saved.notes === 'object' && saved.notes ? saved.notes : {};
if (!['light','dark','system'].includes(saved.theme)) saved.theme='system';
const systemScheme=window.matchMedia('(prefers-color-scheme: dark)');
applyTheme();
let data, route, renderToken = 0, mermaidPromise, diagramQueue=Promise.resolve();
function applyTheme() {
 const effective=saved.theme==='system'?(systemScheme.matches?'dark':'light'):saved.theme;
 document.documentElement.dataset.theme=effective;
 document.documentElement.dataset.themePreference=saved.theme;
 document.querySelector('meta[name="theme-color"]')?.setAttribute('content',effective==='dark'?'#0f1116':'#ffffff');
 const names={light:['sun','Light'],dark:['moon','Dark'],system:['monitor','System']};
 const choice=names[saved.theme];
 const trigger=document.querySelector('.theme-trigger');
 if(trigger){trigger.innerHTML=icon(choice[0]);trigger.setAttribute('aria-label','Apariencia: '+choice[1]);}
 document.querySelectorAll('[data-theme-value]').forEach(button=>{const checked=button.dataset.themeValue===saved.theme;button.setAttribute('aria-checked',checked);button.querySelector('.theme-check').innerHTML=checked?icon('check'):'';});
}
function closeThemeMenu(focus=false) {
 const menu=document.querySelector('#theme-menu'),trigger=document.querySelector('.theme-trigger');
 if(menu)menu.hidden=true;
 trigger?.setAttribute('aria-expanded','false');
 if(focus)trigger?.focus({preventScroll:true});
}
function toggleThemeMenu() {
 const menu=document.querySelector('#theme-menu');if(!menu)return;
 const open=menu.hidden;menu.hidden=!open;
 document.querySelector('.theme-trigger').setAttribute('aria-expanded',String(open));
 if(open)(menu.querySelector('[aria-checked="true"]') || menu.querySelector('button'))?.focus();
}
systemScheme.addEventListener('change',()=>{if(saved.theme==='system'){applyTheme();refreshDiagrams();}});
const key = (c,s) => `${c.id}/${s.id}`;
const isDone = (c,s) => saved.completed[key(c,s)] === true;
const count = c => c.sections.filter(s => isDone(c,s)).length;
const totalDone = () => data.courses.reduce((n,c) => n+count(c),0);
const total = () => data.courses.reduce((n,c) => n+c.sections.length,0);
const lessonUrl = (c,s) => `#lab/${c.id}/${s.id}`;
const nextLesson = c => c.sections.find(s => !isDone(c,s)) || c.sections[0];
const asset = path => new URL(path, document.baseURI).href;
function persist() { try { localStorage.setItem(STORAGE, JSON.stringify(saved)); } catch { toast('No se ha podido guardar en este navegador. Puedes exportar tu informe.'); } }
function toast(message) { const t=document.querySelector('#toast'); t.textContent=message; t.classList.add('visible'); clearTimeout(toast.timer); toast.timer=setTimeout(()=>t.classList.remove('visible'),3000); }
function progress(c) { return Math.round(count(c)/c.sections.length*100); }
function plain(s) { return s.replace(/```[\s\S]*?```/g,' ').replace(/<[^>]+>/g,' ').replace(/[#*_`>|\[\]]/g,' ').replace(/\s+/g,' ').trim(); }
function slugPath(source, href) {
  const base=source.includes('/')?source.slice(0,source.lastIndexOf('/')+1):'';
  const parts=[];
  for(const piece of (base+href).split('/')) { if(piece==='..')parts.pop(); else if(piece!=='.' && piece)parts.push(piece); }
  return parts.join('/');
}
function resolveLink(c,source,href) {
  if(/^(https?:|mailto:)/.test(href)) return href;
  if(href.startsWith('#')) { const id=href.slice(1); const step=c.sections.find(s=>s.id===(c.aliases?.[id]||id))||c.sections[0]; return lessonUrl(c,step); }
  if(href.includes('LAB-02-UI-MODERNIZATION/') && c.id==='java')return lessonUrl(data.courses[1],data.courses[1].sections[0]);
  const path=slugPath(source,decodeURIComponent(href.split('#')[0]));
  if(path==='LAB.md' || path==='README.md')return lessonUrl(c,c.sections[0]);
  if(c.resources.some(r=>r.path===path))return `#recurso/${c.id}/${encodeURIComponent(path)}`;
  if(c.images[path])return asset(c.images[path]);
  if(c.files[path])return asset(c.files[path]);
  return `${c.sourceUrl}/${path.split('/').map(encodeURIComponent).join('/')}`;
}
function markdown(c,source,text) {
  const template=document.createElement('template');
  template.innerHTML=DOMPurify.sanitize(marked.parse(text,{gfm:true}),{ADD_ATTR:['target']});
  template.content.querySelectorAll('img').forEach(img=>{
    const path=slugPath(source,img.getAttribute('src') || '');
    img.src=asset(c.images[path] || ''); img.loading='lazy'; img.decoding='async';
  });
  template.content.querySelectorAll('a[href]').forEach(a=>{
    a.href=resolveLink(c,source,a.getAttribute('href'));
    if(!a.getAttribute('href').startsWith('#')) {a.target='_blank';a.rel='noopener noreferrer';}
  });
  template.content.querySelectorAll('table').forEach(table=>{const wrap=document.createElement('div');wrap.className='table-scroll';table.replaceWith(wrap);wrap.append(table);});
  template.content.querySelectorAll('pre').forEach(pre=>{
    const code=pre.querySelector('code');
    if(code?.classList.contains('language-mermaid')) {
      const figure=document.createElement('figure');figure.className='diagram-block';
      const diagram=document.createElement('div');diagram.className='mermaid';diagram.textContent=code.textContent;diagram.dataset.source=code.textContent;
      figure.append(diagram);pre.replaceWith(figure);
    } else {
      pre.classList.add('code-block');
      const button=document.createElement('button');button.className='copy-code';button.dataset.action='copy-code';button.innerHTML=icon('copy')+'<span>Copiar</span>';button.setAttribute('aria-label','Copiar el código');pre.prepend(button);
    }
  });
  const wrapper=document.createElement('div');wrapper.append(template.content);return wrapper.innerHTML;
}
function diagrams(token) {
 const nodes=[...app.querySelectorAll('.mermaid:not([data-processed]):not([data-rendering])')].filter(n=>n.checkVisibility ? n.checkVisibility() : n.getClientRects().length>0);
 if(!nodes.length)return diagramQueue;
 nodes.forEach(n=>n.dataset.rendering='true');
 diagramQueue=diagramQueue.catch(()=>{}).then(async()=>{
  try {
   mermaidPromise ||= import('mermaid').then(({default:m})=>m);
   const m=await mermaidPromise;if(token!==renderToken)return;
   const dark=document.documentElement.dataset.theme==='dark';
   m.initialize({startOnLoad:false,securityLevel:'strict',theme:dark?'dark':'base',themeVariables:{primaryColor:dark?'#1d293c':'#edf2ff',primaryTextColor:dark?'#f4f4f4':'#171717',primaryBorderColor:dark?'#637ca6':'#8bb1f3',secondaryColor:dark?'#202b3b':'#f1f5fc',tertiaryColor:dark?'#151a23':'#f7f9fd',lineColor:dark?'#b3c4df':'#526789',textColor:dark?'#f4f4f4':'#171717',background:dark?'#12161d':'#ffffff',edgeLabelBackground:dark?'#181e29':'#ffffff',clusterBkg:dark?'#171e29':'#f5f7fc',clusterBorder:dark?'#3e4a60':'#c7d2e4',fontFamily:'IBM Plex Sans, sans-serif'},suppressErrorRendering:true});
   nodes.forEach(n=>{n.textContent=n.dataset.source;delete n.dataset.processed;});
   await m.run({nodes});if(token!==renderToken)return;
   nodes.forEach(node=>{const fig=node.closest('figure');if(!node.querySelector('svg') || !fig)return;fig.querySelector('.diagram-expand')?.remove();const button=document.createElement('button');button.className='diagram-expand';button.dataset.action='expand-diagram';button.innerHTML=icon('expand')+'Ampliar diagrama';fig.append(button);});
  } catch {nodes.forEach(n=>{if(!n.querySelector('svg'))n.classList.add('diagram-source');});}
  finally {nodes.forEach(n=>delete n.dataset.rendering);}
 });
 return diagramQueue;
}
function refreshDiagrams() {
 const token=++renderToken;
 app.querySelectorAll('.mermaid').forEach(n=>{n.textContent=n.dataset.source;delete n.dataset.processed;delete n.dataset.rendering;n.classList.remove('diagram-source');n.closest('figure')?.querySelector('.diagram-expand')?.remove();});
 diagrams(token);
}
function parseRoute() {
  const parts=location.hash.replace(/^#/,'').split('/');
  if(parts[0]==='lab') {const c=data.courses.find(c=>c.id===parts[1]); const s=c?.sections.find(s=>s.id===(c.aliases?.[parts[2]]||parts[2]));if(c&&s)return {kind:'lesson',course:c,section:s};}
  if(parts[0]==='recurso') {const c=data.courses.find(c=>c.id===parts[1]);let path='';try{path=decodeURIComponent(parts.slice(2).join('/'));}catch{}const r=c?.resources.find(r=>r.path===path);if(c&&r)return {kind:'reference',course:c,reference:r};}
  return {kind:parts[0]==='recursos'?'resources':'home'};
}
function sidebar() {
  return `<aside class="sidebar" aria-label="Navegación del workshop">
    <button class="sidebar-search" data-action="search">${icon('search')}<span>Buscar en los retos</span><kbd>⌘ K</kbd></button>
    <span class="nav-label">WORKSHOP</span>
    <a class="nav-main ${route.kind==='home'?'active':''}" href="#inicio" ${route.kind==='home'?'aria-current="page"':''}>${icon('home')}<span>Vista general</span></a>
    <div class="course-nav">${data.courses.map(c=>`<div class="course-nav-group"><a class="nav-main ${route.course?.id===c.id?'active':''}" href="${lessonUrl(c,nextLesson(c))}">${icon(c.id==='java'?'code':'layers')}<span>${c.title}</span><span class="nav-course-number">${c.number}</span></a>${route.course?.id===c.id?`<nav class="lesson-list" aria-label="Hitos de ${c.title}">${c.sections.map((s,i)=>`<a href="${lessonUrl(c,s)}" class="lesson-link ${route.section?.id===s.id?'current':''} ${isDone(c,s)?'done':''}" ${route.section?.id===s.id?'aria-current="step"':''}><span class="lesson-index">${isDone(c,s)?icon('check'):String(i+1).padStart(2,'0')}</span><span>${s.title}</span></a>`).join('')}</nav>`:''}</div>`).join('')}</div>
    <a class="nav-main ${route.kind==='resources'?'active':''}" href="#recursos">${icon('download')}<span>Material y descargas</span></a>
    ${route.kind==='home'?'':`<div class="sidebar-bottom"><div class="local-progress"><span>Tu recorrido</span><strong>${totalDone()}<span> / ${total()}</span></strong></div><div class="progress-track"><span style="width:${Math.round(totalDone()/total()*100)}%"></span></div><p>${icon('info')} Tu progreso se guarda en este navegador.</p><a class="repository-link" href="${data.repository}" target="_blank" rel="noopener noreferrer">Ver repositorio ${icon('external')}</a></div>`}
  </aside>`;
}
function header() {
  const options=[['light','sun','Light'],['dark','moon','Dark'],['system','monitor','System']];
  const selected=options.find(([value])=>value===saved.theme);
  return `<header class="topbar"><div class="topbar-left"><button class="icon-button mobile-menu" data-action="menu" aria-label="Abrir navegación" aria-expanded="false">${icon('menu')}</button><a class="site-brand" href="#inicio"><span class="bob-mark" aria-hidden="true">${bobIcon.replace(/<style>[\s\S]*?<\/style>/,'')}</span><span>Bobathon <strong>BCN</strong></span><span class="brand-year">2026</span></a><nav class="header-nav" aria-label="Secciones del sitio"><a href="#inicio" class="selected">Workshop</a><a href="https://bob.ibm.com/docs" target="_blank" rel="noopener noreferrer">Bob Docs ${icon('external')}</a></nav></div><div class="topbar-actions"><button class="icon-button header-search" data-action="search" aria-label="Buscar en los retos">${icon('search')}</button><div class="theme-control"><button class="icon-button theme-trigger" data-action="theme-menu" aria-label="Apariencia: ${selected[2]}" aria-haspopup="menu" aria-expanded="false" aria-controls="theme-menu">${icon(selected[1])}</button><div id="theme-menu" class="theme-menu" role="menu" aria-label="Apariencia" hidden>${options.map(([value,symbol,label])=>`<button type="button" role="menuitemradio" aria-checked="${saved.theme===value}" data-action="select-theme" data-theme-value="${value}">${icon(symbol)}<span>${label}</span><span class="theme-check">${saved.theme===value?icon('check'):''}</span></button>`).join('')}</div></div><a class="repository-top-link" href="${data.repository}" target="_blank" rel="noopener noreferrer">Repositorio ${icon('external')}</a></div></header>`;
}
function courseCard(c) {
  const n=count(c);return `<a class="lab-card lab-${c.id}" href="${lessonUrl(c,nextLesson(c))}"><div class="card-eyebrow"><span class="lab-icon">${icon(c.id==='java'?'code':'layers')}</span><span>RETO ${c.number}</span><span class="card-arrow">${icon('arrow')}</span></div><h2>${c.title}</h2><span class="stack-tag">${c.stack}</span><p>${c.description}</p><div class="card-bottom"><span>${n?`${n} de ${c.sections.length} hitos completados`:`${c.sections.length} hitos para explorar`}</span><strong>${n?'Continuar':'Empezar'} ${icon('arrow')}</strong></div><div class="card-progress"><span style="width:${progress(c)}%"></span></div></a>`;
}
function comparison() {
 const c=data.courses[1];
 const before=asset(c.images['referencia/capturas-aportadas/antes-jsf.png']);
 const after=asset(c.images['referencia/capturas-aportadas/despues-react.png']);
 return `<section class="comparison-section" aria-labelledby="comparison-heading"><div class="section-heading"><div><span class="eyebrow">EL RESULTADO, A LA VISTA</span><h2 id="comparison-heading">Mismas reglas. Otra experiencia.</h2></div><div class="segmented" aria-label="Pantallas a comparar"><button class="selected" data-action="comparison-tab" data-pair="home" aria-pressed="true">Inicio</button><button data-action="comparison-tab" data-pair="list" aria-pressed="false">Listado</button></div></div><div class="compare-frame" style="--reveal:50%"><img class="compare-after" src="${after}" alt="Después: dashboard React de RoomFlow" loading="lazy"><div class="compare-before"><img src="${before}" alt="Antes: listado y formulario JSF de RoomFlow" loading="lazy"></div><span class="compare-label before-label">ANTES <b id="before-stack">JSF</b></span><span class="compare-label after-label">DESPUÉS <b>REACT</b></span><span class="compare-divider"><span>‹ ${icon('layers')} ›</span></span><input class="compare-range" type="range" min="0" max="100" value="50" aria-label="Porcentaje de imagen original visible" data-action="compare"></div><p class="compare-caption">${icon('info')} Arrastra para comparar. Las vistas de Inicio muestran capturas de referencia; en Listado puedes comparar el mismo estado inicial.</p></section>`;
}
function home() {
 return `<main id="main" class="main-content home-content" tabindex="-1"><h1 class="sr-only">Retos del workshop</h1><div class="lab-grid">${data.courses.map(courseCard).join('')}</div></main>`;
}
function lesson() {
 const c=route.course,s=route.section,i=c.sections.indexOf(s),done=isDone(c,s);let source=s.markdown.replace(/^\s*(?:<a[^>]+><\/a>\s*)?(?:#{1,3} [^\n]+\n)/,'');
 return `<main id="main" class="main-content lesson-content" tabindex="-1"><div class="lesson-topline"><a href="#inicio" class="text-link muted">${icon('back')} Todos los laboratorios</a><span class="lesson-position">HITO ${String(i+1).padStart(2,'0')} <span>/ ${String(c.sections.length).padStart(2,'0')}</span></span></div><div class="lesson-heading"><span class="eyebrow">${c.project.toUpperCase()} · ${c.stack}</span><h1>${s.title}</h1><p>${s.subtitle}</p></div><div class="lesson-layout"><article class="reading-panel"><section class="milestone-action" aria-label="Acción principal"><span class="eyebrow">TU SIGUIENTE ACCIÓN EN BOB</span><p>${esc(s.action)}</p><ol class="ide-path" aria-label="Dónde actuar">${s.path.map(p=>`<li>${esc(p)}</li>`).join('')}</ol></section><div class="role-summary"><div><span>${icon('sparkle')} BOB</span><p>${esc(s.bob)}</p></div><div><span>${icon('check')} TÚ</span><p>${esc(s.participant)}</p></div></div><div class="markdown-body">${markdown(c,s.source,source)}</div>${s.comparison?`<details class="milestone-reference"><summary>Ver el comparador de antes y después</summary>${comparison()}</details>`:''}${s.screenshot?`<details class="milestone-reference"><summary>Ver una captura orientativa</summary><figure><img src="${asset(c.images[s.screenshot])}" alt="${esc(s.caption)}" loading="lazy"><figcaption>${esc(s.caption)}</figcaption></figure></details>`:''}<div class="lesson-navigation"><a class="button secondary ${i===0?'invisible':''}" href="${i?lessonUrl(c,c.sections[i-1]):'#inicio'}">${icon('back')} Anterior</a><button class="button primary" data-action="complete-next">${i===c.sections.length-1?'Completar reto':'Completar y seguir'} ${icon('arrow')}</button></div></article><aside class="lesson-aside"><div class="checkpoint-card"><span class="aside-eyebrow">${icon('check')} PUEDES CONTINUAR CUANDO</span><p class="expected-result">${esc(s.expected)}</p><button class="completion-button ${done?'is-complete':''}" data-action="toggle-complete" aria-pressed="${done}"><span class="completion-checkbox">${done?icon('check'):''}</span>${done?'Hito completado':'Marcar como completado'}</button><div class="aside-progress"><span>Avance del reto</span><strong>${count(c)}/${c.sections.length}</strong></div><div class="progress-track"><span style="width:${progress(c)}%"></span></div></div><details class="notes-card" ${s.id==='concluir'?'open':''}><summary>${icon('note')} Tus notas</summary><label class="sr-only" for="lesson-notes">Notas de este hito</label><textarea id="lesson-notes" data-action="save-notes" placeholder="Qué decidiste, qué comprobaste y qué queda pendiente…">${esc(saved.notes[key(c,s)] || '')}</textarea><span class="notes-saved">Se guardan en este navegador</span></details><a class="aside-download" href="${asset(c.download)}" download>${icon('download')} Descargar este laboratorio ${icon('chevron')}</a><button class="aside-download" data-action="export-report" data-course="${c.id}">${icon('note')} Exportar mi recorrido ${icon('chevron')}</button></aside></div></main>`;
}
function resources() {
 return `<main id="main" class="main-content resources-content" tabindex="-1"><span class="eyebrow">TODO PARA TRABAJAR</span><h1>Tu material. Tus conclusiones.</h1><p class="page-description">Descarga los proyectos para abrirlos en Bob y lleva contigo las notas y decisiones de tu recorrido.</p><div class="resource-grid">${data.courses.map(c=>`<section class="resource-card"><span class="lab-icon">${icon(c.id==='java'?'code':'layers')}</span><span class="eyebrow">LABORATORIO ${c.number}</span><h2>${c.project}</h2><p>${c.description}</p><div class="resource-actions"><a class="button primary" href="${asset(c.download)}" download>${icon('download')} Descargar proyecto</a><a class="button secondary" href="${c.sourceUrl}" target="_blank" rel="noopener noreferrer">Ver fuentes ${icon('external')}</a></div><div class="resource-divider"></div><div class="aside-progress"><span>${count(c)} de ${c.sections.length} hitos completados</span><strong>${progress(c)}%</strong></div><div class="progress-track"><span style="width:${progress(c)}%"></span></div><button class="text-link export-link" data-action="export-report" data-course="${c.id}">${icon('note')} Exportar notas y avance ${icon('arrow')}</button></section>`).join('')}</div><section class="delivery-section"><h2>Conserva tus decisiones y evidencias.</h2><div class="delivery-grid"><div><span>01</span><h3>Explica tus decisiones</h3><p>Qué detectó Bob, qué elegiste y por qué. Conserva las versiones y rutas de tu ejecución.</p></div><div><span>02</span><h3>Adjunta evidencias</h3><p>Incluye capturas, diagramas y resultados reales. Distingue pruebas automáticas y recorridos manuales.</p></div><div><span>03</span><h3>Escribe tus conclusiones</h3><p>Qué cambió, qué se preservó y qué queda pendiente para el siguiente paso.</p></div></div></section><div class="storage-note">${icon('info')} El progreso y las notas pertenecen a este navegador. Exporta tu recorrido para conservar una copia o cambiar de equipo.</div><button class="text-link reset-button" data-action="reset-progress">${icon('reset')} Reiniciar mi progreso</button></main>`;
}
function reference() {
 const c=route.course,r=route.reference;return `<main id="main" class="main-content reference-content" tabindex="-1"><a class="text-link muted" href="${lessonUrl(c,nextLesson(c))}">${icon('back')} Volver al laboratorio</a><div class="lesson-heading"><span class="eyebrow">REFERENCIA · ${c.project}</span><h1>${esc(r.title)}</h1><p>Consulta este material como apoyo a tu recorrido.</p></div><article class="reading-panel markdown-body">${markdown(c,r.path,r.markdown.replace(/^# [^\n]+\n/,''))}</article></main>`;
}
function render(focus=true) {
 route=parseRoute();const token=++renderToken;document.querySelectorAll('dialog[open]').forEach(d=>d.close());
 document.body.classList.remove('nav-open');
 app.innerHTML=`${sidebar()}<div class="page-shell">${header()}${route.kind==='home'?home():route.kind==='lesson'?lesson():route.kind==='resources'?resources():reference()}</div><button class="nav-overlay" data-action="menu" aria-label="Cerrar navegación"></button>`;
 document.title=`${route.section?.title || (route.kind==='resources'?'Material y descargas':'Retos del workshop')} · Bobathon BCN 2026`;
 window.scrollTo(0,0);if(focus)app.querySelector('#main')?.focus({preventScroll:true});
 diagrams(token);
}
function download(content,name,type='text/markdown;charset=utf-8') {const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function exportReport(c) {
 let text=`# Mi recorrido · ${c.title}\n\nProyecto: ${c.project}\nDestino: ${c.stack}\nHitos revisados: ${count(c)} de ${c.sections.length}\n\nEste archivo recoge tus notas y avance. Añade las evidencias de tu ejecución al informe final.\n`;
 for(const s of c.sections)text+=`\n## ${s.title}\n\nRevisión: ${isDone(c,s)?'COMPLETADA':'PENDIENTE'}\n\n${saved.notes[key(c,s)] || 'Sin notas todavía.'}\n`;
 text+='\n## Conclusiones\n\nQué cambió, qué se conservó, resultados comprobados y siguientes pasos:\n\n';download(text,`mi-recorrido-${c.project.toLowerCase()}.md`);toast('Tu recorrido se ha exportado.');
}
function openSearch() {
 const d=document.querySelector('#search-dialog');d.innerHTML=`<div class="dialog-header"><h2 id="search-title">¿Qué estás buscando?</h2><button class="icon-button" data-action="close-dialog" aria-label="Cerrar búsqueda">${icon('close')}</button></div><label class="search-field">${icon('search')}<input type="search" id="global-search" placeholder="Prueba con Maven, conflicto, Java 21…" autocomplete="off" aria-label="Buscar en el workshop"></label><div id="search-results" class="search-results"><p>Busca una regla, una herramienta o un paso de cualquiera de los dos laboratorios.</p></div>`;d.showModal();d.querySelector('input').focus();
}
function search(value) {
 const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const q=norm(value.trim());const el=document.querySelector('#search-results');if(!el)return;
 const matches=[];if(q.length>1)for(const c of data.courses)for(const s of c.sections){const text=plain([s.action,s.bob,s.participant,s.expected,s.markdown].join(' '));const at=norm(s.title+' '+text).indexOf(q);if(at!==-1)matches.push({c,s,text});}
 el.innerHTML=q.length<2?'<p>Escribe al menos dos caracteres.</p>':!matches.length?'<p>No hay resultados. Prueba con otra palabra.</p>':`<span class="result-count">${matches.length} hitos encontrados</span>${matches.slice(0,16).map(({c,s,text})=>`<a class="search-result" href="${lessonUrl(c,s)}"><span>${c.project}</span><strong>${esc(s.title)} ${icon('arrow')}</strong><p>${esc(text.slice(0,180))}…</p></a>`).join('')}`;
}
let diagramScale=1;
function openDiagram(button) {
 const svg=button.closest('figure')?.querySelector('svg');if(!svg)return;
 const d=document.querySelector('#diagram-dialog');d.innerHTML=`<div class="dialog-header"><h2 id="diagram-title">Explora el diagrama</h2><div class="diagram-tools"><button class="icon-button" data-action="diagram-minus" aria-label="Alejar">−</button><button class="icon-button" data-action="diagram-plus" aria-label="Acercar">+</button><button class="icon-button" data-action="diagram-download" aria-label="Descargar SVG">${icon('download')}</button><button class="icon-button" data-action="close-dialog" aria-label="Cerrar diagrama">${icon('close')}</button></div></div><div class="diagram-viewport"><div class="diagram-canvas">${svg.outerHTML}</div></div>`;diagramScale=1;d.showModal();
}
async function copyCode(button) {
 const text=button.closest('pre')?.querySelector('code')?.textContent || '';
 let copied=false;
 try {await navigator.clipboard.writeText(text);copied=true;} catch {
  const helper=document.createElement('textarea');helper.value=text;helper.setAttribute('readonly','');helper.style.cssText='position:fixed;left:-9999px;top:0';document.body.append(helper);helper.select();
  try {copied=document.execCommand('copy');} catch {copied=false;}
  helper.remove();button.focus({preventScroll:true});
 }
 if(copied){button.innerHTML=icon('check')+'<span>Copiado</span>';setTimeout(()=>{if(button.isConnected)button.innerHTML=icon('copy')+'<span>Copiar</span>';},1800);}
 else {const range=document.createRange();range.selectNodeContents(button.closest('pre').querySelector('code'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Código seleccionado. Usa el atajo de copiar de tu equipo.');}
}
function switchComparison(button) {
 const c=data.courses[1],list=button.dataset.pair==='list';
 const before=c.images[list?'referencia/sesion-bob/antes-listado.png':'referencia/capturas-aportadas/antes-jsf.png'];
 const after=c.images[list?'referencia/sesion-bob/despues-listado.png':'referencia/capturas-aportadas/despues-react.png'];
 const frame=document.querySelector('.compare-frame');frame.querySelector('.compare-before img').src=asset(before);frame.querySelector('.compare-after').src=asset(after);
 frame.querySelector('.compare-before img').alt=list?'Antes: listado Struts con cuatro reservas':'Antes: listado JSF';frame.querySelector('.compare-after').alt=list?'Después: listado React con las mismas cuatro reservas':'Después: dashboard React';
 frame.querySelector('#before-stack').textContent=list?'STRUTS':'JSF';
 document.querySelectorAll('[data-action="comparison-tab"]').forEach(b=>{const selected=b===button;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',selected);});
}
document.addEventListener('click',e=>{
 const action=e.target.closest('[data-action]');
 if(!e.target.closest('.theme-control'))closeThemeMenu();
 if(e.target.closest('.search-result'))document.querySelector('#search-dialog').close();
 if(!action)return;
 const name=action.dataset.action;
 if(name==='search')openSearch();
 if(name==='close-dialog')action.closest('dialog')?.close();
 if(name==='menu'){const open=document.body.classList.toggle('nav-open');document.querySelector('.mobile-menu')?.setAttribute('aria-expanded',open);if(open)document.querySelector('.sidebar a')?.focus();else document.querySelector('.mobile-menu')?.focus();}
 if(name==='theme-menu')toggleThemeMenu();
 if(name==='select-theme'){saved.theme=action.dataset.themeValue;persist();applyTheme();closeThemeMenu(true);refreshDiagrams();}
 if(name==='toggle-complete' || name==='complete-next'){
  const {course:c,section:s}=route;if(!c||!s)return;
  saved.completed[key(c,s)]=name==='complete-next'?true:!isDone(c,s);persist();
  if(name==='complete-next') {const i=c.sections.indexOf(s);if(i<c.sections.length-1)location.hash=lessonUrl(c,c.sections[i+1]);else{location.hash='#recursos';toast('Recorrido completado. Guarda tus evidencias y conclusiones.');}}
  else {render(false);document.querySelector('[data-action="toggle-complete"]')?.focus({preventScroll:true});}
 }
 if(name==='copy-code')copyCode(action);
 if(name==='export-report'){const c=data.courses.find(c=>c.id===action.dataset.course);if(c)exportReport(c);}
 if(name==='expand-diagram')openDiagram(action);
 if(name==='diagram-plus'||name==='diagram-minus'){diagramScale=Math.max(.5,Math.min(3,diagramScale+(name==='diagram-plus' ? 0.25 : -0.25)));document.querySelector('.diagram-canvas').style.zoom=diagramScale;}
 if(name==='diagram-download'){const svg=document.querySelector('#diagram-dialog svg');if(svg)download(svg.outerHTML,'diagrama-bobathon.svg','image/svg+xml;charset=utf-8');}
 if(name==='comparison-tab')switchComparison(action);
 if(name==='reset-progress'){
  const d=document.querySelector('#notes-dialog');d.innerHTML=`<div class="dialog-header"><h2 id="notes-title">Reiniciar los hitos</h2><button class="icon-button" data-action="close-dialog" aria-label="Cerrar">${icon('close')}</button></div><p>Se desmarcarán las hitos completados. Tus notas se conservarán.</p><div class="dialog-actions"><button class="button secondary" data-action="close-dialog">Conservar progreso</button><button class="button primary" data-action="confirm-reset">Reiniciar hitos</button></div>`;d.showModal();
 }
 if(name==='confirm-reset'){saved.completed={};persist();action.closest('dialog').close();render(false);toast('Hitos reiniciados. Tus notas se conservan.');}
});
document.addEventListener('input',e=>{
 if(e.target.id==='global-search')search(e.target.value);
 if(e.target.dataset.action==='compare')e.target.closest('.compare-frame').style.setProperty('--reveal',e.target.value+'%');
 if(e.target.dataset.action==='save-notes' && route.course && route.section){saved.notes[key(route.course,route.section)]=e.target.value;persist();const status=document.querySelector('.notes-saved');if(status)status.textContent='Notas guardadas en este navegador';}
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeThemeMenu(document.querySelector('#theme-menu')?.hidden===false);if(e.target.closest('.theme-menu') && ['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();const buttons=[...document.querySelectorAll('#theme-menu button')];const current=buttons.indexOf(document.activeElement);const index=e.key==='Home'?0:e.key==='End'?buttons.length-1:(current+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length;buttons[index].focus();}if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();if(!document.querySelector('#search-dialog').open)openSearch();}if(e.key==='Escape')document.querySelectorAll('dialog[open]').forEach(d=>d.close());if(e.key==='Escape' && document.body.classList.contains('nav-open')){document.body.classList.remove('nav-open');document.querySelector('.mobile-menu')?.setAttribute('aria-expanded','false');document.querySelector('.mobile-menu')?.focus();}});
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
document.addEventListener('toggle',e=>{if(e.target.tagName==='DETAILS' && e.target.open)diagrams(renderToken);},true);
document.querySelector('.skip-link').addEventListener('click',e=>{e.preventDefault();const main=document.querySelector('#main');main?.focus();main?.scrollIntoView({block:'start'});});
document.addEventListener('focusin',e=>{if(!e.target.closest('.theme-control'))closeThemeMenu();});
window.addEventListener('hashchange',()=>render());
try {
 const response=await fetch(asset('content/courses.json'));if(!response.ok)throw new Error('content');data=await response.json();const migrated=migrateProgress(saved,data.courses);if(migrated!==saved){saved=migrated;persist();}render(false);
} catch {
 app.innerHTML='<main id="main" class="initial-loading"><h1>No se ha podido cargar el workshop.</h1><p>Comprueba la conexión y vuelve a abrir la página.</p><button class="button primary" onclick="location.reload()">Volver a cargar</button></main>';
}
