import numpy as np
from PIL import Image
import pandas as pd
import random
import matplotlib.pyplot as plt

# /home/adarsh-sharma/Desktop/grey_scale.jpeg
# image = input("enter the file location: ")
# you can use the image given on folder.
# will convert to input later!!


def encryption():

    image = "/home/adarsh-sharma/Desktop/grey_scale.jpeg"

    key = int(input("enter key: "))

    random.seed(key)

    # Taking image from user
    img = Image.open(image).convert('L')

    img_arr = np.array(img)

    print(img_arr)

    height = np.shape(img_arr)[0]  # rows

    weidth = np.shape(img_arr)[1]

    # generating random image

    # if you don't do *10 the image will not be encrypted correctly.
    imarray = np.random.randint(0, 256, size=(height, weidth)) * 10

    print(imarray)

    im = Image.fromarray(imarray.astype('uint8'))

    # im.show()

    # merging the 2 image arrays

    encoded = np.add(imarray, img_arr)

    # encoded_img = Image.fromarray(encoded.astype('uint8')) #PIL doesn't work as it is supposed to be

    # encoded_img.show()

    plt.imshow(encoded)

    # plt.show()

    DF = pd.DataFrame(encoded)

    DF.to_csv("encoded_img.csv")

    return DF, key, height, weidth


def decryption(key, height, weidth, DF):

    random.seed(key)

    imarray = np.random.randint(0, 256, size=(height, weidth)) * 10
