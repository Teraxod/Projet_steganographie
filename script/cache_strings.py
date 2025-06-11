#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os

# Pour afficher les erreurs dans le navigateur
cgitb.enable()

print("Content-Type: text/html; charset=utf-8\n")

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()
file_item = form["image"] if "image" in form else None
mot_cache = form.getvalue("mot")

if file_item is None or not hasattr(file_item, 'file') or not mot_cache:
    print("""
    <html><head><meta charset="utf-8"><title>Erreur</title></head><body>
    <h1>❌ Erreur : formulaire incomplet.</h1>
    <p>Veuillez fournir une image et un mot à cacher.</p>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

filename = os.path.basename(file_item.filename)
input_path = os.path.join(upload_dir, filename)

try:
    # Enregistrer l'image originale
    with open(input_path, 'wb') as f:
        f.write(file_item.file.read())

    # Lire les données binaires de l'image
    with open(input_path, 'rb') as f:
        data = f.read()

    # Ajouter le mot caché à la fin, encodé en utf-8 et entouré de sauts de ligne
    mot_cache_bytes = b"\n" + mot_cache.encode('utf-8') + b"\n"
    output_path = os.path.join(upload_dir, "image_strings.png")

    with open(output_path, 'wb') as f:
        f.write(data + mot_cache_bytes)

    # Afficher la page de confirmation
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
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #80cbc4;">
        <h1>✅ Mot caché avec succès dans l'image !</h1>
        <p>📥 <a href="/uploads/image_strings.png" download>Télécharger l'image modifiée</a></p>
        <p>🏠 <a href="/index.html">Retour à l'accueil</a></p>
    </body>
    </html>
    """)

except Exception as e:
    print(f"""
    <html>
    <head><meta charset="utf-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
        <h1>❌ Erreur lors du traitement : {str(e)}</h1>
        <p>🏠 <a href="/index.html">Retour à l'accueil</a></p>
    </body>
    </html>
    """)
