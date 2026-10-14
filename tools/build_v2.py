#!/usr/bin/env python3
"""
Generador del rediseño (carpeta v2/).  Uso:  python3 tools/build_v2.py

Reutiliza el menú, los datos de contacto y las cifras de tools/build.py.
Mientras una página no esté portada al diseño nuevo, sus enlaces apuntan
a la versión actual del sitio (../pagina.html).
"""
import math
import os
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "v2")
sys.path.insert(0, HERE)
import build as v1  # noqa: E402  (menú, contacto y textos del sitio actual)

PORTED = {"index.html"}          # páginas ya hechas en v2
NAME = v1.NAME
TAGLINE = v1.TAGLINE
CONTACT = v1.CONTACT


def lnk(href):
    """Enlace a una página; si aún no está en v2, apunta al sitio actual."""
    page = href.split("#")[0].split("?")[0]
    if page in PORTED or href.startswith(("http", "mailto:", "tel:", "#")):
        return href
    return "../" + href


FLECHA = '<svg class="flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square" aria-hidden="true"><path d="M3 12h17M13 5l7 7-7 7"/></svg>'


def panal_svg():
    """Panal de la cama de corte láser, como mosaico sin costuras."""
    r = 20.0
    w, h = math.sqrt(3) * r, 3 * r

    def hexa(cx, cy):
        pts = [(cx + r * math.cos(math.radians(-90 + 60 * k)), cy + r * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
        return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"

    d = " ".join([hexa(w / 2, r), hexa(0, r + 1.5 * r), hexa(w, r + 1.5 * r)])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.3f} {h:.1f}" width="{w:.3f}" height="{h:.1f}">'
            f'<path d="{d}" fill="none" stroke="#001c72" stroke-opacity=".10" stroke-width="1"/></svg>')


def cabecera(actual):
    items = []
    for label, href, kids in v1.NAV:
        page = href.split("#")[0]
        cur = ' aria-current="page"' if page == actual else ""
        subs = "".join(f'<a href="{lnk(h)}">{escape(l)}</a>' for l, h, _ in kids)
        items.append(f'<li class="tiene-sub"><a class="enlace" href="{lnk(href)}"{cur}>{escape(label)}</a><div class="sub">{subs}</div></li>')
    cta_l, cta_h = v1.NAV_CTA
    return f"""<header class="cabecera">
  <div class="contenedor">
    <a class="marca-logo" href="index.html" aria-label="{NAME}, inicio"><img src="images/logo.png" alt="{NAME} · {TAGLINE}" width="681" height="181"></a>
    <nav class="nav" id="menu-principal" aria-label="Principal">
      <ul>{''.join(items)}</ul>
      <span class="reloj" id="reloj" aria-hidden="true">Chalco</span>
      <a class="boton boton--lleno" href="{lnk(cta_h)}">{escape(cta_l)}</a>
    </nav>
    <button class="boton-menu" aria-expanded="false" aria-controls="menu-principal">Menú</button>
  </div>
</header>"""


def pie():
    c = CONTACT
    cols = "".join(f'<li><a href="{lnk(h)}">{escape(l)}</a></li>' for l, h, _ in v1.NAV)
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie-grid">
      <div>
        <img src="images/logo-blanco.png" alt="{NAME} · {TAGLINE}" width="681" height="181">
        <p>Empoderando a la comunidad local a través de la fabricación digital, la educación, la innovación y el emprendimiento.</p>
      </div>
      <div><h3>Explora</h3><ul><li><a href="index.html">Inicio</a></li>{cols}</ul></div>
      <div><h3>Servicios</h3><ul>
        <li><a href="{lnk('laboratorio.html#servicios')}">Fabricación digital</a></li>
        <li><a href="{lnk('laboratorio.html#usa-el-espacio')}">Usa el espacio</a></li>
        <li><a href="{lnk('innovacion.html')}">Innovación e I+D</a></li>
        <li><a href="{lnk('contacto.html')}">Solicitar cotización</a></li>
      </ul></div>
      <div><h3>Contacto</h3><ul>
        <li><a href="mailto:{c['email']}">{c['email']}</a></li>
        <li><a href="tel:{c['tel_href']}">{c['tel_label']}</a></li>
        <li><a href="{c['maps']}" target="_blank" rel="noopener">{escape(c['address'])}</a></li>
      </ul></div>
    </div>
    <div class="legal">
      <span>© <span id="anio">2026</span> {NAME.upper()}. Todos los derechos reservados.</span>
      <nav aria-label="Legal"><a href="{lnk('politica-de-privacidad.html')}">Políticas de privacidad</a><a href="{lnk('terminos-de-los-servicios.html')}">Términos de los servicios</a></nav>
    </div>
  </div>
</footer>"""


def pagina(slug, titulo, desc, cuerpo):
    full = f"{NAME} · {TAGLINE}" if slug == "index.html" else f"{titulo} · {NAME}"
    return f"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#f1f3fa">
<meta name="robots" content="noindex">
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
<script src="js/main.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Datos de la hoja de especificaciones: (máquina, trabaja con, sirve para)
# --------------------------------------------------------------------------
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

MANIFIESTO = [
    "Sin mínimos de producción.",
    "Máquinas y procesos bajo el mismo techo.",
    "Piezas únicas que la industria masiva no atiende.",
    "Estándares de la FabLab Network.",
    "Acompañamiento técnico de la idea al objeto.",
]


def index():
    paths = open(os.path.join(HERE, "marca_paths.txt"), encoding="utf-8").read().replace("\n", " ")
    ejes = "".join(
        f'<a class="eje" href="{lnk(h)}"><span class="nombre">{n}</span><p class="detalle">{escape(d)}</p>{FLECHA}</a>'
        for n, h, d in EJES)
    filas = "".join(
        f'<tr><td>{escape(m)}</td><td>{escape(t)}</td><td>{escape(s)}</td>'
        f'<td><a class="cotizar" href="{lnk("contacto.html")}?servicio={m.replace(" ", "%20")}">Cotizar</a></td></tr>'
        for m, t, s in HOJA)
    manifiesto = "".join(f"<p>{escape(t)}</p>" for t in MANIFIESTO)
    cuerpo = f"""
<section class="hero">
  <div class="contenedor">
    <h1><span>Del archivo</span><span>al objeto.</span></h1>
    <div class="marca-corte" aria-hidden="true">
      <svg viewBox="0 0 512 512"><path id="pieza" class="pieza" fill-rule="evenodd" d="{paths}"/><circle id="rayo" class="rayo" r="7" cx="256" cy="256"/></svg>
    </div>
    <div class="pie-hero">
      <p>Fabrica con nosotros, aprende en el taller o convierte tu idea en un negocio. Somos un centro de innovación y tecnologías creativas en Chalco.</p>
      <div class="fila-botones">
        <a class="boton boton--lleno" href="{lnk('contacto.html')}">Cotiza tu proyecto</a>
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
    <div class="cabeza">
      <h2>Qué máquina para qué material</h2>
      <p>Elige por material o cuéntanos tu proyecto y te decimos cuál conviene. Trabajamos con tus archivos o los diseñamos contigo.</p>
    </div>
    <table class="tabla">
      <thead><tr><th scope="col">Máquina</th><th scope="col">Trabaja con</th><th scope="col">Sirve para</th><th scope="col"><span class="visually-hidden">Acción</span></th></tr></thead>
      <tbody>{filas}</tbody>
    </table>
  </div>
</section>

<section class="manifiesto">
  <div class="contenedor">{manifiesto}</div>
</section>

<section class="resultados">
  <div class="contenedor">
    <p class="frase">Desde Chalco hemos terminado más de <b>2,200 proyectos</b>, acompañado a más de <b>150 emprendedores</b>, dado más de <b>15 bootcamps</b> y construido más de <b>20 colaboraciones</b> con instituciones.</p>
    <a href="{v1.IMPACT_REPORT}" target="_blank" rel="noopener">Ver el informe de actividades</a>
  </div>
</section>

<section class="final">
  <div class="contenedor">
    <h2>Trae tu archivo o trae tu idea.</h2>
    <div class="sub-final">
      <p>Te respondemos con la viabilidad, los tiempos y el costo. Estamos en La Bomba, Chalco de Díaz Covarrubias, Estado de México.</p>
      <div class="fila-botones">
        <a class="boton boton--lleno" href="{lnk('contacto.html')}">Solicitar cotización</a>
        <a class="boton boton--borde" href="{CONTACT['maps']}" target="_blank" rel="noopener">Cómo llegar</a>
      </div>
    </div>
  </div>
</section>
"""
    return pagina("index.html", TAGLINE,
                  "Fabjardin es un centro de innovación y tecnologías creativas en Chalco: fabricación digital, innovación, emprendimiento y formación.",
                  cuerpo)


def main():
    with open(os.path.join(OUT, "images", "panal.svg"), "w", encoding="utf-8") as f:
        f.write(panal_svg())
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index())
    print("OK: v2/index.html generado")


if __name__ == "__main__":
    main()
