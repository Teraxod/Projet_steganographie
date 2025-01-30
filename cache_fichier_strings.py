# Ce script va cacher un fichier.txt dans les strings d'une image

def get_filename(file_path):
    import os
    return os.path.basename(file_path)

def hide_filename_in_image(image_path, text_file_path, output_image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
        filename = get_filename(text_file_path)
        new_img_data = img_data + b'\n' + filename.encode()  # Ajouter le nom du fichier

        with open(output_image_path, 'wb') as out_img_file:
            out_img_file.write(new_img_data)

        print(f"Image avec nom de fichier caché sauvegardée sous {output_image_path}")
    except Exception as e:
        print(f"Erreur lors de l'ajout du nom du fichier à l'image : {e}")

image_path = 'image.png'  
text_file_path = 'flag.txt'  
output_image_path = 'image_avec_nom_cache_exif.png'  
hide_filename_in_image(image_path, text_file_path, output_image_path)
