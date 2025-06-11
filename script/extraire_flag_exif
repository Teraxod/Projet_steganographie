#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
from PIL import Image, PngImagePlugin
import io

cgitb.enable()

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

if "image" not in form or not form["image"].file:
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h2>❌ Erreur : aucun fichier reçu.</h2>
        <p><a href="/page4.html">← Retour à la page précédente</a></p>
    </body>
    </html>
    """)
    exit()

file_item = form["image"]

try:
    image_data = file_item.file.read()
    image = Image.open(io.BytesIO(image_data))
except Exception as e:
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h2>❌ Erreur lors de la lecture de l'image :</h2>
        <pre>{str(e)}</pre>
        <p><a href="/page4.html">← Retour à la page précédente</a></p>
    </body>
    </html>
    """)
    exit()

if not isinstance(image, PngImagePlugin.PngImageFile):
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h2>❌ Erreur : l'image n'est pas un fichier PNG.</h2>
        <p><a href="/page4.html">← Retour à la page précédente</a></p>
    </body>
    </html>
    """)
    exit()

metadata = image.text if hasattr(image, "text") else {}

flag = None
for key, value in metadata.items():
    if isinstance(value, str) and value.lower().startswith("flag"):
        flag = value
        break

if not flag:
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Flag non trouvé</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; color:#ef5350;">
        <h2>❌ Aucun flag trouvé dans les métadonnées de l'image.</h2>
        <p><a href="/index.html">← Retour à la page précédente</a></p>
    </body>
    </html>
    """)
else:
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
        <h1>✅ Flag trouvé : <code>{flag}</code></h1>
        <p><a href="/index.html">← Retour à la page précédente</a></p>
    </body>
    </html>
    """)
