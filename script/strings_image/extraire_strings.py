#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os

# Pour afficher les erreurs dans le navigateur
cgitb.enable()

upload_dir = "/var/www/html/uploads/"
os.makedirs(upload_dir, exist_ok=True)

form = cgi.FieldStorage()

# Vérification de la présence du fichier image
if "image" not in form or not form["image"].filename:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px;">
        <h1>❌ Erreur : Aucun fichier téléchargé.</h1>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

file_item = form["image"]
filename = os.path.basename(file_item.filename)
input_path = os.path.join(upload_dir, filename)

try:
    with open(input_path, "wb") as f:
        f.write(file_item.file.read())
except Exception as e:
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px;">
        <h1>❌ Erreur lors de l'enregistrement du fichier :</h1>
        <pre>{str(e)}</pre>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

try:
    with open(input_path, "rb") as f:
        data = f.read()
except Exception as e:
    print("Content-Type: text/html; charset=utf-8\n")
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px;">
        <h1>❌ Erreur lors de la lecture de l'image :</h1>
        <pre>{str(e)}</pre>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

try:
    data_str = data.decode("utf-8", errors="ignore")
except Exception:
    print("Content-Type: text/html; charset=utf-8\n")
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px;">
        <h1>❌ Erreur lors de la décodification des données de l'image.</h1>
        <p><a href="/index.html">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
    exit()

flag = None
start_idx = data_str.find("flag{")
if start_idx != -1:
    end_idx = data_str.find("}", start_idx)
    if end_idx != -1:
        flag = data_str[start_idx:end_idx+1]

print("Content-Type: text/html; charset=utf-8\n")

if flag:
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
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; background-color:#121212; color:#80cbc4;">
        <h1>✅ Flag trouvé : <code>{flag}</code></h1>
        <p><a href="/index.html" style="color:#80cbc4; text-decoration:none;">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
else:
    print("""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Flag non trouvé</title>
    </head>
    <body style="font-family: Ubuntu, sans-serif; text-align:center; padding-top:40px; background-color:#121212; color:#ef5350;">
        <h1>❌ Aucun flag trouvé dans l'image.</h1>
        <p><a href="/index.html" style="color:#ef5350; text-decoration:none;">← Retour à l'accueil</a></p>
    </body>
    </html>
    """)
