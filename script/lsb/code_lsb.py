#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import base64
from PIL import Image
from io import BytesIO
import struct
import sys

cgitb.enable()

def cacher_message_lsb_img(img, message):
    img_mod = img.copy()
    largeur, hauteur = img_mod.size
    pixels = img_mod.load()
    # Encode la longueur du message sur 4 octets (32 bits)
    message_bytes = message.encode('utf-8')
    longueur = len(message_bytes)
    longueur_bytes = struct.pack('>I', longueur)
    binaire_msg = ''.join(f'{byte:08b}' for byte in longueur_bytes + message_bytes)
    idx = 0
    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y][:3]
            if idx < len(binaire_msg):
                r = (r & 0xFE) | int(binaire_msg[idx])
                idx += 1
            if idx < len(binaire_msg):
                g = (g & 0xFE) | int(binaire_msg[idx])
                idx += 1
            if idx < len(binaire_msg):
                b = (b & 0xFE) | int(binaire_msg[idx])
                idx += 1
            if len(pixels[x, y]) == 4:
                a = pixels[x, y][3]
                pixels[x, y] = (r, g, b, a)
            else:
                pixels[x, y] = (r, g, b)
            if idx >= len(binaire_msg):
                break
        if idx >= len(binaire_msg):
            break
    return img_mod

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
imgfile = form['imgfile'] if "imgfile" in form else None
flag = form.getfirst("flag", "").strip()
output_img = form.getfirst("output_img", "image_flag.png").strip()

if "imgfile" not in form or not getattr(imgfile, "file", None) or not flag or not output_img:
    print("""<html><body style="color:red; text-align:center; padding-top:40px;">
    <h2>Erreur : Tous les champs sont obligatoires.</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>""")
    sys.exit(0)


try:
    # Lecture de l'image uploadée
    img_bytes = imgfile.file.read()
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
except Exception as e:
    print(f"""<html><body style="color:red;"><h2>Erreur lors de la lecture de l'image : {e}</h2></body></html>""")
    sys.exit(0)

# Sauvegarde l'image originale pour download
original_name = "original_upload.png"
img.save(f"/var/www/html/{original_name}")

# Cache le flag
img_mod = cacher_message_lsb_img(img, flag)
img_mod.save(f"/var/www/html/{output_img}")

# Génère un aperçu base64
buf = BytesIO()
img_mod.save(buf, format="PNG")
img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

print(f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Résultat Stegano LSB</title>
    <style>
        body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
        a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        .container {{ max-width: 700px; margin: auto; }}
        img {{ margin: 32px 0 24px 0; max-width:100%; border-radius: 8px; box-shadow: 0 4px 32px #000a; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Images générées avec succès !</h1>
        <img src="data:image/png;base64,{img_b64}" alt="Aperçu image modifiée">
        <p>
            <a href="/{original_name}" download="{original_name}">⬇️ Télécharger l'image originale</a><br>
            <a href="/{output_img}" download="{output_img}">⬇️ Télécharger l'image avec le flag caché</a>
        </p>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </div>
</body>
</html>
""")
