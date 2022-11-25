import cv2
import pytesseract
import numpy as np
from googletrans import Translator, constants
from pprint import pprint

pytesseract.pytesseract.tesseract_cmd = r'C:\python\tesseract.exe'
image = 'sample2.png'
img = cv2.imread(image)#Alternatively: can be skipped if you have a Blackwhite image
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)

kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)


translator = Translator()
detection = translator.detect(out_below)

print("OUTPUT:", out_below)
print("Language:", constants.LANGUAGES[detection.lang], f'({detection.lang})')
# print("Language code:", detection.lang)
print("Confidence:", detection.confidence)

language_destination = 'en'
translation = translator.translate(out_below, language_destination)
print(translation)
# print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

