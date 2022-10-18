# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:51:18 2021

@author: mathe
"""

## Splits a pdf into images for OCR processes

from pdf2image import convert_from_path
import os

def splitPdf(pathIn, folderOut):

    os.chdir(folderOut)

    print("starting conversion")

    convert_from_path(pathIn, dpi= 300, output_folder = folderOut, poppler_path='C:/Program Files/poppler-0.68.0/bin', use_pdftocairo=True)

    print("converted")

pdfDir = "D:/Primary sources/manuscripts/Opuscules_de_Maqrîzî_A_MAD_ibn_btv1b52504743c.pdf"
outFolder = "C:/Users/mathe/Documents/Kitab project/For_OCR/Maqrizi_Rasail"

for root, dirs, files in os.walk(pdfDir, topdown=False):
    for name in files:
        filePath = os.path.join(root, name)
        newFolderName = ".".join(name.split(".")[0:-1]) + "/"
        outPath = os.path.join(outFolder, newFolderName)
        if not os.path.exists(outPath):
            os.mkdir(outPath)
        print(filePath)
        print(outPath)
        splitPdf(filePath, outPath)

