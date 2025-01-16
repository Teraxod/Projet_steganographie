import openai

# CATCH PHRASE SOUS FORME CHALLENGE ROOTME#
#"Chaque début est une fondation : il mérite toute l’attention qu’il réclame pour bâtir le reste avec solidité."#
#
# Remplace par ta clé API OpenAI
openai.api_key = "ta_cle_api_openai"

def generer_texte(mot):
    texte_genere = []
    
    # Pour chaque lettre du mot, on va appeler l'API ChatGPT
    for lettre in mot:
        prompt = f"Fournis une phrase qui commence par la lettre '{lettre.upper()}' et qui fait sens dans un texte cohérent."
        
        # Appel à l'API ChatGPT
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Tu peux aussi utiliser un modèle comme gpt-4
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
        )
        
        # Récupérer la réponse générée
        phrase = response.choices[0].text.strip()
        texte_genere.append(phrase)

    return "\n".join(texte_genere)

# Demander à l'utilisateur de saisir un mot
mot_utilisateur = input("Entrez un mot pour cacher dans le texte: ")

# Générer et afficher le texte
texte = generer_texte(mot_utilisateur)
print("\nVoici le texte généré avec le mot caché :\n")
print(texte)
