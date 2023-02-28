# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:51:18 2021

@author: mathe
"""

## Splits a pdf into images for OCR processes

from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
import os
import re

def splitPdf(pathIn, folderOut, first_page = None, last_page = None):

    os.chdir(folderOut)

    print("starting conversion")

    convert_from_path(pathIn, dpi= 300, output_folder = folderOut, use_pdftocairo=True, first_page = first_page, last_page = last_page)

    print("converted")


def splitSelection(pdfDir, outDir, firstPage = 30, pageCount = None):
    for root, dirs, files in os.walk(pdfDir, topdown=False):
        for name in files:
            if re.search("\.pdf", name):
                filePath = os.path.join(root, name)
                # newFolderName = ".".join(name.split(".")[0:-1]) + "/"
                newFolderName = os.path.join(root, "YME-images")
                outPath = os.path.join(outDir, newFolderName)
                if not os.path.exists(outPath):
                    os.mkdir(outPath)
                print(filePath)
                print(outPath)
                if not pageCount:
                    splitPdf(filePath, outPath)
                else:
                    pageTotal = pdfinfo_from_path(filePath)["Pages"]
                    if pageCount > pageTotal:
                        print("Too few pages for count splitting entire pdf")
                        splitPdf(filePath, outPath)
                    else:
                        while firstPage + pageCount > pageTotal:
                            firstPage = firstPage - 1                 
                        splitPdf(filePath, outPath, first_page = firstPage, last_page = firstPage + pageCount)



# pdfDir = "/mnt/d/Primary sources/manuscripts/"
# outFolder = "/mnt/c/Users/mathe/Downloads/"

# print(pdfDir)

generalDir = "/mnt/c/Users/mathe/Documents/Github-repos/DH23/session_6/Yousef"
print(generalDir)

# for folder in os.listdir(generalDir):
#     print(folder)
#     folderPath = os.path.join(generalDir, folder)

splitSelection(generalDir, generalDir, firstPage=30, pageCount = 10)


# splitSelection(pdfDir, outFolder, firstPage=30, pageCount = 2)

