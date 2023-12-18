import os
from pathlib import Path
from lxml import etree

from jinja2 import Environment, PackageLoader, select_autoescape

def get_header_data(path):
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
    # print(author_ref)
    # breakpoint()
    return {
        "author": author[0],
        "author_ref": author_ref[0],
        "title": title[0],
        "src_title": print_source_title[0],
        "src_ref": print_source_ref[0],
        "src_publisher": print_source_publisher[0],
        "src_pub_place": print_source_pub_place[0],
        "src_pub_date": print_source_pub_date[0],
        "time_slot": time_slot[0],
        "path": path
    }

def main():
    env = Environment(
        loader=PackageLoader("disproweb"),
        autoescape=select_autoescape()
    )

    template = env.get_template("index_eltec.html")
    corpus_dir = Path("../data/ELTEC_FILES/")
    xml_paths = [path for path in corpus_dir.iterdir() if path.is_file() and path.suffix == ".xml"]
    headers = [get_header_data(path) for path in xml_paths]


    corpus = {}
    for header in headers:
        if header["author_ref"] not in corpus:
            corpus[header["author_ref"]] = [ header ]
        else:
            corpus[header["author_ref"]].append(header)

    index = {}
    for ref in corpus.keys():
        initial = corpus[ref][0]["author"][0]
        if initial not in index:
            index[initial.lower()] = [ (ref, " ".join(corpus[ref][0]["author"].split(" ")[0:2])) ]
        else:
            index[initial.lower()].append((ref, " ".join(corpus[ref][0]["author"].split(" ")[0:2])))

    with open("../index.html", "w") as f:
        f.write(template.render(corpus=corpus,
                                index=index,
                                title_count=len(headers),
                                author_count=len(corpus.keys()),
                                alphabet="aábcčdďeéfghiíjklľmnňoóôpqrsštťuúvwxyýzž"))

    # breakpoint()

if __name__ == "__main__":
    main()



# corpus = []
# index = {}
# total_title_count = 0
# for author in authors:
#     titles = [(title,
#                [f"./data/{author}/{title}/{title_version}" for title_version in os.listdir(f"{data_root}{author}/{title}/")])
#               for title in os.listdir(data_root + author + "/") if os.path.isdir(f"{data_root}{author}/{title}/")]

#     corpus.append((author, titles))

#     # Creating index
#     author_names = list(reversed(author.split()))
#     author_key = author_names[0][0].lower()
#     if author_key in index:
#         index[author_key].append((f"{author_names[0]}, {' '.join(author_names[1:])}", len(titles), author.lower().replace(" ", "-")))
#     else:
#         index[author_key] = [(f"{author_names[0]}, {' '.join(author_names[1:])}", len(titles), author.lower().replace(" ", "-"))]

#     total_title_count += len(titles)

# with open("../index.html", "w") as f:
#     f.write(template.render(corpus=corpus,
#                             title_count = total_title_count,
#                             author_count=len(authors),
#                             index=index,
#                             alphabet="aábcčdďeéfghiíjklľmnňoóôpqrsštťuúvwxyýzž"))
