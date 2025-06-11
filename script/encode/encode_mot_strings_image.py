#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import base64

cgitb.enable()

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()
image_item = form["image"] if "image" in form else None
message = form.getvalue("message")
encoding = form.getvalue("encoding")

print("Content-Type: text/html; charset=utf-8\n")

if image_item is None or not getattr(image_item, "filename", None) or not message or not encoding:
    print("""
    <html><head><meta charset="utf-8"><title>Erreur</title></head><body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
    <h1>❌ Erreur : Image, message ou méthode d'encodage manquante.</h1>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

try:
    # Sauvegarde de l'image originale
    image_path = os.path.join(upload_dir, os.path.basename(image_item.filename))
    with open(image_path, "wb") as f:
        f.write(image_item.file.read())

    # Lecture des données binaires
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Encodage du message selon la méthode choisie
    if encoding == "base64":
        encoded_msg = base64.b64encode(message.encode('utf-8'))
    elif encoding == "binary":
        encoded_msg = ' '.join(format(ord(c), '08b') for c in message).encode('utf-8')
    else:
        print(f"""
        <html><head><meta charset="utf-8"><title>Erreur</title></head><body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
        <h1>❌ Méthode d'encodage inconnue : {encoding}</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
        </body></html>
        """)
        exit()

    # Ajout des délimiteurs autour du message encodé
    delimiter_start = b"###START###"
    delimiter_end = b"###END###"
    new_image_data = image_data + delimiter_start + encoded_msg + delimiter_end

    # Enregistrement de l'image modifiée
    output_filename = "image_modifiee_" + os.path.basename(image_item.filename)
    output_image_path = os.path.join(upload_dir, output_filename)
    with open(output_image_path, "wb") as f:
        f.write(new_image_data)

    # Affichage de la page de succès
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
        <h1>✅ Message encodé avec succès !</h1>
        <p>📥 <a href="/uploads/{output_filename}" download>Télécharger l'image modifiée</a></p>
        <a href="/index.html">← Retour à l'accueil</a>
      </body>
    </html>
    """)

except Exception as e:
    print(f"""
    <html>
    <head><meta charset="utf-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
      <h1>❌ Erreur lors du traitement : {str(e)}</h1>
      <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body>
    </html>
    """)
