/**
 * Prefija las rutas internas con la carpeta donde vive el sitio.
 *
 * La demo se publica en una subcarpeta (demos.emp2web.com/electricistacertificado/),
 * así que un enlace escrito como `/servicios` o una imagen `/images/x.jpg`
 * apuntaría fuera del sitio. Esta función antepone la carpeta correcta.
 *
 * Cuando el sitio se publique en electricistascertificadosbogota.com, `base`
 * vuelve a `/` en astro.config.mjs y esta función deja de prefijar nada,
 * sin tocar ni un enlace.
 *
 * NO toca los enlaces externos (https://, wa.me, mailto:, tel:) ni las anclas (#).
 */
export function ruta(destino: string | undefined | null): string {
  if (!destino) return "";

  // Externos y anclas: se dejan tal cual.
  if (/^([a-z]+:|\/\/|#)/i.test(destino)) return destino;

  // Relativos (sin barra inicial): tampoco se tocan.
  if (!destino.startsWith("/")) return destino;

  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  return base + destino;
}
