# Collections of functions used to generate, validate and present the corpus

import os, sys
import zipfile, json, random, string
from bs4.dammit import encoding_res

import pytesseract
import unidecode
import requests

from datetime import date
from pathlib import Path
from lxml import etree
from PIL import Image
from livereload import Server
from bs4 import BeautifulSoup
from functools import reduce

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

    header_data["path"] = f"data/ELTEC_FILES/{Path(path).name}"

    # Author and title name
    author = xml.xpath("//tei:titleStmt/tei:author/text()",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["author"] = author[0] if len(author) > 0 else ""

    author_ref = xml.xpath("//tei:titleStmt/tei:author/@ref",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["author_ref"] = author_ref[0] if len(author_ref) > 0 else "viaf:00000"

    title = xml.xpath("//tei:titleStmt/tei:title/text()",
                       namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["title"] = title[0] if len(title) > 0 else ""

    # Info about source edition
    print_source_ref = xml.xpath("//tei:sourceDesc/tei:bibl[@type='printSource']/tei:title/text()",
                              namespaces={ "tei": "http://www.tei-c.org/ns/1.0" })
    header_data["srced_title"] = print_source_ref[0] if len(print_source_ref) > 0 else ""

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

    # breakpoint()

    return header_data

def generate_eltec_file(path=None, text=None, header_data_file=f"{templates_dir}/eltec_header_data.json"):
    """
    Writes an xml file valid relative to the eltec-1 scheme. The XML is
    generated via parametrized xslt schema. Can be given header data file and /
    or 'text' to be used within ELTeC '<teiHeader>' and '<body>' tags
    respectivelly.
    """
    schema = etree.XSLT(etree.parse(f"{schemas_dir}/eltec.xsl")) # Loading the schema

    # Unloading the ELTeC header data from json into dictionary
    with open(header_data_file, "r", encoding="utf-8") as f:
        header_data = json.load(f)

    # values need to be quoted in order to be processed by xslt
    xslt_params = {k:f"'{v}'" for (k,v) in zip(header_data["xslt_params"].keys(), header_data["xslt_params"].values())}

    # Wordcount from text, if provided
    if text:
        text_soup = BeautifulSoup(text, "xml")
        word_count = len(text_soup.get_text().split())
        xslt_params["words"] = f"'{str(word_count)}'"

    # constructing the value of <author> eltec tag and adding it to the xslt parameters
    author = f"{header_data['author_last_name']}, {header_data['author_first_name']}"
    author += f" [{header_data['author_alter_name']}]" if header_data["author_alter_name"] != "" else "" # In case autho has alter name
    author += f" ({header_data['author_birth_date']}-{header_data['author_death_date']})"
    xslt_params["author"] = f"'{author}'"

    # Constructing the random part of id (rest of the id is generated from lang and pub_date in xslt)
    xslt_params["id"] = str(random.randint(0, 1000))

    # Constructing creation date
    xslt_params["creation_date"] = f"'{str(date.today().isoformat())}'"

    # Generating file name if none was given
    if not path:
        path = Path(unidecode.unidecode(f"{header_data['xslt_params']['title'].lower().replace(' ','_')}__{header_data['author_last_name'].lower()}.xml"))
    else:
        path = Path(path)

    # (re)writing eltec file or cancelling the operation
    if path.exists():
        mode = input(f"\nThe file '{path}' already exists. Enter 'w' for rewrite, or anything else to cancel the operation: ")
        if mode == "w": # Rewriting
            print(f"\nRewriting {path.name} ...")

            eltec_file = schema(etree.XML("<body xmlns='http://www.tei-c.org/ns/1.0'><p></p></body>"), **xslt_params)
            eltec_file.write(path, encoding="utf-8", pretty_print=True)

            #  Reload the eltec file with soup and combine it with extracted contents.
            #  We are doing this in two steps, because it is easier to debug existing 
            #  invalid xml file, than deal just with xslt errors.
            with open(path, "r", encoding="utf-8") as f:
                eltec_soup = BeautifulSoup(f.read(), "xml")
                # Clearing superfluous elements added by BS
                # eltec_soup.html.unwrap()
                # eltec_soup.body.unwrap()

                # breakpoint()
                
                body_soup = BeautifulSoup(f"<div>{text}</div>", "xml")
                body_soup.div.unwrap()

                eltec_soup.find("text").p.decompose()
                eltec_soup.find("tei:body").decompose()
                eltec_soup.find("text").append(body_soup)

            with open(path, "w", encoding="utf-8") as f:
                f.write(eltec_soup.prettify())

            update_word_count(path, encoding="utf-8")
        else: # Cancelling
            print("\nCancelling the operation.")
            return
    else: # Creating
        print(f"\nCreating {path.name} ...")
        eltec_file = schema(etree.XML("<body xmlns='http://www.tei-c.org/ns/1.0'><p></p></body>"), **xslt_params)
        eltec_file.write(path, encoding="utf-8", pretty_print=True)

        #  Reload the eltec file with soup and combine it with extracted contents.
        #  We are doing this in two steps, because it is easier to debug existing 
        #  invalid xml file, than deal just with xslt errors.
        with open(path, "r", encoding="utf-8") as f:
            eltec_soup = BeautifulSoup(f.read(), "xml")
            body_soup = BeautifulSoup(text, "xml")

            body_soup = BeautifulSoup(f"<div>{text}</div>", "xml")
            body_soup.div.unwrap()

            # Clean-up
            eltec_soup.find("text").p.decompose()
            eltec_soup.find("tei:body").decompose()

            # Adding the contents
            eltec_soup.find("text").append(body_soup)

        with open(path, "w", encoding="utf-8") as f:
            f.write(eltec_soup.prettify())

        update_word_count(path, encoding="utf-8")

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
    Generating a valid xml fragment pluggable into eltec-1 <body> out of set
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

    # breakpoint()

    # Clean-up
    text = text.replace("", "<pb></pb>") # The '' character represents a page break

    # Paired square brackets are interpreted in XML as encompassing PCDATA
    text = text.replace("[", "(").replace("]", ")").strip("<")


    # getting list paragraphs and removing whitespace characters
    text = [paragraph.strip(string.whitespace) for paragraph in text.split("\n\n")]

    # removing empty paragraphs
    text = [f"<p>{paragraph}</p>" for paragraph in text if len(paragraph) != paragraph.count(" ")]

    # breakpoint()

    # collating into string
    text = "".join(text)

    # Dumping raw text into file for debuggig purposes
    file = open("unvalidated_body.txt", "w")
    file.write(text)
    file.close()

    return "".join(text)

def get_eltec_body_from_raw_text(raw_text):
    text = text.replace("", "<pb></pb>") # The '' character represents a page break

    # Paired square brackets are interpreted in XML as encompassing PCDATA
    text = text.replace("[", "(").replace("]", ")")

    # getting list paragraphs and removing whitespace characters
    text = [paragraph.strip(string.whitespace) for paragraph in text.split("\n\n")]

    # tagging and removing empty paragraphs
    text = [f"<p>{paragraph}</p>" for paragraph in text if len(paragraph) != paragraph.count(" ")]

    return "".join(text)

def get_eltec_body_from_pdf(path_to_pdf, images=True):
    """
    Generating a valid xml fragment pluggable into eltec-1 <body> out of pdf.
    """
    # breakpoint()
    path_to_pdf = Path(path_to_pdf).absolute()
    if not path_to_pdf.is_file():
        print(f"'{path_to_pdf.name}' is not a file.")
        return
    working_dir = path_to_pdf.parent.absolute()
    if images:
        # Generating images put of pages of pdf
        print(f"Converting pdf to images with pdftoppm ...")
        os.system(f"pdftoppm -png {path_to_pdf} {working_dir}/") # generates images
        return get_eltec_body_from_images(working_dir)

def get_eltec_body_from_zf_html(path_to_html):
    """
    GETs the file from url and transform it into valid eltec body.
    Structure of 'Zlaty Fond SME' is assumed.
    """
    # Dealing with possible encoding mismatch.
    try:
        with open(Path(path_to_html).absolute(), "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    except UnicodeDecodeError:
        with open(Path(path_to_html).absolute(), "r", encoding="cp1252", errors="ignore") as f:
            print("Encoding from cp1252 into UTF-8 \n")
            # utf8_encoded_text = f.read().encode("latin-1", "replace").decode("cp1252").encode("UTF-8")
            # breakpoint()
            soup = BeautifulSoup(f.read(), "html.parser")

    # Removing superfluous elements
    if soup.head:
        soup.head.decompose()

    if soup.find("div", id="hlavicka"):
        soup.find("div", id="hlavicka").decompose()

    if soup.find("div", class_="titlepage"):
        soup.find("div", class_="titlepage").decompose()

    if soup.find("div", class_="toc"):
        soup.find("div", class_="toc").decompose()

    if soup.find("div", class_="bibliography"):
        soup.find("div", class_="bibliography").decompose()

    if soup.find("div", id="spodok"):
        soup.find("div", id="spodok").decompose()

    if soup.body:
        soup.body.attrs = { "xmlns":"http://www.tei-c.org/ns/1.0" }

    if soup.find("div", class_="book"):
        soup.find("div", class_="book").unwrap()
    
    # breakpoint()
    # All chapters are within divs divs witch 'chapter' classes
    chapters = soup.find_all("div", class_="chapter")

    for chapter in chapters:
        # Extract chapter name and remove <titlepage>
        titlepage = chapter.find("div", class_="titlepage")
        title = titlepage.h2.contents[1]
        titlepage.decompose()
    
        # Replace literal layouts with <l></l> tags
        # breakpoint()
        literal_layouts = chapter.find_all("div", class_="literallayout")
        # breakpoint()
        for layout in literal_layouts:
            lines = layout.text.replace("\xa0", u" ").split("\n")
            lss = [BeautifulSoup(f"<l>{line}</l>", features="lxml").l for line in lines]
            layout.replace_with(lss[0])
            inserted = lss[0]
            for ls in lss[1:]:
                inserted.insert_after(ls)
                inserted = ls
        
        # Transform footnotes refs
        footnote_refs = chapter.find_all("a")
        for ref in footnote_refs:
            ref_target = ref.attrs["href"].strip("#")
            ref.parent.replace_with(soup.new_tag("ref", target=ref_target))
        
        # breakpoint()
        # Create eltec container for chapters, if there is more than one
        if len(chapters) > 1:
            chapter.wrap(soup.new_tag("div", type="chapter"))
            chapter_head = soup.new_tag("head")
            chapter_head.extend([title])
            chapter.insert(0, chapter_head)
        chapter.unwrap()

    # Transform footnotes
    footnotes_divs = soup.find_all("div", class_="footnotes")
    if len(footnotes_divs) > 0:
        eltec_notes = soup.new_tag("div", type="notes")
        for div in footnotes_divs:
            for footnote in div.find_all("div", class_="footnote"):
                eltec_note = soup.new_tag("note")
                eltec_note["xml:id"] = footnote.ref.attrs["target"]
                footnote.ref.decompose()
                contents_wo_tags = "".join([s.strip("\n") for s in footnote.strings])
                eltec_note.append(contents_wo_tags)
                eltec_notes.append(eltec_note)
            div.decompose()

        soup.html.append(eltec_notes)
        back = soup.new_tag("back")
        back.attrs["xmlns"] = "http://www.tei-c.org/ns/1.0"
        eltec_notes.wrap(back)
    # breakpoint()
    soup.html.wrap(soup.new_tag("text"))
    soup.html.unwrap()

    # Transform blockquotes
    bquote_divs = soup.find_all("div", class_="blockquote")
    for div in bquote_divs:
        contents_wo_tags = "".join([s.strip("\n") for s in div.strings])
        eltec_quote = soup.new_tag("quote")
        eltec_quote.append(contents_wo_tags)
        div.parent.replace_with(eltec_quote)

    # Transforming bold spans
    bold_spans = soup.find_all("span", class_="bold")
    for span in bold_spans:
        contents_wo_tags = "".join([s.strip("\n") for s in span.strings])
        eltec_emph = soup.new_tag("emph")
        eltec_emph.append(contents_wo_tags)
        span.replace_with(eltec_emph)

    # Transform remaining emphases
    emphs = soup.find_all("span", class_="emphasis")
    for emph in emphs:
        eltec_emph = soup.new_tag("emph")
        eltec_emph.append("".join(s for s in emph.strings))
        emph.replace_with(eltec_emph)

    # Finally, remove parent tags
    soup.find("text").unwrap()
    # with open("debug.html", "w") as nf:
        # nf.write(soup.prettify()) # for debugging
    return soup.prettify()

# Functions for XML validation against ELTeC schemas
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

    # breakpoint()

    # Creating dictionary that associate authors with the titles they have
    # written
    corpus = {}
    for header in headers:
        if header["author_ref"] not in corpus:
            corpus[header["author_ref"]] = [ header ]
        else:
            corpus[header["author_ref"]].append(header)

    # breakpoint()

    # Creating dictionary that associate letters with authors (through their
    # last names initials)
    index = {}
    for ref in corpus.keys():
        initial = corpus[ref][0]["author"].strip()[0].lower()
        if initial not in index:
            index[initial] = [ (ref, " ".join(corpus[ref][0]["author"].strip().split(" ")[0:2])) ]
        else:
            index[initial].append((ref, " ".join(corpus[ref][0]["author"].strip().split(" ")[0:2])))

    # Generate index.html
    with open(f"{project_dir.absolute()}/index.html", "w") as index_file:
        index_file.write(template.render(corpus=corpus,
                                   index=index,
                                   title_count=len(headers),
                                   author_count=len(corpus.keys())))

    zip_corpus() # create corpus archive

    # Recompiling tailwind css
    tailwindcli_path = project_dir.joinpath('tailwindcss').absolute()
    tailwindsrc_path = project_dir.joinpath('static/css/tw_source.css').absolute()
    compiledcss_path = project_dir.joinpath('static/css/global.css').absolute()
    os.system(f"{tailwindcli_path} -i {tailwindsrc_path} -o {compiledcss_path}")

    print("Website (and archive) was successfully regenerated.")

# Just some quick and dirty helper functions
def get_all_eltecs():
    eltec_dir = project_dir.joinpath("data/ELTEC_FILES")
    return [title for title in eltec_dir.iterdir() if title.is_file() if title.suffix == ".xml"]

def get_stats():
    data_dir = project_dir.joinpath("data")
    eltec_dir = data_dir.joinpath("ELTEC_FILES")

    raw = [[title for title in item.iterdir()] for item in data_dir.iterdir() if item.is_dir()]
    print(f"No. of unprocessed authors: {len(raw)}")
    raw = reduce(lambda x, y: x + y, raw)
    print(f"No. of unprocessed titles: {len(raw)}")

    eltecs = [title for title in eltec_dir.iterdir() if title.is_file()]
    total_cc = 0
    total_wc = 0
    for title in eltecs:
        with open(title, "r", encoding="utf-8") as f:
            try:
                eltec_soup = BeautifulSoup(f.read(), "xml")
                total_cc += len(eltec_soup.find("text").get_text())
                total_wc += len(eltec_soup.find("text").get_text().split())
                author = eltec_soup.author
                breakpoint()
            except UnicodeDecodeError:
                print(f"UnicodedecodeError at file {title}")
    print(f"Total character count processed: {total_cc}")
    print(f"Total word count processed: {total_wc}")
    print(f"No. of processed titles: {len(eltecs) - 1}")

def get_authors_without_ref():
    eltec_dir = project_dir.joinpath("data/ELTEC_FILES")
    eltecs = [title for title in eltec_dir.iterdir() if title.is_file() if title.name != "dispro.zip"]
    for title in eltecs:
        with open(title, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "xml")
            if not reduce(lambda x, y: x and "ref" in y.attrs.keys(), soup.find_all("author"), True):
                print(title)

def get_word_counts():
    for title in get_all_eltecs():
        with open(title, "r") as f:
            soup = BeautifulSoup(f.read(), "xml")
            word_count = soup.find("measure", unit="words").get_text()
            print(f"{title.stem}: {word_count} words".strip("\n"))

def update_word_count(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as f:
        # breakpoint()
        soup = BeautifulSoup(f.read(), "xml")

        # Making the calucations
        word_count = len(soup.find("text").get_text().split())
        size = "short" if word_count < 50000 else "medium" if word_count < 100000 else "long"

        # Updating the "words" in <measure>
        words_measure_tag = soup.find("measure", unit="words")
        words_measure_tag.replace_with(soup.new_tag("measure", unit="words"))
        soup.find("measure", unit="words").insert(0, str(word_count))

        # Updating the <size>
        size_tag = soup.find("eltec:size")
        if size_tag:
            size_tag.attrs["key"] = size
        else:
            soup.textDesc.insert(1, soup.new_tag("eltec:size", key=size))

    with open(path, "w", encoding=encoding) as f:
        f.write(soup.prettify())


def update_word_counts():
    for title in get_all_eltecs():
        with open(title, "r") as f:
            # breakpoint()
            soup = BeautifulSoup(f.read(), "xml")
            word_count = str(len(soup.find("text").get_text().split()))
            words_measure_tag = soup.find("measure", unit="words")
            words_measure_tag.replace_with(soup.new_tag("measure", unit="words"))
            soup.find("measure", unit="words").insert(0, word_count)

        with open(title, "w") as f:
            f.write(soup.prettify())

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

        # Regenerate the index, if changes are made to its template, corpus, or tailwind source
        twsource_path = project_dir.joinpath("static/css/tw_source.css").absolute()
        server.watch(templates_dir.joinpath("index.html").absolute(), regenerate_web)
        server.watch(twsource_path, regenerate_web)

        # Serving the index at project root
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
    elif "-efp" in options: # options used to generate eltec from pdf

        # breakpoint()

        images = input("Does the pdf conain scans of the original? (y/n)")
        images = True if images == "y" or images == "" else False

        if len(arguments) < 1:
            print("You need to provide a path to pdf file.")
        elif len(arguments) < 2:
            print("You need ot providfe a path to header data file")
        else:
            text = get_eltec_body_from_pdf(arguments[0], images)
            if not text:
                return
            generate_eltec_file(text=text,
                                header_data_file=arguments[1])
    elif "-efh" in options: # option used to generate eltec from HTML

        if len(arguments) < 1:
            print("You need to provide a path to a HTML file.")
        elif len(arguments) < 2:
            print("You need to provide a path to header data file.")
        else:
            text = get_eltec_body_from_zf_html(arguments[0])
            if not text:
                print("Something went wrong as no text was generated.")
                return
            generate_eltec_file(text=text, header_data_file=arguments[1])
    else:
        # get_stats()
        # get_authors_without_ref()
        # update_word_counts()
        # get_word_counts()
        eltec_validate_corpus()

if __name__ == "__main__":
    main()
