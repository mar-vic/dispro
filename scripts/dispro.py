# Collections of scripts used to generate, validate and present the corpus

import os, sys

from pathlib import Path
from lxml import etree

project_dir = Path(__file__).parents[1]
schemes_dir = project_dir.joinpath("schemas")
corpus_dir = project_dir.joinpath("data/ELTEC_FILES")

# Functions used to validate xml-s against ELTeC schemas
# -----------------------------------------------------

def eltec_validate_file(xml_path, scheme_path=schemes_dir.joinpath("eltec-1.rng").absolute()):
    """Validate individual xml file against (eltec-1) schema."""
    xml = etree.parse(xml_path) # reading the xml to validate

    # Lading schema definition
    rng = etree.parse(scheme_path)
    rng = etree.RelaxNG(rng)

    # Validating the document
    if rng.validate(xml):
        return (True, None)
    else:
        # Providing error log, when the document is invalid
        return (False, rng.error_log)

def eltec_validate_corpus(scheme_path=schemes_dir.joinpath("eltec-1.rng").absolute()):
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

def main():
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")] # Reading command-line options
    arguments = [arg for arg in sys.argv[1:] if not arg.startswith("-") ] # Reading command-line arguments

    if "-v" in options: # ELTeC validation
        if len(arguments) == 0: # corpus validation
            print("Validating whole corpus ...")
            val_results = eltec_validate_corpus()
            if val_results == []:
                print("All files in corpus are valid.")
            else:
                print("Invalid files found within the corpus!\n")
                for path, errors in val_results:
                    print(f"Errors in '{path.name}':")
                    print(f"{errors}\n\n")
            breakpoint()
            exit()
        else: # individual file validation
            isvalid, errors = eltec_validate_file(arguments[0])
            if isvalid:
                print(f"File '{arguments[0]}' is valid relative to eltec-1 scheme.")
            else:
                print(f"File '{arguments[0]}' is invalid relative to eltec-1 scheme:")
                print(errors)

if __name__ == "__main__":
    main()
