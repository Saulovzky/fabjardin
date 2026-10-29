#!/usr/bin/env python3
"""
Genera todas las páginas de Fabjardin.

Uso:  python3 tools/build.py

Aquí viven el menú (NAV), los datos de contacto, los servicios y el texto de
cada página. Después de editar algo, vuelve a ejecutarlo y sube los .html
resultantes. Las fotos de servicios se detectan solas: si existe
images/servicios/<archivo>.webp, aparece en la página de Laboratorio.
"""
import json
import math
import os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://fabjardin.com"
NAME = "Fabjardin"
TAGLINE = "Centro de Innovación y Tecnologías Creativas"

CONTACT = {
    "email": "info@fabjardin.com",
    "tel_label": "55 7657 1685",
    "tel_href": "+525576571685",
    "wa": "https://wa.me/525576571685?text=Hola%20Fabjardin%2C%20quiero%20m%C3%A1s%20informaci%C3%B3n",
    "address": "C. 5 de Febrero No. 23B, Col. La Bomba, C.P. 56600, Chalco de Díaz Covarrubias, Estado de México",
    "maps": "https://maps.app.goo.gl/UQqeSkzYNFNghbhFA",
}
IMPACT_REPORT = "https://heyzine.com/flip-book/5ed696c717.html#page/1"
IMPACT_EMBED = "https://heyzine.com/flip-book/5ed696c717.html"
MENCIONES_ID = "1-1WrQYKHlLJjEo2LxpB4wvuJF1AK_56E"
MENCIONES_VER = f"https://drive.google.com/file/d/{MENCIONES_ID}/view?usp=drive_link"
MENCIONES_EMBED = f"https://drive.google.com/file/d/{MENCIONES_ID}/preview"
FABLAB_NETWORK = "https://www.fablabs.io/"
FABLAB_PERFIL = "https://fablabs.io/labs/fabjardin"

# --------------------------------------------------------------------------
# Menú: (etiqueta, enlace, [(subetiqueta, enlace)])
# --------------------------------------------------------------------------
NAV = [
    ("Nosotros", "nosotros.html", [
        ("Quiénes somos", "nosotros.html"), ("Impacto", "nosotros.html#impacto"), ("Red FabLab y aliados", "nosotros.html#red")]),
    ("Laboratorio", "laboratorio.html", [
        ("Servicios y tecnologías", "laboratorio.html#servicios"), ("Para qué sirve cada equipo", "laboratorio.html#equipamiento")]),
    ("Innovación y emprendimiento", "innovacion-y-emprendimiento.html", [
        ("Para quien quiera y lo necesite", "innovacion-y-emprendimiento.html#para-quien"), ("Servicios", "innovacion-y-emprendimiento.html#servicios")]),
    ("Educación", "educacion.html", [
        ("Talleres y cursos", "educacion.html#talleres"), ("Instituciones", "educacion.html#instituciones")]),
    ("Comunidad", "comunidad.html", [
        ("Eventos y agenda", "comunidad.html#agenda"), ("Proyectos", "comunidad.html#proyectos"), ("Noticias", "comunidad.html#noticias")]),
]
NAV_CTA = ("Cotiza tu proyecto", "contacto.html")

# --------------------------------------------------------------------------
# Servicios de fabricación: (nombre, foto, qué hace, qué se puede hacer)
# --------------------------------------------------------------------------
SERVICES = [
    ("Corte láser CO2", "corte-laser-co2.webp", "Para cortar y grabar madera, acrílico, cartón, cuero, papel y textiles.",
     "Desde maquetas arquitectónicas y cajas personalizadas hasta grabado en cuero y joyería en acrílico."),
    ("Grabado láser UV", "grabado-laser-uv.webp", "Para grabar metales desnudos y materiales delicados.",
     "Personalizar joyería, marcar códigos, logos o QRs en herramientas y piezas industriales, grabar cristalería, cerámica y componentes electrónicos."),
    ("Prensas de calor", "prensas-de-calor.webp", "Sublimación o vinil textil sobre diversos materiales, con presión y temperatura exactas.",
     "Desde estampar playeras y bolsas, aplicar vinil textil en ropa deportiva, hasta personalizar artículos como tazas, termos y mousepads."),
    ("Impresión 3D de filamento", "impresion-3d-filamento.webp", "Para materializar volúmenes y geometrías complejas con plásticos de uso hobby y técnico.",
     "Prototipos rápidos, piezas de repuesto, figuras artísticas, maquetas y piezas funcionales."),
    ("Impresión 3D de resina", "impresion-3d-resina.webp", "Para materializar volúmenes y geometrías complejas con altísima resolución.",
     "Piezas con detalles finos, como miniaturas, joyería o modelismo."),
    ("Router CNC", "router-cnc.webp", "Para cortar tableros completos de madera, MDF, OSB, aluminio o plásticos de ingeniería.",
     "Mobiliario (sillas, mesas, estanterías), stands para ferias, estructuras paramétricas y moldes grandes."),
    ("Corte de vinil", "corte-de-vinil.webp", "Para cortar vinil adhesivo, vinil textil, cobre adhesivo o dibujar con bolígrafo en gran formato.",
     "Stickers, rotulación de ventanas, vinil textil para estampar camisetas (heat transfer) y circuitos flexibles de cobre."),
    ("Circuitos", "circuitos.webp", "Para complementar proyectos que integren iluminación, electricidad o electrónica.",
     "Desde iluminar un logo y construir letreros neón hasta darle movimiento con motores a una base de pastel o a una maqueta."),
    ("Escáner 3D", "escaner-3d.webp", "Para capturar y digitalizar objetos reales y convertirlos en un archivo digital editable.",
     "Desde crear el plano de una pieza rota o antigua para hacer un repuesto, hasta digitalizar artesanías o partes del cuerpo para personalización médica."),
    ("Asesoría y diseño", "asesoria-y-diseno.webp", "Más que máquinas: revisamos contigo tu proyecto y te sugerimos el mejor camino.",
     "Prototipado, servicio de modelado 3D y CAD, servicios de vectorización y consultoría para desarrollo de producto."),
]
SERVICE_OPTIONS = [s[0] for s in SERVICES] + [
    "Innovación y emprendimiento", "Educación / talleres", "Otro / no estoy seguro",
]

# Hoja de la portada: (máquina, trabaja con, sirve para)
HOJA = [
    ("Corte láser CO2", "Madera, acrílico, cartón, cuero, papel y textiles", "Maquetas, cajas personalizadas, grabado en cuero y joyería en acrílico"),
    ("Grabado láser UV", "Metales desnudos, cristalería, cerámica y componentes electrónicos", "Joyería personalizada, códigos QR y logos en herramientas y piezas industriales"),
    ("Prensas de calor", "Playeras, bolsas, tazas, termos y mousepads", "Sublimación y vinil textil con presión y temperatura exactas"),
    ("Impresión 3D de filamento", "Plásticos de uso hobby y técnico", "Prototipos, repuestos, figuras, maquetas y piezas funcionales"),
    ("Impresión 3D de resina", "Resina de alta resolución", "Miniaturas, joyería, modelismo y piezas con detalle fino"),
    ("Router CNC", "Madera, MDF, OSB, aluminio y plásticos de ingeniería", "Mobiliario, stands para ferias, estructuras paramétricas y moldes"),
    ("Corte de vinil", "Vinil adhesivo, vinil textil y cobre adhesivo", "Stickers, rotulación de ventanas, camisetas y circuitos flexibles"),
    ("Circuitos", "Iluminación, motores y electrónica", "Letreros neón, logos iluminados y maquetas con movimiento"),
    ("Escáner 3D", "Objetos reales", "Planos de piezas rotas, digitalizar artesanías y personalización médica"),
    ("Asesoría y diseño", "Tu idea o tus archivos", "Modelado 3D y CAD, vectorización y consultoría de producto"),
]

EJES = [
    ("Laboratorio", "laboratorio.html", "Fabricación digital y uso del taller, con la maquinaria lista para usar."),
    ("Innovación y emprendimiento", "innovacion-y-emprendimiento.html", "Orientación, asesoría, formación y comunidad para despegar tu idea o proyecto, sea del tamaño que sea."),
    ("Educación", "educacion.html", "Talleres, formaciones intensivas y programas para escuelas, empresas y nuestra comunidad."),
    ("Comunidad", "comunidad.html", "Eventos, proyectos y personas con las que creamos en conjunto."),
]

DIFERENCIALES = [
    ("Innovación InHouse", "Máquinas y procesos en un solo lugar, listo para usar."),
    ("Certificación global", "Operamos bajo los estándares de la FabLab Network."),
    ("Agilidad radical", "De la idea al producto, sin mínimos de producción."),
    ("Hiper-personalización", "Fabricación de piezas únicas que la industria masiva no puede atender."),
    ("Socios de la innovación", "Know-how técnico y acompañamiento en diseño y metodologías."),
]
FAB_MIT = "https://fab.cba.mit.edu/"
MANIFIESTO = [
    "Haz solo una pieza, o las que necesites.",
    "Todo lo que necesitas para fabricar, en un solo lugar.",
    ("Parte de una red mundial de laboratorios de fabricación.", FAB_MIT, "Conoce la red"),
    "Te acompañamos desde el 0, hasta el 1.",
]
# Equipamiento por área: (área, qué cubre, [nombres de máquinas de HOJA])
EQUIPO = [
    ("Corte y grabado láser", "Dos tecnologías láser: una para cortar y grabar materiales orgánicos, otra para marcar metales y materiales delicados.", ["Corte láser CO2", "Grabado láser UV"]),
    ("Impresión 3D", "Filamento para piezas funcionales y resina para alta resolución.", ["Impresión 3D de filamento", "Impresión 3D de resina"]),
    ("Router CNC", "Corte de tableros completos y de formatos grandes.", ["Router CNC"]),
    ("Textil y personalización", "Sublimación, vinil textil, stickers y rotulación.", ["Prensas de calor", "Corte de vinil"]),
    ("Electrónica", "Iluminación, circuitos y movimiento con motores para tus prototipos.", ["Circuitos"]),
    ("Escaneo y diseño 3D", "Pasar de lo real a lo digital y viceversa: escáner, modelado CAD y vectorización.", ["Escáner 3D", "Asesoría y diseño"]),
]


# --------------------------------------------------------------------------
# Piezas de HTML
# --------------------------------------------------------------------------
TONOS = {  # color de acento por página (paleta en css/styles.css)
    "index": "lima", "nosotros": "azul", "laboratorio": "lima", "innovacion-y-emprendimiento": "cian",
    "educacion": "sol", "comunidad": "lila", "contacto": "lima",
}


def hay(ruta):
    return os.path.exists(os.path.join(ROOT, ruta))


def foto(ruta, alt="", clase=""):
    """<img> si el archivo existe; si no, cadena vacía (queda el color de la paleta)."""
    if not hay(ruta):
        return ""
    c = f' class="{clase}"' if clase else ""
    return f'<img{c} src="{ruta}" alt="{escape(alt)}" loading="lazy" decoding="async">'


def rebanadas():
    """Mini columnas con imágenes recortadas; al pasar el cursor una se abre completa (images/educacion/*.webp)."""
    d = os.path.join(ROOT, "images", "educacion")
    fotos = sorted(f for f in os.listdir(d) if f.endswith(".webp"))[:6] if os.path.isdir(d) else []
    colores = ["sol", "coral", "lima", "cian", "lila", "azul"]
    if fotos:
        cols = "".join(f'<figure class="reb" tabindex="0"><img src="images/educacion/{f}" alt="Actividad en Fabjardin" loading="eager" decoding="async"></figure>' for f in fotos)
    else:
        cols = "".join(f'<figure class="reb t-{c}" tabindex="0"></figure>' for c in colores[:4])
    return f'<div class="rebanadas">{cols}</div>'


def mosaico(slug):
    """Tres formas de color a la derecha del encabezado; aceptan fotos images/hero/<pagina>-1..3.webp."""
    base = slug.replace(".html", "")
    if base == "educacion":
        return rebanadas()
    formas = "".join(f'<span class="m{i}">{foto(f"images/hero/{base}-{i}.webp")}</span>' for i in (1, 2, 3))
    return f'<div class="mosaico" aria-hidden="true">{formas}</div>'


FLECHA = ('<svg class="flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
          'stroke-linecap="square" aria-hidden="true"><path d="M3 12h17M13 5l7 7-7 7"/></svg>')


def cot(servicio=""):
    return "contacto.html" + (f"?servicio={servicio.replace(' ', '%20')}" if servicio else "")


def cabecera(actual):
    items = []
    for label, href, kids in NAV:
        cur = ' aria-current="page"' if href.split("#")[0] == actual else ""
        subs = "".join(f'<a href="{h}">{escape(l)}</a>' for l, h in kids)
        items.append(f'<li class="tiene-sub"><a class="enlace" href="{href}"{cur}>{escape(label)}</a><div class="sub">{subs}</div></li>')
    cl, ch = NAV_CTA
    return f"""<header class="cabecera">
  <div class="contenedor">
    <a class="marca-logo" href="index.html" aria-label="{NAME}, inicio"><img src="images/logo-blanco.png" alt="{NAME} · {TAGLINE}" width="681" height="181"></a>
    <nav class="nav" id="menu-principal" aria-label="Principal">
      <ul>{''.join(items)}</ul>
      <span class="reloj" id="reloj" aria-hidden="true">Chalco</span>
      <a class="boton boton--lima" href="{ch}">{escape(cl)}</a>
    </nav>
    <button class="boton-menu" aria-expanded="false" aria-controls="menu-principal">Menú</button>
  </div>
</header>"""


MAPA = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3766.314326419251!2d-98.89386162547895!3d19.268692381975946!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x85ce1fd58ad5ab77%3A0xfa9b490e87970e4a!2sFABJardin!5e0!3m2!1ses!2ses!4v1793065188727!5m2!1ses!2ses"

WA_ICONO = '<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.4 4 15.03c0 2.12.55 4.19 1.6 6.01L4 29l8.12-1.57a12 12 0 0 0 3.92.66C22.68 28.1 28 22.7 28 16.07 28 9.4 22.7 3 16.04 3zm0 22.04c-1.2 0-2.38-.32-3.4-.93l-.24-.15-4.82.93.97-4.7-.16-.25a9.9 9.9 0 0 1-1.52-5.3c0-5.5 4.47-9.97 9.98-9.97 5.5 0 9.97 4.47 9.97 9.97 0 5.5-4.47 10.4-9.78 10.4zm5.47-7.46c-.3-.15-1.77-.87-2.04-.97-.28-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.41-1.5-.9-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.7.3 1.26.48 1.69.62.7.22 1.35.19 1.86.12.57-.08 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35z"/></svg>'


def pie():
    c = CONTACT
    cols = "".join(f'<li><a href="{h}">{escape(l)}</a></li>' for l, h, _ in NAV)
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie-grid">
      <div>
        <img src="images/logo-blanco.png" alt="{NAME} · {TAGLINE}" width="681" height="181">
        <p>Empoderando a la comunidad local a través de la fabricación digital, la educación, la innovación y el emprendimiento.</p>
      </div>
      <div><h3>Explora</h3><ul><li><a href="index.html">Inicio</a></li>{cols}</ul></div>
      <div><h3>Servicios</h3><ul>
        <li><a href="laboratorio.html#servicios">Fabricación digital</a></li>
        <li><a href="innovacion-y-emprendimiento.html">Innovación y emprendimiento</a></li>
        <li><a href="contacto.html">Solicitar cotización</a></li>
      </ul></div>
      <div><h3>Contacto</h3><ul>
        <li><a href="mailto:{c['email']}">{c['email']}</a></li>
        <li><a href="{c['wa']}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp al {c['tel_label']}">{c['tel_label']} · WhatsApp</a></li>
        <li><a href="{c['maps']}" target="_blank" rel="noopener">{escape(c['address'])}</a></li>
      </ul></div>
      <div class="pie-mapa"><iframe src="{MAPA}" title="Mapa de ubicación de Fabjardin" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
    </div>
    <div class="legal">
      <span>© <span id="anio">2026</span> {NAME.upper()}. Todos los derechos reservados.</span>
      <nav aria-label="Legal"><a href="politica-de-privacidad.html">Políticas de privacidad</a><a href="terminos-de-los-servicios.html">Términos de los servicios</a></nav>
    </div>
  </div>
</footer>"""


def pagina(slug, titulo, desc, cuerpo, noindex=False):
    full = f"{NAME} · {TAGLINE}" if slug == "index.html" else f"{titulo} · {NAME}"
    url = f"{SITE_URL}/" + ("" if slug == "index.html" else slug)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#001c72">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(full)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/images/og-fabjardin.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preload" href="fonts/display-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/body-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/styles.css">
</head>
<body data-tono="{TONOS.get(slug.replace(".html", ""), "lima")}">
<a class="saltar" href="#contenido">Saltar al contenido</a>
{cabecera(slug)}
<main id="contenido">
{cuerpo.replace("<!--MOSAICO-->", mosaico(slug))}
</main>
{pie()}
<a class="wa-flotante" href="{CONTACT["wa"]}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{WA_ICONO}<span>WhatsApp</span></a>
<script src="js/config.js"></script>
<script src="js/main.js"></script>
</body>
</html>
"""


def panal_svg(color="#001c72", op=".10"):
    """Panal de la cama de corte láser como mosaico sin costuras."""
    r = 20.0
    w, h = math.sqrt(3) * r, 3 * r

    def hexa(cx, cy):
        pts = [(cx + r * math.cos(math.radians(-90 + 60 * k)), cy + r * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
        return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
    d = " ".join([hexa(w / 2, r), hexa(0, r + 1.5 * r), hexa(w, r + 1.5 * r)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.3f} {h:.1f}" width="{w:.3f}" height="{h:.1f}">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1"/></svg>')


def hero_int(titulo, entrada, migas, lineal=False, html=False, extra=""):
    trail = '<a href="index.html">Inicio</a>' + "".join(f" / {m}" for m in migas)
    return f"""<section class="hero-int{" hero-int--lineal" if lineal else ""}{" hero-int--frase" if html else ""}">
  <div class="contenedor">
    <div class="texto-hero">
      <div class="migas">{trail}</div>
      {titulo if html else f"<h1>{escape(titulo)}</h1>"}
      {entrada if html else (f'<p class="entrada">{escape(entrada)}</p>' if entrada else "")}
    </div>
    {"" if lineal else "<!--MOSAICO-->"}
  </div>
</section>"""


def bloque(fondo, contenido, ident=""):
    i = f' id="{ident}"' if ident else ""
    return f'<section class="bloque bloque--{fondo}"{i}><div class="contenedor">{contenido}</div></section>'


def cabeza(titulo, texto="", sola=False):
    p = f"<p>{escape(texto)}</p>" if texto else ""
    clase = " cabeza--sola" if (sola or not texto) else ""
    return f'<div class="cabeza{clase}"><h2>{escape(titulo)}</h2>{p}</div>'


def filas(items):
    return '<div class="filas">' + "".join(f'<div class="fila"><span class="num">{i:02d}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for i, (t, d) in enumerate(items, 1)) + "</div>"


def pasos(items):
    return '<ol class="pasos">' + "".join(f"<li><h3>{escape(t)}</h3><p>{escape(d)}</p></li>" for t, d in items) + "</ol>"


def puntos(items):
    return '<ul class="puntos">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def panel(titulo, texto, etiqueta, href):
    return (f'<aside class="panel"><h3>{escape(titulo)}</h3><p>{escape(texto)}</p>'
            f'<a class="boton boton--claro" href="{href}">{escape(etiqueta)}</a></aside>')


def llamado(titulo="¿Tienes una idea o un proyecto?", texto="Cuéntanos qué necesitas y te respondemos con la mejor solución.",
            etiqueta="Solicita tu cotización", href="contacto.html"):
    return f"""<section class="llamado"><div class="contenedor"><div class="caja">
  <div><h2>{escape(titulo)}</h2>{"<p>"+escape(texto)+"</p>" if texto else ""}</div>
  <a class="boton boton--lima" href="{href}"{' target="_blank" rel="noopener"' if href.startswith("http") else ""}>{escape(etiqueta)}</a>
</div></div></section>"""


def visores():
    """Informe de actividades (flipbook interactivo) y documento de menciones, ambos incrustados."""
    return f"""<div class="visores">
  <article class="visor">
    <h3>Informe de actividades</h3>
    <div class="marco"><iframe src="{IMPACT_EMBED}" title="Informe de actividades de Fabjardin" loading="lazy" allowfullscreen allow="fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
    <a class="boton boton--lima boton--chico" href="{IMPACT_REPORT}" target="_blank" rel="noopener">Abrir en pantalla completa</a>
  </article>
  <article class="visor">
    <h3>Informes, artículos y publicaciones donde nos mencionan</h3>
    <div class="marco"><iframe src="{MENCIONES_EMBED}" title="Informes, artículos y publicaciones donde nos hacen mención" loading="lazy" allow="fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
    <a class="boton boton--lima boton--chico" href="{MENCIONES_VER}" target="_blank" rel="noopener">Abrir el documento</a>
  </article>
</div>"""


def impacto_frase():
    cifras = [(2200, "Proyectos"), (150, "Emprendedores"), (15, "Formaciones"), (20, "Colaboraciones con instituciones")]
    items = "".join(f'<li><b data-meta="{n}">+{n:,}</b><span>{escape(t)}</span></li>' for n, t in cifras)
    return f'<ul class="impacto-num" aria-label="Nuestro impacto en cifras">{items}</ul>'


# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------
PAGES = {}


def page(slug, titulo, desc, cuerpo, noindex=False):
    PAGES[slug] = (titulo, desc, cuerpo, noindex)


def tile(archivo, forma, etiqueta, color, pos="50% 50%"):
    img = foto(f"images/servicios/{archivo}.webp", etiqueta)
    if img:
        img = img.replace("<img", f'<img style="object-position:{pos}"', 1).replace('loading="lazy"', 'loading="eager"')
    return f'<div class="tile {forma} t-{color}"><span class="et">{escape(etiqueta)}</span>{img}</div>'


def marca_tile(paths, animada):
    ident = ' id="pieza"' if animada else ""
    rayo = '<circle id="rayo" class="rayo" r="7" cx="256" cy="256"/>' if animada else ""
    return (f'<div class="tile circulo t-lima t-marca"><svg viewBox="0 0 512 512"><path{ident} class="pieza" fill-rule="evenodd" d="{paths}"/>{rayo}</svg></div>')


COLUMNA_A = [("corte-laser-co2", "rect", "Corte láser", "cian", "50% 60%"), ("impresion-3d-resina", "circulo", "Resina 3D", "coral", "50% 40%"),
             ("router-cnc", "rect", "Router CNC", "sol", "50% 30%"), ("prensas-de-calor", "circulo", "Prensas de calor", "lila", "45% 50%"),
             ("asesoria-y-diseno", "rect", "Asesoría y diseño", "azul", "50% 50%")]
COLUMNA_B = [("escaner-3d", "rect", "Escáner 3D", "lila", "40% 50%"), ("impresion-3d-filamento", "circulo", "Impresión 3D", "sol", "45% 55%"),
             ("circuitos", "rect", "Circuitos", "coral", "55% 50%"), ("grabado-laser-uv", "circulo", "Grabado UV", "cian", "50% 60%"),
             ("corte-de-vinil", "rect", "Corte de vinil", "azul", "50% 50%")]


def columna(items, marca=None):
    return "".join(tile(*t) for t in items) if marca is None else marca + "".join(tile(*t) for t in items)



# --------------------------------------------------------------------------
# Asistente interactivo de la portada: ¿qué necesitas y podemos hacerlo?
# --------------------------------------------------------------------------
def _maq(nombre):
    t, u = next((t, u) for m, t, u in HOJA if m == nombre)
    return {"m": nombre, "con": t, "para": u, "cot": cot(nombre)}


def _fab(titulo, texto, maquinas):
    return {"res": {"si": "Sí, lo hacemos aquí", "titulo": titulo, "texto": texto, "items": [_maq(m) for m in maquinas],
                    "ctas": [{"l": "Cotizar mi proyecto", "h": cot(maquinas[0])}, {"l": "Hablar por WhatsApp", "h": "wa"}]}}


def _ruta(titulo, texto, ver, href, cotiza):
    return {"res": {"si": "Te ayudamos con esto", "titulo": titulo, "texto": texto, "items": [],
                    "ctas": [{"l": ver, "h": href}, {"l": "Pedir información", "h": cot(cotiza)}]}}


GUIA = {
    "q": "¿Qué quieres lograr?",
    "o": [
        {"t": "Fabricar algo", "d": "Una pieza, un producto o un regalo", "n": {
            "q": "¿Qué quieres hacer?",
            "o": [
                {"t": "Cortar o grabar madera, acrílico, cuero, cartón o papel", **_fab("Corte láser CO2", "Ideal para maquetas, cajas personalizadas, letreros y grabados.", ["Corte láser CO2"])},
                {"t": "Marcar metal, vidrio, cerámica o piezas industriales", **_fab("Grabado láser UV", "Para grabar metales desnudos y materiales delicados.", ["Grabado láser UV"])},
                {"t": "Estampar playeras, bolsas, tazas o termos", **_fab("Prensas de calor y corte de vinil", "Sublimación y vinil textil con presión y temperatura exactas.", ["Prensas de calor", "Corte de vinil"])},
                {"t": "Hacer stickers, rótulos o letreros de vinil", **_fab("Corte de vinil", "Para cortar vinil adhesivo, vinil textil y cobre adhesivo.", ["Corte de vinil"])},
                {"t": "Imprimir una pieza en 3D", **_fab("Impresión 3D", "Filamento para piezas funcionales y resina cuando necesitas detalle fino.", ["Impresión 3D de filamento", "Impresión 3D de resina"])},
                {"t": "Cortar muebles, tableros o piezas grandes", **_fab("Router CNC", "Para tableros completos y formatos grandes.", ["Router CNC"])},
                {"t": "Hacer algo con luces, motores o electrónica", **_fab("Circuitos", "Para integrar iluminación, electricidad o electrónica a tu proyecto.", ["Circuitos"])},
                {"t": "Copiar o digitalizar una pieza que ya existe", **_fab("Escáner 3D", "Captura el objeto real y lo convierte en un archivo digital editable.", ["Escáner 3D"])},
                {"t": "Tengo la idea, pero no sé cómo hacerla", **_fab("Asesoría y diseño", "Revisamos contigo tu proyecto y te sugerimos el mejor camino.", ["Asesoría y diseño"])},
            ]}},
        {"t": "Aprender haciendo", "d": "Talleres y capacitaciones intensivas", **_ruta("Educación en el taller", "Talleres, formaciones intensivas y programas para escuelas, empresas y nuestra comunidad.", "Ver talleres y programas", "educacion.html", "Educación / talleres")},
        {"t": "Impulsar mi idea o proyecto", "d": "Orientación para despegar, aunque no sepas por dónde", **_ruta("Impulsa tu proyecto", "Te ayudamos a despegar tu idea o proyecto, por sencillo que sea: orientación, asesoría, formación y comunidad.", "Ver cómo te acompañamos", "innovacion-y-emprendimiento.html", "Innovación y emprendimiento")},
        {"t": "Aún no lo sé", "d": "Cuéntanos y te orientamos", "res": {"si": "Platiquemos", "titulo": "Cuéntanos en qué andas", "texto": "Describe tu idea y te decimos si podemos hacerla y con qué.", "items": [],
            "ctas": [{"l": "Escríbenos", "h": "contacto.html"}, {"l": "Hablar por WhatsApp", "h": "wa"}]}},
    ],
}


def guia():
    datos = json.dumps(GUIA, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section class="guia" id="asistente">
  <div class="contenedor"><div class="caja">
    <div class="guia-cab">
      <p class="sello">Asistente</p>
      <h2>¿Qué necesitas? Te decimos si podemos hacerlo, y con qué.</h2>
    </div>
    <div class="guia-app" id="guia-app" aria-live="polite">
      <noscript><p>Cuéntanos en qué andas desde la <a href="contacto.html">página de contacto</a>.</p></noscript>
    </div>
    <script type="application/json" id="guia-datos">{datos}</script>
  </div></div>
</section>"""


def home():
    paths = open(os.path.join(ROOT, "tools", "marca_paths.txt"), encoding="utf-8").read().replace("\n", " ")
    ejes = "".join(
        f'<a class="eje" href="{h}"><span class="n">{i:02d}</span>{foto("images/ejes/" + h.replace(".html", "") + ".webp", n, "eje-foto")}'
        f'<span class="nombre">{n}</span><p class="detalle">{escape(d)}</p><span class="ir">{FLECHA}</span></a>'
        for i, (n, h, d) in enumerate(EJES, 1))
    col_a = '<div class="grupo">' + columna(COLUMNA_A) + "</div>"
    col_b = '<div class="grupo">' + columna(COLUMNA_B, marca_tile(paths, True)) + "</div>"
    col_b2 = '<div class="grupo">' + columna(COLUMNA_B, marca_tile(paths, False)) + "</div>"
    manif = "".join(
        f"<p>{escape(t)}</p>" if isinstance(t, str) else
        f'<p>{escape(t[0])} <a class="mas" href="{t[1]}" target="_blank" rel="noopener">{escape(t[2])} {FLECHA}</a></p>'
        for t in MANIFIESTO)
    return f"""
<section class="hero">
  <div class="contenedor">
    <div class="hero-texto">
      <h1><span>Facilitamos y centralizamos la fabricación de tus proyectos,</span> <span class="acento">en un solo lugar.</span></h1>
      <p class="hero-p">Fabrica con nosotros, aprende en el taller o convierte tu idea en un negocio. Somos un centro de innovación y tecnologías creativas en Chalco.</p>
      <div class="fila-botones">
        <a class="boton boton--lima" href="contacto.html">Cuéntanos en qué andas</a>
        <a class="boton boton--borde-claro" href="laboratorio.html#equipamiento">Ver máquinas y materiales</a>
      </div>
    </div>
    <div class="collage" aria-hidden="true">
      <div class="col col-a"><div class="pista">{col_a}{col_a}</div></div>
      <div class="col col-b"><div class="pista">{col_b}{col_b2}</div></div>
    </div>
  </div>
</section>

<section class="ejes">
  <div class="contenedor">
    <h2>Un solo centro. Cuatro maneras de entrar.</h2>
    <div class="lista-ejes">{ejes}</div>
  </div>
</section>

{guia()}

<section class="manifiesto"><div class="contenedor">{manif}</div></section>

"""


page("index.html", TAGLINE,
     "Fabjardin es un centro de innovación y tecnologías creativas en Chalco: fabricación digital, innovación, emprendimiento y formación.",
     home())

# ---- Nosotros ----
PALABRAS_CENTRO = ["centro", "nodo", "hub", "punto", "espacio", "núcleo", "laboratorio", "ecosistema", "taller", "jardín"]
NOSOTROS_H1 = (
    '<h1 aria-label="Somos un centro donde creamos comunidad mediante proyectos creativos, tecnológicos, educativos y de emprendimiento.">'
    '<span class="ln1" aria-hidden="true">Somos un <span class="flash" data-palabras="' + ",".join(PALABRAS_CENTRO) + '">centro</span></span>'
    '<span class="ln2" aria-hidden="true">donde creamos comunidad mediante proyectos creativos, tecnológicos, educativos y de emprendimiento.</span></h1>')
NOSOTROS_TXT = (
    '<div class="entrada entrada--prosa">'
    '<p>Nacemos para ser un motor de transformación comunitaria y movilidad social, que usa la tecnología como herramienta para cerrar brechas.</p>'
    '<p>Nuestro propósito es empoderar a nuestra región mediante la innovación técnica, convirtiendo el conocimiento científico y de vanguardia en un bien público que impulsa:</p>'
    '<ul class="metas"><li>el progreso colectivo</li><li>la soberanía tecnológica</li><li>el desarrollo sostenible desde la base social</li></ul></div>')

ICONOS_DIF = [  # uno por diferencial, en el mismo orden
    '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
    '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    '<path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3M14 2v4M8 10v4M16 18v4"/>',
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
]


def diferenciales():
    out = "".join(
        f'<div class="dif"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONOS_DIF[i]}</svg></span>'
        f'<h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for i, (t, d) in enumerate(DIFERENCIALES))
    return f'<div class="difs">{out}</div>'


ALIADOS = [  # (archivo, nombre) en images/aliados/
    ("codecu", "CODECU Atlazalpan, Centro Multidisciplinario"), ("diet", "DIET, Dirección de Incubación de Empresas Tecnológicas"),
    ("ipn", "Instituto Politécnico Nacional"), ("tuvch", "Tecnológico Universitario del Valle de Chalco"),
    ("cecytem", "CECYTEM, Colegio de Estudios Científicos y Tecnológicos del Estado de México"), ("tecnm", "Tecnológico Nacional de México"),
    ("ime", "Instituto Mexiquense del Emprendedor"), ("posible", "POSIBLE"),
]


def aliados():
    def pista(oculta):
        a = ' aria-hidden="true"' if oculta else ""
        return "".join(f'<li{a}><img src="images/aliados/{f}.svg" alt="{"" if oculta else escape(n)}" height="72" decoding="async"></li>' for f, n in ALIADOS)
    return (f'<section class="aliados" id="aliados" aria-label="Nuestros aliados"><div class="contenedor"><h2>Nuestros aliados</h2></div>'
            f'<div class="ali-carril"><ul class="ali-pista">{pista(False)}{pista(True)}</ul></div></section>')


page("nosotros.html", "Nosotros",
     "Conoce a Fabjardin: misión, visión, impacto y nuestra pertenencia a la red global FabLab.",
     hero_int(NOSOTROS_H1, NOSOTROS_TXT, ["Nosotros"], lineal=True, html=True)
     + bloque("papel", cabeza("Misión y visión") + filas([
         ("Nuestra misión", "Empoderar a la comunidad facilitando el acceso a la fabricación digital y tecnologías de vanguardia, para transformar ideas en proyectos de alto impacto educativo, social y económico."),
         ("Visión", "Ser el nodo de referencia regional en innovación y creatividad, donde la colaboración y la tecnología se unen para impulsar el desarrollo sostenible y transformar el futuro de nuestras comunidades."),
     ]), "quienes-somos")
     + bloque("hoja", cabeza("Lo que nos hace diferentes") + diferenciales())
     + f'<section class="resultados" id="impacto"><div class="contenedor">{impacto_frase()}{visores()}</div></section>'
     + bloque("papel", f'''<div class="cabeza cabeza--sola cabeza--ancha"><h2>¿Qué es un FabLab?</h2>
  <p>Un FabLab (laboratorio de fabricación) es un espacio comunitario con herramientas de fabricación digital, como cortadoras láser, impresoras 3D, fresadoras CNC y electrónica, abierto para que cualquier persona aprenda y fabrique casi cualquier cosa. Nació a principios de los 2000 en el Center for Bits and Atoms del MIT y hoy es una red de más de 2,500 laboratorios en unos 125 países. Fabjardín forma parte de esa red y opera bajo sus estándares.</p></div>
  <div class="fila-botones"><a class="boton boton--lleno" href="{FABLAB_PERFIL}" target="_blank" rel="noopener">Fabjardín en la red FabLab</a>
  <a class="boton boton--borde" href="{FAB_MIT}" target="_blank" rel="noopener">Conoce la red</a></div>
  <p class="fuente">Fuente: <a href="https://news.mit.edu/2023/how-mits-fab-labs-scaled-around-world-0605" target="_blank" rel="noopener">MIT News, 2023</a></p>''', "red")
     + bloque("hoja", cabeza("Su impacto en la sociedad") + filas([
         ("Acceso para todas las personas", "Pone herramientas de fabricación digital al alcance de la comunidad, como una biblioteca de herramientas, sin necesidad de comprar maquinaria cara."),
         ("Educación que se aprende haciendo", "Del curso del MIT “How To Make (almost) Anything” nació la Fab Academy: formación práctica en la que se aprende fabricando."),
         ("Producción local", "Permite fabricar cerca de donde se necesita. Iniciativas como Fab City impulsan ciudades que producen lo que consumen."),
         ("Comunidad y oportunidades", "Fortalece capacidades locales, apoya a quienes emprenden y conecta a las personas con conocimiento y proyectos de todo el mundo."),
     ]), "impacto-social")
     + aliados()
     + llamado("¿Quieres trabajar en conjunto?", "", "Escríbenos", "contacto.html"))


# ---- Laboratorio ----
def equipamiento():
    """Lista de nombres; al pasar el cursor (o tocar) se muestra el detalle de cada equipo."""
    largo = {n: l for n, _, _, l in SERVICES}  # el detalle de cada servicio vive aquí
    datos = {m: (t, largo.get(m, u)) for m, t, u in HOJA}
    nombres = [n for n, _, _, _ in SERVICES]  # mismo orden y numeración que la matriz de servicios
    out = []
    for i, m in enumerate(nombres, 1):
        t, u = datos[m]
        out.append(
            f'<div class="eq"><button type="button" class="eq-b" id="eq-b{i}" aria-expanded="false" aria-controls="eq-p{i}">'
            f'<span class="num">{i:02d}</span><span class="eq-n">{escape(m)}</span>'
            f'<svg class="eq-f" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>'
            f'<div class="eq-p" id="eq-p{i}" role="region" aria-labelledby="eq-b{i}"><div class="eq-d"><h3>{escape(m)}</h3><dl>'
            f'<div><dt>Trabaja con</dt><dd>{escape(t)}</dd></div>'
            f'<div><dt>Sirve para</dt><dd>{escape(u)}</dd></div></dl>'
            f'</div></div></div>')
    return f'<div class="equipos" id="equipos" style="--n:{len(nombres)}">' + "".join(out) + "</div>"


def servicios_lab():
    out = []
    for i, (nombre, archivo, corto, largo) in enumerate(SERVICES, 1):
        img = foto(f"images/servicios/{archivo}", nombre)
        clase = "servicio con-foto" if img else "servicio"
        out.append(f'<article class="{clase}"><div class="visual"><span class="n">{i:02d}</span>{img}</div>'
                   f'<div class="cuerpo"><h3>{escape(nombre)}</h3><p class="corto">{escape(corto)}</p>'
                   f'</div></article>')
    return '<div class="lista-servicios">' + "".join(out) + "</div>"


page("laboratorio.html", "Laboratorio de fabricación digital",
     "Servicios de fabricación digital en Chalco: corte láser, grabado UV, impresión 3D, router CNC, vinil, circuitos, escáner 3D y uso del espacio.",
     hero_int("Fabricación y herramientas digitales, en un solo lugar", "", ["Laboratorio"], lineal=True)
     + bloque("papel", cabeza("Servicios y tecnologías") + servicios_lab(), "servicios")
     + bloque("hoja", cabeza("Para qué sirve cada equipo") + equipamiento(), "equipamiento")
     + llamado("¿Aún no sabes por dónde iniciar? Conéctate con el equipo", "", "Escribir por WhatsApp", CONTACT["wa"]))

# ---- Innovación ----
# ---- Innovación y emprendimiento (una sola sección) ----
def _svg(path):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{path}</svg>')


ICONOS_SERV = [
    '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',   # orientación
    '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',  # asesoría
    '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',   # formación
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',  # comunidad
]
SERV_IE = [
    ("Orientación inicial", "Una primera conversación para entender tu idea, aunque hoy no sepas por dónde empezar.",
     ["Conocemos tu idea o proyecto", "Te decimos qué sigue y por dónde empezar"], None),
    ("Asesoría y mentoría", "Acompañamiento para aterrizar tu idea y hacerla avanzar paso a paso.",
     ["Definir qué problema resuelve tu idea y para quién", "Pruebas y mejoras con lo que vas aprendiendo", "Seguimiento con el equipo"], None),
    ("Formación", "Aprende haciendo, con talleres y formaciones intensivas.",
     ["Talleres y cursos prácticos", "Formaciones intensivas", "Pensamiento de diseño, creatividad, innovación y emprendimiento"], ("Ver talleres y cursos", "educacion.html#talleres")),
    ("Comunidad y colaboración", "Emprender es más fácil en compañía: conoce a otras personas que están creando.",
     ["Encuentros y jornadas abiertas", "Colaboraciones con instituciones que abren puertas a tu proyecto"], ("Conocer la comunidad", "comunidad.html")),
]


def servicios_ie():
    out = ""
    for n, (t, d, items, link) in enumerate(SERV_IE, 1):
        li = "".join(f"<li>{escape(x)}</li>" for x in items)
        a = f'<a class="pil-link" href="{link[1]}">{escape(link[0])} {FLECHA}</a>' if link else ""
        out += (f'<article class="pil"><div class="pil-top"><span class="pil-n">{n:02d}</span><span class="ico">{_svg(ICONOS_SERV[n-1])}</span></div>'
                f'<h3>{escape(t)}</h3><p>{escape(d)}</p><ul class="pil-list">{li}</ul>{a}</article>')
    return f'<div class="pilares">{out}</div>'


def cifras_ie():
    cifras = [(150, "Emprendedores acompañados"), (20, "Colaboraciones con instituciones"), (15, "Formaciones")]
    items = "".join(f'<li><b data-meta="{n}">+{n:,}</b><span>{escape(t)}</span></li>' for n, t in cifras)
    return f'<ul class="impacto-num impacto-num--3" aria-label="Resultados">{items}</ul>'


PARA_TODOS = "Si tienes una idea, un proyecto o simplemente ganas de crear algo, aquí hay un lugar para ti. Es para quien quiera y lo necesite: sin importar tu edad, tu experiencia ni el tamaño de tu idea."

page("innovacion-y-emprendimiento.html", "Innovación y emprendimiento",
     "Te ayudamos a despegar: orientación, asesoría, formación y comunidad para quienes quieren innovar o emprender en la región.",
     hero_int("Te ayudamos a despegar",
              "Somos el punto de apoyo para quienes quieren innovar o emprender en la región: personas con una idea, negocios que empiezan, jóvenes e instituciones.",
              ["Innovación y emprendimiento"], lineal=True)
     + bloque("papel", cabeza("Para quien quiera y lo necesite", PARA_TODOS, sola=True), "para-quien")
     + bloque("hoja", cabeza("Servicios") + servicios_ie(), "servicios")
     + f'<section class="resultados" id="resultados"><div class="contenedor">{cifras_ie()}</div></section>'
     + llamado("¿Tienes una idea y no sabes por dónde empezar?", "", "Cuéntanos tu idea", cot("Innovación y emprendimiento")))

# ---- Educación ----
TEMAS = ["Diseño 3D y CAD", "Corte y grabado láser", "Impresión 3D", "Electrónica creativa", "Vectorización y diseño gráfico", "Personalización textil",
         "Innovación", "Pensamiento de diseño", "Creatividad", "Emprendimiento"]
page("educacion.html", "Educación",
     "Talleres prácticos, bootcamps y programas para escuelas y jóvenes sobre nuevas tecnologías y diseño.",
     hero_int("Aprende haciendo",
              "Un ecosistema donde generamos experiencias educativas prácticas sobre nuevas tecnologías creativas.",
              ["Educación"])
     + bloque("papel", f'''<div class="cabeza cabeza--sola cabeza--ancha"><h2>Talleres y cursos</h2>
  <p>Fórmate con nuestras actividades de educación. Si eres una persona curiosa, emprendedora o docente, o simplemente quieres aprender algo nuevo, aquí encuentras talleres y cursos prácticos en los que aprendes haciendo.</p></div>'''
              + '<ul class="temas" id="temas">' + "".join(f"<li>{escape(t)}</li>" for t in TEMAS)
              + '<li class="otro"><form id="form-tema" autocomplete="off"><label class="visually-hidden" for="tema-nuevo">Escribe otro tema que quieras aprender</label>'
                '<input id="tema-nuevo" type="text" maxlength="40" placeholder="¿Otro tema? Escríbelo y da Enter"><button type="submit" aria-label="Grabar tema">↵</button></form></li></ul>', "talleres")
     + bloque("hoja", f'''<div class="cabeza cabeza--sola cabeza--ancha"><h2>Instituciones</h2><div class="cabeza-txt"><p class="steam-p">Implementamos educación <span class="steam" tabindex="0" aria-label="STEAM: Ciencia, Tecnología, Ingeniería, Artes y Matemáticas"><b>STEAM</b><span class="def" role="tooltip"><i><b>S</b>Ciencia</i><i><b>T</b>Tecnología</i><i><b>E</b>Ingeniería</i><i><b>A</b>Artes</i><i><b>M</b>Matemáticas</i></span></span> llevando a escuelas, organizaciones, instituciones y comunidad en general, programas y productos con los que impartimos talleres y cursos para inspirar a niños, jóvenes y adultos a fabricar el futuro.</p></div></div>''' + filas([
         ("Programas educativos", "Contenidos prácticos adaptados a cada nivel y objetivo de aprendizaje."),
         ("Visitas de grupos y escuelas", "Recorridos y actividades en el taller para grupos escolares y comunitarios."),
         ("Proyectos con impacto", "Aprender resolviendo retos reales de la comunidad."),
         ("Consultoría", "Formación y consultoría para la escuela y el profesorado en el ámbito STEAM."),
         ("Aulas", "Puesta en marcha de espacios de innovación y educación basados en nuevas tecnologías."),
     ]), "instituciones")
     + llamado("Capacita a tu equipo o a tu grupo", "", "Solicitar información", cot("Educación / talleres")))

# ---- Comunidad ----
page("comunidad.html", "Comunidad",
     "Eventos, proyectos y noticias de la comunidad Fabjardin.",
     hero_int("Crear es mejor en comunidad",
              "Eventos, proyectos y personas que se encuentran en Fabjardin para aprender, fabricar y colaborar.",
              ["Comunidad"])
     + bloque("papel", f"""<div class="dividido">
  <h2>Eventos y agenda</h2><div class="der">
    <p class="texto-largo">Talleres, jornadas abiertas y encuentros con la comunidad. Pronto publicaremos aquí el calendario.</p>
    <div class="fila-botones"><a class="boton boton--lleno" href="contacto.html">Quiero enterarme</a></div>{panel("Próximamente", "Escríbenos y te avisamos de las próximas actividades abiertas al público.", "Escríbenos", "contacto.html")}</div></div>""", "agenda")
     + bloque("hoja", cabeza("Proyectos", "Más de 2,200 proyectos finalizados, desde maquetas y prototipos hasta productos de emprendedores. Conoce lo que hemos hecho en nuestro informe de actividades.")
              + f'<div class="fila-botones"><a class="boton boton--lleno" href="{IMPACT_REPORT}" target="_blank" rel="noopener">Ver informe de actividades</a></div>', "proyectos")
     + bloque("papel", cabeza("Noticias", "Estamos preparando esta sección con novedades, convocatorias y casos de la comunidad."), "noticias")
     + llamado("Sé parte de la comunidad", "Colabora, aprende o fabrica con nosotros.", "Contáctanos"))

# ---- Contacto ----
opciones = "".join(f'<option value="{escape(o)}">{escape(o)}</option>' for o in SERVICE_OPTIONS)
c = CONTACT
page("contacto.html", "Contacto y cotización",
     "Describe tu idea o proyecto y recibe una cotización de Fabjardin. Escríbenos por correo, teléfono o WhatsApp.",
     hero_int("Solicita tu cotización",
              "Describe tu idea, comparte tus archivos y nuestro equipo técnico analizará la viabilidad para darte la mejor solución.",
              ["Contacto"])
     + bloque("papel", f"""<div class="contacto-grid">
  <div class="formulario">
    <form id="form-cotizacion" novalidate>
      <div class="campos">
        <div class="campo"><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" type="text" autocomplete="name" required></div>
        <div class="campo"><label for="email">Email de contacto</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="campo"><label for="telefono">Teléfono (opcional)</label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div>
        <div class="campo"><label for="servicio">Servicio requerido</label><select id="servicio" name="servicio" required>{opciones}</select></div>
        <div class="campo ancho"><label for="urgencia">Urgencia</label>
          <select id="urgencia" name="urgencia"><option>Normal (3-5 días)</option><option>Prioritario (24-48h)</option><option>Sin prisa</option></select></div>
        <div class="campo ancho"><label for="descripcion">Descripción del proyecto</label><textarea id="descripcion" name="descripcion" required placeholder="Qué quieres fabricar, materiales, medidas, cantidad…"></textarea></div>
        <div class="campo ancho"><label for="archivos">Enlace a tus archivos (DXF, STL, PDF…)</label><input id="archivos" name="archivos" type="url" placeholder="https://drive.google.com/…">
          <span class="ayuda">Sube tus archivos a Google Drive, Dropbox o similar y pega aquí el enlace, con permiso de lectura.</span></div>
        <div class="trampa" aria-hidden="true"><label>No llenar<input name="_gotcha" type="text" tabindex="-1" autocomplete="off"></label></div>
      </div>
      <div class="fila-botones" style="margin-top:1.4rem"><button class="boton boton--lleno" type="submit">Enviar solicitud</button></div>
      <div id="form-estado" class="estado" role="status" aria-live="polite"></div>
    </form>
  </div>
  <aside class="panel">
    <h3>Hablemos</h3>
    <p>También puedes escribirnos directamente. Respondemos a la brevedad.</p>
    <ul class="datos">
      <li><small>Correo</small><a href="mailto:{c['email']}">{c['email']}</a></li>
      <li><small>Teléfono</small><a href="tel:{c['tel_href']}">{c['tel_label']}</a></li>
      <li><small>WhatsApp</small><a id="btn-whatsapp" href="https://wa.me/525576571685" target="_blank" rel="noopener">Escríbenos por WhatsApp</a></li>
      <li><small>Ubicación</small><a href="{c['maps']}" target="_blank" rel="noopener">{escape(c['address'])}</a></li>
    </ul>
  </aside>
</div>"""))

# ---- Legales (borradores) ----
BORRADOR = '<div class="borrador">Borrador: este texto es una plantilla general y debe ser revisado y completado por la persona responsable, idealmente con asesoría legal, antes de la publicación definitiva.</div>'
page("politica-de-privacidad.html", "Políticas de privacidad", "Aviso de privacidad de Fabjardin.",
     hero_int("Políticas de privacidad", "Cómo tratamos tus datos personales.", ["Políticas de privacidad"])
     + bloque("papel", f"""<div class="prosa">{BORRADOR}
<h2>Responsable del tratamiento</h2><p>Fabjardin, con domicilio en {escape(c['address'])}, es responsable del tratamiento de los datos personales que nos proporciones.</p>
<h2>Datos que recabamos</h2><p>Nombre, correo electrónico, teléfono (opcional) y la información del proyecto que compartas mediante el formulario de contacto o por otros medios.</p>
<h2>Finalidades</h2><p>Atender tus solicitudes de cotización, dar seguimiento a tus proyectos y contactarte sobre nuestros servicios, talleres y actividades.</p>
<h2>Derechos ARCO</h2><p>Puedes ejercer tus derechos de acceso, rectificación, cancelación y oposición escribiendo a <a href="mailto:{c['email']}">{c['email']}</a>.</p>
<h2>Cambios al aviso</h2><p>Cualquier modificación se publicará en esta misma página.</p></div>"""), noindex=True)
page("terminos-de-los-servicios.html", "Términos de los servicios", "Términos de los servicios de Fabjardin.",
     hero_int("Términos de los servicios", "Condiciones generales para el uso de nuestros servicios.", ["Términos de los servicios"])
     + bloque("papel", f"""<div class="prosa">{BORRADOR}
<h2>Cotizaciones</h2><p>Las cotizaciones se elaboran a partir de la información y los archivos que proporciones. Los precios y tiempos pueden cambiar si cambian las especificaciones del proyecto.</p>
<h2>Archivos y propiedad intelectual</h2><p>Al enviarnos archivos o diseños declaras tener derecho a usarlos. Los derechos sobre tus diseños siguen siendo tuyos.</p>
<h2>Uso de las instalaciones</h2><p>El uso del espacio y la maquinaria está sujeto a las reglas de seguridad y de operación que te indique el equipo de Fabjardin.</p>
<h2>Contacto</h2><p>Para cualquier duda escríbenos a <a href="mailto:{c['email']}">{c['email']}</a>.</p></div>"""), noindex=True)


# --------------------------------------------------------------------------
def write(path, contenido):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(contenido)


def main():
    for slug, (titulo, desc, cuerpo, noindex) in PAGES.items():
        write(slug, pagina(slug, titulo, desc, cuerpo, noindex))
    write("404.html", pagina(
        "404.html", "Página no encontrada", "La página que buscas no existe.",
        hero_int("No encontramos esa página", "Puede que el enlace haya cambiado.", ["Error 404"])
        + bloque("papel", '<div class="fila-botones"><a class="boton boton--lleno" href="index.html">Volver al inicio</a></div>'), noindex=True))
    write("formacion.html", f"""<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><title>Educación · {NAME}</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}/educacion.html">
<meta http-equiv="refresh" content="0; url=educacion.html"></head>
<body><p>Esta página ahora es <a href="educacion.html">Educación</a>.</p>
<script>location.replace("educacion.html" + location.search + location.hash);</script></body></html>
""")
    for viejo, nombre in (("innovacion.html", "Innovación y emprendimiento"), ("emprendimiento.html", "Innovación y emprendimiento")):
        write(viejo, f"""<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><title>{nombre} · {NAME}</title>
<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}/innovacion-y-emprendimiento.html">
<meta http-equiv="refresh" content="0; url=innovacion-y-emprendimiento.html"></head>
<body><p>Esta página ahora es <a href="innovacion-y-emprendimiento.html">{nombre}</a>.</p>
<script>location.replace("innovacion-y-emprendimiento.html" + location.search + location.hash);</script></body></html>
""")
    write("images/panal.svg", panal_svg())
    write("images/panal-claro.svg", panal_svg("#ffffff", ".08"))

    urls = [s for s, p in PAGES.items() if not p[3]]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s in urls:
        sm.append(f"  <url><loc>{SITE_URL}/{'' if s == 'index.html' else s}</loc></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"OK: {len(PAGES) + 1} páginas generadas")


if __name__ == "__main__":
    main()
