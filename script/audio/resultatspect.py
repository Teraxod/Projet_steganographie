import numpy as np
import librosa
import matplotlib.pyplot as plt
import sys

def extraire_image_spectrogramme(wav_path, img_out="mot_cache.png"):
    # 1. Charge le wav
    y, sr = librosa.load(wav_path, sr=None)
    # 2. Spectrogramme d'amplitude (magnitude)
    S = np.abs(librosa.stft(y, n_fft=512, hop_length=8))
    # 3. Normalise pour affichage
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    S_norm = (S_db - S_db.min()) / (S_db.max() - S_db.min()) * 255
    S_img = S_norm.astype(np.uint8)
    # 4. Retourne (pour que le grave soit en bas comme encodage)
    img = np.flipud(S_img)
    plt.imsave(img_out, img, cmap='gray')
    print(f"Image extraite depuis {wav_path} -> {img_out}")
    print("Lis le mot sur l'image ou utilise un OCR si c'est long.")

if __name__ == "__main__":
    wav_path = input("Fichier audio à analyser (wav) : ")
    img_out = input("Nom du fichier image de sortie (ex : trouvé.png) : ")
    extraire_image_spectrogramme(wav_path, img_out)
