# Dónde se publica

Este código vive en dos repositorios. El flujo `.github/workflows/deploy.yml` decide solo
el destino comparando el repositorio donde corre.

| Repositorio | URL | Qué es |
| --- | --- | --- |
| `Gestiona2/electricistacertificado` | https://demos.emp2web.com/electricistacertificado/ | Demo para mostrar y aprobar |
| `espinosaceballosjhonjairo-eng/pagina-web` | https://electricistascertificadosbogota.com | Sitio definitivo del cliente |

## Cómo se resuelven las rutas

La demo vive en una subcarpeta, así que las rutas internas (`/images/...`, `/brand/...`,
enlaces a `/`) no pueden escribirse fijas: apuntarían a la raíz de `demos.emp2web.com`.

- Los archivos `.astro` pasan esas rutas por `ruta()` (`src/lib/ruta.ts`), que antepone
  la carpeta del sitio cuando existe.
- `astro.config.mjs` toma `PUBLIC_SITE` y `PUBLIC_BASE` del entorno; si no existen, usa el
  dominio del cliente en la raíz.
- El flujo de la demo borra `dist/CNAME` antes de subir: ese archivo le pondría el dominio
  del cliente a la demo y rompería `demos.emp2web.com`.

## Publicar la demo a mano

```bash
git push demo main
```

El flujo "Publicar" compila y sube a GitHub Pages. Tarda un minuto.

## Cuando el cliente tenga su dominio

No hay nada que cambiar en el código: el mismo push al repositorio del cliente compila con
`PUBLIC_BASE=/`. Lo único pendiente es el DNS (registros A de GitHub Pages y CNAME de
`www`) y activar "Enforce HTTPS" en Settings → Pages.
