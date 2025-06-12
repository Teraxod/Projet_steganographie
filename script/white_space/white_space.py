import openai

openai.api_key = ""
def generer_texte(prompt, nb_lignes=50):
    # Génère un texte via OpenAI (gpt-3.5-turbo ou gpt-4)
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ou "gpt-4"
        messages=[
            {"role": "system", "content": "Tu es un écrivain. Rédige un texte cohérent et structuré en plusieurs paragraphes. Chaque phrase ou paragraphe doit être sur une ligne séparée."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600
    )
    texte = response.choices[0].message.content
    # Force une ligne par phrase
    lignes = texte.replace('. ', '.\n').split('\n')
    # S’assure d’avoir assez de lignes
    while len(lignes) < nb_lignes:
        lignes.append("")
    return lignes

def cacher_mot_whitespace(mot, lignes, output_path):
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
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("Mot caché dans :", output_path)

if __name__ == "__main__":
    prompt = input("Sujet ou style du texte à générer : ")
    mot = input("Mot à cacher dans le texte (ascii uniquement) : ")
    output = input("Nom du fichier de sortie (ex: texte_stegano.txt) : ")

    lignes = generer_texte(prompt, nb_lignes=len(mot)*8)
    cacher_mot_whitespace(mot, lignes, output)
