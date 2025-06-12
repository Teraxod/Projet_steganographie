from PIL import Image

def lsb_diff_img(image1_path, image2_path, output_path):
    img1 = Image.open(image1_path).convert('RGB')
    img2 = Image.open(image2_path).convert('RGB')
    assert img1.size == img2.size, "Images de tailles différentes"
    w, h = img1.size
    diff_img = Image.new('RGB', (w, h))
    pixels1 = img1.load()
    pixels2 = img2.load()
    pixels_diff = diff_img.load()
    for y in range(h):
        for x in range(w):
            px1 = pixels1[x, y]
            px2 = pixels2[x, y]
            r = 255 if (px1[0] & 1) != (px2[0] & 1) else 0
            g = 255 if (px1[1] & 1) != (px2[1] & 1) else 0
            b = 255 if (px1[2] & 1) != (px2[2] & 1) else 0
            pixels_diff[x, y] = (r, g, b)
    diff_img.save(output_path)
    print(f"Image de différences LSB générée : {output_path}")

# Utilisation :
lsb_diff_img("pangolin.png", "pangolinn.png", "lsb_diff.png")

def compare_lsb(image1, image2):
    img1 = Image.open(image1).convert('RGB')
    img2 = Image.open(image2).convert('RGB')
    assert img1.size == img2.size, "Images de tailles différentes"
    pixels1 = img1.load()
    pixels2 = img2.load()
    largeur, hauteur = img1.size

    diff_lsb = 0
    for y in range(hauteur):
        for x in range(largeur):
            for i in range(3): # R, G, B
                lsb1 = pixels1[x, y][i] & 1
                lsb2 = pixels2[x, y][i] & 1
                if lsb1 != lsb2:
                    diff_lsb += 1
    print(f"Nombre de bits LSB différents entre les deux images : {diff_lsb}")

compare_lsb("pangolin.png", "pangolinn.png")

def extraire_message_lsb(image_path):
    img = Image.open(image_path)
    largeur, hauteur = img.size
    pixels = img.load()
    bits = []
    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y]
            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))

    # Récupérer la longueur du message (4 octets = 32 bits)
    longueur_bits = bits[:32]
    longueur = int(''.join(longueur_bits), 2)
    # Récupérer les bits du message
    message_bits = bits[32:32 + longueur * 8]
    chars = []
    for i in range(0, len(message_bits), 8):
        octet = message_bits[i:i+8]
        if len(octet) < 8:
            break
        chars.append(chr(int(''.join(octet), 2)))
    return ''.join(chars)

if __name__ == "__main__":
    img_path = input("Nom de l'image avec le mot caché : ")
    message = extraire_message_lsb(img_path)
    print("Message extrait :", message)
