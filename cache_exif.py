# Ce script va cacher le flag dans la partie exif de l'image


from PIL import Image
import piexif

# Ouvre l'image
image_path = 'C:/Users/Documents/image.jpg'
image = Image.open(image_path)

# Charge les métadonnées EXIF existantes
exif_dict = piexif.load(image.info.get("exif"))

# Ajoute un texte personnalisé dans le champ ImageDescription
exif_dict['0th'][piexif.ImageIFD.ImageDescription] = "FLag(cyber_T4er_flag_8)"

# Sauvegarde l'image avec les métadonnées EXIF modifiées
output_path = 'C:/Users/Documents/image_text_exif.jpg'
image.save(output_path, exif=piexif.dump(exif_dict))

print(f"Le texte a été ajouté aux métadonnées EXIF de l'image. Nouvelle image enregistrée sous {output_path}")
