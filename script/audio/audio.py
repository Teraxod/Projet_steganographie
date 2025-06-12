import numpy as np
from PIL import Image, ImageDraw, ImageFont
import librosa
import soundfile as sf

def generer_image_texte(mot, largeur, hauteur=256, police_taille=80):
    img = Image.new('L', (largeur, hauteur), color=255)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", police_taille)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), mot, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((largeur-w)//2, (hauteur-h)//2), mot, fill=0, font=font)
    return np.array(img)

if __name__ == "__main__":
    mot = input("Quel mot veux-tu rendre visible dans le spectrogramme ? ")
    nom_audio = input("Nom du fichier audio (ex : cache.wav) : ")

    # Largeur et durée auto en fonction de la taille du mot
    largeur = max(1024, len(mot)*70)   # 70 pixels par lettre, min 1024px
    duree = max(3, len(mot) // 2)      # 3s minimum, 0.5s/lettre (ajuste si besoin)

    print(f"Largeur de l'image (virtuelle) : {largeur}px")
    print(f"Durée du fichier audio : {duree}s")

    # Générer image (pas sauvegardée)
    img = generer_image_texte(mot.upper(), largeur=largeur, hauteur=256, police_taille=80)

    # Générer l'audio
    S = img[::-1] / 255.0 * 80  # Plus bas = graves, plus haut = aigus, force du signal = 80
    hop_length = S.shape[1] // duree
    y = librosa.griffinlim(S, hop_length=hop_length)
    sf.write(nom_audio, y, samplerate=22050)
    print(f"Audio généré : {nom_audio}\nOuvre-le dans Sonic Visualizer ou Audacity (mode spectrogramme) !")
