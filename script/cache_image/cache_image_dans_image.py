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

# Vérifier la présence des deux fichiers
if "image_base" not in form or "image_cachee" not in form:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <html><head><title>Erreur</title></head><body>
    <h1>❌ Erreur : fichiers manquants.</h1>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

image_base_item = form["image_base"]
image_cachee_item = form["image_cachee"]

if not image_base_item.filename or not image_cachee_item.filename:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <html><head><title>Erreur</title></head><body>
    <h1>❌ Erreur : fichiers manquants.</h1>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

try:
    # Enregistrer l'image de base
    base_path = os.path.join(upload_dir, os.path.basename(image_base_item.filename))
    with open(base_path, "wb") as f:
        f.write(image_base_item.file.read())

    # Lire l'image cachée en binaire et encoder en base64
    image_cachee_data = image_cachee_item.file.read()
    image_cachee_b64 = base64.b64encode(image_cachee_data).decode("utf-8")

    # Charger l'image de base
    image = Image.open(base_path)

    # Préparer les métadonnées PNG avec l'image cachée
    meta = PngImagePlugin.PngInfo()
    meta.add_text("hidden_image", image_cachee_b64)

    # Enregistrer l'image modifiée avec métadonnées
    output_path = os.path.join(upload_dir, "image_avec_cache.png")
    image.save(output_path, pnginfo=meta)

    # Affichage succès
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <html>
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
      <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#80cbc4;">
        <h1>✅ Image cachée avec succès !</h1>
        <p>📦 Fichier modifié : <a href="/uploads/image_avec_cache.png" download>Télécharger</a></p>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
      </body>
    </html>
    """)

except Exception as e:
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <html>
      <head><title>Erreur</title></head>
      <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h1>❌ Erreur lors du traitement : {str(e)}</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
      </body>
    </html>
    """)
