# Tarjeta de presentación virtual

Página aparte, pensada para abrirse desde un código QR en el celular. Es una sola tarjeta que
se lee de arriba abajo: **sin menú, sin cabecera de sitio y sin pie de navegación**.

- **Dirección en producción:** https://electricistascertificadosbogota.com/tarjeta/
- **Dirección que lleva el QR:** `https://electricistascertificadosbogota.com/tarjeta/?origen=qr`
  (el `?origen=qr` no cambia nada en pantalla; sirve para distinguir en las estadísticas
  quién entró por el QR).
- **En la demo:** https://demos.emp2web.com/electricistacertificado/tarjeta/
- Lleva `noindex`: Google no la lista, para que siga mostrando el sitio principal.

## Qué muestra (de arriba abajo)

1. Cabezote azul con el escudo, una trama de circuito y el botón de modo oscuro.
2. Foto, nombre, cargo y zona. La foto cruza el borde del cabezote.
3. **Escribir por WhatsApp** (botón principal) y tres accesos: **Llamar**, **Guardar
   contacto** (descarga el `.vcf`) y **Compartir** (menú del celular o copia el enlace).
4. **Servicios** como tablero de breakers: la persona marca lo que necesita y aparece una
   barra abajo con "Enviar consulta por WhatsApp", que abre el chat con el mensaje armado.
5. Sobre mí, Cómo trabajo, Contacto (WhatsApp, cobertura y sitio web), botón
   **Ver mi página web** y el QR para compartir la tarjeta.
6. Crédito: "Tarjeta desarrollada por emp2web".

Claro por defecto; el oscuro solo si la persona pulsa el botón (se recuerda en su navegador).
Nunca sigue la preferencia del sistema.

## Archivos

| Archivo | Para qué |
| --- | --- |
| `src/pages/tarjeta.astro` | La página. No lleva texto escrito: todo sale de los JSON. Trae también el script del tablero y del botón Compartir. |
| `src/layouts/LayoutTarjeta.astro` | Estructura mínima: sin menú. Pone `noindex`, la fuente, el tema claro/oscuro y las etiquetas para compartir en redes. |
| `src/styles/tarjeta.css` | Estilos de la tarjeta (usa los mismos tokens de `global.css`). La trama del cabezote es un SVG embebido en `.t-cabecera::before`. |
| `src/styles/animaciones.css` | Movimiento compartido con el sitio. |
| `src/scripts/movimiento.js` | Aparición al bajar (`.t-bloque`, `.t-tablero > li`, `.t-pasos li`, `.t-qr`). |
| `src/datos/tarjeta.json` | Textos propios de la tarjeta. |
| `src/datos/inicio.json` | De aquí salen los **servicios** (`servicios.items`), el texto de **Sobre mí** (`nosotros`), los **pasos** (`proceso.pasos`) y el teléfono (`contacto.telefono`). Cambiarlos allí cambia sitio y tarjeta a la vez. |
| `src/datos/sitio.json` | Nombre, WhatsApp, créditos, clave del tema. |
| `public/jhon-jairo-espinosa.vcf` | Contacto que se descarga con "Guardar contacto". |
| `public/qr/qr-tarjeta.png` | QR en alta resolución (1960 px) para imprimir. |
| `public/qr/qr-tarjeta.svg` | QR vectorial para imprenta; lleva fondo blanco propio. |
| `herramientas/generar-qr-vcard.py` | Regenera el QR y el `.vcf`. |

## Cómo se cambian las cosas

- **Un texto, el cargo, la zona o el mensaje de WhatsApp:** `src/datos/tarjeta.json`.
- **Un servicio nuevo o un precio de texto:** `src/datos/inicio.json` → `servicios.items`
  (aparece en la tarjeta y en el sitio).
- **La foto:** reemplazar `public/images/retratos/jhon-jairo-uniforme.jpg` (o cambiar la ruta
  en `tarjeta.json` → `perfil.imagen`). Después **regenerar el `.vcf`**, porque lleva una
  copia de la foto.
- **El teléfono:** `src/datos/sitio.json` → `whatsapp` (solo números, con indicativo, sin `+`).
  Después regenerar el `.vcf`.

## Cómo se generaron el QR y el contacto

Con el script de `herramientas/`. Necesita Python 3 con `qrcode` y `Pillow` ya instalados
(el script no instala nada ni usa internet):

```bash
python3 -I herramientas/generar-qr-vcard.py \
  --url "https://electricistascertificadosbogota.com/tarjeta/?origen=qr" \
  --nombre "Jhon Jairo" --apellido "Espinosa" \
  --cargo "Electricista certificado" \
  --telefono "+573112958692" \
  --web "https://electricistascertificadosbogota.com" \
  --nota "Servicios eléctricos en Bogotá, Colombia. Escribe por WhatsApp." \
  --foto public/images/retratos/jhon-jairo-uniforme.jpg \
  --salida-qr public/qr --salida-vcf public/jhon-jairo-espinosa.vcf
```

Decisiones del QR: corrección de errores nivel Q (aguanta suciedad o impresión pequeña),
tinta azul marino oscura `#061f3c` sobre blanco (contraste alto), 4 módulos de borde
blanco (zona silenciosa obligatoria), 41×41 módulos.

Decisiones del contacto: versión 3.0 de vCard (la lee Android, iPhone y Google Contactos),
foto cuadrada de 240 px en base64, líneas plegadas a 75 caracteres, **sin correo ni
dirección** porque no están confirmados.

## Si cambia el dominio

El QR **lleva la dirección dentro**: si el dominio cambia, hay que regenerarlo y reimprimir.
Mientras el dominio sea el mismo, la tarjeta puede cambiar de diseño o de datos sin tocar
el QR. Por eso conviene probar el dominio definitivo antes de imprimir en cantidad.

## Cómo está construida (decisiones)

- **Una sola fuente de datos.** Servicios, proceso y "Sobre mí" se leen de `inicio.json`
  para que la tarjeta y el sitio nunca se contradigan.
- **El tablero de breakers** es la misma idea del sitio (cada servicio es un breaker que se
  enciende), en versión compacta. Cada fila es un `<button role="switch" aria-checked>`:
  funciona con teclado y lector de pantalla. La barra de abajo usa `inert` mientras está
  oculta para que no reciba el foco.
- **Compartir:** usa `navigator.share` si existe (menú nativo del celular); si no, copia el
  enlace sin el `?origen=qr` y cambia la etiqueta a "Enlace copiado" dos segundos.
- **Movimiento:** la foto salta al abrir, el texto y los botones suben por partes, y las
  secciones aparecen al bajar. Todo con `transform` y `opacity`, apagado con "reducir
  movimiento", y nada queda oculto si el script falla (lo que oculta depende de la clase
  `.js` que pone la cabecera).
- **Trama del cabezote:** pistas de circuito en ángulo recto con nodos, en blanco al 15 % y
  algunos nodos amarillos. Está como SVG dentro del CSS (sin archivo extra, sin peticiones).
- **Responsive:** en celular ocupa todo el ancho; desde 600 px es una tarjeta de 30 rem
  centrada sobre un fondo gris claro.

## Qué no hace

- No tiene formulario, ni correo, ni dirección, ni horarios, ni precios: no están
  confirmados (ver `PENDIENTES.md` y el manual de marca).
- No cuenta escaneos por sí sola: solo marca el `?origen=qr` para que lo vea la herramienta
  de estadísticas que se instale en el sitio.
- El QR no se prueba con cámara en este repositorio: **escanearlo una vez ya publicado**.

## Lista de comprobación antes de imprimir

- [ ] La tarjeta abre en `https://electricistascertificadosbogota.com/tarjeta/` (publicada).
- [ ] Escanear `public/qr/qr-tarjeta.png` desde la pantalla con un celular Android y uno iPhone.
- [ ] "Escribir por WhatsApp", "Llamar", "Guardar contacto" y "Compartir" funcionan.
- [ ] Marcar dos servicios y comprobar el mensaje que llega a WhatsApp.
- [ ] Imprimir una prueba al tamaño final (mínimo 2,5 × 2,5 cm de QR) y escanearla.
