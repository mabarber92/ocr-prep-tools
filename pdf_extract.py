# -*- coding: utf-8 -*-
"""
Converter for Pdfs that contain text - page markers can be specified 
with a regex to insert page numbers in the relevant places
"""

import os
from tika import parser
import re
from PyPDF2 import PdfFileReader, PdfFileWriter

def page_sub(match):
    new_form = "PageV01P"
    page = match.group(1)
    page = str(int(page) - 1)
    rep = new_form + page.zfill(3)
    return rep





def extract_text(in_pdf, out_text, page_left = None, page_right = None, large_file = False):
    
    if large_file:
        text = ""
        print("Large file... converting in chunks")        
        pdf = PdfFileReader(in_pdf)
        pdf_length = pdf.getNumPages()
        print(pdf_length)
        fname = "temp.pdf"
        
        # for page in range(0, 100, 1):
        #     print(page)
        #     pdf_writer = PdfFileWriter()
        #     pdf_writer.addPage(pdf.getPage(page))
        
        #     output_filename = '{}_page_{}.pdf'.format(fname, page+1)
        for x in range(0, pdf_length, 100):
            print("Splitting " + str(x) + " to " + str(x+99))
            writer = PdfFileWriter()
            for i in range(x, x+99, 1):                
                if i > pdf_length-1:
                    print("index over")                    
                    break
                else:
                    writer.addPage(pdf.getPage(i))
                
            with open(fname, 'wb') as out:
                # writer = PdfFileWriter()
                # for i in range(x, x+299, 1):
                #     writer.addPage(pdf.getPage(i))
                writer.write(out)
            print("Passing to extractor")
            extract = parser.from_file(fname)
                     
    
            with open(out_text, "r", encoding = "utf-8") as f:
                text = f.read()
                f.close()
            with open(out_text, "w", encoding = "utf-8") as f:
                f.write(text + "\n" + extract["content"])
                f.close()
            os.remove(fname)
            

  
    else:
        # Extract text
        extract = parser.from_file(in_pdf)
        text = extract["content"]
        
        # Insert markdown compliant page numbers
        if page_left is not None:
            text = re.sub(page_left, page_sub, text)
        if page_right is not None:
            text = re.sub(page_right, page_sub, text)
    
        with open(out_text, "w", encoding = "utf-8") as f:
            f.write(text)
            f.close()

# Specify path for pdf in
in_path = "fankha.pdf"
# Specify path for text out
out_path = "fankha_export.txt"
if not os.path.exists(out_path):
    open(out_path, "x")
# If you wish specify a regex to grap page number on left page - if not using - remove the argument from function
page_left = "(\d+) TEXT AFTER PAGE NUMBER"

# If you wish specify a regex to grap page number on right page - if not using - remove the argument from function
page_right = "TEXT BEFORE PAGE NUMBER (\d+)"

extract_text(in_path, out_path, large_file=True)

