#!/usr/bin/env python3

import cgi
import cgitb
from PIL import Image, PngImagePlugin
import io
import base64

cgitb.enable()  # activer le debug

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()

file_item = form["image"] if "image" in form else None
mot = form.getvalue("mot")

if file_item is not None and hasattr(file_item, 'file') and file_item.file and mot:
    # Lire les données de l'image envoyée
    image_data = file_item.file.read()
    original_image = Image.open(io.BytesIO(image_data))

    # Ajouter le mot caché dans les métadonnées PNG
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("mot_cache", mot)

    # Enregistrer dans un buffer en mémoire
    output_buffer = io.BytesIO()
    original_image.save(output_buffer, format="PNG", pnginfo=metadata)
    output_buffer.seek(0)

    # Encoder en base64 pour lien de téléchargement
    b64_image = base64.b64encode(output_buffer.read()).decode("utf-8")

    # Générer la page HTML
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
    <body>
        <div class="container">
            <h1>Mot caché avec succès !</h1>
            <p>Téléchargez l'image modifiée :</p>
            <a download="image_modifiee.png" href="data:image/png;base64,{b64_image}">📥 Télécharger l'image</a>
            <p>🏠 <a href="/index.html">Retour à l'accueil</a></p>
        </div>
    </body>
    </html>
    """)
else:
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body>
        <h2>Erreur : formulaire incomplet ou fichier non reçu.</h2>
        <p><a href="/index.html">Retour à l'accueil</a></p>
    </body>
    </html>
    """)
