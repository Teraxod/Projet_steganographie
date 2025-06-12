import openai

# Remplace par ta clé API
openai.api_key = ""

def generer_acrostiche(mot):
    mot = mot.strip()

    # Limite la longueur à 12 lettres
    if len(mot) > 12:
        print("Erreur : Le mot doit contenir 12 lettres maximum.")
        return

    # Prompt strict et structurant
    system_msg = (
        f"Tu es un assistant littéraire. Génère exactement {len(mot)} phrases, une pour chaque lettre du mot secret (dans l’ordre). "
        "Chaque phrase commence par la lettre correspondante, forme un tout cohérent, et l'ensemble raconte quelque chose de logique ou une mini-histoire structurée. "
        "N’utilise jamais de guillemets ni de retour à la ligne. Sois clair, précis et cohérent."
    )

    client = openai.OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Le mot secret est '{mot.upper()}'."}
        ],
        max_tokens=400,
        temperature=0.7
    )

    texte = response.choices[0].message.content.strip()

    # On découpe uniquement sur les points
    phrases = [p.strip() for p in texte.split(".") if p.strip()]

    if len(phrases) != len(mot):
        print("⚠ Le nombre de phrases ne correspond pas au nombre de lettres du mot.")
        print("\nTexte brut généré :\n", texte)
        return

    print("\n=== Acrostiche généré ===\n")
    for phrase in phrases:
        print(f"{phrase}.")

if __name__ == "__main__":
    mot_utilisateur = input("Entrez un mot pour l’acrostiche : ").strip()
    generer_acrostiche(mot_utilisateur)
