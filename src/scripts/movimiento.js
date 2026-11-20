/* Movimiento: sombra de la cabecera y aparición de secciones al bajar.
   No oculta nada si el navegador no soporta IntersectionObserver o si la persona pidió menos movimiento. */
(function () {
  var raiz = document.documentElement;
  if (!raiz.classList.contains("js")) return;

  /* sombra de la cabecera */
  var cabecera = document.getElementById("cabecera");
  if (cabecera) {
    var sombra = function () { cabecera.classList.toggle("elevada", window.scrollY > 8); };
    window.addEventListener("scroll", sombra, { passive: true });
    sombra();
  }

  var calmado = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (calmado || !("IntersectionObserver" in window)) {
    document.querySelectorAll(".pasos, .t-pasos").forEach(function (el) { el.classList.add("visto"); });
    return;
  }

  /* [selector, retraso entre hermanos en segundos] */
  var grupos = [
    [".servicios-lateral", 0],
    [".tablero > li", 0.06],
    [".proceso header", 0],
    [".pasos li", 0.2],
    [".trabajos-cabecera", 0],
    [".grupo-cabecera", 0],
    [".galeria .foto", 0.08],
    [".retrato", 0],
    [".nosotros-texto", 0.12],
    [".faq h2", 0],
    [".faq details", 0.07],
    [".contacto-grid > div", 0.15],
    [".pie-nombre", 0],
    [".pie-columnas > div", 0.1],
    /* tarjeta virtual */
    [".t-bloque", 0],
    [".t-tablero > li", 0.05],
    [".t-pasos li", 0.12],
    [".t-qr", 0]
  ];

  var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("visto");
      observador.unobserve(e.target);
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });

  function yaEnPantalla(el) {
    var r = el.getBoundingClientRect();
    return r.top < window.innerHeight * 0.92 && r.bottom > 0;
  }

  grupos.forEach(function (g) {
    var cuenta = new Map();
    document.querySelectorAll(g[0]).forEach(function (el) {
      if (yaEnPantalla(el)) return;
      var padre = el.parentElement;
      var i = cuenta.get(padre) || 0;
      cuenta.set(padre, i + 1);
      el.style.setProperty("--d", Math.min(i * g[1], 0.5) + "s");
      el.classList.add("reveal");
      observador.observe(el);
    });
  });

  /* la línea del proceso se dibuja cuando aparece */
  document.querySelectorAll(".pasos, .t-pasos").forEach(function (el) {
    if (yaEnPantalla(el)) { el.classList.add("visto"); return; }
    observador.observe(el);
  });
})();
