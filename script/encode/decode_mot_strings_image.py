#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import base64
import re

cgitb.enable()

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()

# Vérification de l'image reçue
if "image" not in form or not form["image"].filename:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px;">
        <h1>❌ Erreur : Image manquante.</h1>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

image_item = form["image"]

# Sauvegarde de l'image
image_path = os.path.join(upload_dir, os.path.basename(image_item.filename))
with open(image_path, "wb") as f:
    f.write(image_item.file.read())

# Lecture binaire de l'image
with open(image_path, "rb") as f:
    image_data = f.read()

pattern_start = b"###START###"
pattern_end = b"###END###"

start_index = image_data.find(pattern_start)
end_index = image_data.find(pattern_end, start_index)

if start_index == -1 or end_index == -1:
    flag = "❌ Message non trouvé entre les délimiteurs."
else:
    raw_data = image_data[start_index + len(pattern_start):end_index].strip()
    try:
        decoded_str = raw_data.decode("utf-8")

        # Si binaire sous forme de '0' et '1' en blocs de 8 bits séparés par espaces
        if re.fullmatch(r'(?:[01]{8}\s*)+', decoded_str.strip()):
            bits = decoded_str.split()
            flag = ''.join(chr(int(b, 2)) for b in bits)
        else:
            # Sinon on essaie base64
            flag = base64.b64decode(decoded_str).decode('utf-8')

    except Exception as e:
        flag = f"❌ Erreur de décodage : {str(e)}"

# Affichage HTML résultat
print("Content-Type: text/html; charset=utf-8\n")
print(f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Mot caché dans l'image</title>
    <style>
        body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; }}
        a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        .container {{ max-width: 600px; margin: auto; }}
    </style>
</head>
<body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; background-color:#121212; color:#e0e0e0;">
    <h1>🎯 Message caché extrait</h1>
    <p style="font-size: 18px; color: #80cbc4;"><strong>{flag}</strong></p>
    <p><a href="/index.html" style="color:#80cbc4; text-decoration:none;">← Retour à l'accueil</a></p>
</body>
</html>
""")
