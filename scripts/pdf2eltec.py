#!/usr/bin/env python3

import os, sys, requests, random

from lxml import etree
from pathlib import Path
from datetime import date
import json

from pdf2docx import parse

import eltec

def validate(path):
    xml = etree.parse(path) # reading the xml
    rng_doc = etree.parse("/home/marcus/Projects/third_party/eltec-schemas/eltec-1.rng") # reading the RelaxNG definitions
    rng = etree.RelaxNG(rng_doc)

    if rng.validate(xml):
        print("Document is valid against eltec-1 scheme!")
    else:
        print("Document is invalid!", rng.error_log)

def main():
    if len(sys.argv) < 2:
        print("You need to provide a path to a PDF file to converse.")
        return

    if not os.path.isfile(sys.argv[1]):
        print(f"'{sys.argv[1]}' is not a file!")
        return

    input_file = Path(sys.argv[1])

    # if len(sys.argv) < 3:
    #     print("Using input file name and parent directory for output.")
    #     output_file = input_file.parent.joinpath(input_file.stem + ".docx")
    # else:
    #     output_file = Path(sys.argv[2])

    output_file = input_file.parent.joinpath(input_file.stem + ".docx")

    # converting from pdf to docx
    parse(input_file.absolute(), output_file.absolute())

    # converting from docx to tei xml
    with open(output_file.absolute(), "rb") as docx_file:
        # URL of the webservice for converting docx to TEI XML
        converter_endpoint = "https://teigarage.tei-c.org/ege-webservice/Conversions/docx%3Aapplication%3Avnd.openxmlformats-officedocument.wordprocessingml.document/TEI%3Atext%3Axml/"
        # Issuing POST to the endpoint
        # breakpoint()
        print("Converting from docx to tei xml ...")
        response = requests.post(converter_endpoint, files={"file": docx_file})

    # The response has wrong encoding for some reason, so we are correcting it
    response.encoding = "utf-8"

    # writing the conversion sent by the endpoint to the file
    output_file = output_file.parent.joinpath(output_file.stem + ".xml")
    # breakpoint()
    with open(output_file.absolute(), "w", encoding="utf-8") as tei_file:
        tei_file.write(response.text)

    # Cleaning-up unwanted artifacts from docx tranformation
    xml = etree.parse(output_file.absolute()) # reading the xml
    schema = etree.XSLT(etree.parse("/home/marcus/Projects/dispro/scripts/schemas/clean.xsl")) # reading the 'cleaning' schema
    xml_cleaned = schema(xml) # applying the schema
    xml_cleaned.write(output_file.absolute(), encoding='utf-8', pretty_print=True)

    # generating xml with ELTeC conformant header
    # responses = eltec.promptHeaderData() # collecting data from user
    if len(sys.argv) < 3:
        print("ELTeC header will be populated with empty strings, since no data was supplied.")
        with open("/home/marcus/Projects/dispro/scripts/templates/eltec_header_data.json", "r", encoding="utf-8") as empty_header_data_file:
            header_data = json.load(empty_header_data_file)
    else:
        with open(sys.argv[2], "r", encoding="utf-8") as header_data_file:
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
    xml_eltec = schema(xml_cleaned, **xslt_params) # applying the schema with parameters
    xml_eltec.write(output_file.absolute(), encoding='utf-8', pretty_print=True)

    print(f"Successfully created document {output_file}!")

    # Validating the document just generated against the rng produced by ELTeC group
    validate(output_file.absolute())

if __name__ == "__main__":
    main()
