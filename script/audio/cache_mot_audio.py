#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import librosa
import soundfile as sf
import io
import base64
import sys

cgitb.enable()

def generer_image_texte(mot, largeur, hauteur=400, police_taille=180):
    img = Image.new('L', (largeur, hauteur), color=255)
    draw = ImageDraw.Draw(img)
    try:
        # Prends une police GRASSE existante sur Ubuntu/Debian
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", police_taille)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), mot, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((largeur-w)//2, (hauteur-h)//2), mot, fill=0, font=font)
    return np.array(img)

print("Content-Type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()
mot = form.getfirst("mot", "").strip()
nom_audio = form.getfirst("nom_audio", "cache.wav").strip()

if not mot or not nom_audio.lower().endswith(".wav"):
    print("""
    <!DOCTYPE html>
    <html lang="fr"><head><meta charset="UTF-8"><title>Erreur</title></head>
    <body style="font-family: Ubuntu, sans-serif; text-align: center; padding-top: 40px; color: #ef5350;">
        <h1>❌ Erreur : mot ou nom de fichier non fourni</h1>
        <p><a href="/index.html">🏠 Retour à l'accueil</a></p>
    </body></html>
    """)
    sys.exit(0)

# Largeur et hauteur plus grands pour que le mot ressorte bien
largeur = max(2048, len(mot)*130)   # plus grand = lettres plus visibles
hauteur = 400                      # plus haut = contraste ++
police_taille = 180                # très gros texte
duree = max(3, len(mot) // 2)

img = generer_image_texte(mot.upper(), largeur=largeur, hauteur=hauteur, police_taille=police_taille)

# DEBUG - Génère une image PNG pour vérifier le rendu du mot
try:
    from matplotlib import pyplot as plt
    plt.imsave('/var/www/html/debug_mot.png', img, cmap='gray')
except Exception as e:
    pass  # ignore en prod

S = img[::-1] / 255.0 * 80  # force du signal 80
hop_length = S.shape[1] // duree
y = librosa.griffinlim(S, hop_length=hop_length)
buffer = io.BytesIO()
sf.write(buffer, y, samplerate=22050, format='WAV')
audio_data = buffer.getvalue()
audio_b64 = base64.b64encode(audio_data).decode("utf-8")

print(f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <title>Audio généré</title>
    <style>
        body {{ background-color:#121212; color:#e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
        a {{ color: #80cbc4; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        .container {{ max-width: 600px; margin: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Audio généré avec succès !</h1>
        <p>📥 <a download="{nom_audio}" href="data:audio/wav;base64,{audio_b64}">Télécharger le fichier audio (.wav)</a></p>
        <p>🖼️ <a href="/debug_mot.png" target="_blank">Voir l’image debug du mot caché (debug_mot.png)</a></p>
        <p>🏠 <a href="/index.html">Retour à l'accueil</a></p>
    </div>
</body>
</html>
""")
