#!/usr/lib/cgi-bin/venv/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import openai
import base64

cgitb.enable()
openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def generer_texte_sans_mot(mot):
    mot = mot.strip()
    if len(mot) > 12:
        return None, "Erreur : Le mot doit contenir 12 lettres maximum."
    system_msg = (
        f"Écrit un acrostiche qui masque le message saisie par l'utilisateur. Veille a ce que chaque lettre de mon mot apparaisse a chaque fois au début d'une nouvelle ligne"
    )
    client = openai.OpenAI(api_key=openai.api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Le mot secret est '{mot.upper()}', mais ne l'utilise jamais ni ses lettres comme début de phrase. Raconte simplement l'histoire ou le thème en autant de phrases que de lettres."}
            ],
            max_tokens=400,
            temperature=0.7
        )
        texte = response.choices[0].message.content.strip()
        # On ne découpe que si jamais il a mis plusieurs paragraphes, sinon on garde tel quel
        return texte, None
    except Exception as e:
        return None, f"Erreur lors de la génération : {str(e)}"

print("Content-Type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
mot = form.getfirst("mot", "").strip()

if not mot:
    print("""
    <html><head><meta charset="utf-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
    <h1>❌ Erreur : Aucun mot fourni.</h1>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

texte, erreur = generer_texte_sans_mot(mot)
if erreur:
    print(f"""
    <html><head><meta charset="utf-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
    <h1>❌ {erreur}</h1>
    <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    exit()

# Encode le texte en base64 (utf-8)
texte_b64 = base64.b64encode(texte.encode("utf-8")).decode("ascii")
filename = f"acrostiche_{mot.lower()}.txt"

# Génère un lien data: pour download (AUCUN FICHIER SERVEUR)
print(f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Texte généré</title>
    <style>
      body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
      a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
      a:hover {{ text-decoration: underline; }}
      .container {{ max-width: 600px; margin: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Texte généré avec succès !</h1>
        <p>📥 <a download="{filename}" href="data:text/plain;base64,{texte_b64}">Télécharger le texte (.txt)</a></p>
        <p>🏠 <a href="/index.html">Retour à l'accueil</a></p>
    </div>
</body>
</html>
""")
