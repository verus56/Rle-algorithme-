import numpy as np
from PIL import Image

def decode_rle(data):
    """Décode les données RLE et retourne l'image décompressée"""
    # Convertit les données en un tableau numpy d'entiers non signés 8 bits
    data = np.frombuffer(data, dtype=np.uint8)
    # Initialise l'indice du tableau et la position courante de l'image
    i, pos = 0, 0
    # Initialise l'image décompressée avec des pixels noirs
    img = np.zeros((256, 256, 3), dtype=np.uint8)    #5a47B AAAAA
    # Parcourt les données RLE
    while i < len(data):
        # Lit la valeur du pixel et le nombre de répétitions
        pixel = data[i:i+3]
        count = data[i+3]
        # Remplit la section de l'image correspondante avec la valeur du pixel
        img[pos:pos+count] = pixel
        # Met à jour l'indice du tableau et la position courante de l'image
        i += 4
        pos += count
    # Crée une image PIL à partir de l'array numpy
    return Image.fromarray(img)

# Ouvre le fichier compressé en mode lecture binaire
with open('random_compressed.txt', 'rb') as f:
    # Lit les données RLE depuis le fichier
    rle_data = f.read()
    # Décompresse les données RLE et affiche l'image décompressée
    img = decode_rle(rle_data)
    img.show()



