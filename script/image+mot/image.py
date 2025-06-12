import openai
import requests
from PIL import Image, PngImagePlugin
from io import BytesIO

openai.api_key = ""
def generer_image_avec_openai(prompt):
    # Appel à l'API DALL-E 3 pour générer une image
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    image_url = response.data[0].url
    print(f"Lien de l'image générée : {image_url}")

    # Télécharger l'image
    image_bytes = requests.get(image_url).content
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image

def cacher_message_dans_image(image, chemin, message_secret):
    # Ajout du message dans les métadonnées PNG
    meta = PngImagePlugin.PngInfo()
    meta.add_text("message_secret", message_secret)
    image.save(chemin, "PNG", pnginfo=meta)
    print(f"Image sauvegardée avec le message caché : {chemin}")

if __name__ == "__main__":
    prompt = input("Décris l'image que tu veux générer : ")
    message = input("Que veux-tu cacher dans l'image : ")
    nom_fichier = "image_ai_secrete.png"

    img = generer_image_avec_openai(prompt)
    cacher_message_dans_image(img, nom_fichier, message)
