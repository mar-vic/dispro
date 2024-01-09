# Collections of functions used to generate, validate and present the corpus

import os, sys
import zipfile, json, random, string

import pytesseract

from datetime import date
from pathlib import Path
from lxml import etree
from PIL import Image
from livereload import Server

from jinja2 import Environment, PackageLoader, select_autoescape

project_dir = Path(__file__).absolute().parents[1]
schemas_dir = project_dir.joinpath("schemas")
corpus_dir = project_dir.joinpath("data/ELTEC_FILES")
templates_dir = project_dir.joinpath("scripts/templates")

# Functions used to generate ELTeC XMLs
# -------------------------------------
def get_header_data(path):
    """Extracting data from eltec headers with xpath."""
    header_data = {}
    xml = etree.parse(path)

    # Author and title name
    author = xml.xpath("//tei:titleStmt/tei:author/text()",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["author"] = author[0] if len(author) > 0 else ""

    author_ref = xml.xpath("//tei:titleStmt/tei:author/@ref",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["author_ref"] = author_ref[0] if len(author_ref) > 0 else ""

    title = xml.xpath("//tei:titleStmt/tei:title/text()",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["title"] = title[0] if len(title) > 0 else ""

    # Info about source edition
    print_source_ref = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:title/@ref",
                              namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["srced_ref"] = print_source_ref[0] if len(print_source_ref) > 0 else ""

    print_source_publisher = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:publisher/text()",
                              namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["srced_publisher"] = print_source_publisher[0] if len(print_source_publisher) > 0 else ""

    print_source_pub_place = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:pubPlace/text()",
                                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["srced_pub_place"] = print_source_pub_place[0] if len(print_source_pub_place) > 0 else ""

    print_source_pub_date = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:date/text()",
                                      namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["srced_pub_date"] = print_source_pub_date[0] if len(print_source_pub_date) > 0 else ""

    # Info about first edition
    firsted_publisher = xml.xpath("//tei:sourceDesc/tei:bibl[@type='firstEdition']/tei:publisher/text()",
                                  namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["frsted_publisher"] = firsted_publisher[0] if len(firsted_publisher) > 0 else ""

    firsted_pub_place = xml.xpath("//tei:sourceDesc/tei:bibl[@type='firstEdition']/tei:pubPlace/text()",
                                  namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["frsted_pub_place"] = firsted_pub_place[0] if len(firsted_pub_place) > 0 else ""

    firsted_ref = xml.xpath("//tei:sourceDesc/tei:bibl[@type='firstEdition']/tei:title/@ref",
                            namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["frsted_ref"] = firsted_ref[0] if len(firsted_ref) > 0 else ""

    firsted_pub_date = xml.xpath("//tei:sourceDesc/tei:bibl[@type='firstEdition']/tei:date/text()",
                                 namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["frsted_pub_date"] = firsted_pub_date[0] if len(firsted_pub_date) > 0 else ""

    # The rest: encoding level, gender, size, time slot and cononicity
    encoding_lvl = xml.xpath("//tei:encodingDesc/@n",
                             namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["encoding_lvl"] = encoding_lvl[0] if len(encoding_lvl) > 0 else ""

    gender = xml.xpath("//eltec:authorGender/@key",
                       namespaces={
                           "tei": "http://www.tei-c.org/ns/1.0",
                           "eltec": "http://distantreading.net/eltec/ns"
                       })
    header_data["gender"] = gender[0] if len(gender) > 0 else ""

    size = xml.xpath("//eltec:size/@key",
                     namespaces={
                         "tei": "http://www.tei-c.org/ns/1.0",
                         "eltec": "http://distantreading.net/eltec/ns"
                    })
    header_data["size"] = size[0] if len(size) > 0 else ""

    canonicity = xml.xpath("//eltec:canonicity/@key",
                     namespaces={
                         "tei": "http://www.tei-c.org/ns/1.0",
                         "eltec": "http://distantreading.net/eltec/ns"
                     })
    header_data["canonicity"] = canonicity[0] if len(canonicity) > 0 else ""

    time_slot = xml.xpath("//eltec:timeSlot/@key",
                          namespaces={
                              "tei": "http://www.tei-c.org/ns/1.0",
                              "eltec": "http://distantreading.net/eltec/ns"
                          })
    header_data["time_slot"] = time_slot[0] if len(time_slot) > 0 else ""

    return header_data

def generate_eltec_file(path=None, text=None, header_data_file=f"{templates_dir}/eltec_header_data.json"):
    """
    Writes an xml file valid relative to the eltec-1 scheme. The XML is
    generated via parametrised xslt schema. Can be given header data file and /
    or 'text' to be used within ELTeC '<teiHeader>' and '<body>' tags
    respectivelly.
    """
    schema = etree.XSLT(etree.parse(f"{schemas_dir}/eltec.xsl")) # Loading the schema

    # Unloading the ELTeC header data from json into dictionary
    with open(header_data_file, "r", encoding="utf-8") as f:
        header_data = json.load(f)

    # values need to be quoted in order to be processed by xslt
    xslt_params = {k:f"'{v}'" for (k,v) in zip(header_data["xslt_params"].keys(), header_data["xslt_params"].values())}

    # constructing the value of <author> and adding it to the xslt parameters
    author = f"{header_data['author_last_name']}, {header_data['author_first_name']}"
    author += f" [{header_data['author_alter_name']}]" if header_data["author_alter_name"] != "" else "" # In case autho has alter name
    author += f" ({header_data['author_birth_date']}-{header_data['author_death_date']})"
    xslt_params["author"] = f"'{author}'"

    # Constructing the random part of id (rest of the id is generated from lang and pub_date in xslt)
    xslt_params["id"] = str(random.randint(0, 1000))

    # Constructing creation date
    xslt_params["creation_date"] = date.today().isoformat()

    if not path:
        # Generating file name if none was given
        breakpoint()
        path = Path(f"{header_data['xslt_params']['title'].lower().replace(' ','_')}__{header_data['author_last_name'].lower()}.xml")
    else:
        path = Path(path)

    # (re)writing / updating / cancelling the eltec file
    if path.exists():
        mode = input(f"\nThe file '{path}' already exists. Enter 'w' for rewrite, 'u' for update, or anything else to cancel the operation: ")
        if mode == "w": # Rewriting
            print(f"\nRewriting {path.name} ...")

            # applying the schema to an xml object
            eltec_file = schema(etree.XML(f"<body xmlns='http://www.tei-c.org/ns/1.0'>{text if text else '<p></p>'}</body>"), **xslt_params)

            # writing the result of transformation to the file at path
            eltec_file.write(path, encoding='utf-8', pretty_print=True)

        elif mode == "u": # Updating
            print(f"\nUpdating {path.name} ...")

            # Updating the header data
            header_data_og = get_header_data(path)
            header_data_og.update(xslt_params)

            # parsing <body> contents from the original file if no new contents were provided
            if not text:
                try:
                    text = etree.tostring(etree.parse(path).xpath("//tei:body/*", namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })[0])
                    text = text.decode("utf-8") # decoding from bytes to string
                except IndexError:
                    text = "<p></p>"

            # applying the schema to a dummy xml object
            eltec_file = schema(etree.XML(f"<body xmlns='http://www.tei-c.org/ns/1.0'>{text}</body>"), **xslt_params)

            # writing the result of transformation to the file at path
            eltec_file.write(path, encoding='utf-8', pretty_print=True)

        else: # Cancelling
            print("\nCancelling the operation.")
            return
    else: # Creating
        print(f"\nCreating {path.name} ...")
        eltec_file = schema(etree.XML(f"<body xmlns='http://www.tei-c.org/ns/1.0'>{text if text else '<p></p>'}</body>"), **xslt_params)
        eltec_file.write(path, encoding='utf-8', pretty_print=True)

    # Validating the file
    is_valid, errors = eltec_validate_file(path.absolute())
    if not is_valid:
        print(f"\nThe file '{path}' is invalid relative to the eltec-1 schema:\n")
        print(errors)
    else:
        print(f"\nThe file '{path}' is valid relative to the eltec-1 schema.\n")

    
# Functions for transforming various digital sources of texts to pluggable eltec fragments
# ----------------------------------------------------------------------------------------
def get_eltec_body_from_images(input_dir):
    """
    Generating a valid xml fragment pluggable into eletec-1 <body> out of set
    of images contained within input_dir.
    """
    # Get the paths to image files within the input_dir
    img_paths = [Path(path) for path in os.listdir(input_dir) if Path(path).suffix.lower() in [".jpg", ".jpeg", ".png", ".pbm"]]

    if len(img_paths) == 0:
        print(f"There are no images in provided directory ('{input_dir}')")
        return None

    # Sorting in order to preserve the sequence of pages in the original. It is
    # assumed that the name of images are comprised of numbers representing
    # page order.
    try:
        img_paths = sorted(img_paths, key=lambda path: int(path.stem.replace("-", ""))) # assuming that image file names are numbers
    except ValueError:
        img_paths = sorted(img_paths, key=lambda path: path.stem.split(" ")[-1].replace("-",":")) # assuming that image file names are timestamps

    # Extracting text from imges with the help of pytesseract
    text = ""
    print("Extracting text from images ...")
    for idx, path in enumerate(img_paths):
        os.system("clear")
        print(f"Progress: {idx} / {len(img_paths)} ({'{0:.2f}'.format((idx / len(img_paths)) * 100)}%)")
        print(f"Processing file: {path}")
        text += str(((pytesseract.image_to_string(Image.open(path.absolute()), lang="slk"))))

    # Clean-up
    text.replace("", "<pb></pb>") # The '' character represents a page break

    # getting list paragraphs and removing whitespace characters
    text = [paragraph.strip(string.whitespace) for paragraph in text.split("\n\n")]

    # removing empty paragraphs
    text = [f"<p>{paragraph}</p>" for paragraph in text if len(paragraph) != paragraph.count(" ")]

    # collating into string
    text = "".join(text)
    breakpoint()
    return "".join(text)

# Functions for XML vliadtion against ELTeC schemas
# -------------------------------------------------
def eltec_validate_file(xml_path, schema_path=schemas_dir.joinpath("eltec-1.rng").absolute()):
    """Validate individual xml file against (eltec-1) schema."""
    xml = etree.parse(xml_path) # reading the xml to validate

    # Lading schema definition
    rng = etree.parse(schema_path)
    rng = etree.RelaxNG(rng)

    # Validating the document
    if rng.validate(xml):
        return (True, None)
    else:
        # Providing error log, when the document is invalid
        return (False, rng.error_log)

def eltec_validate_corpus(schema_path=schemas_dir.joinpath("eltec-1.rng").absolute()):
    """Validating the whole corpus (i.e., files in corpus_dir). Returning empty
    list, if all files are valid, relative to given schema, or errors paired
    with paths to identify which parts of corpus are invalid."""
    corpus = [path for path in corpus_dir.iterdir() if path.is_file() and path.suffix.lower() == ".xml"]
    val_results = []
    for path in corpus:
        isvalid, errors = eltec_validate_file(path.absolute())
        if not isvalid:
            val_results.append((path, errors))
    return val_results

# Web (and archive) generation
# ----------------------------
def zip_corpus():
    """Making a zip archive containing all corpus xmls."""
    xml_paths = [path for path in corpus_dir.iterdir() if path.is_file() and path.suffix.lower() == ".xml"]

    with zipfile.ZipFile(f"{corpus_dir.absolute()}/dispro.zip", "w") as archive:
        for path in xml_paths:
            archive.write(path, arcname=path.name)

def regenerate_web():
    """Generating index.html presenting the eltec files in corpus"""

    # Site generation is allowed only if the corpus is valid
    val_results = eltec_validate_corpus()
    if val_results != []:
        print("Invalid files found within the corpus! Resolve following errors before generating the site. \n")
        for path, errors in val_results:
            print(f"Errors in '{path.name}':")
            print(f"{errors}\n\n")
        return

    # Set-up needed for jinja templating.
    env = Environment(
        loader=PackageLoader("dispro"),
        autoescape=select_autoescape()
    )
    template = env.get_template("index.html")

    xml_paths = [path for path in corpus_dir.iterdir() if path.is_file() and path.suffix.lower() == ".xml"]
    headers = [get_header_data(path) for path in xml_paths] # parsing the headers

    # Creating dictionary that associate authors with the titles they have
    # written
    corpus = {}
    for header in headers:
        if header["author_ref"] not in corpus:
            corpus[header["author_ref"]] = [ header ]
        else:
            corpus[header["author_ref"]].append(header)

    # Creating dictionary that associate letters with authors (through their
    # last names initials)
    index = {}
    for ref in corpus.keys():
        initial = corpus[ref][0]["author"][0].lower()
        if initial not in index:
            index[initial] = [ (ref, " ".join(corpus[ref][0]["author"].split(" ")[0:2])) ]
        else:
            index[initial].append((ref, " ".join(corpus[ref][0]["author"].split(" ")[0:2])))

    # Generate index.html
    with open(f"{project_dir.absolute()}/index.html", "w") as index_file:
        index_file.write(template.render(corpus=corpus,
                                   index=index,
                                   title_count=len(headers),
                                   author_count=len(corpus.keys())))

    zip_corpus() # create corpus archive

    print("Website (and archive) was successfully regenerated.")

def main():
    # Command-line interface
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")] # Reading command-line options
    arguments = [arg for arg in sys.argv[1:] if not arg.startswith("-") ] # Reading command-line arguments

    if "-v" in options: # 'v' option is used for invoking ELTeC validation
        if len(arguments) > 0: # individual file validation
            isvalid, errors = eltec_validate_file(arguments[0])
            if isvalid:
                print(f"File '{arguments[0]}' is valid relative to eltec-1 scheme.")
            else:
                print(f"File '{arguments[0]}' is invalid relative to eltec-1 scheme:")
                print(errors)
        else: # corpus validation
            print("Validating whole corpus ...")
            val_results = eltec_validate_corpus()
            if val_results == []:
                print("All files in corpus are valid.")
            else:
                print("Invalid files found within the corpus!\n")
                for path, errors in val_results:
                    print(f"Errors in '{path.name}':")
                    print(f"{errors}\n\n")
    elif "-w" in options: # option used for generating index file
        regenerate_web()
    elif "-wl" in options: # option used for serving (and livereloading) index on localhost
        # Initial web regeneration
        regenerate_web()

        # Initialising the livereload class
        server = Server()

        # Regenerate the index, if changes are made to its template
        server.watch(templates_dir.joinpath("index.html").absolute(), regenerate_web)
        server.serve(root=project_dir.absolute())
    elif "-e" in options: # option used to generate eltec files
        if len(arguments) < 1:
            print("You need to provide a path at which to create the eltec file.")
        elif len(arguments) < 2:
            generate_eltec_file(arguments[0])
        else:
            generate_eltec_file(arguments[0], header_data_file=arguments[1])
    elif "-efi" in options: # option used to generate eltec files from images
        if len(arguments) < 1:
            print("You need to provide a header data file.")
        elif len(arguments) < 2: # Only header data file given
            text = get_eltec_body_from_images(Path.cwd().absolute())
            if not text:
                return
            generate_eltec_file(text=text, header_data_file=arguments[0])
        else: # Header data file and output path given
            text = get_eltec_body_from_images(Path.cwd().absolute())
            if not text:
                return
            generate_eltec_file(path=arguments[0],
                                text=text,
                                header_data_file=arguments[1])
    else:
        pass

if __name__ == "__main__":
    main()
