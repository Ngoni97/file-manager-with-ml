#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 04:18:28 2025

@author: ngoni97
"""
# using pytesseract to read ocr pdf

import os
#import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

filePath = '/home/ngoni97/Documents/MATHEMATICS/Principia Mathematica/Principia_Mathematica [volume.I] alfred_north_whitehead x betrand_russell.pdf'
doc = convert_from_path(filePath, last_page=10)
#img = cv2.imread(filePath)
path, fileName = os.path.split(filePath)
fileBaseName, fileExtension = os.path.splitext(fileName)

i = 0
for page_number, page_data in enumerate(doc):
    #txt = pytesseract.image_to_string(page_data).encode("utf-8")
    txt = pytesseract.image_to_string(Image.fromarray(page_data).encode("utf-8"))
    print("Page # {} - {}".format(str(page_number),txt))
    i += 1
    if i == 5:
        break