# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:51:18 2021

@author: mathe
"""

## Splits a pdf into images for OCR processes

from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path
from PIL import Image
import os
import re

def splitPdf(pathIn, folderOut, first_page = None, last_page = None):

    os.chdir(folderOut)

    print("starting conversion")

    convert_from_path(pathIn, dpi= 300, output_folder = folderOut, use_pdftocairo=True, first_page = first_page, last_page = last_page)

    print("converted")


def splitSelection(pdfDir, outDir, firstPage = None, pageCount = None):
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

def image_dir_to_pdf(image_dir, pdf_path):
    """Take a directory of images and recreate a pdf"""
    images = [Image.open(image_dir + f)
    for f in os.listdir(image_dir)
    ]    
    
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

# pdfDir = "/mnt/d/Primary sources/manuscripts/"
# outFolder = "/mnt/c/Users/mathe/Downloads/"

# print(pdfDir)




# for folder in os.listdir(generalDir):
#     print(folder)
#     folderPath = os.path.join(generalDir, folder)

# splitSelection(pdfDir, outFolder, firstPage=30, pageCount = 2)

