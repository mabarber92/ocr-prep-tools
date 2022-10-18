# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:38:04 2022

@author: mathe
"""

# import PyMuPDF
# from scipy import misc
# import os


# # Function to split images once we have them
# def splitImages(imgDir):
#     os.chdir(imgDir)
#     for root, dirs, files in os.walk(".", topdown=False):
#         for name in files:
#             image_path = os.path.join(root, name)         
#             img = misc.imread(image_path)
#             height, width = img.shape
            
#             # Cut the image in half
#             width_cutoff = width // 2
#             s1 = img[:, :width_cutoff]
#             s2 = img[:, width_cutoff:]
            
            
#             newImagePath1 = image_path.split()
#             # Save each half
#             misc.imsave(, s1)
#             misc.imsave("face2.png", s2)

"""
Create a PDF copy with split-up pages (posterize)
---------------------------------------------------
License: GNU AFFERO GPL V3
(c) 2018 Jorj X. McKie

Usage
------
python posterize.py input.pdf

Result
-------
A file "poster-input.pdf" with 4 output pages for every input page.

Notes
-----
(1) Output file is chosen to have page dimensions of 1/4 of input.

(2) Easily adapt the example to make n pages per input, or decide per each
    input page or whatever.

Dependencies
------------
PyMuPDF 1.12.2 or later
"""
import fitz


def pdfImageSplit(infile):
    src = fitz.open(infile)
    doc = fitz.open()  # empty output PDF
    
    for spage in src:  # for each page in input
        r = spage.rect  # input page rectangle
        d = fitz.Rect(spage.cropbox_position,  # CropBox displacement if not
                      spage.cropbox_position)  # starting at (0, 0)
        #--------------------------------------------------------------------------
        # example: cut input page into 2 x 2 parts
        #--------------------------------------------------------------------------
        r1 = fitz.Rect(0, 0, r.width/2, r.height)
        r2 = fitz.Rect(r.width/2, 0, r.width, r.height)  # top right rect
        # r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left rect
        # r4 = fitz.Rect(r1.br, r.br)  # bottom right rect
        rect_list = [r2, r1]  # put them in a list
    
    
        for rx in rect_list:  # run thru rect list
            rx += d  # add the CropBox displacement
            page = doc.new_page(-1,  # new output page with rx dimensions
                               width = rx.width,
                               height = rx.height)
            page.show_pdf_page(
                    page.rect,  # fill all new page with the image
                    src,  # input document
                    spage.number,  # input page number
                    clip = rx,  # which part to use of input page
                )
    
    # that's it, save output file
    doc.save("split-" + src.name,
             garbage=3,  # eliminate duplicate objects
             deflate=True,  # compress stuff where possible
    )

# Add path to file - will output to same path but with 'split-' added to file name
infile = ""
pdfImageSplit(infile)
