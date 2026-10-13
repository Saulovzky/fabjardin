(function () {
  "use strict";
  var cfg = window.FABJARDIN || {};

  /* ---- Menú móvil ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("menu-principal");
  function setMenu(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".material-symbols-outlined").textContent = open ? "close" : "menu";
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    window.matchMedia("(min-width: 961px)").addEventListener("change", function () { setMenu(false); });
  }

  /* ---- Año del pie ---- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  /* ---- Aparición al hacer scroll ---- */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Imágenes de servicios: si falta el archivo, se muestra el ícono ---- */
  document.querySelectorAll(".service-media img").forEach(function (img) {
    img.addEventListener("error", function () { img.remove(); });
  });

  /* ---- Formulario de cotización ---- */
  var form = document.getElementById("form-cotizacion");
  if (!form) return;
  var status = document.getElementById("form-status");

  // Preselecciona el servicio si viene en la URL: contacto.html?servicio=Router%20CNC
  var param = new URLSearchParams(location.search).get("servicio");
  if (param) {
    var sel = form.querySelector("select[name=servicio]");
    Array.prototype.forEach.call(sel.options, function (o) { if (o.value === param) sel.value = param; });
  }

  function show(msg, ok) {
    status.textContent = msg;
    status.className = "form-status " + (ok ? "ok" : "err");
    status.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.querySelector("[name=_gotcha]").value) return; // antispam
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var data = {};
    new FormData(form).forEach(function (v, k) { if (k !== "_gotcha") data[k] = v; });

    if (cfg.formEndpoint) {
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      fetch(cfg.formEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        form.reset();
        show("¡Gracias! Recibimos tu solicitud y te responderemos pronto.", true);
      }).catch(function () {
        show("No pudimos enviar el formulario. Escríbenos a " + cfg.email + " o por WhatsApp.", false);
      }).finally(function () { btn.disabled = false; });
      return;
    }

    // Sin endpoint configurado: abre el correo con los datos.
    var cuerpo = [
      "Nombre: " + data.nombre,
      "Email: " + data.email,
      "Teléfono: " + (data.telefono || "—"),
      "Servicio: " + data.servicio,
      "Urgencia: " + data.urgencia,
      "Enlace a archivos: " + (data.archivos || "—"),
      "",
      "Descripción del proyecto:",
      data.descripcion
    ].join("\n");
    location.href = "mailto:" + cfg.email +
      "?subject=" + encodeURIComponent("Solicitud de cotización: " + data.servicio) +
      "&body=" + encodeURIComponent(cuerpo);
    show("Abrimos tu programa de correo con la solicitud lista para enviar.", true);
  });

  var wa = document.getElementById("btn-whatsapp");
  if (wa && cfg.whatsapp) {
    wa.href = "https://wa.me/" + cfg.whatsapp + "?text=" +
      encodeURIComponent("Hola, quiero cotizar un proyecto en Fabjardin.");
  }
})();
