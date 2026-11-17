import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// output por defecto queda en "static" — no agregar adapter salvo que el
// proyecto necesite SSR real (formularios y automatizaciones van por
// proxy PHP o GitHub Actions, no requieren servidor Astro en producción).
export default defineConfig({
  // Por defecto, el dominio propio del cliente (sitio en la raíz).
  // La demo define PUBLIC_SITE y PUBLIC_BASE al compilar:
  // PUBLIC_SITE=https://demos.emp2web.com PUBLIC_BASE=/electricistacertificado
  site: process.env.PUBLIC_SITE || "https://electricistascertificadosbogota.com",
  base: process.env.PUBLIC_BASE || "/",
  // barra de desarrollo de Astro desactivada: no debe verse en la vista previa
  devToolbar: { enabled: false },
  vite: {
    plugins: [tailwindcss()],
  },
});
