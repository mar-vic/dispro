import sys
import os
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) < 2:
        print("I need a path to a PDF file!")
        return

    input_file  = sys.argv[1]
    output_dir = os.path.dirname(input_file)
    output_file = f"{output_dir}/{os.path.basename(output_dir)}__OCR.html"

    image_file_list = []

    with TemporaryDirectory() as tempdir:
        print("Getting pdf pages ...")
        pdf_pages = convert_from_path(input_file, 500)

        print("Generating images ...")
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

    text = ""

    with open(output_file, "w") as output_file:
        print("Extracting text from images ...")
        for image_file in image_file_list:
            text += str(((pytesseract.image_to_string(Image.open(image_file), lang="slk"))))
        text = text.replace("-\n", "")
        text = BeautifulSoup(f"<html><body>{text}</body></html>", "html.parser")
        output_file.write(str(text.prettify()))

if __name__ == "__main__":
    main()
