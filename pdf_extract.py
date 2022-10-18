# -*- coding: utf-8 -*-
"""
Converter for Pdfs that contain text - page markers can be specified 
with a regex to insert page numbers in the relevant places
"""

import os
from tika import parser
import re

def page_sub(match):
    new_form = "PageV01P"
    page = match.group(1)
    page = str(int(page) - 1)
    rep = new_form + page.zfill(3)
    return rep





def extract_text(in_pdf, out_text, page_left = None, page_right = None):
    
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
in_path = "D:/Primary sources/Sulami/Pdfs/06 ArabicPart2(37-73).pdf"
# Specify path for text out
out_path = "test_output.txt"

# If you wish specify a regex to grap page number on left page - if not using - remove the argument from function
page_left = "(\d+) TEXT AFTER PAGE NUMBER"

# If you wish specify a regex to grap page number on right page - if not using - remove the argument from function
page_right = "TEXT BEFORE PAGE NUMBER (\d+)"

extract_text(in_path, out_path, page_left, page_right)

