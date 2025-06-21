#!/usr/lib/cgi-bin/venv/bin/python3
import cgi
import cgitb
import numpy as np
import librosa
import matplotlib.pyplot as plt
import io
import base64
import sys

cgitb.enable()  # Active le debug CGI

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
audio_item = form["audio"] if "audio" in form else None
img_out = form.getfirst("img_out", "trouve.png")

if audio_item is None or not getattr(audio_item, "file", None):
    print("""
    <html><body style="color:red;"><h2>Erreur : Aucun fichier audio reçu.</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
    sys.exit(0)

try:
    # Lecture du .wav uploadé
    audio_bytes = audio_item.file.read()
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)

    # Générer le spectrogramme (format image, à lire à l’œil ou via OCR)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=8))
    S_db = librosa.amplitude_to_db(S, ref=np.max)

    # On prépare la figure sans axes ni cadre
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('off')
    ax.imshow(S_db, aspect='auto', origin='lower', cmap='gray')  # Mode GRIS pour contraste max
    plt.tight_layout(pad=0)

    # Sauvegarder l'image en mémoire
    buf = io.BytesIO()
    plt.savefig(buf, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")

    # Affichage HTML
    print(f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>Résultat spectrogramme</title>
        <style>
            body {{ background-color: #121212; color: #e0e0e0; font-family: Arial, sans-serif; padding: 2rem; text-align:center; }}
            .container {{ max-width: 900px; margin: auto; }}
            img {{ max-width: 100%; margin-top: 24px; border-radius: 8px; box-shadow: 0 4px 32px #000a; }}
            a {{ color: #80cbc4; font-weight: bold; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔎 Mot à lire sur le spectrogramme (ouvrez-le dans Sonic Visualizer ou OCR) !</h1>
            <img src="data:image/png;base64,{img_b64}" alt="Spectrogramme audio">
            <p>
                <a href="data:image/png;base64,{img_b64}" download="{img_out}">📥 Télécharger l'image ({img_out})</a>
            </p>
            <p><a href="/index.html">← Retour à l'accueil</a></p>
        </div>
    </body>
    </html>
    """)
except Exception as e:
    print(f"""
    <html><body style="color:red;"><h2>Erreur lors du traitement : {e}</h2>
    <a href="/index.html">Retour à l'accueil</a></body></html>
    """)
