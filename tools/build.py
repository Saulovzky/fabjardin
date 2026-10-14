#!/usr/bin/env python3
"""
Genera todas las páginas de Fabjardin.

Uso:  python3 tools/build.py

Aquí viven el menú (NAV), los datos de contacto, los servicios y el texto de
cada página. Después de editar algo, vuelve a ejecutarlo y sube los .html
resultantes. Las fotos de servicios se detectan solas: si existe
images/servicios/<archivo>.webp, aparece en la página de Laboratorio.
"""
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
    "address": "C. 5 de Febrero No. 23, Col. La Bomba, C.P. 56600, Chalco de Díaz Covarrubias, Estado de México",
    "maps": "https://www.google.com/maps/search/?api=1&query=C.+5+de+Febrero+23+La+Bomba+Chalco+de+D%C3%ADaz+Covarrubias",
}
IMPACT_REPORT = "https://heyzine.com/flip-book/5ed696c717.html#page/1"
FABLAB_NETWORK = "https://www.fablabs.io/"

# --------------------------------------------------------------------------
# Menú: (etiqueta, enlace, [(subetiqueta, enlace)])
# --------------------------------------------------------------------------
NAV = [
    ("Nosotros", "nosotros.html", [
        ("Quiénes somos", "nosotros.html"), ("Impacto", "nosotros.html#impacto"), ("Red FabLab y aliados", "nosotros.html#red")]),
    ("Laboratorio", "laboratorio.html", [
        ("Servicios de fabricación", "laboratorio.html#servicios"), ("Equipamiento y tecnologías", "laboratorio.html#equipamiento"), ("Usa el espacio", "laboratorio.html#usa-el-espacio")]),
    ("Innovación", "innovacion.html", [
        ("I+D para empresas e instituciones", "innovacion.html"), ("Prototipado y producto", "innovacion.html#prototipado"), ("Asesoría y diseño", "innovacion.html#asesoria")]),
    ("Emprendimiento", "emprendimiento.html", [
        ("Acompañamiento", "emprendimiento.html"), ("De la idea al producto", "emprendimiento.html#ruta"), ("Mentorías y red", "emprendimiento.html#red")]),
    ("Formación", "formacion.html", [
        ("Talleres y cursos", "formacion.html"), ("BootCamps", "formacion.html#bootcamps"), ("Escuelas y jóvenes", "formacion.html#escuelas")]),
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
    "Usar el espacio (membresía / acceso)", "Innovación / I+D", "Emprendimiento", "Formación / talleres", "Otro / no estoy seguro",
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
    ("Innovación", "innovacion.html", "I+D, prototipado y desarrollo de producto para empresas e instituciones."),
    ("Emprendimiento", "emprendimiento.html", "Acompañamiento para convertir una idea en un proyecto real."),
    ("Formación", "formacion.html", "Talleres, bootcamps y programas para escuelas y jóvenes."),
    ("Comunidad", "comunidad.html", "Eventos, proyectos y personas que crean en conjunto."),
]

DIFERENCIALES = [
    ("Innovación InHouse", "Máquinas y procesos en un solo lugar, listo para usar."),
    ("Certificación global", "Operamos bajo los estándares de la FabLab Network."),
    ("Agilidad radical", "De la idea al producto, sin mínimos de producción."),
    ("Hiper-personalización", "Fabricación de piezas únicas que la industria masiva no puede atender."),
    ("Socios de la innovación", "Know-how técnico y acompañamiento en diseño y metodologías."),
]
MANIFIESTO = [
    "Sin mínimos de producción.",
    "Máquinas y procesos bajo el mismo techo.",
    "Piezas únicas que la industria masiva no atiende.",
    "Estándares de la FabLab Network.",
    "Acompañamiento técnico de la idea al objeto.",
]
EQUIPO = [
    ("Corte y grabado láser", "Láser CO2 para madera, acrílico, cuero, cartón, papel y textiles, y láser UV para metales y materiales delicados."),
    ("Impresión 3D", "Impresión en filamento para piezas funcionales y en resina para alta resolución."),
    ("Router CNC", "Corte de tableros completos de madera, MDF, OSB, aluminio y plásticos de ingeniería."),
    ("Textil y personalización", "Prensas de calor y corte de vinil para sublimación, vinil textil, stickers y rotulación."),
    ("Electrónica", "Iluminación, circuitos, letreros neón y movimiento con motores para tus prototipos."),
    ("Escaneo y diseño 3D", "Escáner 3D, modelado CAD y vectorización para pasar de lo real a lo digital y viceversa."),
]


# --------------------------------------------------------------------------
# Piezas de HTML
# --------------------------------------------------------------------------
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
    <a class="marca-logo" href="index.html" aria-label="{NAME}, inicio"><img src="images/logo.png" alt="{NAME} · {TAGLINE}" width="681" height="181"></a>
    <nav class="nav" id="menu-principal" aria-label="Principal">
      <ul>{''.join(items)}</ul>
      <span class="reloj" id="reloj" aria-hidden="true">Chalco</span>
      <a class="boton boton--lleno" href="{ch}">{escape(cl)}</a>
    </nav>
    <button class="boton-menu" aria-expanded="false" aria-controls="menu-principal">Menú</button>
  </div>
</header>"""


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
        <li><a href="laboratorio.html#usa-el-espacio">Usa el espacio</a></li>
        <li><a href="innovacion.html">Innovación e I+D</a></li>
        <li><a href="contacto.html">Solicitar cotización</a></li>
      </ul></div>
      <div><h3>Contacto</h3><ul>
        <li><a href="mailto:{c['email']}">{c['email']}</a></li>
        <li><a href="tel:{c['tel_href']}">{c['tel_label']}</a></li>
        <li><a href="{c['maps']}" target="_blank" rel="noopener">{escape(c['address'])}</a></li>
      </ul></div>
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
<meta name="theme-color" content="#f1f3fa">
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
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{cabecera(slug)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
<script src="js/config.js"></script>
<script src="js/main.js"></script>
</body>
</html>
"""


def panal_svg():
    """Panal de la cama de corte láser como mosaico sin costuras."""
    r = 20.0
    w, h = math.sqrt(3) * r, 3 * r

    def hexa(cx, cy):
        pts = [(cx + r * math.cos(math.radians(-90 + 60 * k)), cy + r * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
        return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
    d = " ".join([hexa(w / 2, r), hexa(0, r + 1.5 * r), hexa(w, r + 1.5 * r)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.3f} {h:.1f}" width="{w:.3f}" height="{h:.1f}">'
            f'<path d="{d}" fill="none" stroke="#001c72" stroke-opacity=".10" stroke-width="1"/></svg>')


def hero_int(titulo, entrada, migas):
    trail = '<a href="index.html">Inicio</a>' + "".join(f" / {m}" for m in migas)
    return f"""<section class="hero-int">
  <div class="contenedor">
    <div class="migas">{trail}</div>
    <h1>{escape(titulo)}</h1>
    <p class="entrada">{escape(entrada)}</p>
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
    return '<div class="filas">' + "".join(f'<div class="fila"><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for t, d in items) + "</div>"


def pasos(items):
    return '<ol class="pasos">' + "".join(f"<li><h3>{escape(t)}</h3><p>{escape(d)}</p></li>" for t, d in items) + "</ol>"


def puntos(items):
    return '<ul class="puntos">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def panel(titulo, texto, etiqueta, href):
    return (f'<aside class="panel"><h3>{escape(titulo)}</h3><p>{escape(texto)}</p>'
            f'<a class="boton boton--claro" href="{href}">{escape(etiqueta)}</a></aside>')


def llamado(titulo="¿Tienes una idea o un proyecto?", texto="Cuéntanos qué necesitas y te respondemos con la mejor solución.",
            etiqueta="Solicita tu cotización", href="contacto.html"):
    return f"""<section class="llamado"><div class="contenedor">
  <div><h2>{escape(titulo)}</h2><p>{escape(texto)}</p></div>
  <a class="boton boton--claro" href="{href}">{escape(etiqueta)}</a>
</div></section>"""


def impacto_frase():
    return f"""<p class="frase">Desde Chalco hemos terminado más de <b>2,200 proyectos</b>, acompañado a más de <b>150 emprendedores</b>, dado más de <b>15 bootcamps</b> y construido más de <b>20 colaboraciones</b> con instituciones.</p>
    <a href="{IMPACT_REPORT}" target="_blank" rel="noopener">Ver el informe de actividades</a>"""


# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------
PAGES = {}


def page(slug, titulo, desc, cuerpo, noindex=False):
    PAGES[slug] = (titulo, desc, cuerpo, noindex)


def home():
    paths = open(os.path.join(ROOT, "tools", "marca_paths.txt"), encoding="utf-8").read().replace("\n", " ")
    ejes = "".join(f'<a class="eje" href="{h}"><span class="nombre">{n}</span><p class="detalle">{escape(d)}</p>{FLECHA}</a>' for n, h, d in EJES)
    filas_t = "".join(
        f'<tr><td>{escape(m)}</td><td>{escape(t)}</td><td>{escape(s)}</td><td><a class="cotizar" href="{cot(m)}">Cotizar</a></td></tr>'
        for m, t, s in HOJA)
    manif = "".join(f"<p>{escape(t)}</p>" for t in MANIFIESTO)
    return f"""
<section class="hero">
  <div class="contenedor">
    <h1><span>Del archivo</span><span>al objeto.</span></h1>
    <div class="marca-corte" aria-hidden="true">
      <svg viewBox="0 0 512 512"><path id="pieza" class="pieza" fill-rule="evenodd" d="{paths}"/><circle id="rayo" class="rayo" r="7" cx="256" cy="256"/></svg>
    </div>
    <div class="pie-hero">
      <p>Fabrica con nosotros, aprende en el taller o convierte tu idea en un negocio. Somos un centro de innovación y tecnologías creativas en Chalco.</p>
      <div class="fila-botones">
        <a class="boton boton--lleno" href="contacto.html">Cotiza tu proyecto</a>
        <a class="boton boton--borde" href="#maquinas">Ver máquinas y materiales</a>
      </div>
    </div>
  </div>
</section>

<section class="ejes">
  <div class="contenedor">
    <h2>Un solo centro. Cinco maneras de entrar.</h2>
    <div class="lista-ejes">{ejes}</div>
  </div>
</section>

<section class="especificaciones" id="maquinas">
  <div class="contenedor">
    {cabeza("Qué máquina para qué material", "Elige por material o cuéntanos tu proyecto y te decimos cuál conviene. Trabajamos con tus archivos o los diseñamos contigo.")}
    <table class="tabla">
      <thead><tr><th scope="col">Máquina</th><th scope="col">Trabaja con</th><th scope="col">Sirve para</th><th scope="col"><span class="visually-hidden">Acción</span></th></tr></thead>
      <tbody>{filas_t}</tbody>
    </table>
  </div>
</section>

<section class="manifiesto"><div class="contenedor">{manif}</div></section>

<section class="resultados"><div class="contenedor">{impacto_frase()}</div></section>

<section class="final">
  <div class="contenedor">
    <h2>Trae tu archivo o trae tu idea.</h2>
    <div class="sub-final">
      <p>Te respondemos con la viabilidad, los tiempos y el costo. Estamos en La Bomba, Chalco de Díaz Covarrubias, Estado de México.</p>
      <div class="fila-botones">
        <a class="boton boton--lleno" href="contacto.html">Solicitar cotización</a>
        <a class="boton boton--borde" href="{CONTACT['maps']}" target="_blank" rel="noopener">Cómo llegar</a>
      </div>
    </div>
  </div>
</section>
"""


page("index.html", TAGLINE,
     "Fabjardin es un centro de innovación y tecnologías creativas en Chalco: fabricación digital, innovación, emprendimiento y formación.",
     home())

# ---- Nosotros ----
page("nosotros.html", "Nosotros",
     "Conoce a Fabjardin: misión, visión, impacto y nuestra pertenencia a la red global FabLab.",
     hero_int("Un centro que conecta tecnología, creatividad y comunidad",
              "Somos un centro de fabricación digital parte de la red global FabLab, donde diseñamos y convertimos ideas en proyectos fabricables y tangibles para toda la comunidad.",
              ["Nosotros"])
     + bloque("papel", cabeza("Misión y visión") + filas([
         ("Nuestra misión", "Empoderar a la comunidad facilitando el acceso a la fabricación digital y tecnologías de vanguardia, para transformar ideas en proyectos de alto impacto educativo, social y económico."),
         ("Visión", "Ser el nodo de referencia regional en innovación y creatividad, donde la colaboración y la tecnología se unen para impulsar el desarrollo sostenible y transformar el futuro de nuestras comunidades."),
     ]), "quienes-somos")
     + bloque("hoja", cabeza("Lo que nos hace diferentes") + filas(DIFERENCIALES))
     + f'<section class="resultados" id="impacto"><div class="contenedor">{impacto_frase()}</div></section>'
     + bloque("papel", f"""<div class="dividido">
  <div><h2>Parte de una red global de laboratorios</h2>
    <p class="texto-largo">Formamos parte de la red global <a href="{FABLAB_NETWORK}" target="_blank" rel="noopener">FabLab Network</a> y operamos bajo sus estándares, lo que nos conecta con conocimiento, proyectos y personas de todo el mundo.</p>
    {puntos(["Colaboraciones con instituciones, empresas y organizaciones", "Intercambio de buenas prácticas con otros laboratorios", "Proyectos con impacto educativo, social y económico"])}
  </div>
  {panel("¿Quieres colaborar con nosotros?", "Si representas a una institución, empresa u organización y quieres construir algo en conjunto, escríbenos.", "Contáctanos", "contacto.html")}
</div>""", "red"))


# ---- Laboratorio ----
def servicios_lab():
    out = []
    for nombre, foto, corto, largo in SERVICES:
        existe = os.path.exists(os.path.join(ROOT, "images", "servicios", foto))
        img = f'<img src="images/servicios/{foto}" alt="{escape(nombre)}" loading="lazy" width="180" height="135">' if existe else ""
        clase = "servicio con-foto" if existe else "servicio"
        out.append(f'<div class="{clase}">{img}<div><h3>{escape(nombre)}</h3><p class="corto">{escape(corto)}</p></div>'
                   f'<p class="largo">{escape(largo)}</p><a class="cotizar" href="{cot(nombre)}">Cotizar</a></div>')
    return '<div class="lista-servicios">' + "".join(out) + "</div>"


page("laboratorio.html", "Laboratorio de fabricación digital",
     "Servicios de fabricación digital en Chalco: corte láser, grabado UV, impresión 3D, router CNC, vinil, circuitos, escáner 3D y uso del espacio.",
     hero_int("Fabricación digital, en un solo lugar",
              "Cuéntanos tu idea, envíanos tus archivos o diseños, y los transformamos en objetos que podrás tener en tus manos.",
              ["Laboratorio"])
     + bloque("papel", cabeza("Servicios de fabricación", "Transformamos archivos digitales en objetos físicos con precisión. Elige un servicio o cuéntanos tu proyecto y te orientamos.") + servicios_lab(), "servicios")
     + bloque("hoja", cabeza("Equipamiento y tecnologías", "Herramientas y maquinaria agrupadas por área, listas para tus prototipos, maquetas y producciones.") + filas(EQUIPO), "equipamiento")
     + bloque("papel", f"""<div class="dividido">
  <div><h2>Fabrica tú, sin comprar herramientas caras</h2>
    <p class="texto-largo">Te ofrecemos un espacio con acceso flexible a nuestras instalaciones, equipadas con herramientas y maquinaria, para sacar adelante tus maquetas, trabajos, prototipos o proyectos.</p>
    {puntos(["Acceso flexible a las instalaciones", "Herramientas y maquinaria listas para usar", "Orientación del equipo técnico cuando la necesites"])}
  </div>
  {panel("¿Quieres usar el espacio?", "Cuéntanos qué vas a hacer y te decimos cómo acceder.", "Quiero usar el espacio", cot("Usar el espacio (membresía / acceso)"))}
</div>""", "usa-el-espacio")
     + llamado())

# ---- Innovación ----
page("innovacion.html", "Innovación e I+D",
     "Tu equipo externo de investigación y desarrollo: soluciones a medida, prototipado y desarrollo de producto para empresas, instituciones y emprendedores.",
     hero_int("Tu equipo externo de investigación y desarrollo",
              "Echamos una mano a empresas, instituciones, emprendedores y a la comunidad con soluciones a medida, desde pensar y dinamizar ideas hasta crear prototipos y productos finales.",
              ["Innovación"])
     + bloque("papel", cabeza("I+D para empresas e instituciones", "Combinamos metodologías ágiles, de diseño y de fabricación con la capacidad de producir en casa.") + filas([
         ("Dinamización de ideas", "Sesiones para pensar, explorar y priorizar retos y oportunidades de producto o proceso."),
         ("Diseño a medida", "Soluciones diseñadas para tu necesidad, con acompañamiento técnico en cada decisión."),
         ("Fabricación en casa", "Máquinas y procesos en un solo lugar para pasar de la propuesta al objeto físico sin intermediarios."),
     ]), "id-empresas")
     + bloque("hoja", f"""<div class="dividido">
  <div><h2>De la idea al prototipo funcional</h2>
    <p class="texto-largo">Iteramos contigo hasta tener un prototipo que puedas probar, mostrar y mejorar, sin mínimos de producción.</p>
    {puntos(["Prototipos rápidos y piezas funcionales", "Piezas únicas e hiper-personalizadas", "Pruebas y mejoras en ciclos cortos"])}
  </div>
  {panel("¿Tienes un reto de producto?", "Cuéntanos qué quieres lograr y te proponemos cómo abordarlo.", "Hablemos", cot("Innovación / I+D"))}
</div>""", "prototipado")
     + bloque("papel", cabeza("Asesoría y diseño", "Más que máquinas: revisamos contigo tu proyecto y sugerimos el mejor camino.") + filas([
         ("Modelado 3D y CAD", "Convertimos tus ideas o piezas físicas en modelos listos para fabricar."),
         ("Vectorización", "Preparamos tus gráficos para corte, grabado y vinil."),
         ("Prototipado", "Primeras versiones físicas para validar forma, tamaño y función."),
         ("Consultoría de producto", "Acompañamiento para desarrollar tu producto de punta a punta."),
     ]), "asesoria")
     + llamado("Construyamos la solución juntos", "Platícanos tu reto y armamos una propuesta a tu medida.", "Contáctanos"))

# ---- Emprendimiento ----
page("emprendimiento.html", "Emprendimiento",
     "Acompañamiento para transformar una idea en un proyecto real, desde el inicio hasta la fabricación de tus productos.",
     hero_int("Emprende con tus propios productos",
              "Te acompañamos para transformar una idea en un proyecto real: te guiamos desde el inicio hasta la fabricación.",
              ["Emprendimiento"])
     + bloque("papel", f"""<div class="dividido">
  <div><h2>Un ecosistema para quien quiere crear algo propio</h2>
    <p class="texto-largo">Más de 150 emprendedores han pasado por Fabjardin. Aquí encuentras tecnología, método y personas que te ayudan a avanzar.</p>
    {puntos(["Orientación técnica y de diseño desde la primera idea", "Fabricación de tus prototipos y primeras producciones", "Producción sin mínimos, ideal para validar antes de invertir"])}
  </div>
  {panel("+150 emprendedores beneficiados", "Si tienes una idea de producto, platícanos en qué etapa estás y te decimos cómo podemos ayudarte.", "Quiero emprender", cot("Emprendimiento"))}
</div>""", "acompanamiento")
     + bloque("hoja", cabeza("De la idea al producto", "Nuestra ruta, en cinco pasos.") + pasos([
         ("Idea", "Aterrizamos tu concepto y definimos qué problema resuelve."),
         ("Diseño", "Modelamos y preparamos los archivos para fabricar."),
         ("Prototipo", "Fabricamos una primera versión física para probarla."),
         ("Mejora", "Iteramos con lo aprendido hasta llegar a la versión final."),
         ("Producción", "Fabricamos tus piezas, desde unidades únicas hasta series cortas."),
     ]), "ruta")
     + bloque("papel", cabeza("Mentorías y red", "Fabjardin es un punto de encuentro entre emprendedores, empresas, instituciones y comunidad.") + filas([
         ("Comunidad", "Conoce a otras personas que están creando y fabricando."),
         ("Colaboraciones", "Más de 20 colaboraciones institucionales abren puertas para tus proyectos."),
         ("Formación", "Talleres y bootcamps para fortalecer tus habilidades técnicas y de diseño."),
     ]), "red")
     + llamado("Cuéntanos tu idea", "Te ayudamos a dar el primer paso.", "Hablemos de tu proyecto", cot("Emprendimiento")))

# ---- Formación ----
TEMAS = ["Diseño 3D y CAD", "Corte y grabado láser", "Impresión 3D", "Electrónica creativa", "Vectorización y diseño gráfico", "Personalización textil"]
page("formacion.html", "Formación",
     "Talleres prácticos, bootcamps y programas para escuelas y jóvenes sobre nuevas tecnologías y diseño.",
     hero_int("Aprende haciendo, con las máquinas del taller",
              "Un ecosistema donde impartimos talleres prácticos sobre nuevas tecnologías y diseño.",
              ["Formación"])
     + bloque("papel", cabeza("Talleres y cursos", "Aprendes usando las mismas máquinas con las que fabricamos proyectos reales.")
              + '<ul class="temas">' + "".join(f"<li>{escape(t)}</li>" for t in TEMAS) + "</ul>"
              + f'<p style="margin-top:1.6rem">¿Quieres saber cuándo es el próximo taller? <a href="{cot("Formación / talleres")}">Escríbenos</a> y te avisamos.</p>', "talleres")
     + bloque("tinta", f"""<div class="dividido">
  <div><h2>Capacitaciones intensivas</h2>
    <p class="texto-largo">Más de 15 bootcamps y capacitaciones realizados. Programas intensivos para adquirir habilidades concretas en poco tiempo.</p></div>
  {panel("+15 bootcamps", "Capacitaciones impartidas en Fabjardin.", "Pide información", cot("Formación / talleres"))}
</div>""", "bootcamps")
     + bloque("papel", cabeza("Escuelas y jóvenes", "Diseñamos experiencias educativas para que niñas, niños y jóvenes entiendan cómo funcionan las cosas y se atrevan a crearlas.") + filas([
         ("Programas educativos", "Contenidos prácticos adaptados a cada nivel y objetivo de aprendizaje."),
         ("Visitas de grupos y escuelas", "Recorridos y actividades en el taller para grupos escolares y comunitarios."),
         ("Proyectos con impacto", "Aprender resolviendo retos reales de la comunidad."),
     ]), "escuelas")
     + llamado("Capacita a tu equipo o a tu grupo", "Cuéntanos qué quieres aprender y armamos el programa.", "Solicitar información", cot("Formación / talleres")))

# ---- Comunidad ----
page("comunidad.html", "Comunidad",
     "Eventos, proyectos y noticias de la comunidad Fabjardin.",
     hero_int("Crear es mejor en comunidad",
              "Eventos, proyectos y personas que se encuentran en Fabjardin para aprender, fabricar y colaborar.",
              ["Comunidad"])
     + bloque("papel", f"""<div class="dividido">
  <div><h2>Eventos y agenda</h2>
    <p class="texto-largo">Talleres, jornadas abiertas y encuentros con la comunidad. Pronto publicaremos aquí el calendario.</p>
    <div class="fila-botones"><a class="boton boton--lleno" href="contacto.html">Quiero enterarme</a></div></div>
  {panel("Próximamente", "Escríbenos y te avisamos de las próximas actividades abiertas al público.", "Escríbenos", "contacto.html")}
</div>""", "agenda")
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
    write("images/panal.svg", panal_svg())

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
