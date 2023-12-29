# Collections of functions used to generate, validate and present the corpus

import os, sys
import zipfile, json, random

from datetime import date
from pathlib import Path
from lxml import etree

from jinja2 import Environment, PackageLoader, select_autoescape

project_dir = Path(__file__).absolute().parents[1]
schemas_dir = project_dir.joinpath("schemas")
corpus_dir = project_dir.joinpath("data/ELTEC_FILES")
templates_dir = project_dir.joinpath("scripts/templates")

# Functions used to generate ELTeC XMLs
# -------------------------------------
def generate_eltec_file(path, text="<p></p>", header_data_file=f"{templates_dir}/eltec_header_data.json"):
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
    today = date.today()
    xslt_params["creation_date"] = f"'{today.year}-{today.month}-{today.day}'"

    breakpoint()

    # applying the schema to a dummy xml object
    eltec_file = schema(etree.XML(f"<body xmlns='http://www.tei-c.org/ns/1.0'>{text}</body>"), **xslt_params)

    if not path:
        # Generating file name if none was given
        path = Path(f"{header_data['title']}__{header_data['author_last_name']}.xml")
    else:
        path = Path(path)

    # Determining the mode of operation (re)write / update / cancel
    if path.exists():
        mode = input(f"\nThe file '{path}' already exists. Enter 'w' for rewrite, 'u' for update, or anything else to cancel the operation: ")
        if mode == "w": # Rewriting
            # writing the result of transformation to the file at path
            print(f"\nRewriting {path.name} ...")
            eltec_file.write(path, encoding='utf-8', pretty_print=True)
        elif mode == "u": # Updating
            # TODO: Code for updating the ELTeC file
            print("\nUpdate not implemented yet.")
        else: # Cancelling
            print("\nCancelling the operation.")
            return
    else: # Creating
        print(f"\nCreating {path.name} ...")
        eltec_file.write(path, encoding='utf-8', pretty_print=True)

    # Validating the file
    is_valid, errors = eltec_validate_file(path.absolute())
    if not is_valid:
        print(f"\nThe file '{path}' is invalid relative to the eltec-1 schema:\n")
        print(errors)
    else:
        print(f"\nThe file '{path}' is valid relative to the eltec-1 schema.\n")


# Functions used to validate xml-s against ELTeC schemas
# -----------------------------------------------------

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

def get_header_data(path):
    """Extracting data from eltec headers to be used in web site generation."""
    xml = etree.parse(path)
    author = xml.xpath("//tei:titleStmt/tei:author/text()",
                       namespaces={
                           "tei": "http://www.tei-c.org/ns/1.0"
                       })
    author_ref = xml.xpath("//tei:titleStmt/tei:author/@ref",
                       namespaces={
                           "tei": "http://www.tei-c.org/ns/1.0"
                       })
    title = xml.xpath("//tei:titleStmt/tei:title/text()",
                       namespaces={
                           "tei": "http://www.tei-c.org/ns/1.0"
                       })
    print_source_title = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:title/text()",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0"
                       })
    print_source_ref = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:title/@ref",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0"
                       })
    print_source_publisher = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:publisher/text()",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0"
                       })
    print_source_pub_place = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:pubPlace/text()",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0"
                       })
    print_source_pub_date = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:date/text()",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0"
                       })
    time_slot = xml.xpath("//eltec:timeSlot/@key",
                              namespaces={
                                  "tei": "http://www.tei-c.org/ns/1.0",
                                  "eltec": "http://distantreading.net/eltec/ns"
                              })
    return {
        "author": author[0],
        "author_ref": author_ref[0] if len(author_ref) > 0 else "",
        "title": title[0],
        "src_title": print_source_title[0],
        "src_ref": print_source_ref[0],
        "src_publisher": print_source_publisher[0],
        "src_pub_place": print_source_pub_place[0],
        "src_pub_date": print_source_pub_date[0],
        "time_slot": time_slot[0],
        "path": f"./data/ELTEC_FILES/{path.name}"
    }

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
    elif "-e" in options: # option used to generate eltec files
        if len(arguments) < 1:
            print("You need to provide a path at which to create the eltec file.")
        else:
            generate_eltec_file(arguments[0])
    else:
        pass

if __name__ == "__main__":
    main()
