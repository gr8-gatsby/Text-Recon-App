import cv2
import pytesseract
import numpy as np
from googletrans import Translator, constants
import webbrowser

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

pytesseract.pytesseract.tesseract_cmd = r'C:\python\tesseract.exe'

icon = 'c:\Python\Text_Recon/4150650.ico'
root = Tk()
root.title("Text Extractor and Translator")
root.iconbitmap(icon)
root.resizable(False, False)
# root.geometry('800x400')

def main_func():
    global filename

    filetypes = (
        ('Image Files', '*.png'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    print(filename)

    image = filename
    img = cv2.imread(image)#Alternatively: can be skipped if you have a Blackwhite image
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)
    print(out_below)

    translator = Translator()
    detection = translator.detect(out_below)

    print("Language:", constants.LANGUAGES[detection.lang], f'({detection.lang})')
    print("Confidence:", detection.confidence)

    language_destination = 'en'
    translation = translator.translate(out_below, language_destination)
    print(translation)

    translation_list = list(set(str(translation).split()[3:-2]))
    # print(translation_list)

    # original_frame = LabelFrame(root, text='Original Text', font="Verdana 10 bold", labelanchor=N)
    # original_frame.grid(row=0, column=1, padx=(10, 5), pady=5)

    # original_label = Label(original_frame, text=out_below, font=("Verdana", 10), justify=LEFT)
    # original_label.grid(row=0, column=1, sticky=W, padx=10, pady=(15, 5))

    # translated_frame = LabelFrame(root, text='Original Text', font="Verdana 10 bold", labelanchor=N)
    # translated_frame.grid(row=1, column=1, padx=(10, 5), pady=5)

    # translated_label = Label(translated_frame, text=str(translation), font=("Verdana", 10), justify=LEFT)
    # translated_label.grid(row=0, column=1, sticky=W, padx=10, pady=(15, 5))

    export_file = open('export_file.txt', 'w')
    export_file.write(out_below)
    export_file.write(str(translation))
    webbrowser.open("export_file.txt")

    return filename

file_frame = LabelFrame(root, text='Source Image To Be Processed', font="Verdana 10 bold", labelanchor=N)
file_frame.grid(row=0, column=0, padx=(10, 5), pady=5)

open_button = Button(file_frame, text='Open an Image File', font=("Verdana", 10), justify=CENTER, command=main_func)
open_button.grid(row=1, column=0, sticky=N, padx=10, pady=(15, 5))


root.mainloop()

