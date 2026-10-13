# Fabjardin · Centro de Innovación y Tecnologías Creativas

Sitio web estático (HTML + CSS + JS, sin frameworks) listo para publicarse en **GitHub Pages**.

## Estructura

```
index.html                 Inicio
nosotros.html              Quiénes somos · Impacto · Red FabLab
laboratorio.html           Servicios de fabricación · Equipamiento · Usa el espacio
innovacion.html            I+D · Prototipado · Asesoría y diseño
emprendimiento.html        Acompañamiento · Ruta idea→producto · Mentorías y red
formacion.html             Talleres · BootCamps · Escuelas y jóvenes
comunidad.html             Agenda · Proyectos · Noticias
contacto.html              Formulario de cotización y datos de contacto
politica-de-privacidad.html / terminos-de-los-servicios.html   (borradores)
css/styles.css             Estilos (colores en variables al inicio)
js/config.js               Correo, WhatsApp y endpoint del formulario
js/main.js                 Menú móvil, animaciones, formulario
images/                    Logos, íconos y fotos de servicios
tools/build.py             Generador de las páginas (menú, textos, servicios)
```

## Cómo editar

El menú, el pie de página y los textos viven en `tools/build.py`. Después de cambiar algo:

```bash
python3 tools/build.py
```

Esto regenera todos los `.html`. (También puedes editar un `.html` a mano, pero el siguiente `build.py` lo sobrescribirá.)

## Pendientes antes de publicar

1. **Fotos de servicios.** Copia a `images/servicios/` las imágenes de tu sitio actual con estos nombres (se muestran como ícono hasta que existan):

   | Archivo esperado | Archivo en el sitio actual |
   |---|---|
   | `corte-laser-co2.webp` | `Cortelaserco2-convertido-de-png.webp` |
   | `grabado-laser-uv.webp` | `GrabadoUVyFibra-convertido.webp` |
   | `prensas-de-calor.webp` | `plancha_vinil.webp` |
   | `impresion-3d-filamento.webp` | `Impresion-3D-FDM.webp` |
   | `impresion-3d-resina.webp` | `Impresion-3D_resina-.webp` |
   | `router-cnc.webp` | `routercnc.webp` |
   | `corte-de-vinil.webp` | `Plotter_vinil.webp` |
   | `circuitos.webp` | `Electronica.webp` |
   | `escaner-3d.webp` | `Escáner 3D.webp` |
   | `asesoria-y-diseno.webp` | `Aseosria.webp` |

2. **Formulario de cotización.** GitHub Pages no ejecuta código de servidor. Crea un formulario en [Formspree](https://formspree.io) (o similar) y pega su URL en `js/config.js` → `formEndpoint`. Sin eso, el formulario abre el correo del visitante con los datos ya escritos. Los archivos se comparten por enlace (Drive, Dropbox), porque la subida directa requiere un plan de pago en la mayoría de estos servicios.
3. **Dirección.** El sitio usa la del membrete (*C. 5 de Febrero No. 23*). El sitio anterior decía *5 de Febrero 418*. Confirma cuál es la correcta y corrígela en `CONTACT` dentro de `tools/build.py`.
4. **Redes sociales.** No hay enlaces porque no se conocen las URLs. Agrégalos en el pie de página (`footer_html` en `tools/build.py`).
5. **Textos legales.** Las páginas de privacidad y términos son borradores; revísalos con asesoría legal.
6. **Imagen para redes.** `images/og-fabjardin.png` es la que aparece al compartir el enlace. Cámbiala por una más elaborada si quieres.
7. **Horarios y precios.** Agrega horarios de atención y, si lo deseas, una tabla de tarifas.

## Publicar en GitHub Pages

1. Crea un repositorio nuevo en GitHub (por ejemplo `fabjardin-web`) y sube estos archivos a la rama `main`:
   ```bash
   git init -b main
   git add .
   git commit -m "Sitio Fabjardin"
   git remote add origin https://github.com/TU-USUARIO/fabjardin-web.git
   git push -u origin main
   ```
2. En GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. El workflow `.github/workflows/pages.yml` publica el sitio en cada push. La primera dirección será `https://TU-USUARIO.github.io/fabjardin-web/`.

> Las rutas del sitio son relativas, así que funciona igual en `usuario.github.io/repositorio/` y en tu dominio propio.

## Usar el dominio fabjardin.com

1. Crea un archivo `CNAME` en la raíz con una sola línea: `fabjardin.com`.
2. En tu proveedor de DNS, apunta el dominio a GitHub Pages (registros `A` a `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, y un `CNAME` de `www` a `TU-USUARIO.github.io`). Verifica estos valores en la [documentación de GitHub](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site).
3. En **Settings → Pages → Custom domain** escribe `fabjardin.com` y activa **Enforce HTTPS**.

No cambies el DNS hasta tener el sitio nuevo verificado: mientras tanto, el sitio actual sigue funcionando.
