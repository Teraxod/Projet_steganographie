# Ce script va rechercher dans les exifs d'une image si un flag y est caché

import piexif
from PIL import Image

# Chemin de l'image
image_path = 'C:/Users/Documents/image.jpg'

# Ouvre l'image
image = Image.open(image_path)

# Charge les métadonnées EXIF existantes
exif_dict = piexif.load(image.info.get("exif", b""))

# Fonction pour vérifier si la valeur commence par "flag" et l'afficher
def check_flag(value):
    # Si la valeur est une chaîne de caractères ou un byte string et commence par "flag"
    if isinstance(value, bytes):
        value = value.decode(errors='ignore')  # Décoder les byte strings en texte
    if isinstance(value, str) and value.startswith("flag"):
        return value
    return None

# Affiche les mots qui commencent par "flag"
print("Mots commençant par 'flag' dans les EXIF :")
found_flags = False

for ifd in exif_dict:
    for tag, value in exif_dict[ifd].items():
        flag_value = check_flag(value)  # Vérifie si la valeur commence par "flag"
        if flag_value:
            found_flags = True
            print(f"  Flag trouvé: {flag_value}")

if not found_flags:
    print("  Aucun mot commençant par 'flag' trouvé dans les EXIF.")
