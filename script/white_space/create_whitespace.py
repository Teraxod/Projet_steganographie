#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import openai
import base64
import os

cgitb.enable()
openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # À remplir ou mieux, utiliser une variable d'env

def generer_texte(prompt, nb_lignes=50):
    if openai.api_key:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un écrivain. Rédige un texte cohérent en plusieurs paragraphes. Chaque phrase ou paragraphe doit être sur une ligne séparée."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )
        texte = response.choices[0].message.content
        lignes = texte.replace('. ', '.\n').split('\n')
    else:
        # Si pas de clé, dummy
        lignes = [f"Exemple ligne {i+1}." for i in range(nb_lignes)]
    while len(lignes) < nb_lignes:
        lignes.append("")
    return lignes

def cacher_mot_whitespace(mot, lignes):
    # Encode le mot en binaire
    binaire = ''.join(f"{ord(c):08b}" for c in mot)
    if len(binaire) > len(lignes):
        raise ValueError("Le texte n’a pas assez de lignes pour cacher le mot.")
    out = []
    for i, line in enumerate(lignes):
        if i < len(binaire):
            if binaire[i] == '0':
                out.append(line.rstrip('\n') + ' \n')   # espace = 0
            else:
                out.append(line.rstrip('\n') + '\t\n') # tab = 1
        else:
            out.append(line + '\n')
    return ''.join(out)

print("Content-Type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
prompt = form.getfirst("prompt", "").strip()
mot = form.getfirst("mot", "").strip()
output = form.getfirst("output", "texte_stegano.txt").strip()

if not prompt or not mot or not output:
    print("""
    <html><body style="color:red;"><h2>Erreur : tous les champs sont requis !</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
    exit()

try:
    nb_lignes = len(mot) * 8
    lignes = generer_texte(prompt, nb_lignes=nb_lignes)
    texte_cache = cacher_mot_whitespace(mot, lignes)
    texte_b64 = base64.b64encode(texte_cache.encode("utf-8")).decode("utf-8")
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Texte stéganographié généré</title>
        <style>
            body {{ background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
            a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            .container {{ max-width: 600px; margin: auto; }}
            textarea {{ width: 100%; height: 180px; background: #232323; color: #e0e0e0; border-radius: 8px; padding: 10px; border: none; font-size: 1em; margin-bottom: 1em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Texte stéganographié généré !</h1>
            <textarea readonly>{texte_cache}</textarea>
            <p>
                <a download="{output}" href="data:text/plain;base64,{texte_b64}">📥 Télécharger le texte ({output})</a>
            </p>
            <p><a href="/index.html">← Retour à l'accueil</a></p>
        </div>
    </body>
    </html>
    """)
except Exception as e:
    print(f"<html><body style='color:red;'><h2>Erreur lors du traitement : {e}</h2><a href='/index.html'>Retour à l'accueil</a></body></html>")
