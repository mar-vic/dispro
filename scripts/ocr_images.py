import sys
import os
import re
import platform
from tempfile import TemporaryDirectory
from pathlib import Path
 
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from bs4 import BeautifulSoup

def ocr_images(input_dir, output_file):
    # regex patter for extracting numbers from file names
    # pattern = r'-?\b0*[1-9][0-9]*\.\d+|\b-?0*[1-9][0-9]*\b|\b-0+\b'

    # Get only image file names with correct formatting (ie, ones containg number)
    image_file_names = [Path(img_name) for img_name in os.listdir(input_dir)]

    # breakpoint()

    # Sort image file names so that they correspond to page ordering
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0].split("-")[2]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0].split("_")[1]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0][1:]))
    image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.stem))

    # breakpoint()

    # Genrate absolute paths
    # image_file_paths = [f"{input_dir}/{img_name}" for img_name in image_file_names if os.path.isfile(f"{input_dir}/{img_name}")]

    text = ""


    with open(output_file, "w") as output_file:
        print("Extracting text from images ...")
        idx = 0
        for path in image_file_names:
            idx += 1
            os.system("clear")
            print(f"Progress: {idx} / {len(image_file_names)} ({'{0:.2f}'.format((idx / len(image_file_names)) * 100)}%)")
            print(f"Processing file: {path}")
            text += str(((pytesseract.image_to_string(Image.open(path.absolute()), lang="slk"))))
        text = text.replace("-\n", "")
        text = BeautifulSoup(f"<html><body>{text}</body></html>", "html.parser")
        output_file.write(str(text.prettify()))


def main():
    if len(sys.argv) < 2:
        print("Using working directory!")
        input_directory = os.getcwd()
    else:
        input_directory = sys.argv[1]

    if len(sys.argv) < 3:
        output_file = input(f"Enter the name of the output file or leave blank tu use '{input_directory}/{os.path.basename(input_directory)}__OCR.html': ")
        if output_file == "":
            output_file = f"{os.path.basename(input_directory)}__OCR.html"
        else:
            output_file = f"{output_file}"
    else:
        output_file = sys.argv[2]

    output_file = f"{input_directory}/{output_file}"

    ocr_images(input_directory, output_file)

if __name__ == "__main__":
    main()
