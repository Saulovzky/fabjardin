(function () {
  "use strict";
  var cfg = window.FABJARDIN || {};

  /* ---- Menú en pantallas chicas ---- */
  var boton = document.querySelector(".boton-menu");
  var nav = document.getElementById("menu-principal");
  function menu(abrir) {
    nav.classList.toggle("abierto", abrir);
    document.body.classList.toggle("menu-abierto", abrir);
    boton.setAttribute("aria-expanded", String(abrir));
    boton.textContent = abrir ? "Cerrar" : "Menú";
  }
  if (boton && nav) {
    boton.addEventListener("click", function () { menu(!nav.classList.contains("abierto")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) menu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") menu(false); });
    window.matchMedia("(min-width: 1181px)").addEventListener("change", function () { menu(false); });
  }

  /* ---- Hora en Chalco ---- */
  var reloj = document.getElementById("reloj");
  function hora() {
    try {
      reloj.textContent = "Chalco " + new Intl.DateTimeFormat("es-MX", {
        hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "America/Mexico_City"
      }).format(new Date());
    } catch (e) { /* sin Intl se queda el texto fijo */ }
  }
  if (reloj) { hora(); setInterval(hora, 30000); }

  /* ---- Año del pie ---- */
  var anio = document.getElementById("anio");
  if (anio) anio.textContent = new Date().getFullYear();

  /* ---- El logo se corta con láser: único momento animado de la portada ---- */
  var pieza = document.getElementById("pieza");
  var rayo = document.getElementById("rayo");
  if (pieza && rayo && pieza.getTotalLength &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var largo = pieza.getTotalLength();
    var DURACION = 2800;   // recorrido del rayo
    var CAIDA = 700;       // la pieza se rellena al terminar

    pieza.style.fill = "transparent";
    pieza.style.stroke = "#001c72";
    pieza.style.strokeWidth = "2.5";
    pieza.style.strokeLinejoin = "round";
    pieza.style.strokeDasharray = largo;
    pieza.style.strokeDashoffset = largo;
    rayo.style.opacity = "1";

    var suavizar = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
    var inicio = null;
    var cuadro = function (ahora) {
      if (inicio === null) inicio = ahora;
      var t = Math.min((ahora - inicio) / DURACION, 1);
      var p = suavizar(t);
      var punto = pieza.getPointAtLength(p * largo);
      pieza.style.strokeDashoffset = largo * (1 - p);
      rayo.setAttribute("cx", punto.x);
      rayo.setAttribute("cy", punto.y);
      if (t < 1) { requestAnimationFrame(cuadro); return; }
      rayo.style.opacity = "0";
      pieza.style.transition = "fill " + CAIDA + "ms ease, stroke-width " + CAIDA + "ms ease";
      pieza.style.fill = "#001c72";
      pieza.style.strokeWidth = "0";
    };
    requestAnimationFrame(cuadro);
  }

  /* ---- Formulario de cotización ---- */
  var form = document.getElementById("form-cotizacion");
  if (!form) return;
  var estado = document.getElementById("form-estado");

  // Preselecciona el servicio si viene en la URL: contacto.html?servicio=Router%20CNC
  var param = new URLSearchParams(location.search).get("servicio");
  if (param) {
    var sel = form.querySelector("select[name=servicio]");
    Array.prototype.forEach.call(sel.options, function (o) { if (o.value === param) sel.value = param; });
  }

  function mostrar(msg, ok) {
    estado.textContent = msg;
    estado.className = "estado " + (ok ? "ok" : "error");
    estado.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.querySelector("[name=_gotcha]").value) return; // antispam
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var datos = {};
    new FormData(form).forEach(function (v, k) { if (k !== "_gotcha") datos[k] = v; });

    if (cfg.formEndpoint) {
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(datos)
      }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        form.reset();
        mostrar("Recibimos tu solicitud. Te respondemos pronto.", true);
      }).catch(function () {
        mostrar("No pudimos enviar el formulario. Escríbenos a " + cfg.email + " o por WhatsApp.", false);
      }).finally(function () { btn.disabled = false; });
      return;
    }

    // Sin endpoint configurado: abre el correo con los datos ya escritos.
    var cuerpo = [
      "Nombre: " + datos.nombre,
      "Email: " + datos.email,
      "Teléfono: " + (datos.telefono || "—"),
      "Servicio: " + datos.servicio,
      "Urgencia: " + datos.urgencia,
      "Enlace a archivos: " + (datos.archivos || "—"),
      "",
      "Descripción del proyecto:",
      datos.descripcion
    ].join("\n");
    location.href = "mailto:" + cfg.email +
      "?subject=" + encodeURIComponent("Solicitud de cotización: " + datos.servicio) +
      "&body=" + encodeURIComponent(cuerpo);
    mostrar("Abrimos tu programa de correo con la solicitud lista para enviar.", true);
  });

  var wa = document.getElementById("btn-whatsapp");
  if (wa && cfg.whatsapp) {
    wa.href = "https://wa.me/" + cfg.whatsapp + "?text=" +
      encodeURIComponent("Hola, quiero cotizar un proyecto en Fabjardin.");
  }
})();
