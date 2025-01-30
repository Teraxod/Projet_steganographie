# Ce script va cacher le flag dans la partie exif de l'image


from PIL import Image
import piexif

image_path = 'C:/Users/Documents/image.jpg'
image = Image.open(image_path)

exif_dict = piexif.load(image.info.get("exif"))

exif_dict['0th'][piexif.ImageIFD.ImageDescription] = "FLag(cyber_T4er_flag_8)"

output_path = 'C:/Users/Documents/image_text_exif.jpg'
image.save(output_path, exif=piexif.dump(exif_dict))

print(f"Le texte a été ajouté aux métadonnées EXIF de l'image. Nouvelle image enregistrée sous {output_path}")
