from PIL import Image
import numpy as np
import cv2
import itertools
import warnings

warnings.filterwarnings("ignore")


def encode(image, file_name='compressed_image.txt', bits=15):
    count_list = []
    count = 0
    prev = None
    fimage = image.flatten()
    size = 2 ** (bits + 1) - 2 ** bits  # 32768 = 8000H

    for pixel in fimage:

        if prev == None:
            prev = pixel
            count += 1

            #RLE ABBAALLALAK 3A 5A AAA 3A AA 2A
        else:
            if prev != pixel:
                if count >= 3:
                    count_list.append((size + count, [prev]))
                else:
                    if count_list == []:
                        count_list.append((count, [prev] * count))
                    else:
                        c, color = count_list[-1]
                        if c > size:
                            count_list.append((count, [prev] * count))
                        else:
                            if c + count <= (2 ** bits) - 1:
                                count_list[-1] = (c + count, color + [prev] * count)
                            else:
                                count_list.append((count, [prev] * count))
                prev = pixel
                count = 1
            else:
                if count < (2 ** bits) - 1:
                    count += 1
                else:
                    count_list.append((size + count, [prev]))
                    prev = pixel
                    count = 1

    if count >= 3:
        count_list.append((size + count, [prev]))
    else:
        c, color = count_list[-1]
        if c > size:
            count_list.append((count, [prev] * count))
        else:
            if c + count <= (2 ** bits) - 1:
                count_list[-1] = (c + count, color + [prev] * count)
            else:
                count_list.append((count, [prev] * count))

    # Hexa encoding
    with open(file_name, "w") as file:
        hexa_encoded = "".join(
            map(lambda x: "{0:04x}".format(x[0]) + "".join(map(lambda y: "{0:02x}".format(y), x[1])), count_list))
        """ hexa_encoded = ""
        for count, colors in count_list:
            hexa_encoded += "{0:04x}".format(count)
            for color in colors:
                hexa_encoded += "{0:02x}".format(color) """
        file.write(hexa_encoded)
        file.close()

    # Compression rate
    rate = (1 - (len(hexa_encoded) / 2) / len(fimage)) * 100

    return hexa_encoded, rate

def test_encode():
    # Load test image
    image = Image.open('random.jpg')
    # Convert image to grayscale
    image = image.convert('L')
    # Resize image to reduce computation time
    image = image.resize((512,512))
    # Convert image to numpy array
    image_array = np.array(image)
    # Encode image
    encoded, rate = encode(image_array)
    # Print compression rate
    print('Compression rate: {}%'.format(rate))
    # Save encoded data to file
    with open('encoded_data.txt', 'w') as f:
        f.write(encoded)


test_encode()