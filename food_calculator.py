import cv2
import pytesseract
import numpy as np
from googletrans import Translator, constants
# from pprint import pprint
import csv
from nltk.corpus import stopwords

pytesseract.pytesseract.tesseract_cmd = r'C:\python\tesseract.exe'
image = 'reteta1.png'
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

# print("OUTPUT:", out_below)
print("Language:", constants.LANGUAGES[detection.lang], f'({detection.lang})')
# print("Language code:", detection.lang)
print("Confidence:", detection.confidence)

language_destination = 'en'
translation = translator.translate(out_below, language_destination)
# print(translation)

translation_list = list(set(str(translation).split()[3:-2]))
# print(translation_list)

s=set(stopwords.words('english'))
clean_translation_list = []
for item in translation_list:
    if item not in s:
        clean_translation_list.append(item)



data_list = []

with open('FNDDS Nutrient Values.csv', 'r') as data:
    dataCSV = csv.DictReader(data)

    for line in dataCSV:
        data_list.append([f"{line['Main food description']}".lower(), f"{line['Energy (kcal)']}".lower()])


count = 0
for ingredient in clean_translation_list:
    print(ingredient)
    for item in data_list:
        if ingredient in item[0]:
            print(ingredient, item)
