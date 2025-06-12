import openai
import requests
from PIL import Image
from io import BytesIO
import struct

openai.api_key = ""
def generer_image_openai(prompt, output_path):
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    image_url = response.data[0].url
    print(f"Image générée téléchargée depuis : {image_url}")
    img_bytes = requests.get(image_url).content
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img.save(output_path)
    print(f"Image originale sauvegardée : {output_path}")
    return img

def cacher_message_lsb_img(img, message, output_path):
    img_mod = img.copy()
    largeur, hauteur = img_mod.size
    pixels = img_mod.load()
    # Encode la longueur du message sur 4 octets (32 bits)
    message_bytes = message.encode('utf-8')
    longueur = len(message_bytes)
    longueur_bytes = struct.pack('>I', longueur)  # 4 octets big-endian
    binaire_msg = ''.join(f'{byte:08b}' for byte in longueur_bytes + message_bytes)
    idx = 0
    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y]
            if idx < len(binaire_msg):
                r = (r & 0xFE) | int(binaire_msg[idx])
                idx += 1
            if idx < len(binaire_msg):
                g = (g & 0xFE) | int(binaire_msg[idx])
                idx += 1
            if idx < len(binaire_msg):
                b = (b & 0xFE) | int(binaire_msg[idx])
                idx += 1
            pixels[x, y] = (r, g, b)
            if idx >= len(binaire_msg):
                break
        if idx >= len(binaire_msg):
            break
    img_mod.save(output_path)
    print(f"Image avec message caché sauvegardée : {output_path}")

if __name__ == "__main__":
    prompt = input("Décris l'image que tu veux générer : ")
    original_img_path = input("Nom du fichier pour l'image originale (ex : original.png) : ")
    img = generer_image_openai(prompt, original_img_path)
    message = input("Quel message veux-tu cacher dans l'image : ")
    output_img = input("Nom du fichier de sortie (ex : modifiee.png) : ")
    cacher_message_lsb_img(img, message, output_img)
    print(f"\nImages prêtes :\n - Image originale : {original_img_path}\n - Image modifiée (LSB) : {output_img}")


