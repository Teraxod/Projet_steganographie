#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import base64
import os
from PIL import Image

cgitb.enable()

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()

if "image" not in form:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h1>❌ Erreur : aucun fichier PNG téléchargé.</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

image_item = form["image"]

if not image_item.filename:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h1>❌ Erreur : aucun fichier PNG téléchargé.</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

input_path = os.path.join(upload_dir, os.path.basename(image_item.filename))
try:
    with open(input_path, "wb") as f:
        f.write(image_item.file.read())
except Exception as e:
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h1>❌ Erreur lors de l'enregistrement du fichier : {str(e)}</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

try:
    image = Image.open(input_path)
    metadata = getattr(image, "text", {})

    b64_data = metadata.get("hidden_image")
    if not b64_data:
        raise ValueError("Aucune image cachée trouvée dans les métadonnées.")

    image_cachee_bytes = base64.b64decode(b64_data)

    output_path = os.path.join(upload_dir, "image_extraite.png")
    with open(output_path, "wb") as f:
        f.write(image_cachee_bytes)

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
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#80cbc4;">
        <h1>✅ Image extraite avec succès !</h1>
        <p>📥 <a href="/uploads/image_extraite.png" download>Télécharger l'image extraite</a></p>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)

except Exception as e:
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h1>❌ Erreur : {str(e)}</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)
