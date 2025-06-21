#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import sys

cgitb.enable()

def decode_whitespace_from_lines(lines):
    bits = []
    for line in lines:
        if line.endswith(' \n') or line.endswith(' '):
            bits.append('0')
        elif line.endswith('\t\n') or line.endswith('\t'):
            bits.append('1')
    # Décodage
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(''.join(byte), 2)))
    message = ''.join(chars)
    return message

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
fileitem = form["fichier"] if "fichier" in form else None

if "fichier" not in form or not getattr(fileitem, "file", None):
    print("""
    <html><body style="color:red;"><h2>Erreur : Aucun fichier reçu.</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
    sys.exit(0)

try:
    contenu = fileitem.file.read().decode("utf-8")
    lines = contenu.splitlines(keepends=True)
    mot_cache = decode_whitespace_from_lines(lines)
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Mot caché décodé</title>
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
            <div class="flag">{mot_cache if mot_cache else "(Aucun mot trouvé ou texte corrompu)"}</div>
            <p><a href="/decode_ws.html">← Extraire un autre mot</a></p>
            <p><a href="/index.html">Accueil</a></p>
        </div>
    </body>
    </html>
    """)
except Exception as e:
    print(f"""
    <html><body style="color:red;"><h2>Erreur lors du décodage : {e}</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
