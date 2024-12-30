import cv2
import numpy as np
import pytesseract


def ocr_core(img):
    text = pytesseract.image_to_string(img, lang='eng')
    return text


img = cv2.imread('testocr.png')

# Get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)

# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

img = get_grayscale(img)
img = thresholding(img)
img = remove_noise(img)

print(ocr_core(img))