import cv2
import numpy as np

#HOW TO READ AN IMAGE

img = cv2.imread('img1/fruits.png')

if img is None:
    print("Error: Unable to load image.")
else:
    print("Image loaded successfully.")
    print(type(img))
