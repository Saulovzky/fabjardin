(function () {
  "use strict";

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
    window.matchMedia("(min-width: 961px)").addEventListener("change", function () { menu(false); });
  }

  /* ---- Hora en Chalco ---- */
  var reloj = document.getElementById("reloj");
  function hora() {
    try {
      reloj.textContent = "Chalco " + new Intl.DateTimeFormat("es-MX", {
        hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "America/Mexico_City"
      }).format(new Date());
    } catch (e) { /* sin Intl: se queda el texto fijo */ }
  }
  if (reloj) { hora(); setInterval(hora, 30000); }

  /* ---- Año del pie ---- */
  var anio = document.getElementById("anio");
  if (anio) anio.textContent = new Date().getFullYear();

  /* ---- El logo se corta con láser: único momento animado de la portada ---- */
  var pieza = document.getElementById("pieza");
  var rayo = document.getElementById("rayo");
  if (!pieza || !rayo || !pieza.getTotalLength) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

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

  function suavizar(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  var inicio = null;

  function cuadro(ahora) {
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
  }
  requestAnimationFrame(cuadro);
})();
