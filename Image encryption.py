import numpy as np
from PIL import Image
import pandas as pd
import random
import matplotlib.pyplot as plt

# /home/adarsh-sharma/Desktop/grey_scale.jpeg

# image = input("enter the file location: ")
# you can use the image given on folder.

# will convert to input later!!
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

imarray = np.random.randint(0, 256, size=(height, weidth)) * 10

print(imarray)

im = Image.fromarray(imarray.astype('uint8'))


# im.show()


# merging the 2 image arrays

encoded = np.add(imarray, img_arr)

# encoded_img = Image.fromarray(encoded.astype('uint8'))

# encoded_img.show()

plt.imshow(encoded)

plt.show()
