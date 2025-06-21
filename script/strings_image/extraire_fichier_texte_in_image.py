def extraire_txt_apres_image(img_path, out_txt="extrait.txt"):
    # Signature de fin d'un PNG : 49 45 4E 44 AE 42 60 82
    END_PNG = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
    with open(img_path, 'rb') as f:
        data = f.read()
    idx = data.find(END_PNG)
    if idx == -1:
        print("Fin d'image PNG non trouvée.")
        return
    start = idx + len(END_PNG)
    hidden = data[start:]
    if not hidden.strip():
        print("Aucun texte caché détecté.")
        return
    with open(out_txt, 'wb') as f:
        f.write(hidden)
    print(f"Fichier caché extrait : {out_txt}")

if __name__ == "__main__":
    chemin_image = input("Chemin de l'image modifiée : ")
    nom_sortie = input("Nom du fichier texte extrait [extrait.txt] : ") or "extrait.txt"
    extraire_txt_apres_image(chemin_image, nom_sortie)
