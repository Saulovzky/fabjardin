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

  /* ---- Asistente: ¿qué necesitas y podemos hacerlo? ---- */
  var app = document.getElementById("guia-app");
  var datos = document.getElementById("guia-datos");
  if (app && datos) {
    var arbol;
    try { arbol = JSON.parse(datos.textContent); } catch (e) { arbol = null; }
    if (arbol) {
      var wa = "https://wa.me/" + (cfg.whatsapp || "") + "?text=" +
        encodeURIComponent("Hola, quiero saber si pueden ayudarme con mi proyecto en Fabjardin.");
      var el = function (tag, clase, texto) {
        var n = document.createElement(tag);
        if (clase) n.className = clase;
        if (texto !== undefined) n.textContent = texto;
        return n;
      };
      var pila = [arbol];
      var pintar = function (enfocar) {
        var nodo = pila[pila.length - 1];
        app.textContent = "";
        var paso = el("div", "guia-paso");
        if (nodo.res) {
          var r = nodo.res;
          paso.appendChild(el("p", "guia-si", r.si));
          var t = el("h3", "guia-titulo", r.titulo);
          t.tabIndex = -1;
          paso.appendChild(t);
          paso.appendChild(el("p", "guia-texto", r.texto));
          if (r.items.length) {
            var lista = el("div", "maquinas");
            r.items.forEach(function (it) {
              var c = el("div", "maq");
              c.appendChild(el("h4", "", it.m));
              var dl = el("dl");
              [["Trabaja con", it.con], ["Sirve para", it.para]].forEach(function (par) {
                var d = el("div"); d.appendChild(el("dt", "", par[0])); d.appendChild(el("dd", "", par[1])); dl.appendChild(d);
              });
              c.appendChild(dl);
              var a = el("a", "cotizar", "Cotizar"); a.href = it.cot; c.appendChild(a);
              lista.appendChild(c);
            });
            paso.appendChild(lista);
          }
          var fila = el("div", "fila-botones");
          r.ctas.forEach(function (c, i) {
            var a = el("a", "boton " + (i === 0 ? "boton--lima" : "boton--borde-claro"), c.l);
            a.href = c.h === "wa" ? wa : c.h;
            if (c.h === "wa") { a.target = "_blank"; a.rel = "noopener"; }
            fila.appendChild(a);
          });
          paso.appendChild(fila);
          var nav = el("div", "guia-nav");
          var atras = el("button", "guia-link", "← Cambiar mi respuesta"); atras.type = "button";
          atras.addEventListener("click", function () { pila.pop(); pintar(true); });
          var reinicio = el("button", "guia-link", "Empezar de nuevo"); reinicio.type = "button";
          reinicio.addEventListener("click", function () { pila = [arbol]; pintar(true); });
          nav.appendChild(atras); nav.appendChild(reinicio);
          paso.appendChild(nav);
          app.appendChild(paso);
          if (enfocar) t.focus({ preventScroll: true });
          return;
        }
        var h = el("h3", "guia-pregunta", nodo.q);
        h.tabIndex = -1;
        paso.appendChild(h);
        var opciones = el("div", "guia-opciones");
        nodo.o.forEach(function (o) {
          var b = el("button", "opc"); b.type = "button";
          b.appendChild(el("span", "opc-t", o.t));
          if (o.d) b.appendChild(el("span", "opc-d", o.d));
          b.addEventListener("click", function () { pila.push(o.n || o); pintar(true); });
          opciones.appendChild(b);
        });
        paso.appendChild(opciones);
        if (pila.length > 1) {
          var nv = el("div", "guia-nav");
          var volver = el("button", "guia-link", "← Volver"); volver.type = "button";
          volver.addEventListener("click", function () { pila.pop(); pintar(true); });
          nv.appendChild(volver);
          paso.appendChild(nv);
        }
        app.appendChild(paso);
        if (enfocar) h.focus({ preventScroll: true });
      };
      pintar(false);
    }
  }

  /* ---- Educación: "otro tema" se graba con láser y se puede enviar por correo ---- */
  var formTema = document.getElementById("form-tema");
  var listaTemas = document.getElementById("temas");
  if (formTema && listaTemas) {
    var contador = 0;
    var entrada = document.getElementById("tema-nuevo");
    formTema.addEventListener("submit", function (e) {
      e.preventDefault();
      var texto = entrada.value.replace(/\s+/g, " ").trim();
      if (!texto) { entrada.focus(); return; }
      var li = document.createElement("li");
      li.className = "nuevo grabando c" + (contador++ % 5);
      var t = document.createElement("span");
      t.className = "txt";
      t.textContent = texto;
      var rayo = document.createElement("span");
      rayo.className = "rayo-grabado";
      rayo.setAttribute("aria-hidden", "true");
      li.appendChild(t);
      li.appendChild(rayo);
      var enviar = document.createElement("a");
      enviar.className = "enviar-tema";
      enviar.textContent = "Enviarlo a Fabjardin ↗";
      enviar.href = "mailto:" + (cfg.email || "") + "?subject=" + encodeURIComponent("Tema que quiero aprender: " + texto) +
        "&body=" + encodeURIComponent("Hola, me gustaría aprender sobre: " + texto);
      li.appendChild(enviar);
      listaTemas.insertBefore(li, formTema.parentNode);
      entrada.value = "";
      setTimeout(function () { li.classList.remove("grabando"); li.classList.add("listo"); }, 1900);
    });
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

/* Equipos: nombre -> detalle (hover/foco en escritorio, toque en móvil) */
(function () {
  var cont = document.getElementById("equipos");
  if (!cont) return;
  var items = Array.prototype.slice.call(cont.querySelectorAll(".eq"));
  var escritorio = window.matchMedia("(min-width: 900px)");
  var conHover = window.matchMedia("(hover: hover)");
  cont.classList.add("js");
  function poner(item, abierto) {
    item.classList.toggle("on", abierto);
    item.querySelector(".eq-b").setAttribute("aria-expanded", abierto ? "true" : "false");
  }
  function activar(item) { items.forEach(function (i) { poner(i, i === item); }); }
  items.forEach(function (item) {
    var b = item.querySelector(".eq-b");
    b.addEventListener("mouseenter", function () { if (escritorio.matches && conHover.matches) activar(item); });
    b.addEventListener("focus", function () { if (escritorio.matches) activar(item); });
    b.addEventListener("click", function () {
      if (escritorio.matches) activar(item);
      else poner(item, !item.classList.contains("on"));
    });
  });
  function inicial() { if (escritorio.matches) { if (!cont.querySelector(".eq.on")) activar(items[0]); } else { items.forEach(function (i) { poner(i, false); }); } }
  if (escritorio.addEventListener) escritorio.addEventListener("change", inicial); else escritorio.addListener(inicial);
  inicial();
})();

/* Nosotros: la palabra "centro" cambia a sus sinónimos con un destello */
(function () {
  var el = document.querySelector(".flash[data-palabras]");
  if (!el) return;
  var lista = el.getAttribute("data-palabras").split(",");
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || lista.length < 2) return;
  var i = 0;
  setInterval(function () {
    i = (i + 1) % lista.length;
    el.classList.remove("cambia"); void el.offsetWidth; el.classList.add("cambia");
    setTimeout(function () { el.textContent = lista[i]; }, 120);
  }, 1500);
})();
