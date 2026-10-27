# Fabjardin · Centro de Innovación y Tecnologías Creativas

Sitio web estático (HTML + CSS + JS, sin frameworks) publicado con **GitHub Pages**.

## Estructura

```
index.html                 Portada: "Del archivo al objeto"
nosotros.html              Misión y visión · Impacto · Red FabLab
laboratorio.html           Servicios de fabricación · Equipamiento · Usa el espacio
innovacion.html            I+D · Prototipado · Asesoría y diseño
emprendimiento.html        Acompañamiento · Ruta idea→producto · Mentorías y red
educacion.html             Talleres · BootCamps · Escuelas y jóvenes
comunidad.html             Agenda · Proyectos · Noticias
contacto.html              Formulario de cotización y datos de contacto
politica-de-privacidad.html / terminos-de-los-servicios.html   (borradores)
css/styles.css             Estilos (colores y tamaños en variables al inicio)
js/config.js               Correo, WhatsApp y endpoint del formulario
js/main.js                 Menú móvil, hora, animación del logo y formulario
fonts/                     Big Shoulders Display y Hanken Grotesk (alojadas aquí)
images/                    Logos, íconos, panal y fotos de servicios
tools/build.py             Generador de las páginas (menú, textos, servicios)
tools/marca_paths.txt      Contorno del logo usado en la animación de la portada
```

## Cómo editar

El menú, el pie y los textos de todas las páginas viven en `tools/build.py`. Después de cambiar algo:

```bash
python3 tools/build.py
```

Esto regenera todos los `.html`. Si editas un `.html` a mano, el siguiente `build.py` lo sobrescribirá.

## Imágenes (se detectan solas al ejecutar `python3 tools/build.py`)

Formato WebP (o cambia la extensión en `build.py`). Si el archivo no existe, se ve el color de la paleta.

| Dónde | Carpeta y nombres |
|---|---|
| Collage de la portada (dos columnas que se desplazan) | Usa las fotos de `images/servicios/`. Cambia cuáles y su orden en `COLUMNA_A` / `COLUMNA_B` de `tools/build.py` |
| Cinco ejes de la portada | `images/ejes/` → `laboratorio.webp`, `innovacion.webp`, `emprendimiento.webp`, `educacion.webp`, `comunidad.webp` |
| Encabezado de cada página (3 formas) | `images/hero/` → `<pagina>-1.webp` (rectángulo), `-2.webp`, `-3.webp` (círculos). Ej.: `laboratorio-1.webp` |
| Servicios de Laboratorio | `images/servicios/` (nombres abajo) |

## Paleta

Azul del logo `#001c72` + lima `#c8f53c`, cian `#29d3f0`, sol `#ffc933`, coral `#ff6a45`, lila `#b8a7ff` y azul eléctrico `#2f5bff`. Cada página usa un color de acento (`TONOS` en `tools/build.py`).

## Pendientes

1. **Fotos de servicios.** Guárdalas en `images/servicios/` con estos nombres y vuelve a ejecutar `python3 tools/build.py`: aparecen solas en Laboratorio.

   `corte-laser-co2.webp`, `grabado-laser-uv.webp`, `prensas-de-calor.webp`, `impresion-3d-filamento.webp`, `impresion-3d-resina.webp`, `router-cnc.webp`, `corte-de-vinil.webp`, `circuitos.webp`, `escaner-3d.webp`, `asesoria-y-diseno.webp`

2. **Formulario de cotización.** GitHub Pages no ejecuta código de servidor. Crea un formulario en [Formspree](https://formspree.io) (o similar) y pega su URL en `js/config.js` → `formEndpoint`. Sin eso, el formulario abre el correo del visitante con los datos ya escritos. Los archivos se comparten por enlace (Drive, Dropbox).
3. **Dirección.** Se usa la del membrete (*C. 5 de Febrero No. 23B*). El sitio anterior decía *5 de Febrero 418*. Confirma cuál es y corrígela en `CONTACT` dentro de `tools/build.py`.
4. **Redes sociales.** No hay enlaces porque no se conocen las URLs. Agrégalos en la función `pie()` de `tools/build.py`.
5. **Textos legales.** Privacidad y términos son borradores; revísalos con asesoría legal.
6. **Horarios y precios.** Agrega horarios de atención y, si quieres, tarifas.
7. **Imagen para redes.** `images/og-fabjardin.png` aparece al compartir el enlace. Puedes reemplazarla.

## Publicación

El workflow `.github/workflows/pages.yml` publica el sitio en cada push a `main`. En **Settings → Pages**, el origen debe ser **GitHub Actions**.

### Dominio fabjardin.com

1. Crea un archivo `CNAME` en la raíz con una sola línea: `fabjardin.com`.
2. En tu proveedor de DNS apunta el dominio a GitHub Pages (registros `A` a `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, y un `CNAME` de `www` a `Saulovzky.github.io`). Verifica estos valores en la [documentación de GitHub](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site).
3. En **Settings → Pages → Custom domain** escribe `fabjardin.com` y activa **Enforce HTTPS**.

No cambies el DNS hasta tener el sitio verificado: mientras tanto, el sitio actual sigue funcionando.
