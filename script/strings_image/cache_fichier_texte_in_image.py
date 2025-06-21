#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import base64
import os
from PIL import PngImagePlugin, Image

cgitb.enable()

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()

# Vérif champs requis
if "image" not in form or "filename" not in form or "contenu" not in form:
    print("Content-Type: text/html; charset=utf-8\n")
    print("<h1>❌ Formulaire incomplet</h1>")
    exit()

image_file = form["image"]
filename = form.getvalue("filename")
contenu = form.getvalue("contenu")

# Sécurité de base sur le nom de fichier
if not filename.endswith(".txt") or "/" in filename:
    print("Content-Type: text/html; charset=utf-8\n")
    print("<h1>❌ Nom de fichier invalide</h1>")
    exit()

# Enregistrer l'image uploadée
image_path = os.path.join(upload_dir, os.path.basename(image_file.filename))
with open(image_path, "wb") as f:
    f.write(image_file.file.read())

# Créer le fichier texte temporairement
txt_path = os.path.join(upload_dir, filename)
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(contenu)

# Lire et encoder le fichier entier en base64
with open(txt_path, "rb") as f:
    file_encoded = base64.b64encode(f.read()).decode("utf-8")

# Charger image
image = Image.open(image_path)

# Ajouter le fichier encodé dans les métadonnées (sous clé = nom du fichier)
meta = PngImagePlugin.PngInfo()
meta.add_text(filename, file_encoded)

# Sauver l'image avec fichier caché
output_path = os.path.join(upload_dir, "image_avec_fichier_cache.png")
image.save(output_path, pnginfo=meta)

# Supprimer le fichier texte temporaire
os.remove(txt_path)

# Affichage résultat
print("Content-Type: text/html; charset=utf-8\n")
print(f"""
<html>
<head>
    <meta charset="UTF-8" />
    <title>Fichier caché</title>
    <style>
        body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; }}
        a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
        .container {{ max-width: 600px; margin: auto; text-align:center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✅ Fichier <code>{filename}</code> caché dans l’image</h1>
        <p>📦 <a href="/uploads/image_avec_fichier_cache.png" download>Télécharger l’image modifiée</a></p>
        <p><a href="/index.html">🏠 Retour à l’accueil</a></p>
    </div>
</body>
</html>
""")
