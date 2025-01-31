# Ce script a pour objectif de rechercher si le flag est contenu dans les exifs de l'image

import piexif
from PIL import Image

# Chemin de l'image
image_path = 'image_text_exif.jpg'

# Ouvre l'image
image = Image.open(image_path)

# Charge les métadonnées EXIF existantes en toute sécurité
exif_bytes = image.info.get("exif")
if exif_bytes:
    try:
        exif_dict = piexif.load(exif_bytes)
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement des métadonnées EXIF : {e}")
        exif_dict = {}
else:
    exif_dict = {}

# Fonction pour vérifier si la valeur contient "flag" et l'afficher
def check_flag(value):
    """ Vérifie si la valeur est un texte contenant 'flag' (insensible à la casse). """
    if isinstance(value, bytes):  # Si c'est un byte string, on le décode
        value = value.decode(errors='ignore')
    if isinstance(value, str) and "flag" in value.lower():  # Vérifie si 'flag' est présent
        return value
    return None

# Recherche et affichage des valeurs contenant "flag"
print("\n🔍 Recherche de 'flag' dans les métadonnées EXIF :")
found_flags = False

for ifd, data in exif_dict.items():
    if isinstance(data, dict):  # ✅ Vérifie que la valeur est un dictionnaire
        for tag, value in data.items():
            flag_value = check_flag(value)  # Vérifie si la valeur contient "flag"
            if flag_value:
                found_flags = True
                print(f"  ✅ Flag trouvé dans {ifd} : {flag_value}")

if not found_flags:
    print("  ❌ Aucun flag trouvé dans les métadonnées EXIF.")

