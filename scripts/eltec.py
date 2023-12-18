from __future__ import print_function, unicode_literals

from os.path import dirname, join

from random import randrange
from datetime import datetime

from PyInquirer import prompt
from pprint import pprint

import xml.etree.ElementTree as ET

from jinja2 import Environment, FileSystemLoader
import jinja2

from lxml import etree

project_root = dirname(dirname(__file__))

def generate_eltec_text(html_file):
    html = etree.parse(html_file)
    schema = etree.XSLT(etree.parse("./schemas/"))

def promptHeaderData():
    def validate_year(user_input):
        try:
            datetime.strptime(user_input, "%Y")
        except ValueError:
            return "This is not a valid year!"
        return True

    def validate_extent(user_input):
        try:
            if int(user_input) > 0:
                return True
            return "The number should be more than 0."
        except ValueError:
            return "The value should be number."

    questions = [
        {
            "type": "input",
            "name": "title",
            "message": "Book title (use standard form of title, simplified if necessary)"
        },

        {
            "type": "confirm",
            "name": "title_ref_confirm",
            "message": "Do you want to enter Book's VIAF (or other indentifying code for the book)"
        },

        {
            "type": "input",
            "name": "title_ref",
            "message": "Book VIAF (or other identifying code for the book)",
            "when": lambda answers: answers["title_ref_confirm"]
        },

        {
            "type": "confirm",
            "name": "author_ref_confirm",
            "message": "Do you want to enter author's VIAF (or other indentifying code for the author)"
        },

        {
            "type": "input",
            "name": "author_ref",
            "message": "Author's VIAF (or other identifying code for the author)",
            "when": lambda answers: answers["author_ref_confirm"]
        },

        {
            "type": "input",
            "name": "author_last_name",
            "message": "Author's last name"
        },

        {
            "type": "input",
            "name": "author_first_name",
            "message": "Author's first name"
        },

        {
            "type": "confirm",
            "name": "author_alter_name_confirm",
            "message": "Does the author have alternative name?"
        },

        {
            "type": "input",
            "name": "author_alter_name",
            "message": "Author's alternative name",
            "when": lambda answers: answers["author_alter_name_confirm"],
        },

        {
            "type": "input",
            "name": "author_birth_date",
            "message": "Author's date of birth",
            "validate": validate_year
        },

        {
            "type": "input",
            "name": "author_death_date",
            "message": "Author's date of passing",
            "validate": validate_year
        },

        {
            "type": "input",
            "name": "words",
            "message": "Book's word count",
            "validate": validate_extent
        },

        {
            "type": "confirm",
            "name": "pagecount_confirm",
            "message": "Do you want to enter number of pages in the book?"
        },

        {
            "type": "input",
            "name": "pages",
            "message": "Book page count",
            "when": lambda answers: answers["pagecount_confirm"],
            "validate": validate_extent
        },

        {
            "type": "confirm",
            "name": "volumecount_confirm",
            "message": "Do you want to enter the number of volumes the book is comprised of?"
        },

        {
            "type": "input",
            "name": "vols",
            "message": "Book page count",
            "when": lambda answers: answers["volumecount_confirm"],
            "validate": validate_extent
        },

        {
            "type": "input",
            "name": "pub_place",
            "message": "Publication place of the print edition from which the ELTeC edition is derived"
        },

        {
            "type": "input",
            "name": "publisher",
            "message": "Publisher of the print edition from which the ELTeC edition is derived"
        },

        {
            "type": "input",
            "name": "pub_date",
            "message": "Publication date of the print edition from which the ELTeC edition is derived",
            "validate": validate_year
        },

        {
            "type": "confirm",
            "name": "firsted_confirm",
            "message": "Do you want to add info about the first edition (only for cases where the ELTeC edition is not derived from the first edition)"
        },

        {
            "type": "input",
            "name": "firsted_pub_place",
            "message": "Publication place of the first edition",
            "when": lambda answers: answers["firsted_confirm"],
        },

        {
            "type": "input",
            "name": "firsted_publisher",
            "message": "Publisher of the first edition",
            "when": lambda answers: answers["firsted_confirm"],
        },

        {
            "type": "input",
            "name": "firsted_pub_date",
            "message": "Publication date of the first edition",
            "when": lambda answers: answers["firsted_confirm"],
            "validate": validate_year
        },

        {
            "type": "confirm",
            "name": "digitaled_confirm",
            "message": "Do you want to add info about digital edition (if another digital version of the text is also available e.g. as page images)"
        },

        {
            "type": "input",
            "name": "digitaled_url",
            "message": "URL of digital edition",
            "when": lambda answers: answers["digitaled_confirm"],
        },

        {
            "type": "list",
            "name": "encoding_lvl",
            "message": "Select the level of ELTeC endocding",
            "choices": [ "eltec-0", "eltec-1", "eltec-2" ],
            "default": "eltec-1"
        },

        {
            "type": "list",
            "name": "gender",
            "message": "What's the author's gender? ('F' for female, 'M' for male and 'U' for unknown or multiple.)",
            "choices": [ "F", "M", "U" ]
        },

        {
            "type": "list",
            "name": "size",
            "message": "Size of the book? short (10 - 50k), medium (50 - 100k)) or long (> 100k) (wordcount excluding header and all markup)",
            "choices": [ "short", "medium", "long" ]
        },

        {
            "type": "list",
            "name": "timeSlot",
           "message": "'Timeslot' in which the book was first published? T1 (1840-1859)	T2 (1860-1879)	T3 (1880-1899)	T4 (1900-1920)",
            "choices": [ "T1", "T2", "T3", "T4" ]
        },

        {
            "type": "list",
            "name": "canonicity",
            "message": "Number of times reprinted between 1970 and 2009? low (reprinted infrequently or never)	high (reprinted very frequently)	unspecified (reprint information not available)",
            "choices": [ "low", "high", "unspecified" ]
        },
    ]

    return prompt(questions)

def generate_eltec_file(header_data, text=None, output_dir="."):
    file_name = f"{header_data['book_title']}({header_data['author_last_name']}).xml"

    # Initialize jinja2 templating
    environment = Environment(loader=FileSystemLoader(f"{project_root}/scripts/templates/"))
    eltec_template = environment.get_template("eltec.xml")

    with open(f"{output_dir}/{file_name}", mode="w", encoding="utf-8") as f:
        # render the template with header data and write the xml file
        f.write(eltec_template.render(header_data))

def main():
    generate_eltec_file(promptHeaderData())

if __name__ == "__main__":
    main()

