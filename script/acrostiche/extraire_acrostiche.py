#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import sys

cgitb.enable()

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
fileitem = form["fichier"] if "fichier" in form else None

if fileitem is None or not getattr(fileitem, "file", None):
    print("""
    <html><body style="color:red;"><h2>Erreur : Aucun fichier reçu.</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
    sys.exit(0)

try:
    contenu = fileitem.file.read().decode("utf-8")
    lignes = [l.strip() for l in contenu.splitlines() if l.strip()]
    # On prend la première lettre de chaque ligne
    mot_secret = ''.join([l[0] for l in lignes if l])
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Acrostiche détecté</title>
        <style>
            body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
            .container {{ max-width: 600px; margin: auto; }}
            .flag {{ font-size: 2.2em; color: #80cbc4; letter-spacing: 0.1em; background: #212b22; padding: 16px 0; border-radius: 12px; margin: 24px auto 18px; font-weight: bold; width: 80%; }}
            a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔎 Mot caché extrait</h1>
            <div class="flag">{mot_secret if mot_secret else "(Pas d'acrostiche trouvé)"}</div>
            <p><a href="/decode_acrostiche.html">← Extraire un autre acrostiche</a></p>
            <p><a href="/index.html">Accueil</a></p>
        </div>
    </body>
    </html>
    """)
except Exception as e:
    print(f"""
    <html><body style="color:red;"><h2>Erreur lors du décodage : {e}</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
