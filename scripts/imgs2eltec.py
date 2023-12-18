#!/usr/bin/env python3

import sys, os
import json, random
from pathlib import Path
from datetime import date
from lxml import etree

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from bs4 import BeautifulSoup

def validate(path):
    xml = etree.parse(path) # reading the xml
    rng_doc = etree.parse("/home/marcus/Projects/third_party/eltec-schemas/eltec-1.rng") # reading the RelaxNG definitions
    rng = etree.RelaxNG(rng_doc)

    if rng.validate(xml):
        print("Document is valid against eltec-1 scheme!")
    else:
        print("Document is invalid!", rng.error_log)

def ocr_images(input_dir, output_file):
    # Get only image files
    img_paths = [Path(path) for path in os.listdir(input_dir) if Path(path).suffix.lower() in [".jpg", ".jpeg", ".png"]]

    breakpoint()

    # Sort image file names so that they correspond to page ordering
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0].split("-")[2]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0].split("_")[1]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0]))
    # image_file_names = sorted(image_file_names, key=lambda img_name: int(img_name.split(".")[0][1:]))
    try:
        img_paths = sorted(img_paths, key=lambda path: int(path.stem)) # assuming that image file names are numbers
    except ValueError:
        img_paths = sorted(img_paths, key=lambda path: path.stem.split(" ")[-1].replace("-",":")) # assuming that image file names are timestamps

    # breakpoint()



    text = ""

    with open(output_file, "w") as f:
        print("Extracting text from images ...")
        idx = 0
        for path in img_paths:
            idx += 1
            os.system("clear")
            print(f"Progress: {idx} / {len(img_paths)} ({'{0:.2f}'.format((idx / len(img_paths)) * 100)}%)")
            print(f"Processing file: {path}")
            text += str(((pytesseract.image_to_string(Image.open(path.absolute()), lang="slk"))))
        f.write(text.replace("", "<pb></pb>"))

    with open(output_file, "r") as f:
        lines = f.readlines()
        # breakpoint()

    with open(output_file, "w") as f:
        f.write("<TEI xmlns='http://www.tei-c.org/ns/1.0'>\n")

        f.write("<text>\n<front>\n<div type='titlepage'>\n<head></head>\n</div>\n</front>\n<body><p>\n")

        for index, line in enumerate(lines):
            if line == "\n" and index + 1 < len(lines) and lines[index + 1] != "\n":
                f.write("</p>\n<p>\n")
                continue
            elif line != "\n":
                f.write(line)

        f.write("</p>\n</body>\n</text></TEI>")

    # generating xml with ELTeC conformant header
    # responses = eltec.promptHeaderData() # collecting data from user
    if len(sys.argv) < 2:
        print("ELTeC header will be populated with empty strings, since no data was supplied.")
        with open("/home/marcus/Projects/dispro/scripts/templates/eltec_header_data.json", "r", encoding="utf-8") as empty_header_data_file:
            header_data = json.load(empty_header_data_file)
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as header_data_file:
            header_data = json.load(header_data_file)

    # values need to be quoted to be registered in xslt
    xslt_params = {k:f"'{v}'" for (k,v) in zip(header_data["xslt_params"].keys(), header_data["xslt_params"].values())}

    # constructing the value of <author> and adding it to the xslt parameters
    author = f"{header_data['author_last_name']}, {header_data['author_first_name']}"
    author += f" [{header_data['author_alter_name']}]" if header_data["author_alter_name"] != "" else "" # In case autho has alter name
    author += f" ({header_data['author_birth_date']}-{header_data['author_death_date']})"
    xslt_params["author"] = f"'{author}'"

    # Constructing the random part of id (rest of the id is generated from lang and pub_date in xslt)
    xslt_params["id"] = str(random.randint(0, 1000))

    # Constructing creation date
    today = date.today()
    xslt_params["creation_date"] = f"'{today.year}-{today.month}-{today.day}'"

    # Applying schema with parameters
    schema = etree.XSLT(etree.parse("/home/marcus/Projects/dispro/scripts/schemas/eltec.xsl")) # reading the eltec schema
    xml = etree.parse(output_file)
    xml = schema(xml, **xslt_params) # applying the schema with parameters
    xml.write(output_file, encoding='utf-8', pretty_print=True)

    print(f"Successfully created document {output_file}!")

    # Validating the document just generated against the rng produced by ELTeC group
    validate(output_file)


def main():
    print("Using working directory!")
    input_directory = os.getcwd()

    output_file = input(f"Enter the name of the output file or leave blank tu use '{input_directory}/{os.path.basename(input_directory)}__OCR.html': ")
    if output_file == "":
        output_file = f"{os.path.basename(input_directory)}__OCR.html"
    else:
        output_file = f"{output_file}"

    ocr_images(input_directory, output_file)

if __name__ == "__main__":
    main()
