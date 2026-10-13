#!/usr/bin/env python3
"""
Genera las páginas HTML de Fabjardin a partir de un solo archivo.

Uso:  python3 tools/build.py
Edita aquí el menú (NAV), los servicios (SERVICES) o el texto de cada página
y vuelve a ejecutarlo. Los .html resultantes se suben tal cual a GitHub Pages.
"""
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
# Menú de navegación: (etiqueta, enlace, descripción corta)
# --------------------------------------------------------------------------
NAV = [
    ("Nosotros", "nosotros.html", [
        ("Quiénes somos", "nosotros.html", "Misión, visión y lo que nos hace diferentes"),
        ("Impacto", "nosotros.html#impacto", "Cifras e informe de actividades"),
        ("Red FabLab y aliados", "nosotros.html#red", "Parte de la red global FabLab"),
    ]),
    ("Laboratorio", "laboratorio.html", [
        ("Servicios de fabricación", "laboratorio.html#servicios", "Corte, grabado, impresión 3D, CNC y más"),
        ("Equipamiento y tecnologías", "laboratorio.html#equipamiento", "Lo que hay en el taller"),
        ("Usa el espacio", "laboratorio.html#usa-el-espacio", "Fabrica tú, sin comprar maquinaria"),
    ]),
    ("Innovación", "innovacion.html", [
        ("I+D para empresas e instituciones", "innovacion.html", "Tu equipo externo de investigación"),
        ("Prototipado y producto", "innovacion.html#prototipado", "De la idea al prototipo funcional"),
        ("Asesoría y diseño", "innovacion.html#asesoria", "CAD, modelado 3D y vectorización"),
    ]),
    ("Emprendimiento", "emprendimiento.html", [
        ("Acompañamiento", "emprendimiento.html", "Te guiamos desde la idea"),
        ("De la idea al producto", "emprendimiento.html#ruta", "Nuestra ruta en cinco pasos"),
        ("Mentorías y red", "emprendimiento.html#red", "Conecta con otros emprendedores"),
    ]),
    ("Formación", "formacion.html", [
        ("Talleres y cursos", "formacion.html", "Práctica con tecnologías creativas"),
        ("BootCamps", "formacion.html#bootcamps", "Capacitaciones intensivas"),
        ("Escuelas y jóvenes", "formacion.html#escuelas", "Programas educativos y visitas"),
    ]),
    ("Comunidad", "comunidad.html", [
        ("Eventos y agenda", "comunidad.html#agenda", "Lo que viene en Fabjardin"),
        ("Proyectos", "comunidad.html#proyectos", "Lo que hemos fabricado juntos"),
        ("Noticias", "comunidad.html#noticias", "Entérate de lo nuevo"),
    ]),
]
NAV_CTA = ("Cotiza tu proyecto", "contacto.html")

# --------------------------------------------------------------------------
# Servicios de fabricación (icono de Material Symbols + imagen opcional)
# Las imágenes se esperan en images/servicios/<archivo>. Si no existe, se
# muestra el ícono.
# --------------------------------------------------------------------------
SERVICES = [
    dict(icon="content_cut", img="corte-laser-co2.webp", title="Corte láser CO2",
         short="Para cortar y grabar madera, acrílico, cartón, cuero, papel y textiles.",
         more="Desde maquetas arquitectónicas y cajas personalizadas hasta grabado en cuero y joyería en acrílico."),
    dict(icon="auto_fix_high", img="grabado-laser-uv.webp", title="Grabado láser UV",
         short="Para grabar metales desnudos y materiales delicados.",
         more="Personalizar joyería, marcar códigos, logos o QRs en herramientas y piezas industriales, grabar cristalería, cerámica y componentes electrónicos."),
    dict(icon="checkroom", img="prensas-de-calor.webp", title="Prensas de calor",
         short="Sublimación o vinil textil sobre diversos materiales, con presión y temperatura exactas.",
         more="Desde estampar playeras y bolsas, aplicar vinil textil en ropa deportiva, hasta personalizar artículos como tazas, termos y mousepads."),
    dict(icon="deployed_code", img="impresion-3d-filamento.webp", title="Impresión 3D de filamento",
         short="Para materializar volúmenes y geometrías complejas con plásticos de uso hobby y técnico.",
         more="Prototipos rápidos, piezas de repuesto, figuras artísticas, maquetas y piezas funcionales."),
    dict(icon="water_drop", img="impresion-3d-resina.webp", title="Impresión 3D de resina",
         short="Para materializar volúmenes y geometrías complejas con altísima resolución.",
         more="Piezas con detalles finos, como miniaturas, joyería o modelismo."),
    dict(icon="carpenter", img="router-cnc.webp", title="Router CNC",
         short="Para cortar tableros completos de madera, MDF, OSB, aluminio o plásticos de ingeniería.",
         more="Mobiliario (sillas, mesas, estanterías), stands para ferias, estructuras paramétricas y moldes grandes."),
    dict(icon="draw", img="corte-de-vinil.webp", title="Corte de vinil",
         short="Para cortar vinil adhesivo, vinil textil, cobre adhesivo o dibujar con bolígrafo en gran formato.",
         more="Stickers, rotulación de ventanas, vinil textil para estampar camisetas (heat transfer) y circuitos flexibles de cobre."),
    dict(icon="memory", img="circuitos.webp", title="Circuitos",
         short="Para complementar proyectos que integren iluminación, electricidad o electrónica.",
         more="Desde iluminar un logo y construir letreros neón hasta darle movimiento con motores a una base de pastel o a una maqueta."),
    dict(icon="3d_rotation", img="escaner-3d.webp", title="Escáner 3D",
         short="Para capturar y digitalizar objetos reales y convertirlos en un archivo digital editable.",
         more="Desde crear el plano de una pieza rota o antigua para hacer un repuesto, hasta digitalizar artesanías o partes del cuerpo para personalización médica."),
    dict(icon="support_agent", img="asesoria-y-diseno.webp", title="Asesoría y diseño",
         short="Más que máquinas: revisamos contigo tu proyecto y te sugerimos el mejor camino.",
         more="Prototipado, servicio de modelado 3D y CAD, servicios de vectorización y consultoría para desarrollo de producto."),
]
SERVICE_OPTIONS = [s["title"] for s in SERVICES] + [
    "Usar el espacio (membresía / acceso)", "Innovación / I+D", "Emprendimiento",
    "Formación / talleres", "Otro / no estoy seguro",
]


# --------------------------------------------------------------------------
# Plantilla base
# --------------------------------------------------------------------------
def icon(name, extra=""):
    return f'<span class="material-symbols-outlined" aria-hidden="true"{extra}>{name}</span>'


def nav_html(current):
    out = ['<ul>']
    for label, href, kids in NAV:
        page = href.split("#")[0]
        cur = ' aria-current="page"' if page == current else ""
        out.append('<li class="has-sub">')
        out.append(f'<a class="nav-link" href="{href}"{cur}>{escape(label)}</a>')
        out.append('<ul class="sub">')
        for k_label, k_href, k_desc in kids:
            out.append(f'<li><a href="{k_href}">{escape(k_label)}<small>{escape(k_desc)}</small></a></li>')
        out.append('</ul></li>')
    out.append('</ul>')
    cta_label, cta_href = NAV_CTA
    out.append(f'<a class="btn btn--accent nav-cta" href="{cta_href}">{escape(cta_label)}</a>')
    return "\n".join(out)


def footer_html():
    cols = []
    for label, href, kids in NAV:
        cols.append((label, href))
    links = "\n".join(f'<li><a href="{h}">{escape(l)}</a></li>' for l, h in cols)
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="images/logo-blanco.png" alt="{NAME} · {TAGLINE}" width="{681}" height="{181}">
        <p>Empoderando a la comunidad local a través de la fabricación digital, la educación, la innovación y el emprendimiento.</p>
      </div>
      <div>
        <h4>Explora</h4>
        <ul>
          <li><a href="index.html">Inicio</a></li>
          {links}
        </ul>
      </div>
      <div>
        <h4>Servicios</h4>
        <ul>
          <li><a href="laboratorio.html#servicios">Fabricación digital</a></li>
          <li><a href="laboratorio.html#usa-el-espacio">Usa el espacio</a></li>
          <li><a href="innovacion.html">Innovación e I+D</a></li>
          <li><a href="contacto.html">Solicitar cotización</a></li>
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a></li>
          <li><a href="tel:{CONTACT['tel_href']}">{CONTACT['tel_label']}</a></li>
          <li><a href="{CONTACT['maps']}" target="_blank" rel="noopener">{escape(CONTACT['address'])}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> {NAME.upper()}. Todos los derechos reservados.</span>
      <nav aria-label="Legal">
        <a href="politica-de-privacidad.html">Políticas de privacidad</a>
        <a href="terminos-de-los-servicios.html">Términos de los servicios</a>
      </nav>
    </div>
  </div>
</footer>"""


def render(slug, title, desc, hero, body, noindex=False):
    full_title = f"{title} · {NAME}" if slug != "index.html" else f"{NAME} · {TAGLINE}"
    url = f"{SITE_URL}/{'' if slug == 'index.html' else slug}"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#001c72">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/images/og-fabjardin.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@600;700;800&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0..1,0" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="{NAME}, ir al inicio">
      <img src="images/logo-blanco.png" alt="{NAME} · {TAGLINE}" width="681" height="181">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="menu-principal" aria-label="Abrir menú">
      {icon("menu")}
    </button>
    <nav class="nav" id="menu-principal" aria-label="Principal">
{nav_html(slug)}
    </nav>
  </div>
</header>
<main id="contenido">
{hero}
{body}
</main>
{footer_html()}
<script src="js/config.js"></script>
<script src="js/main.js"></script>
</body>
</html>
"""


def page_hero(eyebrow, h1, lead, crumbs):
    trail = '<a href="index.html">Inicio</a>' + "".join(f" / {c}" for c in crumbs)
    return f"""<section class="page-hero">
  <div class="container">
    <div class="breadcrumb">{trail}</div>
    <span class="eyebrow">{escape(eyebrow)}</span>
    <h1>{escape(h1)}</h1>
    <p class="lead">{escape(lead)}</p>
  </div>
</section>"""


def cta_band(title="¿Tienes una idea o un proyecto?", text="Cuéntanos qué necesitas y te respondemos con la mejor solución.",
             label="Solicita tu cotización", href="contacto.html"):
    return f"""<section class="section section--navy cta-band">
  <div class="container reveal">
    <h2>{escape(title)}</h2>
    <p class="lead">{escape(text)}</p>
    <div class="btn-row"><a class="btn btn--accent" href="{href}">{escape(label)} {icon("arrow_forward")}</a></div>
  </div>
</section>"""


def service_card(s, link=True):
    img = f'<img src="images/servicios/{s["img"]}" alt="" loading="lazy">'
    ask = f'<p style="margin-top:.8rem"><a class="more" href="contacto.html?servicio={s["title"].replace(" ", "%20")}">Cotizar este servicio {icon("arrow_forward")}</a></p>' if link else ""
    return f"""<article class="card service-card reveal">
  <div class="service-media">{icon(s["icon"])}{img}</div>
  <div class="service-body">
    <h3>{escape(s["title"])}</h3>
    <p>{escape(s["short"])}</p>
    <details class="more-info">
      <summary>¿Qué se puede hacer?</summary>
      <p>{escape(s["more"])}</p>
    </details>
    {ask}
  </div>
</article>"""


PAGES = {}

# ==========================================================================
# INICIO
# ==========================================================================
PAGES["index.html"] = dict(
    title=TAGLINE,
    desc="Fabjardin es un centro de innovación y tecnologías creativas en Chalco: fabricación digital, innovación, emprendimiento y formación en un solo ecosistema.",
    hero=f"""<section class="hero">
  <div class="container hero-inner">
    <div>
      <span class="eyebrow">{TAGLINE}</span>
      <h1>Donde las ideas se vuelven <em>productos, proyectos y comunidad</em>.</h1>
      <p class="lead">Facilitamos y centralizamos la fabricación de tus proyectos en un solo lugar, y te acompañamos a innovar, emprender y aprender con tecnologías creativas.</p>
      <div class="btn-row">
        <a class="btn btn--accent" href="laboratorio.html#servicios">Nuestros servicios {icon("arrow_forward")}</a>
        <a class="btn btn--ghost" href="contacto.html">Cotiza tu proyecto</a>
      </div>
    </div>
    <div class="hero-mark" aria-hidden="true"><img src="images/icono-blanco.png" alt="" width="512" height="512"></div>
  </div>
</section>""",
    body=f"""
<section class="section">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Un ecosistema, cinco ejes</span>
      <h2>Todo lo que necesitas para llevar una idea al mundo real</h2>
      <p class="lead">Fabricación, innovación, emprendimiento, formación y comunidad conectados en un mismo espacio.</p>
    </div>
    <div class="grid grid-5">
      <a class="card eje reveal" href="laboratorio.html"><div class="num">01</div><div class="icon">{icon("precision_manufacturing")}</div><h3>Laboratorio</h3><p>Fabricación digital y uso del taller con maquinaria lista para usar.</p><span class="more">Explorar {icon("arrow_forward")}</span></a>
      <a class="card eje reveal" href="innovacion.html"><div class="num">02</div><div class="icon">{icon("lightbulb")}</div><h3>Innovación</h3><p>I+D, prototipado y desarrollo de producto para empresas e instituciones.</p><span class="more">Explorar {icon("arrow_forward")}</span></a>
      <a class="card eje reveal" href="emprendimiento.html"><div class="num">03</div><div class="icon">{icon("rocket_launch")}</div><h3>Emprendimiento</h3><p>Acompañamiento para transformar tu idea en un proyecto real.</p><span class="more">Explorar {icon("arrow_forward")}</span></a>
      <a class="card eje reveal" href="formacion.html"><div class="num">04</div><div class="icon">{icon("school")}</div><h3>Formación</h3><p>Talleres prácticos, bootcamps y programas para escuelas y jóvenes.</p><span class="more">Explorar {icon("arrow_forward")}</span></a>
      <a class="card eje reveal" href="comunidad.html"><div class="num">05</div><div class="icon">{icon("groups")}</div><h3>Comunidad</h3><p>Eventos, proyectos y una red de personas que crean juntas.</p><span class="more">Explorar {icon("arrow_forward")}</span></a>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Acerca de nosotros</span>
        <h2>Un centro de fabricación digital parte de la red global FabLab</h2>
        <p class="lead">Diseñamos y convertimos ideas en proyectos fabricables y tangibles para toda la comunidad.</p>
        <div class="btn-row"><a class="btn btn--navy" href="nosotros.html">Conócenos {icon("arrow_forward")}</a></div>
      </div>
      <div class="mv reveal">
        <div class="card"><div class="icon">{icon("rocket_launch")}</div><h3>Nuestra misión</h3><p>Empoderar a la comunidad facilitando el acceso a la fabricación digital y tecnologías de vanguardia, para transformar ideas en proyectos de alto impacto educativo, social y económico.</p></div>
        <div class="card"><div class="icon">{icon("visibility")}</div><h3>Visión</h3><p>Ser el nodo de referencia regional en innovación y creatividad, donde la colaboración y la tecnología se unen para impulsar el desarrollo sostenible y transformar el futuro de nuestras comunidades.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy" id="impacto">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Nuestro impacto</span><h2>Resultados que se pueden tocar</h2></div>
    <div class="stats reveal">
      <div class="stat"><strong>+2,200</strong><span>Proyectos finalizados</span></div>
      <div class="stat"><strong>+150</strong><span>Emprendedores beneficiados</span></div>
      <div class="stat"><strong>+15</strong><span>BootCamps y capacitaciones</span></div>
      <div class="stat"><strong>+20</strong><span>Colaboraciones institucionales</span></div>
    </div>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--ghost" href="{IMPACT_REPORT}" target="_blank" rel="noopener">Visita nuestro informe de actividades {icon("arrow_forward")}</a></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">¿Qué nos hace diferentes?</span><h2>Tecnología, método y acompañamiento</h2></div>
    <div class="diff">
      <div class="item reveal">{icon("memory")}<h3>Innovación InHouse</h3><p>Máquinas y procesos en un solo lugar, listo para usar.</p></div>
      <div class="item reveal">{icon("workspace_premium")}<h3>Certificación global</h3><p>Operamos bajo los estándares de la FabLab Network.</p></div>
      <div class="item reveal">{icon("bolt")}<h3>Agilidad radical</h3><p>De la idea al producto, sin mínimos de producción.</p></div>
      <div class="item reveal">{icon("fingerprint")}<h3>Hiper-personalización</h3><p>Fabricación de piezas únicas que la industria masiva no puede atender.</p></div>
      <div class="item reveal">{icon("handshake")}<h3>Socios de la innovación</h3><p>Know-how técnico y acompañamiento en diseño y metodologías.</p></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Servicios de fabricación</span>
      <h2>Transformamos archivos digitales en objetos físicos con precisión</h2>
    </div>
    <div class="grid grid-3">
      {"".join(service_card(s, link=False) for s in SERVICES[:6])}
    </div>
    <div class="btn-row"><a class="btn btn--navy" href="laboratorio.html#servicios">Ver todos los servicios {icon("arrow_forward")}</a></div>
  </div>
</section>

{cta_band()}
""",
)

# ==========================================================================
# NOSOTROS
# ==========================================================================
PAGES["nosotros.html"] = dict(
    title="Nosotros",
    desc="Conoce a Fabjardin: misión, visión, impacto y nuestra pertenencia a la red global FabLab.",
    hero=page_hero("Nosotros", "Un centro que conecta tecnología, creatividad y comunidad",
                   "Somos un centro de fabricación digital parte de la red global FabLab, donde diseñamos y convertimos ideas en proyectos fabricables y tangibles para toda la comunidad.",
                   ["Nosotros"]),
    body=f"""
<section class="section" id="quienes-somos">
  <div class="container">
    <div class="mv reveal">
      <div class="card"><div class="icon">{icon("rocket_launch")}</div><h3>Nuestra misión</h3><p>Empoderar a la comunidad facilitando el acceso a la fabricación digital y tecnologías de vanguardia, para transformar ideas en proyectos de alto impacto educativo, social y económico.</p></div>
      <div class="card"><div class="icon">{icon("visibility")}</div><h3>Visión</h3><p>Ser el nodo de referencia regional en innovación y creatividad, donde la colaboración y la tecnología se unen para impulsar el desarrollo sostenible y transformar el futuro de nuestras comunidades.</p></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">¿Qué nos hace diferentes?</span><h2>Lo que nos distingue</h2></div>
    <div class="diff">
      <div class="item reveal">{icon("memory")}<h3>Innovación InHouse</h3><p>Máquinas y procesos en un solo lugar, listo para usar.</p></div>
      <div class="item reveal">{icon("workspace_premium")}<h3>Certificación global</h3><p>Operamos bajo los estándares de la FabLab Network.</p></div>
      <div class="item reveal">{icon("bolt")}<h3>Agilidad radical</h3><p>De la idea al producto, sin mínimos de producción.</p></div>
      <div class="item reveal">{icon("fingerprint")}<h3>Hiper-personalización</h3><p>Fabricación de piezas únicas que la industria masiva no puede atender.</p></div>
      <div class="item reveal">{icon("handshake")}<h3>Socios de la innovación</h3><p>Know-how técnico y acompañamiento en diseño y metodologías.</p></div>
    </div>
  </div>
</section>

<section class="section section--navy" id="impacto">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Impacto</span><h2>Nuestro impacto</h2></div>
    <div class="stats reveal">
      <div class="stat"><strong>+2,200</strong><span>Proyectos finalizados</span></div>
      <div class="stat"><strong>+150</strong><span>Emprendedores beneficiados</span></div>
      <div class="stat"><strong>+15</strong><span>BootCamps y capacitaciones</span></div>
      <div class="stat"><strong>+20</strong><span>Colaboraciones institucionales</span></div>
    </div>
    <div class="btn-row" style="justify-content:center"><a class="btn btn--ghost" href="{IMPACT_REPORT}" target="_blank" rel="noopener">Visita nuestro informe de actividades {icon("arrow_forward")}</a></div>
  </div>
</section>

<section class="section" id="red">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Red FabLab y aliados</span>
      <h2>Parte de una red global de laboratorios</h2>
      <p class="lead">Formamos parte de la red global <a href="{FABLAB_NETWORK}" target="_blank" rel="noopener">FabLab Network</a> y operamos bajo sus estándares, lo que nos conecta con conocimiento, proyectos y personas de todo el mundo.</p>
      <ul class="checks">
        <li>Colaboraciones con instituciones, empresas y organizaciones</li>
        <li>Intercambio de buenas prácticas con otros laboratorios</li>
        <li>Proyectos con impacto educativo, social y económico</li>
      </ul>
    </div>
    <div class="panel reveal">
      <h3>¿Quieres colaborar con nosotros?</h3>
      <p>Si representas a una institución, empresa u organización y quieres construir algo en conjunto, escríbenos.</p>
      <div class="btn-row"><a class="btn btn--accent" href="contacto.html">Contáctanos {icon("arrow_forward")}</a></div>
    </div>
  </div>
</section>
""",
)

# ==========================================================================
# LABORATORIO
# ==========================================================================
EQUIP = [
    ("content_cut", "Corte y grabado láser", "Láser CO2 para madera, acrílico, cuero, cartón, papel y textiles, y láser UV para metales y materiales delicados."),
    ("deployed_code", "Impresión 3D", "Impresión en filamento para piezas funcionales y en resina para alta resolución."),
    ("carpenter", "Router CNC", "Corte de tableros completos de madera, MDF, OSB, aluminio y plásticos de ingeniería."),
    ("checkroom", "Textil y personalización", "Prensas de calor y corte de vinil para sublimación, vinil textil, stickers y rotulación."),
    ("memory", "Electrónica", "Iluminación, circuitos, letreros neón y movimiento con motores para tus prototipos."),
    ("3d_rotation", "Escaneo y diseño 3D", "Escáner 3D, modelado CAD y vectorización para pasar de lo real a lo digital y viceversa."),
]
PAGES["laboratorio.html"] = dict(
    title="Laboratorio de fabricación digital",
    desc="Servicios de fabricación digital en Chalco: corte láser, grabado UV, impresión 3D, router CNC, vinil, circuitos, escáner 3D y uso del espacio.",
    hero=page_hero("Laboratorio", "Fabricación digital, en un solo lugar",
                   "Cuéntanos tu idea, envíanos tus archivos o diseños, y los transformamos en objetos que podrás tener en tus manos.",
                   ["Laboratorio"]),
    body=f"""
<section class="section" id="servicios">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Servicios de fabricación</span>
      <h2>Soluciones de fabricación digital</h2>
      <p class="lead">Transformamos archivos digitales en objetos físicos con precisión. Elige un servicio o cuéntanos tu proyecto y te orientamos.</p>
    </div>
    <div class="grid grid-3">
      {"".join(service_card(s) for s in SERVICES)}
    </div>
  </div>
</section>

<section class="section section--soft" id="equipamiento">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Equipamiento y tecnologías</span>
      <h2>Lo que hay en el taller</h2>
      <p class="lead">Herramientas y maquinaria agrupadas por área, listas para tus prototipos, maquetas y producciones.</p>
    </div>
    <div class="grid grid-3">
      {"".join(f'<div class="card reveal"><div class="icon">{icon(i)}</div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for i, t, d in EQUIP)}
    </div>
  </div>
</section>

<section class="section" id="usa-el-espacio">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Usa el espacio</span>
      <h2>Fabrica tú, sin comprar herramientas caras</h2>
      <p class="lead">Te ofrecemos un espacio con acceso flexible a nuestras instalaciones, equipadas con herramientas y maquinaria, para sacar adelante tus maquetas, trabajos, prototipos o proyectos.</p>
      <ul class="checks">
        <li>Acceso flexible a las instalaciones</li>
        <li>Herramientas y maquinaria listas para usar</li>
        <li>Orientación del equipo técnico cuando la necesites</li>
      </ul>
      <div class="btn-row"><a class="btn btn--navy" href="contacto.html?servicio=Usar%20el%20espacio%20(membres%C3%ADa%20/%20acceso)">Quiero usar el espacio {icon("arrow_forward")}</a></div>
    </div>
    <div class="panel reveal">
      <h3>¿No sabes por dónde empezar?</h3>
      <p>Nuestro equipo revisa tu proyecto contigo y te sugiere qué tecnología, material y proceso conviene usar.</p>
      <div class="btn-row"><a class="btn btn--accent" href="innovacion.html#asesoria">Conoce la asesoría {icon("arrow_forward")}</a></div>
    </div>
  </div>
</section>

{cta_band()}
""",
)

# ==========================================================================
# INNOVACIÓN
# ==========================================================================
PAGES["innovacion.html"] = dict(
    title="Innovación e I+D",
    desc="Tu equipo externo de investigación y desarrollo: soluciones a medida, prototipado y desarrollo de producto para empresas, instituciones y emprendedores.",
    hero=page_hero("Innovación", "Tu equipo externo de Investigación y Desarrollo",
                   "Echamos una mano a empresas, instituciones, emprendedores y a la comunidad con soluciones a medida, desde pensar y dinamizar ideas hasta crear prototipos y productos finales.",
                   ["Innovación"]),
    body=f"""
<section class="section" id="id-empresas">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">I+D para empresas e instituciones</span><h2>Metodologías ágiles, de diseño y de fabricación</h2>
      <p class="lead">Para lograr soluciones a medida combinamos metodologías ágiles, de diseño y de fabricación con la capacidad de producir en casa.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{icon("psychology")}</div><h3>Dinamización de ideas</h3><p>Sesiones para pensar, explorar y priorizar retos y oportunidades de producto o proceso.</p></div>
      <div class="card reveal"><div class="icon">{icon("draw")}</div><h3>Diseño a medida</h3><p>Soluciones diseñadas para tu necesidad, con acompañamiento técnico en cada decisión.</p></div>
      <div class="card reveal"><div class="icon">{icon("precision_manufacturing")}</div><h3>Fabricación en casa</h3><p>Máquinas y procesos en un solo lugar para pasar de la propuesta al objeto físico sin intermediarios.</p></div>
    </div>
  </div>
</section>

<section class="section section--soft" id="prototipado">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Prototipado y desarrollo de producto</span>
      <h2>De la idea al prototipo funcional</h2>
      <p class="lead">Iteramos contigo hasta tener un prototipo que puedas probar, mostrar y mejorar, sin mínimos de producción.</p>
      <ul class="checks">
        <li>Prototipos rápidos y piezas funcionales</li>
        <li>Piezas únicas e hiper-personalizadas</li>
        <li>Pruebas y mejoras en ciclos cortos</li>
      </ul>
    </div>
    <div class="panel reveal">
      <h3>¿Tienes un reto de producto?</h3>
      <p>Cuéntanos qué quieres lograr y te proponemos cómo abordarlo.</p>
      <div class="btn-row"><a class="btn btn--accent" href="contacto.html?servicio=Innovaci%C3%B3n%20/%20I%2BD">Hablemos {icon("arrow_forward")}</a></div>
    </div>
  </div>
</section>

<section class="section" id="asesoria">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Asesoría y diseño</span><h2>Más que máquinas: revisamos contigo y sugerimos</h2></div>
    <div class="grid grid-4">
      <div class="card reveal"><div class="icon">{icon("view_in_ar")}</div><h3>Modelado 3D y CAD</h3><p>Convertimos tus ideas o piezas físicas en modelos listos para fabricar.</p></div>
      <div class="card reveal"><div class="icon">{icon("polyline")}</div><h3>Vectorización</h3><p>Preparamos tus gráficos para corte, grabado y vinil.</p></div>
      <div class="card reveal"><div class="icon">{icon("construction")}</div><h3>Prototipado</h3><p>Primeras versiones físicas para validar forma, tamaño y función.</p></div>
      <div class="card reveal"><div class="icon">{icon("support_agent")}</div><h3>Consultoría de producto</h3><p>Acompañamiento para desarrollar tu producto de punta a punta.</p></div>
    </div>
  </div>
</section>

{cta_band("Construyamos la solución juntos", "Platícanos tu reto y armamos una propuesta a tu medida.", "Contáctanos")}
""",
)

# ==========================================================================
# EMPRENDIMIENTO
# ==========================================================================
PAGES["emprendimiento.html"] = dict(
    title="Emprendimiento",
    desc="Acompañamiento para transformar una idea en un proyecto real, desde el inicio hasta la fabricación de tus productos.",
    hero=page_hero("Emprendimiento", "Emprende con tus propios productos",
                   "Te acompañamos para transformar una idea en un proyecto real: te guiamos desde el inicio hasta la fabricación.",
                   ["Emprendimiento"]),
    body=f"""
<section class="section" id="acompanamiento">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Acompañamiento</span>
      <h2>Un ecosistema para quien quiere crear algo propio</h2>
      <p class="lead">Más de 150 emprendedores han pasado por Fabjardin. Aquí encuentras tecnología, método y personas que te ayudan a avanzar.</p>
      <ul class="checks">
        <li>Orientación técnica y de diseño desde la primera idea</li>
        <li>Fabricación de tus prototipos y primeras producciones</li>
        <li>Producción sin mínimos, ideal para validar antes de invertir</li>
      </ul>
    </div>
    <div class="panel reveal">
      <h3>+150 emprendedores beneficiados</h3>
      <p>Si tienes una idea de producto, platícanos en qué etapa estás y te decimos cómo podemos ayudarte.</p>
      <div class="btn-row"><a class="btn btn--accent" href="contacto.html?servicio=Emprendimiento">Quiero emprender {icon("arrow_forward")}</a></div>
    </div>
  </div>
</section>

<section class="section section--soft" id="ruta">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">De la idea al producto</span><h2>Nuestra ruta en cinco pasos</h2></div>
    <ol class="steps">
      <li class="reveal"><h3>Idea</h3><p>Aterrizamos tu concepto y definimos qué problema resuelve.</p></li>
      <li class="reveal"><h3>Diseño</h3><p>Modelamos y preparamos los archivos para fabricar.</p></li>
      <li class="reveal"><h3>Prototipo</h3><p>Fabricamos una primera versión física para probarla.</p></li>
      <li class="reveal"><h3>Mejora</h3><p>Iteramos con lo aprendido hasta llegar a la versión final.</p></li>
      <li class="reveal"><h3>Producción</h3><p>Fabricamos tus piezas, desde unidades únicas hasta series cortas.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="red">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Mentorías y red</span><h2>No emprendes solo</h2>
      <p class="lead">Fabjardin es un punto de encuentro entre emprendedores, empresas, instituciones y comunidad. Conectamos personas y recursos para que tu proyecto crezca.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{icon("diversity_3")}</div><h3>Comunidad</h3><p>Conoce a otras personas que están creando y fabricando.</p></div>
      <div class="card reveal"><div class="icon">{icon("handshake")}</div><h3>Colaboraciones</h3><p>Más de 20 colaboraciones institucionales abren puertas para tus proyectos.</p></div>
      <div class="card reveal"><div class="icon">{icon("school")}</div><h3>Formación</h3><p>Talleres y bootcamps para fortalecer tus habilidades técnicas y de diseño.</p></div>
    </div>
  </div>
</section>

{cta_band("Cuéntanos tu idea", "Te ayudamos a dar el primer paso.", "Hablemos de tu proyecto", "contacto.html?servicio=Emprendimiento")}
""",
)

# ==========================================================================
# FORMACIÓN
# ==========================================================================
TEMAS = [
    ("view_in_ar", "Diseño 3D y CAD"), ("content_cut", "Corte y grabado láser"), ("deployed_code", "Impresión 3D"),
    ("memory", "Electrónica creativa"), ("polyline", "Vectorización y diseño gráfico"), ("checkroom", "Personalización textil"),
]
PAGES["formacion.html"] = dict(
    title="Formación",
    desc="Talleres prácticos, bootcamps y programas para escuelas y jóvenes sobre nuevas tecnologías y diseño.",
    hero=page_hero("Formación", "Aprende haciendo con tecnologías creativas",
                   "Un ecosistema donde impartimos talleres prácticos sobre nuevas tecnologías y diseño.",
                   ["Formación"]),
    body=f"""
<section class="section" id="talleres">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Talleres y cursos</span><h2>Práctica desde la primera sesión</h2>
      <p class="lead">Aprendes usando las mismas máquinas con las que fabricamos proyectos reales.</p></div>
    <div class="grid grid-3">
      {"".join(f'<div class="card reveal"><div class="icon">{icon(i)}</div><h3>{escape(t)}</h3></div>' for i, t in TEMAS)}
    </div>
    <p class="reveal" style="margin-top:1.6rem">¿Quieres saber cuándo es el próximo taller? <a href="contacto.html?servicio=Formaci%C3%B3n%20/%20talleres">Escríbenos</a> y te avisamos.</p>
  </div>
</section>

<section class="section section--soft" id="bootcamps">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">BootCamps</span>
      <h2>Capacitaciones intensivas</h2>
      <p class="lead">Más de 15 bootcamps y capacitaciones realizados. Programas intensivos para adquirir habilidades concretas en poco tiempo.</p>
    </div>
    <div class="panel reveal">
      <h3>+15</h3>
      <p>BootCamps y capacitaciones impartidos en Fabjardin.</p>
      <div class="btn-row"><a class="btn btn--accent" href="contacto.html?servicio=Formaci%C3%B3n%20/%20talleres">Pide información {icon("arrow_forward")}</a></div>
    </div>
  </div>
</section>

<section class="section" id="escuelas">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Escuelas y jóvenes</span><h2>Llevamos la tecnología al aula</h2>
      <p class="lead">Diseñamos experiencias educativas para que niñas, niños y jóvenes entiendan cómo funcionan las cosas y se atrevan a crearlas.</p></div>
    <div class="grid grid-3">
      <div class="card reveal"><div class="icon">{icon("school")}</div><h3>Programas educativos</h3><p>Contenidos prácticos adaptados a cada nivel y objetivo de aprendizaje.</p></div>
      <div class="card reveal"><div class="icon">{icon("directions_bus")}</div><h3>Visitas de grupos y escuelas</h3><p>Recorridos y actividades en el taller para grupos escolares y comunitarios.</p></div>
      <div class="card reveal"><div class="icon">{icon("emoji_objects")}</div><h3>Proyectos con impacto</h3><p>Aprender resolviendo retos reales de la comunidad.</p></div>
    </div>
  </div>
</section>

{cta_band("Capacita a tu equipo o a tu grupo", "Cuéntanos qué quieres aprender y armamos el programa.", "Solicitar información", "contacto.html?servicio=Formaci%C3%B3n%20/%20talleres")}
""",
)

# ==========================================================================
# COMUNIDAD
# ==========================================================================
PAGES["comunidad.html"] = dict(
    title="Comunidad",
    desc="Eventos, proyectos y noticias de la comunidad Fabjardin.",
    hero=page_hero("Comunidad", "Crear es mejor en comunidad",
                   "Eventos, proyectos y personas que se encuentran en Fabjardin para aprender, fabricar y colaborar.",
                   ["Comunidad"]),
    body=f"""
<section class="section" id="agenda">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Eventos y agenda</span>
      <h2>Lo que viene en Fabjardin</h2>
      <p class="lead">Talleres, jornadas abiertas y encuentros con la comunidad. Pronto publicaremos aquí el calendario.</p>
      <div class="btn-row"><a class="btn btn--navy" href="contacto.html">Quiero enterarme {icon("arrow_forward")}</a></div>
    </div>
    <div class="panel reveal">
      <h3>Próximamente</h3>
      <p>Escríbenos y te avisamos de las próximas actividades abiertas al público.</p>
    </div>
  </div>
</section>

<section class="section section--soft" id="proyectos">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Proyectos</span><h2>Más de 2,200 proyectos finalizados</h2>
      <p class="lead">Desde maquetas y prototipos hasta productos de emprendedores. Conoce lo que hemos hecho en nuestro informe de actividades.</p></div>
    <div class="btn-row"><a class="btn btn--navy" href="{IMPACT_REPORT}" target="_blank" rel="noopener">Ver informe de actividades {icon("arrow_forward")}</a></div>
  </div>
</section>

<section class="section" id="noticias">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Noticias</span><h2>Entérate de lo nuevo</h2>
      <p class="lead">Estamos preparando esta sección con novedades, convocatorias y casos de la comunidad.</p></div>
  </div>
</section>

{cta_band("Sé parte de la comunidad", "Colabora, aprende o fabrica con nosotros.", "Contáctanos")}
""",
)

# ==========================================================================
# CONTACTO
# ==========================================================================
options = "".join(f'<option value="{escape(o)}">{escape(o)}</option>' for o in SERVICE_OPTIONS)
PAGES["contacto.html"] = dict(
    title="Contacto y cotización",
    desc="Describe tu idea o proyecto y recibe una cotización de Fabjardin. Escríbenos por correo, teléfono o WhatsApp.",
    hero=page_hero("Contacto", "Solicita tu cotización",
                   "Describe tu idea, comparte tus archivos y nuestro equipo técnico analizará la viabilidad para darte la mejor solución.",
                   ["Contacto"]),
    body=f"""
<section class="section">
  <div class="container" style="display:grid;grid-template-columns:1.4fr 1fr;gap:2.5rem;align-items:start" id="contacto-grid">
    <div class="form-card reveal">
      <form id="form-cotizacion" novalidate>
        <div class="form-grid">
          <div class="field"><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" type="text" autocomplete="name" required></div>
          <div class="field"><label for="email">Email de contacto</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="telefono">Teléfono (opcional)</label><input id="telefono" name="telefono" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="servicio">Servicio requerido</label><select id="servicio" name="servicio" required>{options}</select></div>
          <div class="field full"><label for="urgencia">Urgencia</label>
            <select id="urgencia" name="urgencia">
              <option>Normal (3-5 días)</option><option>Prioritario (24-48h)</option><option>Sin prisa</option>
            </select></div>
          <div class="field full"><label for="descripcion">Descripción del proyecto</label><textarea id="descripcion" name="descripcion" required placeholder="Cuéntanos qué quieres fabricar, materiales, medidas, cantidad…"></textarea></div>
          <div class="field full"><label for="archivos">Enlace a tus archivos (DXF, STL, PDF…)</label><input id="archivos" name="archivos" type="url" placeholder="https://drive.google.com/…">
            <span class="hint">Sube tus archivos a Google Drive, Dropbox o similar y pega aquí el enlace (con permiso de lectura).</span></div>
          <div class="hp" aria-hidden="true"><label>No llenar<input name="_gotcha" type="text" tabindex="-1" autocomplete="off"></label></div>
        </div>
        <div class="btn-row"><button class="btn btn--navy" type="submit">Enviar solicitud {icon("send")}</button></div>
        <div id="form-status" class="form-status" role="status" aria-live="polite"></div>
      </form>
    </div>
    <aside class="panel reveal">
      <h3>Hablemos</h3>
      <p>También puedes escribirnos directamente. Respondemos a la brevedad.</p>
      <ul class="contact-list">
        <li>{icon("mail")}<div><a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a><small>Correo</small></div></li>
        <li>{icon("call")}<div><a href="tel:{CONTACT['tel_href']}">{CONTACT['tel_label']}</a><small>Teléfono</small></div></li>
        <li>{icon("chat")}<div><a id="btn-whatsapp" href="https://wa.me/525576571685" target="_blank" rel="noopener">Escríbenos por WhatsApp</a><small>Respuesta rápida</small></div></li>
        <li>{icon("location_on")}<div><a href="{CONTACT['maps']}" target="_blank" rel="noopener">{escape(CONTACT['address'])}</a><small>Ubicación</small></div></li>
      </ul>
    </aside>
  </div>
  <style>@media (max-width: 960px) {{ #contacto-grid {{ grid-template-columns: 1fr !important; }} }}</style>
</section>
""",
)

# ==========================================================================
# LEGALES (borradores)
# ==========================================================================
DRAFT = '<div class="draft-banner">Borrador: este texto es una plantilla general y debe ser revisado y completado por la persona responsable (idealmente con asesoría legal) antes de la publicación definitiva.</div>'
PAGES["politica-de-privacidad.html"] = dict(
    title="Políticas de privacidad",
    desc="Aviso de privacidad de Fabjardin.",
    hero=page_hero("Legal", "Políticas de privacidad", "Cómo tratamos tus datos personales.", ["Políticas de privacidad"]),
    body=f"""<section class="section"><div class="container prose">
{DRAFT}
<h2>Responsable del tratamiento</h2>
<p>Fabjardin, con domicilio en {escape(CONTACT['address'])}, es responsable del tratamiento de los datos personales que nos proporciones.</p>
<h2>Datos que recabamos</h2>
<p>Nombre, correo electrónico, teléfono (opcional) y la información del proyecto que compartas mediante el formulario de contacto o por otros medios.</p>
<h2>Finalidades</h2>
<p>Atender tus solicitudes de cotización, dar seguimiento a tus proyectos y contactarte sobre nuestros servicios, talleres y actividades.</p>
<h2>Derechos ARCO</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, cancelación y oposición escribiendo a <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>.</p>
<h2>Cambios al aviso</h2>
<p>Cualquier modificación se publicará en esta misma página.</p>
</div></section>""",
    noindex=True,
)
PAGES["terminos-de-los-servicios.html"] = dict(
    title="Términos de los servicios",
    desc="Términos de los servicios de Fabjardin.",
    hero=page_hero("Legal", "Términos de los servicios", "Condiciones generales para el uso de nuestros servicios.", ["Términos de los servicios"]),
    body=f"""<section class="section"><div class="container prose">
{DRAFT}
<h2>Cotizaciones</h2>
<p>Las cotizaciones se elaboran a partir de la información y los archivos que proporciones. Los precios y tiempos pueden cambiar si cambian las especificaciones del proyecto.</p>
<h2>Archivos y propiedad intelectual</h2>
<p>Al enviarnos archivos o diseños declaras tener derecho a usarlos. Los derechos sobre tus diseños siguen siendo tuyos.</p>
<h2>Uso de las instalaciones</h2>
<p>El uso del espacio y la maquinaria está sujeto a las reglas de seguridad y de operación que te indique el equipo de Fabjardin.</p>
<h2>Contacto</h2>
<p>Para cualquier duda escríbenos a <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>.</p>
</div></section>""",
    noindex=True,
)


# --------------------------------------------------------------------------
# Escritura de archivos
# --------------------------------------------------------------------------
def write(path, content):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for slug, p in PAGES.items():
        write(slug, render(slug, p["title"], p["desc"], p["hero"], p["body"], p.get("noindex", False)))

    write("404.html", render(
        "404.html", "Página no encontrada", "La página que buscas no existe.",
        page_hero("Error 404", "No encontramos esa página", "Puede que el enlace haya cambiado.", []),
        f'<section class="section"><div class="container"><a class="btn btn--navy" href="index.html">Volver al inicio {icon("arrow_forward")}</a></div></section>',
        noindex=True))

    urls = [s for s, p in PAGES.items() if not p.get("noindex")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s in urls:
        loc = SITE_URL + "/" + ("" if s == "index.html" else s)
        sm.append(f"  <url><loc>{loc}</loc></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"OK: {len(PAGES) + 1} páginas generadas en {ROOT}")


if __name__ == "__main__":
    main()
