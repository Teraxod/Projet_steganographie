# Ce script va cacher le flag dans la partie exif de l'image


from PIL import Image
import piexif

# Ouvre l'image
image_path = 'image.jpg'
image = Image.open(image_path)

# Vérifie si l'image a des métadonnées EXIF, sinon initialise un dictionnaire vide
exif_bytes = image.info.get("exif")
if exif_bytes:
    exif_dict = piexif.load(exif_bytes)
else:
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

# Ajoute un texte personnalisé dans le champ ImageDescription
exif_dict['0th'][piexif.ImageIFD.ImageDescription] = b"FLag(test)"

# Sauvegarde l'image avec les métadonnées EXIF modifiées
output_path = 'image_text_exif.jpg'
image.save(output_path, "jpeg", exif=piexif.dump(exif_dict))

print(f"Le texte a été ajouté aux métadonnées EXIF de l'image. Nouvelle image enregistrée sous {output_path}")

