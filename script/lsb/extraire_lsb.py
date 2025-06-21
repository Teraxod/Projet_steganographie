#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import os
from PIL import Image
import io
import base64
import sys

cgitb.enable()

def lsb_diff_img(img1, img2):
    w, h = img1.size
    diff_img = Image.new('RGB', (w, h))
    px1 = img1.load()
    px2 = img2.load()
    px_out = diff_img.load()
    for y in range(h):
        for x in range(w):
            r = 255 if (px1[x, y][0] & 1) != (px2[x, y][0] & 1) else 0
            g = 255 if (px1[x, y][1] & 1) != (px2[x, y][1] & 1) else 0
            b = 255 if (px1[x, y][2] & 1) != (px2[x, y][2] & 1) else 0
            px_out[x, y] = (r, g, b)
    return diff_img

def extraire_message_lsb(img):
    largeur, hauteur = img.size
    pixels = img.load()
    bits = []
    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y]
            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))
    longueur_bits = bits[:32]
    longueur = int(''.join(longueur_bits), 2)
    message_bits = bits[32:32 + longueur * 8]
    chars = []
    for i in range(0, len(message_bits), 8):
        octet = message_bits[i:i+8]
        if len(octet) < 8:
            break
        chars.append(chr(int(''.join(octet), 2)))
    return ''.join(chars)

print("Content-Type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
action = form.getfirst("action", "")

def html_error(msg):
    print(f"<html><body style='color:red;text-align:center;padding-top:30px;'><h2>Erreur : {msg}</h2><a href='/index.html'>Retour à l'accueil</a></body></html>")
    sys.exit(0)

if action == "diff":
    img1_item = form["img1"] if "img1" in form else None
    img2_item = form["img2"] if "img2" in form else None
    output = form.getfirst("output", "lsb_diff.png")

    if not (hasattr(img1_item, "file") and hasattr(img2_item, "file")):
        html_error("Images non reçues")
    try:
        img1 = Image.open(img1_item.file).convert("RGB")
        img2 = Image.open(img2_item.file).convert("RGB")
    except Exception as e:
        html_error(f"Erreur chargement image : {e}")
    if img1.size != img2.size:
        html_error("Les images doivent être de même taille !")
    diff_img = lsb_diff_img(img1, img2)

    buf = io.BytesIO()
    diff_img.save(buf, format="PNG")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    # Sauvegarde sur le serveur si besoin
    diff_img.save(f"/var/www/html/{output}")

    print(f"""
    <!DOCTYPE html>
    <html lang="fr"><head><meta charset="UTF-8"><title>Différence LSB</title>
    <style>
        body {{ background:#121212; color:#e0e0e0; text-align:center; font-family:Arial,sans-serif; }}
        img {{ max-width:600px; margin:24px; border-radius:8px; box-shadow: 0 4px 32px #000a; }}
        a {{ color: #80cbc4; font-weight: bold; }}
    </style>
    </head>
    <body>
        <h1>🖼️ Différences LSB entre les deux images</h1>
        <img src="data:image/png;base64,{img_b64}" alt="diff lsb"><br>
        <a href="/{output}" download="{output}">⬇️ Télécharger l'image de différence</a><br>
        <a href="/index.html">← Retour à l'accueil</a>
    </body>
    </html>
    """)

elif action == "extract":
    img_item = form["img_extract"] if "img_extract" in form else None
    if not (hasattr(img_item, "file")):
        html_error("Image non reçue")
    try:
        img = Image.open(img_item.file).convert("RGB")
    except Exception as e:
        html_error(f"Erreur chargement image : {e}")

    message = extraire_message_lsb(img)
    print(f"""
    <!DOCTYPE html>
    <html lang="fr"><head><meta charset="UTF-8"><title>Message caché LSB</title>
    <style>
        body {{ background:#121212; color:#e0e0e0; text-align:center; font-family:Arial,sans-serif; }}
        .msg {{ margin:30px auto; background:#262626; padding:24px 16px; border-radius:12px; max-width:480px; font-size:1.5em; letter-spacing:2px; }}
        a {{ color: #80cbc4; font-weight: bold; }}
    </style>
    </head>
    <body>
        <h1>🔎 Message extrait en LSB</h1>
        <div class="msg">{message}</div>
        <a href="/index.html">← Retour à l'accueil</a>
    </body>
    </html>
    """)

else:
    html_error("Action inconnue.")
