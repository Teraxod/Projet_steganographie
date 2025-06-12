def decode_whitespace():
    stegano_path = input("Nom du fichier à décoder (ex: texte_stegano.txt) : ")
    with open(stegano_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    bits = []
    for line in lines:
        if line.endswith(' \n'):
            bits.append('0')
        elif line.endswith('\t\n'):
            bits.append('1')
    # Récupérer tous les caractères complets (8 bits)
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(''.join(byte), 2)))
    message = ''.join(chars)
    print("Message extrait :", message)
    return message

# Utilisation
decode_whitespace()
