#!/usr/bin/env python3
"""Genera el QR (PNG + SVG) y el archivo de contacto .vcf de una tarjeta virtual.

Requisitos: Python 3, `qrcode` y `Pillow` ya instalados (este script no instala nada).
No se conecta a ninguna red; solo escribe en la carpeta de salida.

Ejemplo:
  python3 -I generar_qr_vcard.py \
    --url "https://midominio.com/tarjeta/?origen=qr" \
    --nombre "Ana" --apellido "Pérez" --cargo "Fotógrafa" \
    --telefono "+573001112233" --web "https://midominio.com" \
    --nota "Servicios en Bogotá, Colombia." \
    --foto public/images/retratos/ana.jpg \
    --salida-qr public/qr --salida-vcf public/ana-perez.vcf
"""
import argparse, base64, io, os, re, sys

try:
    import qrcode, qrcode.image.svg
    from PIL import Image
except ImportError as e:  # sin instalar nada por cuenta propia
    sys.exit(f"Falta una librería ({e.name}). Instálala tú: pip install qrcode pillow")


def plegar(linea):
    """RFC 6350: las líneas se pliegan a 75 caracteres; las siguientes empiezan con un espacio."""
    partes = []
    while len(linea) > 75:
        partes.append(linea[:75])
        linea = " " + linea[75:]
    partes.append(linea)
    return "\r\n".join(partes)


def escapar(texto):
    return texto.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def crear_qr(url, carpeta, color, nombre_base):
    os.makedirs(carpeta, exist_ok=True)
    # Corrección Q: aguanta ensuciarse o imprimirse pequeño sin perder lectura.
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=40, border=4)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert("RGB")
    img.save(os.path.join(carpeta, nombre_base + ".png"), optimize=True)

    v = qrcode.QRCode(version=qr.version, error_correction=qrcode.constants.ERROR_CORRECT_Q,
                      box_size=10, border=4, image_factory=qrcode.image.svg.SvgPathImage)
    v.add_data(url); v.make(fit=True)
    buf = io.BytesIO(); v.make_image().save(buf)
    svg = buf.getvalue().decode()
    svg = svg.replace('fill="#000000"', f'fill="{color}"')
    lado = re.search(r'viewBox="0 0 (\d+) ', svg).group(1)
    # fondo blanco propio: así se ve igual sobre fondo oscuro y al imprimir
    svg = svg.replace("<path ", f'<rect width="{lado}" height="{lado}" fill="#ffffff"/><path ', 1)
    svg = svg.replace("<svg ", '<svg role="img" aria-label="Código QR" ', 1)
    with open(os.path.join(carpeta, nombre_base + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    return qr.modules_count


def crear_vcf(args):
    lineas = ["BEGIN:VCARD", "VERSION:3.0",
              f"N:{escapar(args.apellido)};{escapar(args.nombre)};;;",
              f"FN:{escapar(args.nombre + ' ' + args.apellido)}"]
    if args.cargo: lineas.append(f"TITLE:{escapar(args.cargo)}")
    if args.telefono: lineas.append(f"TEL;TYPE=CELL,VOICE:{args.telefono}")
    if args.web: lineas.append(f"URL:{args.web}")
    if args.correo: lineas.append(f"EMAIL;TYPE=INTERNET:{args.correo}")
    if args.nota: lineas.append(f"NOTE:{escapar(args.nota)}")
    if args.foto:
        im = Image.open(args.foto).convert("RGB")
        w, h = im.size; lado = min(w, h)
        im = im.crop(((w - lado) // 2, 0, (w - lado) // 2 + lado, lado)).resize((240, 240), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=80)
        lineas.append("PHOTO;ENCODING=b;TYPE=JPEG:" + base64.b64encode(b.getvalue()).decode())
    lineas.append("END:VCARD")
    os.makedirs(os.path.dirname(os.path.abspath(args.salida_vcf)), exist_ok=True)
    with open(args.salida_vcf, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(plegar(l) for l in lineas) + "\r\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", required=True, help="Dirección que abre el QR (con ?origen=qr para medir escaneos)")
    p.add_argument("--nombre", required=True); p.add_argument("--apellido", required=True)
    p.add_argument("--cargo"); p.add_argument("--telefono"); p.add_argument("--web"); p.add_argument("--correo")
    p.add_argument("--nota"); p.add_argument("--foto", help="Retrato; se recorta cuadrado a 240 px")
    p.add_argument("--color-qr", default="#061f3c", help="Tinta del QR (oscura, contraste alto sobre blanco)")
    p.add_argument("--salida-qr", required=True, help="Carpeta donde dejar qr-tarjeta.png y qr-tarjeta.svg")
    p.add_argument("--salida-vcf", required=True, help="Ruta del archivo .vcf")
    args = p.parse_args()
    modulos = crear_qr(args.url, args.salida_qr, args.color_qr, "qr-tarjeta")
    crear_vcf(args)
    print(f"QR de {modulos}x{modulos} módulos en {args.salida_qr}; contacto en {args.salida_vcf}")


if __name__ == "__main__":
    main()
